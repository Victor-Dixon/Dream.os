# Additional Activity Sources for Agent Activity Detection

## Overview
This document outlines additional activity sources that could be checked to improve agent activity detection accuracy beyond the current 7+ sources.

## Currently Checked Sources
1. ✅ ActivityEmitter telemetry events
2. ✅ status.json updates
3. ✅ File modifications in workspace
4. ✅ Devlog creation
5. ✅ Inbox message activity (sent/received)
6. ✅ Task claims (cycle planner)
7. ✅ Contract system activity
8. ✅ Git commits/push
9. ✅ Test runs (pytest cache, coverage)
10. ✅ Swarm Brain activity
11. ✅ Planning documents
12. ✅ Validation results
13. ✅ Evidence files
14. ✅ Message queue activity

## Proposed Additional Sources

### 1. Inbox Message Deletions/Archiving
**Location**: `agent_workspaces/{agent_id}/inbox/archive/`
**Detection Method**: 
- Check for files moved to archive subdirectory
- Monitor deletion timestamps
- Track archive directory modifications

**Implementation**:
```python
def _check_inbox_deletions(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[AgentActivity]:
    """Check inbox message deletions/archiving."""
    activities = []
    inbox_dir = self.workspace_root / agent_id / "inbox"
    archive_dir = inbox_dir / "archive"
    
    # Check archive directory for recently archived messages
    if archive_dir.exists():
        for archived_file in archive_dir.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(archived_file.stat().st_mtime)
                if mtime >= lookback_time:
                    activities.append(AgentActivity(
                        agent_id=agent_id,
                        source="inbox_archive",
                        timestamp=mtime,
                        action=f"Message archived: {archived_file.name}",
                        metadata={"file": archived_file.name, "type": "archive"}
                    ))
            except (OSError, PermissionError):
                continue
    
    # Check for deleted files (compare inbox contents with message history)
    # This would require maintaining a history of inbox contents
    return activities
```

**Confidence**: Medium (Tier 2) - Shows inbox management activity

---

### 2. Sent Messages to Other Agents
**Location**: 
- `data/message_history.json` (if exists)
- `runtime/agent_comms/activity_events.jsonl` (ActivityEmitter)
- Other agent inboxes: `agent_workspaces/{recipient}/inbox/`

**Detection Method**:
- Check message history files for sent messages
- Scan recipient agent inboxes for messages from this agent
- Parse ActivityEmitter events for message sending

**Implementation**:
```python
def _check_sent_messages(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[AgentActivity]:
    """Check messages sent to other agents."""
    activities = []
    
    # Method 1: Check message history file
    message_history = Path("data") / "message_history.json"
    if message_history.exists():
        try:
            with open(message_history, 'r', encoding='utf-8') as f:
                history = json.load(f)
                messages = history.get("messages", [])
                
                for msg in messages:
                    sender = msg.get("sender", "")
                    if sender.lower() == agent_id.lower():
                        timestamp_str = msg.get("timestamp", "")
                        try:
                            msg_time = datetime.fromisoformat(
                                timestamp_str.replace("Z", "+00:00")
                            ).replace(tzinfo=None)
                            if msg_time >= lookback_time:
                                recipient = msg.get("recipient", "unknown")
                                activities.append(AgentActivity(
                                    agent_id=agent_id,
                                    source="message_sent",
                                    timestamp=msg_time,
                                    action=f"Message sent to {recipient}",
                                    metadata={
                                        "recipient": recipient,
                                        "message_id": msg.get("message_id", "")
                                    }
                                ))
                        except Exception:
                            continue
        except Exception as e:
            logger.debug(f"Error reading message history: {e}")
    
    # Method 2: Check recipient agent inboxes
    for recipient_id in AGENTS:
        if recipient_id == agent_id:
            continue
        
        recipient_inbox = self.workspace_root / recipient_id / "inbox"
        if not recipient_inbox.exists():
            continue
        
        try:
            for msg_file in recipient_inbox.glob("*.md"):
                try:
                    with open(msg_file, 'r', encoding='utf-8') as f:
                        content = f.read(500)
                        if f"From: {agent_id}" in content:
                            mtime = datetime.fromtimestamp(msg_file.stat().st_mtime)
                            if mtime >= lookback_time:
                                activities.append(AgentActivity(
                                    agent_id=agent_id,
                                    source="message_sent",
                                    timestamp=mtime,
                                    action=f"Message sent to {recipient_id}",
                                    metadata={
                                        "recipient": recipient_id,
                                        "file": msg_file.name
                                    }
                                ))
                except Exception:
                    continue
        except Exception as e:
            logger.debug(f"Error checking recipient inbox: {e}")
    
    return activities
```

