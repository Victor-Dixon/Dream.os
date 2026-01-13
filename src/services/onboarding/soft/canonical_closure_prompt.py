"""
<!-- SSOT Domain: integration -->

Canonical Swarm Closure Prompt (A+++ Grade)
==========================================

SSOT for session closure and public build finalization.
This is the canonical A+++ version that forces true session completion,
public-build readiness, and zero-drift handoff.

This version enforces:
- Git verification is ALWAYS required (status check every session)
- Blogging criteria are explicit (user-facing = mandatory)
- Session cannot end if mandatory tasks are incomplete

Author: Swarm Architecture Team
Created: 2025-01-XX
License: MIT

This prompt works for:
- Code repos
- Websites
- Research spikes
- Infrastructure work
- Content systems
- Internal tooling
- One-day experiments

Use Cases:
- End of day closure
- End of sprint / cycle
- Before handoff to another agent
- Before public posting
- Before context window reset
"""

# A+++ Canonical Swarm Closure Prompt
CANONICAL_CLOSURE_PROMPT = """🎯 SESSION CLOSURE REQUIRED — BUILD & PUBLIC LOG COMPLETE

This session is NOT complete until:
- Work is committed (or explicitly verified as no-change)
- Knowledge is persisted
- Public-facing update exists where required
- Another agent can resume without context loss

Complete ALL tasks below.

────────────────────────────────────────
MANDATORY CLOSURE TASKS
────────────────────────────────────────

1. Finalize passdown.json
   - Scope completed
   - Decisions made
   - Tradeoffs
   - Must support cold-start handoff
   - NO "next priorities" or future work (belongs in new task creation)

2. Create Final Devlog
   - Factual, reproducible
   - WHAT changed and WHY
   - No narration, no speculation

3. Git Verification (ALWAYS REQUIRED)
   - Run: `git status`
   - If changes exist:
     - ⚠️ **Shared workspace safety**: DO NOT run `git add .`, `git restore .`, or `git clean -fd` in a shared repo checkout.
       - These commands can stage/revert/delete other agents' uncommitted work and untracked artifacts.
       - Use a path-scoped add instead: `git add <paths-you-touched>` OR interactive staging: `git add -p`
     - `git commit -m "agent-<n>: <brief description>"`
     - `git push`
   - If no changes:
     - Explicitly state: "No code changes — verified via git status"

4. PUBLIC SURFACE EXPANSION (PSE) — GOVERNANCE & SAFETY CHANGES
   - If this work touches governance, safety rules, protocols, templates, closure logic, or swarm behavior **you must produce three derivative public artifacts** (PSE).
   - Trigger keywords (any): governance, safety, protocol, closure, canonical prompt, template, shared workspace, swarm rule
   - Required outputs (use template `templates/public_surface_expansion_template.md`):
       1. BLOG_DADUDEKC.md – personal / builder log
       2. BLOG_WEARESWARM.md – swarm ops / doctrine
       3. BLOG_DREAMSCAPE.md – lore / mythic encoding
   - Validation fails if these artifacts are absent when triggers matched

5. Publish Devlog (Internal / Discord)
<<<<<<< HEAD
   - Post to Discord using: `python tools/devlog_poster.py --agent {AGENT_ID} --file <devlog_path>`
   - HARD REQUIREMENT: Fails loudly if `DISCORD_WEBHOOK_AGENT_{N}` env var missing (where N is agent number)
   - Command automatically routes to agent's dedicated `#agent-{n}-devlogs` channel
   - This represents the internal build record and public-facing update

5.5. Cycle Accomplishment Integration (MANDATORY)
   - Run: `python tools/cycle_accomplishment_integrator.py --agent {AGENT_ID} --closure-run-id "{AGENT_ID}:{GIT_SHA}:{UTC_TS}" --tasks-completed <int> --issues-found <int> --consolidation-opportunities <int> --closure-complete`
   - HARD REQUIREMENTS:
     - Idempotent: same closure-run-id must NO-OP (no duplicate points/posts)
     - Atomic status.json update with crash safety
     - Fails loudly if `DISCORD_WEBHOOK_CYCLE_ACCOMPLISHMENTS` missing
     - Uses configurable points from `config/cycle_points.json`
   - Required output: "Cycle accomplishment logged — tasks=X, issues=Y, consolidations=Z, points=P"

6. Blog to Website (CONDITIONAL BUT ENFORCED)
=======
   - Post to Discord using: `python tools/devlog_poster.py --agent Agent-X --file <devlog_path>`
   - This represents the internal build record and public-facing update

5. Blog to Website (CONDITIONAL BUT ENFORCED)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
   - REQUIRED if work affected:
     - User-facing behavior
     - Dashboards
     - APIs
     - Data pipelines
     - Infrastructure
   - Post build update to the appropriate website
   - If not applicable:
     - Explicitly state: "No website blogging required — internal-only change"

<<<<<<< HEAD
7. Update Swarm Brain Database
   - Include exact command used OR
   - "Verified — no update required"

8. Code Quality & Health Check (MANDATORY)
   - Run automated quality audit: `python tools/closure_quality_audit.py --agent Agent-X --audit`
   - Review audit results for linting errors, import issues, and CLI tool problems
   - Validate your changes don't break existing functionality
   - Check for new dependency issues introduced by your changes
   - Use audit tool output to identify issues requiring master task list entries
   - Required: "Code health check completed — [X issues found and documented]"

9. Functionality Consolidation Audit (MANDATORY)
   - Use quality audit tool results: Review consolidation opportunities flagged by the automated audit
   - Manually verify consolidation suggestions: Check if similar functionality can be merged
   - Review tool architecture: Ensure new tools integrate well with existing systems
   - Identify code reuse opportunities: Look for common patterns that could be extracted
   - Document consolidation candidates: Add detailed refactoring tasks to master task list
   - Required: "Consolidation audit completed — [X consolidation opportunities identified]"

10. Issue Documentation & Task List Updates (MANDATORY)
   - Add ALL identified issues to master task list: Code quality issues, CLI warnings, consolidation opportunities
   - Even if you won't fix them now, document for future agents: "Added X tasks to master task list"
   - Include severity levels and estimated effort for each issue
   - Verify task list is updated: Check that new tasks appear in MASTER_TASK_LIST.md
   - Required: "Issue documentation completed — [X tasks added to master task list]"

11. Automatic Workspace Cleanup (SAFE & AGENT-SCOPED)
    - ⚠️ **SAFETY FIRST**: Only clean agent-owned directories (`agent_workspaces/Agent-X/`, `tools/agent_workspaces/Agent-X/`)
    - **NEVER touch shared directories** (src/, tools/, docs/, etc.)
    - **NEVER delete - move to archive instead**: `mv file /path/to/archive/`
    - Clean up session artifacts:
      - Remove temporary test files (`test_*.py` you created)
      - Archive working drafts and devlog drafts
      - Clean cache files in agent workspace
      - Remove session-specific screenshots/logs
    - Verification required: List files before/after, confirm only agent-owned files affected
    - If no cleanup needed: "Agent workspace cleanup completed — no artifacts to clean"

12. Closure Improvement (CHOOSE EXACTLY ONE)
    a) Create ONE small utility tool (≤150 lines)
    b) Define ONE protocol (≤10 lines)
    c) Improve documentation quality (delete, merge, deduplicate)
    d) Explicitly skip with: "Skipped — no actionable gap identified"
=======
6. Update Swarm Brain Database
   - Include exact command used OR
   - "Verified — no update required"

7. Closure Improvement (CHOOSE EXACTLY ONE)
   a) Create ONE small utility tool (≤150 lines)
   b) Define ONE protocol (≤10 lines)
   c) Improve documentation quality (delete, merge, deduplicate)
   d) Explicitly skip with: "Skipped — no actionable gap identified"
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

────────────────────────────────────────
HARD RULES (NON-NEGOTIABLE)

❌ SHARED WORKSPACE SAFETY (CRITICAL)
- NEVER run `git clean -fd` or delete untracked files in a shared repo
- NEVER delete files outside agent-owned directories
- If untracked files exist outside agent scope → Status MUST be 🟡 Blocked

❌ DESTRUCTIVE GIT COMMANDS ARE FORBIDDEN IN SHARED WORKSPACES
- git clean -fd
- git restore .
- rm -rf on repo paths

<<<<<<< HEAD
❌ WORKSPACE CLEANUP SAFETY (MANDATORY)
- NEVER delete files - move to archive directories instead
- NEVER clean shared directories (src/, tools/, docs/, root files)
- ONLY clean agent-owned workspaces (`agent_workspaces/Agent-X/`)
- VERIFY ownership before any cleanup operation
- If unsure about file ownership → Status MUST be 🟡 Blocked

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
When in doubt, choose NON-DESTRUCTIVE verification over cleanup.
────────────────────────────────────────

- No narration
- No summaries
- No next steps
- No speculative language
- Verify before recreating artifacts
- Git status must be checked every session
- If ANY mandatory task is incomplete or unverifiable → Status MUST be 🟡 Blocked

────────────────────────────────────────
OUTPUT CONTRACT (STRICT - A++ FORMAT)
────────────────────────────────────────

- **Task:** [Brief task description - what was accomplished]
- **Project:** [Project/repo name]

- **Actions Taken:**
  - [Bullet 1: factual action]
  - [Bullet 2: factual action]
  - No narration, no summaries

- **Artifacts Created / Updated:**
  - [Exact file path 1]
  - [Exact file path 2]
  - Exact paths only, no descriptions

- **Verification:**
  - [Proof/evidence bullet 1]
  - [Proof/evidence bullet 2]
  - Must show actual verification, not assumptions

- **Public Build Signal:**
  [ONE sentence only - human-readable description of what changed]

- **Git Commit:**
  [Commit hash if committed, or "Not committed" if not]

- **Git Push:**
  [Push status: "Pushed to [branch]" or "Not pushed"]

- **Website Blogging:**
  [Blog post URL if published, or "Not published" if not applicable]

<<<<<<< HEAD
- **Workspace Cleanup:**
  [Cleanup status: "Agent workspace cleanup completed — X files archived" or "No cleanup needed"]

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
- **Status:**
  ✅ Ready
  OR
  🟡 Blocked (specific reason)

FORBIDDEN IN CLOSURE:
- ❌ Workspace cleanup (janitorial deletion)
- ❌ Repo normalization by mass restore/clean
- ❌ Aligning local state via deletion
- ❌ "Next steps" or any future-facing language
- ❌ Narration or summaries (belongs in devlog)
- ❌ Speculation ("should work", "may need")
- ❌ Progress reports ("made progress", "partially completed")

────────────────────────────────────────
PROGRESSION GATE

🚧 DESTRUCTIVE-ACTION ESCALATION GATE
- If closure requires deleting, cleaning, or resetting repo files:
  - STOP immediately
  - Emit 🟡 Blocked
  - State exact conflict and await Captain arbitration
────────────────────────────────────────

Do NOT:
- Start new work
- Open a new session
- Signal readiness

Until:
- Status = ✅ Ready
<<<<<<< HEAD
- All 12 mandatory tasks are verified
=======
- All mandatory tasks are verified
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
- Public Build Signal is present

This closure must stand alone.
Another agent must be able to continue without context loss."""


def get_canonical_closure_prompt() -> str:
    """
    Get the canonical A++ Swarm closure prompt.
    
    Returns:
        The canonical closure prompt text
    """
    return CANONICAL_CLOSURE_PROMPT


__all__ = ["CANONICAL_CLOSURE_PROMPT", "get_canonical_closure_prompt"]

