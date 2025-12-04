# 🔍 SSOT Identification & Duplicate Cleanup Guide

**Date**: 2025-12-03  
**Context**: Circular Imports Team Assignment  
**Principle**: **This is how we clean the project** - Identify SSOTs and cleanup duplicates while fixing issues

---

## 🎯 CORE PRINCIPLE

**While fixing circular imports, identify SSOTs and clean up duplicates** - This is how we systematically clean the project!

---

## 📋 SSOT IDENTIFICATION PROCESS

### **Step 1: Identify Duplicate Patterns**

Look for:
- **Multiple classes doing the same thing** (e.g., `BaseEngine`, `EngineBase`, `BaseEngineClass`)
- **Duplicate initialization logic** (same `__init__` patterns across files)
- **Repeated error handling** (same try/except blocks)
- **Similar validation logic** (duplicate validation functions)
- **Repeated type definitions** (same enums/classes in multiple files)
- **Duplicate utility functions** (same helper functions)

### **Step 2: Designate SSOT**

Choose the **canonical implementation**:
- ✅ Most complete/feature-rich
- ✅ Best documented
- ✅ Most widely used
- ✅ Best location (follows architecture)
- ✅ V2 compliant

### **Step 3: Tag SSOT**

Add SSOT domain tag as **first line** of file:

```python
<!-- SSOT Domain: integration -->
"""
Base Engine - Single Source of Truth
====================================
...
"""
```

**SSOT Domain Options**:
- `integration` - Core systems, messaging, integration patterns
- `architecture` - Design patterns, structure
- `infrastructure` - DevOps, monitoring, tools
- `analytics` - Business intelligence, metrics
- `communication` - Messaging, coordination
- `qa` - Testing, validation

### **Step 4: Refactor Duplicates**

Update other files to use SSOT:

```python
# BEFORE (Duplicate):
class EngineBase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

# AFTER (Use SSOT):
from src.core.common.base_engine import BaseEngine

class MyEngine(BaseEngine):
    def __init__(self):
        super().__init__()
```

### **Step 5: Remove Redundant Code**

- Delete duplicate files if fully replaced
- Archive deprecated implementations
- Update imports across codebase
- Document consolidation in report

---

## 🔍 COMMON DUPLICATE PATTERNS

### **Pattern 1: Multiple Base Classes**

**Example**:
- `BaseEngine` in `src/core/common/base_engine.py`
- `EngineBase` in `src/core/engines/engine_base.py`
- `BaseEngineClass` in `src/core/engines/base.py`

**SSOT**: Choose one canonical base class, consolidate others

---

### **Pattern 2: Duplicate Initialization Logic**

**Example**:
```python
# File 1:
def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.status = "initialized"

# File 2:
def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.status = "initialized"
```

**SSOT**: Extract to base class or utility function

---

### **Pattern 3: Repeated Error Handling**

**Example**:
```python
# Multiple files with same pattern:
try:
    result = operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    return None
```

**SSOT**: Create error handler utility or decorator

---

### **Pattern 4: Duplicate Validation Logic**

**Example**:
- Same validation functions in multiple files
- Repeated parameter checking
- Duplicate type validation

**SSOT**: Consolidate into validation utility module

---

### **Pattern 5: Repeated Type Definitions**

**Example**:
- Same enums in multiple files
- Duplicate model classes
- Repeated constants

**SSOT**: Move to shared models/types module

---

## 📝 DOCUMENTATION REQUIREMENTS

### **For Each SSOT Identified**:

1. **SSOT File**: Location and name
2. **Domain Tag**: Which SSOT domain
3. **Duplicates Found**: List of duplicate files/patterns
4. **Consolidation Actions**: What was refactored
5. **Files Updated**: List of files now using SSOT
6. **Files Removed**: List of duplicate files deleted/archived

### **Report Template**:

```markdown
## SSOT: BaseEngine

**File**: `src/core/common/base_engine.py`
**Domain**: `integration`
**Tag**: `<!-- SSOT Domain: integration -->`

**Duplicates Found**:
- `src/core/engines/engine_base.py` - Duplicate base class
- `src/core/engines/base.py` - Duplicate base class

**Consolidation Actions**:
- Updated 15 engine files to use SSOT BaseEngine
- Removed duplicate engine_base.py
- Archived base.py to deprecated/

**Files Updated**: 15 files
**Files Removed**: 2 files
```

---

## ✅ CHECKLIST FOR EACH AGENT

- [ ] Identify duplicate patterns in assigned chain
- [ ] Designate SSOT for each duplicate group
- [ ] Tag SSOT files with domain tags
- [ ] Refactor duplicates to use SSOT
- [ ] Remove redundant code
- [ ] Document findings in assignment report
- [ ] Update imports across codebase
- [ ] Verify no regressions

---

## 🎯 EXAMPLES FROM PREVIOUS WORK

### **Example 1: Coordinate Loader Consolidation** (Agent-1)

**SSOT**: `src/core/coordinate_loader.py`
**Duplicates**:
- `src/services/handlers/coordinate_handler.py` - `load_coordinates_async()`
- `src/services/messaging_cli_coordinate_management/utilities.py` - `load_coords_file()`

**Result**: Both duplicates refactored to use `get_coordinate_loader()` from SSOT

---

### **Example 2: Soft Onboarding Circular Import Fix** (Agent-1)

**Pattern**: Lazy Import Pattern
**SSOT**: `src/services/soft_onboarding_service.py`
**Fix**: Used lazy loading to break circular dependency

---

## 🚀 INTEGRATION WITH CIRCULAR IMPORT FIXES

**Workflow**:
1. **Fix circular import** (primary task)
2. **While fixing, identify duplicates** (SSOT opportunity)
3. **Designate SSOT** (consolidation)
4. **Refactor to use SSOT** (cleanup)
5. **Document findings** (knowledge sharing)

**This is how we clean the project** - Fix issues AND consolidate duplicates simultaneously!

---

**Status**: ✅ Guide created, ready for team use  
**Integration**: Part of Circular Imports Team Assignment

🐝 WE. ARE. SWARM. ⚡🔥

