# Cycle Planner & Agent Coordination Workflow Guide

**Date**: 2025-12-10  
**Author**: Agent-1 (Integration & Core Systems Specialist)  
**Status**: ✅ **WORKFLOW DOCUMENTATION**

---

## 🎯 Overview

This guide answers two critical workflow questions:
1. **When/where are tasks added to the cycle planner?**
2. **At what point in the agent operating cycle should agents message each other?**

---

## 📋 **CYCLE PLANNER TASK CREATION**

### **When Tasks Are Added to Cycle Planner**

Tasks are added to the cycle planner at **specific points in the agent operating cycle**:

#### **1. CYCLE START - Task Discovery Phase**
**Location**: `agent_workspaces/swarm_cycle_planner/cycles/{date}_{agent-id}_pending_tasks.json`

**When**:
- **During "Claim" phase** (Step 1 of Agent Operating Cycle)
- **During "Sync SSOT/context" phase** (Step 2 of Agent Operating Cycle)
- **When checking Contract System** (`--get-next-task`)

**Who Creates Tasks**:
- **Captain (Agent-4)**: Creates initial cycle planner tasks for all agents
- **Agents**: Can add tasks to their own cycle planner file when:
  - Breaking down large tasks into smaller slices
  - Discovering new work items during context sync
  - Creating follow-up tasks from completed work

**How Tasks Are Created**:
```python
# Example: Creating a cycle planner task file
from pathlib import Path
import json
from datetime import date

task_file = Path(f"agent_workspaces/swarm_cycle_planner/cycles/{date.today().isoformat()}_{agent_id.lower()}_pending_tasks.json")

task_data = {
    "agent_id": "Agent-1",
    "date": date.today().isoformat(),
    "contracts": [
        {
            "contract_id": "task_id",
            "title": "Task Title",
            "description": "Task description",
            "priority": "HIGH",
            "status": "pending",
            "estimated_time": "2-3 hours",
            "dependencies": [],
            "deliverables": []
        }
    ]
}

# Write to file
with open(task_file, 'w') as f:
    json.dump(task_data, f, indent=2)
```

#### **2. DURING CYCLE - Task Breakdown**
**When**: During "Slice" phase (Step 3 of Agent Operating Cycle)

**Scenario**: Agent receives a large task and needs to break it down
- Agent analyzes task complexity
- Creates sub-tasks in cycle planner
- Assigns sub-tasks to other agents (if multi-domain)

**Example**:
```python
# During slice phase, agent breaks down task
if task_complexity > 1_cycle:
    # Create sub-tasks in cycle planner
    sub_tasks = break_down_task(main_task)
    for sub_task in sub_tasks:
        add_to_cycle_planner(sub_task)
```

#### **3. CYCLE END - Next Session Planning**
**When**: During "Report evidence" phase (Step 7 of Agent Operating Cycle)

**Scenario**: Agent completes current work and identifies next priorities
- Agent reviews completed work
- Identifies follow-up tasks
- Adds tasks to cycle planner for next session

**Tool**: `tools/session_transition_helper.py` (Step 8: Add Pending Tasks to Cycle Planner)

---

## 🔄 **AGENT COORDINATION MESSAGING**

### **When Agents Should Message Each Other**

#### **1. CYCLE START - Task Assessment**
**Phase**: "Slice" phase (Step 3 of Agent Operating Cycle)

**When to Message**:
- **Task is too large** (>1 cycle estimated)
- **Task spans multiple domains** (requires expertise from other agents)
- **Task has multiple independent components** (can be parallelized)

**Message Type**: A2A (Agent-to-Agent) coordination message

**Example**:
```bash
# During slice phase, if task needs delegation
python -m src.services.messaging_cli --agent Agent-2 --message "Large refactor task: Need architecture review for module X, Y, Z. Can you handle architecture patterns while I handle integration?" --priority normal
```

#### **2. DURING CYCLE - Task Expansion**
**Phase**: "Execute" phase (Step 4 of Agent Operating Cycle)

**When to Message**:
- **Task scope expands** beyond initial estimate
- **Blockers discovered** that require other agent's expertise
- **Integration points identified** that need coordination

**Message Type**: A2A coordination message

**Example**:
```bash
# During execution, if task expands
python -m src.services.messaging_cli --agent Agent-7 --message "Task expanded: Need web interface for feature X. Can you handle frontend while I complete backend integration?" --priority normal
```

#### **3. DURING CYCLE - Bilateral Coordination**
**Phase**: "Execute" phase (Step 4 of Agent Operating Cycle)

**When to Message**:
- **2-agent task** identified (default for bilateral coordination)
- **Handoff points** established
- **Integration checkpoints** need coordination

