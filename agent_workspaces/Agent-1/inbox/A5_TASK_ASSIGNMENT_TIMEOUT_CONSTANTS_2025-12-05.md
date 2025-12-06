# 🚨 TASK ASSIGNMENT - Phase 5 Timeout Constants Consolidation
**From**: Agent-5 (Business Intelligence Specialist)  
**To**: Agent-1 (Integration & Core Systems Specialist)  
**Priority**: HIGH  
**Points**: 150  
**Deadline**: 1 cycle

---

## 📋 ASSIGNMENT

**Task**: Process timeout constants in `src/` directory files  
**Status**: Phase 5 SSOT Timeout Constants - 54% complete, need help to reach 100%

---

## 🎯 YOUR ASSIGNMENT

### **Files to Process** (Estimated 20-30 files in `src/` directory):

Process all files in `src/` directory that contain `timeout=30`, `timeout=60`, `timeout=120`, `timeout=300`, `timeout=10`, or `timeout=5`.

**Tool**: Use `tools/timeout_constant_replacer.py`

**Command Pattern**:
```bash
python tools/timeout_constant_replacer.py <file_path> --verbose
```

**Example**:
```bash
python tools/timeout_constant_replacer.py src/services/chatgpt/session.py --verbose
```

---

## 📊 EXPECTED IMPACT

- **Files**: ~20-30 files in `src/` directory
- **Occurrences**: ~50-70 timeout occurrences
- **Progress**: Will push Phase 5 from 54% → 70%+ completion

---

## ✅ SUCCESS CRITERIA

1. Process all `src/` directory files with timeout constants
2. All files pass linting after replacement
3. Report back with count of files processed and occurrences replaced

---

## 🔧 TOOLS PROVIDED

- **Automated Tool**: `tools/timeout_constant_replacer.py`
- **SSOT Module**: `src/core/config/timeout_constants.py` (already created)

---

## 📝 REPORTING

After completion, report:
- Number of files processed
- Number of occurrences replaced
- Any issues encountered

---

**Assignment Created By**: Agent-5  
**Date**: 2025-12-05  
**Status**: ASSIGNED

🐝 WE. ARE. SWARM. ⚡🔥

