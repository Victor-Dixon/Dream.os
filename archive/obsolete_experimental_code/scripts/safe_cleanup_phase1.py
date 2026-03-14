#!/usr/bin/env python3
"""
Safe Repository Cleanup - Phase 1
=================================

Zero-risk cleanup of temporary files, cache files, and outdated artifacts.
This script safely removes files that can be regenerated or are no longer needed.

Author: AI Assistant - Repository Cleanup Specialist
Date: 2026-01-08
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class SafeCleanup:
    """Safe repository cleanup utility."""

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root).resolve()
        self.removed_files = []
        self.removed_dirs = []
        self.total_space_saved = 0

    def get_file_size(self, path: Path) -> int:
        """Get file size safely."""
        try:
            return path.stat().st_size
        except:
            return 0

    def safe_remove_file(self, file_path: Path, reason: str = "") -> bool:
        """Safely remove a single file."""
        try:
            if file_path.exists() and file_path.is_file():
                size = self.get_file_size(file_path)
                file_path.unlink()
                self.removed_files.append(str(file_path))
                self.total_space_saved += size
                logger.info(f"🗑️  Removed: {file_path} ({size} bytes) {reason}")
                return True
        except Exception as e:
            logger.warning(f"⚠️  Failed to remove {file_path}: {e}")
        return False

    def safe_remove_dir(self, dir_path: Path, reason: str = "") -> bool:
        """Safely remove a directory tree."""
        try:
            if dir_path.exists() and dir_path.is_dir():
                # Calculate total size before removal
                total_size = sum(self.get_file_size(f) for f in dir_path.rglob("*") if f.is_file())
                shutil.rmtree(dir_path)
                self.removed_dirs.append(str(dir_path))
                self.total_space_saved += total_size
                logger.info(f"🗑️  Removed directory: {dir_path} ({total_size} bytes) {reason}")
                return True
        except Exception as e:
            logger.warning(f"⚠️  Failed to remove directory {dir_path}: {e}")
        return False

    def cleanup_python_cache(self) -> Tuple[int, int]:
        """Clean up Python cache files and directories."""
        logger.info("🧹 Cleaning Python cache files...")

        cache_dirs_removed = 0
        cache_files_removed = 0

        # Remove __pycache__ directories
        for cache_dir in self.repo_root.rglob("__pycache__"):
            if self.safe_remove_dir(cache_dir, "- Python cache directory"):
                cache_dirs_removed += 1

        # Remove .pyc files
        for pyc_file in self.repo_root.rglob("*.pyc"):
            if self.safe_remove_file(pyc_file, "- Python compiled file"):
                cache_files_removed += 1

        logger.info(f"✅ Python cache cleanup: {cache_dirs_removed} dirs, {cache_files_removed} files removed")
        return cache_dirs_removed, cache_files_removed

    def cleanup_temp_test_files(self) -> int:
        """Clean up temporary and test files."""
        logger.info("🧹 Cleaning temporary and test files...")

        temp_files = [
            "temp_health_check.py",
            "test_ai_engine.py",
            "test_thea_cookies.py",
            "test_thea_debug.py",
            "web_validation_test_suite.py",
            "site_health_fix_plan.py",
            "a2a_replies.py",
            "audit_agent_tools.py",
        ]

        removed_count = 0
        for filename in temp_files:
            file_path = self.repo_root / filename
            if self.safe_remove_file(file_path, "- temporary/test file"):
                removed_count += 1

        # Also clean up setup wizard v2 if v1 exists
        if (self.repo_root / "setup_wizard.py").exists():
            v2_path = self.repo_root / "setup_wizard_v2.py"
            if self.safe_remove_file(v2_path, "- superseded setup wizard"):
                removed_count += 1

        logger.info(f"✅ Temporary files cleanup: {removed_count} files removed")
        return removed_count

    def cleanup_outdated_docs(self) -> int:
        """Move outdated documentation to archive."""
        logger.info("🧹 Archiving outdated documentation...")

        # Create archive directory
        archive_dir = self.repo_root / "archive" / "old_docs"
        archive_dir.mkdir(parents=True, exist_ok=True)

        outdated_docs = [
            "thea_code_review.md",
            "DIRECTORY_AUDIT_COORDINATION_DASHBOARD.md",
            "DIRECTORY_AUDIT_PLAN.md",
            "PHASE2_VALIDATION_RESULTS.md",
            "PHASE3_WEB_DEVELOPMENT_PLAN.md",
            "phase3b_cleanup_plan.md",
            "PHASE4_WEB_ARCHITECTURE_ROADMAP.md",
            "ENTERPRISE_ACCELERATION_OUTCOMES_ASSESSMENT.md",
        ]

        archived_count = 0
        for filename in outdated_docs:
            src_path = self.repo_root / filename
            if src_path.exists():
                try:
                    shutil.move(str(src_path), str(archive_dir / filename))
                    logger.info(f"📦 Archived: {filename} → archive/old_docs/")
                    archived_count += 1
                except Exception as e:
                    logger.warning(f"⚠️  Failed to archive {filename}: {e}")

        logger.info(f"✅ Documentation archive: {archived_count} files moved")
        return archived_count

    def cleanup_test_artifacts(self) -> int:
        """Clean up test and validation artifacts."""
        logger.info("🧹 Cleaning test and validation artifacts...")

        test_artifacts = [
            "AGENT6_TOOL_AUDIT_RESULTS.json",
            "agent_tools_audit_results.json",
            "compliance_validation.json",
            "fastapi_validation.json",
            "integration_status.json",
            "dependency_cache.json",
        ]

        # Also clean up validation files with patterns
        validation_patterns = [
            "final_*_validation.json",
            "phase*_validation.json",
            "phase*_to_*validation.json",
            "revenue_engine_*validation.json",
            "ultimate_revenue_engine_*validation.json",
        ]

        removed_count = 0

        # Remove specific files
        for filename in test_artifacts:
            file_path = self.repo_root / filename
            if self.safe_remove_file(file_path, "- test/validation artifact"):
                removed_count += 1

        # Remove pattern-matched files
        for pattern in validation_patterns:
            if "*" in pattern:
                # Simple glob pattern matching
                import glob
                matches = glob.glob(str(self.repo_root / pattern))
                for match in matches:
                    file_path = Path(match)
                    if file_path.is_file():
                        if self.safe_remove_file(file_path, "- validation artifact"):
                            removed_count += 1

        logger.info(f"✅ Test artifacts cleanup: {removed_count} files removed")
        return removed_count

    def run_phase1_cleanup(self) -> dict:
        """Run complete Phase 1 cleanup."""
        logger.info("🚀 Starting Phase 1 Repository Cleanup...")
        logger.info("=" * 50)

        start_time = __import__('time').time()

        # Run all cleanup phases
        cache_dirs, cache_files = self.cleanup_python_cache()
        temp_files = self.cleanup_temp_test_files()
        archived_docs = self.cleanup_outdated_docs()
        test_artifacts = self.cleanup_test_artifacts()

        # Calculate totals
        total_files_removed = len(self.removed_files) + len(self.removed_dirs)
        total_dirs_removed = len(self.removed_dirs)

        end_time = __import__('time').time()
        duration = end_time - start_time

        # Format space saved
        def format_bytes(bytes_val):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if bytes_val < 1024.0:
                    return f"{bytes_val:.1f} {unit}"
                bytes_val /= 1024.0
            return f"{bytes_val:.1f} TB"

        space_saved_str = format_bytes(self.total_space_saved)

        results = {
            "success": True,
            "phase": "Phase 1 - Zero Risk Cleanup",
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "duration_seconds": duration,
            "cleanup_summary": {
                "python_cache_dirs_removed": cache_dirs,
                "python_cache_files_removed": cache_files,
                "temp_files_removed": temp_files,
                "docs_archived": archived_docs,
                "test_artifacts_removed": test_artifacts,
                "total_files_removed": total_files_removed,
                "total_dirs_removed": total_dirs_removed,
                "space_saved_bytes": self.total_space_saved,
                "space_saved_formatted": space_saved_str,
            },
            "removed_files": self.removed_files[:20],  # Limit for readability
            "removed_dirs": self.removed_dirs,
        }

        logger.info("=" * 50)
        logger.info("✅ Phase 1 Cleanup Complete!")
        logger.info(f"📊 Total files removed: {total_files_removed}")
        logger.info(f"📊 Total directories removed: {total_dirs_removed}")
        logger.info(f"💾 Space saved: {space_saved_str}")
        logger.info(".2f")
        logger.info("🔄 Repository is now cleaner and more maintainable!")

        return results

def main():
    """Main cleanup execution."""
    cleanup = SafeCleanup()
    results = cleanup.run_phase1_cleanup()

    # Save results
    import json
    results_file = Path("cleanup_phase1_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📋 Results saved to: {results_file}")

if __name__ == "__main__":
    main()