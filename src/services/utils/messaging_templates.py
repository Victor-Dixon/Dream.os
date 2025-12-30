"""
<!-- SSOT Domain: integration -->

Messaging CLI Templates
======================
Message templates for CLI operations. Enhanced with validation and structure.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
V2 Compliant: <300 lines
"""

from typing import Dict, Any, Optional
from datetime import datetime


def validate_template_vars(template: str, vars_dict: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate that all template variables are provided.
    
    Args:
        template: Template string with {variable} placeholders
        vars_dict: Dictionary of variables to substitute
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import re
    required_vars = set(re.findall(r'\{(\w+)\}', template))
    provided_vars = set(vars_dict.keys())
    missing_vars = required_vars - provided_vars
    
    if missing_vars:
        return False, f"Missing template variables: {', '.join(missing_vars)}"
    return True, None


def format_template(template: str, **kwargs) -> str:
    """
    Format template with validation.
    
    Args:
        template: Template string
        **kwargs: Template variables
        
    Returns:
        Formatted string
        
    Raises:
        ValueError: If required variables are missing
    """
    is_valid, error = validate_template_vars(template, kwargs)
    if not is_valid:
        raise ValueError(error)
    return template.format(**kwargs)


CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" \\
    --agent Agent-2 --priority urgent --tags bug critical

🐝 WE. ARE. SWARM - COORDINATE THROUGH PYAUTOGUI!
"""

SURVEY_MESSAGE_TEMPLATE = """
🐝 SWARM SURVEY INITIATED - SRC/ DIRECTORY ANALYSIS
================================================

**OBJECTIVE:** Comprehensive analysis of src/ directory for consolidation planning
**TARGET:** 683 → ~250 files with full functionality preservation

**PHASES:**
1. Structural Analysis (Directories, files, dependencies)
2. Functional Analysis (Services, capabilities, relationships)
3. Quality Assessment (V2 compliance, violations, anti-patterns)
4. Consolidation Planning (Opportunities, risks, rollback strategies)

**COORDINATION:** Real-time via PyAutoGUI messaging system
**COMMANDER:** Captain Agent-4 (Quality Assurance Specialist)

🐝 WE ARE SWARM - UNITED IN ANALYSIS!
"""

ASSIGNMENT_MESSAGE_TEMPLATE = """
🐝 SURVEY ASSIGNMENT - {agent}
============================

**ROLE:** {assignment}

**DELIVERABLES:**
1. Structural Analysis Report
2. Functional Analysis Report
3. Quality Assessment Report
4. Consolidation Recommendations

**TIMELINE:** 8 days total survey
**COORDINATION:** Real-time via PyAutoGUI

🐝 YOUR EXPERTISE IS CRUCIAL FOR SUCCESSFUL CONSOLIDATION!
"""

CONSOLIDATION_MESSAGE_TEMPLATE = """
🔧 CONSOLIDATION UPDATE
======================

**BATCH:** {batch}
**STATUS:** {status}
**TIMESTAMP:** {timestamp}

**COORDINATION:** Real-time swarm coordination active
**COMMANDER:** Captain Agent-4

🔧 CONSOLIDATION PROGRESS CONTINUES...
"""

# Enhanced templates with better structure
BROADCAST_TEMPLATE = """
🚨 BROADCAST MESSAGE 🚨

**FROM:** {sender}
**PRIORITY:** {priority}
**TIMESTAMP:** {timestamp}

---

{content}

---

🐝 WE. ARE. SWARM. ⚡🔥
"""

TASK_ASSIGNMENT_TEMPLATE = """
📋 TASK ASSIGNMENT - {agent}

**TASK:** {task_name}
**PRIORITY:** {priority}
**DEADLINE:** {deadline}
**DESCRIPTION:** {description}

**DELIVERABLES:**
{deliverables}

**COORDINATION:** Contact Captain Agent-4 for questions

🐝 WE. ARE. SWARM. ⚡🔥
"""

STATUS_UPDATE_TEMPLATE = """
📊 STATUS UPDATE REQUEST

**AGENT:** {agent}
**REQUESTED BY:** {requester}
**TIMESTAMP:** {timestamp}

Please provide current status update including:
- Current tasks
- Progress on active assignments
- Blockers or issues
- Next actions

🐝 WE. ARE. SWARM. ⚡🔥
"""

URGENT_ALERT_TEMPLATE = """
🚨 URGENT ALERT 🚨

**FROM:** {sender}
**TO:** {recipient}
**PRIORITY:** URGENT
**TIMESTAMP:** {timestamp}

{content}

**ACTION REQUIRED:** Immediate response requested

🐝 WE. ARE. SWARM. ⚡🔥
"""


def get_broadcast_template(sender: str, content: str, priority: str = "normal") -> str:
    """Get formatted broadcast message."""
    return format_template(
        BROADCAST_TEMPLATE,
        sender=sender,
        priority=priority.upper(),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        content=content
    )


def get_task_assignment_template(
    agent: str,
    task_name: str,
    description: str,
    priority: str = "normal",
    deadline: str = "TBD",
    deliverables: str = "- Complete assigned task"
) -> str:
    """Get formatted task assignment message."""
    return format_template(
        TASK_ASSIGNMENT_TEMPLATE,
        agent=agent,
        task_name=task_name,
        priority=priority.upper(),
        deadline=deadline,
        description=description,
        deliverables=deliverables
    )


def get_status_update_template(agent: str, requester: str = "Captain Agent-4") -> str:
    """Get formatted status update request."""
    return format_template(
        STATUS_UPDATE_TEMPLATE,
        agent=agent,
        requester=requester,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


def get_urgent_alert_template(sender: str, recipient: str, content: str) -> str:
    """Get formatted urgent alert message."""
    return format_template(
        URGENT_ALERT_TEMPLATE,
        sender=sender,
        recipient=recipient,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        content=content
    )
