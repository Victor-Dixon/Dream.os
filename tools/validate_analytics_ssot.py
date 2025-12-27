#!/usr/bin/env python3
"""
Validate Analytics SSOT Compliance
===================================

Validates analytics tools for SSOT (Single Source of Truth) compliance.
Checks for SSOT tags, domain consistency, and metrics collection compliance.

V2 Compliance | Author: Agent-5 | Date: 2025-12-26
"""

import json
import sys
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class AnalyticsSSOTValidator:
    """Validates analytics SSOT compliance."""
    
    def __init__(self):
        """Initialize validator."""
        self.results_file = project_root / "agent_workspaces" / "Agent-5" / "ANALYTICS_SSOT_VALIDATION_RESULTS.json"
        self.analytics_domain = "analytics"
        
    def find_analytics_tools(self) -> List[Path]:
        """
        Find all analytics tools in codebase.
        
        Returns:
            List of analytics tool paths
        """
        tools_dir = project_root / "tools"
        websites_tools_dir = Path("D:/websites/tools") if Path("D:/websites/tools").exists() else None
        
        analytics_tools = []
        
        # Search for analytics-related tools
        patterns = [
            "*analytics*.py",
            "*metrics*.py",
            "*ga4*.py",
            "*pixel*.py",
            "*tracking*.py"
        ]
        
        for pattern in patterns:
            # Search in main tools directory
            for tool in tools_dir.rglob(pattern):
                if tool.is_file() and tool.suffix == ".py":
                    analytics_tools.append(tool)
            
            # Search in websites tools directory
            if websites_tools_dir:
                for tool in websites_tools_dir.rglob(pattern):
                    if tool.is_file() and tool.suffix == ".py":
                        analytics_tools.append(tool)
        
        return list(set(analytics_tools))
    
    def check_ssot_tags(self, tool_path: Path) -> Dict[str, Any]:
        """
        Check if tool has SSOT tags.
        
        Args:
            tool_path: Path to tool file
            
        Returns:
            SSOT tag validation results
        """
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for SSOT-related comments or tags
            has_ssot_comment = "SSOT" in content or "ssot" in content or "single source of truth" in content.lower()
            has_domain_tag = f"domain: {self.analytics_domain}" in content.lower() or f"domain={self.analytics_domain}" in content.lower()
            
            # Check for analytics domain indicators
            has_analytics_domain = "analytics" in content.lower() and ("domain" in content.lower() or "ssot" in content.lower())
            
            return {
                "has_ssot_comment": has_ssot_comment,
                "has_domain_tag": has_domain_tag,
                "has_analytics_domain": has_analytics_domain,
                "compliant": has_ssot_comment or has_domain_tag or has_analytics_domain
            }
        except Exception as e:
            return {
                "error": str(e),
                "compliant": False
            }
    
    def validate_metrics_collection_ssot(self) -> Dict[str, Any]:
        """
        Validate metrics collection SSOT compliance.
        
        Returns:
            Validation results
        """
        config_file = project_root / "agent_workspaces" / "Agent-5" / "P0_METRICS_COLLECTION_CONFIG.json"
        results_file = project_root / "agent_workspaces" / "Agent-5" / "P0_METRICS_COLLECTION_RESULTS.json"
        
        validation = {
            "config_file_exists": config_file.exists(),
            "results_file_exists": results_file.exists(),
            "config_valid": False,
            "ssot_compliant": False
        }
        
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                
                validation["config_valid"] = True
                # Check for SSOT indicators in config
                validation["ssot_compliant"] = "ssot" in str(config).lower() or "domain" in str(config).lower()
            except Exception as e:
                validation["error"] = str(e)
        
        return validation
    
    def validate_all(self) -> Dict[str, Any]:
        """
        Validate all analytics tools for SSOT compliance.
        
        Returns:
            Complete validation results
        """
        analytics_tools = self.find_analytics_tools()
        
        results = {
            "validation_date": datetime.now().isoformat(),
            "analytics_domain": self.analytics_domain,
            "tools_found": len(analytics_tools),
            "tools_validated": [],
            "metrics_collection": self.validate_metrics_collection_ssot(),
            "summary": {
                "total_tools": 0,
                "compliant_tools": 0,
                "non_compliant_tools": 0,
                "compliance_rate": 0.0
            }
        }
        
        for tool_path in analytics_tools:
            tool_result = {
                "tool": str(tool_path.relative_to(project_root) if tool_path.is_relative_to(project_root) else tool_path),
                "ssot_validation": self.check_ssot_tags(tool_path)
            }
            results["tools_validated"].append(tool_result)
        
        # Calculate summary
        results["summary"]["total_tools"] = len(results["tools_validated"])
        compliant = sum(1 for t in results["tools_validated"] if t["ssot_validation"].get("compliant", False))
        results["summary"]["compliant_tools"] = compliant
        results["summary"]["non_compliant_tools"] = results["summary"]["total_tools"] - compliant
        if results["summary"]["total_tools"] > 0:
            results["summary"]["compliance_rate"] = compliant / results["summary"]["total_tools"]
        
        # Save results
        self.results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return results


def main():
    """Main execution."""
    validator = AnalyticsSSOTValidator()
    results = validator.validate_all()
    
    print("✅ Analytics SSOT Validation Complete")
    print(f"Tools Found: {results['summary']['total_tools']}")
    print(f"Compliant: {results['summary']['compliant_tools']}")
    print(f"Non-Compliant: {results['summary']['non_compliant_tools']}")
    print(f"Compliance Rate: {results['summary']['compliance_rate']:.1%}")
    print(f"\nResults saved to: {validator.results_file}")
    
    # List non-compliant tools
    non_compliant = [t for t in results["tools_validated"] if not t["ssot_validation"].get("compliant", False)]
    if non_compliant:
        print("\n⚠️  Non-Compliant Tools:")
        for tool in non_compliant:
            print(f"  - {tool['tool']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

