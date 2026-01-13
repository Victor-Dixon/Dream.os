# 🔧 SYSTEM UTILIZATION PROTOCOL - MANDATORY AGENT WORKFLOW

**Version**: 1.0  
**Last Updated**: 2025-12-03  
**Author**: Agent-4 (Captain)  
**Status**: 🚨 **MANDATORY FOR ALL AGENTS**

---

## 🎯 **PURPOSE**

Agents are underutilizing critical systems. This protocol makes system utilization **MANDATORY** at key workflow points.

**Underutilized Systems:**
1. ❌ **Project Scanner** - Not run regularly to find opportunities
2. ❌ **State of Project** - Not checking project_analysis.json
3. ❌ **Swarm Brain** - Not searching before starting work
4. ❌ **FSM System** - Not updating fsm_state in status.json
5. ❌ **Contract System** - Not using --get-next-task to claim work

**This protocol fixes that.**

---

## 🔄 **MANDATORY WORKFLOW CHECKPOINTS**

### **CHECKPOINT 1: START OF CYCLE (Every Agent Response)**

**Before doing ANY work, agents MUST:**

1. ✅ **Check Contract System**
   ```bash
   python -m src.services.messaging_cli --get-next-task --agent Agent-X
   ```
   - Claim assigned work FIRST
   - If no contract, proceed to Project Scanner

2. ✅ **Check Swarm Brain**
   ```python
   from src.swarm_brain.swarm_memory import SwarmMemory
   memory = SwarmMemory(agent_id='Agent-X')
   results = memory.search_swarm_knowledge("your task topic")
   ```
   - Search for similar work/patterns
   - Learn from previous solutions
   - Check relevant protocols

3. ✅ **Update FSM State**
   ```python
   # In status.json:
   "fsm_state": "active"  # or "process", "blocked", etc.
   ```
   - Update fsm_state to reflect current state
   - Use AgentLifecycle for automatic updates

4. ✅ **Check Project State** (if starting new work)
   ```bash
   # Review latest project analysis
   cat project_analysis.json | python -m json.tool | grep -A 5 "violations"
   ```
   - Find high-value opportunities
   - Check V2 compliance issues
   - Identify consolidation targets

---

### **CHECKPOINT 2: BEFORE STARTING NEW TASK**

**Before claiming/starting ANY new task:**

1. ✅ **Run Project Scanner** (if analysis is stale >24 hours)
   ```bash
   python tools/run_project_scan.py
   ```
   - Generates project_analysis.json
   - Identifies V2 violations
   - Finds consolidation opportunities

2. ✅ **Check Swarm Brain for Patterns**
   ```python
   memory.search_swarm_knowledge("task type")
   memory.search_swarm_knowledge("similar problem")
   ```
   - Find existing solutions
   - Check for relevant patterns
   - Learn from previous work

3. ✅ **Check Contract System**
   ```bash
   python -m src.services.messaging_cli --get-next-task --agent Agent-X
   ```
   - Claim assigned work before seeking new opportunities

4. ✅ **Update FSM State**
   ```json
   "fsm_state": "active"
   "status": "ACTIVE"
   ```

---

### **CHECKPOINT 3: DURING WORK (State Transitions)**

**When state changes, agents MUST:**

1. ✅ **Update FSM State Immediately**
   ```python
   # ACTIVE → PROCESS (deep work)
   "fsm_state": "process"
   
   # ACTIVE → BLOCKED (waiting)
   "fsm_state": "blocked"
   "blockers": ["reason"]
   
   # BLOCKED → ACTIVE (resolved)
   "fsm_state": "active"
   "blockers": []
   ```

2. ✅ **Update Status.json**
   ```json
   "last_updated": "2025-12-03T12:00:00Z"
   "current_phase": "TASK_NAME"
   "current_tasks": ["Task 1"]
   ```

---

### **CHECKPOINT 4: AFTER COMPLETING TASK**

**After finishing work:**

1. ✅ **Share to Swarm Brain**
   ```python
   memory.share_learning(
       title="What You Learned",
       content="Key insights, patterns, solutions",
       tags=["relevant", "tags"]
   )
   ```

2. ✅ **Update FSM State**
   ```json
   "fsm_state": "complete"
   "status": "COMPLETE"
   ```

3. ✅ **Update Status.json**
   ```json
   "completed_tasks": ["Task 1"]
   "points_earned": 500
   "next_actions": ["Next task"]
   ```

---

## 📋 **QUICK REFERENCE CHECKLIST**

### **Every Cycle Start:**
- [ ] Check Contract System (`--get-next-task`)
- [ ] Check Swarm Brain (search relevant topics)
- [ ] Update FSM State in status.json
- [ ] Update last_updated timestamp

### **Before New Task:**
- [ ] Run Project Scanner (if stale)
- [ ] Check Swarm Brain for patterns
- [ ] Check Contract System
- [ ] Review project_analysis.json for opportunities

### **During Work:**
- [ ] Update FSM State on transitions
- [ ] Update status.json with progress
- [ ] Document blockers if blocked

### **After Task:**
- [ ] Share learning to Swarm Brain
- [ ] Update FSM State to "complete"
- [ ] Update status.json with results
- [ ] Post devlog to Discord

---

## 🚨 **ENFORCEMENT**

**This protocol is MANDATORY. Violations result in:**
- Captain intervention
- Stall recovery prompts
- Reduced autonomy

**Captain monitors:**
- FSM state updates (must be current)
- Contract system usage (must check before seeking work)
- Swarm Brain contributions (must share learnings)
- Project Scanner usage (must run when stale)

---

## 📚 **SYSTEM DOCUMENTATION**

### **Project Scanner:**
- **Guide**: `swarm_brain/procedures/PROCEDURE_PROJECT_SCANNING.md`
- **Tool**: `tools/run_project_scan.py`
- **Output**: `project_analysis.json`

### **Swarm Brain:**
- **Guide**: `swarm_brain/protocols/SWARM_BRAIN_ACCESS_GUIDE.md`
- **API**: `src/swarm_brain/swarm_memory.py`
- **Location**: `swarm_brain/`

### **FSM System:**
- **Guide**: `swarm_brain/protocols/AGENT_LIFECYCLE_FSM.md`
- **API**: `src/core/agent_lifecycle.py`
- **Field**: `status.json["fsm_state"]`

### **Contract System:**
- **Command**: `python -m src.services.messaging_cli --get-next-task --agent Agent-X`
- **Manager**: `src/services/contract_system/manager.py`
- **Storage**: `agent_workspaces/contracts/`

---

## 🎯 **SUCCESS METRICS**

**Agents are successfully utilizing systems when:**
- ✅ FSM state is always current in status.json
- ✅ Contract system checked before seeking work
- ✅ Swarm Brain searched before starting tasks
- ✅ Project Scanner run when analysis is stale
- ✅ Learnings shared to Swarm Brain after completion

---

**🐝 WE. ARE. SWARM. ⚡🔥**

**USE THE SYSTEMS - THEY MAKE YOU SMARTER AND MORE EFFICIENT!**

