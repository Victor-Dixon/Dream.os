"""
State Snapshot Manager - AGI-26
================================

Automated state snapshots for rollback capability.
Captures system state hourly to enable < 5 minute rollback.

Features:
- Hourly automated snapshots
- Database state capture
- File system state capture
- Configuration state capture
- Fast restore (< 5 minutes)
- 7-day retention

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-4 (Captain) with Cloud Agent
License: MIT
"""

import os
import json
import shutil
import tarfile
import subprocess
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


@dataclass
class SnapshotConfig:
    """Configuration for state snapshots."""
    
    # Snapshot settings
    snapshot_dir: str = "/workspace/.state_snapshots"
    interval_hours: int = 1  # Snapshot every hour
    retention_days: int = 7  # Keep snapshots for 7 days
    
    # What to snapshot
    include_database: bool = True
    include_files: bool = True
    include_configs: bool = True
    include_agent_state: bool = True
    
    # File system paths to snapshot
    file_paths: List[str] = None
    
    # Database settings
    db_type: str = "sqlite"  # sqlite, postgres
    db_path: str = "/workspace/swarm.db"
    
    # Compression
    use_compression: bool = True
    compression_level: int = 6  # 0-9 (6 is good balance)
    
    def __post_init__(self):
        if self.file_paths is None:
            self.file_paths = [
                "/workspace/config",
                "/workspace/agent_workspaces",
                "/workspace/.killswitch_state",
            ]


