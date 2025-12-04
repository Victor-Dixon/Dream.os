#!/usr/bin/env python3
"""
Capture Twitch Bot Output
=========================

Runs the bot and captures all output for debugging.
"""

import sys
import subprocess
import time
from pathlib import Path

project_root = Path(__file__).parent.parent
output_file = project_root / "twitch_bot_debug_output.txt"

print("=" * 60)
print("🔍 CAPTURING TWITCH BOT OUTPUT")
print("=" * 60)
print(f"Output will be saved to: {output_file}")
print()
print("Starting bot... (will run for 30 seconds)")
print("=" * 60)
print()

try:
    with open(output_file, "w", encoding="utf-8") as f:
        process = subprocess.Popen(
            [sys.executable, str(project_root / "tools" / "START_CHAT_BOT_NOW.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Capture output for 30 seconds
        start_time = time.time()
        while time.time() - start_time < 30:
            if process.poll() is not None:
                # Process ended
                break
            
            line = process.stdout.readline()
            if line:
                print(line.rstrip())
                f.write(line)
                f.flush()
            
            time.sleep(0.1)
        
        # Terminate if still running
        if process.poll() is None:
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
    
    print()
    print("=" * 60)
    print(f"✅ Output captured to: {output_file}")
    print("=" * 60)
    
except KeyboardInterrupt:
    print("\n⚠️ Interrupted by user")
    if 'process' in locals():
        process.terminate()
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

