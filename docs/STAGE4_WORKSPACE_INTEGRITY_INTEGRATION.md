# Stage-4 Workspace Integrity Enforcement - System Integration

**Date:** 2025-12-28  
**Agent:** Agent-4 (Captain)  
**Status:** ✅ Implementation Complete

## Overview

Stage-4 workspace integrity enforcement provides **governance infrastructure** that integrates with all major agent systems to enforce workspace sovereignty and prevent scope violations.

## Architecture: The Integration Triangle

```
┌─────────────────────────────────────────────────────────┐
│              WORKING TREE AUDIT (Sensor)                 │
│  • Captures git status snapshot                          │
│  • Classifies foreign paths                              │
│  • Creates tasks via HTTP /tasks                        │
│  • Broadcasts violations                                 │
│  • Writes evidence JSON                                 │
└─────────────────────────────────────────────────────────┘
                        │
                        │ evidence file
                        ▼
┌─────────────────────────────────────────────────────────┐
│        CLOSURE VALIDATOR (Judge)                        │
│  • Validates closure format                             │
│  • Checks audit evidence exists                         │
│  • Verifies timestamp freshness                         │
│  • Validates foreign paths handled                      │
│  • Gates closure acceptance                             │
└─────────────────────────────────────────────────────────┘
                        │
                        │ blocks closure
                        ▼
┌─────────────────────────────────────────────────────────┐
│      TASK MANAGER SERVER (Dispatcher)                   │
│  • HTTP /tasks endpoint                                 │
│  • Creates tasks in MASTER_TASK_LOG                      │
│  • Integrates with contract system                      │
│  • Enables automated task creation                      │
└─────────────────────────────────────────────────────────┘
```

## Integration Points

### 1. Master Task Log Integration

**How it works:**
- `working_tree_audit.py` detects foreign paths
- Creates tasks via HTTP POST to `/tasks` endpoint
- `task_manager_http_server.py` receives POST request
- Calls `add_to_inbox()` from `task_manager_server.py`
- Task written to `MASTER_TASK_LOG.md` INBOX section

**Integration code:**
```python
# working_tree_audit.py creates task
task_id = create_task(
    task_manager_url,
    owner="Agent-X",  # Foreign path owner
    title="Working-tree triage: foreign paths detected",
    metadata={"paths": paths, "bucket": bucket}
)

# task_manager_http_server.py handles POST
@app.post("/tasks")
async def create_task(request: Request):
    payload = await request.json()
    result = add_to_inbox(task_text, agent_id=owner)
    # Task written to MASTER_TASK_LOG.md
```

**Evidence tracking:**
- Task IDs stored in `working_tree_audit_*.json` → `task_ids` field
- Validator checks `task_ids` contains all foreign path buckets
- Missing task IDs → closure BLOCKED

### 2. Cycle Planner Integration

**How it works:**
- Cycle planner reads from `MASTER_TASK_LOG.md` via `master_task_log_to_cycle_planner.py`
- Tasks created by audit tool appear in INBOX
- Cycle planner bridge converts INBOX tasks to cycle planner format
- Agents claim tasks via contract system

**Integration flow:**
```
Audit → Creates task in MASTER_TASK_LOG.md INBOX
  ↓
Cycle Planner Bridge → Reads INBOX, converts to cycle_planner_tasks_YYYY-MM-DD.json
  ↓
Contract System → Agent claims task via get_next_task()
  ↓
FSM System → Updates agent state to TASK_EXECUTION
```

**Code references:**
- `src/services/contract_system/cycle_planner_integration.py` - Loads cycle planner tasks
- `src/core/resume_cycle_planner_integration.py` - Auto-claims tasks on resume
- `tools/master_task_log_to_cycle_planner.py` - Bridge from MASTER_TASK_LOG to cycle planner

### 3. Contract System Integration

**How it works:**
- Contract system uses `ContractManager.get_next_task()`
- Checks cycle planner first, then contract storage
- Tasks from audit appear as cycle planner tasks
- Contracts track task assignment and completion

**Integration points:**
- `src/services/contract_system/manager.py` - ContractManager
- `src/services/contract_system/cycle_planner_integration.py` - CyclePlannerIntegration
- Contract storage tracks task lifecycle

**Task lifecycle:**
```
pending → assigned → active → completed
  ↑                      ↓
  └─── audit creates ────┘
```

### 4. FSM System Integration

**How it works:**
- FSM tracks agent state transitions
- Closure validation gates state transitions
- Blocked closures prevent FSM from moving to COMPLETE state
- Evidence check ensures workspace integrity before state change

**FSM States:**
- `ACTIVE` - Agent executing tasks
- `TASK_EXECUTION` - Working on assigned task
- `CLOSURE` - Preparing session closure
- `BLOCKED` - Closure validation failed (audit evidence missing/invalid)

