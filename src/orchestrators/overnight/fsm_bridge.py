#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

FSM Bridge for Overnight Runner - V2 Compliant
===============================================

This module provides a bridge between the overnight runner and the FSM system,
allowing for state management and task orchestration.

Extracted from V1 overnight_runner/fsm_bridge.py and adapted for V2 compliance.

V2 Compliance: ≤400 lines, proper imports, error handling
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# V2 Integration imports
try:
    from ...core.config_ssot import get_unified_config
    from ...core.unified_logging_system import get_logger
    from ...core.constants.paths import get_agent_inbox, get_agent_workspace, ROOT_DIR
except ImportError as e:
    import logging
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)
    
    def get_agent_inbox(agent_id: str) -> Path:
        return Path("agent_workspaces") / agent_id / "inbox"
    
    def get_agent_workspace(agent_id: str) -> Path:
        return Path("agent_workspaces") / agent_id
    
    ROOT_DIR = Path(__file__).resolve().parents[3]

logger = get_logger(__name__)

# V2 Path configuration
FSM_ROOT = ROOT_DIR / "fsm_data"
TASKS_DIR = FSM_ROOT / "tasks"
WORKFLOWS_DIR = FSM_ROOT / "workflows"

# Ensure directories exist
TASKS_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)


def _write_inbox_message(agent: str, message: Dict[str, Any]) -> bool:
    """Write a message to an agent's inbox (V2 compliant)."""
    # Validate agent ID
    valid_agent_ids = {f"Agent-{i}" for i in range(1, 9)}
    if agent not in valid_agent_ids:
        logger.error(
            f"Invalid agent ID: '{agent}'. Must be one of: {', '.join(sorted(valid_agent_ids))}"
        )
        return False
    
    try:
        inbox_dir = get_agent_inbox(agent)
        inbox_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fsm_message_{timestamp}.json"
        filepath = inbox_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Message written to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to write message to {agent} inbox: {e}")
        return False


