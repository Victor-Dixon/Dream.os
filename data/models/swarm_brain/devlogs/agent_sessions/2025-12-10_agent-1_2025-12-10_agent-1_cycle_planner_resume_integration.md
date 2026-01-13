# Cycle Planner Resume Integration - Implementation

**Agent**: Agent-1  
**Date**: 2025-12-10  
**Task**: Connect agent resume prompts with cycle planner to assign correct tasks

## Implementation Summary

Integrated the cycle planner/contract system with the stall recovery resume message system. When an agent is detected as stalled, the system now automatically fetches and includes their next available task assignment in the resume message.

## Changes Made

### 1. Updated `_send_resume_message_to_agent` Method
**File**: `src/discord_commander/status_change_monitor.py`

**Changes**:
- Added cycle planner integration to fetch next available task before sending resume message
- Task assignment is fetched via `ContractManager.get_next_task(agent_id)`
- Task information is included in the resume message template's `actions` parameter
- Task assignment includes:
  - Task title and description
  - Source (cycle_planner or contract_system)
  - Claim command for agent to use
  - Clear action instructions

**Integration Flow**:
1. When stall is detected, `_send_resume_message_to_agent` is called
2. System calls `ContractManager.get_next_task(agent_id)` to fetch next task
3. If task is available, it's included in the resume message template
4. Resume message is sent with task assignment embedded in the `actions` section
5. Agent receives resume prompt with specific task to work on

### 2. Task Assignment Format
**When Task Available**:
```
**TASK ASSIGNED**: {task_title}
Description: {task_description}
Source: {cycle_planner|contract_system}

**Action**: Begin work on this assigned task immediately.
**Claim Command**: `python -m src.services.messaging_cli --get-next-task --agent {agent_id}`

If task is complete or blocked, produce an artifact (commit/test/report) instead.
```

**When No Task Available**:
```
No tasks available in cycle planner. Check inbox for new assignments or continue with current mission.
Resume by producing an artifact: commit/test/report or real code/doc delta.
```

## Benefits

1. **Context-Aware Recovery**: Agents receive specific task assignments when resumed, not just generic "resume work" messages
2. **Automatic Task Assignment**: Tasks are automatically assigned when resume message is sent (via `get_next_task`)
3. **Clear Action Items**: Agents know exactly what to work on when they resume
4. **Cycle Planner Integration**: Leverages existing cycle planner infrastructure
5. **Fallback Handling**: Gracefully handles cases where no tasks are available

## Technical Details

### Integration Points
- **ContractManager**: `src/services/contract_system/manager.py`
  - `get_next_task(agent_id)` - Fetches next task from cycle planner or contract system
  - Returns task with status, source, and task details

- **StatusChangeMonitor**: `src/discord_commander/status_change_monitor.py`
  - `_send_resume_message_to_agent()` - Now includes cycle planner integration
  - Fetches task before sending resume message
  - Includes task in template rendering

### Error Handling
- Non-blocking: If task fetch fails, resume message is still sent without task assignment
- Logging: All task fetch attempts are logged for debugging
- Graceful degradation: Falls back to generic resume message if no tasks available

## Testing

**Manual Test**:
```python
from src.services.contract_system.manager import ContractManager
cm = ContractManager()
result = cm.get_next_task('Agent-1')
# Should return task assignment or "no_tasks" status
```

**Integration Test**:
- Trigger stall recovery for an agent
- Verify resume message includes task assignment if available
- Verify resume message works without task assignment if none available

## Status
✅ **COMPLETE** - Cycle planner integration added to resume message system. Agents will now receive specific task assignments when resumed from stall state.

## Next Steps
- Monitor resume messages to verify task assignments are being included
- Collect feedback on task assignment clarity
- Consider adding task priority/urgency indicators to assignments

