# Agent-1 Batch 4 V2 Refactoring Plan
**Date:** 2025-12-14  
**Agent:** Agent-1 (Integration & Core Systems Specialist)  
**Task:** Batch 4 - unified_onboarding_service.py Refactoring

---

## Executive Summary

**Objective:** Refactor onboarding services to V2 compliance using Handler + Helper Module Pattern

**Current State:**
- `hard_onboarding_service.py`: 870 lines (exceeds V2 limit)
- `soft_onboarding_service.py`: 533 lines (exceeds V2 limit)
- Total: 1403 lines

**Target State:**
- Unified onboarding service structure in `src/services/onboarding/`
- All modules <300 lines (V2 compliant)
- Backward compatibility shim maintained

---

## Module Extraction Strategy

### 1. Handler Modules
- `hard_onboarding_handler.py` - Hard onboarding protocol (5 steps)
- `soft_onboarding_handler.py` - Soft onboarding protocol (6 steps)
- `onboarding_coordinator.py` - Unified coordination logic

### 2. Helper Modules
- `onboarding_helpers.py` - Coordinate loading, validation, message formatting
- `onboarding_templates.py` - Message templates and agent-specific instructions
- `onboarding_protocols.py` - Protocol step implementations

### 3. Service Adapters
- `unified_onboarding_service.py` - Main service adapter (backward compatibility shim)

---

## Extraction Plan

### Phase 1: Extract Helpers
1. Extract coordinate loading/validation → `onboarding_helpers.py`
2. Extract message templates → `onboarding_templates.py`
3. Extract protocol steps → `onboarding_protocols.py`

### Phase 2: Extract Handlers
1. Extract hard onboarding handler → `hard_onboarding_handler.py`
2. Extract soft onboarding handler → `soft_onboarding_handler.py`
3. Create coordinator → `onboarding_coordinator.py`

### Phase 3: Create Shim
1. Create `unified_onboarding_service.py` shim (<300 lines)
2. Import from new modules
3. Maintain backward compatibility

### Phase 4: Validation
1. Verify V2 compliance (all modules <300 lines)
2. Run tests
3. Update imports if needed

---

## Risk Assessment

### High Risk
- **Breaking Changes:** Ensure backward compatibility maintained
- **Import Dependencies:** Update all imports to new structure

### Medium Risk
- **Test Updates:** May need to update test imports
- **Circular Dependencies:** Avoid circular imports between modules

### Low Risk
- **Functionality:** Logic remains the same, just reorganized

---

## Success Criteria

✅ All modules <300 lines  
✅ Backward compatibility maintained  
✅ All tests passing  
✅ No circular dependencies  
✅ V2 compliance verified

---

**Status:** Planning complete, ready for execution

