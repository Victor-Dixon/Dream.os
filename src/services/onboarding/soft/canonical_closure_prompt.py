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

   - REQUIRED if work affected:
     - User-facing behavior
     - Dashboards
     - APIs
     - Data pipelines
     - Infrastructure
   - Post build update to the appropriate website
   - If not applicable:
     - Explicitly state: "No website blogging required — internal-only change"



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

