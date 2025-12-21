# Tier 1 V2 Compliance Refactoring - Architecture Guidance

**Reviewer:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-12-19  
**Requested By:** V2 Compliance Architecture Support  
**Status:** ✅ Guidance Provided

---

## Executive Summary

**Tier 1 Critical Violations:**
- `messaging_template_texts.py` (945 lines) → Target: ~300 lines
- `enhanced_agent_activity_detector.py` (1,215 lines) → Target: ~200 lines
- `github_book_viewer.py` (1,001 lines) → Target: ~200 lines

**Batch 4 Onboarding Services (20% complete):**
- `hard_onboarding_service.py` (870 lines) → Target: ~200 lines
- `soft_onboarding_service.py` (533 lines) → Target: ~200 lines

**Recommended Patterns:**
- **messaging_template_texts.py**: Configuration/Data Pattern (extract templates to modules)
- **enhanced_agent_activity_detector.py**: Strategy Pattern (activity detection strategies)
- **github_book_viewer.py**: MVC Pattern (separate data, view, controller)
- **hard_onboarding_service.py**: Service Layer Pattern (extract protocol steps)
- **soft_onboarding_service.py**: Service Layer Pattern (extract protocol steps)

---

## File Analysis & Pattern Recommendations

### 1. **messaging_template_texts.py** (945 lines)
**Current Structure:**
- Large template string constants (AGENT_OPERATING_CYCLE_TEXT, CYCLE_CHECKLIST_TEXT, etc.)
- Template formatting functions (format_s2a_message, format_d2a_payload)
- Message template dictionaries
- Helper functions

**Recommended Pattern:** **Configuration/Data Pattern** (extract to modules)

**Rationale:**
- Mostly static data/configuration (templates, text constants)
- Can be organized by category (S2A, A2A, D2A, C2A)
- Template functions can be separated
- Already partially addressed in Phase 2 guidance

**Refactoring Strategy:**
1. **Extract Operating Cycle Templates** → `messaging/templates/operating_cycle.py` (~100 lines)
2. **Extract Coordination Templates** → `messaging/templates/coordination.py` (~150 lines)
3. **Extract Discord Templates** → `messaging/templates/discord.py` (~100 lines)
4. **Extract A2A Templates** → `messaging/templates/a2a.py` (~150 lines)
5. **Extract S2A Templates** → `messaging/templates/s2a.py` (~100 lines)
6. **Extract Template Formatters** → `messaging/templates/formatters.py` (~100 lines)
7. **Template Registry** → `messaging/templates/registry.py` (~50 lines)
8. **Maintain backward compatibility** → `messaging_template_texts.py` shim

**Module Structure:**
```
src/core/messaging/templates/
├── __init__.py
├── registry.py (template registry and lookup)
├── formatters.py (format_s2a_message, format_d2a_payload)
├── operating_cycle.py (AGENT_OPERATING_CYCLE_TEXT, CYCLE_CHECKLIST_TEXT)
├── coordination.py (SWARM_COORDINATION_TEXT, A2A templates)
├── discord.py (DISCORD_REPORTING_TEXT, D2A templates)
└── s2a.py (S2A message templates)
```

**Estimated Reduction:** 945 → ~300 lines (68% reduction)

**Note:** This aligns with Phase 2 guidance for `messaging_template_texts.py`. Can coordinate with Phase 2 refactoring.

---

### 2. **enhanced_agent_activity_detector.py** (1,215 lines)
**Current Structure:**
- `EnhancedAgentActivityDetector` class (main detector)
- Multiple activity check methods (_check_status_json, _check_inbox_files, etc.)
- Activity aggregation logic
- Timeout and configuration handling

**Recommended Pattern:** **Strategy Pattern** (activity detection strategies)

**Rationale:**
- Multiple activity detection strategies (status.json, inbox, devlogs, git, etc.)
- Each strategy is independent and can be extracted
- Different strategies for different activity types
- Aggregation logic can be separated

**Refactoring Strategy:**
1. **Extract Activity Detection Strategies** → `orchestrators/overnight/activity/strategies.py` (~400 lines)
   - StatusJsonStrategy
   - InboxFilesStrategy
   - DevlogStrategy
   - GitCommitStrategy
   - MessageQueueStrategy
   - WorkspaceFilesStrategy
   - DiscordPostStrategy
