# ⏰ Swarm Time System Usage Guide
**Date**: 2025-01-27  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **MANDATORY REFERENCE**  
**Purpose**: Ensure accurate timestamps across all swarm operations

---

## 🚨 **CRITICAL PROBLEM**

**Issue**: File metadata shows incorrect creation dates (files appear created later than they actually were). This breaks chronological history in:
- Agent devlogs
- Documentation files
- Status updates
- Progress tracking

**Impact**: 
- ❌ Incorrect chronological ordering
- ❌ Swarm synchronization issues
- ❌ Historical inaccuracy
- ❌ Debugging difficulties

---

## ✅ **SOLUTION: Use Swarm Time System**

**Location**: `src/utils/swarm_time.py`

**All agents MUST use this system for all timestamps.**

---

## 📋 **AVAILABLE FUNCTIONS**

### **1. `get_swarm_time()` → datetime**
Get current local time as datetime object.

```python
from src.utils.swarm_time import get_swarm_time

current_time = get_swarm_time()
# Returns: datetime object with local system time
```

### **2. `format_swarm_timestamp_readable(dt=None)` → str**
Format datetime as human-readable timestamp.

```python
from src.utils.swarm_time import format_swarm_timestamp_readable

timestamp = format_swarm_timestamp_readable()
# Returns: "YYYY-MM-DD HH:MM:SS" (e.g., "2025-01-27 14:30:45")

# Or with specific datetime
timestamp = format_swarm_timestamp_readable(some_datetime)
```

### **3. `format_swarm_timestamp_filename(dt=None)` → str**
Format datetime for use in filenames.

```python
from src.utils.swarm_time import format_swarm_timestamp_filename

filename = format_swarm_timestamp_filename()
# Returns: "YYYYMMDD_HHMMSS_ffffff" (e.g., "20250127_143045_123456")
```

### **4. `format_swarm_timestamp(dt=None)` → str**
Format datetime as ISO 8601 timestamp.

```python
from src.utils.swarm_time import format_swarm_timestamp

iso_timestamp = format_swarm_timestamp()
# Returns: ISO 8601 formatted string
```

### **5. `get_swarm_time_display()` → str**
Get current time formatted for display in messages.

```python
from src.utils.swarm_time import get_swarm_time_display

display_time = get_swarm_time_display()
# Returns: Human-readable timestamp for messages
```

---

## 🎯 **USAGE EXAMPLES**

### **Example 1: Devlog Timestamps**

```python
from src.utils.swarm_time import format_swarm_timestamp_readable

timestamp = format_swarm_timestamp_readable()

devlog_content = f"""
# Devlog Title

**Date**: {timestamp}  
**Agent**: Agent-X  
**Status**: ✅ COMPLETE

Content here...
"""
```

### **Example 2: Status.json Updates**

```python
from src.utils.swarm_time import format_swarm_timestamp_readable
import json

status = {
    "agent_id": "Agent-X",
    "agent_name": "Role Name",
    "status": "ACTIVE_AGENT_MODE",
    "last_updated": format_swarm_timestamp_readable(),  # ✅ CORRECT
    "current_mission": "Mission description"
}

with open("agent_workspaces/Agent-X/status.json", "w") as f:
    json.dump(status, f, indent=2)
```

### **Example 3: Documentation Dates**

```python
from src.utils.swarm_time import format_swarm_timestamp_readable

doc_content = f"""
# Document Title

**Last Updated**: {format_swarm_timestamp_readable()}  
**Author**: Agent-X  
**Status**: ✅ ACTIVE

Document content...
"""
```

### **Example 4: File Creation with Timestamps**

```python
from src.utils.swarm_time import format_swarm_timestamp_filename
from pathlib import Path

timestamp = format_swarm_timestamp_filename()
filename = f"report_{timestamp}.md"

Path(filename).write_text("Report content...")
```

### **Example 5: Message Timestamps**

