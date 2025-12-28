# MCP Task Manager HTTP Integration Architecture

## Overview

The HTTP `/tasks` endpoint (`task_manager_http_server.py`) integrates with the existing task management ecosystem through a well-defined data flow pipeline.

## Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  working_tree_audit.py (Audit Tool)                            │
│  - Detects foreign paths                                        │
│  - POSTs to /tasks endpoint                                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  task_manager_http_server.py (HTTP Shim)                        │
│  - Receives POST /tasks                                         │
│  - Calls add_to_inbox() from task_manager_server.py             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  task_manager_server.py (MCP Server)                            │
│  - add_to_inbox() writes to MASTER_TASK_LOG.md                  │
│  - Updates INBOX section                                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  MASTER_TASK_LOG.md (SSOT)                                      │
│  - INBOX section updated                                        │
│  - Tasks marked with agent assignment                           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  master_task_log_to_cycle_planner.py (Bridge Tool)             │
│  - Parses MASTER_TASK_LOG.md                                    │
│  - Extracts unchecked tasks with [Agent-X] tags                  │
│  - Writes to cycle_planner_tasks_YYYY-MM-DD.json                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  cycle_planner_tasks_YYYY-MM-DD.json (Agent Workspace)         │
│  - agent_workspaces/{Agent-X}/cycle_planner_tasks_*.json       │
│  - Tasks in JSON format for cycle planner                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  CyclePlannerIntegration (Contract System)                     │
│  - load_cycle_planner_tasks() reads JSON files                  │
│  - convert_task_to_contract() converts to contract format      │
│  - get_next_cycle_task() returns next available task           │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ContractManager.get_next_task()                                │
│  - Checks cycle planner first (via CyclePlannerIntegration)      │
│  - Falls back to contract storage                               │
│  - Bootstraps from MASTER_TASK_LOG if both empty                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Agent Resume/Onboarding                                        │
│  - ResumeCyclePlannerIntegration.get_and_claim_next_task()      │
│  - Task included in resume prompt                               │
│  - Agent claims task via contract system                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│  Agent Execution                                                │
│  - Updates status.json (FSM state transitions)                 │
│  - Completes work                                                │
│  - Marks task complete via MCP or contract system               │
└─────────────────────────────────────────────────────────────────┘
```

## System Components

### 1. HTTP Task Endpoint (`task_manager_http_server.py`)

**Purpose:** Provides HTTP interface for `working_tree_audit.py` to create tasks

**Endpoints:**
- `POST /tasks` - Create task in INBOX
- `POST /broadcast` - Acknowledge broadcast (placeholder)

**Integration:**
- Calls `add_to_inbox()` from `task_manager_server.py`
- Writes directly to `MASTER_TASK_LOG.md` INBOX section
- Returns task ID for audit evidence tracking

### 2. MCP Task Manager Server (`task_manager_server.py`)

**Purpose:** MCP protocol interface for task operations

**Functions:**
- `add_to_inbox()` - Adds task to MASTER_TASK_LOG.md INBOX
- `mark_task_complete()` - Marks task complete in MASTER_TASK_LOG.md
- `move_task_to_waiting()` - Moves task to WAITING ON section
- `get_tasks()` - Reads tasks from MASTER_TASK_LOG.md

**Integration:**
- Direct file I/O to `MASTER_TASK_LOG.md`
- Updates timestamp on changes
- Maintains markdown structure

### 3. MASTER_TASK_LOG.md (SSOT)

**Purpose:** Single source of truth for all tasks

**Sections:**
- `## 📥 INBOX` - New tasks (from audit tool, manual entry)
- `## 🎯 THIS WEEK` - Active tasks
- `## ⏳ WAITING ON` - Blocked tasks
- `## 🧊 PARKED` - Deferred tasks

**Task Format:**
```markdown
- [ ] **HIGH** (100 pts): Task description - [Agent-X]
```

**Integration:**
- Read by `master_task_log_to_cycle_planner.py`
- Updated by MCP task manager server
- Parsed by contract system bootstrap

### 4. MASTER_TASK_LOG → Cycle Planner Bridge

**Tool:** `tools/master_task_log_to_cycle_planner.py` (archived but functional)

**Purpose:** Seeds cycle planner JSON files from MASTER_TASK_LOG.md

**Process:**
1. Parses MASTER_TASK_LOG.md sections
2. Extracts unchecked tasks with `[Agent-X]` tags
3. Extracts priority, points, description
4. Writes to `agent_workspaces/{Agent-X}/cycle_planner_tasks_YYYY-MM-DD.json`

**Integration:**
- Called manually: `python tools/master_task_log_to_cycle_planner.py --agent Agent-X`
- Called automatically by ContractManager when bootstrapping
- Creates JSON files for cycle planner consumption

### 5. Cycle Planner Integration (`CyclePlannerIntegration`)

**Location:** `src/services/contract_system/cycle_planner_integration.py`

**Purpose:** Loads tasks from cycle planner JSON files into contract system

