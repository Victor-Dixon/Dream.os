# System Resume Message Update

**Agent:** Agent-4 (Captain)  
**Date:** 2025-12-10  
**Task:** Update system resume message with cycle workflow guidance  
**Status:** ✅ COMPLETE

## Task
Update the system resume message (`CYCLE_CHECKLIST_TEXT` in `messaging_template_texts.py`) to align with the new workflow documentation, specifically:
1. When to add tasks to cycle planner (CYCLE END only)
2. When to message other agents (DURING CYCLE primarily, CYCLE END secondarily)

## Actions Taken

1. **Reviewed Current Template:**
   - Located `CYCLE_CHECKLIST_TEXT` in `src/core/messaging_template_texts.py`
   - Identified gaps in guidance for task addition and messaging timing

2. **Updated Cycle Checklist:**
   - Enhanced CYCLE START section with explicit "DO NOT" guidance
   - Enhanced DURING CYCLE section with "MESSAGE WHEN" scenarios
   - Enhanced CYCLE END section with explicit "ADD TASKS" and "MESSAGE WHEN" guidance
   - Added reference to full workflow documentation

3. **Key Updates:**
   - **CYCLE START:** Added explicit "DO NOT" for adding tasks and messaging (unless urgent)
   - **DURING CYCLE:** Added detailed "MESSAGE WHEN" scenarios (task expands, expertise needed, 75% done, blocked, force multiplier)
   - **CYCLE END:** Added explicit "ADD TASKS" section with location, timing, and what to add
   - **CYCLE END:** Added explicit "MESSAGE WHEN" section for coordination outcomes, handoffs, completions
   - Added reference to full workflow documentation

## Changes Made

**File:** `src/core/messaging_template_texts.py`

**Before:**
- Generic checklist without explicit guidance
- No clear "when to add tasks" or "when to message" instructions
- Missing reference to workflow documentation

**After:**
- Explicit DO NOT guidance for CYCLE START
- Clear MESSAGE WHEN scenarios for DURING CYCLE
- Explicit ADD TASKS and MESSAGE WHEN guidance for CYCLE END
- Reference to `docs/AGENT_OPERATING_CYCLE_WORKFLOW.md` for full details

## Impact

- **Clarity:** Agents now have explicit guidance on when to add tasks (CYCLE END) and when to message (DURING CYCLE/CYCLE END)
- **Consistency:** System resume messages now align with workflow documentation
- **Reference:** Agents can find full details in the workflow documentation
- **Prevention:** Explicit "DO NOT" prevents premature task addition and messaging

## Commit Message
```
docs: Update system resume message with cycle workflow guidance - when to add tasks and message agents
```

## Status
✅ **COMPLETE** - System resume message updated and committed

---
*Documentation artifact: Updated cycle checklist in system resume message template*

