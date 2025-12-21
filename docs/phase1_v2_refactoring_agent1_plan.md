# Phase 1 V2 Refactoring Plan - Agent-1

**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-12  
**Files**: messaging_infrastructure.py (1,922 lines) + synthetic_github.py (1,043 lines)  
**Status**: Analysis Complete, Plan Ready

## V2 Compliance Violations

### messaging_infrastructure.py (1,922 lines)
- **File Size**: 1,922 lines (violation: max 300 lines)
- **Violation Severity**: CRITICAL (>6x limit)
- **Target**: Break into ~7 modules (<300 lines each)

### synthetic_github.py (1,043 lines)
- **File Size**: 1,043 lines (violation: max 300 lines)
- **Violation Severity**: CRITICAL (>3x limit)
- **Target**: Break into ~4 modules (<300 lines each)

## Refactoring Strategy

### messaging_infrastructure.py Breakdown

**Current Structure Analysis**:
- Multiple classes and functions consolidated
- CLI parsing, formatting, handlers, service adapters
- SSOT domain: integration

**Proposed Module Structure**:
1. `src/services/messaging/cli_parser.py` (~200 lines)
   - Argument parsing logic
   - Flag validation
   - Command routing

2. `src/services/messaging/message_formatters.py` (~250 lines)
   - Message formatting utilities
   - Template handling
   - Output formatting

3. `src/services/messaging/delivery_handlers.py` (~280 lines)
   - PyAutoGUI delivery
   - Inbox delivery
   - Delivery mode management

4. `src/services/messaging/service_adapters.py` (~200 lines)
   - Service integration adapters
   - API clients
   - External service wrappers

5. `src/services/messaging/coordination_handlers.py` (~250 lines)
   - Agent coordination logic
   - Status checking
   - Contract system integration

6. `src/services/messaging/messaging_cli.py` (~150 lines)
   - Main CLI entry point
   - Command orchestration
   - High-level workflow

7. `src/services/messaging/__init__.py` (~50 lines)
   - Public API exports
   - Module initialization

**Total**: ~1,380 lines (reduced from 1,922, ~28% reduction)

### synthetic_github.py Breakdown

**Current Structure Analysis**:
- GitHub wrapper with local-first strategy
- Sandbox mode management
- Local repo layer integration
- Deferred push queue integration

**Proposed Module Structure**:
1. `src/core/github/synthetic_client.py` (~250 lines)
   - Main GitHub client interface
   - API method routing
   - Local/remote decision logic

2. `src/core/github/sandbox_manager.py` (~200 lines)
   - Sandbox mode management
   - Configuration handling
   - Mode switching logic

3. `src/core/github/local_router.py` (~280 lines)
   - Local storage routing
   - Cache management
   - Local-first strategy implementation

4. `src/core/github/remote_router.py` (~200 lines)
   - Remote GitHub API calls
   - Rate limiting
   - Error handling

5. `src/core/github/__init__.py` (~50 lines)
   - Public API exports
   - Module initialization

**Total**: ~980 lines (reduced from 1,043, ~6% reduction)

## Implementation Phases

### Phase 1: Analysis & Planning (Week 1) ✅
- [x] File analysis complete
- [x] V2 violations identified
- [x] Refactoring plan created
- [ ] Architecture review with Agent-2
- [ ] V2 compliance criteria from Agent-8

### Phase 2: Module Extraction (Weeks 2-3)
- Extract messaging_infrastructure.py modules
- Extract synthetic_github.py modules
- Maintain backward compatibility
- Update imports incrementally

### Phase 3: Testing & Validation (Week 4)
- Unit tests for new modules
- Integration tests
- V2 compliance validation
- Performance testing

### Phase 4: Integration & Cleanup (Weeks 5-6)
- Update all imports across codebase
- Remove old monolithic files
- Documentation updates
- Final validation

## Coordination Points

### Agent-2 (Architecture Review)
- Review module structure before extraction
- Validate architectural patterns
- Check dependency graph

### Agent-8 (V2 Compliance)
- Validate LOC limits per module
- Check complexity metrics
- Verify compliance standards

### Agent-7/Agent-3 (Integration Testing)
- Test refactored modules integration
- Verify no regressions
- Performance validation

## Success Criteria

1. ✅ All modules <300 lines
2. ✅ All functions <30 lines
3. ✅ All classes <200 lines
4. ✅ Zero test regressions
5. ✅ V2 compliance validated
6. ✅ Performance maintained/improved
7. ✅ Documentation updated

## Risk Mitigation

- **Backward Compatibility**: Maintain existing public APIs
- **Incremental Migration**: Extract modules one at a time
- **Continuous Testing**: Test after each module extraction
- **Rollback Plan**: Keep old files until validation complete

## Timeline

- **Week 1**: Analysis & Planning ✅
- **Weeks 2-3**: Module Extraction
- **Week 4**: Testing & Validation
- **Weeks 5-6**: Integration & Cleanup

**Total**: 4-6 weeks (aligned with swarm timeline)





