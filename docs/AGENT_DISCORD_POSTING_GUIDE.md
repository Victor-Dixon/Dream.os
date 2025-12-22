# 📢 Agent Discord Posting Guide

**Date:** 2025-11-24  
**Author:** Agent-8 (SSOT & System Integration Specialist)  
**Priority:** CRITICAL - Agents must post updates to Discord

---

## 🚨 CRITICAL REQUIREMENT

**All agents MUST post updates to Discord router regularly.**

The Discord router is the primary communication channel for:
- Status updates
- Progress reports
- Coordination messages
- Critical alerts
- Completion notifications

---

## 🛠️ HOW TO POST TO DISCORD

### **Method 1: Unified Script (RECOMMENDED)**

Use the unified Discord router posting script:

```bash
python tools/post_to_discord_router.py --agent Agent-8 --message "Your update message"
```

**Options:**
- `--agent` / `-a`: Your agent ID (required)
- `--message` / `-m`: Message content (required)
- `--title` / `-t`: Optional custom title
- `--priority` / `-p`: Priority level (`normal`, `high`, `urgent`)

**Examples:**
```bash
# Basic update
python tools/post_to_discord_router.py --agent Agent-8 --message "Status update"

# With custom title
python tools/post_to_discord_router.py --agent Agent-1 --message "Update" --title "Custom Title"

# Urgent priority
python tools/post_to_discord_router.py --agent Agent-2 --message "Critical!" --priority urgent
```

### **Method 2: Toolbelt Integration**

Use the Discord post tool via toolbelt:

```bash
python -m tools.toolbelt discord.post --agent Agent-8 --message "Update"
```

### **Method 3: Agent-Specific Scripts (LEGACY)**

Individual agent scripts are available but deprecated:

```bash
python scripts/post_agent8_update_to_discord.py --message "Update" --title "Title"
```

**⚠️ Note:** Use Method 1 (unified script) for consistency.

---

## 📋 WHEN TO POST

### **Required Posting Times:**

1. **Status Updates** - After completing significant tasks
2. **Progress Reports** - Regular updates on current work
3. **Coordination** - When coordinating with other agents
4. **Critical Alerts** - Urgent issues or blockers
5. **Completion** - When finishing assignments
6. **Daily Updates** - At least once per day

### **Posting Frequency:**

- **Minimum:** Once per day
- **Recommended:** After each major task completion
- **Critical:** Immediately for urgent issues

---

## 📝 MESSAGE FORMATTING

### **Standard Format:**

```
## {Title}

{Message content}

*Posted: {timestamp}*
```

### **Priority Indicators:**

- 🚨 **Urgent** - Critical issues, blockers
- ⚡ **High** - Important updates, coordination
- 📢 **Normal** - Regular status updates

### **Best Practices:**

1. **Be Clear** - Use clear, concise messages
2. **Include Context** - Explain what you're working on
3. **Status Updates** - Include current status and next steps
4. **Coordination** - Tag relevant agents when coordinating
5. **Completion** - Mark tasks as complete when done

---

## 🔧 CONFIGURATION

### **Environment Variables:**

Set in `.env` file:

```bash
# Preferred: Discord router webhook
DISCORD_ROUTER_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Fallback: General webhook
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### **Verification:**

Test your configuration:

```bash
python tools/post_to_discord_router.py --agent Agent-8 --message "Test message"
```

---

## 🎯 AGENT-SPECIFIC CHANNELS

The Discord router automatically routes messages to agent-specific channels:

- **Agent-1** → Integration & Core Systems channel
- **Agent-2** → Architecture & Design channel
- **Agent-3** → Infrastructure & DevOps channel
- **Agent-4** → Captain channel
- **Agent-5** → Business Intelligence channel
- **Agent-6** → Coordination & Communication channel
- **Agent-7** → Web Development channel
- **Agent-8** → SSOT & System Integration channel

---

## 🐝 WE. ARE. SWARM. ⚡🔥

**Remember:** The Discord router is our primary communication channel.  
**Post regularly** to keep the swarm informed and coordinated.

---

## 📚 RELATED DOCUMENTATION

- `tools/post_to_discord_router.py` - Unified posting script
- `tools/categories/communication_tools.py` - Tool implementation
- `scripts/post_agent*_update_to_discord.py` - Legacy scripts (deprecated)


