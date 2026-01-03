#!/usr/bin/env python3
"""
Unified Validator - SSOT for Validation Operations
=================================================

Centralized validation system providing comprehensive validation capabilities
across different domains: SSOT config, imports, code-docs alignment, queue behavior,
session transitions, and refactoring status.

<!-- SSOT Domain: tools -->

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-02
V2 Compliant: Yes (<300 lines)
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from src.core.utils.validation_utils import ValidationReporter


@dataclass
class ValidationResult:
    """Standard validation result structure."""
    success: bool
    errors: List[str]
    warnings: List[str]
    data: Optional[Dict[str, Any]] = None


class UnifiedValidator(ValidationReporter):
    """
    Unified validation system consolidating all validation operations.

    Provides SSOT for validation across:
    - SSOT configuration compliance
    - Import statement validation
    - Code-documentation alignment
    - Message queue behavior
    - Agent session transitions
    - Refactoring status tracking
    """

    def __init__(self):
        """Initialize validator with project root context."""
        self.project_root = Path(__file__).resolve().parent.parent
        self.errors = []
        self.warnings = []

    def validate_ssot_config(
        self,
        file_path: Optional[str] = None,
        dir_path: Optional[str] = None
    ) -> ValidationResult:
        """
        Validate SSOT configuration compliance.

        Args:
            file_path: Specific file to validate
            dir_path: Directory to validate recursively

        Returns:
            ValidationResult with success status and details
        """
        self.errors = []
        self.warnings = []

        try:
            if file_path:
                return self._validate_single_file_ssot(file_path)
            elif dir_path:
                return self._validate_directory_ssot(dir_path)
            else:
                return self._validate_project_ssot()
        except Exception as e:
            self.errors.append(f"SSOT validation failed: {str(e)}")
            return ValidationResult(False, self.errors, self.warnings)

    def _validate_single_file_ssot(self, file_path: str) -> ValidationResult:
        """Validate SSOT compliance for a single file."""
        if not os.path.exists(file_path):
            self.errors.append(f"File not found: {file_path}")
            return ValidationResult(False, self.errors, self.warnings)

        # Basic SSOT validation - check for domain tags
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for SSOT domain tag
        if '<!-- SSOT Domain:' not in content:
            self.warnings.append(f"Missing SSOT domain tag in {file_path}")

        return ValidationResult(True, self.errors, self.warnings, {"file": file_path})

    def _validate_directory_ssot(self, dir_path: str) -> ValidationResult:
        """Validate SSOT compliance for a directory."""
        if not os.path.exists(dir_path):
            self.errors.append(f"Directory not found: {dir_path}")
            return ValidationResult(False, self.errors, self.warnings)

        results = []
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.py', '.md', '.json', '.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    result = self._validate_single_file_ssot(file_path)
                    results.append(result)

        return ValidationResult(True, self.errors, self.warnings, {"results": results})

    def _validate_project_ssot(self) -> ValidationResult:
        """Validate SSOT compliance for entire project."""
        return self._validate_directory_ssot(str(self.project_root))

    def validate_imports(self, file_path: str) -> ValidationResult:
        """
        Validate import statements in a Python file.

        Args:
            file_path: Python file to validate

        Returns:
            ValidationResult with import validation details
        """
        self.errors = []
        self.warnings = []

        try:
            if not os.path.exists(file_path):
                self.errors.append(f"File not found: {file_path}")
                return ValidationResult(False, self.errors, self.warnings)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic import validation
            import_lines = [line.strip() for line in content.split('\n')
                          if line.strip().startswith(('import ', 'from '))]

            for line in import_lines:
                if not self._validate_import_syntax(line):
                    self.errors.append(f"Invalid import syntax: {line}")

            return ValidationResult(True, self.errors, self.warnings,
                                  {"imports": import_lines})

        except Exception as e:
            self.errors.append(f"Import validation failed: {str(e)}")
            return ValidationResult(False, self.errors, self.warnings)

    def _validate_import_syntax(self, import_line: str) -> bool:
        """Validate basic import statement syntax."""
        # Simple regex validation for import statements
        import_pattern = r'^(import\s+\w+(\.\w+)*(\s+as\s+\w+)?|from\s+\w+(\.\w+)*\s+import\s+(\w+|\*|\(\s*\w+(\s+as\s+\w+)?(\s*,\s*\w+(\s+as\s+\w+)?)*\s*\)))'
        return bool(re.match(import_pattern, import_line))

    def validate_code_docs_alignment(
        self,
        code_file: str,
        doc_files: List[str]
    ) -> ValidationResult:
        """
        Validate alignment between code and documentation.

        Args:
            code_file: Python code file
            doc_files: List of documentation files

        Returns:
            ValidationResult with alignment analysis
        """
        self.errors = []
        self.warnings = []

        try:
            if not os.path.exists(code_file):
                self.errors.append(f"Code file not found: {code_file}")
                return ValidationResult(False, self.errors, self.warnings)

            # Basic validation - check if files exist
            missing_docs = []
            for doc_file in doc_files:
                if not os.path.exists(doc_file):
                    missing_docs.append(doc_file)

            if missing_docs:
                self.errors.extend([f"Documentation file not found: {doc}"
                                  for doc in missing_docs])

            return ValidationResult(True, self.errors, self.warnings,
                                  {"code_file": code_file, "doc_files": doc_files})

        except Exception as e:
            self.errors.append(f"Code-docs validation failed: {str(e)}")
            return ValidationResult(False, self.errors, self.warnings)

    def validate_queue_behavior(self) -> ValidationResult:
        """
        Validate message queue behavior and health.

        Returns:
            ValidationResult with queue status
        """
        self.errors = []
        self.warnings = []

        try:
            # Basic queue validation - check if queue components exist
            queue_files = [
                "src/core/message_queue/__init__.py",
                "src/core/message_queue/core/processor.py",
                "src/core/message_queue_registry.py"
            ]

            missing_files = []
            for file_path in queue_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)

            if missing_files:
                self.errors.extend([f"Missing queue component: {file}"
                                  for file in missing_files])

            return ValidationResult(True, self.errors, self.warnings,
                                  {"queue_components": queue_files})

        except Exception as e:
            self.errors.append(f"Queue validation failed: {str(e)}")
            return ValidationResult(False, self.errors, self.warnings)

    def validate_session_transition(self, agent: Optional[str] = None) -> ValidationResult:
        """
        Validate agent session transition state.

        Args:
            agent: Specific agent to validate (optional)

        Returns:
            ValidationResult with session status
        """
        self.errors = []
        self.warnings = []

        try:
            # Basic session validation - check workspace structure
            if agent:
                workspace_path = f"agent_workspaces/{agent}"
                if not os.path.exists(workspace_path):
                    self.errors.append(f"Agent workspace not found: {workspace_path}")
            else:
                # Check for any agent workspaces
                workspaces_dir = "agent_workspaces"
                if not os.path.exists(workspaces_dir):
                    self.warnings.append("No agent workspaces directory found")

            return ValidationResult(True, self.errors, self.warnings,
                                  {"agent": agent})

        except Exception as e:
            self.errors.append(f"Session validation failed: {str(e)}")
            return ValidationResult(False, self.errors, self.warnings)

    def validate_refactor_status(self, file_path: Optional[str] = None) -> ValidationResult:
        """
        Validate refactoring status and progress.

        Args:
            file_path: Specific file to check refactor status

        Returns:
            ValidationResult with refactor status
        """
        self.errors = []
        self.warnings = []

        try:
            # Basic refactor validation - check for common refactor indicators
            if file_path:
                if not os.path.exists(file_path):
                    self.errors.append(f"File not found: {file_path}")
                    return ValidationResult(False, self.errors, self.warnings)

                # Check for TODO/FIXME comments as refactor indicators
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                refactor_indicators = ['TODO', 'FIXME', 'REFACTOR', 'HACK']
                found_indicators = []

                for indicator in refactor_indicators:
                    if indicator in content.upper():
                        found_indicators.append(indicator)

                if found_indicators:
                    self.warnings.append(f"Found refactor indicators: {', '.join(found_indicators)}")

            return ValidationResult(True, self.errors, self.warnings,
                                  {"file": file_path})

        except Exception as e:
            self.errors.append(f"Refactor validation failed: {str(e)}")
            return ValidationResult(False, self.errors, self.warnings)


# Export the main validator class
__all__ = ["UnifiedValidator", "ValidationResult"]