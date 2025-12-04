# 🔌 Plugin Discovery Pattern - Implementation Guide

**Date**: 2025-12-03  
**Author**: Agent-5 (Business Intelligence Specialist)  
**Status**: ✅ APPROVED by Agent-2  
**Priority**: HIGH - Implementation Ready

---

## 🎯 Overview

**Plugin Discovery Pattern** is a scalable, zero-circular-dependency solution for auto-discovering and registering implementations of a protocol.

**Key Benefits**:
- ✅ Zero circular dependencies (no module-level imports)
- ✅ Auto-discovery (no manual registration)
- ✅ Protocol-based (DIP compliant)
- ✅ Highly testable
- ✅ Scales infinitely

---

## 📋 When to Use

**Use Plugin Discovery Pattern when**:
- ✅ Multiple implementations of same protocol
- ✅ Consistent naming convention
- ✅ Need auto-discovery
- ✅ Want zero circular dependencies
- ✅ Need high scalability

**Don't use when**:
- ❌ Small number of implementations (<3)
- ❌ Inconsistent naming
- ❌ Need fine-grained control over registration
- ❌ Performance is critical (discovery has small overhead)

---

## 🏗️ Architecture Pattern

### **Core Principle: Dependency Inversion**

```
Registry (High-level) → Engine Protocol (Abstraction) ← Engines (Low-level)
```

**Registry depends on Protocol, not concrete classes!**

---

## 📝 Implementation Steps

### **Step 1: Define Protocol (SSOT)**

**File**: `src/core/engines/contracts.py` (already exists)

```python
from typing import Protocol

class Engine(Protocol):
    """Base engine protocol - all engines must implement this."""
    def initialize(self, context: EngineContext) -> bool: ...
    def execute(self, context: EngineContext, payload: dict) -> EngineResult: ...
    def cleanup(self, context: EngineContext) -> bool: ...
    def get_status(self) -> dict[str, Any]: ...
```

**Status**: ✅ Already SSOT, tagged with `<!-- SSOT Domain: integration -->`

---

### **Step 2: Implement Discovery Logic**

**File**: `src/core/engines/registry.py`

```python
import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Dict, Optional, Type

from .contracts import Engine, EngineContext

logger = logging.getLogger(__name__)

class EngineRegistry:
    """Protocol-based engine registry with auto-discovery."""
    
    def __init__(self):
        self._engines: Dict[str, Type[Engine]] = {}
        self._instances: Dict[str, Engine] = {}
        self._discover_engines()
    
    def _discover_engines(self) -> None:
        """Auto-discover engines implementing Engine protocol."""
        package_path = Path(__file__).parent
        package_name = __package__
        
        logger.info(f"Discovering engines in package: {package_name}")
        discovered_count = 0
        
        for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
            if name.endswith('_core_engine') and not ispkg:
                try:
                    module = importlib.import_module(f'{package_name}.{name}')
                    engine_class = self._find_engine_class(module)
                    
                    if engine_class:
                        engine_type = name.replace('_core_engine', '')
                        self._engines[engine_type] = engine_class
                        discovered_count += 1
                        logger.info(
                            f"Discovered engine: {engine_type} -> {engine_class.__name__}"
                        )
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Skipped {name}: {e}")
                    continue
        
        logger.info(f"Discovery complete: {discovered_count} engines found")
    
    def _find_engine_class(self, module: Any) -> Optional[Type[Engine]]:
        """Find Engine implementation in module."""
        from .contracts import Engine
        
        for attr_name in dir(module):
            if attr_name.startswith('_'):
                continue
            
            try:
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, Engine) and
                    attr is not Engine and
                    attr_name.endswith('CoreEngine')):
                    return attr
            except (TypeError, AttributeError):
                continue
        
        return None
    
    def get_engine(self, engine_type: str) -> Engine:
        """Get engine instance by type (lazy instantiation)."""
        if engine_type not in self._engines:
            available = ', '.join(self._engines.keys())
            raise ValueError(
                f"Unknown engine type: {engine_type}. Available: {available}"
            )
        
        if engine_type not in self._instances:
            self._instances[engine_type] = self._engines[engine_type]()
        
        return self._instances[engine_type]
    
    # ... rest of methods
```

---

### **Step 3: Naming Convention**

**Required**: Engines must follow naming convention:

- **Module name**: `*_core_engine.py` (e.g., `analysis_core_engine.py`)
- **Class name**: `*CoreEngine` (e.g., `AnalysisCoreEngine`)

