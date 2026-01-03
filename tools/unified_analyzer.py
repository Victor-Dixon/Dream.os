#!/usr/bin/env python3
"""
Unified Analyzer - SSOT for Analysis Operations
===============================================

Centralized analysis system providing comprehensive analysis capabilities
across different domains: project structure, file analysis, repository comparison,
consolidation opportunities, and overlap detection.

<!-- SSOT Domain: tools -->

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-02
V2 Compliant: Yes (<300 lines)
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from src.core.utils.validation_utils import ValidationReporter


@dataclass
class AnalysisResult:
    """Standard analysis result structure."""
    success: bool
    data: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


class UnifiedAnalyzer(ValidationReporter):
    """
    Unified analysis system consolidating all analysis operations.

    Provides SSOT for analysis across:
    - Project structure analysis
    - Individual file analysis
    - Repository comparison and consolidation
    - Overlap detection and deduplication
    """

    def __init__(self, project_root: Path):
        """
        Initialize analyzer with project root context.

        Args:
            project_root: Root directory of the project to analyze
        """
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []

    def analyze_project_structure(self) -> AnalysisResult:
        """
        Analyze overall project structure and organization.

        Returns:
            AnalysisResult with project structure insights
        """
        self.errors = []
        self.warnings = []

        try:
            structure_data = {
                "directories": {},
                "file_counts": {},
                "total_files": 0,
                "total_dirs": 0
            }

            # Walk through project structure
            for root, dirs, files in os.walk(self.project_root):
                # Skip common ignore directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

                rel_path = os.path.relpath(root, self.project_root)
                if rel_path == '.':
                    rel_path = 'root'

                structure_data["directories"][rel_path] = {
                    "subdirs": len(dirs),
                    "files": len(files)
                }

                structure_data["total_dirs"] += 1
                structure_data["total_files"] += len(files)

                # Count file types
                for file in files:
                    ext = os.path.splitext(file)[1] or 'no_extension'
                    structure_data["file_counts"][ext] = structure_data["file_counts"].get(ext, 0) + 1

            return AnalysisResult(True, structure_data, self.errors, self.warnings)

        except Exception as e:
            self.errors.append(f"Project structure analysis failed: {str(e)}")
            return AnalysisResult(False, {}, self.errors, self.warnings)

    def analyze_file(self, file_path: Path) -> AnalysisResult:
        """
        Analyze a specific file for various metrics.

        Args:
            file_path: Path to the file to analyze

        Returns:
            AnalysisResult with file analysis data
        """
        self.errors = []
        self.warnings = []

        try:
            if not file_path.exists():
                self.errors.append(f"File not found: {file_path}")
                return AnalysisResult(False, {}, self.errors, self.warnings)

            file_data = {
                "path": str(file_path),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size_bytes": file_path.stat().st_size,
                "last_modified": file_path.stat().st_mtime
            }

            # Analyze content if it's a text file
            if file_path.suffix in ['.py', '.md', '.txt', '.json', '.yaml', '.yml']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    file_data.update({
                        "lines": len(content.splitlines()),
                        "characters": len(content),
                        "is_text": True
                    })

                    # Python-specific analysis
                    if file_path.suffix == '.py':
                        file_data.update(self._analyze_python_file(content))

                except UnicodeDecodeError:
                    file_data["is_text"] = False
                    self.warnings.append("File contains non-text content")

            return AnalysisResult(True, file_data, self.errors, self.warnings)

        except Exception as e:
            self.errors.append(f"File analysis failed: {str(e)}")
            return AnalysisResult(False, {}, self.errors, self.warnings)

    def _analyze_python_file(self, content: str) -> Dict[str, Any]:
        """Analyze Python file content for code metrics."""
        lines = content.splitlines()

        # Count various code elements
        imports = sum(1 for line in lines if line.strip().startswith(('import ', 'from ')))
        classes = sum(1 for line in lines if line.strip().startswith('class '))
        functions = sum(1 for line in lines if line.strip().startswith(('def ', '    def ')))
        comments = sum(1 for line in lines if line.strip().startswith('#'))

        return {
            "imports": imports,
            "classes": classes,
            "functions": functions,
            "comments": comments,
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        }

    def analyze_repository_comparison(self, repos: List[str]) -> AnalysisResult:
        """
        Compare multiple repositories for consolidation opportunities.

        Args:
            repos: List of repository paths to compare

        Returns:
            AnalysisResult with comparison data
        """
        self.errors = []
        self.warnings = []

        try:
            comparison_data = {
                "repositories": [],
                "common_files": {},
                "unique_files": {},
                "total_comparison_size": 0
            }

            for repo_path in repos:
                repo_path = Path(repo_path)
                if not repo_path.exists():
                    self.errors.append(f"Repository not found: {repo_path}")
                    continue

                repo_info = {
                    "path": str(repo_path),
                    "name": repo_path.name,
                    "files": []
                }

                # Get all files in repository
                for root, dirs, files in os.walk(repo_path):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
                    for file in files:
                        file_path = os.path.relpath(os.path.join(root, file), repo_path)
                        repo_info["files"].append(file_path)

                comparison_data["repositories"].append(repo_info)

            return AnalysisResult(True, comparison_data, self.errors, self.warnings)

        except Exception as e:
            self.errors.append(f"Repository comparison failed: {str(e)}")
            return AnalysisResult(False, {}, self.errors, self.warnings)

    def analyze_consolidation_opportunities(self, repos: List[str]) -> AnalysisResult:
        """
        Analyze consolidation opportunities across repositories.

        Args:
            repos: List of repository paths to analyze

        Returns:
            AnalysisResult with consolidation recommendations
        """
        # Use repository comparison as foundation
        comparison_result = self.analyze_repository_comparison(repos)

        if not comparison_result.success:
            return comparison_result

        try:
            consolidation_data = comparison_result.data.copy()
            consolidation_data["recommendations"] = []

            # Basic consolidation logic - identify common file patterns
            all_files = set()
            file_counts = {}

            for repo in consolidation_data["repositories"]:
                repo_files = set(repo["files"])
                all_files.update(repo_files)

                for file in repo_files:
                    file_counts[file] = file_counts.get(file, 0) + 1

            # Identify files that exist in multiple repos
            duplicate_files = {file: count for file, count in file_counts.items() if count > 1}

            if duplicate_files:
                consolidation_data["recommendations"].append({
                    "type": "duplicate_files",
                    "description": f"Found {len(duplicate_files)} files duplicated across repositories",
                    "files": list(duplicate_files.keys())[:10],  # Limit for readability
                    "action": "Consider consolidating shared files into common library"
                })

            return AnalysisResult(True, consolidation_data, self.errors, self.warnings)

        except Exception as e:
            self.errors.append(f"Consolidation analysis failed: {str(e)}")
            return AnalysisResult(False, {}, self.errors, self.warnings)

    def analyze_overlaps(self, analysis_dir: str) -> AnalysisResult:
        """
        Analyze overlaps and potential consolidation in a directory.

        Args:
            analysis_dir: Directory to analyze for overlaps

        Returns:
            AnalysisResult with overlap analysis
        """
        self.errors = []
        self.warnings = []

        try:
            analysis_path = Path(analysis_dir)
            if not analysis_path.exists():
                self.errors.append(f"Analysis directory not found: {analysis_dir}")
                return AnalysisResult(False, {}, self.errors, self.warnings)

            overlap_data = {
                "directory": str(analysis_path),
                "file_groups": {},
                "potential_consolidations": []
            }

            # Group files by similar names/extensions
            file_groups = {}
            for root, dirs, files in os.walk(analysis_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

                for file in files:
                    base_name = os.path.splitext(file)[0].lower()
                    ext = os.path.splitext(file)[1]

                    key = f"{base_name}_{ext}"
                    if key not in file_groups:
                        file_groups[key] = []

                    file_groups[key].append(os.path.join(root, file))

            # Identify groups with multiple files
            overlap_data["file_groups"] = {k: v for k, v in file_groups.items() if len(v) > 1}

            if overlap_data["file_groups"]:
                overlap_data["potential_consolidations"].append({
                    "type": "file_groups",
                    "description": f"Found {len(overlap_data['file_groups'])} file groups with potential overlaps",
                    "action": "Review file groups for consolidation opportunities"
                })

            return AnalysisResult(True, overlap_data, self.errors, self.warnings)

        except Exception as e:
            self.errors.append(f"Overlap analysis failed: {str(e)}")
            return AnalysisResult(False, {}, self.errors, self.warnings)


# Export the main analyzer class
__all__ = ["UnifiedAnalyzer", "AnalysisResult"]