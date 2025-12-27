#!/usr/bin/env python3
"""
Unified Cycle Accomplishments Report Generator
==============================================

**PROTOCOL:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION
**PROTOCOL_VERSION:** 2.0 (Unified)
**PROTOCOL_STATUS:** ACTIVE

Merged capabilities from:
- generate_cycle_accomplishments_report.py (all-agents comprehensive report)
- CycleReportTool (Captain metrics)
- generate_daily_episode.py (accomplishments extraction logic)

Generates a comprehensive cycle accomplishments report with:
1. All-agents accomplishments (from status.json files)
2. Captain metrics (optional manual input)
3. Unified markdown report
4. Discord posting to Agent-4 channel

**USAGE:**
    # Generate all-agents report (default)
    python tools/unified_cycle_accomplishments_report.py

    # Include Captain metrics
    python tools/unified_cycle_accomplishments_report.py --captain-metrics --cycle-number 123 --missions 5 --messages 10

    # Specify date
    python tools/unified_cycle_accomplishments_report.py --date 2025-12-26

**OUTPUT:**
    - Markdown file: reports/cycle_accomplishments_YYYY-MM-DD_HHMMSS.md
    - Discord post: Automatic summary posted to Agent-4 (Captain) channel

**DATA SOURCES:**
    - agent_workspaces/Agent-X/status.json (all agents)
    - Extracts: completed_tasks, achievements, current_tasks, current_mission
    - Optional: Captain metrics (cycle_number, missions_assigned, messages_sent, agents_activated, points_awarded, notes)
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to sys.path for imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import logging

# Setup basic logging
try:
    from src.core.config.logging_config import setup_logging
    setup_logging()
except ImportError:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

AGENT_WORKSPACES_ROOT = project_root / "agent_workspaces"
REPORTS_ROOT = project_root / "reports"


def load_agent_status(agent_id: str) -> Dict[str, Any]:
    """Load agent status.json file."""
    status_file = AGENT_WORKSPACES_ROOT / agent_id / "status.json"
    if not status_file.exists():
        logger.warning(f"Status file not found for {agent_id}: {status_file}")
        return {}
    
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON for {agent_id}: {e}")
        return {}
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


def format_captain_metrics_section(
    cycle_number: Optional[int] = None,
    missions_assigned: int = 0,
    messages_sent: int = 0,
    agents_activated: List[str] = None,
    points_awarded: int = 0,
    notes: str = ""
) -> str:
    """Format Captain metrics section (from CycleReportTool capability)."""
    if cycle_number is None:
        return ""
    
    agents_activated = agents_activated or []
    
    section = f"""## 🎯 CAPTAIN'S CYCLE METRICS #{cycle_number}

**Cycle Number:** {cycle_number}  
**Missions Assigned:** {missions_assigned}  
**Messages Sent:** {messages_sent}  
**Agents Activated:** {len(agents_activated)}  
**Points Awarded:** {points_awarded}

### Agents Activated
"""
    if agents_activated:
        for agent in agents_activated:
            section += f"- {agent}\n"
    else:
        section += "*None this cycle*\n"
    
    if notes:
        section += f"\n### Cycle Notes\n\n{notes}\n"
    
    section += "\n---\n\n"
    
    return section


def format_accomplishments_report(
    accomplishments: List[Dict[str, Any]],
    captain_metrics: Optional[Dict[str, Any]] = None
) -> str:
    """Format accomplishments into unified markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    total_completed = sum(len(a.get('completed_tasks', [])) for a in accomplishments)
    total_achievements = sum(len(a.get('achievements', [])) for a in accomplishments)
    
    report = f"""# Cycle Accomplishments Report

**Generated:** {timestamp}  
**Date:** {date_str}  
**Agents:** {len(accomplishments)}

---

## Summary

This report aggregates accomplishments, completed tasks, and achievements from all active agents during this cycle.

**Total Agents:** {len(accomplishments)}  
**Total Completed Tasks:** {total_completed}  
**Total Achievements:** {total_achievements}

---

"""
    
    # Add Captain metrics section if provided
    if captain_metrics:
        report += format_captain_metrics_section(
            cycle_number=captain_metrics.get("cycle_number"),
            missions_assigned=captain_metrics.get("missions_assigned", 0),
            messages_sent=captain_metrics.get("messages_sent", 0),
            agents_activated=captain_metrics.get("agents_activated", []),
            points_awarded=captain_metrics.get("points_awarded", 0),
            notes=captain_metrics.get("notes", "")
        )
    
    # Add agent accomplishments sections
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

**Generated By:** Unified Cycle Accomplishments Report Generator  
**Protocol:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0 (Unified)  
**Format:** Markdown  
**Timestamp:** {timestamp}

---

