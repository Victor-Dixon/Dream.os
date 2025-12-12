# V2 Refactoring Implementation Plan - Phase 1 Extended

**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-12  
**Task**: CP-005 - V2 Compliance Refactoring Implementation (Extended)  
**Status**: ✅ **PLAN COMPLETE**

---

## Phase 1 Extended Overview

**Target**: All 6 critical violations (>1000 lines)  
**Priority**: HIGH  
**Estimated Impact**: ~8,000+ lines reduction potential  
**Timeline**: 4-5 weeks

## Target Files

1. ✅ unified_discord_bot.py (2,692 lines) - Plan complete
2. ✅ github_book_viewer.py (1,164 lines) - Plan complete
3. **messaging_infrastructure.py** (1,922 lines) - This plan
4. **enhanced_agent_activity_detector.py** (1,367 lines) - This plan
5. **synthetic_github.py** (1,043 lines) - This plan
6. Additional critical file - Needs identification

---

## File 3: messaging_infrastructure.py Refactoring

### Current State
- **Lines**: 1,922
- **Over Limit**: 541%
- **Category**: Core Infrastructure
- **Exception Status**: Approved (temporary)

### Refactoring Strategy

#### Step 1: Extract Message Routing
**Target**: `src/services/messaging_infrastructure/routing.py`

**Extract**:
- Message routing logic
- Route determination
- Destination resolution

**Estimated Lines**: 300 lines

#### Step 2: Extract Message Formatting
**Target**: `src/services/messaging_infrastructure/formatting.py`

**Extract**:
- Template application
- Message formatting
- Content transformation

**Estimated Lines**: 400 lines

#### Step 3: Extract Message Delivery
**Target**: `src/services/messaging_infrastructure/delivery.py`

**Extract**:
- Delivery mechanisms
- Queue management
- Retry logic

**Estimated Lines**: 300 lines

#### Step 4: Extract Message Validation
**Target**: `src/services/messaging_infrastructure/validation.py`

**Extract**:
- Message validation
- Schema checking
- Error handling

**Estimated Lines**: 200 lines

#### Step 5: Extract Message Queue Operations
**Target**: `src/services/messaging_infrastructure/queue_ops.py`

**Extract**:
- Queue operations
- Message persistence
- Queue management

**Estimated Lines**: 250 lines

#### Step 6: Core Orchestration
**Target**: `src/services/messaging_infrastructure/__init__.py`

**Keep**:
- Main coordinator class
- Public API
- Integration points

**Estimated Lines**: 400 lines

### Final Structure
```
src/services/messaging_infrastructure/
├── __init__.py (400 lines) - Core orchestration
├── routing.py (300 lines) - Message routing
├── formatting.py (400 lines) - Message formatting
├── delivery.py (300 lines) - Message delivery
├── validation.py (200 lines) - Message validation
└── queue_ops.py (250 lines) - Queue operations
```

---

## File 4: enhanced_agent_activity_detector.py Refactoring

### Current State
- **Lines**: 1,367
- **Over Limit**: 356%
- **Category**: Activity Detection
- **Exception Status**: Approved (temporary)

### Refactoring Strategy

#### Step 1: Extract Activity Sources
**Target**: `src/orchestrators/overnight/activity_detector/sources.py`

**Extract**:
- File modification detection
- Git activity detection
- Message queue activity
- Tool execution tracking

**Estimated Lines**: 400 lines

#### Step 2: Extract Confidence Scoring
**Target**: `src/orchestrators/overnight/activity_detector/scoring.py`

**Extract**:
- Confidence calculation
- Source weighting
- Recency scoring

**Estimated Lines**: 200 lines

#### Step 3: Extract Activity Assessment
**Target**: `src/orchestrators/overnight/activity_detector/assessment.py`

**Extract**:
- Activity assessment logic
- Cross-validation
- Noise filtering

**Estimated Lines**: 300 lines

#### Step 4: Extract Signal Processing
**Target**: `src/orchestrators/overnight/activity_detector/signals.py`

**Extract**:
- Signal collection
- Signal aggregation
- Signal validation

**Estimated Lines**: 250 lines

#### Step 5: Core Detector
**Target**: `src/orchestrators/overnight/activity_detector/__init__.py`

**Keep**:
- Main detector class
- Public API
- Integration points

