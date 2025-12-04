# 🚨 CAPTAIN MESSAGE - TEXT

**From**: Agent-4 (Past-Captain)
**To**: Agent-4 (Future-Captain)
**Priority**: normal
**Message ID**: captain_restart_pattern_v1_2025-12-03
**Timestamp**: 2025-12-03T00:00:00.000000

---

# Subject: Captain Restart Pattern v1 — SSOT Remediation + Phase 2 Consolidation

Captain,

This is a self-addressed pattern to remove cold-start friction next cycle.

On wake, do NOT start with planning. Start with the loop.

--------------------------------
FIRST 5 MINUTES CHECKLIST
--------------------------------

1) Stamp the restart
   - Open Agent-4/status.json
   - Append an entry to current_tasks like:
     - "Captain restart — applied Restart Pattern v1"
   - Set current_pattern = "Captain_Restart_Pattern_v1"

2) Inbox sweep
   - Check:
     - Agent-4 inbox
     - runtime/agent_comms/ (broadcasts, captain-directed notes)
   - For each unread/pending message:
     - Tag it mentally as:
       - BLOCKER
       - STATUS_UPDATE
       - PROACTIVE_IDEA
   - Do NOT solve yet. Just collect.

3) Status sweep
   - For agents 1–8:
     - Read each agent's status.json:
       - Note: status, next_actions, blockers, focus_domain
     - Flag:
       - STALE: status unchanged for multiple cycles with unfinished work
       - BLOCKED: explicit blocker listed
       - HOT: active work directly touching SSOT remediation or Phase 2 consolidation

4) Immediate follow-ups
   - Respond to:
     1) BLOCKERS affecting multiple agents or shared systems (high priority)
     2) HOT work on:
        - SSOT remediation
        - Phase 2 tools consolidation
     3) Any direct questions to Captain
   - For each response:
     - Use:
       - Force Multiplier
       - Agent Pairing
       - Telephone Game
     - Keep messages short, directive, and concrete.

5) Devlog anchor
   - Add a Captain devlog entry:
     - "Restarted Captain loop using Restart Pattern v1."
     - Summarize:
       - Which agents were contacted
       - Which domains (SSOT / Phase 2 / other) you touched
       - Any new global decisions

After this 5-minute pass, THEN you can choose any deeper strategy or planning.

--------------------------------
ACTIVE MISSIONS TO CARRY FORWARD
--------------------------------

1) SSOT remediation (Priority 1 focus)
   - Objective: Reduce SSOT drift and duplication, starting with highest-impact zones.
   - Domain ownership:
     - Agent-1: Integration SSOT (coordinate loaders, messaging bridges)
     - Agent-2: Architecture SSOT (core patterns, templates, registries)
     - Agent-3: Infrastructure SSOT (message queue, runners, deployment scripts)
     - Agent-5: Analytics SSOT (metrics, tools registry, dashboards)
     - Agent-6: Communication SSOT (Discord/CLI/messaging glue)
     - Agent-7: Web SSOT (DOM tools, scrapers, site deploys)
     - Agent-8: QA SSOT (test infra, coverage, validation standards)
     - Agent-4: Strategic coordination (who owns what; boundary calls)
   - Your job:
     - Identify SSOT conflicts or duplication from messages + statuses.
     - Use Agent Pairing to resolve cross-domain questions.
     - When multiple agents are needed, use Telephone Game.

2) Phase 2 tools consolidation
   - Objective: Move from "many tools; low clarity" → "fewer tools; clear owners; clear metrics."
   - Current positions (treat as default unless contradicted by live status):
     - Agent-3: Phase 2 coordinator for infrastructure + monitoring tools. Target: consolidate overlapping runners, queue monitors, and ops scripts.
     - Agent-5: Completed or near-completed analytics/tooling analysis (39 → ~8 tools). Ready to move from analysis → execution.
   - Your job:
     - Confirm whether consolidation execution has actually started, not just planned.
     - Push at least one concrete consolidation task into motion per relevant agent when you see stalls.

3) Patterns in play
   - Force Multiplier: When a task is too big or touches many files, you split it into parallelizable sub-tasks and assign across agents.
   - Agent Pairing: Whenever SSOT ownership or boundaries are unclear, explicitly pair two agents and ask for a small joint decision/output.
   - Telephone Game: For multi-domain problems, have experts add value sequentially instead of all-in-one messages. You define the hop order and done-condition up front.

--------------------------------
CONCRETE FOLLOW-UP TARGETS NEXT CYCLE
--------------------------------

On restart, use the status + inbox sweep to check:

- Agent-5 (Analytics): Has Phase 2 consolidation EXECUTION started after the analysis? If not, send a clear message defining 1–3 target tools to consolidate first, success criteria, and a short horizon for progress (1–2 cycles).

- Agent-3 (Infrastructure): What is the % completion for Phase 2 infra monitoring consolidation? Any blockers on message queue, runners, or monitoring scripts? If blocked, apply Agent Pairing (e.g., Agent-3 + Agent-1 or Agent-6) instead of letting it stall.

- Agent-2 (Architecture): Check Priority 1 SSOT remediation progress on tagging + consolidating the 43 high-impact architecture files. If it's lagging, use Force Multiplier to assign smaller, clear chunks to multiple agents with shared patterns.

- Agent-1 (Integration): Check the coordinate loader + integration SSOT refactors. Are there still multiple competing loaders or mappings? If yes, designate one as canonical and assign a small consolidation scope.

- Agent-7 (Web): Check DOM utilities and web helpers. Is there one clear SSOT for DOM tools and scrapers? If not, direct consolidation + minimal validation pattern.

For all of the above:
- If progress is happening: reinforce and remove blockers.
- If stalled: send targeted messages that either narrow the scope, add partners (pairing / telephone), or apply Force Multiplier for parallel cleanup.

--------------------------------
OPERATING RULES FOR FUTURE-CAPTAIN
--------------------------------

1) Priority mode: Default: NORMAL priority for all messages. Upgrade to URGENT only when a blocker stops multiple agents or core systems, OR the user declares an explicit emergency.

2) Attention allocation: First: unblock agents. Second: maintain SSOT integrity (Priority 1 zones). Third: push Phase 2 consolidation forward. Only then: new initiatives or experiments.

3) Agent protection: If any agent's status.json indicates deep focus or long-running work, avoid assigning new unrelated tasks unless it affects SSOT or system health. You can always ask for a micro-status or schedule follow-ups in their next cycle instead of interrupting.

4) Devlog discipline: Keep one consolidated Captain devlog entry per "restart pattern" usage. Add short notes to agent devlogs only when you make significant decisions or reassignments for that agent. Devlogs are for narrative continuity, not for duplicating every micro-message.

--------------------------------
CLOSING
--------------------------------

Future-Captain: when you read this, start with:

1) Run the 5-minute checklist.
2) Touch at least one SSOT remediation action and one Phase 2 consolidation action, using Force Multiplier / Pairing / Telephone Game as needed.
3) Log the cycle in your devlog.

After that, you're free to adapt — but never skip the loop.

— Past-Captain

---
*Message delivered via Unified Messaging Service*


