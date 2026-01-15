=======
<!-- SSOT Domain: documentation -->

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
# Task Management System Integration

**Version:** 1.0  
**Last Updated:** 2025-12-22  
**Author:** Agent-4 (Captain)  
**Status:** ACTIVE DOCUMENTATION

---

## 🎯 Purpose

This document provides an overview of how all task management components integrate together: MASTER_TASK_LOG, Task Discovery Protocol, Captain-Level Task Protocol, Cycle Planner, and Contract System.

---

## 🔗 System Components

### 1. MASTER_TASK_LOG.md
**Location:** `MASTER_TASK_LOG.md` (repository root)  
**Purpose:** Central task tracking document  
**Links To:**
- [TASK_DISCOVERY_PROTOCOL.md](TASK_DISCOVERY_PROTOCOL.md) - When no tasks available
- [CAPTAIN_LEVEL_TASK_PROTOCOL.md](CAPTAIN_LEVEL_TASK_PROTOCOL.md) - For Captain-Level Tasks
- Cycle Planner Integration - `src/core/resume_cycle_planner_integration.py`
- Contract System - `src/services/contract_system/`

### 2. TASK_DISCOVERY_PROTOCOL.md
**Location:** `docs/TASK_DISCOVERY_PROTOCOL.md`  
**Purpose:** Systematic approach to finding work when MASTER_TASK_LOG is empty  
**Links To:**
- [MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md) - Where discovered tasks are added
- [CAPTAIN_LEVEL_TASK_PROTOCOL.md](CAPTAIN_LEVEL_TASK_PROTOCOL.md) - For Captain-Level classification
- Cycle Planner - `src/core/resume_cycle_planner_integration.py`
- Contract System - `src/services/contract_system/`
- Cycle Accomplishment Reports - `devlogs/YYYY-MM-DD_agent-X_cycle_accomplishments.md`

### 3. CAPTAIN_LEVEL_TASK_PROTOCOL.md
**Location:** `docs/CAPTAIN_LEVEL_TASK_PROTOCOL.md`  
**Purpose:** Protocol for creating and identifying Captain-Level Tasks  
**Links To:**
- [MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md) - Where Captain-Level Tasks are documented
- [TASK_DISCOVERY_PROTOCOL.md](TASK_DISCOVERY_PROTOCOL.md) - Discovery method
- Cycle Planner - `src/core/resume_cycle_planner_integration.py`
- Contract System - `src/services/contract_system/`

### 4. Cycle Planner Integration
**Location:** `src/core/resume_cycle_planner_integration.py`  
**Purpose:** Automatic task assignment when agents resume work  
**Integration:**
- Tasks from MASTER_TASK_LOG can be added to cycle planner
- Agents automatically claim tasks when resuming work
- Integrated with resume prompt system

### 5. Contract System
**Location:** `src/services/contract_system/`  
**Purpose:** Task claiming and assignment system  
**Usage:** `python -m src.services.messaging_cli --get-next-task --agent Agent-X`  
**Integration:**
- Claims tasks from cycle planner
- Updates MASTER_TASK_LOG with claimed status
- Tracks task assignments
- Tracks points: `total_points`, `completed_points`

### 6. Point System
**Location:** `src/core/gamification/`, `src/core/agent_lifecycle.py`  
**Purpose:** Gamification and achievement tracking  
**Integration:**
- Tracks `points_earned` in agent status.json
- Awards points on task completion
- Leaderboard rankings
- See [POINT_SYSTEM_INTEGRATION.md](POINT_SYSTEM_INTEGRATION.md) for full integration guide

---

## 🔄 Complete Task Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    TASK LIFECYCLE FLOW                       │
└─────────────────────────────────────────────────────────────┘

1. DISCOVERY PHASE
   ├─ Check MASTER_TASK_LOG.md
   │  └─ If empty → Follow TASK_DISCOVERY_PROTOCOL.md
   │     ├─ Step 1: Review Project Reports
   │     ├─ Step 2: Generate Project Scan
   │     ├─ Step 3: Consult with Thea
   │     ├─ Step 4: Review Agent Status Files
   │     ├─ Step 5: Review Recent Commits
   │     ├─ Step 6: Check Test Coverage
   │     ├─ Step 7: Review Cycle Accomplishments
   │     ├─ Step 8: Check Documentation Gaps
   │     ├─ Step 9: Check System Health
   │     └─ Step 10: Review Error Logs
   │
   └─ Task Found → Continue to Classification

2. CLASSIFICATION PHASE
   ├─ Is this Captain-Level?
   │  ├─ YES → Follow CAPTAIN_LEVEL_TASK_PROTOCOL.md
   │  │  ├─ Complete Pre-Creation Checklist
   │  │  ├─ Verify ALL 4 criteria met
   │  │  └─ Document justification
   │  │
   │  └─ NO → Assign to appropriate specialized agent
   │
   └─ Continue to Documentation

3. DOCUMENTATION PHASE
   └─ Add to MASTER_TASK_LOG.md
      ├─ Format: Priority, Description, Source, Justification
      ├─ Section: INBOX, THIS_WEEK, or Captain-Level
      └─ Tag: [Agent-X] or [Agent-4 CAPTAIN]

4. ASSIGNMENT PHASE
   ├─ Option A: Cycle Planner (Automatic)
   │  └─ Add to cycle planner → Auto-assigned when agent resumes
   │
   └─ Option B: Contract System (Manual)
      └─ Agent claims via: --get-next-task --agent Agent-X

