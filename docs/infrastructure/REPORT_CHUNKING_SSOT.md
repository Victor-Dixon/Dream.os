# 📊 Report Chunking SSOT

**Single Source of Truth**: `tools/chunk_reports.py`

**Status**: ✅ **ACTIVE**

---

## 🎯 **PURPOSE**

Chunks JSON reports into 15k character pieces for agent consumption. This is the **only** script that should be used for report chunking.

---

## 📁 **SSOT LOCATION**

```
tools/chunk_reports.py
```

---

## 🔧 **USAGE**

### **Command Line**:
```bash
python tools/chunk_reports.py <report_path>
```

### **Python Import**:
```python
from chunk_reports import chunk_json_report, analyze_report_chunkability, CHUNK_SIZE

# Chunk a report
chunks = chunk_json_report(Path("analysis/module_analysis.json"))

# Analyze chunkability
analysis = analyze_report_chunkability(Path("analysis/module_analysis.json"))
```

---

## 📋 **FEATURES**

- ✅ Chunks JSON reports into 15k character pieces
- ✅ Handles both dicts and lists
- ✅ Safety buffer to ensure chunks stay under limit
- ✅ Chunkability analysis
- ✅ CLI interface
- ✅ Error handling for oversized items

---

## 🚫 **DEPRECATED / RETIRED**

### **Retired Scripts**:
- ❌ `tools/projectscanner_modular_reports.py::chunk_report()` - **DEPRECATED**
  - Now delegates to `chunk_reports.py` for backward compatibility
  - Use `chunk_json_report()` from `chunk_reports.py` instead

### **Different Purpose** (Not Report Chunking):
- `tools/analysis/project_analyzer_reports.py::generate_chunk_reports()` - File-based chunking (different purpose)
- `tools/comprehensive_project_analyzer_BACKUP_PRE_REFACTOR.py` - Backup file

---

## 🔄 **MIGRATION**

If you're using the old `ModularReportGenerator.chunk_report()` method:

**Before**:
```python
from projectscanner_modular_reports import ModularReportGenerator
chunks = ModularReportGenerator.chunk_report(report_path)
```

**After**:
```python
from chunk_reports import chunk_json_report
chunks = chunk_json_report(report_path)
```

---

## ✅ **VERIFICATION**

Run the chunking utility to verify it works:
```bash
python tools/chunk_reports.py analysis/module_analysis.json
```

---

## 🐝 **WE. ARE. SWARM.**

**SSOT**: `tools/chunk_reports.py`  
**Status**: ✅ **ACTIVE**  
**Deprecated**: `projectscanner_modular_reports.py::chunk_report()`

---

*This document establishes `tools/chunk_reports.py` as the SSOT for report chunking.*

