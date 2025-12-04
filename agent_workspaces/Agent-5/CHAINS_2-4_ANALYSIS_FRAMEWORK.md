# 🔍 Chains 2-4 Circular Import Analysis Framework

**Date**: 2025-12-03  
**Author**: Agent-5 (Business Intelligence Specialist)  
**Status**: Analysis Framework Ready  
**Purpose**: Guide analysis of Chains 2-4 for appropriate pattern selection

---

## 🎯 Analysis Objective

Determine the **most appropriate pattern** for each chain:
- **Plugin Discovery Pattern** (recommended for engine-like structures)
- **Lazy Import Pattern** (quick fix, temporary)
- **Dependency Injection** (for complex dependencies)
- **Factory Pattern** (for complex creation logic)

---

## 📋 Chain 2: `src.core.emergency_intervention.unified_emergency`

### **Error Pattern**:
```
cannot import name 'orchestrator' from partially initialized module 
'src.core.emergency_intervention.unified_emergency'
```

### **Affected Files** (~7 files):
1. `src/core/emergency_intervention/unified_emergency/engines/emergency_coordination_engine.py`
2. `src/core/emergency_intervention/unified_emergency/engines/emergency_detection_engine.py`
3. `src/core/emergency_intervention/unified_emergency/engines/emergency_execution_engine.py`
4. `src/core/emergency_intervention/unified_emergency/engines/emergency_recovery_engine.py`
5. `src/core/emergency_intervention/unified_emergency/engines/emergency_response_engine.py`
6. `src/core/emergency_intervention/unified_emergency/engines/emergency_validation_engine.py`
7. `src/core/emergency_intervention/unified_emergency/engines/emergency_verification_engine.py`

### **Root Cause Hypothesis**:
- `__init__.py` imports `orchestrator`
- `orchestrator` imports from engines
- Engines import from `__init__.py` → **Circular dependency**

### **Analysis Questions**:
1. ✅ **Structure**: Does this follow engine pattern? (multiple engines, similar structure)
2. ✅ **Naming Convention**: Do engines follow consistent naming? (`*_engine.py`, `*Engine`)
3. ✅ **Protocol**: Is there a base protocol/interface?
4. ✅ **Orchestrator Role**: What does orchestrator do? (registry-like or coordinator?)
5. ✅ **Dependencies**: What do engines depend on? (orchestrator, base classes, protocols)

### **Pattern Recommendation** (TBD):
- **If engine-like structure**: Plugin Discovery Pattern ⭐⭐⭐⭐⭐
- **If orchestrator is coordinator**: Dependency Injection ⭐⭐⭐⭐
- **If simple fix needed**: Lazy Import Pattern ⭐⭐⭐ (temporary)

### **SSOT & Duplicate Cleanup**:
- [ ] Identify duplicate orchestrator patterns
- [ ] Consolidate similar engine base classes
- [ ] Find duplicate protocol/validation logic
- [ ] Tag SSOT files with domain tags
- [ ] Document duplicates

---

## 📋 Chain 3: `src.core.file_locking`

### **Error Pattern**:
```
cannot import name 'file_locking_engine_base' from partially initialized module 
'src.core.file_locking'
```

### **Affected Files** (~6 files):
1. `src/core/file_locking/engines/file_locking_coordination_engine.py`
2. `src/core/file_locking/engines/file_locking_detection_engine.py`
3. `src/core/file_locking/engines/file_locking_execution_engine.py`
4. `src/core/file_locking/engines/file_locking_recovery_engine.py`
5. `src/core/file_locking/engines/file_locking_validation_engine.py`
6. `src/core/file_locking/engines/file_locking_verification_engine.py`

### **Root Cause Hypothesis**:
- `__init__.py` imports `file_locking_engine_base`
- `file_locking_engine_base` imports from engines
- Engines import from `__init__.py` → **Circular dependency**

### **Analysis Questions**:
1. ✅ **Structure**: Does this follow engine pattern? (multiple engines, similar structure)
2. ✅ **Naming Convention**: Do engines follow consistent naming? (`*_engine.py`, `*Engine`)
3. ✅ **Base Class**: What is `file_locking_engine_base`? (base class, mixin, protocol?)
4. ✅ **Dependencies**: What do engines depend on? (base class, protocols, utilities)
5. ✅ **Similarity to Chain 1**: Is this similar to `src.core.engines`?

### **Pattern Recommendation** (TBD):
- **If engine-like structure**: Plugin Discovery Pattern ⭐⭐⭐⭐⭐
- **If base class is mixin**: Dependency Injection ⭐⭐⭐⭐
- **If simple fix needed**: Lazy Import Pattern ⭐⭐⭐ (temporary)

### **SSOT & Duplicate Cleanup**:
- [ ] Identify duplicate base class patterns
- [ ] Consolidate similar engine initialization logic
- [ ] Find duplicate validation/error handling
- [ ] Tag SSOT files with domain tags
- [ ] Document duplicates

---

## 📋 Chain 4: `src.core.integration_coordinators`

### **Error Pattern**:
```
cannot import name 'messaging_coordinator' from partially initialized module 
'src.core.integration_coordinators'
```

### **Affected Files** (~10 files):
- Multiple files importing from `src.core.integration_coordinators`
- **Note**: Exact list needs verification

### **Root Cause Hypothesis**:
- `__init__.py` imports `messaging_coordinator`
- `messaging_coordinator` imports from integration_coordinators
- Other coordinators import from `__init__.py` → **Circular dependency**