2. **Extract Activity Aggregator** → `orchestrators/overnight/activity/aggregator.py` (~150 lines)
   - Activity aggregation logic
   - Latest activity calculation
3. **Extract Configuration** → `orchestrators/overnight/activity/config.py` (~50 lines)
   - Timeout constants
   - Activity thresholds
4. **Main Detector** → `orchestrators/overnight/activity/detector.py` (~200 lines)
5. **Maintain backward compatibility** → `enhanced_agent_activity_detector.py` shim

**Module Structure:**
```
src/orchestrators/overnight/activity/
├── __init__.py
├── detector.py (EnhancedAgentActivityDetector - main)
├── strategies.py (StatusJsonStrategy, InboxFilesStrategy, etc.)
├── aggregator.py (activity aggregation logic)
└── config.py (timeout constants, thresholds)
```

**Estimated Reduction:** 1,215 → ~200 lines (84% reduction)

---

### 3. **github_book_viewer.py** (1,001 lines)
**Current Structure:**
- `GitHubBookData` class (data loader)
- `GitHubBookNavigator` class (Discord UI view)
- `GitHubBookCommands` class (Discord commands)
- Data loading and management logic

**Recommended Pattern:** **MVC Pattern** (Model-View-Controller)

**Rationale:**
- Clear separation: Data (Model), UI (View), Commands (Controller)
- Data loading is independent of Discord UI
- UI components can be separated
- Commands can be extracted

**Refactoring Strategy:**
1. **Extract Data Model** → `discord_commander/github_book/model.py` (~200 lines)
   - GitHubBookData class
   - Data loading logic
   - Master list management
2. **Extract View Components** → `discord_commander/github_book/views.py` (~300 lines)
   - GitHubBookNavigator (Discord UI)
   - Embed builders
   - UI formatting
3. **Extract Controller** → `discord_commander/github_book/controller.py` (~150 lines)
   - GitHubBookCommands (Discord commands)
   - Command handlers
4. **Extract Utilities** → `discord_commander/github_book/utils.py` (~100 lines)
   - Helper functions
   - Formatting utilities
5. **Maintain backward compatibility** → `github_book_viewer.py` shim

**Module Structure:**
```
src/discord_commander/github_book/
├── __init__.py
├── model.py (GitHubBookData - data model)
├── views.py (GitHubBookNavigator - Discord UI)
├── controller.py (GitHubBookCommands - commands)
└── utils.py (helper functions)
```

**Estimated Reduction:** 1,001 → ~200 lines (80% reduction)

---

### 4. **hard_onboarding_service.py** (870 lines)
**Current Structure:**
- `HardOnboardingService` class (main service)
- Multiple step methods (step_1_clear_chat, step_2_save_session, etc.)
- Coordinate loading and validation
- PyAutoGUI operations

**Recommended Pattern:** **Service Layer Pattern** (extract protocol steps)

**Rationale:**
- Clear protocol steps (5-step RESET protocol)
- Each step can be extracted as a strategy
- Coordinate management can be separated
- PyAutoGUI operations can be abstracted

**Refactoring Strategy:**
1. **Extract Protocol Steps** → `services/onboarding/hard/steps.py` (~300 lines)
   - Step1ClearChat
   - Step2SaveSession
   - Step3NewWindow
   - Step4NavigateToOnboarding
   - Step5SendOnboarding
2. **Extract Coordinate Management** → `services/onboarding/hard/coordinates.py` (~100 lines)
   - Coordinate loading
   - Coordinate validation
3. **Extract PyAutoGUI Operations** → `services/onboarding/hard/operations.py` (~150 lines)
   - PyAutoGUI wrapper
   - Operation helpers
4. **Main Service** → `services/onboarding/hard/service.py` (~200 lines)
5. **Maintain backward compatibility** → `hard_onboarding_service.py` shim

**Module Structure:**
```
src/services/onboarding/hard/
├── __init__.py
├── service.py (HardOnboardingService - main)
├── steps.py (protocol step implementations)
├── coordinates.py (coordinate management)
└── operations.py (PyAutoGUI operations)
```

**Estimated Reduction:** 870 → ~200 lines (77% reduction)

---

### 5. **soft_onboarding_service.py** (533 lines)
**Current Structure:**
- `SoftOnboardingService` class (main service)
- Multiple step methods (step_1_click_chat_input, step_2_save_session, etc.)
- Coordinate loading
- PyAutoGUI operations

