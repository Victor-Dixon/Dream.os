#!/usr/bin/env python3
"""
Protocol Validator Tool
=======================

Validates adherence to established protocols and standards.

Usage:
    python tools/protocol_validator.py --protocol session-closure
    python tools/protocol_validator.py --protocol messaging-contracts
    python tools/protocol_validator.py --file path/to/file.md

Features:
- Validates session closures against A+++ standards
- Checks messaging contract compliance
- Verifies protocol adherence across files
- Generates compliance reports

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-28
Purpose: Ensure protocol compliance and quality standards
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class ProtocolValidator:
    """Validates adherence to established protocols."""

    def __init__(self):
        """Initialize the validator."""
        self.protocols = {
            'session-closure': self._validate_session_closure,
            'messaging-contracts': self._validate_messaging_contracts,
            'git-hygiene': self._validate_git_hygiene
        }

    def validate_file(self, file_path: Path, protocol: str) -> Dict[str, Any]:
        """Validate a file against a specific protocol."""
        if protocol not in self.protocols:
            return {'valid': False, 'error': f'Unknown protocol: {protocol}'}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            validator_func = self.protocols[protocol]
            return validator_func(content, file_path)

        except Exception as e:
            return {'valid': False, 'error': str(e)}

    def _validate_session_closure(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Validate session closure against A+++ standards."""
        issues = []
        required_fields = [
            'Task:', 'Project:', 'Actions Taken:', 'Artifacts Created / Updated:',
            'Verification:', 'Public Build Signal:', 'Git Commit:', 'Git Push:',
            'Website Blogging:', 'Status:'
        ]

        # Check required fields
        for field in required_fields:
            if field not in content:
                issues.append(f'Missing required field: {field}')

        # Check forbidden elements
        forbidden_patterns = [
            r'Next steps?', r'next steps?', r'Future work', r'future work',
            r'should work', r'may need', r'might require',
            r'made progress', r'partially completed'
        ]

        for pattern in forbidden_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f'Forbidden content found: {pattern}')

        # Check status format
        if 'Status:' in content:
            status_section = content.split('Status:')[1].split('\n')[0].strip()
            if not (status_section.startswith('✅ Ready') or
                   (status_section.startswith('🟡 Blocked') and '(' in status_section)):
                issues.append('Invalid status format')

        return {
            'valid': len(issues) == 0,
            'protocol': 'session-closure',
            'issues': issues,
            'file_path': str(file_path)
        }

    def _validate_messaging_contracts(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Validate messaging contracts compliance."""
        issues = []

        # Check for required enum definitions
        required_enums = ['UnifiedMessageType', 'UnifiedMessagePriority', 'UnifiedMessageTag']
        for enum in required_enums:
            if enum not in content:
                issues.append(f'Missing required enum: {enum}')

        # Check for critical sections
        required_sections = [
            'Message Types', 'Message Priorities', 'Message Tags',
            'Delivery Mode Flags', 'CLI Command-Line Flags'
        ]

        for section in required_sections:
            if section not in content:
                issues.append(f'Missing required section: {section}')

        return {
            'valid': len(issues) == 0,
            'protocol': 'messaging-contracts',
            'issues': issues,
            'file_path': str(file_path)
        }

    def _validate_git_hygiene(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Validate git hygiene compliance."""
        issues = []

        # Check for conventional commit patterns
        if 'feat:' not in content and 'fix:' not in content and 'docs:' not in content:
            issues.append('Commit message does not follow conventional format')

        # Check for proper description
        lines = content.split('\n')
        if len(lines) < 2 or not lines[1].strip():
            issues.append('Missing commit description')

        return {
            'valid': len(issues) == 0,
            'protocol': 'git-hygiene',
            'issues': issues,
            'file_path': str(file_path)
        }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate adherence to established protocols"
    )
    parser.add_argument(
        "--protocol",
        required=True,
        choices=['session-closure', 'messaging-contracts', 'git-hygiene'],
        help="Protocol to validate against"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="File to validate"
    )

    args = parser.parse_args()

    validator = ProtocolValidator()
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        return 1

    result = validator.validate_file(file_path, args.protocol)

    if result['valid']:
        print(f"✅ VALID: {args.protocol} compliance confirmed")
        print(f"File: {result['file_path']}")
    else:
        print(f"❌ INVALID: {args.protocol} compliance issues found")
        print(f"File: {result['file_path']}")
        for issue in result['issues']:
            print(f"  - {issue}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
