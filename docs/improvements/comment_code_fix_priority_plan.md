# Comment-Code Mismatch Fix Priority Plan
**Date**: 2025-12-12  
**Priority**: HIGH  
**Status**: Ready for Execution

## Priority Classification

### P0 - Critical (Immediate Fix)
None identified

### P1 - High Priority (Fix This Cycle)
**Parameter Mismatches** (11 instances):
1. `src/core/error_handling/circuit_breaker/protocol.py` - `call()` function missing `*args, **kwargs`
2. `src/core/session/base_session_manager.py` - `create_session()` missing `**kwargs`
3. `src/core/session/rate_limited_session_manager.py` - `create_session()` missing `**kwargs`
4. `src/core/utils/coordination_utils.py` - `store_coordination_history()` missing `**kwargs`
5. `src/domain/ports/logger.py` - `debug()`, `info()`, `warning()` missing `**context` (3 functions)
6. `src/infrastructure/logging/std_logger.py` - `debug()`, `info()`, `warning()` missing `**context` (3 functions)
7. `src/services/chatgpt/session.py` - `create_session()` missing `**kwargs`
8. `src/services/utils/messaging_templates.py` - `format_template()` missing `**kwargs`

**Missing Methods** (8 instances - review for false positives):
1. `src/ai_training/dreamvault/database.py` - `cursor()` method mentioned
2. `src/architecture/design_patterns.py` - `Type1Class()`, `MyObserver()` mentioned
3. `src/core/base/` classes - `super()` mentioned (likely false positives)
4. `src/core/orchestration/base_orchestrator.py` - `super()` mentioned
5. `src/core/utils/validation_utils.py` - `print_validation_report()` mentioned

### P2 - Medium Priority (Next Cycle)
**Type Hints Missing** (70 instances):
- Add type hints where docstrings mention types
- Systematic update across codebase

## Execution Plan

### Immediate Actions (P1)

#### Phase 1: Fix Parameter Mismatches
**Target**: 11 high-priority parameter mismatches

**Strategy**: 
1. Add missing `**kwargs` parameters to function signatures
2. Add missing `**context` parameters to logger functions
3. Ensure backward compatibility (default empty dicts)

**Files to Fix**:
- `src/core/error_handling/circuit_breaker/protocol.py` (1 function)
- `src/core/session/base_session_manager.py` (1 function)
- `src/core/session/rate_limited_session_manager.py` (1 function)
- `src/core/utils/coordination_utils.py` (1 function)
- `src/domain/ports/logger.py` (3 functions)
- `src/infrastructure/logging/std_logger.py` (3 functions)
- `src/services/chatgpt/session.py` (1 function)
- `src/services/utils/messaging_templates.py` (1 function)

#### Phase 2: Review Missing Methods
**Target**: 8 method mentions in docstrings

**Strategy**:
1. Review each case to determine if:
   - Method should be implemented
   - Method should be removed from docstring
   - False positive (e.g., `super()` is built-in)

## Assignment Recommendation

**Agent-8 (SSOT & QA)**: Fix parameter mismatches (Phase 1)
- Domain expertise: Quality assurance, code consistency
- Task size: 11 functions across 8 files (manageable)

**Agent-2 (Architecture & Design)**: Review missing methods (Phase 2)
- Domain expertise: Architecture, design patterns
- Task size: 8 cases to review and fix

## Success Criteria

- ✅ All 11 parameter mismatches fixed
- ✅ All 8 missing method cases resolved (implement or remove)
- ✅ No regressions introduced
- ✅ Tests pass
- ✅ Backward compatibility maintained

## Next Steps

1. **Immediate**: Delegate Phase 1 to Agent-8
2. **Immediate**: Delegate Phase 2 to Agent-2
3. **Follow-up**: Run analyzer again to verify fixes
4. **Future**: Integrate analyzer into CI/CD pipeline



