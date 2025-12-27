#!/usr/bin/env python3
"""
Cycle Accomplishments Report Generator
======================================

**PROTOCOL:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION
**PROTOCOL_VERSION:** 1.0
**PROTOCOL_STATUS:** ACTIVE

Generates a comprehensive cycle accomplishments report by aggregating
accomplishments, completed tasks, and achievements from all agent status files.

**PROTOCOL USAGE:**
    python tools/generate_cycle_accomplishments_report.py

**PROTOCOL OUTPUT:**
    - Markdown file: reports/cycle_accomplishments_YYYY-MM-DD_HHMMSS.md
    - Discord post: Automatic summary posted to Agent-4 (Captain) channel

**PROTOCOL TRIGGERS:**
    - Manual execution: Run script directly
    - Automatic execution: Called by soft_onboard_multiple_agents() when generate_cycle_report=True
    - Post-cycle summary: Run after significant swarm activity cycles

**PROTOCOL DATA SOURCES:**
    - agent_workspaces/Agent-X/status.json (all agents)
    - Extracts: completed_tasks, achievements, current_tasks, current_mission

**PROTOCOL INTEGRATION:**
    - Referenced in: src/services/onboarding/soft/service.py (line 180)
    - Called by: soft_onboard_multiple_agents() function
    - Protocol flag: generate_cycle_report parameter

**PROTOCOL NOTES:**
    - Report includes all agents with valid status.json files
    - Agents with JSON parsing errors are skipped with warnings
    - Report format: Markdown with agent sections, summaries, and metadata
    - **This is the PRIMARY tool for comprehensive all-agents cycle reports**
    - For Captain metrics only, use `CycleReportTool` (captain.cycle_report)
    - See: `docs/CYCLE_REPORT_TOOLS_COMPARISON.md` for tool selection guide
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import logging

# Setup basic logging if logging_config not available
try:
    from src.core.config.logging_config import setup_logging
    setup_logging()
except ImportError:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

AGENT_WORKSPACES_ROOT = project_root / "agent_workspaces"
REPORTS_ROOT = project_root / "reports"


def post_cycle_report_to_discord(report_file: Path, accomplishments: List[Dict[str, Any]]) -> bool:
    """
    Post cycle accomplishments report to Discord.
    
    PROTOCOL: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION
    Posts summary to Captain's channel (Agent-4) or general channel.
    """
    try:
        # Import Discord posting tools
        from tools.categories.communication_tools import DiscordRouterPoster
        
        # Create summary for Discord (truncate if needed)
        total_agents = len(accomplishments)
        total_completed = sum(len(a.get('completed_tasks', [])) for a in accomplishments)
        total_achievements = sum(len(a.get('achievements', [])) for a in accomplishments)
        
        summary = f"""📊 **Cycle Accomplishments Report Generated**

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Total Agents:** {total_agents}
**Total Completed Tasks:** {total_completed}
**Total Achievements:** {total_achievements}

**Report File:** `{report_file.name}`

Full report available in: `reports/cycle_accomplishments_*.md`

*Generated via PROTOCOL: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v1.0*
"""
        
        # Post to Captain's channel (Agent-4)
        poster = DiscordRouterPoster()
        result = poster.post_update(
            agent_id="Agent-4",
            message=summary,
            title="Cycle Accomplishments Report",
            priority="normal"
        )
        
        if result.get("success"):
            logger.info("✅ Cycle accomplishments report posted to Discord")
            return True
        else:
            logger.warning(f"⚠️  Failed to post to Discord: {result.get('error', 'Unknown error')}")
            return False
            
    except ImportError:
        logger.warning("⚠️  DiscordRouterPoster not available, skipping Discord post")
        return False
    except Exception as e:
        logger.error(f"❌ Error posting to Discord: {e}")
        return False


def load_agent_status(agent_id: str) -> Dict[str, Any]:
    """Load agent status.json file."""
    status_file = AGENT_WORKSPACES_ROOT / agent_id / "status.json"
    if not status_file.exists():
        logger.warning(f"Status file not found for {agent_id}: {status_file}")
        return {}
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load status for {agent_id}: {e}")
        return {}


def extract_agent_accomplishments(agent_id: str, status: Dict[str, Any]) -> Dict[str, Any]:
    """Extract accomplishments, completed tasks, and achievements from agent status."""
    return {
        "agent_id": agent_id,
        "agent_name": status.get("agent_name", "Unknown"),
        "status": status.get("status", "UNKNOWN"),
        "current_mission": status.get("current_mission", ""),
        "mission_priority": status.get("mission_priority", ""),
        "completed_tasks": status.get("completed_tasks", []),
        "achievements": status.get("achievements", []),
        "current_tasks": status.get("current_tasks", []),
        "last_updated": status.get("last_updated", ""),
    }


def format_accomplishments_report(accomplishments: List[Dict[str, Any]]) -> str:
    """Format accomplishments into markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# Cycle Accomplishments Report

