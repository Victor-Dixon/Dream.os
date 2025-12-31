# Cycle Snapshot System - Architecture Design

**Date:** 2025-12-31  
**Designed By:** Agent-2 (Architecture & Design Specialist)  
**Coordinated With:** Agent-3 (Infrastructure & DevOps Specialist)  
**Status:** Architecture Design Phase

---

## 🎯 System Vision

**Cycle Snapshot System = Central Nervous System of the Swarm**

A unified system that:
- **Collects** from 30+ systems (MCP servers, services, messaging, git, etc.)
- **Aggregates** into complete project state
- **Resets** agent status.json files to neutral state (smart reset)
- **Distributes** to all systems (blog, Discord, Swarm Brain, vector DB, etc.)
- **Tracks** progression over time (velocity, efficiency, quality trends)
- **Grades** components (infrastructure, communication, development, etc.)
- **Feeds** strategic decision-making

---

## 🏗️ Architecture Overview

### Modular System Structure (V2 Compliant)

```
tools/cycle_snapshots/
├── __init__.py
├── data_collectors/           # Data collection modules
│   ├── __init__.py
│   ├── agent_status_collector.py      # Agent status.json collection
│   ├── task_log_collector.py           # MASTER_TASK_LOG.md parsing
│   ├── git_collector.py                # Git activity analysis
│   ├── changelog_collector.py          # CHANGELOG.md parsing
│   ├── captain_log_collector.py        # Captain log parsing
│   ├── mcp_collector.py                # MCP server data collection
│   └── project_scanner_collector.py     # Project analysis integration
├── aggregators/               # Data aggregation modules
│   ├── __init__.py
│   ├── snapshot_aggregator.py          # Unified snapshot generation
│   ├── metrics_calculator.py           # Metrics calculation
│   └── insights_generator.py           # AI insights generation
├── processors/                 # Data processing modules
│   ├── __init__.py
│   ├── status_resetter.py              # Smart status.json reset logic
│   ├── report_generator.py              # Markdown report generation
│   ├── blog_generator.py                # Victor-voiced blog generation
│   └── distribution_manager.py         # Multi-system distribution
├── integrations/              # System integration modules
│   ├── __init__.py
│   ├── discord_integration.py          # Discord posting
│   ├── blog_integration.py             # WordPress publishing
│   ├── swarm_brain_integration.py      # Swarm Brain learning
│   ├── vector_db_integration.py        # Vector DB storage
│   └── task_manager_integration.py     # Task log updates
├── core/                      # Core utilities
│   ├── __init__.py
│   ├── snapshot_models.py              # Data models
│   ├── snapshot_cache.py               # Caching layer
│   └── snapshot_validator.py           # Validation logic
├── main.py                    # CLI entrypoint
└── README.md                  # Documentation
```

**Total Modules:** ~20 modules, all V2 compliant (<400 lines each)

---

## 🔐 Critical Safety Constraints

### 1. Status.json Reset Safety

**CRITICAL:** Status.json reset must be:
- ✅ **Atomic:** Backup before reset, validate after reset
- ✅ **Reversible:** Keep backups for rollback
- ✅ **Selective:** Smart reset (keep active, archive completed)
- ✅ **Validated:** Verify JSON integrity after reset
- ✅ **Error-Handled:** Skip agent if reset fails, continue with others

