#!/usr/bin/env python3
"""
Documentation Structure Organizer
=================================

Analyzes and organizes documentation structure for better discoverability.
Creates documentation taxonomy, navigation index, and reorganization plan.

V2 Compliance | Author: Agent-6 | Date: 2025-12-25
"""

import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).parent.parent


def analyze_documentation_structure():
    """Analyze current documentation structure."""
    print("🔍 Analyzing documentation structure...")
    
    docs_path = project_root / "docs"
    structure = {
        "categories": defaultdict(list),
        "orphaned_files": [],
        "missing_readme": [],
        "deep_nesting": [],
        "total_files": 0,
        "total_dirs": 0
    }
    
    if not docs_path.exists():
        print(f"❌ docs/ directory not found at {docs_path}")
        return structure
    
    # Scan docs directory
    for root, dirs, files in os.walk(docs_path):
        rel_root = Path(root).relative_to(docs_path)
        depth = len(rel_root.parts)
        
        structure["total_dirs"] += 1
        
        # Check for README in each directory
        if not any(f.lower().startswith("readme") for f in files):
            if files:  # Only flag if directory has files
                structure["missing_readme"].append(str(rel_root))
        
        # Check for deep nesting (> 3 levels)
        if depth > 3:
            structure["deep_nesting"].append(str(rel_root))
        
        # Categorize files by directory
        for f in files:
            if f.endswith(".md"):
                structure["total_files"] += 1
                category = rel_root.parts[0] if rel_root.parts else "root"
                structure["categories"][category].append({
                    "file": f,
                    "path": str(rel_root / f),
                    "depth": depth
                })
    
    return structure


def create_documentation_taxonomy():
    """Create documentation taxonomy based on content analysis."""
    print("📊 Creating documentation taxonomy...")
    
    taxonomy = {
        "architecture": {
            "description": "System architecture, design patterns, technical decisions",
            "patterns": ["architecture", "design", "pattern", "system"],
            "files": []
        },
        "protocols": {
            "description": "Operational protocols, workflows, procedures",
            "patterns": ["protocol", "workflow", "procedure", "process"],
            "files": []
        },
        "guides": {
            "description": "How-to guides, tutorials, getting started",
            "patterns": ["guide", "how-to", "tutorial", "getting-started", "quick-start"],
            "files": []
        },
        "api": {
            "description": "API documentation, endpoints, interfaces",
            "patterns": ["api", "endpoint", "interface", "reference"],
            "files": []
        },
        "agent_workspaces": {
            "description": "Agent-specific documentation and status",
            "patterns": ["agent-", "workspace"],
            "files": []
        },
        "reports": {
            "description": "Audit reports, analysis, assessments",
            "patterns": ["report", "audit", "analysis", "assessment"],
            "files": []
        },
        "coordination": {
            "description": "Cross-agent coordination, collaboration",
            "patterns": ["coordination", "collaboration", "bilateral", "a2a"],
            "files": []
        },
        "messaging": {
            "description": "Messaging system, communication protocols",
            "patterns": ["messaging", "message", "communication", "inbox"],
            "files": []
        },
        "website": {
            "description": "Website documentation, SEO, audits",
            "patterns": ["website", "seo", "web", "wordpress"],
            "files": []
        },
        "other": {
            "description": "Uncategorized documentation",
            "patterns": [],
            "files": []
        }
    }
    
    docs_path = project_root / "docs"
    
    if docs_path.exists():
        for root, _, files in os.walk(docs_path):
            for f in files:
                if f.endswith(".md"):
                    file_path = Path(root) / f
                    rel_path = file_path.relative_to(docs_path)
                    file_lower = f.lower()
                    path_lower = str(rel_path).lower()
                    
                    categorized = False
                    for cat_name, cat_info in taxonomy.items():
                        if cat_name == "other":
                            continue
                        for pattern in cat_info["patterns"]:
                            if pattern in file_lower or pattern in path_lower:
                                taxonomy[cat_name]["files"].append(str(rel_path))
                                categorized = True
                                break
                        if categorized:
                            break
                    
                    if not categorized:
                        taxonomy["other"]["files"].append(str(rel_path))
    
    return taxonomy


