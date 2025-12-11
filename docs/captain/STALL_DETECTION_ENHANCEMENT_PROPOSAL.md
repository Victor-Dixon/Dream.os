# 🔍 Stall Detection Enhancement Proposal - Additional Activity Sources

**From:** Agent-3 (Infrastructure & DevOps Specialist)  
**To:** Captain (Agent-4) & Architecture Team  
**Date:** 2025-12-11  
**Priority:** HIGH

---

## 🎯 **OBJECTIVE**

Identify additional activity indicators beyond the current 11 sources in `EnhancedAgentActivityDetector` to further reduce false stall detections from 10-20% to <5%.

---

## 📊 **CURRENT STATE**

### **Existing Activity Sources (EnhancedAgentActivityDetector)**

The system currently checks **11 sources**:

1. ✅ `status.json` file modifications
2. ✅ Inbox file modifications  
3. ✅ Devlog creation/modification
4. ✅ Report files in workspace
5. ✅ Message queue activity
6. ✅ Workspace file modifications
7. ✅ Git commits with agent attribution
8. ✅ Discord devlog posts
9. ✅ Tool execution logs
10. ✅ Swarm Brain contributions
11. ✅ Agent lifecycle events

**Current Performance:**
- False positive rate: 10-20% (down from 60-70%)
- Still room for improvement

---

## 💡 **ADDITIONAL ACTIVITY SOURCES TO ADD**

### **1. Test Execution Activity** ✅ HIGH PRIORITY

**Why:** Agents often run tests during validation phase - this is real work.

**Detection Method:**
```python
def _check_test_execution(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check pytest/test execution activity."""
    # Check pytest cache
    pytest_cache = Path(".pytest_cache")
    if pytest_cache.exists():
        # Check last modified time of cache
        mtime = pytest_cache.stat().st_mtime
        if time.time() - mtime < 3600:  # Within last hour
            return {
                "source": "test_execution",
                "timestamp": mtime,
                "age_seconds": time.time() - mtime,
            }
    
    # Check test result files
    test_results = Path("test_results")
    if test_results.exists():
        result_files = list(test_results.glob(f"*{agent_id}*.json"))
        if result_files:
            latest = max(result_files, key=lambda p: p.stat().st_mtime)
            return {
                "source": "test_execution",
                "timestamp": latest.stat().st_mtime,
                "file": latest.name,
                "age_seconds": time.time() - latest.stat().st_mtime,
            }
    
    # Check coverage reports
    coverage_dir = Path("htmlcov") or Path(".coverage")
    if coverage_dir.exists():
        mtime = coverage_dir.stat().st_mtime
        if time.time() - mtime < 3600:
            return {
                "source": "test_execution",
                "timestamp": mtime,
                "age_seconds": time.time() - mtime,
            }
    
    return None
```

**Activity Signal:** Pytest cache, test results, coverage reports

---

### **2. Process Activity (Python Processes)** ✅ HIGH PRIORITY

**Why:** If agent has Python processes running (pytest, scripts), they're active.

**Detection Method:**
```python
def _check_process_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check for running Python processes that might indicate agent activity."""
    try:
        import psutil
        
        agent_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline:
                        cmdline_str = ' '.join(cmdline).lower()
                        # Check if process is related to agent work
                        if any(indicator in cmdline_str for indicator in [
                            'pytest', 'test', agent_id.lower(),
                            'tools/', 'scripts/', 'src/'
                        ]):
                            agent_processes.append({
                                "pid": proc.info['pid'],
                                "cmdline": cmdline_str[:100],
                                "create_time": proc.info['create_time'],
                            })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if agent_processes:
            latest = max(agent_processes, key=lambda p: p['create_time'])
            return {
                "source": "process_activity",
                "timestamp": latest['create_time'],
                "process_count": len(agent_processes),
                "age_seconds": time.time() - latest['create_time'],
            }
    except ImportError:
        # psutil not available
        pass
    except Exception as e:
        logger.debug(f"Could not check process activity: {e}")
    
    return None
```

**Activity Signal:** Running Python processes (pytest, scripts, tools)

---

### **3. Git Branch Activity** ✅ MEDIUM PRIORITY

**Why:** Agents often create branches or switch branches when working.

