#!/usr/bin/env python3
"""
Message Queue Service Launcher
===============================

Simple launcher script for the message queue processor.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.core.message_queue_processor.core.processor import main
    main()
except Exception as e:
    print(f"Failed to start message queue: {e}")
    sys.exit(1)