#!/usr/bin/env python3
"""
A+++ Closure Format Validator

Validates session closure documents against A+++ standard.
Returns pass/fail with specific violations.

Usage:
    python tools/validate_closure_format.py <closure_file.md>
    python tools/validate_closure_format.py --check <closure_file.md>
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Required fields in A+++ closure format
REQUIRED_FIELDS = [
    'Task',
    'Project',
    'Actions Taken',
    'Artifacts Created / Updated',
    'Verification',
    'Public Build Signal',
    'Git Commit',
    'Git Push',
    'Website Blogging',
    'Status'
]

# Forbidden elements
FORBIDDEN_PATTERNS = [
    (r'\bnext steps?\b', 'Next steps'),
    (r'\btodo\b', 'TODO'),
    (r'\bfuture work\b', 'Future work'),
    (r'\bremaining tasks?\b', 'Remaining tasks'),
    (r'\bshould work\b', 'Speculation: "should work"'),
    (r'\bmay need\b', 'Speculation: "may need"'),
    (r'\bcould be\b', 'Speculation: "could be"'),
    (r'\bmight require\b', 'Speculation: "might require"'),
    (r'\bmade progress\b', 'Progress report language'),
    (r'\bstarted working\b', 'Progress report language'),
    (r'\bpartially completed\b', 'Progress report language'),
]

# Speculation words
SPECULATION_WORDS = [
    'should', 'may', 'might', 'could', 'possibly', 'perhaps',
    'probably', 'likely', 'unlikely', 'maybe'
]


class ClosureValidator:
    """Validates closure documents against A+++ standard"""
    
    def __init__(self, content: str):
        self.content = content
        self.violations = []
        self.warnings = []
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate closure format.
        
        Returns:
            (is_valid, violations, warnings)
        """
        # Check required fields
        self._check_required_fields()
        
        # Check forbidden elements
        self._check_forbidden_elements()
        
        # Check public build signal format
        self._check_public_build_signal()
        
        # Check verification block
        self._check_verification_block()
        
        # Check status
        self._check_status()
        
        is_valid = len(self.violations) == 0
        return is_valid, self.violations, self.warnings
    
    def _check_required_fields(self):
        """Check that all required fields are present"""
        content_lower = self.content.lower()
        
        for field in REQUIRED_FIELDS:
            # Check for field in various formats
            patterns = [
                f'**{field}:**',
                f'**{field}**',
                f'#{field}',
                f'## {field}',
                field.lower()
            ]
            
            found = False
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    found = True
                    break
            
            if not found:
                self.violations.append(f'Missing required field: {field}')
    
    def _check_forbidden_elements(self):
        """Check for forbidden language patterns"""
        content_lower = self.content.lower()
        
        for pattern, description in FORBIDDEN_PATTERNS:
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                # Get context (20 chars before and after)
                start = max(0, match.start() - 20)
                end = min(len(self.content), match.end() + 20)
                context = self.content[start:end].replace('\n', ' ')
                self.violations.append(
                    f'Forbidden element found: {description} (context: "...{context}...")'
                )
    
    def _check_public_build_signal(self):
        """Check that Public Build Signal is single line"""
        # Find Public Build Signal section
        # Stop at next ** field or end of content
        signal_pattern = r'\*\*Public Build Signal:\*\*?\s*\n\s*([^\n]+(?:\n(?!\s*\*\*)[^\n]+)*)'
        match = re.search(signal_pattern, self.content, re.IGNORECASE | re.MULTILINE)
        
        if not match:
            return  # Already caught by required fields check
        
        signal_content = match.group(1).strip()
        
        # Split by newlines and filter
        # Take only the first non-empty line (the actual signal)
        lines = [line.strip() for line in signal_content.split('\n') if line.strip()]
        
        # Filter out lines that look like next section headers
        content_lines = [line for line in lines if not line.startswith('**') and not line.startswith('#')]
        
        # Check if it's multiple content lines
        if len(content_lines) > 1:
            self.violations.append(
                f'Public Build Signal must be single line (found {len(content_lines)} content lines)'
            )
        
        # Check length (should be reasonable for one sentence)
        # Use first content line only
        first_line = content_lines[0] if content_lines else signal_content.split('\n')[0].strip()
        if len(first_line) > 200:
            self.warnings.append(
                'Public Build Signal is very long (>200 chars) - should be one sentence'
            )
    
    def _check_verification_block(self):
        """Check that verification block contains evidence"""
        # Find Verification section
        verification_pattern = r'\*\*Verification:\*\*?\s*\n(.+?)(?=\n\s*\*\*|\n\s*#|\Z)'
        match = re.search(verification_pattern, self.content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return  # Already caught by required fields check
        
        verification_content = match.group(1).strip()
        
        # Check if it's empty or just placeholder text
        if not verification_content or len(verification_content) < 10:
            self.violations.append(
                'Verification block is empty or too short - must contain proof/evidence'
            )
        
        # Check for evidence indicators
        evidence_indicators = ['✅', 'verified', 'tested', 'confirmed', 'deployed', 'checked']
        has_evidence = any(indicator.lower() in verification_content.lower() 
                          for indicator in evidence_indicators)
        
        if not has_evidence:
            self.warnings.append(
                'Verification block may lack concrete evidence - should include proof'
            )
    
    def _check_status(self):
        """Check that status is valid"""
        status_pattern = r'\*\*Status:\*\*?\s*\n\s*([✅🟡].+?)(?=\n|\Z)'
        match = re.search(status_pattern, self.content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return  # Already caught by required fields check
        
        status = match.group(1).strip()
        
        if '✅' not in status and '🟡' not in status:
            self.violations.append(
                'Status must be ✅ Ready or 🟡 Blocked (with reason)'
            )
        
        if '🟡' in status and 'blocked' not in status.lower():
            self.warnings.append(
                'Blocked status should include specific reason'
            )


def validate_file(file_path: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a closure file.
    
    Args:
        file_path: Path to closure file
        
    Returns:
        (is_valid, violations, warnings)
    """
    if not file_path.exists():
        return False, [f'File not found: {file_path}'], []
    
    content = file_path.read_text(encoding='utf-8')
    validator = ClosureValidator(content)
    return validator.validate()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python tools/validate_closure_format.py <closure_file.md>")
        print("   or: python tools/validate_closure_format.py --check <closure_file.md>")
        sys.exit(1)
    
    file_path = Path(sys.argv[-1])
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    is_valid, violations, warnings = validate_file(file_path)
    
    if is_valid and not warnings:
        print(f"✅ Closure format is valid: {file_path}")
        sys.exit(0)
    
    if violations:
        print(f"❌ Closure format violations in {file_path}:")
        for violation in violations:
            print(f"   - {violation}")
    
    if warnings:
        print(f"⚠️  Warnings in {file_path}:")
        for warning in warnings:
            print(f"   - {warning}")
    
    if violations:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