**Confidence**: High (Tier 1) - Direct communication activity

---

### 3. Project Scan Results
**Location**: 
- `agent_workspaces/{agent_id}/analyses/`
- `consolidation_logs/projectscanner_*.json`
- `docs/archive/consolidation/project_scan_analysis_report.json`

**Detection Method**:
- Check for project scan JSON files
- Monitor analysis directories
- Track project scanner output files

**Implementation**:
```python
def _check_project_scans(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[AgentActivity]:
    """Check project scan analysis files."""
    activities = []
    
    # Check agent workspace analyses directory
    analyses_dir = self.workspace_root / agent_id / "analyses"
    if analyses_dir.exists():
        for scan_file in analyses_dir.rglob("*.json"):
            try:
                mtime = datetime.fromtimestamp(scan_file.stat().st_mtime)
                if mtime >= lookback_time:
                    # Check if file contains project scan data
                    try:
                        with open(scan_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # Check for project scan indicators
                            if any(key in data for key in ["project_scan", "scanner", "analysis"]):
                                activities.append(AgentActivity(
                                    agent_id=agent_id,
                                    source="project_scan",
                                    timestamp=mtime,
                                    action=f"Project scan: {scan_file.name}",
                                    metadata={
                                        "file": str(scan_file.relative_to(analyses_dir)),
                                        "type": "project_analysis"
                                    }
                                ))
                    except Exception:
                        # Still count file modification
                        activities.append(AgentActivity(
                            agent_id=agent_id,
                            source="project_scan",
                            timestamp=mtime,
                            action=f"Analysis file modified: {scan_file.name}",
                            metadata={"file": scan_file.name}
                        ))
            except (OSError, PermissionError):
                continue
    
    # Check consolidation logs for project scanner activity
    consolidation_logs = Path("consolidation_logs")
    if consolidation_logs.exists():
        for log_file in consolidation_logs.glob("projectscanner_*.json"):
            try:
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime >= lookback_time:
                    # Check if agent ID is mentioned in log
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if agent_id.lower() in content.lower():
                                activities.append(AgentActivity(
                                    agent_id=agent_id,
                                    source="project_scan",
                                    timestamp=mtime,
                                    action=f"Project scanner log: {log_file.name}",
                                    metadata={"file": log_file.name, "type": "scanner_log"}
                                ))
                    except Exception:
                        pass
            except (OSError, PermissionError):
                continue
    
    return activities
```

**Confidence**: Medium (Tier 2) - Shows analysis/scanning activity

---

### 4. Status.json Content Changes (Beyond Timestamp)
**Location**: `agent_workspaces/{agent_id}/status.json`

**Detection Method**:
- Compare current status.json content with previous version
- Track changes to mission, tasks, achievements
- Monitor status field transitions

