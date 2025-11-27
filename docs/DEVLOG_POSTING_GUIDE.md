# 📚 Devlog Posting Guide - SSOT

**Last Updated**: 2025-01-27  
**SSOT**: `tools/devlog_manager.py`  
**Status**: ✅ Active - All agents must use this

---

## 🎯 **SINGLE SOURCE OF TRUTH**

**`tools/devlog_manager.py`** is the **ONLY** script for devlog posting.

**All other scripts are deprecated and archived.**

---

## ✅ **HOW TO POST A DEVLOG**

### **Command**:
```bash
python tools/devlog_manager.py post --agent agent-X --file <devlog_file.md>
```

### **For Major Updates** (User Channel):
```bash
python tools/devlog_manager.py post --agent agent-4 --file <devlog_file.md> --major
```

---

## 📋 **AGENT DEVLOG CHANNELS**

Each agent posts to their dedicated Discord channel:

| Agent | Channel | Webhook Variable |
|-------|---------|------------------|
| Agent-1 | `#agent-1-devlogs` | `DISCORD_WEBHOOK_AGENT_1` |
| Agent-2 | `#agent-2-devlogs` | `DISCORD_WEBHOOK_AGENT_2` |
| Agent-3 | `#agent-3-devlogs` | `DISCORD_WEBHOOK_AGENT_3` |
| Agent-4 (Captain) | `#agent-4-devlogs` or `#captain-devlogs` | `DISCORD_WEBHOOK_AGENT_4` or `DISCORD_CAPTAIN_WEBHOOK` |
| Agent-5 | `#agent-5-devlogs` | `DISCORD_WEBHOOK_AGENT_5` |
| Agent-6 | `#agent-6-devlogs` | `DISCORD_WEBHOOK_AGENT_6` |
| Agent-7 | `#agent-7-devlogs` | `DISCORD_WEBHOOK_AGENT_7` |
| Agent-8 | `#agent-8-devlogs` | `DISCORD_WEBHOOK_AGENT_8` |

**User Channel** (Major Updates Only):
- Channel: User's Discord channel
- Webhook: `DISCORD_WEBHOOK_URL`
- Usage: Only for major milestones (use `--major` flag)

---

## 🔗 **STATUS MONITOR INTEGRATION**

Devlog posts are automatically logged to `logs/devlog_posts.json` for status monitor integration.

**Status Monitor Checks**:
- ✅ Latest devlog post timestamp
- ✅ Agent activity detection
- ✅ Stale agent identification

**If an agent posts a devlog, the status monitor knows the agent is active.**

---

## 📊 **WHAT HAPPENS AUTOMATICALLY**

When you post a devlog:

1. ✅ **Swarm Brain Upload** - Devlog uploaded to `swarm_brain/devlogs/`
2. ✅ **Discord Posting** - Posted to your agent channel
3. ✅ **Status Monitor Log** - Logged to `logs/devlog_posts.json`
4. ✅ **Index Update** - Devlog index updated
5. ✅ **Smart Chunking** - Long messages split automatically
6. ✅ **Mermaid Support** - Diagrams converted to images

---

## ⚠️ **DEPRECATED SCRIPTS**

The following scripts are **DEPRECATED** and **ARCHIVED**:

1. ❌ `tools/devlog_auto_poster.py` → `tools/deprecated/devlog_auto_poster.py.deprecated`
2. ❌ `scripts/post_devlogs_to_discord.py` → `tools/deprecated/post_devlogs_to_discord.py.deprecated`
3. ⚠️ `tools/post_devlog_to_discord.py` → **Wrapper only** (calls devlog_manager.py)
4. ⚠️ `tools/check_and_post_unposted_devlogs.py` → Should be updated to use devlog_manager.py

**Do NOT use deprecated scripts. Use `devlog_manager.py` only.**

---

## 🚨 **CRITICAL RULES**

### **DO**:
- ✅ Use `devlog_manager.py` for ALL devlog posting
- ✅ Use `--agent agent-X` flag (lowercase, with dash)
- ✅ Post to your dedicated channel for routine updates
- ✅ Use `--major` flag for major updates to user channel

### **DON'T**:
- ❌ Use deprecated scripts
- ❌ Post to wrong channel
- ❌ Skip the `--agent` flag
- ❌ Use `post_devlog_to_discord.py` directly (use devlog_manager.py)

---

## 📝 **EXAMPLES**

### **Routine Update** (Agent Channel):
```bash
python tools/devlog_manager.py post --agent agent-1 --file devlogs/2025-01-27_task_complete.md
```
→ Posts to `#agent-1-devlogs`

### **Major Milestone** (User Channel):
```bash
python tools/devlog_manager.py post --agent agent-4 --file devlogs/2025-01-27_phase1_complete.md --major
```
→ Posts to user's Discord channel

### **Captain Routine Update**:
```bash
python tools/devlog_manager.py post --agent agent-4 --file agent_workspaces/Agent-4/status_update.md
```
→ Posts to `#agent-4-devlogs` or `#captain-devlogs`

---

## 🔧 **TROUBLESHOOTING**

### **Error: No Discord webhook configured**
- Check environment variable: `DISCORD_WEBHOOK_AGENT_X`
- Verify webhook URL is correct
- Ensure webhook is for the correct channel

### **Error: File not found**
- Use absolute or relative path
- Ensure file exists
- Check file permissions

### **Error: Agent not recognized**
- Use format: `agent-1`, `agent-2`, etc. (lowercase, with dash)
- Or: `Agent-1`, `Agent-2`, etc. (capitalized, with dash)

---

## 🐝 **WE. ARE. SWARM.**

**SSOT**: `tools/devlog_manager.py` - Use this for all devlog posting!

**Status Monitor**: Automatically tracks devlog posts for agent activity detection.

**Clean House**: All deprecated scripts archived. No confusion. Clear pattern.

---

**Generated**: 2025-01-27  
**Captain Agent-4** - Strategic Oversight