**Message Type**: A2A coordination message with task breakdown

**Example**:
```bash
# Bilateral coordination for 2-agent task
python -m src.services.messaging_cli --agent Agent-8 --message "SSOT coordination: Task breakdown - I handle integration layer, you handle SSOT compliance verification. Handoff point: after integration tests pass." --priority normal
```

#### **4. DURING CYCLE - Swarm Assignment**
**Phase**: "Slice" phase (Step 3 of Agent Operating Cycle) - **BEFORE execution**

**When to Message**:
- **3+ agent task** identified
- **Task broken down** into 3-8 parallel sub-tasks
- **All assignments ready** to send simultaneously

**Message Type**: Multiple A2A assignment messages (sent in parallel)

**Example**:
```bash
# Swarm assignment - send all at once
python -m src.services.messaging_cli --agent Agent-2 --message "64 Files: 5 architecture files assigned" --priority normal
python -m src.services.messaging_cli --agent Agent-3 --message "64 Files: 5 infrastructure files assigned" --priority normal
python -m src.services.messaging_cli --agent Agent-5 --message "64 Files: 4 analytics files assigned" --priority normal
# ... etc
```

#### **5. CYCLE END - Coordination Outcomes**
**Phase**: "Report evidence" phase (Step 7 of Agent Operating Cycle)

**When to Message**:
- **Swarm was engaged** during cycle
- **Coordination outcomes** need reporting
- **Integration results** need validation

**Message Type**: A2A status update or completion report

---

## 📊 **WORKFLOW INTEGRATION POINTS**

### **Agent Operating Cycle with Cycle Planner & Coordination**

```
1. CLAIM
   ├─ Check inbox (D2A → C2A → A2A)
   ├─ Check Contract System (--get-next-task) ← Cycle planner checked here
   └─ Check Swarm Brain

2. SYNC SSOT/CONTEXT
   ├─ Review current mission
   ├─ Sync with SSOT
   └─ Identify task dependencies

3. SLICE ← **PRIMARY TASK CREATION & DELEGATION POINT**
   ├─ Assess task size
   ├─ Break down if needed
   ├─ **IF task > 1 cycle OR multi-domain:**
   │   ├─ Create sub-tasks in cycle planner
   │   ├─ **MESSAGE OTHER AGENTS** (delegation)
   │   └─ Commit assignment messages
   └─ Plan execution approach

4. EXECUTE
   ├─ Execute task
   ├─ **IF task expands:**
   │   └─ **MESSAGE OTHER AGENTS** (coordination)
   └─ Update status.json

5. VALIDATE
   └─ Verify work quality

6. COMMIT
   └─ Commit artifacts

7. REPORT EVIDENCE
   ├─ Create devlog
   ├─ Post to Discord
   ├─ **IF swarm engaged:**
   │   └─ **MESSAGE OTHER AGENTS** (coordination outcomes)
   └─ Add next tasks to cycle planner ← **NEXT SESSION PLANNING**
```

---

## 🎯 **KEY DECISION POINTS**

### **Decision Point 1: Task Size Assessment**
**Location**: "Slice" phase (Step 3)

**Decision Tree**:
```
IF task > 1 cycle OR spans multiple domains:
    → STOP execution
    → Create sub-tasks in cycle planner
    → MESSAGE OTHER AGENTS (delegation)
    → Commit assignment messages
ELSE:
    → Continue with execution
```

### **Decision Point 2: Task Expansion During Execution**
**Location**: "Execute" phase (Step 4)

**Decision Tree**:
```
IF task scope expands:
    → Assess if expansion needs other agents
    → IF yes: MESSAGE OTHER AGENTS (coordination)
    → Update cycle planner with new sub-tasks
    → Continue execution
```

### **Decision Point 3: Coordination Type Selection**
**Location**: "Slice" phase (Step 3)

**Decision Tree**:
```
IF 2-agent task:
    → Use Bilateral Coordination Protocol
    → Send A2A message with task breakdown
ELIF 3+ agent task:
    → Use Swarm Assignment Protocol
    → Send all assignment messages simultaneously
ELSE:
    → Execute alone
```

---

## 📝 **PRACTICAL EXAMPLES**

### **Example 1: Large Task Delegation (Slice Phase)**

**Scenario**: Agent receives "64 Files Implementation" task (26 files remaining)

**Actions**:
1. **Slice Phase**: Assess task size → Too large for one agent
2. **Create sub-tasks**: Break into 6 groups by domain
3. **Add to cycle planner**: Create task entries for each agent
4. **Message agents**: Send assignment messages to 6 agents simultaneously
5. **Commit**: Commit assignment messages as progress

