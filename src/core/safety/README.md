# Safety Foundation Module - AGI Phase 0

**Status:** ✅ Implemented
**Version:** 1.0.0
**Date:** 2025-12-28

<!-- SSOT Domain: safety -->

SSOT TOOL METADATA
Purpose: Comprehensive documentation for AGI Phase 0 safety foundation
Description: Complete guide to safety components including sandbox, kill switch, blast radius limiter, audit trail, and state snapshots
Usage: Reference for implementing autonomous operations with safety checks
Date: 2025-12-30
Tags: safety, agi, documentation, autonomous, security

---

## Overview

The Safety Foundation provides critical infrastructure for autonomous operations, ensuring that the Swarm can operate safely without human supervision.

### Components

1. **Safety Sandbox (AGI-17)** - Isolated execution environment
2. **Kill Switch (AGI-18)** - Emergency stop mechanism
3. **Blast Radius Limiter (AGI-19)** - Damage control limits
4. **Audit Trail (AGI-20)** - Decision logging system
5. **State Snapshots (AGI-26)** - Rollback capability

---

## Quick Start

### Installation

```python
from src.core.safety import (
    SafetySandbox,
    get_kill_switch,
    get_blast_radius_limiter,
    get_audit_trail,
    get_snapshot_manager
)
```

### Basic Usage

```python
# Initialize safety components
sandbox = SafetySandbox()
kill_switch = get_kill_switch()
limiter = get_blast_radius_limiter()
audit = get_audit_trail()
snapshots = get_snapshot_manager()

# Execute autonomous code safely
result = sandbox.execute_code(
    code="print('Hello, World!')",
    language="python"
)

# Check blast radius limits
limiter.check_limit(
    resource_type=ResourceType.COST,
    requested_amount=50.0,
    action_id="test_action"
)

# Log autonomous decision
audit.log_decision(
    agent_id="Agent-4",
    agent_name="Captain",
    decision_summary="Deploy new feature",
    decision_rationale="High user demand and low risk",
    options_considered=["Deploy", "Wait", "Test more"],
    chosen_option="Deploy",
    confidence_score=0.85,
    risk_level="medium"
)

# Create state snapshot
snapshot_id = snapshots.create_snapshot(
    description="Before autonomous deployment"
)

# Trigger kill switch if needed
kill_switch.trigger(
    triggered_by="Human",
    trigger_channel="discord",
    reason="Testing emergency stop"
)
```

---

## Component Details

### 1. Safety Sandbox (AGI-17)

**Purpose:** Execute autonomous code in isolated environment

**Features:**
- Docker-based process isolation
- File system access restrictions
- Network access control
- Resource limits (CPU, memory, disk)
- Execution timeout enforcement

**Usage:**

```python
from src.core.safety import SafetySandbox, SandboxConfig

# Configure sandbox
config = SandboxConfig(
    mode=SandboxMode.DOCKER,
    timeout_seconds=300,
    max_cpu_percent=50,
    max_memory_mb=512,
    allow_network=False
)

sandbox = SafetySandbox(config)

# Execute code
result = sandbox.execute_code(
    code="""
import requests
print("Testing API call")
""",
    language="python",
    execution_id="test_001"
)

print(f"Success: {result.success}")
print(f"Output: {result.stdout}")
print(f"Execution time: {result.execution_time_seconds}s")
```

**Safety Checks:**
- Blocks dangerous patterns (rm -rf, eval, exec)
- Validates file access permissions
- Enforces resource limits
- Logs all operations

---

### 2. Kill Switch (AGI-18)

**Purpose:** Emergency stop for autonomous operations

**Features:**
- < 5 second response time
- Multiple trigger channels (Discord, API, CLI, signal)
- Graceful vs. immediate shutdown
- State preservation
- Automatic rollback trigger

**Usage:**

```python
from src.core.safety import get_kill_switch

kill_switch = get_kill_switch()

# Register callback for shutdown events
def on_shutdown(event_type):
    print(f"Shutdown event: {event_type}")
    # Cleanup resources
    
kill_switch.register_callback(on_shutdown)

# Register active operation
kill_switch.register_operation(
    operation_id="deploy_001",
    operation_data={"task": "Deploy feature X"}
)

# Check if system is operational
if kill_switch.is_operational():
    # Proceed with autonomous operation
    pass

# Trigger emergency stop
kill_switch.trigger(
    triggered_by="Agent-4",
    trigger_channel="api",
    reason="Budget limit exceeded",
    graceful=True  # Allow in-progress tasks to complete
)

# Check status
status = kill_switch.get_status()
print(f"State: {status['state']}")
print(f"Active operations: {status['active_operations']}")
```