**Integration code:**
- `src/core/constants/fsm.py` - FSM state definitions
- `src/core/constants/fsm_models.py` - State/transition models
- Closure validator checks audit evidence before allowing FSM transition

**State transition guard:**
```python
# Pseudo-code: FSM transition guard
def can_transition_to_complete(agent_id):
    # Check closure format
    closure_valid = validate_closure_format(closure_file)
    if not closure_valid:
        return False, "Closure format invalid"
    
    # Check audit evidence
    audit_check = check_audit_evidence(closure_file)
    if audit_check.error:
        return False, f"Audit evidence check failed: {audit_check.error}"
    
    return True, "Ready to complete"
```

### 5. Cycle Organizer Integration

**How it works:**
- Cycle organizer coordinates agent work cycles
- Audit evidence ensures workspace integrity at cycle boundaries
- Foreign paths trigger coordination tasks
- Cycle organizer distributes triage tasks to appropriate agents

**Integration points:**
- Cycle organizer reads from MASTER_TASK_LOG
- Tasks created by audit appear as coordination opportunities
- Cycle organizer assigns triage tasks to foreign path owners

### 6. Markov Logic Integration

**Note:** No explicit "Markov logic" system found in codebase. However, the **smart assignment optimizer** (`src/core/smart_assignment_optimizer.py`) provides similar probabilistic task assignment logic.

**How it could integrate:**
- Smart assignment optimizer uses probability models for task assignment
- Audit evidence provides **hard constraints** (foreign paths must be triaged)
- Optimizer respects audit constraints when assigning tasks
- Probability weights adjusted based on workspace integrity violations

**Potential integration:**
```python
# Smart assignment with audit constraints
def assign_task_with_audit_constraints(task, agents):
    # Check audit evidence for foreign paths
    audit_evidence = load_latest_audit_evidence()
    foreign_paths = audit_evidence.get("foreign_paths", {})
    
    # Hard constraint: foreign path owners must triage
    if task.type == "triage" and task.path_owner in foreign_paths:
        return assign_to(task.path_owner)  # Hard constraint
    
    # Otherwise use probabilistic assignment
    return smart_assign(task, agents)  # Probabilistic
```

## Data Flow: Complete Integration

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Agent executes work (modifies files)                    │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. working_tree_audit.py runs (pre-commit hook or manual)   │
│    • Captures git status                                    │
│    • Classifies foreign paths                               │
│    • Creates tasks via HTTP POST to /tasks                  │
│    • Broadcasts violations                                  │
│    • Writes evidence: reports/working_tree_audit_*.json     │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. task_manager_http_server.py receives POST               │
│    • Calls add_to_inbox()                                   │
│    • Writes task to MASTER_TASK_LOG.md INBOX                │
│    • Returns task_id                                        │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. master_task_log_to_cycle_planner.py bridge               │
│    • Reads MASTER_TASK_LOG.md INBOX                          │
│    • Converts to cycle_planner_tasks_YYYY-MM-DD.json         │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Contract System (ContractManager)                        │
│    • get_next_task() checks cycle planner                    │
│    • Agent claims task                                      │
│    • Contract created/assigned                               │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. FSM System                                                │
│    • Agent state: ACTIVE → TASK_EXECUTION                    │
│    • Task execution                                          │
│    • State: TASK_EXECUTION → CLOSURE                         │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Closure Validation (validate_closure_format.py)         │
│    • Checks closure format                                   │
│    • Checks audit evidence exists                            │
│    • Validates timestamp freshness                           │
│    • Verifies foreign paths have task_ids                    │
│    • Verifies broadcast_sent = true                          │
│    • BLOCKS closure if evidence invalid                      │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. FSM Transition (if validation passes)                    │
│    • State: CLOSURE → COMPLETE                               │
│    • Task marked complete in cycle planner                   │
│    • Contract marked complete                                │
│    • MASTER_TASK_LOG updated                                 │
└─────────────────────────────────────────────────────────────┘
```

## Enforcement Gates

### Gate 1: Pre-Commit Hook (Optional)
```bash
# .git/hooks/pre-commit
python tools/working_tree_audit.py --agent Agent-X --no-network
if [ $? -eq 2 ]; then
    echo "BLOCKED: Foreign paths detected without tasks/broadcast"
    exit 1
fi
```

### Gate 2: Closure Validation (Mandatory)
```python
# validate_closure_format.py
audit_error = validator._check_audit_evidence(closure_file_path)
if audit_error:
    violations.append(f'Audit evidence check failed: {audit_error}')
    sys.exit(1)  # Blocks closure
```

### Gate 3: CI/CD Pipeline (Recommended)
```yaml
# .github/workflows/validate-closures.yml
- name: Validate closure format
  run: |
    python tools/validate_closure_format.py closure.md
    if [ $? -ne 0 ]; then
      exit 1  # Fails CI
    fi
