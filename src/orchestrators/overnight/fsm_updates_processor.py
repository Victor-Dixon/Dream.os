#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

FSM Updates Processor - V2 Compliant
=====================================

Processes FSM_UPDATES JSON files from V1 and converts them to V2 FSM format.

Extracted from V1 FSM_UPDATES/ directory analysis.

V2 Compliance: ≤400 lines, proper imports, error handling
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# V2 Integration imports
try:
    from ...core.unified_logging_system import get_logger
    from ...core.constants.paths import ROOT_DIR
    from .fsm_bridge import handle_fsm_update, process_fsm_update
except ImportError as e:
    import logging
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_logger(name):
        return logging.getLogger(name)
    
    ROOT_DIR = Path(__file__).resolve().parents[3]
    
    def handle_fsm_update(update: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": False, "error": "fsm_bridge not available"}
    
    def process_fsm_update(agent: str, update_data: Dict[str, Any]) -> bool:
        return False

logger = get_logger(__name__)


def process_fsm_update_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Process a single FSM update JSON file.
    
    Args:
        filepath: Path to FSM update JSON file
        
    Returns:
        Processed update data or None on error
    """
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
        
        # Extract FSM update from nested structure
        fsm_update = data.get("fsm_update", {})
        if not fsm_update:
            logger.warning(f"No fsm_update found in {filepath.name}")
            return None
        
        # Convert to V2 format
        from_agent = fsm_update.get("from_agent", "unknown")
        to_agent = fsm_update.get("to_agent", "Agent-5")
        task_id = fsm_update.get("task_id", "unknown_task")
        state = fsm_update.get("state", "completed")
        summary = fsm_update.get("summary", "")
        evidence = fsm_update.get("evidence", {})
        
        # Convert evidence dict to list format
        evidence_list = []
        if isinstance(evidence, dict):
            for key, value in evidence.items():
                evidence_list.append({key: value})
        elif isinstance(evidence, list):
            evidence_list = evidence
        
        # Create V2 update format
        update_data = {
            "task_id": task_id,
            "state": state.lower() if isinstance(state, str) else str(state).lower(),
            "summary": summary,
            "evidence": evidence_list,
            "from": from_agent,
            "to": to_agent,
            "timestamp": fsm_update.get("timestamp", datetime.now().isoformat()),
            "workflow": "default",
        }
        
        return update_data
        
    except Exception as e:
        logger.error(f"Failed to process {filepath.name}: {e}")
        return None


def process_fsm_updates_directory(updates_dir: Path, target_agent: str = "Agent-5") -> int:
    """
    Process all FSM update files in a directory.
    
    Args:
        updates_dir: Directory containing FSM update JSON files
        target_agent: Target agent for processing
        
    Returns:
        Number of files processed successfully
    """
    if not updates_dir.exists():
        logger.warning(f"FSM updates directory does not exist: {updates_dir}")
        return 0
    
    processed_count = 0
    
    for filepath in sorted(updates_dir.glob("*.json")):
        update_data = process_fsm_update_file(filepath)
        if not update_data:
            continue
        
        # Process through FSM bridge
        try:
            # Use handle_fsm_update for direct processing
            result = handle_fsm_update(update_data)
            if result.get("ok"):
                logger.info(f"✅ Processed {filepath.name} -> task_id: {update_data['task_id']}")
                processed_count += 1
            else:
                logger.warning(f"⚠️  Failed to process {filepath.name}: {result.get('error')}")
        except Exception as e:
            logger.error(f"❌ Error processing {filepath.name}: {e}")
    
    return processed_count


def migrate_v1_fsm_updates(v1_updates_dir: Path, v2_fsm_dir: Optional[Path] = None) -> int:
    """
    Migrate FSM updates from V1 to V2 format.
    
    Args:
        v1_updates_dir: V1 FSM_UPDATES directory path
        v2_fsm_dir: V2 FSM data directory (uses default if None)
        
    Returns:
        Number of updates migrated
    """
    if v2_fsm_dir is None:
        v2_fsm_dir = ROOT_DIR / "fsm_data" / "tasks"
    
    v2_fsm_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Migrating FSM updates from {v1_updates_dir} to {v2_fsm_dir}")
    
    processed = process_fsm_updates_directory(v1_updates_dir)
    
    logger.info(f"✅ Migrated {processed} FSM updates")
    return processed


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process FSM updates from V1")
    parser.add_argument("--v1-dir", help="V1 FSM_UPDATES directory path")
    parser.add_argument("--v2-dir", help="V2 FSM data directory path")
    parser.add_argument("--agent", default="Agent-5", help="Target agent for processing")
    
    args = parser.parse_args()
    
    if args.v1_dir:
        v1_dir = Path(args.v1_dir)
        v2_dir = Path(args.v2_dir) if args.v2_dir else None
        migrate_v1_fsm_updates(v1_dir, v2_dir)
    else:
        # Default: process from V1 repository
        v1_updates_dir = Path("D:/Agent_Cellphone/FSM_UPDATES")
        if v1_updates_dir.exists():
            migrate_v1_fsm_updates(v1_updates_dir)
        else:
            logger.error(f"V1 FSM_UPDATES directory not found: {v1_updates_dir}")

