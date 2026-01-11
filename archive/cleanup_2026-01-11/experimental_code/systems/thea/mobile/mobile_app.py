"""Simplified mobile application layer with offline persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .mobile_features import MobileFeatureManager, VoiceTask, LocationReminder, QuestProgress


class MobileApp:
    """Mobile wrapper providing basic offline storage."""

    def __init__(self, storage_path: str = "data/mobile_state.json") -> None:
        self.storage_path = Path(storage_path)
        self.manager = MobileFeatureManager()
        self.load_state()

    def load_state(self) -> None:
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text())
            for task_text in data.get("tasks", []):
                self.manager.add_task_from_voice(task_text)
            for rem in data.get("reminders", []):
                self.manager.add_location_reminder(tuple(rem["loc"]), rem["radius"], rem["msg"])
            for quest in data.get("quests", []):
                q = self.manager.track_quest(quest["name"], 0)
                q.progress = quest["progress"]
                q.target = quest.get("target", q.target)

    def save_state(self) -> None:
        tasks = [t.text for t in self.manager.tasks]
        reminders = [{"loc": r.location, "radius": r.radius_meters, "msg": r.message} for r in self.manager.reminders]
        quests = [{"name": q.name, "progress": q.progress, "target": q.target} for q in self.manager.quests]
        data = {"tasks": tasks, "reminders": reminders, "quests": quests}
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.storage_path.write_text(json.dumps(data, indent=2))

    def add_voice_task(self, transcript: str) -> VoiceTask:
        task = self.manager.add_task_from_voice(transcript)
        self.save_state()
        return task

    def add_reminder(self, location: tuple[float, float], radius: float, message: str) -> LocationReminder:
        reminder = self.manager.add_location_reminder(location, radius, message)
        self.save_state()
        return reminder

    def update_location(self, location: tuple[float, float]) -> list[str]:
        messages = self.manager.update_location(location)
        if messages:
            self.save_state()
        return messages

    def progress_quest(self, name: str, inc: int = 1) -> QuestProgress:
        quest = self.manager.track_quest(name, inc)
        self.save_state()
        return quest
