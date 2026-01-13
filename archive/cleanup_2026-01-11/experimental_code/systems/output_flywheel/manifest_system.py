"""
Session Manifest System - SSOT for Artifact Tracking

This module provides a manifest system to track artifact generation,
prevent duplicates, and ensure SSOT compliance across the Output Flywheel.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from uuid import UUID

logger = logging.getLogger(__name__)


class ManifestSystem:
    """
    Session Manifest System - Single Source of Truth for artifact tracking.
    
    Tracks all generated artifacts, links them to work sessions,
    prevents duplicate artifact generation, and ensures consistency.
    """

    def __init__(self, manifest_path: Optional[Path] = None):
        """
        Initialize manifest system.
        
        Args:
            manifest_path: Path to manifest storage (default: outputs/sessions/manifest.json)
        """
        if manifest_path is None:
            manifest_path = Path(__file__).parent / "outputs" / "sessions" / "manifest.json"
        
        self.manifest_path = manifest_path
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self._manifest: Dict = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Load manifest from disk."""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Failed to load manifest: {e}")
                return self._create_empty_manifest()
        return self._create_empty_manifest()

    def _create_empty_manifest(self) -> Dict:
        """Create empty manifest structure."""
        return {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "sessions": {},
            "artifacts": {},
            "artifact_index": {}
        }

    def _save_manifest(self):
        """Save manifest to disk."""
        self._manifest["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                json.dump(self._manifest, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to save manifest: {e}")

    def register_session(self, session_id: str, session_data: Dict) -> bool:
        """
        Register a work session in the manifest.
        
        Args:
            session_id: Unique session identifier (UUID)
            session_data: Work session data (work_session.json structure)
        
        Returns:
            True if registered successfully, False if duplicate
        """
        if session_id in self._manifest["sessions"]:
            logger.warning(f"Session {session_id} already registered")
            return False
        
        self._manifest["sessions"][session_id] = {
            "session_id": session_id,
            "session_type": session_data.get("session_type"),
            "timestamp": session_data.get("timestamp"),
            "agent_id": session_data.get("agent_id"),
            "registered": datetime.now().isoformat(),
            "artifacts": []
        }
        
        self._save_manifest()
        logger.info(f"✅ Registered session: {session_id}")
        return True

    def register_artifact(
        self,
        session_id: str,
        artifact_type: str,
        artifact_path: str,
        artifact_hash: Optional[str] = None
    ) -> bool:
        """
        Register an artifact in the manifest.
        
        Args:
            session_id: Session identifier
            artifact_type: Type of artifact (readme, blog_post, social_post, trade_journal)
            artifact_path: Path to artifact file
            artifact_hash: Optional hash for duplicate detection
        
        Returns:
            True if registered, False if duplicate detected
        """
        # Check for duplicate artifact
        if artifact_hash and self._is_duplicate_artifact(artifact_hash):
            logger.warning(f"⚠️ Duplicate artifact detected: {artifact_path} (hash: {artifact_hash})")
            return False
        
        artifact_id = f"{session_id}_{artifact_type}"
        
        # Register artifact
        self._manifest["artifacts"][artifact_id] = {
            "artifact_id": artifact_id,
            "session_id": session_id,
            "artifact_type": artifact_type,
            "artifact_path": artifact_path,
            "artifact_hash": artifact_hash,
            "registered": datetime.now().isoformat(),
            "status": "ready"
        }
        
        # Add to session's artifact list
        if session_id in self._manifest["sessions"]:
            self._manifest["sessions"][session_id]["artifacts"].append(artifact_id)
        
        # Index by hash for duplicate detection
        if artifact_hash:
            if artifact_hash not in self._manifest["artifact_index"]:
                self._manifest["artifact_index"][artifact_hash] = []
            self._manifest["artifact_index"][artifact_hash].append(artifact_id)
        
        self._save_manifest()
        logger.info(f"✅ Registered artifact: {artifact_id} ({artifact_type})")
        return True

    def _is_duplicate_artifact(self, artifact_hash: str) -> bool:
        """Check if artifact hash already exists."""
        return artifact_hash in self._manifest["artifact_index"]

    def get_session_artifacts(self, session_id: str) -> List[Dict]:
        """Get all artifacts for a session."""
        if session_id not in self._manifest["sessions"]:
            return []
        
        artifact_ids = self._manifest["sessions"][session_id]["artifacts"]
        return [
            self._manifest["artifacts"][aid]
            for aid in artifact_ids
            if aid in self._manifest["artifacts"]
        ]

    def get_artifact(self, artifact_id: str) -> Optional[Dict]:
        """Get artifact by ID."""
        return self._manifest["artifacts"].get(artifact_id)

    def list_sessions(self, session_type: Optional[str] = None) -> List[Dict]:
        """List all sessions, optionally filtered by type."""
        sessions = list(self._manifest["sessions"].values())
        if session_type:
            sessions = [s for s in sessions if s.get("session_type") == session_type]
        return sessions

    def list_artifacts(self, artifact_type: Optional[str] = None) -> List[Dict]:
        """List all artifacts, optionally filtered by type."""
        artifacts = list(self._manifest["artifacts"].values())
        if artifact_type:
            artifacts = [a for a in artifacts if a.get("artifact_type") == artifact_type]
        return artifacts

    def update_artifact_status(self, artifact_id: str, status: str) -> bool:
        """Update artifact status (ready, published, failed)."""
        if artifact_id not in self._manifest["artifacts"]:
            logger.warning(f"Artifact {artifact_id} not found")
            return False
        
        self._manifest["artifacts"][artifact_id]["status"] = status
        self._manifest["artifacts"][artifact_id]["status_updated"] = datetime.now().isoformat()
        self._save_manifest()
        logger.info(f"✅ Updated artifact status: {artifact_id} → {status}")
        return True

    def get_manifest_stats(self) -> Dict:
        """Get manifest statistics."""
        return {
            "total_sessions": len(self._manifest["sessions"]),
            "total_artifacts": len(self._manifest["artifacts"]),
            "sessions_by_type": self._count_by_type("sessions", "session_type"),
            "artifacts_by_type": self._count_by_type("artifacts", "artifact_type"),
            "artifacts_by_status": self._count_by_type("artifacts", "status"),
            "duplicate_hashes": len([
                h for h, aids in self._manifest["artifact_index"].items()
                if len(aids) > 1
            ])
        }

    def _count_by_type(self, collection: str, field: str) -> Dict[str, int]:
        """Count items by type field."""
        counts: Dict[str, int] = {}
        items = self._manifest.get(collection, {})
        for item in items.values():
            item_type = item.get(field, "unknown")
            counts[item_type] = counts.get(item_type, 0) + 1
        return counts

    def verify_ssot_compliance(self) -> Dict:
        """
        Verify SSOT compliance of the manifest system.
        
        Returns:
            Compliance report with violations and recommendations
        """
        violations = []
        warnings = []
        
        # Check for duplicate sessions
        session_ids = set()
        for session_id in self._manifest["sessions"]:
            if session_id in session_ids:
                violations.append(f"Duplicate session ID: {session_id}")
            session_ids.add(session_id)
        
        # Check for orphaned artifacts (artifacts without sessions)
        for artifact_id, artifact in self._manifest["artifacts"].items():
            session_id = artifact.get("session_id")
            if session_id and session_id not in self._manifest["sessions"]:
                warnings.append(f"Orphaned artifact: {artifact_id} (session {session_id} not found)")
        
        # Check for duplicate artifacts (same hash)
        for hash_val, artifact_ids in self._manifest["artifact_index"].items():
            if len(artifact_ids) > 1:
                warnings.append(f"Duplicate artifacts detected: {artifact_ids} (hash: {hash_val})")
        
        # Check for missing artifact files
        for artifact_id, artifact in self._manifest["artifacts"].items():
            artifact_path = Path(artifact.get("artifact_path", ""))
            if artifact_path and not artifact_path.exists():
                warnings.append(f"Missing artifact file: {artifact_id} ({artifact_path})")
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "timestamp": datetime.now().isoformat()
        }


def calculate_artifact_hash(artifact_path: Path) -> str:
    """
    Calculate SHA256 hash of artifact file for duplicate detection.
    
    Args:
        artifact_path: Path to artifact file
    
    Returns:
        SHA256 hash as hex string
    """
    import hashlib
    
    hasher = hashlib.sha256()
    try:
        with open(artifact_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        logger.error(f"Failed to calculate hash for {artifact_path}: {e}")
        return ""


if __name__ == "__main__":
    # Test manifest system
    manifest = ManifestSystem()
    
    # Test session registration
    test_session = {
        "session_id": "test-session-001",
        "session_type": "build",
        "timestamp": datetime.now().isoformat(),
        "agent_id": "Agent-8"
    }
    
    manifest.register_session("test-session-001", test_session)
    
    # Test artifact registration
    manifest.register_artifact(
        "test-session-001",
        "readme",
        "outputs/artifacts/readme_test.md",
        "test-hash-123"
    )
    
    # Get stats
    stats = manifest.get_manifest_stats()
    print(f"Manifest Stats: {stats}")
    
    # Verify SSOT compliance
    compliance = manifest.verify_ssot_compliance()
    print(f"SSOT Compliance: {compliance}")




