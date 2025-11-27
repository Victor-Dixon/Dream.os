# 🔍 Stall Detection & Activity Tracking - Deep Dive

**For:** Victor  
**From:** Agent-4 (Captain)  
**Date:** 2025-01-27

---

## 🎯 OVERVIEW

This document explains **exactly** how the monitoring system detects when agents are stalled and what happens when they are.

---

## 📊 HOW THE SYSTEM TRACKS AGENT ACTIVITY

### **Activity Tracking Mechanism**

The system uses a **simple timestamp-based approach**:

```python
# In monitor.py / monitor_state.py
self.agent_activity = {}  # Agent ID -> last activity timestamp
```

**Key Point:** The system does NOT directly check `status.json` files or devlogs. Instead, it relies on **task updates from the orchestrator**.

### **How Activity Gets Updated**

Activity is updated in **3 main ways**:

#### **1. Task Assignment (Primary Method)**
```python
# In monitor.py - update_tasks()
def update_tasks(self, tasks: List[Dict[str, Any]]) -> None:
    current_time = time.time()
    
    for task in tasks:
        agent_id = task.get('agent_id')
        task_id = task.get('id')
        
        if agent_id:
            # THIS IS WHERE ACTIVITY GETS UPDATED
            self.agent_activity[agent_id] = current_time  # ← Activity timestamp updated
            self.agent_tasks[agent_id] = task_id
```

**What this means:**
- When the orchestrator assigns a task to an agent, the activity timestamp is updated
- This happens **automatically** when tasks are distributed
- The agent doesn't need to do anything - just receiving a task counts as activity

#### **2. Task Completion**
```python
# In monitor.py - mark_task_completed()
def mark_task_completed(self, task_id: str, agent_id: str, duration: float) -> None:
    # Activity timestamp is NOT updated here
    # But the task is cleared
    if agent_id in self.agent_tasks:
        self.agent_tasks[agent_id] = None
```

**Important:** Task completion does **NOT** update the activity timestamp. Only task assignment does.

#### **3. Initialization**
```python
# In monitor.py - start_monitoring()
def start_monitoring(self) -> None:
    current_time = time.time()
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        self.agent_activity[agent_id] = current_time  # ← Initial timestamp
        self.agent_tasks[agent_id] = None
```

**What this means:**
- When monitoring starts, all agents get the current timestamp
- This prevents false positives at startup

---

## ⏱️ HOW STALL DETECTION WORKS

### **The Check Process**

The system checks for stalled agents **every `check_interval` seconds** (default: 60 seconds):

```python
# In monitor.py - get_stalled_agents()
async def get_stalled_agents(self) -> List[str]:
    stalled_agents = []
    current_time = time.time()
    
    for agent_id, last_activity in self.agent_activity.items():
        # Calculate time since last activity
        time_since_activity = current_time - last_activity
        
        # If time exceeds stall_timeout, agent is stalled
        if time_since_activity > self.stall_timeout:
            stalled_agents.append(agent_id)
    
    if stalled_agents:
        self.logger.warning(f"Detected stalled agents: {stalled_agents}")
    
    return stalled_agents
```

### **Stall Detection Logic**

**Formula:**
```
time_since_activity = current_time - last_activity_timestamp

if time_since_activity > stall_timeout:
    agent_status = "stalled"
```

**Default Values:**
- `check_interval`: 60 seconds (how often to check)
- `stall_timeout`: 300 seconds (5 minutes) (how long before considered stalled)

**Status Determination:**
```python
# In monitor.py - get_agent_status()
if time_since_activity > self.stall_timeout:
    status = 'stalled'
elif current_task:
    status = 'busy'
else:
    status = 'idle'
```

---

## 🚨 WHAT HAPPENS WHEN AN AGENT IS DETECTED AS STALLED

### **Step 1: Detection**

Every cycle, the orchestrator checks for stalled agents:

```python
# In orchestrator.py - _check_recovery()
async def _check_recovery(self) -> None:
    # Check for stalled agents
    stalled_agents = await self.monitor.get_stalled_agents()
    
    if stalled_agents:
        self.logger.warning(f"Found {len(stalled_agents)} stalled agents")
        await self.recovery.handle_stalled_agents(stalled_agents)
```

