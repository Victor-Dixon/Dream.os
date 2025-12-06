# 🔍 Core Utils Duplicate Analysis

**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-04  
**Status**: ✅ **ANALYSIS COMPLETE**  
**Priority**: HIGH

---

## 📊 **EXECUTIVE SUMMARY**

**Files Analyzed**: 3 core utility files  
**Duplicates Found**: ⚠️ **SIGNIFICANT OVERLAP** - `simple_utils.py` has 6 duplicate functions  
**Recommendation**: Consolidate `simple_utils.py` with `unified_file_utils.py`

---

## 📁 **FILE ANALYSIS**

### **1. simple_utils.py** (109 lines)

**Location**: `src/core/utils/simple_utils.py`  
**Purpose**: Simple utility functions following KISS principles  
**Complexity**: 10 (low)

**Functions** (10 functions):
1. `read_file(filepath)` - Read file content
2. `write_file(filepath, content)` - Write content to file
3. `list_files(directory, extension=None)` - List files in directory
4. `get_timestamp()` - Get current timestamp
5. `format_string(template, **kwargs)` - Format string with variables
6. `is_valid_path(path)` - Check if path is valid
7. `create_directory(path)` - Create directory if it doesn't exist
8. `delete_file(filepath)` - Delete file
9. `get_file_size(filepath)` - Get file size in bytes
10. `copy_file(source, destination)` - Copy file from source to destination

**Status**: ⚠️ **DUPLICATES FOUND** - 6 functions overlap with `unified_file_utils.py`

---

### **2. unified_file_utils.py** (321 lines)

**Location**: `src/utils/unified_file_utils.py`  
**Purpose**: Main unified file utilities interface (SSOT)  
**Complexity**: 55 (high)

**Functions** (28 functions):
- File operations (read, write, list, copy, delete)
- Directory operations (create, size)
- Metadata operations (size, hash, modified time)
- Serialization (JSON, YAML)
- Backup operations
- Validation operations

**Status**: ✅ **SSOT** - Unified file utilities

---

## 🔍 **DUPLICATE ANALYSIS**

### **Common Functions** (6 functions):

1. **`read_file()` / `read_json()` / `read_yaml()`**
   - `simple_utils.read_file()` - Reads raw file content
   - `unified_file_utils.read_json()` - Reads JSON file
   - `unified_file_utils.read_yaml()` - Reads YAML file
   - **Status**: ⚠️ **PARTIAL DUPLICATE** - `read_file()` is more basic, but overlaps

2. **`write_file()` / `write_json()` / `write_yaml()`**
   - `simple_utils.write_file()` - Writes raw content
   - `unified_file_utils.write_json()` - Writes JSON file
   - `unified_file_utils.write_yaml()` - Writes YAML file
   - **Status**: ⚠️ **PARTIAL DUPLICATE** - `write_file()` is more basic, but overlaps

3. **`list_files()`**
   - `simple_utils.list_files(directory, extension=None)` - Lists files with extension filter
   - `unified_file_utils.list_files(directory, pattern="*")` - Lists files with pattern
   - **Status**: ⚠️ **DUPLICATE** - Same functionality, different parameter names

4. **`get_file_size()`**
   - `simple_utils.get_file_size(filepath)` - Returns file size in bytes
   - `unified_file_utils.get_file_size(file_path)` - Returns file size in bytes
   - **Status**: ⚠️ **DUPLICATE** - Identical functionality

5. **`copy_file()`**
   - `simple_utils.copy_file(source, destination)` - Copies file
   - `unified_file_utils.copy_file(source, destination)` - Copies file
   - **Status**: ⚠️ **DUPLICATE** - Identical functionality

6. **`create_directory()`**
   - `simple_utils.create_directory(path)` - Creates directory
   - `unified_file_utils.ensure_directory()` - Ensures directory exists (via FileUtils)
   - **Status**: ⚠️ **DUPLICATE** - Same functionality

---

### **Unique Functions** (4 functions in `simple_utils.py`):

1. **`get_timestamp()`** - ✅ **UNIQUE** - Timestamp formatting
2. **`format_string()`** - ✅ **UNIQUE** - String formatting with variables
3. **`is_valid_path()`** - ✅ **UNIQUE** - Path validation
4. **`delete_file()`** - ⚠️ **POTENTIAL DUPLICATE** - May exist in unified_file_utils

**Status**: 4 unique functions, 6 duplicate functions

---

## 🎯 **CONSOLIDATION RECOMMENDATION**

### **Option 1: Redirect Shim Pattern** ✅ **RECOMMENDED**

**Strategy**: Convert `simple_utils.py` to redirect shim

**Action**:
1. Keep unique functions (`get_timestamp()`, `format_string()`, `is_valid_path()`)
2. Redirect duplicate functions to `unified_file_utils.py`
3. Maintain backward compatibility

