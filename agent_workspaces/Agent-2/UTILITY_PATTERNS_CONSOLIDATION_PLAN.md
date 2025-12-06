# 🔧 Utility Patterns Consolidation Plan

**Agent**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-04  
**Status**: ✅ **CONSOLIDATION PLAN READY**  
**Priority**: HIGH

---

## 📊 **EXECUTIVE SUMMARY**

**Focus**: Utility pattern consolidation from 140 groups analysis  
**File Utilities**: 14 duplicate functions identified  
**Config Utilities**: 1 duplicate class (FileScanner)  
**Core Utils**: 3 files to analyze (coordination_utils, message_queue_utils, simple_utils)

**Status**: Consolidation plan ready for execution

---

## 📁 **FILE UTILITIES CONSOLIDATION**

### **Current State**:

**unified_file_utils.py** (SSOT):
- Modular architecture (uses `file_operations/` submodules)
- 28 functions
- V2 compliant

**file_utils.py** (Duplicate):
- Monolithic architecture
- 20 functions
- 14 common functions with `unified_file_utils.py`

### **Consolidation Strategy**:

**Phase 1**: Convert `file_utils.py` to redirect shim

**Action**: Create backward-compatible wrapper

**Implementation**:
```python
# file_utils.py - Redirect shim
"""
File Utils - V2 Compliance Redirect
===================================

Redirects to unified_file_utils.py for backward compatibility.
Maintains FileUtils static methods interface.
"""

from typing import Any
from .unified_file_utils import (
    UnifiedFileUtils,
    BackupOperations,
    BackupManager,
    FileValidator,
    UnifiedFileScanner,
    create_backup_manager,
    FileValidationResult,
)

# Create singleton instance
_unified_instance = UnifiedFileUtils()

class FileUtils:
    """Backward compatibility wrapper for UnifiedFileUtils."""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists."""
        from pathlib import Path
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists."""
        return _unified_instance.file_exists(file_path)
    
    @staticmethod
    def read_json(file_path: str) -> dict[str, Any] | None:
        """Read JSON file."""
        return _unified_instance.read_json(file_path)
    
    @staticmethod
    def write_json(file_path: str, data: dict[str, Any]) -> bool:
        """Write JSON file."""
        return _unified_instance.write_json(file_path, data)
    
    @staticmethod
    def read_yaml(file_path: str) -> dict[str, Any] | None:
        """Read YAML file."""
        return _unified_instance.read_yaml(file_path)
    
    @staticmethod
    def write_yaml(file_path: str, data: dict[str, Any]) -> bool:
        """Write YAML file."""
        return _unified_instance.write_yaml(file_path, data)
    
    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if file is readable."""
        from .unified_file_utils import FileMetadataOperations
        return FileMetadataOperations.is_file_readable(file_path)
    
    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if file is writable."""
        from .unified_file_utils import FileMetadataOperations
        return FileMetadataOperations.is_file_writable(file_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int | None:
        """Get file size."""
        return _unified_instance.get_file_size(file_path)
    
    @staticmethod
    def get_file_modified_time(file_path: str) -> datetime | None:
        """Get file modified time."""
        from .unified_file_utils import FileMetadataOperations
        return FileMetadataOperations.get_file_modified_time(file_path)
    
    @staticmethod
    def get_file_hash(file_path: str) -> str | None:
        """Get file hash."""
        return _unified_instance.get_file_hash(file_path)
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension."""
        from .unified_file_utils import FileMetadataOperations
        return FileMetadataOperations.get_file_extension(file_path)
    
    @staticmethod
    def is_json_file(file_path: str) -> bool:
        """Check if file is JSON."""
        from .unified_file_utils import FileMetadataOperations
        return FileMetadataOperations.is_json_file(file_path)
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> list[str]:
        """List files in directory."""
        return _unified_instance.list_files(directory, pattern)
    
    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """Get directory size."""
        return _unified_instance.get_directory_size(directory_path)
    
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file."""
        return _unified_instance.copy_file(source, destination)
    
    @staticmethod
    def create_backup(file_path: str, backup_suffix: str = ".backup") -> str | None:
        """Create file backup."""
        return _unified_instance.create_backup(file_path)
    
    @staticmethod
    def restore_from_backup(backup_path: str, target_path: str) -> bool:
        """Restore from backup."""
        from .unified_file_utils import BackupOperations
        return BackupOperations.restore_from_backup(backup_path, target_path)
    
    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """Safely delete file."""
        from .unified_file_utils import BackupOperations
        return BackupOperations.safe_delete_file(file_path)
    
    @staticmethod
    def validate_file_path(file_path: str) -> dict[str, Any]:
        """Validate file path."""
        result = _unified_instance.validate_file(file_path)
        # Convert FileValidationResult to dict for backward compatibility
        return {
            "path": result.path,
            "exists": result.exists,
            "is_file": result.is_file,
            "is_directory": result.is_directory,
            "readable": result.readable,
            "writable": result.writable,
            "size_bytes": result.size_bytes,
            "modified_time": result.modified_time.isoformat() if result.modified_time else None,
            "errors": result.errors,
        }

# Backward compatibility exports
__all__ = ["FileUtils"]
```

