# File Locking Fix Specification - Agent-7

**Date**: 2025-12-01  
**Agent**: Agent-7 (Web Development Specialist)  
**Status**: 🚨 **CRITICAL FIX REQUIRED**  
**Priority**: CRITICAL

---

## 🚨 **ISSUE**

**Error**: `[WinError 5] Access is denied: 'message_queue\\queue.json.tmp' -> 'message_queue\\queue.json'`

**Impact**: Broadcast messages partially failing (6/8 instead of 8/8)

**Root Cause**: Windows file locking - queue.json may be locked by queue processor during atomic rename operation.

---

## 🔧 **FIX REQUIREMENTS**

### **1. Add Retry Logic with Exponential Backoff** (CRITICAL)

**Location**: `src/core/message_queue_persistence.py` → `save_entries()` method

**Implementation**:
```python
def save_entries(self, entries: List[IQueueEntry]) -> None:
    """Save queue entries to JSON file with atomic write and retry logic."""
    import time
    import shutil
    from pathlib import Path
    
    data = [entry.to_dict() for entry in entries]
    temp_file = self.queue_file.with_suffix('.json.tmp')
    
    # Retry configuration
    max_retries = 5
    base_delay = 0.1  # 100ms
    max_delay = 2.0   # 2 seconds
    
    for attempt in range(max_retries):
        try:
            # Write to temp file
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, separators=(',', ':'), ensure_ascii=False, default=str)
            
            # Atomic move (Windows-compatible with retry)
            if self.queue_file.exists():
                try:
                    self.queue_file.unlink()
                except PermissionError:
                    # File may be locked, wait and retry
                    if attempt < max_retries - 1:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        time.sleep(delay)
                        continue
                    raise
            
            # Use shutil.move instead of rename (handles Windows locks better)
            shutil.move(str(temp_file), str(self.queue_file))
            return  # Success!
            
        except (PermissionError, OSError) as e:
            if "WinError 5" in str(e) or "Access is denied" in str(e):
                # File locked - retry with exponential backoff
                if attempt < max_retries - 1:
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    print(f"⚠️ File locked, retrying in {delay:.2f}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    continue
                else:
                    # Final attempt failed
                    print(f"❌ Failed to save queue entries after {max_retries} attempts: {e}")
                    raise
            else:
                # Other error - raise immediately
                raise
        except Exception as e:
            print(f"❌ Failed to save queue entries: {e}")
            raise
        finally:
            # Clean up temp file on error
            if temp_file.exists() and attempt == max_retries - 1:
                try:
                    temp_file.unlink()
                except Exception:
                    pass
```

---

### **2. Use shutil.move Instead of rename** (HIGH)

**Why**: `shutil.move()` handles Windows file locks better than `Path.rename()`

**Change**: Replace `temp_file.rename(self.queue_file)` with `shutil.move(str(temp_file), str(self.queue_file))`

---

### **3. Add File Lock Check Before Write** (MEDIUM)

**Optional Enhancement**: Check if file is locked before attempting write

```python
def _is_file_locked(self, filepath: Path) -> bool:
    """Check if file is locked by another process."""
    try:
        # Try to open file in exclusive mode
        with open(filepath, "r+b") as f:
            pass
        return False
    except (PermissionError, OSError):
        return True
```

---

### **4. Improve Error Handling** (MEDIUM)

**Add specific error messages**:
- Distinguish between file locked vs. other errors
- Log retry attempts
- Provide actionable error messages

---

## 🧪 **TESTING REQUIREMENTS**

1. **Test Concurrent Access**:
   - Run queue processor
   - Send broadcast message (8 agents)
   - Verify all 8 messages queued successfully
   - Check for WinError 5 in logs

2. **Test Retry Logic**:
   - Simulate file lock (open queue.json in another process)
   - Attempt to save entries
   - Verify retry attempts logged
   - Verify eventual success or proper error

3. **Test Broadcast**:
   - Send broadcast message
   - Verify 8/8 messages delivered
   - Check queue.json for all entries

---

## 📋 **IMPLEMENTATION CHECKLIST**

- [ ] Add retry logic with exponential backoff
- [ ] Replace `rename()` with `shutil.move()`
- [ ] Add specific WinError 5 handling
- [ ] Add retry attempt logging
- [ ] Test concurrent access
- [ ] Test broadcast (8/8 delivery)
- [ ] Update error messages
- [ ] Document changes

---

## 🎯 **EXPECTED OUTCOME**

After fix:
- ✅ Broadcast messages: 8/8 delivered (not 6/8)
- ✅ No WinError 5 Access Denied errors
- ✅ Queue file operations succeed with retry
- ✅ Proper error logging for debugging

---

**Status**: 🚨 **CRITICAL FIX - IMPLEMENT IMMEDIATELY**

**🐝 WE. ARE. SWARM. ⚡🔥**

