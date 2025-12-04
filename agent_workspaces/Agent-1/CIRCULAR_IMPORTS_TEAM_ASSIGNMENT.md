# 🔄 Circular Imports Team Assignment

**Date**: 2025-12-03  
**Priority**: HIGH (Blocks other import fixes)  
**Status**: TEAM ASSEMBLED - Ready for Execution  
**Team**: Agent-1 (Coordinator), Agent-5, Agent-7, Agent-2 (Architecture Review)

---

## 🎯 MISSION

Fix all circular import issues in the codebase using proven patterns (Lazy Import Pattern, TYPE_CHECKING, dependency injection).

**CRITICAL**: While fixing circular imports, **IDENTIFY SSOTs AND CLEAN UP DUPLICATES** - This is how we clean the project!

**Total Circular Import Chains**: 4 major chains, ~30 files affected

---

## 📊 CIRCULAR IMPORT CHAINS IDENTIFIED

### **Chain 1: `src.core.engines` - base_engine** (~15 files) 🔴 HIGH PRIORITY

**Error Pattern**:
```
cannot import name 'base_engine' from partially initialized module 'src.core.engines' 
(most likely due to a circular import)
```

**Affected Files** (from `quarantine/BROKEN_IMPORTS.md`):
1. `src/core/engines/coordination/coordination_engine.py`
2. `src/core/engines/coordination/coordination_engine_base.py`
3. `src/core/engines/coordination/coordination_engine_factory.py`
4. `src/core/engines/coordination/coordination_engine_manager.py`
5. `src/core/engines/coordination/coordination_engine_registry.py`
6. `src/core/engines/coordination/coordination_engine_utils.py`
7. `src/core/engines/coordination/coordination_engine_validator.py`
8. `src/core/engines/execution/execution_engine.py`
9. `src/core/engines/execution/execution_engine_base.py`
10. `src/core/engines/execution/execution_engine_factory.py`
11. `src/core/engines/execution/execution_engine_manager.py`
12. `src/core/engines/execution/execution_engine_registry.py`
13. `src/core/engines/execution/execution_engine_utils.py`
14. `src/core/engines/execution/execution_engine_validator.py`
15. `src/core/engines/execution/execution_engine_wrapper.py`

**Root Cause**: `src/core/engines/__init__.py` likely imports `base_engine` from `src.core.common.base_engine`, but files in engines/ try to import `base_engine` from `src.core.engines`, creating circular dependency

**Actual Location**: `base_engine` is in `src/core/common/base_engine.py` (not in engines/)

**Fix Strategy**: 
- Update imports in engines/ files to use `from src.core.common.base_engine import BaseEngine`
- Use TYPE_CHECKING for type hints in `__init__.py`
- Lazy imports in `__init__.py` if needed
- Verify `__init__.py` doesn't create circular dependency

**Assigned To**: **Agent-5** (Business Intelligence - Good at architectural patterns)

**SSOT & Duplicate Cleanup Tasks**:
1. Identify duplicate base engine patterns across engines/
2. Consolidate similar engine initialization logic
3. Find duplicate validation/error handling patterns
4. Tag SSOT files with `<!-- SSOT Domain: integration -->`
5. Document duplicates found in assignment report

---

### **Chain 2: `src.core.emergency_intervention.unified_emergency` - orchestrator** (~7 files) 🔴 HIGH PRIORITY

**Error Pattern**:
```
cannot import name 'orchestrator' from partially initialized module 
'src.core.emergency_intervention.unified_emergency' (most likely due to a circular import)
```

**Affected Files**:
1. `src/core/emergency_intervention/unified_emergency/engines/emergency_coordination_engine.py`
2. `src/core/emergency_intervention/unified_emergency/engines/emergency_detection_engine.py`
3. `src/core/emergency_intervention/unified_emergency/engines/emergency_execution_engine.py`
4. `src/core/emergency_intervention/unified_emergency/engines/emergency_recovery_engine.py`
5. `src/core/emergency_intervention/unified_emergency/engines/emergency_response_engine.py`
6. `src/core/emergency_intervention/unified_emergency/engines/emergency_validation_engine.py`
7. `src/core/emergency_intervention/unified_emergency/engines/emergency_verification_engine.py`

**Root Cause**: `__init__.py` imports `orchestrator` which imports from engines, creating circular dependency

**Fix Strategy**:
- Lazy import pattern (like soft_onboarding_service fix)
- TYPE_CHECKING for type hints
- Extract orchestrator to separate module if needed

**Assigned To**: **Agent-7** (Web Development - Good at refactoring and patterns)

**Note**: Directory `src/core/emergency_intervention/unified_emergency/` may not exist - verify before starting

**SSOT & Duplicate Cleanup Tasks**:
1. Identify duplicate orchestrator patterns
2. Consolidate similar engine base classes
3. Find duplicate protocol/validation logic
4. Tag SSOT files with appropriate domain tags
5. Document duplicates found in assignment report

---

### **Chain 3: `src.core.file_locking` - file_locking_engine_base** (~6 files) 🟡 MEDIUM PRIORITY

