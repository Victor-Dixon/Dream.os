# Stall Detection Improvement Analysis

**Agent**: Agent-7 (Web Development Specialist)  
**Date**: 2025-12-11  
**Purpose**: Identify additional activity indicators to reduce false stall detections

---

## 📊 **CURRENT STATE ANALYSIS**

### **Existing Activity Indicators** (EnhancedAgentActivityDetector)

The system currently checks **11 activity indicators**:

1. ✅ `status.json` modification
2. ✅ Inbox file modifications
3. ✅ Devlog creation/modification
4. ✅ Report files in workspace
5. ✅ Message queue activity
6. ✅ Workspace file modifications (any file, <24 hours)
7. ✅ Git commits (with agent name in commit message)
8. ✅ Discord devlog posts
9. ✅ Tool execution (from logs/tool_executions.json)
10. ✅ Swarm Brain contributions
11. ✅ Agent lifecycle events (cycle_count, last_cycle, fsm_state)

**Current Coverage**: Comprehensive, but some gaps identified below.

---

## 🔍 **ADDITIONAL ACTIVITY INDICATORS TO CHECK**

### **1. Terminal Command Execution** ⚠️ **HIGH PRIORITY**

**Why**: Agents often run commands before committing (e.g., tests, validation, git status)

**Implementation**:
- Check process logs if available (e.g., `logs/command_executions.json`)
- Monitor terminal command history files (`.bash_history`, `.zsh_history`)
- Check for temporary execution artifacts (test outputs, validation results)

**Challenges**:
- Terminal history may not be agent-specific
- Process logs may not exist or be accessible
- Security/privacy concerns with command history

**Recommendation**: ⚠️ **MEDIUM PRIORITY** - Implement if process logging is available

---

### **2. Cycle Planner Updates** ✅ **HIGH PRIORITY**

**Why**: Agents update cycle planner tasks, indicating active planning

**Location**: `agent_workspaces/{agent_id}/cycle_planner_tasks_YYYY-MM-DD.json`

**Implementation**:
```python
def _check_cycle_planner(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check cycle planner task file modifications."""
    agent_dir = self.agent_workspaces / agent_id
    if not agent_dir.exists():
        return None
    
    # Check today's cycle planner file
    today = datetime.now().strftime("%Y-%m-%d")
    cycle_planner = agent_dir / f"cycle_planner_tasks_{today}.json"
    
    if cycle_planner.exists():
        mtime = cycle_planner.stat().st_mtime
        return {
            "source": "cycle_planner",
            "timestamp": mtime,
            "age_seconds": time.time() - mtime,
        }
    
    # Check most recent cycle planner file
    cycle_planners = list(agent_dir.glob("cycle_planner_tasks_*.json"))
    if cycle_planners:
        latest = max(cycle_planners, key=lambda p: p.stat().st_mtime)
        mtime = latest.stat().st_mtime
        # Only return if recent (within 7 days)
        if time.time() - mtime < (7 * 24 * 3600):
            return {
                "source": "cycle_planner",
                "timestamp": mtime,
                "age_seconds": time.time() - mtime,
            }
    return None
```

**Recommendation**: ✅ **IMPLEMENT** - High value, easy to check

---

### **3. Activity Log Files** ✅ **HIGH PRIORITY**

**Why**: Many agents create activity logs in `agent_workspaces/{agent_id}/activity/`

**Location**: `agent_workspaces/{agent_id}/activity/*.md`

**Implementation**:
```python
def _check_activity_logs(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check activity log files."""
    activity_dir = self.agent_workspaces / agent_id / "activity"
    if not activity_dir.exists():
        return None
    
    activity_files = list(activity_dir.glob("*.md"))
    if not activity_files:
        return None
    
    latest_file = max(activity_files, key=lambda p: p.stat().st_mtime)
    mtime = latest_file.stat().st_mtime
    
    # Only return if recent (within 24 hours)
    age_seconds = time.time() - mtime
    if age_seconds > 86400:
        return None
    
    return {
        "source": "activity_logs",
        "timestamp": mtime,
        "file": latest_file.name,
        "age_seconds": age_seconds,
    }
```

