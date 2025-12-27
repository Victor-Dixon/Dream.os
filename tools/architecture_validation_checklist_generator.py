#!/usr/bin/env python3
"""
Architecture Validation Checklist Generator
===========================================

Generates comprehensive architecture validation checklists for post-deployment
validation, code reviews, and architecture compliance verification.

This tool would have been helpful during the post-deployment validation planning
to automatically generate validation checklists based on architecture patterns,
V2 compliance requirements, and site-specific validation needs.

Usage:
    python tools/architecture_validation_checklist_generator.py --type post-deployment --site tradingrobotplug.com
    python tools/architecture_validation_checklist_generator.py --type code-review --file path/to/file.php
    python tools/architecture_validation_checklist_generator.py --type v2-compliance --directory src/
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class ArchitectureValidationChecklistGenerator:
    """Generates architecture validation checklists."""
    
    def __init__(self):
        self.v2_compliance_rules = {
            "file_size": {"max_lines": 300, "description": "Files must be < 300 lines"},
            "function_size": {"max_lines": 30, "description": "Functions must be < 30 lines"},
            "class_size": {"max_lines": 200, "description": "Classes must be < 200 lines"},
            "ssot_tags": {"required": True, "description": "All files must have SSOT domain tags"}
        }
        
        self.wordpress_patterns = {
            "modular_functions": {
                "description": "Modular functions.php structure with inc/ directory",
                "checks": [
                    "functions.php loads modules from inc/ directory",
                    "Each module is < 300 lines (V2 compliant)",
                    "Module boundaries are clear and well-defined",
                    "No circular dependencies between modules"
                ]
            },
            "rest_api": {
                "description": "REST API endpoint registration",
                "checks": [
                    "All endpoints registered with register_rest_route()",
                    "Endpoint namespaces follow convention (wp/v2/theme-name)",
                    "Permission callbacks are defined",
                    "All endpoints are accessible via /wp-json/",
                    "Error handling is implemented"
                ]
            },
            "dark_theme": {
                "description": "Dark theme CSS architecture",
                "checks": [
                    "CSS variables defined in variables.css",
                    "Dark theme colors use CSS variables",
                    "Light theme fallback implemented",
                    "Theme toggle functionality (if applicable)",
                    "Color contrast meets WCAG standards"
                ]
            },
            "mobile_responsive": {
                "description": "Mobile responsive architecture",
                "checks": [
                    "Breakpoints defined (mobile, tablet, desktop)",
                    "Media queries use consistent breakpoints",
                    "Touch targets are appropriately sized",
                    "Layout adapts correctly at each breakpoint",
                    "No horizontal scrolling on mobile"
                ]
            }
        }
    
    def generate_post_deployment_checklist(
        self, 
        site_name: str,
        validation_scope: List[str]
    ) -> Dict[str, Any]:
        """Generate post-deployment validation checklist."""
        checklist = {
            "site": site_name,
            "generated": datetime.now().isoformat(),
            "scope": validation_scope,
            "sections": []
        }
        
        if "architecture" in validation_scope:
            checklist["sections"].append({
                "section": "Architecture Validation",
                "checks": [
                    "Review modular functions.php structure",
                    "Verify module boundaries and dependencies",
                    "Check for circular dependencies",
                    "Validate file organization and structure",
                    "Review theme file structure"
                ]
            })
        
        if "rest_api" in validation_scope:
            checklist["sections"].append({
                "section": "REST API Validation",
                "checks": [
                    "Verify all endpoints registered",
                    "Test each endpoint accessibility",
                    "Validate endpoint naming conventions",
                    "Check permission callbacks",
                    "Verify error handling",
                    "Test endpoint responses"
                ]
            })
        
        if "v2_compliance" in validation_scope:
            checklist["sections"].append({
                "section": "V2 Compliance Validation",
                "checks": [
                    f"Verify all files < {self.v2_compliance_rules['file_size']['max_lines']} lines",
                    f"Verify all functions < {self.v2_compliance_rules['function_size']['max_lines']} lines",
                    f"Verify all classes < {self.v2_compliance_rules['class_size']['max_lines']} lines",
                    "Verify SSOT domain tags present",
                    "Check code organization and structure"
                ]
            })
        
        if "ui_ux" in validation_scope:
            checklist["sections"].append({
                "section": "UI/UX Validation",
                "checks": [
                    "Verify dark theme implementation",
                    "Check mobile responsive breakpoints",
                    "Validate hero section patterns",
                    "Test form functionality",
                    "Verify CTA visibility and functionality",
                    "Check navigation structure"
                ]
            })
        
        return checklist
    
    def generate_code_review_checklist(
        self,
        file_path: Path,
        file_type: str = "php"
    ) -> Dict[str, Any]:
        """Generate code review checklist for a specific file."""
        checklist = {
            "file": str(file_path),
            "type": file_type,
            "generated": datetime.now().isoformat(),
            "sections": []
        }
        
        # V2 Compliance checks
        checklist["sections"].append({
            "section": "V2 Compliance",
            "checks": [
                f"File size < {self.v2_compliance_rules['file_size']['max_lines']} lines",
                f"All functions < {self.v2_compliance_rules['function_size']['max_lines']} lines",
                f"All classes < {self.v2_compliance_rules['class_size']['max_lines']} lines",
                "SSOT domain tag present",
                "Code organization follows patterns"
            ]
        })
        
        # File-type specific checks
        if file_type == "php":
            checklist["sections"].append({
                "section": "PHP Best Practices",
                "checks": [
                    "Proper error handling",
                    "Input validation and sanitization",
                    "Security best practices (nonces, capabilities)",
                    "WordPress coding standards",
                    "No deprecated functions"
                ]
            })
        elif file_type == "js":
            checklist["sections"].append({
                "section": "JavaScript Best Practices",
                "checks": [
                    "Proper error handling",
                    "No console errors",
                    "ES6+ syntax where appropriate",
                    "Proper variable scoping",
                    "No global namespace pollution"
                ]
            })
        elif file_type == "css":
            checklist["sections"].append({
                "section": "CSS Best Practices",
                "checks": [
                    "CSS variables used for theming",
                    "Mobile responsive breakpoints",
                    "No !important overuse",
                    "Proper specificity",
                    "Accessibility considerations"
                ]
            })
        
        return checklist
    
    def format_checklist_markdown(self, checklist: Dict[str, Any]) -> str:
        """Format checklist as markdown."""
        lines = []
        
        if "site" in checklist:
            lines.append(f"# Architecture Validation Checklist - {checklist['site']}")
        elif "file" in checklist:
            lines.append(f"# Code Review Checklist - {Path(checklist['file']).name}")
        
        lines.append("")
        lines.append(f"**Generated:** {checklist['generated']}")
        lines.append("")
        
        if "scope" in checklist:
            lines.append(f"**Validation Scope:** {', '.join(checklist['scope'])}")
            lines.append("")
        
        for section in checklist["sections"]:
            lines.append(f"## {section['section']}")
            lines.append("")
            for i, check in enumerate(section["checks"], 1):
                lines.append(f"- [ ] {check}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate architecture validation checklists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post-deployment validation for TradingRobotPlug.com
  python tools/architecture_validation_checklist_generator.py \\
    --type post-deployment \\
    --site tradingrobotplug.com \\
    --scope architecture rest_api v2_compliance ui_ux

  # Code review checklist for a PHP file
  python tools/architecture_validation_checklist_generator.py \\
    --type code-review \\
    --file path/to/file.php

  # V2 compliance checklist for a directory
  python tools/architecture_validation_checklist_generator.py \\
    --type v2-compliance \\
    --directory src/
        """
    )
    
    parser.add_argument(
        "--type",
        required=True,
        choices=["post-deployment", "code-review", "v2-compliance"],
        help="Type of checklist to generate"
    )
    
    parser.add_argument(
        "--site",
        help="Site name (for post-deployment validation)"
    )
    
    parser.add_argument(
        "--file",
        type=Path,
        help="File path (for code-review)"
    )
    
    parser.add_argument(
        "--directory",
        type=Path,
        help="Directory path (for v2-compliance)"
    )
    
    parser.add_argument(
        "--scope",
        nargs="+",
        default=["architecture", "rest_api", "v2_compliance", "ui_ux"],
        help="Validation scope (for post-deployment)"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)"
    )
    
    args = parser.parse_args()
    
    generator = ArchitectureValidationChecklistGenerator()
    
    if args.type == "post-deployment":
        if not args.site:
            parser.error("--site is required for post-deployment validation")
        checklist = generator.generate_post_deployment_checklist(
            args.site,
            args.scope
        )
    elif args.type == "code-review":
        if not args.file:
            parser.error("--file is required for code-review")
        file_type = args.file.suffix.lstrip(".")
        checklist = generator.generate_code_review_checklist(
            args.file,
            file_type
        )
    elif args.type == "v2-compliance":
        # TODO: Implement directory scanning
        print("V2 compliance directory scanning not yet implemented")
        sys.exit(1)
    
    markdown = generator.format_checklist_markdown(checklist)
    
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
        print(f"✅ Checklist generated: {args.output}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()

