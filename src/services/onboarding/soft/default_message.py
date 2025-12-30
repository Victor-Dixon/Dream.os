"""
<!-- SSOT Domain: integration -->

Default Soft Onboarding Message - S2A Template Content
=======================================================

Default message content for soft onboarding that tells agents to come online
and find out how to act and respond.

This content is used to populate the S2A SOFT_ONBOARDING template's
{context} and {actions} fields.

V2 Compliant: Includes Shared Workspace Safety, Output Contract, and audit requirements.
"""

# Default context for soft onboarding (richer header with FSM state and safety warnings)
DEFAULT_SOFT_ONBOARDING_CONTEXT = (
    "## 🛰️ **S2A ACTIVATION DIRECTIVE — SWARM ONBOARDING v2.1**\n\n"
    "**Signal Type:** System → Agent (S2A)\n"
    "**Priority:** Immediate\n"
    "**Mode:** Autonomous Execution\n"
    "**FSM Target State:** ACTIVE\n\n"
    "────────────────────────────────────────\n"
    "⚠️ **SHARED WORKSPACE SAFETY (CRITICAL)**\n"
    "────────────────────────────────────────\n"
    "**Destructive git commands are FORBIDDEN:**\n"
    "- ❌ `git clean -fd`\n"
    "- ❌ `git restore .`\n"
    "- ❌ `rm -rf` on repo paths\n"
    "- ❌ Deleting untracked files (they may belong to other agents)\n\n"
    "**Agent Ownership Boundary:**\n"
    "- You may modify ONLY `agent_workspaces/{agent_id}/**` (your workspace)\n"
    "- You may modify ONLY files explicitly assigned in your task\n"
    "- Any change outside scope → STOP and escalate\n\n"
    "**Branch Policy:** Commit directly to `main`. No feature branches.\n"
    "────────────────────────────────────────"
)

# Default actions for soft onboarding (atomic instructions with full cycle checklist)
DEFAULT_SOFT_ONBOARDING_ACTIONS = (
    "## Operating Cycle (Claim → Sync → Slice → Execute → Validate → Commit → Report)\n\n"
    "**1) Load State:**\n"
    "```bash\n"
    "# Read inbox and status\n"
    "cat agent_workspaces/{agent_id}/inbox/*.md\n"
    "cat agent_workspaces/{agent_id}/status.json\n"
    "```\n\n"
    "**2) Claim One Task (priority order):**\n"
    "- Inbox directives > active status.json > contract system > MASTER_TASK_LOG.md\n"
    "```bash\n"
    "python -m src.services.messaging_cli --agent {agent_id} --get-next-task\n"
    "```\n\n"
    "**3) Sync with Swarm:**\n"
    "- Check Swarm Brain for patterns (advisory)\n"
    "- Review other agent status.json files for coordination\n\n"
    "**4) Execute One Real Deliverable:**\n"
    "- No narration, no speculation\n"
    "- Produce artifact/result OR 1 blocker (blocker + fix + owner)\n\n"
    "**5) Validate Work:**\n"
    "- Run lints, tests as applicable\n"
    "- Verify changes work as expected\n\n"
    "**6) Commit Changes:**\n"
    "```bash\n"
    "git add <your-files-only>  # Explicit paths, NOT git add .\n"
    "git commit -m \"Agent-X: Brief description\"\n"
    "git push\n"
    "```\n\n"
    "**7) Report Evidence:**\n"
    "- Update status.json (task, progress, blockers)\n"
    "- Post to Discord with artifact/validation/delegation\n\n"
    "────────────────────────────────────────\n"
    "**SESSION CLOSURE REQUIREMENT**\n"
    "────────────────────────────────────────\n"
    "Before ending session, run working-tree audit:\n"
    "```bash\n"
    "python tools/working_tree_audit.py --agent {agent_id}\n"
    "```\n\n"
    "Then complete SESSION CLOSURE ritual using:\n"
    "- Template: `templates/session-closure-template.md`\n"
    "- Validator: `python tools/validate_closure_format.py`\n"
    "- Rules: `.cursor/rules/session-closure.mdc`\n"
)


def get_output_contract_stub() -> str:
    """
    Return the 10-line A++ Output Contract skeleton for copy-paste.
    
    Returns:
        String containing the A++ closure format skeleton
    """
    return (
        "────────────────────────────────────────\n"
        "**OUTPUT CONTRACT (STRICT - A++ FORMAT)**\n"
        "────────────────────────────────────────\n"
        "```markdown\n"
        "- **Task:** [Brief task description]\n"
        "- **Project:** [Project/repo name]\n"
        "\n"
        "- **Actions Taken:**\n"
        "  - [Factual action 1]\n"
        "  - [Factual action 2]\n"
        "\n"
        "- **Artifacts Created / Updated:**\n"
        "  - [Exact file path]\n"
        "\n"
        "- **Verification:**\n"
        "  - [Proof with commit hash/command output/message ID]\n"
        "\n"
        "- **Public Build Signal:**\n"
        "  [ONE sentence - what changed]\n"
        "\n"
        "- **Git Commit:** [hash or \"Not committed\"]\n"
        "- **Git Push:** [Pushed to main or \"Not pushed\"]\n"
        "- **Website Blogging:** [URL or \"Not published\"]\n"
        "\n"
        "- **Status:** ✅ Ready OR 🟡 Blocked (reason)\n"
        "```\n"
        "────────────────────────────────────────"
    )


def get_default_soft_onboarding_message(agent_id: str) -> tuple[str, str]:
    """
    Get default soft onboarding context and actions for an agent.
    
    Args:
        agent_id: Target agent ID (e.g., "Agent-1")
        
    Returns:
        Tuple of (context, actions) strings for the S2A SOFT_ONBOARDING template
    """
    context = DEFAULT_SOFT_ONBOARDING_CONTEXT.format(agent_id=agent_id)
    actions = DEFAULT_SOFT_ONBOARDING_ACTIONS.format(agent_id=agent_id)
    
    # Append output contract stub to actions
    actions += "\n\n" + get_output_contract_stub()
    
    return context, actions


def get_full_onboarding_message(agent_id: str) -> str:
    """
    Get the complete onboarding message with context, actions, and output contract.
    
    Args:
        agent_id: Target agent ID (e.g., "Agent-1")
        
    Returns:
        Complete onboarding message string
    """
    context, actions = get_default_soft_onboarding_message(agent_id)
    return f"{context}\n\n{actions}"
