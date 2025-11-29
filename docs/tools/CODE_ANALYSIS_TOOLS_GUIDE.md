# Code Analysis Tools Guide

**Last Updated**: 2025-11-27  
**Status**: ✅ **PRODUCTION READY**

---

## 🎯 **OVERVIEW**

Two complementary tools for identifying unused or unneeded functionality:

1. **`analyze_unneeded_functionality.py`** (Agent-2) - Finds code WITHOUT test coverage
2. **`test_usage_analyzer.py`** (Agent-3) - Finds code WITH test coverage but NOT used in production

**Key Insight**: Use both tools together for comprehensive dead code detection.

---

## 🔍 **TOOL 1: analyze_unneeded_functionality.py**

**Author**: Agent-2 (Architecture & Design Specialist)  
**Purpose**: Identifies code without test coverage (potentially unused)

### **Usage**:
```bash
python tools/analyze_unneeded_functionality.py src/core
```

### **What It Finds**:
- Functions/methods with 0% test coverage
- Classes without test coverage
- Files completely without tests
- Unused imports (future enhancement)

### **Output**:
- Console: Summary of files without tests
- JSON: Detailed analysis of untested code

### **When to Use**:
- **Before creating tests**: Identify what needs test coverage
- **Code cleanup**: Find potentially dead code that's untested
- **Coverage analysis**: Understand test coverage gaps

---

## 🔍 **TOOL 2: test_usage_analyzer.py**

**Author**: Agent-3 (Infrastructure & DevOps Specialist)  
**Purpose**: Identifies code that IS tested but NOT used in production

### **Usage**:
```bash
python tools/test_usage_analyzer.py src/core/orchestration
```

### **What It Finds**:
- Methods/functions tested but never called in production
- Test-only functionality (dead code that's tested)
- Over-tested unused code

### **Output**:
- Console: Summary of modules with unused candidates
- JSON: Detailed analysis saved to `agent_workspaces/Agent-3/unused_functionality_analysis.json`

### **When to Use**:
- **After creating tests**: Find what's tested but unused
- **Code cleanup**: Remove dead code that's being tested
- **Test optimization**: Remove tests for unused functionality

---

## 🔄 **COMBINED WORKFLOW**

### **Step 1: Find Untested Code** (Tool 1)
```bash
python tools/analyze_unneeded_functionality.py src/core
```
**Result**: List of code without tests

### **Step 2: Create Tests**
Create comprehensive tests for identified code

### **Step 3: Find Unused Tested Code** (Tool 2)
```bash
python tools/test_usage_analyzer.py src/core
```
**Result**: List of code that's tested but unused

### **Step 4: Verify & Remove**
1. Verify Protocol requirements (some methods required by interface)
2. Search codebase for actual usage
3. Remove confirmed unused code
4. Remove corresponding tests

---

## 📊 **COMPARISON**

| Feature | analyze_unneeded_functionality | test_usage_analyzer |
|---------|------------------------------|---------------------|
| **Focus** | Code WITHOUT tests | Code WITH tests but NOT used |
| **Use Case** | Before test creation | After test creation |
| **Method** | Coverage analysis | Production usage search |
| **Output** | Untested code list | Unused tested code list |
| **Complementary** | ✅ Yes - Use together | ✅ Yes - Use together |

---

## ✅ **VERIFICATION PROCESS**

Before removing any code identified by either tool:

1. **Check Protocol Requirements**: Some methods required by Protocol interfaces
2. **Search Codebase**: Use `grep` or codebase search for actual usage
3. **Check Imports**: Verify no dynamic imports or string-based calls
4. **Review Tests**: Ensure tests aren't the only usage
5. **Document Decision**: Record why code is kept or removed

---

## 🚀 **BEST PRACTICES**

1. **Use Both Tools**: They complement each other
2. **Verify Before Removing**: Always check Protocol requirements
3. **Document Findings**: Track cleanup progress
4. **Update Tests**: Remove tests for removed code
5. **Maintain Coverage**: Keep test coverage high after cleanup

---

## 📝 **EXAMPLES**

### **Example 1: Finding Untested Code**
```bash
# Find code without tests
python tools/analyze_unneeded_functionality.py src/core/orchestration

# Output: Lists functions/classes without test coverage
```

### **Example 2: Finding Unused Tested Code**
```bash
# Find code that's tested but unused
python tools/test_usage_analyzer.py src/core/orchestration

# Output: Lists methods tested but not used in production
```

### **Example 3: Complete Cleanup Workflow**
```bash
# Step 1: Find untested code
python tools/analyze_unneeded_functionality.py src/core

# Step 2: Create tests (manual)

# Step 3: Find unused tested code
python tools/test_usage_analyzer.py src/core

# Step 4: Verify and remove (manual)
```

---

## 🐝 **WE. ARE. SWARM.**

**Status**: ✅ Both tools production ready and complementary.

**Key Principle**: Use both tools together for comprehensive dead code detection and cleanup.

