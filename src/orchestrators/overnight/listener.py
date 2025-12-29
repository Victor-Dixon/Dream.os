#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Overnight Listener - V2 Compliant
==================================

Monitors agent inboxes, processes messages, updates state, and handles FSM updates.

Extracted from V1 overnight_runner/listener.py and adapted for V2 compliance.

V2 Compliance: ≤400 lines, proper imports, error handling
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from src.core.config.timeout_constants import TimeoutConstants

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


def _load_env_file(path: Optional[str] = None) -> None:
    """Load environment variables from .env file."""
    if not path:
        # Try default .env at repo root
        env_file = ROOT_DIR / ".env"
        if not env_file.exists():
            return
        path = str(env_file)
    
    try:
        env_path = Path(path)
        if not env_path.exists():
            return
        
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            os.environ[k] = v
    except Exception as e:
        logger.warning(f"Failed to load env file {path}: {e}")


def _post_discord(webhook: Optional[str], username: str, use_embed: bool, title: str, description: str) -> None:
    """Post message to Discord webhook."""
    if not webhook:
        return
    
    try:
        import urllib.request as request
        import urllib.error as error
        
        payload: Dict[str, Any] = {"username": username}
        if use_embed:
            payload["embeds"] = [{"title": title, "description": description, "color": 5814783}]
        else:
            payload["content"] = f"**{title}**\n{description}"
        
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(webhook, data=data, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=TimeoutConstants.HTTP_QUICK):
            pass
    except Exception as e:
        logger.debug(f"Discord post failed: {e}")


