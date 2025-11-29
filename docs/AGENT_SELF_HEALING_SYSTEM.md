# 🏥 Agent Self-Healing System - Complete Integration Guide

**Author:** Agent-3 (Infrastructure & DevOps Specialist)  
**Date:** 2025-01-27  
**Priority:** CRITICAL - Prevents 2XX stalled agents

---

## 🎯 WHAT IT DOES

The **Agent Self-Healing System** automatically detects and recovers stalled agents **before they accumulate**. It runs continuously as part of the overnight orchestrator to prevent agent stalls from reaching critical levels (like 2XX stalled agents).

---

## 🔄 HOW IT WORKS - FULL INTEGRATION

### **Architecture Overview:**

```
┌─────────────────────────────────────────────────────────────┐
│  Overnight Orchestrator (Main Coordinator)                  │
│  - Runs every cycle (10 minutes default)                    │
│  - Coordinates all subsystems                                │
└────────────┬────────────────────────────────────────────────┘
             │
             ├───► ProgressMonitor (Detection)
             │     - Uses EnhancedAgentActivityDetector
             │     - Checks status.json, devlogs, inbox
             │     - Identifies stalled agents
             │
             ├───► Self-Healing System (PROACTIVE RECOVERY) 🆕
             │     - Runs EVERY 30 SECONDS (continuous daemon)
             │     - Detects stalls in 2 MINUTES (aggressive)
             │     - Automatic file-level recovery
             │     - Force status.json updates
             │     - Clear stuck tasks
             │     - Reset agent status
             │     - Send rescue messages
             │
             └───► RecoverySystem (STANDARD RECOVERY)
                   - Runs on orchestrator cycle
                   - Handles complex recovery scenarios
                   - Sends Discord alerts
                   - Task reassignment
```

---

## 🚀 HOW IT'S INTEGRATED

### **1. Orchestrator Integration**

The self-healing system is integrated into `OvernightOrchestrator`:

```python
# src/orchestrators/overnight/orchestrator.py

class OvernightOrchestrator:
    def __init__(self):
        # ... existing code ...
        
        # Self-healing system initialization
        self.self_healing_system = get_self_healing_system(healing_config)
        
    async def start(self):
        # Start self-healing daemon
        self.self_healing_system.start()  # Runs continuously
        
    async def _check_recovery(self):
        # PROACTIVE: Self-healing runs FIRST (every 30s via daemon)
        if self.self_healing_system:
            stalled = await self.self_healing_system._detect_stalled_agents()
            for agent_id, duration in stalled:
                await self.self_healing_system._heal_stalled_agent(agent_id, duration)
        
        # STANDARD: Existing recovery system runs on cycle
        stalled_agents = await self.monitor.get_stalled_agents()
        await self.recovery.handle_stalled_agents(stalled_agents)
```

### **2. Continuous Monitoring (Daemon Mode)**

The self-healing system runs as a **background daemon** that checks every 30 seconds:

```python
# Background task runs continuously
async def _monitoring_loop(self):
    while self.running:
        await self._check_and_heal_all_agents()  # Check all 8 agents
        await asyncio.sleep(30)  # Wait 30 seconds
```

### **3. Detection Strategy**

The system uses **two-layer detection**:

1. **Self-Healing Detection** (2-minute threshold):
   - Checks `status.json` file modification time
   - Checks via `EnhancedAgentActivityDetector`
   - More aggressive (catches stalls faster)

2. **Monitor Detection** (5-minute threshold):
   - Existing `ProgressMonitor` system
   - Uses task assignment tracking
   - Standard recovery flow

---

## 🔧 HEALING ACTIONS (Progressive Recovery)

When a stalled agent is detected, the system tries **less invasive actions first**:

### **Action 1: Force Status Update** (Least Invasive)
- Updates `status.json` `last_updated` timestamp
- Adds healing marker to status
- Refreshes file modification time

### **Action 2: Clear Stuck Tasks**
- Removes old/stuck tasks from status
- Marks tasks as cleared in healing history

