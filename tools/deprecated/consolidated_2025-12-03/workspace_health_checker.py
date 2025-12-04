#!/usr/bin/env python3
"""
Workspace Health Checker
========================

Comprehensive workspace health check tool that verifies:
- Inbox message status
- Workspace cleanliness
- Status file consistency
- Issue identification
- Devlog organization

Usage:
    python tools/workspace_health_checker.py [--agent Agent-X]
    python tools/workspace_health_checker.py --all
    python tools/workspace_health_checker.py --report
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Agent definitions
AGENTS = {
    "Agent-1": "Integration & Core Systems Specialist",
    "Agent-2": "Architecture & Design Specialist",
    "Agent-3": "Infrastructure & DevOps Specialist",
    "Agent-4": "Captain (Strategic Oversight)",
    "Agent-5": "Business Intelligence Specialist",
    "Agent-6": "Coordination & Communication Specialist",
    "Agent-7": "Web Development Specialist",
    "Agent-8": "SSOT & System Integration Specialist"
}


@dataclass
class HealthCheckResult:
    """Result of a health check."""
    agent_id: str
    timestamp: str
    inbox_status: Dict
    workspace_status: Dict
    status_files_status: Dict
    issues: List[Dict]
    devlog_status: Dict
    overall_health: str
    recommendations: List[str]


def check_inbox_health(agent_id: str) -> Dict:
    """Check inbox message health."""
    inbox_dir = Path(f"agent_workspaces/{agent_id}/inbox")
    
    if not inbox_dir.exists():
        return {
            "status": "MISSING",
            "message_count": 0,
            "unprocessed_count": 0,
            "old_messages": 0,
            "issues": ["Inbox directory does not exist"]
        }
    
    messages = list(inbox_dir.glob("*.md"))
    unprocessed = []
    old_messages = []
    cutoff_date = datetime.now() - timedelta(days=7)
    
    for msg_file in messages:
        # Check if message is old
        try:
            mtime = datetime.fromtimestamp(msg_file.stat().st_mtime)
            if mtime < cutoff_date:
                old_messages.append(msg_file.name)
        except Exception:
            pass
        
        # Check if message is in messages.json (processed)
        messages_json = inbox_dir / "messages.json"
        if messages_json.exists():
            try:
                with open(messages_json, 'r') as f:
                    msg_data = json.load(f)
                    if msg_file.stem not in msg_data.get("messages", {}):
                        unprocessed.append(msg_file.name)
            except Exception:
                unprocessed.append(msg_file.name)
        else:
            unprocessed.append(msg_file.name)
    
    issues = []
    if unprocessed:
        issues.append(f"{len(unprocessed)} unprocessed messages")
    if old_messages:
        issues.append(f"{len(old_messages)} messages older than 7 days")
    
    return {
        "status": "HEALTHY" if not issues else "NEEDS_ATTENTION",
        "message_count": len(messages),
        "unprocessed_count": len(unprocessed),
        "old_messages": len(old_messages),
        "issues": issues
    }


def check_workspace_cleanliness(agent_id: str) -> Dict:
    """Check workspace cleanliness."""
    workspace_dir = Path(f"agent_workspaces/{agent_id}")
    
    if not workspace_dir.exists():
        return {
            "status": "MISSING",
            "issues": ["Workspace directory does not exist"]
        }
    
    issues = []
    
    # Check for orphaned files
    expected_dirs = ["inbox", "devlogs", "outbox", "reports"]
    for expected_dir in expected_dirs:
        expected_path = workspace_dir / expected_dir
        if not expected_path.exists():
            issues.append(f"Missing expected directory: {expected_dir}")
    
    # Check for excessive files in root workspace
    root_files = [f for f in workspace_dir.iterdir() if f.is_file() and f.suffix == ".md"]
    if len(root_files) > 20:
        issues.append(f"Too many markdown files in root ({len(root_files)}), consider organizing")
    
    # Check devlog organization
    devlog_dir = workspace_dir / "devlogs"
    if devlog_dir.exists():
        devlogs = list(devlog_dir.glob("*.md"))
        if len(devlogs) > 100:
            issues.append(f"Large number of devlogs ({len(devlogs)}), consider archiving")
    
    return {
        "status": "HEALTHY" if not issues else "NEEDS_ATTENTION",
        "issues": issues
    }


def check_status_files_consistency(agent_id: str) -> Dict:
    """Check status file consistency."""
    issues = []
    
    # Check agent status.json
    agent_status_file = Path(f"agent_workspaces/{agent_id}/status.json")
    agent_status = None
    if agent_status_file.exists():
        try:
            with open(agent_status_file, 'r') as f:
                agent_status = json.load(f)
        except Exception as e:
            issues.append(f"Error reading agent status.json: {e}")
    else:
        issues.append("Agent status.json missing")
    
    # Check runtime/AGENT_STATUS.json
    runtime_status_file = Path("runtime/AGENT_STATUS.json")
    runtime_status = None
    if runtime_status_file.exists():
        try:
            with open(runtime_status_file, 'r') as f:
                runtime_data = json.load(f)
                runtime_status = runtime_data.get(agent_id)
        except Exception as e:
            issues.append(f"Error reading runtime AGENT_STATUS.json: {e}")
    else:
        issues.append("runtime/AGENT_STATUS.json missing")
    
    # Check consistency
    if agent_status and runtime_status:
        agent_last_updated = agent_status.get("last_updated", "")
        runtime_last_updated = runtime_status.get("last_updated", "")
        
        if agent_last_updated != runtime_last_updated:
            issues.append("Status file timestamps inconsistent")
    
    return {
        "status": "HEALTHY" if not issues else "NEEDS_ATTENTION",
        "agent_status_exists": agent_status_file.exists(),
        "runtime_status_exists": runtime_status_file.exists(),
        "consistency": "CONSISTENT" if not issues else "INCONSISTENT",
        "issues": issues
    }


def identify_issues(agent_id: str) -> List[Dict]:
    """Identify issues in workspace."""
    issues = []
    workspace_dir = Path(f"agent_workspaces/{agent_id}")
    
    # Check for common error patterns
    if workspace_dir.exists():
        for file_path in workspace_dir.rglob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if "ERROR" in content or "FIXME" in content or "TODO" in content:
                    issues.append({
                        "type": "CONTENT_ISSUE",
                        "file": str(file_path.relative_to(workspace_dir)),
                        "severity": "LOW",
                        "message": "Contains ERROR/FIXME/TODO markers"
                    })
            except Exception:
                pass
    
    return issues


def check_devlog_status(agent_id: str) -> Dict:
    """Check devlog organization status."""
    devlog_dir = Path(f"agent_workspaces/{agent_id}/devlogs")
    
    if not devlog_dir.exists():
        return {
            "status": "MISSING",
            "count": 0,
            "issues": ["Devlog directory does not exist"]
        }
    
    devlogs = list(devlog_dir.glob("*.md"))
    recent_devlogs = []
    cutoff_date = datetime.now() - timedelta(days=7)
    
    for devlog in devlogs:
        try:
            mtime = datetime.fromtimestamp(devlog.stat().st_mtime)
            if mtime > cutoff_date:
                recent_devlogs.append(devlog.name)
        except Exception:
            pass
    
    issues = []
    if len(devlogs) > 100:
        issues.append(f"Large number of devlogs ({len(devlogs)}), consider archiving")
    if len(recent_devlogs) == 0:
        issues.append("No recent devlogs (last 7 days)")
    
    return {
        "status": "HEALTHY" if not issues else "NEEDS_ATTENTION",
        "count": len(devlogs),
        "recent_count": len(recent_devlogs),
        "issues": issues
    }


def check_workspace_health(agent_id: str) -> HealthCheckResult:
    """Perform comprehensive workspace health check."""
    inbox_status = check_inbox_health(agent_id)
    workspace_status = check_workspace_cleanliness(agent_id)
    status_files_status = check_status_files_consistency(agent_id)
    issues = identify_issues(agent_id)
    devlog_status = check_devlog_status(agent_id)
    
    # Determine overall health
    all_statuses = [
        inbox_status.get("status"),
        workspace_status.get("status"),
        status_files_status.get("status"),
        devlog_status.get("status")
    ]
    
    if "MISSING" in all_statuses:
        overall_health = "CRITICAL"
    elif "NEEDS_ATTENTION" in all_statuses:
        overall_health = "NEEDS_ATTENTION"
    else:
        overall_health = "HEALTHY"
    
    # Generate recommendations
    recommendations = []
    if inbox_status.get("unprocessed_count", 0) > 0:
        recommendations.append(f"Process {inbox_status['unprocessed_count']} unprocessed inbox messages")
    if inbox_status.get("old_messages", 0) > 0:
        recommendations.append(f"Archive {inbox_status['old_messages']} old messages (>7 days)")
    if workspace_status.get("issues"):
        recommendations.extend([f"Fix: {issue}" for issue in workspace_status["issues"]])
    if status_files_status.get("issues"):
        recommendations.extend([f"Fix: {issue}" for issue in status_files_status["issues"]])
    if devlog_status.get("issues"):
        recommendations.extend([f"Fix: {issue}" for issue in devlog_status["issues"]])
    
    return HealthCheckResult(
        agent_id=agent_id,
        timestamp=datetime.now().isoformat(),
        inbox_status=inbox_status,
        workspace_status=workspace_status,
        status_files_status=status_files_status,
        issues=issues,
        devlog_status=devlog_status,
        overall_health=overall_health,
        recommendations=recommendations
    )


def print_health_report(result: HealthCheckResult):
    """Print formatted health report."""
    print(f"\n{'='*70}")
    print(f"🏥 Workspace Health Check: {result.agent_id}")
    print(f"{'='*70}")
    print(f"Timestamp: {result.timestamp}")
    print(f"Overall Health: {result.overall_health}")
    print()
    
    print("📬 Inbox Status:")
    print(f"  Status: {result.inbox_status['status']}")
    print(f"  Messages: {result.inbox_status.get('message_count', 0)}")
    print(f"  Unprocessed: {result.inbox_status.get('unprocessed_count', 0)}")
    print(f"  Old Messages: {result.inbox_status.get('old_messages', 0)}")
    if result.inbox_status.get('issues'):
        for issue in result.inbox_status['issues']:
            print(f"  ⚠️  {issue}")
    print()
    
    print("📁 Workspace Status:")
    print(f"  Status: {result.workspace_status['status']}")
    if result.workspace_status.get('issues'):
        for issue in result.workspace_status['issues']:
            print(f"  ⚠️  {issue}")
    print()
    
    print("📊 Status Files Status:")
    print(f"  Status: {result.status_files_status['status']}")
    print(f"  Consistency: {result.status_files_status.get('consistency', 'UNKNOWN')}")
    if result.status_files_status.get('issues'):
        for issue in result.status_files_status['issues']:
            print(f"  ⚠️  {issue}")
    print()
    
    print("📝 Devlog Status:")
    print(f"  Status: {result.devlog_status['status']}")
    print(f"  Total Devlogs: {result.devlog_status.get('count', 0)}")
    print(f"  Recent Devlogs: {result.devlog_status.get('recent_count', 0)}")
    if result.devlog_status.get('issues'):
        for issue in result.devlog_status['issues']:
            print(f"  ⚠️  {issue}")
    print()
    
    if result.issues:
        print("🚨 Issues Identified:")
        for issue in result.issues:
            print(f"  {issue['type']}: {issue.get('file', 'N/A')} - {issue.get('message', 'N/A')}")
        print()
    
    if result.recommendations:
        print("💡 Recommendations:")
        for rec in result.recommendations:
            print(f"  • {rec}")
        print()
    
    print(f"{'='*70}\n")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Workspace Health Checker")
    parser.add_argument("--agent", type=str, help="Agent ID to check (e.g., Agent-5)")
    parser.add_argument("--all", action="store_true", help="Check all agents")
    parser.add_argument("--report", action="store_true", help="Generate JSON report")
    
    args = parser.parse_args()
    
    if args.all:
        agents_to_check = list(AGENTS.keys())
    elif args.agent:
        if args.agent not in AGENTS:
            print(f"❌ Error: Unknown agent {args.agent}")
            sys.exit(1)
        agents_to_check = [args.agent]
    else:
        print("❌ Error: Must specify --agent or --all")
        parser.print_help()
        sys.exit(1)
    
    results = []
    for agent_id in agents_to_check:
        result = check_workspace_health(agent_id)
        results.append(result)
        
        if not args.report:
            print_health_report(result)
    
    if args.report:
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "results": [asdict(r) for r in results]
        }
        report_file = Path(f"reports/workspace_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        print(f"✅ Report saved to: {report_file}")


if __name__ == "__main__":
    main()

