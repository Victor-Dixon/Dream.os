# Tool Selection Decision Tree - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **DECISION TREE READY**  
**For**: Swarm-wide tool selection guidance

---

## 🎯 **TOOL SELECTION DECISION TREE**

### **Scenario: Starting Integration Work**

```
START
  │
  ├─> Need to clean repository?
  │   │
  │   ├─> YES → Use detect_venv_files.py
  │   │   │
  │   │   └─> Venv files found?
  │   │       │
  │   │       ├─> YES → Remove venv files, update .gitignore
  │   │       │
  │   │       └─> NO → Continue
  │   │
  │   └─> NO → Continue
  │
  ├─> Need to find duplicates?
  │   │
  │   ├─> YES → Use enhanced_duplicate_detector.py
  │   │   │
  │   │   ├─> Content-based duplicates? → Use exact duplicate detection
  │   │   │
  │   │   └─> Name-based duplicates? → Use name duplicate detection
  │   │
  │   └─> NO → Continue
  │
  ├─> Need to check integration issues?
  │   │
  │   ├─> YES → Use check_integration_issues.py
  │   │
  │   └─> NO → Continue
  │
  ├─> Need to extract patterns?
  │   │
  │   ├─> YES → Use analyze_merged_repo_patterns.py
  │   │
  │   └─> NO → Continue
  │
  └─> Ready for service integration
```

---

## 🛠️ **TOOL SELECTION BY TASK**

### **Task: Clean Virtual Environment Files**
**Tool**: `detect_venv_files.py` (Agent-5)  
**When**: Always first (Phase 0)  
**Output**: List of venv files, .gitignore suggestions

---

### **Task: Detect Duplicates**
**Tool**: `enhanced_duplicate_detector.py` (Agent-2)  
**When**: After venv cleanup (Phase 0)  
**Output**: Duplicate report, SSOT recommendations, resolution script

**Options**:
- Content-based detection (exact duplicates)
- Name-based detection (same name, different content)
- Both (recommended)

---

### **Task: Check Integration Issues**
**Tool**: `check_integration_issues.py` (Agent-3)  
**When**: After cleanup, before integration (Phase 0)  
**Output**: Integration issues, conflicts, dependency problems

---

### **Task: Extract Patterns**
**Tool**: `analyze_merged_repo_patterns.py` (Agent-2)  
**When**: Before service integration (Phase 1)  
**Output**: Extracted patterns, pattern categories, integration points

---

## 📊 **TOOL COMBINATION GUIDE**

### **Complete Integration Workflow**:
1. `detect_venv_files.py` → Clean venv
2. `enhanced_duplicate_detector.py` → Resolve duplicates
3. `check_integration_issues.py` → Check issues
4. `analyze_merged_repo_patterns.py` → Extract patterns

### **Quick Cleanup**:
1. `detect_venv_files.py` → Clean venv
2. `enhanced_duplicate_detector.py` → Resolve duplicates

### **Pattern Analysis Only**:
1. `analyze_merged_repo_patterns.py` → Extract patterns

---

## 🎯 **TOOL SELECTION BY PHASE**

### **Phase 0: Pre-Integration Cleanup**
- **Primary**: `detect_venv_files.py`, `enhanced_duplicate_detector.py`
- **Secondary**: `check_integration_issues.py`

### **Phase 1: Pattern Extraction**
- **Primary**: `analyze_merged_repo_patterns.py`

### **Phase 2: Service Integration**
- **Primary**: Templates and guides (no tools needed)
- **Reference**: Service Architecture Patterns

### **Phase 3: Testing & Validation**
- **Primary**: Test frameworks (pytest, etc.)
- **Reference**: Integration Templates

---

## ✅ **TOOL SELECTION CHECKLIST**

### **Before Starting**:
- [ ] Know which phase you're in
- [ ] Know what task you need to do
- [ ] Have tool available
- [ ] Understand tool output

### **Tool Usage**:
- [ ] Run tool with correct parameters
- [ ] Review tool output
- [ ] Act on tool recommendations
- [ ] Document tool results

---

**Status**: ✅ **DECISION TREE READY**  
**Last Updated**: 2025-11-26 15:00:00 (Local System Time)

