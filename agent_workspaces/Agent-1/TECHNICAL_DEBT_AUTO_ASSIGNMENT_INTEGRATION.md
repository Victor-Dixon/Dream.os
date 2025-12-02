# 🔄 Technical Debt Auto-Assignment Integration

**Date**: 2025-12-02  
**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Status**: ✅ **INTEGRATION CREATED**  
**Priority**: HIGH

---

## 🎯 **CONCEPT**

**Tie technical debt reports → Messaging system → Agent resume system**

This creates a **continuous loop** where agents are **ALWAYS working on real tasks**:

1. **Weekly Report Generated** → Agent-5 generates technical debt report
2. **Tasks Extracted** → Auto-assigner extracts actionable tasks
3. **Tasks Assigned** → Messaging CLI sends tasks to agents
4. **Status Tracked** → Agent status.json updated with new tasks
5. **Work Continuous** → Agents always have real work assigned

---

## 🔧 **INTEGRATION COMPONENTS**

### **1. Auto-Task Assigner** (`systems/technical_debt/auto_task_assigner.py`)

**Purpose**: Automatically assigns tasks from weekly reports to agents

**Features**:
- ✅ Reads weekly technical debt reports
- ✅ Extracts actionable tasks (non-blocked, pending items)
- ✅ Matches tasks to agents based on specializations
- ✅ Checks agent availability (not blocked, has capacity)
- ✅ Sends tasks via messaging CLI
- ✅ Updates agent status.json files
- ✅ Supports continuous loop mode

**Usage**:
```bash
# One-time assignment
python systems/technical_debt/auto_task_assigner.py

# Dry run (test without assigning)
python systems/technical_debt/auto_task_assigner.py --dry-run

# Continuous loop (check every hour)
python systems/technical_debt/auto_task_assigner.py --continuous --interval 60
```

---

## 🔄 **WORKFLOW**

### **Step 1: Report Generation** (Agent-5)
- Weekly report generated every Monday
- Saved to: `systems/technical_debt/reports/weekly_report_YYYY-MM-DD.json`

### **Step 2: Task Extraction** (Auto-Assigner)
- Reads latest weekly report
- Extracts actionable tasks:
  - Pending items > 0
  - Status not "BLOCKED"
  - Categorized by priority

### **Step 3: Agent Matching** (Auto-Assigner)
- Matches tasks to agents based on:
  - Category keywords
  - Agent specializations
  - Current workload (max 3 tasks per agent)

### **Step 4: Task Assignment** (Messaging CLI)
- Sends task via: `python -m src.services.messaging_cli --agent Agent-X --message "..." --priority urgent`
- Task includes:
  - Category name
  - Pending count
  - Status
  - Action instructions

### **Step 5: Status Update** (Auto-Assigner)
- Updates agent `status.json`:
  - Adds task to `current_tasks`
  - Updates `last_updated`
  - Updates `current_mission` if needed

### **Step 6: Continuous Loop** (Optional)
- Runs every N minutes (default: 60)
- Checks for new tasks
- Assigns to available agents
- Keeps agents working continuously

---

## 📊 **AGENT SPECIALIZATIONS**

**Task Matching Logic**:
- **Agent-1**: Integration, Core Systems, Coordination, Messaging
- **Agent-2**: Architecture, Design, Duplicate Review, Patterns
- **Agent-3**: Infrastructure, DevOps, Test Validation, Deployment
- **Agent-7**: Web Development, Integration Wiring, Discord, API
- **Agent-8**: SSOT, System Integration, Metrics, Unified Systems

**Default**: Agent-1 (if no match found)

---

## 🎯 **BENEFITS**

1. **Continuous Work**: Agents always have real tasks assigned
2. **Automatic Assignment**: No manual task distribution needed
3. **Smart Matching**: Tasks matched to agent specializations
4. **Status Tracking**: All tasks tracked in status.json
5. **Capacity Management**: Limits tasks per agent (max 3)
6. **Blocked Detection**: Skips blocked agents automatically

---

## 🚀 **USAGE EXAMPLES**

### **One-Time Assignment** (After Weekly Report)
```bash
# Assign tasks from latest report
python systems/technical_debt/auto_task_assigner.py
```

### **Continuous Mode** (Always-On)
```bash
# Run continuous loop (check every hour)
python systems/technical_debt/auto_task_assigner.py --continuous --interval 60

# Run in background
nohup python systems/technical_debt/auto_task_assigner.py --continuous --interval 60 > auto_assigner.log 2>&1 &
```

### **Dry Run** (Test Before Assigning)
```bash
# Test assignment without actually sending
python systems/technical_debt/auto_task_assigner.py --dry-run
```

---

## 📋 **INTEGRATION WITH EXISTING SYSTEMS**

### **Messaging System** ✅
- Uses: `src/services/messaging_cli.py`
- Sends tasks via unified messaging
- Supports priority levels (urgent, normal)

### **Agent Resume System** ✅
- Updates: `agent_workspaces/Agent-X/status.json`
- Tracks: `current_tasks`, `current_mission`, `last_updated`
- Maintains: Agent availability status

### **Technical Debt Tracking** ✅
- Reads: `systems/technical_debt/reports/weekly_report_*.json`
- Uses: `TechnicalDebtTracker` data structure
- Integrates: With Agent-5's monitoring system

---

## 🔄 **CONTINUOUS LOOP CONFIGURATION**

**Recommended Settings**:
- **Interval**: 60 minutes (check hourly)
- **Max Tasks Per Agent**: 3 (prevents overload)
- **Priority Filtering**: Assigns urgent tasks first

**Monitoring**:
- Logs assignment results
- Tracks skipped tasks (unavailable agents)
- Reports errors for debugging

---

## ✅ **NEXT STEPS**

1. **Test Integration**:
   ```bash
   python systems/technical_debt/auto_task_assigner.py --dry-run
   ```

2. **Run First Assignment**:
   ```bash
   python systems/technical_debt/auto_task_assigner.py
   ```

3. **Enable Continuous Mode** (Optional):
   ```bash
   python systems/technical_debt/auto_task_assigner.py --continuous --interval 60
   ```

4. **Monitor Results**:
   - Check agent status.json files
   - Verify tasks in messaging system
   - Review assignment logs

---

**Status**: ✅ **INTEGRATION COMPLETE**  
**Ready for**: Testing and deployment  
**Impact**: Agents will always have real tasks assigned automatically

🐝 **WE. ARE. SWARM. ⚡🔥**

