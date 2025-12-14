# Agent-7 Phase 2: MessagingCommands Extraction Architecture Guidance
**Date**: 2025-12-14  
**Coordinated By**: Agent-2  
**Status**: Architecture Review & Guidance

---

## 📋 Current Status

**Phase 1 Complete** ✅:
- UI components extracted: ConfirmShutdownView, ConfirmRestartView
- File reduced: 2,764 → 2,695 lines (-69 lines, 2.5% reduction)

**Phase 2 Starting**:
- MessagingCommands class: 1,797 lines (lines 899-2695)
- 24+ commands identified
- Target: Extract into separate command handler modules

---

## 🏗️ Architecture Pattern

### Existing Pattern in Codebase

The codebase already follows a pattern of extracting command groups into separate files:

**Existing Command Files**:
- `tools_commands.py` - Tools/toolbelt commands
- `trading_commands.py` - Trading-related commands
- `music_commands.py` - Music commands
- `file_share_commands.py` - File sharing commands
- `approval_commands.py` - Approval workflow commands
- `systems_inventory_commands.py` - Systems inventory commands
- `swarm_showcase_commands.py` - Swarm showcase commands
- `webhook_commands.py` - Webhook commands

**Pattern Structure**:
```python
# Example: tools_commands.py pattern
class ToolsCommands(commands.Cog):
    """Discord commands for [domain]."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    @commands.command(name="command_name")
    async def command_method(self, ctx: commands.Context, ...):
        """Command implementation."""
        pass
```

---

## 🎯 Recommended Extraction Strategy

### Command Grouping Strategy

Group the 24+ commands into logical modules based on functionality:

#### **1. Core System Commands** (`core_system_commands.py`)
**Commands** (6-8 commands):
- `thea` - Thea session management
- `status` - System status
- `monitor` - Monitoring commands
- `control_panel` - Main control panel
- `gui` - GUI interface
- `help_cmd` - Help command
- `list_commands` - List all commands

**Estimated Size**: ~400-500 lines  
**V2 Compliance**: ✅ (<300 lines per module after extraction)

#### **2. Messaging Commands** (`agent_messaging_commands.py`)
**Commands** (4-5 commands):
- `message` - Send message to agent
- `broadcast` - Broadcast to all agents
- `mermaid` - Mermaid diagram rendering

**Estimated Size**: ~300-400 lines  
**V2 Compliance**: ✅ (<300 lines per module)

#### **3. Profile Commands** (`profile_commands.py`)
**Commands** (2 commands):
- `aria_profile` - Aria profile
- `carmyn_profile` - Carmyn profile

**Estimated Size**: ~150-200 lines  
**V2 Compliance**: ✅ (<300 lines)

#### **4. System Control Commands** (`system_control_commands.py`)
**Commands** (2 commands):
- `shutdown_cmd` - Shutdown system
- `restart_cmd` - Restart system

**Estimated Size**: ~200-250 lines  
**V2 Compliance**: ✅ (<300 lines)

#### **5. Onboarding Commands** (`onboarding_commands.py`)
**Commands** (2 commands):
- `soft_onboard` - Soft onboarding
- `hard_onboard` - Hard onboarding

**Estimated Size**: ~400-500 lines  
**V2 Compliance**: ⚠️ (May need further splitting)

#### **6. Git Commands** (`git_commands.py`)
**Commands** (1 command):
- `git_push` - Git push operations

**Estimated Size**: ~200-250 lines  
**V2 Compliance**: ✅ (<300 lines)

#### **7. Agent Management Commands** (`agent_management_commands.py`)
**Commands** (3-4 commands):
- `unstall` - Unstall agent
- `heal` - Agent healing
- `session` - Session management

**Estimated Size**: ~400-500 lines  
**V2 Compliance**: ⚠️ (May need further splitting)

#### **8. Integration Commands** (`integration_commands.py`)
**Commands** (3-4 commands):
- `obs` - OBS integration
- `pieces` - Pieces integration
- `sftp` - SFTP integration

**Estimated Size**: ~300-400 lines  
**V2 Compliance**: ✅ (<300 lines per module)

---

## 📐 Module Organization

### Directory Structure

```
src/discord_commander/
├── unified_discord_bot.py (reduced to ~900 lines)
├── commands/
│   ├── __init__.py
│   ├── core_system_commands.py
│   ├── agent_messaging_commands.py
│   ├── profile_commands.py
│   ├── system_control_commands.py
│   ├── onboarding_commands.py
│   ├── git_commands.py
│   ├── agent_management_commands.py
│   └── integration_commands.py
└── ...
```

