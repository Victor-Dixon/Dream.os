#!/usr/bin/env python3
"""
Start Message Queue Processor
==============================

Starts the message queue processor to process queued messages from Discord bot and other sources.

Usage:
    python scripts/start_queue_processor.py

The processor will run continuously, processing messages from the queue.
Press Ctrl+C to stop.
"""

import logging
from src.core.message_queue_processor import MessageQueueProcessor
import sys
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Start the message queue processor."""
    logger.info("🚀 Starting Message Queue Processor...")

    # Initialize processor
    processor = MessageQueueProcessor()

    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("🛑 Shutting down queue processor...")
        processor.running = False
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Process queue continuously
    logger.info("✅ Queue processor started. Processing messages...")
    logger.info("   Press Ctrl+C to stop")

    try:
        # Process queue with 5 second interval between batches
        processor.process_queue(
            max_messages=None,  # Unlimited
            batch_size=1,  # Process one at a time
            interval=5.0  # Check every 5 seconds
        )
    except KeyboardInterrupt:
        logger.info("🛑 Queue processor stopped by user")
    except Exception as e:
        logger.error(f"❌ Queue processor error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())




