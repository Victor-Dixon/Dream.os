# Learning: Fast Sync Check-ins (2025-12-08)

## Context
- Captain restart cycle (Cycle 28) required rapid alignment across Agents 1–8 for SSOT remediation and Phase 2 consolidation.
- Prior cycles had manual per-agent messages; overhead and risk of omissions.

## Pattern
- Use a templated all-agent check-in: request (1) status, (2) top next_action, (3) blockers, (4) % complete — keep to 2–3 lines.
- Send to all agents in one sweep to maintain cadence and reduce copy/paste errors.
- Treat stale timestamps as high-risk even if tasks are marked complete.

## Tooling
- Added `tools/session_quick_checkin.py` to broadcast the template to all agents.

## Actions this cycle
- Broadcast check-in sent to Agents 1–8 after restart.
- Targeted pings to Agents 1,2,3,5,7,8 on SSOT/Phase 2 focus areas.

## Recommendations
- Run the broadcast at the start of each restart cycle.
- If no reply within a cycle, escalate with Agent Pairing or Force Multiplier.
- Update SWARM_ORGANIZER immediately after responses to keep SSOT current.

