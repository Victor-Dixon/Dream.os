#!/bin/bash
"""
FastAPI Service Setup Script for TradingRobotPlug
==================================================

Automates virtual environment setup, .env configuration, and systemd service installation.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
"""

set -e

BACKEND_DIR="backend"
VENV_DIR="venv"
PYTHON_VERSION="python3.11"

echo "🚀 TradingRobotPlug FastAPI Service Setup"
echo ""

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found: $BACKEND_DIR"
    echo "   Expected location: $(pwd)/$BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR"
echo "✅ Changed to backend directory: $(pwd)"
echo ""

# Step 1: Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_VERSION -m venv "$VENV_DIR"
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Step 2: Activate virtual environment and upgrade pip
echo ""
echo "📦 Activating virtual environment and upgrading pip..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip

# Step 3: Install dependencies
echo ""
echo "📦 Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping dependency installation"
fi

# Step 4: Configure .env file
echo ""
echo "📝 Configuring .env file..."
if [ -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created from .env.example"
    echo "⚠️  IMPORTANT: Edit .env file with actual values:"
    echo "   - DATABASE_URL"
    echo "   - ALPACA_API_KEY and ALPACA_SECRET_KEY"
    echo "   - API_SECRET_KEY and JWT_SECRET_KEY"
    echo "   - CORS_ORIGINS (for production)"
else
    if [ -f ".env" ]; then
        echo "✅ .env file already exists"
    else
        echo "⚠️  .env.example not found, .env file not created"
    fi
fi

# Step 5: Install systemd service
echo ""
echo "📋 Installing systemd service..."
if [ -f "/tmp/tradingrobotplug-fastapi.service" ]; then
    echo "   Copying service file to /etc/systemd/system/..."
    sudo cp /tmp/tradingrobotplug-fastapi.service /etc/systemd/system/
    echo "✅ Service file installed"
    
    echo "   Reloading systemd daemon..."
    sudo systemctl daemon-reload
    echo "✅ Systemd daemon reloaded"
    
    echo "   Enabling service..."
    sudo systemctl enable tradingrobotplug-fastapi
    echo "✅ Service enabled"
    
    echo ""
    echo "📋 Service installation complete!"
    echo "   To start the service: sudo systemctl start tradingrobotplug-fastapi"
    echo "   To check status: sudo systemctl status tradingrobotplug-fastapi"
    echo "   To view logs: sudo journalctl -u tradingrobotplug-fastapi -f"
else
    echo "⚠️  Service file not found at /tmp/tradingrobotplug-fastapi.service"
    echo "   Service file should have been deployed by deployment script"
fi

# Step 6: Verify health endpoint (if service is running)
echo ""
echo "🏥 Verifying health endpoint..."
if systemctl is-active --quiet tradingrobotplug-fastapi; then
    sleep 2
    if curl -s http://localhost:8001/health > /dev/null; then
        echo "✅ Health endpoint responding"
        curl -s http://localhost:8001/health | python3 -m json.tool || curl -s http://localhost:8001/health
    else
        echo "⚠️  Health endpoint not responding (service may still be starting)"
    fi
else
    echo "ℹ️  Service not running yet. Start with: sudo systemctl start tradingrobotplug-fastapi"
fi

echo ""
echo "✅ FastAPI service setup complete!"
echo ""
echo "📋 Next Steps:"
echo "   1. Edit .env file with actual configuration values"
echo "   2. Initialize database (if needed): python -c 'from database.connection import init_database; init_database()'"
echo "   3. Start service: sudo systemctl start tradingrobotplug-fastapi"
echo "   4. Verify health: curl http://localhost:8001/health"
echo "   5. Agent-7: Run endpoint verification script"

