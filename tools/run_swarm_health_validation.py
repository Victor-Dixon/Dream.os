#!/usr/bin/env python3
"""
Swarm Health Validation - Agent-4 Captain Validation Tool
==========================================================

Runs cycle health checks across all agents and produces validation report.

Author: Agent-4 (Captain)
Date: 2025-12-10
Purpose: Produce validation artifact for stall recovery protocol
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from swarm_brain.agent_field_manual.automation.cycle_health_check import (
    CycleHealthCheck
)


def run_swarm_validation() -> dict:
    """Run health checks for all agents"""
    agents = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-5",
        "Agent-6", "Agent-7", "Agent-8", "Agent-4"
    ]
    
    checker = CycleHealthCheck(max_age_minutes=30)
    results = {
        "validation_timestamp": datetime.utcnow().isoformat() + "Z",
        "validation_type": "swarm_cycle_health_check",
        "executed_by": "Agent-4",
        "agents": {}
    }
    
    for agent_id in agents:
        print(f"\n=== {agent_id} Health Check ===")
        
        try:
            # Run pre-cycle check
            pre_result = checker.pre_cycle_check(agent_id)
            
            # Run post-cycle check
            post_result = checker.post_cycle_check(agent_id)
            
            results["agents"][agent_id] = {
                "pre_cycle": pre_result,
                "post_cycle": post_result,
                "overall_status": "PASS" if (
                    pre_result.get("passed", False) and 
                    post_result.get("passed", False)
                ) else "FAIL"
            }
            
            status_icon = "✅" if results["agents"][agent_id]["overall_status"] == "PASS" else "❌"
            print(f"{status_icon} {agent_id}: {results['agents'][agent_id]['overall_status']}")
            
        except Exception as e:
            results["agents"][agent_id] = {
                "error": str(e),
                "overall_status": "ERROR"
            }
            print(f"❌ {agent_id}: ERROR - {e}")
    
    # Calculate summary
    total = len(agents)
    passed = sum(
        1 for a in results["agents"].values() 
        if a.get("overall_status") == "PASS"
    )
    failed = sum(
        1 for a in results["agents"].values() 
        if a.get("overall_status") == "FAIL"
    )
    errors = sum(
        1 for a in results["agents"].values() 
        if a.get("overall_status") == "ERROR"
    )
    
    results["summary"] = {
        "total_agents": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%"
    }
    
    return results


def main():
    """Main execution"""
    print("🔍 Running Swarm Health Validation...")
    print("=" * 50)
    
    results = run_swarm_validation()
    
    # Save results
    output_dir = Path("agent_workspaces/Agent-4/validation_reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"swarm_health_check_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Total Agents: {results['summary']['total_agents']}")
    print(f"Passed: {results['summary']['passed']}")
    print(f"Failed: {results['summary']['failed']}")
    print(f"Errors: {results['summary']['errors']}")
    print(f"Pass Rate: {results['summary']['pass_rate']}")
    print(f"\n📄 Report saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    main()

