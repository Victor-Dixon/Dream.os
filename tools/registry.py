#!/usr/bin/env python3
"""
Tool Registry - Centralized Tool Discovery and Management
Provides comprehensive tool catalog with metadata, dependencies, and usage tracking

Usage:
    python tools/registry.py --list
    python tools/registry.py --info <tool_name>
    python tools/registry.py --category <category>
    python tools/registry.py --validate
"""

import json
import os
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set
import importlib.util


@dataclass
class ToolMetadata:
    """Metadata for a tool in the registry"""
    name: str
    category: str
    description: str
    file_path: str
    version: str = "1.0.0"
    author: str = "Agent-4"
    dependencies: List[str] = None
    python_version: str = ">=3.8"
    last_updated: str = ""
    line_count: int = 0
    status: str = "active"
    tags: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
        if not self.last_updated:
            self.last_updated = time.strftime("%Y-%m-%d")


class ToolRegistry:
    """Centralized registry for all tools"""

    def __init__(self):
        self.tools_dir = Path(__file__).parent
        self.registry_file = self.tools_dir / "registry.json"
        self.tools: Dict[str, ToolMetadata] = {}
        self.categories: Set[str] = set()
        self._load_registry()

    def _load_registry(self):
        """Load tool registry from JSON file"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    data = json.load(f)
                    for name, tool_data in data.items():
                        self.tools[name] = ToolMetadata(**tool_data)
                        self.categories.add(tool_data['category'])
            except Exception as e:
                print(f"Warning: Could not load registry: {e}")

    def _save_registry(self):
        """Save tool registry to JSON file"""
        data = {name: asdict(tool) for name, tool in self.tools.items()}
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _analyze_tool_file(self, file_path: Path) -> ToolMetadata:
        """Analyze a tool file to extract metadata"""
        name = file_path.stem
        metadata = ToolMetadata(
            name=name,
            category="utility",  # Default category
            description=f"Tool: {name}",
            file_path=str(file_path.relative_to(self.tools_dir.parent))
        )

        # Analyze file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                metadata.line_count = len(lines)

                # Extract description from docstring
                if '"""' in content:
                    docstring_start = content.find('"""') + 3
                    docstring_end = content.find('"""', docstring_start)
                    if docstring_end > docstring_start:
                        docstring = content[docstring_start:docstring_end].strip()
                        first_line = docstring.split('\n')[0]
                        metadata.description = first_line

                # Categorize based on filename patterns
                if 'a2a' in name or 'coordination' in name:
                    metadata.category = "coordination"
                elif 'test' in name or 'validation' in name or 'diagnostic' in name:
                    metadata.category = "testing"
                elif 'ai' in name or 'vector' in name:
                    metadata.category = "ai"
                elif 'deploy' in name or 'infrastructure' in name:
                    metadata.category = "infrastructure"
                elif 'robinhood' in name or 'trading' in name:
                    metadata.category = "trading"
                elif 'discord' in name or 'devlog' in name:
                    metadata.category = "communication"
                elif 'compliance' in name or 'verify' in name:
                    metadata.category = "quality"
                elif 'inventory' in name or 'audit' in name:
                    metadata.category = "analysis"

                # Extract dependencies (basic analysis)
                if 'import ' in content:
                    imports = []
                    for line in lines:
                        line = line.strip()
                        if line.startswith('import ') or line.startswith('from '):
                            if 'src.' in line:  # Internal dependencies
                                continue
                            imports.append(line)
                    if imports:
                        metadata.dependencies = imports[:5]  # Limit to 5

        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

        return metadata

    def scan_tools_directory(self):
        """Scan tools directory and update registry"""
        print("🔍 Scanning tools directory...")

        for file_path in self.tools_dir.glob("*.py"):
            if file_path.name == "registry.py":
                continue

            name = file_path.stem
            if name not in self.tools:
                print(f"📝 Adding new tool: {name}")
                metadata = self._analyze_tool_file(file_path)
                self.tools[name] = metadata
                self.categories.add(metadata.category)

        self._save_registry()
        print(f"✅ Registry updated: {len(self.tools)} tools across {len(self.categories)} categories")

    def list_tools(self, category: Optional[str] = None) -> List[ToolMetadata]:
        """List all tools or tools in a category"""
        if category:
            return [tool for tool in self.tools.values() if tool.category == category]
        return list(self.tools.values())

    def get_tool_info(self, name: str) -> Optional[ToolMetadata]:
        """Get information about a specific tool"""
        return self.tools.get(name)

    def validate_tools(self) -> Dict[str, str]:
        """Validate that all registered tools exist and are importable"""
        results = {}

        for name, tool in self.tools.items():
            file_path = self.tools_dir.parent / tool.file_path
            if not file_path.exists():
                results[name] = f"❌ File not found: {tool.file_path}"
                continue

            # Try to import the tool
            try:
                spec = importlib.util.spec_from_file_location(name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    results[name] = "✅ Import successful"
                else:
                    results[name] = "⚠️ Could not create module spec"
            except Exception as e:
                results[name] = f"❌ Import failed: {str(e)[:100]}"

        return results

    def get_categories(self) -> List[str]:
        """Get list of all categories"""
        return sorted(list(self.categories))

    def get_registry_stats(self) -> Dict:
        """Get registry statistics"""
        stats = {
            "total_tools": len(self.tools),
            "categories": len(self.categories),
            "tools_by_category": {},
            "avg_line_count": 0,
            "total_lines": 0
        }

        total_lines = 0
        for tool in self.tools.values():
            stats["tools_by_category"][tool.category] = stats["tools_by_category"].get(tool.category, 0) + 1
            total_lines += tool.line_count

        stats["total_lines"] = total_lines
        if stats["total_tools"] > 0:
            stats["avg_line_count"] = round(total_lines / stats["total_tools"], 1)

        return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Tool Registry - Centralized Tool Management")
    parser.add_argument("--scan", action="store_true", help="Scan tools directory and update registry")
    parser.add_argument("--list", action="store_true", help="List all tools")
    parser.add_argument("--category", help="List tools in specific category")
    parser.add_argument("--info", help="Get detailed info for specific tool")
    parser.add_argument("--validate", action="store_true", help="Validate all registered tools")
    parser.add_argument("--stats", action="store_true", help="Show registry statistics")

    args = parser.parse_args()

    registry = ToolRegistry()

    if args.scan:
        registry.scan_tools_directory()

    elif args.list:
        tools = registry.list_tools()
        print(f"📋 All Tools ({len(tools)} total):\n")
        for tool in sorted(tools, key=lambda x: x.category):
            print(f"  {tool.name} - {tool.category}: {tool.description}")

    elif args.category:
        tools = registry.list_tools(args.category)
        print(f"📋 Tools in category '{args.category}' ({len(tools)} tools):\n")
        for tool in tools:
            print(f"  {tool.name}: {tool.description}")

    elif args.info:
        tool = registry.get_tool_info(args.info)
        if tool:
            print(f"📋 Tool Information: {tool.name}\n")
            print(f"  Category: {tool.category}")
            print(f"  Description: {tool.description}")
            print(f"  File: {tool.file_path}")
            print(f"  Lines: {tool.line_count}")
            print(f"  Status: {tool.status}")
            print(f"  Last Updated: {tool.last_updated}")
            if tool.dependencies:
                print(f"  Dependencies: {', '.join(tool.dependencies[:3])}")
            if tool.tags:
                print(f"  Tags: {', '.join(tool.tags)}")
        else:
            print(f"❌ Tool '{args.info}' not found")

    elif args.validate:
        print("🔍 Validating tools...")
        results = registry.validate_tools()
        for name, status in results.items():
            print(f"  {name}: {status}")

    elif args.stats:
        stats = registry.get_registry_stats()
        print("📊 Registry Statistics:\n")
        print(f"  Total Tools: {stats['total_tools']}")
        print(f"  Categories: {stats['categories']}")
        print(f"  Total Lines: {stats['total_lines']}")
        print(f"  Average Lines per Tool: {stats['avg_line_count']}\n")
        print("  Tools by Category:")
        for category, count in stats['tools_by_category'].items():
            print(f"    {category}: {count} tools")

    else:
        print("Use --scan, --list, --category, --info, --validate, or --stats")
        print("\nAvailable categories:")
        for category in registry.get_categories():
            print(f"  - {category}")


if __name__ == "__main__":
    main()