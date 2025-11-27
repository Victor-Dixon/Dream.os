# 🗺️ Config SSOT Facade Dependency Map

**Author**: Agent-8 (SSOT & System Integration Specialist)  
**Date**: 2025-01-27  
**Status**: ACTIVE  
**Purpose**: Comprehensive mapping of config_ssot facade/shim dependencies to prevent regressions

---

## 🎯 OVERVIEW

This document maps all dependencies between config_ssot (SSOT) and its facade/shim files to ensure backward compatibility and prevent regressions during goldmine merges.

**Goal**: Zero regressions during config consolidation.

---

## 📊 FACADE STRUCTURE

### **Core SSOT (Single Source of Truth)**

```
src/core/config_ssot.py (Main Entry Point - 86 lines)
│
├── config/config_accessors.py (Accessor Functions)
│   ├── get_config(key, default)
│   ├── get_unified_config()
│   ├── get_timeout_config()
│   ├── get_agent_config()
│   ├── get_browser_config()
│   ├── get_threshold_config()
│   ├── get_file_pattern_config()
│   ├── get_test_config()
│   └── get_report_config()
│
├── config/config_dataclasses.py (Config Models)
│   ├── TimeoutConfig
│   ├── AgentConfig
│   ├── BrowserConfig
│   ├── ThresholdConfig
│   ├── FilePatternConfig
│   ├── TestConfig
│   └── ReportConfig
│
├── config/config_manager.py (UnifiedConfigManager)
│   └── UnifiedConfigManager (SSOT implementation)
│
└── config/config_enums.py (Enums)
    ├── ConfigEnvironment
    ├── ConfigSource
    └── ReportFormat
```

### **Backward Compatibility Shims**

```
Shim Files (Re-export from config_ssot):
│
├── src/core/config_core.py (91 lines)
│   ├── Re-exports: get_config, get_agent_config, get_timeout_config, etc.
│   ├── Deprecated functions: set_config, reload_config, validate_config, get_all_config
│   └── Status: ✅ DEPRECATED - All imports from config_ssot
│
├── src/core/unified_config.py (89 lines)
│   ├── Re-exports: All dataclasses, enums, accessors
│   ├── Deprecated alias: UnifiedConfig = UnifiedConfigManager
│   └── Status: ✅ DEPRECATED - All imports from config_ssot
│
├── src/core/config_browser.py (53 lines)
│   ├── BrowserConfig dataclass (uses get_config from config_core)
│   └── Status: ⚠️ NEEDS UPDATE - Should use config_ssot directly
│
└── src/core/config_thresholds.py (65 lines)
    ├── ThresholdConfig dataclass (uses get_config from config_core)
    └── Status: ⚠️ NEEDS UPDATE - Should use config_ssot directly
```

**Note**: `src/shared_utils/config.py` is NOT a shim - it provides `get_setting()` utility (different from `get_config()`).

---

## 🔗 DEPENDENCY GRAPH

### **Direct SSOT Imports (Preferred)**

**Files using config_ssot directly**:
1. `src/core/__init__.py` - Imports config_ssot module
2. `src/utils/config_remediator.py` - Auto-migration tool
3. `src/utils/config_auto_migrator.py` - Auto-migration tool

**Total**: 3 files (preferred approach)

### **Shim Imports (Backward Compatible)**

#### **1. config_core.py Shim**

**Files importing from config_core**:
1. `src/core/__init__.py` - Module import
2. `src/core/config_browser.py` - Uses `get_config` from config_core ⚠️
3. `src/core/config_thresholds.py` - Uses `get_config` from config_core ⚠️

**Total**: 3 files (2 need update)

#### **2. unified_config.py Shim**

