# 🚨 Optimized Stall/Resume Prompt Integration

**Date**: 2025-11-28  
**Author**: Agent-4 (Captain)  
**Status**: ✅ IMPLEMENTED  
**Priority**: CRITICAL - Prevents 2XX stalled agents

---

## 🎯 **OVERVIEW**

The stall/resume prompt has been optimized and integrated with:
1. **FSM (Finite State Machine)** - Provides state-specific recovery actions
2. **Cycle Planner** - Suggests next available task
3. **Agent State Context** - Uses last known mission and status

**Result**: Context-aware recovery prompts that guide agents back to productive work.

---

## 🔄 **INTEGRATION POINTS**

### **1. Self-Healing System** (`src/core/agent_self_healing_system.py`)

**Stage 2 (8 minutes)**: Uses optimized prompt with FSM + Cycle Planner

```python
# Line 327-333
if stall_duration >= RESCUE_THRESHOLD:
    stall_duration_minutes = stall_duration / 60.0
    await self._send_rescue_message(agent_id, stall_duration_minutes=stall_duration_minutes)
```

### **2. Recovery Messaging** (`src/orchestrators/overnight/recovery_messaging.py`)

**Updated**: `send_agent_rescue_message()` now uses optimized prompt generator

```python
# Uses OptimizedStallResumePrompt
rescue_message = generate_optimized_resume_prompt(
    agent_id=agent_id,
    fsm_state=None,  # Loaded from status.json
    last_mission=None,  # Loaded from status.json
    stall_duration_minutes=stall_duration_minutes
)
```

---

## 📊 **FSM STATE-SPECIFIC RECOVERY ACTIONS**

### **START State**
- Check inbox for new assignments
- Review mission objectives
- Initialize workspace
- Claim task from cycle planner

### **ACTIVE State**
- Continue current task execution
- Check for blockers and resolve
- Update status.json with progress
- Move to next action in queue

### **PROCESS State**
- Complete current processing operation
- Check if operation completed successfully
- Return to ACTIVE state
- Report processing results

### **BLOCKED State**
- Document blocker clearly
- Check if blocker auto-resolved
- Notify Captain if still blocked
- Find workaround or alternative task

### **COMPLETE State**
- Finalize deliverables
- Post devlog to Discord
- Update cycle planner (mark complete)
- Transition to END state

### **END State**
- Clean up workspace
- Update status.json
- Check for new assignments
- Transition to START for new mission

---

## 📋 **CYCLE PLANNER INTEGRATION**

The optimized prompt automatically:
1. **Loads** agent's cycle planner file (`swarm_cycle_planner/cycles/{date}_{agent}_pending_tasks.json`)
2. **Finds** first PENDING or READY task
3. **Displays** task details (ID, title, priority, points, status)
4. **Suggests** claiming and executing the task

**Example Output**:
```
📋 NEXT TASK FROM CYCLE PLANNER:
- Task: Stage 1 Step 4: Repository Merging (A7-STAGE1-MERGE-001)
- Priority: HIGH
- Points: 300
- Status: PENDING
- Action: Claim and execute this task immediately
```

---

## 🎯 **PROMPT STRUCTURE**

### **Urgency Levels**
- **🚨🚨 CRITICAL** (10+ minutes): "Immediate action required!"
- **🚨 URGENT** (8+ minutes): "Resume operations immediately!"
- **⚠️ WARNING** (5+ minutes): "Continue your work now."
- **🔄 RECOVERY** (<5 minutes): "Resume operations and continue your work."

### **Prompt Sections**
1. **Urgency Header** - Based on stall duration
2. **Current State** - FSM state, last mission, stall duration
3. **Next Task** - From Cycle Planner (if available)
4. **Recovery Actions** - FSM state-specific actions
5. **Autonomous Principles** - Reminders about autonomy
6. **FSM Transition** - Guidance on state transition

---

## 🔧 **USAGE**

### **In Self-Healing System**
```python
from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt

# Generate prompt
prompt = generate_optimized_resume_prompt(
    agent_id="Agent-3",
    fsm_state="blocked",  # Optional - will load from status.json if None
    last_mission="Test Coverage Expansion",  # Optional - will load if None
    stall_duration_minutes=8.5
)

# Send via messaging system
send_message(content=prompt, recipient="Agent-3", ...)
```

### **Direct Usage**
```python
from src.core.optimized_stall_resume_prompt import OptimizedStallResumePrompt

generator = OptimizedStallResumePrompt()
prompt = generator.generate_resume_prompt(
    agent_id="Agent-7",
    fsm_state=None,  # Auto-load from status.json
    last_mission=None,  # Auto-load from status.json
    stall_duration_minutes=5.0
)
```

---

## ✅ **BENEFITS**

1. **Context-Aware**: Uses agent's actual FSM state and mission
2. **Task-Specific**: Suggests next task from Cycle Planner
3. **State-Appropriate**: Recovery actions match agent's lifecycle state
4. **Urgency-Based**: Prompt urgency matches stall duration
5. **Autonomous**: Reminds agents they are autonomous and should continue

---

## 🔄 **INTEGRATION STATUS**

- ✅ **Optimized Prompt Generator**: `src/core/optimized_stall_resume_prompt.py`
- ✅ **Self-Healing Integration**: Updated `_send_rescue_message()`
- ✅ **Recovery Messaging Integration**: Updated `send_agent_rescue_message()`
- ✅ **FSM State Actions**: Defined for all 6 states
- ✅ **Cycle Planner Integration**: Auto-loads and suggests tasks

---

## 📝 **NEXT STEPS**

1. **Test** with actual stalled agents
2. **Monitor** recovery success rates
3. **Tune** FSM state actions based on results
4. **Expand** Cycle Planner integration (auto-claim tasks?)

---

**🚀 OPTIMIZED PROMPTS = BETTER RECOVERY = FEWER STALLED AGENTS!**