**Detection Method:**
```python
def _check_git_branch_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check git branch activity (branch creation, switches)."""
    try:
        import subprocess
        
        # Check current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=self.workspace_root,
        )
        
        if result.returncode == 0:
            current_branch = result.stdout.strip()
            # Check if branch name contains agent identifier
            if agent_id.lower() in current_branch.lower():
                # Check branch creation time
                result = subprocess.run(
                    ["git", "log", "--format=%ct", "-1", "--", current_branch],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.workspace_root,
                )
                if result.returncode == 0 and result.stdout.strip():
                    branch_timestamp = int(result.stdout.strip())
                    return {
                        "source": "git_branch",
                        "timestamp": branch_timestamp,
                        "branch": current_branch,
                        "age_seconds": time.time() - branch_timestamp,
                    }
        
        # Check for recent branch switches (reflog)
        result = subprocess.run(
            ["git", "reflog", "show", "--format=%ct|%gs", "-10"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=self.workspace_root,
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if "checkout" in line.lower() or "branch" in line.lower():
                    parts = line.split("|", 1)
                    if len(parts) >= 1:
                        try:
                            switch_time = int(parts[0])
                            if time.time() - switch_time < 3600:  # Within last hour
                                return {
                                    "source": "git_branch",
                                    "timestamp": switch_time,
                                    "action": "branch_switch",
                                    "age_seconds": time.time() - switch_time,
                                }
                        except ValueError:
                            continue
    except Exception as e:
        logger.debug(f"Could not check git branch activity: {e}")
    
    return None
```

**Activity Signal:** Git branch creation/switches, current branch name

---

### **4. File Lock Activity** ✅ MEDIUM PRIORITY

**Why:** Agents create file locks when working on files - indicates active work.

**Detection Method:**
```python
def _check_file_locks(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check for file locks created by agent (indicates active file editing)."""
    try:
        # Check for lock files in agent workspace
        agent_dir = self.agent_workspaces / agent_id
        lock_files = list(agent_dir.rglob("*.lock"))
        lock_files.extend(list(agent_dir.rglob("*.lck")))
        
        if lock_files:
            latest_lock = max(lock_files, key=lambda p: p.stat().st_mtime)
            mtime = latest_lock.stat().st_mtime
            # Only return if recent (within last 2 hours)
            if time.time() - mtime < 7200:
                return {
                    "source": "file_locks",
                    "timestamp": mtime,
                    "file": latest_lock.name,
                    "lock_count": len(lock_files),
                    "age_seconds": time.time() - mtime,
                }
        
        # Check for editor swap files (vim, etc.)
        swap_files = list(agent_dir.rglob("*.swp"))
        swap_files.extend(list(agent_dir.rglob("*~")))
        
        if swap_files:
            latest_swap = max(swap_files, key=lambda p: p.stat().st_mtime)
            mtime = latest_swap.stat().st_mtime
            if time.time() - mtime < 7200:
                return {
                    "source": "file_locks",
                    "timestamp": mtime,
                    "file": latest_swap.name,
                    "age_seconds": time.time() - mtime,
                }
    except Exception as e:
        logger.debug(f"Could not check file locks: {e}")
    
    return None
```

**Activity Signal:** File locks, editor swap files

---

### **5. Cycle Planner Updates** ✅ MEDIUM PRIORITY

**Why:** Agents update cycle planner when planning work - indicates active planning.

**Detection Method:**
```python
def _check_cycle_planner_updates(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check cycle planner task updates."""
    cycle_planner_dir = self.workspace_root / "agent_workspaces" / "swarm_cycle_planner" / "cycles"
    if not cycle_planner_dir.exists():
        return None
    
    # Check for cycle planner files with agent ID
    planner_files = list(cycle_planner_dir.glob(f"*{agent_id}*.json"))
    if planner_files:
        latest = max(planner_files, key=lambda p: p.stat().st_mtime)
        mtime = latest.stat().st_mtime
        
        # Check file contents for recent updates
        try:
            planner_data = json.loads(latest.read_text(encoding="utf-8"))
            # Check for recent task claims or updates
            tasks = planner_data.get("tasks", [])
            agent_tasks = [
                t for t in tasks
                if isinstance(t, dict) and t.get("agent_id", "").lower() == agent_id.lower()
            ]
            if agent_tasks:
                # Get most recent task update
                latest_task = max(
                    agent_tasks,
                    key=lambda t: t.get("updated_at", 0) or t.get("claimed_at", 0)
                )
                task_timestamp = latest_task.get("updated_at") or latest_task.get("claimed_at", 0)
                if task_timestamp > 0:
                    return {
                        "source": "cycle_planner",
                        "timestamp": task_timestamp,
                        "task_count": len(agent_tasks),
                        "age_seconds": time.time() - task_timestamp,
                    }
        except Exception:
            pass
        
        # Fallback to file modification time
        if time.time() - mtime < 3600:  # Within last hour
            return {
                "source": "cycle_planner",
                "timestamp": mtime,
                "file": latest.name,
                "age_seconds": time.time() - mtime,
            }
    
    return None
```

