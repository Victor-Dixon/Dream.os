# Batch 4 Onboarding Services Refactoring - Execution Guide

**Date:** 2025-12-19  
**Agent:** Agent-2 (Architecture & Design Specialist)  
**Request:** Architecture guidance for Batch 4 refactoring execution  
**Status:** ✅ EXECUTION GUIDE COMPLETE

---

## Executive Summary

**Files to Refactor:**
- `hard_onboarding_service.py`: 880 lines → <500 lines (target: ~200 lines)
- `soft_onboarding_service.py`: 533 lines → <500 lines (target: ~200 lines)

**Pattern:** Service Layer Pattern with Protocol Step Extraction  
**Estimated Reduction:** 1,413 lines → ~400 lines (72% reduction)  
**Timeline:** 2 cycles (can be parallelized)

---

## 1. Current State Analysis

### **1.1 hard_onboarding_service.py (880 lines)**

**Current Structure:**
- `HardOnboardingService` class (BaseService)
- 5 protocol step methods (step_1 through step_5)
- Large agent-specific instructions mapping (~400+ lines)
- Coordinate loading/validation
- PyAutoGUI operations
- Main execution method (`execute_hard_onboarding`)
- Standalone functions (`hard_onboard_agent`, `hard_onboard_multiple_agents`)

**Key Components:**
1. **Protocol Steps** (~200 lines):
   - `step_1_clear_chat()` - Clear chat with Ctrl+Shift+Backspace
   - `step_2_send_execute()` - Execute with Ctrl+Enter
   - `step_3_new_window()` - Create new window with Ctrl+N
   - `step_4_navigate_to_onboarding()` - Navigate to onboarding coords
   - `step_5_send_onboarding_message()` - Send onboarding message

2. **Agent Instructions** (~400 lines):
   - Large mapping of agent-specific instructions
   - Already extracted to `onboarding/agent_instructions.py` (via `_get_agent_specific_instructions()`)

3. **Coordinate Management** (~50 lines):
   - `_load_agent_coordinates()` - Delegates to `onboarding_helpers`
   - `_validate_coordinates()` - Delegates to `onboarding_helpers`

4. **PyAutoGUI Operations** (~150 lines):
   - Embedded in step methods
   - Mouse movements, clicks, hotkeys
   - Clipboard operations

5. **Main Execution** (~80 lines):
   - `execute_hard_onboarding()` - Orchestrates all steps

**Refactoring Opportunities:**
- ✅ Agent instructions already extracted (good)
- ⚠️ Protocol steps can be extracted to separate module
- ⚠️ PyAutoGUI operations can be abstracted
- ⚠️ Coordinate management already delegated (good)

---

### **1.2 soft_onboarding_service.py (533 lines)**

**Current Structure:**
- `SoftOnboardingService` class (BaseService)
- 6 protocol step methods (step_1 through step_6)
- Coordinate loading
- PyAutoGUI operations
- Fallback messaging operations
- Main execution method (`execute_soft_onboarding`)
- Standalone functions (`soft_onboard_agent`, `soft_onboard_multiple_agents`)
- Cycle accomplishments report function (unrelated, should be moved)

**Key Components:**
1. **Protocol Steps** (~250 lines):
   - `step_1_click_chat_input()` - Click chat input
   - `step_2_save_session()` - Save session (Ctrl+Enter)
   - `step_3_send_cleanup_prompt()` - Send cleanup message
   - `step_4_open_new_tab()` - Open new tab (Ctrl+T)
   - `step_5_navigate_to_onboarding()` - Navigate to onboarding coords
   - `step_6_paste_onboarding_message()` - Paste and send message

2. **Coordinate Management** (~30 lines):
   - `_load_agent_coordinates()` - Uses coordinate loader

3. **PyAutoGUI Operations** (~150 lines):
   - Embedded in step methods
   - Mouse movements, clicks, hotkeys
   - Clipboard operations

