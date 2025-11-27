# Queue-Based Messaging Architecture

**Status**: ✅ IMPLEMENTED  
**Date**: 2025-01-28  
**Author**: Agent-7 (Web Development Specialist)

---

## **Overview**

All messaging logic now routes through the message queue to prevent race conditions and ensure proper PyAutoGUI orchestration. This ensures that only one operation controls the keyboard at a time, preventing the "9 ppl controlling my keyboard" scenario.

---

## **Architecture Flow**

### **Message Flow**:
```
Caller → MessageCoordinator → MessageQueue → QueueProcessor → PyAutoGUI (with keyboard lock)
```

### **Key Components**:

1. **MessageCoordinator** (`src/services/messaging_infrastructure.py`)
   - **ALL** messages route through the queue
   - `send_to_agent()`: Enqueues single messages
   - `broadcast_to_all()`: Enqueues messages for all agents
   - Provides fallback to direct send only if queue unavailable

2. **MessageQueue** (`src/core/message_queue.py`)
   - Persistent queue storage
   - FIFO ordering
   - Retry logic for failed deliveries

3. **MessageQueueProcessor** (`src/core/message_queue_processor.py`)
   - Processes queued messages sequentially
   - **CRITICAL**: Uses `keyboard_control` lock for entire PyAutoGUI operation
   - Ensures only one message delivery at a time
   - Fallback to inbox file delivery if PyAutoGUI fails

4. **KeyboardControlLock** (`src/core/keyboard_control_lock.py`)
   - Global lock for ALL keyboard/mouse operations
   - Prevents concurrent PyAutoGUI operations
   - Timeout protection (30s default)

---

## **Race Condition Prevention**

### **Before (Race Conditions)**:
- Multiple callers → Direct `send_message()` → Concurrent PyAutoGUI operations
- Discord, CLI, agents all trying to control keyboard simultaneously
- Messages could overlap or fail silently

### **After (Sequential Processing)**:
- Multiple callers → Queue → Sequential processing → One PyAutoGUI operation at a time
- Keyboard lock ensures exclusive access
- Messages processed in order (FIFO)

---

## **Usage Examples**

### **Via CLI**:
```bash
python -m src.services.messaging_cli --agent Agent-5 --message "Hello"
```
**Flow**: CLI → `handle_message()` → `MessageCoordinator.send_to_agent()` → Queue → Processor

### **Via Python Code**:
```python
from src.services.messaging_infrastructure import MessageCoordinator

# Single message
MessageCoordinator.send_to_agent("Agent-5", "Hello")

# Broadcast
MessageCoordinator.broadcast_to_all("System update", priority=UnifiedMessagePriority.URGENT)
```

### **Queue Processing**:
```bash
# Start queue processor (processes queued messages)
python -m src.core.message_queue_processor
```

---

## **Keyboard Lock Integration**

The queue processor wraps each PyAutoGUI delivery in a `keyboard_control` context:

```python
with keyboard_control(f"queue_delivery::{recipient}"):
    ok = send_message(...)
```

This ensures:
- Only one PyAutoGUI operation at a time
- Timeout protection (prevents deadlocks)
- Proper cleanup on errors

---

## **Benefits**

1. **Race Condition Prevention**: Sequential processing eliminates concurrent keyboard operations
2. **Reliability**: Queue persistence means messages aren't lost if system crashes
3. **Retry Logic**: Failed messages can be retried automatically
4. **Observability**: Queue statistics and health monitoring
5. **Scalability**: Can handle bursts of messages without overwhelming the system

---

## **Migration Notes**

### **What Changed**:
- `MessageCoordinator.send_to_agent()` now enqueues instead of calling `send_message()` directly
- `MessageCoordinator.broadcast_to_all()` now enqueues all messages
- Direct `send_message()` calls are deprecated (use MessageCoordinator)

### **Backward Compatibility**:
- Fallback to direct send if queue unavailable (for development/debugging)
- Existing code using `MessageCoordinator` automatically benefits from queue

---

## **Testing**

### **Verify Queue Processing**:
```bash
# 1. Enqueue a message
python -m src.services.messaging_cli --agent Agent-5 --message "Test"

# 2. Check queue (should show pending message)
ls message_queue/

# 3. Process queue
python -m src.core.message_queue_processor 1

# 4. Verify message delivered (check inbox or chat)
```

---

## **Future Enhancements**

1. **Priority Processing**: Urgent messages processed before regular messages
2. **Batch Processing**: Process multiple messages in one keyboard lock session
3. **Delivery Confirmation**: Wait for delivery confirmation before marking as delivered
4. **Dead Letter Queue**: Handle messages that fail after max retries

---

*Last Updated: 2025-01-28*