**Implementation:**
```python
def reset_agent_status_safely(agent_id: str, snapshot_data: dict, workspace_root: Path) -> bool:
    """
    Safely reset agent status.json with full error handling.
    
    Safety Measures:
    1. Create backup before reset
    2. Validate JSON before and after
    3. Atomic write (write to temp, then rename)
    4. Rollback on failure
    5. Log all operations
    """
    status_file = workspace_root / "agent_workspaces" / agent_id / "status.json"
    backup_file = status_file.parent / f"status_backup_{timestamp}.json"
    
    try:
        # 1. Backup
        shutil.copy(status_file, backup_file)
        
        # 2. Read and validate
        current_status = json.load(open(status_file, 'r', encoding='utf-8'))
        validate_status_json(current_status)
        
        # 3. Generate reset status
        reset_status = generate_reset_status(current_status, snapshot_data)
        validate_status_json(reset_status)
        
        # 4. Atomic write
        temp_file = status_file.with_suffix('.json.tmp')
        json.dump(reset_status, open(temp_file, 'w', encoding='utf-8'), indent=2)
        temp_file.replace(status_file)  # Atomic rename
        
        # 5. Validate final state
        final_status = json.load(open(status_file, 'r', encoding='utf-8'))
        validate_status_json(final_status)
        
        return True
        
    except Exception as e:
        # Rollback on failure
        if backup_file.exists():
            shutil.copy(backup_file, status_file)
        logger.error(f"Reset failed for {agent_id}: {e}")
        return False
```

### 2. Discord Bot Integration Safety

**CRITICAL:** Must not break StatusChangeMonitor:
- ✅ **No Discord Dependencies:** Core library has zero Discord dependencies
- ✅ **Additive Only:** Extend existing, don't replace
- ✅ **Backward Compatible:** StatusChangeMonitor continues working
- ✅ **Gradual Migration:** Migrate StatusChangeMonitor later (separate phase)

**Architecture Decision:**
- Core snapshot system: **NO Discord dependencies**
- Discord integration: **Separate module** (`integrations/discord_integration.py`)
- StatusChangeMonitor: **Uses core library** (future migration, not Phase 1)

### 3. Concurrent Access Safety

**CRITICAL:** Prevent concurrent snapshot runs:
- ✅ **Lock File:** `reports/cycle_snapshots/.snapshot_in_progress`
- ✅ **Check Before Start:** Fail if lock exists
- ✅ **Release After Complete:** Always release lock (even on error)
- ✅ **Timeout:** Lock expires after 1 hour (stale lock cleanup)

---

## 📐 Module Design Specifications

### Module 1: `data_collectors/agent_status_collector.py`

**Purpose:** Collect agent status.json files safely

**Functions:**
- `collect_all_agent_status(workspace_root: Path) -> Dict[str, Dict]` (30 lines)
- `collect_agent_status(agent_id: str, workspace_root: Path) -> Optional[Dict]` (25 lines)
- `validate_status_json(status: Dict) -> bool` (20 lines)

**Dependencies:**
- Uses `src/core/agent_status/reader.py` (from status monitor consolidation)

**V2 Compliance:** ✅ <400 lines, functions <30 lines

---

### Module 2: `data_collectors/task_log_collector.py`

**Purpose:** Parse MASTER_TASK_LOG.md and extract task metrics

**Functions:**
- `parse_task_log(workspace_root: Path) -> Dict[str, Any]` (30 lines)
- `extract_task_metrics(task_log_content: str) -> Dict[str, Any]` (30 lines)
- `compare_with_previous_snapshot(current: Dict, previous: Dict) -> Dict[str, Any]` (30 lines)

**Dependencies:**
- MCP: `mcp_task-manager_get_tasks()` (optional, fallback to file parsing)

**V2 Compliance:** ✅ <400 lines, functions <30 lines

---

### Module 3: `data_collectors/git_collector.py`

**Purpose:** Analyze git activity since last snapshot

**Functions:**
- `analyze_git_activity(workspace_root: Path, since_timestamp: datetime) -> Dict[str, Any]` (30 lines)
- `get_commits_since(since_timestamp: datetime) -> List[Dict]` (25 lines)
- `calculate_git_metrics(commits: List[Dict]) -> Dict[str, Any]` (25 lines)

**Dependencies:**
- MCP: `mcp_git-operations_get_recent_commits()` (optional, fallback to git CLI)

**V2 Compliance:** ✅ <400 lines, functions <30 lines

---

### Module 4: `data_collectors/mcp_collector.py`

**Purpose:** Collect data from all MCP servers

