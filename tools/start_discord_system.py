#!/usr/bin/env python3
"""
Start Discord System
===================

Starts both the Discord bot and message queue processor.

Author: Agent-6 (Coordination & Communication Specialist)
Created: 2025-12-21
License: MIT
<!-- SSOT Domain: tools -->
"""

import subprocess
import sys
import time
from pathlib import Path

def main():
    """Start Discord bot and queue processor."""
    project_root = Path(__file__).parent.parent
    
    print("🚀 Starting Discord System...")
    print("=" * 60)
    
    # Start message queue processor
    print("📬 Starting message queue processor...")
    queue_processor = subprocess.Popen(
        [sys.executable, "-m", "src.core.message_queue_processor"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"✅ Queue processor started (PID: {queue_processor.pid})")
    
    # Wait a moment for queue processor to initialize
    time.sleep(2)
    
    # Start Discord bot
    print("🤖 Starting Discord bot...")
    bot_process = subprocess.Popen(
        [sys.executable, "-m", "src.discord_commander.bot_runner"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"✅ Discord bot started (PID: {bot_process.pid})")
    
    print("\n✅ Discord system started successfully!")
    print("   - Message queue processor: Running")
    print("   - Discord bot: Running")
    print("\n🛑 Press Ctrl+C to stop both processes")
    
    try:
        # Wait for both processes
        queue_processor.wait()
        bot_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping Discord system...")
        queue_processor.terminate()
        bot_process.terminate()
        queue_processor.wait()
        bot_process.wait()
        print("✅ Discord system stopped")

if __name__ == "__main__":
    main()





