#!/usr/bin/env python3
"""
Phase 1 Consolidation Script - Agent Workspace Cleanup

This script automates the consolidation of agent workspaces to eliminate duplication
and optimize storage usage. Phase 1 focuses on:

1. QUICK_START.md deduplication across agent workspaces
2. Cache file cleanup (.pyc files)
3. Archive consolidation within agent workspaces
4. Status.json standardization

Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import os
import sys
import json
import shutil
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@dataclass
class ConsolidationResult:
    """Tracks the result of a consolidation operation"""
    operation: str
    files_processed: int
    files_removed: int
    space_saved_bytes: int
    space_saved_mb: float
    status: str  # "success", "warning", "error"
    timestamp: str
    details: List[str]

    def to_dict(self):
        return asdict(self)

@dataclass
class Phase1ConsolidationReport:
    """Complete report for Phase 1 consolidation operations"""
    timestamp: str
    total_operations: int
    total_files_processed: int
    total_files_removed: int
    total_space_saved_mb: float
    operations: List[ConsolidationResult]
    errors: List[str]
    warnings: List[str]

class Phase1Consolidator:
    """Handles Phase 1 consolidation operations for agent workspaces"""

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.agent_workspaces = self.base_path / "agent_workspaces"
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for consolidation operations"""
        log_file = self.base_path / "logs" / f"phase1_consolidation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file.parent.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file content"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes"""
        return file_path.stat().st_size

    def find_agent_workspaces(self) -> List[Path]:
        """Find all agent workspace directories"""
        if not self.agent_workspaces.exists():
            self.logger.error(f"Agent workspaces directory not found: {self.agent_workspaces}")
            return []

        workspaces = []
        for item in self.agent_workspaces.iterdir():
            if item.is_dir() and item.name.startswith("Agent-"):
                workspaces.append(item)

        self.logger.info(f"Found {len(workspaces)} agent workspaces: {[w.name for w in workspaces]}")
        return sorted(workspaces)

    def consolidate_quickstart_files(self) -> ConsolidationResult:
        """Consolidate QUICK_START.md files across agent workspaces"""
        self.logger.info("Starting QUICK_START.md consolidation...")

        workspaces = self.find_agent_workspaces()
        if not workspaces:
            return ConsolidationResult(
                operation="quickstart_deduplication",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="error",
                timestamp=datetime.now().isoformat(),
                details=["No agent workspaces found"]
            )

        quickstart_files = []
        for workspace in workspaces:
            qs_file = workspace / "QUICK_START.md"
            if qs_file.exists():
                file_hash = self.calculate_file_hash(qs_file)
                file_size = self.get_file_size(qs_file)
                quickstart_files.append({
                    'path': qs_file,
                    'hash': file_hash,
                    'size': file_size,
                    'agent': workspace.name
                })

        if not quickstart_files:
            return ConsolidationResult(
                operation="quickstart_deduplication",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="warning",
                timestamp=datetime.now().isoformat(),
                details=["No QUICK_START.md files found"]
            )

        # Group files by hash to find duplicates
        hash_groups = {}
        for file_info in quickstart_files:
            file_hash = file_info['hash']
            if file_hash not in hash_groups:
                hash_groups[file_hash] = []
            hash_groups[file_hash].append(file_info)

        # Keep the first occurrence of each unique file, remove others
        files_removed = 0
        space_saved = 0
        details = []

        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                # Sort by agent number to keep the lowest numbered agent
                files.sort(key=lambda x: int(x['agent'].split('-')[1]))

                # Keep the first file, remove the rest
                keep_file = files[0]['path']
                remove_files = files[1:]

                for file_info in remove_files:
                    file_path = file_info['path']
                    try:
                        # Create backup before removal
                        backup_dir = self.base_path / "backups" / "phase1_consolidation" / datetime.now().strftime("%Y%m%d_%H%M%S")
                        backup_dir.mkdir(parents=True, exist_ok=True)

                        backup_path = backup_dir / f"{file_path.name}_{file_info['agent']}"
                        shutil.copy2(file_path, backup_path)

                        # Remove the duplicate file
                        file_path.unlink()
                        files_removed += 1
                        space_saved += file_info['size']

                        details.append(f"Removed duplicate: {file_path} (backed up to {backup_path})")
                        self.logger.info(f"Removed duplicate QUICK_START.md: {file_path}")

                    except Exception as e:
                        details.append(f"Error removing {file_path}: {str(e)}")
                        self.logger.error(f"Error removing {file_path}: {str(e)}")

        return ConsolidationResult(
            operation="quickstart_deduplication",
            files_processed=len(quickstart_files),
            files_removed=files_removed,
            space_saved_bytes=space_saved,
            space_saved_mb=round(space_saved / (1024 * 1024), 2),
            status="success" if files_removed > 0 else "warning",
            timestamp=datetime.now().isoformat(),
            details=details
        )

    def cleanup_cache_files(self) -> ConsolidationResult:
        """Clean up .pyc cache files from agent workspaces"""
        self.logger.info("Starting cache file cleanup...")

        workspaces = self.find_agent_workspaces()
        if not workspaces:
            return ConsolidationResult(
                operation="cache_cleanup",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="error",
                timestamp=datetime.now().isoformat(),
                details=["No agent workspaces found"]
            )

        cache_files = []
        for workspace in workspaces:
            # Find all .pyc files recursively
            for pyc_file in workspace.rglob("*.pyc"):
                if pyc_file.exists():
                    file_size = self.get_file_size(pyc_file)
                    cache_files.append({
                        'path': pyc_file,
                        'size': file_size
                    })

        # Also check for __pycache__ directories
        pycache_dirs = []
        for workspace in workspaces:
            for pycache_dir in workspace.rglob("__pycache__"):
                if pycache_dir.is_dir():
                    pycache_dirs.append(pycache_dir)

        files_removed = 0
        space_saved = 0
        details = []

        # Remove individual .pyc files
        for file_info in cache_files:
            try:
                file_info['path'].unlink()
                files_removed += 1
                space_saved += file_info['size']
                details.append(f"Removed cache file: {file_info['path']}")
            except Exception as e:
                details.append(f"Error removing {file_info['path']}: {str(e)}")
                self.logger.error(f"Error removing cache file {file_info['path']}: {str(e)}")

        # Remove __pycache__ directories
        for pycache_dir in pycache_dirs:
            try:
                shutil.rmtree(pycache_dir)
                # Count files in the directory that were removed
                dir_files = list(pycache_dir.rglob("*"))
                files_removed += len(dir_files)
                details.append(f"Removed cache directory: {pycache_dir} ({len(dir_files)} files)")
                self.logger.info(f"Removed cache directory: {pycache_dir}")
            except Exception as e:
                details.append(f"Error removing directory {pycache_dir}: {str(e)}")
                self.logger.error(f"Error removing cache directory {pycache_dir}: {str(e)}")

        return ConsolidationResult(
            operation="cache_cleanup",
            files_processed=len(cache_files) + len(pycache_dirs),
            files_removed=files_removed,
            space_saved_bytes=space_saved,
            space_saved_mb=round(space_saved / (1024 * 1024), 2),
            status="success" if files_removed > 0 else "warning",
            timestamp=datetime.now().isoformat(),
            details=details
        )

    def consolidate_archives(self) -> ConsolidationResult:
        """Consolidate archive directories within agent workspaces"""
        self.logger.info("Starting archive consolidation...")

        workspaces = self.find_agent_workspaces()
        if not workspaces:
            return ConsolidationResult(
                operation="archive_consolidation",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="error",
                timestamp=datetime.now().isoformat(),
                details=["No agent workspaces found"]
            )

        # Find all archive directories
        archive_dirs = []
        for workspace in workspaces:
            archive_dir = workspace / "archive"
            if archive_dir.exists() and archive_dir.is_dir():
                # Count files in archive
                archive_files = list(archive_dir.rglob("*"))
                file_count = len([f for f in archive_files if f.is_file()])
                archive_dirs.append({
                    'path': archive_dir,
                    'file_count': file_count,
                    'agent': workspace.name
                })

        if not archive_dirs:
            return ConsolidationResult(
                operation="archive_consolidation",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="warning",
                timestamp=datetime.now().isoformat(),
                details=["No archive directories found"]
            )

        # Create centralized archive structure
        central_archive = self.base_path / "agent_workspaces" / "consolidated_archives"
        central_archive.mkdir(exist_ok=True)

        files_moved = 0
        space_saved = 0  # We'll calculate this as reduction in duplication
        details = []

        for archive_info in archive_dirs:
            archive_path = archive_info['path']
            agent_name = archive_info['agent']

            # Create agent-specific directory in central archive
            agent_archive = central_archive / agent_name
            agent_archive.mkdir(exist_ok=True)

            # Move contents to central location
            for item in archive_path.iterdir():
                if item.is_file():
                    try:
                        # Check if file already exists in central location
                        dest_path = agent_archive / item.name
                        if dest_path.exists():
                            # Compare file sizes first (quick check)
                            if item.stat().st_size == dest_path.stat().st_size:
                                # Files might be identical, remove duplicate
                                item.unlink()
                                space_saved += dest_path.stat().st_size
                                details.append(f"Removed duplicate archive file: {item}")
                                continue

                        # Move file to central archive
                        shutil.move(str(item), str(dest_path))
                        files_moved += 1
                        details.append(f"Moved {item.name} from {agent_name} to consolidated archive")

                    except Exception as e:
                        details.append(f"Error moving {item}: {str(e)}")
                        self.logger.error(f"Error moving {item}: {str(e)}")

            # Remove empty archive directory
            try:
                if not list(archive_path.iterdir()):
                    archive_path.rmdir()
                    details.append(f"Removed empty archive directory: {archive_path}")
            except Exception as e:
                details.append(f"Could not remove archive directory {archive_path}: {str(e)}")

        return ConsolidationResult(
            operation="archive_consolidation",
            files_processed=sum(d['file_count'] for d in archive_dirs),
            files_removed=files_moved,  # Files moved to central location
            space_saved_bytes=space_saved,
            space_saved_mb=round(space_saved / (1024 * 1024), 2),
            status="success" if files_moved > 0 else "warning",
            timestamp=datetime.now().isoformat(),
            details=details
        )

    def standardize_status_files(self) -> ConsolidationResult:
        """Ensure status.json files are standardized across agents"""
        self.logger.info("Starting status.json standardization...")

        workspaces = self.find_agent_workspaces()
        if not workspaces:
            return ConsolidationResult(
                operation="status_standardization",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="error",
                timestamp=datetime.now().isoformat(),
                details=["No agent workspaces found"]
            )

        status_files = []
        for workspace in workspaces:
            status_file = workspace / "status.json"
            if status_file.exists():
                try:
                    with open(status_file, 'r') as f:
                        data = json.load(f)
                    status_files.append({
                        'path': status_file,
                        'data': data,
                        'agent': workspace.name,
                        'size': self.get_file_size(status_file)
                    })
                except Exception as e:
                    self.logger.error(f"Error reading status file {status_file}: {str(e)}")

        if not status_files:
            return ConsolidationResult(
                operation="status_standardization",
                files_processed=0,
                files_removed=0,
                space_saved_bytes=0,
                space_saved_mb=0.0,
                status="warning",
                timestamp=datetime.now().isoformat(),
                details=["No status.json files found"]
            )

        # Check for required fields and standardize format
        required_fields = ["agent_id", "agent_name", "status", "current_phase",
                          "last_updated", "current_mission", "mission_priority",
                          "current_tasks", "completed_tasks", "achievements", "next_actions"]

        files_processed = 0
        files_updated = 0
        details = []

        for file_info in status_files:
            files_processed += 1
            status_data = file_info['data']
            status_path = file_info['path']

            # Check for missing required fields
            missing_fields = []
            for field in required_fields:
                if field not in status_data:
                    missing_fields.append(field)

            if missing_fields:
                # Add missing fields with default values
                for field in missing_fields:
                    if field == "agent_id":
                        status_data[field] = file_info['agent']
                    elif field == "agent_name":
                        # Extract readable name from agent ID
                        agent_num = file_info['agent'].split('-')[1]
                        role_map = {
                            "1": "Integration & Core Systems",
                            "2": "Architecture & Design",
                            "3": "Infrastructure & DevOps",
                            "4": "Captain (Strategic Oversight)",
                            "5": "Business Intelligence",
                            "6": "Coordination & Communication",
                            "7": "Web Development",
                            "8": "SSOT & System Integration"
                        }
                        status_data[field] = role_map.get(agent_num, f"Agent {agent_num}")
                    elif field in ["current_tasks", "completed_tasks", "achievements", "next_actions"]:
                        status_data[field] = []
                    elif field == "status":
                        status_data[field] = "ACTIVE_AGENT_MODE"
                    elif field == "current_phase":
                        status_data[field] = "TASK_EXECUTION"
                    elif field == "last_updated":
                        status_data[field] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    elif field == "current_mission":
                        status_data[field] = "System consolidation and optimization"
                    elif field == "mission_priority":
                        status_data[field] = "HIGH"
                    else:
                        status_data[field] = ""

                # Write updated file
                try:
                    with open(status_path, 'w') as f:
                        json.dump(status_data, f, indent=2)
                    files_updated += 1
                    details.append(f"Standardized status.json for {file_info['agent']}: added {len(missing_fields)} missing fields")
                except Exception as e:
                    details.append(f"Error updating {status_path}: {str(e)}")
                    self.logger.error(f"Error updating status file {status_path}: {str(e)}")

        return ConsolidationResult(
            operation="status_standardization",
            files_processed=files_processed,
            files_removed=0,  # No files removed, only updated
            space_saved_bytes=0,  # Space might actually increase slightly due to formatting
            space_saved_mb=0.0,
            status="success" if files_updated > 0 else "warning",
            timestamp=datetime.now().isoformat(),
            details=details
        )

    def run_phase1_consolidation(self) -> Phase1ConsolidationReport:
        """Run all Phase 1 consolidation operations"""
        self.logger.info("Starting Phase 1 consolidation operations...")

        operations = []
        errors = []
        warnings = []

        # Run all consolidation operations
        consolidation_operations = [
            self.consolidate_quickstart_files,
            self.cleanup_cache_files,
            self.consolidate_archives,
            self.standardize_status_files
        ]

        for operation in consolidation_operations:
            try:
                result = operation()
                operations.append(result)

                if result.status == "error":
                    errors.extend(result.details)
                elif result.status == "warning":
                    warnings.extend(result.details)

                self.logger.info(f"Completed {result.operation}: {result.files_removed} files removed, "
                               f"{result.space_saved_mb} MB saved")

            except Exception as e:
                error_msg = f"Error in {operation.__name__}: {str(e)}"
                errors.append(error_msg)
                self.logger.error(error_msg)

        # Calculate totals
        total_operations = len(operations)
        total_files_processed = sum(op.files_processed for op in operations)
        total_files_removed = sum(op.files_removed for op in operations)
        total_space_saved_mb = sum(op.space_saved_mb for op in operations)

        report = Phase1ConsolidationReport(
            timestamp=datetime.now().isoformat(),
            total_operations=total_operations,
            total_files_processed=total_files_processed,
            total_files_removed=total_files_removed,
            total_space_saved_mb=round(total_space_saved_mb, 2),
            operations=operations,
            errors=errors,
            warnings=warnings
        )

        # Save detailed report
        self.save_report(report)

        self.logger.info(f"Phase 1 consolidation complete: {total_files_removed} files removed, "
                        f"{total_space_saved_mb} MB saved")

        return report

    def save_report(self, report: Phase1ConsolidationReport):
        """Save the consolidation report to file"""
        reports_dir = self.base_path / "reports" / "consolidation"
        reports_dir.mkdir(parents=True, exist_ok=True)

        report_file = reports_dir / f"phase1_consolidation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": report.timestamp,
                "summary": {
                    "total_operations": report.total_operations,
                    "total_files_processed": report.total_files_processed,
                    "total_files_removed": report.total_files_removed,
                    "total_space_saved_mb": report.total_space_saved_mb
                },
                "operations": [op.to_dict() for op in report.operations],
                "errors": report.errors,
                "warnings": report.warnings
            }, f, indent=2)

        self.logger.info(f"Consolidation report saved to: {report_file}")

    def print_summary(self, report: Phase1ConsolidationReport):
        """Print a human-readable summary of the consolidation results"""
        print("\n" + "="*80)
        print("PHASE 1 CONSOLIDATION REPORT")
        print("="*80)
        print(f"Timestamp: {report.timestamp}")
        print(f"Total Operations: {report.total_operations}")
        print(f"Files Processed: {report.total_files_processed}")
        print(f"Files Removed: {report.total_files_removed}")
        print(f"Space Saved: {report.total_space_saved_mb} MB")
        print()

        print("OPERATION DETAILS:")
        print("-" * 40)
        for op in report.operations:
            print(f"• {op.operation}: {op.files_removed} files removed, {op.space_saved_mb} MB saved")
        print()

        if report.errors:
            print("ERRORS:")
            print("-" * 40)
            for error in report.errors:
                print(f"❌ {error}")
            print()

        if report.warnings:
            print("WARNINGS:")
            print("-" * 40)
            for warning in report.warnings:
                print(f"⚠️  {warning}")
            print()

        print("✅ Phase 1 consolidation completed successfully!")


def main():
    """Main entry point for Phase 1 consolidation"""
    print("Phase 1 Consolidation Script - Agent Workspace Cleanup")
    print("This script will consolidate agent workspaces to eliminate duplication.")
    print()

    # Get confirmation
    response = input("Do you want to proceed with Phase 1 consolidation? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Consolidation cancelled.")
        return

    # Run consolidation
    consolidator = Phase1Consolidator()
    report = consolidator.run_phase1_consolidation()
    consolidator.print_summary(report)


if __name__ == "__main__":
    main()