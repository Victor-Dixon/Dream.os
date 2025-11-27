# 🔍 Agent Status Monitoring System - Explained for Victor

**From**: Agent-4 (Captain)  
**To**: Victor  
**Date**: 2025-01-27  
**Purpose**: Detailed explanation of agent status monitoring system

---

## 🎯 THE BIG PICTURE

**What It Does**: The monitoring system watches all 8 agents 24/7 to make sure they're working and not stuck.

**Why It Matters**: Since "the system never stops," we need to know:
- Which agents are working
- Which agents are stuck (stalled)
- Which agents need help
- Overall system health

**Think of it like**: A security guard watching 8 workers, making sure they're all doing their jobs and not frozen.

---

## 🏗️ HOW IT WORKS (Simple Explanation)

### **The Three Main Parts:**

1. **ProgressMonitor** (`src/orchestrators/overnight/monitor.py`)
   - The "watchdog" that checks on agents
   - Tracks when each agent last did something
   - Detects if an agent is stuck (stalled)

2. **MonitorState** (`src/orchestrators/overnight/monitor_state.py`)
   - The "memory" that remembers agent activity
   - Stores timestamps of last activity
   - Tracks what task each agent is working on

3. **OvernightOrchestrator** (`src/orchestrators/overnight/orchestrator.py`)
   - The "boss" that runs everything
   - Starts/stops monitoring
   - Coordinates the whole system

---

## ⚙️ HOW IT TRACKS AGENTS

### **What Gets Tracked:**

For each agent (Agent-1 through Agent-8):

1. **Last Activity Time**: When did they last do something?
   - Updated every time agent completes a task
   - Used to detect if agent is stuck

2. **Current Task**: What are they working on right now?
   - Task ID or description
   - Set when agent starts a task
   - Cleared when task completes

3. **Status**: Are they busy, idle, or stalled?
   - **Busy**: Working on a task
   - **Idle**: No current task
   - **Stalled**: No activity for too long (default: 5 minutes)

### **The Tracking Process:**

```
1. Agent starts working → Update "last_activity" timestamp
2. Agent gets a task → Set "current_task" 
3. Agent completes task → Clear "current_task", update "last_activity"
4. Monitor checks every 60 seconds (default)
5. If no activity for 5 minutes (default) → Mark as "stalled"
```

---

## 🔧 CONFIGURATION (The Settings)

### **Key Settings in `config/orchestration.yml`:**

```yaml
overnight:
  monitoring:
    check_interval: 60        # How often to check (seconds)
    stall_timeout: 300         # When to mark as stalled (seconds)
    health_checks: true        # Enable health monitoring
    performance_tracking: true # Track performance metrics
```

### **What Each Setting Does:**

1. **`check_interval: 60`**
   - **What**: How often the monitor checks on agents
   - **Default**: Every 60 seconds (1 minute)
   - **Why**: Balance between responsiveness and system load
   - **Change if**: You want faster/slower checks

2. **`stall_timeout: 300`**
   - **What**: How long before marking agent as "stalled"
   - **Default**: 300 seconds (5 minutes)
   - **Why**: Agents might take time on complex tasks
   - **Change if**: Tasks take longer/shorter than expected

3. **`health_checks: true`**
   - **What**: Enable health status monitoring
   - **Default**: true
   - **Why**: Detects system-wide issues
   - **Keep**: true (recommended)

4. **`performance_tracking: true`**
   - **What**: Track performance metrics
   - **Default**: true
   - **Why**: See how well system is performing
   - **Keep**: true (recommended)

---

## 🚨 STALL DETECTION (How It Knows Agents Are Stuck)

### **The Logic:**

```python
current_time = time.time()
last_activity = agent_activity[agent_id]
time_since_activity = current_time - last_activity

if time_since_activity > stall_timeout:
    status = "stalled"  # Agent is stuck!
elif current_task:
    status = "busy"     # Agent is working
else:
    status = "idle"     # Agent has no task
```

