# 🔧 Reconfigure Agent Status Monitor for Continuous Operation

**From**: Agent-4 (Captain)  
**To**: Victor  
**Date**: 2025-01-27  
**Purpose**: Step-by-step guide to reconfigure monitoring for never-stopping operation

---

## 🎯 THE GOAL

**Make the monitoring system run forever without stopping.**

Currently, the system has:
- `max_cycles: 60` (stops after 60 cycles = 10 hours)
- We need it to run **infinitely**

---

## 📝 STEP-BY-STEP RECONFIGURATION

### **Step 1: Open the Configuration File**

The configuration file is located at:
```
config/orchestration.yml
```

### **Step 2: Find the Overnight Section**

Look for this section (around line 32-38):

```yaml
# Overnight autonomous execution
overnight:
  enabled: true
  cycle_interval: 10  # minutes per cycle (V2 cycle-based)
  max_cycles: 60  # 10 hours total
  auto_restart: true
```

### **Step 3: Change `max_cycles` to 0**

**Change this:**
```yaml
max_cycles: 60  # 10 hours total
```

**To this:**
```yaml
max_cycles: 0  # 0 = infinite cycles (never stops)
```

### **Step 4: Verify Monitoring Settings**

Make sure the monitoring section looks like this (around line 53-58):

```yaml
# Monitoring
monitoring:
  check_interval: 60  # seconds (checks every minute)
  stall_timeout: 300  # seconds (5 minutes = stalled)
  health_checks: true
  performance_tracking: true
```

**These settings are good for continuous operation:**
- `check_interval: 60` - Checks every minute (good balance)
- `stall_timeout: 300` - 5 minutes before marking stalled (reasonable)
- `health_checks: true` - Keep enabled
- `performance_tracking: true` - Keep enabled

### **Step 5: Verify Auto-Restart is Enabled**

Make sure this is set:
```yaml
auto_restart: true  # Restarts if crashes
```

### **Step 6: Save the File**

Save `config/orchestration.yml` after making changes.

---

## ✅ FINAL CONFIGURATION (What It Should Look Like)

```yaml
# Overnight autonomous execution
overnight:
  enabled: true                    # ✅ MUST be true
  cycle_interval: 10               # minutes per cycle
  max_cycles: 0                    # ✅ 0 = infinite (never stops)
  auto_restart: true               # ✅ Restart if crashes
  
  # Monitoring
  monitoring:
    check_interval: 60             # Check every 60 seconds
    stall_timeout: 300             # 5 minutes = stalled
    health_checks: true             # Enable health checks
    performance_tracking: true     # Track performance
```

---

## 🔍 VERIFICATION (How to Check It's Working)

### **Method 1: Check Configuration is Loaded**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor
from src.core.unified_config import get_unified_config

config = get_unified_config()
monitor = ProgressMonitor(config.get('overnight', {}))

info = monitor.get_monitor_info()
print(f"Monitoring active: {info['monitoring_active']}")
print(f"Check interval: {info['check_interval']} seconds")
print(f"Stall timeout: {info['stall_timeout']} seconds")
```

### **Method 2: Check Orchestrator Settings**

```python
from src.orchestrators.overnight.orchestrator import OvernightOrchestrator

orchestrator = OvernightOrchestrator()
print(f"Enabled: {orchestrator.enabled}")
print(f"Max cycles: {orchestrator.max_cycles}")  # Should be 0
print(f"Auto restart: {orchestrator.auto_restart}")  # Should be True
```

### **Method 3: Check Status in Real-Time**

```bash
# Check agent status
python tools/agent_status_quick_check.py --all

# Or use V2 tool
python -m tools.toolbelt captain.status_check
```

---

## 🚀 STARTING THE CONTINUOUS MONITOR

### **Option 1: Start Orchestrator (Recommended)**

The orchestrator will start the monitor automatically:

```python
from src.orchestrators.overnight.orchestrator import OvernightOrchestrator

orchestrator = OvernightOrchestrator()
await orchestrator.start()  # Monitor starts, runs forever
```

### **Option 2: Start Monitor Directly**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor

monitor = ProgressMonitor()
monitor.start_monitoring()

# Monitor is now running continuously
# It will check agents every 60 seconds
# It will run forever (until manually stopped)
```

### **Option 3: Command Line (If Available)**

```bash
# If there's a CLI command
python -m src.orchestrators.overnight.cli start --continuous
```

---

## ⚙️ ADVANCED CONFIGURATION OPTIONS

### **For Faster Response (More Frequent Checks):**

```yaml
monitoring:
  check_interval: 30  # Check every 30 seconds (faster)
  stall_timeout: 180  # 3 minutes = stalled (faster detection)
```

### **For Longer Tasks (More Patient):**