### **Analysis Questions**:
1. ✅ **Structure**: Is this coordinator pattern? (multiple coordinators, similar structure)
2. ✅ **Naming Convention**: Do coordinators follow consistent naming?
3. ✅ **Protocol**: Is there a base coordinator protocol/interface?
4. ✅ **Messaging Coordinator Role**: What does messaging_coordinator do?
5. ✅ **Dependencies**: What do coordinators depend on? (messaging, protocols, utilities)

### **Pattern Recommendation** (TBD):
- **If coordinator-like structure**: Plugin Discovery Pattern ⭐⭐⭐⭐⭐
- **If messaging is central**: Dependency Injection ⭐⭐⭐⭐
- **If simple fix needed**: Lazy Import Pattern ⭐⭐⭐ (temporary)

### **SSOT & Duplicate Cleanup**:
- [ ] Identify duplicate coordinator patterns
- [ ] Consolidate similar coordinator base classes
- [ ] Find duplicate messaging/protocol logic
- [ ] Tag SSOT files with domain tags
- [ ] Document duplicates

---

## 🔍 Analysis Methodology

### **Step 1: Structure Analysis**
```python
# Check directory structure
import os
from pathlib import Path

def analyze_structure(directory: Path):
    """Analyze directory structure for pattern matching."""
    engines = list(directory.glob("**/*_engine.py"))
    coordinators = list(directory.glob("**/*_coordinator.py"))
    base_files = list(directory.glob("**/*base*.py"))
    protocols = list(directory.glob("**/*protocol*.py"))
    
    return {
        "engines": len(engines),
        "coordinators": len(coordinators),
        "base_files": len(base_files),
        "protocols": len(protocols),
        "structure_type": determine_structure_type(engines, coordinators)
    }
```

### **Step 2: Dependency Analysis**
```python
import ast

def analyze_dependencies(file_path: Path):
    """Analyze import dependencies in file."""
    with open(file_path) as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend([alias.name for alias in node.names])
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)
    
    return imports
```

### **Step 3: Naming Convention Analysis**
```python
def check_naming_convention(files: list[Path]) -> dict:
    """Check if files follow consistent naming convention."""
    patterns = {
        "engine_pattern": r".*_engine\.py$",
        "coordinator_pattern": r".*_coordinator\.py$",
        "base_pattern": r".*base.*\.py$",
    }
    
    matches = {}
    for pattern_name, pattern in patterns.items():
        matches[pattern_name] = sum(
            1 for f in files if re.match(pattern, f.name)
        )
    
    return matches
```

### **Step 4: Protocol/Interface Analysis**
```python
def find_protocols(directory: Path) -> list[str]:
    """Find protocol/interface definitions."""
    protocols = []
    for file in directory.rglob("*.py"):
        with open(file) as f:
            content = f.read()
            if "Protocol" in content or "ABC" in content:
                protocols.append(file)
    return protocols
```

---

## 📊 Decision Framework

### **Plugin Discovery Pattern** ⭐⭐⭐⭐⭐
**Use when**:
- ✅ Multiple implementations of same protocol
- ✅ Consistent naming convention (`*_engine.py`, `*Engine`)
- ✅ Protocol/interface exists
- ✅ Similar structure to Chain 1

**Example**: Chain 1 (`src.core.engines`)

---

### **Dependency Injection** ⭐⭐⭐⭐
**Use when**:
- ✅ Complex dependencies between components
- ✅ Need fine-grained control
- ✅ Orchestrator/coordinator pattern
- ✅ Not engine-like structure

**Example**: Chain 2 (if orchestrator is coordinator, not registry)

---

### **Lazy Import Pattern** ⭐⭐⭐
**Use when**:
- ✅ Quick fix needed
- ✅ Temporary solution
- ✅ Simple circular dependency
- ✅ Not scalable long-term

**Example**: Temporary fix before Plugin Discovery

---

## 📝 Analysis Checklist

For each chain, complete:

- [ ] **Structure Analysis**: Directory structure, file count, patterns
- [ ] **Dependency Analysis**: Import dependencies, circular paths
- [ ] **Naming Convention**: Consistency check
- [ ] **Protocol/Interface**: Existence and usage
- [ ] **Similarity to Chain 1**: Comparison for pattern reuse
- [ ] **SSOT Identification**: Duplicate patterns, consolidation opportunities
- [ ] **Pattern Recommendation**: Best pattern with rationale
- [ ] **Migration Path**: Steps to implement chosen pattern

---

## 🎯 Next Steps

1. **Agent-2/Agent-7**: Analyze Chain 2 structure and dependencies
2. **Agent-7**: Analyze Chain 3 structure and dependencies
3. **Agent-1**: Analyze Chain 4 structure and dependencies
4. **Agent-5**: Synthesize findings and recommend patterns
5. **Team**: Review recommendations and approve patterns

---

## 📚 Reference

- **Chain 1 Pattern**: Plugin Discovery Pattern (approved)
- **Implementation Guide**: `agent_workspaces/Agent-5/PLUGIN_DISCOVERY_IMPLEMENTATION_GUIDE.md`
- **Pattern Documentation**: `swarm_brain/shared_learnings/PLUGIN_DISCOVERY_PATTERN_2025-12-03.md`
- **Lazy Import Pattern**: `swarm_brain/patterns/LAZY_IMPORT_PATTERN_2025-01-27.md`

---

**Status**: ✅ Analysis Framework Ready  
**Ready for**: Agent-2, Agent-7, Agent-1 analysis

🐝 **WE. ARE. SWARM. ⚡🔥**