```python
from src.utils.swarm_time import get_swarm_time_display

message = f"""
[A2A] Message Title

**Timestamp**: {get_swarm_time_display()}  
**From**: Agent-X  
**To**: Agent-Y

Message content...
"""
```

---

## 📊 **WHEN TO USE SWARM TIME**

### **✅ ALWAYS Use For**:

1. **Devlog Timestamps**
   - Date headers in devlog files
   - Creation timestamps
   - Update timestamps

2. **Documentation Dates**
   - "Last Updated" fields
   - "Created" dates
   - Version timestamps

3. **Status.json Updates**
   - `last_updated` field
   - Task completion timestamps
   - Progress update timestamps

4. **File Creation**
   - Filename timestamps
   - File metadata timestamps
   - Archive timestamps

5. **Message Timestamps**
   - Inbox message headers
   - Coordination messages
   - Progress reports

6. **Progress Tracking**
   - Milestone timestamps
   - Task completion times
   - Cycle timestamps

---

## ❌ **DO NOT**

- ❌ Use `datetime.now()` directly (may not match system time)
- ❌ Use hardcoded timestamps
- ❌ Use file system metadata for timestamps
- ❌ Assume file creation time is accurate
- ❌ Use UTC time when local time is needed
- ❌ Skip timestamps in devlogs or documentation

---

## ✅ **DO**

- ✅ Always import and use `get_swarm_time()` or formatting functions
- ✅ Use `format_swarm_timestamp_readable()` for human-readable timestamps
- ✅ Use `format_swarm_timestamp_filename()` for filename timestamps
- ✅ Update timestamps when files are modified
- ✅ Include timestamps in all devlogs and documentation
- ✅ Use swarm time for all status.json updates
- ✅ Verify timestamps are accurate before committing

---

## 🔧 **COMMAND LINE USAGE**

### **Get Current Time**:
```bash
python -c "from src.utils.swarm_time import format_swarm_timestamp_readable; print(format_swarm_timestamp_readable())"
```

### **Get Filename Timestamp**:
```bash
python -c "from src.utils.swarm_time import format_swarm_timestamp_filename; print(format_swarm_timestamp_filename())"
```

---

## 📊 **BENEFITS**

### **True Chronological History**:
- ✅ Accurate timestamps create correct chronological order
- ✅ Devlogs reflect true work timeline
- ✅ Documentation shows accurate update history

### **Swarm Synchronization**:
- ✅ All agents use same time source
- ✅ Consistent timestamps across swarm
- ✅ Swarm stays in sync

### **Metadata Accuracy**:
- ✅ File creation dates match actual work time
- ✅ No more "created later than actual" issues
- ✅ Accurate historical records

### **Debugging**:
- ✅ Accurate timestamps help identify when work happened
- ✅ Easier to trace issues chronologically
- ✅ Better historical analysis

---

## 🎯 **QUICK REFERENCE**

```python
# Import
from src.utils.swarm_time import (
    get_swarm_time,
    format_swarm_timestamp_readable,
    format_swarm_timestamp_filename,
    format_swarm_timestamp,
    get_swarm_time_display
)

# Most common use cases:
timestamp = format_swarm_timestamp_readable()  # For devlogs, docs, status.json
filename_ts = format_swarm_timestamp_filename()  # For filenames
display_ts = get_swarm_time_display()  # For messages
```

---

## 🚨 **MANDATORY CHECKLIST**

Before creating any file with timestamps:

- [ ] Imported `swarm_time` functions
- [ ] Used `format_swarm_timestamp_readable()` for dates
- [ ] Used `format_swarm_timestamp_filename()` for filenames
- [ ] Updated `status.json` with accurate timestamp
- [ ] Included timestamp in devlog header
- [ ] Verified timestamp accuracy

---

**Status**: ✅ **MANDATORY REFERENCE**  
**Last Updated**: 2025-01-27  
**All Agents**: Must use swarm time system for all timestamps

