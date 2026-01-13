# 📬 Message Queue System - Detailed Explanation

**Date**: 2025-11-24  
**Agent**: Agent-6 (Coordination & Communication Specialist)  
**Purpose**: Comprehensive explanation of message queue system  
**Status**: ✅ **COMPLETE**

---

## 🎯 **OVERVIEW**

The Message Queue System is a **persistent, priority-based queuing system** that ensures reliable message delivery between agents, Discord, and the user. It prevents race conditions when multiple sources try to send messages simultaneously.

---

## 🏗️ **ARCHITECTURE**

### **Core Components**:

1. **MessageQueue** (`src/core/message_queue.py`)
   - Handles enqueue/dequeue operations
   - Manages priority-based ordering
   - Provides persistence layer

2. **MessageQueueProcessor** (`src/core/message_queue_processor.py`)
   - Processes messages sequentially
   - Handles delivery attempts
   - Manages status updates

3. **PyAutoGUIMessagingDelivery** (`src/core/messaging_pyautogui.py`)
   - Delivers messages via GUI automation
   - Uses PyAutoGUI for keyboard/mouse control

4. **Keyboard Control Lock** (`src/core/keyboard_control_lock.py`)
   - **CRITICAL**: Prevents race conditions
   - Ensures only ONE message delivery at a time

5. **FileQueuePersistence** (`src/core/message_queue_persistence.py`)
   - Stores queue state in `message_queue/queue.json`
   - Atomic operations for thread safety

---

## 🔄 **MESSAGE FLOW**

### **Step 1: Enqueue (Adding Message to Queue)**

```python
# Message is added to queue
queue_id = message_queue.enqueue(message_data)
```

**What Happens**:
1. **Generate Queue ID**: Unique UUID for tracking
2. **Calculate Priority**: Based on message priority (urgent > regular)
3. **Create Queue Entry**: 
   - Status: `PENDING`
   - Priority score calculated
   - Timestamp recorded
4. **Atomic Save**: Write to `message_queue/queue.json`
5. **Log to History**: Save to message repository (SSOT)
6. **Track Metrics**: Update BI metrics

**Queue Entry Structure**:
```json
{
  "queue_id": "uuid-here",
  "message": {...},
  "priority_score": 1.0,
  "status": "PENDING",
  "created_at": "2025-11-24T...",
  "updated_at": "2025-11-24T...",
  "metadata": {...}
}
```

---

### **Step 2: Dequeue (Getting Messages for Processing)**

```python
# Get next messages for processing
messages = message_queue.dequeue(batch_size=1)
```

**What Happens**:
1. **Load Queue**: Read from `message_queue/queue.json`
2. **Filter PENDING**: Only get messages with status `PENDING`
3. **Priority Sort**: Use max-heap to get highest priority first
4. **Update Status**: Change status to `PROCESSING`
5. **Atomic Save**: Write updated status back to file
6. **Return Entries**: Return list of entries to process

**Priority Algorithm**:
- Uses Python `heapq` for efficient priority queue
- Negates priority scores (max-heap via min-heap)
- Processes highest priority messages first

---

### **Step 3: Processing (Delivery Attempt)**

```python
# Process queue sequentially
processor.process_queue()
```

**What Happens**:
1. **Get Next Message**: Dequeue highest priority message
2. **Acquire Keyboard Lock**: **CRITICAL** - Prevents race conditions
3. **Create Unified Message**: Convert queue entry to UnifiedMessage format
4. **Attempt Delivery**: 
   - PyAutoGUI delivery (GUI automation)
   - Or inbox fallback (file-based)
5. **Update Status**: Mark as `DELIVERED` or `FAILED`
6. **Log Results**: Save to message history
7. **Release Lock**: Free keyboard for next message

**Sequential Processing**:
- **One message at a time** (batch_size=1 by default)
- Prevents "9 ppl controlling keyboard" scenario
- Ensures clean delivery without interference

---

### **Step 4: Delivery (PyAutoGUI)**

```python
# Deliver message via PyAutoGUI
with keyboard_control("queue_processor"):
    success = delivery.send_message(unified_message)
```

**What Happens**:
1. **Acquire Global Lock**: Keyboard control lock prevents conflicts
2. **Focus Target Window**: Move mouse to agent's chat input coordinates
3. **Clear Input**: `Ctrl+A` → `Delete` to clear existing text
4. **Open New Tab/Window**: `Ctrl+T` or `Ctrl+N` (configurable)
5. **Wait for Tab**: 1.0 second delay for tab to load
6. **Paste Content**: 
   - Fast method: Clipboard paste (`Ctrl+V`)
   - Fallback: Character-by-character typing
7. **Send Message**: Press `Enter` to submit
8. **Release Lock**: Free keyboard for next operation

**Timing**:
- Move duration: 0.5 seconds
- Focus stabilization: 0.5 seconds
- Tab creation wait: 1.0 seconds
- Paste wait: 1.0 seconds
- Inter-message delay: 0.5 seconds

---

## 🔒 **KEYBOARD CONTROL LOCK**

### **Purpose**:
Prevents race conditions when:
- Discord bot sends message
- User types manually
- Multiple agents send messages
- Queue processor delivers messages

### **How It Works**:
```python
# Global lock for ALL keyboard operations
_keyboard_control_lock = threading.Lock()

# Context manager ensures exclusive access
with keyboard_control("source_name"):
    # Only ONE source can control keyboard here
    pyautogui.typewrite("message")
```

**Lock Features**:
- **Global**: Single lock for entire system
- **Timeout**: 30 seconds max wait (prevents deadlocks)
- **Source Tracking**: Logs which source holds lock
- **Automatic Release**: Context manager ensures cleanup

**Lock Timeout Handling**:
- If lock timeout occurs → Try inbox fallback
- Prevents messages from being lost
- Ensures delivery even if GUI automation fails

