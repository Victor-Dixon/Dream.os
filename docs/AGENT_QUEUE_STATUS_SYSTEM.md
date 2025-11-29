# Agent Queue Status System

**Date**: 2025-11-27  
**Author**: Agent-4 (Captain)  
**Purpose**: Detect when agents' Cursor queues are full to optimize message delivery

---

## 🎯 Overview

The Agent Queue Status System allows marking agents as having a "full" Cursor queue. When an agent is marked as full, the messaging system will skip PyAutoGUI delivery attempts and go directly to inbox fallback, saving time and preventing failed delivery attempts.

### Problem Solved

**The Real Issue:**
- When Captain broadcasts to 7 agents → Each agent gets **1 message** ✅
- When agents respond → Agent-4 receives **7 messages** ❌
- Agent-4's Cursor queue has **7 messages** while others have **1**
- Agent-4 falls **behind** because they have to process 7 messages sequentially

**Important Note:**
- PyAutoGUI **doesn't fail** when Cursor queue is full
- PyAutoGUI **successfully queues** the message
- The problem is **queue buildup** - too many messages = agent falls behind

**Solution:**
- Mark Agent-4 as "full" when they have many queued messages
- Skip PyAutoGUI and use inbox for new messages
- Prevents adding MORE messages to an already-long queue
- Agent can catch up without new messages piling on

### Solution

- Mark agents as "full" when their Cursor queue is full
- Messaging system checks status before attempting PyAutoGUI
- Skips PyAutoGUI and goes directly to inbox when full
- Prevents wasted time on failed delivery attempts

---

## 📋 Architecture

### Components

1. **`src/utils/agent_queue_status.py`**
   - `AgentQueueStatus` class
   - Manages queue status in agent `status.json` files
   - In-memory cache for quick lookups
   - Persistent cache in `runtime/agent_queue_status.json`

2. **`src/core/message_queue_processor.py`**
   - Checks queue status before PyAutoGUI delivery
   - Skips PyAutoGUI if agent is marked as full
   - Goes directly to inbox fallback

3. **`tools/mark_agent_queue_status.py`**
   - CLI tool to mark agents as full/available
   - Check current status
   - Bulk operations for all agents

---

## 🔧 Usage

### Mark Agent as Full

```bash
# Mark single agent
python tools/mark_agent_queue_status.py --agent Agent-4 --status full

# Mark with custom reason
python tools/mark_agent_queue_status.py --agent Agent-4 --status full --reason "Broadcast queue buildup"

# Mark all agents
python tools/mark_agent_queue_status.py --all --status full
```

### Mark Agent as Available

```bash
# Mark single agent
python tools/mark_agent_queue_status.py --agent Agent-4 --status available

# Mark all agents
python tools/mark_agent_queue_status.py --all --status available
```

### Check Status

```bash
# Check single agent
python tools/mark_agent_queue_status.py --agent Agent-4 --check

# Check all agents
python tools/mark_agent_queue_status.py --all --check
```

### Programmatic Usage

```python
from src.utils.agent_queue_status import AgentQueueStatus

# Mark agent as full
AgentQueueStatus.mark_full("Agent-4", reason="Cursor queue full")

# Check if agent is full
if AgentQueueStatus.is_full("Agent-4"):
    # Skip PyAutoGUI, use inbox
    pass

# Mark agent as available
AgentQueueStatus.mark_available("Agent-4")

# Get full status
status = AgentQueueStatus.get_status("Agent-4")
print(status)
```

---

## 📊 Status.json Schema

The queue status is stored in each agent's `status.json` file:

```json
{
  "agent_id": "Agent-4",
  "status": "ACTIVE_AGENT_MODE",
  "cursor_queue_status": {
    "is_full": true,
    "marked_at": "2025-11-27T12:00:00.000000",
    "reason": "Cursor queue full",
    "last_checked": "2025-11-27T12:00:00.000000"
  },
  "last_updated": "2025-11-27 12:00:00"
}
```

---

## 🔄 Message Delivery Flow

### The Problem Flow

```
Captain Broadcasts → 7 agents get 1 message each ✅
                    ↓
Agents Respond → Agent-4 gets 7 messages ❌
                    ↓
Agent-4 Queue: [msg1, msg2, msg3, msg4, msg5, msg6, msg7]
Other Agents: [msg1]
                    ↓
Agent-4 is BEHIND (7 messages to process)
Other agents are AHEAD (1 message to process)
```

