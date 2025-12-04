# 🗺️ MASTER DEPENDENCY MAP

**Date**: 2025-12-03  
**Status**: ACTIVE  
**Purpose**: Comprehensive mapping of all import dependencies across the project  
**Maintained By**: Agent-2 (Architecture & Design Specialist)

---

## 🎯 OVERVIEW

This document serves as the **Single Source of Truth (SSOT)** for all import dependencies in the project. It tracks:
- Module dependencies
- Common import patterns
- Known broken imports
- Fix status and progress

---

## 📊 DEPENDENCY CATEGORIES

### **Category 1: Standard Library Imports**
Common Python standard library imports used across the project:
- `typing` (Dict, List, Callable, Optional, Union, Any)
- `logging`
- `dataclasses` (dataclass, field)
- `enum` (Enum)
- `pathlib` (Path)
- `json`, `datetime`, `os`, `sys`

### **Category 2: Core Module Imports**
Core project modules and their dependencies:
- `src.core.*` - Core functionality
- `src.services.*` - Service layer
- `src.utils.*` - Utility functions
- `src.infrastructure.*` - Infrastructure layer

### **Category 3: External Dependencies**
Third-party packages (tracked in requirements.txt):
- PyQt6, selenium, etc.

---

## 🔴 KNOWN BROKEN IMPORTS (By Category)

### **1. Missing Type Imports** (~50 files)
**Error Pattern**: `name 'Dict' is not defined`, `name 'List' is not defined`, etc.

**Affected Areas**:
- `src/core/performance/*` (11 files)
- `src/trading_robot/*` (~30 files)
- `src/integrations/jarvis/*` (4 files)
- `src/tools/duplicate_detection/*` (4 files)
- `src/gaming/*` (~5 files)

**Fix**: Add `from typing import Dict, List, Callable, Any, Optional, Union`

**Status**: 🔄 IN PROGRESS

---

### **2. Missing Logging Imports** (~10 files)
**Error Pattern**: `name 'logging' is not defined`

**Affected Files**:
- `src/core/documentation_indexing_service.py`
- `src/core/documentation_search_service.py`
- `src/core/search_history_service.py`
- `src/gaming/handlers/gaming_alert_handlers.py`
- `src/gaming/utils/*` (3 files)

**Fix**: Add `import logging`

**Status**: 🔄 IN PROGRESS

---

### **3. Missing Dataclass Imports** (~5 files)
**Error Pattern**: `name 'dataclass' is not defined`

**Affected Files**:
- `src/core/utils/agent_matching.py`
- `src/core/utils/coordination_utils.py`
- `src/core/utils/message_queue_utils.py`
- `src/core/utils/simple_utils.py`

**Fix**: Add `from dataclasses import dataclass, field`

**Status**: 🔄 IN PROGRESS

---

### **4. Missing Enum Imports** (~2 files)
**Error Pattern**: `name 'Enum' is not defined`

**Affected Files**:
- `src/gaming/models/gaming_alert_models.py`
- `src/gaming/models/gaming_models.py`

**Fix**: Add `from enum import Enum`

**Status**: 🔄 IN PROGRESS

---

### **5. Missing Path Imports** (~2 files)
**Error Pattern**: `name 'Path' is not defined`

**Affected Files**:
- `src/tools/duplicate_detection/find_duplicates.py`
- `src/tools/duplicate_detection/file_hash.py`

**Fix**: Add `from pathlib import Path`

**Status**: 🔄 IN PROGRESS

---

### **6. Missing Union Import** (~1 file)
**Error Pattern**: `name 'Union' is not defined`

**Affected Files**:
- `src/gaming/dreamos/resumer_v2/atomic_file_manager.py`

**Fix**: Add `from typing import Union`

**Status**: 🔄 IN PROGRESS

---

### **7. Syntax Errors** (~15 files)
**Error Pattern**: `non-default argument 'task_id' follows default argument`

**Affected Areas**:
- `src/domain/*` (8 files)
- `src/infrastructure/*` (7 files)

**Fix**: Reorder function parameters (non-default before default)

**Status**: ⏳ PENDING

---

### **8. Missing Modules** (~20 files)
**Error Pattern**: `No module named 'X'`

**Common Missing Modules**:
- `src.services.vector_database` (7 files)
- `src.core.managers.execution.task_manager` (~20 files)
- `src.core.deployment.deployment_coordinator` (10 files)
- `src.core.enhanced_integration.integration_models` (9 files)
- Others

**Status**: ⏳ PENDING (Requires architectural decisions)

---

### **9. Circular Dependencies** (~25 files)
**Error Pattern**: `cannot import name 'X' from partially initialized module`

**Affected Areas**:
- `src/core/engines/*` (18 files) - `base_engine` circular import
- `src/core/error_handling/*` (20 files) - `CircuitBreaker` circular import
- `src/core/file_locking/*` (7 files) - `file_locking_engine_base` circular import
- `src/core/integration_coordinators/*` (10 files) - `messaging_coordinator` circular import
- Others

**Status**: ⏳ PENDING (Requires architectural refactoring)

---

## 📈 PROGRESS TRACKING

### **Fixed** ✅
- None yet (starting now)

### **In Progress** 🔄
- Category 1: Missing Type Imports
- Category 2: Missing Logging Imports
- Category 3: Missing Dataclass Imports
- Category 4: Missing Enum Imports
- Category 5: Missing Path Imports
- Category 6: Missing Union Import

### **Pending** ⏳
- Category 7: Syntax Errors
- Category 8: Missing Modules
- Category 9: Circular Dependencies

---

## 🔧 FIX TEMPLATES

### **Template 1: Missing Type Imports**
```python
# Add to top of file (after other imports)
from typing import Dict, List, Callable, Any, Optional, Union
```

### **Template 2: Missing Logging**
```python
# Add to top of file
import logging
```

### **Template 3: Missing Dataclass**
```python
# Add to top of file
from dataclasses import dataclass, field
```

### **Template 4: Missing Enum**
```python
# Add to top of file
from enum import Enum
```

### **Template 5: Missing Path**
```python
# Add to top of file
from pathlib import Path
```

---

## 📝 NOTES

- This map is updated as fixes are applied
- Priority: Fix easy wins first (Categories 1-6), then tackle architectural issues (Categories 7-9)
- Use `tools/import_chain_validator.py` to validate fixes
- Update `quarantine/BROKEN_IMPORTS.md` as errors are resolved

---

**Last Updated**: 2025-12-03  
**Next Review**: After each fix batch

