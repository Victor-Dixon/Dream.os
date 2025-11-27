#!/usr/bin/env python3
"""Check queue status."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.message_queue import MessageQueue

q = MessageQueue()
stats = q.get_statistics()
print('Queue Status:')
print(f'  Pending: {stats.get("pending", 0)}')
print(f'  Processing: {stats.get("processing", 0)}')
print(f'  Delivered: {stats.get("delivered", 0)}')
print(f'  Failed: {stats.get("failed", 0)}')