**Implementation**:
```python
def _check_status_content_changes(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[AgentActivity]:
    """Check status.json for meaningful content changes."""
    activities = []
    status_file = self.workspace_root / agent_id / "status.json"
    
    if not status_file.exists():
        return activities
    
    try:
        # Check file modification time
        mtime = datetime.fromtimestamp(status_file.stat().st_mtime)
        if mtime < lookback_time:
            return activities
        
        # Read current status
        with open(status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        # Check for meaningful content changes
        last_updated_str = status.get("last_updated", "")
        current_mission = status.get("current_mission", "")
        current_tasks = status.get("current_tasks", [])
        completed_tasks = status.get("completed_tasks", [])
        achievements = status.get("achievements", [])
        status_field = status.get("status", "")
        
        # Parse timestamp
        try:
            if 'T' in last_updated_str:
                last_updated = datetime.fromisoformat(
                    last_updated_str.replace("Z", "+00:00")
                ).replace(tzinfo=None)
            else:
                last_updated = datetime.strptime(
                    last_updated_str, "%Y-%m-%d %H:%M:%S"
                )
            
            if last_updated >= lookback_time:
                # Determine type of activity based on content
                if completed_tasks:
                    activities.append(AgentActivity(
                        agent_id=agent_id,
                        source="status_completion",
                        timestamp=last_updated,
                        action=f"Tasks completed: {len(completed_tasks)}",
                        metadata={
                            "completed_count": len(completed_tasks),
                            "tasks": completed_tasks[:3]  # First 3
                        }
                    ))
                
                if achievements:
                    activities.append(AgentActivity(
                        agent_id=agent_id,
                        source="status_achievement",
                        timestamp=last_updated,
                        action=f"Achievements: {len(achievements)}",
                        metadata={"achievements": achievements[:3]}
                    ))
                
                if current_mission and current_mission != "N/A":
                    activities.append(AgentActivity(
                        agent_id=agent_id,
                        source="status_mission",
                        timestamp=last_updated,
                        action=f"Mission: {current_mission[:50]}",
                        metadata={"mission": current_mission[:100]}
                    ))
                
                # Status field transitions (e.g., TASK_EXECUTION -> VALIDATION)
                if status_field:
                    activities.append(AgentActivity(
                        agent_id=agent_id,
                        source="status_transition",
                        timestamp=last_updated,
                        action=f"Status: {status_field}",
                        metadata={"status": status_field}
                    ))
        except Exception:
            # Fallback to file mtime
            activities.append(AgentActivity(
                agent_id=agent_id,
                source="status_update",
                timestamp=mtime,
                action="Status file modified",
                metadata={"file_mtime": True}
            ))
    except Exception as e:
        logger.debug(f"Error checking status content: {e}")
    
    return activities
```

**Confidence**: High (Tier 1) - Direct status updates with meaningful content

---

### 5. Devlog Content Analysis (Project Scans in Devlogs)
**Location**: `devlogs/`

**Detection Method**:
- Parse devlog content for project scan mentions
- Check for analysis reports embedded in devlogs
- Track devlog modifications (not just creation)

**Implementation**:
```python
def _check_devlog_content(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[AgentActivity]:
    """Check devlog content for project scans and analysis."""
    activities = []
    
    if not self.devlogs_dir.exists():
        return activities
    
    try:
        pattern = f"*{agent_id.lower()}*.md"
        for devlog_file in self.devlogs_dir.glob(pattern):
            try:
                mtime = datetime.fromtimestamp(devlog_file.stat().st_mtime)
                if mtime >= lookback_time:
                    # Read devlog content
                    try:
                        with open(devlog_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Check for project scan indicators
                        scan_keywords = [
                            "project scan", "projectscanner", "analysis report",
                            "codebase analysis", "repository scan"
                        ]
                        
                        if any(keyword.lower() in content.lower() for keyword in scan_keywords):
                            activities.append(AgentActivity(
                                agent_id=agent_id,
                                source="devlog_scan",
                                timestamp=mtime,
                                action=f"Devlog with project scan: {devlog_file.name}",
                                metadata={
                                    "file": devlog_file.name,
                                    "type": "project_scan_mention"
                                }
                            ))
                        
                        # Check for devlog modifications (not just creation)
                        # This indicates ongoing work
                        if mtime > lookback_time:
                            activities.append(AgentActivity(
                                agent_id=agent_id,
                                source="devlog_update",
                                timestamp=mtime,
                                action=f"Devlog updated: {devlog_file.name}",
                                metadata={"file": devlog_file.name, "type": "update"}
                            ))
                    except Exception:
                        # Still count file modification
                        activities.append(AgentActivity(
                            agent_id=agent_id,
                            source="devlog",
                            timestamp=mtime,
                            action=f"Devlog modified: {devlog_file.name}",
                            metadata={"file": devlog_file.name}
                        ))
            except (OSError, PermissionError):
                continue
    except Exception as e:
        logger.warning(f"Error checking devlog content for {agent_id}: {e}")
    
    return activities
```

