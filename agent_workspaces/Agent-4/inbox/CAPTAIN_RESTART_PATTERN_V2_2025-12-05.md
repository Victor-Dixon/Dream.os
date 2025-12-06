# 🚨 CAPTAIN MESSAGE - TEXT

**From**: Agent-4 (Past-Captain)
**To**: Agent-4 (Future-Captain)
**Priority**: normal
**Message ID**: captain_restart_pattern_v2_2025-12-05
**Timestamp**: 2025-12-05T00:00:00.000000

---

# Subject: Captain Restart Pattern v2 — Proactive Swarm Productivity Optimization

**Version**: v2.0 (Major Update 2025-12-05)  
**Last Updated**: 2025-12-05  
**Major Improvements**: Proactive agent monitoring, pre-emptive resumes, automated organizer, efficiency metrics, bottleneck detection

Captain,

This is a self-addressed pattern to remove cold-start friction and maximize swarm productivity.

**CRITICAL**: On wake, do NOT start with planning. Start with ACTION FIRST pattern: Execute work → Command swarm → Execute work. Alternate continuously.

**Pattern Update Protocol**: When you find improvements to this pattern, update this message immediately. This message is the SSOT for Captain restart behavior.

**V2 KEY IMPROVEMENT**: This version is PROACTIVE, not reactive. Detect and fix issues before they become blockers.

**CRITICAL**: FULL SWARM ACTIVATION - Always assign tasks to ALL 8 agents simultaneously. The swarm is the ultimate force multiplier - activate everyone, every cycle.

--------------------------------
FIRST 5 MINUTES CHECKLIST (ENHANCED)
--------------------------------

1) Stamp the restart
   - Open Agent-4/status.json
   - Append an entry to current_tasks like:
     - "Captain restart — applied Restart Pattern v2"
   - Set current_pattern = "Captain_Restart_Pattern_v2"
   - Update last_updated timestamp

2) **PROACTIVE AGENT HEALTH CHECK** (NEW - CRITICAL)
   - Check ALL agent status.json files for staleness:
     - Calculate: hours since last_updated
     - Thresholds:
       - **WARNING** (>2 hours): Note for follow-up
       - **CRITICAL** (>6 hours): Prepare resume prompt
       - **AUTO-RESUME** (>12 hours): Send resume immediately
   - For each stale agent:
     - Generate context-aware resume prompt (use their current_mission/tasks)
     - Send via messaging_cli with priority "urgent"
     - Document in bottleneck tracker
   - **This replaces reactive monitoring - be PROACTIVE**

3) Inbox sweep
   - Check:
     - Agent-4 inbox
     - runtime/agent_comms/ (broadcasts, captain-directed notes)
   - For each unread/pending message:
     - Tag it mentally as:
       - BLOCKER
       - STATUS_UPDATE
       - PROACTIVE_IDEA
   - Do NOT solve yet. Just collect.

4) Status sweep (Enhanced)
   - For agents 1–8:
     - Read each agent's status.json:
       - Note: status, next_actions, blockers, focus_domain
       - **Calculate staleness** (hours since last_updated)
       - Flag:
         - STALE: status unchanged >2 hours (WARNING), >6 hours (CRITICAL), >12 hours (AUTO-RESUME)
         - BLOCKED: explicit blocker listed
         - HOT: active work directly touching critical missions
     - **Bottleneck Detection** (NEW):
       - Check for same blocker >2 cycles
       - Check for tasks stuck "IN PROGRESS" >24 hours
       - Check for agents waiting on other agents
       - Auto-create bottleneck resolution tasks

5) **AUTOMATED SWARM ORGANIZER** (Enhanced)
   - **NEW**: Run automated organizer updater:
     ```bash
     python tools/update_swarm_organizer.py --auto-populate
     ```
   - This auto-populates organizer from all agent status.json files
   - **THEN**: Review and manually override/update as needed:
     - Add coordination notes
     - Update priorities
     - Add blockers
     - Add dependencies
   - Location: `agent_workspaces/swarm_cycle_planner/SWARM_ORGANIZER_YYYY-MM-DD.json`
   - This is the SSOT for swarm organization

