# <!-- SSOT Domain: gaming -->
"""Data models for gaming integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


# IntegrationStatus - Redirect to SSOT
# SSOT: src/architecture/system_integration.py
from src.architecture.system_integration import IntegrationStatus


# Gaming Classes - Redirect to SSOT
# SSOT: src/gaming/models/gaming_models.py
from src.gaming.models.gaming_models import (
    GameType,
    GameSession,
    EntertainmentSystem,
)
