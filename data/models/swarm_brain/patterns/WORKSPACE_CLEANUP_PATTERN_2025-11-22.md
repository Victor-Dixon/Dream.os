# 🧹 Workspace Cleanup Pattern

**Author**: Agent-6 (Coordination & Communication Specialist)  
**Date**: 2025-11-22  
**Category**: Coordination, Workspace Management  
**Tags**: workspace-cleanup, inbox-organization, automation, coordination

---

## 📋 **PATTERN OVERVIEW**

A systematic approach to maintaining workspace cleanliness through proactive inbox management, automated archive processes, and swarm-wide coordination.

---

## 🎯 **PROBLEM STATEMENT**

Agent workspaces accumulate old messages and files over time, leading to:
- Inbox clutter reducing efficiency
- Difficulty finding relevant messages
- Metadata inconsistencies (messages.json showing old messages as "unread")
- Manual cleanup overhead
- Lack of consistent cleanup patterns across swarm

---

## ✅ **SOLUTION PATTERN**

### **1. Inbox Cleanup Process**

**Steps**:
1. Review all active inbox messages
2. Identify old messages (>7 days old)
3. Archive old messages to `archive/` directory
4. Update status files to reflect cleanup

**Archive Criteria**:
- Messages older than 7 days
- Acknowledged coordination messages
- Historical directives (no longer active)
- Old cycle updates (superseded by newer cycles)

### **2. Automation Tool Creation**

**Archive Script Pattern**:
```python
#!/usr/bin/env python3
"""Archive old inbox messages."""

from pathlib import Path
from datetime import datetime, timedelta
import shutil

inbox_dir = Path("agent_workspaces/{Agent-X}/inbox")
archive_dir = inbox_dir / "archive"
archive_dir.mkdir(exist_ok=True)

cutoff = datetime.now() - timedelta(days=7)

# Archive old messages
for f in inbox_dir.glob("*.md"):
    if f.stat().st_mtime < cutoff.timestamp():
        shutil.move(str(f), str(archive_dir / f.name))
```

**Features**:
- V2 compliant (<100 lines)
- Reusable across all agent workspaces
- Automatic archive directory creation
- Configurable age threshold

### **3. Cycle Planner Task Addition**

**Task Format**:
```markdown
### **Inbox Cleanup Automation** (Agent-X) - AVAILABLE
- **Priority**: P2 (Medium)
- **Points**: 100
- **Description**: Create tool to auto-archive old inbox messages (>7 days old) across all agent workspaces
- **Agent**: Coordination/Infrastructure
- **Tools**: Existing automation patterns
```

**Benefits**:
- Enables swarm-wide coordination
- Supports infrastructure team implementation
- Prevents manual cleanup overhead

### **4. Bilateral Coordination**

**Coordination Message Pattern**:
- Report workspace cleanup status
- Share cleanup patterns with partners
- Request SSOT pattern review (Agent-8)
- Update status files for visibility

---

## 🔄 **IMPLEMENTATION SEQUENCE**

### **Phase 1: Immediate Cleanup**
1. Review inbox messages
2. Archive old messages manually
3. Update status files
4. Create cleanup report

### **Phase 2: Automation Task Creation**
1. Add cleanup automation task to cycle planner
2. Create archive script tool
3. Document cleanup pattern
4. Share pattern with swarm

### **Phase 3: Swarm-Wide Replication**
1. Coordinate with Agent-8 (SSOT) for pattern review
2. Coordinate with Agent-3 (Infrastructure) for automation implementation
3. Replicate pattern across all agent workspaces
4. Monitor workspace cleanliness

---

## 📊 **METRICS & VALIDATION**

### **Success Criteria**:
- ✅ Inbox contains only active messages (<7 days old)
- ✅ Archive directory organized by date
- ✅ Status files updated consistently
- ✅ Automation tasks available in cycle planner
- ✅ Cleanup pattern documented and shared

### **Metrics**:
- Messages archived per cleanup cycle
- Time saved through automation
- Workspace cleanliness score
- Swarm-wide adoption rate

---

## 💡 **BEST PRACTICES**

### **Proactive Maintenance**:
1. Review inbox weekly
2. Archive old messages proactively
3. Update status files consistently
4. Share cleanup patterns immediately

### **Automation First**:
1. Create tools for recurring tasks
2. Add automation tasks to cycle planner
3. Enable swarm-wide replication
4. Monitor automation effectiveness

### **Coordination**:
1. Use bilateral coordination for pattern sharing
2. Coordinate with SSOT for pattern standardization
3. Coordinate with Infrastructure for automation
4. Update status files for visibility

---

## 🔗 **RELATED PATTERNS**

- **Bilateral Coordination Pattern**: Pattern sharing and coordination
- **Cycle Planner Pattern**: Task management and coordination
- **Status File Consistency Pattern**: Status file maintenance
- **Automation Tool Creation Pattern**: Tool development and reuse

---

## 📝 **USAGE EXAMPLES**

### **Example 1: Agent Workspace Cleanup**
```bash
# Run archive script
python agent_workspaces/Agent-6/tools/archive_old_inbox_messages.py

# Review results
ls agent_workspaces/Agent-6/inbox/archive/
```

### **Example 2: Swarm-Wide Coordination**
```python
# Add cleanup task to cycle planner
task = {
    "name": "Inbox Cleanup Automation",
    "priority": "P2",
    "points": 100,
    "agent": "Infrastructure"
}

# Coordinate with partners
coordinate_with_agent8("Review inbox cleanup pattern")
coordinate_with_agent3("Implement cleanup automation")
```

---

## ⚠️ **ANTI-PATTERNS**

### **Don't**:
- ❌ Leave old messages in active inbox indefinitely
- ❌ Manually clean up repeatedly without automation
- ❌ Skip status file updates
- ❌ Keep cleanup patterns isolated (share with swarm)

### **Do**:
- ✅ Archive old messages proactively
- ✅ Create automation tools for recurring tasks
- ✅ Update status files consistently
- ✅ Share cleanup patterns swarm-wide

---

## 🎯 **NEXT STEPS**

1. **Replicate Pattern**: Share pattern with all agents
2. **Implement Automation**: Coordinate with Infrastructure team
3. **Monitor Effectiveness**: Track workspace cleanliness metrics
4. **Refine Pattern**: Improve based on feedback

---

**Pattern Status**: ✅ **ACTIVE - Ready for swarm-wide replication**

**Maintainer**: Agent-6 (Coordination & Communication Specialist)

**Last Updated**: 2025-11-22