**Trigger Channels:**
1. **Discord:** `/kill-autonomous` command
2. **API:** `POST /api/killswitch` endpoint
3. **CLI:** `python -m src.core.safety.cli kill-switch --trigger`
4. **Signal:** SIGTERM or SIGINT

---

### 3. Blast Radius Limiter (AGI-19)

**Purpose:** Limit damage from any single autonomous action

**Features:**
- Cost limits ($100 per action)
- File modification limits (10 files per action)
- API call limits (1000 calls per action)
- Time-based rolling windows (hourly, daily)
- Warning thresholds (80% of limit)

**Usage:**

```python
from src.core.safety import get_blast_radius_limiter, ResourceType

limiter = get_blast_radius_limiter()

# Check limit before action
try:
    limiter.check_limit(
        resource_type=ResourceType.COST,
        requested_amount=75.0,  # $75
        action_id="expensive_operation"
    )
    
    # Proceed with operation
    perform_expensive_operation()
    
    # Record actual usage
    limiter.record_usage(
        resource_type=ResourceType.COST,
        amount=72.50,
        action_id="expensive_operation"
    )

except BlastRadiusViolation as e:
    print(f"Blast radius limit exceeded: {e}")
    # Escalate to human or skip operation

# Get usage report
report = limiter.get_usage_report()
print(f"Cost usage: {report['cost']['usage']['hourly']:.2f} / {report['cost']['limits']['per_hour']:.2f}")
```

**Default Limits:**

| Resource | Per Action | Per Hour | Per Day |
|----------|-----------|----------|---------|
| Cost | $100 | $500 | $2,000 |
| Files | 10 | 50 | 200 |
| API Calls | 1,000 | 5,000 | 20,000 |
| DB Writes | 100 | 500 | 2,000 |

---

### 4. Audit Trail (AGI-20)

**Purpose:** Immutable logging of all autonomous decisions

**Features:**
- Append-only logging (cannot modify past events)
- Structured JSON format
- Decision reasoning capture
- Outcome tracking
- Hash chain integrity verification
- 90-day retention

**Usage:**

```python
from src.core.safety import get_audit_trail, EventType

audit = get_audit_trail()

# Log autonomous decision
event_id = audit.log_decision(
    agent_id="Agent-7",
    agent_name="Web Development Specialist",
    decision_summary="Deploy website update",
    decision_rationale="A/B test shows 15% conversion improvement",
    options_considered=[
        "Deploy immediately",
        "Wait for more data",
        "Deploy to 10% of users first"
    ],
    chosen_option="Deploy to 10% of users first",
    confidence_score=0.90,
    risk_level="low",
    estimated_cost=5.0,
    context={
        "ab_test_results": {"conversion_lift": 0.15, "p_value": 0.01},
        "deployment_strategy": "canary"
    }
)

# Execute operation
result = deploy_website_update()

# Update outcome
audit.update_outcome(
    event_id=event_id,
    outcome="Successfully deployed to 10% of users",
    success=True,
    actual_cost=4.75
)

# Query audit history
recent_decisions = audit.query_events(
    agent_id="Agent-7",
    event_type=EventType.DECISION,
    limit=10
)

# Verify integrity
is_valid = audit.verify_integrity()
print(f"Audit trail integrity: {'✅' if is_valid else '❌'}")
```

**Event Types:**
- `DECISION` - Autonomous decision made
- `ACTION` - Action executed
- `ESCALATION` - Escalated to human
- `APPROVAL` - Human approval received
- `REJECTION` - Human rejection received
- `ERROR` - Error occurred
- `ROLLBACK` - Action rolled back

---

### 5. State Snapshots (AGI-26)

**Purpose:** Enable fast rollback (< 5 minutes)

**Features:**
- Hourly automated snapshots
- Database state capture
- File system state capture
- Configuration state capture
- Compression to save space
- 7-day retention

**Usage:**