**Estimated Lines**: 200 lines

### Final Structure
```
src/orchestrators/overnight/activity_detector/
├── __init__.py (200 lines) - Core detector
├── sources.py (400 lines) - Activity sources
├── scoring.py (200 lines) - Confidence scoring
├── assessment.py (300 lines) - Activity assessment
└── signals.py (250 lines) - Signal processing
```

---

## File 5: synthetic_github.py Refactoring

### Current State
- **Lines**: 1,043
- **Over Limit**: 248%
- **Category**: GitHub Integration
- **Exception Status**: Approved (temporary)

### Refactoring Strategy

#### Step 1: Extract GitHub API Client
**Target**: `src/core/github_integration/api_client.py`

**Extract**:
- GitHub API interactions
- Request handling
- Response processing

**Estimated Lines**: 300 lines

#### Step 2: Extract Repository Operations
**Target**: `src/core/github_integration/repository_ops.py`

**Extract**:
- Repository operations
- File operations
- Branch management

**Estimated Lines**: 250 lines

#### Step 3: Extract Content Generation
**Target**: `src/core/github_integration/content_gen.py`

**Extract**:
- Content generation
- File content creation
- Template processing

**Estimated Lines**: 200 lines

#### Step 4: Extract Synthetic Operations
**Target**: `src/core/github_integration/synthetic_ops.py`

**Extract**:
- Synthetic repository operations
- Mock operations
- Testing utilities

**Estimated Lines**: 200 lines

#### Step 5: Core Integration
**Target**: `src/core/github_integration/__init__.py`

**Keep**:
- Main integration class
- Public API
- Integration points

**Estimated Lines**: 200 lines

### Final Structure
```
src/core/github_integration/
├── __init__.py (200 lines) - Core integration
├── api_client.py (300 lines) - GitHub API client
├── repository_ops.py (250 lines) - Repository operations
├── content_gen.py (200 lines) - Content generation
└── synthetic_ops.py (200 lines) - Synthetic operations
```

---

## Implementation Timeline (Extended)

### Week 1-2: unified_discord_bot.py + github_book_viewer.py
- Days 1-7: unified_discord_bot.py refactoring
- Days 8-14: github_book_viewer.py refactoring

### Week 3: messaging_infrastructure.py
- Days 1-3: Extract routing and formatting
- Days 4-5: Extract delivery and validation
- Days 6-7: Extract queue operations, core orchestration

### Week 4: enhanced_agent_activity_detector.py
- Days 1-2: Extract activity sources
- Days 3-4: Extract scoring and assessment
- Days 5-7: Extract signals, core detector

### Week 5: synthetic_github.py
- Days 1-2: Extract API client
- Days 3-4: Extract repository operations
- Days 5-7: Extract content generation, synthetic ops, core integration

### Week 6: Integration & Validation
- Integration testing
- Performance validation
- Documentation updates
- Code review

## Success Metrics

### Code Reduction
- unified_discord_bot.py: 2,692 → ~400 lines (85% reduction)
- github_book_viewer.py: 1,164 → ~200 lines (83% reduction)
- messaging_infrastructure.py: 1,922 → ~400 lines (79% reduction)
- enhanced_agent_activity_detector.py: 1,367 → ~200 lines (85% reduction)
- synthetic_github.py: 1,043 → ~200 lines (81% reduction)
- **Total Reduction**: ~6,200+ lines

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
- **Priority**: HIGH (messaging_infrastructure.py affects core systems)

### Agent-7 (Web Development)
- UI component extraction patterns (if applicable)
- Modal handler refactoring support

### Agent-8 (SSOT & System Integration)
- V2 compliance validation
- Code quality review
- Architecture review
- **Priority**: HIGH (all files affect system integration)

## Next Actions

1. ✅ Create extended implementation plan (THIS ARTIFACT)
2. ⏳ Wait for coordination responses
3. ⏳ Begin Phase 1 implementation (unified_discord_bot.py)
4. ⏳ Create detailed extraction scripts
5. ⏳ Set up testing framework

## Status

✅ **EXTENDED IMPLEMENTATION PLAN COMPLETE** - Phase 1 refactoring plan extended to cover all 5 critical violations

**Progress**: Ready to begin implementation once coordination established

---

*Extended plan generated as part of CP-005 task execution*

