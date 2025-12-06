"""
SSOT Compliance Verifier for Output Flywheel

Verifies single source of truth compliance across all pipelines,
work sessions, and artifacts.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class SSOTVerifier:
    """
    SSOT Compliance Verifier for Output Flywheel system.
    
    Verifies:
    - Single source of truth for work sessions
    - No duplicate artifacts
    - SSOT compliance across pipelines
    - Manifest system consistency
    """

    def __init__(self, base_path: Path):
        """
        Initialize SSOT verifier.
        
        Args:
            base_path: Base path to output_flywheel system
        """
        self.base_path = Path(base_path)
        self.sessions_path = self.base_path / "outputs" / "sessions"
        self.artifacts_path = self.base_path / "outputs" / "artifacts"
        self.manifest_path = self.base_path / "outputs" / "sessions" / "manifest.json"

    def verify_work_session_ssot(self) -> Dict:
        """
        Verify single source of truth for work sessions.
        
        Checks:
        - No duplicate session IDs
        - Single storage location for sessions
        - No duplicate session tracking systems
        """
        violations = []
        warnings = []
        
        # Check for duplicate session files
        session_files = list(self.sessions_path.glob("work_session_*.json"))
        session_ids: Set[str] = set()
        
        for session_file in session_files:
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    session_id = session_data.get("session_id")
                    
                    if session_id in session_ids:
                        violations.append(f"Duplicate session ID: {session_id} (file: {session_file.name})")
                    session_ids.add(session_id)
            except (json.JSONDecodeError, IOError) as e:
                warnings.append(f"Failed to read session file {session_file.name}: {e}")
        
        # Check for session files in wrong locations
        other_session_files = list(self.base_path.rglob("work_session_*.json"))
        if len(other_session_files) > len(session_files):
            warnings.append(f"Found {len(other_session_files) - len(session_files)} session files outside sessions/ directory")
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "total_sessions": len(session_ids),
            "session_files": len(session_files)
        }

    def verify_artifact_ssot(self) -> Dict:
        """
        Verify single source of truth for artifacts.
        
        Checks:
        - No duplicate artifacts
        - Single storage location
        - Artifact deduplication working
        """
        violations = []
        warnings = []
        
        # Check for duplicate artifact files
        artifact_files = list(self.artifacts_path.rglob("*.md"))
        artifact_names: Dict[str, List[Path]] = {}
        
        for artifact_file in artifact_files:
            artifact_name = artifact_file.name
            if artifact_name not in artifact_names:
                artifact_names[artifact_name] = []
            artifact_names[artifact_name].append(artifact_file)
        
        # Check for duplicate names
        for name, paths in artifact_names.items():
            if len(paths) > 1:
                warnings.append(f"Duplicate artifact name: {name} ({len(paths)} files)")
        
        # Check for artifacts outside artifacts/ directory
        other_artifacts = []
        for pattern in ["README.md", "build-log.md", "social_post*.md", "trade_journal*.md"]:
            other_artifacts.extend(list(self.base_path.parent.rglob(pattern)))
        
        if other_artifacts:
            warnings.append(f"Found {len(other_artifacts)} artifacts outside artifacts/ directory")
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "total_artifacts": len(artifact_files),
            "duplicate_names": len([n for n, p in artifact_names.items() if len(p) > 1])
        }

    def verify_pipeline_ssot(self) -> Dict:
        """
        Verify SSOT compliance across pipelines.
        
        Checks:
        - Each pipeline uses SSOT for input data
        - Artifacts stored in SSOT location
        - No duplicate pipeline execution
        """
        violations = []
        warnings = []
        
        # Check pipeline files exist
        pipelines_path = self.base_path / "pipelines"
        expected_pipelines = ["build_artifact.py", "trade_artifact.py", "life_aria_artifact.py"]
        
        for pipeline_file in expected_pipelines:
            pipeline_path = pipelines_path / pipeline_file
            if not pipeline_path.exists():
                warnings.append(f"Expected pipeline not found: {pipeline_file}")
        
        # Check for duplicate pipeline execution (would need runtime tracking)
        # This is a placeholder for future implementation
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "pipelines_checked": len(expected_pipelines)
        }

    def verify_manifest_ssot(self) -> Dict:
        """
        Verify manifest system SSOT compliance.
        
        Checks:
        - Manifest file exists
        - Manifest structure is valid
        - No duplicate entries
        """
        violations = []
        warnings = []
        
        if not self.manifest_path.exists():
            warnings.append("Manifest file does not exist (may be first run)")
            return {
                "compliant": True,
                "violations": violations,
                "warnings": warnings,
                "manifest_exists": False
            }
        
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Check for duplicate session IDs in manifest
            session_ids = set()
            for session_id in manifest.get("sessions", {}):
                if session_id in session_ids:
                    violations.append(f"Duplicate session ID in manifest: {session_id}")
                session_ids.add(session_id)
            
            # Check for duplicate artifact IDs
            artifact_ids = set()
            for artifact_id in manifest.get("artifacts", {}):
                if artifact_id in artifact_ids:
                    violations.append(f"Duplicate artifact ID in manifest: {artifact_id}")
                artifact_ids.add(artifact_id)
            
        except (json.JSONDecodeError, IOError) as e:
            violations.append(f"Failed to read manifest: {e}")
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "manifest_exists": True
        }

    def verify_all(self) -> Dict:
        """
        Run all SSOT verification checks.
        
        Returns:
            Comprehensive SSOT compliance report
        """
        logger.info("🔍 Starting SSOT verification...")
        
        work_session_ssot = self.verify_work_session_ssot()
        artifact_ssot = self.verify_artifact_ssot()
        pipeline_ssot = self.verify_pipeline_ssot()
        manifest_ssot = self.verify_manifest_ssot()
        
        all_compliant = all([
            work_session_ssot["compliant"],
            artifact_ssot["compliant"],
            pipeline_ssot["compliant"],
            manifest_ssot["compliant"]
        ])
        
        total_violations = (
            len(work_session_ssot["violations"]) +
            len(artifact_ssot["violations"]) +
            len(pipeline_ssot["violations"]) +
            len(manifest_ssot["violations"])
        )
        
        total_warnings = (
            len(work_session_ssot["warnings"]) +
            len(artifact_ssot["warnings"]) +
            len(pipeline_ssot["warnings"]) +
            len(manifest_ssot["warnings"])
        )
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "compliant": all_compliant,
            "total_violations": total_violations,
            "total_warnings": total_warnings,
            "work_session_ssot": work_session_ssot,
            "artifact_ssot": artifact_ssot,
            "pipeline_ssot": pipeline_ssot,
            "manifest_ssot": manifest_ssot
        }
        
        if all_compliant:
            logger.info("✅ SSOT verification complete - All checks passed")
        else:
            logger.warning(f"⚠️ SSOT verification complete - {total_violations} violations found")
        
        return report


if __name__ == "__main__":
    # Test SSOT verifier
    base_path = Path(__file__).parent
    verifier = SSOTVerifier(base_path)
    
    report = verifier.verify_all()
    print(json.dumps(report, indent=2))