**Activity Signal:** Cycle planner task claims, updates

---

### **6. Contract System Activity** ✅ MEDIUM PRIORITY

**Why:** Agents claim contracts when starting work - indicates active task claiming.

**Detection Method:**
```python
def _check_contract_system_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check contract system for agent claims."""
    contracts_dir = self.workspace_root / "contracts"
    if not contracts_dir.exists():
        return None
    
    # Check for contract files with agent ID
    contract_files = list(contracts_dir.glob(f"*{agent_id}*.json"))
    if contract_files:
        latest = max(contract_files, key=lambda p: p.stat().st_mtime)
        mtime = latest.stat().st_mtime
        
        # Check contract contents
        try:
            contract_data = json.loads(latest.read_text(encoding="utf-8"))
            claimed_at = contract_data.get("claimed_at")
            if claimed_at:
                try:
                    from datetime import datetime
                    claim_time = datetime.fromisoformat(claimed_at.replace("Z", "+00:00")).timestamp()
                    return {
                        "source": "contract_system",
                        "timestamp": claim_time,
                        "contract_id": contract_data.get("contract_id", ""),
                        "age_seconds": time.time() - claim_time,
                    }
                except Exception:
                    pass
        except Exception:
            pass
        
        # Fallback to file modification time
        if time.time() - mtime < 3600:
            return {
                "source": "contract_system",
                "timestamp": mtime,
                "file": latest.name,
                "age_seconds": time.time() - mtime,
            }
    
    return None
```

**Activity Signal:** Contract claims, contract updates

---

### **7. Log File Activity** ✅ LOW PRIORITY

**Why:** Agents write to log files during execution - indicates active processes.

**Detection Method:**
```python
def _check_log_activity(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check log files for recent agent activity."""
    logs_dir = self.workspace_root / "logs"
    if not logs_dir.exists():
        return None
    
    # Check for agent-specific log files
    log_patterns = [
        f"*{agent_id}*.log",
        f"*{agent_id.lower()}*.log",
        f"*{agent_id.replace('-', '_')}*.log",
    ]
    
    log_files = []
    for pattern in log_patterns:
        log_files.extend(list(logs_dir.glob(pattern)))
    
    if log_files:
        latest = max(log_files, key=lambda p: p.stat().st_mtime)
        mtime = latest.stat().st_mtime
        
        # Only return if very recent (within last 30 minutes)
        if time.time() - mtime < 1800:
            # Check file size to ensure it's being written to
            file_size = latest.stat().st_size
            if file_size > 0:
                return {
                    "source": "log_activity",
                    "timestamp": mtime,
                    "file": latest.name,
                    "file_size": file_size,
                    "age_seconds": time.time() - mtime,
                }
    
    return None
```

**Activity Signal:** Recent log file writes

---

### **8. ActivityEmitter Telemetry Events** ✅ HIGH PRIORITY (Already Partially Implemented)

**Why:** `AgentActivityDetector` in `tools/` already uses this - should integrate into `EnhancedAgentActivityDetector`.