### **Step 2: Recovery System Activation**

When stalled agents are detected, the recovery system handles them:

```python
# In recovery.py - handle_stalled_agents()
async def handle_stalled_agents(self, stalled_agents: list[str]) -> None:
    self.logger.warning(f"Handling {len(stalled_agents)} stalled agents")
    
    for agent_id in stalled_agents:
        await self._rescue_agent(agent_id)
```

### **Step 3: Agent Rescue**

The system sends a rescue message to the stalled agent:

```python
# In recovery.py - _rescue_agent()
async def _rescue_agent(self, agent_id: str) -> None:
    # Reset recovery attempts counter
    self.recovery_attempts[agent_id] = 0
    
    # Send rescue message
    await self.messaging.send_agent_rescue_message(agent_id)
    
    # Record rescue in history
    self.failure_history.append({
        "type": "agent_rescue",
        "agent_id": agent_id,
        "timestamp": time.time(),
    })
    
    self.logger.info(f"Agent rescue completed for {agent_id}")
```

### **Step 4: Rescue Message**

The rescue message sent to the agent:

```python
# In recovery_messaging.py - send_agent_rescue_message()
async def send_agent_rescue_message(self, agent_id: str) -> None:
    rescue_message = f"[RESCUE] {agent_id} - Reset and resume operations. Report status."
    
    # Message is sent via PyAutoGUI to agent's chat interface
    await asyncio.get_event_loop().run_in_executor(
        None, send_message_to_agent, agent_id, rescue_message
    )
```

**Message Content:**
```
[RESCUE] Agent-X - Reset and resume operations. Report status.
```

---

## 🔄 THE COMPLETE FLOW

### **Normal Operation:**
```
1. Orchestrator assigns task to Agent-X
   ↓
2. monitor.update_tasks() called
   ↓
3. agent_activity["Agent-X"] = current_time (updated)
   ↓
4. Agent works on task
   ↓
5. Every 60 seconds: check for stalled agents
   ↓
6. time_since_activity < 300 seconds → Agent is "busy" or "idle"
   ↓
7. Continue monitoring
```

### **Stalled Agent Flow:**
```
1. Agent receives task
   ↓
2. agent_activity["Agent-X"] = timestamp (updated)
   ↓
3. Agent stops responding/working
   ↓
4. 5+ minutes pass with no new task assignment
   ↓
5. Check cycle runs: time_since_activity > 300 seconds
   ↓
6. Agent marked as "stalled"
   ↓
7. orchestrator._check_recovery() called
   ↓
8. recovery.handle_stalled_agents() called
   ↓
9. recovery._rescue_agent() called
   ↓
10. Rescue message sent: "[RESCUE] Agent-X - Reset and resume operations. Report status."
   ↓
11. Recovery attempt recorded in failure_history
   ↓
12. Monitoring continues
```

---

## ⚠️ IMPORTANT LIMITATIONS

### **What the System DOES NOT Check:**

1. **❌ Does NOT check `status.json` files directly**
   - The monitoring system doesn't read status.json
   - It only tracks activity via task assignments

2. **❌ Does NOT check devlogs**
   - Devlog creation doesn't update activity
   - Only task assignments update activity

3. **❌ Does NOT check inbox processing**
   - Inbox activity doesn't update the timestamp
   - Only orchestrator task assignments do

### **What This Means:**

**An agent can be working but still appear "stalled" if:**
- They're working on a task but no new task has been assigned
- They're updating status.json but not receiving new tasks
- They're creating devlogs but not receiving new tasks
- They're processing inbox messages but not receiving new tasks

**The system only knows an agent is active if:**
- A new task is assigned to them (via orchestrator)
- The task assignment updates their activity timestamp

---

## 🔧 CONFIGURATION

### **Key Settings (config/orchestration.yml):**

```yaml
overnight:
  monitoring:
    check_interval: 60      # Check every 60 seconds
    stall_timeout: 300      # 5 minutes = stalled
    health_checks: true
    performance_tracking: true
```

### **How to Adjust:**

**To make stall detection more sensitive:**
- Decrease `stall_timeout` (e.g., 180 seconds = 3 minutes)

**To make stall detection less sensitive:**
- Increase `stall_timeout` (e.g., 600 seconds = 10 minutes)

