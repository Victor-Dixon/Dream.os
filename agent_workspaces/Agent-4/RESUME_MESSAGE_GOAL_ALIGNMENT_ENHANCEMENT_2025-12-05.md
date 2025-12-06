# Resume Message Goal Alignment Enhancement
**Date**: 2025-12-05  
**Agent**: Agent-4 (Captain)  
**Priority**: CRITICAL

---

## 🎯 **OBJECTIVE**

Enhance resume messages to align with current project goals and agent-specific assignments to maximize swarm productivity and goal achievement.

---

## 📊 **CURRENT STATE**

### **What Resume Messages Include**:
- ✅ FSM state recovery actions
- ✅ Cycle planner tasks
- ✅ Scheduled tasks
- ✅ System utilization protocols
- ✅ Force multiplier patterns

### **What Resume Messages MISS**:
- ❌ Project priority alignment
- ❌ Agent-specific task assignments
- ❌ Current mission context
- ❌ Goal-aligned recovery actions

---

## ✅ **ENHANCEMENT PLAN**

### **Add to Resume Messages**:

1. **Project Priority Alignment Section**:
   - Violation Consolidation (CRITICAL - #1)
   - SSOT Remediation (HIGH - #2)
   - Phase 2 Consolidation (HIGH - #3)

2. **Agent-Specific Task Assignments**:
   - Load from FULL_SWARM_ACTIVATION document
   - Reference violation consolidation tasks
   - Reference SSOT remediation tasks
   - Reference Phase 2 consolidation tasks

3. **Current Mission Context**:
   - Agent's current mission from status.json
   - Mission priority
   - Specific tasks from assignments

4. **Goal-Aligned Recovery Actions**:
   - Replace generic actions with goal-specific actions
   - Reference specific assignments
   - Align with project priorities

---

## 🔧 **IMPLEMENTATION**

Update `src/core/optimized_stall_resume_prompt.py`:

1. Add method to load agent assignments from FULL_SWARM_ACTIVATION
2. Add project priority section builder
3. Enhance _build_prompt() with goal alignment
4. Update recovery actions to be goal-aligned

---

**Status**: Plan ready for implementation  
**Priority**: CRITICAL - Resume messages critical for goal achievement

🐝 WE. ARE. SWARM. ⚡🔥


