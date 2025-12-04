# 🔄 Chain 2: CircuitBreaker Circular Import Fix - Dependency Injection Pattern

**Date**: 2025-12-03  
**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Priority**: HIGH  
**Status**: IN PROGRESS  
**Pattern**: Dependency Injection

---

## 🎯 MISSION

Fix CircuitBreaker circular import issues using Dependency Injection pattern.

**Files Affected**: ~20 files  
**Issue**: CircuitBreaker circular import  
**Solution**: Extract protocol, inject dependencies  
**Time**: 1-2 days

---

## 📊 ANALYSIS

### **Circular Import Chain Identified**:

1. `src/core/error_handling/__init__.py` imports `CircuitBreaker` from `.circuit_breaker`
2. `src/core/error_handling/circuit_breaker/__init__.py` tries to import from `..circuit_breaker` (parent)
3. `src/core/error_handling/circuit_breaker.py` imports from `.error_handling_core`
4. Multiple files import `CircuitBreaker` directly, creating cycles

### **Files Using CircuitBreaker** (from grep):
1. `src/core/error_handling/__init__.py`
2. `src/core/error_handling/circuit_breaker/__init__.py`
3. `src/core/error_handling/circuit_breaker.py`
4. `src/core/error_handling/circuit_breaker/core.py`
5. `src/core/error_handling/component_management.py`
6. `src/core/error_handling/error_config.py`
7. `src/core/error_handling/error_models_core.py`
8. `src/core/error_handling/error_execution.py`
9. Plus ~12 more files (need to identify)

### **Duplicate Patterns Identified**:
- ✅ `circuit_breaker.py` - Main CircuitBreaker class
- ⚠️ `circuit_breaker/core.py` - CircuitBreakerCore class (duplicate functionality?)
- ⚠️ Both have similar state management and logic

### **SSOT Designation**:
- **SSOT**: `src/core/error_handling/circuit_breaker.py` (main implementation)
- **Duplicate**: `src/core/error_handling/circuit_breaker/core.py` (consolidate or remove)

---

## 🏗️ SOLUTION: DEPENDENCY INJECTION PATTERN

### **Phase 1: Extract Protocol** ✅

Create `src/core/error_handling/circuit_breaker/protocol.py`:

```python
"""
Circuit Breaker Protocol - SSOT for Circuit Breaker Interface
=============================================================

<!-- SSOT Domain: integration -->

Protocol defining the Circuit Breaker interface contract.
All Circuit Breaker implementations must conform to this protocol.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from typing import Protocol, Any, Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.config.config_dataclasses import CircuitBreakerConfig


class ICircuitBreaker(Protocol):
    """Circuit Breaker protocol - defines the interface contract."""
    
    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute function with circuit breaker protection."""
        ...
    
    def get_state(self) -> str:
        """Get current circuit breaker state."""
        ...
    
    def get_status(self) -> dict[str, Any]:
        """Get current circuit breaker status."""
        ...
```

### **Phase 2: Create Provider/Factory** ✅

Create `src/core/error_handling/circuit_breaker/provider.py`:

```python
"""
Circuit Breaker Provider - Dependency Injection Factory
=======================================================

<!-- SSOT Domain: integration -->

Factory/provider for creating Circuit Breaker instances.
Uses dependency injection to break circular imports.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.config.config_dataclasses import CircuitBreakerConfig
    from .protocol import ICircuitBreaker


class CircuitBreakerProvider:
    """Provider for Circuit Breaker instances (Dependency Injection)."""
    
    @staticmethod
    def create(config: 'CircuitBreakerConfig') -> 'ICircuitBreaker':
        """Create a Circuit Breaker instance."""
        # Lazy import to avoid circular dependency
        from ..circuit_breaker import CircuitBreaker
        return CircuitBreaker(config)
    
    @staticmethod
    def get_default() -> 'ICircuitBreaker':
        """Get default Circuit Breaker instance."""
        from src.core.config.config_dataclasses import CircuitBreakerConfig
        config = CircuitBreakerConfig(
            name="default",
            failure_threshold=5,
            recovery_timeout=60.0
        )
        return CircuitBreakerProvider.create(config)
```

### **Phase 3: Refactor Files to Use Dependency Injection** ✅

