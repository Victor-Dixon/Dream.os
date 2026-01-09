# SSOT Config Validation Pattern

**Author**: Agent-8 (SSOT & System Integration Specialist)  
**Date**: 2025-01-27  
**Category**: SSOT Enforcement, Config Consolidation  
**Status**: ✅ ACTIVE

---

## 🎯 **PATTERN OVERVIEW**

Validates that `config_ssot` is used correctly and facade/shims remain mapped during config updates. Prevents SSOT violations in config consolidation.

---

## 🔧 **IMPLEMENTATION**

### **Tool**: `tools/ssot_config_validator.py`
- **Lines**: 314 (V2 compliant)
- **Purpose**: Validate config_ssot usage and facade mapping
- **Usage**:
  ```bash
  # Validate a file
  python tools/ssot_config_validator.py --file src/path/to/file.py
  
  # Validate a directory
  python tools/ssot_config_validator.py --dir src/services/
  
  # Check facade mapping
  python tools/ssot_config_validator.py --check-facade
  
  # Generate report
  python tools/ssot_config_validator.py --file src/path/to/file.py --report
  ```

---

## 📋 **VALIDATION RULES**

### **1. Valid SSOT Imports**
- ✅ `from src.core.config_ssot import ...`
- ✅ `import src.core.config_ssot`
- ✅ `from src.core import config_ssot`

### **2. Deprecated Imports (Violations)**
- ❌ `from src.core.config_core import ...`
- ❌ `from src.core.unified_config import ...`
- ❌ `from src.core.config_browser import ...`
- ❌ `from src.core.config_thresholds import ...`
- ❌ `from src.shared_utils.config import ...`
- ❌ `from src.services.config import ...`

### **3. Facade Shim Files (Must Remain Mapped)**
- `src/core/config_core.py`
- `src/core/unified_config.py`
- `src/core/config_browser.py`
- `src/core/config_thresholds.py`
- `src/shared_utils/config.py`

---

## 🎯 **USE CASES**

### **Before PR Merges**
Validate that new code uses config_ssot:
```bash
python tools/ssot_config_validator.py --dir src/services/ --report
```

### **During Config Updates**
Check facade mapping integrity:
```bash
python tools/ssot_config_validator.py --check-facade
```

### **After Config Consolidation**
Verify no regressions:
```bash
python tools/ssot_config_validator.py --dir src/ --report
```

---

## 💡 **KEY LEARNINGS**

1. **Proactive Validation**: Check config_ssot usage before PR merges, not after
2. **Facade Mapping**: Facade shims must remain mapped to config_ssot
3. **Deprecated Imports**: All deprecated config imports should be flagged
4. **Automation**: Tool enables automated SSOT enforcement during merges

---

## 🔄 **INTEGRATION**

### **Batch 2 PR Merges**
- Run validator before each PR merge
- Verify config_ssot usage in merged code
- Check facade mapping after merges

### **Goldmine Config Unification**
- Validate config_ssot usage before goldmine merges
- Map facade dependencies
- Prevent regressions

---

## 📊 **METRICS**

- **Violations Detected**: Config SSOT violations
- **Facade Status**: Facade shim mapping integrity
- **Valid Imports**: config_ssot usage count

---

## 🐝 **SWARM BENEFIT**

- **Prevents SSOT Violations**: Catches violations before PR merges
- **Enforces Config SSOT**: Ensures config_ssot usage across codebase
- **Maintains Facade Mapping**: Verifies facade shims remain mapped
- **Automates Validation**: Reduces manual checking overhead

---

**Status**: ✅ **ACTIVE PATTERN**  
**Tool**: `tools/ssot_config_validator.py`  
**V2 Compliant**: Yes (314 lines)

**WE. ARE. SWARM!** 🐝⚡🔥

