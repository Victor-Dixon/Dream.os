#!/usr/bin/env python3
"""
Project Inventory Catalog System
=================================

<!-- SSOT Domain: infrastructure -->

Comprehensive cataloging of all tools, files, and capabilities across the repository.
Provides cross-agent visibility and integration readiness assessment.

V2 Compliance | Author: Agent-4 | Date: 2026-01-07
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict

# Domain mappings for SSOT compliance
SSOT_DOMAINS = {
    "core": "Core system functionality and architecture",
    "infrastructure": "Infrastructure, deployment, and DevOps tools",
    "integration": "API integrations, third-party services, and connectors",
    "trading_robot": "Trading robot specific functionality and algorithms",
    "ai_automation": "AI-powered automation and intelligent systems",
    "messaging": "Communication systems, messaging, and coordination",
    "discord": "Discord bot and community management tools",
    "swarm_brain": "Swarm intelligence and multi-agent coordination",
    "analytics": "Data analytics, reporting, and business intelligence",
    "data": "Data management, storage, and processing",
    "performance": "Performance monitoring, optimization, and metrics",
    "safety": "Security, compliance, and safety systems",
    "communication": "Communication tools and notification systems",
    "git": "Version control and Git operations",
    "architecture": "System architecture and design patterns",
    "domain": "Domain modeling and business logic",
    "error_handling": "Error handling, logging, and debugging",
    "qa": "Quality assurance, testing, and validation",
    "ai_training": "AI model training and machine learning",
    "gaming": "Gaming and simulation systems",
    "vision": "Computer vision and image processing",
    "logging": "Logging and audit trail systems"
}

@dataclass
class ToolMetadata:
    """Metadata for a discovered tool."""
    name: str
    path: str
    domain: str
    capabilities: List[str]
    dependencies: List[str]
    status: str  # active, deprecated, experimental
    last_modified: str
    file_size: int
    description: str
    ssot_compliant: bool


@dataclass
class DomainInventory:
    """Inventory for a specific domain."""
    domain: str
    description: str
    tools: List[ToolMetadata]
    total_tools: int
    active_tools: int
    deprecated_tools: int
    capabilities: Set[str]
    cross_references: Dict[str, List[str]]


@dataclass
class ProjectInventory:
    """Complete project inventory across all domains."""
    timestamp: str
    repository_stats: Dict[str, Any]
    domain_inventories: Dict[str, DomainInventory]
    integration_readiness: Dict[str, Any]
    recommendations: List[str]


class ProjectInventoryCatalog:
    """
    Comprehensive project inventory catalog system.

    Catalogs all tools, files, and capabilities with:
    - SSOT domain compliance checking
    - Cross-agent visibility
    - Integration readiness assessment
    - Capability mapping and dependencies
    """

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.inventory: Optional[ProjectInventory] = None

        # Patterns for tool discovery
        self.tool_patterns = [
            r'^tools/.*\.py$',
            r'^src/.*tools.*\.py$',
            r'^.*_tool.*\.py$',
            r'^.*tool.*\.py$',
            r'^scripts/.*\.py$',
            r'^.*_cli\.py$',
            r'^.*_service\.py$'
        ]

    def generate_full_inventory(self) -> ProjectInventory:
        """
        Generate comprehensive project inventory.

        Returns:
            Complete project inventory with all domains and tools
        """
        print("🔍 Generating comprehensive project inventory...")

        # Get repository statistics
        repo_stats = self._analyze_repository_stats()

        # Discover all tools
        all_tools = self._discover_tools()

        # Organize by domains
        domain_inventories = self._organize_by_domains(all_tools)

        # Assess integration readiness
        integration_readiness = self._assess_integration_readiness(domain_inventories)

        # Generate recommendations
        recommendations = self._generate_recommendations(domain_inventories, integration_readiness)

        inventory = ProjectInventory(
            timestamp=datetime.now().isoformat(),
            repository_stats=repo_stats,
            domain_inventories=domain_inventories,
            integration_readiness=integration_readiness,
            recommendations=recommendations
        )

        self.inventory = inventory
        print("✅ Project inventory generation complete")

        return inventory

    def _analyze_repository_stats(self) -> Dict[str, Any]:
        """Analyze basic repository statistics."""
        stats = {
            "total_files": 0,
            "total_directories": 0,
            "total_size_mb": 0,
            "file_types": {},
            "largest_files": [],
            "recently_modified": []
        }

        for root, dirs, files in os.walk(self.root_path):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            stats["total_directories"] += len(dirs)

            for file in files:
                if file.startswith('.'):
                    continue

                filepath = Path(root) / file
                stats["total_files"] += 1

                # File size
                try:
                    size = filepath.stat().st_size
                    stats["total_size_mb"] += size / (1024 * 1024)

                    # Track largest files
                    if len(stats["largest_files"]) < 10:
                        stats["largest_files"].append((str(filepath), size))
                    else:
                        stats["largest_files"].sort(key=lambda x: x[1], reverse=True)
                        if size > stats["largest_files"][-1][1]:
                            stats["largest_files"][-1] = (str(filepath), size)

                except OSError:
                    pass

                # File types
                ext = filepath.suffix
                stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1

                # Recently modified (last 7 days)
                try:
                    mtime = filepath.stat().st_mtime
                    if mtime > datetime.now().timestamp() - (7 * 24 * 60 * 60):
                        stats["recently_modified"].append(str(filepath))
                except OSError:
                    pass

        # Format results
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        stats["largest_files"] = stats["largest_files"][:5]  # Top 5
        stats["recently_modified"] = stats["recently_modified"][:10]  # Top 10

        return stats

    def _discover_tools(self) -> List[ToolMetadata]:
        """Discover all tools in the repository."""
        tools = []

        for root, dirs, files in os.walk(self.root_path):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            for file in files:
                if not file.endswith('.py'):
                    continue

                filepath = Path(root) / file
                relative_path = filepath.relative_to(self.root_path)

                # Check if it matches tool patterns
                path_str = str(relative_path)
                is_tool = any(re.search(pattern, path_str) for pattern in self.tool_patterns)

                if is_tool:
                    tool_metadata = self._analyze_tool_file(filepath, relative_path)
                    if tool_metadata:
                        tools.append(tool_metadata)

        return tools

    def _analyze_tool_file(self, filepath: Path, relative_path: Path) -> Optional[ToolMetadata]:
        """Analyze a tool file and extract metadata."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract domain from SSOT comment
            domain = self._extract_ssot_domain(content)

            # Extract capabilities from docstring and function names
            capabilities = self._extract_capabilities(content)

            # Extract dependencies
            dependencies = self._extract_dependencies(content)

            # Determine status
            status = self._determine_tool_status(filepath, content)

            # Get file metadata
            stat = filepath.stat()
            last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

            # Extract description
            description = self._extract_description(content)

            # Check SSOT compliance
            ssot_compliant = domain in SSOT_DOMAINS

            return ToolMetadata(
                name=filepath.stem,
                path=str(relative_path),
                domain=domain,
                capabilities=capabilities,
                dependencies=dependencies,
                status=status,
                last_modified=last_modified,
                file_size=stat.st_size,
                description=description,
                ssot_compliant=ssot_compliant
            )

        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")
            return None

    def _extract_ssot_domain(self, content: str) -> str:
        """Extract SSOT domain from file content."""
        # Look for SSOT domain comment
        match = re.search(r'<!-- SSOT Domain: (\w+) -->', content)
        if match:
            return match.group(1)

        # Try alternative formats
        match = re.search(r'SSOT Domain: (\w+)', content)
        if match:
            return match.group(1)

        return "unknown"

    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract capabilities from tool content."""
        capabilities = []

        # Look for function definitions
        functions = re.findall(r'def (\w+)\(', content)
        capabilities.extend([f.replace('_', ' ').title() for f in functions[:5]])  # Limit to 5

        # Look for class definitions
        classes = re.findall(r'class (\w+)\(', content)
        capabilities.extend([f"Class: {c}" for c in classes[:3]])  # Limit to 3

        # Look for key operations in docstrings
        docstring_match = re.search(r'""".*?(.*?)"""', content, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1).lower()
            if 'create' in docstring:
                capabilities.append("Content Creation")
            if 'analyze' in docstring or 'analysis' in docstring:
                capabilities.append("Analysis")
            if 'validate' in docstring or 'validation' in docstring:
                capabilities.append("Validation")
            if 'deploy' in docstring:
                capabilities.append("Deployment")

        return capabilities[:10]  # Limit capabilities

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract import dependencies."""
        dependencies = []

        # Find import statements
        imports = re.findall(r'^(?:from|import) (\w+)', content, re.MULTILINE)
        dependencies.extend(list(set(imports)))  # Remove duplicates

        return dependencies[:10]  # Limit dependencies

    def _determine_tool_status(self, filepath: Path, content: str) -> str:
        """Determine tool status based on file analysis."""
        # Check for deprecation markers
        if re.search(r'(deprecated|DEPRECATED|TODO.*remove)', content, re.IGNORECASE):
            return "deprecated"

        # Check for experimental markers
        if re.search(r'(experimental|EXPERIMENTAL|beta|BETA)', content, re.IGNORECASE):
            return "experimental"

        # Check file age (old files might be deprecated)
        try:
            mtime = filepath.stat().st_mtime
            days_old = (datetime.now().timestamp() - mtime) / (24 * 60 * 60)
            if days_old > 90:  # Older than 90 days
                return "deprecated"
        except:
            pass

        return "active"

    def _extract_description(self, content: str) -> str:
        """Extract tool description from docstring."""
        # Look for module docstring
        match = re.search(r'""".*?(.*?)"""', content, re.DOTALL)
        if match:
            description = match.group(1).strip()
            # Take first 200 characters
            return description[:200] + "..." if len(description) > 200 else description

        return "No description available"

    def _organize_by_domains(self, tools: List[ToolMetadata]) -> Dict[str, DomainInventory]:
        """Organize tools by SSOT domains."""
        domain_groups = {}

        for tool in tools:
            domain = tool.domain
            if domain not in domain_groups:
                domain_groups[domain] = []

            domain_groups[domain].append(tool)

        # Create domain inventories
        domain_inventories = {}
        for domain, domain_tools in domain_groups.items():
            description = SSOT_DOMAINS.get(domain, f"Domain: {domain}")

            # Calculate statistics
            total_tools = len(domain_tools)
            active_tools = sum(1 for t in domain_tools if t.status == "active")
            deprecated_tools = sum(1 for t in domain_tools if t.status == "deprecated")

            # Collect all capabilities
            all_capabilities = set()
            for tool in domain_tools:
                all_capabilities.update(tool.capabilities)

            # Find cross-references (tools that depend on other domains)
            cross_references = {}
            for tool in domain_tools:
                for dep in tool.dependencies:
                    # Check if dependency relates to another domain
                    for other_domain in SSOT_DOMAINS.keys():
                        if other_domain in dep.lower():
                            if other_domain not in cross_references:
                                cross_references[other_domain] = []
                            cross_references[other_domain].append(tool.name)

            domain_inventory = DomainInventory(
                domain=domain,
                description=description,
                tools=domain_tools,
                total_tools=total_tools,
                active_tools=active_tools,
                deprecated_tools=deprecated_tools,
                capabilities=all_capabilities,
                cross_references=cross_references
            )

            domain_inventories[domain] = domain_inventory

        return domain_inventories

    def _assess_integration_readiness(self, domain_inventories: Dict[str, DomainInventory]) -> Dict[str, Any]:
        """Assess integration readiness across domains."""
        assessment = {
            "overall_readiness_score": 0,
            "domain_readiness": {},
            "integration_gaps": [],
            "cross_domain_dependencies": {},
            "ssot_compliance": {}
        }

        total_domains = len(domain_inventories)
        total_readiness_score = 0

        for domain, inventory in domain_inventories.items():
            # Calculate domain readiness
            active_ratio = inventory.active_tools / inventory.total_tools if inventory.total_tools > 0 else 0
            ssot_compliance = sum(1 for t in inventory.tools if t.ssot_compliant) / inventory.total_tools if inventory.total_tools > 0 else 0

            domain_score = (active_ratio * 0.6 + ssot_compliance * 0.4) * 100
            total_readiness_score += domain_score

            assessment["domain_readiness"][domain] = {
                "score": round(domain_score, 1),
                "active_tools_ratio": round(active_ratio, 2),
                "ssot_compliance_ratio": round(ssot_compliance, 2),
                "cross_references": len(inventory.cross_references)
            }

            # Track SSOT compliance
            assessment["ssot_compliance"][domain] = round(ssot_compliance * 100, 1)

        # Calculate overall score
        assessment["overall_readiness_score"] = round(total_readiness_score / total_domains, 1) if total_domains > 0 else 0

        # Identify integration gaps
        assessment["integration_gaps"] = self._identify_integration_gaps(domain_inventories)

        # Map cross-domain dependencies
        assessment["cross_domain_dependencies"] = self._map_cross_domain_dependencies(domain_inventories)

        return assessment

    def _identify_integration_gaps(self, domain_inventories: Dict[str, DomainInventory]) -> List[str]:
        """Identify integration gaps and missing capabilities."""
        gaps = []

        # Check for domains with low readiness
        for domain, inventory in domain_inventories.items():
            readiness = inventory.active_tools / inventory.total_tools if inventory.total_tools > 0 else 0
            if readiness < 0.7:  # Less than 70% active tools
                gaps.append(f"Domain '{domain}' has low readiness ({readiness:.1%}) - {inventory.deprecated_tools} deprecated tools")

        # Check for missing core domains
        core_domains = ["core", "infrastructure", "integration"]
        missing_core = [d for d in core_domains if d not in domain_inventories]
        if missing_core:
            gaps.append(f"Missing core domains: {', '.join(missing_core)}")

        # Check for domains with no cross-references (isolation)
        isolated_domains = [d for d, inv in domain_inventories.items() if not inv.cross_references]
        if isolated_domains:
            gaps.append(f"Isolated domains with no cross-references: {', '.join(isolated_domains)}")

        return gaps

    def _map_cross_domain_dependencies(self, domain_inventories: Dict[str, DomainInventory]) -> Dict[str, List[str]]:
        """Map cross-domain dependencies."""
        dependencies = {}

        for domain, inventory in domain_inventories.items():
            for ref_domain, tools in inventory.cross_references.items():
                if ref_domain not in dependencies:
                    dependencies[ref_domain] = []
                if domain not in dependencies[ref_domain]:
                    dependencies[ref_domain].append(domain)

        return dependencies

    def _generate_recommendations(self, domain_inventories: Dict[str, DomainInventory],
                                integration_readiness: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []

        # SSOT compliance recommendations
        ssot_compliance = integration_readiness.get("ssot_compliance", {})
        low_compliance_domains = [d for d, score in ssot_compliance.items() if score < 80]
        if low_compliance_domains:
            recommendations.append(f"Improve SSOT compliance in domains: {', '.join(low_compliance_domains)}")

        # Domain readiness recommendations
        domain_readiness = integration_readiness.get("domain_readiness", {})
        low_readiness_domains = [d for d, data in domain_readiness.items() if data["score"] < 70]
        if low_readiness_domains:
            recommendations.append(f"Address low readiness in domains: {', '.join(low_readiness_domains)}")

        # Deprecated tool cleanup
        deprecated_domains = []
        for domain, inventory in domain_inventories.items():
            if inventory.deprecated_tools > inventory.active_tools:
                deprecated_domains.append(f"{domain} ({inventory.deprecated_tools} deprecated vs {inventory.active_tools} active)")

        if deprecated_domains:
            recommendations.append(f"Clean up deprecated tools in: {', '.join(deprecated_domains)}")

        # Integration gap recommendations
        integration_gaps = integration_readiness.get("integration_gaps", [])
        if integration_gaps:
            recommendations.extend(integration_gaps[:3])  # Limit to top 3

        return recommendations or ["✅ Project inventory is well-maintained with good integration readiness"]


def main():
    """Command-line interface for project inventory catalog."""
    import argparse

    parser = argparse.ArgumentParser(description="Project Inventory Catalog System")
    parser.add_argument("--output", type=str, default="project_inventory.json",
                       help="Output file path (default: project_inventory.json)")
    parser.add_argument("--summary", action="store_true",
                       help="Generate summary view only")
    parser.add_argument("--domain", type=str,
                       help="Focus on specific domain")

    args = parser.parse_args()

    # Generate inventory
    print("🔍 Starting project inventory catalog generation...")
    catalog = ProjectInventoryCatalog()
    inventory = catalog.generate_full_inventory()

    if args.domain and args.domain in inventory.domain_inventories:
        # Focus on specific domain
        domain_inv = inventory.domain_inventories[args.domain]
        output = {
            "domain": args.domain,
            "description": domain_inv.description,
            "statistics": {
                "total_tools": domain_inv.total_tools,
                "active_tools": domain_inv.active_tools,
                "deprecated_tools": domain_inv.deprecated_tools,
                "capabilities": list(domain_inv.capabilities),
                "cross_references": domain_inv.cross_references
            },
            "tools": [asdict(tool) for tool in domain_inv.tools]
        }
    elif args.summary:
        # Summary view
        output = {
            "timestamp": inventory.timestamp,
            "repository_stats": inventory.repository_stats,
            "domain_summary": {
                domain: {
                    "total_tools": inv.total_tools,
                    "active_tools": inv.active_tools,
                    "deprecated_tools": inv.deprecated_tools,
                    "ssot_compliant_tools": sum(1 for t in inv.tools if t.ssot_compliant),
                    "capabilities_count": len(inv.capabilities)
                }
                for domain, inv in inventory.domain_inventories.items()
            },
            "integration_readiness": inventory.integration_readiness,
            "recommendations": inventory.recommendations
        }
    else:
        # Full inventory
        output = asdict(inventory)

    # Save to file
    with open(args.output, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Project inventory saved to {args.output}")

    # Print summary
    print("\n📊 INVENTORY SUMMARY:")
    print(f"  • Total domains: {len(inventory.domain_inventories)}")
    print(f"  • Total tools: {sum(inv.total_tools for inv in inventory.domain_inventories.values())}")
    print(f"  • Active tools: {sum(inv.active_tools for inv in inventory.domain_inventories.values())}")
    print(f"  • Integration readiness: {inventory.integration_readiness.get('overall_readiness_score', 0)}%")
    print(f"  • SSOT compliance: {sum(1 for inv in inventory.domain_inventories.values() if all(t.ssot_compliant for t in inv.tools))} domains fully compliant")


if __name__ == "__main__":
    main()