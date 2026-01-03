"""
context_manager.py

This module defines the ContextManager class, which provides persistent memory storage
for AI agents. It allows storing and retrieving context (e.g., past interactions) for a project,
to enable context-aware responses. A global instance (`global_context`) is provided for
easy integration across the project.
"""

import os
import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger("ContextManager")
logger.setLevel(logging.DEBUG)

class ContextManager:
    def __init__(self, memory_file: str = "context_memory.json"):
        """
        Initializes the ContextManager by loading existing memory from disk or starting fresh.

        Args:
            memory_file (str): Path to the JSON file for persisting context.
        """
        self.memory_file = memory_file
        self.memory: Dict[str, List[Dict[str, str]]] = self._load_memory()

    def _load_memory(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Loads the memory data from the JSON file.

        Returns:
            Dict[str, List[Dict[str, str]]]: A dictionary mapping project names to a list of interactions.
        """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"Loaded context memory from {self.memory_file}")
                return data if isinstance(data, dict) else {}
            except Exception as e:
                logger.error(f"Failed to load memory file '{self.memory_file}': {e}")
        return {}

    def _save_memory(self) -> None:
        """
        Persists the current memory data to the JSON file.
        """
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4)
            logger.info(f"Context memory saved to {self.memory_file}")
        except Exception as e:
            logger.error(f"Failed to save memory file '{self.memory_file}': {e}")

    def store_memory(self, project: str, user_input: str, ai_response: str) -> None:
        """
        Stores an interaction in memory for a given project.

        Args:
            project (str): The project or domain name.
            user_input (str): The user's input.
            ai_response (str): The AI's response.
        """
        if project not in self.memory:
            self.memory[project] = []
        self.memory[project].append({
            "user_input": user_input,
            "ai_response": ai_response
        })
        self._save_memory()
        logger.info(f"Stored memory for project '{project}'.")

    def retrieve_memory(self, project: str, limit: int = 5) -> str:
        """
        Retrieves the most recent interactions for a project.

        Args:
            project (str): The project to retrieve memory for.
            limit (int): Maximum number of interactions to return.

        Returns:
            str: A formatted string of the recent interactions, or an empty string if none exist.
        """
        if project in self.memory:
            interactions = self.memory[project][-limit:]
            memory_context = "\n".join(
                f"User: {entry['user_input']}\nAI: {entry['ai_response']}"
                for entry in interactions
            )
            return memory_context
        return ""

    def clear_memory(self, project: str) -> None:
        """
        Clears all stored memory for a given project.

        Args:
            project (str): The project whose memory should be cleared.
        """
        if project in self.memory:
            del self.memory[project]
            self._save_memory()
            logger.info(f"Cleared memory for project '{project}'.")

# Global instance for use across the project
global_context = ContextManager()
