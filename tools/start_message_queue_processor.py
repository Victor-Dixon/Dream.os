#!/usr/bin/env python3
"""
Start Message Queue Processor (Tools Directory Wrapper)
========================================================

Convenience wrapper for starting the message queue processor from the tools directory.
This script delegates to the main script in scripts/start_queue_processor.py

Usage:
    python tools/start_message_queue_processor.py
    OR
    python scripts/start_queue_processor.py

The processor will run continuously, processing messages from the queue.
Press Ctrl+C to stop.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import and run the main script
if __name__ == "__main__":
    # Import the main function from the scripts directory
    import importlib.util
    script_path = project_root / "scripts" / "start_queue_processor.py"
    
    if not script_path.exists():
        print(f"❌ Error: Script not found at {script_path}")
        sys.exit(1)
    
    spec = importlib.util.spec_from_file_location("start_queue_processor", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Run the main function
    sys.exit(module.main())
