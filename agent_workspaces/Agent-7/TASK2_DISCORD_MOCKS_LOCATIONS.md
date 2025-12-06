# TASK 2: Discord Test Mocks Consolidation Phase 3 - Location Analysis

**Date**: 2025-12-05 14:00:00  
**Status**: IN PROGRESS  
**Target**: 9 locations

---

## 📋 **LOCATIONS FOUND** (3/9 - 33%)

### **Production Files Using test_utils.py** (3 locations):

1. ✅ **`src/discord_commander/github_book_viewer.py`**
   - Uses: `from .test_utils import get_mock_discord`
   - Status: ✅ Already using SSOT

2. ✅ **`src/discord_commander/messaging_commands.py`**
   - Uses: `from .test_utils import get_mock_discord`
   - Status: ✅ Already using SSOT

3. ✅ **`src/discord_commander/controllers/messaging_controller_view.py`**
   - Uses: `from ..test_utils import get_mock_discord`
   - Status: ✅ Already using SSOT

---

## 🔍 **TEST FILES ANALYSIS** (Need to Check)

### **Test Files Found** (4 files):
1. `tests/discord/test_messaging_commands.py` - Uses `sys.modules` mocking (not test_utils)
2. `tests/discord/test_messaging_controller.py` - Uses `sys.modules` mocking (not test_utils)
3. `tests/discord/test_discord_gui_controller.py` - Uses `sys.modules` mocking (not test_utils)
4. `tests/discord/test_discord_service.py` - Need to check

---

## 🎯 **PHASE 3 ACTIONS NEEDED**

### **Option 1: Convert test files to use test_utils.py**
- Convert `sys.modules` mocking to use unified `test_utils.py`
- Create unified utilities for common mock patterns
- Update all test files to use unified utilities

### **Option 2: Create additional unified utilities**
- Create mock factories for common test scenarios
- Create mock fixtures that can be reused
- Document mock usage patterns

---

## 📊 **NEXT STEPS**

1. ⏳ Check all 4 test files for mock usage patterns
2. ⏳ Identify 6 more locations (may include test files or other production files)
3. ⏳ Create unified utilities for common mock patterns
4. ⏳ Update all locations to use unified utilities

---

**Status**: 🔍 **ANALYZING** - 3/9 locations found, analyzing test files for additional locations