**Recommendation**: ✅ **IMPLEMENT** - High value, many agents use this

---

### **4. Contract System Interactions** ✅ **MEDIUM PRIORITY**

**Why**: Agents query contract system for tasks (`--get-next-task`), indicating active work

**Implementation**:
- Check contract system logs if available
- Monitor `agent_workspaces/{agent_id}/contracts/` directory
- Check for contract completion files

**Challenges**:
- Contract system may not log interactions
- May need contract system to expose activity API

**Recommendation**: ⚠️ **MEDIUM PRIORITY** - Implement if contract system exposes activity logs

---

### **5. Test Execution Results** ✅ **MEDIUM PRIORITY**

**Why**: Agents run tests before committing (pytest, validation scripts)

**Implementation**:
- Check for test result files (`test_results/`, `.pytest_cache/`, `coverage.json`)
- Monitor test output files (if timestamped)
- Check pytest cache modification times

**Example**:
```python
def _check_test_execution(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check test execution artifacts."""
    # Check coverage.json modification (updated after test runs)
    coverage_file = self.workspace_root / "coverage.json"
    if coverage_file.exists():
        mtime = coverage_file.stat().st_mtime
        age_seconds = time.time() - mtime
        if age_seconds < 3600:  # Within last hour
            return {
                "source": "test_execution",
                "timestamp": mtime,
                "age_seconds": age_seconds,
            }
    return None
```

**Recommendation**: ✅ **IMPLEMENT** - Medium value, indicates active work

---

### **6. File Creation in Workspace** ⚠️ **LOW PRIORITY**

**Why**: Agents create new files during work (not just modifications)

**Implementation**:
- Already partially covered by `_check_workspace_files()`
- Could add explicit file creation tracking

**Recommendation**: ⚠️ **LOW PRIORITY** - Already covered by existing check

---

### **7. API Endpoint Activity** ⚠️ **MEDIUM PRIORITY**

**Why**: If web layer is running, API hits indicate agent testing/usage

**Implementation**:
- Check web server logs if available
- Monitor API endpoint access logs
- Track agent-specific API usage

**Challenges**:
- Requires web server logging
- May not be agent-specific
- Only relevant if web layer is running

**Recommendation**: ⚠️ **MEDIUM PRIORITY** - Implement if web server logs are available

---

### **8. Passdown Files** ✅ **HIGH PRIORITY**

**Why**: Agents update passdown.json when completing work

**Location**: `agent_workspaces/{agent_id}/passdown.json`

**Implementation**:
```python
def _check_passdown(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check passdown.json file modifications."""
    passdown_file = self.agent_workspaces / agent_id / "passdown.json"
    if not passdown_file.exists():
        return None
    
    mtime = passdown_file.stat().st_mtime
    age_seconds = time.time() - mtime
    
    # Only return if recent (within 24 hours)
    if age_seconds > 86400:
        return None
    
    return {
        "source": "passdown",
        "timestamp": mtime,
        "age_seconds": age_seconds,
    }
```

**Recommendation**: ✅ **IMPLEMENT** - High value, many agents use this

---

### **9. Session Artifacts** ✅ **MEDIUM PRIORITY**

**Why**: Agents create session artifacts when working

**Location**: `agent_workspaces/{agent_id}/session_artifacts/`

**Implementation**:
- Similar to activity logs check
- Monitor session artifact directory modifications

**Recommendation**: ✅ **IMPLEMENT** - Medium value, complements activity logs

---

### **10. Git Working Directory Changes** ✅ **HIGH PRIORITY**

**Why**: Agents make changes before committing (git status shows modified files)