*This report is automatically generated from agent status.json files.*
"""
    
    return report


def post_cycle_report_to_discord(
    report_file: Path,
    accomplishments: List[Dict[str, Any]],
    captain_metrics: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Post cycle accomplishments report to Discord.
    
    Posts to Agent-4 (Captain) channel with summary.
    """
    try:
        from tools.categories.communication_tools import DiscordRouterPoster
        
        total_agents = len(accomplishments)
        total_completed = sum(len(a.get('completed_tasks', [])) for a in accomplishments)
        total_achievements = sum(len(a.get('achievements', [])) for a in accomplishments)
        
        summary = f"""📊 **Cycle Accomplishments Report Generated**

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Total Agents:** {total_agents}
**Total Completed Tasks:** {total_completed}
**Total Achievements:** {total_achievements}
"""
        
        # Add Captain metrics if provided
        if captain_metrics:
            summary += f"""
**Captain Metrics:**
- Cycle #{captain_metrics.get('cycle_number', 'N/A')}
- Missions Assigned: {captain_metrics.get('missions_assigned', 0)}
- Messages Sent: {captain_metrics.get('messages_sent', 0)}
- Agents Activated: {len(captain_metrics.get('agents_activated', []))}
- Points Awarded: {captain_metrics.get('points_awarded', 0)}
"""
        
        summary += f"""
**Report File:** `{report_file.name}`

Full report available in: `reports/cycle_accomplishments_*.md`

*Generated via PROTOCOL: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0 (Unified)*
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


def generate_unified_cycle_report(
    target_date: Optional[str] = None,
    captain_metrics: Optional[Dict[str, Any]] = None
) -> Optional[Path]:
    """
    Generate unified cycle accomplishments report.
    
    Merges capabilities from:
    - generate_cycle_accomplishments_report.py (all-agents report)
    - CycleReportTool (Captain metrics)
    """
    logger.info("📊 Generating unified cycle accomplishments report...")
    
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
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
    report_content = format_accomplishments_report(accomplishments, captain_metrics)
    
    # Save report
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_ROOT / f"cycle_accomplishments_{timestamp_str}.md"
    
    REPORTS_ROOT.mkdir(exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    logger.info(f"✅ Unified cycle accomplishments report generated: {report_file}")
    print(f"Report generated: {report_file}")
    
    # Post to Discord
    try:
        logger.info("📢 Posting cycle accomplishments report to Discord...")
        post_cycle_report_to_discord(report_file, accomplishments, captain_metrics)
    except Exception as e:
        logger.warning(f"⚠️  Failed to post cycle report to Discord: {e}")
        # Don't fail the entire report generation if Discord posting fails
    
    return report_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Unified Cycle Accomplishments Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all-agents report (default)
  python tools/unified_cycle_accomplishments_report.py

  # Include Captain metrics
  python tools/unified_cycle_accomplishments_report.py \\
    --captain-metrics \\
    --cycle-number 123 \\
    --missions 5 \\
    --messages 10 \\
    --agents Agent-1 Agent-2 Agent-3 \\
    --points 150 \\
    --notes "Great cycle progress"

  # Specify date
  python tools/unified_cycle_accomplishments_report.py --date 2025-12-26
        """
    )
    
    parser.add_argument(
        "--date",
        type=str,
        help="Target date for report (YYYY-MM-DD format, default: today)"
    )
    
    parser.add_argument(
        "--captain-metrics",
        action="store_true",
        help="Include Captain metrics section"
    )
    
    parser.add_argument(
        "--cycle-number",
        type=int,
        help="Cycle number (required if --captain-metrics)"
    )
    
    parser.add_argument(
        "--missions",
        type=int,
        default=0,
        help="Missions assigned (default: 0)"
    )
    
    parser.add_argument(
        "--messages",
        type=int,
        default=0,
        help="Messages sent (default: 0)"
    )
    
    parser.add_argument(
        "--agents",
        nargs="+",
        help="Agents activated (space-separated list)"
    )
    
    parser.add_argument(
        "--points",
        type=int,
        default=0,
        help="Points awarded (default: 0)"
    )
    
    parser.add_argument(
        "--notes",
        type=str,
        default="",
        help="Cycle notes"
    )
    
    args = parser.parse_args()
    
    # Validate Captain metrics arguments
    captain_metrics = None
    if args.captain_metrics:
        if args.cycle_number is None:
            logger.error("❌ --cycle-number is required when using --captain-metrics")
            sys.exit(1)
        
        captain_metrics = {
            "cycle_number": args.cycle_number,
            "missions_assigned": args.missions,
            "messages_sent": args.messages,
            "agents_activated": args.agents or [],
            "points_awarded": args.points,
            "notes": args.notes
        }
    
    try:
        report_file = generate_unified_cycle_report(
            target_date=args.date,
            captain_metrics=captain_metrics
        )
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




