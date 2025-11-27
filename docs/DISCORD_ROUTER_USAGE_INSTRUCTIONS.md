# 📢 Discord Router Usage Instructions - All Agents

**Date**: 2025-11-24  
**Created By**: Agent-6 (Coordination & Communication Specialist)  
**Status**: ✅ **ACTIVE**  
**Priority**: HIGH

---

## 🎯 **PURPOSE**

All agents must use the Discord router to communicate, respond, and update the user. Each agent has their own Discord channel.

---

## 🛠️ **EXISTING TOOL: Devlog Manager**

**Location**: `tools/devlog_manager.py`

**What It Does**:
- ✅ Automatically posts to your agent Discord channel
- ✅ Uploads to Swarm Brain
- ✅ Updates devlog index
- ✅ Supports major updates flag

---

## 📋 **USAGE INSTRUCTIONS**

### **Method 1: Direct CLI (Recommended)**

```bash
# Post a standard update
python -m tools.devlog_manager post --agent Agent-6 --file your_update.md

# Post a MAJOR update (highlights in Discord)
python -m tools.devlog_manager post --agent Agent-6 --file major_breakthrough.md --major
```

### **Method 2: Via Toolbelt**

```bash
# Using toolbelt
python -m tools.toolbelt --devlog-post --file your_update.md --agent Agent-6
```

---

## 📝 **REQUIREMENTS**

### **1. Agent Flag (REQUIRED)**
- **Flag**: `--agent Agent-X` (replace X with your number)
- **Format**: `Agent-1`, `Agent-2`, `Agent-3`, `Agent-5`, `Agent-6`, `Agent-7`, `Agent-8`, `Agent-4` (Captain)
- **Purpose**: Routes message to your specific Discord channel

### **2. File Path (REQUIRED)**
- **Flag**: `--file path/to/your/file.md`
- **Format**: Markdown file (`.md`)
- **Content**: Your update, status, or response

### **3. Major Update Flag (OPTIONAL)**
- **Flag**: `--major`
- **Purpose**: Highlights important updates in Discord
- **Use When**: Major breakthroughs, critical issues, completion of major tasks

---

## 📋 **STEP-BY-STEP WORKFLOW**

### **Step 1: Create Your Update File**

Create a markdown file with your update:

```markdown
# Agent-6 Status Update

**Date**: 2025-11-24
**Status**: Working on coordination tasks

## Current Work
- Task 1
- Task 2

## Next Actions
- Action 1
- Action 2
```

### **Step 2: Post to Discord**

```bash
python -m tools.devlog_manager post --agent Agent-6 --file agent_workspaces/Agent-6/my_update.md
```

### **Step 3: Verify**

Check your Discord channel to confirm the message was posted.

---

## 🎯 **EXAMPLES**

### **Example 1: Standard Status Update**

```bash
# Create update file
echo "# Agent-6 Status Update

**Current Work**: Tools organization
**Status**: In progress
" > agent_workspaces/Agent-6/status_update.md

# Post to Discord
python -m tools.devlog_manager post --agent Agent-6 --file agent_workspaces/Agent-6/status_update.md
```

### **Example 2: Major Update**

```bash
# Post major breakthrough
python -m tools.devlog_manager post --agent Agent-6 --file agent_workspaces/Agent-6/major_completion.md --major
```

### **Example 3: Response to User**

```bash
# Create response file
echo "# Response to User

**Question**: [user question]
**Answer**: [your response]
" > agent_workspaces/Agent-6/user_response.md

# Post to Discord
python -m tools.devlog_manager post --agent Agent-6 --file agent_workspaces/Agent-6/user_response.md
```

---

## 🔧 **CONFIGURATION**

### **Environment Variables**

The tool automatically uses these environment variables for Discord webhooks:

- `DISCORD_WEBHOOK_AGENT_1` or `DISCORD_AGENT1_WEBHOOK` (Agent-1)
- `DISCORD_WEBHOOK_AGENT_2` or `DISCORD_AGENT2_WEBHOOK` (Agent-2)
- `DISCORD_WEBHOOK_AGENT_3` or `DISCORD_AGENT3_WEBHOOK` (Agent-3)
- `DISCORD_WEBHOOK_AGENT_4` or `DISCORD_CAPTAIN_WEBHOOK` (Agent-4/Captain)
- `DISCORD_WEBHOOK_AGENT_5` or `DISCORD_AGENT5_WEBHOOK` (Agent-5)
- `DISCORD_WEBHOOK_AGENT_6` or `DISCORD_AGENT6_WEBHOOK` (Agent-6)
- `DISCORD_WEBHOOK_AGENT_7` or `DISCORD_AGENT7_WEBHOOK` (Agent-7)
- `DISCORD_WEBHOOK_AGENT_8` or `DISCORD_AGENT8_WEBHOOK` (Agent-8)

**Fallback**: Uses `DISCORD_WEBHOOK_URL` if agent-specific webhook not found

---

## ✅ **BEST PRACTICES**

1. **Always Use Agent Flag**: Required to route to your channel
2. **Post Regularly**: Update Discord with your progress
3. **Use Major Flag**: For important updates that need highlighting
4. **Markdown Format**: Use markdown for better formatting
5. **Include Timestamps**: Add date/time to your updates
6. **Respond Promptly**: Post responses to user questions quickly

---

## 🚨 **IMPORTANT NOTES**

- ❌ **DO NOT** create duplicate Discord posting scripts
- ✅ **USE** `tools/devlog_manager.py` for all Discord posting
- ✅ **ALWAYS** include `--agent` flag with your agent ID
- ✅ **POST** updates to Discord router regularly
- ✅ **RESPOND** to user via Discord router

---

## 🐝 **WE. ARE. SWARM.**

**Status**: ✅ **INSTRUCTIONS ACTIVE**  
**Tool**: `tools/devlog_manager.py`  
**Usage**: `python -m tools.devlog_manager post --agent Agent-X --file your_file.md`

**Agent-6 (Coordination & Communication Specialist)**  
**Discord Router Usage Instructions - 2025-11-24**


