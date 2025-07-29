"""
Gamification module for Startup Financial OS MVP.

This module handles badges, progress tracking, and user engagement features.
"""

from .badges import load_badges, check_badge_eligibility, award_badge

__all__ = [
    "load_badges",
    "check_badge_eligibility", 
    "award_badge"
] 