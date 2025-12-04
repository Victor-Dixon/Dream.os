<!-- SSOT Domain: architecture -->
# 🛡️ SSOT Patterns & Best Practices - GitHub Bypass System

**Author**: Agent-8 (SSOT & System Integration Specialist)  
**Date**: 2025-01-28  
**Status**: ✅ ACTIVE  
**Purpose**: SSOT patterns and best practices for GitHub Bypass System components

---

## 🎯 OVERVIEW

This document defines SSOT (Single Source of Truth) patterns and best practices for the GitHub Bypass System. All components follow these patterns to ensure system integrity and maintainability.

---

## 📋 SSOT PATTERNS

### **Pattern 1: Getter Function SSOT**

**Principle**: All components expose a single getter function as the SSOT entry point.

**Implementation**:
```python
# ✅ CORRECT - SSOT Getter Pattern
def get_local_repo_manager(base_path: Optional[Path] = None) -> LocalRepoManager:
    """Get LocalRepoManager instance (SSOT)."""
    global _instance
    if _instance is None:
        _instance = LocalRepoManager(base_path=base_path)
    return _instance

# ❌ WRONG - Direct Instantiation
manager = LocalRepoManager()  # Don't do this!
```

**Components Using This Pattern**:
- ✅ `get_local_repo_manager()` - LocalRepoManager SSOT
- ✅ `get_deferred_push_queue()` - DeferredPushQueue SSOT
- ✅ `get_synthetic_github()` - SyntheticGitHub SSOT
- ✅ `get_consolidation_buffer()` - ConsolidationBuffer SSOT
- ✅ `get_conflict_resolver()` - MergeConflictResolver SSOT

---

### **Pattern 2: Dependency Injection via SSOT**

**Principle**: Components should use SSOT getters for dependencies, not direct instantiation.

**Implementation**:
```python
# ✅ CORRECT - Dependency Injection via SSOT
class SyntheticGitHub:
    def __init__(self):
        self.local_repo_manager = get_local_repo_manager()  # SSOT getter
        self.queue = get_deferred_push_queue()  # SSOT getter

# ❌ WRONG - Direct Dependency Creation
class SyntheticGitHub:
    def __init__(self):
        self.local_repo_manager = LocalRepoManager()  # Creates duplicate!
        self.queue = DeferredPushQueue()  # Creates duplicate!
```

---

### **Pattern 3: Singleton Pattern (Optional)**

**Principle**: Getter functions may use singleton pattern to ensure single instance.

**Implementation**:
```python
# ✅ CORRECT - Singleton Pattern (Optional)
_instance = None

def get_component():
    global _instance
    if _instance is None:
        _instance = Component()
    return _instance

# ✅ ALSO CORRECT - Factory Pattern (New Instance Each Call)
def get_component():
    return Component()  # New instance, but still SSOT getter
```

**Note**: Singleton is optional. The key is having a single getter function as SSOT entry point.

---

### **Pattern 4: No Duplicate Implementations**

**Principle**: Each component should have exactly one implementation class.

**Rules**:
- ✅ One class definition per component
- ✅ One getter function per component
- ❌ No duplicate class names
- ❌ No duplicate getter functions

**Validation**:
```python
# Check for duplicates
def validate_no_duplicates(file_path: Path, class_name: str):
    tree = ast.parse(content)
    classes = [node.name for node in ast.walk(tree) 
               if isinstance(node, ast.ClassDef) and node.name == class_name]
    assert len(classes) == 1, f"Duplicate {class_name} found"
```

---

### **Pattern 5: Configuration SSOT**

**Principle**: Configuration should be loaded from a single source.

**Implementation**:
```python
# ✅ CORRECT - Config from SSOT
from src.core.config_ssot import get_config

config_value = get_config("github_timeout")

# ❌ WRONG - Hardcoded Config
config_value = 30  # Hardcoded value
```

---

## 🔧 BEST PRACTICES

### **1. Always Use Getter Functions**

**Rule**: Never instantiate components directly. Always use getter functions.

```python
# ✅ CORRECT
from src.core.local_repo_layer import get_local_repo_manager
manager = get_local_repo_manager()

# ❌ WRONG
from src.core.local_repo_layer import LocalRepoManager
manager = LocalRepoManager()
```

### **2. Import Getter Functions, Not Classes**

**Rule**: Import getter functions as primary interface. Classes are implementation details.

```python
# ✅ CORRECT - Import getter
from src.core.synthetic_github import get_synthetic_github
github = get_synthetic_github()

# ⚠️ ACCEPTABLE - Import class for type hints only
from src.core.synthetic_github import get_synthetic_github, SyntheticGitHub
github: SyntheticGitHub = get_synthetic_github()
```

### **3. Use SSOT for Inter-Component Dependencies**

