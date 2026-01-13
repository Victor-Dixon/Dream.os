"""
Tests for behavioral_scoring.py - BehavioralScorer class.

Target: Golden test fixtures validate scoring algorithms
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from src.services.trader_replay.behavioral_scoring import BehavioralScorer
from src.services.trader_replay.repositories import TradeRepository
from src.services.trader_replay.replay_engine import ReplayEngine
from src.services.trader_replay.models import PaperTrade, TradeSide, TradeStatus
from tests.fixtures.trader_replay import (
    create_disciplined_session_fixture,
    create_chaotic_session_fixture,
)


class TestBehavioralScoring:
    """Test BehavioralScorer class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)
        yield db_path
        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def trade_repository(self, temp_db):
        """Create TradeRepository instance."""
        return TradeRepository(temp_db)

    @pytest.fixture
    def scorer(self, trade_repository):
        """Create BehavioralScorer instance."""
        return BehavioralScorer(trade_repository)

    @pytest.fixture
    def disciplined_session(self, temp_db):
        """Create disciplined session with trades."""
        fixture = create_disciplined_session_fixture()
        engine = ReplayEngine(temp_db)
        
        session_id = engine.create_session(
            symbol=fixture["symbol"],
            session_date=fixture["session_date"],
            timeframe=fixture["timeframe"],
            candles=fixture["candles"],
        )

        # Insert trades
        trade_repo = TradeRepository(temp_db)
        for trade_data in fixture["trades"]:
            trade = PaperTrade(
                session_id=session_id,
                entry_timestamp=datetime.fromisoformat(trade_data["entry_timestamp"]),
                exit_timestamp=datetime.fromisoformat(trade_data["exit_timestamp"]) if trade_data.get("exit_timestamp") else None,
                entry_price=trade_data["entry_price"],
                exit_price=trade_data.get("exit_price"),
                quantity=trade_data["quantity"],
                side=TradeSide(trade_data["side"]),
                entry_type=trade_data["entry_type"],
                stop_loss=trade_data.get("stop_loss"),
                take_profit=trade_data.get("take_profit"),
                pnl=trade_data.get("pnl"),
                r_multiple=trade_data.get("r_multiple"),
                status=TradeStatus(trade_data["status"]),
            )
            trade_repo.create(trade)

        return session_id, fixture["expected_scores"]

    @pytest.fixture
    def chaotic_session(self, temp_db):
        """Create chaotic session with trades."""
        fixture = create_chaotic_session_fixture()
        engine = ReplayEngine(temp_db)
        
        session_id = engine.create_session(
            symbol=fixture["symbol"],
            session_date=fixture["session_date"],
            timeframe=fixture["timeframe"],
            candles=fixture["candles"],
        )

        # Insert trades
        trade_repo = TradeRepository(temp_db)
        for trade_data in fixture["trades"]:
            trade = PaperTrade(
                session_id=session_id,
                entry_timestamp=datetime.fromisoformat(trade_data["entry_timestamp"]),
                exit_timestamp=datetime.fromisoformat(trade_data["exit_timestamp"]) if trade_data.get("exit_timestamp") else None,
                entry_price=trade_data["entry_price"],
                exit_price=trade_data.get("exit_price"),
                quantity=trade_data["quantity"],
                side=TradeSide(trade_data["side"]),
                entry_type=trade_data["entry_type"],
                stop_loss=trade_data.get("stop_loss"),
                take_profit=trade_data.get("take_profit"),
                pnl=trade_data.get("pnl"),
                r_multiple=trade_data.get("r_multiple"),
                status=TradeStatus(trade_data["status"]),
            )
            trade_repo.create(trade)

        return session_id, fixture["expected_scores"]

    def test_stop_integrity_score_disciplined(self, scorer, disciplined_session):
        """Test stop integrity score on disciplined session."""
        session_id, expected_scores = disciplined_session
        score = scorer.calculate_stop_integrity_score(session_id, scorer.trade_repository.list_by_session(session_id))

        min_score, max_score = expected_scores["stop_integrity"]
        assert min_score <= score.score_value <= max_score, \
            f"Stop integrity score {score.score_value} not in expected range [{min_score}, {max_score}]"
        assert score.score_type == "stop_integrity"
        assert "total_trades" in score.details

    def test_stop_integrity_score_chaotic(self, scorer, chaotic_session):
        """Test stop integrity score on chaotic session (should be low)."""
        session_id, expected_scores = chaotic_session
        score = scorer.calculate_stop_integrity_score(session_id, scorer.trade_repository.list_by_session(session_id))

        min_score, max_score = expected_scores["stop_integrity"]
        assert min_score <= score.score_value <= max_score, \
            f"Stop integrity score {score.score_value} not in expected range [{min_score}, {max_score}]"
        assert score.score_type == "stop_integrity"

    def test_patience_score_disciplined(self, scorer, disciplined_session):
        """Test patience score on disciplined session (should be high)."""
        session_id, expected_scores = disciplined_session
        score = scorer.calculate_patience_score(session_id, scorer.trade_repository.list_by_session(session_id))

        min_score, max_score = expected_scores["patience"]
        assert min_score <= score.score_value <= max_score, \
            f"Patience score {score.score_value} not in expected range [{min_score}, {max_score}]"
        assert score.score_type == "patience"

    def test_patience_score_chaotic(self, scorer, chaotic_session):
        """Test patience score on chaotic session (should be low due to overtrading)."""
        session_id, expected_scores = chaotic_session
        score = scorer.calculate_patience_score(session_id, scorer.trade_repository.list_by_session(session_id))

        min_score, max_score = expected_scores["patience"]
        assert min_score <= score.score_value <= max_score, \
            f"Patience score {score.score_value} not in expected range [{min_score}, {max_score}]"
        assert score.score_type == "patience"

    def test_disciplined_scores_higher_than_chaotic(self, scorer, disciplined_session, chaotic_session):
        """Test that disciplined session scores higher than chaotic session."""
        disciplined_id, _ = disciplined_session
        chaotic_id, _ = chaotic_session

        disciplined_trades = scorer.trade_repository.list_by_session(disciplined_id)
        chaotic_trades = scorer.trade_repository.list_by_session(chaotic_id)

        # Compare scores
        disciplined_stop = scorer.calculate_stop_integrity_score(disciplined_id, disciplined_trades)
        chaotic_stop = scorer.calculate_stop_integrity_score(chaotic_id, chaotic_trades)

        disciplined_patience = scorer.calculate_patience_score(disciplined_id, disciplined_trades)
        chaotic_patience = scorer.calculate_patience_score(chaotic_id, chaotic_trades)

        assert disciplined_stop.score_value > chaotic_stop.score_value, \
            f"Disciplined stop integrity ({disciplined_stop.score_value}) should be > chaotic ({chaotic_stop.score_value})"

        assert disciplined_patience.score_value > chaotic_patience.score_value, \
            f"Disciplined patience ({disciplined_patience.score_value}) should be > chaotic ({chaotic_patience.score_value})"

    def test_calculate_all_scores(self, scorer, disciplined_session):
        """Test calculate_all_scores returns all score types."""
        session_id, _ = disciplined_session
        scores = scorer.calculate_all_scores(session_id)

        assert len(scores) == 4
        score_types = {s.score_type for s in scores}
        assert score_types == {
            "stop_integrity",
            "patience",
            "risk_discipline",
            "rule_adherence",
        }

        # All scores should be 0-100
        for score in scores:
            assert 0 <= score.score_value <= 100