**Functions:**
- `collect_mcp_data(workspace_root: Path) -> Dict[str, Any]` (30 lines)
- `collect_swarm_brain_data() -> Dict[str, Any]` (25 lines)
- `collect_website_data() -> Dict[str, Any]` (25 lines)
- `collect_deployment_data() -> Dict[str, Any]` (25 lines)
- `collect_analytics_data() -> Dict[str, Any]` (25 lines)

**Dependencies:**
- All MCP servers (swarm_brain, task_manager, git_operations, website_manager, etc.)

**V2 Compliance:** ✅ <400 lines, functions <30 lines

---

### Module 5: `processors/status_resetter.py`

**Purpose:** Safely reset agent status.json files

**Functions:**
- `reset_all_agent_status(snapshot_data: Dict, workspace_root: Path) -> Dict[str, bool]` (30 lines)
- `reset_agent_status_safely(agent_id: str, snapshot_data: Dict, workspace_root: Path) -> bool` (50 lines - complex but necessary)
- `generate_reset_status(current: Dict, snapshot_data: Dict) -> Dict` (30 lines)
- `filter_active_items(items: List) -> List` (20 lines)
- `backup_status_file(status_file: Path) -> Path` (15 lines)

**Safety Features:**
- Atomic writes
- Backup before reset
- Validation before/after
- Rollback on failure
- Error isolation (one agent failure doesn't stop others)

**V2 Compliance:** ⚠️ `reset_agent_status_safely` may exceed 30 lines (complex safety logic), but acceptable for critical operation

---

### Module 6: `aggregators/snapshot_aggregator.py`

**Purpose:** Aggregate all collected data into unified snapshot

**Functions:**
- `aggregate_snapshot(all_data: Dict[str, Dict]) -> Dict[str, Any]` (30 lines)
- `generate_snapshot_metadata(cycle_num: int) -> Dict[str, Any]` (20 lines)
- `generate_project_state(metrics: Dict) -> Dict[str, Any]` (30 lines)

**V2 Compliance:** ✅ <400 lines, functions <30 lines

---

### Module 7: `processors/report_generator.py`

**Purpose:** Generate markdown report from snapshot

**Functions:**
- `generate_markdown_report(snapshot: Dict) -> str` (50 lines - acceptable for report generation)
- `format_agent_section(agent_id: str, agent_data: Dict) -> str` (30 lines)
- `format_metrics_section(metrics: Dict) -> str` (30 lines)

**V2 Compliance:** ⚠️ `generate_markdown_report` may exceed 30 lines, but acceptable for report generation

---

### Module 8: `processors/blog_generator.py`

**Purpose:** Generate Victor-voiced blog post

**Functions:**
- `generate_blog_content(snapshot: Dict, workspace_root: Path) -> str` (50 lines - acceptable)
- `transform_to_narrative(snapshot: Dict) -> str` (30 lines)
- `apply_victor_voice(content: str, workspace_root: Path) -> str` (uses existing blog_generator)

**Dependencies:**
- Reuses `tools/cycle_accomplishments/blog_generator.py` (apply_victor_voice)

**V2 Compliance:** ⚠️ `generate_blog_content` may exceed 30 lines, but acceptable for content generation

---

### Module 9: `integrations/distribution_manager.py`

**Purpose:** Distribute snapshot to all systems

**Functions:**
- `distribute_snapshot(snapshot: Dict, workspace_root: Path) -> Dict[str, bool]` (30 lines)
- `distribute_to_discord(snapshot: Dict) -> bool` (25 lines)
- `distribute_to_blog(snapshot: Dict) -> bool` (25 lines)
- `distribute_to_swarm_brain(snapshot: Dict) -> bool` (25 lines)
- `distribute_to_vector_db(snapshot: Dict) -> bool` (25 lines)

**V2 Compliance:** ✅ <400 lines, functions <30 lines

---

## 🔄 Integration Patterns

### Pattern 1: MCP Server Integration

**Approach:** Use MCP tools for data collection

**Example:**
```python
def collect_swarm_brain_data() -> Dict[str, Any]:
    """Collect data from Swarm Brain MCP server."""
    try:
        # Query Swarm Brain for insights
        insights = mcp_swarm_brain_search_swarm_knowledge(
            agent_id="Agent-4",
            query="cycle patterns productivity",
            limit=5
        )
        
        # Feed snapshot to Swarm Brain
        mcp_swarm_brain_share_learning(
            agent_id="Agent-4",
            title=f"Cycle {cycle_num} Snapshot",
            content=snapshot_summary,
            tags=["cycle-snapshot", "strategic-planning"]
        )
        
        return {
            "insights": insights,
            "learning_shared": True
        }
    except Exception as e:
        logger.warning(f"Swarm Brain integration failed: {e}")
        return {"insights": [], "learning_shared": False}
```

**Benefits:**
- Standardized interface
- Error handling built-in
- Optional (graceful degradation)

---

### Pattern 2: Service Integration

**Approach:** Import and use service classes directly

**Example:**
```python
def collect_contract_data() -> Dict[str, Any]:
    """Collect data from contract service."""
    try:
        from src.services.contract_system.manager import ContractManager
        
        contract_manager = ContractManager()
        contracts = contract_manager.get_all_contracts()
        
        return {
            "total": len(contracts),
            "active": len([c for c in contracts if c.status == 'active']),
            "completed_this_cycle": get_completed_contracts(contracts)
        }
    except Exception as e:
        logger.warning(f"Contract service integration failed: {e}")
        return {"total": 0, "active": 0, "completed_this_cycle": 0}
```

**Benefits:**
- Direct access
- Type safety
- Performance

---

### Pattern 3: File System Integration

**Approach:** Read files directly (with parsing)

**Example:**
```python
def collect_task_log_data(workspace_root: Path) -> Dict[str, Any]:
    """Collect data from MASTER_TASK_LOG.md."""
    task_log_file = workspace_root / "MASTER_TASK_LOG.md"
    
    if not task_log_file.exists():
        return {"error": "MASTER_TASK_LOG.md not found"}
    
    try:
        content = task_log_file.read_text(encoding='utf-8')
        return parse_task_log(content)
    except Exception as e:
        logger.error(f"Task log parsing failed: {e}")
        return {"error": str(e)}
```

**Benefits:**
- No dependencies
- Works offline
- Fast

---

## 🛡️ Safety Architecture

### 1. Lock File System

```python
class SnapshotLock:
    """Manages snapshot lock file to prevent concurrent runs."""
    
    def __init__(self, workspace_root: Path):
        self.lock_file = workspace_root / "reports" / "cycle_snapshots" / ".snapshot_in_progress"
        self.lock_timeout = 3600  # 1 hour
    
    def acquire(self) -> bool:
        """Acquire lock if available."""
        if self.lock_file.exists():
            # Check if lock is stale
            lock_age = time.time() - self.lock_file.stat().st_mtime
            if lock_age > self.lock_timeout:
                # Stale lock, remove it
                self.lock_file.unlink()
            else:
                return False  # Lock active
        
        # Create lock
        self.lock_file.write_text(f"{datetime.now().isoformat()}\n{os.getpid()}")
        return True
    
    def release(self):
        """Release lock."""
        if self.lock_file.exists():
            self.lock_file.unlink()
```

---

### 2. Backup System

```python
class StatusBackupManager:
    """Manages status.json backups before reset."""
    
    def __init__(self, workspace_root: Path):
        self.backup_dir = workspace_root / "reports" / "cycle_snapshots" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.retention_days = 30
    
    def backup_status(self, agent_id: str, status_file: Path) -> Path:
        """Create backup of status.json before reset."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"{agent_id}_status_{timestamp}.json"
        shutil.copy(status_file, backup_file)
        return backup_file
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period."""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        for backup_file in self.backup_dir.glob("*.json"):
            if datetime.fromtimestamp(backup_file.stat().st_mtime) < cutoff:
                backup_file.unlink()
```

---

### 3. Validation System

```python
class SnapshotValidator:
    """Validates snapshot data and status.json integrity."""
    
    def validate_status_json(self, status: Dict) -> Tuple[bool, List[str]]:
        """Validate status.json structure and content."""
        errors = []
        
        # Required fields
        required = ["agent_id", "agent_name", "status"]
        for field in required:
            if field not in status:
                errors.append(f"Missing required field: {field}")
        
        # Validate JSON structure
        try:
            json.dumps(status)  # Ensure serializable
        except Exception as e:
            errors.append(f"Invalid JSON structure: {e}")
        
        return len(errors) == 0, errors
    
    def validate_snapshot(self, snapshot: Dict) -> Tuple[bool, List[str]]:
        """Validate complete snapshot structure."""
        errors = []
        
        # Required top-level keys
        required = ["snapshot_metadata", "agent_accomplishments", "project_metrics"]
        for key in required:
            if key not in snapshot:
                errors.append(f"Missing required snapshot key: {key}")
        
        return len(errors) == 0, errors
```

---

## 🔗 Integration with Existing Systems

### 1. Cycle Accomplishments System

**Relationship:** Cycle Snapshot extends Cycle Accomplishments

**Integration:**
- Reuse `data_collector.py` from cycle_accomplishments
- Reuse `blog_generator.py` for Victor voice
- Extend `main.py` to support snapshot mode

**Command:**
```bash
# Generate cycle accomplishments (existing)
python -m tools.cycle_accomplishments.main

# Generate cycle snapshot (new)
python -m tools.cycle_snapshots.main

# Generate both (combined)
python -m tools.cycle_snapshots.main --include-accomplishments
```

---

### 2. Agent Status Monitor System

**Relationship:** Cycle Snapshot uses unified status reading library

**Integration:**
- Use `src/core/agent_status/reader.py` (from consolidation)
- No direct integration with StatusChangeMonitor (separate concerns)
- Status reset happens AFTER snapshot generation

**Safety:**
- StatusChangeMonitor continues working during snapshot
- Snapshot reads status.json (no conflicts)
- Reset happens atomically (StatusChangeMonitor sees clean state)

---

### 3. MCP Servers

**Relationship:** Cycle Snapshot consumes MCP server data

**Integration:**
- Use MCP tools for data collection
- Graceful degradation if MCP unavailable
- Optional integrations (don't fail if MCP down)

**Pattern:**
```python
def collect_mcp_data_safely() -> Dict[str, Any]:
    """Collect MCP data with graceful degradation."""
    data = {}
    
    # Try each MCP server, continue on failure
    try:
        data['swarm_brain'] = collect_swarm_brain_data()
    except Exception as e:
        logger.warning(f"Swarm Brain unavailable: {e}")
        data['swarm_brain'] = {}
    
    try:
        data['task_manager'] = collect_task_manager_data()
    except Exception as e:
        logger.warning(f"Task Manager unavailable: {e}")
        data['task_manager'] = {}
    
    return data
```

---

## 📊 Data Flow Architecture

### Collection Phase

```
┌─────────────────┐
│  Agent Status   │──┐
│  (status.json)  │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │
│  MASTER_TASK_   │  │
│  LOG.md         │──┤
└─────────────────┘  │
                     ├──► Snapshot Aggregator
┌─────────────────┐  │
│  Git History    │  │
│  (commits)      │──┤
└─────────────────┘  │
                     │
┌─────────────────┐  │
│  MCP Servers   │──┤
│  (30+ systems) │  │
└─────────────────┘  │
                     │
┌─────────────────┐  │
│  Project Files  │──┘
│  (CHANGELOG,    │
│   captain log)  │
└─────────────────┘
```

### Processing Phase

```
Snapshot Aggregator
    │
    ├──► Generate Snapshot JSON
    ├──► Generate Markdown Report
    ├──► Generate Blog Post
    └──► Calculate Metrics
```

### Reset Phase

```
For Each Agent:
    │
    ├──► Backup status.json
    ├──► Archive completed items
    ├──► Generate reset status
    ├──► Validate reset status
    ├──► Atomic write
    └──► Verify final state
```

### Distribution Phase

```
Snapshot
    │
    ├──► Save to reports/
    ├──► Post to Discord
    ├──► Publish to WordPress
    ├──► Feed to Swarm Brain
    ├──► Store in Vector DB
    ├──► Update Task Log
    └──► Notify all systems
```

---

## 🎯 Implementation Phases

### Phase 1: Core Foundation (Agent-3)
**Duration:** 2-3 cycles  
**Risk:** LOW

**Modules:**
1. `data_collectors/agent_status_collector.py`
2. `data_collectors/task_log_collector.py`
3. `data_collectors/git_collector.py`
4. `aggregators/snapshot_aggregator.py`
5. `core/snapshot_models.py`
6. `main.py` (basic CLI)

**Deliverables:**
- Basic snapshot generation (agent status + task log + git)
- JSON snapshot output
- Markdown report generation
- Unit tests

**Safety:**
- No status reset yet (Phase 2)
- No Discord integration yet (Phase 3)
- Read-only operations

---

### Phase 2: Status Reset (Agent-3 + Agent-2 Review)
**Duration:** 2-3 cycles  
**Risk:** MEDIUM (touches status.json)

**Modules:**
1. `processors/status_resetter.py`
2. `core/snapshot_validator.py`
3. Backup system
4. Rollback mechanism

**Deliverables:**
- Safe status.json reset logic
- Backup system
- Validation system
- Rollback capability

**Safety:**
- Agent-2 reviews reset logic before implementation
- Agent-4 validates after implementation
- Extensive testing with one agent first

---

### Phase 3: MCP Integration (Agent-3)
**Duration:** 2-3 cycles  
**Risk:** LOW (additive)

**Modules:**
1. `data_collectors/mcp_collector.py`
2. Integration with 10+ MCP servers

**Deliverables:**
- MCP data collection
- Graceful degradation
- Error handling

---

### Phase 4: Distribution (Agent-3)
**Duration:** 2-3 cycles  
**Risk:** LOW (additive)

**Modules:**
1. `integrations/distribution_manager.py`
2. `integrations/discord_integration.py`
3. `integrations/blog_integration.py`
4. `integrations/swarm_brain_integration.py`

**Deliverables:**
- Multi-system distribution
- Discord posting
- Blog publishing
- Swarm Brain learning

---

### Phase 5: Advanced Features (Agent-3 + Agent-2)
**Duration:** 2-3 cycles  
**Risk:** LOW

**Modules:**
1. `processors/blog_generator.py`
2. `aggregators/insights_generator.py`
3. Historical tracking
4. Trend analysis

**Deliverables:**
- Victor-voiced blog posts
- AI insights
- Historical comparison
- Trend analysis

---

## 🔒 Safety Protocols

### Pre-Implementation
1. **Agent-2:** Review architecture design
2. **Agent-4:** Approve status reset approach
3. **Agent-3:** Confirm implementation plan

### During Implementation
1. **Agent-3:** Create feature branch
2. **Agent-3:** Test in isolation
3. **Agent-2:** Review code before merge
4. **Agent-4:** Validate Discord bot still works

### Post-Implementation
1. **Agent-4:** Test status reset with one agent
2. **Agent-4:** Validate status.json integrity
3. **Agent-2:** Architecture validation
4. **All:** Approve before production use

---

## 📋 Next Steps

1. **Agent-2:** Finalize architecture design (this document)
2. **Agent-3:** Review architecture, confirm approach
3. **Agent-2 + Agent-3:** Design status reset logic together
4. **Agent-3:** Begin Phase 1 implementation
5. **Agent-2:** Review Phase 1 code
6. **Agent-4:** Validate safety after Phase 1

---

**Status:** Architecture Design Complete  
**Ready for:** Agent-3 review and Phase 1 implementation  
**Safety:** All critical constraints addressed

