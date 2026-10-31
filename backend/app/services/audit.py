"""
app/services/audit.py — Audit activity log service for GET /audit/logs.

Returns a list of AuditActivity dicts matching the frontend TypeScript AuditActivity type.
"""

from __future__ import annotations

from typing import Any

_AUDIT_LOG: list[dict[str, Any]] = [
    {
        "id": "ACT-9912",
        "timestamp": "2026-10-30 14:15 IST",
        "event": "Forex Model Forecast Recalibrated",
        "category": "Forex Intelligence",
        "actor": "TradeShield ML Pipeline (Engine v2.4)",
        "details": (
            "15-day USD/INR trajectory updated with latest US Treasury 10Y and DXY tick data. "
            "Central estimate Nov 14 raised to 86.82."
        ),
        "status": "Success",
        "hashVerification": "Verified (Hash: a812f9...210)",
    },
    {
        "id": "ACT-9911",
        "timestamp": "2026-10-30 11:40 IST",
        "event": "Port Congestion Risk Alert Triggered",
        "category": "Shipment Logistics",
        "actor": "AIS Logistics Sentinel",
        "details": (
            "Shipment TS-SHP-2026-0891 flagged Elevated Risk: Rotterdam container dwell times "
            "crossed 4.8-day threshold (+42% delay cost risk)."
        ),
        "status": "Alert",
        "hashVerification": "Logged & Dispatched",
    },
    {
        "id": "ACT-9910",
        "timestamp": "2026-10-29 16:30 IST",
        "event": "Forward Contract Advice Computed",
        "category": "Hedging Decision",
        "actor": "Decision Rules Engine",
        "details": (
            "Analyzed $95,000 USD receivable maturing Nov 12. "
            "Forward rate quote 86.6850 offers +0.26 INR gain with zero downside. "
            "Action: Lock 80%."
        ),
        "status": "Success",
        "hashVerification": "Audited",
    },
    {
        "id": "ACT-9909",
        "timestamp": "2026-10-28 17:34 IST",
        "event": "Document Verified Against Notary Hash",
        "category": "Documentation",
        "actor": "Alex Mercer",
        "details": (
            "Bill of Entry #BE-908124 uploaded and cryptographic hash verified against "
            "ICEGATE customs EDI signature node."
        ),
        "status": "Success",
        "hashVerification": "SHA-256 Intact",
    },
    {
        "id": "ACT-9908",
        "timestamp": "2026-10-27 14:12 IST",
        "event": "Document Tamper / Mismatch Flagged",
        "category": "Integrity Warning",
        "actor": "Verification Sentinel",
        "details": (
            "Packing List HAM_941_V2 digest failed to match original customs declaration hash. "
            "Marked 'Attention Needed'."
        ),
        "status": "Warning",
        "hashVerification": "Mismatch Flagged",
    },
]


def get_audit_logs() -> list[dict[str, Any]]:
    """Return the full audit activity log."""
    return _AUDIT_LOG

