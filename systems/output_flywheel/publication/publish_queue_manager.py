"""
Publish Queue Manager - Phase 3
=================================

Manages publication queue for artifacts.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import json
import time
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from uuid import uuid4


class PublishQueueEntry:
    """Publication queue entry."""
    
    def __init__(
        self,
        artifact_type: str,
        source_file: str,
        targets: List[str],
        status: str = "pending",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize queue entry."""
        self.id = str(uuid4())
        self.artifact_type = artifact_type
        self.source_file = source_file
        self.targets = targets
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "artifact_type": self.artifact_type,
            "source_file": self.source_file,
            "targets": self.targets,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PublishQueueEntry':
        """Create from dictionary."""
        entry = cls(
            artifact_type=data["artifact_type"],
            source_file=data["source_file"],
            targets=data["targets"],
            status=data.get("status", "pending"),
            metadata=data.get("metadata", {})
        )
        entry.id = data.get("id", str(uuid4()))
        entry.created_at = data.get("created_at", datetime.now().isoformat())
        entry.updated_at = data.get("updated_at", datetime.now().isoformat())
        return entry


class PublishQueueManager:
    """Manages publication queue."""
    
    def __init__(self, queue_dir: Optional[Path] = None):
        """Initialize queue manager."""
        if queue_dir is None:
            queue_dir = Path("systems/output_flywheel/outputs/publish_queue")
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self.queue_file = self.queue_dir / "publish_queue.json"
    
    def _load_queue(self) -> List[Dict[str, Any]]:
        """Load queue from JSON file."""
        if not self.queue_file.exists():
            return []
        
        try:
            content = self.queue_file.read_text(encoding="utf-8")
            if not content.strip():
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "entries" in data:
                return data["entries"]
            return []
        except Exception as e:
            print(f"⚠️ Failed to load publish queue: {e}")
            return []
    
    def _save_queue(self, entries: List[Dict[str, Any]], max_retries: int = 5, base_delay: float = 0.1) -> None:
        """Save queue to JSON file with retry logic."""
        temp_file = self.queue_file.with_suffix('.json.tmp')
        
        # Write to temp file
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, ensure_ascii=False, default=str)
        except PermissionError as e:
            error_msg = f"Permission denied writing temp file: {temp_file}\n"
            error_msg += f"Error: {e}\n"
            error_msg += "Suggestion: Check file permissions and ensure directory is writable"
            raise PermissionError(error_msg) from e
        except OSError as e:
            error_msg = f"OS error writing temp file: {temp_file}\n"
            error_msg += f"Error: {e}\n"
            error_msg += "Suggestion: Check disk space and directory permissions"
            raise OSError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error writing temp file: {temp_file}\n"
            error_msg += f"Error: {e}\n"
            error_msg += f"Error type: {type(e).__name__}"
            raise Exception(error_msg) from e
        
        # Atomic move with retry logic
        for attempt in range(max_retries):
            try:
                if self.queue_file.exists():
                    try:
                        self.queue_file.unlink()
                    except PermissionError:
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt)
                            time.sleep(delay)
                            continue
                        raise
                
                shutil.move(str(temp_file), str(self.queue_file))
                return
                
            except (PermissionError, OSError) as e:
                winerror_code = getattr(e, 'winerror', None)
                if winerror_code == 5:  # Access Denied
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
                        continue
                    else:
                        error_msg = f"Failed to save queue after {max_retries} retries\n"
                        error_msg += f"File: {self.queue_file}\n"
                        error_msg += f"Error: Access Denied (WinError 5)\n"
                        error_msg += "Suggestion: Close any programs accessing the queue file and try again"
                        raise PermissionError(error_msg) from e
                elif winerror_code == 32:  # File in use
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        delay = min(delay, 2.0)  # Cap delay
                        time.sleep(delay)
                        continue
                    else:
                        error_msg = f"Failed to save queue after {max_retries} retries\n"
                        error_msg += f"File: {self.queue_file}\n"
                        error_msg += f"Error: File in use (WinError 32)\n"
                        error_msg += "Suggestion: Another process is using the queue file. Wait and try again."
                        raise OSError(error_msg) from e
                else:
                    error_msg = f"Failed to save queue file\n"
                    error_msg += f"File: {self.queue_file}\n"
                    error_msg += f"Error: {e}\n"
                    if winerror_code:
                        error_msg += f"WinError code: {winerror_code}\n"
                    error_msg += "Suggestion: Check file permissions and disk space"
                    raise
    
    def add_entry(
        self,
        artifact_type: str,
        source_file: str,
        targets: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Add entry to publication queue."""
        entry = PublishQueueEntry(
            artifact_type=artifact_type,
            source_file=source_file,
            targets=targets,
            metadata=metadata
        )
        
        entries = self._load_queue()
        entries.append(entry.to_dict())
        self._save_queue(entries)
        
        return entry.id
    
    def get_pending_entries(self) -> List[PublishQueueEntry]:
        """Get all pending entries."""
        entries_data = self._load_queue()
        return [
            PublishQueueEntry.from_dict(e)
            for e in entries_data
            if e.get("status") == "pending"
        ]
    
    def update_status(self, entry_id: str, status: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update entry status."""
        entries = self._load_queue()
        
        for entry in entries:
            if entry.get("id") == entry_id:
                entry["status"] = status
                entry["updated_at"] = datetime.now().isoformat()
                if metadata:
                    entry["metadata"].update(metadata)
                self._save_queue(entries)
                return True
        
        return False
    
    def get_entry(self, entry_id: str) -> Optional[PublishQueueEntry]:
        """Get entry by ID."""
        entries = self._load_queue()
        
        for entry_data in entries:
            if entry_data.get("id") == entry_id:
                return PublishQueueEntry.from_dict(entry_data)
        
        return None
    
    def remove_entry(self, entry_id: str) -> bool:
        """Remove entry from queue."""
        entries = self._load_queue()
        original_count = len(entries)
        
        entries = [e for e in entries if e.get("id") != entry_id]
        
        if len(entries) < original_count:
            self._save_queue(entries)
            return True
        
        return False
    
    def get_queue_stats(self) -> Dict[str, int]:
        """Get queue statistics."""
        entries = self._load_queue()
        
        stats = {
            "total": len(entries),
            "pending": 0,
            "processing": 0,
            "published": 0,
            "failed": 0
        }
        
        for entry in entries:
            status = entry.get("status", "pending")
            if status in stats:
                stats[status] += 1
        
        return stats