**Recommended Pattern:** **Service Layer Pattern** (extract protocol steps)

**Rationale:**
- Clear protocol steps (6-step soft onboarding protocol)
- Each step can be extracted as a strategy
- Similar structure to hard onboarding (can share utilities)
- PyAutoGUI operations can be abstracted

**Refactoring Strategy:**
1. **Extract Protocol Steps** → `services/onboarding/soft/steps.py` (~200 lines)
   - Step1ClickChatInput
   - Step2SaveSession
   - Step3SendCleanupPrompt
   - Step4OpenNewTab
   - Step5NavigateToOnboarding
   - Step6PasteOnboarding
2. **Extract Shared Utilities** → `services/onboarding/shared/` (~100 lines)
   - Coordinate management (shared with hard onboarding)
   - PyAutoGUI operations (shared with hard onboarding)
3. **Main Service** → `services/onboarding/soft/service.py` (~150 lines)
4. **Maintain backward compatibility** → `soft_onboarding_service.py` shim

**Module Structure:**
```
src/services/onboarding/soft/
├── __init__.py
├── service.py (SoftOnboardingService - main)
└── steps.py (protocol step implementations)

src/services/onboarding/shared/
├── __init__.py
├── coordinates.py (shared coordinate management)
└── operations.py (shared PyAutoGUI operations)
```

**Estimated Reduction:** 533 → ~200 lines (62% reduction)

**Note:** Can share utilities with hard onboarding service.

---

## Architecture Pattern Summary

### Pattern Selection Matrix

| File | Current Lines | Pattern | Target Lines | Reduction |
|------|---------------|---------|-------------|-----------|
| messaging_template_texts.py | 945 | Configuration/Data | ~300 | 68% |
| enhanced_agent_activity_detector.py | 1,215 | Strategy | ~200 | 84% |
| github_book_viewer.py | 1,001 | MVC | ~200 | 80% |
| hard_onboarding_service.py | 870 | Service Layer | ~200 | 77% |
| soft_onboarding_service.py | 533 | Service Layer | ~200 | 62% |
| **Total** | **4,564** | **Mixed** | **~1,100** | **76%** |

---

## Implementation Plan

### Phase 1: messaging_template_texts.py (Priority: HIGH)
**Status:** Already planned in Phase 2 infrastructure refactoring

**Steps:**
1. Coordinate with Phase 2 refactoring
2. Extract templates by category
3. Create template registry
4. Update imports across codebase
5. Verify backward compatibility

**Estimated Time:** 1-2 cycles (can coordinate with Phase 2)
**Dependencies:** Phase 2 infrastructure refactoring

---

### Phase 2: enhanced_agent_activity_detector.py (Priority: HIGH)
**Status:** Independent refactoring

**Steps:**
1. Create `src/orchestrators/overnight/activity/` directory structure
2. Extract activity detection strategies
3. Extract activity aggregator
4. Extract configuration
5. Refactor main detector
6. Create backward compatibility shim
7. Update imports across codebase
8. Verify all tests pass

**Estimated Time:** 2-3 cycles
**Dependencies:** None (can start immediately)

---

### Phase 3: github_book_viewer.py (Priority: MEDIUM)
**Status:** Independent refactoring

**Steps:**
1. Create `src/discord_commander/github_book/` directory structure
2. Extract data model
3. Extract view components
4. Extract controller
5. Extract utilities
6. Create backward compatibility shim
7. Update imports across codebase
8. Verify all tests pass

**Estimated Time:** 2-3 cycles
**Dependencies:** None (can start immediately)

---

### Phase 4: hard_onboarding_service.py (Priority: HIGH - Batch 4)
**Status:** Batch 4, 20% complete

**Steps:**
1. Create `src/services/onboarding/hard/` directory structure
2. Extract protocol steps
3. Extract coordinate management
4. Extract PyAutoGUI operations
5. Refactor main service
6. Create backward compatibility shim
7. Update imports across codebase
8. Verify all tests pass

**Estimated Time:** 2 cycles
**Dependencies:** None (can start immediately)

---

### Phase 5: soft_onboarding_service.py (Priority: HIGH - Batch 4)
**Status:** Batch 4, 20% complete

**Steps:**
1. Create `src/services/onboarding/soft/` directory structure
2. Create `src/services/onboarding/shared/` for shared utilities
3. Extract protocol steps
4. Extract shared utilities (coordinates, operations)
5. Refactor main service
6. Create backward compatibility shim
7. Update imports across codebase
8. Verify all tests pass

