"""
Sanity rules loader and validator for the wizard module.
"""

import yaml
import os
from typing import List, Dict, Any

def load_sanity_rules() -> List[Dict[str, Any]]:
    """Load sanity rules from sanity_rules.yml file."""
    rules_path = os.path.join(os.path.dirname(__file__), 'sanity_rules.yml')
    
    with open(rules_path, 'r', encoding='utf-8') as f:
        rules = yaml.safe_load(f)
    
    return rules

def validate_metrics(metrics: Dict[str, float], drivers: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate metrics against sanity rules and return violations."""
    rules = load_sanity_rules()
    violations = []
    
    # Create context for rule evaluation
    context = {**metrics, **drivers}
    
    for rule in rules:
        condition = rule['condition']
        
        try:
            # Simple condition evaluation (for MVP)
            # In production, use a proper expression evaluator
            if evaluate_condition(condition, context):
                violations.append(rule)
        except Exception as e:
            # Log error but continue with other rules
            print(f"Error evaluating rule {rule['id']}: {e}")
    
    return violations

def evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    """Evaluate a condition string against the context."""
    # Simple condition evaluator for MVP
    # In production, use a proper expression evaluator like `asteval`
    
    # Replace variable names with values
    for key, value in context.items():
        if isinstance(value, (int, float)):
            condition = condition.replace(key, str(value))
    
    # Simple evaluation for common patterns
    if '<' in condition:
        parts = condition.split('<')
        if len(parts) == 2:
            try:
                left = float(parts[0].strip())
                right = float(parts[1].strip())
                return left < right
            except ValueError:
                return False
    
    elif '>' in condition:
        parts = condition.split('>')
        if len(parts) == 2:
            try:
                left = float(parts[0].strip())
                right = float(parts[1].strip())
                return left > right
            except ValueError:
                return False
    
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