# Hardened Agent Resume System

**Date**: 2025-01-27  
**Author**: Agent-1 (Integration & Core Systems Specialist)  
**Priority**: CRITICAL - Prevents false resume prompts to active agents

## Overview

The agent resume system has been hardened to better detect when agents are active, preventing false positives that would send unnecessary resume prompts to agents who are already working.

## Key Improvements

### 1. Multi-Source Activity Detection

**File**: `src/core/hardened_activity_detector.py`

- **Tier 1 Sources** (Most Reliable):
  - Telemetry events (ActivityEmitter)
  - Git commits with agent name
  - Contract system activity
  - Test execution (pytest, coverage)

- **Tier 2 Sources** (Reliable):
  - Status.json updates with meaningful content
  - File modifications in workspace
  - Devlog creation
  - Inbox message processing

- **Tier 3 Sources** (Less Reliable):
  - Message queue activity
  - Workspace access patterns

### 2. Confidence Scoring System

Each activity signal is assigned a confidence score (0.0-1.0) based on:
- Source tier (Tier 1 = 0.85-0.9, Tier 2 = 0.6-0.7, Tier 3 = 0.3-0.4)
- Signal recency (older signals get penalty)
- Multiple signals boost confidence
- Cross-validation between sources

**Confidence Levels**:
- `VERY_HIGH` (0.9): Multiple tier-1 signals
- `HIGH` (0.7): Single tier-1 or multiple tier-2
- `MEDIUM` (0.5): Single tier-2
- `LOW` (0.3): Tier-3 signals
- `VERY_LOW` (0.1): Unreliable signals

### 3. Noise Filtering

**File**: `src/core/stall_resumer_guard.py`

Enhanced filtering to exclude:
- Resume prompts themselves
- Acknowledgments ("ack", "got it", "copy")
- Stall recovery markers
- Control messages

### 4. Validation Gate

**New Function**: `should_send_resume(agent_id, lookback_minutes)`

Before sending a resume prompt, the system:
1. Assesses agent activity using hardened detector
2. Checks confidence score (minimum 0.5)
3. Validates signal consistency
4. Returns `(should_send: bool, reason: str)`

**Result**: Resume prompts are only sent when:
- Agent is actually inactive (confidence < 0.5)
- OR validation failed but system allows (fail-open for safety)

### 5. Integration Points

#### Resume Prompt Generator
**File**: `src/core/optimized_stall_resume_prompt.py`

- Added `validate_activity` parameter (default: True)
- Returns `None` if agent is active (prevents prompt generation)
- Logs reason when skipping resume

#### Status Checker
**File**: `tools/check_agent_statuses.py`

- Uses hardened detector when available
- Falls back to legacy detector if needed
- Shows confidence scores and activity sources
- Prevents false escalation when activity detected

## Usage Examples

### Check if Agent Should Receive Resume

```python
from src.core.stall_resumer_guard import should_send_resume

should_send, reason = should_send_resume("Agent-7", lookback_minutes=60)
if should_send:
    print(f"Sending resume: {reason}")
else:
    print(f"Skipping resume: {reason}")
```

### Assess Agent Activity Directly

```python
from src.core.hardened_activity_detector import HardenedActivityDetector

detector = HardenedActivityDetector()
assessment = detector.assess_agent_activity("Agent-7", lookback_minutes=60)

print(f"Active: {assessment.is_active}")
print(f"Confidence: {assessment.confidence:.2f}")
print(f"Last Activity: {assessment.last_activity}")
print(f"Reasons: {', '.join(assessment.reasons)}")
```

### Generate Resume Prompt (with validation)

```python
from src.core.optimized_stall_resume_prompt import OptimizedStallResumePrompt

prompt_gen = OptimizedStallResumePrompt()
prompt = prompt_gen.generate_resume_prompt(
    "Agent-7",
    validate_activity=True  # Will return None if agent is active
)

if prompt:
    # Send prompt
    pass
else:
    # Agent is active, skip resume
    pass
```

## Benefits

1. **Reduced False Positives**: Agents actively working won't receive unnecessary resume prompts
2. **Better Accuracy**: Multi-source validation provides more reliable activity detection
3. **Confidence Scoring**: System can make informed decisions about agent state
4. **Noise Filtering**: Excludes resume prompts and acknowledgments from activity signals
5. **Fail-Safe Design**: System fails open (allows resume) if detection fails

## Configuration

### Minimum Confidence Threshold

Default: `0.5` (configurable in `HardenedActivityDetector`)

```python
detector = HardenedActivityDetector()
detector.min_confidence_threshold = 0.6  # Stricter threshold
```

### Time Windows

- Tier 1 sources: 1 hour window
- Tier 2 sources: 30 minute window
- Tier 3 sources: 15 minute window

## Monitoring

The system logs all decisions:

- `⏸️ Skipping resume`: Agent is active, resume not sent
- `✅ Sending resume`: Agent is inactive, resume will be sent
- `⚠️ Resume validation failed`: Signals inconsistent but resume allowed

## Future Enhancements

1. **Machine Learning**: Train model on historical activity patterns
2. **Adaptive Thresholds**: Adjust confidence thresholds based on agent behavior
3. **Real-time Monitoring**: Continuous activity tracking instead of periodic checks
4. **Agent-Specific Rules**: Custom detection rules per agent specialization

## Testing

Run status checker with hardened detection:

```bash
python tools/check_agent_statuses.py
```

Disable activity detection (legacy mode):

```bash
python tools/check_agent_statuses.py --no-activity-check
```

## Related Files

- `src/core/hardened_activity_detector.py` - Core detection logic
- `src/core/stall_resumer_guard.py` - Validation gate
- `src/core/optimized_stall_resume_prompt.py` - Resume prompt generator
- `tools/check_agent_statuses.py` - Status checker with integration
- `src/orchestrators/overnight/enhanced_agent_activity_detector.py` - Legacy detector (still used as fallback)

