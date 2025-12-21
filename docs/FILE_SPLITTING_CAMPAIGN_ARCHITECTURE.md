# File Splitting Campaign Architecture Plan

**Date**: 2025-12-17  
**Author**: Agent-2 (Architecture & Design Specialist)  
**Coordinated With**: Agent-4  
**Status**: Architecture Design Phase

---

## 🎯 Objective

Split top 10 large files (>500 lines) that violate V2 compliance (file size >300 lines) into smaller, focused modules to improve:
- **V2 Compliance**: Reduce file size violations
- **Code Maintainability**: Improve readability and organization
- **Optimization**: Enable better code reuse and testing

---

## 📋 Target Files (Top 10)

| Rank | File | Lines | Over Limit | Priority |
|------|------|-------|------------|----------|
| 1 | `src/orchestrators/overnight/enhanced_agent_activity_detector.py` | 1,367 | +1,067 | **P0** |
| 2 | `src/discord_commander/github_book_viewer.py` | 1,164 | +864 | **P0** |
| 3 | `src/core/messaging_template_texts.py` | 966 | +666 | **P0** |
| 4 | `src/services/hard_onboarding_service.py` | 880 | +580 | **P1** |
| 5 | `src/discord_commander/views/main_control_panel_view.py` | 877 | +577 | **P1** |
| 6 | `src/discord_commander/status_change_monitor.py` | 826 | +526 | **P1** |
| 7 | `src/discord_commander/templates/broadcast_templates.py` | 819 | +519 | **P1** |
| 8 | `src/core/messaging_pyautogui.py` | 801 | +501 | **P1** |
| 9 | `src/core/message_queue_processor.py` | 773 | +473 | **P1** |
| 10 | `src/core/auto_gas_pipeline_system.py` | 687 | +387 | **P2** |

**Total Lines to Split**: ~9,153 lines across 10 files  
**Target**: Split into ~30-50 modules (average ~200-300 lines per module)

---

## 🏗️ Architecture Principles

### **1. Single Responsibility Principle (SRP)**
- Each new module should have one clear purpose
- Group related functions/classes together
- Separate concerns (UI, business logic, data access)

### **2. Dependency Management**
- Maintain backward compatibility during split
- Use `__init__.py` to expose public APIs
- Keep imports clean and explicit

### **3. V2 Compliance Targets**
- **File Size**: <300 lines per file
- **Function Size**: <30 lines per function
- **Class Size**: <200 lines per class
- **SSOT Tags**: Add appropriate domain tags

### **4. Testing Strategy**
- Preserve existing test coverage
- Add module-level tests for new modules
- Integration tests for refactored components

---

## 📐 Splitting Strategy by File

### **1. enhanced_agent_activity_detector.py (1,367 lines → ~5 modules)**

**Current Structure**: Monolithic detector with multiple responsibilities

**Proposed Split**:
```
src/orchestrators/overnight/enhanced_agent_activity_detector/
├── __init__.py                    # Public API exports
├── detector_core.py              # Core detection logic (~250 lines)
├── activity_analyzer.py          # Activity analysis (~250 lines)
├── pattern_matcher.py            # Pattern matching logic (~250 lines)
├── state_manager.py              # State management (~250 lines)
└── detector_config.py            # Configuration and constants (~150 lines)
```

**Key Considerations**:
- Maintain backward compatibility via `__init__.py`
- Extract configuration to separate module
- Separate analysis logic from detection logic

---

### **2. github_book_viewer.py (1,164 lines → ~4 modules)**

**Current Structure**: Large viewer with UI, data fetching, and rendering

**Proposed Split**:
```
src/discord_commander/github_book_viewer/
├── __init__.py                    # Public API exports
├── viewer_core.py                # Core viewer logic (~300 lines)
├── github_client.py              # GitHub API interactions (~300 lines)
├── book_parser.py                # Book content parsing (~300 lines)
└── viewer_ui.py                  # UI components (~250 lines)
```

**Key Considerations**:
- Separate GitHub API calls from UI rendering
- Extract parsing logic for reusability
- Maintain Discord embed generation in UI module

---

### **3. messaging_template_texts.py (966 lines → ~3-4 modules)**

**Current Structure**: Large template collection

**Proposed Split**:
```
src/core/messaging_template_texts/
├── __init__.py                    # Public API exports
├── template_core.py              # Core template functions (~300 lines)
├── agent_templates.py            # Agent-specific templates (~250 lines)
├── system_templates.py           # System message templates (~250 lines)
└── template_utils.py             # Template utilities (~150 lines)
```

**Key Considerations**:
- Group templates by domain (agent, system, etc.)
- Extract common template utilities
- Maintain template registry pattern

---

### **4. hard_onboarding_service.py (880 lines → ~3 modules)**

**Current Structure**: Large onboarding service with multiple phases

**Proposed Split**:
```
src/services/hard_onboarding_service/
├── __init__.py                    # Public API exports
├── onboarding_core.py           # Core onboarding logic (~300 lines)
├── onboarding_phases.py         # Phase implementations (~300 lines)
└── onboarding_validators.py      # Validation logic (~250 lines)
```

