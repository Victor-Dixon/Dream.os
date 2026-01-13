#!/usr/bin/env python3
"""
Analyze Duplicates for Wave B Consolidation
==========================================

Categorizes duplicate files for systematic SSOT consolidation.
Focuses on code duplicates that need to be moved to canonical locations.

Wave B Strategy:
1. Identify code duplicates (not just docs/reports)
2. Map to SSOT canonical locations
3. Plan consolidation batches
4. Ensure imports can be updated safely
"""

import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict

def analyze_duplicate_patterns():
    """Analyze duplicate patterns for consolidation planning."""
    print("🔍 Analyzing duplicate patterns for Wave B consolidation...")

    # Focus on code directories that need consolidation
    # Exclude agent_workspaces (runtime artifacts) and focus on actual code
    code_dirs = [
        Path("src"),
        Path("mcp_servers"),
        Path("scripts"),
        Path("tools"),
        Path("systems"),
        Path("temp_repos/Thea/src"),  # Only Thea code, not whole temp_repos
        Path("swarm_brain/shared_learnings"),  # Only code-like content
    ]

    # SSOT canonical mappings
    canonical_mappings = {
        # Deploy scripts -> MCP deployment server
        "scripts/deploy_via_wordpress_admin.py": "mcp_servers/deployment_server.py",
        "tools/deploy_tradingrobotplug_plugin.py": "mcp_servers/deployment_server.py",
        "tools/deploy_tradingrobotplug_plugin_phase3.py": "mcp_servers/deployment_server.py",
        "tools/deploy_fastapi_tradingrobotplug.py": "mcp_servers/deployment_server.py",
        "tools/deploy_weareswarm_feed_system.py": "mcp_servers/deployment_server.py",
        "tools/deploy_weareswarm_font_fix.py": "mcp_servers/deployment_server.py",
        "tools/deploy_tradingrobotplug_font_fix.py": "mcp_servers/deployment_server.py",

        # WordPress management -> WP-CLI server
        "tools/wordpress_manager.py": "mcp_servers/wp_cli_manager_server.py",

        # Site adapters -> base adapter
        "src/control_plane/adapters/hostinger/": "src/control_plane/adapters/base.py",
    }

    hashes = {}
    file_info = {}

    # Scan for duplicates in code areas
    for scan_dir in code_dirs:
        if not scan_dir.exists():
            continue

        for file_path in scan_dir.rglob("*"):
            if not file_path.is_file():
                continue

            # Focus on code files that might need consolidation
            if file_path.suffix not in [".py", ".js", ".ts", ".md"]:
                continue

            # Skip obvious non-code and runtime artifacts
            skip_parts = [".git", ".venv", "__pycache__", ".pytest_cache", "node_modules",
                         "agent_workspaces", "__pycache__", ".pytest_cache"]
            if any(part in skip_parts for part in file_path.parts):
                continue

            # Skip temp_repos except Thea source code
            if "temp_repos" in file_path.parts:
                if not ("Thea" in file_path.parts and "src" in file_path.parts):
                    continue

            try:
                with open(file_path, "rb") as f:
                    # Full file hash for accurate detection
                    file_hash = hashlib.sha256(f.read()).hexdigest()

                if file_hash not in hashes:
                    hashes[file_hash] = []
                hashes[file_hash].append(file_path)

                # Store file info
                file_info[str(file_path)] = {
                    "size": file_path.stat().st_size,
                    "extension": file_path.suffix,
                    "path": str(file_path),
                    "relative_path": str(file_path.relative_to(Path("."))),
                    "parent_dir": str(file_path.parent)
                }

            except Exception as e:
                print(f"   Warning: Could not process {file_path}: {e}")
                continue

    # Analyze duplicate groups
    consolidation_candidates = []
    easy_deletes = []
    needs_review = []

    for file_hash, files in hashes.items():
        if len(files) < 2:
            continue

        group_info = {
            "hash": file_hash,
            "count": len(files),
            "total_size": sum(file_info[str(f)]["size"] for f in files),
            "files": [file_info[str(f)] for f in files],
            "extensions": list(set(f.suffix for f in files)),
            "directories": list(set(str(f.parent) for f in files))
        }

        # Categorize for consolidation
        if _is_easy_consolidation(group_info):
            consolidation_candidates.append(group_info)
        elif _is_easy_delete(group_info):
            easy_deletes.append(group_info)
        else:
            needs_review.append(group_info)

    return {
        "consolidation_candidates": consolidation_candidates,
        "easy_deletes": easy_deletes,
        "needs_review": needs_review,
        "summary": {
            "total_duplicate_groups": len(consolidation_candidates) + len(easy_deletes) + len(needs_review),
            "consolidation_candidates": len(consolidation_candidates),
            "easy_deletes": len(easy_deletes),
            "needs_review": len(needs_review)
        }
    }