@dataclass
class Snapshot:
    """Metadata for a state snapshot."""
    snapshot_id: str
    timestamp: str
    snapshot_path: str
    size_bytes: int
    components: Dict[str, bool]  # What was included
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class StateSnapshotManager:
    """
    Automated state snapshot manager for rollback capability.
    
    Captures:
    - Database state
    - File system state (configs, agent workspaces)
    - Agent status files
    - System configuration
    
    Provides:
    - Hourly automated snapshots
    - Fast restore (< 5 minutes target)
    - 7-day retention
    - Compression to save space
    """
    
    def __init__(self, config: Optional[SnapshotConfig] = None):
        """
        Initialize state snapshot manager.
        
        Args:
            config: Snapshot configuration (uses defaults if None)
        """
        self.config = config or SnapshotConfig()
        self.snapshot_dir = Path(self.config.snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_file = self.snapshot_dir / "snapshots.json"
        self.snapshots: List[Snapshot] = []
        
        self._load_metadata()
        
        logger.info(f"StateSnapshotManager initialized: {self.snapshot_dir}")
    
    def _load_metadata(self):
        """Load snapshot metadata from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                    self.snapshots = [
                        Snapshot(**snapshot_data)
                        for snapshot_data in data.get("snapshots", [])
                    ]
                logger.info(f"Loaded {len(self.snapshots)} snapshot records")
            except Exception as e:
                logger.error(f"Failed to load snapshot metadata: {e}")
    
    def _save_metadata(self):
        """Save snapshot metadata to disk."""
        try:
            data = {
                "snapshots": [s.to_dict() for s in self.snapshots],
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        except Exception as e:
            logger.error(f"Failed to save snapshot metadata: {e}")
    
    def create_snapshot(
        self,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Create a new state snapshot.
        
        Args:
            description: Optional description
            tags: Optional tags/metadata
        
        Returns:
            Snapshot ID if successful, None otherwise
        """
        snapshot_id = f"snapshot_{int(time.time())}"
        timestamp = datetime.now().isoformat()
        
        logger.info(f"Creating snapshot: {snapshot_id}")
        
        # Create snapshot directory
        snapshot_path = self.snapshot_dir / snapshot_id
        snapshot_path.mkdir(exist_ok=True)
        
        components = {}
        
        try:
            # Snapshot database
            if self.config.include_database:
                components["database"] = self._snapshot_database(snapshot_path)
            
            # Snapshot files
            if self.config.include_files:
                components["files"] = self._snapshot_files(snapshot_path)
            
            # Snapshot configs
            if self.config.include_configs:
                components["configs"] = self._snapshot_configs(snapshot_path)
            
            # Snapshot agent state
            if self.config.include_agent_state:
                components["agent_state"] = self._snapshot_agent_state(snapshot_path)
            
            # Compress snapshot
            if self.config.use_compression:
                self._compress_snapshot(snapshot_path)
            
            # Calculate size
            size_bytes = self._get_snapshot_size(snapshot_path)
            
            # Create snapshot record
            snapshot = Snapshot(
                snapshot_id=snapshot_id,
                timestamp=timestamp,
                snapshot_path=str(snapshot_path),
                size_bytes=size_bytes,
                components=components,
                metadata={
                    "description": description,
                    "tags": tags or {},
                    "config": asdict(self.config)
                }
            )
            
            self.snapshots.append(snapshot)
            self._save_metadata()
            
            logger.info(
                f"✅ Snapshot created: {snapshot_id} "
                f"(size: {size_bytes / (1024*1024):.1f} MB)"
            )
            
            # Cleanup old snapshots
            self._cleanup_old_snapshots()
            
            return snapshot_id
        
        except Exception as e:
            logger.error(f"Failed to create snapshot: {e}")
            # Cleanup failed snapshot
            if snapshot_path.exists():
                shutil.rmtree(snapshot_path, ignore_errors=True)
            return None
    
    def _snapshot_database(self, snapshot_path: Path) -> bool:
        """Snapshot database state."""
        try:
            if self.config.db_type == "sqlite":
                db_file = Path(self.config.db_path)
                if db_file.exists():
                    dest_file = snapshot_path / "database.db"
                    shutil.copy2(db_file, dest_file)
                    logger.debug("Database snapshot complete (SQLite)")
                    return True
            
            elif self.config.db_type == "postgres":
                # TODO: Implement postgres dump
                logger.warning("Postgres snapshot not yet implemented")
                return False
            
            return False
        
        except Exception as e:
            logger.error(f"Database snapshot failed: {e}")
            return False
    
    def _snapshot_files(self, snapshot_path: Path) -> bool:
        """Snapshot file system state."""
        try:
            files_dir = snapshot_path / "files"
            files_dir.mkdir(exist_ok=True)
            
            for source_path in self.config.file_paths:
                source = Path(source_path)
                if not source.exists():
                    logger.warning(f"Path not found: {source_path}")
                    continue
                
                # Determine destination path
                dest_name = source.name
                dest = files_dir / dest_name
                
                if source.is_file():
                    shutil.copy2(source, dest)
                elif source.is_dir():
                    shutil.copytree(source, dest, dirs_exist_ok=True)
            
            logger.debug("File snapshot complete")
            return True
        
        except Exception as e:
            logger.error(f"File snapshot failed: {e}")
            return False
    
    def _snapshot_configs(self, snapshot_path: Path) -> bool:
        """Snapshot configuration files."""
        try:
            config_dir = snapshot_path / "configs"
            config_dir.mkdir(exist_ok=True)
            
            # Copy config directory
            workspace_config = Path("/workspace/config")
            if workspace_config.exists():
                shutil.copytree(
                    workspace_config,
                    config_dir / "config",
                    dirs_exist_ok=True
                )
            
            logger.debug("Config snapshot complete")
            return True
        
        except Exception as e:
            logger.error(f"Config snapshot failed: {e}")
            return False
    
    def _snapshot_agent_state(self, snapshot_path: Path) -> bool:
        """Snapshot agent state files."""
        try:
            agent_dir = snapshot_path / "agent_state"
            agent_dir.mkdir(exist_ok=True)
            
            # Copy agent workspaces
            workspaces = Path("/workspace/agent_workspaces")
            if workspaces.exists():
                shutil.copytree(
                    workspaces,
                    agent_dir / "agent_workspaces",
                    dirs_exist_ok=True
                )
            
            logger.debug("Agent state snapshot complete")
            return True
        
        except Exception as e:
            logger.error(f"Agent state snapshot failed: {e}")
            return False
    
    def _compress_snapshot(self, snapshot_path: Path):
        """Compress snapshot directory to tarball."""
        try:
            tarball_path = Path(str(snapshot_path) + ".tar.gz")
            
            with tarfile.open(tarball_path, "w:gz", compresslevel=self.config.compression_level) as tar:
                tar.add(snapshot_path, arcname=snapshot_path.name)
            
            # Remove uncompressed directory
            shutil.rmtree(snapshot_path)
            
            logger.debug(f"Snapshot compressed: {tarball_path.name}")
        
        except Exception as e:
            logger.error(f"Snapshot compression failed: {e}")
    
    def _get_snapshot_size(self, snapshot_path: Path) -> int:
        """Get total size of snapshot."""
        # Check for compressed version
        tarball = Path(str(snapshot_path) + ".tar.gz")
        if tarball.exists():
            return tarball.stat().st_size
        
        # Calculate directory size
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(snapshot_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        
        return total_size
    
    def restore_snapshot(
        self,
        snapshot_id: str,
        components: Optional[List[str]] = None
    ) -> bool:
        """
        Restore from a snapshot.
        
        Args:
            snapshot_id: ID of snapshot to restore
            components: List of components to restore (None = all)
        
        Returns:
            True if restore successful
        """
        # Find snapshot
        snapshot = next((s for s in self.snapshots if s.snapshot_id == snapshot_id), None)
        if not snapshot:
            logger.error(f"Snapshot not found: {snapshot_id}")
            return False
        
        logger.info(f"Restoring snapshot: {snapshot_id}")
        start_time = time.time()
        
        try:
            snapshot_path = Path(snapshot.snapshot_path)
            
            # Decompress if needed
            tarball = Path(str(snapshot_path) + ".tar.gz")
            if tarball.exists():
                logger.info("Decompressing snapshot...")
                with tarfile.open(tarball, "r:gz") as tar:
                    tar.extractall(path=snapshot_path.parent)
            
            # Restore components
            if components is None:
                components = list(snapshot.components.keys())
            
            for component in components:
                if component == "database":
                    self._restore_database(snapshot_path)
                elif component == "files":
                    self._restore_files(snapshot_path)
                elif component == "configs":
                    self._restore_configs(snapshot_path)
                elif component == "agent_state":
                    self._restore_agent_state(snapshot_path)
            
            duration = time.time() - start_time
            logger.info(f"✅ Snapshot restored in {duration:.1f} seconds")
            
            return True
        
        except Exception as e:
            logger.error(f"Snapshot restore failed: {e}")
            return False
    
    def _restore_database(self, snapshot_path: Path):
        """Restore database from snapshot."""
        db_file = snapshot_path / "database.db"
        if db_file.exists():
            dest_file = Path(self.config.db_path)
            shutil.copy2(db_file, dest_file)
            logger.info("Database restored")
    
    def _restore_files(self, snapshot_path: Path):
        """Restore files from snapshot."""
        files_dir = snapshot_path / "files"
        if files_dir.exists():
            for item in files_dir.iterdir():
                # Find original path
                for original_path in self.config.file_paths:
                    original = Path(original_path)
                    if original.name == item.name:
                        if item.is_file():
                            shutil.copy2(item, original)
                        elif item.is_dir():
                            shutil.copytree(item, original, dirs_exist_ok=True)
                        logger.debug(f"Restored: {original_path}")
            logger.info("Files restored")
    
    def _restore_configs(self, snapshot_path: Path):
        """Restore configs from snapshot."""
        config_dir = snapshot_path / "configs" / "config"
        if config_dir.exists():
            dest_dir = Path("/workspace/config")
            shutil.copytree(config_dir, dest_dir, dirs_exist_ok=True)
            logger.info("Configs restored")
    
    def _restore_agent_state(self, snapshot_path: Path):
        """Restore agent state from snapshot."""
        agent_dir = snapshot_path / "agent_state" / "agent_workspaces"
        if agent_dir.exists():
            dest_dir = Path("/workspace/agent_workspaces")
            shutil.copytree(agent_dir, dest_dir, dirs_exist_ok=True)
            logger.info("Agent state restored")
    
    def _cleanup_old_snapshots(self):
        """Remove snapshots older than retention period."""
        cutoff_time = datetime.now() - timedelta(days=self.config.retention_days)
        
        removed_count = 0
        for snapshot in self.snapshots[:]:  # Copy list for safe removal
            snapshot_time = datetime.fromisoformat(snapshot.timestamp)
            
            if snapshot_time < cutoff_time:
                # Remove snapshot files
                snapshot_path = Path(snapshot.snapshot_path)
                tarball = Path(str(snapshot_path) + ".tar.gz")
                
                if tarball.exists():
                    tarball.unlink()
                elif snapshot_path.exists():
                    shutil.rmtree(snapshot_path)
                
                # Remove from list
                self.snapshots.remove(snapshot)
                removed_count += 1
        
        if removed_count > 0:
            self._save_metadata()
            logger.info(f"Cleaned up {removed_count} old snapshots")
    
    def list_snapshots(self) -> List[Dict]:
        """List all available snapshots."""
        return [s.to_dict() for s in self.snapshots]
    
    def get_latest_snapshot(self) -> Optional[Snapshot]:
        """Get the most recent snapshot."""
        if self.snapshots:
            return max(self.snapshots, key=lambda s: s.timestamp)
        return None


# Global singleton instance
_snapshot_manager_instance = None


def get_snapshot_manager() -> StateSnapshotManager:
    """Get the global snapshot manager instance."""
    global _snapshot_manager_instance
    if _snapshot_manager_instance is None:
        _snapshot_manager_instance = StateSnapshotManager()
    return _snapshot_manager_instance