```yaml
monitoring:
  check_interval: 120  # Check every 2 minutes (less frequent)
  stall_timeout: 900   # 15 minutes = stalled (more patient)
```

### **For Maximum Performance Tracking:**

```yaml
monitoring:
  check_interval: 60
  stall_timeout: 300
  health_checks: true
  performance_tracking: true  # Track all metrics
```

---

## 🔄 WHAT HAPPENS AFTER RECONFIGURATION

### **Before (Current):**
- Runs for 60 cycles (10 hours)
- Stops automatically
- Needs manual restart

### **After (Reconfigured):**
- Runs for infinite cycles (forever)
- Never stops automatically
- Auto-restarts if crashes
- Continuously monitors all agents

---

## 📊 MONITORING OUTPUT (What You'll See)

### **Every Check Cycle (Every 60 seconds):**

```
[INFO] Cycle 1: Checking agent status...
[INFO] Agent-1: busy (task_123)
[INFO] Agent-2: idle
[INFO] Agent-3: busy (task_456)
...
[INFO] No stalled agents detected
[INFO] System health: healthy
```

### **If Agent Stalls:**

```
[WARNING] Detected stalled agents: ['Agent-5']
[WARNING] Agent-5: No activity for 305 seconds
[ERROR] System health: unhealthy
[ERROR] Issues: ['Stalled agents: [Agent-5]']
```

### **Performance Metrics (Periodic):**

```
[INFO] Performance metrics:
  - Cycles completed: 42
  - Total tasks: 150
  - Completed tasks: 128
  - Failed tasks: 7
  - Completion rate: 85.3%
  - Uptime: 7.0 hours
```

---

## 🛡️ SAFETY FEATURES

### **Auto-Restart Protection:**

If the monitor crashes, `auto_restart: true` will:
1. Detect the crash
2. Log the error
3. Restart the monitor
4. Continue monitoring

### **Health Check Protection:**

If system health degrades:
1. Health checks detect issues
2. Logs warnings
3. Can trigger recovery actions
4. Prevents cascading failures

### **Stall Detection Protection:**

If agents stall:
1. Monitor detects stall
2. Logs warning
3. Marks agent as stalled
4. Can trigger recovery/rescue

---

## 🎯 QUICK REFERENCE

### **Key Settings for Continuous Operation:**

| Setting | Value | Purpose |
|---------|-------|---------|
| `enabled` | `true` | Enable overnight operations |
| `max_cycles` | `0` | Infinite cycles (never stops) |
| `auto_restart` | `true` | Restart if crashes |
| `check_interval` | `60` | Check every 60 seconds |
| `stall_timeout` | `300` | 5 minutes = stalled |
| `health_checks` | `true` | Enable health monitoring |
| `performance_tracking` | `true` | Track performance |

### **File to Edit:**
```
config/orchestration.yml
```

### **Section to Edit:**
```yaml
overnight:
  max_cycles: 0  # Change from 60 to 0
```

---

## ✅ CHECKLIST

- [ ] Opened `config/orchestration.yml`
- [ ] Found `overnight:` section
- [ ] Changed `max_cycles: 60` to `max_cycles: 0`
- [ ] Verified `enabled: true`
- [ ] Verified `auto_restart: true`
- [ ] Verified monitoring settings are correct
- [ ] Saved the file
- [ ] Tested configuration loads correctly
- [ ] Started the monitor
- [ ] Verified it's running continuously

---

## 🚨 TROUBLESHOOTING

### **Issue: Monitor Still Stops**

**Check:**
1. Is `max_cycles: 0` set correctly?
2. Is `enabled: true`?
3. Are there any errors in logs?
4. Is `auto_restart: true`?

**Fix:**
```yaml
overnight:
  enabled: true
  max_cycles: 0  # Must be 0, not 60
  auto_restart: true
```

### **Issue: Monitor Not Starting**

**Check:**
1. Is configuration file valid YAML?
2. Are there syntax errors?
3. Is the file path correct?

**Fix:**
```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('config/orchestration.yml'))"
```

### **Issue: Agents Always Stalled**

**Check:**
1. Is `stall_timeout` too short?
2. Are agents actually working?
3. Is activity being tracked?

**Fix:**
```yaml
monitoring:
  stall_timeout: 600  # Increase to 10 minutes
```

---

## 📝 SUMMARY FOR VICTOR

**To Make It Never Stop:**

1. **Edit**: `config/orchestration.yml`
2. **Find**: `overnight:` section
3. **Change**: `max_cycles: 60` → `max_cycles: 0`
4. **Save**: The file
5. **Start**: The orchestrator/monitor
6. **Verify**: It's running continuously

**That's it!** The system will now run forever, continuously monitoring all 8 agents.

---

**WE. ARE. SWARM. MONITORED. CONTINUOUS.** 🐝⚡🔥

*Reconfiguration guide for Victor - 2025-01-27*




