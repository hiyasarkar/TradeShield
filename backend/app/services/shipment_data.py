"""
app/services/shipment_data.py — Shipments list service for GET /shipments.

Returns a list of Shipment dicts matching the frontend TypeScript Shipment type.
Supports optional role filter ('exporter' | 'importer').
"""

from __future__ import annotations

from typing import Any

_SHIPMENTS: list[dict[str, Any]] = [
    {
        "id": "TS-SHP-2026-0891",
        "reference": "EXP-ROT-891",
        "role": "exporter",
        "origin": "Mundra Port, India (INMUN)",
        "destination": "Port of Rotterdam, Netherlands (NLRTM)",
        "cargo": "Precision CNC Aluminum Flanges (24 MT)",
        "carrier": "Maersk Line (Maersk Mc-Kinney Moller)",
        "voyage": "MSK-2641W",
        "departureDate": "2026-10-18",
        "estimatedArrival": "2026-11-14",
        "status": "In Transit",
        "riskLevel": "Elevated",
        "riskScore": 74,
        "riskFactors": {
            "portCongestion": "Elevated: Rotterdam container terminal dwell time is 4.8 days (+1.9d vs baseline).",
            "weatherRisk": "Moderate: Strong Atlantic low-pressure front expected along English Channel Nov 10-12.",
            "routeDisruption": "Active: Cape of Good Hope rerouting adds 9.4 sailing days avoiding Red Sea zone.",
            "vesselDelay": "Tracking 38 hours behind schedule past Gibraltar passage.",
        },
        "costExposureEstimate": "₹1,18,000 (Demurrage + potential delay penalty)",
        "associatedInvoiceUSD": 95000,
        "insuranceStatus": "Covered (ICC-A Marine All-Risk)",
        "coordinates": {"lat": 21.5, "lng": 39.8},
        "milestones": [
            {"date": "Oct 18", "event": "Vessel departed Mundra Port", "status": "completed"},
            {"date": "Oct 24", "event": "Passed Arabian Sea / Gulf of Aden transit point", "status": "completed"},
            {"date": "Oct 30", "event": "Rounding Cape Coast / South Atlantic passage", "status": "in-progress"},
            {"date": "Nov 10", "event": "Estimated Bay of Biscay waypoint", "status": "pending"},
            {"date": "Nov 14", "event": "Projected arrival Rotterdam Maasvlakte", "status": "pending"},
        ],
    },
    {
        "id": "TS-SHP-2026-0904",
        "reference": "EXP-EWR-904",
        "role": "exporter",
        "origin": "JNPT Nhava Sheva, India (INNSA)",
        "destination": "Port of New York / Newark, USA (USNWK)",
        "cargo": "Organic Cotton Yarn & Finished Twill (40ft HQ)",
        "carrier": "MSC Mediterranean Shipping (MSC Gülsün)",
        "voyage": "MSC-0892E",
        "departureDate": "2026-10-22",
        "estimatedArrival": "2026-11-19",
        "status": "In Transit",
        "riskLevel": "Low",
        "riskScore": 22,
        "riskFactors": {
            "portCongestion": "Normal: Newark PNCT dwell time is 1.8 days.",
            "weatherRisk": "Low: Calm mid-Atlantic sea conditions, wave heights under 2.1m.",
            "routeDisruption": "None: Standard direct trans-Atlantic corridor.",
            "vesselDelay": "On-time arrival projected (+4 hrs buffer).",
        },
        "costExposureEstimate": "₹0 (Nominal operations)",
        "associatedInvoiceUSD": 142000,
        "insuranceStatus": "Covered (ICC-A + War Risk)",
        "milestones": [
            {"date": "Oct 22", "event": "Cleared customs & loaded at JNPT", "status": "completed"},
            {"date": "Oct 28", "event": "Suez Canal northbound transit cleared", "status": "completed"},
            {"date": "Oct 30", "event": "Exiting Mediterranean via Strait of Gibraltar", "status": "in-progress"},
            {"date": "Nov 19", "event": "Estimated berthing Port of Newark", "status": "pending"},
        ],
    },
    {
        "id": "TS-SHP-2026-0941",
        "reference": "EXP-HAM-941",
        "role": "exporter",
        "origin": "Mundra Port, India (INMUN)",
        "destination": "Port of Hamburg, Germany (DEHAM)",
        "cargo": "Specialty Guar Gum Derivatives & Food Starches",
        "carrier": "CMA CGM (Antoine de Saint Exupery)",
        "voyage": "CMA-1029W",
        "departureDate": "2026-10-15",
        "estimatedArrival": "2026-11-16",
        "status": "Delayed",
        "riskLevel": "Critical",
        "riskScore": 88,
        "riskFactors": {
            "portCongestion": "Critical: Elbe River tidal restrictions + Hamburg dock strike warning Nov 12-14.",
            "weatherRisk": "High: North Sea squalls causing container vessel holding patterns.",
            "routeDisruption": "Active: Cape detour added 11 days sailing.",
            "vesselDelay": "Tracking 72 hours behind initial bill of lading schedule.",
        },
        "costExposureEstimate": "₹2,45,000 (Buyer SLA penalty + holding demurrage)",
        "associatedInvoiceUSD": 65000,
        "insuranceStatus": "Covered (ICC-A + Consequential Loss Endorsement)",
        "milestones": [
            {"date": "Oct 15", "event": "Vessel departed Mundra", "status": "completed"},
            {"date": "Oct 26", "event": "Crossed South Atlantic ridge", "status": "completed"},
            {"date": "Oct 30", "event": "Off West African coast (Mauritania)", "status": "in-progress"},
            {"date": "Nov 12", "event": "Expected English Channel pilot pickup", "status": "pending"},
            {"date": "Nov 16", "event": "Revised Hamburg CTA berthing", "status": "pending"},
        ],
    },
    {
        "id": "TS-SHP-2026-0812",
        "reference": "IMP-SHA-812",
        "role": "importer",
        "origin": "Port of Shanghai, China (CNSHA)",
        "destination": "Nhava Sheva JNPT, India (INNSA)",
        "cargo": "Lithium-Ion Battery Cells & BMS Modules (2x40ft Hazmat)",
        "carrier": "COSCO Shipping (COSCO Universe)",
        "voyage": "COS-8831W",
        "departureDate": "2026-10-21",
        "estimatedArrival": "2026-11-08",
        "status": "In Transit",
        "riskLevel": "Elevated",
        "riskScore": 78,
        "riskFactors": {
            "portCongestion": "Moderate: JNPT terminal gates facing 24hr truck turn time backlog.",
            "weatherRisk": "High: Tropical storm depression active in South China Sea near Paracel Islands.",
            "routeDisruption": "Vessel conducted 48hr storm avoidance slow steaming.",
            "vesselDelay": "Delayed by 52 hours; customs import window tight.",
        },
        "costExposureEstimate": "₹1,85,000 (Production downtime buffer at Pune plant)",
        "associatedInvoiceUSD": 145000,
        "insuranceStatus": "Covered (Institute Bulk & Hazmat Clauses)",
        "milestones": [
            {"date": "Oct 21", "event": "Cleared customs at Yangshan Terminal Shanghai", "status": "completed"},
            {"date": "Oct 25", "event": "Weather avoidance reroute around Hainan", "status": "completed"},
            {"date": "Oct 30", "event": "Transiting Malacca Strait westbound", "status": "in-progress"},
            {"date": "Nov 08", "event": "Expected discharge JNPT Nhava Sheva", "status": "pending"},
        ],
    },
]


def get_shipments(role: str | None = None) -> list[dict[str, Any]]:
    """Return all shipments, optionally filtered by role ('exporter' | 'importer')."""
    if role:
        return [s for s in _SHIPMENTS if s["role"] == role.lower().strip()]
    return _SHIPMENTS

