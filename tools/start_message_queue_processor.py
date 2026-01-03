#!/usr/bin/env python3
"""
Message Queue Processor Startup Script
=====================================

Starts the message queue processor directly.

V2 Compliance | Author: Agent-2 | Date: 2026-01-01
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    try:
        # Use direct imports with fallback logic
        try:
            # Try importing from the package structure
            from src.core.message_queue import MessageQueue, QueueConfig
        except ImportError:
            # Fallback: import classes directly
            import sys
            import os
            project_root = os.path.dirname(os.path.dirname(__file__))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

            # Import the module directly and get classes
            import src.core.message_queue_impl as mq_module
            MessageQueue = mq_module.MessageQueue
            QueueConfig = mq_module.QueueConfig

        from src.core.message_queue_interfaces import IMessageQueue
        from src.core.message_queue.core.processor import MessageQueueProcessor

        print("✅ MessageQueueProcessor imported successfully")

        # Create and start processor
        config = QueueConfig()
        queue = MessageQueue(config=config)
        processor = MessageQueueProcessor(queue=queue, config=config)
        print("✅ MessageQueueProcessor initialized")

        # Start processing (this will run indefinitely)
        print("🚀 Starting message queue processing...")
        processed = processor.process_queue()
        print(f"✅ Processing complete: {processed} messages handled")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)