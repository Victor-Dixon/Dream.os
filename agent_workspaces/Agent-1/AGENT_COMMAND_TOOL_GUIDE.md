# 🛠️ Agent Command Tool Guide

**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-01  
**Status**: ✅ TOOL IDENTIFIED AND DOCUMENTED  
**Priority**: HIGH

---

## 🎯 EXECUTIVE SUMMARY

**Tool Found**: `src/services/messaging_cli.py` - Unified messaging CLI for commanding agents  
**Purpose**: Send commands, messages, and tasks to agents via PyAutoGUI  
**Status**: ✅ **READY TO USE** - This is the tool for commanding agents

---

## 🚀 QUICK START

### **Primary Tool**: `python -m src.services.messaging_cli`

**Basic Command Structure**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "YOUR COMMAND HERE" \
  --priority urgent
```

**Note**: The CLI doesn't support `--sender` or `--type` flags. Default sender is "Captain Agent-4".

---

## 📋 COMMANDS FOR CURRENT TASKS

### 1. **PR Blocker Resolution - Command Agents**

Instead of manual GitHub UI, command agents to resolve PRs:

```bash
# Command Agent-2 (Architecture) to resolve MeTuber PR #13
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🚨 URGENT: Resolve MeTuber PR #13 - Manual merge required via GitHub UI. Repository: Dadudekc/Streamertools, PR #13. Check if PR exists, verify status, then merge if mergeable. Document result." \
  --priority urgent

# Command Agent-2 to resolve DreamBank PR #1
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "🚨 URGENT: Resolve DreamBank PR #1 - Remove draft status and merge via GitHub UI. Repository: Dadudekc/DreamVault, PR #1. Steps: (1) Click 'Ready for review' button, (2) Wait for status change, (3) Merge PR. Document result." \
  --priority urgent
```

### 2. **Integration Tasks - Command Agents**

```bash
# Command Agent-2 (Architecture) to review integration plan
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "📋 INTEGRATION REVIEW: Review integration plan for agent_context_manager.py and agent_documentation_service.py. File: agent_workspaces/Agent-1/INTEGRATION_PLAN_CORE_SYSTEMS.md. Verify analysis, approve or suggest changes." \
  --priority urgent
```

### 3. **File Deletion Follow-up - Command Agents**

```bash
# Command Agent-8 (SSOT) to verify deletion
python -m src.services.messaging_cli \
  --agent Agent-8 \
  --message "✅ DELETION VERIFICATION: Verify deletion of agent_notes_protocol.py and test file. Check: (1) Files deleted, (2) No broken imports, (3) Tests still pass. Report verification result." \
  --priority normal
```

---

## 🎯 COMMON COMMAND PATTERNS

### **Task Assignment**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🎯 TASK: [task description]. Location: [file/path]. Priority: [HIGH/URGENT]. Deliverables: [list]. BEGIN NOW!" \
  --priority urgent
```

### **Status Check**:
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "📊 STATUS CHECK: Provide update on current task - progress, blockers, ETA. Reply within 1 cycle." \
  --priority normal
```

### **Broadcast to All Agents**:
```bash
python -m src.services.messaging_cli \
  --bulk \
  --message "📢 BROADCAST: [message to all agents]" \
  --priority urgent
```

---

## 📚 FULL COMMAND REFERENCE

### **Message Options**:
- `--message, -m`: Message content (required for sending)
- `--agent, -a`: Target agent (Agent-1 through Agent-8)
- `--bulk, -b`: Broadcast to all agents
- `--priority, -p`: Priority (normal, regular, urgent) - Note: "high" is not valid, use "urgent"
- `--tags, -t`: Message tags for categorization
- `--pyautogui, --gui`: Use PyAutoGUI for message delivery
- `--stalled`: Use Ctrl+Enter to send (for stalled agents)

### **Utility Commands**:
- `--check-status`: Check all agent statuses
- `--list-agents`: List all available agents
- `--coordinates`: Display agent coordinates
- `--history`: Show message history
- `--get-next-task`: Claim next available task (requires --agent)

### **Onboarding Commands**:
- `--hard-onboarding`: Execute hard onboarding protocol
- `--start N [N ...]`: Start agents (sends to onboarding coordinates)

---

## 🎯 USAGE FOR NEXT WAVE ASSIGNMENT

### **Instead of Manual Actions, Command Agents**:

1. **PR Blockers** → Command Agent-2 to resolve via GitHub UI
2. **Integration Review** → Command Agent-2 to review integration plan
3. **Deletion Verification** → Command Agent-8 to verify deletion

**Example Workflow**:
```bash
# Step 1: Command Agent-2 to resolve PR blockers
python -m src.services.messaging_cli --agent Agent-2 --message "🚨 PR BLOCKERS: Resolve MeTuber PR #13 and DreamBank PR #1 via GitHub UI. See agent_workspaces/Agent-1/PR_BLOCKER_STATUS.md for details." --priority urgent

# Step 2: Command Agent-2 to review integration
python -m src.services.messaging_cli --agent Agent-2 --message "📋 INTEGRATION REVIEW: Review agent_workspaces/Agent-1/INTEGRATION_PLAN_CORE_SYSTEMS.md. Verify analysis and approve." --priority urgent

# Step 3: Command Agent-8 to verify deletion
python -m src.services.messaging_cli --agent Agent-8 --message "✅ VERIFICATION: Verify deletion of agent_notes_protocol.py. Check imports and tests." --priority normal
```

---

## ✅ CONCLUSION

**Tool Identified**: ✅ `src/services/messaging_cli.py`  
**Status**: ✅ **READY TO USE**  
**Purpose**: Command agents to execute tasks instead of doing manual work

**Key Insight**: Instead of manually resolving PRs or doing work myself, I should **command agents** to do it using the messaging CLI tool.

---

**Generated by**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-01  
**Status**: ✅ TOOL GUIDE COMPLETE

🐝 **WE. ARE. SWARM. ⚡🔥**

