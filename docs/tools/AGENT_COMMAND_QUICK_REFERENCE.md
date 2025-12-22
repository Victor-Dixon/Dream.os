# 🎯 Agent Command Quick Reference

**Tool**: `python -m src.services.messaging_cli`  
**Purpose**: Command agents to do everything through the unified messaging system

---

## 🚀 **BASIC COMMANDS**

### **Send Message to Specific Agent**
```bash
python -m src.services.messaging_cli --message "Your task here" --agent Agent-1
```

### **Broadcast to All Agents**
```bash
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
```

### **Send with Priority**
```bash
python -m src.services.messaging_cli --message "URGENT: Fix issue" \
    --agent Agent-2 --priority urgent
```

---

## 📋 **COMMON USE CASES**

### **1. Assign Tasks to Agents**
```bash
# Single agent
python -m src.services.messaging_cli -m "Track file deletion progress" -a Agent-6

# Multiple agents (send individually)
python -m src.services.messaging_cli -m "Complete investigation report" -a Agent-1
python -m src.services.messaging_cli -m "Complete investigation report" -a Agent-2
```

### **2. Broadcast Swarm-Wide Commands**
```bash
# Urgent swarm alert
python -m src.services.messaging_cli -m "URGENT: System update required" \
    --broadcast --priority urgent

# Normal coordination message
python -m src.services.messaging_cli -m "Check inbox for new assignments" --broadcast
```

### **3. Task Management**
```bash
# Get next task for agent
python -m src.services.messaging_cli --get-next-task --agent Agent-7

# List all tasks
python -m src.services.messaging_cli --list-tasks

# Check task status
python -m src.services.messaging_cli --task-status TASK_ID

# Complete task
python -m src.services.messaging_cli --complete-task TASK_ID
```

### **4. Agent Onboarding**
```bash
# Hard onboarding (5-step reset)
python -m src.services.messaging_cli --hard-onboarding --agent Agent-6 --role "Coordination Specialist"

# Onboarding with custom file
python -m src.services.messaging_cli --hard-onboarding \
    --agent Agent-7 \
    --onboarding-file path/to/onboarding_message.md
```

### **5. Start Agents**
```bash
# Start specific agents (sends to onboarding coordinates)
python -m src.services.messaging_cli --start 1 2 3

# Start all agents
python -m src.services.messaging_cli --start 1 2 3 4 5 6 7 8
```

---

## 🎯 **ADVANCED FEATURES**

### **Message Tags**
```bash
# Categorize messages with tags
python -m src.services.messaging_cli -m "File deletion investigation" \
    -a Agent-1 --tags captain file-deletion investigation
```

### **Priority Levels**
- `normal` / `regular` - Default priority
- `urgent` - High priority, requires immediate attention

### **Coordination Modes**
```bash
# Survey coordination
python -m src.services.messaging_cli --survey-coordination

# Consolidation coordination
python -m src.services.messaging_cli --consolidation-coordination

# Consolidation batch
python -m src.services.messaging_cli --consolidation-batch BATCH_ID

# Consolidation status
python -m src.services.messaging_cli --consolidation-status "Phase 1 complete"
```

### **Utility Commands**
```bash
# Display agent coordinates
python -m src.services.messaging_cli --coordinates

# Display leaderboard
python -m src.services.messaging_cli --leaderboard

# Save message to all agents (Ctrl+Enter)
python -m src.services.messaging_cli --save
```

---

## 📝 **EXAMPLES FOR COORDINATION**

### **File Deletion Investigation**
```bash
# Assign to Agent-1
python -m src.services.messaging_cli -m "Investigate core systems files (5 files)" -a Agent-1

# Assign to Agent-2
python -m src.services.messaging_cli -m "Investigate architecture files (4 files)" -a Agent-2

# Assign to Agent-3
python -m src.services.messaging_cli -m "Investigate infrastructure files (3 files)" -a Agent-3

# Assign to Agent-7
python -m src.services.messaging_cli -m "Investigate application files (2 files)" -a Agent-7

# Assign to Agent-8
python -m src.services.messaging_cli -m "Investigate duplicates and SSOT violations (54 files)" -a Agent-8
```

### **Website Fixes**
```bash
# Assign website fixes to Agent-7
python -m src.services.messaging_cli -m "Fix critical website issues: prismblossom.online (2 fixes), FreeRideInvestor (2 fixes)" -a Agent-7 --priority urgent
```

### **WordPress Deployer**
```bash
# Assign WordPress deployer fixes to Agent-7
python -m src.services.messaging_cli -m "Fix WordPress deployer credential loading and enhance error messages" -a Agent-7
```

### **Swarm Coordination**
```bash
# Coordinate swarm-wide
python -m src.services.messaging_cli -m "Track file deletion progress, update session summary, maintain swarm coordination" -a Agent-6 --priority urgent
```

---

## 🔧 **TECHNICAL DETAILS**

### **Delivery Modes**
- **Default**: Inbox mode (file-based messaging)
- **PyAutoGUI**: Use `--pyautogui` flag for GUI automation

### **Message Format**
Messages are delivered to agent inboxes at:
```
agent_workspaces/{Agent-X}/inbox/
```

### **Message Structure**
- **From**: Sender (default: "Captain Agent-4")
- **To**: Recipient agent
- **Priority**: normal/regular/urgent
- **Tags**: Categorization tags
- **Content**: Message body

---

## 🚨 **BEST PRACTICES**

1. **Be Specific**: Include clear task descriptions
2. **Use Priorities**: Mark urgent tasks appropriately
3. **Tag Messages**: Use tags for categorization
4. **Follow Up**: Check agent status after assignments
5. **Coordinate**: Use broadcast for swarm-wide coordination

---

## 📚 **RELATED TOOLS**

- **Captain Tools**: `tools/categories/captain_tools*.py`
- **Agent Toolbelt**: `python -m tools.toolbelt`
- **Discord Commander**: Discord bot for agent commands
- **Agent Check-in**: `tools/agent_checkin.py`

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Use this tool to command agents and coordinate the swarm!*