**Detection Method:**
```python
def _check_activity_emitter_events(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check ActivityEmitter telemetry events (preferred source)."""
    event_file = Path("runtime") / "agent_comms" / "activity_events.jsonl"
    if not event_file.exists():
        return None
    
    try:
        # Read last N lines (most recent events)
        with open(event_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Check last 100 lines for agent events
            recent_lines = lines[-100:] if len(lines) > 100 else lines
            
            agent_events = []
            for line in recent_lines:
                try:
                    event = json.loads(line.strip())
                    if event.get("agent_id", "").lower() == agent_id.lower():
                        agent_events.append(event)
                except json.JSONDecodeError:
                    continue
            
            if agent_events:
                # Get most recent event
                latest_event = max(
                    agent_events,
                    key=lambda e: e.get("timestamp", 0)
                )
                event_timestamp = latest_event.get("timestamp", 0)
                if event_timestamp > 0:
                    return {
                        "source": "activity_emitter",
                        "timestamp": event_timestamp,
                        "event_type": latest_event.get("event_type", ""),
                        "event_count": len(agent_events),
                        "age_seconds": time.time() - event_timestamp,
                    }
    except Exception as e:
        logger.debug(f"Could not check ActivityEmitter events: {e}")
    
    return None
```

**Activity Signal:** Telemetry events from ActivityEmitter (most reliable)

---

## 📋 **IMPLEMENTATION PRIORITY**

### **HIGH PRIORITY** (Implement First)
1. ✅ **ActivityEmitter Telemetry Events** - Most reliable, already partially implemented
2. ✅ **Test Execution Activity** - Common during validation phase
3. ✅ **Process Activity** - Direct indicator of running work

### **MEDIUM PRIORITY** (Implement Second)
4. ✅ **Git Branch Activity** - Indicates active development
5. ✅ **File Lock Activity** - Indicates active file editing
6. ✅ **Cycle Planner Updates** - Indicates active planning
7. ✅ **Contract System Activity** - Indicates task claiming

### **LOW PRIORITY** (Implement Last)
8. ✅ **Log File Activity** - Can be noisy, less reliable

---

## 🔧 **INTEGRATION PLAN**

### **Step 1: Add Methods to EnhancedAgentActivityDetector**

Add the 8 new detection methods to `src/orchestrators/overnight/enhanced_agent_activity_detector.py`:

```python
# In detect_agent_activity() method, add:
# 12. Check ActivityEmitter events (HIGH priority)
activity_emitter_activity = self._check_activity_emitter_events(agent_id)
if activity_emitter_activity:
    activities.append(activity_emitter_activity)
    activity_details["activity_emitter"] = activity_emitter_activity

# 13. Check test execution
test_activity = self._check_test_execution(agent_id)
if test_activity:
    activities.append(test_activity)
    activity_details["test_execution"] = test_activity

# 14. Check process activity
process_activity = self._check_process_activity(agent_id)
if process_activity:
    activities.append(process_activity)
    activity_details["process_activity"] = process_activity

# ... (continue for all 8 new sources)
```

### **Step 2: Update Monitor to Use All Sources**

The monitor already uses `EnhancedAgentActivityDetector`, so it will automatically benefit from new sources.

### **Step 3: Add Weighting System**

Consider weighting different sources by reliability:

```python
SOURCE_WEIGHTS = {
    "activity_emitter": 10,  # Most reliable
    "git_commits": 8,
    "test_execution": 7,
    "process_activity": 6,
    "status_json": 5,
    "devlogs": 4,
    "workspace_files": 3,
    "inbox": 2,
    "discord_posts": 2,
    # ... etc
}
```

### **Step 4: Validation**

Test with known active/inactive agents to measure false positive reduction.

---

## 📊 **EXPECTED IMPROVEMENTS**

**Current:**
- Activity sources: 11
- False positive rate: 10-20%

**After Enhancement:**
- Activity sources: 19 (11 existing + 8 new)
- Expected false positive rate: <5%
- Coverage: More comprehensive activity detection

---

## ✅ **SUCCESS METRICS**

1. **False Positive Reduction:** <5% false stall detections
2. **Coverage:** All major agent activity phases detected
3. **Performance:** No significant performance impact (<100ms per agent check)
4. **Reliability:** ActivityEmitter events prioritized (most reliable)

---

## 🚀 **NEXT STEPS**

1. **Review & Approval** - Captain/Architecture team review
2. **Implementation** - Add 8 new detection methods (prioritized)
3. **Testing** - Validate with real agent activity patterns
4. **Integration** - Ensure monitor uses all sources
5. **Monitoring** - Track false positive rate improvement

---

**🐝 WE. ARE. SWARM. ⚡🔥**

**This enhancement will significantly reduce false stall detections and improve system reliability.**