**Rule**: Components should use SSOT getters to access other components.

```python
# ✅ CORRECT - SSOT Dependency
class SyntheticGitHub:
    def __init__(self):
        self.local_repo_manager = get_local_repo_manager()
        self.queue = get_deferred_push_queue()

# ❌ WRONG - Direct Dependency
class SyntheticGitHub:
    def __init__(self):
        self.local_repo_manager = LocalRepoManager()
        self.queue = DeferredPushQueue()
```

### **4. Document SSOT Entry Points**

**Rule**: Getter functions should be clearly documented as SSOT entry points.

```python
def get_component() -> Component:
    """
    Get Component instance (SSOT).
    
    This is the single source of truth for Component instances.
    Use this function to access Component throughout the codebase.
    
    Returns:
        Component: Component instance
    """
    ...
```

### **5. Validate SSOT Compliance in Tests**

**Rule**: Include SSOT compliance validation in integration tests.

```python
def test_ssot_compliance():
    """Test SSOT getter functions exist and work."""
    assert callable(get_local_repo_manager)
    assert callable(get_deferred_push_queue)
    assert callable(get_synthetic_github)
    # ... etc
```

---

## 🚨 ANTI-PATTERNS (DO NOT DO THIS)

### **1. Direct Instantiation**
```python
# ❌ DON'T DO THIS
manager = LocalRepoManager()  # Bypasses SSOT
```

### **2. Multiple Getter Functions**
```python
# ❌ DON'T DO THIS
def get_local_repo_manager(): ...
def create_local_repo_manager(): ...  # Duplicate entry point!
```

### **3. Duplicate Class Definitions**
```python
# ❌ DON'T DO THIS
class LocalRepoManager: ...  # First definition
class LocalRepoManager: ...  # Duplicate definition!
```

### **4. Bypassing SSOT Getters**
```python
# ❌ DON'T DO THIS
_instance = LocalRepoManager()  # Bypasses getter
```

---

## 📊 SSOT COMPLIANCE CHECKLIST

### **Component Compliance**:
- [x] Has single getter function as SSOT entry point
- [x] Getter function is documented
- [x] No duplicate class definitions
- [x] No duplicate getter functions
- [x] Uses SSOT getters for dependencies
- [x] Configuration uses config_ssot
- [x] Tests validate SSOT compliance

### **System Compliance**:
- [x] All components follow SSOT patterns
- [x] No duplicate implementations exist
- [x] Integration tests validate SSOT
- [x] Documentation describes SSOT patterns

---

## 🔍 VALIDATION TOOLS

### **1. SSOT Validation Tests**
```bash
# Run SSOT validation tests
pytest tests/integration/test_github_bypass_ssot_validation.py -v
```

### **2. Duplicate Detection**
```python
# Check for duplicate getter functions
python -c "
from pathlib import Path
import ast
file = Path('src/core/synthetic_github.py')
tree = ast.parse(file.read_text())
getters = [n.name for n in ast.walk(tree) 
           if isinstance(n, ast.FunctionDef) and n.name.startswith('get_')]
print(f'Getter functions: {getters}')
"
```

### **3. Import Validation**
```python
# Validate imports use getter functions
grep -r "LocalRepoManager()" src/  # Should find no direct instantiations
grep -r "get_local_repo_manager()" src/  # Should find getter usage
```

---

## 📝 EXAMPLES

### **Example 1: Creating a New Component**

```python
# ✅ CORRECT Implementation
_instance = None

def get_my_component(config: Optional[Dict] = None) -> MyComponent:
    """
    Get MyComponent instance (SSOT).
    
    This is the single source of truth for MyComponent instances.
    """
    global _instance
    if _instance is None:
        _instance = MyComponent(config=config)
    return _instance

class MyComponent:
    def __init__(self, config: Optional[Dict] = None):
        # Use SSOT getters for dependencies
        self.dependency = get_other_component()
        self.config = config or {}
```

### **Example 2: Using Components**

```python
# ✅ CORRECT Usage
from src.core.local_repo_layer import get_local_repo_manager
from src.core.synthetic_github import get_synthetic_github

manager = get_local_repo_manager()
github = get_synthetic_github()

# Use components
success, repo_path, was_local = github.get_repo("test-repo")
```

---

## 🎯 SUMMARY

**Key Principles**:
1. ✅ Use getter functions as SSOT entry points
2. ✅ No duplicate implementations
3. ✅ Dependency injection via SSOT getters
4. ✅ Configuration from config_ssot
5. ✅ Validation in tests

**Benefits**:
- Single source of truth for each component
- Easy to maintain and update
- Clear integration patterns
- Reduced complexity
- Better testability

---

**Status**: ✅ ACTIVE - All GitHub Bypass components comply with SSOT patterns

🐝 WE. ARE. SWARM. ⚡🔥

