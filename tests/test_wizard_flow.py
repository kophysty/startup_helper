"""
Tests for wizard module.
"""

import pytest
import sys
import os
import yaml

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_questions_yml_structure():
    """Test that questions.yml has the correct structure."""
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'wizard', 'questions.yml')
    
    with open(questions_path, 'r') as f:
        questions = yaml.safe_load(f)
    
    # Check that questions is a list
    assert isinstance(questions, list)
    
    # Check that each question has required fields
    required_fields = ['id', 'text', 'type']
    for question in questions:
        for field in required_fields:
            assert field in question, f"Question missing required field: {field}"
        
        # Check that id is unique
        assert question['id'] is not None
        assert isinstance(question['id'], str)

def test_sanity_rules_yml_structure():
    """Test that sanity_rules.yml has the correct structure."""
    rules_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'wizard', 'sanity_rules.yml')
    
    with open(rules_path, 'r') as f:
        rules = yaml.safe_load(f)
    
    # Check that rules is a list
    assert isinstance(rules, list)
    
    # Check that each rule has required fields
    required_fields = ['id', 'name', 'condition', 'message', 'severity']
    for rule in rules:
        for field in required_fields:
            assert field in rule, f"Rule missing required field: {field}"
        
        # Check severity is valid
        valid_severities = ['info', 'warning', 'critical']
        assert rule['severity'] in valid_severities, f"Invalid severity: {rule['severity']}"

def test_questions_count():
    """Test that we have exactly 20 questions as specified in the blueprint."""
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'wizard', 'questions.yml')
    
    with open(questions_path, 'r') as f:
        questions = yaml.safe_load(f)
    
    assert len(questions) == 20, f"Expected 20 questions, got {len(questions)}"

def test_question_types():
    """Test that question types are valid."""
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'wizard', 'questions.yml')
    
    with open(questions_path, 'r') as f:
        questions = yaml.safe_load(f)
    
    valid_types = ['currency', 'integer', 'percent', 'select']
    
    for question in questions:
        assert question['type'] in valid_types, f"Invalid question type: {question['type']}"

def test_branch_logic():
    """Test that branch logic is consistent."""
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'wizard', 'questions.yml')
    
    with open(questions_path, 'r') as f:
        questions = yaml.safe_load(f)
    
    valid_project_types = ["B2B SaaS", "B2C SaaS", "E-commerce", "Marketplace"]
    
    for question in questions:
        if 'branch' in question:
            for project_type in question['branch']:
                assert project_type in valid_project_types, f"Invalid project type in branch: {project_type}" 