def _read_inbox_messages(agent: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Read messages from an agent's inbox (V2 compliant)."""
    try:
        inbox_dir = get_agent_inbox(agent)
        if not inbox_dir.exists():
            return []
        
        messages = []
        for filepath in sorted(inbox_dir.glob("fsm_message_*.json"), reverse=True):
            if len(messages) >= limit:
                break
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    message = json.load(f)
                    message['_filepath'] = str(filepath)
                    messages.append(message)
            except Exception as e:
                logger.warning(f"⚠️  Failed to read {filepath}: {e}")
                continue
        
        return messages
        
    except Exception as e:
        logger.error(f"❌ Failed to read inbox for {agent}: {e}")
        return []


def _scan_repositories_for_tasks(repo_root: Path = None) -> List[Dict[str, Any]]:
    """Scan all repositories for TASK_LIST.md entries and seed queued tasks."""
    tasks = []
    
    # Use configurable repo root or default
    if repo_root is None:
        repo_root = ROOT_DIR / "repos"
    
    if not repo_root.exists():
        logger.warning(f"⚠️  Repository root {repo_root} does not exist")
        return tasks

    try:
        for repo in sorted(repo_root.iterdir()):
            if not repo.is_dir() or repo.name.startswith('.'):
                continue

            tasklist_file = repo / "TASK_LIST.md"
            if not tasklist_file.exists():
                continue

            try:
                # Read TASK_LIST.md and extract tasks
                content = tasklist_file.read_text(encoding='utf-8')

                # Simple task extraction (can be enhanced)
                lines = content.split('\n')
                current_task = None

                for line in lines:
                    line = line.strip()
                    if line.startswith('## '):
                        if current_task:
                            tasks.append(current_task)

                        current_task = {
                            'repo': repo.name,
                            'title': line[3:],  # Remove '## '
                            'status': 'queued',
                            'created': datetime.now().isoformat(),
                            'filepath': str(tasklist_file)
                        }
                    elif line.startswith('- ') and current_task:
                        if 'description' not in current_task:
                            current_task['description'] = line[2:]  # Remove '- '

                if current_task:
                    tasks.append(current_task)

            except Exception as e:
                logger.warning(f"⚠️  Failed to process {tasklist_file}: {e}")
                continue

        logger.info(f"✅ Scanned {len(tasks)} tasks from repositories")
        return tasks

    except Exception as e:
        logger.error(f"❌ Failed to scan repositories: {e}")
        return tasks


def _create_fsm_task(owner: str, task_data: Dict[str, Any], repo_root: Path = None) -> Dict[str, Any]:
    """Create an FSM task from task data."""
    if repo_root is None:
        repo_root = ROOT_DIR / "repos"
    
    return {
        "id": f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "type": "task",
        "owner": owner,
        "title": task_data.get('title', 'Untitled Task'),
        "description": task_data.get('description', 'No description'),
        "repo": task_data.get('repo', 'unknown'),
        "status": "queued",
        "priority": "medium",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "assignee": None,
        "evidence": [],
        "transitions": [],
        "workflow": "default",
        "repo_path": str(repo_root / task_data.get('repo', '')),
    }


def handle_fsm_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Assign queued tasks to agents and drop messages into their inboxes."""
    agents = payload.get("agents", [])
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    
    available: List[tuple[Path, Dict[str, Any]]] = []
    for fp in sorted(TASKS_DIR.glob("*.json")):
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
            if data.get("state") == "queued" and not data.get("owner"):
                available.append((fp, data))
        except Exception as e:
            logger.warning(f"⚠️  Failed to read task file {fp}: {e}")
            continue

    assigned = 0
    for agent in agents:
        if not available:
            break
        fp, data = available.pop(0)
        data["owner"] = agent
        data["state"] = "assigned"
        fp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        
        message = {
            "type": "task",
            "from": payload.get("from"),
            "to": agent,
            "task_id": data.get("task_id") or data.get("id"),
            "repo": data.get("repo"),
            "intent": data.get("intent"),
            "timestamp": datetime.now().isoformat(),
        }
        
        inbox_dir = get_agent_inbox(agent)
        inbox_dir.mkdir(parents=True, exist_ok=True)
        msg_fp = inbox_dir / f"task_{data.get('task_id') or data.get('id')}.json"
        msg_fp.write_text(json.dumps(message, indent=2), encoding="utf-8")
        assigned += 1

    return {"ok": True, "count": assigned}


def handle_fsm_update(update: Dict[str, Any]) -> Dict[str, Any]:
    """Persist task state updates and notify the captain."""
    task_id = update.get("task_id")
    if not task_id:
        return {"ok": False, "error": "task_id required"}

    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    fp = TASKS_DIR / f"{task_id}.json"
    data: Dict[str, Any] = {}
    if fp.exists():
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning(f"⚠️  Failed to read task file {fp}: {e}")
    
    data.update({"task_id": task_id, "state": update.get("state")})
    if update.get("evidence"):
        data.setdefault("evidence", []).extend(update["evidence"])
    
    fp.write_text(json.dumps(data, indent=2), encoding="utf-8")

    captain = update.get("captain")
    if captain:
        verify_msg = {
            "type": "verify",
            "from": update.get("from"),
            "task_id": task_id,
            "state": update.get("state"),
            "summary": update.get("summary"),
            "timestamp": datetime.now().isoformat(),
        }
        inbox_dir = get_agent_inbox(captain)
        inbox_dir.mkdir(parents=True, exist_ok=True)
        verify_fp = inbox_dir / f"verify_{task_id}.json"
        verify_fp.write_text(json.dumps(verify_msg, indent=2), encoding="utf-8")

    return {"ok": True, "state": data.get("state")}


def process_fsm_update(agent: str, update_data: Dict[str, Any]) -> bool:
    """Process an FSM update from an agent."""
    try:
        # Validate update data
        required_fields = ['task_id', 'state', 'summary']
        for field in required_fields:
            if field not in update_data:
                logger.error(f"❌ Missing required field: {field}")
                return False
        
        # Write update to agent's inbox for FSM processing
        message = {
            "type": "fsm_update",
            "from": agent,
            "task_id": update_data['task_id'],
            "state": update_data['state'],
            "summary": update_data['summary'],
            "evidence": update_data.get('evidence', []),
            "timestamp": datetime.now().isoformat(),
            "workflow": update_data.get('workflow', 'default')
        }
        
        return _write_inbox_message(agent, message)
        
    except Exception as e:
        logger.error(f"❌ Failed to process FSM update: {e}")
        return False


def get_fsm_status(agent: str) -> Dict[str, Any]:
    """Get FSM status for a specific agent."""
    try:
        # Read recent messages from agent's inbox
        messages = _read_inbox_messages(agent, limit=20)
        
        # Filter for FSM-related messages
        fsm_messages = [msg for msg in messages if msg.get('type') in ['fsm_update', 'fsm_request']]
        
        # Get agent's current state
        state_file = get_agent_workspace(agent) / "state.json"
        current_state = {}
        if state_file.exists():
            try:
                current_state = json.loads(state_file.read_text(encoding='utf-8'))
            except Exception:
                pass
        
        return {
            "agent": agent,
            "current_state": current_state,
            "fsm_messages": fsm_messages,
            "last_update": current_state.get('updated', 'unknown'),
            "status": "active" if fsm_messages else "inactive"
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get FSM status for {agent}: {e}")
        return {"agent": agent, "error": str(e)}


def seed_fsm_tasks(owner: str, repo_root: Path = None) -> List[Dict[str, Any]]:
    """Seed FSM with tasks from repository TASK_LIST.md files."""
    try:
        # Scan repositories for tasks
        repo_tasks = _scan_repositories_for_tasks(repo_root)
        
        # Convert to FSM tasks
        fsm_tasks = []
        for task_data in repo_tasks:
            fsm_task = _create_fsm_task(owner, task_data, repo_root)
            fsm_tasks.append(fsm_task)
        
        # Write tasks to FSM inbox
        for task in fsm_tasks:
            message = {
                "type": "fsm_task_seed",
                "task": task,
                "timestamp": datetime.now().isoformat()
            }
            _write_inbox_message("Agent-5", message)  # Send to FSM orchestrator
        
        logger.info(f"✅ Seeded {len(fsm_tasks)} FSM tasks")
        return fsm_tasks
        
    except Exception as e:
        logger.error(f"❌ Failed to seed FSM tasks: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    logger.info("FSM Bridge module loaded")
    logger.info(f"FSM Root: {FSM_ROOT}")
    logger.info(f"Tasks Dir: {TASKS_DIR}")

