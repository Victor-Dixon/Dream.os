#!/usr/bin/env python3
"""
Technical Debt Base Classes - Modular V2 Compliance
====================================================

<!-- SSOT Domain: integration -->

Base classes and utilities for technical debt management commands.

V2 Compliant: Modular base classes
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TechnicalDebtBase:
    """Base class for technical debt command functionality."""

    def __init__(self):
        """Initialize base technical debt functionality."""
        self.debt_orchestrator = None
        self._initialize_orchestrator()

    def _initialize_orchestrator(self):
        """Initialize the technical debt orchestrator."""
        try:
            from systems.technical_debt.integration.orchestrator import TechnicalDebtIntegrationOrchestrator
            self.debt_orchestrator = TechnicalDebtIntegrationOrchestrator()
            logger.info("✅ Technical Debt Integration Orchestrator initialized")
        except ImportError as e:
            logger.warning(f"⚠️ Technical Debt integration not available: {e}")
            self.debt_orchestrator = None

    def _check_orchestrator_available(self) -> bool:
        """Check if the debt orchestrator is available."""
        if not self.debt_orchestrator:
            return False
        return True


class DebateBase:
    """Base class for debate functionality."""

    def __init__(self):
        """Initialize debate base functionality."""
        self.debates_dir = None
        self.active_debates = {}
        self._initialize_debate_system()

    def _initialize_debate_system(self):
        """Initialize the debate system."""
        try:
            import sys
            from pathlib import Path as PathLib
            project_root = PathLib(__file__).resolve().parents[4]
            self.debates_dir = project_root / "debates"
            self.debates_dir.mkdir(exist_ok=True)
            self._load_active_debates()
            logger.info("✅ Debate system initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize debate system: {e}")

    def _load_active_debates(self):
        """Load active debates from files."""
        try:
            for debate_file in self.debates_dir.glob("*.json"):
                try:
                    import json
                    from datetime import datetime

                    with open(debate_file, 'r', encoding='utf-8') as f:
                        debate_data = json.load(f)

                    debate_id = debate_data.get("debate_id")
                    deadline = debate_data.get("deadline")

                    # Check if debate is still active
                    if deadline:
                        from datetime import datetime
                        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                        if datetime.now().replace(tzinfo=deadline_dt.tzinfo) < deadline_dt:
                            self.active_debates[debate_id] = debate_data

                except Exception as e:
                    logger.warning(f"Failed to load debate {debate_file}: {e}")

            logger.info(f"Loaded {len(self.active_debates)} active debates")

        except Exception as e:
            logger.error(f"Error loading active debates: {e}")

    def _save_debate(self, debate_data: dict):
        """Save debate data to file."""
        try:
            debate_id = debate_data["debate_id"]
            debate_file = self.debates_dir / f"{debate_id}.json"

            import json
            with open(debate_file, 'w', encoding='utf-8') as f:
                json.dump(debate_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving debate {debate_data.get('debate_id')}: {e}")


__all__ = ["TechnicalDebtBase", "DebateBase"]