### **What Happens When Agent is Stalled:**

1. Monitor detects stall
2. Logs warning: "Detected stalled agents: [Agent-X]"
3. Health status marked as unhealthy
4. Recovery system can be triggered (if configured)

---

## 📊 STATUS REPORTS (What You Can See)

### **Agent Status Information:**

For each agent, you get:
```json
{
  "status": "busy" | "idle" | "stalled",
  "last_activity": 1234567890.123,  // Unix timestamp
  "time_since_activity": 45.2,       // Seconds since last activity
  "current_task": "task_123"         // Current task ID or null
}
```

### **System Health Status:**

```json
{
  "healthy": true | false,
  "issues": ["Stalled agents: [Agent-3]", ...],
  "completion_rate": 0.85,  // 85% of tasks completed
  "failure_rate": 0.05,     // 5% of tasks failed
  "stalled_agents": ["Agent-3"]
}
```

### **Performance Metrics:**

```json
{
  "cycles_completed": 42,
  "total_tasks": 150,
  "completed_tasks": 128,
  "failed_tasks": 7,
  "average_cycle_time": 600.5,  // seconds
  "average_task_time": 45.2,     // seconds
  "uptime_seconds": 25200,       // 7 hours
  "cycles_per_hour": 6.0,
  "tasks_per_hour": 21.4
}
```

---

## 🔄 THE MONITORING LOOP (How It Runs Continuously)

### **The Main Loop:**

```python
while is_running:
    # 1. Check for stalled agents
    stalled_agents = await monitor.get_stalled_agents()
    
    # 2. Check system health
    health_status = await monitor.get_health_status()
    
    # 3. Update agent status
    agent_status = monitor.get_agent_status()
    
    # 4. Generate status report
    report = monitor.generate_status_report()
    
    # 5. Wait before next check
    await asyncio.sleep(check_interval)
```

### **What Happens Each Cycle:**

1. **Check Agents**: Look at all 8 agents
2. **Detect Stalls**: Find agents with no recent activity
3. **Check Health**: Determine if system is healthy
4. **Update Metrics**: Track performance
5. **Wait**: Sleep for `check_interval` seconds
6. **Repeat**: Do it all over again

---

## 🛠️ HOW TO RECONFIGURE IT

### **Option 1: Edit Configuration File**

Edit `config/orchestration.yml`:

```yaml
overnight:
  monitoring:
    check_interval: 30        # Check every 30 seconds (faster)
    stall_timeout: 600        # 10 minutes before marking stalled
    health_checks: true
    performance_tracking: true
```

### **Option 2: Programmatic Configuration**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor

config = {
    'overnight': {
        'monitoring': {
            'check_interval': 30,      # 30 seconds
            'stall_timeout': 600,       # 10 minutes
            'health_checks': True,
            'performance_tracking': True
        }
    }
}

monitor = ProgressMonitor(config)
monitor.start_monitoring()
```

### **Option 3: Environment Variables**

Set environment variables (if supported):
```bash
export MONITOR_CHECK_INTERVAL=30
export MONITOR_STALL_TIMEOUT=600
```

---

## 🎯 RECOMMENDED CONFIGURATIONS

### **For Continuous Operation (Never Stops):**

```yaml
overnight:
  monitoring:
    check_interval: 60        # Check every minute
    stall_timeout: 300        # 5 minutes = stalled
    health_checks: true
    performance_tracking: true
  enabled: true               # MUST be true
  auto_restart: true          # Restart if crashes
  max_cycles: 0               # 0 = infinite cycles
```

### **For Faster Response (More Responsive):**

```yaml
overnight:
  monitoring:
    check_interval: 30        # Check every 30 seconds
    stall_timeout: 180        # 3 minutes = stalled
    health_checks: true
    performance_tracking: true
