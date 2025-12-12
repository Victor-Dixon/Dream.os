# V2 Refactoring Implementation Plan - Phase 1

**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-12  
**Task**: CP-005 - V2 Compliance Refactoring Implementation  
**Status**: ✅ **PLAN COMPLETE**

---

## Phase 1 Overview

**Target**: Critical violations (>1000 lines)  
**Priority**: HIGH  
**Estimated Impact**: ~3,856 lines reduction potential  
**Timeline**: 2-3 cycles

## Target Files

1. **unified_discord_bot.py** (2,692 lines → target: <500 lines)
2. **github_book_viewer.py** (1,164 lines → target: <300 lines)

---

## File 1: unified_discord_bot.py Refactoring

### Current State
- **Lines**: 2,692
- **Over Limit**: 796%
- **Category**: Core Orchestration
- **Exception Status**: Approved (temporary)

### Refactoring Strategy

#### Step 1: Extract Command Handlers
**Target**: `src/discord_commander/handlers/`

**Files to Create**:
- `handlers/command_router.py` (200 lines) - Command routing logic
- `handlers/slash_commands.py` (300 lines) - Slash command handlers
- `handlers/user_commands.py` (250 lines) - User command handlers
- `handlers/message_commands.py` (200 lines) - Message command handlers
- `handlers/context_commands.py` (150 lines) - Context menu handlers

**Extraction Pattern**:
```python
# Before (in unified_discord_bot.py)
@bot.slash_command(...)
async def some_command(ctx, ...):
    # handler logic

# After (in handlers/slash_commands.py)
class SlashCommandHandlers:
    @staticmethod
    async def some_command(ctx, ...):
        # handler logic

# In unified_discord_bot.py (orchestration only)
from .handlers.slash_commands import SlashCommandHandlers
bot.add_application_command(SlashCommandHandlers.some_command)
```

#### Step 2: Extract Event Handlers
**Target**: `src/discord_commander/events/`

**Files to Create**:
- `events/ready_handler.py` (100 lines) - Bot ready event
- `events/message_handler.py` (200 lines) - Message events
- `events/reaction_handler.py` (150 lines) - Reaction events
- `events/member_handler.py` (200 lines) - Member events
- `events/error_handler.py` (150 lines) - Error handling

**Extraction Pattern**:
```python
# Before
@bot.event
async def on_ready():
    # logic

# After (in events/ready_handler.py)
class ReadyHandler:
    @staticmethod
    async def handle(bot):
        # logic

# In unified_discord_bot.py
from .events.ready_handler import ReadyHandler
bot.event(ReadyHandler.handle)
```

#### Step 3: Extract Modal Handlers
**Target**: `src/discord_commander/modals/`

**Files to Create**:
- `modals/task_modal.py` (200 lines) - Task-related modals
- `modals/agent_modal.py` (200 lines) - Agent-related modals
- `modals/coordination_modal.py` (150 lines) - Coordination modals
- `modals/system_modal.py` (150 lines) - System modals

#### Step 4: Extract Core Orchestration
**Target**: `src/discord_commander/core/`

**Files to Create**:
- `core/bot_initializer.py` (200 lines) - Bot initialization
- `core/command_registry.py` (150 lines) - Command registration
- `core/event_registry.py` (150 lines) - Event registration
- `core/config_manager.py` (100 lines) - Configuration management

### Final Structure
```
src/discord_commander/
├── unified_discord_bot.py (400 lines) - Core orchestration only
├── handlers/
│   ├── command_router.py
│   ├── slash_commands.py
│   ├── user_commands.py
│   ├── message_commands.py
│   └── context_commands.py
├── events/
│   ├── ready_handler.py
│   ├── message_handler.py
│   ├── reaction_handler.py
│   ├── member_handler.py
│   └── error_handler.py
├── modals/
│   ├── task_modal.py
│   ├── agent_modal.py
│   ├── coordination_modal.py
│   └── system_modal.py
└── core/
    ├── bot_initializer.py
    ├── command_registry.py
    ├── event_registry.py
    └── config_manager.py
```

### Implementation Steps
1. Create directory structure
2. Extract command handlers (test each extraction)
3. Extract event handlers (test each extraction)
4. Extract modal handlers (test each extraction)
5. Extract core orchestration
6. Update imports and references
7. Run integration tests
8. Verify bot functionality

