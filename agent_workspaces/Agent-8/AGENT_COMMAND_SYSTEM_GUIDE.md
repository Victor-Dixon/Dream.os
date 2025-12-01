# 🎯 Agent Command System Guide - File Deletion Investigation

**Date**: 2025-12-01  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: ✅ **GUIDE CREATED**  
**Priority**: HIGH

---

## 🚀 THE GOAL

**Command agents to do everything** - Use the messaging CLI and task system to assign work to agents instead of doing it manually.

---

## 🛠️ AVAILABLE TOOLS

### **1. Messaging CLI** (`src/services/messaging_cli.py`)

**Primary tool for commanding agents**

**Commands**:
```bash
# Send message to specific agent
python -m src.services.messaging_cli --message "Your assignment" --agent Agent-2

# Assign task to agent
python -m src.services.messaging_cli --get-next-task --agent Agent-2

# Broadcast to all agents
python -m src.services.messaging_cli --message "System update" --broadcast
```

---

### **2. Task System** (`--get-next-task`)

**For structured task assignment**

**Commands**:
```bash
# Agent claims next task
python -m src.services.messaging_cli --get-next-task --agent Agent-2

# List all tasks
python -m src.services.messaging_cli --list-tasks

# Check task status
python -m src.services.messaging_cli --task-status <task-id>

# Complete task
python -m src.services.messaging_cli --complete-task <task-id> --agent Agent-2
```

---

### **3. Mission Control** (`tools/agent_mission_controller.py`)

**Autonomous mission generation**

**Commands**:
```bash
# Get mission brief for agent
python -m tools.toolbelt --mission-control --agent Agent-2

# Save mission to file
python -m tools.toolbelt --mission-control --agent Agent-2 --save
```

---

### **4. Autonomous Task Engine** (`tools/autonomous_task_engine.py`)

**Task discovery and recommendation**

**Commands**:
```bash
# Discover tasks for agent
python tools/autonomous_task_engine.py --agent Agent-2

# Get task recommendations
python tools/autonomous_task_engine.py --recommend --agent Agent-2
```

---

## 📋 HOW TO COMMAND AGENTS FOR FILE DELETION INVESTIGATION

### **Example: Assign File Deletion Investigation to Agents**

```bash
# Assign to Agent-2 (Architecture files)
python -m src.services.messaging_cli \
  --message "🔨 FILE DELETION INVESTIGATION ASSIGNMENT

📋 YOUR ASSIGNMENT: Investigate architecture-related files

Files to Review:
- architecture/design_patterns.py
- architecture/system_integration.py
- architecture/unified_architecture_core.py

Deliverable: agent_workspaces/Agent-2/ARCHITECTURE_FILES_INVESTIGATION_REPORT.md

🐝 WE. ARE. SWARM. ⚡🔥" \
  --agent Agent-2 \
  --priority urgent

# Assign to Agent-1 (Core systems)
python -m src.services.messaging_cli \
  --message "🔨 FILE DELETION INVESTIGATION ASSIGNMENT

📋 YOUR ASSIGNMENT: Investigate core/system integration files

Files to Review:
- core/agent_context_manager.py
- core/agent_documentation_service.py
- core/agent_lifecycle.py

Deliverable: agent_workspaces/Agent-1/CORE_SYSTEMS_INVESTIGATION_REPORT.md

🐝 WE. ARE. SWARM. ⚡🔥" \
  --agent Agent-1 \
  --priority urgent
```

---

## 🎯 RECOMMENDED WORKFLOW

### **Step 1: Create Tasks in Task System**

Instead of sending messages, create structured tasks:

```bash
# This would require task creation tool (may need to be built)
# For now, use messaging CLI with structured format
```

### **Step 2: Assign Tasks to Agents**

```bash
# Use messaging CLI to send structured assignments
python -m src.services.messaging_cli \
  --message "Task: File Deletion Investigation
Category: Architecture Files
Files: 3 files
Deliverable: ARCHITECTURE_FILES_INVESTIGATION_REPORT.md
Deadline: Complete investigation" \
  --agent Agent-2 \
  --priority urgent
```

### **Step 3: Agents Claim Tasks**

```bash
# Agent-2 claims task
python -m src.services.messaging_cli --get-next-task --agent Agent-2
```