```python
from src.core.safety import get_snapshot_manager

snapshots = get_snapshot_manager()

# Create manual snapshot
snapshot_id = snapshots.create_snapshot(
    description="Before risky autonomous operation",
    tags={"operation": "database_migration", "agent": "Agent-8"}
)

# Execute risky operation
try:
    perform_risky_operation()
except Exception as e:
    print(f"Operation failed: {e}")
    
    # Restore from snapshot
    success = snapshots.restore_snapshot(snapshot_id)
    if success:
        print("✅ System restored from snapshot")
    else:
        print("❌ Restore failed - manual intervention required")

# List available snapshots
all_snapshots = snapshots.list_snapshots()
for snapshot in all_snapshots:
    print(f"{snapshot['snapshot_id']}: {snapshot['timestamp']}")
    print(f"  Size: {snapshot['size_bytes'] / (1024*1024):.1f} MB")
    print(f"  Components: {', '.join(snapshot['components'].keys())}")

# Get latest snapshot
latest = snapshots.get_latest_snapshot()
print(f"Latest snapshot: {latest.snapshot_id} ({latest.timestamp})")
```

**What Gets Snapshotted:**
- SQLite database (`/workspace/swarm.db`)
- Configuration files (`/workspace/config`)
- Agent workspaces (`/workspace/agent_workspaces`)
- Kill switch state (`.killswitch_state`)

---

## CLI Tool

A command-line interface is provided for managing safety components:

```bash
# Check safety status
python -m src.core.safety.cli status

# Trigger kill switch
python -m src.core.safety.cli kill-switch --trigger --reason "Testing"

# Create snapshot
python -m src.core.safety.cli snapshot --create --description "Manual backup"

# Restore snapshot
python -m src.core.safety.cli snapshot --restore snapshot_1735430400

# Check blast radius usage
python -m src.core.safety.cli blast-radius --report

# Query audit trail
python -m src.core.safety.cli audit --query --agent Agent-7 --limit 20

# Verify audit integrity
python -m src.core.safety.cli audit --verify
```

---

## Integration with Autonomous Operations

### Required Pattern

All autonomous operations MUST follow this pattern:

```python
from src.core.safety import (
    get_kill_switch,
    get_blast_radius_limiter,
    get_audit_trail,
    get_snapshot_manager,
    SafetySandbox
)

def autonomous_operation(task):
    """Example autonomous operation with safety checks."""
    
    # 1. Check kill switch
    kill_switch = get_kill_switch()
    if not kill_switch.is_operational():
        raise RuntimeError("Kill switch triggered - aborting operation")
    
    # 2. Register operation
    operation_id = f"op_{int(time.time())}"
    kill_switch.register_operation(operation_id, {"task": task})
    
    # 3. Check blast radius limits
    limiter = get_blast_radius_limiter()
    try:
        limiter.check_limit(
            resource_type=ResourceType.COST,
            requested_amount=estimated_cost,
            action_id=operation_id
        )
    except BlastRadiusViolation:
        kill_switch.unregister_operation(operation_id)
        raise
    
    # 4. Log decision
    audit = get_audit_trail()
    event_id = audit.log_decision(
        agent_id=agent_id,
        agent_name=agent_name,
        decision_summary=f"Execute {task}",
        decision_rationale=rationale,
        options_considered=options,
        chosen_option=chosen,
        confidence_score=confidence,
        risk_level=risk
    )
    
    # 5. Create snapshot if high-risk
    snapshots = get_snapshot_manager()
    snapshot_id = None
    if risk_level == "high":
        snapshot_id = snapshots.create_snapshot(
            description=f"Before {task}"
        )
    
    # 6. Execute in sandbox if code execution
    try:
        if requires_code_execution:
            sandbox = SafetySandbox()
            result = sandbox.execute_code(code, language)
        else:
            result = execute_task(task)
        
        # 7. Record usage
        limiter.record_usage(
            resource_type=ResourceType.COST,
            amount=actual_cost,
            action_id=operation_id
        )
        
        # 8. Update audit outcome
        audit.update_outcome(
            event_id=event_id,
            outcome="Success",
            success=True,
            actual_cost=actual_cost
        )
        
        # 9. Unregister operation
        kill_switch.unregister_operation(operation_id)
        
        return result
    
    except Exception as e:
        # Rollback if snapshot exists
        if snapshot_id:
            snapshots.restore_snapshot(snapshot_id)
        
        # Update audit
        audit.update_outcome(
            event_id=event_id,
            outcome=f"Failed: {str(e)}",
            success=False
        )
        
        kill_switch.unregister_operation(operation_id)
        raise
```

