#!/usr/bin/env python3
"""
Quick test script to identify actual runtime errors in tools.
Tests import and basic initialization.
"""

import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Tools with runtime errors from audit
RUNTIME_ERROR_TOOLS = [
    "tools.unified_blogging_automation",
    "tools.unified_github_pr_creator",
    "tools.unstick_agent3_assignment",
    "tools.update_all_sites_branding",
    "tools.update_blog_posts_with_fixed_links",
    "tools.update_freerideinvestor_menus",
    "tools.update_freerideinvestor_premium_report",
    "tools.update_github_repo_description",
    "tools.v2_checker_formatters",
    "tools.v2_compliance_summary",
    "tools.validate_batch_consolidation",
    "tools.validate_duplicate_analysis",
    "tools.validate_imports",
    "tools.validate_resume_cycle_planner_integration",
    "tools.validate_stall_detection",
    "tools.validate_stall_detection_enhancement",
    "tools.validate_swarm_snapshot_view",
    "tools.validate_trackers",
    "tools.verify_all_ci_workflows",
    "tools.verify_batch1_main_branches",
    "tools.verify_batch1_main_content",
    "tools.verify_batch1_merge_commits",
    "tools.verify_batch2_prs",
    "tools.verify_batch2_target_repos",
    "tools.verify_batch3_ssot",
    "tools.verify_batch4_ssot",
    "tools.verify_batch5_ssot",
    "tools.verify_batch_ssot",
    "tools.verify_contract_leads_merge",
    "tools.verify_discord_buttons",
    "tools.verify_dream_os_ci",
    "tools.verify_failed_merge_repos",
    "tools.verify_hsq_astros_css",
    "tools.verify_merges",
    "tools.verify_phase1_repos",
    "tools.verify_remaining_branches",
    "tools.verify_v2_function_class_limits",
    "tools.verify_website_fixes",
    "tools.vote_tools_ranking_debate",
    "tools.web_domain_security_audit",
    "tools.wordpress_admin_deployer",
    "tools.work_attribution_tool",
    "tools.work_completion_verifier",
]

def test_tool(module_name):
    """Test if a tool can be imported and has a main function."""
    try:
        module = __import__(module_name, fromlist=[''])
        print(f"✅ {module_name}: Import successful")
        
        # Check for main function
        if hasattr(module, 'main'):
            print(f"   → Has main() function")
        else:
            print(f"   → No main() function")
        
        return True
    except SyntaxError as e:
        print(f"❌ {module_name}: SyntaxError - {e}")
        return False
    except ImportError as e:
        print(f"❌ {module_name}: ImportError - {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name}: RuntimeError - {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("Testing runtime error tools...\n")
    
    results = {"success": 0, "syntax": 0, "import": 0, "runtime": 0}
    
    for tool in RUNTIME_ERROR_TOOLS:
        result = test_tool(tool)
        if result:
            results["success"] += 1
        else:
            # Could be syntax, import, or runtime
            results["runtime"] += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {results['success']} successful, {results['runtime']} errors")
    print(f"{'='*60}")


