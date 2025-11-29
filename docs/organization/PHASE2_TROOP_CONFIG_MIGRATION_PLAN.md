# 🏆 Phase 2: TROOP Config Migration Plan

**Created**: 2025-11-24  
**Agent**: Agent-6 (Coordination & Communication Specialist)  
**Status**: 🚀 **EXECUTION READY**  
**Priority**: MEDIUM - Standalone Goldmine

---

## 🎯 **MIGRATION OBJECTIVE**

Migrate TROOP config file to use `config_ssot` as SSOT. TROOP is a standalone goldmine (no merge planned), so this is a simple migration.

**Target**: Zero SSOT violations, 100% backward compatibility, zero regressions.

---

## 📊 **CONFIG FILE TO MIGRATE**

### **`Scripts/Utilities/config_handling/config.py`** (21 lines) - LOW PRIORITY

**Current Structure**:
- Small utility config (accessors only)
- 21 lines, 536 bytes
- Simple accessor functions

**SSOT Mapping**:
- Config accessors → `config_ssot.get_config()`
- Simple migration path

**Migration Strategy**:
1. Create shim for backward compatibility (if needed)
2. Update imports to config_ssot
3. Test functionality
4. Document changes

---

## 🔧 **MIGRATION EXECUTION PLAN**

### **Phase 1: Analysis** (IMMEDIATE) ✅ COMPLETE

**Actions**:
1. [x] Scan TROOP for config imports
2. [x] Analyze config.py usage
3. [x] Document dependencies

**Results**:
- **Total files with config imports**: 7 files
- **Import pattern**: All import `setup_logging` from `Utilities.config_handling.config`
- **Files**:
  1. `Scripts/Backtesting/backtest_strategy.py`
  2. `Scripts/Data_Fetchers/fetch_financial_data.py`
  3. `Scripts/Data_Processing/apply_indicators.py`
  4. `Scripts/MLIntegration/predict_signals.py`
  5. `Scripts/RiskManagement/risk_calculator.py`
  6. `Scripts/Scheduler/scheduler.py`
  7. `Scripts/model_training/optimize_hyperparameters.py`

**Analysis**:
- `config.py` only provides `setup_logging()` function (logging setup, not config management)
- `get_config_value()` function exists but not used in dependencies
- Simple migration: Create shim that maps to standard Python logging

**Deliverable**: ✅ `docs/organization/PHASE2_TROOP_DEPENDENCY_MAP.json` - COMPLETE

---

### **Phase 2: Shim Creation** (IMMEDIATE)

**Strategy**: Create minimal shim if backward compatibility needed.

**Shim**: `TROOP/Scripts/Utilities/config_handling/config_shim.py`
```python
"""
Config Shim - Backward Compatibility Layer for TROOP

Maintains setup_logging() compatibility while migrating to standard logging.
"""

import logging
import os

def setup_logging(log_file: str = "troop.log"):
    """Setup logging - backward compatibility shim."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def get_config_value(key: str, default=None):
    """Get config value from environment - maps to config_ssot if available."""
    # Try config_ssot first
    try:
        import sys
        from pathlib import Path
        repo_root = Path(__file__).parent.parent.parent.parent.parent / "Agent_Cellphone_V2_Repository"
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        
        import importlib.util
        config_ssot_path = repo_root / "src" / "core" / "config_ssot.py"
        if config_ssot_path.exists():
            spec = importlib.util.spec_from_file_location("config_ssot", config_ssot_path)
            config_ssot = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_ssot)
            return config_ssot.get_config(key, default)
    except:
        pass
    
    # Fallback to environment variable
    return os.getenv(key, default)

__all__ = ["setup_logging", "get_config_value"]
```

**Note**: TROOP's config.py is primarily for logging setup, not config management. Migration is simple - maintain logging compatibility.

---

### **Phase 3: Import Updates** (NEXT)

**Actions**:
1. [ ] Update imports to use config_ssot or shim
2. [ ] Test functionality
3. [ ] Verify no regressions

---

### **Phase 4: Testing & Validation** (CRITICAL)

**Test Checklist**:
- [ ] Config access works
- [ ] No regressions
- [ ] SSOT validation passes

---

## 📋 **EXECUTION CHECKLIST**

- [x] Config file identified
- [x] Migration plan created
- [x] Dependency analysis complete ✅ (7 files, setup_logging imports)
- [x] Shim created ✅ (config_shim.py created)
- [ ] Imports updated (7 files) - PENDING
- [ ] Testing complete

---

## 🎯 **SUCCESS CRITERIA**

- ✅ Zero SSOT violations
- ✅ 100% backward compatibility
- ✅ Zero regressions
- ✅ All tests passing

---

**Status**: 🚀 **READY FOR EXECUTION**

**Next Step**: Execute Phase 1 - Dependency Analysis

🐝 WE. ARE. SWARM. ⚡🔥