### **Step 4: Monitor Progress**

```bash
# Check task status
python -m src.services.messaging_cli --list-tasks

# Check specific task
python -m src.services.messaging_cli --task-status <task-id>
```

---

## 🔧 TOOLS FOR FILE DELETION INVESTIGATION

### **Current Tools Available**:

1. ✅ **Messaging CLI** - Send assignments to agents
2. ✅ **Task System** - Structured task assignment
3. ✅ **Mission Control** - Autonomous mission generation
4. ✅ **Autonomous Task Engine** - Task discovery

### **Tools That Could Help**:

1. ⏭️ **Task Creation Tool** - Create tasks programmatically
2. ⏭️ **Bulk Assignment Tool** - Assign multiple tasks at once
3. ⏭️ **Investigation Template Generator** - Generate investigation templates
4. ⏭️ **Progress Tracker** - Track investigation progress across agents

---

## 📊 EXAMPLE: File Deletion Investigation Assignment

### **Instead of Manual Investigation**:

❌ **Manual Approach** (What I did):
- Manually investigated 49 duplicate files
- Manually verified SSOT compliance
- Created reports manually

✅ **Command-Based Approach** (What should be done):

```bash
# Assign duplicate investigation to Agent-8
python -m src.services.messaging_cli \
  --message "🔨 DUPLICATE INVESTIGATION ASSIGNMENT

📋 YOUR ASSIGNMENT: Investigate 49 duplicate files

Tasks:
1. Run content comparison on all duplicates
2. Identify true duplicates vs false positives
3. Create resolution plan

Deliverable: DUPLICATE_RESOLUTION_PLAN.md

🐝 WE. ARE. SWARM. ⚡🔥" \
  --agent Agent-8 \
  --priority urgent

# Assign SSOT verification to Agent-8
python -m src.services.messaging_cli \
  --message "🔨 SSOT VERIFICATION ASSIGNMENT

📋 YOUR ASSIGNMENT: Verify SSOT compliance

Files to Review:
- config/ssot.py
- Files with deletion markers (3 files)
- Deprecated directories (2 files)

Deliverable: SSOT_VERIFICATION_REPORT.md

🐝 WE. ARE. SWARM. ⚡🔥" \
  --agent Agent-8 \
  --priority urgent
```

---

## 🎯 KEY INSIGHT

**The goal is to command agents, not do the work yourself.**

**Tools Available**:
- ✅ Messaging CLI - Send commands
- ✅ Task System - Assign structured tasks
- ✅ Mission Control - Generate missions
- ✅ Autonomous Task Engine - Discover tasks

**Next Steps**:
1. Use messaging CLI to assign file deletion investigation to appropriate agents
2. Use task system for structured assignments
3. Use mission control for autonomous mission generation
4. Build additional tools if needed (task creation, bulk assignment)

---

## 📝 RECOMMENDATIONS

### **For File Deletion Investigation**:

1. **Create Task Creation Tool**:
   - Programmatically create tasks for file deletion investigation
   - Assign to appropriate agents based on file categories

2. **Use Messaging CLI**:
   - Send structured assignments to agents
   - Use priority flags for urgent work
   - Use tags for categorization

3. **Leverage Task System**:
   - Create tasks in task queue
   - Agents claim tasks via `--get-next-task`
   - Track progress via `--list-tasks`

4. **Use Mission Control**:
   - Generate autonomous missions for agents
   - Match work to agent specialization
   - Prevent overlap automatically

---

## 🚀 CONCLUSION

**Status**: ✅ **GUIDE CREATED**

The goal is to **command agents to do everything**, not do it manually. Use the messaging CLI, task system, and mission control tools to assign work to agents.

**Available Tools**:
- ✅ Messaging CLI (`src/services/messaging_cli.py`)
- ✅ Task System (`--get-next-task`)
- ✅ Mission Control (`tools/agent_mission_controller.py`)
- ✅ Autonomous Task Engine (`tools/autonomous_task_engine.py`)

**Next Action**: Use these tools to command agents for file deletion investigation work.

---

🐝 WE. ARE. SWARM. ⚡🔥

**Agent-8 - SSOT & System Integration Specialist**  
*Commanding Agents Through Tools*

