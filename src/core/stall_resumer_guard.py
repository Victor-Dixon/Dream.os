"""
Stall resumer guard utilities.
<!-- SSOT Domain: infrastructure -->


Provides:
- is_resumer_prompt: detect stall/recovery prompts (no-reply).
- is_meaningful_progress: gate inactivity resets to real work.
- should_send_resume: validate if resume prompt should be sent (prevents false positives).
"""

from typing import Any, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


RESUMER_MARKERS = {
    "SWARM PULSE",
    "SWARM-PULSE",
    "NO-ACKNOWLEDGMENTS",
    "RESUMER PROMPT",
    "Inactivity Detected",
    "[C2A]",
    "#NO-REPLY",
    "#PROGRESS-ONLY",
    "#ARTIFACT-REQUIRED",
    "#SWARM-PULSE",
    "#SWARM-HEARTBEAT",
}

NOISE_PHRASES = {
    "ack",
    "acknowledged",
    "resuming",
    "got it",
    "copy",
    "noted",
}


def is_resumer_prompt(message: str) -> bool:
    """Return True if the incoming text is a stall/resume prompt that should be no-reply."""
    text = message or ""
    return any(marker in text for marker in RESUMER_MARKERS)


def is_meaningful_progress(event: Dict[str, Any]) -> bool:
    """
    Return True only for events that represent real work:
    - git_commit
    - test_pass / validation_pass
    - report/doc update with delta
    - file_write outside trivial status updates
    """
    etype = (event.get("type") or "").lower()
    if etype in {"git_commit", "test_pass", "validation_pass", "report_created"}:
        return True

    if etype == "file_write":
        path = (event.get("path") or "").lower()
        if not path:
            return False
        if path.endswith("status.json"):
            return False
        return True

    if etype == "message":
        text = (event.get("text") or "").lower()
        if any(p in text for p in NOISE_PHRASES):
            return False
        return False

    return False


def should_send_resume(agent_id: str, lookback_minutes: int = 60) -> Tuple[bool, str]:
    """
    Validate if resume prompt should be sent to agent.
    
    Uses hardened activity detection to prevent false positives.
    
    Args:
        agent_id: Agent identifier
        lookback_minutes: How far back to check for activity
        
    Returns:
        (should_send: bool, reason: str)
    """
    try:
        from src.core.hardened_activity_detector import HardenedActivityDetector
        
        detector = HardenedActivityDetector()
        assessment = detector.assess_agent_activity(agent_id, lookback_minutes)
        
        # Don't send resume if agent is active
        if assessment.is_active:
            reason = (
                f"Agent is ACTIVE (confidence: {assessment.confidence:.2f}). "
                f"Last activity: {assessment.last_activity} "
                f"({assessment.inactivity_minutes:.1f} min ago). "
                f"Reasons: {', '.join(assessment.reasons)}"
            )
            logger.info(f"⏸️ Skipping resume for {agent_id}: {reason}")
            return False, reason
        
        # Send resume if agent is inactive and validation passed
        if not assessment.validation_passed:
            reason = (
                f"Activity signals failed validation. "
                f"Confidence: {assessment.confidence:.2f}. "
                f"Signals: {len(assessment.signals)}"
            )
            logger.warning(f"⚠️ Resume validation failed for {agent_id}: {reason}")
            # Still send resume but with warning
            return True, f"Validation failed but sending anyway: {reason}"
        
        reason = (
            f"Agent is INACTIVE (confidence: {assessment.confidence:.2f}). "
            f"Last activity: {assessment.last_activity or 'Never'}. "
            f"Inactivity: {assessment.inactivity_minutes:.1f} minutes. "
            f"Reasons: {', '.join(assessment.reasons)}"
        )
        logger.info(f"✅ Sending resume to {agent_id}: {reason}")
        return True, reason
        
    except ImportError:
        # Fallback: allow resume if hardened detector not available
        logger.warning("Hardened activity detector not available, allowing resume")
        return True, "Hardened detector not available, using fallback"
    except Exception as e:
        # On error, allow resume (fail open)
        logger.error(f"Error checking activity for {agent_id}: {e}")
        return True, f"Error checking activity: {e}"