**Methods:**
- `load_cycle_planner_tasks()` - Reads JSON files from agent workspace
- `convert_task_to_contract()` - Converts cycle planner format to contract format
- `get_next_cycle_task()` - Returns next pending task
- `mark_task_complete()` - Updates JSON file when task completed

**Integration:**
- Called by `ContractManager.get_next_task()`
- Reads from `agent_workspaces/{Agent-X}/cycle_planner_tasks_*.json`
- Converts to contract format for contract system

### 6. Contract System (`ContractManager`)

**Location:** `src/services/contract_system/manager.py`

**Purpose:** Unified task assignment and claiming system

**Methods:**
- `get_next_task()` - Gets next task for agent (checks cycle planner first)
- `bootstrap_from_master_task_log()` - Seeds cycle planner from MASTER_TASK_LOG when empty
- `get_agent_status()` - Returns agent's contract status

**Integration Flow:**
1. Check cycle planner (via `CyclePlannerIntegration`)
2. If empty, check contract storage
3. If still empty, bootstrap from MASTER_TASK_LOG
4. Return task as contract

### 7. Resume Cycle Planner Integration

**Location:** `src/core/resume_cycle_planner_integration.py`

**Purpose:** Integrates task assignment into agent resume prompts

**Methods:**
- `get_and_claim_next_task()` - Gets and claims task for resume prompt
- Uses `ContractManager` to get task
- Returns task details for inclusion in prompt

**Integration:**
- Called during agent onboarding/resume
- Task included in S2A prompt
- Agent claims task via contract system

### 8. FSM System (Agent State Machines)

**Location:** `agent_workspaces/{Agent-X}/status.json`

**Purpose:** Tracks agent state transitions

**States:**
- `ACTIVE` - Agent executing tasks
- `IDLE` - Agent waiting for work
- `BLOCKED` - Agent blocked on dependency
- `COMPLETE` - Task completed

**Integration:**
- Updated when agent claims/completes tasks
- Read by coordination systems
- Used for agent lifecycle management

**Note:** FSM transitions are managed in `status.json`, not a separate FSM engine. State is inferred from status fields.

### 9. Markov Logic (`SmartAssignmentOptimizer`)

**Location:** `src/core/smart_assignment_optimizer.py`

**Purpose:** Intelligent agent assignment using Swarm Brain knowledge and Markov chain performance probabilities

**Components:**
- **Markov Chain:** Tracks agent performance history and transition probabilities
- **Swarm Brain Integration:** Uses knowledge base for agent capability matching
- **Score Calculation:** Combines Swarm Brain (70%) + Markov chain (30%) for assignment

**Methods:**
- `_initialize_markov_chain()` - Initializes agent performance probability matrix
- `_calculate_markov_score()` - Calculates score based on agent performance history
- `assign_violation()` - Assigns violations to best-suited agents

**Integration:**
- Called by `gasline_integrations.py` for violation assignment
- Uses Swarm Brain MCP server for knowledge queries
- Could integrate with `ContractManager` for task assignment optimization

**Current Usage:**
- V2 compliance violation assignment
- Agent capability matching
- Performance-based routing

**Potential Integration:**
- Extend to task assignment in `ContractManager.get_next_task()`
- Use Markov chain to influence task selection probabilities
- Model agent-task fit probabilistically

### 10. FSM System (`fsm_bridge.py`)

**Location:** `message_task/fsm_bridge.py`

**Purpose:** Bridges message-driven workflow with FSM state transitions

**Components:**
- **State Transition Matrix:** Validates agent state transitions
- **Message-Driven Triggers:** Messages trigger FSM state changes
- **State Validation:** Ensures valid state transitions

**Integration:**
- Reads agent `status.json` for current FSM state
- Validates transitions before state changes
- Integrates with messaging system for state-driven workflows

**Note:** FSM state is primarily tracked in `agent_workspaces/{Agent-X}/status.json` with fields like:
- `status`: ACTIVE, IDLE, BLOCKED, COMPLETE
- `current_phase`: TASK_EXECUTION, COORDINATION, etc.
- `fsm_state`: Explicit FSM state (if present)

### 11. Cycle Organizer (Referenced but Not Found)

**Status:** Referenced in documentation but no implementation found

**References Found:**
- `docs/STAGE4_WORKSPACE_INTEGRITY_INTEGRATION.md` mentions cycle organizer
- Described as coordinating agent work cycles
- Should read from MASTER_TASK_LOG and distribute tasks

**Possible Implementations:**
- May be planned but not yet implemented
- Could be part of `CyclePlannerIntegration` (already handles cycle planning)
- May refer to the operating cycle workflow (documented in `cycle_texts.py`)

**Recommendation:** If cycle organizer is needed, it could be:
- A wrapper around `CyclePlannerIntegration` + `ContractManager`
- A coordination layer that distributes tasks across agents
- An orchestrator that manages agent work cycles

## Data Flow Example

### Scenario: Foreign Path Detected by Audit Tool