**Generated:** {timestamp}  
**Date:** {date_str}  
**Agents:** {len(accomplishments)}

---

## Summary

This report aggregates accomplishments, completed tasks, and achievements from all active agents during this cycle.

**Total Agents:** {len(accomplishments)}  
**Total Completed Tasks:** {sum(len(a.get('completed_tasks', [])) for a in accomplishments)}  
**Total Achievements:** {sum(len(a.get('achievements', [])) for a in accomplishments)}

---

"""
    
    for agent_data in accomplishments:
        agent_id = agent_data["agent_id"]
        agent_name = agent_data["agent_name"]
        status = agent_data["status"]
        mission = agent_data["current_mission"]
        priority = agent_data["mission_priority"]
        completed_tasks = agent_data.get("completed_tasks", [])
        achievements = agent_data.get("achievements", [])
        current_tasks = agent_data.get("current_tasks", [])
        last_updated = agent_data.get("last_updated", "")
        
        report += f"""## {agent_id}: {agent_name}

**Status:** {status}  
**Priority:** {priority}  
**Last Updated:** {last_updated}

### Current Mission
{mission}

### Completed Tasks ({len(completed_tasks)})
"""
        
        if completed_tasks:
            for task in completed_tasks[:20]:  # Limit to 20 most recent
                report += f"- {task}\n"
            if len(completed_tasks) > 20:
                report += f"\n*... and {len(completed_tasks) - 20} more completed tasks*\n"
        else:
            report += "*No completed tasks recorded*\n"
        
        report += f"\n### Achievements ({len(achievements)})\n"
        
        if achievements:
            for achievement in achievements[:15]:  # Limit to 15 most recent
                report += f"- {achievement}\n"
            if len(achievements) > 15:
                report += f"\n*... and {len(achievements) - 15} more achievements*\n"
        else:
            report += "*No achievements recorded*\n"
        
        report += f"\n### Active Tasks ({len(current_tasks)})\n"
        
        if current_tasks:
            # Show most recent active tasks
            recent_tasks = [t for t in current_tasks if not t.startswith("✅")][:10]
            if not recent_tasks:
                recent_tasks = current_tasks[:10]
            
            for task in recent_tasks:
                report += f"- {task}\n"
            if len(current_tasks) > 10:
                report += f"\n*... and {len(current_tasks) - 10} more active tasks*\n"
        else:
            report += "*No active tasks recorded*\n"
        
        report += "\n---\n\n"
    
    report += f"""
## Report Metadata

**Generated By:** Cycle Accomplishments Report Generator  
**Protocol:** Soft Onboarding Cycle Report Generation  
**Format:** Markdown  
**Timestamp:** {timestamp}

---

*This report is automatically generated from agent status.json files.*
"""
    
    return report


def generate_cycle_accomplishments_report() -> Path:
    """Generate cycle accomplishments report from all agent status files."""
    logger.info("📊 Generating cycle accomplishments report...")
    
    # Find all agent directories
    agent_dirs = [d for d in AGENT_WORKSPACES_ROOT.iterdir() 
                  if d.is_dir() and d.name.startswith("Agent-")]
    
    accomplishments = []
    
    for agent_dir in sorted(agent_dirs):
        agent_id = agent_dir.name
        status = load_agent_status(agent_id)
        
        if status:
            agent_data = extract_agent_accomplishments(agent_id, status)
            accomplishments.append(agent_data)
            logger.info(f"✅ Loaded accomplishments for {agent_id}")
        else:
            logger.warning(f"⚠️  No status data for {agent_id}")
    
    if not accomplishments:
        logger.error("❌ No agent accomplishments found!")
        return None
    
    # Generate report
    report_content = format_accomplishments_report(accomplishments)
    
    # Save report
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_ROOT / f"cycle_accomplishments_{timestamp_str}.md"
    
    REPORTS_ROOT.mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    logger.info(f"✅ Cycle accomplishments report generated: {report_file}")
    print(f"Report generated: {report_file}")
    
    # Post to Discord (PROTOCOL: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION)
    try:
        logger.info("📢 Posting cycle accomplishments report to Discord...")
        post_cycle_report_to_discord(report_file, accomplishments)
    except Exception as e:
        logger.warning(f"⚠️  Failed to post cycle report to Discord: {e}")
        # Don't fail the entire report generation if Discord posting fails
    
    return report_file


def main():
    """Main entry point."""
    try:
        report_file = generate_cycle_accomplishments_report()
        if report_file:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Failed to generate cycle accomplishments report: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

