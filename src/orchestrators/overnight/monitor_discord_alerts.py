"""

<!-- SSOT Domain: monitoring -->
Monitor Discord Alerts - Discord Router Integration
===================================================

Sends Discord alerts when stalled agents are detected.
Integrates with Discord router for agent-specific channel notifications.

V2 Compliance: ≤300 lines, single responsibility, comprehensive error handling.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
"""

import os
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from src.core.config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


def get_agent_webhook(agent_id: str) -> Optional[str]:
    """

<!-- SSOT Domain: monitoring -->
    Get Discord webhook URL for an agent.
    
    Args:
        agent_id: Agent identifier (e.g., "Agent-2")
        
    Returns:
        Webhook URL or None if not configured
    """
    # Normalize agent ID
    agent_normalized = agent_id.lower().replace("-", "_")
    agent_number = agent_id.split("-")[-1] if "-" in agent_id else None
    
    # Try multiple environment variable formats
    webhook_vars = [
        f"DISCORD_WEBHOOK_{agent_normalized.upper()}",
        f"DISCORD_{agent_normalized.upper()}_WEBHOOK",
        f"DISCORD_AGENT{agent_number}_WEBHOOK" if agent_number else None,
        "DISCORD_ROUTER_WEBHOOK_URL",
        "DISCORD_WEBHOOK_URL",
    ]
    
    for var in webhook_vars:
        if var and os.getenv(var):
            return os.getenv(var)
    
    return None


def send_stall_alert(agent_id: str, stall_duration_seconds: float, activity_details: Dict[str, Any]) -> bool:
    """

<!-- SSOT Domain: monitoring -->
    Send Discord alert for stalled agent.
    
    Args:
        agent_id: Agent identifier
        stall_duration_seconds: How long agent has been stalled
        activity_details: Activity detection details
        
    Returns:
        True if alert sent successfully, False otherwise
    """
    webhook_url = get_agent_webhook(agent_id)
    
    if not webhook_url:
        logger.warning(f"⚠️ No Discord webhook configured for {agent_id}")
        return False
    
    # Format stall duration
    minutes = int(stall_duration_seconds / 60)
    hours = int(minutes / 60)
    if hours > 0:
        duration_str = f"{hours}h {minutes % 60}m"
    else:
        duration_str = f"{minutes}m"
    
    # Get activity source info
    activity_sources = activity_details.get("activity_sources", [])
    latest_source = activity_details.get("latest_source", "none")
    
    # Create alert message
    content = f"""## 🚨 Agent Stall Alert
<!-- SSOT Domain: monitoring -->

**Agent**: {agent_id}
**Stall Duration**: {duration_str}
**Last Activity Source**: {latest_source}
**Activity Sources Checked**: {len(activity_sources)}

### Activity Details:
- **Latest Activity**: {datetime.fromtimestamp(activity_details.get('latest_activity', 0)).strftime('%Y-%m-%d %H:%M:%S') if activity_details.get('latest_activity', 0) > 0 else 'None'}
- **Activity Sources**: {', '.join(activity_sources) if activity_sources else 'None detected'}

### Action Required:
Agent has been stalled for {duration_str}. Recovery system will attempt to rescue the agent.

*Alert sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    payload = {
        "content": content,
        "username": "Status Monitor",
        "avatar_url": None,
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=TimeoutConstants.HTTP_SHORT)
        response.raise_for_status()
        logger.info(f"✅ Discord alert sent for {agent_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send Discord alert for {agent_id}: {e}")
        return False


def send_recovery_alert(agent_id: str, recovery_status: str, details: Optional[str] = None) -> bool:
    """

<!-- SSOT Domain: monitoring -->
    Send Discord alert for recovery action.
    
    Args:
        agent_id: Agent identifier
        recovery_status: Status of recovery ("attempted", "succeeded", "failed")
        details: Additional details about recovery
        
    Returns:
        True if alert sent successfully, False otherwise
    """
    webhook_url = get_agent_webhook(agent_id)
    
    if not webhook_url:
        logger.warning(f"⚠️ No Discord webhook configured for {agent_id}")
        return False
    
    # Create recovery message
    emoji = "✅" if recovery_status == "succeeded" else "🔄" if recovery_status == "attempted" else "❌"
    
    content = f"""## {emoji} Agent Recovery Alert
<!-- SSOT Domain: monitoring -->

**Agent**: {agent_id}
**Recovery Status**: {recovery_status.upper()}
{f'**Details**: {details}' if details else ''}

*Alert sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    payload = {
        "content": content,
        "username": "Status Monitor",
        "avatar_url": None,
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=TimeoutConstants.HTTP_SHORT)
        response.raise_for_status()
        logger.info(f"✅ Recovery alert sent for {agent_id}: {recovery_status}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send recovery alert for {agent_id}: {e}")
        return False


def send_health_alert(issues: List[str], health_status: Dict[str, Any]) -> bool:
    """

<!-- SSOT Domain: monitoring -->
    Send Discord alert for system health issues.
    
    Args:
        issues: List of health issues
        health_status: Full health status information
        
    Returns:
        True if alert sent successfully, False otherwise
    """
    # Use general webhook or router webhook
    webhook_url = (
        os.getenv("DISCORD_ROUTER_WEBHOOK_URL") or
        os.getenv("DISCORD_WEBHOOK_URL")
    )
    
    if not webhook_url:
        logger.warning("⚠️ No Discord webhook configured for health alerts")
        return False
    
    content = f"""## 🚨 System Health Alert
<!-- SSOT Domain: monitoring -->

**Issues Detected**: {len(issues)}
**Health Status**: {'❌ UNHEALTHY' if not health_status.get('healthy', True) else '⚠️ DEGRADED'}

### Issues:
{chr(10).join(f'- {issue}' for issue in issues)}

### Health Metrics:
- **Completion Rate**: {health_status.get('completion_rate', 0):.1%}
- **Failure Rate**: {health_status.get('failure_rate', 0):.1%}
- **Stalled Agents**: {len(health_status.get('stalled_agents', []))}

*Alert sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    payload = {
        "content": content,
        "username": "Status Monitor",
        "avatar_url": None,
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=TimeoutConstants.HTTP_SHORT)
        response.raise_for_status()
        logger.info(f"✅ Health alert sent: {len(issues)} issues")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send health alert: {e}")
        return False


