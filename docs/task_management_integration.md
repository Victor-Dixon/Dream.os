# Task Management System Integration

**Purpose:** How agents integrate with MASTER_TASK_LOG.md via MCP

**Last Updated:** 2025-12-16

---

## Overview

The task management system is integrated into the agent operating cycle via:
1. **MCP Server** (`task_manager_server.py`) - Provides tools for task operations
2. **Updated Templates** - A2A and S2A messages include task management instructions
3. **Cycle Procedures** - CYCLE START, DURING, and END all reference task management

---

## MCP Server: task_manager_server

### Location
`mcp_servers/task_manager_server.py`

### Configuration
Add to MCP settings (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/task_manager_server.py"
      ]
    }
  }
}
```

### Available Tools

1. **`add_task_to_inbox`** - Add task to INBOX
2. **`mark_task_complete`** - Mark task as done
3. **`move_task_to_waiting`** - Move task to WAITING ON
4. **`get_tasks`** - Read tasks from log

See `mcp_servers/TASK_MANAGER_README.md` for full documentation.

---

## Updated Operating Cycle Procedures

### CYCLE START

**New Step Added:**
```
- Check MASTER_TASK_LOG.md (use MCP: get_tasks) for assigned tasks
  - Review THIS WEEK section for priorities
  - Check WAITING ON for unblocked items
  - Reference: DELEGATION_BOARD.md for task ownership
```

**Location:** `src/core/messaging_template_texts.py` - `CYCLE_CHECKLIST_TEXT`

### DURING CYCLE

**New Steps Added:**
```
- If new task identified → Use MCP: add_task_to_inbox(task, agent_id)
- If task blocked → Use MCP: move_task_to_waiting(task_description, reason, agent_id)
```

**Location:** `src/core/messaging_template_texts.py` - `CYCLE_CHECKLIST_TEXT`

### CYCLE END

**New Mandatory Section Added:**
```
✅ UPDATE MASTER_TASK_LOG (MANDATORY):
- Use MCP tool: task_manager_server
- If task completed → mark_task_complete(task_description, section="THIS WEEK")
- If task blocked → move_task_to_waiting(task_description, reason="blocked on X", agent_id="{agent_id}")
- If new task identified → add_task_to_inbox(task="description", agent_id="{agent_id}")
- Location: MASTER_TASK_LOG.md (repository root)
- Reference: QUICK_START_GUIDE.md
```

**Location:** `src/core/messaging_template_texts.py` - `CYCLE_CHECKLIST_TEXT`

---

## Updated A2A Template

### Changes Made

1. **CYCLE START** - Added task log check
2. **DURING CYCLE** - Added task capture steps
3. **CYCLE END** - Added mandatory task update section

**Location:** `src/core/messaging_template_texts.py` - `MESSAGE_TEMPLATES[MessageCategory.A2A]`

---

## Agent Workflow

### Example: Agent Completing a Task

1. **CYCLE START:**
   - Agent checks `get_tasks(section="THIS WEEK")`
   - Sees task: "Prototype Kiki's site theme"
   - Begins work

2. **DURING CYCLE:**
   - Agent identifies new subtask: "Upload photos"
   - Calls `add_task_to_inbox(task="Upload photos to Kiki site", agent_id="Agent-1")`

3. **CYCLE END:**
   - Agent completes main task
   - Calls `mark_task_complete(task_description="Prototype Kiki's site theme", section="THIS WEEK")`
   - Updates status.json, commits, posts devlog

### Example: Agent Blocked

1. **DURING CYCLE:**
   - Agent is blocked: "Waiting for logo from Little Sister"
   - Calls `move_task_to_waiting(task_description="Prototype Kiki's site theme", reason="waiting for logo from Little Sister", agent_id="Agent-1")`

2. **CYCLE END:**
   - Task is now in WAITING ON section
   - Agent moves to next available task

---

## Benefits

1. **Automatic Task Tracking** - Agents update task log automatically
2. **No Task Loss** - Everything captured in one place
3. **CEO Visibility** - Victor sees all tasks and status
4. **Delegation Ready** - Tasks can be assigned via DELEGATION_BOARD
5. **Swarm Coordination** - Tasks visible to all agents

---

## Integration Points

### With DELEGATION_BOARD.md
- Tasks in MASTER_TASK_LOG reference DELEGATION_BOARD for ownership
- Agents check DELEGATION_BOARD to see if task is assigned to them

### With SWARM_TASK_PACKETS.md
- Swarm packets can create tasks in INBOX
- Completed packets mark tasks complete

### With QUICK_START_GUIDE.md
- Agents reference guide for task management workflow
- CEO uses guide for delegation decisions

---

## Testing

### Manual Test

1. Start MCP server:
   ```bash
   python mcp_servers/task_manager_server.py
   ```

2. Test adding task:
   ```json
   {
     "method": "tools/call",
     "params": {
       "name": "add_task_to_inbox",
       "arguments": {
         "task": "Test task from agent",
         "agent_id": "Agent-1"
       }
     }
   }
   ```

3. Verify task appears in MASTER_TASK_LOG.md INBOX section

### Agent Test

1. Agent receives S2A message
2. Agent checks `get_tasks` at cycle start
3. Agent updates task log at cycle end
4. Verify updates in MASTER_TASK_LOG.md

---

## Troubleshooting

### MCP Server Not Found
- Check MCP configuration in client settings
- Verify Python path is correct
- Check file path in args

### Task Not Appearing
- Check MASTER_TASK_LOG.md file exists
- Verify file permissions
- Check regex patterns in server code

### Agent Not Updating
- Verify MCP tools are available to agent
- Check agent has access to task_manager_server
- Review cycle end checklist in agent messages

---

## Future Enhancements

1. **Task Assignment** - Directly assign tasks to agents via MCP
2. **Task Dependencies** - Link tasks that depend on each other
3. **Task Priorities** - Add priority levels to tasks
4. **Task Deadlines** - Add due dates to tasks
5. **Task Analytics** - Track completion rates, cycle times

---

## Related Documents

- `MASTER_TASK_LOG.md` - The task log file
- `DELEGATION_BOARD.md` - Task ownership assignments
- `SWARM_TASK_PACKETS.md` - Swarm execution directives
- `QUICK_START_GUIDE.md` - How to use the system
- `OWNERSHIP_DECISION_MATRIX.md` - Decision guide
- `mcp_servers/TASK_MANAGER_README.md` - MCP server documentation