4. **Messaging Fallback** (~50 lines):
   - `_send_cleanup_via_messaging()` - Fallback for cleanup
   - `_send_onboarding_via_messaging()` - Fallback for onboarding

5. **Main Execution** (~50 lines):
   - `execute_soft_onboarding()` - Orchestrates all steps

6. **Unrelated Function** (~50 lines):
   - `generate_cycle_accomplishments_report()` - Should be moved to separate module

**Refactoring Opportunities:**
- ⚠️ Protocol steps can be extracted to separate module
- ⚠️ PyAutoGUI operations can be abstracted
- ⚠️ Messaging fallback can be extracted
- ⚠️ Cycle accomplishments function should be moved

---

## 2. Refactoring Strategy

### **2.1 Shared Components (Extract First)**

**Create:** `src/services/onboarding/shared/`

**Files to Create:**
1. **`operations.py`** (~150 lines) - Shared PyAutoGUI operations
   ```python
   class PyAutoGUIOperations:
       """Shared PyAutoGUI operations for onboarding."""
       
       def click_at_coords(self, x: int, y: int, duration: float = 0.5) -> bool:
           """Click at coordinates with animation."""
           ...
       
       def send_hotkey(self, *keys: str, wait: float = 0.8) -> bool:
           """Send hotkey combination."""
           ...
       
       def paste_text(self, text: str) -> bool:
           """Paste text via clipboard."""
           ...
       
       def clear_input(self) -> bool:
           """Clear input field (Ctrl+A, Delete)."""
           ...
   ```

2. **`coordinates.py`** (~50 lines) - Already exists in `onboarding_helpers.py`, can create wrapper
   ```python
   class OnboardingCoordinates:
       """Coordinate management for onboarding."""
       
       def load_coordinates(self, agent_id: str) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
           """Load chat and onboarding coordinates."""
           ...
       
       def validate_coordinates(self, agent_id: str, coords: Tuple[int, int]) -> bool:
           """Validate coordinates."""
           ...
   ```

**Benefits:**
- Shared utilities reduce duplication
- Easier to test PyAutoGUI operations
- Consistent coordinate handling

---

### **2.2 Hard Onboarding Refactoring**

**Create:** `src/services/onboarding/hard/`

**Files to Create:**
1. **`steps.py`** (~250 lines) - Protocol step implementations
   ```python
   class HardOnboardingSteps:
       """Hard onboarding protocol steps."""
       
       def __init__(self, pyautogui_ops: PyAutoGUIOperations, coords: OnboardingCoordinates):
           self.ops = pyautogui_ops
           self.coords = coords
       
       def step_1_clear_chat(self, agent_id: str) -> bool:
           """Step 1: Clear chat with Ctrl+Shift+Backspace."""
           ...
       
       def step_2_send_execute(self) -> bool:
           """Step 2: Execute with Ctrl+Enter."""
           ...
       
       def step_3_new_window(self) -> bool:
           """Step 3: Create new window with Ctrl+N."""
           ...
       
       def step_4_navigate_to_onboarding(self, agent_id: str) -> bool:
           """Step 4: Navigate to onboarding coordinates."""
           ...
       
       def step_5_send_onboarding_message(self, agent_id: str, message: str) -> bool:
           """Step 5: Send onboarding message."""
           ...
   ```

2. **`service.py`** (~200 lines) - Main service (orchestrator)
   ```python
   class HardOnboardingService(BaseService):
       """Hard onboarding service (refactored)."""
       
       def __init__(self):
           super().__init__("HardOnboardingService")
           self.steps = HardOnboardingSteps(...)
           ...
       
       def execute_hard_onboarding(self, agent_id: str, message: str, role: str = None) -> bool:
           """Execute hard onboarding protocol."""
           # Orchestrate steps
           ...
   ```

3. **`__init__.py`** - Module exports

**Estimated Reduction:** 880 → ~200 lines (77% reduction)

---

### **2.3 Soft Onboarding Refactoring**

**Create:** `src/services/onboarding/soft/`

