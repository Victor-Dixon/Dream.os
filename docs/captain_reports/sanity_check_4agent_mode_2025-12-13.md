# Sanity Check - 4-Agent Mode Configuration

**Date**: 2025-12-13  
**Captain**: Agent-4  
**Status**: ⚠️ ISSUES FOUND

---

## ✅ VERIFIED CORRECTLY

### **1. Agent Mode Configuration**
- ✅ `agent_mode_config.json` set to "4-agent" mode
- ✅ Active agents: Agent-1, Agent-2, Agent-3, Agent-4
- ✅ Inactive agents: Agent-5, Agent-6, Agent-7, Agent-8

### **2. Core Systems (Mode-Aware)**
- ✅ `orchestrator._get_active_agents()` - Uses mode manager ✅
- ✅ `recovery_messaging._broadcast_to_all_agents()` - Uses mode manager ✅
- ✅ `tools/send_resume_directives_all_agents.py` - Uses mode manager ✅
- ✅ `tools/force_multiplier_monitor.py` - Uses mode manager ✅
- ✅ Start agents commands - Mode-aware ✅

---

## ⚠️ ISSUES FOUND (Need Updates)

### **1. Hardcoded Agent Lists (8 agents)**

#### **`src/orchestrators/overnight/monitor_state.py:44`**
```python
for i in range(1, 9):  # ❌ Hardcoded to 8 agents
```
**Impact**: Monitor state initialization includes all 8 agents
**Fix**: Use `get_active_agents()` from mode manager

#### **`src/orchestrators/overnight/recovery.py:82`**
```python
self.recovery_attempts = {f"Agent-{i}": 0 for i in range(1, 9)}  # ❌ Hardcoded
```
**Impact**: Tracks recovery attempts for all 8 agents
**Fix**: Initialize only for active agents

#### **`src/orchestrators/overnight/recovery_state.py:34`**
```python
self.recovery_attempts = {f"Agent-{i}": 0 for i in range(1, 9)}  # ❌ Hardcoded
```
**Impact**: Tracks recovery attempts for all 8 agents
**Fix**: Initialize only for active agents

#### **`src/orchestrators/overnight/scheduler.py:105`**
```python
self.agent_load = {f"Agent-{i}": 0 for i in range(1, 9)}  # ❌ Hardcoded
```
**Impact**: Tracks load for all 8 agents
**Fix**: Initialize only for active agents

#### **`src/orchestrators/overnight/scheduler_refactored.py:105`**
```python
self.agent_load = {f"Agent-{i}": 0 for i in range(1, 9)}  # ❌ Hardcoded
```
**Impact**: Tracks load for all 8 agents
**Fix**: Initialize only for active agents

#### **`src/orchestrators/overnight/fsm_bridge.py:59`**
```python
valid_agent_ids = {f"Agent-{i}" for i in range(1, 9)}  # ❌ Hardcoded
```
**Impact**: Validates all 8 agents
**Fix**: Use mode-aware validation

#### **`src/services/handlers/command_handler.py:17`**
```python
return [f'Agent-{i}' for i in range(1, 9)]  # ❌ Hardcoded
```
**Impact**: Command handler returns all 8 agents
**Fix**: Use mode-aware agent list

#### **`src/services/chat_presence/status_reader.py:76`**
```python
for i in range(1, 9):  # ❌ Hardcoded
```
**Impact**: Reads status for all 8 agents
**Fix**: Only read active agents

#### **`src/services/messaging_cli_handlers.py:124`**
```python
f"📢 Broadcast successful to {success}/8 agents"  # ❌ Hardcoded count
```
**Impact**: Message shows "/8 agents" instead of actual count
**Fix**: Use dynamic count

---

### **2. Syntax Error**

#### **`src/core/config/__init__.py`**
- ❌ Contains HTML comment syntax: `<!-- SSOT Domain: core -->`
- **Impact**: Prevents imports from core module
- **Fix**: Remove or convert to Python comment

---

### **3. Agent-5 Specific Code (Minor - May Be Intentional)**

Several files have hardcoded references to Agent-5:
- `orchestrator.py:227` - Seeds FSM tasks for Agent-5
- `fsm_bridge.py:359` - Sends to Agent-5 inbox
- `listener.py:427` - Default agent is Agent-5
- Various FSM-related files default to Agent-5

**Note**: These may be intentional for FSM/contract system, but should be mode-aware if Agent-5 is inactive.

---

## 📊 IMPACT ASSESSMENT

### **High Impact** (Blocks Mode-Aware Operation)
- ❌ `monitor_state.py` - Initializes tracking for all 8 agents
- ❌ `recovery.py` - Tracks recovery for all 8 agents
- ❌ `recovery_state.py` - Tracks recovery for all 8 agents
- ❌ `scheduler.py` - Tracks load for all 8 agents
- ❌ `scheduler_refactored.py` - Tracks load for all 8 agents
- ❌ **Syntax error in `config/__init__.py`** - Blocks imports

### **Medium Impact** (Functional but Not Optimal)
- ⚠️ `fsm_bridge.py` - Validates all 8 agents
- ⚠️ `command_handler.py` - Returns all 8 agents
- ⚠️ `status_reader.py` - Reads all 8 agents
- ⚠️ `messaging_cli_handlers.py` - Shows hardcoded "/8" count

### **Low Impact** (May Be Intentional)
- ℹ️ Agent-5 specific code in FSM system

---

## 🔧 RECOMMENDED FIXES

### **Priority 1: Fix Syntax Error**
```python
# src/core/config/__init__.py
# Remove: <!-- SSOT Domain: core -->
# Replace with: # SSOT Domain: core
```

### **Priority 2: Update Monitoring/Recovery Systems**
Update all files with `range(1, 9)` to use `get_active_agents()`

### **Priority 3: Update Scheduler Systems**
Update agent_load initialization to use active agents only

### **Priority 4: Update Utilities**
Update status readers, command handlers, and FSM bridge

---

## ✅ WORKING CORRECTLY

Despite the issues above, the **core messaging and orchestration** systems are mode-aware:
- ✅ Message delivery (PyAutoGUI/queue)
- ✅ Resume directives
- ✅ Start commands
- ✅ Force multiplier monitor
- ✅ Recovery broadcasts
- ✅ Orchestrator agent list

**The system will NOT send messages to Agents 5-8**, but may track/initialize data structures for them.

---

## 🎯 NEXT STEPS

1. Fix syntax error in `config/__init__.py` (CRITICAL)
2. Update monitor_state.py to use active agents only
3. Update recovery systems to use active agents only
4. Update scheduler systems to use active agents only
5. Update utility handlers to be mode-aware

---

*Report generated by Agent-4 (Captain)*