**Estimated Effort**: 2-3 hours

---

## ⚙️ **CONFIG UTILITIES CONSOLIDATION**

### **Current State**:

**unified_config_utils.py**:
- Contains `FileScanner` class (lines 207-258)
- Contains `UnifiedConfigurationConsolidator`

**config_file_scanner.py**:
- Contains `FileScanner` class (extracted module)
- Uses `ConfigurationScanner` from `config_scanners.py`

**config_consolidator.py**:
- Uses `FileScanner` from `file_scanner.py` (correct)

### **Consolidation Strategy**:

**Phase 1**: Remove duplicate `FileScanner` from `unified_config_utils.py`

**Action**: Import `FileScanner` from `config_file_scanner.py`

**Implementation**:
```python
# unified_config_utils.py
# Remove FileScanner class (lines 207-258)
# Add import:
from .config_file_scanner import FileScanner

# Update UnifiedConfigurationConsolidator to use imported FileScanner
# (no changes needed - already uses FileScanner)
```

**Estimated Effort**: 1-2 hours

---

## 🔧 **CORE UTILS ANALYSIS**

### **Files to Analyze**:

1. **coordination_utils.py** (34 complexity)
2. **message_queue_utils.py** (26 complexity)
3. **simple_utils.py** (10 complexity)

### **Analysis Plan**:

1. Extract function signatures
2. Compare with other utility files
3. Identify duplicate patterns
4. Consolidate if duplicates found

**Status**: ⏳ Analysis in progress

---

## 📋 **CONSOLIDATION EXECUTION PLAN**

### **Phase 1: File Utilities** (HIGH PRIORITY)

1. ✅ **COMPLETE**: Analysis of duplicates
2. ⏳ **NEXT**: Create redirect shim in `file_utils.py`
3. ⏳ **NEXT**: Test backward compatibility
4. ⏳ **NEXT**: Update imports gradually

**Estimated Time**: 2-3 hours

---

### **Phase 2: Config Utilities** (MEDIUM PRIORITY)

1. ✅ **COMPLETE**: Analysis of duplicates
2. ⏳ **NEXT**: Remove `FileScanner` from `unified_config_utils.py`
3. ⏳ **NEXT**: Import from `config_file_scanner.py`
4. ⏳ **NEXT**: Test configuration scanning

**Estimated Time**: 1-2 hours

---

### **Phase 3: Core Utils** (MEDIUM PRIORITY)

1. ⏳ **NEXT**: Analyze `coordination_utils.py`
2. ⏳ **NEXT**: Analyze `message_queue_utils.py`
3. ⏳ **NEXT**: Analyze `simple_utils.py`
4. ⏳ **NEXT**: Identify duplicate patterns
5. ⏳ **NEXT**: Consolidate if duplicates

**Estimated Time**: 3-4 hours

---

## 📊 **CONSOLIDATION METRICS**

### **File Utilities**:
- **Duplicate Functions**: 14 functions
- **Code Reduction**: ~200-250 lines (after redirect shim)
- **Import Updates**: ~20-30 files (gradual migration)

### **Config Utilities**:
- **Duplicate Classes**: 1 class (FileScanner)
- **Code Reduction**: ~50-100 lines
- **Import Updates**: ~5-10 files

### **Core Utils**:
- **Analysis**: 3 files
- **Duplicates**: TBD (analysis in progress)

---

## 🎯 **NEXT ACTIONS**

### **Immediate (This Cycle)**:
1. ⏳ Create redirect shim for `file_utils.py`
2. ⏳ Remove duplicate `FileScanner` from `unified_config_utils.py`
3. ⏳ Analyze core utils for duplicates

### **Short-Term (Next Cycle)**:
1. Update imports to use unified utilities
2. Test backward compatibility
3. Complete core utils consolidation

---

**Status**: ✅ Consolidation plan ready - Starting execution  
**Next**: Create redirect shim for file_utils.py

🐝 **WE. ARE. SWARM. ⚡🔥**