```

## Evidence File Format

**Location:** `reports/working_tree_audit_YYYYMMDD_HHMMSS.json`

**Structure:**
```json
{
  "ts": "20251228_014450",
  "agent": "Agent-4",
  "snapshot_file": "reports/working_tree_diff_20251228_014450.txt",
  "status_count": 166,
  "foreign_paths": {
    "Agent-2": ["agent_workspaces/Agent-2/status.json"],
    "foreign.misc": ["stray.tmp"]
  },
  "task_ids": {
    "Agent-2": "task_12345",
    "foreign.misc": "task_67890"
  },
  "broadcast_required": true,
  "broadcast_sent": true
}
```

**Validation rules:**
1. **Timestamp freshness:** Audit must be within 1 hour of closure
2. **Foreign paths → task_ids:** All foreign path buckets must have task IDs
3. **Broadcast required:** If foreign paths exist, `broadcast_sent` must be `true`

## Integration Benefits

### 1. **Automated Task Creation**
- Foreign paths automatically create triage tasks
- No manual task entry required
- Tasks appear in MASTER_TASK_LOG → cycle planner → contract system

### 2. **Enforced Coordination**
- Broadcast ensures swarm awareness
- Task IDs ensure accountability
- Evidence file provides audit trail

### 3. **FSM State Integrity**
- Closure validation gates state transitions
- Prevents agents from completing with workspace violations
- Ensures workspace sovereignty

### 4. **Contract System Alignment**
- Tasks from audit integrate with contract lifecycle
- Contract system tracks triage task completion
- Cycle planner distributes work appropriately

### 5. **Observable State**
- Evidence files provide timestamped snapshots
- Audit trail enables debugging and analysis
- Hard evidence prevents "he said, she said" disputes

## Usage Examples

### Example 1: Normal Flow (No Foreign Paths)
```bash
# 1. Agent works on task
git add agent_workspaces/Agent-4/my_file.py
git commit -m "feat: Add feature"

# 2. Audit runs (no foreign paths)
python tools/working_tree_audit.py --agent Agent-4 --no-network
# Exit code: 0 (OK)

# 3. Closure validation
python tools/validate_closure_format.py closure.md
# ✅ Closure format is valid
# ✅ Audit evidence found and valid
```

### Example 2: Foreign Paths Detected
```bash
# 1. Agent accidentally modifies foreign file
git add agent_workspaces/Agent-2/status.json

# 2. Audit runs (detects foreign path)
python tools/working_tree_audit.py --agent Agent-4 --task-manager-url http://localhost:8000
# Creates task in MASTER_TASK_LOG.md
# Broadcasts to swarm
# Exit code: 0 (OK - tasks created)

# 3. Closure validation
python tools/validate_closure_format.py closure.md
# ✅ Closure format is valid
# ✅ Audit evidence found
# ✅ Foreign paths have task_ids
# ✅ Broadcast sent
```

### Example 3: Violation (Missing Tasks)
```bash
# 1. Audit runs but task creation fails
python tools/working_tree_audit.py --agent Agent-4 --no-network
# Exit code: 2 (BLOCKED - foreign paths without tasks)

# 2. Closure validation
python tools/validate_closure_format.py closure.md
# ❌ Audit evidence check failed: Foreign paths detected but missing task IDs
# Exit code: 1 (BLOCKED)
```

## Configuration

### Environment Variables
```bash
# Task manager HTTP server URL
export TASK_MANAGER_URL="http://localhost:8000"

# Messaging server URL (for broadcasts)
export MSG_SERVER_URL="http://localhost:8001"
```

### HTTP Server Startup
```bash
# Start task manager HTTP server
python mcp_servers/task_manager_http_server.py --host 127.0.0.1 --port 8000
```

## Future Enhancements

1. **FSM Integration Hook**
   - Add FSM transition guard that calls audit evidence check
   - Prevent state transitions if evidence invalid

2. **Contract System Hook**
   - Auto-create contracts from audit tasks
   - Track triage task completion in contract lifecycle

3. **Cycle Organizer Integration**
   - Cycle organizer reads audit evidence
   - Distributes triage tasks based on foreign path ownership
   - Coordinates triage completion

4. **Markov Logic Integration**
   - Smart assignment optimizer respects audit constraints
   - Probabilistic assignment weighted by workspace integrity

5. **Pre-Commit Hook**
   - Automatic audit on every commit
   - Blocks commits with unhandled foreign paths

## References

- **Audit Tool:** `tools/working_tree_audit.py`
- **Validator:** `tools/validate_closure_format.py`
- **HTTP Server:** `mcp_servers/task_manager_http_server.py`
- **Task Manager:** `mcp_servers/task_manager_server.py`
- **Cycle Planner:** `src/services/contract_system/cycle_planner_integration.py`
- **Contract System:** `src/services/contract_system/manager.py`
- **FSM System:** `src/core/constants/fsm.py`
- **Resume Integration:** `src/core/resume_cycle_planner_integration.py`