```

### **For Longer Tasks (More Patient):**

```yaml
overnight:
  monitoring:
    check_interval: 120       # Check every 2 minutes
    stall_timeout: 900        # 15 minutes = stalled
    health_checks: true
    performance_tracking: true
```

---

## 🔍 HOW TO CHECK STATUS

### **Method 1: Quick Check Tool**

```bash
# Check all agents
python tools/agent_status_quick_check.py --all

# Check specific agent
python tools/agent_status_quick_check.py --agent Agent-3

# Detailed check
python tools/agent_status_quick_check.py --agent Agent-3 --detail
```

### **Method 2: Captain Status Check (V2 Tool)**

```bash
# Using tools_v2
python -m tools_v2.toolbelt captain.status_check
```

### **Method 3: Programmatic Check**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor

monitor = ProgressMonitor()
monitor.start_monitoring()

# Get agent status
agent_status = monitor.get_agent_status()
print(agent_status)

# Get health status
health = await monitor.get_health_status()
print(health)

# Get performance metrics
metrics = monitor.get_performance_metrics()
print(metrics)
```

---

## 🚀 STARTING THE MONITOR

### **Automatic Start (Recommended):**

The monitor starts automatically when the orchestrator runs:

```python
from src.orchestrators.overnight.orchestrator import OvernightOrchestrator

orchestrator = OvernightOrchestrator()
await orchestrator.start()  # Monitor starts automatically
```

### **Manual Start:**

```python
from src.orchestrators.overnight.monitor import ProgressMonitor

monitor = ProgressMonitor()
monitor.start_monitoring()

# Monitor is now running
# It will check agents every check_interval seconds
```

### **Stop Monitoring:**

```python
monitor.stop_monitoring()
```

---

## ⚠️ COMMON ISSUES & FIXES

### **Issue 1: Monitor Not Running**

**Symptoms**: No status updates, agents not being tracked

**Fix**:
```python
# Check if monitoring is active
info = monitor.get_monitor_info()
if not info['monitoring_active']:
    monitor.start_monitoring()
```

### **Issue 2: Agents Always Marked as Stalled**

**Symptoms**: All agents show as "stalled" even when working

**Possible Causes**:
- `stall_timeout` too short
- Agent activity not being updated
- Clock/timezone issues

**Fix**:
```yaml
# Increase stall_timeout
stall_timeout: 600  # 10 minutes instead of 5
```

### **Issue 3: Monitor Stops After Some Time**

**Symptoms**: Monitor works initially but stops later

**Possible Causes**:
- Exception in monitoring loop
- System resource limits
- Configuration issues

**Fix**:
```yaml
# Enable auto-restart
overnight:
  auto_restart: true
  max_cycles: 0  # Infinite cycles
```

---

## 📝 SUMMARY FOR VICTOR

**What It Is**: A watchdog system that monitors all 8 agents continuously.

**What It Does**:
- Tracks when each agent last did something
- Detects if agents are stuck (stalled)
- Reports system health
- Tracks performance metrics

**Key Settings**:
- `check_interval`: How often to check (default: 60 seconds)
- `stall_timeout`: When to mark as stalled (default: 300 seconds = 5 minutes)

**To Make It Never Stop**:
- Set `enabled: true`
- Set `auto_restart: true`
- Set `max_cycles: 0` (infinite)

**To Check Status**:
```bash
python tools/agent_status_quick_check.py --all
```

---

## 🔗 RELATED FILES

- **Main Monitor**: `src/orchestrators/overnight/monitor.py`
- **State Management**: `src/orchestrators/overnight/monitor_state.py`
- **Orchestrator**: `src/orchestrators/overnight/orchestrator.py`
- **Quick Check Tool**: `tools/agent_status_quick_check.py`
- **Captain Tool**: `tools_v2.toolbelt captain.status_check` (use `tools_v2.toolbelt captain.status_check`)

---

**WE. ARE. SWARM. MONITORED. POWERFUL.** 🐝⚡🔥

*Explained for Victor - 2025-01-27*



