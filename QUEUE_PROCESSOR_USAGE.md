# Message Queue Processor - Usage Guide

## Correct File Location

The message queue processor starter script is located at:
```
scripts/start_queue_processor.py
```

**NOT** `tools/start_message_queue_processor.py` (that file doesn't exist)

## How to Run

### From Project Root

```bash
# Windows PowerShell
python scripts/start_queue_processor.py

# Linux/Mac
python3 scripts/start_queue_processor.py
```

### What It Does

The queue processor:
1. Processes queued messages from the message queue
2. Delivers messages via PyAutoGUI to agent chat windows
3. Runs continuously, checking for new messages every 5 seconds
4. Processes one message at a time (batch_size=1)

### Stopping the Processor

Press **Ctrl+C** to stop the queue processor gracefully.

## Related Files

- **Processor Code**: `src/core/message_queue_processor.py` (shim)
- **Actual Implementation**: `src/core/message_queue_processor/core/processor.py`
- **Starter Script**: `scripts/start_queue_processor.py`

## Note

This will process the messages that were queued earlier (like the ones we saw queued but failing to deliver immediately). The queue processor will retry those messages when the target windows are available.