**Pattern**: Instead of importing CircuitBreaker directly, inject it:

```python
# BEFORE (Circular Import):
from src.core.error_handling import CircuitBreaker

class Service:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(config)

# AFTER (Dependency Injection):
from src.core.error_handling.circuit_breaker.provider import CircuitBreakerProvider
from src.core.error_handling.circuit_breaker.protocol import ICircuitBreaker

class Service:
    def __init__(self, circuit_breaker: ICircuitBreaker | None = None):
        self.circuit_breaker = circuit_breaker or CircuitBreakerProvider.create(config)
```

---

## 📋 IMPLEMENTATION PLAN

### **Step 1: Extract Protocol** (30 minutes)
- [x] Create `circuit_breaker/protocol.py`
- [x] Define `ICircuitBreaker` protocol
- [x] Tag as SSOT

### **Step 2: Create Provider** (30 minutes)
- [x] Create `circuit_breaker/provider.py`
- [x] Implement `CircuitBreakerProvider` with lazy imports
- [x] Tag as SSOT

### **Step 3: Refactor Core Files** (1 hour)
- [ ] Update `circuit_breaker.py` to implement protocol
- [ ] Update `circuit_breaker/__init__.py` to use provider
- [ ] Update `error_handling/__init__.py` to use provider
- [ ] Fix `circuit_breaker/core.py` (consolidate or remove)

### **Step 4: Refactor Consumer Files** (2-3 hours)
- [ ] Update `component_management.py` to use dependency injection
- [ ] Update `error_config.py` to use dependency injection
- [ ] Update `error_models_core.py` to use dependency injection
- [ ] Update `error_execution.py` to use dependency injection
- [ ] Update all other files (~16 more files)

### **Step 5: SSOT & Duplicate Cleanup** (1 hour)
- [ ] Identify duplicate CircuitBreaker implementations
- [ ] Consolidate `circuit_breaker/core.py` into main implementation
- [ ] Tag SSOT files with `<!-- SSOT Domain: integration -->`
- [ ] Remove or archive duplicates

### **Step 6: Testing** (30 minutes)
- [ ] Test all files import successfully
- [ ] Verify no circular import errors
- [ ] Test CircuitBreaker functionality
- [ ] Run existing tests

---

## 🔍 SSOT & DUPLICATE CLEANUP

### **SSOT Files**:
- ✅ `src/core/error_handling/circuit_breaker.py` - Main CircuitBreaker implementation
- ✅ `src/core/error_handling/circuit_breaker/protocol.py` - Circuit Breaker protocol (NEW)
- ✅ `src/core/error_handling/circuit_breaker/provider.py` - Circuit Breaker provider (NEW)

### **Duplicates to Consolidate**:
- ⚠️ `src/core/error_handling/circuit_breaker/core.py` - CircuitBreakerCore (similar to CircuitBreaker)
  - **Action**: Consolidate into main CircuitBreaker or remove if redundant

### **Duplicate Patterns**:
- Multiple CircuitBreaker state management logic
- Duplicate timeout/recovery logic
- Similar error handling patterns

---

## ✅ SUCCESS CRITERIA

1. ✅ **No circular import errors** - All files import successfully
2. ✅ **Protocol extracted** - ICircuitBreaker protocol defined
3. ✅ **Provider created** - CircuitBreakerProvider with lazy imports
4. ✅ **All files refactored** - ~20 files use dependency injection
5. ✅ **SSOTs identified** - All canonical implementations tagged
6. ✅ **Duplicates cleaned** - Redundant code removed or consolidated
7. ✅ **Tests pass** - No regressions

---

## 📊 PROGRESS TRACKING

- [x] **Step 1**: Extract Protocol ✅
- [x] **Step 2**: Create Provider ✅
- [ ] **Step 3**: Refactor Core Files ⏳
- [ ] **Step 4**: Refactor Consumer Files ⏳
- [ ] **Step 5**: SSOT & Duplicate Cleanup ⏳
- [ ] **Step 6**: Testing ⏳

---

**Status**: 🚀 **IN PROGRESS** - Protocol and Provider created, starting refactoring  
**Estimated Completion**: 4-6 hours total

🐝 WE. ARE. SWARM. ⚡🔥

