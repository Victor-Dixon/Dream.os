# 🔄 Lazy Import Pattern - Circular Import Resolution

**Date**: 2025-01-27  
**Agent**: Agent-1 (Integration & Core Systems)  
**Status**: ✅ **PATTERN DOCUMENTED**

---

## 🎯 **PATTERN OVERVIEW**

The Lazy Import Pattern resolves circular import dependencies by deferring imports until they are actually needed, using Python's property decorator.

---

## 🐛 **PROBLEM**

Circular imports occur when:
- Module A imports Module B
- Module B imports Module A
- Both imports happen at module level

**Example**:
```python
# soft_onboarding_service.py
from .handlers.soft_onboarding_handler import SoftOnboardingHandler

class SoftOnboardingService:
    def __init__(self):
        self.handler = SoftOnboardingHandler()  # ❌ Circular import!

# soft_onboarding_handler.py
from ..soft_onboarding_service import SoftOnboardingService  # ❌ Circular import!
```

**Result**: `ImportError: cannot import name 'X' from partially initialized module`

---

## ✅ **SOLUTION: Lazy Import Pattern**

### **Implementation**

```python
class SoftOnboardingService:
    def __init__(self):
        # Don't import handler in __init__ - avoid circular import
        self._handler = None
        logger.info("SoftOnboardingService initialized")
    
    @property
    def handler(self):
        """Lazy-load handler to avoid circular import."""
        if self._handler is None:
            from .handlers.soft_onboarding_handler import SoftOnboardingHandler
            self._handler = SoftOnboardingHandler()
        return self._handler
```

### **How It Works**

1. **Initialization**: Store `None` instead of importing
2. **First Access**: Property decorator checks if `_handler` is `None`
3. **Lazy Load**: Import happens only when property is first accessed
4. **Cache**: Store instance in `_handler` for subsequent accesses

---

## 📊 **BENEFITS**

1. **No Circular Dependency**: Import happens after both modules are initialized
2. **Same API**: No breaking changes to existing code
3. **Performance**: Handler loaded only when needed
4. **Pythonic**: Follows Python best practices
5. **Reusable**: Pattern works for any circular import scenario

---

## 🔄 **USAGE PATTERNS**

### **Pattern 1: Property Decorator (Recommended)**

```python
class Service:
    def __init__(self):
        self._dependency = None
    
    @property
    def dependency(self):
        if self._dependency is None:
            from .dependency_module import Dependency
            self._dependency = Dependency()
        return self._dependency
```

### **Pattern 2: Method-Level Import**

```python
class Service:
    def do_something(self):
        # Import inside method, not at module level
        from .dependency_module import Dependency
        dep = Dependency()
        return dep.execute()
```

### **Pattern 3: Function-Level Import**

```python
def get_service():
    # Import inside function
    from .service_module import Service
    return Service()
```

---

## 🎯 **WHEN TO USE**

**Use Lazy Import Pattern when**:
- ✅ Circular import detected
- ✅ Dependency is optional or rarely used
- ✅ Want to maintain same API
- ✅ Need to defer expensive imports

**Don't use when**:
- ❌ Dependency is always needed (just fix the architecture)
- ❌ Import is cheap and always required
- ❌ Better to refactor architecture to remove circular dependency

---

## 📝 **BEST PRACTICES**

1. **Use Property Decorator**: Cleanest API, maintains same interface
2. **Cache the Instance**: Store in private variable to avoid re-importing
3. **Document the Pattern**: Add comment explaining why lazy import is used
4. **Consider Architecture**: Sometimes better to refactor than use lazy import

---

## 🔍 **VERIFICATION**

**Test Import**:
```bash
python -c "from src.services.soft_onboarding_service import SoftOnboardingService; s = SoftOnboardingService(); print('✅ Import successful')"
```

**Test Usage**:
```python
service = SoftOnboardingService()
# Handler loaded on first access
handler = service.handler  # ✅ No circular import!
```

---

## 📚 **RELATED PATTERNS**

- **Dependency Injection**: Pass dependencies as parameters
- **Factory Pattern**: Create instances via factory functions
- **Module Refactoring**: Extract common code to shared module

---

## 🎓 **LEARNINGS**

1. **Lazy imports solve circular dependencies** without breaking APIs
2. **Property decorator** is the cleanest implementation
3. **Cache instances** to avoid repeated imports
4. **Document the pattern** for future maintainers

---

**Status**: ✅ **PATTERN DOCUMENTED**  
**Reusability**: ✅ **HIGH**  
**Complexity**: ✅ **LOW**

