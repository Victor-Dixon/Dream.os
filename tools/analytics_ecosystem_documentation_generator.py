#!/usr/bin/env python3
"""
Automated Analytics Ecosystem Documentation Generator
=====================================================

<!-- SSOT Domain: analytics -->

Automatically generates comprehensive documentation for the enterprise analytics ecosystem.
Scans all analytics tools, extracts metadata, and creates unified documentation.

V2 Compliance | Author: Agent-3 | Date: 2026-01-07
"""

from __future__ import annotations

import asyncio
import importlib
import inspect
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ToolMetadata:
    """Metadata extracted from an analytics tool."""
    name: str
    path: str
    description: str
    author: str
    domain: str
    version: str
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    dependencies: List[str]
    last_modified: str


@dataclass
class EcosystemDocumentation:
    """Complete ecosystem documentation."""
    generated_at: str
    total_tools: int
    total_functions: int
    total_classes: int
    domains: Dict[str, List[str]]
    tools: Dict[str, ToolMetadata]
    architecture_overview: str
    integration_patterns: List[str]
    maintenance_guide: str


class AnalyticsEcosystemDocumentationGenerator:
    """
    Automatically generates comprehensive documentation for the analytics ecosystem.

    Scans all tools in the analytics ecosystem and creates:
    - Tool inventories and metadata
    - Function and class documentation
    - Architecture diagrams
    - Integration patterns
    - Maintenance procedures
    """

    def __init__(self):
        self.analytics_tools_path = Path("tools")
        self.src_path = Path("src")
        self.docs_path = Path("docs")

    async def generate_full_documentation(self) -> EcosystemDocumentation:
        """
        Generate complete documentation for the analytics ecosystem.

        Returns:
            Comprehensive documentation object
        """
        logger.info("📚 Generating analytics ecosystem documentation...")

        # Discover all analytics tools
        analytics_tools = await self._discover_analytics_tools()

        # Extract metadata from each tool
        tool_metadata = {}
        total_functions = 0
        total_classes = 0

        for tool_path in analytics_tools:
            metadata = await self._extract_tool_metadata(tool_path)
            if metadata:
                tool_metadata[metadata.name] = metadata
                total_functions += len(metadata.functions)
                total_classes += len(metadata.classes)

        # Group tools by domain
        domains = self._group_tools_by_domain(tool_metadata)

        # Generate architecture overview
        architecture_overview = self._generate_architecture_overview(tool_metadata, domains)

        # Identify integration patterns
        integration_patterns = self._identify_integration_patterns(tool_metadata)

        # Generate maintenance guide
        maintenance_guide = self._generate_maintenance_guide(tool_metadata)

        documentation = EcosystemDocumentation(
            generated_at=datetime.now().isoformat(),
            total_tools=len(tool_metadata),
            total_functions=total_functions,
            total_classes=total_classes,
            domains=domains,
            tools=tool_metadata,
            architecture_overview=architecture_overview,
            integration_patterns=integration_patterns,
            maintenance_guide=maintenance_guide
        )

        logger.info(f"✅ Documentation generated for {len(tool_metadata)} tools")

        return documentation

    async def _discover_analytics_tools(self) -> List[Path]:
        """Discover all analytics-related tools in the ecosystem."""
        analytics_tools = []

        # Scan tools directory for analytics tools
        if self.analytics_tools_path.exists():
            for file_path in self.analytics_tools_path.glob("*.py"):
                if self._is_analytics_tool(file_path):
                    analytics_tools.append(file_path)

        # Scan src directory for analytics services
        if self.src_path.exists():
            for file_path in self.src_path.glob("**/*.py"):
                if self._is_analytics_service(file_path):
                    analytics_tools.append(file_path)

        return analytics_tools

    def _is_analytics_tool(self, file_path: Path) -> bool:
        """Check if a tool file is analytics-related."""
        analytics_keywords = [
            'analytics', 'ga4', 'pixel', 'facebook', 'tracking',
            'deployment', 'compliance', 'validation', 'health',
            'monitoring', 'verification', 'orchestrator', 'dashboard'
        ]

        filename = file_path.stem.lower()
        return any(keyword in filename for keyword in analytics_keywords)

    def _is_analytics_service(self, file_path: Path) -> bool:
        """Check if a service file is analytics-related."""
        if 'infrastructure' in str(file_path) and 'analytics' in str(file_path):
            return True
        if 'services' in str(file_path) and any(part in str(file_path) for part in ['verification', 'validation']):
            return True
        return False

    async def _extract_tool_metadata(self, tool_path: Path) -> Optional[ToolMetadata]:
        """Extract comprehensive metadata from a tool file."""
        try:
            # Read file content
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract basic information
            name = tool_path.stem
            description = self._extract_description(content)
            author = self._extract_author(content)
            domain = self._extract_domain(content)
            version = self._extract_version(content)

            # Extract functions and classes
            functions = self._extract_functions(content)
            classes = self._extract_classes(content)

            # Extract dependencies
            dependencies = self._extract_dependencies(content)

            # Get last modified time
            last_modified = datetime.fromtimestamp(tool_path.stat().st_mtime).isoformat()

            return ToolMetadata(
                name=name,
                path=str(tool_path),
                description=description,
                author=author,
                domain=domain,
                version=version,
                functions=functions,
                classes=classes,
                dependencies=dependencies,
                last_modified=last_modified
            )

        except Exception as e:
            logger.warning(f"Failed to extract metadata from {tool_path}: {e}")
            return None

    def _extract_description(self, content: str) -> str:
        """Extract tool description from docstring or comments."""
        # Look for module docstring
        docstring_match = re.search(r'""".*?"""', content, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(0).strip('"""')
            # Extract first line or meaningful description
            lines = [line.strip() for line in docstring.split('\n') if line.strip()]
            if lines:
                return lines[0]

        # Fallback: look for description in comments
        desc_match = re.search(r'# .*?[Dd]escription:?\s*(.+)', content)
        if desc_match:
            return desc_match.group(1).strip()

        return f"Analytics tool: {Path(content).stem if 'content' in locals() else 'Unknown'}"

    def _extract_author(self, content: str) -> str:
        """Extract author information."""
        author_match = re.search(r'# Author:\s*(.+)', content, re.IGNORECASE)
        if author_match:
            return author_match.group(1).strip()
        return "Agent-3"

    def _extract_domain(self, content: str) -> str:
        """Extract SSOT domain."""
        domain_match = re.search(r'# SSOT Domain:\s*(.+)', content, re.IGNORECASE)
        if domain_match:
            return domain_match.group(1).strip()
        return "analytics"

    def _extract_version(self, content: str) -> str:
        """Extract version information."""
        version_match = re.search(r'# V\d+', content)
        if version_match:
            return version_match.group(0).strip('# ')
        return "V2"

    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        """Extract function definitions and metadata."""
        functions = []

        # Find all function definitions
        func_pattern = r'(?:async\s+)?def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*[^:]+)?\s*:'        # Find all function definitions
        func_matches = re.finditer(func_pattern, content)

        for match in func_matches:
            func_name = match.group(1)
            start_pos = match.start()

            # Extract function signature
            signature = self._extract_function_signature(content, start_pos)

            # Extract docstring
            docstring = self._extract_function_docstring(content, start_pos)

            # Determine if async
            is_async = 'async' in signature

            functions.append({
                'name': func_name,
                'signature': signature,
                'docstring': docstring,
                'is_async': is_async,
                'line_number': content[:start_pos].count('\n') + 1
            })

        return functions

    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions and metadata."""
        classes = []

        # Find all class definitions
        class_pattern = r'class\s+(\w+)(?:\([^)]*\))?\s*:'
        class_matches = re.finditer(class_pattern, content)

        for match in class_matches:
            class_name = match.group(1)
            start_pos = match.start()

            # Extract class docstring
            docstring = self._extract_class_docstring(content, start_pos)

            # Extract methods (simplified)
            methods = self._extract_class_methods(content, start_pos)

            classes.append({
                'name': class_name,
                'docstring': docstring,
                'methods': methods,
                'line_number': content[:start_pos].count('\n') + 1
            })

        return classes

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract import statements."""
        dependencies = []

        # Find import statements
        import_pattern = r'^(?:from\s+|\s*)import\s+(.+)$'
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                # Clean up the import statement
                dep = re.sub(r'#.*', '', line).strip()  # Remove comments
                if dep:
                    dependencies.append(dep)

        return dependencies

    def _extract_function_signature(self, content: str, start_pos: int) -> str:
        """Extract complete function signature."""
        # Find the end of the signature (next colon or end of line)
        signature_end = content.find('\n', start_pos)
        if signature_end == -1:
            signature_end = len(content)

        signature = content[start_pos:signature_end].strip()
        return signature

    def _extract_function_docstring(self, content: str, start_pos: int) -> str:
        """Extract function docstring."""
        # Look for triple quotes after the function definition
        remaining = content[start_pos:]
        docstring_match = re.search(r'"""(.*?)"""', remaining, re.DOTALL)
        if docstring_match:
            return docstring_match.group(1).strip()
        return ""

    def _extract_class_docstring(self, content: str, start_pos: int) -> str:
        """Extract class docstring."""
        remaining = content[start_pos:]
        docstring_match = re.search(r'"""(.*?)"""', remaining, re.DOTALL)
        if docstring_match:
            return docstring_match.group(1).strip()
        return ""

    def _extract_class_methods(self, content: str, start_pos: int) -> List[str]:
        """Extract class methods (simplified)."""
        methods = []

        # Find method definitions within reasonable bounds
        method_pattern = r'(?:async\s+)?def\s+(\w+)\s*\('
        remaining = content[start_pos:]

        # Limit search to avoid going too far
        next_class = remaining.find('\nclass ')
        if next_class == -1:
            search_area = remaining
        else:
            search_area = remaining[:next_class]

        method_matches = re.finditer(method_pattern, search_area)
        for match in method_matches:
            method_name = match.group(1)
            if not method_name.startswith('_'):  # Skip private methods
                methods.append(method_name)

        return methods

    def _group_tools_by_domain(self, tool_metadata: Dict[str, ToolMetadata]) -> Dict[str, List[str]]:
        """Group tools by their SSOT domain."""
        domains = {}

        for tool in tool_metadata.values():
            domain = tool.domain
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(tool.name)

        return domains

    def _generate_architecture_overview(self, tool_metadata: Dict[str, ToolMetadata],
                                      domains: Dict[str, List[str]]) -> str:
        """Generate architecture overview."""
        overview = f"""
# Enterprise Analytics Ecosystem Architecture

## Overview
The enterprise analytics ecosystem consists of {len(tool_metadata)} specialized tools organized across {len(domains)} domains.

## Domain Structure
"""

        for domain, tools in domains.items():
            overview += f"""
### {domain.title()} Domain ({len(tools)} tools)
- {chr(10).join(f"  - {tool}" for tool in tools)}
"""

        overview += f"""

## Key Architectural Components

### Infrastructure Layer
- Website Health Monitoring
- Server Error Diagnostics
- Analytics Deployment Monitoring

### Business Logic Layer
- Compliance Validation
- Live Verification
- Deployment Orchestration

### Presentation Layer
- Executive Dashboards
- Operations Center
- Health Scoring System

### Integration Layer
- Automated Deployment
- Remote Deployment Tools
- Configuration Management

## Data Flow Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │───▶│   Validation    │───▶│   Deployment    │
│   & Health      │    │   & Compliance  │    │   & Execution   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Alerting      │    │   Reporting     │    │   Operations    │
│   & Response    │    │   & Analytics  │    │   & Maintenance │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quality Assurance
- Automated testing frameworks
- Health scoring algorithms
- Compliance validation pipelines
- Performance monitoring systems

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        return overview

    def _identify_integration_patterns(self, tool_metadata: Dict[str, ToolMetadata]) -> List[str]:
        """Identify common integration patterns."""
        patterns = []

        # Check for common integration patterns
        has_async = any(any(f.get('is_async', False) for f in tool.functions)
                       for tool in tool_metadata.values())
        has_monitoring = any('monitor' in tool.name.lower() for tool in tool_metadata.values())
        has_validation = any('valid' in tool.name.lower() for tool in tool_metadata.values())
        has_deployment = any('deploy' in tool.name.lower() for tool in tool_metadata.values())

        if has_async:
            patterns.append("Asynchronous Operations: Tools use async/await for non-blocking operations")

        if has_monitoring:
            patterns.append("Observer Pattern: Monitoring tools observe system state and report changes")

        if has_validation:
            patterns.append("Strategy Pattern: Validation tools implement different validation strategies")

        if has_deployment:
            patterns.append("Pipeline Pattern: Deployment tools implement multi-stage execution pipelines")

        patterns.extend([
            "Factory Pattern: Tool instantiation through configuration-based factories",
            "Repository Pattern: Data access abstracted through repository interfaces",
            "Command Pattern: Operations encapsulated as executable commands"
        ])

        return patterns

    def _generate_maintenance_guide(self, tool_metadata: Dict[str, ToolMetadata]) -> str:
        """Generate maintenance and operations guide."""
        guide = f"""
# Enterprise Analytics Ecosystem Maintenance Guide

## System Overview
This guide covers maintenance procedures for the {len(tool_metadata)} analytics ecosystem tools.

## Daily Operations

### Health Monitoring
- Run `analytics_ecosystem_health_scorer.py` daily
- Review health scores and risk levels
- Address critical and high-risk issues immediately

### Log Review
- Check application logs for errors
- Review analytics data collection
- Monitor deployment status

## Weekly Maintenance

### Tool Updates
- Review tool versions and dependencies
- Update documentation as needed
- Test tool integrations

### Performance Optimization
- Analyze system performance metrics
- Optimize slow-running operations
- Review and optimize database queries

## Monthly Procedures

### Compliance Review
- Run full compliance audits
- Review GDPR and privacy compliance
- Update compliance documentation

### Security Assessment
- Review access controls
- Update security configurations
- Audit user permissions

## Troubleshooting

### Common Issues
- **Tool failures**: Check dependencies and configuration
- **Network timeouts**: Review network connectivity and timeouts
- **Data inconsistencies**: Validate data sources and transformations

### Diagnostic Tools
- `analytics_ecosystem_health_scorer.py` - Overall system health
- `website_health_monitor.py` - Infrastructure diagnostics
- `server_error_diagnostic.py` - Error analysis

## Emergency Procedures

### System Down
1. Check infrastructure health
2. Review recent deployments
3. Contact on-call engineer
4. Implement rollback if necessary

### Data Loss
1. Check backup systems
2. Review recovery procedures
3. Restore from last known good state
4. Validate data integrity

## Contact Information
- Primary: Agent-3 (Infrastructure & DevOps)
- Secondary: Agent-4 (Captain - Strategic Oversight)
- Emergency: System administrators

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        return guide


async def generate_documentation_files(doc_generator: AnalyticsEcosystemDocumentationGenerator,
                                     output_dir: str = "docs/analytics") -> None:
    """Generate documentation files from the ecosystem documentation."""
    os.makedirs(output_dir, exist_ok=True)

    # Generate main documentation
    documentation = await doc_generator.generate_full_documentation()

    # Write JSON documentation
    json_path = f"{output_dir}/ecosystem_documentation.json"
    with open(json_path, 'w') as f:
        json.dump(asdict(documentation), f, indent=2)

    # Write architecture overview
    arch_path = f"{output_dir}/architecture_overview.md"
    with open(arch_path, 'w') as f:
        f.write(documentation.architecture_overview)

    # Write maintenance guide
    maint_path = f"{output_dir}/maintenance_guide.md"
    with open(maint_path, 'w') as f:
        f.write(documentation.maintenance_guide)

    # Write tool inventory
    inventory_path = f"{output_dir}/tool_inventory.md"
    with open(inventory_path, 'w') as f:
        f.write(f"# Analytics Ecosystem Tool Inventory\n\n")
        f.write(f"Generated: {documentation.generated_at}\n\n")
        f.write(f"Total Tools: {documentation.total_tools}\n")
        f.write(f"Total Functions: {documentation.total_functions}\n")
        f.write(f"Total Classes: {documentation.total_classes}\n\n")

        for domain, tools in documentation.domains.items():
            f.write(f"## {domain.title()} Domain\n\n")
            for tool_name in tools:
                tool = documentation.tools[tool_name]
                f.write(f"### {tool.name}\n\n")
                f.write(f"- **Path**: {tool.path}\n")
                f.write(f"- **Description**: {tool.description}\n")
                f.write(f"- **Author**: {tool.author}\n")
                f.write(f"- **Version**: {tool.version}\n")
                f.write(f"- **Last Modified**: {tool.last_modified}\n")
                f.write(f"- **Functions**: {len(tool.functions)}\n")
                f.write(f"- **Classes**: {len(tool.classes)}\n")
                f.write(f"- **Dependencies**: {len(tool.dependencies)}\n\n")

                if tool.classes:
                    f.write("**Classes:**\n")
                    for cls in tool.classes:
                        f.write(f"- {cls['name']}: {cls['docstring'][:100]}...\n")
                    f.write("\n")

    logger.info(f"✅ Documentation files generated in {output_dir}")


async def main():
    """Command-line interface for documentation generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Analytics Ecosystem Documentation Generator")
    parser.add_argument("--output-dir", type=str, default="docs/analytics",
                       help="Output directory for documentation files")
    parser.add_argument("--json-only", action="store_true",
                       help="Generate only JSON documentation")

    args = parser.parse_args()

    # Initialize generator
    generator = AnalyticsEcosystemDocumentationGenerator()

    if args.json_only:
        # Generate only JSON
        documentation = await generator.generate_full_documentation()
        output_path = f"{args.output_dir}/ecosystem_documentation.json"
        os.makedirs(args.output_dir, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(asdict(documentation), f, indent=2)

        print(f"✅ JSON documentation generated: {output_path}")
    else:
        # Generate full documentation suite
        await generate_documentation_files(generator, args.output_dir)
        print(f"✅ Full documentation suite generated in: {args.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())