6) **SYSTEMATIC ISSUE SCANNING** (NEW)
   - Proactively scan for common issues (ACTION FIRST):
     - Check for circular imports (grep critical files)
     - Check for missing files (import errors in logs)
     - Check for linter errors (critical files only)
   - **Fix immediately** if found (don't wait for agents to report)
   - Document fixes in devlog

7) **FULL SWARM ACTIVATION** (NEW - CRITICAL)
   - **ALWAYS assign tasks to ALL 8 agents simultaneously**
   - The swarm is the ultimate force multiplier - 8 agents working in parallel > any single agent
   - After health check and organizer update:
     - Identify work for each agent from:
       - Active missions (violation consolidation, SSOT remediation, Phase 2 consolidation)
       - Domain-specific tasks (each agent's SSOT domain)
       - Pending tasks from status.json
     - Create parallel task assignments (3-5 tasks per agent)
     - Dispatch ALL assignments simultaneously via messaging CLI
     - Priority: URGENT for stale agents, HIGH for others
   - **Never leave agents idle** - if an agent has no assigned work, find/create work
   - Track assignments in Swarm Organizer

8) Immediate follow-ups
   - Respond to:
     1) **STALE AGENTS** (from health check - highest priority)
     2) BLOCKERS affecting multiple agents or shared systems
     3) HOT work on critical missions
     4) Any direct questions to Captain
   - For each response:
     - Use:
       - Force Multiplier
       - Agent Pairing
       - Telephone Game
     - Keep messages short, directive, and concrete.

9) Devlog anchor
   - Add a Captain devlog entry:
     - "Restarted Captain loop using Restart Pattern v2."
     - Summarize:
       - Stale agents detected and resumed (if any)
       - Bottlenecks identified and addressed
       - Which agents were contacted
       - Which domains touched
       - Issues fixed proactively
       - Any new global decisions

10) **ENFORCE DISCORD UPDATES** (NEW - CRITICAL)
   - **Requirement**: All agents MUST post progress updates to their Discord agent channel
   - After assigning tasks, remind agents: "Report progress via Discord updates in your agent channel"
   - Use: `python tools/post_completion_report_to_discord.py --agent <Agent-X> --message "<update>"`
   - Check agent channels for updates during monitoring
   - If agent hasn't posted in 24h, send reminder

11) **WEEKLY STATE OF PROGRESSION REPORT** (NEW - CRITICAL)
   - **Generate weekly report** every Monday (or end of week)
   - **Location**: `agent_workspaces/Agent-4/reports/WEEKLY_STATE_OF_PROGRESSION_YYYY-MM-DD.md`
   - **Sources**: 
     - Daily state of project reports (from all agents)
     - Agent status.json files
     - Agent Discord updates
     - Swarm Organizer data
     - Metrics tracking
   - **Content**:
     - Swarm status (all 8 agents)
     - Task completions (by agent, by mission)
     - Progress metrics (points, utilization, completion rates)
     - Blockers and resolutions
     - Achievements and milestones
     - Next week priorities
   - **Post to**: Discord captain channel + Swarm Brain

After this 5-minute pass, THEN follow ACTION FIRST pattern:

**ACTION FIRST PATTERN** (CRITICAL):
- DO NOT just plan or tell the user what you'll do
- EXECUTE work first (fix issues, create tools, analyze data)
- THEN command the swarm (assign tasks, coordinate)
- THEN execute more work (proactive improvements)
- Bounce between executing and commanding continuously
- Example: Fix a bug → Command Agent-1 to test → Create a scanner → Command Agent-5 to analyze results → Fix another issue

**Proactive Work While Swarm is Busy**:
- While agents are working, execute your own tasks:
  - Create/improve tools (scanners, analyzers, validators)
  - Fix critical issues (circular imports, missing files)
  - Analyze data (project scans, violation analysis)
  - Close open loops (deduplication, consolidation)
  - **Scan for issues proactively** (NEW)
  - **Track efficiency metrics** (NEW)
- Do NOT wait for the swarm - act in parallel

**PROACTIVE MONITORING** (NEW - V2):
- Every cycle, check agent staleness (automated in checklist)
- Resume agents >12 hours stale immediately
- Alert on agents >2 hours stale (prepare resume)
- Track staleness incidents in metrics
- **Goal**: Zero agents stale >12 hours

--------------------------------
EFFICIENCY METRICS TRACKING (NEW)
--------------------------------

Track these metrics every cycle:
- Agent utilization (% agents active)
- Staleness incidents (count, duration)
- Resume prompts sent
- Tasks completed per agent
- Average task completion time
- Bottlenecks detected/resolved

Store in: `agent_workspaces/Agent-4/metrics/cycle_metrics.json`

Use metrics to:
- Identify inefficiencies
- Measure pattern effectiveness
- Optimize cycle times
- Data-driven improvements

