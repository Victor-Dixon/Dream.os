# messaging_template_texts.py Refactoring Plan

**Date:** 2025-12-14  
**Author:** Agent-2 (Architecture & Design Specialist)  
**File:** `src/core/messaging_template_texts.py`  
**Current Size:** 1,419 lines  
**Target:** ~100-150 line backward-compatibility shim + modular files (<300 lines each)  
**Priority:** HIGH (Critical Violation)  
**Status:** ⏳ PLANNING

---

## 📋 Executive Summary

This document provides a comprehensive refactoring plan for `messaging_template_texts.py` (1,419 lines), the largest Critical violation remaining. The file contains messaging template strings organized by category (S2A, D2A, C2A, A2A, A2C) and helper functions. The refactoring will split this into modular files while maintaining backward compatibility.

**Target:** Eliminate 1 Critical violation (>1000 lines)  
**Approach:** Category-based modular extraction + backward-compatibility shim  
**Pattern:** Template Module + Category Modules Pattern  
**Estimated Reduction:** 1,419 lines → ~100 line shim + 5-6 modules (<300 lines each)

---

## 🔍 Current State Analysis

### File Structure:
```
messaging_template_texts.py (1,419 lines)
├── Top-level constants (6 constants, ~280 lines)
│   ├── AGENT_OPERATING_CYCLE_TEXT
│   ├── CYCLE_CHECKLIST_TEXT
│   ├── SWARM_COORDINATION_TEXT
│   ├── DISCORD_REPORTING_TEXT
│   ├── D2A_RESPONSE_POLICY_TEXT
│   └── D2A_REPORT_FORMAT_TEXT
├── MESSAGE_TEMPLATES dictionary (~1,100 lines)
│   ├── MessageCategory.S2A (System-to-Agent templates)
│   ├── MessageCategory.D2A (Discord-to-Agent templates)
│   ├── MessageCategory.C2A (Captain-to-Agent templates)
│   ├── MessageCategory.A2A (Agent-to-Agent templates)
│   └── MessageCategory.A2C (Agent-to-Captain templates)
└── Helper functions (~40 lines)
    ├── format_d2a_payload()
    └── format_s2a_message()
```

### Dependencies:
- **Imported by:**
  - `src/core/messaging_templates.py`
  - `src/core/messaging_models_core.py`
- **Imports:**
  - `from .messaging_models import MessageCategory`
  - `from typing import Any`

### Content Breakdown:
- **Constants**: 6 top-level text constants (~280 lines)
- **Templates**: Large nested dictionary with 5 message categories (~1,100 lines)
- **Functions**: 2 helper functions (~40 lines)
- **Total**: 1,419 lines (exceeds V2 limit by 1,119 lines)

---

## 🎯 Target Architecture

### Proposed Structure:
```
src/core/messaging_templates/
├── __init__.py (~50 lines) - Backward compatibility shim
├── constants.py (~280 lines) - Top-level text constants
├── s2a_templates.py (~250 lines) - S2A (System-to-Agent) templates
├── d2a_templates.py (~150 lines) - D2A (Discord-to-Agent) templates
├── c2a_templates.py (~200 lines) - C2A (Captain-to-Agent) templates
├── a2a_templates.py (~200 lines) - A2A (Agent-to-Agent) templates
├── a2c_templates.py (~150 lines) - A2C (Agent-to-Captain) templates
└── formatters.py (~50 lines) - Helper functions (format_d2a_payload, format_s2a_message)
```

### Backward Compatibility:
- `src/core/messaging_template_texts.py` becomes ~100 line shim
- Re-exports all public APIs from modular files
- Maintains exact import paths for existing code

---

## 📐 Refactoring Strategy

### Pattern: Template Module + Category Modules Pattern

**Principle:** Split templates by message category while maintaining unified access via backward-compatibility shim.

**Benefits:**
- Clear separation by message category
- Each module <300 lines (V2 compliant)
- Easy to maintain and extend
- Backward compatible (no breaking changes)

### Phase Breakdown:

#### Phase 1: Extract Constants Module
- **Target:** `src/core/messaging_templates/constants.py`
- **Content:** All 6 top-level text constants
- **Size:** ~280 lines
- **Exports:** All 6 constants

#### Phase 2: Extract Category Modules
- **Target:** 5 category-specific template files
  - `s2a_templates.py` - S2A templates (~250 lines)
  - `d2a_templates.py` - D2A templates (~150 lines)
  - `c2a_templates.py` - C2A templates (~200 lines)
  - `a2a_templates.py` - A2A templates (~200 lines)
  - `a2c_templates.py` - A2C templates (~150 lines)
- **Content:** Template dictionaries for each category
- **Exports:** Category-specific template dictionaries

#### Phase 3: Extract Formatters Module
- **Target:** `src/core/messaging_templates/formatters.py`
- **Content:** Helper functions (`format_d2a_payload`, `format_s2a_message`)
- **Size:** ~50 lines
- **Exports:** Both helper functions

#### Phase 4: Create Unified Templates Module
- **Target:** `src/core/messaging_templates/templates.py`
- **Content:** Combines all category templates into MESSAGE_TEMPLATES dict
- **Size:** ~80 lines
- **Exports:** MESSAGE_TEMPLATES dictionary

#### Phase 5: Create Backward Compatibility Shim
- **Target:** `src/core/messaging_template_texts.py` (replacement)
- **Content:** Imports and re-exports all public APIs
- **Size:** ~100 lines
- **Exports:** All original exports (maintains __all__)

---

## 🔧 Implementation Details

### Module Structure:

#### constants.py:
```python
"""Messaging template constants."""
AGENT_OPERATING_CYCLE_TEXT = (...)
CYCLE_CHECKLIST_TEXT = (...)
SWARM_COORDINATION_TEXT = (...)
DISCORD_REPORTING_TEXT = (...)
D2A_RESPONSE_POLICY_TEXT = (...)
D2A_REPORT_FORMAT_TEXT = (...)
```

#### s2a_templates.py:
```python
"""S2A (System-to-Agent) message templates."""
from typing import Any
from ..messaging_models import MessageCategory

S2A_TEMPLATES: dict[str, Any] = {
    "CONTROL": (...),
    "STALL_RECOVERY": (...),
    # ... all S2A templates
}
```

#### templates.py:
```python
"""Unified message templates dictionary."""
from typing import Any
from .s2a_templates import S2A_TEMPLATES
from .d2a_templates import D2A_TEMPLATES
from .c2a_templates import C2A_TEMPLATES
from .a2a_templates import A2A_TEMPLATES
from .a2c_templates import A2C_TEMPLATES
from ..messaging_models import MessageCategory

MESSAGE_TEMPLATES: dict[MessageCategory, Any] = {
    MessageCategory.S2A: S2A_TEMPLATES,
    MessageCategory.D2A: D2A_TEMPLATES,
    MessageCategory.C2A: C2A_TEMPLATES,
    MessageCategory.A2A: A2A_TEMPLATES,
    MessageCategory.A2C: A2C_TEMPLATES,
}
```

#### messaging_template_texts.py (shim):
```python
"""Messaging Templates - Backward Compatibility Shim."""
from __future__ import annotations

# Re-export all from modular files
from .messaging_templates.constants import (
    AGENT_OPERATING_CYCLE_TEXT,
    CYCLE_CHECKLIST_TEXT,
    SWARM_COORDINATION_TEXT,
    DISCORD_REPORTING_TEXT,
    D2A_RESPONSE_POLICY_TEXT,
    D2A_REPORT_FORMAT_TEXT,
)
from .messaging_templates.templates import MESSAGE_TEMPLATES
from .messaging_templates.formatters import format_d2a_payload, format_s2a_message

__all__ = [
    "MESSAGE_TEMPLATES",
    "AGENT_OPERATING_CYCLE_TEXT",
    "CYCLE_CHECKLIST_TEXT",
    "DISCORD_REPORTING_TEXT",
    "D2A_RESPONSE_POLICY_TEXT",
    "D2A_REPORT_FORMAT_TEXT",
    "format_d2a_payload",
    "format_s2a_message",
]
```

