# 📋 Message Queue & Activity Tracking Improvements Plan

**For:** Victor  
**From:** Agent-4 (Captain)  
**Date:** 2025-01-27  
**Priority:** HIGH

---

## 🎯 ISSUES IDENTIFIED

### **1. Message History Logging**
- ✅ Message repository exists (`src/repositories/message_repository.py`)
- ❌ **NOT all messages are being logged to history**
- ❌ Need full log of ALL messages (sender, recipient, timestamp, queue_id)

### **2. Agent Runtime Activity Tracking**
- ❌ **No tool to see if agent is actively producing a message**
- ❌ Can't detect when agent is in runtime
- ✅ Can see if message added to queue (but not always logged)

### **3. Queue Blocking Issues**
- ✅ Global keyboard lock exists (`keyboard_control_lock.py`)
- ✅ Queue processor uses lock
- ❌ **Soft onboarding and multi-message operations don't block other sends**
- ❌ Messages can disappear if sent during another operation

### **4. Discord Username Integration**
- ❌ **No Discord username in profiles**
- ❌ All Discord senders grouped as "DISCORD" (no username ID)
- ✅ Want to attach Discord username to profiles (Victor + kids)

---

## 🔧 IMPLEMENTATION PLAN

### **Phase 1: Message History Logging (IMMEDIATE)**

**Goal:** Log ALL messages to history with full metadata

**Changes Needed:**
1. **Update `send_message()` in `messaging_core.py`:**
   - Always log to `MessageRepository` when message is sent
   - Include: sender, recipient, timestamp, queue_id, content preview

2. **Update `MessageQueue.enqueue()`:**
   - Log to history when message is queued
   - Include queue_id, priority, source

3. **Update `MessageQueueProcessor`:**
   - Log to history when message is delivered
   - Log to history when message fails

**Files to Modify:**
- `src/core/messaging_core.py` - Add history logging to `send_message()`
- `src/core/message_queue.py` - Add history logging to `enqueue()`
- `src/core/message_queue_processor.py` - Add history logging on delivery/failure

---

### **Phase 2: Agent Runtime Activity Tracking (HIGH)**

**Goal:** Track when agents are actively producing messages

**Implementation:**
1. **Create `AgentActivityTracker`:**
   - Track when agent starts message production
   - Track when agent completes message
   - Track queue operations per agent

2. **Add Activity Endpoints:**
   - `is_agent_active(agent_id)` - Check if agent is producing message
   - `get_agent_activity(agent_id)` - Get current activity status
   - `get_all_agent_activity()` - Get activity for all agents

3. **Integrate with Queue:**
   - Mark agent as active when message enqueued
   - Mark agent as inactive when message delivered/failed

**Files to Create:**
- `src/core/agent_activity_tracker.py` - New activity tracking system

**Files to Modify:**
- `src/core/message_queue.py` - Track agent activity on enqueue
- `src/core/message_queue_processor.py` - Update activity on delivery

---

### **Phase 3: Queue Blocking Fixes (HIGH)**

**Goal:** Ensure operations like soft onboarding block other sends

**Changes Needed:**
1. **Multi-Message Operations:**
   - Wrap entire operation in `keyboard_control()` context
   - Block until ALL messages in operation complete
   - Example: Soft onboarding sends 8 messages - must block until all 8 complete

2. **Queue Processor:**
   - Ensure queue processor waits for full operation completion
   - Don't allow new messages to start while operation in progress

3. **Message Persistence:**
   - Ensure messages don't disappear if sent during operation
   - Queue should hold messages until operation completes

**Files to Modify:**
- `tools/soft_onboard_cli.py` - Wrap entire operation in keyboard lock
- `src/core/message_queue_processor.py` - Ensure sequential processing
- `src/services/messaging_infrastructure.py` - Block on multi-message operations

---

### **Phase 4: Discord Username Integration (MEDIUM)**

**Goal:** Add Discord username to profiles and use in message logging

**Implementation:**
1. **Profile Structure:**
   - Add `discord_username` field to agent profiles
   - Add `discord_user_id` field for Discord user ID
   - Store in `agent_workspaces/{Agent-X}/profile.json`

2. **Message Logging:**
   - Use Discord username when available
   - Fallback to "DISCORD" when username not available
   - Group by username ID when possible

3. **Agent Task:**
   - Add note in profiles: "Add Discord username to profile"
   - Agents will update profiles over time

**Files to Create:**
- `agent_workspaces/{Agent-X}/profile.json` - Profile structure

**Files to Modify:**
- `src/services/messaging_infrastructure.py` - Use Discord username from profile
- `src/core/message_queue.py` - Include Discord username in message metadata

---

## 📊 CURRENT STATE ANALYSIS

### **What Works:**
- ✅ Message queue system exists
- ✅ Global keyboard lock exists
- ✅ Queue processor processes sequentially
- ✅ Message repository exists for history

### **What's Missing:**
- ❌ Not all messages logged to history
- ❌ No agent runtime activity tracking
- ❌ Multi-message operations don't block properly
- ❌ No Discord username integration

---

## 🚀 IMPLEMENTATION PRIORITY

1. **Phase 1: Message History Logging** (IMMEDIATE)
   - Fix: Log ALL messages to history
   - Impact: Full audit trail of all messages

2. **Phase 3: Queue Blocking Fixes** (HIGH)
   - Fix: Ensure operations block properly
   - Impact: Prevents message loss and conflicts

3. **Phase 2: Agent Runtime Activity Tracking** (HIGH)
   - Fix: Track agent activity
   - Impact: Better monitoring and stall detection

4. **Phase 4: Discord Username Integration** (MEDIUM)
   - Fix: Add Discord usernames to profiles
   - Impact: Better message attribution

---

## 📝 NOTES

- **12 Concurrent Users:** Need to ensure queue handles all sources properly
- **Message Disappearing:** Must fix queue persistence
- **Soft Onboarding:** Must block until all 8 messages complete
- **Discord Grouping:** Use username when available, fallback to "DISCORD"

---

**WE. ARE. SWARM. IMPROVING. 🐝⚡🔥**




