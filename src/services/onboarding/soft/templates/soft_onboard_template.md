<!-- SSOT Domain: onboarding -->

[HEADER] S2A ONBOARDING (SOFT)
From: SYSTEM
To: {{AGENT}}
Priority: regular
Message ID: {{UUID}}
Timestamp: {{TIMESTAMP}}

## 🛰️ **S2A ACTIVATION DIRECTIVE — SWARM ONBOARDING v2.1**

**Signal Type:** System → Agent (S2A)
**Priority:** Immediate
**Mode:** Autonomous Execution
**FSM Target State:** ACTIVE

────────────────────────────────────────
⚠️ **SHARED WORKSPACE SAFETY (CRITICAL)**
────────────────────────────────────────
**Destructive git commands are FORBIDDEN:**
- ❌ `git clean -fd`
- ❌ `git restore .`
- ❌ `rm -rf` on repo paths
- ❌ Deleting untracked files (they may belong to other agents)

**Agent Ownership Boundary:**
- You may modify ONLY `agent_workspaces/{{AGENT}}/**` (your workspace)
- You may modify ONLY files explicitly assigned in your task
- Any change outside scope → STOP and escalate

**Branch Policy:** Commit directly to `main`. No feature branches.
────────────────────────────────────────

## Operating Cycle (Claim → Sync → Slice → Execute → Validate → Commit → Report)

**1) Load State:**
```bash
# Read inbox and status
cat agent_workspaces/{{AGENT}}/inbox/*.md
cat agent_workspaces/{{AGENT}}/status.json
```

**2) Claim One Task (priority order):**
- Inbox directives > active status.json > contract system > MASTER_TASK_LOG.md
```bash
python -m src.services.messaging_cli --agent {{AGENT}} --get-next-task
```

**3) Sync with Swarm:**
- Check Swarm Brain for patterns (advisory)
- Review other agent status.json files for coordination

**4) Execute One Real Deliverable:**
- No narration, no speculation
- Produce artifact/result OR 1 blocker (blocker + fix + owner)

**5) Validate Work:**
- Run lints, tests as applicable
- Verify changes work as expected

**6) Commit Changes:**
```bash
git add <your-files-only>  # Explicit paths, NOT git add .
git commit -m "Agent-X: Brief description"
git push
```

**7) Report Evidence:**
- Update status.json (task, progress, blockers)
- Post to Discord with artifact/validation/delegation

────────────────────────────────────────
**SESSION CLOSURE REQUIREMENT**
────────────────────────────────────────
Before ending session, run working-tree audit:
```bash
python tools/working_tree_audit.py --agent {{AGENT}}
```

Then complete SESSION CLOSURE ritual using:
- Template: `templates/session-closure-template.md`
- Validator: `python tools/validate_closure_format.py`
- Rules: `.cursor/rules/session-closure.mdc`

────────────────────────────────────────
**OUTPUT CONTRACT (STRICT - A++ FORMAT)**
────────────────────────────────────────
```markdown
- **Task:** [Brief task description]
- **Project:** [Project/repo name]

- **Actions Taken:**
  - [Factual action 1]
  - [Factual action 2]

- **Artifacts Created / Updated:**
  - [Exact file path]

- **Verification:**
  - [Proof with commit hash/command output/message ID]

- **Public Build Signal:**
  [ONE sentence - what changed]

- **Git Commit:** [hash or "Not committed"]
- **Git Push:** [Pushed to main or "Not pushed"]
- **Website Blogging:** [URL or "Not published"]

- **Status:** ✅ Ready OR 🟡 Blocked (reason)
```
────────────────────────────────────────