**Example**:
```python
# analysis_core_engine.py
from .contracts import AnalysisEngine, EngineContext, EngineResult

class AnalysisCoreEngine(AnalysisEngine):
    """Analysis engine implementation."""
    # ... implementation
```

---

### **Step 4: Testing**

**File**: `tests/test_engine_registry.py`

```python
import pytest
from src.core.engines.registry import EngineRegistry
from src.core.engines.contracts import EngineContext

def test_auto_discovery():
    """Test that engines are auto-discovered."""
    registry = EngineRegistry()
    engine_types = registry.get_engine_types()
    
    assert len(engine_types) > 0
    assert "analysis" in engine_types
    assert "coordination" in engine_types

def test_protocol_compliance():
    """Test that discovered engines implement Engine protocol."""
    registry = EngineRegistry()
    context = EngineContext(config={}, logger=logging.getLogger(), metrics={})
    
    for engine_type in registry.get_engine_types():
        engine = registry.get_engine(engine_type)
        assert hasattr(engine, 'initialize')
        assert hasattr(engine, 'execute')
        assert hasattr(engine, 'cleanup')
        assert hasattr(engine, 'get_status')
        
        # Test initialization
        result = engine.initialize(context)
        assert isinstance(result, bool)

def test_no_circular_imports():
    """Test that registry can be imported without circular dependencies."""
    from src.core.engines.registry import EngineRegistry
    registry = EngineRegistry()
    assert registry is not None
```

---

## 🔧 Migration from Lazy Imports

### **Before (Lazy Imports - Technical Debt)**:

```python
def _initialize_engines(self) -> None:
    """Lazy imports - temporary technical debt."""
    from .analysis_core_engine import AnalysisCoreEngine
    from .coordination_core_engine import CoordinationCoreEngine
    # ... 14 more hardcoded imports
    self._engines = {
        "analysis": AnalysisCoreEngine,
        "coordination": CoordinationCoreEngine,
        # ... hardcoded mapping
    }
```

### **After (Plugin Discovery)**:

```python
def _discover_engines(self) -> None:
    """Auto-discover engines - no hardcoded imports!"""
    # Discovery logic automatically finds all engines
    # No manual registration needed
```

---

## 📊 Comparison: Before vs After

| Aspect | Lazy Imports | Plugin Discovery |
|--------|-------------|------------------|
| **Circular Dependencies** | ✅ None | ✅ None |
| **Maintenance** | ❌ High (14 imports) | ✅ Zero (auto) |
| **Scalability** | ❌ Manual updates | ✅ Infinite |
| **DIP Compliance** | ❌ No | ✅ Yes |
| **Testability** | ⚠️ Medium | ✅ High |
| **Performance** | ✅ Fast | ✅ Fast (one-time) |

---

## 🚨 Common Pitfalls & Solutions

### **Pitfall 1: Naming Convention Not Followed**

**Problem**: Engine not discovered because naming doesn't match

**Solution**: 
- Module must end with `_core_engine.py`
- Class must end with `CoreEngine`
- Follow convention strictly

---

### **Pitfall 2: Protocol Not Implemented**

**Problem**: Class found but doesn't implement Engine protocol

**Solution**:
- Ensure class inherits from Engine protocol
- Implement all required methods
- Use type hints for protocol compliance

---

### **Pitfall 3: Import Errors During Discovery**

**Problem**: Discovery fails on import errors

**Solution**:
- Wrap in try/except
- Log warnings but continue
- Don't break on missing engines

---

## ✅ Verification Checklist

- [ ] Protocol defined and tagged as SSOT
- [ ] Discovery logic implemented
- [ ] Naming convention documented
- [ ] Unit tests created
- [ ] Integration tests pass
- [ ] No circular dependencies
- [ ] All engines discovered
- [ ] Logging configured
- [ ] Type hints complete
- [ ] Documentation updated

---

## 📚 Related Patterns

- **Lazy Import Pattern**: Quick fix, temporary solution
- **Dependency Injection**: Alternative for fine-grained control
- **Factory Pattern**: Alternative for complex creation logic

---

## 🎯 Next Steps

1. **Implement** in `registry.py` (Agent-1)
2. **Test** thoroughly (Agent-8)
3. **Document** in swarm_brain (Agent-5) ✅
4. **Apply** to Chains 2-4 (after analysis)

---

**Status**: ✅ Implementation Guide Complete  
**Ready for**: Agent-1 implementation

🐝 **WE. ARE. SWARM. ⚡🔥**

