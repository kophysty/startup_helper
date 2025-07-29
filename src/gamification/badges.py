"""
Badges system for gamification module.
"""

import yaml
import os
from typing import List, Dict, Any

def load_badges() -> List[Dict[str, Any]]:
    """Load badges from badges.yml file."""
    badges_path = os.path.join(os.path.dirname(__file__), 'badges.yml')
    
    with open(badges_path, 'r', encoding='utf-8') as f:
        badges = yaml.safe_load(f)
    
    return badges

def check_badge_eligibility(user_metrics: Dict[str, float], user_actions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check which badges a user is eligible for."""
    badges = load_badges()
    eligible_badges = []
    
    # Create context for badge evaluation
    context = {**user_metrics, **user_actions}
    
    for badge in badges:
        condition = badge['condition']
        
        try:
            if evaluate_badge_condition(condition, context):
                eligible_badges.append(badge)
        except Exception as e:
            # Log error but continue with other badges
            print(f"Error evaluating badge {badge['id']}: {e}")
    
    return eligible_badges

def award_badge(user_id: str, badge_id: str) -> Dict[str, Any]:
    """Award a badge to a user."""
    badges = load_badges()
    
    for badge in badges:
        if badge['id'] == badge_id:
            # In a real implementation, this would save to a database
            return {
                "user_id": user_id,
                "badge": badge,
                "awarded_at": "2025-01-XX",  # Would be actual timestamp
                "points_earned": badge.get('points', 0)
            }
    
    raise ValueError(f"Badge with ID '{badge_id}' not found")

def evaluate_badge_condition(condition: str, context: Dict[str, Any]) -> bool:
    """Evaluate a badge condition against the context."""
    # Simple condition evaluator for MVP
    # Similar to sanity_rules.evaluate_condition but for badge conditions
    
    # Replace variable names with values
    for key, value in context.items():
        if isinstance(value, (int, float, bool)):
            condition = condition.replace(key, str(value))
    
    # Simple evaluation for common patterns
    if '==' in condition:
        parts = condition.split('==')
        if len(parts) == 2:
            left = parts[0].strip()
            right = parts[1].strip()
            return left == right
    
    elif '>=' in condition:
        parts = condition.split('>=')
        if len(parts) == 2:
            try:
                left = float(parts[0].strip())
                right = float(parts[1].strip())
                return left >= right
            except ValueError:
                return False
    
    elif '<=' in condition:
        parts = condition.split('<=')
        if len(parts) == 2:
            try:
                left = float(parts[0].strip())
                right = float(parts[1].strip())
                return left <= right
            except ValueError:
                return False
    
    return False

def get_user_badges(user_id: str) -> List[Dict[str, Any]]:
    """Get all badges awarded to a user."""
    # In a real implementation, this would query a database
    # For MVP, return empty list
    return []

def get_user_points(user_id: str) -> int:
    """Get total points earned by a user."""
    # In a real implementation, this would query a database
    # For MVP, return 0
    return 0 