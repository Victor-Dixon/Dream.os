#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Message Plans - V2 Compliant
=============================

Message plan building for overnight operations.
Extracted from V1 overnight_runner/runner.py message plan patterns.

Provides different work strategies:
- contracts: Contract-based work
- autonomous-dev: Self-directed development
- fsm-driven: FSM task-driven workflow
- single-repo-beta: Focused beta-readiness
- prd-milestones: PRD milestone alignment

V2 Compliance: ≤400 lines, proper structure
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

# V2 Integration imports
try:
    from ...core.unified_logging_system import get_logger
    from ...core.constants.paths import ROOT_DIR
except ImportError as e:
    import logging
    logging.warning(f"V2 integration imports failed: {e}")
    def get_logger(name):
        return logging.getLogger(name)
    ROOT_DIR = None

logger = get_logger(__name__)


class MessageTag(Enum):
    """Message tag types for overnight operations."""
    RESUME = "resume"
    TASK = "task"
    COORDINATE = "coordinate"
    SYNC = "sync"
    VERIFY = "verify"
    CAPTAIN = "captain"


@dataclass
class PlannedMessage:
    """Planned message structure."""
    tag: MessageTag
    template: str  # Accepts {agent} placeholder


def build_message_plan(plan: str, repos_root: Optional[str] = None) -> List[PlannedMessage]:
    """
    Build message plan based on strategy.
    
    Args:
        plan: Plan name (contracts, autonomous-dev, fsm-driven, etc.)
        repos_root: Optional repos root path for plan-specific messages
        
    Returns:
        List of planned messages
    """
    plan = plan.lower()
    
    # Contracts mode - Contract-based work
    if plan == "contracts":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} review your assigned contracts in inbox and the repo TASK_LIST.md. "
                "Update TASK_LIST.md with next verifiable steps."
            ),
            PlannedMessage(
                MessageTag.TASK,
                "{agent} complete one contract to acceptance criteria. "
                "Commit small, verifiable edits; attach evidence."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} post a contract update to Agent-5: task_id, current state, next action, evidence links."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} 10-min contract sync: changed, state per task_id, risks, next verifiable action."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify acceptance criteria and tests/build. "
                "Provide evidence. If blocked, stage diffs and summarize."
            ),
        ]
    
    # Autonomous development mode
    if plan == "autonomous-dev":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume autonomous development. "
                "Choose the highest-leverage task from your assigned repos and begin now."
            ),
            PlannedMessage(
                MessageTag.TASK,
                "{agent} implement one concrete improvement (tests/build/lint/docs/refactor). "
                "Prefer reuse over new code. Commit in small, verifiable edits."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} prompt a peer agent with your next step and ask for a quick sanity check. "
                "Incorporate feedback, avoid duplication."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} 10-min sync: what changed, open TODO, and the next verifiable action. "
                "Keep momentum; avoid placeholders."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify outcomes (tests/build). "
                "If blocked by permissions, stage diffs and summarize impact + next steps for review."
            ),
        ]
    
    # FSM-driven mode
    if plan == "fsm-driven":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume: check FSM inbox for assigned tasks. "
                "Review current task state and evidence requirements."
            ),
            PlannedMessage(
                MessageTag.TASK,
                "{agent} execute one verifiable step on assigned FSM task. "
                "Commit with tests/build evidence; send fsm_update to Agent-5."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} coordinate: declare current task_id and state to avoid duplication. "
                "Post progress updates to Agent-5 inbox for FSM processing."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} 10-min FSM sync: task state, evidence collected, next verifiable action."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify task completion criteria. "
                "Send final fsm_update with evidence to Agent-5."
            ),
        ]
    
    # Single-repo beta-readiness mode
    if plan == "single-repo-beta":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume: focus the target repo to reach beta-ready."
            ),
            PlannedMessage(
                MessageTag.TASK,
                "{agent} implement one concrete step toward beta-ready in the focus repo."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} coordinate to avoid duplication; declare your focus area in the repo."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} 10-min sync: status vs beta-ready checklist for the focus repo; next verifiable step."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify beta-ready criteria (GUI flows/tests). "
                "Attach evidence; summarize gaps if any."
            ),
        ]
    
    # PRD milestones mode
    if plan == "prd-milestones":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume: align to PRD milestones; pick next milestone and extract a small, verifiable task."
            ),
            PlannedMessage(
                MessageTag.TASK,
                "{agent} implement one step tied to the current PRD milestone; "
                "commit with tests/build evidence."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} coordinate on milestone ownership to avoid duplication; "
                "declare your current milestone ID."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} 10-min sync: status vs active milestone; next verifiable step; risks."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify acceptance against the milestone's criteria; "
                "attach evidence and summary."
            ),
        ]
    
    # Resume-only mode (minimal)
    if plan == "resume-only":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume autonomous operations. Continue working overnight. Summarize hourly."
            )
        ]
    
    # Resume-task-sync mode (default fallback)
    if plan == "resume-task-sync":
        repos_line = f" under {repos_root}" if repos_root else ""
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume operations. Maintain uninterrupted focus. Report blockers."
            ),
            PlannedMessage(
                MessageTag.TASK,
                f"{{agent}} choose highest-impact repo{repos_line}. Ship 1 measurable improvement."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} coordinate with team. Hand off incomplete work with clear next steps."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} 30-min sync: brief status, next step, risks."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify tests/build. If blocked by approvals, prepare changes and summaries."
            ),
        ]
    
    # Aggressive mode
    if plan == "aggressive":
        return [
            PlannedMessage(
                MessageTag.RESUME,
                "{agent} resume now. Prioritize compilers: tests/build>lint>docs>CI."
            ),
            PlannedMessage(
                MessageTag.TASK,
                "{agent} implement 1-2 fixes from failing tests or lints. Stage diffs with clear messages."
            ),
            PlannedMessage(
                MessageTag.COORDINATE,
                "{agent} request handoff from peers. Consolidate partial work into a single branch plan."
            ),
            PlannedMessage(
                MessageTag.SYNC,
                "{agent} sync: what changed, what remains, ETA by next cycle."
            ),
            PlannedMessage(
                MessageTag.VERIFY,
                "{agent} verify outcomes. Prepare a concise summary for morning review."
            ),
        ]
    
    # Default fallback
    logger.warning(f"Unknown plan '{plan}', using 'resume-task-sync' as fallback")
    return build_message_plan("resume-task-sync", repos_root)


def get_available_plans() -> List[str]:
    """Get list of available message plans."""
    return [
        "contracts",
        "autonomous-dev",
        "fsm-driven",
        "single-repo-beta",
        "prd-milestones",
        "resume-only",
        "resume-task-sync",
        "aggressive",
    ]


def format_message(planned: PlannedMessage, agent: str, **kwargs) -> str:
    """
    Format a planned message with agent name and optional variables.
    
    Args:
        planned: Planned message
        agent: Agent ID
        **kwargs: Additional variables for template formatting
        
    Returns:
        Formatted message string
    """
    message = planned.template.format(agent=agent, **kwargs)
    return message


if __name__ == "__main__":
    # Example usage
    logger.info("Message Plans module loaded")
    logger.info(f"Available plans: {', '.join(get_available_plans())}")
    
    # Test a plan
    plan = build_message_plan("contracts")
    logger.info(f"Contracts plan has {len(plan)} messages")
    for msg in plan:
        formatted = format_message(msg, "Agent-1")
        logger.info(f"  {msg.tag.value}: {formatted[:60]}...")

