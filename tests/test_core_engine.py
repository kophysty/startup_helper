"""
Tests for core_engine module.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core_engine.formulas import calc_mrr, calc_churn, calc_cac, calc_runway, calc_burn_rate, calc_ltv

def test_calc_mrr():
    """Test MRR calculation."""
    inputs = {"price": 50, "customers": 10}
    assert calc_mrr(inputs) == 500

def test_calc_churn():
    """Test churn rate calculation."""
    inputs = {"churn_rate": 5.5}
    assert calc_churn(inputs) == 5.5

def test_calc_cac():
    """Test CAC calculation."""
    inputs = {"marketing_spend": 1000, "new_customers": 20}
    assert calc_cac(inputs) == 50

def test_calc_cac_zero_customers():
    """Test CAC calculation with zero customers (should not divide by zero)."""
    inputs = {"marketing_spend": 1000, "new_customers": 0}
    assert calc_cac(inputs) == 1000  # Should use max(0, 1) = 1

def test_calc_runway():
    """Test runway calculation."""
    inputs = {
        "price": 50,
        "customers": 10,
        "expenses_monthly": 400,
        "cash_balance": 10000
    }
    # MRR = 500, Burn = 400 - 500 = -100 (negative burn means profit)
    # Runway = 10000 / max(-100, 1) = 10000 / 1 = 10000
    assert calc_runway(inputs) == 10000

def test_calc_runway_positive_burn():
    """Test runway calculation with positive burn rate."""
    inputs = {
        "price": 50,
        "customers": 5,
        "expenses_monthly": 1000,
        "cash_balance": 10000
    }
    # MRR = 250, Burn = 1000 - 250 = 750
    # Runway = 10000 / 750 ≈ 13.33
    expected_runway = 10000 / 750
    assert abs(calc_runway(inputs) - expected_runway) < 0.01

def test_calc_burn_rate():
    """Test burn rate calculation."""
    inputs = {"expenses_monthly": 1000, "price": 50, "customers": 10}
    # MRR = 500, Burn = 1000 - 500 = 500
    assert calc_burn_rate(inputs) == 500

def test_calc_ltv():
    """Test LTV calculation."""
    inputs = {"price": 50, "churn_rate": 5}
    # LTV = 50 / (5/100) = 50 / 0.05 = 1000
    assert calc_ltv(inputs) == 1000

def test_calc_ltv_zero_churn():
    """Test LTV calculation with zero churn."""
    inputs = {"price": 50, "churn_rate": 0}
    assert calc_ltv(inputs) == 0

def test_metric_functions_dict():
    """Test that all metric functions are available in METRIC_FUNCS."""
    from core_engine.formulas import METRIC_FUNCS
    
    expected_functions = ["mrr", "churn", "cac", "runway", "burn_rate", "ltv"]
    for func_name in expected_functions:
        assert func_name in METRIC_FUNCS
        assert callable(METRIC_FUNCS[func_name]) 