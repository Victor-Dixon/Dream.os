# 🚀 Soft Onboarding All Agents - Manual Procedure

## Executive Summary

Due to GUI automation dependencies, soft onboarding requires manual execution. This document provides the complete procedure for soft onboarding all 8 agents in the swarm.

## Agent Configuration

**Current Mode:** 8-agent
**Active Agents:** Agent-1, Agent-2, Agent-3, Agent-4, Agent-5, Agent-6, Agent-7, Agent-8
**Processing Order:** Agent-1, Agent-2, Agent-3, Agent-5, Agent-6, Agent-7, Agent-8, Agent-4

## Soft Onboarding Protocol

Each agent requires a 6-step soft onboarding sequence:

### Step 1: Click Chat Input
- Navigate to Discord interface
- Click on the chat input field for the target agent

### Step 2: Save Session
- Use Ctrl+S or File → Save to preserve current session state

### Step 3: Send Cleanup Prompt
- Send the A++ session closure prompt to prepare agent for onboarding

### Step 4: Open New Tab
- Open a new browser tab for the onboarding process

### Step 5: Navigate to Onboarding
- Navigate to the agent's onboarding interface

### Step 6: Paste Onboarding Message
- Paste the full soft onboarding message with context and actions

## Default Onboarding Message Template

```
## 🛰️ S2A ACTIVATION DIRECTIVE — SWARM ONBOARDING v2.1

**Signal Type:** System → Agent (S2A)
**Priority:** Immediate
**Mode:** Autonomous Execution
**FSM Target State:** ACTIVE

────────────────────────────────────────
⚠️ SHARED WORKSPACE SAFETY (CRITICAL)
────────────────────────────────────────
**Destructive git commands are FORBIDDEN:**
- ❌ `git clean -fd`
- ❌ `git restore .`
- ❌ `rm -rf` on repo paths
- ❌ Deleting untracked files (they may belong to other agents)

**Agent Ownership Boundary:**
- You may modify ONLY `agent_workspaces/{agent_id}/**` (your workspace)
- You may modify ONLY files explicitly assigned in your task
- Any change outside scope → STOP and escalate

**Branch Policy:** Commit directly to `main`. No feature branches.
────────────────────────────────────────

## Operating Cycle (Claim → Sync → Slice → Execute → Validate → Commit → Report)

**1) Load State:**
```bash
# Read inbox and status
cat agent_workspaces/{agent_id}/inbox/*.md
cat agent_workspaces/{agent_id}/status.json
```

**2) Claim One Task (priority order):**
- Inbox directives > active status.json > contract system > MASTER_TASK_LOG.md
```bash
python -m src.services.messaging_cli --agent {agent_id} --get-next-task
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
python tools/working_tree_audit.py --agent {agent_id}
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
```

## Execution Checklist

### Pre-Onboarding Setup
- [ ] Ensure Discord interface is accessible
- [ ] Verify agent workspaces exist: `agent_workspaces/Agent-X/`
- [ ] Confirm messaging system is operational
- [ ] Review current agent status files

### Agent Onboarding Sequence

#### Agent-1 (Priority: Captain Agent)
- [ ] Execute 6-step soft onboarding protocol
- [ ] Verify inbox creation: `agent_workspaces/Agent-1/inbox/`
- [ ] Confirm status.json initialization
- [ ] Test basic messaging functionality

#### Agent-2 through Agent-8 (Parallel Processing)
For each agent in processing order:
- [ ] Execute 6-step soft onboarding protocol
- [ ] Verify workspace isolation
- [ ] Test agent-specific messaging
- [ ] Validate status reporting

### Post-Onboarding Validation

#### System Health Checks
- [ ] All 8 agents show ACTIVE status
- [ ] Inbox directories populated with onboarding messages
- [ ] Status.json files contain proper initialization data
- [ ] No workspace conflicts or permission issues

#### Swarm Coordination Tests
- [ ] Agent-to-agent messaging functional
- [ ] Status synchronization working
- [ ] Task assignment system operational
- [ ] Discord integration active

#### Performance Validation
- [ ] Response times within acceptable ranges
- [ ] Memory usage stable across agents
- [ ] No resource conflicts between agents
- [ ] Error rates at acceptable levels

## Automation Scripts

If GUI automation becomes available, use these scripts:

### Single Agent Test
```bash
python simple_soft_onboard_test.py  # Tests Agent-1
```

### Full Swarm Onboarding
```bash
python soft_onboard_all_agents.py   # Onboards all 8 agents
```

## Troubleshooting

### Common Issues

#### GUI Automation Timeout
**Symptom:** Scripts timeout during execution
**Solution:** Execute manual procedure above
**Prevention:** Ensure proper desktop environment access

#### Workspace Permission Errors
**Symptom:** Agent cannot write to workspace
**Solution:** Check directory permissions and ownership
**Command:** `chmod 755 agent_workspaces/Agent-X/`

#### Messaging System Unavailable
**Symptom:** Agents cannot send/receive messages
**Solution:** Restart messaging services
**Command:** `python -m src.services.messaging_infrastructure`

#### Status Synchronization Issues
**Symptom:** Status.json files not updating
**Solution:** Check file system permissions and agent access
**Command:** `ls -la agent_workspaces/Agent-X/status.json`

## Success Metrics

### Completion Criteria
- [ ] All 8 agents successfully onboarded
- [ ] Zero workspace conflicts
- [ ] Full messaging system functionality
- [ ] Status reporting operational
- [ ] Discord integration active

### Performance Targets
- **Onboarding Time:** < 5 minutes per agent
- **System Stability:** 99.9% uptime during onboarding
- **Error Rate:** < 1% failure rate
- **Response Time:** < 30 seconds average

## Next Steps

After successful soft onboarding:

1. **Task Assignment:** Begin distributing work via MASTER_TASK_LOG.md
2. **Coordination Testing:** Execute A2A coordination scenarios
3. **Performance Monitoring:** Monitor swarm efficiency metrics
4. **Continuous Improvement:** Refine onboarding based on feedback

## Contact

For onboarding assistance or issues:
- **Technical Support:** Agent-1 (Captain)
- **Coordination:** Agent-7 (Infrastructure Lead)
- **Documentation:** Agent-3 (DevOps Specialist)

---

*Soft Onboarding Procedure | Swarm Activation Protocol*
*8-Agent Swarm | Parallel Processing | Enterprise Coordination*