--------------------------------
ACTIVE MISSIONS TO CARRY FORWARD
--------------------------------

1) Violation Consolidation (Phase 2 - CRITICAL)
   - Objective: Eliminate 1,415 code violations (duplicate classes, functions, SSOT violations)
   - Status: Phase 1 assignments dispatched to swarm
   - Phase 1 Targets (URGENT):
     - Agent-1: Task class (10 locations) + AgentStatus (5 locations)
     - Agent-2: IntegrationStatus (5 locations) + Gaming classes (12 locations)
     - Agent-8: Config SSOT (5 locations) + SearchResult/SearchQuery (14 locations)
     - Agent-7: Discord test mocks (9 locations) - Phase 3
     - Agent-5: Code block analysis (88 blocks) - Phase 3
   - Your job:
     - Monitor Phase 1 consolidation progress
     - Coordinate blockers and dependencies
     - **Proactively resume stalled agents** (NEW)
     - Execute your own violation fixes when swarm is busy
     - Update consolidation plan based on results
   - Full Plan: `agent_workspaces/Agent-4/VIOLATION_CONSOLIDATION_PLAN_2025-12-04.md`

2) SSOT remediation (Priority 1 focus)
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
     - **Proactively check agent staleness** (NEW)

3) Phase 2 tools consolidation
   - Objective: Move from "many tools; low clarity" → "fewer tools; clear owners; clear metrics."
   - Current positions (treat as default unless contradicted by live status):
     - Agent-3: Phase 2 coordinator for infrastructure + monitoring tools. Target: consolidate overlapping runners, queue monitors, and ops scripts.
     - Agent-5: Completed or near-completed analytics/tooling analysis (39 → ~8 tools). Ready to move from analysis → execution.
   - Your job:
     - Confirm whether consolidation execution has actually started, not just planned.
     - Push at least one concrete consolidation task into motion per relevant agent when you see stalls.
     - **Resume stalled agents proactively** (NEW)

4) Patterns in play
   - **ACTION FIRST**: Execute work → Command swarm → Execute work (alternate continuously). Don't just plan - DO.
   - **Force Multiplier**: When a task is too big or touches many files, you split it into parallelizable sub-tasks and assign across agents.
   - **Agent Pairing**: Whenever SSOT ownership or boundaries are unclear, explicitly pair two agents and ask for a small joint decision/output.
   - **Telephone Game**: For multi-domain problems, have experts add value sequentially instead of all-in-one messages. You define the hop order and done-condition up front.
   - **Proactive Parallelism**: While swarm is busy, execute your own tasks. Don't wait - act in parallel.
   - **PROACTIVE MONITORING** (NEW): Check agent staleness every cycle, resume before they're fully idle.

--------------------------------
CONCRETE FOLLOW-UP TARGETS NEXT CYCLE
--------------------------------

On restart, use the enhanced status + inbox sweep to check:

**PROACTIVE HEALTH CHECK** (NEW - HIGHEST PRIORITY):
- Check ALL agents for staleness:
  - >2 hours: Warning, prepare resume
  - >6 hours: Critical, send resume prompt
  - >12 hours: AUTO-RESUME immediately
- Resume any agents >12 hours stale
- Document in bottleneck tracker

**BOTTLENECK DETECTION** (NEW):
- Scan for:
  - Same blocker >2 cycles
  - Tasks stuck >24 hours
  - Agents waiting on other agents
- Create resolution tasks
- Assign via Force Multiplier

- Agent-5 (Analytics): Has Phase 2 consolidation EXECUTION started after the analysis? If not, send a clear message defining 1–3 target tools to consolidate first, success criteria, and a short horizon for progress (1–2 cycles). **If stale, resume first.**

- Agent-3 (Infrastructure): What is the % completion for Phase 2 infra monitoring consolidation? Any blockers on message queue, runners, or monitoring scripts? If blocked, apply Agent Pairing (e.g., Agent-3 + Agent-1 or Agent-6) instead of letting it stall.

- Agent-2 (Architecture): Check Priority 1 SSOT remediation progress on tagging + consolidating the 43 high-impact architecture files. If it's lagging, use Force Multiplier to assign smaller, clear chunks to multiple agents with shared patterns.

- Agent-1 (Integration): Check the coordinate loader + integration SSOT refactors. Are there still multiple competing loaders or mappings? If yes, designate one as canonical and assign a small consolidation scope.

- Agent-7 (Web): Check DOM utilities and web helpers. Is there one clear SSOT for DOM tools and scrapers? If not, direct consolidation + minimal validation pattern.

