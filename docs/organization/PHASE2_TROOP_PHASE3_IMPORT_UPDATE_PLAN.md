# 🔄 Phase 3: TROOP Config Migration - Import Updates

**Created**: 2025-01-28  
**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Status**: 🚀 **READY FOR EXECUTION**  
**Priority**: MEDIUM

---

## 🎯 **PHASE 3 OBJECTIVE**

Update imports in 7 TROOP Scripts files to use the config shim created in Phase 2.

**Target**: All files updated to use `config_shim.py` instead of `config.py`

---

## 📊 **FILES TO UPDATE**

Based on Phase 1 dependency analysis, the following 7 files need import updates:

1. `Scripts/Backtesting/backtest_strategy.py` (line 4)
2. `Scripts/Data_Fetchers/fetch_financial_data.py` (line 4)
3. `Scripts/Data_Processing/apply_indicators.py` (line 5)
4. `Scripts/MLIntegration/predict_signals.py` (line 5)
5. `Scripts/RiskManagement/risk_calculator.py` (line 4)
6. `Scripts/Scheduler/scheduler.py` (line 6)
7. `Scripts/model_training/optimize_hyperparameters.py` (line 8)

**Note**: `Scripts/strategy/moving_average_crossover.py` also imports setup_logging (8th file)

---

## 🔧 **IMPORT UPDATE STRATEGY**

### **Current Import Pattern**:
```python
from Utilities.config_handling.config import setup_logging
```

### **Updated Import Pattern**:
```python
from Utilities.config_handling.config_shim import setup_logging
```

**Alternative** (if shim is in same directory):
```python
from .config_shim import setup_logging
```

---

## 📋 **EXECUTION CHECKLIST**

- [ ] Locate TROOP repository (check temp_repos or repos root)
- [ ] Verify config_shim.py exists at `Scripts/Utilities/config_handling/config_shim.py`
- [ ] Update import in `Scripts/Backtesting/backtest_strategy.py`
- [ ] Update import in `Scripts/Data_Fetchers/fetch_financial_data.py`
- [ ] Update import in `Scripts/Data_Processing/apply_indicators.py`
- [ ] Update import in `Scripts/MLIntegration/predict_signals.py`
- [ ] Update import in `Scripts/RiskManagement/risk_calculator.py`
- [ ] Update import in `Scripts/Scheduler/scheduler.py`
- [ ] Update import in `Scripts/model_training/optimize_hyperparameters.py`
- [ ] Update import in `Scripts/strategy/moving_average_crossover.py` (if needed)
- [ ] Test imports (verify no import errors)
- [ ] Verify functionality (run basic tests if available)

---

## 🎯 **SUCCESS CRITERIA**

- ✅ All 7-8 files updated with new import
- ✅ No import errors
- ✅ Functionality preserved (setup_logging works)
- ✅ Backward compatibility maintained via shim

---

## 📝 **NOTES**

- TROOP is a standalone goldmine (no merge planned)
- Simple migration: Only logging setup, not config management
- Shim provides backward compatibility
- All files import `setup_logging` only (no other config functions used)

---

**Status**: 🚀 **READY FOR EXECUTION**  
**Next Step**: Locate TROOP repository and execute import updates

🐝 WE. ARE. SWARM. ⚡🔥

