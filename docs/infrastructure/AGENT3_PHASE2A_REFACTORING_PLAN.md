# Agent-3 Phase 2A Infrastructure Refactoring Plan

## Overview
**File**: `src/core/messaging_pyautogui.py`  
**Current Size**: 775 lines (exceeds ~400-line V2 guideline)  
**Target**: ~400 lines per module (guideline, not hard limit)  
**Focus**: Clean, production-ready, scalable code with clear separation of concerns  
**Pattern**: Service Layer Pattern  
**Status**: Planning Phase

## Current Structure Analysis

### Main Components
1. **Helper Functions** (lines 42-115):
   - `get_message_tag()` - Determines message tag based on sender/recipient
   - `format_c2a_message()` - Formats message with correct tag

2. **PyAutoGUIMessagingDelivery Class** (lines 118-790):
   - `__init__()` - Initialization
   - `validate_coordinates()` - Coordinate validation (lines 126-185)
   - `send_message()` - Main entry point with retry logic (lines 187-231)
   - `_send_message_attempt()` - Single attempt with lock management (lines 233-330)
   - `_execute_delivery_operations()` - Actual delivery operations (lines 332-790)

3. **Legacy Functions** (lines 793-821):
   - `send_message_pyautogui()` - Legacy wrapper
   - `send_message_to_onboarding_coords()` - Legacy wrapper
   - `send_message_to_agent()` - Legacy wrapper

## Refactoring Strategy: Service Layer Pattern

### Module Extraction Plan

#### 1. CoordinateRoutingService (`src/core/messaging_coordinate_routing.py`)
**Responsibility**: Coordinate selection and routing logic  
**Extract from**: `_execute_delivery_operations()` lines 336-532  
**Key Functions**:
- `get_coordinates_for_message()` - Main coordinate selection logic
- `handle_agent4_routing()` - Agent-4 special case handling
- `validate_coordinate_selection()` - Coordinate validation
- `is_onboarding_message()` - Message type detection

**Estimated Size**: ~200 lines

#### 2. MessageFormattingService (`src/core/messaging_formatting.py`)
**Responsibility**: Message formatting and template detection  
**Extract from**: `_execute_delivery_operations()` lines 536-625, helper functions  
**Key Functions**:
- `format_message_content()` - Main formatting logic
- `detect_template_header()` - Template detection
- `get_message_tag()` - Tag determination (move from main file)
- `format_c2a_message()` - Message formatting (move from main file)

**Estimated Size**: ~150 lines

#### 3. ClipboardService (`src/core/messaging_clipboard.py`)
**Responsibility**: Clipboard operations with locking  
**Extract from**: `_execute_delivery_operations()` lines 690-722  
**Key Functions**:
- `copy_to_clipboard()` - Thread-safe clipboard copy
- `verify_clipboard()` - Clipboard verification
- `clear_clipboard()` - Clipboard clearing (if needed)

**Estimated Size**: ~80 lines

#### 4. PyAutoGUIOperationsService (`src/core/messaging_pyautogui_operations.py`)
**Responsibility**: PyAutoGUI operations (move, click, paste, send)  
**Extract from**: `_execute_delivery_operations()` lines 627-790  
**Key Functions**:
- `move_to_coordinates()` - Mouse movement with validation
- `focus_input_field()` - Input field focusing
- `clear_input_field()` - Input field clearing
- `paste_content()` - Content pasting
- `send_message()` - Message sending (Enter/Ctrl+Enter)

**Estimated Size**: ~200 lines

#### 5. Refactored Main File (`src/core/messaging_pyautogui.py`)
**Responsibility**: Orchestration and coordination  
**Keep**:
- `PyAutoGUIMessagingDelivery` class (orchestrator)
- `send_message()` - Main entry point with retry
- `_send_message_attempt()` - Single attempt coordination
- Legacy wrapper functions

**Use Services**:
- CoordinateRoutingService for coordinate selection
- MessageFormattingService for message formatting
- ClipboardService for clipboard operations
- PyAutoGUIOperationsService for GUI operations

**Estimated Size**: ~250 lines

## Implementation Steps

1. **Create Service Modules** (in order):
   - [ ] CoordinateRoutingService
   - [ ] MessageFormattingService
   - [ ] ClipboardService
   - [ ] PyAutoGUIOperationsService

2. **Refactor Main File**:
   - [ ] Update imports
   - [ ] Inject services into PyAutoGUIMessagingDelivery
   - [ ] Replace inline logic with service calls
   - [ ] Maintain backward compatibility

3. **Testing**:
   - [ ] Unit tests for each service
   - [ ] Integration tests for main class
   - [ ] Verify legacy functions still work

4. **Architecture Review**:
   - [ ] Coordinate with Agent-2 for checkpoint review
   - [ ] Validate Service Layer pattern implementation
   - [ ] Verify V2 compliance (all modules ~400 lines guideline, clean code principles)

## V2 Compliance Targets

- ✅ All modules ~400 lines (guideline - clean code principles take precedence)
- ✅ Service Layer pattern (clear separation of concerns)
- ✅ Dependency injection (services injected, not hardcoded)
- ✅ Backward compatibility (legacy functions preserved)
- ✅ SSOT domain tags maintained
- ✅ Single Responsibility Principle (each service has one clear purpose)
- ✅ Code quality, maintainability, and scalability prioritized over line counts

## Timeline

- **Phase 2A**: messaging_pyautogui.py refactoring
  - ETA: 1-2 cycles
  - Architecture review checkpoint: After completion

## Coordination

- **Agent-2**: Architecture review checkpoint after Phase 2A
- **Agent-1**: Integration testing support (if needed)
- **Agent-4 (Captain)**: Status updates and validation

