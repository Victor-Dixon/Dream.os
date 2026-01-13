"""
Analysis Handlers
=================

Handler classes for unified analysis tool operations.
Wires unified_analyzer.py to web layer with BaseHandler pattern.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from flask import jsonify, request

from src.core.base.base_handler import BaseHandler

# Import unified analyzer
import sys
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))
from tools.unified_analyzer import UnifiedAnalyzer


class AnalysisHandlers(BaseHandler):
    """Handler class for analysis operations."""

    def __init__(self):
        """Initialize analysis handlers."""
        super().__init__("AnalysisHandlers")
        self.project_root = project_root
        self.analyzer = UnifiedAnalyzer(project_root=project_root)

    def handle_analyze(self, request) -> tuple:
        """
        Handle analysis request by category.
        
        Expected JSON body:
        {
            "category": "repository|structure|file|consolidation|overlaps",
            "file": "path/to/file" (for file category),
            "repos": "path1,path2" (for repository/consolidation),
            "analysis_dir": "path/to/dir" (for overlaps),
            "project_root": "path/to/project" (optional)
        }
        """
        try:
            data = request.get_json() or {}
            category = data.get("category", "all")
            project_root_path = Path(data.get("project_root")) if data.get("project_root") else project_root
            
            analyzer = UnifiedAnalyzer(project_root=project_root_path)
            
            if category == "structure":
                result = analyzer.analyze_project_structure()
            elif category == "file":
                if not data.get("file"):
                    return self.format_error("File path required for file analysis", 400)
                result = analyzer.analyze_file(Path(data["file"]))
            elif category == "repository":
                if not data.get("repos"):
                    return self.format_error("Repository paths required", 400)
                repos_list = data["repos"].split(",") if isinstance(data["repos"], str) else data["repos"]
                repo_metadata = [analyzer.analyze_repository(Path(r)) for r in repos_list]
                result = {"repositories": repo_metadata}
            elif category == "consolidation":
                if not data.get("repos"):
                    return self.format_error("Repository paths required", 400)
                repos_list = data["repos"].split(",") if isinstance(data["repos"], str) else data["repos"]
                repo_metadata = [analyzer.analyze_repository(Path(r)) for r in repos_list]
                result = analyzer.detect_consolidation_opportunities(repo_metadata)
            elif category == "overlaps":
                if not data.get("analysis_dir"):
                    return self.format_error("Analysis directory required", 400)
                result = analyzer.analyze_overlaps(Path(data["analysis_dir"]))
            elif category == "all":
                repos_list = data.get("repos")
                if repos_list:
                    repos_list = repos_list.split(",") if isinstance(repos_list, str) else repos_list
                    repos_list = [Path(r) for r in repos_list]
                analysis_dir_path = Path(data["analysis_dir"]) if data.get("analysis_dir") else None
                result = analyzer.run_full_analysis(repos=repos_list, analysis_dir=analysis_dir_path)
            else:
                return self.format_error(f"Invalid category: {category}", 400)
            
            from flask import jsonify
            return jsonify(self.format_response({
                "category": category,
                "analysis": result
            })), 200
        except Exception as e:
            error_response = self.handle_error(e, "Analysis failed")
            from flask import jsonify
            return jsonify(error_response), 500

    def handle_get_categories(self, request) -> tuple:
        """List available analysis categories."""
        categories = [
            "repository",
            "structure",
            "file",
            "consolidation",
            "overlaps",
            "all"
        ]
        from flask import jsonify
        return jsonify(self.format_response({
            "categories": categories,
            "count": len(categories)
        })), 200

    def handle_repository_analysis(self, request) -> tuple:
        """
        Run repository analysis.
        
        Expected JSON body:
        {
            "repos": "path1,path2" or ["path1", "path2"]
        }
        """
        try:
            data = request.get_json() or {}
            if not data.get("repos"):
                return self.format_error("Repository paths required", 400)
            
            repos_list = data["repos"]
            if isinstance(repos_list, str):
                repos_list = repos_list.split(",")
            
            repo_metadata = [self.analyzer.analyze_repository(Path(r)) for r in repos_list]
            from flask import jsonify
            return jsonify(self.format_response({
                "repositories": repo_metadata,
                "count": len(repo_metadata)
            })), 200
        except Exception as e:
            error_response = self.handle_error(e, "Repository analysis failed")
            from flask import jsonify
            return jsonify(error_response), 500