### Testing Strategy
- Unit tests for each extracted handler
- Integration tests for command routing
- End-to-end tests for bot functionality
- Regression tests for existing features

---

## File 2: github_book_viewer.py Refactoring

### Current State
- **Lines**: 1,164
- **Over Limit**: 288%
- **Category**: Complex State Management
- **Exception Status**: Approved (temporary)

### Refactoring Strategy

#### Step 1: Extract State Management
**Target**: `src/discord_commander/github_book_viewer/state.py`

**Extract**:
- Viewer state classes
- State transition logic
- State persistence

**Estimated Lines**: 300 lines

#### Step 2: Extract UI Rendering
**Target**: `src/discord_commander/github_book_viewer/ui.py`

**Extract**:
- Embed generation
- Button creation
- View rendering logic

**Estimated Lines**: 250 lines

#### Step 3: Extract API Client
**Target**: `src/discord_commander/github_book_viewer/api.py`

**Extract**:
- GitHub API interactions
- File fetching logic
- Content parsing

**Estimated Lines**: 200 lines

#### Step 4: Extract Navigation Logic
**Target**: `src/discord_commander/github_book_viewer/navigation.py`

**Extract**:
- Page navigation
- Chapter navigation
- Search functionality

**Estimated Lines**: 200 lines

#### Step 5: Core Orchestration
**Target**: `src/discord_commander/github_book_viewer/__init__.py`

**Keep**:
- Main viewer class (orchestration only)
- Public API
- Integration points

**Estimated Lines**: 200 lines

### Final Structure
```
src/discord_commander/github_book_viewer/
├── __init__.py (200 lines) - Core orchestration
├── state.py (300 lines) - State management
├── ui.py (250 lines) - UI rendering
├── api.py (200 lines) - GitHub API client
└── navigation.py (200 lines) - Navigation logic
```

### Implementation Steps
1. Create directory structure
2. Extract state management (test state transitions)
3. Extract UI rendering (test embed generation)
4. Extract API client (test API calls)
5. Extract navigation logic (test navigation)
6. Update core orchestration
7. Run integration tests
8. Verify viewer functionality

### Testing Strategy
- Unit tests for state management
- Unit tests for UI rendering
- Unit tests for API client
- Integration tests for viewer functionality
- Regression tests for existing features

---

## Implementation Timeline

### Week 1: unified_discord_bot.py
- Days 1-2: Extract command handlers
- Days 3-4: Extract event handlers
- Days 5-6: Extract modal handlers
- Day 7: Extract core orchestration, testing

### Week 2: github_book_viewer.py
- Days 1-2: Extract state management
- Days 3-4: Extract UI rendering
- Days 5-6: Extract API client and navigation
- Day 7: Core orchestration, testing

### Week 3: Integration & Validation
- Integration testing
- Performance validation
- Documentation updates
- Code review

## Success Metrics

### Code Reduction
- unified_discord_bot.py: 2,692 → ~400 lines (85% reduction)
- github_book_viewer.py: 1,164 → ~200 lines (83% reduction)
- **Total Reduction**: ~3,256 lines

### Quality Metrics
- All tests passing
- No functionality regressions
- Improved code maintainability
- Better separation of concerns

### V2 Compliance
- All new files <300 lines
- Core orchestration files <500 lines
- Clear module boundaries
- Proper dependency management

## Risk Mitigation

### Risks
1. Breaking existing functionality
2. Import/dependency issues
3. Testing coverage gaps
4. Performance degradation

### Mitigation
1. Incremental extraction with tests
2. Comprehensive integration testing
3. Code review at each step
4. Performance benchmarking

## Coordination Requirements

### Agent-1 (Integration & Core Systems)
- Integration testing strategy
- Test coverage requirements
- CI/CD integration

### Agent-7 (Web Development)
- UI component extraction patterns
- Modal handler refactoring support

### Agent-8 (SSOT & System Integration)
- V2 compliance validation
- Code quality review
- Architecture review

## Next Actions

1. ✅ Create implementation plan (THIS ARTIFACT)
2. ⏳ Wait for coordination responses
3. ⏳ Begin Phase 1 implementation
4. ⏳ Create detailed extraction scripts
5. ⏳ Set up testing framework

## Status

✅ **IMPLEMENTATION PLAN COMPLETE** - Phase 1 refactoring plan created with detailed technical specifications

**Progress**: Ready to begin implementation once coordination established

---

*Plan generated as part of CP-005 task execution*

