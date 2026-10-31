"""
app/services/documents_data.py — Trade documents list service for GET /documents.

Returns a list of TradeDocument dicts matching the frontend TypeScript TradeDocument type.
Supports optional shipmentId filter (matches shipmentRef field).
"""

from __future__ import annotations

from typing import Any

_DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "DOC-2026-4401",
        "title": "Commercial Invoice #EXP-2026-891",
        "type": "Commercial Invoice",
        "shipmentRef": "TS-SHP-2026-0891",
        "counterparty": "Dutch Precision B.V. (Rotterdam)",
        "uploadDate": "2026-10-17 11:24 IST",
        "fileSize": "1.42 MB",
        "fileName": "Commercial_Invoice_EXP_891_Signed.pdf",
        "sha256Hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "integrityStatus": "Verified",
        "verificationDetails": {
            "algorithm": "SHA-256 with RSA-4096 Timestamp Signature",
            "notarySource": "TradeShield Vault & DGFT ICEGATE Node",
            "signedBy": "Alex Mercer (Authorized Signatory, Zenith Precision)",
            "verifiedAt": "2026-10-17 11:25:02 IST",
            "qrPayload": "TRSHLD://VERIFY/DOC-2026-4401/e3b0c442...855",
            "isTamperProof": True,
        },
        "amountUSD": 95000,
    },
    {
        "id": "DOC-2026-4402",
        "title": "Marine Cargo Insurance Certificate",
        "type": "Insurance Certificate",
        "shipmentRef": "TS-SHP-2026-0891",
        "counterparty": "New India Assurance / Lloyd's Syndicate",
        "uploadDate": "2026-10-18 09:15 IST",
        "fileSize": "890 KB",
        "fileName": "Marine_Cargo_Cert_POL_98124.pdf",
        "sha256Hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
        "integrityStatus": "Verified",
        "verificationDetails": {
            "algorithm": "SHA-256 Digest",
            "notarySource": "Insurer Policy Portal Linkage",
            "signedBy": "Underwriting Desk, Marine Hull & Cargo Dept",
            "verifiedAt": "2026-10-18 09:16:40 IST",
            "qrPayload": "TRSHLD://VERIFY/DOC-2026-4402/7f83b165...069",
            "isTamperProof": True,
        },
        "amountUSD": 95000,
    },
    {
        "id": "DOC-2026-4403",
        "title": "Ocean Bill of Lading (B/L) #MSK2641-01",
        "type": "Bill of Lading",
        "shipmentRef": "TS-SHP-2026-0891",
        "counterparty": "A.P. Moller - Maersk",
        "uploadDate": "2026-10-19 16:45 IST",
        "fileSize": "2.15 MB",
        "fileName": "Master_BL_Maersk_MSK2641_01.pdf",
        "sha256Hash": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
        "integrityStatus": "Verified",
        "verificationDetails": {
            "algorithm": "SHA-256 Carrier Manifest Check",
            "notarySource": "Maersk EDI Carrier Exchange",
            "signedBy": "Port Operations Master, Mundra",
            "verifiedAt": "2026-10-19 16:50:11 IST",
            "qrPayload": "TRSHLD://VERIFY/DOC-2026-4403/4b227777...f8a",
            "isTamperProof": True,
        },
        "amountUSD": 95000,
    },
    {
        "id": "DOC-2026-4404",
        "title": "Packing List & Weight Certificate",
        "type": "Packing List",
        "shipmentRef": "TS-SHP-2026-0891",
        "counterparty": "Zenith Warehouse QA Division",
        "uploadDate": "2026-10-18 14:10 IST",
        "fileSize": "640 KB",
        "fileName": "Packing_List_EXP_891_Weights.pdf",
        "sha256Hash": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        "integrityStatus": "Attention Needed",
        "verificationDetails": {
            "algorithm": "SHA-256 Digest Match Check",
            "notarySource": "Internal Hash Check",
            "signedBy": "Unsigned / Draft Revision Detected",
            "verifiedAt": "Mismatch Warning: Net tare weight field differs by 120kg from export manifest",
            "qrPayload": "TRSHLD://VERIFY/DOC-2026-4404/PENDING",
            "isTamperProof": False,
        },
        "amountUSD": 95000,
    },
    {
        "id": "DOC-2026-4405",
        "title": "Certificate of Origin (e-CoO)",
        "type": "Certificate of Origin",
        "shipmentRef": "TS-SHP-2026-0891",
        "counterparty": "Bombay Chamber of Commerce & Industry",
        "uploadDate": "2026-10-19 10:05 IST",
        "fileSize": "1.12 MB",
        "fileName": "BCCI_Cert_of_Origin_EXP_891.pdf",
        "sha256Hash": "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d96cd385ccab5b9697f8",
        "integrityStatus": "Verified",
        "verificationDetails": {
            "algorithm": "SHA-256 with e-CoO QR Integration",
            "notarySource": "DGFT e-CoO Registry Node",
            "signedBy": "Secretary, BCCI Trade Facilitation",
            "verifiedAt": "2026-10-19 10:07:18 IST",
            "qrPayload": "TRSHLD://VERIFY/DOC-2026-4405/6ca13d52...7f8",
            "isTamperProof": True,
        },
        "amountUSD": 95000,
    },
]


def get_documents(shipment_id: str | None = None) -> list[dict[str, Any]]:
    """Return all documents, optionally filtered by shipmentRef."""
    if shipment_id:
        return [d for d in _DOCUMENTS if d["shipmentRef"] == shipment_id]
    return _DOCUMENTS

