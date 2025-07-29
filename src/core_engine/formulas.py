"""
Financial calculation formulas for Startup Financial OS MVP.

This module contains the core financial metrics calculations used by the application.
"""

from typing import Dict, Any

def calc_mrr(inputs: Dict[str, float]) -> float:
    """Calculate Monthly Recurring Revenue."""
    return inputs["price"] * inputs["customers"]

def calc_churn(inputs: Dict[str, float]) -> float:
    """Calculate churn rate (percentage)."""
    return inputs["churn_rate"]

def calc_cac(inputs: Dict[str, float]) -> float:
    """Calculate Customer Acquisition Cost."""
    return inputs["marketing_spend"] / max(inputs["new_customers"], 1)

def calc_runway(inputs: Dict[str, float]) -> float:
    """Calculate runway in months."""
    burn = inputs["expenses_monthly"] - calc_mrr(inputs)
    return inputs["cash_balance"] / max(burn, 1)

def calc_burn_rate(inputs: Dict[str, float]) -> float:
    """Calculate monthly burn rate."""
    return inputs["expenses_monthly"] - calc_mrr(inputs)

def calc_ltv(inputs: Dict[str, float]) -> float:
    """Calculate Lifetime Value."""
    if inputs["churn_rate"] == 0:
        return 0
    return inputs["price"] / (inputs["churn_rate"] / 100)

METRIC_FUNCS = {
    "mrr": calc_mrr,
    "churn": calc_churn,
    "cac": calc_cac,
    "runway": calc_runway,
    "burn_rate": calc_burn_rate,
    "ltv": calc_ltv,
} 