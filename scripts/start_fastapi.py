#!/usr/bin/env python3
"""
FastAPI Service Launcher
========================

Simple launcher script for the FastAPI service.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.web.fastapi_app import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
except Exception as e:
    print(f"Failed to start FastAPI service: {e}")
    sys.exit(1)