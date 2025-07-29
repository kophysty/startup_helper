"""
Logging configuration for Startup Financial OS MVP.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: str = "sage.log"):
    """Setup logging configuration for the application."""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / log_file),
            logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("streamlit").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging setup complete. Level: {log_level}, File: {log_file}")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)

def log_user_action(user_id: str, action: str, details: dict = None):
    """Log user actions for analytics and debugging."""
    logger = get_logger("user_actions")
    log_data = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "details": details or {}
    }
    logger.info(f"User action: {log_data}")

def log_agent_interaction(user_id: str, input_text: str, response: str, metrics: dict = None):
    """Log AI agent interactions for learning and audit."""
    logger = get_logger("agent_interactions")
    log_data = {
        "user_id": user_id,
        "input": input_text,
        "response": response,
        "metrics": metrics or {},
        "timestamp": datetime.now().isoformat()
    }
    logger.info(f"Agent interaction: {log_data}")

def log_feedback(user_id: str, advice_id: str, rating: str, feedback_text: str = None):
    """Log user feedback on AI advice."""
    logger = get_logger("feedback")
    log_data = {
        "user_id": user_id,
        "advice_id": advice_id,
        "rating": rating,  # "positive" or "negative"
        "feedback_text": feedback_text,
        "timestamp": datetime.now().isoformat()
    }
    logger.info(f"User feedback: {log_data}") 