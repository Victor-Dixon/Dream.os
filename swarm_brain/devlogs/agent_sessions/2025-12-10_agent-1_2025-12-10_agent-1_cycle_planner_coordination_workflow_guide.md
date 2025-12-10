# Cycle Planner & Coordination Workflow Guide - Complete

**Date**: 2025-12-10  
**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Status**: ✅ **COMPLETE**

---

## 📋 **TASK**

Create comprehensive workflow guide answering:
1. **When/where are tasks added to the cycle planner?**
2. **At what point in the agent operating cycle should agents message each other?**

---

## ✅ **ACTIONS TAKEN**

### **1. Workflow Guide Creation**
- Created comprehensive workflow guide: `docs/messaging/CYCLE_PLANNER_AND_COORDINATION_WORKFLOW_2025-12-10.md`
- Documented all cycle planner task creation points
- Documented all agent coordination messaging points
- Included decision trees and practical examples

### **2. Key Findings Documented**

#### **Cycle Planner Task Creation**:
- **Slice Phase** (Step 3): Primary point for creating sub-tasks when breaking down large tasks
- **Report Phase** (Step 7): Point for adding next session tasks
- **Claim Phase** (Step 1): Point for checking existing tasks from cycle planner

#### **Agent Coordination Messaging**:
- **Slice Phase** (Step 3): PRIMARY delegation point - BEFORE execution
- **Execute Phase** (Step 4): Coordination point if task expands DURING execution
- **Report Phase** (Step 7): Coordination outcomes reporting

### **3. Workflow Integration Points**
- Documented complete agent operating cycle with cycle planner and coordination actions
- Created decision trees for task size assessment, task expansion, and coordination type selection
- Included practical examples for large task delegation, task expansion, and next session planning

### **4. Best Practices & Anti-Patterns**
- Documented best practices for task creation and agent messaging
- Documented anti-patterns to avoid
- Created summary table mapping cycle phases to actions

---

## 📊 **KEY TAKEAWAYS**

1. **Tasks are added to cycle planner**:
   - **Slice phase**: When breaking down large tasks (BEFORE execution)
   - **Report phase**: When planning next session (AFTER execution)

2. **Agents message each other**:
   - **Slice phase**: For delegation (BEFORE execution) - PRIMARY POINT
   - **Execute phase**: For coordination (DURING execution) - if task expands
   - **Report phase**: For outcomes (AFTER execution) - if swarm engaged

3. **Delegation happens FIRST**:
   - Assess task size in slice phase
   - If task > 1 cycle OR multi-domain → STOP and delegate
   - Don't start working alone on large tasks

4. **Cycle planner integration**:
   - Resume system automatically fetches tasks from cycle planner
   - Tasks are created manually or via tools
   - Tasks are checked during "Claim" phase

---

## 📁 **ARTIFACTS**

- **Workflow Guide**: `docs/messaging/CYCLE_PLANNER_AND_COORDINATION_WORKFLOW_2025-12-10.md`
  - Comprehensive 400+ line workflow documentation
  - Includes decision trees, examples, and best practices
  - Answers both user questions with clear guidance

---

## ✅ **STATUS**

**Status**: ✅ **COMPLETE**

**Next Actions**:
- Guide is ready for use by all agents
- Provides clear workflow guidance for cycle planner and coordination
- Can be referenced during agent operating cycle execution

---

**Commit Message**: `agent-1: Created comprehensive cycle planner and coordination workflow guide`

