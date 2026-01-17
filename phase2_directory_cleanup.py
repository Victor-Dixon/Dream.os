#!/usr/bin/env python3
"""
Phase 2 Directory Audit Cleanup Script
Agent-6 Coordination & Communication Specialist
Directory Audit Phase 2 - Controlled Cleanup & Archiving

This script executes the controlled cleanup operations for Agent-6 assigned directories
based on the DIRECTORY_AUDIT_PHASE2_EXECUTION_PLAN.md
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path

class DirectoryCleanup:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.archive_base = self.base_dir / "archives"
        self.today = datetime.now().strftime("%Y%m%d")
        self.thirty_days_ago = datetime.now() - timedelta(days=30)

        # Create archive directories
        self.agent_workspace_archive = self.archive_base / "agent_workspaces_archive" / self.today
        self.project_scans_archive = self.archive_base / "project_scans_archive" / self.today
        self.debates_archive = self.archive_base / "debates_archive" / self.today

        for archive_dir in [self.agent_workspace_archive, self.project_scans_archive, self.debates_archive]:
            archive_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 Archive directories created for {self.today}")

    def log_operation(self, operation, details):
        """Log cleanup operations"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {operation}: {details}"
        print(log_entry)

        # Append to execution log
        log_file = self.base_dir / "DIRECTORY_AUDIT_PHASE2_EXECUTION_LOG.md"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{log_entry}\n")

    def safe_delete_directory(self, dir_path):
        """Safely delete a directory with logging"""
        if not dir_path.exists():
            self.log_operation("SKIP", f"Directory {dir_path} does not exist")
            return True

        try:
            # Check if directory is empty first
            if not any(dir_path.iterdir()):
                dir_path.rmdir()
                self.log_operation("DELETE", f"Removed empty directory {dir_path}")
                return True
            else:
                self.log_operation("SKIP", f"Directory {dir_path} is not empty, manual review required")
                return False
        except Exception as e:
            self.log_operation("ERROR", f"Failed to delete {dir_path}: {e}")
            return False

    def archive_old_files(self, source_dir, archive_dir, pattern="*", days_old=30):
        """Archive files older than specified days"""
        if not source_dir.exists():
            self.log_operation("SKIP", f"Source directory {source_dir} does not exist")
            return 0

        archived_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)

        for file_path in source_dir.glob(pattern):
            if file_path.is_file():
                # Check file modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff_date:
                    # Archive the file
                    relative_path = file_path.relative_to(source_dir)
                    archive_path = archive_dir / relative_path

                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(archive_path))

                    self.log_operation("ARCHIVE", f"Moved {file_path} to {archive_path}")
                    archived_count += 1

        return archived_count

    def analyze_agent_workspaces(self):
        """Analyze agent workspaces for cleanup candidates"""
        workspace_dir = self.base_dir / "agent_workspaces"
        if not workspace_dir.exists():
            self.log_operation("SKIP", "agent_workspaces directory does not exist")
            return [], []

        self.log_operation("ANALYZE", "Starting agent workspace analysis")

        # Get all agent directories
        agent_dirs = [d for d in workspace_dir.iterdir() if d.is_dir() and d.name.startswith("Agent-")]

        old_workspaces = []
        active_workspaces = []

        for agent_dir in agent_dirs:
            # Check for status.json
            status_file = agent_dir / "status.json"
            if status_file.exists():
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status_data = json.load(f)

                    # Check last activity
                    last_updated_str = status_data.get("last_updated", "")
                    if last_updated_str:
                        # Parse the timestamp (handle different formats)
                        try:
                            if "T" in last_updated_str:
                                last_updated = datetime.fromisoformat(last_updated_str.replace("Z", "+00:00"))
                            else:
                                last_updated = datetime.strptime(last_updated_str, "%Y-%m-%d %H:%M:%S")

                            # Make comparison timezone-naive for consistency
                            thirty_days_ago_naive = self.thirty_days_ago.replace(tzinfo=None) if hasattr(self.thirty_days_ago, 'tzinfo') and self.thirty_days_ago.tzinfo else self.thirty_days_ago
                            last_updated_naive = last_updated.replace(tzinfo=None) if hasattr(last_updated, 'tzinfo') and last_updated.tzinfo else last_updated

                            if last_updated_naive < thirty_days_ago_naive:
                                old_workspaces.append((agent_dir, last_updated))
                                self.log_operation("IDENTIFY", f"Old workspace: {agent_dir.name} (last active: {last_updated})")
                            else:
                                active_workspaces.append((agent_dir, last_updated))
                                self.log_operation("ACTIVE", f"Active workspace: {agent_dir.name} (last active: {last_updated})")
                        except ValueError:
                            self.log_operation("WARN", f"Could not parse timestamp for {agent_dir.name}: {last_updated_str}")
                    else:
                        # No timestamp, check directory modification time
                        dir_mtime = datetime.fromtimestamp(agent_dir.stat().st_mtime)
                        if dir_mtime < self.thirty_days_ago:
                            old_workspaces.append((agent_dir, dir_mtime))
                            self.log_operation("IDENTIFY", f"Old workspace (no status): {agent_dir.name} (modified: {dir_mtime})")
                        else:
                            active_workspaces.append((agent_dir, dir_mtime))
                except json.JSONDecodeError:
                    self.log_operation("WARN", f"Invalid status.json in {agent_dir.name}")
            else:
                # No status.json, check directory age
                dir_mtime = datetime.fromtimestamp(agent_dir.stat().st_mtime)
                if dir_mtime < self.thirty_days_ago:
                    old_workspaces.append((agent_dir, dir_mtime))
                    self.log_operation("IDENTIFY", f"Old workspace (no status): {agent_dir.name} (modified: {dir_mtime})")
                else:
                    active_workspaces.append((agent_dir, dir_mtime))

        self.log_operation("SUMMARY", f"Found {len(old_workspaces)} old workspaces and {len(active_workspaces)} active workspaces")
        return old_workspaces, active_workspaces

    def cleanup_temp_directories(self):
        """Clean up temporary directories"""
        self.log_operation("PHASE", "Starting temporary directory cleanup")

        # temp_repo_analysis
        temp_repo_dir = self.base_dir / "temp_repo_analysis"
        if self.safe_delete_directory(temp_repo_dir):
            self.log_operation("SUCCESS", "temp_repo_analysis directory cleaned up")
        else:
            self.log_operation("REVIEW", "temp_repo_analysis requires manual review")

        # temp_sales_funnel_p0 (already completed according to log)
        temp_sales_dir = self.base_dir / "temp_sales_funnel_p0"
        if not temp_sales_dir.exists():
            self.log_operation("COMPLETE", "temp_sales_funnel_p0 already removed in previous execution")
        elif self.safe_delete_directory(temp_sales_dir):
            self.log_operation("SUCCESS", "temp_sales_funnel_p0 directory cleaned up")
        else:
            self.log_operation("REVIEW", "temp_sales_funnel_p0 requires manual review")

    def archive_project_scans(self):
        """Archive old project scans"""
        self.log_operation("PHASE", "Starting project scans archival")

        project_scans_dir = self.base_dir / "project_scans"
        archived_count = self.archive_old_files(project_scans_dir, self.project_scans_archive, days_old=30)

        self.log_operation("COMPLETE", f"Archived {archived_count} old project scan files")

        # Clean up empty directories
        for dir_path in project_scans_dir.rglob("*"):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                self.log_operation("CLEANUP", f"Removed empty directory {dir_path}")

    def handle_debates_directory(self):
        """Handle debates directory (migration to decision log)"""
        debates_dir = self.base_dir / "debates"
        if not debates_dir.exists():
            self.log_operation("COMPLETE", "debates directory does not exist - no action required")
            return

        self.log_operation("PHASE", "Starting debates directory migration")

        # Create decision log structure
        decision_log_dir = self.base_dir / "archives" / "decision_log" / datetime.now().strftime("%Y")
        decision_log_dir.mkdir(parents=True, exist_ok=True)

        # Move completed/resolved debates
        completed_debates = list(debates_dir.glob("*completed*")) + list(debates_dir.glob("*resolved*"))
        for debate_file in completed_debates:
            shutil.move(str(debate_file), str(decision_log_dir / debate_file.name))
            self.log_operation("MIGRATE", f"Moved completed debate: {debate_file.name}")

        # Archive old debates (>90 days)
        archived_count = self.archive_old_files(debates_dir, self.debates_archive, days_old=90)
        self.log_operation("ARCHIVE", f"Archived {archived_count} old debate files")

        # Update decision log index
        index_file = decision_log_dir / "README.txt"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(f"Decision Log Archive - {datetime.now().strftime('%Y')}\n")
            f.write("========================================\n\n")
            for file_path in decision_log_dir.glob("*.md"):
                f.write(f"- {file_path.name}\n")

        self.log_operation("INDEX", f"Created decision log index: {index_file}")

    def execute_phase2_operations(self):
        """Execute all Phase 2 operations"""
        self.log_operation("START", "Phase 2 Directory Cleanup Operations - Agent-6")

        # Initialize log file
        log_file = self.base_dir / "DIRECTORY_AUDIT_PHASE2_EXECUTION_LOG.md"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"# Directory Audit Phase 2 Execution Log\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Agent:** Agent-6 (Coordination & Communication)\n")
            f.write(f"**Phase:** Controlled Cleanup & Archiving\n\n")

        # Execute operations in priority order
        self.cleanup_temp_directories()
        self.archive_project_scans()
        self.handle_debates_directory()

        # Analyze agent workspaces (but don't auto-cleanup yet - requires manual review)
        old_workspaces, active_workspaces = self.analyze_agent_workspaces()

        # Summary
        total_archived = 0
        total_cleaned = 0

        self.log_operation("SUMMARY", f"Phase 2 operations completed")
        self.log_operation("METRICS", f"Old workspaces identified: {len(old_workspaces)}")
        self.log_operation("METRICS", f"Active workspaces: {len(active_workspaces)}")
        self.log_operation("STATUS", "Ready for manual review of agent workspace cleanup candidates")

        print("\n" + "="*60)
        print("PHASE 2 EXECUTION COMPLETE")
        print("="*60)
        print(f"📊 Old workspaces to review: {len(old_workspaces)}")
        print(f"✅ Active workspaces preserved: {len(active_workspaces)}")
        print(f"📝 Full log: DIRECTORY_AUDIT_PHASE2_EXECUTION_LOG.md")
        print("="*60)

if __name__ == "__main__":
    cleaner = DirectoryCleanup()
    cleaner.execute_phase2_operations()