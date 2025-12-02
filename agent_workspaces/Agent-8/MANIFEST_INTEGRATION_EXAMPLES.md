# 🔧 Manifest System Integration Examples for Pipelines

**Date**: 2025-12-02 05:21:33  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: 📋 **INTEGRATION EXAMPLES**  
**Priority**: HIGH

---

## 🎯 INTEGRATION OBJECTIVE

**Mission**: Provide code examples for integrating manifest system into Output Flywheel pipelines

**Goal**: Ensure all pipelines register sessions and artifacts in the manifest system for SSOT compliance.

---

## 📋 INTEGRATION PATTERNS

### **Pattern 1: Build Pipeline Integration**

**File**: `systems/output_flywheel/pipelines/build_artifact.py`

**Integration Points**:
1. Register session at pipeline start
2. Register artifacts after generation
3. Calculate artifact hashes for deduplication
4. Verify SSOT compliance

**Example Code**:

```python
from systems.output_flywheel.manifest_system import ManifestSystem, calculate_artifact_hash
from systems.output_flywheel.ssot_verifier import SSOTVerifier
from pathlib import Path

def run_build_pipeline(session: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute Build → Artifact pipeline with manifest system integration."""
    session_id = session.get("session_id", "unknown-session")
    logger.info("Running Build → Artifact pipeline for session %s", session_id)
    
    # Initialize manifest system
    manifest = ManifestSystem()
    
    # Register session in manifest (SSOT compliance)
    if not manifest.register_session(session_id, session):
        logger.warning(f"Session {session_id} already registered or registration failed")
    
    # Pre-flight SSOT verification (optional but recommended)
    verifier = SSOTVerifier(Path("systems/output_flywheel"))
    pre_check = verifier.verify_work_session_ssot()
    if not pre_check["compliant"]:
        logger.warning(f"SSOT violations detected: {pre_check['violations']}")
    
    # ... existing pipeline code ...
    # (repo scan, story extraction, artifact generation)
    
    # After generating artifacts, register them in manifest
    artifacts = session.get("artifacts") or {}
    
    # Register README artifact
    if artifacts.get("readme", {}).get("generated"):
        readme_path = Path(artifacts["readme"]["path"])
        if readme_path.exists():
            artifact_hash = calculate_artifact_hash(readme_path)
            manifest.register_artifact(
                session_id,
                "readme",
                str(readme_path),
                artifact_hash
            )
    
    # Register build_log artifact
    if artifacts.get("build_log", {}).get("generated"):
        build_log_path = Path(artifacts["build_log"]["path"])
        if build_log_path.exists():
            artifact_hash = calculate_artifact_hash(build_log_path)
            manifest.register_artifact(
                session_id,
                "build_log",
                str(build_log_path),
                artifact_hash
            )
    
    # Register social_post artifact
    if artifacts.get("social_post", {}).get("generated"):
        social_path = Path(artifacts["social_post"]["path"])
        if social_path.exists():
            artifact_hash = calculate_artifact_hash(social_path)
            manifest.register_artifact(
                session_id,
                "social_post",
                str(social_path),
                artifact_hash
            )
    
    # Post-generation SSOT verification
    post_check = verifier.verify_artifact_ssot()
    if not post_check["compliant"]:
        logger.error(f"SSOT violations after generation: {post_check['violations']}")
    
    # Get manifest statistics for monitoring
    stats = manifest.get_manifest_stats()
    logger.info(f"Manifest stats: {stats['total_sessions']} sessions, {stats['total_artifacts']} artifacts")
    
    return session, outputs
```

---

### **Pattern 2: Trade Pipeline Integration**

**File**: `systems/output_flywheel/pipelines/trade_artifact.py`

**Example Code**:

```python
from systems.output_flywheel.manifest_system import ManifestSystem, calculate_artifact_hash

def run_trade_pipeline(session: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute Trade → Artifact pipeline with manifest system integration."""
    session_id = session.get("session_id", "unknown-session")
    
    # Initialize manifest system
    manifest = ManifestSystem()
    
    # Register session
    manifest.register_session(session_id, session)
    
    # ... existing pipeline code ...
    # (trade processing, journal generation, social post generation)
    
    # Register artifacts
    artifacts = session.get("artifacts") or {}
    
    if artifacts.get("trade_journal", {}).get("generated"):
        journal_path = Path(artifacts["trade_journal"]["path"])
        if journal_path.exists():
            artifact_hash = calculate_artifact_hash(journal_path)
            manifest.register_artifact(
                session_id,
                "trade_journal",
                str(journal_path),
                artifact_hash
            )
    
    if artifacts.get("social_post", {}).get("generated"):
        social_path = Path(artifacts["social_post"]["path"])
        if social_path.exists():
            artifact_hash = calculate_artifact_hash(social_path)
            manifest.register_artifact(
                session_id,
                "social_post",
                str(social_path),
                artifact_hash
            )
    
    return session, outputs
```

