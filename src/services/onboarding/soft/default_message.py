"""
Default Soft Onboarding Message - S2A Template Content
=======================================================

Default message content for soft onboarding that tells agents to come online
and find out how to act and respond.

This content is used to populate the S2A SOFT_ONBOARDING template's
{context} and {actions} fields.
"""

# Default context for soft onboarding
DEFAULT_SOFT_ONBOARDING_CONTEXT = (
    "## 🛰️ **S2A ACTIVATION DIRECTIVE — SWARM ONBOARDING v2.0**\n\n"
    "**Signal Type:** System → Agent (S2A)\n"
    "**Priority:** Immediate\n"
    "**Mode:** Autonomous Execution"
)

# Default actions for soft onboarding (atomic instructions, no acknowledgments)
DEFAULT_SOFT_ONBOARDING_ACTIONS = (
    "1) Load state:\n"
    "- Read: agent_workspaces/{agent_id}/inbox/\n"
    "- Read: agent_workspaces/{agent_id}/status.json\n\n"
    "2) Claim one objective (in order):\n"
    "- Inbox directives > active status.json > contract system > MASTER_TASK_LOG.md\n"
    "- Command:\n"
    "  python -m src.services.messaging_cli --agent {agent_id} --get-next-task\n\n"
    "3) Execute one real deliverable now.\n"
    "- No narration.\n"
    "- Produce artifact/result or 1 blocker (blocker + fix + owner).\n\n"
    "4) Maintain state:\n"
    "- Update status.json (task, progress, blockers)\n"
    "- Log decisions only if they change future work\n\n"
    "5) If ending session: run SESSION CLOSURE ritual (use the provided cleanup prompt).\n"
)

def get_default_soft_onboarding_message(agent_id: str) -> tuple[str, str]:
    """
    Get default soft onboarding context and actions for an agent.
    
    Args:
        agent_id: Target agent ID (e.g., "Agent-1")
        
    Returns:
        Tuple of (context, actions) strings for the S2A SOFT_ONBOARDING template
    """
    context = DEFAULT_SOFT_ONBOARDING_CONTEXT
    actions = DEFAULT_SOFT_ONBOARDING_ACTIONS.format(agent_id=agent_id)
    return context, actions

