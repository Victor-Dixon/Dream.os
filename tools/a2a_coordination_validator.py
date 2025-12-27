#!/usr/bin/env python3
"""
A2A Coordination Validator Tool
===============================

Validates A2A coordination messages to ensure:
- Template is properly applied
- Sender identification is correct
- Message format follows coordination protocol
- Required fields are present

V2 Compliance | Author: Agent-2 | Date: 2025-12-25

<!-- SSOT Domain: integration -->
"""

import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class A2ACoordinationValidator:
    """Validates A2A coordination messages."""
    
    REQUIRED_SECTIONS = [
        "[HEADER] A2A COORDINATION",
        "COORDINATION REQUEST",
        "WHY THIS COORDINATION?",
        "EXPECTED CONTRIBUTION",
        "TIMING",
        "RESPONSE REQUIRED",
        "REPLY FORMAT",
        "REPLY COMMAND"
    ]
    
    REQUIRED_HEADER_FIELDS = [
        "From:",
        "To:",
        "Priority:",
        "Message ID:",
        "Timestamp:"
    ]
    
    def __init__(self):
        """Initialize validator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.validations: List[str] = []
    
    def validate_message_file(self, message_path: Path) -> Dict[str, Any]:
        """Validate A2A message from file."""
        if not message_path.exists():
            return {
                "valid": False,
                "error": f"Message file not found: {message_path}"
            }
        
        content = message_path.read_text(encoding='utf-8')
        return self.validate_message_content(content)
    
    def validate_message_content(self, content: str) -> Dict[str, Any]:
        """Validate A2A message content."""
        self.errors = []
        self.warnings = []
        self.validations = []
        
        # Check for A2A header
        if "[HEADER] A2A COORDINATION" not in content:
            self.errors.append("Missing A2A coordination header")
            return self._build_result()
        
        # Validate header fields
        self._validate_header(content)
        
        # Validate required sections
        self._validate_sections(content)
        
        # Validate sender identification
        self._validate_sender(content)
        
        # Validate message ID format
        self._validate_message_id(content)
        
        # Validate timestamp format
        self._validate_timestamp(content)
        
        # Validate coordination request content
        self._validate_coordination_request(content)
        
        return self._build_result()
    
    def _validate_header(self, content: str):
        """Validate header fields."""
        for field in self.REQUIRED_HEADER_FIELDS:
            if field not in content:
                self.errors.append(f"Missing required header field: {field}")
            else:
                self.validations.append(f"Header field present: {field}")
    
    def _validate_sections(self, content: str):
        """Validate required sections."""
        for section in self.REQUIRED_SECTIONS:
            if section not in content:
                self.warnings.append(f"Missing section: {section}")
            else:
                self.validations.append(f"Section present: {section}")
    
    def _validate_sender(self, content: str):
        """Validate sender identification."""
        # Check for "From: CAPTAIN" (should be "From: Agent-4" or "From: Agent-X")
        if "From: CAPTAIN" in content:
            self.warnings.append("Sender shows 'CAPTAIN' - should be 'Agent-4' or 'Agent-X' for clarity")
        elif re.search(r"From: Agent-\d+", content):
            self.validations.append("Sender properly identified as Agent-X")
        else:
            self.warnings.append("Sender format unclear")
    
    def _validate_message_id(self, content: str):
        """Validate message ID format."""
        message_id_match = re.search(r"Message ID: ([a-f0-9-]+)", content)
        if message_id_match:
            msg_id = message_id_match.group(1)
            if len(msg_id) == 36 and msg_id.count('-') == 4:  # UUID format
                self.validations.append("Message ID format valid (UUID)")
            else:
                self.warnings.append(f"Message ID format unusual: {msg_id}")
        else:
            self.errors.append("Message ID not found or invalid format")
    
    def _validate_timestamp(self, content: str):
        """Validate timestamp format."""
        timestamp_match = re.search(r"Timestamp: ([0-9T:.-]+)", content)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
            try:
                # Try to parse ISO format
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                self.validations.append("Timestamp format valid (ISO 8601)")
            except ValueError:
                self.warnings.append(f"Timestamp format may be invalid: {timestamp}")
        else:
            self.warnings.append("Timestamp not found or invalid format")
    
    def _validate_coordination_request(self, content: str):
        """Validate coordination request content."""
        if "COORDINATION REQUEST" in content:
            # Check if request has actual content (not just header)
            request_match = re.search(r"\*\*COORDINATION REQUEST\*\*:\s*(.+?)(?=\*\*|$)", content, re.DOTALL)
            if request_match:
                request_content = request_match.group(1).strip()
                if len(request_content) < 10:
                    self.warnings.append("Coordination request content seems too short")
                else:
                    self.validations.append("Coordination request has content")
            else:
                self.warnings.append("Coordination request section may be empty")
    
    def _build_result(self) -> Dict[str, Any]:
        """Build validation result."""
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "validations": self.validations,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "validation_count": len(self.validations)
        }
    
    def validate_inbox_messages(self, agent_id: str, limit: int = 10) -> Dict[str, Any]:
        """Validate recent A2A messages in agent inbox."""
        inbox_path = project_root / "agent_workspaces" / agent_id / "inbox"
        if not inbox_path.exists():
            return {
                "valid": False,
                "error": f"Inbox not found: {inbox_path}"
            }
        
        # Find A2A messages
        a2a_messages = []
        for msg_file in sorted(inbox_path.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
            content = msg_file.read_text(encoding='utf-8')
            if "[HEADER] A2A COORDINATION" in content:
                result = self.validate_message_content(content)
                a2a_messages.append({
                    "file": msg_file.name,
                    "validation": result
                })
        
        return {
            "valid": True,
            "messages_found": len(a2a_messages),
            "messages": a2a_messages,
            "summary": {
                "total": len(a2a_messages),
                "valid": sum(1 for m in a2a_messages if m["validation"]["valid"]),
                "with_errors": sum(1 for m in a2a_messages if m["validation"]["error_count"] > 0),
                "with_warnings": sum(1 for m in a2a_messages if m["validation"]["warning_count"] > 0)
            }
        }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate A2A coordination messages")
    parser.add_argument("--message", type=Path, help="Path to message file to validate")
    parser.add_argument("--agent", help="Agent ID to validate inbox messages")
    parser.add_argument("--limit", type=int, default=10, help="Limit for inbox validation")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    validator = A2ACoordinationValidator()
    
    if args.message:
        result = validator.validate_message_file(args.message)
    elif args.agent:
        result = validator.validate_inbox_messages(args.agent, args.limit)
    else:
        parser.print_help()
        return
    
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'='*60}")
        print("A2A Coordination Message Validation")
        print(f"{'='*60}\n")
        
        if "valid" in result:
            print(f"Status: {'✅ VALID' if result['valid'] else '❌ INVALID'}\n")
            
            if result.get("errors"):
                print("❌ Errors:")
                for error in result["errors"]:
                    print(f"  - {error}")
                print()
            
            if result.get("warnings"):
                print("⚠️  Warnings:")
                for warning in result["warnings"]:
                    print(f"  - {warning}")
                print()
            
            if result.get("validations"):
                print("✅ Validations:")
                for validation in result["validations"][:10]:  # Show first 10
                    print(f"  - {validation}")
                if len(result["validations"]) > 10:
                    print(f"  ... and {len(result['validations']) - 10} more")
                print()
            
            if "summary" in result:
                print("📊 Summary:")
                print(f"  Total messages: {result['summary']['total']}")
                print(f"  Valid: {result['summary']['valid']}")
                print(f"  With errors: {result['summary']['with_errors']}")
                print(f"  With warnings: {result['summary']['with_warnings']}")


if __name__ == "__main__":
    main()