5. EXECUTION PHASE
   └─ Agent updates status.json
      ├─ Mark task as IN_PROGRESS
      ├─ Update progress
      └─ Document blockers if any

6. COMPLETION PHASE
   └─ Mark complete in MASTER_TASK_LOG.md
      ├─ Update task status: ✅ COMPLETE
      ├─ Document deliverables
      └─ Update agent status.json
```

---

## 📊 Integration Matrix

| Component | MASTER_TASK_LOG | TASK_DISCOVERY | CAPTAIN_LEVEL | Cycle Planner | Contract System |
|-----------|----------------|----------------|---------------|---------------|-----------------|
| **MASTER_TASK_LOG** | ✅ Self | ✅ Links | ✅ Links | ✅ References | ✅ References |
| **TASK_DISCOVERY** | ✅ Links | ✅ Self | ✅ Links | ✅ References | ✅ References |
| **CAPTAIN_LEVEL** | ✅ Links | ✅ Links | ✅ Self | ✅ References | ✅ References |
| **Cycle Planner** | ✅ Reads from | ✅ Can add to | ✅ Can add to | ✅ Self | ✅ Integrates |
| **Contract System** | ✅ Updates | ✅ Can claim | ✅ Can claim | ✅ Reads from | ✅ Self |

---

## 🎯 Usage Scenarios

### Scenario 1: No Tasks Available
1. Agent checks MASTER_TASK_LOG.md → Empty
2. Follows TASK_DISCOVERY_PROTOCOL.md
3. Discovers task via 10-step checklist
4. Checks if Captain-Level → Follows CAPTAIN_LEVEL_TASK_PROTOCOL.md if yes
5. Adds task to MASTER_TASK_LOG.md
6. Optionally adds to Cycle Planner
7. Agent claims via Contract System

### Scenario 2: Creating Captain-Level Task
1. Agent identifies potential Captain-Level Task
2. Follows CAPTAIN_LEVEL_TASK_PROTOCOL.md
3. Completes Pre-Creation Checklist
4. Verifies ALL 4 criteria met
5. Documents justification
6. Adds to MASTER_TASK_LOG.md in "Captain-Level Strategic Oversight Tasks" section
7. Tags with [Agent-4 CAPTAIN]

### Scenario 3: Task Assignment
1. Task exists in MASTER_TASK_LOG.md
2. Option A: Added to Cycle Planner → Auto-assigned on agent resume
3. Option B: Agent claims via Contract System: `--get-next-task --agent Agent-X`
4. Task marked as CLAIMED in MASTER_TASK_LOG.md
5. Agent updates status.json

---

## 🔍 Quick Reference Links

### Finding Tasks
- **No tasks?** → [TASK_DISCOVERY_PROTOCOL.md](TASK_DISCOVERY_PROTOCOL.md)
- **All tasks claimed?** → [TASK_DISCOVERY_PROTOCOL.md](TASK_DISCOVERY_PROTOCOL.md)
- **Need work?** → [TASK_DISCOVERY_PROTOCOL.md](TASK_DISCOVERY_PROTOCOL.md)

### Point System
- **How points work?** → [POINT_SYSTEM_INTEGRATION.md](POINT_SYSTEM_INTEGRATION.md)
- **Point values?** → HIGH: 100-200, MEDIUM: 50-100, LOW: 25-50
- **Captain-Level multiplier?** → 1.5x (see [POINT_SYSTEM_INTEGRATION.md](POINT_SYSTEM_INTEGRATION.md))

### Creating Tasks
- **Regular task?** → Add to [MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md) INBOX
- **Captain-Level?** → Follow [CAPTAIN_LEVEL_TASK_PROTOCOL.md](CAPTAIN_LEVEL_TASK_PROTOCOL.md) first
- **From discovery?** → Document source in task description

### Assigning Tasks
- **Automatic?** → Add to Cycle Planner (`src/core/resume_cycle_planner_integration.py`)
- **Manual claim?** → Use Contract System: `--get-next-task --agent Agent-X`
- **Captain-Level?** → Always [Agent-4 CAPTAIN]

---

## ✅ Verification Checklist

When creating/updating tasks, verify:

- [ ] Task is in [MASTER_TASK_LOG.md](../MASTER_TASK_LOG.md)
- [ ] If Captain-Level, follows [CAPTAIN_LEVEL_TASK_PROTOCOL.md](CAPTAIN_LEVEL_TASK_PROTOCOL.md)
- [ ] If discovered, source documented (per [TASK_DISCOVERY_PROTOCOL.md](TASK_DISCOVERY_PROTOCOL.md))
- [ ] Proper agent assignment tag
- [ ] Links to related protocols included
- [ ] Cycle Planner integration considered (if applicable)

---

## 📌 Key Principles

1. **MASTER_TASK_LOG.md is SSOT** - All tasks must be documented here
2. **Protocols are mandatory** - Follow TASK_DISCOVERY and CAPTAIN_LEVEL protocols
3. **Bidirectional links** - All components link to each other
4. **Cycle Planner integration** - Optional but recommended for automatic assignment
5. **Contract System** - Alternative manual claiming method

---

**Document Status:** ✅ ACTIVE  
**Next Review:** 2025-03-22  
**Maintained By:** Agent-4 (Captain)

🐝 WE. ARE. SWARM. ⚡🔥