**Files to Create:**
1. **`steps.py`** (~300 lines) - Protocol step implementations
   ```python
   class SoftOnboardingSteps:
       """Soft onboarding protocol steps."""
       
       def __init__(self, pyautogui_ops: PyAutoGUIOperations, coords: OnboardingCoordinates):
           self.ops = pyautogui_ops
           self.coords = coords
       
       def step_1_click_chat_input(self, agent_id: str) -> bool:
           """Step 1: Click chat input."""
           ...
       
       def step_2_save_session(self) -> bool:
           """Step 2: Save session (Ctrl+Enter)."""
           ...
       
       def step_3_send_cleanup_prompt(self, agent_id: str, message: str = None) -> bool:
           """Step 3: Send cleanup prompt."""
           ...
       
       def step_4_open_new_tab(self) -> bool:
           """Step 4: Open new tab (Ctrl+T)."""
           ...
       
       def step_5_navigate_to_onboarding(self, agent_id: str) -> bool:
           """Step 5: Navigate to onboarding coordinates."""
           ...
       
       def step_6_paste_onboarding_message(self, agent_id: str, message: str) -> bool:
           """Step 6: Paste and send onboarding message."""
           ...
   ```

2. **`messaging_fallback.py`** (~100 lines) - Messaging fallback operations
   ```python
   class OnboardingMessagingFallback:
       """Fallback messaging for onboarding when PyAutoGUI unavailable."""
       
       def send_cleanup_via_messaging(self, agent_id: str, message: str = None) -> bool:
           """Send cleanup message via messaging system."""
           ...
       
       def send_onboarding_via_messaging(self, agent_id: str, message: str) -> bool:
           """Send onboarding message via messaging system."""
           ...
   ```

3. **`service.py`** (~200 lines) - Main service (orchestrator)
   ```python
   class SoftOnboardingService(BaseService):
       """Soft onboarding service (refactored)."""
       
       def __init__(self):
           super().__init__("SoftOnboardingService")
           self.steps = SoftOnboardingSteps(...)
           self.messaging_fallback = OnboardingMessagingFallback()
           ...
       
       def execute_soft_onboarding(self, agent_id: str, message: str, **kwargs) -> bool:
           """Execute soft onboarding protocol."""
           # Orchestrate steps
           ...
   ```

4. **`__init__.py`** - Module exports

**Additional Refactoring:**
- Move `generate_cycle_accomplishments_report()` to `tools/generate_cycle_accomplishments_report.py` (already exists)

**Estimated Reduction:** 533 → ~200 lines (62% reduction)

---

## 3. Detailed Refactoring Steps

### **Phase 1: Extract Shared Components**

**Step 1.1: Create Shared Operations Module**
- [ ] Create `src/services/onboarding/shared/operations.py`
- [ ] Extract PyAutoGUI operations from both services
- [ ] Create `PyAutoGUIOperations` class
- [ ] Methods: `click_at_coords()`, `send_hotkey()`, `paste_text()`, `clear_input()`
- [ ] Test operations independently

**Step 1.2: Create Shared Coordinates Module**
- [ ] Create `src/services/onboarding/shared/coordinates.py` (or use existing `onboarding_helpers.py`)
- [ ] Wrap existing coordinate functions
- [ ] Create `OnboardingCoordinates` class (optional, can use functions)
- [ ] Test coordinate loading/validation

**Deliverables:**
- ✅ Shared operations module
- ✅ Shared coordinates module (or wrapper)
- ✅ Tests for shared components

---

### **Phase 2: Refactor Hard Onboarding**

**Step 2.1: Create Hard Onboarding Steps Module**
- [ ] Create `src/services/onboarding/hard/steps.py`
- [ ] Create `HardOnboardingSteps` class
- [ ] Extract step_1 through step_5 methods
- [ ] Inject shared operations and coordinates
- [ ] Test each step independently

