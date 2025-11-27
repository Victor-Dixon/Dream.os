# 🔍 Agent Status Monitor - How It Works Now

**Updated:** 2025-01-27  
**Status:** ✅ Continuous Operation Enabled

---

## 🎯 WHAT IT DOES

The agent status monitor watches all 8 agents 24/7 to ensure they're working and not stuck. Since "the system never stops," we need continuous monitoring.

**Think of it like:** A security guard watching 8 workers, making sure they're all doing their jobs and not frozen.

---

## ⚙️ HOW IT TRACKS AGENTS

### **Activity Tracking:**

The system tracks **when agents last did something**:

1. **Task Assignment** → Updates activity timestamp (primary method)
2. **Task Completion** → Clears current task
3. **Initialization** → Sets initial timestamp when monitoring starts

**Key Point:** Activity is updated when the orchestrator assigns tasks to agents. The agent doesn't need to do anything special - just receiving a task counts as activity.

---

## 🚨 STALL DETECTION

### **How It Works:**

Every **60 seconds** (default), the monitor checks:

```python
time_since_activity = current_time - last_activity

if time_since_activity > 300 seconds (5 minutes):
    status = "stalled"  # Agent is stuck!
elif agent has current_task:
    status = "busy"     # Agent is working
else:
    status = "idle"     # Agent has no task
```

### **What Happens When Stalled:**

1. Monitor detects stall
2. Logs warning: "Detected stalled agents: [Agent-X]"
3. Health status marked as unhealthy
4. Recovery system can trigger rescue message

---

## 📊 CURRENT CONFIGURATION

**From `config/orchestration.yml`:**

```yaml
overnight:
  enabled: true
  max_cycles: 0              # 0 = infinite (never stops)
  auto_restart: true
  
  monitoring:
    check_interval: 60      # Check every 60 seconds
    stall_timeout: 300       # 5 minutes = stalled
    health_checks: true
    performance_tracking: true
```

**Key Settings:**
- **`check_interval: 60`** → Monitor checks agents every minute
- **`stall_timeout: 300`** → Agent marked as stalled after 5 minutes of no activity
- **`max_cycles: 0`** → System runs continuously (never stops)

---

## 🔍 HOW TO CHECK STATUS

### **Quick Check (All Agents):**
```bash
python tools/agent_status_quick_check.py --all
```

### **Check Specific Agent:**
```bash
python tools/agent_status_quick_check.py --agent Agent-3
```

### **Using V2 Toolbelt:**
```bash
python -m tools_v2.toolbelt captain.status_check
```

### **Using Activity Tracker Tool:**
```python
from tools_v2.toolbelt_core import ToolbeltCore
toolbelt = ToolbeltCore()
result = toolbelt.run("agent_activity.track", {"check_all": True})
```

---

## 📈 STATUS INFORMATION

**For Each Agent:**
- **Status**: `busy` | `idle` | `stalled`
- **Last Activity**: Unix timestamp
- **Time Since Activity**: Seconds since last activity
- **Current Task**: Task ID or `null`

**System Health:**
- **Healthy**: `true` | `false`
- **Stalled Agents**: List of stalled agent IDs
- **Issues**: List of detected problems

---

## 🛠️ RECONFIGURATION

**To Change Check Frequency:**
```yaml
monitoring:
  check_interval: 30  # Check every 30 seconds (faster)
```

**To Change Stall Timeout:**
```yaml
monitoring:
  stall_timeout: 600  # 10 minutes before marking stalled
```

**To Enable Continuous Operation:**
```yaml
overnight:
  enabled: true
  max_cycles: 0       # 0 = infinite cycles
  auto_restart: true
```

---

## ⚠️ IMPORTANT NOTES

1. **Activity Updates**: Activity is primarily updated when tasks are assigned, not when agents update status.json files
2. **Stall Detection**: Based on time since last activity, not file modifications
3. **Continuous Operation**: With `max_cycles: 0`, the system runs indefinitely
4. **Recovery**: Stalled agents can receive rescue messages automatically

---

## 🔗 RELATED FILES

- **Main Monitor**: `src/orchestrators/overnight/monitor.py`
- **State Management**: `src/orchestrators/overnight/monitor_state.py`
- **Orchestrator**: `src/orchestrators/overnight/orchestrator.py`
- **Configuration**: `config/orchestration.yml`
- **Quick Check Tool**: `tools/agent_status_quick_check.py`

---

**WE. ARE. SWARM. MONITORED. POWERFUL.** 🐝⚡🔥

*Updated: 2025-01-27 - Continuous Operation Enabled*