**Confidence**: Medium (Tier 2) - Shows documentation/analysis activity

---

### 6. Message Queue Processing
**Location**: `data/message_queue.json`

**Detection Method**:
- Check for messages processed/removed from queue
- Track message queue modifications
- Monitor queue size changes

**Implementation**:
```python
def _check_message_queue_processing(
    self,
    agent_id: str,
    lookback_time: datetime
) -> List[AgentActivity]:
    """Check message queue for processed messages."""
    activities = []
    queue_file = Path("data") / "message_queue.json"
    
    if not queue_file.exists():
        return activities
    
    try:
        # Check file modification time
        mtime = datetime.fromtimestamp(queue_file.stat().st_mtime)
        if mtime >= lookback_time:
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)
            
            messages = queue_data.get("messages", [])
            
            # Check for messages for this agent that were processed
            for msg in messages:
                recipient = msg.get("recipient", "")
                if agent_id.lower() in recipient.lower():
                    timestamp_str = msg.get("timestamp", "")
                    status = msg.get("status", "")
                    
                    # Check if message was processed/read
                    if status in ["processed", "read", "acknowledged"]:
                        try:
                            msg_time = datetime.fromisoformat(
                                timestamp_str.replace("Z", "+00:00")
                            ).replace(tzinfo=None)
                            if msg_time >= lookback_time:
                                activities.append(AgentActivity(
                                    agent_id=agent_id,
                                    source="queue_processing",
                                    timestamp=msg_time,
                                    action=f"Message processed: {status}",
                                    metadata={
                                        "message_id": msg.get("message_id", ""),
                                        "status": status
                                    }
                                ))
                        except Exception:
                            continue
    except Exception as e:
        logger.debug(f"Error checking message queue: {e}")
    
    return activities
```

**Confidence**: Medium (Tier 2) - Shows message processing activity

---

## Implementation Priority

### High Priority (Immediate Value)
1. **Sent Messages to Other Agents** - Direct communication activity
2. **Status.json Content Changes** - Meaningful status updates
3. **Inbox Message Deletions/Archiving** - Inbox management activity

### Medium Priority (Nice to Have)
4. **Project Scan Results** - Analysis activity
5. **Devlog Content Analysis** - Documentation activity
6. **Message Queue Processing** - Queue management

## Integration Points

### Update `AgentActivityDetector.detect_agent_activity()`
Add new checks in the appropriate phase:
```python
# In detect_agent_activity method, add:
activities.extend(self._check_sent_messages(agent_id, lookback_time))
activities.extend(self._check_inbox_deletions(agent_id, lookback_time))
activities.extend(self._check_project_scans(agent_id, lookback_time))
activities.extend(self._check_status_content_changes(agent_id, lookback_time))
activities.extend(self._check_devlog_content(agent_id, lookback_time))
activities.extend(self._check_message_queue_processing(agent_id, lookback_time))
```

### Update `HardenedActivityDetector.assess_agent_activity()`
Add corresponding methods with confidence scoring:
```python
signals.extend(self._check_sent_messages_signals(agent_id, lookback_time))
signals.extend(self._check_status_content_signals(agent_id, lookback_time))
# etc.
```

## Testing Considerations

1. **Performance**: Some checks (like scanning all recipient inboxes) may be expensive
2. **False Positives**: Need to filter out automated/system messages
3. **Noise Filtering**: Archive operations might be automated, not agent activity
4. **Temporal Validation**: Ensure timestamps are within lookback window

## Notes

- Some sources may require maintaining state/history (e.g., inbox deletions)
- Consider caching results for expensive operations
- Balance detection accuracy with performance impact
- Some sources may overlap with existing checks (e.g., ActivityEmitter already tracks some message sends)

