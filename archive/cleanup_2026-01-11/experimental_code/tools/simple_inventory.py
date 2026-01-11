#!/usr/bin/env python3
"""
Simple Project Inventory
========================

Basic cataloging of project structure and key components.

Author: Agent-4 | Date: 2026-01-07
"""

import json
import os
from datetime import datetime
from pathlib import Path

def catalog_directory(directory, max_depth=2, current_depth=0):
    """Recursively catalog a directory structure."""
    if current_depth > max_depth:
        return {"type": "directory", "truncated": True}

    result = {"type": "directory", "contents": {}}

    try:
        for item in os.listdir(directory):
            if item.startswith('.') or item in ['__pycache__', 'node_modules']:
                continue

            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result["contents"][item] = catalog_directory(item_path, max_depth, current_depth + 1)
            else:
                ext = os.path.splitext(item)[1]
                result["contents"][item] = {
                    "type": "file",
                    "extension": ext,
                    "size": os.path.getsize(item_path)
                }
    except PermissionError:
        result["error"] = "Permission denied"

    return result

def analyze_tools():
    """Analyze tools directory."""
    tools_dir = Path("tools")
    tools_info = {"total_files": 0, "by_extension": {}, "categories": {}}

    if tools_dir.exists():
        for file_path in tools_dir.rglob("*"):
            if file_path.is_file():
                tools_info["total_files"] += 1
                ext = file_path.suffix
                tools_info["by_extension"][ext] = tools_info["by_extension"].get(ext, 0) + 1

                # Categorize tools
                name = file_path.stem.lower()
                if "diagnostic" in name or "diagnostic" in name:
                    category = "diagnostics"
                elif "analytics" in name or "inventory" in name:
                    category = "analytics"
                elif "deploy" in name or "infrastructure" in name:
                    category = "infrastructure"
                elif "test" in name or "validate" in name:
                    category = "testing"
                else:
                    category = "utilities"

                tools_info["categories"][category] = tools_info["categories"].get(category, 0) + 1

    return tools_info

def analyze_alerts():
    """Analyze alerts directory."""
    alerts_info = {"total_alerts": 0, "by_level": {}, "by_source": {}, "recent_trends": []}

    alerts_dir = Path("alerts")
    if alerts_dir.exists():
        for file_path in alerts_dir.glob("alert_*.json"):
            try:
                with open(file_path, 'r') as f:
                    alert = json.load(f)
                    alerts_info["total_alerts"] += 1

                    level = alert.get("level", "unknown")
                    source = alert.get("source", "unknown")

                    alerts_info["by_level"][level] = alerts_info["by_level"].get(level, 0) + 1
                    alerts_info["by_source"][source] = alerts_info["by_source"].get(source, 0) + 1
            except:
                continue

    return alerts_info

def analyze_agent_workspaces():
    """Analyze agent workspaces."""
    workspaces_info = {"total_agents": 0, "agents": [], "workspace_sizes": {}}

    workspaces_dir = Path("agent_workspaces")
    if workspaces_dir.exists():
        for agent_dir in workspaces_dir.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                workspaces_info["total_agents"] += 1
                workspaces_info["agents"].append(agent_dir.name)

                # Calculate workspace size
                total_size = 0
                file_count = 0
                for file_path in agent_dir.rglob("*"):
                    if file_path.is_file():
                        file_count += 1
                        try:
                            total_size += file_path.stat().st_size
                        except:
                            pass

                workspaces_info["workspace_sizes"][agent_dir.name] = {
                    "files": file_count,
                    "size_mb": round(total_size / (1024 * 1024), 2)
                }

    return workspaces_info

def main():
    """Generate simple project inventory."""
    print("🔍 Generating simple project inventory...")

    inventory = {
        "timestamp": datetime.now().isoformat(),
        "project_structure": {},
        "tools_analysis": analyze_tools(),
        "alerts_analysis": analyze_alerts(),
        "agent_workspaces": analyze_agent_workspaces()
    }

    # Catalog key directories
    key_dirs = ["src", "tools", "docs", "tests", "scripts"]
    for dir_name in key_dirs:
        if os.path.exists(dir_name):
            print(f"  📁 Analyzing {dir_name}...")
            inventory["project_structure"][dir_name] = catalog_directory(dir_name, max_depth=1)

    # Save inventory
    with open('simple_inventory.json', 'w') as f:
        json.dump(inventory, f, indent=2)

    print("✅ Simple inventory generated")

    # Print summary
    print("\n📊 PROJECT INVENTORY SUMMARY:")
    print(f"  • Tools: {inventory['tools_analysis']['total_files']} files")
    print(f"  • Agents: {inventory['agent_workspaces']['total_agents']} active workspaces")
    print(f"  • Alerts: {inventory['alerts_analysis']['total_alerts']} total alerts")

    if inventory['tools_analysis']['categories']:
        print(f"  • Tool categories: {', '.join(inventory['tools_analysis']['categories'].keys())}")

    if inventory['alerts_analysis']['by_level']:
        top_levels = sorted(inventory['alerts_analysis']['by_level'].items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  • Top alert levels: {', '.join(f'{level}({count})' for level, count in top_levels)}")

if __name__ == "__main__":
    main()