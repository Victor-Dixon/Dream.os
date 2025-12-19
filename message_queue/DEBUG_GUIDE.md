# Message Queue Debugging Guide

## Current Status

Based on the codebase analysis, here are the key components and potential issues:

### Components
1. **Message Queue Core** (`src/core/message_queue.py`)
   - Main queue implementation with retry logic
   - Handles PENDING, PROCESSING, DELIVERED, FAILED states
   - Has retry backoff for failed messages

2. **Queue Processor** (`src/core/message_queue_processor/`)
   - Modular processor with error handling
   - Handles delivery via PyAutoGUI and inbox fallback

3. **Persistence Layer** (`src/core/message_queue_persistence.py`)
   - File-based JSON storage
   - Has Windows file locking retry logic (8 retries, exponential backoff)
   - Handles corrupted file recovery

### Common Issues

#### 1. File Locking (Windows)
**Symptoms:**
- PermissionError when accessing queue.json
- "File is already in use" errors
- Queue processor can't save entries

**Causes:**
- Multiple queue processor instances running
- File handle not released properly
- Windows file locking behavior

**Solutions:**
```bash
# Check for multiple processes
Get-Process python | Where-Object {$_.CommandLine -like "*queue*"}

# Kill stuck processes
Stop-Process -Name python -Force

# Restart queue processor
python tools/start_message_queue_processor.py
```

#### 2. Corrupted Queue File
**Symptoms:**
- JSON decode errors
- Queue file exists but can't be parsed
- Entries missing required fields

**Solutions:**
- Check `message_queue/backups/` for backup files
- Queue persistence has auto-recovery for corrupted files
- Manual recovery: Copy from most recent backup

#### 3. Stuck Messages
**Symptoms:**
- Messages in PROCESSING status for > 5 minutes
- Queue not processing new messages
- High number of PROCESSING entries

**Solutions:**
```python
# Use error monitor to reset stuck messages
from src.core.message_queue_error_monitor import MessageQueueErrorMonitor
monitor = MessageQueueErrorMonitor()
monitor.reset_stuck_messages()
```

#### 4. Silent Failures
**Symptoms:**
- Messages queued but never delivered
- No error logs
- Queue appears to be processing but messages don't arrive

**Debug Steps:**
1. Check queue status:
   ```python
   from src.core.message_queue import MessageQueue
   queue = MessageQueue()
   stats = queue.get_statistics()
   print(stats)
   ```

2. Check health:
   ```python
   health = queue.get_health_status()
   print(health)
   ```

3. Check error monitor:
   ```python
   from src.core.message_queue_error_monitor import MessageQueueErrorMonitor
   monitor = MessageQueueErrorMonitor()
   alerts = monitor.check_all()
   print(alerts)
   ```

### Debugging Tools

#### 1. Quick Debug Script
```bash
python tools/debug_queue.py
```
Shows:
- Queue file status
- Entry counts by status
- Stuck messages
- Failed messages
- Recent activity

#### 2. Full Diagnostic
```bash
python tools/diagnose_message_queue.py
```
Shows:
- Detailed queue analysis
- Log file analysis
- Error patterns
- Recommendations

#### 3. Error Monitor
```python
from src.core.message_queue_error_monitor import MessageQueueErrorMonitor

monitor = MessageQueueErrorMonitor()
alerts = monitor.check_all()
print(json.dumps(alerts, indent=2))
```

### Queue File Location
- **Main queue**: `message_queue/queue.json`
- **Backups**: `message_queue/backups/queue_YYYYMMDD_HHMMSS_corrupted.json`
- **Metrics**: `message_queue/metrics.json`
- **Alerts**: `message_queue/alerts.json` (if error monitor enabled)

### Manual Queue Inspection

If you need to manually inspect the queue:

```python
import json
from pathlib import Path

queue_file = Path("message_queue/queue.json")
if queue_file.exists():
    with open(queue_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total entries: {len(data)}")
    for entry in data[:10]:  # First 10 entries
        print(f"ID: {entry.get('queue_id')[:16]}...")
        print(f"  Status: {entry.get('status')}")
        print(f"  Recipient: {entry.get('message', {}).get('recipient', 'unknown')}")
        print(f"  Created: {entry.get('created_at', 'unknown')[:19]}")
        print()
```

### Reset Options

#### Reset Stuck Messages
```python
from src.core.message_queue_error_monitor import MessageQueueErrorMonitor
monitor = MessageQueueErrorMonitor()
monitor.reset_stuck_messages()
```

#### Resend Failed Messages
```python
from src.core.message_queue import MessageQueue
queue = MessageQueue()
resent = queue.resend_failed_messages(max_messages=10)
print(f"Reset {resent} failed messages for retry")
```

#### Clear Queue (DANGER - loses all messages)
```python
from pathlib import Path
import shutil
from datetime import datetime

queue_file = Path("message_queue/queue.json")
if queue_file.exists():
    # Backup first
    backup = queue_file.parent / f"queue_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(queue_file, backup)
    
    # Clear queue
    with open(queue_file, 'w') as f:
        json.dump([], f)
    print(f"Queue cleared. Backup saved to {backup}")
```

### Next Steps

1. **Run debug script** to see current state
2. **Check for stuck processes** that might be locking files
3. **Review error logs** in `logs/` directory
4. **Use error monitor** to identify specific issues
5. **Check queue processor logs** if running

### Key Files to Check

- `message_queue/queue.json` - Main queue file
- `message_queue/backups/` - Corrupted file backups
- `logs/queue_processor.log` - Processor logs (if exists)
- `src/core/message_queue_persistence.py` - Persistence logic
- `src/core/message_queue_error_monitor.py` - Error detection