**Estimated Time:** 1-2 cycles
**Dependencies:** Can coordinate with hard onboarding (shared utilities)

---

## Integration Points

### Backward Compatibility
All files need backward compatibility shims:
- `messaging_template_texts.py` → imports from `messaging/templates/`
- `enhanced_agent_activity_detector.py` → imports from `orchestrators/overnight/activity/`
- `github_book_viewer.py` → imports from `discord_commander/github_book/`
- `hard_onboarding_service.py` → imports from `services/onboarding/hard/`
- `soft_onboarding_service.py` → imports from `services/onboarding/soft/`

### Import Updates Required
- Need systematic import update strategy
- Consider automated refactoring tool
- Test after each phase

---

## V2 Compliance Strategy

### Target Line Counts
- **messaging_template_texts.py**: 945 → ~300 lines ✅
- **enhanced_agent_activity_detector.py**: 1,215 → ~200 lines ✅
- **github_book_viewer.py**: 1,001 → ~200 lines ✅
- **hard_onboarding_service.py**: 870 → ~200 lines ✅
- **soft_onboarding_service.py**: 533 → ~200 lines ✅

### Module Size Limits
- All extracted modules should be < 400 lines
- Largest modules: ~300 lines each ✅
- All modules: < 400 lines ✅

---

## Risk Assessment

### High Risk
- **Import updates**: Many files may import these modules
- **Backward compatibility**: Critical for system stability
- **Activity detection**: Enhanced detector is critical path
- **Onboarding services**: Critical for agent initialization

### Medium Risk
- **Template extraction**: Large refactor but low impact
- **GitHub book viewer**: Less critical, can be done incrementally

### Mitigation Strategies
1. **Incremental refactoring**: One module at a time
2. **Comprehensive testing**: Verify after each extraction
3. **Backward compatibility shims**: Maintain during transition
4. **Automated import updates**: Use refactoring tools where possible

---

## Success Criteria

### Tier 1 Complete When:
- ✅ All 3 Tier 1 files under V2 compliance limits
- ✅ All modules < 400 lines
- ✅ Backward compatibility maintained
- ✅ All imports updated and verified
- ✅ All tests passing
- ✅ Architecture patterns properly applied

### Batch 4 Complete When:
- ✅ Both onboarding services under V2 compliance limits
- ✅ All modules < 400 lines
- ✅ Shared utilities extracted
- ✅ Backward compatibility maintained
- ✅ All imports updated and verified
- ✅ All tests passing
- ✅ Architecture patterns properly applied

---

## Recommendations

### Pattern Application Priority
1. **enhanced_agent_activity_detector.py** (Strategy) - Start here (independent, high impact)
2. **hard_onboarding_service.py** (Service Layer) - Batch 4 priority
3. **soft_onboarding_service.py** (Service Layer) - Batch 4 priority, can share utilities
4. **github_book_viewer.py** (MVC) - Can run in parallel
5. **messaging_template_texts.py** (Configuration) - Coordinate with Phase 2

### Coordination Strategy
- **Agent-3**: Execute refactoring (infrastructure expertise)
- **Agent-2**: Architecture review at each checkpoint
- **Agent-1**: Integration testing after each phase

### Checkpoint Reviews
- After Phase 1: Review template organization
- After Phase 2: Review strategy pattern implementation
- After Phase 3: Review MVC pattern implementation
- After Phase 4: Review hard onboarding service layer
- After Phase 5: Review soft onboarding service layer
- Final: Complete architecture review

---

## Conclusion

**Architecture Guidance Status:** ✅ **APPROVED**

**Recommended Approach:**
1. **Configuration/Data Pattern** for messaging_template_texts.py (extract to modules)
2. **Strategy Pattern** for enhanced_agent_activity_detector.py (activity detection strategies)
3. **MVC Pattern** for github_book_viewer.py (separate data, view, controller)
4. **Service Layer Pattern** for hard_onboarding_service.py (extract protocol steps)
5. **Service Layer Pattern** for soft_onboarding_service.py (extract protocol steps, share utilities)

**Estimated Total Reduction:** 4,564 → ~1,100 lines (76% reduction)

**Ready for implementation with architecture guidance provided.**

---

🐝 **WE. ARE. SWARM. ⚡🔥**
