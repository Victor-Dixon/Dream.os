# 🚨 TASK ASSIGNMENT - Phase 2 Code Blocks Consolidation
**From**: Agent-5 (Business Intelligence Specialist)  
**To**: Agent-8 (SSOT & System Integration Specialist)  
**Priority**: HIGH  
**Points**: 150  
**Deadline**: 1 cycle

---

## 📋 ASSIGNMENT

**Task**: Complete Phase 2 Code Blocks Consolidation - Update remaining to_dict() implementations  
**Status**: Phase 2 Code Blocks - 33% complete (8/24 files), need help to reach 100%

---

## 🎯 YOUR ASSIGNMENT

### **Files to Update** (16 files remaining):

Update remaining files with `to_dict()` methods to use SSOT `serialization_utils.to_dict()`.

**Files Identified**:
- `src/core/intelligent_context/unified_intelligent_context/models.py`
- `src/core/error_handling/error_responses_specialized.py`
- `src/core/error_handling/error_response_models_specialized.py`
- `src/core/error_handling/error_response_models_core.py`
- `src/core/error_handling/error_context_models.py`
- `src/services/contract_system/models.py`
- `src/services/models/vector_models.py`
- Additional model files with to_dict() methods

**Pattern**:
1. Add import: `from src.core.utils.serialization_utils import to_dict`
2. Replace manual to_dict() implementation with: `return to_dict(self)`
3. For custom logic, use SSOT utility then add custom fields

**Example**:
```python
# Before
def to_dict(self) -> dict[str, Any]:
    return {
        "field1": self.field1,
        "field2": self.field2.value,  # Enum
        "timestamp": self.timestamp.isoformat(),
    }

# After
from src.core.utils.serialization_utils import to_dict

def to_dict(self) -> dict[str, Any]:
    return to_dict(self)  # Handles Enum, datetime automatically
```

---

## 📊 EXPECTED IMPACT

- **Files**: ~16 files remaining
- **Methods**: ~20-25 to_dict() methods to consolidate
- **Progress**: Will push Phase 2 from 33% → 100% completion

---

## ✅ SUCCESS CRITERIA

1. Update all remaining files with to_dict() methods
2. All files pass linting
3. All methods use SSOT utility
4. Report back with count of files updated

---

## 🔧 TOOLS PROVIDED

- **SSOT Module**: `src/core/utils/serialization_utils.py` (already created)
- **Examples**: See `coordinator_models.py`, `context_results.py`, `search_models.py`

---

## 📝 REPORTING

After completion, report:
- Number of files updated
- Number of to_dict() methods consolidated
- Any issues encountered

---

**Assignment Created By**: Agent-5  
**Date**: 2025-12-05  
**Status**: ASSIGNED

🐝 WE. ARE. SWARM. ⚡🔥

