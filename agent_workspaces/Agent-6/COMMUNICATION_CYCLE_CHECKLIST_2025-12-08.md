# Communication Cycle Checklist (Agent-6)
**Date:** 2025-12-08  
**Owner:** Agent-6 (Coordination & Communication)  
**Purpose:** Soft onboarding alignment — codify start/during/end steps and Discord reporting discipline.

---

## Cycle Start
- Inbox sweep priority: D2A → C2A → A2A; capture blockers/asks.
- Contract check: `--get-next-task` if applicable.
- Swarm Brain/context refresh: scan recent coordination topics.
- Status update: set `status=ACTIVE_AGENT_MODE`, `current_phase=TASK_EXECUTION`, bump `last_updated`.
- Confirm mission + next_actions for the slice; note blockers if any.

## During Cycle
- Update status.json on phase change or task completion.
- Log blockers immediately (with owner + proposed fix).
- Maintain coordination pings only when they move work forward.
- Keep FSM in TASK_EXECUTION; avoid idle/ack-only loops.

## Cycle End
- Record completed_tasks/next_actions in status.json.
- Prepare Discord completion post (primary visibility).
- Commit/attach artifacts (docs/tests/validation logs) before posting.
- File devlog entry referencing artifacts and status updates.

## Discord Reporting (required)
- When to post: slice completion, meaningful commit, validation/test results, or blockers.
- Include: Task, Actions Taken, Status (✅ or 🟡 + next step), Commit/msg (if code), Artifacts/paths.
- Channel: #agent-6-devlogs (or designated coordination channel).

## Completion Template (short)
- Task: <what was done>
- Actions: <bullets>
- Status: ✅ done / 🟡 blocked (<next step/owner>)
- Artifacts: <paths or commands>
- Notes: <optional risk/ask>

## Current focus (soft onboard)
- Refresh status + mission.
- Codify cycle checklist + Discord reporting.
- Resume coordination monitors after alignment.