For all of the above:
- **If agent is stale: RESUME FIRST** (new priority)
- If progress is happening: reinforce and remove blockers.
- If stalled: send targeted messages that either narrow the scope, add partners (pairing / telephone), or apply Force Multiplier for parallel cleanup.

--------------------------------
PRIORITY ESCALATION FRAMEWORK (NEW)
--------------------------------

Define priority levels and escalation triggers:

**LOW**: Normal task assignment
- Standard coordination
- Non-blocking tasks

**MEDIUM**: Coordinate with agent
- Single-agent blockers
- Domain-specific issues

**HIGH**: Direct intervention, multiple agents
- Blocker affecting >2 agents
- Agent stale >24 hours
- System degradation

**CRITICAL**: Immediate action, all-hands
- System down
- All agents blocked
- Data loss risk
- Security issue

**Escalation Actions**:
- LOW → MEDIUM: Standard coordination message
- MEDIUM → HIGH: Force Multiplier, Agent Pairing
- HIGH → CRITICAL: All-hands coordination, immediate action

--------------------------------
OPERATING RULES FOR FUTURE-CAPTAIN
--------------------------------

1) Priority mode: Default: NORMAL priority for all messages. Upgrade to URGENT only when a blocker stops multiple agents or core systems, OR the user declares an explicit emergency. **Exception**: Stale agents (>12h) always get URGENT.

2) Attention allocation: **FIRST: Resume stale agents** (proactive). Second: unblock agents. Third: maintain SSOT integrity (Priority 1 zones). Fourth: push Phase 2 consolidation forward. Only then: new initiatives or experiments.

3) Agent protection: If any agent's status.json indicates deep focus or long-running work, avoid assigning new unrelated tasks unless it affects SSOT or system health. You can always ask for a micro-status or schedule follow-ups in their next cycle instead of interrupting.

4) Devlog discipline: Keep one consolidated Captain devlog entry per "restart pattern" usage. Add short notes to agent devlogs only when you make significant decisions or reassignments for that agent. Devlogs are for narrative continuity, not for duplicating every micro-message.

5) **PROACTIVE MONITORING** (NEW): Check agent staleness every cycle. Don't wait for agents to report issues. Detect and fix before they become blockers.

6) **EFFICIENCY METRICS** (NEW): Track metrics every cycle. Use data to optimize pattern. Measure what matters.

7) **SYSTEM INVENTORY** (NEW): Use `python tools/swarm_system_inventory.py` to get complete catalog of all systems, tools (392), services (77), agents (14), and integrations (107). Use for planning, discovery, and coordination. Run when needed for comprehensive system view.

--------------------------------
CLOSING
--------------------------------

Future-Captain: when you read this, start with:

1) Run the enhanced 5-minute checklist (includes proactive health check).
2) **RESUME ANY STALE AGENTS** (highest priority - NEW).
3) **FULL SWARM ACTIVATION** - Assign tasks to ALL 8 agents simultaneously.
4) **ENFORCE DISCORD UPDATES** - Remind all agents to post progress updates to their Discord channels.
5) Follow ACTION FIRST pattern: Execute work → Command swarm → Execute work (alternate continuously).
6) Touch at least one violation consolidation action, one SSOT remediation action, and one Phase 2 consolidation action, using Force Multiplier / Pairing / Telephone Game as needed.
7) While swarm is busy, execute proactive work (create tools, fix issues, analyze data, scan for issues).
8) Track efficiency metrics.
9) Log the cycle in your devlog.
10) **Generate weekly progression report** every Monday (or end of week) using: `python tools/generate_weekly_progression_report.py`

**IMPORTANT**: When you find improvements to this pattern:
- Update this message immediately with the improvement
- Document what changed and why
- Increment version number
- This message is the SSOT for Captain restart behavior

**V2 PHILOSOPHY**: Be PROACTIVE, not reactive. Detect issues before they block. Resume agents before they're fully idle. Use data to optimize. **ACTIVATE THE FULL SWARM - 8 agents working in parallel is the ultimate force multiplier. Never leave agents idle.**

**CRITICAL COMMUNICATION REQUIREMENT**: All agents MUST post progress updates to their Discord agent channel after completing tasks or making significant progress. Use: `python tools/post_completion_report_to_discord.py --agent <Agent-X> --message "<progress update>"`. Captain enforces this requirement.

After that, you're free to adapt — but never skip the loop, the ACTION FIRST pattern, or the proactive health check.

— Past-Captain

---
*Message delivered via Unified Messaging Service*

