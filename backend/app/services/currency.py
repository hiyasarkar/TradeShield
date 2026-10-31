"""
app/services/currency.py — Currency intelligence service.

Delegates to the TradeShield ML service (ML/app/api/routes/forecast.py) which
returns calibrated multi-horizon USD/INR range forecasts produced by a trained
quantile-regression model with isotonic calibration.

Fallback: if the ML service is unavailable, returns a structured error response
so the API stays up and the frontend can degrade gracefully.
"""

from __future__ import annotations

import logging
from typing import Any

from app.services.ml_client import get_ml_forecast, get_ml_health

logger = logging.getLogger(__name__)


def get_currency_forecast(currency_pair: str, forecast_days: int) -> dict[str, Any]:
    """Return a calibrated multi-day USD/INR FX forecast from the ML service.

    Parameters
    ----------
    currency_pair:
        Currency pair string (currently only "USD/INR" or "USDINR" is supported
        by the ML model; other pairs fall back gracefully).
    forecast_days:
        Number of business days to forecast ahead (1–15).

    Returns
    -------
    dict with keys:
        currency_pair, forecast_days, current_rate, dates,
        median, bands_50 {lower, upper}, bands_90 {lower, upper},
        data_freshness, model_version, has_edge, source
    On ML service failure:
        feature, status="ml_unavailable", error, currency_pair, forecast_days
    """
    # Normalise pair name — ML service only supports USDINR
    normalised = currency_pair.replace("/", "").upper()
    if normalised != "USDINR":
        logger.warning(
            "Currency pair %s is not supported by the ML model; "
            "only USDINR is available. Returning unsupported response.",
            currency_pair,
        )
        return {
            "feature": "currency_forecast",
            "status": "unsupported_pair",
            "currency_pair": currency_pair,
            "forecast_days": forecast_days,
            "message": f"The ML model only supports USDINR. Requested: {currency_pair}.",
        }

    try:
        ml_result = get_ml_forecast(horizon=forecast_days)
        logger.info(
            "ML forecast fetched: version=%s, horizon=%s, has_edge=%s",
            ml_result.get("model_version"),
            ml_result.get("horizon"),
            ml_result.get("has_edge"),
        )
        return {
            "currency_pair": currency_pair,
            "forecast_days": forecast_days,
            "current_rate": ml_result.get("current_rate"),
            "dates": ml_result.get("dates", []),
            "median": ml_result.get("median", []),
            "bands_50": ml_result.get("bands_50", {}),
            "bands_90": ml_result.get("bands_90", {}),
            "data_freshness": ml_result.get("data_freshness"),
            "model_version": ml_result.get("model_version"),
            "has_edge": ml_result.get("has_edge", False),
            "source": "tradeshield_ml",
        }

    except RuntimeError as exc:
        logger.error("ML service unavailable for currency forecast: %s", exc)
        return {
            "feature": "currency_forecast",
            "status": "ml_unavailable",
            "currency_pair": currency_pair,
            "forecast_days": forecast_days,
            "error": str(exc),
            "message": (
                "The ML forecasting service is currently unavailable. "
                "Start the ML service with: cd ML && uvicorn app.api.main:app --port 9000"
            ),
        }
