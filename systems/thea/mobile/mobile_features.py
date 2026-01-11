"""Mobile-specific features for Dreamscape.
Includes voice-based task creation, location reminders, and quest tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple


@dataclass
class VoiceTask:
    """Task created from voice input."""

    text: str
    created_at: datetime = field(default_factory=datetime.now)
    completed: bool = False


@dataclass
class LocationReminder:
    """Location-based reminder."""

    location: Tuple[float, float]  # latitude, longitude
    radius_meters: float
    message: str
    triggered: bool = False


@dataclass
class QuestProgress:
    """Simple quest progress tracker."""

    name: str
    progress: int = 0
    target: int = 1

    def is_complete(self) -> bool:
        return self.progress >= self.target


class MobileFeatureManager:
    """Manage mobile-specific features."""

    def __init__(self) -> None:
        self.tasks: List[VoiceTask] = []
        self.reminders: List[LocationReminder] = []
        self.quests: List[QuestProgress] = []

    def add_task_from_voice(self, transcript: str) -> VoiceTask:
        """Create a task from transcribed voice input."""
        task = VoiceTask(text=transcript)
        self.tasks.append(task)
        return task

    def add_location_reminder(self, location: Tuple[float, float], radius_meters: float, message: str) -> LocationReminder:
        """Add a location-based reminder."""
        reminder = LocationReminder(location, radius_meters, message)
        self.reminders.append(reminder)
        return reminder

    def update_location(self, current_location: Tuple[float, float]) -> List[str]:
        """Check reminders against the current location and trigger messages."""
        triggered = []
        for reminder in self.reminders:
            if not reminder.triggered and self._within_radius(current_location, reminder.location, reminder.radius_meters):
                reminder.triggered = True
                triggered.append(reminder.message)
        return triggered

    def _within_radius(self, p1: Tuple[float, float], p2: Tuple[float, float], radius: float) -> bool:
        """Very rough distance check using Euclidean approximation."""
        lat_diff = p1[0] - p2[0]
        lon_diff = p1[1] - p2[1]
        return (lat_diff ** 2 + lon_diff ** 2) ** 0.5 <= radius / 111_000  # ~meters per degree

    def track_quest(self, name: str, increment: int = 1) -> QuestProgress:
        """Update or create quest progress."""
        quest = next((q for q in self.quests if q.name == name), None)
        if not quest:
            quest = QuestProgress(name=name, target=10)
            self.quests.append(quest)
        quest.progress += increment
        return quest
