#!/bin/bash
# Trading Robot Virtual Environment Setup Script
# Generated: 2025-12-20
# Author: Agent-3 (Infrastructure & DevOps Specialist)

set -e

echo "🚀 Setting up Trading Robot virtual environment..."

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

echo "📍 Using Python: $($PYTHON_CMD --version)"

# Create virtual environment
echo "📦 Creating virtual environment in venv..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
