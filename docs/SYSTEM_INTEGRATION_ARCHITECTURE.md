<<<<<<< HEAD
<!-- SSOT Domain: documentation -->

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
# System Integration Architecture

## Overview

The MCP servers are the **interface layer** that integrates with the core swarm systems. Here's how everything connects:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MCP SERVERS (Interface Layer)                       │
├──────────────────┬──────────────────┬──────────────────┬───────────────────┤
│ task-manager     │ swarm-brain      │ swarm-messaging  │ deployment        │
│ cleanup-manager  │ git-operations   │ discord-integration│ validation-audit │
└────────┬─────────┴────────┬─────────┴────────┬─────────┴─────────┬─────────┘
         │                  │                  │                   │
         ▼                  ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CORE SYSTEMS LAYER                                 │
├──────────────────┬──────────────────┬──────────────────┬───────────────────┤
│ MASTER_TASK_LOG  │  Swarm Brain     │  Messaging CLI   │  Deployment       │
│ (SSOT)           │  (Knowledge DB)  │  (PyAutoGUI)     │  Scripts          │
└────────┬─────────┴────────┬─────────┴────────┬─────────┴─────────┬─────────┘
         │                  │                  │                   │
         ▼                  ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Cycle Planner  │  Contract System  │  FSM Bridge  │  Markov Optimizer     │
│  Integration    │  (Manager)        │  (State)     │  (Smart Assignment)   │
└─────────────────┴───────────────────┴──────────────┴───────────────────────┘
         │                  │                  │                   │
         ▼                  ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Agent-1  │  Agent-2  │  Agent-3  │  Agent-4  │  Agent-5  │  ...           │
│  status.json (FSM State)  │  inbox/  │  passdown.json  │  devlogs/         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. MASTER_TASK_LOG.md (Central Task Registry)

### What It Is
The **Single Source of Truth (SSOT)** for all tasks across the swarm.

### Structure
```markdown
## 📥 INBOX        # New tasks, unassigned
## 🎯 THIS WEEK    # Active tasks, assigned to agents
## ⏳ WAITING ON   # Blocked tasks
## 🧊 PARKED       # Deferred tasks
```

### How MCP Integrates
```
task-manager MCP
      │
      ├── add_task_to_inbox()     → Writes to INBOX section
      ├── mark_task_complete()    → Marks [x] checkbox
      ├── move_task_to_waiting()  → Moves to WAITING ON section
      └── get_tasks()             → Reads all sections
```

---

## 2. Cycle Planner System

### What It Is
Converts MASTER_TASK_LOG tasks into **per-agent JSON files** for daily planning.

### Location
```
agent_workspaces/{Agent-X}/cycle_planner_tasks_YYYY-MM-DD.json
```

### Integration Flow
```
MASTER_TASK_LOG.md
        │
        ▼
master_task_log_to_cycle_planner.py  (Bridge)
        │
        ▼
cycle_planner_tasks_YYYY-MM-DD.json  (Per-agent)
        │
        ▼
CyclePlannerIntegration.load_cycle_planner_tasks()
        │
        ▼
ContractManager.get_next_task()  (Returns as contract)
```

### Key File
`src/services/contract_system/cycle_planner_integration.py`

```python
class CyclePlannerIntegration:
    def load_cycle_planner_tasks(agent_id, target_date)  # Reads JSON
    def convert_task_to_contract(task, agent_id)         # → Contract format
    def get_next_cycle_task(agent_id)                    # Next pending task
    def mark_task_complete(agent_id, task_id)            # Update JSON
```

---

## 3. Contract System

### What It Is
The **assignment and claiming system** for agent tasks. Ensures agents have assigned work.

### Location
`src/services/contract_system/manager.py`

### Integration Flow
```
Agent Resume/Onboarding
        │
        ▼
ContractManager.get_next_task(agent_id)
        │
        ├── 1. Check CyclePlannerIntegration (first priority)
        ├── 2. Check ContractStorage (fallback)
        └── 3. Bootstrap from MASTER_TASK_LOG (if empty)
        │
        ▼
Return Contract { task_id, title, priority, status, agent_id }
```

