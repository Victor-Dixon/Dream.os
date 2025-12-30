#!/usr/bin/env python3

"""
<!-- SSOT Domain: logging -->

Speech Log Manager
==================

Manages logging of speech captions to:
- Devlogs
- Memory JSON
- Session context

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT

""""""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class SpeechLogManager:
    """
    Manages logging of speech captions to various destinations.

    Logs captions to:
    - Devlogs directory
    - Memory/session context
    - Agent inboxes (if task assignment)
    """

    def __init__(
        self,
        devlogs_path: str = "devlogs",
        memory_path: str = "swarm_brain/knowledge_base.json",
    ):
        """
        Initialize speech log manager.

        Args:
            devlogs_path: Path to devlogs directory
            memory_path: Path to memory/knowledge base JSON
        """
        self.devlogs_path = Path(devlogs_path)
        self.memory_path = Path(memory_path)
        self.devlogs_path.mkdir(parents=True, exist_ok=True)

    def log_caption(
        self,
        caption_text: str,
        interpreted: Optional[dict] = None,
        destination: str = "devlog",
    ) -> bool:
        """
        Log caption to specified destination.

        Args:
            caption_text: Caption text
            interpreted: Interpreted caption data (optional)
            destination: Destination type ("devlog", "memory", "both")

        Returns:
            True if logged successfully
        """
        success = True

        if destination in ["devlog", "both"]:
            success &= self._log_to_devlog(caption_text, interpreted)

        if destination in ["memory", "both"]:
            success &= self._log_to_memory(caption_text, interpreted)

        return success

    def _log_to_devlog(self, caption_text: str, interpreted: Optional[dict]) -> bool:
        """
        Log caption to devlog file.

        Args:
            caption_text: Caption text
            interpreted: Interpreted data

        Returns:
            True if logged successfully
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}_speech_caption.md"
            filepath = self.devlogs_path / filename

            content = self._format_devlog(caption_text, interpreted)

            filepath.write_text(content, encoding="utf-8")
            logger.info(f"📝 Logged caption to devlog: {filename}")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to log to devlog: {e}")
            return False

    def _format_devlog(self, caption_text: str, interpreted: Optional[dict]) -> str:
        """
        Format devlog entry for caption.

        Args:
            caption_text: Caption text
            interpreted: Interpreted data

        Returns:
            Formatted devlog content
        """
        lines = [
            "# 🎤 Speech Caption Log",
            "",
            f"**Timestamp:** {datetime.now().isoformat()}",
            "",
            "## Caption Text",
            "",
            f"> {caption_text}",
            "",
        ]

        if interpreted:
            lines.extend([
                "## Interpretation",
                "",
                f"- **Intent:** {interpreted.get('intent', 'unknown')}",
                f"- **Target Agents:** {', '.join(interpreted.get('target_agents', []))}",
                f"- **Action Type:** {interpreted.get('action_type', 'unknown')}",
                f"- **Confidence:** {interpreted.get('confidence', 0.0):.2f}",
                "",
            ])

        lines.append("---")
        lines.append("*Logged by Speech Log Manager*")

        return "\n".join(lines)

    def _log_to_memory(
        self, caption_text: str, interpreted: Optional[dict]
    ) -> bool:
        """
        Log caption to memory/knowledge base.

        Args:
            caption_text: Caption text
            interpreted: Interpreted data

        Returns:
            True if logged successfully
        """
        try:
            # Load existing memory
            memory_data = {}
            if self.memory_path.exists():
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    memory_data = json.load(f)

            # Initialize speech_logs if not present
            if "speech_logs" not in memory_data:
                memory_data["speech_logs"] = []

            # Add new entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "caption": caption_text,
                "interpreted": interpreted or {},
            }

            memory_data["speech_logs"].append(entry)

            # Keep only last 100 entries
            memory_data["speech_logs"] = memory_data["speech_logs"][-100:]

            # Save memory
            self.memory_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(memory_data, f, indent=2)

            logger.info("💾 Logged caption to memory")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to log to memory: {e}")
            return False

    def get_recent_captions(self, limit: int = 10) -> list[dict]:
        """
        Get recent caption entries from memory.

        Args:
            limit: Number of entries to return

        Returns:
            List of caption entries
        """
        try:
            if not self.memory_path.exists():
                return []

            with open(self.memory_path, "r", encoding="utf-8") as f:
                memory_data = json.load(f)

            speech_logs = memory_data.get("speech_logs", [])
            return speech_logs[-limit:]

        except Exception as e:
            logger.error(f"❌ Failed to get recent captions: {e}")
            return []


__all__ = ["SpeechLogManager"]




