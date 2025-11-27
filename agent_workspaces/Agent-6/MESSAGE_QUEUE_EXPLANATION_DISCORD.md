# 📬 Message Queue System - Complete Explanation

## 🎯 **WHAT IS THE MESSAGE QUEUE?**

A **persistent, priority-based queuing system** that ensures reliable message delivery between agents, Discord, and the user. Prevents race conditions when multiple sources try to send messages simultaneously.

---

## 🏗️ **ARCHITECTURE (4 Core Components)**

### **1. MessageQueue** (`src/core/message_queue.py`)
- Handles enqueue/dequeue operations
- Manages priority-based ordering
- Stores messages in `message_queue/queue.json`

### **2. MessageQueueProcessor** (`src/core/message_queue_processor.py`)
- Processes messages **sequentially** (one at a time)
- Handles delivery attempts
- Updates message status

### **3. PyAutoGUIMessagingDelivery** (`src/core/messaging_pyautogui.py`)
- Delivers messages via GUI automation
- Uses PyAutoGUI for keyboard/mouse control
- Sends to agent chat input coordinates

### **4. Keyboard Control Lock** (`src/core/keyboard_control_lock.py`)
- **CRITICAL**: Prevents "9 ppl controlling keyboard" scenario
- Global lock ensures only ONE message delivery at a time
- Prevents conflicts between Discord, agents, user

---

## 🔄 **HOW IT WORKS (Step-by-Step)**

### **STEP 1: ENQUEUE (Add Message to Queue)**

```python
queue_id = message_queue.enqueue(message_data)
```

**What Happens**:
1. Generate unique Queue ID (UUID)
2. Calculate priority score (urgent > regular)
3. Create queue entry with status `PENDING`
4. Save to `message_queue/queue.json` (atomic operation)
5. Log to message history (SSOT)
6. Track metrics

**Queue Entry**:
```json
{
  "queue_id": "uuid",
  "message": {...},
  "priority_score": 1.0,
  "status": "PENDING",
  "created_at": "2025-11-24T...",
  "updated_at": "2025-11-24T..."
}
```

---

### **STEP 2: DEQUEUE (Get Messages for Processing)**

```python
messages = message_queue.dequeue(batch_size=1)
```

**What Happens**:
1. Load queue from `message_queue/queue.json`
2. Filter messages with status `PENDING`
3. Sort by priority (highest first) using max-heap
4. Update status to `PROCESSING`
5. Save updated status (atomic)
6. Return entries to process

**Priority Algorithm**:
- Uses Python `heapq` for efficient sorting
- Processes urgent messages first
- Batch size = 1 (sequential processing)

---

### **STEP 3: PROCESSING (Delivery Attempt)**

```python
processor.process_queue()
```

**What Happens**:
1. Get next message (highest priority)
2. **Acquire Keyboard Lock** (CRITICAL - prevents race conditions)
3. Create UnifiedMessage format
4. Attempt delivery:
   - PyAutoGUI (GUI automation) - primary
   - Inbox fallback (file-based) - backup
5. Update status: `DELIVERED` or `FAILED`
6. Log to message history
7. Release keyboard lock

**Sequential Processing**:
- **One message at a time** (batch_size=1)
- Prevents keyboard conflicts
- Ensures clean delivery

---

### **STEP 4: DELIVERY (PyAutoGUI Operations)**

```python
with keyboard_control("queue_processor"):
    success = delivery.send_message(unified_message)
```

**What Happens**:
1. **Acquire Global Lock** (prevents conflicts)
2. **Focus Target Window**: Move mouse to agent's chat coordinates
3. **Clear Input**: `Ctrl+A` → `Delete`
4. **Open New Tab**: `Ctrl+T` or `Ctrl+N`
5. **Wait**: 1.0 second for tab to load
6. **Paste Content**: 
   - Fast: Clipboard paste (`Ctrl+V`)
   - Fallback: Character-by-character typing
7. **Send**: Press `Enter`
8. **Release Lock**: Free keyboard

**Timing**:
- Move: 0.5s
- Focus: 0.5s
- Tab wait: 1.0s
- Paste wait: 1.0s
- Inter-message: 0.5s

---

## 🔒 **KEYBOARD CONTROL LOCK (CRITICAL)**

