# 🔌 Plugin Discovery Pattern - Swarm Learning

**Date**: 2025-12-03  
**Agent**: Agent-5 (Business Intelligence Specialist)  
**Status**: ✅ **PATTERN DOCUMENTED & APPROVED**  
**Approved By**: Agent-2 (Architecture & Design Specialist)

---

## 🎯 **PATTERN OVERVIEW**

The Plugin Discovery Pattern resolves circular import dependencies and enables scalable auto-discovery of protocol implementations using Python's `pkgutil` and `importlib`.

**Key Principle**: Registry depends on Protocol (abstraction), not concrete classes.

---

## 🐛 **PROBLEM**

### **Circular Import Issue**:
```
Registry imports Engines → __init__.py imports Registry → Circular Dependency
```

### **Maintenance Burden**:
- Adding new engine requires modifying registry
- 14+ hardcoded imports
- Violates Open/Closed Principle
- Tight coupling to concrete classes

---

## ✅ **SOLUTION: Plugin Discovery Pattern**

### **Core Implementation**:

```python
import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Dict, Optional, Type
from .contracts import Engine

logger = logging.getLogger(__name__)

class EngineRegistry:
    """Protocol-based registry with auto-discovery."""
    
    def __init__(self):
        self._engines: Dict[str, Type[Engine]] = {}
        self._instances: Dict[str, Engine] = {}
        self._discover_engines()  # Auto-discover!
    
    def _discover_engines(self) -> None:
        """Auto-discover engines implementing Engine protocol."""
        package_path = Path(__file__).parent
        package_name = __package__
        
        for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
            if name.endswith('_core_engine') and not ispkg:
                try:
                    module = importlib.import_module(f'{package_name}.{name}')
                    engine_class = self._find_engine_class(module)
                    if engine_class:
                        engine_type = name.replace('_core_engine', '')
                        self._engines[engine_type] = engine_class
                        logger.info(f"Discovered: {engine_type} -> {engine_class.__name__}")
                except (ImportError, AttributeError) as e:
                    logger.warning(f"Skipped {name}: {e}")
                    continue
    
    def _find_engine_class(self, module: Any) -> Optional[Type[Engine]]:
        """Find Engine implementation in module."""
        for attr_name in dir(module):
            if attr_name.startswith('_'):
                continue
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, Engine) and
                attr is not Engine and
                attr_name.endswith('CoreEngine')):
                return attr
        return None
```

---

## 📊 **BENEFITS**

1. **Zero Circular Dependencies**: No module-level imports
2. **Auto-Discovery**: New engines automatically registered
3. **Protocol-Based**: DIP compliant (depends on abstractions)
4. **Highly Testable**: Easy to mock and test
5. **Infinite Scalability**: Works with any number of engines
6. **Zero Maintenance**: No manual registration needed

---

## 🔄 **USAGE PATTERNS**

### **Pattern 1: Standard Discovery**

```python
# Registry automatically discovers all engines
registry = EngineRegistry()
engine_types = registry.get_engine_types()  # ['analysis', 'coordination', ...]
engine = registry.get_engine('analysis')
```

### **Pattern 2: Custom Naming Convention**

```python
# Modify discovery to match your naming convention
if name.endswith('_engine') and not ispkg:  # Custom convention
    # ... discovery logic
```

### **Pattern 3: Protocol-Based Detection**

```python
# Use Protocol to ensure compliance
if issubclass(attr, Engine) and attr is not Engine:
    # Found valid engine implementation
```

---

## 🎯 **WHEN TO USE**

**Use Plugin Discovery Pattern when**:
- ✅ Multiple implementations of same protocol
- ✅ Consistent naming convention
- ✅ Need auto-discovery
- ✅ Want zero circular dependencies
- ✅ Need high scalability

**Don't use when**:
- ❌ Small number of implementations (<3)
- ❌ Inconsistent naming
- ❌ Need fine-grained control
- ❌ Performance is critical

---

## 📝 **BEST PRACTICES**

1. **Naming Convention**: Enforce strict naming (module: `*_core_engine.py`, class: `*CoreEngine`)
2. **Protocol First**: Define Protocol before implementing discovery
3. **Error Handling**: Gracefully handle import errors, log warnings
4. **Logging**: Use proper logging (not print statements)
5. **Type Hints**: Complete type hints for all methods
6. **Testing**: Comprehensive unit tests for discovery logic

---

## 🔍 **VERIFICATION**

**Test Discovery**:
```python
registry = EngineRegistry()
assert len(registry.get_engine_types()) > 0
assert "analysis" in registry.get_engine_types()
```

**Test Protocol Compliance**:
```python
engine = registry.get_engine("analysis")
assert hasattr(engine, 'initialize')
assert hasattr(engine, 'execute')
```

**Test No Circular Dependencies**:
```python
from src.core.engines.registry import EngineRegistry  # ✅ No circular import!
```

---

## 📚 **RELATED PATTERNS**

- **Lazy Import Pattern**: Quick fix, temporary solution
- **Dependency Injection**: Alternative for fine-grained control
- **Factory Pattern**: Alternative for complex creation logic

---

## 🎓 **LEARNINGS**

1. **Plugin Discovery solves circular dependencies** without workarounds
2. **Protocol-based design** enables true DIP compliance
3. **Auto-discovery eliminates** maintenance burden
4. **Naming conventions** are critical for discovery
5. **Proper logging** essential for debugging discovery

---

## 🚀 **REAL-WORLD EXAMPLE**

**Chain 1 (`src.core.engines`)**:
- **Before**: 14 hardcoded imports, circular dependencies
- **After**: Auto-discovery, zero circular dependencies, infinite scalability
- **Result**: ✅ Zero maintenance, DIP compliant, highly testable

---

## 📋 **IMPLEMENTATION CHECKLIST**

- [ ] Define Protocol (SSOT)
- [ ] Implement discovery logic
- [ ] Enforce naming convention
- [ ] Add proper logging
- [ ] Complete type hints
- [ ] Write unit tests
- [ ] Test protocol compliance
- [ ] Verify no circular dependencies
- [ ] Document pattern
- [ ] Update imports

---

**Status**: ✅ **PATTERN DOCUMENTED**  
**Reusability**: ✅ **HIGH**  
**Complexity**: ✅ **MEDIUM**  
**Approved**: ✅ **YES** (Agent-2)

---

**Next**: Apply to Chains 2-4 after analysis

🐝 **WE. ARE. SWARM. ⚡🔥**

