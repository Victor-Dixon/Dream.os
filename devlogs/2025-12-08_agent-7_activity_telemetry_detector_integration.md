# 📡 Activity Telemetry v1 Detector Integration

**Agent:** Agent-7 (Web Development Specialist)  
**Date:** 2025-12-08  
**Status:** ✅ Delivered  
**Scope:** ActivityEmitter-driven activity scoring for stall/resume signal

---

## What changed
- Ingest `runtime/agent_comms/activity_events.jsonl` inside `AgentActivityDetector` and fold events into summaries.
- Added weighted scoring with tiering (Tier1: TASK_COMPLETED, GIT_PUSH, MONEY_METRIC, TOOL_RUN failure) and `is_active(agent, window_s=…)` API.
- Activity detection now prefers event signals for last-activity and inactivity duration; legacy sources remain as fallback.

## Rationale
- Reduce noise from status.json-only heuristics and trust emitter-backed signals for stall/resume decisions.

## Notes / Next Steps
- Activity events file missing will gracefully fall back to legacy heuristics.
- Threshold defaults to score ≥3 or any Tier1 hit; adjust per ops feedback if too strict/lenient.