### **Problem**: 
"9 ppl controlling my keyboard" - Multiple sources (Discord, agents, user) trying to send simultaneously.

### **Solution**:
```python
# Global lock for ALL keyboard operations
_keyboard_control_lock = threading.Lock()

# Context manager ensures exclusive access
with keyboard_control("source_name"):
    # Only ONE source can control keyboard here
    pyautogui.typewrite("message")
```

**Features**:
- **Global**: Single lock for entire system
- **Timeout**: 30 seconds max (prevents deadlocks)
- **Source Tracking**: Logs which source holds lock
- **Auto Release**: Context manager ensures cleanup

**Lock Timeout Handling**:
- If timeout → Try inbox fallback
- Prevents message loss
- Ensures delivery even if GUI fails

---

## 📊 **MESSAGE STATUSES**

### **Lifecycle**:
```
PENDING → PROCESSING → DELIVERED ✅
PENDING → PROCESSING → FAILED ❌
```

### **Status Meanings**:
- **PENDING**: In queue, waiting for processing
- **PROCESSING**: Currently being delivered
- **DELIVERED**: Successfully delivered
- **FAILED**: Delivery failed (with error)

**Critical**: Status is **always** updated, even on errors. Prevents messages from getting stuck.

---

## 🛡️ **RACE CONDITION PREVENTION**

### **4-Layer Protection**:

1. **Global Keyboard Lock**: Only ONE source controls keyboard
2. **Sequential Processing**: One message at a time
3. **Atomic Operations**: Thread-safe file operations
4. **Status Tracking**: Prevents duplicate processing

---

## 📁 **PERSISTENCE**

### **Storage**:
- **File**: `message_queue/queue.json`
- **Format**: JSON array of queue entries
- **Atomic**: Thread-safe operations

### **Queue File Structure**:
```json
[
  {
    "queue_id": "uuid",
    "message": {
      "sender": "Agent-4",
      "recipient": "Agent-6",
      "content": "Message text",
      "priority": "urgent"
    },
    "priority_score": 1.0,
    "status": "PENDING",
    "created_at": "2025-11-24T...",
    "updated_at": "2025-11-24T..."
  }
]
```

---

## 🚨 **ERROR HANDLING**

### **Delivery Failures**:
1. **PyAutoGUI Error** → Try inbox fallback
2. **Lock Timeout** → Try inbox fallback
3. **Any Exception** → Try inbox fallback
4. **Status Always Updated** → Even on failure

### **Inbox Fallback**:
- If GUI delivery fails → Write to inbox file
- Ensures message is never lost
- File-based delivery as backup

---

## 📈 **METRICS & MONITORING**

### **Tracked Metrics**:
- `queue.enqueued` - Messages added
- `queue.deliveries.success` - Successful deliveries
- `queue.deliveries.failed` - Failed deliveries
- `queue.size` - Current queue size
- `queue.processing` - Processing duration

### **Statistics**:
- Queue size
- Messages by status
- Average processing time
- Success/failure rates

---

## 🔧 **CONFIGURATION**

```python
QueueConfig(
    queue_directory="message_queue",
    max_queue_size=1000,
    processing_batch_size=1,  # Sequential
    max_age_days=7,
    cleanup_interval=3600
)
```

---

## 📋 **USAGE**

### **Enqueue**:
```python
queue_id = queue.enqueue({
    "sender": "Agent-4",
    "recipient": "Agent-6",
    "content": "Hello!",
    "priority": "urgent"
})
```

### **Process**:
```python
processor = MessageQueueProcessor()
processor.process_queue()  # Processes all messages
```

### **Check Status**:
```python
status = queue.get_entry_status(queue_id)
# Returns: "PENDING", "PROCESSING", "DELIVERED", or "FAILED"
```

---

## 🎯 **KEY FEATURES**

✅ **Priority-Based**: Urgent messages first  
✅ **Persistent**: Survives restarts  
✅ **Thread-Safe**: Atomic operations  
✅ **Race Condition Free**: Global keyboard lock  
✅ **Reliable**: Inbox fallback  
✅ **Trackable**: Full history & metrics  
✅ **Scalable**: Handles 1000+ messages  

---

## 🐝 **WE. ARE. SWARM.**

**Status**: ✅ **EXPLANATION COMPLETE**  
**Tool**: Message Queue System  
**Purpose**: Reliable message delivery with race condition prevention


