# 🏥 Discord Commands - Self-Healing System

**Added:** 2025-01-27  
**Author:** Agent-3

---

## 📋 AVAILABLE COMMANDS

### **`!heal status`** - View Healing Statistics
Shows overall healing system statistics:
- Total healing actions
- Success rate
- Terminal cancellation counts (today)
- Recent healing actions

**Usage:**
```
!heal status
```

**Example Output:**
```
🏥 Self-Healing System Status

📊 Overall Statistics
Total Actions: 15
Success Rate: 93.3%
Successful: 14
Failed: 1

🛑 Terminal Cancellations (Today)
Agent-3: 2
Agent-7: 1

🔄 Recent Actions
✅ Agent-3: cancel_terminal
✅ Agent-7: rescue
✅ Agent-1: reset
```

---

### **`!heal check`** - Immediately Heal Stalled Agents
Triggers immediate healing check for all agents and displays results.

**Usage:**
```
!heal check
```

**Example Output:**
```
🏥 Healing Check Results

📊 Results
Stalled Agents Found: 2
Agents Healed: 2
Agents Failed: 0

✅ Successfully Healed
Agent-3, Agent-7
```

---

### **`!heal cancel_count [Agent-X]`** - View Terminal Cancellations
Shows terminal cancellation count for specific agent or all agents.

**Usage:**
```
!heal cancel_count          # All agents
!heal cancel_count Agent-3  # Specific agent
```

**Example Output:**
```
🛑 Terminal Cancellations - Agent-3

Today: 2 cancellation(s)
```

---

### **`!heal agent Agent-X`** - Agent-Specific Stats
Shows detailed healing statistics for a specific agent.

**Usage:**
```
!heal agent Agent-3
```

**Example Output:**
```
🏥 Agent Healing Stats - Agent-3

📊 Healing Actions
Total: 5
Successful: 5
Failed: 0

🛑 Terminal Cancellations
Today: 2
```

---

## 🔄 COMPARISON: `!heal` vs `!unstall`

### **`!heal`** - Self-Healing System
- **Automatic:** Runs continuously in background
- **Progressive:** 5min → 8min → 10min recovery
- **Comprehensive:** Terminal cancellation, rescue, reset, hard onboard
- **Statistics:** Full tracking and history
- **Usage:** `!heal [status|check|cancel_count|agent]`

### **`!unstall`** - Manual Recovery
- **Manual:** Triggered by user command
- **Simple:** Sends continuation message
- **Quick:** Immediate action
- **Usage:** `!unstall Agent-X`

**When to use:**
- **`!heal`**: Check system status, view statistics, trigger manual healing check
- **`!unstall`**: Quick manual recovery for a specific agent you know is stalled

---

## 📊 COMMAND SUMMARY

| Command | Description | Example |
|---------|-------------|---------|
| `!heal status` | Show healing statistics | `!heal status` |
| `!heal check` | Immediately heal all stalled agents | `!heal check` |
| `!heal cancel_count` | Show terminal cancellations (all agents) | `!heal cancel_count` |
| `!heal cancel_count Agent-3` | Show cancellations for specific agent | `!heal cancel_count Agent-3` |
| `!heal agent Agent-3` | Show detailed stats for agent | `!heal agent Agent-3` |

---

## 🎯 WORKFLOW EXAMPLES

### **Check System Health:**
```
!heal status
```

### **Trigger Immediate Healing:**
```
!heal check
```

### **Check Terminal Cancellations:**
```
!heal cancel_count
```

### **Investigate Specific Agent:**
```
!heal agent Agent-3
!heal cancel_count Agent-3
```

---

## ✅ STATUS

**Command Added:** ✅  
**Syntax Verified:** ✅  
**Ready for Use:** ✅

The `!heal` command is now available in Discord for managing the self-healing system!