1. **Audit Tool** (`working_tree_audit.py`)
   ```
   POST http://localhost:8000/tasks
   {
     "queue": "INBOX",
     "owner": "Agent-4",
     "title": "Working-tree triage: foreign paths detected",
     "metadata": {"paths": ["stray.tmp"], "bucket": "foreign.misc"}
   }
   ```

2. **HTTP Server** (`task_manager_http_server.py`)
   - Receives POST
   - Calls `add_to_inbox("Working-tree triage...", agent_id="Agent-4")`

3. **MCP Server** (`task_manager_server.py`)
   - Writes to MASTER_TASK_LOG.md INBOX section:
   ```markdown
   - [ ] Working-tree triage: foreign paths detected (from Agent-4)
   ```

4. **Bridge Tool** (manual or automatic)
   ```bash
   python tools/master_task_log_to_cycle_planner.py --agent Agent-4
   ```
   - Creates `agent_workspaces/Agent-4/cycle_planner_tasks_2025-12-28.json`:
   ```json
   {
     "pending_tasks": [{
       "task_id": "mtl-001",
       "title": "Working-tree triage: foreign paths detected",
       "priority": "medium",
       "status": "pending"
     }]
   }
   ```

5. **Contract System** (next agent resume)
   - `ContractManager.get_next_task("Agent-4")`
   - `CyclePlannerIntegration.get_next_cycle_task("Agent-4")`
   - Returns contract for task

6. **Agent Resume**
   - `ResumeCyclePlannerIntegration.get_and_claim_next_task("Agent-4")`
   - Task included in S2A prompt
   - Agent claims and executes

7. **Completion**
   - Agent marks task complete via MCP: `mark_task_complete()`
   - Updates MASTER_TASK_LOG.md: `[x]` checkbox
   - Updates cycle planner JSON: `status: "completed"`

## Integration Points Summary

| System | Integration Method | Data Format | Update Frequency | Location |
|--------|-------------------|-------------|------------------|----------|
| HTTP /tasks | REST API POST | JSON payload | On-demand (audit tool) | `mcp_servers/task_manager_http_server.py` |
| MCP Task Manager | MCP protocol | JSON-RPC | On-demand (agents) | `mcp_servers/task_manager_server.py` |
| MASTER_TASK_LOG | File I/O | Markdown | Real-time (MCP writes) | `MASTER_TASK_LOG.md` |
| Cycle Planner Bridge | Python script | JSON files | Manual or bootstrap | `tools/master_task_log_to_cycle_planner.py` |
| Contract System | Python imports | Contract objects | On agent resume | `src/services/contract_system/manager.py` |
| Cycle Planner Integration | Python imports | JSON → Contract | On task claim | `src/services/contract_system/cycle_planner_integration.py` |
| Resume Integration | Python imports | Contract → Prompt | On resume | `src/core/resume_cycle_planner_integration.py` |
| FSM System | status.json | JSON | On state transitions | `agent_workspaces/{Agent-X}/status.json` |
| FSM Bridge | Python imports | State validation | On messages | `message_task/fsm_bridge.py` |
| Markov Logic | Python imports | Probability matrix | On assignment | `src/core/smart_assignment_optimizer.py` |
| Gas Pipeline | Python imports | Auto-gas triggers | Perpetual motion | `src/core/auto_gas_pipeline_system.py` |

## Integration Enhancements

### Markov Logic Integration Opportunity

**Current State:** Markov logic exists but only used for violation assignment

**Enhancement:** Extend `SmartAssignmentOptimizer` to `ContractManager`

**Implementation:**
```python
# In ContractManager.get_next_task()
if self.markov_optimizer:
    # Use Markov chain to score task-agent fit
    scores = self.markov_optimizer.score_agents_for_task(task)
    # Select agent with highest score
```

**Benefits:**
- Probabilistic task assignment based on agent performance history
- Better task-agent matching
- Performance-based routing

### FSM Integration Enhancement

**Current State:** FSM tracked in status.json, validated by fsm_bridge.py

**Enhancement:** Auto-update FSM state on task claim/completion

**Implementation:**
```python
# On task claim
update_fsm_state(agent_id, "ACTIVE", "TASK_EXECUTION")

# On task completion  
update_fsm_state(agent_id, "IDLE", "AWAITING_ASSIGNMENT")
```

**Benefits:**
- Automatic state tracking
- State-driven workflows
- Better coordination visibility

## Recommendations

1. **Automate Bridge Execution**
   - Add cron/scheduler to run `master_task_log_to_cycle_planner.py` periodically
   - Or trigger on MASTER_TASK_LOG.md changes

2. **Add Task ID Tracking**
   - HTTP endpoint should return task ID
   - Store task ID in audit evidence JSON
   - Enable task completion tracking

3. **FSM Integration**
   - Update FSM state when task claimed/completed
   - Add state transition logging
   - Integrate with status.json updates

4. **Markov Logic (if needed)**
   - Implement probabilistic task assignment
   - Model agent capabilities and task fit
   - Use for intelligent task routing

5. **Cycle Organizer (if exists)**
   - Document cycle organizer system if found
   - Integrate with cycle planner JSON files
   - Coordinate task scheduling

