#!/usr/bin/env python3
"""
Mock Discord Bot - Processes Queued Messages
==============================================

This script simulates a Discord bot to process queued messages
without requiring actual Discord credentials. It reads messages
from the unified messaging queue and "delivers" them.

Useful for development and testing when Discord credentials are not available.

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-09
"""

import time
import json
import sys
from pathlib import Path
from typing import Dict, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockDiscordBot:
    """Mock Discord bot that processes queued messages."""

    def __init__(self):
        self.queue_dir = Path("ops/messaging/message_queue")
        self.processed_dir = Path("ops/messaging/processed")
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.running = False

    def start(self):
        """Start the mock Discord bot."""
        logger.info("🤖 Mock Discord Bot Starting...")
        logger.info("📨 Processing queued messages...")

        self.running = True
        processed_count = 0

        try:
            while self.running:
                messages_processed = self._process_queued_messages()
                if messages_processed > 0:
                    processed_count += messages_processed
                    logger.info(f"✅ Processed {messages_processed} messages (total: {processed_count})")
                else:
                    logger.debug("📭 No messages in queue, waiting...")
                    time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            logger.info("🛑 Mock Discord Bot stopped by user")
        except Exception as e:
            logger.error(f"❌ Mock Discord Bot error: {e}")
        finally:
            logger.info(f"🏁 Mock Discord Bot finished. Total messages processed: {processed_count}")

    def stop(self):
        """Stop the mock Discord bot."""
        logger.info("🛑 Stopping Mock Discord Bot...")
        self.running = False

    def _process_queued_messages(self) -> int:
        """Process messages from the queue."""
        if not self.queue_dir.exists():
            return 0

        processed = 0

        # Look for message files
        for queue_file in self.queue_dir.glob("*.json"):
            try:
                with open(queue_file, 'r') as f:
                    message_data = json.load(f)

                # "Deliver" the message (log it)
                self._deliver_message(message_data)

                # Move to processed directory
                processed_file = self.processed_dir / queue_file.name
                queue_file.rename(processed_file)

                processed += 1
                logger.info(f"📨 Delivered message: {message_data.get('content', '')[:50]}...")

            except Exception as e:
                logger.error(f"❌ Error processing message {queue_file}: {e}")

        return processed

    def _deliver_message(self, message_data: Dict):
        """Simulate delivering a message to Discord."""
        recipient = message_data.get('recipient', 'unknown')
        content = message_data.get('content', '')
        priority = message_data.get('priority', 'normal')
        sender = message_data.get('sender', 'unknown')

        # Log the "delivery"
        logger.info(f"📤 [MOCK DELIVERY] {sender} -> {recipient}: {content[:100]}{'...' if len(content) > 100 else ''}")
        logger.info(f"   Priority: {priority}")
        logger.info(f"   Tags: {message_data.get('tags', [])}")

        # In a real Discord bot, this would send to Discord API
        # For mock, we just log it

def create_pid_file(pid: int) -> None:
    """Create the discord.pid file."""
    pid_dir = Path("pids")
    pid_dir.mkdir(exist_ok=True)
    pid_file = pid_dir / "discord.pid"

    with open(pid_file, 'w') as f:
        f.write(str(pid))

    logger.info(f"✅ Created discord.pid with PID: {pid}")

def main():
    """Main entry point."""
    import sys
    import subprocess

    logger.info("🤖 Starting Mock Discord Bot...")

    try:
        # Start the mock bot in background
        process = subprocess.Popen(
            [sys.executable, __file__, "run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path.cwd()
        )

        # Create PID file
        create_pid_file(process.pid)

        logger.info("✅ Mock Discord bot launched successfully!")
        logger.info(f"📝 Process ID: {process.pid}")
        logger.info(f"📝 PID file: pids/discord.pid")
        logger.info("📨 Bot will process queued messages every 5 seconds")

        return 0

    except Exception as e:
        logger.error(f"❌ Failed to launch mock Discord bot: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # Run the bot
        bot = MockDiscordBot()
        bot.start()
    else:
        # Launch the bot
        sys.exit(main())