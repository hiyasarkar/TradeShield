"""
app/services/ml_client.py — Thin async HTTP client for the TradeShield ML service.

The ML service (ML/app/api/main.py) runs as a separate FastAPI process, typically
on port 9000. This module provides helper functions that the backend services call
to delegate forecast and advice decisions to the trained model.

Environment variable:
    ML_SERVICE_URL  — base URL of the ML service (default: http://localhost:9000)
"""

from __future__ import annotations

import logging
import os
from typing import Any

import urllib.request
import urllib.error
import json

logger = logging.getLogger(__name__)

ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL", "http://localhost:9000").rstrip("/")

_TIMEOUT_SECONDS = 10


def _get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Synchronous GET helper (avoids adding httpx/aiohttp as a hard dependency).

    Returns the parsed JSON response dict, or raises RuntimeError on failure.
    """
    query = ""
    if params:
        parts = []
        for k, v in params.items():
            if v is not None:
                parts.append(f"{k}={urllib.parse.quote(str(v))}")
        if parts:
            query = "?" + "&".join(parts)

    url = f"{ML_SERVICE_URL}{path}{query}"
    logger.debug("ML client GET %s", url)

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=_TIMEOUT_SECONDS) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ML service returned HTTP {exc.code} for {path}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"ML service unreachable at {ML_SERVICE_URL}{path}: {exc.reason}"
        ) from exc
    except Exception as exc:
        raise RuntimeError(f"ML client error for {path}: {exc}") from exc


# Fix missing import
import urllib.parse  # noqa: E402  (needed by _get above)


# ── Public API ────────────────────────────────────────────────────────────────

def get_ml_forecast(horizon: int = 15) -> dict[str, Any]:
    """Fetch calibrated USD/INR multi-horizon forecast from the ML service.

    ML endpoint: GET /forecast?horizon=<N>

    Returns GetForecastResponse dict:
        horizon, current_rate, dates, median,
        bands_50 {lower, upper}, bands_90 {lower, upper},
        data_freshness, model_version, has_edge
    """
    return _get("/forecast", {"horizon": horizon})


def get_ml_advice(
    direction: str,
    amount_usd: float,
    horizon: int = 15,
    threshold: float | None = None,
) -> dict[str, Any]:
    """Fetch FX hedging advice from the ML service.

    ML endpoint: GET /advice?direction=<exporter|importer>&amount_usd=<N>&horizon=<N>

    Returns GetAdviceResponse dict:
        decision (LOCK_NOW | WAIT), reason, reasoning {...}
    """
    params: dict[str, Any] = {
        "direction": direction,
        "amount_usd": amount_usd,
        "horizon": horizon,
    }
    if threshold is not None:
        params["threshold"] = threshold
    return _get("/advice", params)


def get_ml_health() -> dict[str, Any]:
    """Check the ML service health endpoint.

    Returns HealthResponse dict with status, model_loaded, model_version, etc.
    Raises RuntimeError if the service is unreachable.
    """
    return _get("/health")

