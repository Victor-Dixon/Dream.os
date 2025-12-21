# Agent Resume System - Quick Reference

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│              Agent Resume System Architecture               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. Status Monitor / Captain                                │
│     - Detects stale agents (status.json > threshold)        │
│     - Triggers resume prompt generation                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  2. OptimizedStallResumePrompt                              │
│     - Generates context-aware recovery prompts              │
│     - Integrates with FSM, Cycle Planner, Project Goals     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  3. should_send_resume() [Guard]                            │
│     - Validates agent activity BEFORE generating prompt     │
│     - Prevents false positives                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  4. HardenedActivityDetector                                │
│     - Multi-source activity detection                       │
│     - Confidence scoring (0.0-1.0)                          │
│     - Cross-validation                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│ Tier 1    │  │ Tier 2    │  │ Tier 3    │
│ Sources   │  │ Sources   │  │ Sources   │
│           │  │           │  │           │
│ • Telemetry│  │ • Status  │  │ • Message │
│ • Git     │  │ • Files   │  │   Queue   │
│ • Contracts│  │ • Devlogs │  │ • Access  │
│ • Tests   │  │ • Inbox   │  │   Patterns│
└───────────┘  └───────────┘  └───────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  5. ActivityAssessment                                      │
│     - is_active: bool                                       │
│     - confidence: float (0.0-1.0)                            │
│     - last_activity: datetime                              │
│     - signals: List[ActivitySignal]                        │
│     - validation_passed: bool                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌──────────────┐            ┌──────────────┐
│ Agent ACTIVE │            │ Agent INACTIVE│
│ (confidence  │            │ (confidence   │
│  ≥ 0.5)      │            │  < 0.5)      │
│              │            │              │
│ SKIP RESUME  │            │ GENERATE     │
│              │            │ RESUME       │
└──────────────┘            └──────────────┘
```

## Decision Flow

```
START: Agent appears stalled (status.json stale)
  │
  ├─→ Check activity with HardenedActivityDetector
  │   │
  │   ├─→ Collect signals from 8 sources
  │   │   ├─ Tier 1: Telemetry, Git, Contracts, Tests
  │   │   ├─ Tier 2: Status, Files, Devlogs, Inbox
  │   │   └─ Tier 3: Message Queue, Access Patterns
  │   │
  │   ├─→ Filter noise (resume prompts, acknowledgments)
  │   │
  │   ├─→ Calculate confidence:
  │   │   ├─ Multiple Tier-1 → 0.9 (VERY_HIGH)
  │   │   ├─ Single Tier-1 → 0.7 (HIGH)
  │   │   ├─ Multiple Tier-2 → 0.7 (HIGH)
  │   │   ├─ Single Tier-2 → 0.5 (MEDIUM)
  │   │   └─ Tier-3 → 0.3 (LOW)
  │   │
  │   ├─→ Apply recency penalties:
  │   │   ├─ >1 hour old → × 0.7
  │   │   └─ >30 min old → × 0.85
  │   │
  │   └─→ Cross-validate:
  │       ├─ Temporal consistency (within 24h window)
  │       ├─ Recency (within lookback window)
  │       └─ Reliability (at least Tier-1 or Tier-2 signal)
  │
  ├─→ Decision:
  │   │
  │   ├─→ If confidence ≥ 0.5 AND validation passed:
  │   │   └─→ Agent is ACTIVE → SKIP RESUME
  │   │
  │   └─→ If confidence < 0.5 OR validation failed:
  │       └─→ Agent is INACTIVE → GENERATE RESUME PROMPT
  │           │
  │           ├─→ Get FSM state from status.json
  │           ├─→ Get next task from Cycle Planner
  │           ├─→ Load agent assignments
  │           ├─→ Build context-aware prompt
  │           └─→ Send to agent
  │
  END