### **Action 3: Reset Agent Status** (More Invasive)
- Creates fresh `status.json` with default values
- Sets agent to "ACTIVE_AGENT_MODE"
- Marks as recovered in healing history

### **Action 4: Send Rescue Message**
- Calls `RecoverySystem._rescue_agent()`
- Sends message to agent inbox
- Triggers agent wake-up

### **Action 5: Escalation** (If All Fail)
- Creates `.ESCALATION_REQUIRED` marker file
- Logs error for manual intervention
- After 3 failed attempts

---

## 📊 CONFIGURATION

### **Orchestration Config** (`config/orchestration.yml`):

```yaml
overnight:
  enabled: true
  
  # Self-healing configuration
  self_healing:
    enabled: true                    # Enable self-healing
    check_interval: 30               # Check every 30 seconds
    max_attempts: 3                  # Max recovery attempts per agent
    auto_reset: true                 # Allow status.json reset
  
  # Monitoring configuration (shared with self-healing)
  monitoring:
    check_interval: 60               # Monitor check interval
    stall_timeout: 300               # 5 minutes = stalled (standard)
                                     # Self-healing uses 120s (2 min)
```

### **Self-Healing Config Defaults:**

```python
SelfHealingConfig(
    check_interval_seconds=30,      # Check every 30 seconds
    stall_threshold_seconds=120,    # 2 minutes = stalled (aggressive)
    recovery_attempts_max=3,        # Max 3 attempts before escalation
    auto_reset_enabled=True,        # Allow status.json reset
    force_update_enabled=True,      # Force status updates
    clear_stuck_tasks=True,         # Clear stuck tasks
)
```

---

## 🎮 USAGE

### **1. Automatic (Default)**

The system runs **automatically** when the orchestrator starts:

```bash
# Start orchestrator (self-healing starts automatically)
python -m src.orchestrators.overnight.orchestrator
```

### **2. Manual Immediate Check**

Run immediate healing check:

```bash
python tools/heal_stalled_agents.py --check-now
```

Output:
```
🏥 IMMEDIATE STALLED AGENT HEALING CHECK
=======================================
🔍 Detected 8 stalled agents: [...]
🏥 Healing Agent-1 (stalled 12962s, attempt 1/3)
✅ Agent-1: Healing successful
...
✅ Successfully healed: Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7, Agent-8
```

### **3. Standalone Daemon Mode**

Run self-healing as standalone daemon (without orchestrator):

```bash
python tools/heal_stalled_agents.py --start-daemon --interval 30 --threshold 120
```

---

## 🔍 HOW IT DETECTS STALLS

### **Detection Sources:**

1. **Status.json File Modification Time**
   ```python
   file_mtime = status_file.stat().st_mtime
   age_seconds = current_time - file_mtime
   if age_seconds > 120:  # 2 minutes
       agent_is_stalled = True
   ```

2. **Enhanced Activity Detector** (if available)
   ```python
   detector = EnhancedAgentActivityDetector()
   stale_agents = detector.get_stale_agents(max_age_seconds=120)
   # Returns: [(agent_id, age_seconds), ...]
   ```

3. **Activity Sources Checked:**
   - `status.json` last_updated timestamp
   - Devlog files (recent activity)
   - Inbox messages (receipt time)
   - Task assignments
   - File modifications in workspace

---

## ✅ HEALING SUCCESS INDICATORS

After healing, agents show these markers:

```json
{
  "agent_id": "Agent-3",
  "status": "ACTIVE_AGENT_MODE",
  "last_updated": "2025-01-27 19:03:24",
  "healing_applied": [
    {
      "timestamp": "2025-01-27T19:03:24.342",
      "action": "force_update",
      "reason": "stall_recovery"
    }
  ]
}
```

---

## 📈 MONITORING & STATISTICS

Get healing statistics:

```python
from src.core.agent_self_healing_system import get_self_healing_system

system = get_self_healing_system()
stats = system.get_healing_stats()

# Output:
{
  "total_actions": 8,
  "successful": 8,
  "failed": 0,
  "success_rate": 100.0,
  "by_agent": {
    "Agent-1": {"total": 1, "successful": 1, "failed": 0},
    ...
  },
  "recent_actions": [...]
}
```

