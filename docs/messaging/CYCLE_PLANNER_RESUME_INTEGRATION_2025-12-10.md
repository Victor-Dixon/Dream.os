# Cycle Planner Resume Integration

**Date**: 2025-12-10  
**Author**: Agent-1 (Integration & Core Systems Specialist)  
**Status**: ✅ **IMPLEMENTED**

---

## 🎯 Overview

Connected the agent resume prompt system with the cycle planner to automatically assign correct tasks when agents are resumed from stall state.

## 🔄 Integration Flow

### Before Integration
1. Agent detected as stalled
2. Generic resume message sent: "Resume work, produce artifact"
3. Agent must manually check for tasks

### After Integration
1. Agent detected as stalled
2. System automatically fetches next available task from cycle planner/contract system
3. Resume message includes specific task assignment with:
   - Task title and description
   - Source (cycle_planner or contract_system)
   - Claim command
   - Clear action instructions
4. Agent receives resume prompt with specific task to work on

## 📋 Implementation Details

### Modified File
**`src/discord_commander/status_change_monitor.py`**

**Method**: `_send_resume_message_to_agent()`

**Changes**:
1. Added cycle planner integration at start of method
2. Calls `ContractManager.get_next_task(agent_id)` to fetch next task
3. Builds task assignment text if task is available
4. Includes task assignment in template's `actions` parameter
5. Non-blocking: Falls back gracefully if task fetch fails

### Integration Points

**ContractManager** (`src/services/contract_system/manager.py`):
- `get_next_task(agent_id)` - Fetches next task from cycle planner (priority) or contract system (fallback)
- Returns task with status, source, and task details
- Automatically marks task as assigned when retrieved

**StatusChangeMonitor** (`src/discord_commander/status_change_monitor.py`):
- `_send_resume_message_to_agent()` - Now includes cycle planner integration
- Fetches task before sending resume message
- Includes task in template rendering via `actions` parameter

## 📊 Task Assignment Format

### When Task Available
```
**TASK ASSIGNED**: {task_title}
Description: {task_description}
Source: {cycle_planner|contract_system}

**Action**: Begin work on this assigned task immediately.
**Claim Command**: `python -m src.services.messaging_cli --get-next-task --agent {agent_id}`

If task is complete or blocked, produce an artifact (commit/test/report) instead.
```

### When No Task Available
```
No tasks available in cycle planner. Check inbox for new assignments or continue with current mission.
Resume by producing an artifact: commit/test/report or real code/doc delta.
```

## ✅ Benefits

1. **Context-Aware Recovery**: Agents receive specific task assignments, not generic "resume work" messages
2. **Automatic Task Assignment**: Tasks are automatically assigned when resume message is sent
3. **Clear Action Items**: Agents know exactly what to work on when they resume
4. **Cycle Planner Integration**: Leverages existing cycle planner infrastructure
5. **Fallback Handling**: Gracefully handles cases where no tasks are available

## 🔧 Technical Details

### Error Handling
- **Non-blocking**: If task fetch fails, resume message is still sent without task assignment
- **Logging**: All task fetch attempts are logged for debugging
- **Graceful degradation**: Falls back to generic resume message if no tasks available

### Task Assignment Logic
1. First checks cycle planner for pending tasks (priority)
2. Falls back to contract system if no cycle planner tasks
3. Returns "no_tasks" status if nothing available
4. Task is automatically marked as assigned when retrieved

## 🧪 Testing

**Manual Test**:
```python
from src.services.contract_system.manager import ContractManager
cm = ContractManager()
result = cm.get_next_task('Agent-1')
# Returns: {'agent_id': 'Agent-1', 'task': {...}, 'status': 'assigned', 'source': 'contract_system'}
```

**Integration Test**:
- Trigger stall recovery for an agent
- Verify resume message includes task assignment if available
- Verify resume message works without task assignment if none available

## 📝 Usage

The integration is automatic - no changes needed to how stall recovery works. When an agent is detected as stalled:

1. System fetches next task from cycle planner/contract system
2. Task assignment is included in resume message template
3. Agent receives resume prompt with specific task to work on
4. Agent can claim task using provided command or work on assigned task directly

## 🚀 Future Enhancements

Potential improvements:
- Add task priority/urgency indicators
- Include task deadline information
- Show task dependencies
- Add task progress tracking
- Include related tasks from cycle planner

---

**Status**: ✅ **COMPLETE** - Cycle planner integration added to resume message system. Agents will now receive specific task assignments when resumed from stall state.

