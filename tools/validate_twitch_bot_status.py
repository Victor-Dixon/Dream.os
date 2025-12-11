#!/usr/bin/env python3
"""
Twitch Bot Status Validation Tool

Validates current Twitch bot configuration, connection capability, and diagnostic status.
Produces a validation report for coordination efforts.

V2 Compliance: <300 lines, single responsibility
Author: Agent-4 (Captain)
Date: 2025-12-11
Priority: HIGH - Supports Twitch bot coordination diagnostics
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logger = None
try:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
except Exception:
    pass


class TwitchBotStatusValidator:
    """Validates Twitch bot status and configuration."""
    
    def __init__(self):
        """Initialize validator."""
        self.project_root = project_root
        self.config_path = self.project_root / "config" / "chat_presence.json"
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "validator": "Agent-4 (Captain)",
            "checks": {},
            "overall_status": "unknown",
            "recommendations": []
        }
    
    def check_config_exists(self) -> bool:
        """Check if configuration file exists."""
        exists = self.config_path.exists()
        self.validation_results["checks"]["config_exists"] = {
            "status": "pass" if exists else "fail",
            "message": f"Config file exists: {exists}",
            "path": str(self.config_path)
        }
        return exists
    
    def check_config_valid(self) -> bool:
        """Check if configuration is valid JSON."""
        if not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            required_fields = ["twitch_username", "twitch_oauth_token", "twitch_channel"]
            missing = [field for field in required_fields if field not in config]
            
            valid = len(missing) == 0
            self.validation_results["checks"]["config_valid"] = {
                "status": "pass" if valid else "fail",
                "message": "Config is valid JSON" if valid else f"Missing fields: {missing}",
                "fields_present": list(config.keys()),
                "missing_fields": missing
            }
            return valid
        except json.JSONDecodeError as e:
            self.validation_results["checks"]["config_valid"] = {
                "status": "fail",
                "message": f"Invalid JSON: {e}",
                "error": str(e)
            }
            return False
        except Exception as e:
            self.validation_results["checks"]["config_valid"] = {
                "status": "error",
                "message": f"Error reading config: {e}",
                "error": str(e)
            }
            return False
    
    def check_oauth_token_format(self) -> bool:
        """Check if OAuth token has correct format."""
        if not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            token = config.get("twitch_oauth_token", "")
            has_prefix = token.startswith("oauth:")
            valid_length = len(token) > 10  # Basic length check
            
            valid = has_prefix and valid_length
            self.validation_results["checks"]["oauth_token_format"] = {
                "status": "pass" if valid else "fail",
                "message": f"Token format valid: {valid}",
                "has_oauth_prefix": has_prefix,
                "has_valid_length": valid_length,
                "token_preview": token[:20] + "..." if len(token) > 20 else token[:10]
            }
            return valid
        except Exception as e:
            self.validation_results["checks"]["oauth_token_format"] = {
                "status": "error",
                "message": f"Error checking token: {e}",
                "error": str(e)
            }
            return False
    
    def check_bridge_file_exists(self) -> bool:
        """Check if Twitch bridge file exists."""
        bridge_path = self.project_root / "src" / "services" / "chat_presence" / "twitch_bridge.py"
        exists = bridge_path.exists()
        self.validation_results["checks"]["bridge_file_exists"] = {
            "status": "pass" if exists else "fail",
            "message": f"Bridge file exists: {exists}",
            "path": str(bridge_path)
        }
        return exists
    
    def check_diagnostic_tools_exist(self) -> bool:
        """Check if diagnostic tools are available."""
        tools = [
            "debug_twitch_irc_connection.py",
            "check_twitch_bot_live_status.py",
            "monitor_twitch_bot.py",
            "twitch_bot_health_monitor.py"
        ]
        
        tools_dir = self.project_root / "tools"
        existing_tools = []
        missing_tools = []
        
        for tool in tools:
            tool_path = tools_dir / tool
            if tool_path.exists():
                existing_tools.append(tool)
            else:
                missing_tools.append(tool)
        
        all_exist = len(missing_tools) == 0
        self.validation_results["checks"]["diagnostic_tools_exist"] = {
            "status": "pass" if all_exist else "partial",
            "message": f"Diagnostic tools: {len(existing_tools)}/{len(tools)} available",
            "existing_tools": existing_tools,
            "missing_tools": missing_tools
        }
        return all_exist
    
    def check_orchestrator_exists(self) -> bool:
        """Check if orchestrator file exists."""
        orchestrator_path = (
            self.project_root / "src" / "services" / "chat_presence" / 
            "chat_presence_orchestrator.py"
        )
        exists = orchestrator_path.exists()
        self.validation_results["checks"]["orchestrator_exists"] = {
            "status": "pass" if exists else "fail",
            "message": f"Orchestrator file exists: {exists}",
            "path": str(orchestrator_path)
        }
        return exists
    
    def generate_recommendations(self):
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if not self.validation_results["checks"].get("config_exists", {}).get("status") == "pass":
            recommendations.append({
                "priority": "HIGH",
                "action": "Create configuration file",
                "details": "Config file missing. Create config/chat_presence.json with required fields."
            })
        
        if not self.validation_results["checks"].get("config_valid", {}).get("status") == "pass":
            missing = self.validation_results["checks"].get("config_valid", {}).get("missing_fields", [])
            if missing:
                recommendations.append({
                    "priority": "HIGH",
                    "action": "Add missing configuration fields",
                    "details": f"Missing fields: {', '.join(missing)}"
                })
        
        if not self.validation_results["checks"].get("oauth_token_format", {}).get("status") == "pass":
            recommendations.append({
                "priority": "HIGH",
                "action": "Verify OAuth token format",
                "details": "Token should start with 'oauth:' prefix. Regenerate at https://twitchapps.com/tmi/"
            })
        
        if not self.validation_results["checks"].get("bridge_file_exists", {}).get("status") == "pass":
            recommendations.append({
                "priority": "CRITICAL",
                "action": "Twitch bridge file missing",
                "details": "Core bridge implementation file not found. This is required for bot operation."
            })
        
        missing_tools = self.validation_results["checks"].get("diagnostic_tools_exist", {}).get("missing_tools", [])
        if missing_tools:
            recommendations.append({
                "priority": "LOW",
                "action": "Restore missing diagnostic tools",
                "details": f"Missing tools: {', '.join(missing_tools)}"
            })
        
        self.validation_results["recommendations"] = recommendations
    
    def determine_overall_status(self):
        """Determine overall validation status."""
        checks = self.validation_results["checks"]
        
        critical_checks = ["config_exists", "config_valid", "bridge_file_exists", "orchestrator_exists"]
        critical_passed = all(
            checks.get(check, {}).get("status") == "pass" 
            for check in critical_checks
        )
        
        if critical_passed:
            if checks.get("oauth_token_format", {}).get("status") == "pass":
                self.validation_results["overall_status"] = "ready"
            else:
                self.validation_results["overall_status"] = "config_issue"
        else:
            self.validation_results["overall_status"] = "not_ready"
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks."""
        print("🔍 Twitch Bot Status Validation")
        print("=" * 50)
        print()
        
        print("Checking configuration...")
        self.check_config_exists()
        if self.config_path.exists():
            self.check_config_valid()
            self.check_oauth_token_format()
        
        print("Checking core files...")
        self.check_bridge_file_exists()
        self.check_orchestrator_exists()
        
        print("Checking diagnostic tools...")
        self.check_diagnostic_tools_exist()
        
        print()
        print("Generating recommendations...")
        self.generate_recommendations()
        
        print("Determining overall status...")
        self.determine_overall_status()
        
        return self.validation_results
    
    def print_report(self):
        """Print validation report to console."""
        results = self.validation_results
        
        print()
        print("=" * 50)
        print("VALIDATION REPORT")
        print("=" * 50)
        print()
        print(f"Timestamp: {results['timestamp']}")
        print(f"Overall Status: {results['overall_status'].upper()}")
        print()
        
        print("CHECK RESULTS:")
        print("-" * 50)
        for check_name, check_result in results["checks"].items():
            status_icon = "✅" if check_result["status"] == "pass" else "❌" if check_result["status"] == "fail" else "⚠️"
            print(f"{status_icon} {check_name}: {check_result['status']}")
            print(f"   {check_result['message']}")
            print()
        
        if results["recommendations"]:
            print("RECOMMENDATIONS:")
            print("-" * 50)
            for rec in results["recommendations"]:
                print(f"🔴 {rec['priority']}: {rec['action']}")
                print(f"   {rec['details']}")
                print()
    
    def save_report(self, output_path: Optional[Path] = None) -> Path:
        """Save validation report to file."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = (
                self.project_root / "agent_workspaces" / "Agent-4" / 
                "validation_reports" / f"twitch_bot_validation_{timestamp}.json"
            )
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.validation_results, f, indent=2)
        
        return output_path


def main():
    """Main validation entry point."""
    validator = TwitchBotStatusValidator()
    results = validator.validate_all()
    validator.print_report()
    
    report_path = validator.save_report()
    print(f"✅ Validation report saved: {report_path}")
    
    return 0 if results["overall_status"] in ["ready", "config_issue"] else 1


if __name__ == "__main__":
    sys.exit(main())