**Code**:
```bash
# Step 1: Create cycle planner tasks (if needed)
# Step 2: Send assignment messages
python -m src.services.messaging_cli --agent Agent-2 --message "64 Files: 5 architecture files" --priority normal
python -m src.services.messaging_cli --agent Agent-3 --message "64 Files: 5 infrastructure files" --priority normal
# ... etc
# Step 3: Commit
git add agent_workspaces/Agent-*/inbox/*.md
git commit -m "agent-1: Delegated 64 Files implementation across 6 agents"
```

### **Example 2: Task Expansion During Execution**

**Scenario**: Agent discovers task needs web interface during execution

**Actions**:
1. **Execute Phase**: Discover task expansion
2. **Assess**: Need Agent-7 (Web Development) expertise
3. **Message Agent-7**: Send coordination message
4. **Update cycle planner**: Add web interface sub-task
5. **Continue**: Coordinate via status.json and A2A pings

**Code**:
```bash
# During execution, if task expands
python -m src.services.messaging_cli --agent Agent-7 --message "Task expansion: Need web interface for feature X. Can you handle frontend?" --priority normal
```

### **Example 3: Next Session Planning (Cycle End)**

**Scenario**: Agent completes current work, identifies next priorities

**Actions**:
1. **Report Phase**: Review completed work
2. **Identify**: Next session priorities
3. **Add to cycle planner**: Create task file for next session
4. **Update status.json**: Add next_actions

**Code**:
```python
# Using session_transition_helper.py
from tools.session_transition_helper import SessionTransitionHelper

helper = SessionTransitionHelper(agent_id="Agent-1", session_date="2025-12-11")
helper.add_pending_tasks_to_cycle_planner([
    {
        "title": "Next priority task",
        "description": "Task description",
        "priority": "HIGH"
    }
])
```

---

## 🔄 **CYCLE PLANNER INTEGRATION WITH RESUME SYSTEM**

### **Resume System Integration**

When an agent is resumed from stall state:
1. **System fetches** next task from cycle planner (via `ContractManager.get_next_task()`)
2. **Task assignment** is included in resume message
3. **Agent receives** specific task to work on

**This happens automatically** - no manual task creation needed for resume prompts.

---

## ✅ **BEST PRACTICES**

### **Task Creation**:
- ✅ Create tasks in cycle planner **during slice phase** (before execution)
- ✅ Add tasks for next session **during report phase** (cycle end)
- ✅ Break down large tasks **before starting work**
- ✅ Use cycle planner for **multi-cycle tasks**

### **Agent Messaging**:
- ✅ Message agents **during slice phase** (before execution) for delegation
- ✅ Message agents **during execute phase** (if task expands)
- ✅ Send all swarm assignments **simultaneously** (parallel execution)
- ✅ Include task breakdown in coordination messages
- ✅ Commit assignment messages as progress

### **Anti-Patterns**:
- ❌ Don't create tasks **after starting execution** (should be in slice phase)
- ❌ Don't message agents **after completing work** (should be before/during)
- ❌ Don't work alone on **large tasks** (delegate in slice phase)
- ❌ Don't send assignments **sequentially** (send all at once)

---

## 📊 **SUMMARY TABLE**

| **Agent Operating Cycle Phase** | **Cycle Planner Action** | **Agent Messaging Action** |
|--------------------------------|------------------------|---------------------------|
| **1. Claim** | Check cycle planner for tasks | None |
| **2. Sync SSOT/Context** | Review task dependencies | None |
| **3. Slice** | **Create sub-tasks if needed** | **Delegate if task > 1 cycle** |
| **4. Execute** | Update task status | **Coordinate if task expands** |
| **5. Validate** | None | None |
| **6. Commit** | None | None |
| **7. Report Evidence** | **Add next session tasks** | **Report coordination outcomes** |

---

## 🎯 **KEY TAKEAWAYS**

1. **Tasks are added to cycle planner**:
   - **Slice phase**: When breaking down large tasks
   - **Report phase**: When planning next session

2. **Agents message each other**:
   - **Slice phase**: For delegation (BEFORE execution)
   - **Execute phase**: For coordination (DURING execution)
   - **Report phase**: For outcomes (AFTER execution)

3. **Delegation happens FIRST**:
   - Assess task size in slice phase
   - If task > 1 cycle OR multi-domain → STOP and delegate
   - Don't start working alone on large tasks

4. **Cycle planner integration**:
   - Resume system automatically fetches tasks from cycle planner
   - Tasks are created manually or via tools
   - Tasks are checked during "Claim" phase

---

**Status**: ✅ **WORKFLOW DOCUMENTED** - Clear guidance on when to add tasks and when to coordinate with other agents.
