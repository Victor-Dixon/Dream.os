# MessagingCommands Extraction Plan - Phase 2
**Date**: 2025-12-13  
**Agent**: Agent-7 (Web Development Specialist)  
**Status**: ⏳ Planning Phase 2 Extraction  
**Target**: `unified_discord_bot.py` MessagingCommands class (1,797 lines)

---

## 📊 Current State

**MessagingCommands Class**:
- **Location**: `unified_discord_bot.py` lines 899-2695
- **Size**: 1,797 lines
- **Commands**: 23 commands identified
- **V2 Status**: ❌ Way over 300 line limit

---

## 🎯 Extraction Strategy

### Command Grouping Analysis

**23 Commands Identified**:

1. **Core Messaging Commands** (5 commands):
   - `gui` - Open messaging GUI
   - `message` - Send message to agent
   - `broadcast` - Broadcast to all agents
   - `status` - View swarm status
   - `monitor` - Control status monitor

2. **System Control Commands** (4 commands):
   - `control/panel/menu` - Open control panel
   - `shutdown` - Shutdown bot
   - `restart` - Restart bot
   - `thea` - Thea session management

3. **Onboarding Commands** (2 commands):
   - `soft_onboard` - Soft onboard agents
   - `hard_onboard` - Hard onboard agents

4. **Utility Commands** (5 commands):
   - `help` - Show help
   - `commands` - List commands
   - `mermaid` - Render Mermaid diagram
   - `git_push` - Push to GitHub
   - `session` - Post session report

5. **Profile Commands** (2 commands):
   - `aria` - Aria profile
   - `carmyn` - Carmyn profile

6. **Agent Management Commands** (2 commands):
   - `unstall` - Unstall agent
   - `heal` - Self-healing system

7. **Placeholder Commands** (3 commands):
   - `obs` - Observations (placeholder)
   - `pieces` - Pieces (placeholder)
   - `sftp` - SFTP credentials guide

---

## 📁 Proposed Module Structure

### Option 1: Grouped by Functionality (Recommended)

```
src/discord_commander/commands/
├── __init__.py
├── core_messaging_commands.py      # gui, message, broadcast, status, monitor
├── system_control_commands.py      # control, shutdown, restart, thea
├── onboarding_commands.py          # soft_onboard, hard_onboard
├── utility_commands.py             # help, commands, mermaid, git_push, session
├── profile_commands.py             # aria, carmyn
├── agent_management_commands.py    # unstall, heal
└── placeholder_commands.py        # obs, pieces, sftp
```

**Estimated Sizes**:
- `core_messaging_commands.py`: ~400-500 lines
- `system_control_commands.py`: ~300-400 lines
- `onboarding_commands.py`: ~300-400 lines
- `utility_commands.py`: ~300-400 lines
- `profile_commands.py`: ~100-150 lines
- `agent_management_commands.py`: ~300-400 lines
- `placeholder_commands.py`: ~150-200 lines

**Total**: ~1,850-2,650 lines (split across 7 files, each <500 lines)

### Option 2: Single Commands Module (Alternative)

Extract entire MessagingCommands class to `messaging_commands.py`:
- **Size**: Still 1,797 lines (over limit)
- **Status**: Not viable - still violates V2

---

## ✅ Recommended Approach: Option 1

**Phase 2A: Extract Core Messaging Commands**
- Extract: `gui`, `message`, `broadcast`, `status`, `monitor`
- Target: `commands/core_messaging_commands.py`
- Estimated: ~400-500 lines

**Phase 2B: Extract System Control Commands**
- Extract: `control`, `shutdown`, `restart`, `thea`
- Target: `commands/system_control_commands.py`
- Estimated: ~300-400 lines

**Phase 2C: Extract Onboarding Commands**
- Extract: `soft_onboard`, `hard_onboard`
- Target: `commands/onboarding_commands.py`
- Estimated: ~300-400 lines

**Phase 2D: Extract Remaining Commands**
- Extract: utility, profile, agent_management, placeholder commands
- Target: Multiple smaller modules
- Estimated: ~600-800 lines total

---

## 🔄 Integration Plan

1. **Create commands/ directory**
2. **Extract command groups** one at a time
3. **Update unified_discord_bot.py** to import and register cogs
4. **Test functionality** after each extraction
5. **Validate** with Agent-8 QA

---

## 📊 Expected Results

**After Phase 2 Complete**:
- `unified_discord_bot.py`: ~900-1,000 lines (reduced by ~1,700 lines)
- `commands/` directory: 7 new command handler modules
- **Total Reduction**: ~1,700 lines from unified_discord_bot.py
- **V2 Compliance**: unified_discord_bot.py still over limit, but significantly reduced

---

## 🚀 Next Steps

1. **Create commands/ directory structure**
2. **Begin Phase 2A**: Extract core messaging commands
3. **Test integration**: Verify bot still works
4. **Continue with Phase 2B-D**: Extract remaining command groups
5. **QA Validation**: Agent-8 validates refactored modules

---

**Status**: ⏳ Planning complete, ready to begin extraction  
**Next**: Create commands/ directory and begin Phase 2A