**Key Considerations**:
- Separate phase logic from core service
- Extract validation into dedicated module
- Maintain service interface

---

### **5. main_control_panel_view.py (877 lines → ~3-4 modules)**

**Current Structure**: Large view with multiple UI components

**Proposed Split**:
```
src/discord_commander/views/main_control_panel/
├── __init__.py                    # Public API exports
├── view_core.py                  # Core view logic (~250 lines)
├── panel_components.py           # UI components (~250 lines)
├── panel_handlers.py             # Event handlers (~250 lines)
└── panel_utils.py                # View utilities (~100 lines)
```

**Key Considerations**:
- Separate UI components from event handling
- Extract reusable view utilities
- Maintain view interface

---

### **6. status_change_monitor.py (826 lines → ~3 modules)**

**Current Structure**: Monitor with detection and notification logic

**Proposed Split**:
```
src/discord_commander/status_change_monitor/
├── __init__.py                    # Public API exports
├── monitor_core.py                # Core monitoring logic (~300 lines)
├── change_detector.py            # Change detection (~300 lines)
└── notification_handler.py      # Notification logic (~200 lines)
```

**Key Considerations**:
- Separate detection from notification
- Extract change detection algorithms
- Maintain monitor interface

---

### **7. broadcast_templates.py (819 lines → ~3 modules)**

**Current Structure**: Large template collection for broadcasts

**Proposed Split**:
```
src/discord_commander/templates/broadcast_templates/
├── __init__.py                    # Public API exports
├── template_core.py              # Core template functions (~300 lines)
├── broadcast_types.py            # Type-specific templates (~300 lines)
└── template_helpers.py           # Template helpers (~200 lines)
```

**Key Considerations**:
- Group templates by broadcast type
- Extract common template helpers
- Maintain template registry

---

### **8. messaging_pyautogui.py (801 lines → ~3 modules)**

**Current Structure**: Large PyAutoGUI operation collection

**Proposed Split**:
```
src/core/messaging_pyautogui/
├── __init__.py                    # Public API exports
├── pyautogui_core.py             # Core operations (~300 lines)
├── operation_sequences.py        # Operation sequences (~300 lines)
└── operation_utils.py            # Operation utilities (~200 lines)
```

**Key Considerations**:
- Separate core operations from sequences
- Extract reusable operation utilities
- Maintain operation interface

---

### **9. message_queue_processor.py (773 lines → ~3 modules)**

**Current Structure**: Large processor with queue management and processing

**Proposed Split**:
```
src/core/message_queue_processor/
├── __init__.py                    # Public API exports
├── processor_core.py             # Core processing logic (~300 lines)
├── queue_manager.py              # Queue management (~250 lines)
└── processor_handlers.py        # Message handlers (~200 lines)
```

**Key Considerations**:
- Separate queue management from processing
- Extract message handlers
- Maintain processor interface

---

### **10. auto_gas_pipeline_system.py (687 lines → ~3 modules)**

**Current Structure**: Large pipeline with multiple stages

**Proposed Split**:
```
src/core/auto_gas_pipeline_system/
├── __init__.py                    # Public API exports
├── pipeline_core.py              # Core pipeline logic (~250 lines)
├── pipeline_stages.py            # Stage implementations (~250 lines)
└── pipeline_utils.py            # Pipeline utilities (~150 lines)
```

**Key Considerations**:
- Separate stage logic from core pipeline
- Extract pipeline utilities
- Maintain pipeline interface

---

## 🔄 Implementation Phases

### **Phase 1: Architecture Design (Current)**
- ✅ Identify target files
- ✅ Design splitting strategy
- ✅ Create architecture plan
- ⏳ Review and approval

### **Phase 2: Preparation (Week 1)**
- Create new module directories
- Set up `__init__.py` files with backward compatibility
- Document public APIs
- Create migration plan

### **Phase 3: Splitting (Week 2-3)**
- Split files one at a time (P0 → P1 → P2)
- Maintain backward compatibility
- Update imports incrementally
- Run tests after each split

### **Phase 4: Cleanup (Week 4)**
- Remove deprecated code
- Update documentation
- Verify V2 compliance
- Final testing

---

## ✅ Success Criteria

1. **V2 Compliance**: All split files <300 lines
2. **Backward Compatibility**: Existing code continues to work
3. **Test Coverage**: Maintain or improve test coverage
4. **Code Quality**: Improved readability and maintainability
5. **Documentation**: All new modules documented

---

## 🚨 Risk Mitigation

1. **Breaking Changes**: Use `__init__.py` to maintain imports
2. **Test Failures**: Run tests after each split
3. **Import Cycles**: Careful dependency management
4. **Performance**: Monitor for performance regressions

---

## 📝 Next Steps

1. **Review Architecture Plan**: Get approval from Agent-4
2. **Create Module Structure**: Set up directories and `__init__.py` files
3. **Begin Splitting**: Start with P0 files (enhanced_agent_activity_detector.py)
4. **Coordinate Execution**: Work with Agent-4 for implementation

---

🐝 **WE. ARE. SWARM. ⚡🔥**