### Key Methods
```python
class ContractManager:
    get_next_task(agent_id)              # Primary entry point
    bootstrap_from_master_task_log()     # Seeds cycle planner if empty
    get_agent_status(agent_id)           # Contract status
    get_system_status()                  # Overall status
```

---

## 4. FSM System (Finite State Machine)

### What It Is
Tracks **agent state transitions** during task execution.

### State Storage
```
agent_workspaces/{Agent-X}/status.json
```

### States
```
┌───────┐      claim      ┌────────┐     complete    ┌──────┐
│ IDLE  │ ───────────────▶│ ACTIVE │ ──────────────▶ │ DONE │
└───────┘                 └────────┘                 └──────┘
                              │
                          blocked
                              │
                              ▼
                        ┌─────────┐
                        │ BLOCKED │
                        └─────────┘
```

### Integration Points

#### A. Agent Lifecycle (`src/core/agent_lifecycle.py`)
```python
class AgentLifecycle:
    start_cycle()           # IDLE → ACTIVE
    start_mission(name)     # Updates mission
    complete_task(title)    # Task completion
    end_cycle(commit=True)  # Final cleanup
```

#### B. FSM Bridge (`src/message_task/fsm_bridge.py`)
```python
class TaskState(Enum):
    TODO = "todo"
    DOING = "doing"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"

def can_transition(from_state, to_state) → bool
def get_transition_event(from_state, to_state) → TaskEvent
```

#### C. status.json Structure
```json
{
  "agent_id": "Agent-7",
  "status": "ACTIVE",
  "fsm_state": "doing",
  "current_phase": "TASK_EXECUTION",
  "current_mission": "Tool Consolidation",
  "mission_priority": "HIGH",
  "cycle_count": 42,
  "current_tasks": ["Consolidate tools"],
  "completed_tasks": ["Archive obsolete tools"],
  "blockers": []
}
```

---

## 5. Markov Logic (Smart Assignment)

### What It Is
**Probabilistic agent assignment** using performance history and knowledge base.

### Location
`src/core/smart_assignment_optimizer.py`

### Algorithm
```
Assignment Score = 
    (Specialization Match × 0.4) +
    (Markov Performance × 0.3) +
    (Swarm Brain Knowledge × 0.2) +
    (Workload Balance × 0.1)
```

### Components
```python
class SmartAssignmentOptimizer:
    # Agent specialization mapping
    agent_specializations = {
        "Agent-1": ["testing", "qa", "integration"],
        "Agent-2": ["architecture", "v2_compliance"],
        "Agent-3": ["infrastructure", "devops"],
        "Agent-7": ["web", "frontend", "ui"],
        ...
    }
    
    # Markov chain (performance history)
    markov_chain = {
        "Agent-1": {"success_rate": 0.85, "avg_completion_time": 0.8},
        ...
    }
    
    def assign_violations(violations) → Dict[agent_id, List[violations]]
    def _find_best_agent_for_violation(violation) → agent_id
    def _calculate_markov_score(agent_id, violation_type) → float
```

### Integration with Swarm Brain
```python
# Uses swarm-brain MCP server
self.swarm_memory = SwarmMemory(agent_id="GaslineHub")
history = self.swarm_memory.search_swarm_knowledge("agent performance")
```

---

## 6. Complete Integration Flow

### Task Lifecycle Example

