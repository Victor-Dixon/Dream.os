#!/usr/bin/env python3
from src.core.message_queue_impl import MessageQueue, QueueConfig

config = QueueConfig()
mq = MessageQueue(config=config)

entries = mq.persistence.load_entries()
print('Total entries loaded:', len(entries))

print('Checking each entry status:')
for i, e in enumerate(entries):
    status = getattr(e, 'status', 'NO_STATUS_ATTR')
    print(f'  Entry {i}: status="{status}" (type: {type(status)})')
    if status == 'PENDING':
        print(f'    *** FOUND PENDING ENTRY {i} ***')

print('\nCalling _get_pending_entries:')
pending = mq._get_pending_entries(entries)
print('Pending entries returned:', len(pending))