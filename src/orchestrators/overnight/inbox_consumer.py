#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Inbox Consumer - Bridges Agent Responses to FSM System
=======================================================

Processes captured agent responses and converts them to FSM events.

Extracted from V1 overnight_runner/inbox_consumer.py and adapted for V2 compliance.

V2 Compliance: ≤400 lines, proper imports, error handling
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# V2 Integration imports
try:
    from ...core.unified_logging_system import get_logger
    from ...core.constants.paths import get_agent_inbox, ROOT_DIR
except ImportError as e:
    import logging
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_logger(name):
        return logging.getLogger(name)
    
    def get_agent_inbox(agent_id: str) -> Path:
        return Path("agent_workspaces") / agent_id / "inbox"
    
    ROOT_DIR = Path(__file__).resolve().parents[3]

logger = get_logger(__name__)

# V2 Path configuration - configurable via environment or config
def get_inbox_root(agent_id: str = "Agent-5") -> Path:
    """Get inbox root directory for agent."""
    return get_agent_inbox(agent_id)


def get_outbox_root(agent_id: str = "Agent-5") -> Path:
    """Get outbox root directory for FSM updates."""
    current_date = datetime.now().strftime("%Y%m%d")
    outbox_base = ROOT_DIR / "communications" / f"overnight_{current_date}" / agent_id / "fsm_update_inbox"
    return outbox_base


def ensure_outbox(agent_id: str = "Agent-5") -> Path:
    """Ensure the outbox directory exists."""
    outbox_root = get_outbox_root(agent_id)
    outbox_root.mkdir(parents=True, exist_ok=True)
    return outbox_root


def to_fsm_event(envelope: Dict[str, Any]) -> Dict[str, Any]:
    """Convert captured response envelope to FSM event format."""
    p = envelope.get("payload", {})
    
    if p.get("type") == "agent_report":
        return {
            "type": "fsm_update",
            "from": envelope.get("from", "unknown"),
            "to": "Agent-5",
            "timestamp": envelope.get("timestamp", datetime.now().isoformat()),
            "task_id": p.get("task", p.get("task_id", "unknown_task")),
            "state": "completed" if p.get("status", "").lower() in ["done", "completed", "finished"] else "in_progress",
            "summary": p.get("summary", p.get("commit_message", "Task completed")),
            "evidence": p.get("actions", p.get("evidence", [])),
            "raw": p.get("raw", "")
        }
    
    # Fallback for freeform responses
    return {
        "type": "note",
        "from": envelope.get("from", "unknown"),
        "to": "Agent-5",
        "timestamp": envelope.get("timestamp", datetime.now().isoformat()),
        "summary": p.get("summary", "Agent response captured"),
        "raw": p.get("raw", "")
    }


def process_inbox(agent_id: str = "Agent-5", outbox_root: Path = None) -> int:
    """
    Process all files in the inbox directory.
    
    Args:
        agent_id: Agent ID to process inbox for
        outbox_root: Optional outbox root path (uses default if None)
        
    Returns:
        Number of files processed
    """
    inbox_root = get_inbox_root(agent_id)
    if not inbox_root.exists():
        logger.warning(f"⚠️  Inbox directory does not exist: {inbox_root}")
        return 0
    
    if outbox_root is None:
        outbox_root = ensure_outbox(agent_id)
    
    processed_count = 0
    
    for f in sorted(inbox_root.glob("*.json")):
        try:
            # Read and parse the envelope
            env = json.loads(f.read_text(encoding="utf-8"))
            
            # Convert to FSM event format
            ev = to_fsm_event(env)
            
            # Write to outbox
            out = outbox_root / f.name
            out.write_text(json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8")
            
            # Remove processed file
            f.unlink(missing_ok=True)
            
            logger.info(f"[INBOX_CONSUMER] Processed {f.name} -> {ev.get('type', 'unknown')}")
            processed_count += 1
            
        except Exception as e:
            logger.error(f"Error processing {f.name}: {e}")
    
    return processed_count


def process_inbox_continuous(agent_id: str = "Agent-5", poll_interval: float = 1.0, max_iterations: int = None):
    """
    Continuously process inbox files.
    
    Args:
        agent_id: Agent ID to process inbox for
        poll_interval: Seconds between inbox checks
        max_iterations: Maximum number of iterations (None for infinite)
    """
    logger.info(f"Starting continuous inbox processing for {agent_id}")
    iteration = 0
    
    try:
        while max_iterations is None or iteration < max_iterations:
            processed = process_inbox(agent_id)
            if processed > 0:
                logger.info(f"Processed {processed} files from {agent_id} inbox")
            
            time.sleep(poll_interval)
            iteration += 1
            
    except KeyboardInterrupt:
        logger.info("Inbox processing stopped by user")
    except Exception as e:
        logger.error(f"Error in continuous inbox processing: {e}")


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Process agent inbox and convert to FSM events")
    parser.add_argument("--agent", default="Agent-5", help="Agent ID to process")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--poll-interval", type=float, default=1.0, help="Poll interval in seconds")
    parser.add_argument("--max-iterations", type=int, help="Maximum iterations (for continuous mode)")
    
    args = parser.parse_args()
    
    if args.continuous:
        process_inbox_continuous(args.agent, args.poll_interval, args.max_iterations)
    else:
        processed = process_inbox(args.agent)
        logger.info(f"Processed {processed} files")

