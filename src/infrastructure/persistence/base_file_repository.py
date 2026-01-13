"""
Base File Repository - Abstract Base Class for File-Based Repositories
======================================================================

Abstract base class consolidating common file I/O patterns for file-based repositories.
Reduces code duplication across ContractRepository, MessageRepository, ActivityRepository, etc.

<!-- SSOT Domain: infrastructure -->

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any


class BaseFileRepository(ABC):
    """
    Abstract base class for file-based repositories.
    
    Provides common file I/O operations:
    - File initialization
    - JSON loading/saving
    - Error handling
    - Metadata management
    
    Subclasses should implement:
    - _get_default_data() - Return default data structure
    - _get_data_key() - Return key for data array in JSON
    """

    def __init__(self, file_path: str | Path):
        """
        Initialize file repository.
        
        Args:
            file_path: Path to JSON file for storage
        """
        self.file_path = Path(file_path)
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Ensure file exists with proper structure."""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            default_data = self._get_default_data()
            self._save_data(default_data)

    @abstractmethod
    def _get_default_data(self) -> dict[str, Any]:
        """
        Get default data structure for new file.
        
        Returns:
            Dictionary with default structure including metadata
        """
        pass

    @abstractmethod
    def _get_data_key(self) -> str:
        """
        Get key for data array in JSON structure.
        
        Returns:
            Key name (e.g., "contracts", "messages", "activity_logs")
        """
        pass

    def _load_data(self) -> dict[str, Any]:
        """
        Load data from file.
        
        Returns:
            Data dictionary from file, or default if file doesn't exist/corrupted
        """
        try:
            with open(self.file_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            # Return default structure if file is corrupted or missing
            return self._get_default_data()

    def _save_data(self, data: dict[str, Any]) -> bool:
        """
        Save data to file.
        
        Args:
            data: Data dictionary to save
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def _update_metadata(self, data: dict[str, Any]) -> None:
        """
        Update metadata in data structure.
        
        Args:
            data: Data dictionary to update
        """
        if "metadata" not in data:
            data["metadata"] = {}
        
        data["metadata"]["version"] = data["metadata"].get("version", "1.0")
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        if "created_at" not in data["metadata"]:
            data["metadata"]["created_at"] = datetime.now().isoformat()

    def _get_items(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Get items array from data structure.
        
        Args:
            data: Data dictionary
            
        Returns:
            List of items
        """
        data_key = self._get_data_key()
        return data.get(data_key, [])

    def _set_items(self, data: dict[str, Any], items: list[dict[str, Any]]) -> None:
        """
        Set items array in data structure.
        
        Args:
            data: Data dictionary to update
            items: List of items to set
        """
        data_key = self._get_data_key()
        data[data_key] = items

    def _add_item(self, item: dict[str, Any]) -> bool:
        """
        Add item to repository.
        
        Args:
            item: Item dictionary to add
            
        Returns:
            True if add successful, False otherwise
        """
        data = self._load_data()
        items = self._get_items(data)
        
        # Add timestamp if not present
        if "timestamp" not in item and "created_at" not in item:
            item["created_at"] = datetime.now().isoformat()
        
        items.append(item)
        self._set_items(data, items)
        self._update_metadata(data)
        
        return self._save_data(data)

    def _find_item(self, predicate: callable) -> dict[str, Any] | None:
        """
        Find item matching predicate.
        
        Args:
            predicate: Function that takes item and returns bool
            
        Returns:
            First matching item or None
        """
        items = self._get_items(self._load_data())
        for item in items:
            if predicate(item):
                return item
        return None

    def _update_item(self, predicate: callable, updates: dict[str, Any]) -> bool:
        """
        Update item matching predicate.
        
        Args:
            predicate: Function that takes item and returns bool
            updates: Dictionary of updates to apply
            
        Returns:
            True if update successful, False if item not found
        """
        data = self._load_data()
        items = self._get_items(data)
        
        updated = False
        for item in items:
            if predicate(item):
                item.update(updates)
                item["updated_at"] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            self._set_items(data, items)
            self._update_metadata(data)
            return self._save_data(data)
        
        return False

    def _delete_item(self, predicate: callable) -> bool:
        """
        Delete item matching predicate.
        
        Args:
            predicate: Function that takes item and returns bool
            
        Returns:
            True if delete successful, False if item not found
        """
        data = self._load_data()
        items = self._get_items(data)
        
        original_count = len(items)
        items = [item for item in items if not predicate(item)]
        
        if len(items) < original_count:
            self._set_items(data, items)
            self._update_metadata(data)
            return self._save_data(data)
        
        return False

    def _filter_items(self, predicate: callable) -> list[dict[str, Any]]:
        """
        Filter items matching predicate.
        
        Args:
            predicate: Function that takes item and returns bool
            
        Returns:
            List of matching items
        """
        items = self._get_items(self._load_data())
        return [item for item in items if predicate(item)]

    def _sort_items(self, items: list[dict[str, Any]], key: str, reverse: bool = True) -> list[dict[str, Any]]:
        """
        Sort items by key.
        
        Args:
            items: List of items to sort
            key: Key to sort by (e.g., "timestamp", "created_at")
            reverse: Sort in reverse order (default: True, newest first)
            
        Returns:
            Sorted list of items
        """
        return sorted(items, key=lambda x: x.get(key, ""), reverse=reverse)

    def _limit_items(self, items: list[dict[str, Any]], limit: int | None) -> list[dict[str, Any]]:
        """
        Limit number of items.
        
        Args:
            items: List of items
            limit: Maximum number of items (None for no limit)
            
        Returns:
            Limited list of items
        """
        if limit is None:
            return items
        return items[:limit]

