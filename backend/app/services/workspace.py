"""
app/services/workspace.py — Exporter / Importer workspace service.

Returns a WorkspaceSummary dict matching the frontend TypeScript type,
keyed by role ('exporter' | 'importer').
"""

from __future__ import annotations

from typing import Any


_WORKSPACES: dict[str, dict[str, Any]] = {
    "exporter": {
        "userName": "Alex Mercer",
        "companyName": "Zenith Precision Forgings Ltd.",
        "role": "exporter",
        "title": "Exporter Workspace",
        "currencyExposureLabel": "Total Open Receivables",
        "totalExposureUSD": 482500,
        "totalExposureINR": 41700062,
        "hedgedAmountUSD": 285000,
        "unhedgedAmountUSD": 197500,
        "hedgeRatio": 59.1,
        "riskDirectionText": "Rupee appreciation erases export margin",
        "primaryRiskMetric": "₹1,24,000 downside at 85.80 INR",
        "activeShipmentsCount": 5,
        "shipmentsAtRiskCount": 2,
        "documentsNeedingAttention": 3,
        "pendingPaymentsUSD": 165000,
        "nextSettlementDate": "Nov 12, 2026",
        "nextSettlementAmount": "$95,000 USD",
        "advisorRecommendation": {
            "headline": "Consider locking forward rate for Nov 12 receivable",
            "badge": "Action Recommended",
            "badgeType": "lime",
            "exposureTarget": "$95,000 USD receivable from Dutch Auto B.V.",
            "bankForwardQuote": 86.6850,
            "expectedSpot": 86.7200,
            "spotSpread": "-0.0350 INR",
            "downsideRiskProtected": "₹82,175 protected if spot retraces to 85.82",
            "reasoning": (
                "Forward premium pays +0.2600 INR above current spot (86.425). "
                "Locking provides guaranteed realization of ₹82,35,075 with zero downside risk, "
                "while unhedged holding has a 36% probability of dollar weakness."
            ),
            "suggestedAction": "Lock 80% ($75,000) at 86.6850; leave 20% spot open if risk-tolerant.",
        },
    },
    "importer": {
        "userName": "Alex Mercer",
        "companyName": "AeroTech Components India Pvt Ltd.",
        "role": "importer",
        "title": "Importer Workspace",
        "currencyExposureLabel": "Total Open Payables",
        "totalExposureUSD": 368000,
        "totalExposureINR": 31804400,
        "hedgedAmountUSD": 140000,
        "unhedgedAmountUSD": 228000,
        "hedgeRatio": 38.0,
        "riskDirectionText": "Dollar appreciation raises landed procurement cost",
        "primaryRiskMetric": "₹1,82,400 added cost at 87.20 INR",
        "activeShipmentsCount": 4,
        "shipmentsAtRiskCount": 2,
        "documentsNeedingAttention": 2,
        "pendingPaymentsUSD": 145000,
        "nextSettlementDate": "Nov 08, 2026",
        "nextSettlementAmount": "$120,000 USD",
        "advisorRecommendation": {
            "headline": "Review hedge coverage: High dollar breakout probability",
            "badge": "High Volatility Warning",
            "badgeType": "coral",
            "exposureTarget": "$120,000 USD payable to Shenzhen Silicon Tech",
            "bankForwardQuote": 86.6600,
            "expectedSpot": 86.7200,
            "spotSpread": "+0.0600 INR",
            "downsideRiskProtected": "₹91,200 potential overrun prevented if USD tests 87.42",
            "reasoning": (
                "USD/INR is testing upper channel resistance with strong DXY momentum. "
                "An unhedged payable exposes your landed margin to significant foreign exchange slippage. "
                "Bank quote at 86.6600 caps maximum outlay."
            ),
            "suggestedAction": "Book Import Forward Contract for $100,000 immediately at 86.6600.",
        },
    },
}


def get_workspace(role: str) -> dict[str, Any]:
    """Return workspace summary for the given role ('exporter' | 'importer')."""
    role = role.lower().strip()
    if role not in _WORKSPACES:
        return {
            "error": f"Unknown role '{role}'. Must be 'exporter' or 'importer'.",
            "role": role,
        }
    return _WORKSPACES[role]
