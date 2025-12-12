#!/usr/bin/env python3
"""
Check Agent Statuses - Captain Pattern Execution (Enhanced)
===========================================================

Quick script to check all agent status.json files for staleness with multi-source
activity detection. Used by Captain to identify agents that need resume prompts.

Enhanced with multi-source activity detection to reduce false stall detections.

<!-- SSOT Domain: infrastructure -->

Author: Agent-4 (Captain)
Date: 2025-12-05
Updated: 2025-12-11 - Added multi-source activity detection
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

def check_agent_statuses(use_activity_detection: bool = True) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict]]:
    """Check all agent statuses and categorize by staleness."""
    
    agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8', 'Agent-4']
    # Calculate workspace root (parent of agent_workspaces directory)
    agent_workspaces = Path("agent_workspaces")
    if agent_workspaces.exists():
        workspace_root = agent_workspaces.parent
    else:
        # Fallback: assume we're in workspace root
        workspace_root = Path(".")
        agent_workspaces = workspace_root / "agent_workspaces"
    
    fresh_agents = []  # <2 hours
    warning_agents = []  # 2-6 hours
    critical_agents = []  # 6-12 hours
    auto_resume_agents = []  # >12 hours
    
    now = datetime.now()
    
    # Initialize hardened activity detector if enabled
    activity_detector = None
    if use_activity_detection:
        try:
            from src.core.hardened_activity_detector import HardenedActivityDetector
            activity_detector = HardenedActivityDetector(workspace_root)
        except ImportError:
            # Fallback to legacy detector
            try:
                from tools.agent_activity_detector import AgentActivityDetector
                activity_detector = AgentActivityDetector(workspace_root)
            except ImportError:
                use_activity_detection = False
    
    for agent_id in agents:
        status_file = agent_workspaces / agent_id / "status.json"
        
        if not status_file.exists():
            auto_resume_agents.append({
                "agent_id": agent_id,
                "status": "NO_STATUS_FILE",
                "hours_old": None,
                "last_updated": None
            })
            continue
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            last_updated_str = status.get('last_updated', '')
            agent_status = status.get('status', 'UNKNOWN')
            mission = status.get('current_mission', 'N/A')
            
            if not last_updated_str:
                auto_resume_agents.append({
                    "agent_id": agent_id,
                    "status": agent_status,
                    "hours_old": None,
                    "last_updated": None,
                    "mission": mission
                })
                continue
            
            # Parse timestamp
            try:
                # Handle different timestamp formats
                if 'T' in last_updated_str:
                    if last_updated_str.endswith('Z'):
                        last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
                    else:
                        last_updated = datetime.fromisoformat(last_updated_str)
                else:
                    # Format: "YYYY-MM-DD HH:MM:SS"
                    last_updated = datetime.strptime(last_updated_str, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                auto_resume_agents.append({
                    "agent_id": agent_id,
                    "status": agent_status,
                    "hours_old": None,
                    "last_updated": last_updated_str,
                    "mission": mission,
                    "error": f"Invalid timestamp: {e}"
                })
                continue
            
            # Calculate hours since update
            if last_updated.tzinfo:
                hours_old = (now - last_updated.replace(tzinfo=None)).total_seconds() / 3600
            else:
                hours_old = (now - last_updated).total_seconds() / 3600
            
            # Enhanced: Verify activity if status appears stale using hardened detector
            is_actually_active = False
            activity_sources = []
            confidence = None
            if hours_old >= 2 and use_activity_detection and activity_detector:
                try:
                    # Use hardened detector if available
                    if hasattr(activity_detector, 'assess_agent_activity'):
                        assessment = activity_detector.assess_agent_activity(agent_id, lookback_minutes=60)
                        is_actually_active = assessment.is_active
                        confidence = assessment.confidence
                        activity_sources = [s.source.name for s in assessment.signals[:3]]
                    else:
                        # Fallback to legacy detector
                        summary = activity_detector.detect_agent_activity(
                            agent_id, lookback_minutes=60, use_events=True
                        )
                        is_actually_active = summary.is_active
                        if summary.last_activity and last_updated:
                            if summary.last_activity > last_updated:
                                is_actually_active = True
                        activity_sources = summary.activity_sources
                except Exception as e:
                    pass  # Fallback to status.json only
            
            agent_info = {
                "agent_id": agent_id,
                "status": agent_status,
                "hours_old": round(hours_old, 1),
                "last_updated": last_updated_str,
                "mission": mission[:60],
                "activity_verified": is_actually_active if hours_old >= 2 else None,
                "activity_sources": activity_sources if activity_sources else None,
                "confidence": round(confidence, 2) if confidence is not None else None
            }
            
            # Categorize by staleness, but consider activity verification
            # If agent has recent activity, don't escalate to higher categories
            effective_hours_old = hours_old
            if is_actually_active and hours_old >= 2:
                # Recent activity detected - treat as if status was updated more recently
                # Cap at warning level instead of critical/auto-resume
                effective_hours_old = min(hours_old, 5.9)  # Treat as warning, not critical
            
            if effective_hours_old < 2:
                fresh_agents.append(agent_info)
            elif effective_hours_old < 6:
                warning_agents.append(agent_info)
            elif effective_hours_old < 12:
                critical_agents.append(agent_info)
            else:
                auto_resume_agents.append(agent_info)
                
        except Exception as e:
            auto_resume_agents.append({
                "agent_id": agent_id,
                "status": "ERROR",
                "hours_old": None,
                "last_updated": None,
                "error": str(e)
            })
    
    return fresh_agents, warning_agents, critical_agents, auto_resume_agents


def main():
    """Print agent status summary."""
    import argparse
    parser = argparse.ArgumentParser(description="Check agent statuses with activity detection")
    parser.add_argument("--no-activity-check", action="store_true",
                       help="Disable multi-source activity detection")
    args = parser.parse_args()
    
    fresh, warning, critical, auto_resume = check_agent_statuses(
        use_activity_detection=not args.no_activity_check
    )
    
    print("=" * 60)
    print("AGENT STATUS CHECK - Captain Pattern Execution")
    print("=" * 60)
    print()
    
    print(f"🟢 FRESH (<2 hours): {len(fresh)}")
    for agent in fresh:
        print(f"  - {agent['agent_id']}: {agent['status']} ({agent['hours_old']}h ago) - {agent['mission']}")
    
    print()
    print(f"🟡 WARNING (2-6 hours): {len(warning)}")
    for agent in warning:
        status_note = ""
        if agent.get('activity_verified'):
            sources = agent.get('activity_sources', [])
            if sources:
                status_note = f" [Activity: {', '.join(sources[:2])}]"
        print(f"  - {agent['agent_id']}: {agent['status']} ({agent['hours_old']}h ago){status_note} - {agent['mission']}")
    
    print()
    print(f"🟠 CRITICAL (6-12 hours): {len(critical)}")
    for agent in critical:
        status_note = ""
        if agent.get('activity_verified'):
            sources = agent.get('activity_sources', [])
            if sources:
                status_note = f" [Activity: {', '.join(sources[:2])}]"
        print(f"  - {agent['agent_id']}: {agent['status']} ({agent['hours_old']}h ago){status_note} - {agent['mission']}")
    
    print()
    print(f"🔴 AUTO-RESUME (>12 hours): {len(auto_resume)}")
    for agent in auto_resume:
        hours_str = f"{agent['hours_old']}h ago" if agent['hours_old'] else "UNKNOWN"
        status_note = ""
        if not agent.get('activity_verified') and agent.get('hours_old'):
            status_note = " [No recent activity detected]"
        print(f"  - {agent['agent_id']}: {agent['status']} ({hours_str}){status_note} - {agent.get('mission', 'N/A')}")
    
    print()
    print("=" * 60)
    print(f"Total Agents: {len(fresh) + len(warning) + len(critical) + len(auto_resume)}")
    print(f"Need Resume: {len(critical) + len(auto_resume)}")
    print("=" * 60)
    
    # Return exit code based on staleness
    if auto_resume:
        return 2  # Need immediate resume
    elif critical:
        return 1  # Need resume soon
    else:
        return 0  # All good


if __name__ == "__main__":
    sys.exit(main())

