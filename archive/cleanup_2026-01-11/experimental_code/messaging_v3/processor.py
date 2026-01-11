#!/usr/bin/env python3
"""
Background Message Processor - Clean and Simple
"""

import logging
import time
import signal
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(parent_dir))

from queue import MessageQueue
from delivery import send_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageProcessor:
    """Background message processor."""

    def __init__(self, queue: MessageQueue = None):
        self.queue = queue or MessageQueue()
        self.running = False

    def process_batch(self, batch_size: int = 5) -> int:
        """Process a batch of messages."""
        messages = self.queue.dequeue(batch_size)

        if not messages:
            return 0

        success_count = 0
        for msg in messages:
            try:
                if send_message(msg.recipient, msg.content, msg.sender):
                    success_count += 1
                    logger.info(f"✅ Delivered to {msg.recipient}")
                else:
                    logger.error(f"❌ Failed to deliver to {msg.recipient}")

                # Small delay between messages to prevent overwhelming
                time.sleep(1.0)

            except Exception as e:
                logger.error(f"❌ Error processing message to {msg.recipient}: {e}")

        return success_count

    def run_forever(self, interval: float = 5.0, batch_size: int = 3):
        """Run processor continuously."""
        self.running = True
        logger.info("🚀 Message processor started")

        def signal_handler(signum, frame):
            logger.info("🛑 Received shutdown signal")
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            while self.running:
                processed = self.process_batch(batch_size)
                if processed > 0:
                    logger.info(f"📊 Processed {processed} messages")

                if processed == 0:
                    time.sleep(interval)  # Wait before checking again

        except KeyboardInterrupt:
            logger.info("🛑 Stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            return 1

        logger.info("✅ Message processor stopped")
        return 0


def main():
    """Main entry point."""
    processor = MessageProcessor()
    return processor.run_forever()


if __name__ == "__main__":
    sys.exit(main())