**Step 2.2: Create Hard Onboarding Service Module**
- [ ] Create `src/services/onboarding/hard/service.py`
- [ ] Create `HardOnboardingService` class
- [ ] Inject steps, operations, coordinates
- [ ] Implement `execute_hard_onboarding()` orchestrator
- [ ] Test full execution flow

**Step 2.3: Create Backward Compatibility Shim**
- [ ] Update `hard_onboarding_service.py` to import from new module
- [ ] Maintain existing API (class and functions)
- [ ] Test backward compatibility
- [ ] Update imports if needed

**Deliverables:**
- ✅ Hard onboarding steps module (~250 lines)
- ✅ Hard onboarding service module (~200 lines)
- ✅ Backward compatibility shim (~50 lines)
- ✅ Tests passing

---

### **Phase 3: Refactor Soft Onboarding**

**Step 3.1: Create Soft Onboarding Steps Module**
- [ ] Create `src/services/onboarding/soft/steps.py`
- [ ] Create `SoftOnboardingSteps` class
- [ ] Extract step_1 through step_6 methods
- [ ] Inject shared operations and coordinates
- [ ] Test each step independently

**Step 3.2: Create Messaging Fallback Module**
- [ ] Create `src/services/onboarding/soft/messaging_fallback.py`
- [ ] Extract `_send_cleanup_via_messaging()` and `_send_onboarding_via_messaging()`
- [ ] Create `OnboardingMessagingFallback` class
- [ ] Test messaging fallback

**Step 3.3: Create Soft Onboarding Service Module**
- [ ] Create `src/services/onboarding/soft/service.py`
- [ ] Create `SoftOnboardingService` class
- [ ] Inject steps, operations, coordinates, messaging fallback
- [ ] Implement `execute_soft_onboarding()` orchestrator
- [ ] Test full execution flow

