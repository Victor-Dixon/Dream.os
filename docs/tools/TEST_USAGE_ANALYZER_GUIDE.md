# Test Usage Analyzer - Tool Guide

**Created**: 2025-11-27  
**Author**: Agent-3 (Infrastructure & DevOps Specialist)  
**Status**: ✅ **PRODUCTION READY**

---

## 🎯 **PURPOSE**

Identifies unused functionality by analyzing test files to find methods/functions that are only tested but never used in production code.

**Key Insight**: Test coverage analysis reveals unused functionality - tests are not just validation, they're discovery tools.

---

## 🚀 **USAGE**

### **Basic Usage**:
```bash
# Analyze a directory
python tools/test_usage_analyzer.py src/core/orchestration

# Analyze entire core directory
python tools/test_usage_analyzer.py src/core

# Via toolbelt
python -m tools.agent_toolbelt --test-usage-analyzer src/core/orchestration
```

### **Output**:
- Console: Summary of modules with unused candidates
- JSON: Detailed analysis saved to `agent_workspaces/Agent-3/unused_functionality_analysis.json`

---

## 🔍 **HOW IT WORKS**

1. **Parse Source Files**: Extracts functions, classes, and methods
2. **Find Test Files**: Identifies test files for each module
3. **Extract Tested Methods**: Finds methods tested in test files
4. **Search Production Usage**: Checks if tested methods are used in production code
5. **Identify Unused**: Flags methods only in tests, not in production

---

## 📊 **OUTPUT FORMAT**

```json
[
  {
    "module": "src/core/orchestration/orchestrator_components.py",
    "functions": 5,
    "classes": 1,
    "test_files": ["tests/core/test_orchestration_orchestrator_components.py"],
    "unused_candidates": [
      {
        "type": "method",
        "name": "OrchestratorComponents.get_all_components",
        "class": "OrchestratorComponents",
        "method": "get_all_components",
        "file": "src/core/orchestration/orchestrator_components.py",
        "tested": true,
        "used_in_production": false
      }
    ]
  }
]
```

---

## ✅ **VERIFICATION PROCESS**

Before removing identified unused functionality:

1. **Check Protocol Requirements**: Verify if method is required by Protocol interface
2. **Search Codebase**: Confirm no production usage
3. **Check Tests**: Ensure method only used in tests
4. **Remove Safely**: Delete method and corresponding tests

---

## 🎯 **SUCCESS METRICS**

- **Accuracy**: Identifies truly unused methods (not Protocol requirements)
- **Safety**: Verifies Protocol compliance before removal
- **Efficiency**: Saves time identifying dead code manually

---

## 📝 **EXAMPLE: OrchestratorComponents.get_all_components()**

**Found**: Method only tested, never used in production  
**Verified**: Not required by Protocol interface  
**Action**: Removed method and test  
**Result**: LOC reduced, code quality improved

---

## 🐝 **WE. ARE. SWARM.**

**Tool Status**: ✅ Production ready, registered in toolbelt  
**Usage**: `python -m tools.agent_toolbelt --test-usage-analyzer <directory>`



