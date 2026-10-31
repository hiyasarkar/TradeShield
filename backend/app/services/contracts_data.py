"""
app/services/contracts_data.py — Forward contracts list for GET /contracts/forward.

Returns a list of ForwardContract dicts matching the frontend TypeScript ForwardContract type.
"""

from __future__ import annotations

from typing import Any

_FORWARD_CONTRACTS: list[dict[str, Any]] = [
    {
        "id": "FWD-2026-0182",
        "bank": "HDFC Bank Global Treasury",
        "contractType": "Export Forward (Deliverable)",
        "currencyPair": "USD/INR",
        "notionalUSD": 150000,
        "lockedRate": 86.5800,
        "spotAtBooking": 86.3200,
        "bookingDate": "2026-10-05",
        "maturityDate": "2026-11-20",
        "status": "Active",
        "lifecycleStage": "shipped",
        "integrityHash": "9f83c162bca9812401efb561cda41a203f56781290312fa89b2138947612caba",
        "digitalSignature": "RSA-4096:0x4A8F...29E1 (HDFC Treasury Verified)",
        "mtmGainLossINR": 39000,
        "settlementInstructions": "Nostro Credit to Citibank NY AC #981240",
    },
    {
        "id": "FWD-2026-0189",
        "bank": "ICICI Bank FX Desk",
        "contractType": "Export Forward (Deliverable)",
        "currencyPair": "USD/INR",
        "notionalUSD": 135000,
        "lockedRate": 86.7200,
        "spotAtBooking": 86.4100,
        "bookingDate": "2026-10-18",
        "maturityDate": "2026-12-15",
        "status": "Active",
        "lifecycleStage": "signed",
        "integrityHash": "3d29a5108cb9214710fba23984019aeb240187429184baed0912481093582410",
        "digitalSignature": "RSA-4096:0x89D2...11B4 (ICICI Treasury Verified)",
        "mtmGainLossINR": 39825,
        "settlementInstructions": "RTGS to ICICI Mumbai Overseas Branch",
    },
    {
        "id": "FWD-2026-0164",
        "bank": "State Bank of India (SBI Forex)",
        "contractType": "Import Forward (Deliverable)",
        "currencyPair": "USD/INR",
        "notionalUSD": 140000,
        "lockedRate": 86.4500,
        "spotAtBooking": 86.2000,
        "bookingDate": "2026-09-12",
        "maturityDate": "2026-10-25",
        "status": "Matured & Settled",
        "lifecycleStage": "paid",
        "integrityHash": "c019284ba56910248aef019283741029ba301982740192837401928374019283",
        "digitalSignature": "RSA-4096:0x77E1...00A3 (SBI Global Verified)",
        "mtmGainLossINR": 24500,
        "settlementInstructions": "Settled via Nostro remittance",
    },
]


def get_forward_contracts() -> list[dict[str, Any]]:
    """Return all forward contracts."""
    return _FORWARD_CONTRACTS