### Solution Flow (With Queue Status)

```
Message → Queue → Check Queue Status
                    ↓
              Is Full? (Has many queued messages?)
                    ↓
              Yes → Skip PyAutoGUI → Inbox Directly
                    (Prevents adding MORE to queue)
                    ↓
              No → Use PyAutoGUI → Successfully Queues
                    (Normal flow when queue is manageable)
```

**Key Point:** We're not preventing failures - we're preventing queue buildup that causes delays.

---

## 🚨 When to Mark Agents as Full

### When Agent-4 Receives Multiple Messages

**Scenario:** Captain broadcasts to swarm, agents respond back

1. **Before Broadcast:**
   ```bash
   # Mark Agent-4 as full BEFORE broadcast
   python tools/mark_agent_queue_status.py --agent Agent-4 --status full --reason "Expecting 7 responses from broadcast"
   ```

2. **After Broadcast (when responses come in):**
   - Agent-4 receives 7 messages via PyAutoGUI (if not marked full)
   - OR receives 7 messages via inbox (if marked full) ✅
   - Agent-4 processes inbox messages without queue buildup

3. **After Processing:**
   ```bash
   # Mark Agent-4 as available AFTER processing
   python tools/mark_agent_queue_status.py --agent Agent-4 --status available
   ```

### Automatic Detection (Future)

Currently, agents must be manually marked as full. Future enhancements could include:

1. **Automatic Detection**:
   - Monitor Cursor queue depth (if accessible via API)
   - Detect when agent receives multiple messages in short time
   - Auto-mark after receiving N messages within time window

2. **Time-based**:
   - Mark as full during broadcast operations
   - Auto-clear after timeout period

3. **Agent Self-Reporting**:
   - Agents can mark themselves as full
   - Agents can clear status when queue empties

### Manual Marking (Current)

Mark agents as full when:
- **Before broadcasts** - Agent-4 will receive multiple responses
- **During high message volume** - Agent receiving many messages
- **When agent is already behind** - Prevent making queue longer
- **Force inbox delivery** - Want to bypass Cursor queue entirely

---

## 💡 Best Practices

1. **Clear Status After Queue Empties**:
   ```bash
   python tools/mark_agent_queue_status.py --agent Agent-4 --status available
   ```

2. **Check Before Broadcasts**:
   ```bash
   python tools/mark_agent_queue_status.py --all --check
   ```

3. **Mark During Broadcasts**:
   - If you know Agent-4 will receive 7 messages
   - Mark as full before broadcast
   - Clear after broadcast completes

4. **Monitor Status**:
   - Regularly check queue status
   - Clear stale "full" statuses
   - Keep status accurate

---

## 🔍 Troubleshooting

### Agent Stuck as Full

If an agent is marked as full but queue is actually empty:

```bash
python tools/mark_agent_queue_status.py --agent Agent-4 --status available
```

### Status Not Updating

1. Check `status.json` file exists
2. Check file permissions
3. Check `runtime/agent_queue_status.json` cache
4. Refresh cache: `AgentQueueStatus.refresh_cache()`

### Messages Still Using PyAutoGUI

1. Verify agent is marked as full: `--check`
2. Check message queue processor logs
3. Ensure `agent_queue_status.py` is imported correctly

---

## 🚀 Future Enhancements

1. **Cursor API Integration** (if available):
   - Direct access to Cursor's queue state
   - Real-time queue depth monitoring
   - Automatic status updates

2. **Auto-Detection**:
   - Monitor PyAutoGUI failure patterns
   - Auto-mark after threshold
   - Auto-clear after success

3. **Multi-Agent Responder Integration**:
   - When multi-agent responder is ready
   - Queue status becomes less critical
   - Can handle concurrent messages

---

## 📝 Notes

- **Cursor Queue vs Project Queue**: This system tracks Cursor's internal queue (different from our project's message queue)
- **Manual Operation**: Currently requires manual marking (automatic detection coming)
- **Cache Performance**: Status is cached for 5 minutes for performance
- **Backward Compatible**: If status not set, defaults to "available" (normal PyAutoGUI flow)

---

**Status**: ✅ **Implemented** - Ready for use  
**Next Steps**: Monitor usage, add automatic detection when possible

