<!-- SSOT Domain: architecture -->
# V2 Compliance - Next Violations Plan
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-14  
**Status**: 🟡 Planning Phase

---

## Executive Summary

Analysis of next 5-10 V2 compliance violations in `src/` directory requiring refactoring. Focus on high-impact, high-ROI violations that can be systematically addressed.

---

## Priority Violations Analysis

### Critical Violations (>600 lines)

#### 1. `src/discord_commander/unified_discord_bot.py` - 2,695 lines ⚡ CRITICAL
- **Exceeds by**: 2,295 lines
- **Status**: Currently being refactored by Agent-7 (26.7% reduction achieved)
- **Action**: Continue coordination with Agent-7, monitor progress

#### 2. `src/orchestrators/overnight/enhanced_agent_activity_detector.py` - 1,367 lines ⚡ CRITICAL
- **Exceeds by**: 967 lines
- **Refactor Priority**: HIGH
- **ROI Score**: 9.0 (HIGH)
- **Strategy**: Extract modules by functionality:
  - Activity detection logic
  - Agent status tracking
  - Recovery mechanisms
  - Notification handlers
- **Estimated Effort**: 3 cycles
- **Estimated Points**: 500 pts

#### 3. `src/discord_commander/github_book_viewer.py` - 1,164 lines ⚡ CRITICAL
- **Exceeds by**: 764 lines
- **Status**: Analysis pending (coordination with Agent-7)
- **Action**: Await Agent-7 Phase 1 completion, then coordinate extraction strategy

#### 4. `src/infrastructure/browser/thea_browser_service.py` - 1,013 lines ⚡ CRITICAL
- **Exceeds by**: 613 lines
- **Refactor Priority**: HIGH
- **ROI Score**: 8.5 (HIGH)
- **Strategy**: Extract browser operation modules:
  - Browser initialization/config
  - Navigation handlers
  - Element interaction
  - Page state management
- **Estimated Effort**: 2.5 cycles
- **Estimated Points**: 350 pts

#### 5. `src/services/chat_presence/twitch_bridge.py` - 954 lines ⚡ CRITICAL
- **Exceeds by**: 554 lines
- **Refactor Priority**: MEDIUM-HIGH
- **ROI Score**: 7.5 (MEDIUM-HIGH)
- **Strategy**: Extract by integration type:
  - Twitch API client
  - Message routing
  - Presence monitoring
  - Event handlers
- **Estimated Effort**: 2 cycles
- **Estimated Points**: 250 pts

### High-Priority Violations (500-600 lines)

#### 6. `src/core/messaging_template_texts.py` - 885 lines
- **Exceeds by**: 485 lines
- **Refactor Priority**: MEDIUM
- **ROI Score**: 6.5 (MEDIUM)
- **Strategy**: Split by message category:
  - Template definitions by domain (system, coordination, error, etc.)
  - Template formatters
  - Template utilities
- **Estimated Effort**: 1.5 cycles
- **Estimated Points**: 200 pts

#### 7. `src/services/hard_onboarding_service.py` - 870 lines
- **Exceeds by**: 470 lines
- **Refactor Priority**: MEDIUM
- **ROI Score**: 7.0 (MEDIUM)
- **Strategy**: Extract onboarding phases:
  - Initialization/setup
  - Template loading
  - Agent configuration
  - Validation/verification
- **Estimated Effort**: 2 cycles
- **Estimated Points**: 250 pts

#### 8. `src/discord_commander/status_change_monitor.py` - 826 lines
- **Exceeds by**: 426 lines
- **Refactor Priority**: MEDIUM
- **ROI Score**: 6.0 (MEDIUM)
- **Strategy**: Extract monitoring components:
  - Status detection
  - Change tracking
  - Notification logic
- **Estimated Effort**: 1.5 cycles
- **Estimated Points**: 200 pts

#### 9. `src/discord_commander/templates/broadcast_templates.py` - 819 lines
- **Exceeds by**: 419 lines
- **Refactor Priority**: MEDIUM
- **ROI Score**: 6.0 (MEDIUM)
- **Strategy**: Split by broadcast type:
  - Message templates by category
  - Formatters
  - Utilities
- **Estimated Effort**: 1.5 cycles
- **Estimated Points**: 200 pts

#### 10. `src/core/hardened_activity_detector.py` - 809 lines
- **Exceeds by**: 409 lines
- **Refactor Priority**: MEDIUM
- **ROI Score**: 6.5 (MEDIUM)
- **Strategy**: Extract detection modules:
  - Activity pattern detection
  - State tracking
  - Recovery logic
- **Estimated Effort**: 2 cycles
- **Estimated Points**: 200 pts

---

## Execution Plan

### Phase 1: Critical Refactoring (Weeks 1-2)
**Target**: Top 3 critical violations

1. **Monitor Agent-7**: `unified_discord_bot.py` (in progress)
2. **Plan extraction**: `enhanced_agent_activity_detector.py` (ready for assignment)
3. **Coordinate**: `github_book_viewer.py` (after Agent-7 Phase 1)

### Phase 2: High-Priority Refactoring (Weeks 2-3)
**Target**: Violations #4-6

4. **Browser service refactoring**: `thea_browser_service.py`
5. **Twitch bridge refactoring**: `twitch_bridge.py`
6. **Template texts refactoring**: `messaging_template_texts.py`

### Phase 3: Medium-Priority Refactoring (Weeks 3-4)
**Target**: Violations #7-10

7-10. Systematic refactoring of remaining violations

---

## ROI Summary

| Priority | Files | Total Points | Total Effort | Avg ROI |
|----------|-------|--------------|--------------|---------|
| Critical | 3 | 1,150 pts | 7.5 cycles | 8.2 |
| High | 3 | 800 pts | 6 cycles | 7.0 |
| Medium | 4 | 850 pts | 7 cycles | 6.3 |
| **TOTAL** | **10** | **2,800 pts** | **20.5 cycles** | **7.2** |

---

## Coordination Requirements

### Agent Assignments

- **Agent-7**: Continue `unified_discord_bot.py`, coordinate `github_book_viewer.py`
- **Agent-1**: Consider `thea_browser_service.py` (infrastructure)
- **Agent-3**: Consider `twitch_bridge.py` (integration)
- **Agent-8**: QA validation for all refactorings

### Architecture Support

- Provide extraction pattern guidance
- Review module boundaries
- Validate SSOT domain alignments
- Coordinate cross-agent dependencies

---

## Success Criteria

- [ ] All 10 violations reduced to <400 lines
- [ ] Module extraction maintains functionality
- [ ] No regressions in test coverage
- [ ] SSOT domain tags applied
- [ ] Architecture documentation updated

---

## Next Actions

1. ✅ Create violation plan document
2. ⏳ Coordinate with Agent-7 on `github_book_viewer.py` timing
3. ⏳ Assign `enhanced_agent_activity_detector.py` (recommend Agent-1)
4. ⏳ Assign `thea_browser_service.py` (recommend Agent-1)
5. ⏳ Begin Phase 1 execution

---

**Status**: 🟡 Planning Complete - Ready for Execution  
**Next Update**: After Phase 1 assignments confirmed
