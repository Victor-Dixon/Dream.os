#!/usr/bin/env python3
"""
FastAPI Server Runner
=====================

Standalone script to run the FastAPI application with uvicorn.
This script is used by the service manager to start FastAPI in background mode.

V2 Compliant: <300 lines
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import os
import sys
import uvicorn
import logging

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the FastAPI app for uvicorn
from src.web.fastapi_app import app

def run_fastapi_server():
    """Function to run the FastAPI server (for service manager compatibility)."""
    main()

def main():
    """Main entry point for FastAPI server."""
    try:
        logger.info("🚀 Starting FastAPI server...")

        # Import the FastAPI app
        from src.web.fastapi_app import app

        # Get configuration from environment
        host = os.getenv('FASTAPI_HOST', '0.0.0.0')
        port = int(os.getenv('FASTAPI_PORT', '8001'))

        logger.info(f"🌐 Starting server on {host}:{port}")

        # Run with uvicorn
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )

    except KeyboardInterrupt:
        logger.info("🛑 FastAPI server stopped by user")
    except Exception as e:
        logger.error(f"❌ FastAPI server failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()