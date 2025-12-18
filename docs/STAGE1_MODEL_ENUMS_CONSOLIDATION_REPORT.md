# Model Enums Consolidation Report
**Date**: 2025-12-17  
**Agent**: Agent-5  
**Task**: A5-STAGE1-DUPLICATE-001  
**Purpose**: Consolidate duplicate model enum classes per duplication check findings

---

## 📋 Consolidation Plan

### SSOT Designation
- **SSOT**: `src/core/coordination/swarm/coordination_models.py` ✅
- **Deprecated**: Various duplicate locations ⚠️

### Enum Mappings

| Enum Class | Duplicate Locations | SSOT Location | Notes |
|------------|---------------------|---------------|-------|
| TaskStatus | `src/services/contract_system/models.py`<br>`src/core/managers/execution/execution_operations.py` | `src/core/coordination/swarm/coordination_models.py` | SSOT: PENDING, IN_PROGRESS, COMPLETED, FAILED<br>Duplicates may have additional values (CANCELLED, RUNNING) |
| Priority | `src/core/intelligent_context/unified_intelligent_context/models.py` | `src/core/coordination/swarm/coordination_models.py` | SSOT: TaskPriority (LOW, MEDIUM, HIGH, CRITICAL)<br>Use TaskPriority or create alias |
| CoordinationStrategy | `src/workflows/models.py` | `src/core/coordination/swarm/coordination_models.py` | SSOT: COLLABORATIVE, INDEPENDENT, HIERARCHICAL<br>Workflows has different values (PARALLEL, SEQUENTIAL, etc.) - may need migration strategy |

---

## ⚠️ Important Notes

### TaskStatus Differences
- **SSOT**: PENDING, IN_PROGRESS, COMPLETED, FAILED
- **contract_system**: Also has CANCELLED
- **execution_operations**: Has RUNNING instead of IN_PROGRESS, also has CANCELLED

**Migration Strategy**: Map RUNNING → IN_PROGRESS, handle CANCELLED separately or add to SSOT if needed.

### Priority Differences
- **SSOT**: TaskPriority (LOW, MEDIUM, HIGH, CRITICAL)
- **unified_intelligent_context**: Priority (LOW, MEDIUM, HIGH, CRITICAL) - same values, different name

**Migration Strategy**: Simple rename/alias to TaskPriority.

### CoordinationStrategy Differences
- **SSOT**: COLLABORATIVE, INDEPENDENT, HIERARCHICAL
- **workflows**: PARALLEL, SEQUENTIAL, DECISION_TREE, AUTONOMOUS

**Migration Strategy**: These represent different concepts. May need to:
1. Keep both with different names
2. Create mapping between them
3. Expand SSOT to include both sets

---

## ✅ Consolidation Steps

1. **Add Deprecation Warnings**
   - Add deprecation warnings to duplicate enum files
   - Direct users to SSOT locations
   - Include migration notes

2. **Verify Enum Compatibility**
   - Check if duplicate enums have additional values needed in SSOT
   - Determine if SSOT needs expansion or if values can be mapped

3. **Update Imports**
   - Update all imports from duplicate locations to SSOT
   - Handle value mapping where necessary

4. **Create Migration Guide**
   - Document value mappings
   - Provide code examples for migration

5. **Remove Deprecated Files**
   - After migration complete, remove duplicate enum definitions
   - Update documentation

---

## 📊 Expected Impact

- **Duplicate Classes Eliminated**: ~5 (TaskStatus x2, Priority x1, CoordinationStrategy x1, plus related)
- **Code Consolidation**: Multiple locations → SSOT coordination models
- **Maintainability**: Single source of truth for model enums

---

## 🔄 Next Steps

1. Review enum value differences between duplicates and SSOT
2. Determine if SSOT needs expansion or if mapping is sufficient
3. Add deprecation warnings to duplicate enum files
4. Create value mapping documentation
5. Update imports across codebase
6. Test functionality
7. Remove deprecated enum definitions after migration

---

🐝 **WE. ARE. SWARM. ⚡🔥**
