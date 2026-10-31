from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.schemas import (
    CurrencyForecastRequest,
    ContractAdviceRequest,
    ShipmentRiskRequest,
    InsuranceRequest,
    DocumentRequest,
    DocumentVerifyRequest,
    ContractIntegrityRequest,
    WorkspaceRequest,
    ComplianceCheckRequest,
)

from app.services.forex import get_forex_data
from app.services.currency import get_currency_forecast
from app.services.contracts import get_contract_advice, verify_contract_integrity
from app.services.contracts_data import get_forward_contracts
from app.services.shipment import analyze_shipment
from app.services.shipment_data import get_shipments
from app.services.insurance import recommend_insurance
from app.services.documents import register_document, verify_document
from app.services.documents_data import get_documents
from app.services.workspace import get_workspace
from app.services.audit import get_audit_logs
from app.services.compliance import (
    get_compliance_overview,
    get_compliance_norms,
    check_trade_compliance,
)
from app.services.ml_client import get_ml_health, ML_SERVICE_URL


app = FastAPI(title="TradeShield Backend", version="1.0.0")

# CORS — allow Next.js dev server (port 3000) to call backend directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Backend liveness probe. Also reports ML service reachability."""
    ml_status: dict = {"url": ML_SERVICE_URL, "status": "unknown"}
    try:
        ml_health = get_ml_health()
        ml_status["status"] = ml_health.get("status", "unknown")
        ml_status["model_loaded"] = ml_health.get("model_loaded", False)
        ml_status["model_version"] = ml_health.get("model_version")
    except RuntimeError as exc:
        ml_status["status"] = "unreachable"
        ml_status["error"] = str(exc)
    return {"status": "ok", "ml_service": ml_status}


# ─── Forex ────────────────────────────────────────────────────────────────────

@app.get("/forex/usd-inr")
def forex_usd_inr():
    """Live USD/INR forecast from ML service → { rates, timeSeries, metrics }.
    Used by frontend useForexData() SWR hook via /api/forex/usd-inr."""
    return get_forex_data()


@app.post("/currency/forecast")
def currency_forecast(request: CurrencyForecastRequest):
    """ML-backed multi-day currency forecast (POST interface)."""
    return get_currency_forecast(request.currency_pair, request.forecast_days)


# ─── Workspace ────────────────────────────────────────────────────────────────

@app.get("/workspace")
def workspace_get(role: str = Query(default="exporter")):
    """Return WorkspaceSummary for the given role (GET for frontend SWR)."""
    return get_workspace(role)


@app.post("/workspace")
def workspace_post(request: WorkspaceRequest):
    """Return WorkspaceSummary for the given role (POST interface)."""
    return get_workspace(request.role)


# ─── Shipments ────────────────────────────────────────────────────────────────

@app.get("/shipments")
def shipments_list(role: Optional[str] = Query(default=None)):
    """Return Shipment[] optionally filtered by role (GET for frontend SWR)."""
    return get_shipments(role)


@app.post("/shipments/analyze")
def shipment_risk(request: ShipmentRiskRequest):
    """Analyze risk for a single shipment (POST interface)."""
    return analyze_shipment(
        request.origin,
        request.destination,
        request.cargo_type,
        request.departure_date,
        request.transport_mode,
    )


# ─── Documents ────────────────────────────────────────────────────────────────

@app.get("/documents")
def documents_list(shipmentId: Optional[str] = Query(default=None)):
    """Return TradeDocument[] optionally filtered by shipmentId (GET for SWR)."""
    return get_documents(shipmentId)


@app.post("/documents")
def create_document(request: DocumentRequest):
    """Register a new trade document and return its hash."""
    return register_document(
        request.document_name,
        request.document_type,
        request.trade_reference,
        request.owner_role,
    )


@app.post("/documents/verify")
def document_verification(request: DocumentVerifyRequest):
    """Verify a document's SHA-256 hash against stored value."""
    return verify_document(
        request.document_id,
        request.expected_hash,
        request.submitted_hash,
    )


# ─── Forward Contracts ────────────────────────────────────────────────────────

@app.get("/contracts/forward")
def forward_contracts():
    """Return ForwardContract[] (GET for frontend SWR useForwardContracts)."""
    return get_forward_contracts()


@app.post("/contracts/advice")
def contract_advice(request: ContractAdviceRequest):
    """ML-backed hedge advice for a specific contract (POST interface)."""
    return get_contract_advice(
        request.currency_pair,
        request.amount,
        request.current_rate,
        request.offered_forward_rate,
        request.payment_days,
    )


@app.post("/contracts/verify-integrity")
def contract_integrity(request: ContractIntegrityRequest):
    """SHA-256 integrity check for contract terms."""
    return verify_contract_integrity(
        request.contract_id,
        request.contract_terms,
        request.expected_hash,
    )


# ─── Audit ────────────────────────────────────────────────────────────────────

@app.get("/audit/logs")
def audit_logs():
    """Return AuditActivity[] (GET for frontend SWR useAuditActivity)."""
    return get_audit_logs()


# ─── Insurance ────────────────────────────────────────────────────────────────

@app.post("/insurance/recommend")
def insurance_advice(request: InsuranceRequest):
    """Recommend cargo insurance coverage."""
    return recommend_insurance(
        request.cargo_type,
        request.cargo_value,
        request.currency,
        request.origin,
        request.destination,
        request.transport_mode,
    )


# ─── Compliance (DGFT / ICEGATE / FEMA / FTA) ────────────────────────────────
# Dual-prefixed: Next.js proxies /api/* → backend, so /api/compliance/overview
# becomes /compliance/overview at the backend. Both prefixes kept for safety.

@app.get("/api/compliance/overview")
@app.get("/compliance/overview")
def compliance_overview():
    return get_compliance_overview()


@app.get("/api/compliance/norms")
@app.get("/compliance/norms")
def compliance_norms():
    return get_compliance_norms()


@app.post("/api/compliance/check")
@app.post("/compliance/check")
def compliance_check(request: ComplianceCheckRequest):
    return check_trade_compliance(
        request.trade_type,
        request.partner_country,
        request.product_category,
        request.hs_code,
        request.declared_value_usd,
        request.shipping_bill_date,
    )
