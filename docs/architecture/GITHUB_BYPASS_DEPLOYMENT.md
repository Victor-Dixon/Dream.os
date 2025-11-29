# GitHub Bypass System - Deployment Guide

**Date**: 2025-11-28  
**Status**: ✅ **READY FOR DEPLOYMENT**  
**Priority**: CRITICAL

---

## ✅ **COMPLETED COMPONENTS**

All core components are implemented and tested:

1. ✅ Local Repo Layer
2. ✅ Deferred Push Queue
3. ✅ Synthetic GitHub Wrapper
4. ✅ Consolidation Buffer
5. ✅ Merge Conflict Resolver
6. ✅ GitHub Pusher Agent
7. ✅ Updated `repo_safe_merge_v2.py`
8. ✅ Integration Tests

---

## 🚀 **DEPLOYMENT STEPS**

### **Step 1: Verify Installation**

```bash
# Test imports
python -c "from src.core.synthetic_github import get_synthetic_github; print('✅ OK')"
python -c "from tools.repo_safe_merge_v2 import SafeRepoMergeV2; print('✅ OK')"
python -c "from tools.github_pusher_agent import GitHubPusherAgent; print('✅ OK')"
```

### **Step 2: Set Up GitHub Pusher Agent (Windows)**

```powershell
# Run setup script
cd tools
.\setup_github_pusher_service.ps1
```

**Manual Setup (if script fails)**:
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "-u `"$PWD\tools\github_pusher_agent.py`"" -WorkingDirectory $PWD
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)
Register-ScheduledTask -TaskName "GitHubPusherAgent" -Action $action -Trigger $trigger -Description "Processes deferred GitHub push queue"
```

### **Step 3: Set Up GitHub Pusher Agent (Linux/Mac)**

```bash
# Make script executable
chmod +x tools/setup_github_pusher_service.sh

# Run setup
./tools/setup_github_pusher_service.sh
```

**Manual Setup (if script fails)**:
```bash
# Add to crontab
crontab -e

# Add this line (runs every 5 minutes):
*/5 * * * * cd /path/to/project && python -u tools/github_pusher_agent.py --once --max-items 10 >> logs/github_pusher_agent.log 2>&1
```

### **Step 4: Test the System**

```bash
# Test local repo manager
python -c "
from src.core.local_repo_layer import get_local_repo_manager
m = get_local_repo_manager()
print('✅ Local Repo Manager works')
"

# Test deferred queue
python -c "
from src.core.deferred_push_queue import get_deferred_push_queue
q = get_deferred_push_queue()
entry_id = q.enqueue_push('test-repo', 'test-branch', reason='test')
print(f'✅ Enqueued: {entry_id}')
print(f'📊 Stats: {q.get_stats()}')
"

# Test synthetic GitHub
python -c "
from src.core.synthetic_github import get_synthetic_github
github = get_synthetic_github()
print(f'✅ Synthetic GitHub initialized')
print(f'🔒 Sandbox mode: {github.is_sandbox_mode()}')
"
```

### **Step 5: Run Integration Tests**

```bash
# Run integration tests
python -m pytest tests/integration/test_github_bypass_system.py -v
```

---

## 📋 **USAGE EXAMPLES**

### **Example 1: Use New Local-First Merge Tool**

```bash
# Dry run
python tools/repo_safe_merge_v2.py FocusForge focusforge --target-num 24 --source-num 32

# Execute
python tools/repo_safe_merge_v2.py FocusForge focusforge --target-num 24 --source-num 32 --execute
```

### **Example 2: Check Deferred Queue**

```python
from src.core.deferred_push_queue import get_deferred_push_queue

queue = get_deferred_push_queue()
stats = queue.get_stats()
print(f"Pending: {stats['pending']}")
print(f"Retrying: {stats['retrying']}")
print(f"Failed: {stats['failed']}")
```

### **Example 3: Check Consolidation Buffer**

```python
from src.core.consolidation_buffer import get_consolidation_buffer

buffer = get_consolidation_buffer()
stats = buffer.get_stats()
print(f"Pending: {stats['pending']}")
print(f"Merged: {stats['merged']}")
print(f"Applied: {stats['applied']}")
```

### **Example 4: Manual Queue Processing**

```bash
# Process queue once
python tools/github_pusher_agent.py --once

# Process queue continuously (for testing)
python tools/github_pusher_agent.py --interval 60 --max-items 5
```

---

## 🔍 **MONITORING**

### **Check Queue Status**

```python
from src.core.deferred_push_queue import get_deferred_push_queue

queue = get_deferred_push_queue()
stats = queue.get_stats()
print(json.dumps(stats, indent=2))
```

