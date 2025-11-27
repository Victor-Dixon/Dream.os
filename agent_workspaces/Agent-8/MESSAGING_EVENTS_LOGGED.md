# 📋 Messaging Events Logged

**Date:** 2025-01-27  
**Author:** Agent-8 (SSOT & System Integration Specialist)

---

## 🎯 Overview

The messaging system logs events at multiple stages of the message lifecycle. All events are stored in `data/message_history.json` via the `MessageRepository` (SSOT).

---

## 📊 Logged Events

### 1. **QUEUED** (Message Enqueued)
**Location:** `src/core/message_queue.py:176-187`

**When:** Message is added to the queue

**Logged Fields:**
```json
{
  "from": "sender_id",
  "to": "recipient_id",
  "message_type": "text|broadcast|onboarding",
  "priority": "normal|urgent",
  "content": "message content (truncated to 500 chars)",
  "content_length": 123,
  "queue_id": "uuid",
  "source": "queue|discord|cli",
  "status": "QUEUED",
  "timestamp": "2025-01-27T21:30:00.000000Z"
}
```

**Metrics Tracked:**
- `queue.enqueued` (total count)
- `queue.enqueued.by_sender.{sender}` (per sender)
- `queue.enqueued.by_recipient.{recipient}` (per recipient)
- `queue.size` (current queue size)

**Agent Activity:** Marks sender as active (if sender starts with "Agent-")

---

### 2. **PROCESSING** (Message Being Processed)
**Location:** `src/core/message_queue.py:268`

**When:** Message is dequeued and being delivered

**Status Change:** Queue entry status set to "PROCESSING"

**Note:** This is a queue status change, not a separate history log entry. The message remains in history with "QUEUED" status until delivery completes.

---

### 3. **DELIVERED** (Message Successfully Delivered)
**Location:** `src/core/message_queue_processor.py:300-308`

**When:** Message is successfully delivered via PyAutoGUI or inbox fallback

**Logged Fields:**
```json
{
  "from": "sender_id",
  "to": "recipient_id",
  "content": "message content (truncated to 200 chars)",
  "content_length": 123,
  "queue_id": "uuid",
  "status": "delivered",
  "timestamp": "2025-01-27T21:30:05.000000Z"
}
```

**Metrics Tracked:**
- `queue.deliveries.success` (total successful deliveries)
- `queue.deliveries.by_sender.{sender}` (per sender)
- `queue.deliveries.by_recipient.{recipient}` (per recipient)
- `queue.processing` (processing duration)

**Agent Activity:** Marks recipient as complete (if recipient starts with "Agent-")

**Additional Logging:**
- Also logged in `messaging_core.py:235` when delivery service confirms success
- Status updated to "delivered" in message history

---

### 4. **FAILED** (Message Delivery Failed)
**Location:** `src/core/message_queue_processor.py:353-364`

**When:** Message delivery fails (PyAutoGUI error, timeout, etc.)

**Logged Fields:**
```json
{
  "from": "sender_id",
  "to": "recipient_id",
  "content": "message content (truncated to 200 chars)",
  "queue_id": "uuid",
  "status": "FAILED",
  "error": "error message",
  "failed_at": "2025-01-27T21:30:10.000000Z",
  "timestamp": "2025-01-27T21:30:10.000000Z"
}
```

**Metrics Tracked:**
- `queue.deliveries.failed` (total failed deliveries)
- `queue.failures.by_sender.{sender}` (per sender)

**Agent Activity:** Marks recipient as inactive (if recipient starts with "Agent-")

**Additional Logging:**
- Also logged in `messaging_core.py:253` when send_message fails
- Status updated to "FAILED" in message history

---

### 5. **SENT** (Message Sent via Core)
**Location:** `src/core/messaging_core.py:215`

**When:** Message is sent through messaging core (before queue)

**Logged Fields:**
```json
{
  "from": "sender",
  "to": "recipient",
  "content": "message content (truncated to 200 chars)",
  "content_length": 123,
  "message_type": "text|broadcast|onboarding",
  "priority": "normal|urgent",
  "tags": ["tag1", "tag2"],
  "metadata": {...},
  "timestamp": "2025-01-27T21:30:00.000000Z"
}
```

**Note:** This is logged when message is sent directly (not queued), or when delivery service confirms success.

---

## 📈 Metrics Tracked (BI Integration)

**Location:** `src/repositories/message_repository.py:131-157`

**Per Message:**
- `messages.total` (total messages logged)
- `messages.by_sender.{sender}` (per sender)
- `messages.by_recipient.{recipient}` (per recipient)
- `messages.by_type.{type}` (per message type: text, broadcast, onboarding)
- `messages.by_priority.{priority}` (per priority: normal, urgent)
- `messages.by_discord_user.{username}` (if Discord username available)

---

## 🔄 Message Lifecycle

```
1. SENT → Logged in messaging_core.py (if sent directly)
   ↓
2. QUEUED → Logged in message_queue.py (when enqueued)
   ↓
3. PROCESSING → Queue status change (not logged separately)
   ↓
4. DELIVERED → Logged in message_queue_processor.py (on success)
   OR
   FAILED → Logged in message_queue_processor.py (on failure)
```

---

## 📁 Storage Location

**Primary Storage:** `data/message_history.json`

**Structure:**
```json
{
  "messages": [
    {
      "message_id": "msg_20250127_213000",
      "from": "sender",
      "to": "recipient",
      "content": "...",
      "status": "QUEUED|delivered|FAILED",
      "timestamp": "...",
      ...
    }
  ],
  "metadata": {
    "version": "1.0",
    "created_at": "..."
  }
}
```

---

## 🎯 Key Points

1. **SSOT Enforcement:** All message logging goes through `MessageRepository` (single source of truth)
2. **Multiple Log Points:** Messages can be logged at different stages (sent, queued, delivered, failed)
3. **Metrics Integration:** BI metrics tracked alongside history logging
4. **Agent Activity:** Agent activity tracking integrated with message logging
5. **Error Handling:** Logging failures don't block message delivery (graceful degradation)

---

## 🔍 Query Methods

**MessageRepository provides:**
- `get_message_history(agent_id, limit)` - Get history filtered by agent
- `get_recent_messages(limit)` - Get recent messages
- `get_messages_by_sender(sender_id)` - Get all messages from sender
- `get_messages_by_recipient(recipient_id)` - Get all messages to recipient
- `get_message_count(agent_id)` - Get message count
- `clear_old_messages(days)` - Cleanup old messages
- `compress_old_messages(days, level)` - Compress old messages

---

**Status:** Complete documentation of messaging events logged  
**Last Updated:** 2025-01-27