```

## Activity Sources (Tiered)

### Tier 1: Most Reliable (0.8-0.9 confidence)
- **TELEMETRY_EVENT**: ActivityEmitter events
  - Task completion, git push, validation pass
  - Confidence: 0.9 (tier-1 events), 0.72 (tier-2 events), 0.54 (other)
- **GIT_COMMIT**: Git commits with agent name
  - Confidence: 0.85
- **CONTRACT_CLAIMED**: Contract system activity
  - Confidence: 0.85
- **TEST_EXECUTION**: Test runs (pytest cache, coverage)
  - Confidence: 0.8 (pytest), 0.72 (coverage)

### Tier 2: Reliable (0.6-0.7 confidence)
- **STATUS_UPDATE**: status.json with meaningful content
  - Confidence: 0.7 (with content), 0.49 (file mtime only)
- **FILE_MODIFICATION**: Workspace file changes
  - Confidence: 0.65
- **DEVLOG_CREATED**: Devlog creation
  - Confidence: 0.7
- **INBOX_PROCESSING**: Inbox message processing
  - Confidence: 0.6

### Tier 3: Less Reliable (0.3-0.4 confidence)
- **MESSAGE_QUEUE**: Message queue activity
  - Confidence: 0.4
- **WORKSPACE_ACCESS**: File access patterns
  - Confidence: 0.3

## Confidence Thresholds

```
Confidence Score → Decision
─────────────────────────────────
0.9 - 1.0  → VERY_HIGH → Active (definitely)
0.7 - 0.89 → HIGH      → Active (likely)
0.5 - 0.69 → MEDIUM    → Active (maybe)
0.3 - 0.49 → LOW       → Inactive (maybe)
0.0 - 0.29 → VERY_LOW  → Inactive (likely)

Threshold: 0.5
- ≥ 0.5 → Agent is ACTIVE → Skip resume
- < 0.5 → Agent is INACTIVE → Send resume
```

## Noise Filtering

The system filters out these patterns from activity signals:
- "resumer"
- "stall-recovery"
- "no-acknowledgments"
- "inactivity detected"
- "[c2a]"
- "#no-reply"
- "#progress-only"

This prevents resume prompts from counting as activity.

## Key Functions

### `HardenedActivityDetector.assess_agent_activity()`
```python
assessment = detector.assess_agent_activity(
    agent_id: str,
    lookback_minutes: int = 60
) -> ActivityAssessment
```

### `should_send_resume()`
```python
should_send, reason = should_send_resume(
    agent_id: str,
    lookback_minutes: int = 60
) -> Tuple[bool, str]
```

### `OptimizedStallResumePrompt.generate_resume_prompt()`
```python
prompt = generator.generate_resume_prompt(
    agent_id: str,
    fsm_state: Optional[str] = None,
    last_mission: Optional[str] = None,
    stall_duration_minutes: float = 0.0,
    validate_activity: bool = True  # ← Key parameter
) -> Optional[str]
```

## Usage Examples

### Check Agent Status
```bash
python tools/check_agent_statuses.py
```

### Test Activity Detection
```python
from src.core.hardened_activity_detector import HardenedActivityDetector

detector = HardenedActivityDetector()
assessment = detector.assess_agent_activity('Agent-7', lookback_minutes=60)

print(f"Active: {assessment.is_active}")
print(f"Confidence: {assessment.confidence:.2f}")
print(f"Last Activity: {assessment.last_activity}")
print(f"Reasons: {', '.join(assessment.reasons)}")
```

### Test Resume Guard
```python
from src.core.stall_resumer_guard import should_send_resume

should_send, reason = should_send_resume('Agent-7', lookback_minutes=60)
print(f"Should send resume: {should_send}")
print(f"Reason: {reason}")
```

## Error Handling

The system **fails open** (allows resume) to prevent missed resumes:

- **Import errors** → Allow resume
- **Detection errors** → Allow resume (with logging)
- **Validation failures** → Allow resume (with warning)
- **Missing dependencies** → Fallback gracefully

This ensures truly stalled agents still receive prompts even if detection fails.

