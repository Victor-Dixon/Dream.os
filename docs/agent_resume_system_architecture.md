# Agent Resume System Architecture

## Overview

The agent resume system detects when agents have stalled and automatically sends recovery prompts to get them back to work. The system has been **hardened** with multi-source activity detection to prevent false positives (sending resume prompts to agents who are actively working).

## System Components

### 1. **Hardened Activity Detector** (`src/core/hardened_activity_detector.py`)

The core component that determines if an agent is actually active or truly stalled.

#### Key Features:
- **Multi-source validation**: Checks 8 different activity sources
- **Confidence scoring**: Assigns 0.0-1.0 confidence scores based on source reliability
- **Cross-validation**: Ensures signals are consistent and not stale
- **Noise filtering**: Excludes resume prompts and acknowledgments from activity signals

#### Activity Sources (Tiered by Reliability):

**Tier 1 (Most Reliable - 0.8-0.9 confidence):**
- `TELEMETRY_EVENT`: ActivityEmitter events (task completion, git push, validation)
- `GIT_COMMIT`: Git commits with agent name
- `CONTRACT_CLAIMED`: Contract system activity
- `TEST_EXECUTION`: Test runs (pytest cache, coverage files)

**Tier 2 (Reliable - 0.6-0.7 confidence):**
- `STATUS_UPDATE`: status.json with meaningful content
- `FILE_MODIFICATION`: Workspace file changes
- `DEVLOG_CREATED`: Devlog creation
- `INBOX_PROCESSING`: Inbox message processing

**Tier 3 (Less Reliable - 0.3-0.4 confidence):**
- `MESSAGE_QUEUE`: Message queue activity
- `WORKSPACE_ACCESS`: File access patterns

#### Detection Process:

```python
assessment = detector.assess_agent_activity(agent_id, lookback_minutes=60)
```

Returns `ActivityAssessment` with:
- `is_active`: Boolean indicating if agent is active
- `confidence`: 0.0-1.0 confidence score
- `last_activity`: Timestamp of most recent activity
- `inactivity_minutes`: Minutes since last activity
- `signals`: List of detected activity signals
- `validation_passed`: Whether signals passed cross-validation
- `reasons`: Human-readable reasons for the assessment

#### Confidence Calculation:

- **Multiple Tier-1 signals** → 0.9 (VERY_HIGH)
- **Single Tier-1 signal** → 0.7 (HIGH)
- **Multiple Tier-2 signals** → 0.7 (HIGH)
- **Single Tier-2 signal** → 0.5 (MEDIUM)
- **Tier-3 signals** → 0.3 (LOW)

Recency penalties:
- Activity >1 hour old: confidence × 0.7
- Activity >30 min old: confidence × 0.85

#### Validation Rules:

1. **Temporal consistency**: Signals must be within 24-hour window
2. **Recency check**: Most recent signal must be within lookback window
3. **Reliability requirement**: At least one Tier-1 or Tier-2 signal required

### 2. **Stall Resumer Guard** (`src/core/stall_resumer_guard.py`)

Validation gate that prevents false resume prompts.

#### Key Functions:

**`should_send_resume(agent_id, lookback_minutes=60)`**
- Uses hardened activity detector to check if agent is active
- Returns `(should_send: bool, reason: str)`
- **Prevents resume** if agent is active (confidence ≥ 0.5)
- **Allows resume** if agent is inactive or validation fails
- **Fail-safe design**: Fails open (allows resume) on errors

**`is_resumer_prompt(message)`**
- Detects if a message is a stall/recovery prompt
- Used to filter out resume prompts from activity signals

**`is_meaningful_progress(event)`**
- Determines if an event represents real work (not just acknowledgments)
- Used to gate inactivity resets

### 3. **Optimized Stall Resume Prompt Generator** (`src/core/optimized_stall_resume_prompt.py`)

