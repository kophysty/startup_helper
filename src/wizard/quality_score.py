"""
Startup Quality Score Calculator

This module calculates a quality score for startups based on their financial metrics.
"""

from typing import Dict, Any

def calculate_quality_score(answers: Dict[str, Any]) -> int:
    """
    Calculate startup quality score (0-100) based on answers.
    
    Args:
        answers: Dictionary of wizard answers
        
    Returns:
        Quality score from 0 to 100
    """
    score = 0
    
    # Churn rate scoring
    churn_rate = answers.get("churn_rate", 100)
    if churn_rate < 3:
        score += 25
    elif churn_rate < 5:
        score += 20
    elif churn_rate < 10:
        score += 10
    elif churn_rate < 20:
        score += 5
    
    # CAC/LTV ratio scoring
    cac = answers.get("cac", 0)
    ltv = answers.get("ltv", 1)
    if ltv > 0:
        cac_ltv_ratio = cac / ltv
        if cac_ltv_ratio < 0.2:
            score += 20
        elif cac_ltv_ratio < 0.3:
            score += 15
        elif cac_ltv_ratio < 0.5:
            score += 10
        elif cac_ltv_ratio < 1.0:
            score += 5
    
    # Runway scoring
    runway = answers.get("runway", 0)
    if runway >= 18:
        score += 20
    elif runway >= 12:
        score += 15
    elif runway >= 6:
        score += 10
    elif runway >= 3:
        score += 5
    
    # Burn rate scoring
    burn_rate = answers.get("burn_rate", 0)
    revenue = answers.get("revenue_monthly", 0) or (answers.get("price", 0) * answers.get("customers", 0))
    if revenue > 0 and burn_rate < revenue:
        score += 15
    elif revenue > 0 and burn_rate < revenue * 1.5:
        score += 10
    elif revenue > 0 and burn_rate < revenue * 2:
        score += 5
    
    # Growth rate scoring
    new_customers = answers.get("new_customers", 0)
    existing_customers = answers.get("customers", 0)
    if existing_customers > 0:
        growth_rate = (new_customers / existing_customers) * 100
        if growth_rate >= 20:
            score += 15
        elif growth_rate >= 10:
            score += 10
        elif growth_rate >= 5:
            score += 5
    
    # Team size scoring (lean is better)
    team_size = answers.get("team_size", 1)
    if team_size <= 5:
        score += 10
    elif team_size <= 10:
        score += 5
    elif team_size <= 20:
        score += 2
    
    # Price point scoring
    price = answers.get("price", 0)
    if price >= 100:
        score += 10
    elif price >= 50:
        score += 8
    elif price >= 25:
        score += 5
    elif price >= 10:
        score += 3
    
    return min(100, max(0, score))

def get_quality_feedback(score: int) -> str:
    """
    Get feedback message based on quality score.
    
    Args:
        score: Quality score (0-100)
        
    Returns:
        Feedback message
    """
    if score >= 80:
        return "🚀 Excellent! Your startup has strong fundamentals."
    elif score >= 60:
        return "✅ Good! You're on the right track with room for improvement."
    elif score >= 40:
        return "⚠️ Fair. Focus on the key metrics to improve your score."
    elif score >= 20:
        return "🔧 Needs work. Review the benchmarks and adjust your strategy."
    else:
        return "🔄 Start with the basics. Focus on churn, CAC, and runway."

def calculate_score_delta(old_score: int, new_score: int) -> str:
    """
    Calculate and format score delta for display.
    
    Args:
        old_score: Previous score
        new_score: Current score
        
    Returns:
        Formatted delta string
    """
    delta = new_score - old_score
    if delta > 0:
        return f"+{delta} pts"
    elif delta < 0:
        return f"{delta} pts"
    else:
        return "0 pts" 