### **Check Sandbox Mode**

```python
from src.core.synthetic_github import get_synthetic_github

github = get_synthetic_github()
if github.is_sandbox_mode():
    print("🔒 Sandbox mode enabled - GitHub operations deferred")
else:
    print("🔓 Normal mode - GitHub available")
```

### **View Task Status (Windows)**

```powershell
Get-ScheduledTask -TaskName GitHubPusherAgent | Format-List
```

### **View Logs (Linux/Mac)**

```bash
tail -f logs/github_pusher_agent.log
```

---

## 🛠️ **TROUBLESHOOTING**

### **Issue: Queue Not Processing**

**Solution**:
1. Check if pusher agent is running: `Get-ScheduledTask -TaskName GitHubPusherAgent` (Windows) or `crontab -l` (Linux)
2. Manually process queue: `python tools/github_pusher_agent.py --once`
3. Check logs for errors

### **Issue: Sandbox Mode Stuck**

**Solution**:
```python
from src.core.synthetic_github import get_synthetic_github

github = get_synthetic_github()
github.sandbox_mode.disable()  # Manually disable
```

### **Issue: Local Repos Not Found**

**Solution**:
```python
from src.core.local_repo_layer import get_local_repo_manager

manager = get_local_repo_manager()
# Clone from GitHub
manager.clone_from_github("repo-name", github_user="Dadudekc")
```

---

## ✅ **VERIFICATION CHECKLIST**

- [ ] All components import successfully
- [ ] Integration tests pass
- [ ] GitHub Pusher Agent scheduled/configured
- [ ] Deferred queue processes successfully
- [ ] Sandbox mode detection works
- [ ] Local repo manager can clone repos
- [ ] Consolidation buffer tracks merge plans
- [ ] `repo_safe_merge_v2.py` works in dry-run mode

---

## 🎯 **NEXT STEPS AFTER DEPLOYMENT**

1. **Test with Real Consolidation**: Run actual consolidation using `repo_safe_merge_v2.py`
2. **Monitor Queue**: Watch deferred queue for first few operations
3. **Verify Pusher Agent**: Ensure it processes queue every 5 minutes
4. **Update Other Tools**: Gradually migrate other consolidation tools to use new architecture

---

*Deployment ready - system eliminates GitHub as bottleneck!* 🚀


**Date**: 2025-11-28  
**Status**: ✅ **READY FOR DEPLOYMENT**  
**Priority**: CRITICAL

---

## ✅ **COMPLETED COMPONENTS**

All core components are implemented and tested:

1. ✅ Local Repo Layer
2. ✅ Deferred Push Queue
3. ✅ Synthetic GitHub Wrapper
4. ✅ Consolidation Buffer
5. ✅ Merge Conflict Resolver
6. ✅ GitHub Pusher Agent
7. ✅ Updated `repo_safe_merge_v2.py`
8. ✅ Integration Tests

---

## 🚀 **DEPLOYMENT STEPS**

### **Step 1: Verify Installation**

```bash
# Test imports
python -c "from src.core.synthetic_github import get_synthetic_github; print('✅ OK')"
python -c "from tools.repo_safe_merge_v2 import SafeRepoMergeV2; print('✅ OK')"
python -c "from tools.github_pusher_agent import GitHubPusherAgent; print('✅ OK')"
```

### **Step 2: Set Up GitHub Pusher Agent (Windows)**

```powershell
# Run setup script
cd tools
.\setup_github_pusher_service.ps1
```

**Manual Setup (if script fails)**:
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "-u `"$PWD\tools\github_pusher_agent.py`"" -WorkingDirectory $PWD
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 365)
Register-ScheduledTask -TaskName "GitHubPusherAgent" -Action $action -Trigger $trigger -Description "Processes deferred GitHub push queue"
```

### **Step 3: Set Up GitHub Pusher Agent (Linux/Mac)**

```bash
# Make script executable
chmod +x tools/setup_github_pusher_service.sh

# Run setup
./tools/setup_github_pusher_service.sh
```

**Manual Setup (if script fails)**:
```bash
# Add to crontab
crontab -e

# Add this line (runs every 5 minutes):
*/5 * * * * cd /path/to/project && python -u tools/github_pusher_agent.py --once --max-items 10 >> logs/github_pusher_agent.log 2>&1
```

### **Step 4: Test the System**