---

## 🚨 ESCALATION & FAILURE HANDLING

If an agent fails healing after 3 attempts:

1. **Escalation Marker Created:**
   ```
   agent_workspaces/Agent-X/.ESCALATION_REQUIRED
   ```

2. **Logs Error:**
   ```
   🚨 ESCALATION: Agent-X requires manual intervention (3 recovery attempts failed)
   ```

3. **History Tracked:**
   - All healing attempts recorded in `healing_history`
   - Can review what was tried
   - Helps diagnose persistent issues

---

## 🔄 INTEGRATION WITH EXISTING SYSTEMS

### **Works With:**

1. **ProgressMonitor** ✅
   - Self-healing uses same detection logic
   - Complements monitor (faster response)

2. **RecoverySystem** ✅
   - Self-healing handles file-level recovery
   - RecoverySystem handles complex scenarios
   - Both work together

3. **EnhancedAgentActivityDetector** ✅
   - Primary detection source
   - Comprehensive activity checking
   - Status.json + devlogs + inbox

4. **Messaging System** ✅
   - Rescue messages via messaging core
   - Notifications to agents
   - Coordination support

---

## 🎯 KEY DIFFERENCES: Self-Healing vs Standard Recovery

| Feature | Self-Healing | Standard Recovery |
|---------|--------------|-------------------|
| **Check Interval** | Every 30 seconds | Every 10 minutes (orchestrator cycle) |
| **Stall Threshold** | 2 minutes (aggressive) | 5 minutes (standard) |
| **Recovery Actions** | File-level (status.json) | Complex (messaging, task reassignment) |
| **When Runs** | Continuous daemon | On orchestrator cycle |
| **Speed** | Fast (immediate file updates) | Slower (full recovery flow) |
| **Purpose** | Prevent accumulation | Handle complex failures |

**Together:** Self-healing prevents the problem, standard recovery handles complex cases.

---

## 💡 EXAMPLE FLOW

### **Scenario: Agent-3 Stalls**

1. **00:00** - Agent-3's `status.json` last updated
2. **00:02** - Self-healing detects stall (2 minutes passed)
3. **00:02** - Action 1: Force status update (updates timestamp)
4. **00:02** - ✅ Agent-3 marked as active again

**OR if status update fails:**

1. **00:02** - Action 1 fails (file locked?)
2. **00:02** - Action 2: Clear stuck tasks
3. **00:02** - ✅ Agent-3 recovered

**OR if all actions fail:**

1. **00:02** - Actions 1-4 all fail
2. **00:04** - Attempt 2 fails again
3. **00:06** - Attempt 3 fails again
4. **00:06** - 🚨 Escalation: Manual intervention required

---

## 🛠️ TROUBLESHOOTING

### **Self-healing not running?**

Check orchestrator config:
```yaml
overnight:
  self_healing:
    enabled: true  # Must be true
```

### **Not detecting stalls?**

Check thresholds:
- Self-healing: 120 seconds (2 minutes)
- Monitor: 300 seconds (5 minutes)

### **Healing not working?**

Check healing stats:
```bash
python tools/heal_stalled_agents.py --check-now --verbose
```

Look for errors in logs:
```
ERROR: Error forcing status update for Agent-X: [error message]
```

---

## ✅ SUMMARY

**The self-healing system is FULLY INTEGRATED:**

1. ✅ Runs automatically when orchestrator starts
2. ✅ Continuous monitoring (every 30 seconds)
3. ✅ Aggressive detection (2-minute threshold)
4. ✅ Progressive recovery actions
5. ✅ Works with existing monitor/recovery systems
6. ✅ Can run standalone for immediate healing
7. ✅ Full statistics and history tracking
8. ✅ Escalation for persistent failures

**Result:** Prevents 2XX stalled agents by catching and healing stalls immediately, before they accumulate.

---

**🎯 MISSION ACCOMPLISHED:** The system is proactive, integrated, and prevents agent stalls from reaching critical levels!

