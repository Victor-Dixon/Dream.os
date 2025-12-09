"""
Stall resumer guard utilities.

Provides:
- is_resumer_prompt: detect stall/recovery prompts (no-reply).
- is_meaningful_progress: gate inactivity resets to real work.
"""

from typing import Any, Dict


RESUMER_MARKERS = {
    "STALL-RECOVERY",
    "NO-ACKNOWLEDGMENTS",
    "RESUMER PROMPT",
    "Inactivity Detected",
    "[C2A]",
    "#NO-REPLY",
    "#PROGRESS-ONLY",
    "#ARTIFACT-REQUIRED",
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