**Implementation**:
```python
def _check_git_working_directory(self, agent_id: str) -> Optional[Dict[str, Any]]:
    """Check git working directory for uncommitted changes."""
    try:
        import subprocess
        
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=self.workspace_root,
        )
        
        if result.returncode != 0:
            return None
        
        # Parse modified files
        modified_files = []
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                modified_files.append(line.strip())
        
        if not modified_files:
            return None
        
        # Check if any modified files are in agent workspace
        agent_workspace_path = f"agent_workspaces/{agent_id}/"
        agent_files = [f for f in modified_files if agent_workspace_path in f]
        
        if agent_files:
            # Check modification time of most recent file
            latest_mtime = 0
            for file_line in agent_files:
                file_path = file_line.split()[-1]  # Get filename
                full_path = self.workspace_root / file_path
                if full_path.exists():
                    mtime = full_path.stat().st_mtime
                    latest_mtime = max(latest_mtime, mtime)
            
            if latest_mtime > 0:
                return {
                    "source": "git_working_directory",
                    "timestamp": latest_mtime,
                    "modified_files_count": len(agent_files),
                    "age_seconds": time.time() - latest_mtime,
                }
        
        return None
    except Exception as e:
        logger.debug(f"Could not check git working directory: {e}")
        return None
```

**Recommendation**: ✅ **IMPLEMENT** - High value, catches work before commit

---

### **11. Validation Script Execution** ✅ **MEDIUM PRIORITY**

**Why**: Agents run validation scripts (e.g., `test_ssot_preservation.py`)

**Implementation**:
- Check for validation result files
- Monitor validation script execution logs
- Check for validation output files

**Recommendation**: ⚠️ **MEDIUM PRIORITY** - May overlap with test execution check

---

### **12. Documentation Files Created** ⚠️ **LOW PRIORITY**

**Why**: Agents create documentation/reports in root or docs/

**Implementation**:
- Check for new markdown files in workspace root or docs/
- Monitor timestamp of documentation files

**Challenges**:
- Hard to attribute to specific agent
- Many documentation files are shared

**Recommendation**: ⚠️ **LOW PRIORITY** - Hard to attribute, may cause false positives

---

## 🎯 **RECOMMENDED IMPLEMENTATIONS**

### **High Priority** (Implement First):

1. ✅ **Cycle Planner Updates** - Easy, high value
2. ✅ **Activity Log Files** - Easy, high value
3. ✅ **Passdown Files** - Easy, high value
4. ✅ **Git Working Directory Changes** - Medium complexity, high value

### **Medium Priority** (Consider Implementing):

5. ✅ **Test Execution Results** - Easy, medium value
6. ✅ **Session Artifacts** - Easy, medium value
7. ⚠️ **Contract System Interactions** - Depends on contract system API

### **Low Priority** (Future Consideration):

8. ⚠️ **Terminal Command Execution** - Depends on process logging
9. ⚠️ **API Endpoint Activity** - Depends on web server logs
10. ⚠️ **Validation Script Execution** - May overlap with test execution

---

## 📊 **IMPACT ANALYSIS**

### **Expected Reduction in False Positives**:

- **Current**: ~11 activity indicators checked
- **With High Priority Additions**: ~15 activity indicators
- **Estimated False Positive Reduction**: **30-40%**

### **Implementation Effort**:

- **High Priority Items**: ~2-4 hours total
- **Medium Priority Items**: ~3-6 hours total
- **Total Estimated Effort**: ~5-10 hours

---

## 🔧 **IMPLEMENTATION PLAN**

### **Phase 1: High Priority** (2-4 hours)
1. Add `_check_cycle_planner()` method
2. Add `_check_activity_logs()` method
3. Add `_check_passdown()` method
4. Add `_check_git_working_directory()` method

### **Phase 2: Medium Priority** (3-6 hours)
5. Add `_check_test_execution()` method
6. Add `_check_session_artifacts()` method
7. Evaluate contract system integration feasibility

### **Phase 3: Validation** (1-2 hours)
8. Test with real agent activity
9. Validate false positive reduction
10. Document new activity indicators

---

## ✅ **CONCLUSION**

**Current System**: Already comprehensive with 11 indicators  
**Gap Analysis**: 4 high-priority additions identified  
**Impact**: Expected 30-40% reduction in false positives  
**Effort**: ~5-10 hours total implementation

**Recommendation**: Implement Phase 1 (High Priority) additions to immediately improve stall detection accuracy.

---

**🐝 WE. ARE. SWARM. ⚡🔥**

*Agent-7 - Web Development Specialist*
