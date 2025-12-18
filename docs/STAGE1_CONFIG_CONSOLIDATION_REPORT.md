# Configuration Classes Consolidation Report
**Date**: 2025-12-17  
**Agent**: Agent-5  
**Task**: A5-STAGE1-DUPLICATE-001  
**Purpose**: Consolidate duplicate configuration classes per duplication check findings

---

## 📋 Consolidation Plan

### SSOT Designation
- **SSOT**: `src/core/config/config_dataclasses.py` ✅ (for BrowserConfig, ThresholdConfig)
- **SSOT**: `src/core/config/timeout_constants.py` ✅ (for TimeoutConstants)
- **Deprecated**: Various duplicate locations ⚠️

### Class Mappings

| Config Class | Duplicate Locations | SSOT Location |
|--------------|---------------------|---------------|
| BrowserConfig | `src/core/config_browser.py`<br>`src/infrastructure/browser/browser_models.py` | `src/core/config/config_dataclasses.py` |
| ThresholdConfig | `src/core/config_thresholds.py` | `src/core/config/config_dataclasses.py` |
| TimeoutConstants | `src/core/performance/coordination_performance_monitor.py` | `src/core/config/timeout_constants.py` |

---

## 🔍 Import Analysis

### Files Using Duplicate Config Imports


**src\infrastructure\browser\thea_browser_core.py**
- Line 29: from .browser_models import BrowserConfig, TheaConfig

**src\infrastructure\browser\thea_browser_service.py**
- Line 25: from .browser_models import BrowserConfig, TheaConfig

---

## ✅ Consolidation Steps

1. **Add Deprecation Warnings**
   - Add deprecation warnings to duplicate config class files
   - Direct users to SSOT locations

2. **Update Imports**
   - Update all imports from duplicate locations to SSOT
   - Use the mapping table above

3. **Verify Functionality**
   - Test that SSOT config classes work correctly
   - Ensure no functionality is lost
   - Check for API differences between duplicates

4. **Remove Deprecated Files**
   - After migration complete, remove or consolidate duplicate files
   - Update documentation

---

## 📊 Expected Impact

- **Duplicate Classes Eliminated**: ~3 (BrowserConfig, ThresholdConfig, TimeoutConstants)
- **Code Consolidation**: Multiple locations → SSOT config files
- **Maintainability**: Single source of truth for configuration classes

---

## 🔄 Next Steps

1. Review duplicate config class implementations
2. Ensure SSOT versions have all needed functionality
3. Add deprecation warnings to duplicate files
4. Update imports across codebase
5. Test and verify functionality
6. Remove deprecated files after migration

---

## ⚠️ Notes

- `BrowserConfig` appears in 3 locations with potentially different APIs
- Need to verify all functionality is preserved in SSOT version
- Some duplicates may have additional properties/methods to migrate

---

🐝 **WE. ARE. SWARM. ⚡🔥**