```bash
# Test local repo manager
python -c "
from src.core.local_repo_layer import get_local_repo_manager
m = get_local_repo_manager()
print('✅ Local Repo Manager works')
"

# Test deferred queue
python -c "
from src.core.deferred_push_queue import get_deferred_push_queue
q = get_deferred_push_queue()
entry_id = q.enqueue_push('test-repo', 'test-branch', reason='test')
print(f'✅ Enqueued: {entry_id}')
print(f'📊 Stats: {q.get_stats()}')
"

# Test synthetic GitHub
python -c "
from src.core.synthetic_github import get_synthetic_github
github = get_synthetic_github()
print(f'✅ Synthetic GitHub initialized')
print(f'🔒 Sandbox mode: {github.is_sandbox_mode()}')
"
```

### **Step 5: Run Integration Tests**

```bash
# Run integration tests
python -m pytest tests/integration/test_github_bypass_system.py -v
```

---

## 📋 **USAGE EXAMPLES**

### **Example 1: Use New Local-First Merge Tool**

```bash
# Dry run
python tools/repo_safe_merge_v2.py FocusForge focusforge --target-num 24 --source-num 32

# Execute
python tools/repo_safe_merge_v2.py FocusForge focusforge --target-num 24 --source-num 32 --execute
```

### **Example 2: Check Deferred Queue**

```python
from src.core.deferred_push_queue import get_deferred_push_queue

queue = get_deferred_push_queue()
stats = queue.get_stats()
print(f"Pending: {stats['pending']}")
print(f"Retrying: {stats['retrying']}")
print(f"Failed: {stats['failed']}")
```

### **Example 3: Check Consolidation Buffer**

```python
from src.core.consolidation_buffer import get_consolidation_buffer

buffer = get_consolidation_buffer()
stats = buffer.get_stats()
print(f"Pending: {stats['pending']}")
print(f"Merged: {stats['merged']}")
print(f"Applied: {stats['applied']}")
```

### **Example 4: Manual Queue Processing**

```bash
# Process queue once
python tools/github_pusher_agent.py --once

# Process queue continuously (for testing)
python tools/github_pusher_agent.py --interval 60 --max-items 5
```

---

## 🔍 **MONITORING**

### **Check Queue Status**

```python
from src.core.deferred_push_queue import get_deferred_push_queue

queue = get_deferred_push_queue()
stats = queue.get_stats()
print(json.dumps(stats, indent=2))
```

### **Check Sandbox Mode**

```python
from src.core.synthetic_github import get_synthetic_github

github = get_synthetic_github()
if github.is_sandbox_mode():
    print("🔒 Sandbox mode enabled - GitHub operations deferred")
else:
    print("🔓 Normal mode - GitHub available")
```

### **View Task Status (Windows)**

```powershell
Get-ScheduledTask -TaskName GitHubPusherAgent | Format-List
```

### **View Logs (Linux/Mac)**

```bash
tail -f logs/github_pusher_agent.log
```

---

## 🛠️ **TROUBLESHOOTING**

### **Issue: Queue Not Processing**

**Solution**:
1. Check if pusher agent is running: `Get-ScheduledTask -TaskName GitHubPusherAgent` (Windows) or `crontab -l` (Linux)
2. Manually process queue: `python tools/github_pusher_agent.py --once`
3. Check logs for errors

### **Issue: Sandbox Mode Stuck**

**Solution**:
```python
from src.core.synthetic_github import get_synthetic_github

github = get_synthetic_github()
github.sandbox_mode.disable()  # Manually disable
```

### **Issue: Local Repos Not Found**

**Solution**:
```python
from src.core.local_repo_layer import get_local_repo_manager

manager = get_local_repo_manager()
# Clone from GitHub
manager.clone_from_github("repo-name", github_user="Dadudekc")
```

---

## ✅ **VERIFICATION CHECKLIST**

- [ ] All components import successfully
- [ ] Integration tests pass
- [ ] GitHub Pusher Agent scheduled/configured
- [ ] Deferred queue processes successfully
- [ ] Sandbox mode detection works
- [ ] Local repo manager can clone repos
- [ ] Consolidation buffer tracks merge plans
- [ ] `repo_safe_merge_v2.py` works in dry-run mode

---

## 🎯 **NEXT STEPS AFTER DEPLOYMENT**

1. **Test with Real Consolidation**: Run actual consolidation using `repo_safe_merge_v2.py`
2. **Monitor Queue**: Watch deferred queue for first few operations
3. **Verify Pusher Agent**: Ensure it processes queue every 5 minutes
4. **Update Other Tools**: Gradually migrate other consolidation tools to use new architecture

---

*Deployment ready - system eliminates GitHub as bottleneck!* 🚀

