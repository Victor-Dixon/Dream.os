# ⏰ Progressive Recovery Timeline - Self-Healing System

**Author:** Agent-3  
**Date:** 2025-01-27  
**Status:** ✅ IMPLEMENTED

---

## 🎯 RECOVERY TIMELINE

The self-healing system uses **progressive recovery based on stall duration**:

```
Agent Stalls
    ↓
0-5 minutes: Monitoring (no action)
    ↓
5 minutes: 🛑 CANCEL TERMINAL OPERATIONS
    ↓
8 minutes: 🚨 RESCUE PROTOCOL (if still stalled)
    ↓
10 minutes: 🚨🚨 HARD ONBOARD (if still stalled)
```

---

## ⏰ STAGE 1: 5 MINUTES - Cancel Terminal Operations

**Action:** Click agent's chat input coordinates + Press **SHIFT+BACKSPACE**

**What it does:**
- Clicks agent's chat input field (from `cursor_agent_coords.json`)
- Presses `SHIFT+BACKSPACE` keyboard shortcut
- Cancels any running terminal operations (like Ctrl+C in terminal)

**Tracking:**
- Counts how many times terminal is cancelled per agent per day
- Session = One day (resets at midnight)
- Stored in `agent_workspaces/.terminal_cancellation_tracking.json`

**After cancellation:**
- Waits 30 seconds
- Checks if agent status.json was updated
- If updated → Agent recovered, stop healing
- If not updated → Continue to Stage 2

**Example:**
```
Agent-3 stalled 5 minutes
    ↓
Click coordinates (-1269, 1021)
    ↓
Press SHIFT+BACKSPACE
    ↓
Wait 30 seconds
    ↓
Check status.json update
    ↓
If updated: ✅ Done
If not: Continue to Stage 2
```

---

## 🚨 STAGE 2: 8 MINUTES - Rescue Protocol

**Actions (all executed if agent still stalled):**

### 1. Send Rescue Message
- Sends message via `RecoverySystem._rescue_agent()`
- Notifies agent to wake up
- Triggers agent activity

### 2. Clear Stuck Tasks
- Removes old/stuck tasks from `status.json`
- Clears `current_tasks` array
- Marks tasks as cleared in healing history

### 3. Reset Agent Status
- Creates fresh `status.json`
- Sets `status: "ACTIVE_AGENT_MODE"`
- Sets `current_phase: "TASK_EXECUTION"`
- Clears all old state

**Example:**
```
Agent-3 still stalled after terminal cancellation
    ↓
Send rescue message → Inbox
    ↓
Clear stuck tasks → Empty current_tasks
    ↓
Reset status.json → Fresh state
    ↓
Check if agent recovered
```

---

## 🚨🚨 STAGE 3: 10 MINUTES - Hard Onboarding

**Action:** Complete agent reset via `HardOnboardingService`

**Protocol (5 steps):**
1. **Clear chat**: Click chat input + Ctrl+Shift+Backspace
2. **Execute**: Press Ctrl+Enter
3. **New window**: Press Ctrl+N
4. **Navigate**: Move to onboarding input coordinates
5. **Send message**: Send onboarding message (Enter)

**What happens:**
- Agent completely reset
- New session started
- Ready for fresh task assignment
- All old state cleared

**Example:**
```
Agent-3 still stalled after rescue protocol
    ↓
Hard onboarding initiated
    ↓
Step 1: Clear chat
    ↓
Step 2: Execute
    ↓
Step 3: New window
    ↓
Step 4: Navigate to onboarding
    ↓
Step 5: Send onboarding message
    ↓
✅ Agent fully reset and ready
```

---

## 📊 TERMINAL CANCELLATION TRACKING

### **How it works:**

1. **Per-Agent Tracking:**
   - Each agent has separate cancellation count
   - Stored in `agent_workspaces/.terminal_cancellation_tracking.json`

2. **Daily Session:**
   - Session = One calendar day
   - Resets at midnight
   - Format: `YYYY-MM-DD`

3. **Tracking File Structure:**
```json
{
  "Agent-1": {
    "2025-01-27": 3
  },
  "Agent-3": {
    "2025-01-27": 1
  }
}
```

4. **Query Cancellation Count:**
```python
system = get_self_healing_system()
count = system.get_cancellation_count_today("Agent-3")
# Returns: 1 (cancelled once today)
```

---

## 🔄 FLOW DIAGRAM

```
Agent Stalled
    ↓
Check stall duration
    ↓
┌─────────────────────────────────┐
│ Duration < 5 minutes?           │
│ → Continue monitoring           │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ Duration >= 5 minutes?          │
│ → Cancel terminal (SHIFT+BACKSPACE)│
│ → Wait 30 seconds               │
│ → Check recovery                │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ Still stalled >= 8 minutes?     │
│ → Send rescue message           │
│ → Clear stuck tasks             │
│ → Reset status.json             │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ Still stalled >= 10 minutes?    │
│ → Hard onboard agent            │
│ → Complete reset protocol       │
└─────────────────────────────────┘
    ↓
✅ Agent recovered or escalated
```

---

## 📈 STATISTICS

The system tracks:

1. **Terminal Cancellations:**
   - Count per agent per day
   - Query: `system.get_cancellation_count_today(agent_id)`

2. **Healing Actions:**
   - All actions recorded in `healing_history`
   - Success/failure rates
   - By-agent breakdown

3. **Recovery Attempts:**
   - Tracks failed attempts
   - Escalation after 3 failures

**Example stats:**
```json
{
  "terminal_cancellations_today": {
    "Agent-1": 0,
    "Agent-3": 1,
    "Agent-7": 0
  },
  "total_actions": 8,
  "success_rate": 87.5
}
```

---

## ⚙️ CONFIGURATION

### **Thresholds (hardcoded constants):**
```python
TERMINAL_CANCEL_THRESHOLD = 300  # 5 minutes
RESCUE_THRESHOLD = 480           # 8 minutes
HARD_ONBOARD_THRESHOLD = 600     # 10 minutes
```

### **Enable/Disable Actions:**
```yaml
self_healing:
  terminal_cancel_enabled: true   # Enable terminal cancellation
  hard_onboard_enabled: true      # Enable hard onboarding
```

---

## ✅ SUMMARY

**Progressive Recovery Timeline:**

- **5 minutes**: Cancel terminal (SHIFT+BACKSPACE)
- **8 minutes**: Rescue + Clear + Reset
- **10 minutes**: Hard onboard

**Key Features:**

- ✅ Terminal cancellation with coordinate clicking
- ✅ Cancellation count tracking per day (session)
- ✅ Progressive escalation based on duration
- ✅ Hard onboarding integration
- ✅ Full statistics and history

**Result:** Agents are automatically recovered before reaching critical levels!

