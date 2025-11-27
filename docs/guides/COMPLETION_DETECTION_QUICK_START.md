# Completion Detection Quick Start Guide

**For All Agents - SSOT Completion Detection**

## Problem Solved

Agents couldn't detect when commands/tasks finished, preventing autonomous operation.

## Solution

Use `TaskCompletionDetector` and `CommandExecutionWrapper` - SSOT for completion detection.

---

## Quick Usage

### **1. Simple Output Detection**

```python
from src.core.task_completion_detector import detect_command_completion

# After running a command, check output
output = "Processing complete ✅"
is_complete, reason = detect_command_completion(output)

if is_complete:
    print(f"Task finished: {reason}")
    # Proceed to next task
```

### **2. Task Registration & Monitoring**

```python
from src.core.task_completion_detector import get_completion_detector

detector = get_completion_detector()

# Register task before starting
detector.register_task(
    task_id="my_task_123",
    task_type="command",
    success_patterns=["complete", "done", "✅"],
    failure_patterns=["error", "failed", "❌"],
    timeout=300,  # 5 minutes
)

# Execute your command/operation
# ... do work ...

# Update with output
detector.update_task_output("my_task_123", output_text, exit_code=0)

# Check completion
is_complete, status = detector.is_task_complete("my_task_123")
if is_complete:
    print(f"Task {status}: {reason}")
```

### **3. Command Execution with Auto-Detection**

```python
from src.core.command_execution_wrapper import execute_command_with_completion

# Execute command with automatic completion detection
result = execute_command_with_completion(
    "python my_script.py",
    task_id="script_execution",
    check_completion=True,
    timeout=300,
)

if result.is_complete:
    if result.success:
        print(f"✅ Success: {result.completion_reason}")
    else:
        print(f"❌ Failed: {result.completion_reason}")
    # Proceed to next task
```

---

## Completion Indicators Detected

### **Success Indicators:**
- ✅ Exit code 0
- ✅ Patterns: "complete", "done", "finished", "success", "✅"
- ✅ Prompt returns: "PS D:\>", "$ ", "> "
- ✅ Output files created (if specified)

### **Failure Indicators:**
- ❌ Non-zero exit codes
- ❌ Patterns: "error", "failed", "❌", "exception", "fatal"
- ❌ Timeout exceeded

---

## Integration Pattern

```python
# 1. Register task
detector = get_completion_detector()
detector.register_task(task_id, "command")

# 2. Execute command/operation
# ... your code ...

# 3. Update with output
detector.update_task_output(task_id, output, exit_code)

# 4. Check completion
is_complete, status = detector.is_task_complete(task_id)

# 5. Proceed if complete
if is_complete:
    # Move to next task autonomously
    proceed_to_next_task()
```

---

## Common Patterns

### **PowerShell Commands:**
```python
# PowerShell commands return to prompt when done
output = "PS D:\Agent_Cellphone_V2_Repository>"
is_complete, reason = detect_command_completion(output)
# Returns: (True, "Prompt returned: PS D:\\")
```

### **Python Scripts:**
```python
# Python scripts exit with code 0 on success
result = execute_command_with_completion(
    "python script.py",
    check_completion=True,
)
# Auto-detects exit code 0 = success
```

### **File Operations:**
```python
# Register task expecting output file
detector.register_task(
    "file_operation",
    expected_output_file="output.json",
)
# Auto-detects when file is created
```

---

## Best Practices

1. **Always register long-running tasks** - Enables timeout detection
2. **Use exit codes when available** - Most reliable completion signal
3. **Specify success/failure patterns** - For custom output formats
4. **Check completion before proceeding** - Prevents race conditions
5. **Clean up completed tasks** - Call `cleanup_completed_tasks()` periodically

---

## SSOT Compliance

✅ **Single Source of Truth:** All agents use same completion detection logic  
✅ **V2 Compliant:** All files <400 lines  
✅ **Autonomous:** Agents can detect completion and proceed independently  

---

**Status:** ✅ READY FOR USE  
**For:** All Agents  
**Priority:** HIGH (Enables Autonomy)