**Step 3.4: Move Unrelated Function**
- [ ] Move `generate_cycle_accomplishments_report()` to `tools/generate_cycle_accomplishments_report.py` (verify it doesn't already exist)
- [ ] Update imports if needed

**Step 3.5: Create Backward Compatibility Shim**
- [ ] Update `soft_onboarding_service.py` to import from new module
- [ ] Maintain existing API (class and functions)
- [ ] Test backward compatibility
- [ ] Update imports if needed

**Deliverables:**
- ✅ Soft onboarding steps module (~300 lines)
- ✅ Messaging fallback module (~100 lines)
- ✅ Soft onboarding service module (~200 lines)
- ✅ Backward compatibility shim (~50 lines)
- ✅ Unrelated function moved
- ✅ Tests passing

---

## 4. Module Structure (Final)

```
src/services/onboarding/
├── __init__.py
├── onboarding_helpers.py (existing - coordinate helpers)
├── agent_instructions.py (existing - agent instructions)
├── onboarding_template_loader.py (existing)
├── shared/
│   ├── __init__.py
│   ├── operations.py (PyAutoGUI operations - NEW)
│   └── coordinates.py (coordinate wrapper - NEW, optional)
├── hard/
│   ├── __init__.py
│   ├── service.py (HardOnboardingService - NEW)
│   └── steps.py (HardOnboardingSteps - NEW)
└── soft/
    ├── __init__.py
    ├── service.py (SoftOnboardingService - NEW)
    ├── steps.py (SoftOnboardingSteps - NEW)
    └── messaging_fallback.py (OnboardingMessagingFallback - NEW)

src/services/
├── hard_onboarding_service.py (shim - UPDATED)
└── soft_onboarding_service.py (shim - UPDATED)
```

---

## 5. Validation Approach

### **5.1 Pre-Refactoring Validation**

**Checklist:**
- [ ] Document current behavior (test cases)
- [ ] Identify all call sites
- [ ] Verify test coverage
- [ ] Create integration test suite
- [ ] Document API contracts

**Test Cases to Document:**
- Hard onboarding: All 5 steps execute correctly
- Soft onboarding: All 6 steps execute correctly
- Coordinate loading: Works for all agents
- PyAutoGUI fallback: Messaging system works when PyAutoGUI unavailable
- Error handling: Invalid coordinates, missing agents, etc.

---

### **5.2 During Refactoring Validation**

**After Each Phase:**
- [ ] Run existing tests
- [ ] Verify no regressions
- [ ] Check line counts
- [ ] Validate imports
- [ ] Test backward compatibility

**Validation Commands:**
```bash
# Check line counts
python -c "with open('src/services/onboarding/hard/service.py') as f: print(len(f.readlines()))"
python -c "with open('src/services/onboarding/soft/service.py') as f: print(len(f.readlines()))"

# Run tests
pytest tests/ -k onboarding

# Check imports
python -c "from src.services.onboarding.hard.service import HardOnboardingService; print('✅ Import works')"
python -c "from src.services.onboarding.soft.service import SoftOnboardingService; print('✅ Import works')"
```

---

### **5.3 Post-Refactoring Validation**

**Integration Testing:**
- [ ] Test hard onboarding end-to-end
- [ ] Test soft onboarding end-to-end
- [ ] Test backward compatibility (old imports still work)
- [ ] Test error handling
- [ ] Test PyAutoGUI unavailable scenario
- [ ] Test coordinate validation
- [ ] Test all agent IDs

**Code Quality:**
- [ ] V2 compliance: All files <400 lines ✅
- [ ] Functions <100 lines ✅
- [ ] No circular dependencies
- [ ] Proper error handling
- [ ] Documentation complete
- [ ] Type hints present

**Performance:**
- [ ] No performance regressions
- [ ] Memory usage acceptable
- [ ] Execution time similar

---

## 6. Backward Compatibility Strategy

### **6.1 Shim Implementation**

**hard_onboarding_service.py (Shim):**
```python
"""
Hard Onboarding Service - Backward Compatibility Shim
====================================================

This module maintains backward compatibility while delegating to refactored modules.
"""

from src.services.onboarding.hard.service import HardOnboardingService
from src.services.onboarding.hard.service import execute_hard_onboarding
from src.services.onboarding.hard.service import hard_onboard_agent
from src.services.onboarding.hard.service import hard_onboard_multiple_agents

# Re-export for backward compatibility
__all__ = [
    "HardOnboardingService",
    "execute_hard_onboarding",
    "hard_onboard_agent",
    "hard_onboard_multiple_agents",
]
```

**soft_onboarding_service.py (Shim):**
```python
"""
Soft Onboarding Service - Backward Compatibility Shim
=====================================================

This module maintains backward compatibility while delegating to refactored modules.
"""

from src.services.onboarding.soft.service import SoftOnboardingService
from src.services.onboarding.soft.service import execute_soft_onboarding
from src.services.onboarding.soft.service import soft_onboard_agent
from src.services.onboarding.soft.service import soft_onboard_multiple_agents

# Re-export for backward compatibility
__all__ = [
    "SoftOnboardingService",
    "execute_soft_onboarding",
    "soft_onboard_agent",
    "soft_onboard_multiple_agents",
]
```

**Benefits:**
- No breaking changes
- Gradual migration possible
- Existing code continues to work
- Can update imports incrementally

---

## 7. Risk Mitigation

### **7.1 High Risk Areas**

**PyAutoGUI Operations:**
- **Risk:** Timing-sensitive operations may break
- **Mitigation:** Extract with same timing, test thoroughly
- **Validation:** Test with real UI interactions

**Coordinate Management:**
- **Risk:** Coordinate loading/validation changes
- **Mitigation:** Use existing `onboarding_helpers.py`, don't change logic
- **Validation:** Test with all agent IDs

**Agent Instructions:**
- **Risk:** Instructions mapping changes
- **Mitigation:** Already extracted, don't touch
- **Validation:** Verify instructions still load correctly

---

### **7.2 Testing Strategy**

**Unit Tests:**
- Test each step independently
- Mock PyAutoGUI operations
- Test error handling
- Test coordinate validation

**Integration Tests:**
- Test full onboarding flow
- Test with real coordinates (if possible)
- Test fallback scenarios
- Test error recovery

**Regression Tests:**
- Run existing test suite
- Test all call sites
- Test backward compatibility
- Test edge cases

---

## 8. Implementation Checklist

### **Phase 1: Shared Components**
- [ ] Create `onboarding/shared/operations.py`
- [ ] Extract PyAutoGUI operations
- [ ] Create `PyAutoGUIOperations` class
- [ ] Test operations
- [ ] Create `onboarding/shared/coordinates.py` (or use existing)
- [ ] Test coordinates

### **Phase 2: Hard Onboarding**
- [ ] Create `onboarding/hard/steps.py`
- [ ] Extract protocol steps
- [ ] Create `HardOnboardingSteps` class
- [ ] Test steps
- [ ] Create `onboarding/hard/service.py`
- [ ] Refactor main service
- [ ] Test service
- [ ] Update shim
- [ ] Test backward compatibility

### **Phase 3: Soft Onboarding**
- [ ] Create `onboarding/soft/steps.py`
- [ ] Extract protocol steps
- [ ] Create `SoftOnboardingSteps` class
- [ ] Test steps
- [ ] Create `onboarding/soft/messaging_fallback.py`
- [ ] Extract messaging fallback
- [ ] Test messaging fallback
- [ ] Create `onboarding/soft/service.py`
- [ ] Refactor main service
- [ ] Test service
- [ ] Move `generate_cycle_accomplishments_report()` (if needed)
- [ ] Update shim
- [ ] Test backward compatibility

### **Final Validation**
- [ ] All files <400 lines ✅
- [ ] All functions <100 lines ✅
- [ ] All tests passing ✅
- [ ] Backward compatibility verified ✅
- [ ] No regressions ✅
- [ ] Documentation updated ✅

---

## 9. Success Criteria

**File Size:**
- ✅ `hard_onboarding_service.py` (shim): <100 lines
- ✅ `onboarding/hard/service.py`: <300 lines
- ✅ `onboarding/hard/steps.py`: <300 lines
- ✅ `soft_onboarding_service.py` (shim): <100 lines
- ✅ `onboarding/soft/service.py`: <300 lines
- ✅ `onboarding/soft/steps.py`: <300 lines
- ✅ `onboarding/shared/operations.py`: <200 lines

**Functionality:**
- ✅ All protocol steps work correctly
- ✅ Backward compatibility maintained
- ✅ Error handling preserved
- ✅ Performance maintained

**Code Quality:**
- ✅ V2 compliant (all files <400 lines)
- ✅ Functions <100 lines
- ✅ Proper separation of concerns
- ✅ Good test coverage

---

## 10. Execution Timeline

**Cycle 1:**
- Day 1: Extract shared components
- Day 2: Refactor hard onboarding
- Day 3: Test hard onboarding

**Cycle 2:**
- Day 1: Refactor soft onboarding
- Day 2: Test soft onboarding
- Day 3: Final validation and documentation

**Total:** 2 cycles (6 days)

---

## 11. Next Steps

**Immediate Actions:**
1. Review this execution guide
2. Create shared components module
3. Begin Phase 1 (Extract Shared Components)

**Week 1:**
- Complete Phase 1 and Phase 2
- Hard onboarding refactored and tested

**Week 2:**
- Complete Phase 3
- Soft onboarding refactored and tested
- Final validation

---

## Conclusion

**Refactoring Strategy:** Service Layer Pattern with Protocol Step Extraction

**Key Approach:**
- Extract shared PyAutoGUI operations
- Extract protocol steps to separate modules
- Maintain backward compatibility with shims
- Preserve all functionality

**Expected Outcome:**
- 880 lines → ~200 lines (hard onboarding)
- 533 lines → ~200 lines (soft onboarding)
- 72% total reduction
- V2 compliant
- Maintainable and testable

**Recommendation:** Begin with Phase 1 (Shared Components) as foundation for both services.

---

🐝 **WE. ARE. SWARM. ⚡🔥**