def generate_documentation_index():
    """Generate documentation index/navigation."""
    print("📝 Generating documentation index...")
    
    taxonomy = create_documentation_taxonomy()
    
    index_content = """# Documentation Index

**Generated:** {}

## Quick Navigation

""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Add category sections
    for cat_name, cat_info in taxonomy.items():
        if cat_info["files"]:
            index_content += f"### {cat_name.replace('_', ' ').title()}\n\n"
            index_content += f"_{cat_info['description']}_\n\n"
            
            # Show first 10 files per category
            for f in cat_info["files"][:10]:
                index_content += f"- [{f}](docs/{f})\n"
            
            if len(cat_info["files"]) > 10:
                index_content += f"- ... and {len(cat_info['files']) - 10} more files\n"
            
            index_content += "\n"
    
    return index_content, taxonomy


def create_reorganization_plan(structure, taxonomy):
    """Create reorganization plan."""
    print("📋 Creating reorganization plan...")
    
    plan = {
        "timestamp": datetime.now().isoformat(),
        "current_state": {
            "total_files": structure["total_files"],
            "total_dirs": structure["total_dirs"],
            "missing_readme": len(structure["missing_readme"]),
            "deep_nesting": len(structure["deep_nesting"])
        },
        "taxonomy_distribution": {
            cat: len(info["files"]) for cat, info in taxonomy.items()
        },
        "recommendations": [],
        "actions": []
    }
    
    # Add recommendations
    if structure["missing_readme"]:
        plan["recommendations"].append({
            "type": "missing_readme",
            "priority": "MEDIUM",
            "count": len(structure["missing_readme"]),
            "action": "Add README.md files to directories with content",
            "directories": structure["missing_readme"][:10]
        })
    
    if structure["deep_nesting"]:
        plan["recommendations"].append({
            "type": "deep_nesting",
            "priority": "LOW",
            "count": len(structure["deep_nesting"]),
            "action": "Consider flattening directories nested > 3 levels",
            "directories": structure["deep_nesting"][:10]
        })
    
    # Add action items
    plan["actions"] = [
        {"action": "Create docs/README.md as main documentation entry point", "priority": "HIGH"},
        {"action": "Add category README files (architecture/README.md, etc.)", "priority": "MEDIUM"},
        {"action": "Create DOCUMENTATION_INDEX.md for navigation", "priority": "HIGH"},
        {"action": "Review and archive outdated documentation", "priority": "LOW"},
        {"action": "Consolidate duplicate documentation identified in audit", "priority": "MEDIUM"}
    ]
    
    return plan


def main():
    """Main entry point."""
    print("🏗️ DOCUMENTATION STRUCTURE ORGANIZER")
    print("=" * 50)
    
    # Step 1: Analyze current structure
    structure = analyze_documentation_structure()
    
    print(f"\n📊 Current Structure:")
    print(f"   Total files: {structure['total_files']}")
    print(f"   Total directories: {structure['total_dirs']}")
    print(f"   Missing README: {len(structure['missing_readme'])}")
    print(f"   Deep nesting (>3): {len(structure['deep_nesting'])}")
    
    # Step 2: Create taxonomy
    taxonomy = create_documentation_taxonomy()
    
    print(f"\n📁 Taxonomy Distribution:")
    for cat, info in taxonomy.items():
        if info["files"]:
            print(f"   {cat}: {len(info['files'])} files")
    
    # Step 3: Generate index
    index_content, _ = generate_documentation_index()
    
    # Step 4: Create reorganization plan
    plan = create_reorganization_plan(structure, taxonomy)
    
    # Save outputs
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Save plan
    plan_path = reports_dir / "documentation_reorganization_plan.json"
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2, default=str)
    print(f"\n✅ Plan saved: {plan_path}")
    
    # Save index
    index_path = project_root / "docs" / "DOCUMENTATION_INDEX.md"
    index_path.parent.mkdir(exist_ok=True)
    with open(index_path, "w") as f:
        f.write(index_content)
    print(f"✅ Index saved: {index_path}")
    
    # Summary
    print(f"\n📋 REORGANIZATION PLAN SUMMARY:")
    print(f"   Recommendations: {len(plan['recommendations'])}")
    print(f"   Action items: {len(plan['actions'])}")
    
    for action in plan["actions"]:
        print(f"   [{action['priority']}] {action['action']}")
    
    return plan


if __name__ == "__main__":
    main()