---

### **Pattern 3: Life/Aria Pipeline Integration**

**File**: `systems/output_flywheel/pipelines/life_aria_artifact.py`

**Example Code**:

```python
from systems.output_flywheel.manifest_system import ManifestSystem, calculate_artifact_hash

def run_life_aria_pipeline(session: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute Life/Aria → Artifact pipeline with manifest system integration."""
    session_id = session.get("session_id", "unknown-session")
    
    # Initialize manifest system
    manifest = ManifestSystem()
    
    # Register session
    manifest.register_session(session_id, session)
    
    # ... existing pipeline code ...
    # (devlog generation, screenshot notes, social post)
    
    # Register artifacts
    artifacts = session.get("artifacts") or {}
    
    for artifact_type in ["devlog_entry", "screenshot_gallery_notes", "social_post"]:
        if artifacts.get(artifact_type, {}).get("generated"):
            artifact_path = Path(artifacts[artifact_type]["path"])
            if artifact_path.exists():
                artifact_hash = calculate_artifact_hash(artifact_path)
                manifest.register_artifact(
                    session_id,
                    artifact_type,
                    str(artifact_path),
                    artifact_hash
                )
    
    return session, outputs
```

---

## 🔍 SSOT VERIFICATION INTEGRATION

### **Pre-Flight Verification**:

```python
from systems.output_flywheel.ssot_verifier import SSOTVerifier

def run_pipeline_with_ssot_verification(session: Dict[str, Any]):
    """Run pipeline with SSOT verification."""
    verifier = SSOTVerifier(Path("systems/output_flywheel"))
    
    # Pre-flight check
    pre_check = verifier.verify_work_session_ssot()
    if not pre_check["compliant"]:
        logger.warning(f"Pre-flight SSOT violations: {pre_check['violations']}")
    
    # Run pipeline
    updated_session, outputs = run_pipeline(session)
    
    # Post-generation check
    post_check = verifier.verify_artifact_ssot()
    if not post_check["compliant"]:
        logger.error(f"Post-generation SSOT violations: {post_check['violations']}")
    
    return updated_session, outputs
```

---

## 📊 MONITORING INTEGRATION

### **Manifest Statistics for Agent-5**:

```python
from systems.output_flywheel.manifest_system import ManifestSystem

def get_metrics_for_monitoring():
    """Get manifest statistics for monitoring."""
    manifest = ManifestSystem()
    stats = manifest.get_manifest_stats()
    
    return {
        "total_sessions": stats["total_sessions"],
        "total_artifacts": stats["total_artifacts"],
        "sessions_by_type": stats["sessions_by_type"],
        "artifacts_by_type": stats["artifacts_by_type"],
        "artifacts_by_status": stats["artifacts_by_status"],
        "duplicate_hashes": stats["duplicate_hashes"]
    }
```

---

## ✅ INTEGRATION CHECKLIST

### **For Each Pipeline**:
- [ ] Import ManifestSystem and calculate_artifact_hash
- [ ] Initialize manifest system at pipeline start
- [ ] Register session when pipeline starts
- [ ] Register each artifact after generation
- [ ] Calculate artifact hash for deduplication
- [ ] Verify SSOT compliance (optional but recommended)
- [ ] Log manifest statistics

---

## 🎯 NEXT STEPS

1. ⏭️ Integrate manifest system into build_artifact.py
2. ⏭️ Integrate manifest system into trade_artifact.py
3. ⏭️ Integrate manifest system into life_aria_artifact.py
4. ⏭️ Test integration with sample sessions
5. ⏭️ Verify SSOT compliance

---

🐝 WE. ARE. SWARM. ⚡🔥

**Agent-8 - SSOT & System Integration Specialist**  
*Providing Manifest System Integration Examples*

