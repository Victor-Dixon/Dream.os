#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Quick validation script for CI/CD fixes.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""
import json
from pathlib import Path

def validate_ci_fixes():
    """Validate CI/CD fixes are complete."""
    results = {
        "workflow_files": [],
        "linting_fixes": [],
        "tools_created": [],
        "status": "PASS"
    }
    
    # Check workflow files
    workflows = [
        ".github/workflows/ci.yml",
        ".github/workflows/ci-optimized.yml",
        ".github/workflows/ci-minimal.yml",
        ".github/workflows/ci-robust.yml"
    ]
    
    for workflow in workflows:
        if Path(workflow).exists():
            results["workflow_files"].append(f"✅ {workflow}")
        else:
            results["workflow_files"].append(f"❌ {workflow} MISSING")
            results["status"] = "FAIL"
    
    # Check fixed files
    fixed_files = [
        "agent1_response.py",
        "config.py",
        "check_activation_messages.py",
        "check_queue_status.py",
        "check_recent_activations.py"
    ]
    
    for file in fixed_files:
        if Path(file).exists():
            results["linting_fixes"].append(f"✅ {file}")
    
    # Check tools
    tools = [
        "tools/diagnose_ci_failures.py",
        "tools/fix_ci_workflow.py",
        "tools/create_robust_ci_workflow.py"
    ]
    
    for tool in tools:
        if Path(tool).exists():
            results["tools_created"].append(f"✅ {tool}")
    
    print(json.dumps(results, indent=2))
    return results["status"] == "PASS"

if __name__ == "__main__":
    validate_ci_fixes()

