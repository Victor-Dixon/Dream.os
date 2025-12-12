# Phase 2 V2 Refactoring Plan - High Priority Violations

**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-12  
**Task**: CP-006 - Refactor top 10 largest V2 violations  
**Status**: ✅ **PLAN COMPLETE**

---

## Executive Summary

**Phase 1 Status**: 5 critical violations (>1000 lines) delegated to swarm  
**Phase 2 Scope**: 22 high-priority violations (500-1000 lines)  
**Target**: Top 10 high-priority violations for immediate refactoring  
**Strategy**: Parallel execution across swarm for 4-6x speed improvement

---

## Phase 1 Status Review

### Completed Delegations
1. ✅ **unified_discord_bot.py** (2,692 lines) → Agent-7
2. ✅ **messaging_infrastructure.py** (1,922 lines) → Agent-1
3. ✅ **enhanced_agent_activity_detector.py** (1,367 lines) → Agent-3
4. ✅ **github_book_viewer.py** (1,164 lines) → Agent-7
5. ✅ **synthetic_github.py** (1,043 lines) → Agent-1

**Total Phase 1 Impact**: ~6,200+ lines reduction potential

---

## Phase 2 Target Files

### Top 10 High-Priority Violations (500-1000 lines)

| # | File | Lines | Over Limit | Priority | Domain |
|---|------|-------|------------|----------|--------|
| 1 | `twitch_bridge.py` | 954 | +654 | HIGH | Chat Presence |
| 2 | `hard_onboarding_service.py` | 870 | +570 | HIGH | Onboarding |
| 3 | `hardened_activity_detector.py` | 853 | +553 | HIGH | Activity Detection |
| 4 | `broadcast_templates.py` | 819 | +519 | HIGH | Discord Templates |
| 5 | `status_change_monitor.py` | 811 | +511 | HIGH | Discord Monitoring |
| 6 | `messaging_pyautogui.py` | 791 | +491 | HIGH | Messaging |
| 7 | `discord_gui_modals.py` | 789 | +489 | HIGH | Discord GUI |
| 8 | `discord_service.py` | 768 | +468 | HIGH | Discord Service |
| 9 | `fsm_bridge.py` | 756 | +456 | HIGH | FSM Integration |
| 10 | `unified_messaging_service.py` | 745 | +445 | HIGH | Messaging |

**Total Lines Over Limit**: 5,156 lines  
**Target Reduction**: ~3,500-4,000 lines (70-80% reduction)

---

## Refactoring Strategy

### Extraction Patterns

#### Pattern 1: Service Layer Separation
**Applies to**: `twitch_bridge.py`, `hard_onboarding_service.py`, `discord_service.py`

**Strategy**:
- Extract business logic → `services/{domain}/core/`
- Extract models → `services/{domain}/models/`
- Extract utilities → `services/{domain}/utils/`
- Main file → Orchestration only (~200-300 lines)

**Example**: `twitch_bridge.py` (954 lines)
```
twitch_bridge.py (orchestration, ~250 lines)
├── twitch/core/twitch_connection_manager.py (~200 lines)
├── twitch/core/twitch_message_handler.py (~200 lines)
├── twitch/models/twitch_models.py (~150 lines)
└── twitch/utils/twitch_utils.py (~150 lines)
```

#### Pattern 2: Component Extraction
**Applies to**: `broadcast_templates.py`, `discord_gui_modals.py`, `status_change_monitor.py`

**Strategy**:
- Extract template definitions → `discord_commander/templates/{domain}/`
- Extract modal components → `discord_commander/views/{domain}/`
- Extract monitoring logic → `discord_commander/monitors/{domain}/`
- Main file → Registry/Factory only (~200-250 lines)

**Example**: `broadcast_templates.py` (819 lines)
```
broadcast_templates.py (registry, ~200 lines)
├── templates/broadcast/onboarding_templates.py (~150 lines)
├── templates/broadcast/wrapup_templates.py (~150 lines)
├── templates/broadcast/urgent_templates.py (~150 lines)
└── templates/broadcast/base_templates.py (~150 lines)
```

#### Pattern 3: Infrastructure Separation
**Applies to**: `hardened_activity_detector.py`, `messaging_pyautogui.py`, `fsm_bridge.py`

**Strategy**:
- Extract detection logic → `core/{domain}/detectors/`
- Extract messaging logic → `core/{domain}/messaging/`
- Extract bridge logic → `core/{domain}/bridges/`
- Main file → Coordinator only (~200-250 lines)

**Example**: `hardened_activity_detector.py` (853 lines)
```
hardened_activity_detector.py (coordinator, ~200 lines)
├── core/activity_detection/sources/file_detector.py (~150 lines)
├── core/activity_detection/sources/git_detector.py (~150 lines)
├── core/activity_detection/sources/message_detector.py (~150 lines)
└── core/activity_detection/confidence_scorer.py (~200 lines)
```

