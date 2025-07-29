"""
Sage AI Agent for Startup Financial OS MVP.

This module contains the core AI agent functionality for financial analysis and advice.
"""

import os
import json
import openai
from typing import Dict, Any, List
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are **Sage**, an AI co-founder and financial advisor for startups.

Your role:
1. Ask concise clarifying questions to understand the startup's financial situation
2. Calculate key financial metrics (MRR, churn, CAC, runway, etc.)
3. Suggest one specific, actionable improvement based on the data
4. Explain financial concepts in plain language, avoiding jargon

Guidelines:
- Be encouraging but realistic
- Focus on runway and sustainability
- Provide specific, actionable advice
- Keep responses under 150 tokens
- Use emojis sparingly but effectively
"""

class SageAgent:
    """Sage AI Agent for startup financial analysis."""
    
    def __init__(self):
        self.conversation_history = []
        self.current_metrics = {}
    
    def calculate_model(self, drivers: Dict[str, Any]) -> Dict[str, float]:
        """Calculate financial metrics from input drivers."""
        from ..core_engine.formulas import METRIC_FUNCS
        
        # Convert string values to float where needed
        processed_drivers = {}
        for key, value in drivers.items():
            if isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                processed_drivers[key] = float(value)
            else:
                processed_drivers[key] = value
        
        # Calculate all metrics
        metrics = {}
        for metric_name, calc_func in METRIC_FUNCS.items():
            try:
                metrics[metric_name] = calc_func(processed_drivers)
            except (KeyError, ZeroDivisionError):
                metrics[metric_name] = 0.0
        
        self.current_metrics = metrics
        return metrics
    
    def suggest_changes(self, drivers: Dict[str, Any], metrics: Dict[str, float]) -> str:
        """Generate AI-powered suggestions for improvement."""
        
        # Prepare context for AI
        context = {
            "drivers": drivers,
            "metrics": metrics,
            "project_type": drivers.get("project_type", "Unknown")
        }
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                temperature=0.3,
                max_tokens=150,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze this startup data and provide one specific improvement suggestion: {json.dumps(context, indent=2)}"}
                ],
                functions=[
                    {
                        "name": "recommendation",
                        "description": "Provide a specific, actionable recommendation",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "advice": {
                                    "type": "string",
                                    "description": "One specific, actionable piece of advice"
                                },
                                "priority": {
                                    "type": "string",
                                    "enum": ["critical", "high", "medium", "low"],
                                    "description": "Priority level of the recommendation"
                                }
                            },
                            "required": ["advice", "priority"]
                        }
                    }
                ],
                function_call={"name": "recommendation"}
            )
            
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "recommendation":
                result = json.loads(function_call.arguments)
                return result["advice"]
            else:
                return "I need more data to provide specific advice. Please complete the wizard questions."
                
        except Exception as e:
            return f"Unable to generate advice at this time. Error: {str(e)}"
    
    def log_conversation(self, user_input: str, agent_response: str, metrics: Dict[str, float] = None):
        """Log conversation for learning and audit purposes."""
        entry = {
            "user_input": user_input,
            "agent_response": agent_response,
            "metrics": metrics or {},
            "timestamp": str(datetime.now())
        }
        self.conversation_history.append(entry)
    
    def get_relevant_context(self, k: int = 5) -> List[Dict]:
        """Get k most relevant previous conversations for context."""
        # Simple implementation - return last k conversations
        return self.conversation_history[-k:] if self.conversation_history else []

# Standalone functions for direct use
def calculate_model(drivers: Dict[str, Any]) -> Dict[str, float]:
    """Calculate financial metrics from input drivers."""
    agent = SageAgent()
    return agent.calculate_model(drivers)

def suggest_changes(drivers: Dict[str, Any], metrics: Dict[str, float]) -> str:
    """Generate AI-powered suggestions for improvement."""
    agent = SageAgent()
    return agent.suggest_changes(drivers, metrics) 