**Files importing from unified_config**:
1. `src/core/__init__.py` - Module import
2. `src/orchestrators/overnight/recovery.py` - `get_unified_config`
3. `src/orchestrators/overnight/monitor.py` - `get_unified_config`
4. `src/workflows/engine.py` - `get_unified_config`
5. `src/vision/utils.py` - `get_unified_config`
6. `src/vision/ocr.py` - Via utils
7. `src/vision/integration.py` - `get_unified_config`
8. `src/vision/capture.py` - Via utils
9. `src/vision/analysis.py` - `get_unified_config`
10. `src/orchestrators/overnight/orchestrator.py` - `get_unified_config`
11. `src/orchestrators/overnight/scheduler_refactored.py` - `get_unified_config`
12. `src/orchestrators/overnight/scheduler_deprecated.py` - `get_unified_config`
13. `src/orchestrators/overnight/scheduler.py` - `get_unified_config`

**Total**: 13 files (all backward compatible via shim)

#### **3. config_browser.py Shim**

**Files importing from config_browser**:
1. `src/core/__init__.py` - Module import

**Total**: 1 file (module import only)

#### **4. config_thresholds.py Shim**

**Files importing from config_thresholds**:
1. `src/core/__init__.py` - Module import

**Total**: 1 file (module import only)

---

## 🚨 CRITICAL DEPENDENCIES

### **Files That Need Update**

#### **1. src/core/config_browser.py** ⚠️
**Current**:
```python
from .config_core import get_config
```

**Should Be**:
```python
from .config_ssot import get_config
```

**Impact**: Low (only used internally, not imported elsewhere)

#### **2. src/core/config_thresholds.py** ⚠️
**Current**:
```python
from .config_core import get_config
```

**Should Be**:
```python
from .config_ssot import get_config
```

**Impact**: Low (only used internally, not imported elsewhere)

---

## 📋 FACADE MAPPING TABLE

### **Exported Symbols Mapping**

| Symbol | config_ssot | config_core | unified_config | config_browser | config_thresholds |
|--------|-------------|-------------|---------------|----------------|-------------------|
| `get_config()` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `get_unified_config()` | ✅ | ❌ | ✅ (shim) | ❌ | ❌ |
| `get_agent_config()` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `get_timeout_config()` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `get_browser_config()` | ✅ | ❌ | ✅ (shim) | ❌ | ❌ |
| `get_threshold_config()` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `TimeoutConfig` | ✅ | ❌ | ✅ (shim) | ❌ | ❌ |
| `AgentConfig` | ✅ | ❌ | ✅ (shim) | ❌ | ❌ |
| `BrowserConfig` | ✅ | ❌ | ✅ (shim) | ✅ (class) | ❌ |
| `ThresholdConfig` | ✅ | ❌ | ✅ (shim) | ❌ | ✅ (class) |
| `UnifiedConfigManager` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `ConfigEnvironment` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `ConfigSource` | ✅ | ✅ (shim) | ✅ (shim) | ❌ | ❌ |
| `ReportFormat` | ✅ | ❌ | ✅ (shim) | ❌ | ❌ |

**Legend**:
- ✅ = Available
- ❌ = Not available
- (shim) = Re-exported from config_ssot
- (class) = Defined in file

---

## 🔄 IMPORT MIGRATION PATHS

### **Migration Priority**

#### **High Priority** (Internal shims)
1. `src/core/config_browser.py` → Use `config_ssot.get_config` directly
2. `src/core/config_thresholds.py` → Use `config_ssot.get_config` directly

#### **Medium Priority** (External usage - can wait)
3. `src/orchestrators/overnight/*.py` → Migrate to `config_ssot.get_unified_config`
4. `src/workflows/engine.py` → Migrate to `config_ssot.get_unified_config`
5. `src/vision/*.py` → Migrate to `config_ssot.get_unified_config`

**Note**: Medium priority items can remain on shims for backward compatibility.

---

## 🛡️ REGRESSION PREVENTION

### **Critical Rules**

1. ✅ **Never Break Shims**: All shim files must continue to work
2. ✅ **Never Remove Shim Exports**: All exported symbols must remain available
3. ✅ **Never Change Shim Signatures**: Function signatures must remain identical
4. ✅ **Always Test Shims**: Verify shim functionality after any changes
5. ✅ **Document Changes**: Update this map when shims change

### **Pre-Merge Validation**

