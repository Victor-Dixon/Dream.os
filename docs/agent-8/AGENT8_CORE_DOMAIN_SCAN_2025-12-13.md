# Core Domain Code Quality Scan Report

**Date**: 2025-12-13
**Agent**: Agent-8 (SSOT & System Integration Specialist)
**Task**: Core Domain Scanning - Code Quality Analysis

---

## Summary

- **Total Files Scanned**: 10
- **HIGH Priority Issues**: 10
- **MEDIUM Priority Issues**: 0
- **LOW Priority Issues**: 0
- **Missing SSOT Tags**: 4

---

## Detailed Results

| File | Lines | Functions | Classes | SSOT | Issues | Priority |
|------|-------|-----------|---------|------|--------|----------|
| `src\core\hardened_activity_detector.py` | 810 | 0 | 0 | ❌ | 2 | 🔴 HIGH |
| `src\core\agent_self_healing_system.py` | 752 | 0 | 0 | ❌ | 2 | 🔴 HIGH |
| `src\core\auto_gas_pipeline_system.py` | 688 | 0 | 0 | ❌ | 2 | 🔴 HIGH |
| `src\core\stress_test_metrics.py` | 524 | 0 | 0 | ❌ | 2 | 🔴 HIGH |
| `src\core\messaging_template_texts.py` | 886 | 0 | 0 | ✅ | 1 | 🔴 HIGH |
| `src\core\messaging_pyautogui.py` | 792 | 0 | 0 | ✅ | 1 | 🔴 HIGH |
| `src\core\message_queue_processor.py` | 766 | 0 | 0 | ✅ | 1 | 🔴 HIGH |
| `src\core\debate_to_gas_integration.py` | 620 | 0 | 0 | ✅ | 1 | 🔴 HIGH |
| `src\core\message_queue.py` | 618 | 0 | 0 | ✅ | 1 | 🔴 HIGH |
| `src\core\messaging_core.py` | 527 | 0 | 0 | ✅ | 1 | 🔴 HIGH |

---

## Files by Priority

### HIGH Priority (10 files)

- **`src\core\hardened_activity_detector.py`** (810 lines)
  - V2 violation: 810 lines (limit: 300)
  - Missing SSOT tag

- **`src\core\agent_self_healing_system.py`** (752 lines)
  - V2 violation: 752 lines (limit: 300)
  - Missing SSOT tag

- **`src\core\auto_gas_pipeline_system.py`** (688 lines)
  - V2 violation: 688 lines (limit: 300)
  - Missing SSOT tag

- **`src\core\stress_test_metrics.py`** (524 lines)
  - V2 violation: 524 lines (limit: 300)
  - Missing SSOT tag

- **`src\core\messaging_template_texts.py`** (886 lines)
  - V2 violation: 886 lines (limit: 300)

- **`src\core\messaging_pyautogui.py`** (792 lines)
  - V2 violation: 792 lines (limit: 300)

- **`src\core\message_queue_processor.py`** (766 lines)
  - V2 violation: 766 lines (limit: 300)

- **`src\core\debate_to_gas_integration.py`** (620 lines)
  - V2 violation: 620 lines (limit: 300)

- **`src\core\message_queue.py`** (618 lines)
  - V2 violation: 618 lines (limit: 300)

- **`src\core\messaging_core.py`** (527 lines)
  - V2 violation: 527 lines (limit: 300)

---

## Recommendations

### V2 Compliance Issues

- `src\core\hardened_activity_detector.py` - 810 lines (exceeds 300 line limit)
- `src\core\agent_self_healing_system.py` - 752 lines (exceeds 300 line limit)
- `src\core\auto_gas_pipeline_system.py` - 688 lines (exceeds 300 line limit)
- `src\core\stress_test_metrics.py` - 524 lines (exceeds 300 line limit)
- `src\core\messaging_template_texts.py` - 886 lines (exceeds 300 line limit)
- `src\core\messaging_pyautogui.py` - 792 lines (exceeds 300 line limit)
- `src\core\message_queue_processor.py` - 766 lines (exceeds 300 line limit)
- `src\core\debate_to_gas_integration.py` - 620 lines (exceeds 300 line limit)
- `src\core\message_queue.py` - 618 lines (exceeds 300 line limit)
- `src\core\messaging_core.py` - 527 lines (exceeds 300 line limit)

### Missing SSOT Tags

- `src\core\hardened_activity_detector.py`
- `src\core\agent_self_healing_system.py`
- `src\core\auto_gas_pipeline_system.py`
- `src\core\stress_test_metrics.py`

**Status**: Scan complete, ready for prioritization and remediation

🐝 **WE. ARE. SWARM. ⚡🔥**