"""
Repository Merge Routes - Merge Improvements Web Integration
============================================================

Flask routes for repository merge status tracking and management.
Provides web API access to merge improvements system.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict, Optional

# Create blueprint
repository_merge_bp = Blueprint("repository_merge", __name__, url_prefix="/api/repository-merge")


def _get_merge_improvements():
    """Get RepositoryMergeImprovements instance (lazy import)."""
    try:
        from src.core.repository_merge_improvements import get_merge_improvements
        return get_merge_improvements()
    except ImportError:
        return None


@repository_merge_bp.route("/status", methods=["GET"])
def get_merge_status():
    """
    Get repository merge status overview.
    
    Returns:
        JSON with status summary, repo statuses, and attempt tracking
    """
    try:
        improvements = _get_merge_improvements()
        if not improvements:
            return jsonify({
                "error": "Merge improvements not available",
                "message": "Repository merge improvements module not found"
            }), 503
        
        # Get all repo statuses
        repo_statuses = {}
        for name, meta in improvements.repo_statuses.items():
            repo_statuses[name] = {
                "name": meta.name,
                "normalized_name": meta.normalized_name,
                "status": meta.status.value,
                "last_seen": meta.last_seen,
                "last_checked": meta.last_checked,
                "error_count": meta.error_count,
                "last_error": meta.last_error,
                "merged_into": meta.merged_into
            }
        
        # Get merge attempts summary
        attempts_summary = {}
        for pair, attempt in improvements.merge_attempts.items():
            attempts_summary[pair] = {
                "source_repo": attempt.source_repo,
                "target_repo": attempt.target_repo,
                "first_attempt": attempt.first_attempt,
                "last_attempt": attempt.last_attempt,
                "attempt_count": attempt.attempt_count,
                "success": attempt.success,
                "last_error": attempt.last_error,
                "error_type": attempt.error_type.value if attempt.error_type else None
            }
        
        # Calculate summary statistics
        total_repos = len(repo_statuses)
        status_counts = {}
        for meta in improvements.repo_statuses.values():
            status = meta.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total_attempts = len(attempts_summary)
        successful_attempts = sum(1 for a in attempts_summary.values() if a["success"])
        failed_attempts = total_attempts - successful_attempts
        
        permanent_errors = sum(
            1 for a in attempts_summary.values() 
            if a.get("error_type") == "permanent"
        )
        transient_errors = sum(
            1 for a in attempts_summary.values() 
            if a.get("error_type") == "transient"
        )
        
        return jsonify({
            "summary": {
                "total_repositories": total_repos,
                "status_breakdown": status_counts,
                "total_merge_attempts": total_attempts,
                "successful_attempts": successful_attempts,
                "failed_attempts": failed_attempts,
                "permanent_errors": permanent_errors,
                "transient_errors": transient_errors
            },
            "repository_statuses": repo_statuses,
            "merge_attempts": attempts_summary
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to get merge status",
            "message": str(e)
        }), 500


@repository_merge_bp.route("/repo/<repo_name>/status", methods=["GET"])
def get_repo_status(repo_name: str):
    """
    Get status for a specific repository.
    
    Args:
        repo_name: Repository name (normalized automatically)
    """
    try:
        improvements = _get_merge_improvements()
        if not improvements:
            return jsonify({
                "error": "Merge improvements not available"
            }), 503
        
        meta = improvements.get_repo_status(repo_name)
        if not meta:
            return jsonify({
                "error": "Repository not found",
                "repo_name": repo_name,
                "normalized_name": improvements.normalize_repo_name(repo_name)
            }), 404
        
        return jsonify({
            "repo_name": meta.name,
            "normalized_name": meta.normalized_name,
            "status": meta.status.value,
            "last_seen": meta.last_seen,
            "last_checked": meta.last_checked,
            "error_count": meta.error_count,
            "last_error": meta.last_error,
            "merged_into": meta.merged_into
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to get repository status",
            "message": str(e)
        }), 500


@repository_merge_bp.route("/validate", methods=["POST"])
def validate_merge():
    """
    Validate a merge before attempting (pre-flight checks).
    
    Request body:
        {
            "source_repo": "source/repo",
            "target_repo": "target/repo"
        }
    """
    try:
        improvements = _get_merge_improvements()
        if not improvements:
            return jsonify({
                "error": "Merge improvements not available"
            }), 503
        
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body required"
            }), 400
        
        source_repo = data.get("source_repo")
        target_repo = data.get("target_repo")
        
        if not source_repo or not target_repo:
            return jsonify({
                "error": "Invalid request",
                "message": "source_repo and target_repo required"
            }), 400
        
        # Run complete pre-merge validation
        should_proceed, error, validation_details = improvements.pre_merge_validation(
            source_repo=source_repo,
            target_repo=target_repo,
            github_client=None  # Could pass GitHub client if available
        )
        
        return jsonify({
            "should_proceed": should_proceed,
            "error": error,
            "validation_details": validation_details
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to validate merge",
            "message": str(e)
        }), 500


@repository_merge_bp.route("/classify-error", methods=["POST"])
def classify_error():
    """
    Classify an error message (permanent vs transient).
    
    Request body:
        {
            "error_message": "Source repo not available"
        }
    """
    try:
        improvements = _get_merge_improvements()
        if not improvements:
            return jsonify({
                "error": "Merge improvements not available"
            }), 503
        
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body required"
            }), 400
        
        error_message = data.get("error_message", "")
        if not error_message:
            return jsonify({
                "error": "Invalid request",
                "message": "error_message required"
            }), 400
        
        error_type = improvements.classify_error(error_message)
        
        return jsonify({
            "error_message": error_message,
            "error_type": error_type.value,
            "is_permanent": error_type == improvements.ErrorType.PERMANENT,
            "should_retry": error_type == improvements.ErrorType.TRANSIENT,
            "description": {
                "permanent": "Don't retry - repository not available, deleted, or access denied",
                "transient": "Retry with backoff - network issues, rate limits, temporary errors",
                "unknown": "Log and investigate - error pattern not recognized"
            }.get(error_type.value, "Unknown error type")
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to classify error",
            "message": str(e)
        }), 500


@repository_merge_bp.route("/normalize-name", methods=["POST"])
def normalize_repo_name():
    """
    Normalize a repository name.
    
    Request body:
        {
            "repo_name": "Dadudekc/focusforge"
        }
    """
    try:
        improvements = _get_merge_improvements()
        if not improvements:
            return jsonify({
                "error": "Merge improvements not available"
            }), 503
        
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body required"
            }), 400
        
        repo_name = data.get("repo_name", "")
        if not repo_name:
            return jsonify({
                "error": "Invalid request",
                "message": "repo_name required"
            }), 400
        
        normalized = improvements.normalize_repo_name(repo_name)
        
        return jsonify({
            "original": repo_name,
            "normalized": normalized,
            "changed": repo_name != normalized
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to normalize repository name",
            "message": str(e)
        }), 500


@repository_merge_bp.route("/attempts", methods=["GET"])
def get_merge_attempts():
    """
    Get merge attempt history.
    
    Query params:
        - source_repo: Filter by source repository
        - target_repo: Filter by target repository
        - error_type: Filter by error type (permanent/transient/unknown)
        - success: Filter by success (true/false)
    """
    try:
        improvements = _get_merge_improvements()
        if not improvements:
            return jsonify({
                "error": "Merge improvements not available"
            }), 503
        
        # Get filters from query params
        source_filter = request.args.get("source_repo")
        target_filter = request.args.get("target_repo")
        error_type_filter = request.args.get("error_type")
        success_filter = request.args.get("success")
        
        # Filter attempts
        filtered_attempts = []
        for pair, attempt in improvements.merge_attempts.items():
            # Apply filters
            if source_filter and attempt.source_repo != source_filter:
                continue
            if target_filter and attempt.target_repo != target_filter:
                continue
            if error_type_filter and (not attempt.error_type or attempt.error_type.value != error_type_filter):
                continue
            if success_filter:
                success_bool = success_filter.lower() == "true"
                if attempt.success != success_bool:
                    continue
            
            filtered_attempts.append({
                "pair": pair,
                "source_repo": attempt.source_repo,
                "target_repo": attempt.target_repo,
                "first_attempt": attempt.first_attempt,
                "last_attempt": attempt.last_attempt,
                "attempt_count": attempt.attempt_count,
                "success": attempt.success,
                "last_error": attempt.last_error,
                "error_type": attempt.error_type.value if attempt.error_type else None
            })
        
        return jsonify({
            "attempts": filtered_attempts,
            "total": len(filtered_attempts),
            "filters": {
                "source_repo": source_filter,
                "target_repo": target_filter,
                "error_type": error_type_filter,
                "success": success_filter
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to get merge attempts",
            "message": str(e)
        }), 500

