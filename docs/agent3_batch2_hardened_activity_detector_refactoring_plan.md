# Batch 2: hardened_activity_detector.py Refactoring Plan

**File**: `src/core/hardened_activity_detector.py`  
**Current Size**: 854 lines  
**Target**: 4 modules (<300 lines each)  
**Status**: Planning Complete ✅  
**Author**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-12-14

---

## Current Structure Analysis

### Classes (5):
1. `ActivityConfidence` (Enum) - 7 lines
2. `ActivitySource` (Enum) - 21 lines  
3. `ActivitySignal` (dataclass) - 8 lines
4. `ActivityAssessment` (dataclass) - 12 lines
5. `HardenedActivityDetector` (main class) - ~800 lines

### Methods in HardenedActivityDetector (17):
- `__init__` - Initialization
- `assess_agent_activity` - Main assessment method (~70 lines)
- `_check_telemetry_events` - Tier 1 source (~60 lines)
- `_get_telemetry_confidence` - Helper (~15 lines)
- `_check_git_activity` - Tier 1 source (~50 lines)
- `_check_git_activity_by_path` - Tier 1 source (~85 lines)
- `_parse_git_log_with_files` - Helper (~60 lines)
- `_check_contract_activity` - Tier 1 source (~50 lines)
- `_check_test_execution` - Tier 1 source (~40 lines)
- `_check_status_updates` - Tier 2 source (~65 lines)
- `_check_file_modifications` - Tier 2 source (~50 lines)
- `_check_devlog_activity` - Tier 2 source (~35 lines)
- `_check_inbox_processing` - Tier 2 source (~35 lines)
- `_filter_noise` - Helper (~10 lines)
- `_calculate_confidence` - Core logic (~60 lines)
- `_validate_signals` - Validation (~35 lines)

---

## Module Breakdown Plan

### Module 1: `activity_detector_models.py` (~50 lines)
**Purpose**: Data models and enums

**Contents**:
- `ActivityConfidence` (Enum)
- `ActivitySource` (Enum)
- `ActivitySignal` (dataclass)
- `ActivityAssessment` (dataclass)

**Dependencies**: None (pure models)

---

### Module 2: `activity_source_checkers.py` (~280 lines)
**Purpose**: Tier 1 & Tier 2 activity source checkers

**Contents**:
- `_check_telemetry_events` (~60 lines)
- `_get_telemetry_confidence` (~15 lines)
- `_check_git_activity` (~50 lines)
- `_check_git_activity_by_path` (~85 lines)
- `_parse_git_log_with_files` (~60 lines)
- `_check_contract_activity` (~50 lines)
- `_check_test_execution` (~40 lines)

**Dependencies**: 
- `activity_detector_models.py` (ActivitySignal, ActivitySource)
- External: subprocess, ContractManager

---

### Module 3: `activity_source_checkers_tier2.py` (~200 lines)
**Purpose**: Tier 2 activity source checkers

**Contents**:
- `_check_status_updates` (~65 lines)
- `_check_file_modifications` (~50 lines)
- `_check_devlog_activity` (~35 lines)
- `_check_inbox_processing` (~35 lines)

**Dependencies**:
- `activity_detector_models.py` (ActivitySignal, ActivitySource)

---

### Module 4: `hardened_activity_detector.py` (refactored, ~250 lines)
**Purpose**: Main orchestrator class

**Contents**:
- `__init__` - Initialization
- `assess_agent_activity` - Main assessment method
- `_filter_noise` - Noise filtering
- `_calculate_confidence` - Confidence calculation
- `_validate_signals` - Signal validation

**Dependencies**:
- `activity_detector_models.py` (all models)
- `activity_source_checkers.py` (Tier 1 checkers)
- `activity_source_checkers_tier2.py` (Tier 2 checkers)

---

## Refactoring Strategy

### Step 1: Extract Models
- Create `activity_detector_models.py`
- Move all enums and dataclasses
- Update imports in main file

### Step 2: Extract Tier 1 Checkers
- Create `activity_source_checkers.py`
- Move all Tier 1 source checking methods
- Keep helper methods with their related checkers

### Step 3: Extract Tier 2 Checkers
- Create `activity_source_checkers_tier2.py`
- Move all Tier 2 source checking methods

### Step 4: Refactor Main Class
- Update `HardenedActivityDetector` to use extracted modules
- Keep orchestration logic only
- Maintain backward compatibility

---

## V2 Compliance

- ✅ All modules <300 lines
- ✅ Single responsibility per module
- ✅ Clear dependency hierarchy
- ✅ Backward compatibility maintained
- ✅ SSOT domain tags applied

---

## Testing Strategy

1. **Unit Tests**: Test each checker module independently
2. **Integration Tests**: Test main detector with all checkers
3. **Backward Compatibility**: Ensure existing code still works
4. **Performance**: Verify no performance regression

---

## Estimated Effort

- **Module 1 (Models)**: 30 minutes
- **Module 2 (Tier 1 Checkers)**: 2 hours
- **Module 3 (Tier 2 Checkers)**: 1.5 hours
- **Module 4 (Refactor Main)**: 1 hour
- **Testing**: 1 hour
- **Total**: ~6 hours

---

## Next Steps

1. ✅ Planning complete
2. ⏳ Awaiting approval to proceed
3. ⏳ Begin Module 1 extraction when approved

---

**Status**: ✅ Planning Complete - Ready for Execution


