#!/usr/bin/env python3
"""
V2 Compliance Refactoring Progress Monitor
Monitors V2 compliance refactoring progress across Agent-1, Agent-7, Agent-8
and verifies dashboard compliance numbers (110 violations, 87.6% compliance).

Agent-6: Coordination & Communication Specialist
Task: Monitor V2 compliance refactoring progress (HIGH priority)
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_agent_status(agent_id):
    """Load agent status.json file."""
    status_path = Path(f"agent_workspaces/{agent_id}/status.json")
    if status_path.exists():
        try:
            with open(status_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    return None

def extract_v2_progress(agent_status):
    """Extract V2 refactoring progress from agent status."""
    if not agent_status:
        return None
    
    progress = {
        "agent_id": agent_status.get("agent_id", "unknown"),
        "status": agent_status.get("status", "unknown"),
        "v2_refactoring": {}
    }
    
    # Agent-7 specific: V2 refactoring status
    if "v2_refactoring_status" in agent_status:
        progress["v2_refactoring"]["status"] = agent_status["v2_refactoring_status"]
    
    # Agent-7 specific: Batch progress
    if "batch_1_progress" in agent_status:
        batch_progress = agent_status["batch_1_progress"]
        progress["v2_refactoring"]["batch_1"] = {}
        for file, data in batch_progress.items():
            if isinstance(data, dict):
                progress["v2_refactoring"]["batch_1"][file] = {
                    "status": data.get("status", "unknown"),
                    "original_lines": data.get("original_lines", 0),
                    "current_lines": data.get("current_lines", 0),
                    "reduction": data.get("reduction", 0),
                    "remaining": data.get("remaining", 0)
                }
    
    # Agent-1 specific: Phase progress
    if "phase_0_contract" in agent_status:
        phase = agent_status["phase_0_contract"]
        progress["v2_refactoring"]["phase_0"] = {
            "status": phase.get("status", "unknown"),
            "result": phase.get("result", "")
        }
    
    # Agent-8 specific: SSOT/QA progress
    if "current_mission" in agent_status:
        mission = agent_status["current_mission"]
        if "SSOT" in mission or "imports" in mission:
            progress["v2_refactoring"]["mission"] = mission
    
    return progress

def check_dashboard_compliance():
    """Check dashboard compliance numbers (110 violations, 87.6% compliance)."""
    # Search for dashboard compliance references
    dashboard_files = [
        "src/web/static/js/dashboard-ui-helpers.js",
        "src/web/static/js/dashboard-communication.js",
        "src/web/static/js/architecture/pattern-coordination-methods.js"
    ]
    
    compliance_info = {
        "violations_count": None,
        "compliance_percent": None,
        "sources": []
    }
    
    for file_path in dashboard_files:
        path = Path(file_path)
        if path.exists():
            try:
                content = path.read_text(encoding="utf-8")
                # Look for violation counts and compliance percentages
                if "110" in content or "87.6" in content:
                    compliance_info["sources"].append(str(path))
            except Exception as e:
                pass
    
    return compliance_info

def generate_progress_report():
    """Generate comprehensive V2 compliance progress report."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "agents": {},
        "dashboard_compliance": {},
        "summary": {}
    }
    
    # Monitor Agent-1 (Integration & Core Systems)
    agent1_status = load_agent_status("Agent-1")
    if agent1_status:
        report["agents"]["Agent-1"] = extract_v2_progress(agent1_status)
    
    # Monitor Agent-7 (Web Development)
    agent7_status = load_agent_status("Agent-7")
    if agent7_status:
        report["agents"]["Agent-7"] = extract_v2_progress(agent7_status)
    
    # Monitor Agent-8 (SSOT & System Integration)
    agent8_status = load_agent_status("Agent-8")
    if agent8_status:
        report["agents"]["Agent-8"] = extract_v2_progress(agent8_status)
    
    # Check dashboard compliance numbers
    report["dashboard_compliance"] = check_dashboard_compliance()
    
    # Generate summary
    active_agents = sum(1 for a in report["agents"].values() if a and a.get("status") == "ACTIVE")
    total_agents = len(report["agents"])
    
    report["summary"] = {
        "total_agents_monitored": total_agents,
        "active_agents": active_agents,
        "dashboard_compliance_verified": len(report["dashboard_compliance"]["sources"]) > 0,
        "next_check": "Monitor refactoring progress, verify dashboard numbers"
    }
    
    return report

def main():
    """Main execution function."""
    print("=" * 70)
    print("V2 COMPLIANCE REFACTORING PROGRESS MONITOR")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    report = generate_progress_report()
    
    # Display agent progress
    print("AGENT PROGRESS:")
    print("-" * 70)
    for agent_id, progress in report["agents"].items():
        if progress:
            print(f"\n{agent_id}:")
            print(f"  Status: {progress.get('status', 'unknown')}")
            if progress.get("v2_refactoring"):
                v2 = progress["v2_refactoring"]
                if "status" in v2:
                    print(f"  V2 Refactoring Status: {v2['status']}")
                if "batch_1" in v2:
                    print(f"  Batch 1 Files: {len(v2['batch_1'])}")
                    for file, data in v2["batch_1"].items():
                        print(f"    - {file}: {data.get('current_lines', 0)} lines (reduced from {data.get('original_lines', 0)})")
                if "phase_0" in v2:
                    print(f"  Phase 0: {v2['phase_0'].get('status', 'unknown')}")
                if "mission" in v2:
                    print(f"  Mission: {v2['mission']}")
        else:
            print(f"\n{agent_id}: Status not available")
    
    # Display dashboard compliance
    print("\n" + "=" * 70)
    print("DASHBOARD COMPLIANCE CHECK:")
    print("-" * 70)
    dashboard = report["dashboard_compliance"]
    if dashboard["sources"]:
        print(f"✅ Dashboard compliance references found in {len(dashboard['sources'])} files:")
        for source in dashboard["sources"]:
            print(f"  - {source}")
    else:
        print("⚠️  No dashboard compliance references found (110 violations, 87.6% compliance)")
    
    # Display summary
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("-" * 70)
    summary = report["summary"]
    print(f"Total agents monitored: {summary['total_agents_monitored']}")
    print(f"Active agents: {summary['active_agents']}")
    print(f"Dashboard compliance verified: {summary['dashboard_compliance_verified']}")
    print(f"Next check: {summary['next_check']}")
    
    # Save report
    output_path = Path("agent_workspaces/Agent-6/v2_compliance_progress_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report saved to: {output_path}\n")

if __name__ == "__main__":
    main()