**Before any goldmine merge**:
```bash
# Test all shim imports
python -c "from src.core.config_core import get_config; print('config_core OK')"
python -c "from src.core.unified_config import get_unified_config; print('unified_config OK')"
python -c "from src.core.config_browser import BrowserConfig; print('config_browser OK')"
python -c "from src.core.config_thresholds import ThresholdConfig; print('config_thresholds OK')"

# Test direct SSOT imports
python -c "from src.core.config_ssot import get_config, get_unified_config; print('config_ssot OK')"

# Run validation
python scripts/validate_config_ssot.py
```

### **Post-Merge Validation**

**After any goldmine merge**:
```bash
# Re-test all shims
# Re-run validation
# Verify no new config files created outside SSOT
# Update dependency map if changes made
```

---

## 📊 DEPENDENCY STATISTICS

### **Import Counts**

- **Direct SSOT imports**: 3 files
- **config_core shim imports**: 3 files (2 internal, 1 module)
- **unified_config shim imports**: 13 files
- **config_browser imports**: 1 file (module only)
- **config_thresholds imports**: 1 file (module only)

**Total files using config system**: 21 files

### **Shim Status**

- ✅ **config_core.py**: Fully functional shim (all exports from config_ssot)
- ✅ **unified_config.py**: Fully functional shim (all exports from config_ssot)
- ⚠️ **config_browser.py**: Needs update (uses config_core instead of config_ssot)
- ⚠️ **config_thresholds.py**: Needs update (uses config_core instead of config_ssot)

---

## 🔧 MAINTENANCE TASKS

### **Immediate (High Priority)**

1. [ ] Update `src/core/config_browser.py` to use `config_ssot.get_config` directly
2. [ ] Update `src/core/config_thresholds.py` to use `config_ssot.get_config` directly
3. [ ] Test both files after update
4. [ ] Verify no regressions

### **Future (Medium Priority)**

1. [ ] Migrate orchestrator files to direct config_ssot imports
2. [ ] Migrate workflow files to direct config_ssot imports
3. [ ] Migrate vision files to direct config_ssot imports
4. [ ] Document migration progress

### **Long-term (Low Priority)**

1. [ ] Consider removing shims after full migration (requires coordination)
2. [ ] Update all documentation to prefer config_ssot
3. [ ] Add linting rules to prefer config_ssot imports

---

## 📝 NOTES

### **Key Principles**

1. **SSOT First**: config_ssot is the single source of truth
2. **Backward Compatibility**: Shims maintain existing imports
3. **Gradual Migration**: Can migrate files over time
4. **No Breaking Changes**: All shims must remain functional
5. **Documentation**: Keep this map current

### **Shim Design Pattern**

**Shim Pattern**:
```python
# Deprecated shim file
import warnings
warnings.warn("File deprecated. Use config_ssot instead.", DeprecationWarning)

# Re-export from SSOT
from .config_ssot import (
    get_config,
    get_unified_config,
    # ... all exports
)

# Maintain backward compatibility
__all__ = [
    "get_config",
    "get_unified_config",
    # ... all exports
]
```

### **Tools Available**

- `scripts/validate_config_ssot.py` - SSOT validation
- `tools/ssot_config_validator.py` - Facade verification
- `src/utils/config_remediator.py` - Auto-migration tool
- `src/utils/config_auto_migrator.py` - Auto-migration tool

---

## ✅ SUCCESS CRITERIA

### **Facade Mapping Complete**

- [x] All shim files identified
- [x] All dependencies mapped
- [x] Import paths documented
- [x] Migration paths defined
- [x] Regression prevention checklist created
- [ ] High-priority updates completed (config_browser, config_thresholds)

### **Quality Gates**

- ✅ **Zero Breaking Changes**: All shims functional
- ✅ **100% Backward Compatibility**: Existing imports work
- ✅ **Documentation Current**: Map updated
- ✅ **Validation Passing**: All tests pass

---

## 🐝 WE. ARE. SWARM.

**Agent-8 - SSOT & System Integration Specialist**  
*Maintaining Config SSOT Facade Integrity*

**Status**: ✅ Dependency map created, ready for goldmine merges  
**Next Steps**: Update config_browser.py and config_thresholds.py to use config_ssot directly

---

*Last Updated: 2025-01-27*  
*Version: 1.0*