**Error Pattern**:
```
cannot import name 'file_locking_engine_base' from partially initialized module 
'src.core.file_locking' (most likely due to a circular import)
```

**Affected Files**:
1. `src/core/file_locking/engines/file_locking_coordination_engine.py`
2. `src/core/file_locking/engines/file_locking_detection_engine.py`
3. `src/core/file_locking/engines/file_locking_execution_engine.py`
4. `src/core/file_locking/engines/file_locking_recovery_engine.py`
5. `src/core/file_locking/engines/file_locking_validation_engine.py`
6. `src/core/file_locking/engines/file_locking_verification_engine.py`

**Root Cause**: `__init__.py` imports `file_locking_engine_base` which imports from engines

**Fix Strategy**:
- Lazy import pattern
- TYPE_CHECKING for type hints
- Similar pattern to Chain 2

**Assigned To**: **Agent-7** (Can handle after Chain 2 - similar pattern)

---

### **Chain 4: `src.core.integration_coordinators` - messaging_coordinator** (~10 files) 🟡 MEDIUM PRIORITY

**Error Pattern**:
```
cannot import name 'messaging_coordinator' from partially initialized module 
'src.core.integration_coordinators' (most likely due to a circular import)
```

**Affected Files** (need to verify exact list):
- Multiple files importing from `src.core.integration_coordinators`

**Root Cause**: `__init__.py` imports `messaging_coordinator` which imports from integration_coordinators

**Fix Strategy**:
- Lazy import pattern
- TYPE_CHECKING for type hints
- Dependency injection if appropriate

**Assigned To**: **Agent-1** (Integration & Core Systems - Own domain)

**Note**: Directory `src/core/integration_coordinators/` may not exist - verify before starting

**SSOT & Duplicate Cleanup Tasks**:
1. Identify duplicate coordinator patterns
2. Consolidate messaging coordinator logic
3. Find duplicate integration patterns
4. Tag SSOT files with `<!-- SSOT Domain: integration -->`
5. Document duplicates found in assignment report

---

## 🔍 SSOT IDENTIFICATION & DUPLICATE CLEANUP

**REQUIRED**: As you fix circular imports, identify and consolidate duplicates:

### **SSOT Identification Checklist**:
1. ✅ **Identify duplicate patterns** - Look for similar code/logic across files
2. ✅ **Designate SSOT** - Choose canonical implementation
3. ✅ **Tag with SSOT domain** - Add `<!-- SSOT Domain: {domain} -->` tag
4. ✅ **Refactor duplicates** - Update other files to use SSOT
5. ✅ **Remove redundant code** - Delete or archive duplicates

### **Common Duplicate Patterns to Look For**:
- **Multiple base classes** doing the same thing
- **Duplicate initialization logic** across engines
- **Repeated error handling patterns**
- **Similar validation logic** in multiple files
- **Duplicate type definitions** or enums
- **Repeated utility functions**

### **SSOT Domain Tags**:
- `<!-- SSOT Domain: integration -->` - Core systems, messaging, integration
- `<!-- SSOT Domain: architecture -->` - Design patterns, structure
- `<!-- SSOT Domain: infrastructure -->` - DevOps, monitoring, tools
- `<!-- SSOT Domain: analytics -->` - Business intelligence, metrics
- `<!-- SSOT Domain: communication -->` - Messaging, coordination
- `<!-- SSOT Domain: qa -->` - Testing, validation

### **Example SSOT Consolidation**:
```python
# BEFORE (Duplicate):
# file1.py
class BaseEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

# file2.py  
class EngineBase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

# AFTER (SSOT):
# src/core/common/base_engine.py (SSOT)
<!-- SSOT Domain: integration -->
class BaseEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

# file1.py, file2.py - Use SSOT
from src.core.common.base_engine import BaseEngine
```

---

## 🛠️ PROVEN PATTERNS TO USE

### **Pattern 1: Lazy Import Pattern** ✅ (Already Used Successfully)

**Example**: `soft_onboarding_service.py` fix

```python
class Service:
    def __init__(self):
        # Don't import at module level - avoid circular import
        self._dependency = None
    
    @property
    def dependency(self):
        """Lazy-load dependency to avoid circular import."""
        if self._dependency is None:
            from .dependency_module import Dependency
            self._dependency = Dependency()
        return self._dependency
```

**Documentation**: `swarm_brain/patterns/LAZY_IMPORT_PATTERN_2025-01-27.md`

---

### **Pattern 2: TYPE_CHECKING Imports**

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .other_module import SomeClass

# Use SomeClass only in type hints, not at runtime
def func(param: 'SomeClass') -> None:
    pass
```

---

### **Pattern 3: Dependency Injection**

Instead of importing directly, pass dependencies as parameters:

```python
# Instead of:
from .other_module import Dependency
class Service:
    def __init__(self):
        self.dep = Dependency()

# Use:
class Service:
    def __init__(self, dependency: Dependency):
        self.dep = dependency