**To check more frequently:**
- Decrease `check_interval` (e.g., 30 seconds)

**To check less frequently:**
- Increase `check_interval` (e.g., 120 seconds)

---

## 📊 ACTIVITY TRACKING SUMMARY

### **What Updates Activity:**
- ✅ Task assignment (via orchestrator)
- ✅ Initialization (when monitoring starts)

### **What Does NOT Update Activity:**
- ❌ Task completion
- ❌ Status.json updates
- ❌ Devlog creation
- ❌ Inbox processing
- ❌ Manual agent work

### **Activity Detection Method:**
- **Primary:** Task assignment timestamps
- **Not Used:** File modification times, status.json reading, devlog scanning

---

## 🎯 KEY TAKEAWAYS

1. **Activity = Task Assignment**
   - The system only knows an agent is active when they receive a new task
   - Working on existing tasks doesn't update activity

2. **Stall = No New Tasks for 5+ Minutes**
   - An agent is "stalled" if no new task has been assigned in 5+ minutes
   - This doesn't mean they're not working - just that no new tasks were assigned

3. **Rescue = Automatic Message**
   - When stalled, agent receives a rescue message
   - Message is sent via PyAutoGUI to their chat interface
   - Recovery attempt is logged

4. **Limitation: File-Based Activity Not Tracked**
   - The system doesn't check if agents are updating files
   - It only tracks orchestrator task assignments
   - This is a design choice for simplicity

---

## 🔍 EXAMPLE SCENARIOS

### **Scenario 1: Agent Working Normally**
```
T+0:00 - Task assigned → activity updated
T+1:00 - Check cycle → time_since = 60s → status = "busy" ✅
T+2:00 - Check cycle → time_since = 120s → status = "busy" ✅
T+3:00 - Check cycle → time_since = 180s → status = "busy" ✅
T+4:00 - Check cycle → time_since = 240s → status = "busy" ✅
T+5:00 - Check cycle → time_since = 300s → status = "stalled" ⚠️
```

**Problem:** Agent is still working, but no new task assigned, so they appear stalled.

### **Scenario 2: Agent Actually Stalled**
```
T+0:00 - Task assigned → activity updated
T+1:00 - Agent stops responding
T+2:00 - Check cycle → time_since = 120s → status = "busy"
T+3:00 - Check cycle → time_since = 180s → status = "busy"
T+4:00 - Check cycle → time_since = 240s → status = "busy"
T+5:00 - Check cycle → time_since = 300s → status = "stalled" ⚠️
T+5:01 - Rescue message sent → "[RESCUE] Agent-X - Reset and resume operations."
```

**Result:** Agent receives rescue message.

### **Scenario 3: Agent Working But No New Tasks**
```
T+0:00 - Task assigned → activity updated
T+0:30 - Agent completes task, updates status.json
T+1:00 - Agent creates devlog
T+2:00 - Agent processes inbox
T+3:00 - Agent continues working on related tasks
T+5:00 - Check cycle → time_since = 300s → status = "stalled" ⚠️
```

**Problem:** Agent is working, but no new task assigned, so they appear stalled.

---

## 💡 RECOMMENDATIONS

### **For Better Activity Detection:**

1. **Update Activity on Task Completion:**
   ```python
   def mark_task_completed(self, task_id: str, agent_id: str, duration: float) -> None:
       # ADD THIS:
       self.agent_activity[agent_id] = time.time()  # Update activity on completion
   ```

2. **Check Status.json Modification Times:**
   - Add a method to check `status.json` file modification times
   - Update activity if status.json was modified recently

3. **Check Devlog Creation:**
   - Monitor devlog directory for new files
   - Update activity if agent created a devlog recently

4. **Hybrid Approach:**
   - Combine task assignment tracking with file-based activity detection
   - Agent is active if: new task OR status.json updated OR devlog created

---

## 📝 CONCLUSION

The current system uses a **simple but limited** approach:
- ✅ Simple to implement
- ✅ Low overhead
- ❌ Doesn't detect file-based activity
- ❌ Can have false positives (working agents appear stalled)

**The system is designed for orchestrator-driven task distribution, not file-based activity detection.**

---

**WE. ARE. SWARM. MONITORED. UNDERSTOOD.** 🐝⚡🔥




