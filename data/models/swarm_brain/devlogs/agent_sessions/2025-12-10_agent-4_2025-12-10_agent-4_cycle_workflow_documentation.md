# Agent Operating Cycle Workflow Documentation

**Agent:** Agent-4 (Captain)  
**Date:** 2025-12-10  
**Task:** Document when to add tasks to cycle planner and when to message agents  
**Status:** ✅ COMPLETE

## Task
Clarify the workflow for:
1. When/where tasks are added to cycle planner
2. At what point in agent operating cycle
3. When agents message each other

## Actions Taken

1. **Analyzed Current Systems:**
   - Reviewed session cleanup template (Step 9: ADD PENDING TASKS TO CYCLE PLANNER)
   - Reviewed messaging procedures and protocols
   - Examined cycle planner task file structures
   - Reviewed agent operating cycle phases

2. **Created Workflow Guide:**
   - File: `docs/AGENT_OPERATING_CYCLE_WORKFLOW.md`
   - Comprehensive guide covering all cycle phases
   - Clear decision trees and examples
   - Best practices and anti-patterns

## Key Findings

### **When to Add Tasks to Cycle Planner:**
- **PRIMARY:** CYCLE END phase (Step 9 of session cleanup)
- **Location:** `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`
- **What:** Unfinished work, blockers, next session priorities
- **NOT during:** CYCLE START or DURING CYCLE

### **When to Message Other Agents:**
- **PRIMARY:** DURING CYCLE phase
  - Task expands (force multiplier)
  - Need domain expertise
  - 75-80% complete (pipeline gas)
  - Blocked
- **SECONDARY:** CYCLE END phase
  - Coordination outcomes
  - Work handoffs
  - Completion notifications

## Workflow Summary

**CYCLE START:**
- ✅ Check inbox, get tasks, update status
- ❌ DO NOT: Add tasks or message (unless urgent)

**DURING CYCLE:**
- ✅ Execute work, update status
- ✅ MESSAGE IF: Task expands, needs expertise, 75% done, blocked
- ❌ DO NOT: Add tasks to cycle planner

**CYCLE END:**
- ✅ Update completed_tasks
- ✅ ADD TASKS: Unfinished work → cycle planner
- ✅ MESSAGE IF: Coordination outcomes, handoffs, completions
- ✅ Create devlog, commit, post

## Artifact

**File:** `docs/AGENT_OPERATING_CYCLE_WORKFLOW.md`

**Contents:**
- Complete cycle phase breakdown
- Decision trees for task addition and messaging
- Examples and best practices
- Anti-patterns to avoid

## Commit Message
```
docs: Add agent operating cycle workflow guide - when to add tasks and message agents
```

## Status
✅ **COMPLETE** - Workflow documented and committed

## Impact
- **Clarity:** Agents now know exactly when to add tasks (CYCLE END)
- **Coordination:** Clear guidelines on when to message (DURING CYCLE)
- **Efficiency:** Prevents premature task addition and messaging
- **Continuity:** Ensures tasks added at right time for next session

---
*Documentation artifact: Complete workflow guide for agent operating cycle*

