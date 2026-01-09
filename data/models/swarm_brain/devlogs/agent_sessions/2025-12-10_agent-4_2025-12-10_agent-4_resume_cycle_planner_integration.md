# Resume Prompt + Cycle Planner Integration

**Agent:** Agent-4 (Captain)  
**Date:** 2025-12-10  
**Task:** Connect agent resume prompts with cycle planner for automatic task assignment  
**Status:** ✅ COMPLETE

## Task
Integrate the agent resume prompt system with the cycle planner so that when agents resume work after inactivity, they automatically receive assigned tasks from their cycle planner.

## Actions Taken

1. **Created Resume Cycle Planner Integration Module**
   - File: `src/core/resume_cycle_planner_integration.py`
   - Integrates with ContractManager to get and claim tasks
   - Two modes: auto-claim (default) and preview-only

2. **Updated Optimized Stall Resume Prompt**
   - File: `src/core/optimized_stall_resume_prompt.py`
   - Added `auto_claim_tasks` parameter (default: True)
   - Integrated ResumeCyclePlannerIntegration
   - Modified task retrieval to use ContractManager.get_next_task()
   - Enhanced prompt to include assigned task details

3. **Key Features**
   - **Auto-claim mode**: Automatically claims and assigns tasks when generating resume prompt
   - **Preview mode**: Shows available tasks without claiming (if auto_claim_tasks=False)
   - **Task details in prompt**: Shows task ID, title, priority, description, status
   - **Fallback support**: Falls back to old method if integration unavailable

## Technical Implementation

### ResumeCyclePlannerIntegration Class
- `get_and_claim_next_task(agent_id)`: Claims task automatically
- `get_next_task_preview(agent_id)`: Preview without claiming
- Uses ContractManager.get_next_task() which checks cycle planner first

### Updated Prompt Generation
- When `auto_claim_tasks=True` (default):
  - Automatically claims next available task
  - Includes "TASK ASSIGNED" section in prompt
  - Task marked as "assigned" in cycle planner
- When `auto_claim_tasks=False`:
  - Shows available task without claiming
  - Includes "AVAILABLE TASK" section with claim instructions

## Files Modified

1. **Created:**
   - `src/core/resume_cycle_planner_integration.py` (101 lines)

2. **Modified:**
   - `src/core/optimized_stall_resume_prompt.py`
     - Added ResumeCyclePlannerIntegration initialization
     - Updated task retrieval logic
     - Enhanced prompt building with task assignment section

## Benefits

1. **Automatic Task Assignment**: Agents receive assigned tasks immediately on resume
2. **Reduced Friction**: No need to manually claim tasks after resuming
3. **Better Context**: Resume prompts include specific task details
4. **Integration**: Uses existing ContractManager infrastructure
5. **Backward Compatible**: Falls back gracefully if integration unavailable

## Testing

- ✅ Module imports successfully
- ✅ Prompt generation works with integration
- ✅ No linting errors
- ✅ Backward compatible (falls back if ContractManager unavailable)

## Usage

When an agent resumes after inactivity:
1. System detects inactivity
2. Generates resume prompt with auto_claim_tasks=True
3. ContractManager.get_next_task() checks cycle planner
4. Task automatically claimed and marked "assigned"
5. Resume prompt includes task details
6. Agent immediately knows what task to work on

## Commit Message
```
feat: Integrate resume prompt with cycle planner for automatic task assignment (Agent-4)
```

## Status
✅ **COMPLETE** - Integration implemented, tested, and committed

## Impact
- **Agent Efficiency**: Agents immediately know their assigned task on resume
- **Task Management**: Automatic task assignment reduces manual coordination
- **Context Awareness**: Resume prompts now include specific task context
- **Workflow Improvement**: Seamless integration between resume and task assignment

---
*Real artifact: New integration module + updated prompt system*

