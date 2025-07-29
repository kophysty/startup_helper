#!/bin/bash

# Startup Financial OS MVP - Linting Script

echo "🔍 Running code quality checks..."

# Run black for code formatting
echo "📝 Formatting code with black..."
black src/ tests/ streamlit_app.py

# Run ruff for linting
echo "🧹 Running ruff linter..."
ruff check src/ tests/ streamlit_app.py

# Run mypy for type checking
echo "🔍 Running type checks with mypy..."
mypy src/ tests/ streamlit_app.py

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v

echo "✅ Code quality checks completed!" 