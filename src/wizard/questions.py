"""
Questions loader for the wizard module.
"""

import yaml
import os
from typing import List, Dict, Any

def load_questions() -> List[Dict[str, Any]]:
    """Load questions from questions.yml file."""
    questions_path = os.path.join(os.path.dirname(__file__), 'questions.yml')
    
    with open(questions_path, 'r', encoding='utf-8') as f:
        questions = yaml.safe_load(f)
    
    return questions

def get_question_by_id(question_id: str) -> Dict[str, Any]:
    """Get a specific question by its ID."""
    questions = load_questions()
    
    for question in questions:
        if question['id'] == question_id:
            return question
    
    raise ValueError(f"Question with ID '{question_id}' not found")

def get_questions_for_project_type(project_type: str) -> List[Dict[str, Any]]:
    """Get questions that apply to a specific project type."""
    questions = load_questions()
    
    filtered_questions = []
    for question in questions:
        # If no branch specified, include for all project types
        if 'branch' not in question or not question['branch']:
            filtered_questions.append(question)
        # If branch specified, check if project type is included
        elif project_type in question['branch']:
            filtered_questions.append(question)
    
    return filtered_questions 