# 📢 Discord Communication Pattern - Updated Guidelines

**Date**: 2025-01-27  
**Created By**: Agent-4 (Captain)  
**Status**: ✅ **COMMUNICATION PATTERN UPDATED**  
**Priority**: HIGH

---

## 🎯 **USER CLARIFICATION**

**User Statement**: "All agents have a discord channel that they can post in. I thought the discord router was for that. The post yall have been using should be for major updates to me."

---

## 📢 **DISCORD COMMUNICATION PATTERN**

### **Agent Channels**:
- ✅ **Each agent has their own Discord channel**
- ✅ **Agents can post to their own channels**
- ✅ **Discord router (`devlog_manager.py`) is for agent-to-channel posting**

### **Major Updates**:
- ✅ **`devlog_manager.py --major`** is for **major updates to the user**
- ✅ **Not for routine agent communications**
- ✅ **Reserved for significant milestones and updates**

---

## 🛠️ **TOOLS**

### **Discord Router** (`tools/devlog_manager.py`):
- **Purpose**: Post routine communications to agent's own Discord channel
- **Usage**: `python -m tools.devlog_manager post --agent Agent-X --file your_file.md`
- **When to Use**: Routine updates, status reports, progress updates, coordination messages

### **Major Updates** (`tools/post_devlog_to_discord.py`):
- **Purpose**: Post major updates directly to the user
- **Usage**: `python tools/post_devlog_to_discord.py your_file.md`
- **When to Use**: Major milestones, phase completions, critical achievements, user-requested updates

---

## 📋 **COMMUNICATION GUIDELINES**

### **Use Discord Router** (`devlog_manager.py` with `--agent`):
- ✅ Routine agent communications
- ✅ Status updates
- ✅ Progress reports
- ✅ Coordination messages
- ✅ Daily/weekly updates
- ✅ Task completions
- ✅ Response to other agents

### **Use Major Updates** (`post_devlog_to_discord.py`):
- ✅ Major milestones (e.g., "Phase 1 100% ready")
- ✅ Phase completions
- ✅ Critical achievements
- ✅ User-requested updates
- ✅ Significant system changes
- ✅ Major blocker resolutions

---

## 🎯 **EXAMPLES**

### **Discord Router** (Agent Channel):
```bash
# Agent-7 posts routine update to their channel
python -m tools.devlog_manager post --agent Agent-7 --file devlogs/2025-01-27_agent7_testing_update.md

# Agent-1 posts status update to their channel
python -m tools.devlog_manager post --agent Agent-1 --file agent_workspaces/Agent-1/status_update.md
```

### **Major Updates** (User Channel):
```bash
# Captain posts major milestone to user
python tools/devlog_manager.py post --agent agent-4 --file devlogs/2025-01-27_phase1_unblocked_final_confirmation.md --major
```

---

## 📝 **WORKFLOW**

### **For Routine Communications**:
1. **Create Devlog**: Create devlog in `devlogs/` or agent workspace
2. **Post to Agent Channel**: Use `devlog_manager.py` with `--agent Agent-X`
3. **Update Status**: Update agent status and coordination documents

### **For Major Updates**:
1. **Create Devlog**: Create devlog in `devlogs/` directory
2. **Post to User**: Use `post_devlog_to_discord.py` for major updates
3. **Reserve for**: Significant milestones, critical achievements

---

## ✅ **CORRECTED PATTERN**

### **Before (Incorrect)**:
- ❌ Using `post_devlog_to_discord.py` for all communications
- ❌ Posting routine updates to user channel
- ❌ Not using agent channels

### **After (Correct)**:
- ✅ Using `devlog_manager.py` with `--agent` for routine communications
- ✅ Posting to agent's own Discord channel
- ✅ Using `post_devlog_to_discord.py` only for major updates to user

---

## 🎯 **AGENT INSTRUCTIONS**

### **All Agents**:
1. **Routine Communications**: Use `devlog_manager.py` with `--agent Agent-X` to post to your channel
2. **Major Updates**: Use `post_devlog_to_discord.py` for user updates
3. **Follow Pattern**: Maintain consistent communication pattern

### **Agent IDs**:
- `Agent-1` through `Agent-8`
- `Agent-4` is Captain

---

## ✅ **AGENT CONFIRMATION**

### **Agent-7 Confirmation** (2025-01-27):
- ✅ **Pattern Understood**: Agent-7 has confirmed understanding of communication pattern
- ✅ **Correct Usage**: Will use `devlog_manager.py` with `--agent Agent-7` for routine devlogs (posts to Agent-7 channel)
- ✅ **Major Updates**: Will use `post_devlog_to_discord.py` for major updates to user
- ✅ **Status**: Pattern corrected and internalized

---

**Status**: ✅ **COMMUNICATION PATTERN UPDATED & CONFIRMED**

**Discord router (`devlog_manager.py`) is for agent-to-channel posting. Use `--major` flag for major updates to the user. Communication pattern corrected and confirmed by Agent-7!**

**🐝 WE. ARE. SWARM. ⚡🔥**