Generates context-aware recovery prompts based on:
- FSM state (agent's current lifecycle state)
- Cycle Planner (next available tasks)
- Agent's last known mission/tasks
- Project priorities and goal alignment

#### Key Features:

- **Activity validation**: Checks if agent is active before generating prompt
- **Auto-task claiming**: Can automatically claim tasks from cycle planner
- **FSM-aware**: Provides state-specific recovery actions
- **Goal-aligned**: Aligns prompts with project priorities

#### Integration with Activity Detection:

```python
def generate_resume_prompt(
    agent_id: str,
    validate_activity: bool = True  # Default: validate before generating
) -> Optional[str]:
    if validate_activity:
        should_send, reason = should_send_resume(agent_id, lookback_minutes=60)
        if not should_send:
            logger.info(f"⏸️ Skipping resume prompt: {reason}")
            return None  # Don't generate prompt if agent is active
```

### 4. **Status Checker** (`tools/check_agent_statuses.py`)

Command-line tool used by Captain to check all agent statuses.

#### Enhanced Features:

- **Multi-source activity detection**: Uses hardened detector to verify activity
- **False positive prevention**: Doesn't escalate agents with recent activity
- **Confidence display**: Shows confidence scores and activity sources
- **Categorization**: Groups agents by staleness (fresh, warning, critical, auto-resume)

#### Usage:

```bash
# Check statuses with activity detection (default)
python tools/check_agent_statuses.py

# Disable activity detection (legacy mode)
python tools/check_agent_statuses.py --no-activity-check
```

#### Output Categories:

- **🟢 FRESH** (<2 hours): Recent status updates
- **🟡 WARNING** (2-6 hours): Stale but may have activity
- **🟠 CRITICAL** (6-12 hours): Needs resume soon
- **🔴 AUTO-RESUME** (>12 hours): Needs immediate resume

If activity is detected, agents are **not escalated** to higher categories even if status.json is stale.

### 5. **Resume Cycle Planner Integration** (`src/core/resume_cycle_planner_integration.py`)

Connects resume prompts with cycle planner to automatically assign tasks.

#### Features:

- **Auto-claim tasks**: Automatically claims tasks when agents resume
- **Task preview**: Shows available tasks without claiming
- **Contract system integration**: Uses ContractManager for task assignment

## System Flow

### Resume Prompt Generation Flow:

```
1. Status Monitor detects stale agent
   ↓
2. OptimizedStallResumePrompt.generate_resume_prompt()
   ↓
3. should_send_resume() validates activity
   ↓
4. HardenedActivityDetector.assess_agent_activity()
   ├─ Checks telemetry events
   ├─ Checks git activity
   ├─ Checks contract activity
   ├─ Checks test execution
   ├─ Checks status updates
   ├─ Checks file modifications
   ├─ Checks devlog activity
   └─ Checks inbox processing
   ↓
5. Filters noise (resume prompts, acknowledgments)
   ↓
6. Calculates confidence score
   ↓
7. Cross-validates signals
   ↓
8. Returns ActivityAssessment
   ↓
9. should_send_resume() decides:
   ├─ If active (confidence ≥ 0.5) → Skip resume
   └─ If inactive → Generate resume prompt
   ↓
10. Resume prompt generated with:
    ├─ FSM state-specific actions
    ├─ Next task from cycle planner (auto-claimed)
    ├─ Project priorities alignment
    └─ Agent-specific assignments
```

### Activity Detection Flow:

```
1. Collect signals from all sources
   ↓
2. Filter noise (resume prompts, acknowledgments)
   ↓
3. Sort by timestamp (most recent first)
   ↓
4. Calculate confidence:
   ├─ Group by tier (1, 2, 3)
   ├─ Apply tier-based confidence
   └─ Apply recency penalties
   ↓
5. Cross-validate:
   ├─ Check temporal consistency
   ├─ Check recency
   └─ Check reliability requirement
   ↓
6. Determine is_active:
   ├─ confidence ≥ 0.5
   ├─ validation_passed
   ├─ last_activity exists
   └─ last_activity within lookback window
```

## Configuration

### Hardened Activity Detector Settings:

```python
# Minimum confidence threshold
min_confidence_threshold = 0.5

# Time windows for activity validation
tier1_window_seconds = 3600  # 1 hour
tier2_window_seconds = 1800  # 30 min
tier3_window_seconds = 900   # 15 min

# Noise patterns to filter
noise_patterns = {
    "resumer", "stall-recovery", "no-acknowledgments",
    "inactivity detected", "[c2a]", "#no-reply", "#progress-only"
}
```

### Resume Prompt Settings:

```python
# Auto-claim tasks when resuming
auto_claim_tasks = True

# Validate activity before generating
validate_activity = True

# Lookback window for activity detection
lookback_minutes = 60
```

## Error Handling

### Fail-Safe Design:

The system is designed to **fail open** (allow resume) rather than fail closed (block resume):

1. **Import errors**: Falls back to allowing resume
2. **Detection errors**: Logs error but allows resume
3. **Validation failures**: Allows resume with warning
4. **Missing dependencies**: Falls back gracefully

This ensures that truly stalled agents still receive resume prompts even if detection fails.

## Logging

All components use structured logging:

- **INFO**: Normal operations (skipping resume, sending resume)
- **WARNING**: Validation failures, missing dependencies
- **ERROR**: Detection errors, unexpected failures
- **DEBUG**: Detailed signal information

## Performance Considerations

### Optimizations:

1. **Cached lookups**: Git log limited to last 200 lines
2. **Selective checks**: Only checks relevant sources
3. **Early exits**: Stops checking if high-confidence signal found
4. **Parallel processing**: Could be parallelized for multiple agents

### Time Complexity:

- **Telemetry check**: O(n) where n = recent events (capped at 200)
- **Git check**: O(n) where n = commits in lookback window
- **File system checks**: O(n) where n = files in workspace
- **Overall**: O(n) where n = number of signals to check

## Testing

### Manual Testing:

```bash
# Check agent statuses
python tools/check_agent_statuses.py

# Test activity detection for specific agent
python -c "
from src.core.hardened_activity_detector import HardenedActivityDetector
detector = HardenedActivityDetector()
assessment = detector.assess_agent_activity('Agent-7', lookback_minutes=60)
print(f'Active: {assessment.is_active}, Confidence: {assessment.confidence}')
print(f'Reasons: {assessment.reasons}')
"

# Test resume guard
python -c "
from src.core.stall_resumer_guard import should_send_resume
should_send, reason = should_send_resume('Agent-7', lookback_minutes=60)
print(f'Should send: {should_send}')
print(f'Reason: {reason}')
"
```

## Future Enhancements

### Potential Improvements:

1. **Adaptive timing**: Adjust lookback windows based on agent behavior
2. **Machine learning**: Learn from false positives/negatives
3. **Parallel detection**: Check multiple agents concurrently
4. **Real-time monitoring**: Stream activity events instead of polling
5. **Custom thresholds**: Per-agent confidence thresholds
6. **Activity patterns**: Detect work patterns (e.g., "Agent-7 works in bursts")

## Related Files

- `src/core/hardened_activity_detector.py` - Core activity detection
- `src/core/stall_resumer_guard.py` - Validation gate
- `src/core/optimized_stall_resume_prompt.py` - Prompt generator
- `src/core/resume_cycle_planner_integration.py` - Task assignment
- `tools/check_agent_statuses.py` - Status checker tool
- `src/discord_commander/status_change_monitor.py` - Status monitor integration

## Summary

The hardened agent resume system prevents false positives by:

1. **Multi-source validation**: Checks 8 different activity sources
2. **Confidence scoring**: Makes decisions based on signal strength
3. **Cross-validation**: Ensures signals are consistent
4. **Noise filtering**: Excludes resume prompts and acknowledgments
5. **Fail-safe design**: Fails open to prevent missed resumes

The system successfully prevents sending resume prompts to agents who are actively working, while still catching truly stalled agents.