class OvernightListener:
    """V2-compliant listener for monitoring agent inboxes."""
    
    def __init__(
        self,
        agent_id: str,
        inbox_dir: Optional[Path] = None,
        poll_interval: float = 0.2,
        devlog_webhook: Optional[str] = None,
        devlog_username: str = "Agent Devlog",
        devlog_embed: bool = False,
    ):
        """Initialize listener."""
        self.agent_id = agent_id
        self.inbox_dir = inbox_dir or get_agent_inbox(agent_id)
        self.poll_interval = poll_interval
        self.devlog_webhook = devlog_webhook
        self.devlog_username = devlog_username
        self.devlog_embed = devlog_embed
        
        # State management
        self.workspace = get_agent_workspace(agent_id)
        self.state_path = self.workspace / "state.json"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        
        # Processed files tracking
        self.processed_dir = self.inbox_dir / "processed"
        self.processed_dir.mkdir(exist_ok=True)
        
        self.is_running = False
        self.logger = get_logger(__name__)
    
    def load_state(self) -> Dict[str, Any]:
        """Load agent state from state.json."""
        try:
            if self.state_path.exists():
                return json.loads(self.state_path.read_text(encoding="utf-8"))
        except Exception as e:
            self.logger.warning(f"Failed to load state: {e}")
        return {"state": "idle"}
    
    def save_state(self, data: Dict[str, Any]) -> None:
        """Save agent state to state.json."""
        try:
            self.state_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
    
    def _now(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    def _process_message(self, data: Dict[str, Any]) -> None:
        """Process a single message."""
        self.logger.info(f"[INBOX] {self.agent_id} <- {json.dumps(data, ensure_ascii=False)}")
        
        # Load current state
        st = self.load_state()
        msg_type = str(data.get("type", "")).lower()
        
        # Check TTL if provided
        ttl_s = data.get("ttl_s")
        created_at = data.get("created_at")
        if isinstance(ttl_s, (int, float)) and created_at:
            try:
                created = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
                age = (datetime.now() - created).total_seconds()
                if age > float(ttl_s):
                    self.logger.debug(f"Message expired (age: {age}s > ttl: {ttl_s}s)")
                    return
            except Exception:
                pass
        
        # Update state based on message type
        next_state = st.get("state", "idle")
        if msg_type == "task":
            next_state = "executing"
        elif msg_type == "sync":
            next_state = "syncing"
        elif msg_type == "verify":
            next_state = "verifying"
        elif msg_type == "resume":
            next_state = "ready"
        elif msg_type in ("ack", "note", "ui_request"):
            next_state = st.get("state", "idle")
        
        # Update state
        st.update({
            "last_message": data,
            "state": next_state,
            "updated": self._now(),
            "schema_version": data.get("schema_version", 1),
        })
        self.save_state(st)
        
        # Handle FSM updates
        if msg_type in ("fsm_update", "verify") and st.get("state") in ("done", "completed", "ready"):
            self._emit_resume_signal()
        
        # Handle UI requests
        if msg_type == "ui_request":
            self._emit_ui_signal(data)
        
        # Update contracts if task_id present
        if "task_id" in data:
            self._update_contracts(data)
        
        # Post to Discord if configured
        if self.devlog_webhook:
            self._post_devlog(data, st)
    
    def _emit_resume_signal(self) -> None:
        """Emit resume signal for runner."""
        try:
            signal_root = ROOT_DIR / "communications" / "_signals"
            signal_root.mkdir(parents=True, exist_ok=True)
            signal_file = signal_root / f"resume_now_{self.agent_id}.signal"
            signal_file.write_text(self._now(), encoding="utf-8")
        except Exception as e:
            self.logger.debug(f"Failed to emit resume signal: {e}")
    
    def _emit_ui_signal(self, data: Dict[str, Any]) -> None:
        """Emit UI request signal."""
        try:
            signal_root = ROOT_DIR / "communications" / "_signals"
            signal_root.mkdir(parents=True, exist_ok=True)
            
            ui_sig = {
                "agent": self.agent_id,
                "intent": data.get("intent") or "open_new_chat_and_check_inbox",
                "task_id": data.get("task_id"),
                "message": data.get("payload", {}).get("message") if isinstance(data.get("payload"), dict) else data.get("message"),
                "created_at": self._now(),
            }
            
            signal_file = signal_root / f"ui_request_{self.agent_id}.json"
            signal_file.write_text(json.dumps(ui_sig, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            self.logger.debug(f"Failed to emit UI signal: {e}")
    
    def _update_contracts(self, data: Dict[str, Any]) -> None:
        """Update contracts file and TASK_LIST.md."""
        try:
            comms_root = ROOT_DIR / "communications"
            if not comms_root.exists():
                return
            
            # Find latest overnight_* folder
            candidates = sorted([p for p in comms_root.iterdir() if p.is_dir() and p.name.startswith("overnight_")])
            if not candidates:
                return
            
            latest = candidates[-1]
            agent_dir = latest / self.agent_id
            contracts_path = agent_dir / "FSM_CONTRACTS" / "contracts.json"
            if not contracts_path.exists():
                contracts_path = agent_dir / "contracts.json"
            
            if contracts_path.exists():
                try:
                    contracts = json.loads(contracts_path.read_text(encoding="utf-8"))
                except Exception:
                    contracts = []
                
                # Update or add contract
                updated = False
                target_repo_path = data.get("repo_path")
                
                for contract in contracts:
                    if isinstance(contract, dict) and contract.get("task_id") == data.get("task_id"):
                        if "state" in data:
                            contract["state"] = data["state"]
                        if "evidence" in data:
                            existing = contract.get("evidence", [])
                            new_ev = data["evidence"] if isinstance(data["evidence"], list) else [data["evidence"]]
                            contract["evidence"] = existing + new_ev
                        target_repo_path = contract.get("repo_path")
                        contract["updated"] = self._now()
                        updated = True
                        break
                
                if not updated:
                    entry = {k: v for k, v in data.items() if k in ("task_id", "state", "summary", "evidence", "repo_path")}
                    entry["updated"] = self._now()
                    contracts.append(entry)
                
                contracts_path.parent.mkdir(parents=True, exist_ok=True)
                contracts_path.write_text(json.dumps(contracts, ensure_ascii=False, indent=2), encoding="utf-8")
                
                # Patch TASK_LIST.md
                if target_repo_path and isinstance(target_repo_path, str) and "state" in data:
                    self._patch_task_list(Path(target_repo_path), data)
        except Exception as e:
            self.logger.debug(f"Failed to update contracts: {e}")
    
    def _patch_task_list(self, repo_path: Path, data: Dict[str, Any]) -> None:
        """Patch TASK_LIST.md with state badge."""
        try:
            task_list = repo_path / "TASK_LIST.md"
            if not task_list.exists():
                return
            
            lines = task_list.read_text(encoding="utf-8").splitlines()
            new_lines = []
            found = False
            summary = data.get("summary", "")
            state = data.get("state", "")
            
            for line in lines:
                if not found and line.strip().startswith("- [") and summary and summary in line:
                    found = True
                    if "(state:" in line:
                        newline = re.sub(r"\(state:[^)]+\)", f"(state: {state})", line)
                    else:
                        newline = f"{line} (state: {state})"
                    new_lines.append(newline)
                else:
                    new_lines.append(line)
            
            if found:
                task_list.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        except Exception as e:
            self.logger.debug(f"Failed to patch TASK_LIST.md: {e}")
    
    def _post_devlog(self, data: Dict[str, Any], state: Dict[str, Any]) -> None:
        """Post devlog to Discord."""
        try:
            msg_type = str(data.get("type", "")).lower()
            task_id = data.get("task_id") or ""
            repo_path = data.get("repo_path") or ""
            summary = data.get("summary") or data.get("message") or ""
            state_str = data.get("state") or state.get("state") or ""
            
            title = f"{self.agent_id} {msg_type.upper()} {task_id}".strip()
            desc_parts = []
            
            if state_str:
                desc_parts.append(f"state: {state_str}")
            if summary:
                desc_parts.append(f"summary: {summary}")
            if repo_path:
                desc_parts.append(f"repo: {repo_path}")
            if "evidence" in data:
                ev = data["evidence"]
                if isinstance(ev, list):
                    desc_parts.append("evidence: " + "; ".join(map(str, ev))[:900])
            
            description = " | ".join(desc_parts) or json.dumps(data)[:1000]
            _post_discord(self.devlog_webhook, self.devlog_username, self.devlog_embed, title, description)
        except Exception as e:
            self.logger.debug(f"Failed to post devlog: {e}")
    
    def process_inbox(self) -> int:
        """Process all new files in inbox."""
        if not self.inbox_dir.exists():
            return 0
        
        processed_count = 0
        
        # Process JSON files
        for filepath in sorted(self.inbox_dir.glob("*.json")):
            try:
                data = json.loads(filepath.read_text(encoding="utf-8"))
                self._process_message(data)
                
                # Move to processed
                processed_file = self.processed_dir / filepath.name
                filepath.rename(processed_file)
                processed_count += 1
            except Exception as e:
                self.logger.warning(f"Failed to process {filepath.name}: {e}")
        
        # Process markdown files (inbox messages)
        for filepath in sorted(self.inbox_dir.glob("*.md")):
            try:
                # Extract metadata from markdown
                content = filepath.read_text(encoding="utf-8")
                # Simple extraction - can be enhanced
                if "CAPTAIN MESSAGE" in content or "INBOX MESSAGE" in content:
                    data = {
                        "type": "text",
                        "content": content,
                        "timestamp": self._now(),
                    }
                    self._process_message(data)
                    
                    # Move to processed
                    processed_file = self.processed_dir / filepath.name
                    filepath.rename(processed_file)
                    processed_count += 1
            except Exception as e:
                self.logger.warning(f"Failed to process {filepath.name}: {e}")
        
        return processed_count
    
    def start(self) -> None:
        """Start listening."""
        self.is_running = True
        self.logger.info(f"Listening for {self.agent_id} inbox at: {self.inbox_dir}")
    
    def stop(self) -> None:
        """Stop listening."""
        self.is_running = False
        self.logger.info("Stopped inbox listener")
    
    def run(self) -> None:
        """Run listener loop."""
        self.start()
        try:
            while self.is_running:
                self.process_inbox()
                time.sleep(self.poll_interval)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()


def main() -> int:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser("overnight_listener")
    parser.add_argument("--agent", default="Agent-5", help="Agent ID to monitor")
    parser.add_argument("--inbox", help="Inbox directory path (optional)")
    parser.add_argument("--poll", type=float, default=0.2, help="Poll interval in seconds")
    parser.add_argument("--env-file", help="Path to .env file")
    parser.add_argument("--devlog-webhook", help="Discord webhook URL")
    parser.add_argument("--devlog-username", default="Agent Devlog", help="Discord username")
    parser.add_argument("--devlog-embed", action="store_true", help="Use embed format")
    
    args = parser.parse_args()
    
    # Load environment
    _load_env_file(args.env_file)
    
    # Get config
    config = get_unified_config()
    devlog_webhook = args.devlog_webhook or config.get_env("DISCORD_WEBHOOK_URL")
    devlog_username = args.devlog_username or config.get_env("DEVLOG_USERNAME", "Agent Devlog")
    
    # Create listener
    inbox_dir = Path(args.inbox) if args.inbox else None
    listener = OvernightListener(
        agent_id=args.agent,
        inbox_dir=inbox_dir,
        poll_interval=args.poll,
        devlog_webhook=devlog_webhook,
        devlog_username=devlog_username,
        devlog_embed=args.devlog_embed,
    )
    
    # Run
    listener.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

