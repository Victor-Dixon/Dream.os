# 🚨 Agent-4 Stall/Resume Prompt Optimization - 2025-11-28

## 📋 Mission Summary

Optimized the stall/resume prompt system and integrated it with FSM (Finite State Machine) and Cycle Planner for context-aware agent recovery.

## 🎯 Implementation

### **1. Created Optimized Prompt Generator**
- **File**: `src/core/optimized_stall_resume_prompt.py`
- **Features**:
  - FSM state-specific recovery actions (6 states)
  - Cycle Planner task suggestions
  - Urgency levels based on stall duration
  - Agent state context (mission, FSM state)

### **2. Integrated with Self-Healing System**
- **File**: `src/core/agent_self_healing_system.py`
- **Update**: `_send_rescue_message()` now uses optimized prompt
- **Stage 2 (8 minutes)**: Sends FSM+Cycle Planner integrated prompt

### **3. Integrated with Recovery Messaging**
- **File**: `src/orchestrators/overnight/recovery_messaging.py`
- **Update**: `send_agent_rescue_message()` uses optimized prompt generator
- **Backward Compatible**: Default stall_duration_minutes=0.0

## 🔥 Key Features

### **FSM State-Specific Actions**
- **START**: Check inbox, review mission, claim task
- **ACTIVE**: Continue task, check blockers, update status
- **PROCESS**: Complete operation, return to ACTIVE
- **BLOCKED**: Document blocker, find workaround
- **COMPLETE**: Finalize deliverables, post devlog
- **END**: Clean up, check for new assignments

### **Cycle Planner Integration**
- Auto-loads agent's cycle planner file
- Finds first PENDING or READY task
- Displays task details (ID, title, priority, points)
- Suggests claiming and executing task

### **Urgency Levels** (Updated 2025-12-03)
- 🚨🚨 **CRITICAL** (10+ min): Immediate action required
- 🚨 **URGENT** (5+ min): Resume immediately (aligned with 5-minute threshold)
- ⚠️ **WARNING** (3+ min): Continue work now
- 🔄 **RECOVERY** (<3 min): Resume operations

## 📊 Impact

**Before**:
- Generic rescue message: "[RESCUE] Agent-X - Reset and resume operations. Report status."
- No context about agent's state
- No task suggestions
- No FSM guidance

**After**:
- Context-aware prompt with FSM state
- Cycle Planner task suggestions
- State-specific recovery actions
- Urgency-based messaging
- Autonomous operation reminders

## ✅ Status

- ✅ Optimized prompt generator created
- ✅ Self-healing system integrated
- ✅ Recovery messaging integrated
- ✅ Documentation created
- ✅ No linter errors

## 📝 Documentation

- **Integration Guide**: `docs/STALL_RESUME_PROMPT_INTEGRATION.md`
- **FSM Guide**: `swarm_brain/protocols/AGENT_LIFECYCLE_FSM.md`

---

**Captain Agent-4**  
*Optimizing recovery prompts for better agent autonomy and faster stall recovery*