---

## Agent Assignment Strategy

### Domain-Based Assignment

| Agent | Domain Expertise | Assigned Files | Count |
|-------|-----------------|---------------|-------|
| **Agent-7** | Web Development | `discord_gui_modals.py`, `broadcast_templates.py`, `status_change_monitor.py` | 3 |
| **Agent-1** | Integration & Core Systems | `unified_messaging_service.py`, `messaging_pyautogui.py`, `fsm_bridge.py` | 3 |
| **Agent-3** | Infrastructure & DevOps | `hardened_activity_detector.py` | 1 |
| **Agent-5** | Business Intelligence | `twitch_bridge.py` | 1 |
| **Agent-2** | Architecture & Design | `hard_onboarding_service.py`, `discord_service.py` | 2 |

**Total**: 10 files across 5 agents

---

## Implementation Timeline

### Week 1-2: Planning & Coordination
- **Agent-2**: Create detailed extraction plans for each file
- **All Agents**: Review extraction patterns and provide feedback
- **Agent-2**: Finalize refactoring plans and assign tasks

### Week 3-4: Parallel Execution
- **Agent-7**: Refactor Discord GUI components (3 files)
- **Agent-1**: Refactor messaging/FSM components (3 files)
- **Agent-3**: Refactor activity detection (1 file)
- **Agent-5**: Refactor Twitch bridge (1 file)
- **Agent-2**: Refactor onboarding/Discord service (2 files)

### Week 5: Integration & Testing
- **All Agents**: Integration testing
- **Agent-1**: Integration test coordination
- **Agent-8**: QA validation

### Week 6: Validation & Documentation
- **Agent-2**: Run V2 compliance validation
- **Agent-2**: Update progress reports
- **Agent-8**: Final QA review

**Total Timeline**: 6 weeks (parallel execution)

---

## Expected Impact

### Code Reduction
- **Target**: 3,500-4,000 lines reduction
- **Files Refactored**: 10 files
- **New Files Created**: ~30-40 smaller modules
- **Average File Size**: 200-300 lines (V2 compliant)

### Quality Improvements
- **Maintainability**: Smaller, focused modules
- **Testability**: Isolated components easier to test
- **Reusability**: Extracted components can be reused
- **Readability**: Clear separation of concerns

### Compliance Status
- **Before**: 10 files violating V2 (500-1000 lines)
- **After**: 0 files violating V2 (all <300 lines)
- **Improvement**: 10 violations resolved

---

## Risk Mitigation

### Integration Risks
- **Risk**: Breaking changes during refactoring
- **Mitigation**: Comprehensive integration tests before/after
- **Owner**: Agent-1 (Integration testing)

### Coordination Risks
- **Risk**: Agents working on interdependent files
- **Mitigation**: Clear handoff points and integration checkpoints
- **Owner**: Agent-2 (Architecture coordination)

### Quality Risks
- **Risk**: Reduced code quality during refactoring
- **Mitigation**: Agent-8 QA validation at each stage
- **Owner**: Agent-8 (Quality assurance)

---

## Success Metrics

### Quantitative Metrics
- ✅ 10 files refactored to <300 lines
- ✅ 3,500-4,000 lines reduction achieved
- ✅ 0 new violations introduced
- ✅ 100% test coverage maintained

### Qualitative Metrics
- ✅ Improved code maintainability
- ✅ Better separation of concerns
- ✅ Enhanced reusability
- ✅ Clearer architecture

---

## Next Steps

### Immediate Actions
1. **Agent-2**: Create detailed extraction plans for each file
2. **Agent-2**: Send task assignments to swarm
3. **All Agents**: Review plans and provide feedback
4. **Agent-2**: Finalize coordination timeline

### Coordination Messages
- **Agent-7**: Discord GUI refactoring assignment (3 files)
- **Agent-1**: Messaging/FSM refactoring assignment (3 files)
- **Agent-3**: Activity detection refactoring assignment (1 file)
- **Agent-5**: Twitch bridge refactoring assignment (1 file)
- **Agent-2**: Onboarding/Discord service refactoring (2 files)

---

## Status

✅ **PLAN COMPLETE** - Phase 2 refactoring strategy documented

**Progress**:
- Analysis: ✅ Complete (10 files identified)
- Strategy: ✅ Complete (extraction patterns defined)
- Assignment: ⏳ Pending (coordination messages to be sent)
- Execution: ⏳ Pending (awaiting agent assignments)

**Next Actions**:
- Create detailed extraction plans for each file
- Send task assignments to swarm
- Establish coordination timeline
- Begin parallel execution

---

*Phase 2 plan generated as part of CP-006 task execution*