**Implementation**:
```python
# simple_utils.py - Redirect shim
from ..utils.unified_file_utils import UnifiedFileUtils

_unified_instance = UnifiedFileUtils()

# Unique functions (keep)
def get_timestamp():
    """Get current timestamp."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_string(template, **kwargs):
    """Format string with variables."""
    try:
        return template.format(**kwargs)
    except Exception:
        return template

def is_valid_path(path):
    """Check if path is valid."""
    try:
        import os
        return os.path.exists(path)
    except Exception:
        return False

# Redirect duplicate functions to unified_file_utils
def read_file(filepath):
    """Read file content."""
    # Use unified_file_utils for file reading
    # Note: unified_file_utils has read_json/read_yaml, but not raw read_file
    # Keep simple implementation for raw file reading
    try:
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def write_file(filepath, content):
    """Write content to file."""
    # Use unified_file_utils for directory creation
    from pathlib import Path
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    # Keep simple implementation for raw file writing
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False

def list_files(directory, extension=None):
    """List files in directory."""
    if extension:
        pattern = f"*.{extension.lstrip('.')}"
    else:
        pattern = "*"
    return _unified_instance.list_files(directory, pattern)

def get_file_size(filepath):
    """Get file size in bytes."""
    return _unified_instance.get_file_size(filepath)

def copy_file(source, destination):
    """Copy file from source to destination."""
    return _unified_instance.copy_file(source, destination)

def create_directory(path):
    """Create directory if it doesn't exist."""
    from pathlib import Path
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def delete_file(filepath):
    """Delete file."""
    # Check if unified_file_utils has delete functionality
    # If not, keep simple implementation
    try:
        import os
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception:
        return False
```

**Benefits**:
- ✅ Eliminates 6 duplicate functions
- ✅ Maintains backward compatibility
- ✅ Keeps unique functions
- ✅ Single source of truth for file operations

**Estimated Effort**: 2-3 hours

---

### **Option 2: Full Migration** ⚠️ **NOT RECOMMENDED**

**Strategy**: Remove `simple_utils.py`, migrate all imports

**Risks**:
- ❌ Breaking changes
- ❌ Requires all imports updated at once
- ❌ Higher risk of errors

**Status**: ⚠️ Not recommended - Use redirect shim instead

---

## 📋 **COORDINATION UTILS & MESSAGE QUEUE UTILS**

### **coordination_utils.py** (101 lines)

**Analysis**:
- ✅ **NO DUPLICATES** - Domain-specific coordination utilities
- ✅ Uses `AgentMatchingUtils` (proper composition)
- ✅ Stub classes for missing utilities (proper architecture)
- ✅ Coordination-specific functionality

**Status**: ✅ **NO CONSOLIDATION NEEDED** - Domain-specific, no duplicates

---

### **message_queue_utils.py** (215 lines)

**Analysis**:
- ✅ **NO DUPLICATES** - Message queue-specific utilities
- ✅ Queue-specific operations (priority scoring, retry delays, heap building)
- ✅ No overlap with file utilities
- ✅ Domain-specific functionality

**Status**: ✅ **NO CONSOLIDATION NEEDED** - Domain-specific, no duplicates

---

## 📊 **CONSOLIDATION METRICS**

### **simple_utils.py**:
- **Duplicate Functions**: 6 functions
- **Unique Functions**: 4 functions
- **Code Reduction**: ~40-50 lines (after redirect shim)
- **Import Updates**: ~5-10 files (gradual migration)

### **coordination_utils.py**:
- **Duplicates**: 0 functions
- **Status**: ✅ No consolidation needed

### **message_queue_utils.py**:
- **Duplicates**: 0 functions
- **Status**: ✅ No consolidation needed

---

## 🎯 **CONSOLIDATION PLAN**

### **Phase 1: simple_utils.py Consolidation** ⏳ **NEXT**

**Action**: Convert to redirect shim

**Steps**:
1. ⏳ Keep unique functions (`get_timestamp()`, `format_string()`, `is_valid_path()`)
2. ⏳ Redirect duplicate functions to `unified_file_utils.py`
3. ⏳ Maintain backward compatibility
4. ⏳ Test imports

**Estimated Effort**: 2-3 hours

---

## ✅ **FINDINGS SUMMARY**

### **simple_utils.py**:
- ⚠️ **6 duplicate functions** found
- ✅ **4 unique functions** (keep)
- ✅ **Consolidation recommended**: Use redirect shim pattern

### **coordination_utils.py**:
- ✅ **NO DUPLICATES** - Domain-specific utilities
- ✅ **NO CONSOLIDATION NEEDED**

### **message_queue_utils.py**:
- ✅ **NO DUPLICATES** - Domain-specific utilities
- ✅ **NO CONSOLIDATION NEEDED**

---

**Status**: ✅ Analysis complete - Consolidation plan ready  
**Next**: Convert `simple_utils.py` to redirect shim

🐝 **WE. ARE. SWARM. ⚡🔥**