---

## 📊 **MESSAGE STATUSES**

### **Status Lifecycle**:

1. **PENDING** → Message in queue, waiting for processing
2. **PROCESSING** → Currently being delivered
3. **DELIVERED** → Successfully delivered
4. **FAILED** → Delivery failed (with error message)

### **Status Transitions**:

```
PENDING → PROCESSING → DELIVERED ✅
PENDING → PROCESSING → FAILED ❌
```

**Critical**: Status is **always** updated, even on errors. Prevents messages from getting stuck in `PROCESSING`.

---

## 🛡️ **RACE CONDITION PREVENTION**

### **Problem**: 
"9 ppl controlling my keyboard" - Multiple sources trying to send messages simultaneously.

### **Solution**:

1. **Global Keyboard Lock**:
   - Single lock for ALL keyboard operations
   - Only ONE source can control keyboard at a time
   - Prevents conflicts between Discord, agents, user

2. **Sequential Processing**:
   - Queue processor handles ONE message at a time
   - No parallel delivery attempts
   - Clean, predictable delivery

3. **Atomic Operations**:
   - Queue file operations are atomic
   - Prevents corruption from concurrent access
   - Thread-safe persistence layer

4. **Status Tracking**:
   - Messages marked `PROCESSING` during delivery
   - Prevents duplicate processing
   - Ensures status always updated

---

## 📁 **PERSISTENCE**

### **Storage**:
- **File**: `message_queue/queue.json`
- **Format**: JSON array of queue entries
- **Atomic Operations**: Thread-safe file operations

### **Queue Entry Structure**:
```json
{
  "queue_id": "uuid",
  "message": {
    "sender": "Agent-4",
    "recipient": "Agent-6",
    "content": "Message text",
    "priority": "urgent",
    "type": "text"
  },
  "priority_score": 1.0,
  "status": "PENDING",
  "created_at": "2025-11-24T...",
  "updated_at": "2025-11-24T...",
  "metadata": {
    "delivery_callback": false
  }
}
```

### **Persistence Operations**:
- **Load**: Read entire queue from file
- **Save**: Write entire queue to file (atomic)
- **Atomic**: Operations wrapped in file locking

---

## 🔄 **RETRY MECHANISM**

### **Failed Messages**:
- Status set to `FAILED`
- Error message stored in metadata
- Delivery attempts counter incremented

### **Retry Logic**:
- Currently: Manual retry (not automatic)
- Future: Exponential backoff retry
- Max attempts: Configurable (default: 3)

---

## 📈 **METRICS & MONITORING**

### **BI Integration**:
- **Metrics Tracked**:
  - `queue.enqueued` - Messages added to queue
  - `queue.deliveries.success` - Successful deliveries
  - `queue.deliveries.failed` - Failed deliveries
  - `queue.size` - Current queue size
  - `queue.processing` - Processing duration

### **Statistics**:
- Queue size
- Messages by status
- Average processing time
- Success/failure rates

### **Health Monitoring**:
- Queue depth
- Processing backlog
- Error rates
- Stuck messages detection

---

## 🚨 **ERROR HANDLING**

### **Delivery Failures**:
1. **PyAutoGUI Error**: Try inbox fallback
2. **Lock Timeout**: Try inbox fallback
3. **Any Exception**: Try inbox fallback
4. **Status Always Updated**: Even on failure

### **Inbox Fallback**:
- If GUI delivery fails → Write to inbox file
- Ensures message is never lost
- File-based delivery as backup

### **Error Logging**:
- All errors logged to message history
- Error messages stored in queue entry metadata
- Debug logging for troubleshooting

---

## 🔧 **CONFIGURATION**

### **QueueConfig**:
```python
QueueConfig(
    queue_directory="message_queue",
    max_queue_size=1000,
    processing_batch_size=10,
    max_age_days=7,
    retry_base_delay=1.0,
    retry_max_delay=300.0,
    cleanup_interval=3600
)
```

### **Key Settings**:
- **max_queue_size**: Maximum messages in queue (1000)
- **processing_batch_size**: Messages per batch (default: 1 for sequential)
- **max_age_days**: Auto-cleanup after 7 days
- **cleanup_interval**: Cleanup every hour

---

## 📋 **USAGE EXAMPLES**

### **Enqueue Message**:
```python
from src.core.message_queue import MessageQueue

queue = MessageQueue()
queue_id = queue.enqueue({
    "sender": "Agent-4",
    "recipient": "Agent-6",
    "content": "Hello Agent-6!",
    "priority": "urgent",
    "type": "text"
})
```

### **Process Queue**:
```python
from src.core.message_queue_processor import MessageQueueProcessor

processor = MessageQueueProcessor()
processor.process_queue()  # Processes all messages
```

### **Check Status**:
```python
status = queue.get_entry_status(queue_id)
# Returns: "PENDING", "PROCESSING", "DELIVERED", or "FAILED"
```

### **Get Statistics**:
```python
stats = queue.get_statistics()
# Returns: Queue size, status breakdown, metrics
```

---

## 🎯 **KEY FEATURES**

1. **Priority-Based**: Urgent messages processed first
2. **Persistent**: Queue survives restarts
3. **Thread-Safe**: Atomic operations prevent corruption
4. **Race Condition Free**: Global keyboard lock
5. **Reliable**: Inbox fallback if GUI fails
6. **Trackable**: Full message history and metrics
7. **Scalable**: Handles 1000+ messages

---

## 🐝 **WE. ARE. SWARM.**

**Status**: ✅ **EXPLANATION COMPLETE**  
**Next**: Post to Discord channel

**Agent-6 (Coordination & Communication Specialist)**  
**Message Queue System Explanation - 2025-11-24**