---

## Testing

### Unit Tests

```bash
# Run all safety tests
pytest tests/test_safety/

# Run specific component tests
pytest tests/test_safety/test_sandbox.py
pytest tests/test_safety/test_kill_switch.py
pytest tests/test_safety/test_blast_radius.py
pytest tests/test_safety/test_audit_trail.py
pytest tests/test_safety/test_snapshots.py
```

### Integration Tests

```bash
# Test full safety workflow
pytest tests/test_safety/test_integration.py

# Test autonomous operation with all safety checks
pytest tests/test_safety/test_autonomous_operation.py
```

---

## Performance

### Benchmarks

| Component | Operation | Time | Notes |
|-----------|-----------|------|-------|
| Sandbox | Execute Python code | ~100ms | Docker overhead |
| Kill Switch | Trigger | < 5s | Guaranteed |
| Blast Radius | Check limit | ~1ms | In-memory check |
| Audit Trail | Log decision | ~5ms | Append-only write |
| Snapshots | Create snapshot | ~30s | Depends on data size |
| Snapshots | Restore snapshot | < 5min | Target met |

---

## Monitoring

### Metrics to Track

1. **Kill Switch:**
   - Trigger count
   - Active operations count
   - Time to shutdown

2. **Blast Radius:**
   - Resource utilization (%)
   - Violations per day
   - Near-limit warnings

3. **Audit Trail:**
   - Events logged per hour
   - Integrity check results
   - Storage size

4. **Snapshots:**
   - Snapshot frequency
   - Restore success rate
   - Storage usage

---

## Troubleshooting

### Kill Switch Won't Trigger

1. Check if disarmed: `kill_switch.is_armed()`
2. Verify state file: `cat /workspace/.killswitch_state`
3. Check logs: `tail -f /var/log/safety_*.log`

### Blast Radius False Positives

1. Review limits: `limiter.get_usage_report()`
2. Adjust limits if appropriate
3. Check enforcement mode: `limiter.limits[ResourceType.COST].enforcement_mode`

### Audit Trail Integrity Failed

1. Run verification: `audit.verify_integrity()`
2. Check for file corruption
3. Review recent events: `audit.query_events(limit=100)`

### Snapshot Restore Failed

1. Verify snapshot exists: `snapshots.list_snapshots()`
2. Check disk space
3. Review logs for errors
4. Manual restore: Extract tarball and copy files

---

## Security Considerations

### Threat Model

**Threats Addressed:**
- Runaway autonomous operations
- Budget exhaustion
- Data deletion
- Unauthorized access
- Configuration tampering

**Threats NOT Addressed:**
- Malicious insider with root access
- Physical security
- Network-level attacks
- Supply chain attacks

### Security Best Practices

1. **Secrets Management:** Use environment variables or secrets manager
2. **File Permissions:** Restrict access to audit logs and snapshots
3. **Network Isolation:** Run sandbox in isolated network
4. **Regular Audits:** Review audit trail weekly
5. **Backup Strategy:** Offsite backup of snapshots

---

## Roadmap

### Phase 0 (Complete)
- [x] Safety Sandbox (AGI-17)
- [x] Kill Switch (AGI-18)
- [x] Blast Radius Limiter (AGI-19)
- [x] Audit Trail (AGI-20)
- [x] State Snapshots (AGI-26)

### Phase 0.5 (Next)
- [ ] Decision Validation Engine (AGI-22)
- [ ] Human Escalation Triggers (AGI-28)
- [ ] Real-Time Dashboard (AGI-34)
- [ ] Anomaly Detection (AGI-37)

### Phase 1 (Future)
- [ ] Integrate with swarm_daemon.py (AGI-01)
- [ ] Automated testing suite
- [ ] Performance optimizations
- [ ] Multi-node support

---

## License

MIT License - See LICENSE file for details.

---

## Support

- **Issues:** https://github.com/yourusername/yourrepo/issues
- **Discord:** #safety-foundation channel
- **Captain:** Agent-4 (Strategic Oversight)

---

**Safety First. Autonomy Second.**  
🐝 WE. ARE. SWARM. ⚡🔥