### Import Pattern

**In `unified_discord_bot.py`**:
```python
from src.discord_commander.commands.core_system_commands import CoreSystemCommands
from src.discord_commander.commands.agent_messaging_commands import AgentMessagingCommands
from src.discord_commander.commands.profile_commands import ProfileCommands
from src.discord_commander.commands.system_control_commands import SystemControlCommands
from src.discord_commander.commands.onboarding_commands import OnboardingCommands
from src.discord_commander.commands.git_commands import GitCommands
from src.discord_commander.commands.agent_management_commands import AgentManagementCommands
from src.discord_commander.commands.integration_commands import IntegrationCommands

# In setup_hook or __init__:
async def setup_hook(self):
    # ... existing setup ...
    
    # Register command cogs
    await self.add_cog(CoreSystemCommands(self, self.gui_controller))
    await self.add_cog(AgentMessagingCommands(self, self.gui_controller))
    await self.add_cog(ProfileCommands(self, self.gui_controller))
    await self.add_cog(SystemControlCommands(self, self.gui_controller))
    await self.add_cog(OnboardingCommands(self, self.gui_controller))
    await self.add_cog(GitCommands(self, self.gui_controller))
    await self.add_cog(AgentManagementCommands(self, self.gui_controller))
    await self.add_cog(IntegrationCommands(self, self.gui_controller))
```

---

## ✅ V2 Compliance Validation

### Target Metrics

**Before Extraction**:
- `unified_discord_bot.py`: 2,695 lines ❌ (2,395 over limit)

**After Extraction**:
- `unified_discord_bot.py`: ~900 lines ✅ (<300 lines per logical section)
- Each command module: <300 lines ✅
- Total reduction: ~1,795 lines extracted

### Module Size Validation

If any module exceeds 300 lines:
1. **Further split by sub-functionality** (e.g., split onboarding into `soft_onboarding_commands.py` and `hard_onboarding_commands.py`)
2. **Extract shared utilities** into `commands/utils/` directory
3. **Extract view classes** into `views/` directory (already done for UI components)

---

## 🔧 Implementation Steps

### Step 1: Create Commands Directory Structure
```bash
mkdir -p src/discord_commander/commands
touch src/discord_commander/commands/__init__.py
```

### Step 2: Extract Command Groups (Priority Order)

1. **Start with smallest groups** (Profile Commands - 2 commands)
2. **Extract core system commands** (most frequently used)
3. **Extract messaging commands** (core functionality)
4. **Extract system control** (shutdown/restart)
5. **Extract remaining groups** (onboarding, git, agent management, integrations)

### Step 3: Update unified_discord_bot.py

1. Remove MessagingCommands class definition
2. Add imports for new command modules
3. Register cogs in `setup_hook()`
4. Update any internal references

### Step 4: Validation

1. **V2 Compliance Check**: Each module <300 lines
2. **Import Validation**: All imports resolve correctly
3. **Functionality Test**: All commands work as expected
4. **SSOT Tagging**: Add SSOT tags to new modules

---

## 📝 SSOT Tagging

All new command modules should include SSOT tags:

```python
"""
[Module Description]

<!-- SSOT Domain: web -->
"""
```

---

## 🎯 Expected Impact

**Phase 2 Target**:
- Extract 1,797 lines from MessagingCommands
- Reduce `unified_discord_bot.py` to ~900 lines
- Create 8 command modules (<300 lines each)
- Total reduction: ~1,795 lines (66.5% reduction from original 2,695 lines)

**Combined Phase 1 + Phase 2**:
- Original: 2,764 lines
- After Phase 1: 2,695 lines (-69 lines)
- After Phase 2: ~900 lines (-1,795 lines total)
- **Total Reduction**: 67.4% reduction

---

## 🔄 Coordination Points

- **Agent-1**: Boundary files coordination (pending Agent-7 Phase 1)
- **Agent-8**: QA validation ready for Phase 1 modules (Priority 1)
- **Agent-2**: Architecture guidance and coordination support

---

## ✅ Next Steps

1. **Agent-7**: Begin extraction with Profile Commands (smallest, lowest risk)
2. **Agent-7**: Validate pattern with first module before proceeding
3. **Agent-7**: Coordinate with Agent-8 for QA validation after each module group
4. **Agent-2**: Available for architecture questions and validation

---

**🐝 WE. ARE. SWARM. ⚡🔥**
