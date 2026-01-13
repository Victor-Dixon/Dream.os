#!/usr/bin/env python3
"""
FastAPI Service Launcher
========================

Proper launcher script for the FastAPI service.
"""

import sys
import os
import logging
import uvicorn

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Start the FastAPI server."""
    try:
        from src.web.fastapi_app import app

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
        )

        logger = logging.getLogger(__name__)
        logger.info("🚀 Starting FastAPI server...")

        # Start server with proper configuration
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            log_level="info",
            access_log=True,
            workers=1  # Single worker for development
        )

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Failed to start FastAPI service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()