---

## 📊 Expected Results

### File Size Reduction:
- **Before:** 1,419 lines (1 file)
- **After:** ~100 line shim + 7 modular files (<300 lines each)
- **Reduction:** 93% reduction in main file size
- **Compliance:** 100% V2 compliant (all files <300 lines)

### Module Breakdown:
```
messaging_template_texts.py: ~100 lines (shim) ✅
messaging_templates/
├── __init__.py: ~50 lines ✅
├── constants.py: ~280 lines ✅
├── templates.py: ~80 lines ✅
├── s2a_templates.py: ~250 lines ✅
├── d2a_templates.py: ~150 lines ✅
├── c2a_templates.py: ~200 lines ✅
├── a2a_templates.py: ~200 lines ✅
├── a2c_templates.py: ~150 lines ✅
└── formatters.py: ~50 lines ✅
```

### Compliance Impact:
- **Before:** 1 Critical violation (>1000 lines)
- **After:** 0 violations (all files <300 lines)
- **Compliance Improvement:** 87.7% → 87.8% (1 violation eliminated)

---

## ⚠️ Risk Assessment

### Identified Risks:

1. **Import Path Changes**
   - **Risk:** Breaking changes to imports
   - **Mitigation:** Backward-compatibility shim maintains exact import paths
   - **Severity:** LOW (shim prevents breaking changes)

2. **Circular Dependencies**
   - **Risk:** Circular imports between modules
   - **Mitigation:** Clear dependency hierarchy (constants → templates → category modules → shim)
   - **Severity:** LOW (proper import order prevents cycles)

3. **Template Dictionary Structure**
   - **Risk:** MESSAGE_TEMPLATES dict structure changes
   - **Mitigation:** Maintain exact structure in templates.py
   - **Severity:** LOW (structure preserved)

4. **Testing Requirements**
   - **Risk:** Import tests may fail
   - **Mitigation:** Verify all imports work after refactoring
   - **Severity:** MEDIUM (requires testing)

### Dependency Risks:
- ✅ **Breaking Changes:** None (shim maintains API)
- ✅ **Import Paths:** Backward compatible via shim
- ✅ **Public API:** All exports preserved

---

## ✅ Success Criteria

### Completion Criteria:
- [ ] All modules created and V2 compliant (<300 lines each)
- [ ] Backward-compatibility shim created (~100 lines)
- [ ] All imports work (messaging_templates.py, messaging_models_core.py)
- [ ] MESSAGE_TEMPLATES structure maintained
- [ ] All constants accessible via original import paths
- [ ] Helper functions work correctly
- [ ] No breaking changes to dependent code
- [ ] V2 compliance verified (0 violations)

### Testing Requirements:
- [ ] Import tests pass
- [ ] Template access tests pass
- [ ] Formatter function tests pass
- [ ] Integration tests pass

---

## 📅 Implementation Timeline

### Estimated Effort: 2-3 cycles

**Phase 1-2** (Cycle 1): Extract constants and category modules  
**Phase 3-4** (Cycle 2): Extract formatters and create unified templates  
**Phase 5** (Cycle 3): Create shim and integration testing

---

## 🔗 Related Documents

- V2 Compliance Dashboard: `docs/v2_compliance/V2_COMPLIANCE_DASHBOARD.md`
- Comprehensive Violation Report: `docs/v2_compliance/COMPREHENSIVE_V2_VIOLATION_REPORT_2025-12-14.md`
- Architecture Patterns: Handler + Helper, Template Module patterns

---

## 📝 Notes

- This file contains canonical policy text and template strings (SSOT domain: integration)
- Templates are used extensively throughout the messaging system
- Backward compatibility is critical (2 importing files)
- Category-based extraction provides clear organization and maintainability

---

**Architecture Plan:** Agent-2  
**Status:** ✅ **READY FOR EXECUTION**  
**Date:** 2025-12-14

---

**WE. ARE. SWARM!** 🐝⚡
