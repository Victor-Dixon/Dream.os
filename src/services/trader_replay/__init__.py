"""
Trader Replay Journal Service
==============================

Dream.OS integrated trading replay and journaling system.
Provides interactive market replay training with agent integration.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: Service pattern with orchestrator, repository, models
Author: Agent-3 (Infrastructure & DevOps Specialist) with Agent-5 (Business Intelligence)
License: MIT
"""

from .trader_replay_orchestrator import TraderReplayOrchestrator
from .models import (
    ReplaySession,
    ReplaySessionStatus,
    PaperTrade,
    JournalEntry,
    BehavioralScore,
    Candle,
    TradeSide,
    TradeStatus,
    JournalEntryType,
)
from .replay_engine import ReplayEngine, ReplayState
from .repositories import (
    SessionRepository,
    TradeRepository,
    JournalRepository,
    ScoreRepository,
)
from .behavioral_scoring import BehavioralScorer

__all__ = [
    "TraderReplayOrchestrator",
    "ReplaySession",
    "ReplaySessionStatus",
    "PaperTrade",
    "JournalEntry",
    "BehavioralScore",
    "Candle",
    "TradeSide",
    "TradeStatus",
    "JournalEntryType",
    "ReplayEngine",
    "ReplayState",
    "SessionRepository",
    "TradeRepository",
    "JournalRepository",
    "ScoreRepository",
    "BehavioralScorer",
]