```

---

## 📋 TEAM ASSIGNMENTS

### **Agent-5** (Business Intelligence Specialist)
- **Assignment**: Chain 1 - `src.core.engines` base_engine circular import (~15 files)
- **Priority**: HIGH
- **Estimated Time**: 2-3 hours
- **Approach**: 
  1. Analyze `src/core/engines/__init__.py` and `base_engine.py`
  2. Identify circular dependency path
  3. Apply TYPE_CHECKING and lazy imports
  4. Refactor if needed to break cycle
  5. Test all 15 files

---

### **Agent-7** (Web Development Specialist)
- **Assignment**: Chain 2 & 3 - Emergency intervention & File locking (~13 files)
- **Priority**: HIGH (Chain 2), MEDIUM (Chain 3)
- **Estimated Time**: 2-3 hours
- **Approach**:
  1. Start with Chain 2 (emergency_intervention) - 7 files
  2. Use Lazy Import Pattern (proven with soft_onboarding_service)
  3. Apply same pattern to Chain 3 (file_locking) - 6 files
  4. Test all files

---

### **Agent-1** (Integration & Core Systems Specialist - Coordinator)
- **Assignment**: Chain 4 - `src.core.integration_coordinators` (~10 files)
- **Priority**: MEDIUM
- **Estimated Time**: 1-2 hours
- **Approach**:
  1. Analyze integration_coordinators circular dependency
  2. Apply appropriate pattern (lazy import or TYPE_CHECKING)
  3. Test all files
  4. Coordinate team progress

---

### **Agent-2** (Architecture & Design Specialist)
- **Role**: Architecture Review & Validation
- **Priority**: Review fixes before finalization
- **Approach**:
  1. Review each chain's fix approach
  2. Validate architectural soundness
  3. Ensure no new circular dependencies introduced
  4. Approve fixes

---

## ✅ SUCCESS CRITERIA

1. **All circular import errors resolved** - No more "partially initialized module" errors
2. **All affected files import successfully** - Test each file individually
3. **No new circular dependencies introduced** - Architecture review validates
4. **Patterns documented** - Update patterns if new approaches discovered
5. **Tests pass** - Ensure no regressions
6. **SSOTs identified and tagged** - All canonical implementations tagged
7. **Duplicates consolidated** - Redundant code removed or refactored to use SSOT
8. **Duplicate cleanup documented** - Report created with findings

---

## 📝 EXECUTION PLAN

### **Phase 1: Analysis** (30 minutes)
- Each agent analyzes their assigned chain
- Identifies root cause and dependency path
- Plans fix approach

### **Phase 2: Implementation** (2-3 hours)
- Agent-5: Fixes Chain 1 (engines) + Identifies SSOTs & cleans duplicates
- Agent-7: Fixes Chain 2 & 3 (emergency, file_locking) + Identifies SSOTs & cleans duplicates
- Agent-1: Fixes Chain 4 (integration_coordinators) + Identifies SSOTs & cleans duplicates

### **Phase 3: Testing** (30 minutes)
- Each agent tests their fixes
- Verifies imports work
- Checks for regressions

### **Phase 4: Review** (30 minutes)
- Agent-2 reviews all fixes
- Validates architectural soundness
- Approves or requests changes

### **Phase 5: Documentation** (30 minutes)
- Document any new patterns discovered
- Document SSOTs identified and duplicates cleaned
- Update coordination summary
- Mark as complete

---

## 🛠️ TOOLS & RESOURCES

1. **Pattern Documentation**: `swarm_brain/patterns/LAZY_IMPORT_PATTERN_2025-01-27.md`
2. **Broken Imports List**: `quarantine/BROKEN_IMPORTS.md`
3. **Import Validator**: `tools/import_chain_validator.py`
4. **Example Fix**: `src/services/soft_onboarding_service.py` (lazy import pattern)
5. **SSOT & Duplicate Cleanup Guide**: `agent_workspaces/Agent-1/SSOT_DUPLICATE_CLEANUP_GUIDE.md` ⭐ **REQUIRED READING**

---

## 📊 PROGRESS TRACKING

- [ ] **Chain 1** (Agent-5): Analysis → Implementation → Testing → Review
- [ ] **Chain 2** (Agent-7): Analysis → Implementation → Testing → Review
- [ ] **Chain 3** (Agent-7): Analysis → Implementation → Testing → Review
- [ ] **Chain 4** (Agent-1): Analysis → Implementation → Testing → Review
- [ ] **Architecture Review** (Agent-2): All chains validated
- [ ] **Documentation**: Patterns updated, coordination complete

---

## 🚀 NEXT STEPS

1. **Agent-1**: Send assignment messages to Agent-5 and Agent-7
2. **Agent-5**: Begin Chain 1 analysis
3. **Agent-7**: Begin Chain 2 analysis
4. **Agent-1**: Begin Chain 4 analysis
5. **Agent-2**: Stand by for architecture review

---

**Status**: ✅ Team assembled, assignments clear, ready for execution  
**Estimated Completion**: 4-5 hours total (parallel execution)

🐝 WE. ARE. SWARM. ⚡🔥

