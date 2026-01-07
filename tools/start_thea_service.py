#!/usr/bin/env python3
"""
Thea Service Startup Script
===========================

Starts the Thea HTTP service for AI guidance.

Usage:
    python tools/start_thea_service.py                    # Start on localhost:8002
    python tools/start_thea_service.py --port 8003        # Custom port
    python tools/start_thea_service.py --host 0.0.0.0    # Bind to all interfaces

Author: Agent-6 (Quality Assurance & Deployment)
"""

import asyncio
import sys
import signal
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from services.thea_http_service import create_thea_http_service

async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Start Thea HTTP Service")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8002,
        help="Port to bind to (default: 8002)"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # Set up logging
    import logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting Thea HTTP Service...")
    logger.info(f"📍 Binding to {args.host}:{args.port}")

    # Create and start service
    service = create_thea_http_service(args.host, args.port)

    # Handle graceful shutdown
    def signal_handler(signum, frame):
        logger.info("🛑 Shutdown signal received")
        # Note: uvicorn handles shutdown gracefully

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await service.start_service()
    except KeyboardInterrupt:
        logger.info("✅ Service stopped by user")
    except Exception as e:
        logger.error(f"❌ Service error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)