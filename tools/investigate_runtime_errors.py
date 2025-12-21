#!/usr/bin/env python3
"""
Investigate Runtime Errors in Broken Tools
==========================================

Systematically tests tools with runtime errors to identify root causes.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-20
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import json

PROJECT_ROOT = Path(__file__).parent.parent


def test_tool_runtime(tool_path: Path) -> Dict[str, any]:
    """Test if a tool can run with --help flag."""
    result = {
        "tool": str(tool_path.relative_to(PROJECT_ROOT)),
        "has_help": False,
        "runtime_error": None,
        "error_type": None,
        "missing_deps": [],
        "status": "unknown"
    }
    
    # Check if file exists
    if not tool_path.exists():
        result["status"] = "not_found"
        result["runtime_error"] = "File not found"
        return result
    
    # Try to run with --help
    try:
        run_result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if run_result.returncode == 0:
            result["has_help"] = True
            result["status"] = "working"
        else:
            # Analyze error
            stderr = run_result.stderr
            
            # Check for common error patterns
            if "ModuleNotFoundError" in stderr or "ImportError" in stderr:
                result["error_type"] = "missing_dependency"
                # Extract module name
                import re
                match = re.search(r"'(.*?)'", stderr)
                if match:
                    result["missing_deps"].append(match.group(1))
            elif "AttributeError" in stderr:
                result["error_type"] = "attribute_error"
            elif "NameError" in stderr:
                result["error_type"] = "name_error"
            elif "TypeError" in stderr:
                result["error_type"] = "type_error"
            elif "KeyError" in stderr:
                result["error_type"] = "key_error"
            elif "FileNotFoundError" in stderr:
                result["error_type"] = "missing_file"
            else:
                result["error_type"] = "other"
            
            result["runtime_error"] = stderr[:500]  # First 500 chars
            result["status"] = "broken"
            
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["runtime_error"] = "Tool execution timed out (>10 seconds)"
        result["error_type"] = "timeout"
    except Exception as e:
        result["status"] = "exception"
        result["runtime_error"] = str(e)[:500]
        result["error_type"] = "exception"
    
    return result


def categorize_errors(results: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize errors by type."""
    categories = {
        "working": [],
        "missing_dependency": [],
        "attribute_error": [],
        "name_error": [],
        "type_error": [],
        "key_error": [],
        "missing_file": [],
        "timeout": [],
        "other": [],
        "exception": []
    }
    
    for result in results:
        error_type = result.get("error_type", "other")
        status = result.get("status", "unknown")
        
        if status == "working":
            categories["working"].append(result)
        elif error_type in categories:
            categories[error_type].append(result)
        else:
            categories["other"].append(result)
    
    return categories


def main():
    """Investigate runtime errors for Agent-5 chunk tools."""
    
    # Runtime error tools from audit
    runtime_error_tools = [
        "tools/generate_utils_catalog_enhanced.py",
        "tools/git_based_merge_primary.py",
        "tools/git_commit_verifier.py",
        "tools/github_pr_debugger.py",
        "tools/hostinger_api_helper.py",
        "tools/houstonsipqueen_theme_and_post.py",
        "tools/identify_unnecessary_files.py",
        "tools/implement_dadudekc_positioning_unification.py",
        "tools/independent_architecture_review.py",
        "tools/integration_workflow_automation.py",
        "tools/investigate_freerideinvestor_500_error.py",
        "tools/irc_connection_diagnostics.py",
        "tools/map_dadudekc_smoke_session_cta.py",
        "tools/markov_8agent_roi_optimizer.py",
        "tools/markov_cycle_simulator.py",
        "tools/memory_leak_scanner.py",
        "tools/merge_dreambank_pr1_via_git.py",
        "tools/merge_prs_via_api.py",
        "tools/monitor_twitch_bot.py",
        "tools/monitor_twitch_bot_status.py",
        "tools/nightly_site_audit.py",
        "tools/phase2_agent_cellphone_dependency_analyzer.py",
        "tools/pin_houstonsipqueen_post.py",
        "tools/populate_tasks_from_health_check.py",
        "tools/post_4agent_mode_blog.py",
        "tools/post_agent3_devlog_session_cleanup.py",
        "tools/post_agent5_seo_breakthrough_blog.py",
        "tools/post_completion_report_to_discord.py",
        "tools/post_cycle_accomplishments_dual.py",
        "tools/post_dadudekc_family_business_blog.py",
        "tools/post_devlog_to_discord.py",
        "tools/post_dream_os_review.py",
        "tools/post_swarm_philosophy_blog.py",
        "tools/post_swarm_site_health_breakthrough.py",
        "tools/prepare_integration_testing.py",
        "tools/hard_onboard_agents_6_7_8.py",
        "tools/heal_stalled_agents.py"
    ]
    
    print("🔍 Investigating Runtime Errors")
    print("=" * 70)
    print(f"Testing {len(runtime_error_tools)} tools...\n")
    
    results = []
    for tool_rel_path in runtime_error_tools:
        tool_path = PROJECT_ROOT / tool_rel_path
        if not tool_path.exists():
            print(f"⚠️  Tool not found: {tool_rel_path}")
            continue
        
        print(f"Testing {tool_path.name}...", end=" ")
        result = test_tool_runtime(tool_path)
        results.append(result)
        
        if result["status"] == "working":
            print("✅ WORKING")
        else:
            error_type = result.get("error_type", "unknown")
            print(f"❌ {error_type.upper()}")
    
    # Categorize errors
    categories = categorize_errors(results)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 RUNTIME ERROR SUMMARY")
    print("=" * 70)
    
    print(f"\n✅ Working: {len(categories['working'])}")
    for result in categories['working']:
        print(f"   - {Path(result['tool']).name}")
    
    print(f"\n❌ Missing Dependencies: {len(categories['missing_dependency'])}")
    for result in categories['missing_dependency']:
        deps = ", ".join(result.get('missing_deps', []))
        print(f"   - {Path(result['tool']).name}: {deps}")
    
    print(f"\n❌ Attribute Errors: {len(categories['attribute_error'])}")
    for result in categories['attribute_error']:
        print(f"   - {Path(result['tool']).name}")
    
    print(f"\n❌ Name Errors: {len(categories['name_error'])}")
    for result in categories['name_error']:
        print(f"   - {Path(result['tool']).name}")
    
    print(f"\n❌ Type Errors: {len(categories['type_error'])}")
    for result in categories['type_error']:
        print(f"   - {Path(result['tool']).name}")
    
    print(f"\n❌ Missing Files: {len(categories['missing_file'])}")
    for result in categories['missing_file']:
        print(f"   - {Path(result['tool']).name}")
    
    print(f"\n⏱️  Timeouts: {len(categories['timeout'])}")
    for result in categories['timeout']:
        print(f"   - {Path(result['tool']).name}")
    
    print(f"\n❌ Other Errors: {len(categories['other'])}")
    for result in categories['other']:
        error_type = result.get('error_type', 'unknown')
        print(f"   - {Path(result['tool']).name}: {error_type}")
    
    # Save results
    results_file = PROJECT_ROOT / "agent_workspaces" / "Agent-5" / "tool_audit_assignments" / "RUNTIME_ERRORS_INVESTIGATION.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "investigation_date": "2025-12-20",
            "total_tools_tested": len(results),
            "categories": {k: len(v) for k, v in categories.items()},
            "results": results,
            "categorized": {k: [r['tool'] for r in v] for k, v in categories.items()}
        }, f, indent=2)
    
    print(f"\n✅ Results saved: {results_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