def _is_easy_consolidation(group_info: Dict) -> bool:
    """Check if duplicate group is easy to consolidate."""
    files = group_info["files"]

    # Focus on Python files for Wave B (code consolidation)
    if not all(f["extension"] == ".py" for f in files):
        return False

    # Must be in different directories (actual duplication, not copies)
    dirs = set(f["parent_dir"] for f in files)
    if len(dirs) < 2:
        return False

    # Exclude agent_workspaces (runtime artifacts)
    if any("agent_workspaces" in f["path"] for f in files):
        return False

    # Allow temp_repos but require at least one non-temp file (real consolidation target)
    has_non_temp = any("temp_repos" not in f["path"] for f in files)
    if not has_non_temp:
        return False

    # Reasonable file size (allow up to 500KB for consolidation)
    if group_info["total_size"] > 500000:  # 500KB
        return False

    return True

def _is_easy_delete(group_info: Dict) -> bool:
    """Check if duplicate group can be easily deleted."""
    files = group_info["files"]

    # Documentation files in archives
    if all("archive" in f["path"] or "reports" in f["path"] for f in files):
        return True

    # Exact copies in same directory structure
    # (like backup files, temp files)
    dirs = set(f["path"].rsplit("/", 1)[0] for f in files)
    if len(dirs) == 1:  # All in same directory
        return True

    return False

def generate_consolidation_plan(analysis_results: Dict) -> Dict[str, Any]:
    """Generate detailed consolidation plan."""
    print("📋 Generating Wave B consolidation plan...")

    plan = {
        "wave_b_plan": {
            "name": "Code Consolidation Wave",
            "description": "Move duplicate code to SSOT canonical locations",
            "batches": []
        }
    }

    # Create consolidation batches
    candidates = analysis_results["consolidation_candidates"]

    # Group by functionality
    functional_groups = defaultdict(list)

    for candidate in candidates:
        # Determine functional group
        func_group = _determine_functional_group(candidate)
        functional_groups[func_group].append(candidate)

    # Create batches
    batch_num = 1
    for func_group, candidates in functional_groups.items():
        if not candidates:
            continue

        batch = {
            "batch_id": f"B{batch_num}",
            "name": f"{func_group.title()} Consolidation",
            "description": f"Consolidate {len(candidates)} duplicate groups in {func_group}",
            "functional_group": func_group,
            "duplicate_groups": len(candidates),
            "estimated_files": sum(len(c["files"]) for c in candidates),
            "estimated_savings_kb": sum(c["total_size"] for c in candidates) // 1024,
            "risk_level": _assess_batch_risk(candidates),
            "consolidation_steps": _generate_consolidation_steps(func_group, candidates)
        }

        plan["wave_b_plan"]["batches"].append(batch)
        batch_num += 1

    # Sort batches by risk (low risk first)
    plan["wave_b_plan"]["batches"].sort(key=lambda x: x["risk_level"])

    return plan

def _determine_functional_group(candidate: Dict) -> str:
    """Determine the functional group for a duplicate candidate."""
    files = [f["path"] for f in candidate["files"]]

    # Check for deployment-related
    if any("deploy" in f.lower() for f in files):
        return "deployment"

    # Check for WordPress related
    if any("wordpress" in f.lower() or "wp" in f.lower() for f in files):
        return "wordpress"

    # Check for adapter related
    if any("adapter" in f.lower() for f in files):
        return "adapters"

    # Check for utility/helper functions
    if any("util" in f.lower() or "helper" in f.lower() for f in files):
        return "utilities"

    # Default category
    return "general"

