"""
app/services/contracts.py — Forward contract advisor and contract integrity service.

Contract advice delegates to the TradeShield ML service
(ML/app/api/routes/advice.py) which produces a transparent rule-based
LOCK_NOW / WAIT hedging decision backed by the trained quantile model.

Contract integrity verification is a local SHA-256 hash comparison
(no ML required).
"""

from __future__ import annotations

import hashlib
import logging
import math
from typing import Any

from app.services.ml_client import get_ml_advice

logger = logging.getLogger(__name__)


# ── Forward Contract Advisor ──────────────────────────────────────────────────

def get_contract_advice(
    currency_pair: str,
    amount: float,
    current_rate: float,
    offered_forward_rate: float,
    payment_days: int,
) -> dict[str, Any]:
    """Generate a hedge recommendation by calling the ML advice endpoint.

    The ML service's Advisor evaluates:
    - expected_gain = median forecast vs current forward-adjusted rate
    - downside_risk = distance from current rate to 5th/95th quantile
    - Returns LOCK_NOW if no reliable model edge, else WAIT with a range

    Parameters
    ----------
    currency_pair:
        E.g. "USD/INR". Only USDINR is modelled; others get a rule-based fallback.
    amount:
        Trade exposure in USD.
    current_rate:
        Spot rate at request time (informational; ML uses its own live tick).
    offered_forward_rate:
        Forward rate offered by the bank (used for local spread commentary).
    payment_days:
        Business days until payment / settlement (mapped to forecast horizon, max 15).

    Returns
    -------
    dict with keys:
        currency_pair, amount_usd, decision (LOCK_NOW|WAIT), reason,
        reasoning {...}, offered_forward_rate, forward_spread_comment, source
    On ML service failure:
        feature, status="ml_unavailable", error, ...
    """
    normalised = currency_pair.replace("/", "").upper()

    # Map payment_days → ML horizon (capped at 15 business days)
    horizon = min(max(1, payment_days), 15)

    # Determine trade direction from caller context
    # Backend callers can pass role via currency_pair prefix convention "EXPORT:USD/INR"
    # or we default to "exporter" as the most common MSME use-case
    direction = "exporter"
    if ":" in currency_pair:
        role_prefix, currency_pair = currency_pair.split(":", 1)
        direction = "importer" if role_prefix.strip().lower() == "import" else "exporter"
        normalised = currency_pair.replace("/", "").upper()

    if normalised != "USDINR":
        return _rule_based_advice(
            currency_pair, amount, current_rate, offered_forward_rate, payment_days
        )

    try:
        ml_result = get_ml_advice(
            direction=direction,
            amount_usd=amount,
            horizon=horizon,
        )
        logger.info(
            "ML advice: decision=%s, direction=%s, amount_usd=%s, horizon=%s",
            ml_result.get("decision"),
            direction,
            amount,
            horizon,
        )

        # Compute a local forward spread commentary
        spread_comment = _forward_spread_comment(
            offered_forward_rate, current_rate, payment_days
        )

        return {
            "currency_pair": currency_pair,
            "amount_usd": amount,
            "direction": direction,
            "horizon_days": horizon,
            "decision": ml_result.get("decision"),
            "reason": ml_result.get("reason"),
            "reasoning": ml_result.get("reasoning", {}),
            "offered_forward_rate": offered_forward_rate,
            "forward_spread_comment": spread_comment,
            "source": "tradeshield_ml",
        }

    except RuntimeError as exc:
        logger.error("ML service unavailable for contract advice: %s", exc)
        return {
            "feature": "forward_contract_advisor",
            "status": "ml_unavailable",
            "currency_pair": currency_pair,
            "amount": amount,
            "current_rate": current_rate,
            "offered_forward_rate": offered_forward_rate,
            "payment_days": payment_days,
            "error": str(exc),
            "message": (
                "The ML advice service is currently unavailable. "
                "Start with: cd ML && uvicorn app.api.main:app --port 9000"
            ),
        }


def _forward_spread_comment(
    offered: float, spot: float, days: int
) -> str:
    """Local commentary on how the offered forward rate compares to spot."""
    if spot <= 0:
        return "Spot rate unavailable for spread calculation."
    annualised_premium_pct = ((offered - spot) / spot) * (365.0 / max(days, 1)) * 100
    direction = "premium" if offered >= spot else "discount"
    return (
        f"Offered forward rate of {offered:.4f} implies a "
        f"{abs(annualised_premium_pct):.2f}% annualised {direction} over spot ({spot:.4f})."
    )


def _rule_based_advice(
    currency_pair: str,
    amount: float,
    current_rate: float,
    offered_forward_rate: float,
    payment_days: int,
) -> dict[str, Any]:
    """Simple rule-based fallback for non-USDINR pairs."""
    spread = offered_forward_rate - current_rate
    decision = "LOCK_NOW" if spread >= 0 else "WAIT"
    return {
        "currency_pair": currency_pair,
        "amount": amount,
        "decision": decision,
        "reason": (
            f"Rule-based (ML model only covers USDINR): "
            f"offered forward {offered_forward_rate:.4f} vs spot {current_rate:.4f}."
        ),
        "source": "rule_based_fallback",
    }


# ── Contract Integrity ────────────────────────────────────────────────────────

def verify_contract_integrity(
    contract_id: str,
    contract_terms: str,
    expected_hash: str | None = None,
) -> dict[str, Any]:
    """SHA-256 hash the contract terms and compare against the expected hash.

    No ML required — this is a deterministic cryptographic check.

    Parameters
    ----------
    contract_id:
        Unique identifier for the contract (for audit purposes).
    contract_terms:
        Full text / JSON string of the contract to be hashed.
    expected_hash:
        Previously stored SHA-256 hex digest to compare against.
        If None, only the computed hash is returned (registration mode).

    Returns
    -------
    dict with:
        contract_id, computed_hash, algorithm="SHA-256",
        integrity_status ("VERIFIED" | "TAMPER_DETECTED" | "HASH_REGISTERED"),
        match (bool | None)
    """
    computed = hashlib.sha256(contract_terms.encode("utf-8")).hexdigest()

    if expected_hash is None:
        return {
            "contract_id": contract_id,
            "computed_hash": computed,
            "algorithm": "SHA-256",
            "integrity_status": "HASH_REGISTERED",
            "match": None,
            "message": "No expected hash provided. Store this hash for future verification.",
        }

    match = computed == expected_hash.strip().lower()
    return {
        "contract_id": contract_id,
        "computed_hash": computed,
        "expected_hash": expected_hash,
        "algorithm": "SHA-256",
        "integrity_status": "VERIFIED" if match else "TAMPER_DETECTED",
        "match": match,
        "message": (
            "Contract integrity confirmed. Hashes match."
            if match
            else "WARNING: Contract tampering detected. Computed hash does not match expected hash."
        ),
    }
