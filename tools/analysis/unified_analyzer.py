#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: unified_analyzer module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-analysis-unified-analyzer
# @registry docs/recovery/recovery_registry.yaml#tools-analysis-unified-analyzer

"""
Unified Analyzer
================

Comprehensive project analysis tool for repository structure, file analysis,
consolidation opportunities, and overlap detection.

<!-- SSOT Domain: tools -->

Navigation References:
├── Related Files:
│   ├── Analysis Handlers → src/web/analysis_handlers.py
│   ├── Analysis Routes → src/web/analysis_routes.py
│   ├── Project Inventory → tools/project_inventory_catalog.py
│   └── Directory Audit → tools/directory_audit_helper.py
├── Documentation:
│   └── Analysis API → docs/api/ANALYSIS_API.md
└── Testing:
    └── Analysis Tests → tests/tools/test_unified_analyzer.py

Features:
- Project structure analysis
- File content analysis
- Repository metadata extraction
- Consolidation opportunity detection
- Overlap analysis
- Full analysis orchestration

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-08
Phase: Phase 3 Tool Fixes
@registry docs/recovery/recovery_registry.yaml#tools-analysis-unified-analyzer
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UnifiedAnalyzer:
    """
    Unified analyzer for comprehensive project analysis.

    Navigation:
    ├── Used by: analysis_handlers.py web endpoints
    ├── Integrates with: project_inventory_catalog.py, directory_audit_helper.py
    └── Related: Repository analysis, consolidation planning, overlap detection
    """

    def __init__(self, project_root: Path):
        """
        Initialize the unified analyzer.

        Navigation:
        ├── Sets up: project root, analysis parameters
        └── Related: Path validation, analysis configuration
        """
        self.project_root = Path(project_root)
        self.analysis_timestamp = datetime.now()

        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {self.project_root}")

        logger.info(f"🧠 UnifiedAnalyzer initialized for project: {self.project_root}")

    def run_full_analysis(self, repos: Optional[List[Path]] = None,
                         analysis_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Run comprehensive full analysis.

        Navigation:
        ├── Orchestrates: All analysis types in sequence
        ├── Returns: Consolidated analysis results
        └── Related: Complete project assessment workflow
        """
        results = {
            "timestamp": self.analysis_timestamp.isoformat(),
            "project_root": str(self.project_root),
            "analyses": {}
        }

        try:
            # Project structure analysis
            results["analyses"]["structure"] = self.analyze_project_structure()

            # Repository analysis if repos provided
            if repos:
                repo_metadata = [self.analyze_repository(repo) for repo in repos]
                results["analyses"]["repositories"] = repo_metadata

                # Consolidation analysis
                results["analyses"]["consolidation"] = self.detect_consolidation_opportunities(repo_metadata)

            # Overlap analysis if directory provided
            if analysis_dir:
                results["analyses"]["overlaps"] = self.analyze_overlaps(analysis_dir)

            results["status"] = "success"
            results["total_analyses"] = len(results["analyses"])

        except Exception as e:
            logger.error(f"Full analysis failed: {e}")
            results["status"] = "error"
            results["error"] = str(e)

        return results

    def analyze_project_structure(self) -> Dict[str, Any]:
        """
        Analyze overall project structure.

        Navigation:
        ├── Scans: Directory structure, file types, sizes
        ├── Returns: Structural metadata and statistics
        └── Related: Project inventory, directory analysis
        """
        structure = {
            "directories": {},
            "file_types": {},
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0
        }

        try:
            for root, dirs, files in os.walk(self.project_root):
                root_path = Path(root)
                rel_root = root_path.relative_to(self.project_root)

                # Count directories
                structure["total_dirs"] += len(dirs)

                # Analyze files
                for file in files:
                    file_path = root_path / file
                    structure["total_files"] += 1

                    # File size
                    try:
                        size = file_path.stat().st_size
                        structure["total_size"] += size
                    except OSError:
                        size = 0

                    # File type analysis
                    ext = file_path.suffix.lower()
                    if ext not in structure["file_types"]:
                        structure["file_types"][ext] = {"count": 0, "total_size": 0}
                    structure["file_types"][ext]["count"] += 1
                    structure["file_types"][ext]["total_size"] += size

                # Directory info
                if str(rel_root) != ".":
                    dir_info = {
                        "file_count": len(files),
                        "subdirs": len(dirs),
                        "path": str(rel_root)
                    }
                    structure["directories"][str(rel_root)] = dir_info

        except Exception as e:
            logger.error(f"Project structure analysis failed: {e}")
            structure["error"] = str(e)

        return structure

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze individual file content and metadata.

        Navigation:
        ├── Extracts: File metadata, content analysis, structure
        ├── Returns: Comprehensive file information
        └── Related: File content analysis, metadata extraction
        """
        analysis = {
            "path": str(file_path),
            "exists": file_path.exists(),
            "metadata": {},
            "content_analysis": {}
        }

        if not file_path.exists():
            analysis["error"] = "File does not exist"
            return analysis

        try:
            # File metadata
            stat = file_path.stat()
            analysis["metadata"] = {
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "extension": file_path.suffix,
                "name": file_path.name
            }

            # Content analysis for text files
            if self._is_text_file(file_path):
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    analysis["content_analysis"] = {
                        "line_count": len(content.splitlines()),
                        "char_count": len(content),
                        "word_count": len(content.split()),
                        "is_python": file_path.suffix == '.py',
                        "has_shebang": content.startswith('#!'),
                        "has_main": '__main__' in content if file_path.suffix == '.py' else False
                    }

                    # Python-specific analysis
                    if file_path.suffix == '.py':
                        analysis["content_analysis"]["imports"] = self._extract_python_imports(content)
                        analysis["content_analysis"]["classes"] = self._extract_python_classes(content)
                        analysis["content_analysis"]["functions"] = self._extract_python_functions(content)

                except UnicodeDecodeError:
                    analysis["content_analysis"]["binary_file"] = True

        except Exception as e:
            logger.error(f"File analysis failed for {file_path}: {e}")
            analysis["error"] = str(e)

        return analysis

    def analyze_repository(self, repo_path: Path) -> Dict[str, Any]:
        """
        Analyze repository metadata and structure.

        Navigation:
        ├── Extracts: Git info, file structure, metadata
        ├── Returns: Repository analysis results
        └── Related: Repository assessment, metadata collection
        """
        analysis = {
            "path": str(repo_path),
            "exists": repo_path.exists(),
            "metadata": {},
            "structure": {}
        }

        if not repo_path.exists():
            analysis["error"] = "Repository path does not exist"
            return analysis

        try:
            # Basic repository info
            analysis["metadata"] = {
                "name": repo_path.name,
                "full_path": str(repo_path.absolute()),
                "is_git_repo": (repo_path / ".git").exists()
            }

            # Git analysis if it's a git repo
            if analysis["metadata"]["is_git_repo"]:
                git_info = self._analyze_git_repository(repo_path)
                analysis["metadata"].update(git_info)

            # Structure analysis
            analysis["structure"] = self._analyze_repo_structure(repo_path)

        except Exception as e:
            logger.error(f"Repository analysis failed for {repo_path}: {e}")
            analysis["error"] = str(e)

        return analysis

    def detect_consolidation_opportunities(self, repo_metadata: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect consolidation opportunities across repositories.

        Navigation:
        ├── Analyzes: Duplicate files, shared dependencies, consolidation potential
        ├── Returns: Consolidation recommendations
        └── Related: Repository consolidation planning, deduplication
        """
        opportunities = {
            "total_repos": len(repo_metadata),
            "shared_files": {},
            "consolidation_candidates": [],
            "estimated_savings": {}
        }

        try:
            # Analyze shared files across repositories
            file_occurrences = {}
            for repo in repo_metadata:
                if "structure" in repo and "files" in repo["structure"]:
                    for file_info in repo["structure"]["files"]:
                        file_name = file_info.get("name", "")
                        if file_name not in file_occurrences:
                            file_occurrences[file_name] = []
                        file_occurrences[file_name].append(repo["metadata"]["name"])

            # Identify shared files
            for file_name, repos in file_occurrences.items():
                if len(repos) > 1:
                    opportunities["shared_files"][file_name] = repos

            # Generate consolidation recommendations
            if len(repo_metadata) > 1:
                opportunities["consolidation_candidates"] = self._generate_consolidation_recommendations(repo_metadata)

        except Exception as e:
            logger.error(f"Consolidation analysis failed: {e}")
            opportunities["error"] = str(e)

        return opportunities

    def analyze_overlaps(self, analysis_dir: Path) -> Dict[str, Any]:
        """
        Analyze overlaps and redundancies in analysis directory.

        Navigation:
        ├── Scans: Analysis outputs, identifies duplicates, patterns
        ├── Returns: Overlap analysis results
        └── Related: Analysis deduplication, pattern recognition
        """
        overlaps = {
            "directory": str(analysis_dir),
            "exists": analysis_dir.exists(),
            "analysis_files": [],
            "duplicate_findings": {},
            "overlap_summary": {}
        }

        if not analysis_dir.exists():
            overlaps["error"] = "Analysis directory does not exist"
            return overlaps

        try:
            # Find analysis files
            analysis_files = list(analysis_dir.glob("*.json")) + list(analysis_dir.glob("*.md"))
            overlaps["analysis_files"] = [str(f) for f in analysis_files]

            # Analyze for overlaps (simplified implementation)
            overlaps["overlap_summary"] = {
                "total_files": len(analysis_files),
                "file_types": self._count_file_types(analysis_files),
                "estimated_overlaps": "Analysis would require detailed content comparison"
            }

        except Exception as e:
            logger.error(f"Overlap analysis failed: {e}")
            overlaps["error"] = str(e)

        return overlaps

    # Helper methods

    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file is likely a text file."""
        text_extensions = {'.txt', '.py', '.js', '.json', '.md', '.html', '.css', '.xml', '.yaml', '.yml'}
        return file_path.suffix.lower() in text_extensions

    def _extract_python_imports(self, content: str) -> List[str]:
        """Extract Python import statements."""
        imports = []
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        return imports

    def _extract_python_classes(self, content: str) -> List[str]:
        """Extract Python class definitions."""
        classes = []
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith('class '):
                class_name = line.split('(')[0].replace('class ', '').strip()
                classes.append(class_name)
        return classes

    def _extract_python_functions(self, content: str) -> List[str]:
        """Extract Python function definitions."""
        functions = []
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith('def '):
                func_name = line.split('(')[0].replace('def ', '').strip()
                functions.append(func_name)
        return functions

    def _analyze_git_repository(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze git repository information."""
        git_info = {"git_analysis": "basic"}

        try:
            # This would normally use git commands, but for now return basic info
            git_info.update({
                "has_git": True,
                "branches": ["main"],  # Placeholder
                "last_commit": "unknown",  # Placeholder
                "contributors": ["unknown"]  # Placeholder
            })
        except Exception:
            git_info["git_error"] = "Git analysis failed"

        return git_info

    def _analyze_repo_structure(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze repository file structure."""
        structure = {"files": [], "directories": []}

        try:
            for root, dirs, files in os.walk(repo_path):
                level = len(Path(root).relative_to(repo_path).parts)

                # Limit depth for performance
                if level > 3:
                    continue

                for file in files[:50]:  # Limit files per directory
                    file_path = Path(root) / file
                    try:
                        stat = file_path.stat()
                        structure["files"].append({
                            "name": file,
                            "path": str(file_path.relative_to(repo_path)),
                            "size": stat.st_size,
                            "extension": file_path.suffix
                        })
                    except OSError:
                        continue

                for dir_name in dirs[:20]:  # Limit subdirs
                    structure["directories"].append({
                        "name": dir_name,
                        "path": str(Path(root).relative_to(repo_path) / dir_name)
                    })

        except Exception as e:
            structure["error"] = str(e)

        return structure

    def _generate_consolidation_recommendations(self, repo_metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate consolidation recommendations."""
        recommendations = []

        try:
            # Simple consolidation logic based on file counts and types
            for i, repo1 in enumerate(repo_metadata):
                for j, repo2 in enumerate(repo_metadata):
                    if i >= j:
                        continue

                    # Check for consolidation opportunities
                    if self._repos_have_similar_structure(repo1, repo2):
                        recommendations.append({
                            "type": "structure_consolidation",
                            "repositories": [repo1["metadata"]["name"], repo2["metadata"]["name"]],
                            "reason": "Similar directory structures detected",
                            "confidence": 0.7
                        })

        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")

        return recommendations

    def _repos_have_similar_structure(self, repo1: Dict[str, Any], repo2: Dict[str, Any]) -> bool:
        """Check if two repositories have similar structures."""
        # Simple similarity check based on file type distribution
        try:
            types1 = repo1.get("structure", {}).get("file_types", {})
            types2 = repo2.get("structure", {}).get("file_types", {})

            # Check if they have similar dominant file types
            common_types = set(types1.keys()) & set(types2.keys())
            return len(common_types) > 0 and len(common_types) / max(len(types1), len(types2)) > 0.5

        except Exception:
            return False

    def _count_file_types(self, files: List[Path]) -> Dict[str, int]:
        """Count file types in a list of files."""
        types = {}
        for file_path in files:
            ext = file_path.suffix.lower()
            types[ext] = types.get(ext, 0) + 1
        return types


# Global instance for tool access
unified_analyzer = UnifiedAnalyzer(Path(__file__).parent.parent)

if __name__ == "__main__":
    # Example usage
    analyzer = UnifiedAnalyzer(Path.cwd())
    results = analyzer.run_full_analysis()
    print(json.dumps(results, indent=2))