def _assess_batch_risk(candidates: List[Dict]) -> str:
    """Assess risk level for a consolidation batch."""
    total_files = sum(len(c["files"]) for c in candidates)
    total_size = sum(c["total_size"] for c in candidates)

    # High risk if many files or large codebase
    if total_files > 20 or total_size > 50000:  # 50KB
        return "HIGH"

    # Medium risk if moderate complexity
    if total_files > 10 or total_size > 20000:  # 20KB
        return "MEDIUM"

    # Low risk for small, simple consolidations
    return "LOW"

def _generate_consolidation_steps(func_group: str, candidates: List[Dict]) -> List[str]:
    """Generate step-by-step consolidation instructions."""
    steps = []

    # Determine canonical location based on functional group
    canonical_locations = {
        "deployment": "mcp_servers/deployment_server.py",
        "wordpress": "mcp_servers/wp_cli_manager_server.py",
        "adapters": "src/control_plane/adapters/base.py",
        "utilities": "src/core/utils/",
        "general": "src/core/common/"
    }

    canonical = canonical_locations.get(func_group, "src/core/common/")

    steps.extend([
        f"1. Identify canonical location: {canonical}",
        f"2. Analyze {len(candidates)} duplicate groups for consolidation",
        "3. Extract common functionality to canonical location",
        "4. Update imports in all duplicate files to use canonical",
        "5. Run tests to ensure functionality preserved",
        "6. Remove duplicate implementations",
        "7. Update documentation references"
    ])

    return steps

def save_analysis_results(results: Dict, plan: Dict):
    """Save analysis results and consolidation plan."""
    Path("reports").mkdir(exist_ok=True)

    # Save detailed analysis
    with open("reports/wave_b_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    # Save consolidation plan
    with open("reports/wave_b_consolidation_plan.json", "w") as f:
        json.dump(plan, f, indent=2)

    # Generate human-readable summary
    summary = f"""# Wave B Consolidation Analysis

## Summary
- **Total duplicate groups analyzed:** {results['summary']['total_duplicate_groups']}
- **Consolidation candidates:** {results['summary']['consolidation_candidates']}
- **Easy deletes:** {results['summary']['easy_deletes']}
- **Needs review:** {results['summary']['needs_review']}

## Consolidation Batches
"""

    for batch in plan["wave_b_plan"]["batches"]:
        summary += f"""
### {batch['batch_id']}: {batch['name']}
- **Risk Level:** {batch['risk_level']}
- **Duplicate Groups:** {batch['duplicate_groups']}
- **Files Affected:** {batch['estimated_files']}
- **Space Savings:** {batch['estimated_savings_kb']}KB

**Steps:**
"""
        for step in batch['consolidation_steps']:
            summary += f"- {step}\n"

    with open("reports/wave_b_consolidation_plan.md", "w") as f:
        f.write(summary)

    print("✅ Analysis saved to reports/wave_b_*")

def main():
    """Main analysis function."""
    print("🛰️ Wave B Consolidation Analysis")
    print("=" * 40)

    # Run analysis
    analysis_results = analyze_duplicate_patterns()

    print("📊 Analysis Results:")
    print(f"   Total duplicate groups: {analysis_results['summary']['total_duplicate_groups']}")
    print(f"   Consolidation candidates: {analysis_results['summary']['consolidation_candidates']}")
    print(f"   Easy deletes: {analysis_results['summary']['easy_deletes']}")
    print(f"   Needs review: {analysis_results['summary']['needs_review']}")

    # Generate consolidation plan
    consolidation_plan = generate_consolidation_plan(analysis_results)

    print(f"\n📋 Generated {len(consolidation_plan['wave_b_plan']['batches'])} consolidation batches")

    # Save results
    save_analysis_results(analysis_results, consolidation_plan)

    print("\n✅ Wave B analysis complete!")
    print("   Review reports/wave_b_consolidation_plan.md for detailed plan")

if __name__ == "__main__":
    main()