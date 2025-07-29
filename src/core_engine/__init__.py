"""
Core Engine module for Startup Financial OS MVP.

This module contains the core financial calculation formulas and metrics.
"""

from .formulas import METRIC_FUNCS, calc_mrr, calc_churn, calc_cac, calc_runway

__all__ = [
    "METRIC_FUNCS",
    "calc_mrr", 
    "calc_churn",
    "calc_cac",
    "calc_runway"
] 