```
1. TASK CREATION
   ┌─────────────────────────────────────────────────────────────┐
   │  Captain/Agent creates task                                  │
   │  → mcp_task-manager_add_task_to_inbox("Fix bug", "Agent-7") │
   │  → Writes to MASTER_TASK_LOG.md INBOX                        │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
2. CYCLE PLANNING
   ┌─────────────────────────────────────────────────────────────┐
   │  master_task_log_to_cycle_planner.py --agent Agent-7        │
   │  → Creates cycle_planner_tasks_2025-12-28.json              │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
3. CONTRACT ASSIGNMENT
   ┌─────────────────────────────────────────────────────────────┐
   │  Agent resumes / gets onboarded                             │
   │  → ContractManager.get_next_task("Agent-7")                 │
   │  → CyclePlannerIntegration.get_next_cycle_task()            │
   │  → Returns Contract { task_id, title, priority }            │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
4. FSM STATE TRANSITION
   ┌─────────────────────────────────────────────────────────────┐
   │  AgentLifecycle.start_mission("Fix bug", "HIGH")            │
   │  → status.json: status="ACTIVE", fsm_state="doing"          │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
5. TASK EXECUTION
   ┌─────────────────────────────────────────────────────────────┐
   │  Agent works on task                                         │
   │  → Uses mcp_swarm-brain_share_learning() for knowledge       │
   │  → Uses mcp_git-operations_* for verification               │
   │  → Uses mcp_deployment-manager_* for deployments            │
   └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
6. TASK COMPLETION
   ┌─────────────────────────────────────────────────────────────┐
   │  AgentLifecycle.complete_task("Fix bug")                    │
   │  → status.json: status="IDLE", completed_tasks++            │
   │  → mcp_task-manager_mark_task_complete("Fix bug")           │
   │  → MASTER_TASK_LOG.md: [x] Fix bug                          │
   │  → CyclePlannerIntegration.mark_task_complete()             │
   └─────────────────────────────────────────────────────────────┘
```

---

## 7. MCP Server Integration Matrix

| MCP Server | Integrates With | How |
|------------|-----------------|-----|
| `task-manager` | MASTER_TASK_LOG.md | Direct file I/O |
| `task-manager` | Cycle Planner | Via bridge tool |
| `swarm-brain` | Markov Optimizer | Knowledge queries |
| `swarm-brain` | Agent decisions | Learning storage |
| `swarm-messaging` | Agent coordination | PyAutoGUI delivery |
| `cleanup-manager` | Agent workspaces | Inbox archival |
| `git-operations` | Work verification | Git log parsing |
| `deployment` | Website systems | SFTP/WP-CLI |
| `validation-audit` | Closure compliance | Format checking |
| `devlog-manager` | Discord | Webhook posting |
| `discord-integration` | Notifications | Webhooks |

---

## 8. Key Integration Files

| System | File | Purpose |
|--------|------|---------|
| Task Manager MCP | `mcp_servers/task_manager_server.py` | MCP interface |
| Cycle Planner | `src/services/contract_system/cycle_planner_integration.py` | Task loading |
| Contract Manager | `src/services/contract_system/manager.py` | Assignment |
| FSM Bridge | `src/message_task/fsm_bridge.py` | State transitions |
| Agent Lifecycle | `src/core/agent_lifecycle.py` | Status updates |
| Markov Optimizer | `src/core/smart_assignment_optimizer.py` | Smart assignment |
| Resume Integration | `src/core/resume_cycle_planner_integration.py` | Onboarding |

---

## 9. Current Gaps & Enhancement Opportunities

### Gap 1: Cycle Planner Automation
**Current:** Bridge tool runs manually
**Enhancement:** Auto-trigger on MASTER_TASK_LOG changes

### Gap 2: Markov in Contract System
**Current:** Only used for violation assignment
**Enhancement:** Extend to all task assignments

### Gap 3: FSM Webhook Notifications
**Current:** FSM state in status.json only
**Enhancement:** Notify Discord on state transitions

### Gap 4: Cycle Organizer
**Referenced:** In documentation
**Status:** Not implemented
**Recommendation:** May be redundant with CyclePlannerIntegration

---

## 10. System Health Indicators

```
✅ MASTER_TASK_LOG.md exists and has tasks
✅ Cycle planner JSON files generated daily
✅ ContractManager returns tasks for agents
✅ FSM states in status.json are valid
✅ Markov chain has performance history
✅ Swarm Brain queries return results
```

---

## Summary

The MCP servers provide the **interface layer** that agents use to interact with:

1. **MASTER_TASK_LOG** → `task-manager` MCP
2. **Cycle Planner** → via Contract System
3. **Contract System** → Python imports + MCP
4. **FSM System** → `status.json` + AgentLifecycle
5. **Markov Logic** → SmartAssignmentOptimizer + swarm-brain MCP
6. **Knowledge Base** → `swarm-brain` MCP

All systems work together to ensure:
- Tasks flow from creation to completion
- Agents get appropriate assignments
- State transitions are tracked
- Knowledge is preserved and queried

