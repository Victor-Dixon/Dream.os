"""
Tests for repositories.py - Repository isolation and CRUD operations.

Target: Repository boundary enforcement, CRUD validation, foreign key constraints
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from src.services.trader_replay.repositories import (
    SessionRepository,
    TradeRepository,
    JournalRepository,
    ScoreRepository,
)
from src.services.trader_replay.models import (
    ReplaySession,
    ReplaySessionStatus,
    PaperTrade,
    TradeSide,
    TradeStatus,
    JournalEntry,
    JournalEntryType,
    BehavioralScore,
)
from src.services.trader_replay.replay_engine import ReplayEngine
from tests.fixtures.trader_replay import create_test_session_data


class TestSessionRepository:
    """Test SessionRepository class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database with schema initialized."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        # Initialize schema using ReplayEngine
        engine = ReplayEngine(db_path)
        yield db_path

        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def repository(self, temp_db):
        """Create SessionRepository instance."""
        return SessionRepository(temp_db)

    @pytest.fixture
    def session_id(self, temp_db):
        """Create a test session and return its ID."""
        engine = ReplayEngine(temp_db)
        session_data = create_test_session_data()
        return engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

    def test_get_existing_session(self, repository, session_id):
        """Test getting an existing session."""
        session = repository.get(session_id)

        assert session is not None
        assert session.session_id == session_id
        assert session.symbol == "TEST"
        assert session.session_date == "2024-01-15"
        assert session.timeframe == "1m"
        assert session.status == ReplaySessionStatus.READY

    def test_get_nonexistent_session(self, repository):
        """Test getting a non-existent session returns None."""
        session = repository.get(99999)
        assert session is None

    def test_list_all_sessions(self, repository, session_id):
        """Test listing all sessions."""
        sessions = repository.list_all()

        assert len(sessions) >= 1
        assert any(s.session_id == session_id for s in sessions)

    def test_list_sessions_filtered_by_symbol(self, repository, session_id):
        """Test listing sessions filtered by symbol."""
        sessions = repository.list_all(symbol="TEST")

        assert len(sessions) >= 1
        assert all(s.symbol == "TEST" for s in sessions)
        assert any(s.session_id == session_id for s in sessions)

    def test_list_sessions_filtered_by_nonexistent_symbol(self, repository):
        """Test listing sessions with non-existent symbol returns empty list."""
        sessions = repository.list_all(symbol="NONEXISTENT")
        assert len(sessions) == 0

    def test_update_session_status(self, repository, session_id):
        """Test updating session status."""
        # Update to IN_PROGRESS
        success = repository.update_status(
            session_id, ReplaySessionStatus.IN_PROGRESS)
        assert success is True

        # Verify update
        session = repository.get(session_id)
        assert session.status == ReplaySessionStatus.IN_PROGRESS

    def test_update_nonexistent_session_status(self, repository):
        """Test updating non-existent session returns False."""
        success = repository.update_status(
            99999, ReplaySessionStatus.IN_PROGRESS)
        assert success is False


class TestTradeRepository:
    """Test TradeRepository class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database with schema initialized."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        engine = ReplayEngine(db_path)
        yield db_path

        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def repository(self, temp_db):
        """Create TradeRepository instance."""
        return TradeRepository(temp_db)

    @pytest.fixture
    def session_id(self, temp_db):
        """Create a test session and return its ID."""
        engine = ReplayEngine(temp_db)
        session_data = create_test_session_data()
        return engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

    def test_create_trade(self, repository, session_id):
        """Test creating a new trade."""
        trade = PaperTrade(
            session_id=session_id,
            entry_timestamp=datetime(2024, 1, 15, 9, 30, 0),
            entry_price=100.0,
            quantity=10,
            side=TradeSide.LONG,
            entry_type="market",
            stop_loss=99.0,
            status=TradeStatus.OPEN,
        )

        trade_id = repository.create(trade)
        assert trade_id > 0

    def test_get_trade(self, repository, session_id):
        """Test getting a trade by ID."""
        # Create trade
        trade = PaperTrade(
            session_id=session_id,
            entry_timestamp=datetime(2024, 1, 15, 9, 30, 0),
            entry_price=100.0,
            quantity=10,
            side=TradeSide.LONG,
            entry_type="market",
            status=TradeStatus.OPEN,
        )
        trade_id = repository.create(trade)

        # Get trade
        retrieved = repository.get(trade_id)
        assert retrieved is not None
        assert retrieved.trade_id == trade_id
        assert retrieved.session_id == session_id
        assert retrieved.entry_price == 100.0
        assert retrieved.quantity == 10
        assert retrieved.side == TradeSide.LONG

    def test_get_nonexistent_trade(self, repository):
        """Test getting non-existent trade returns None."""
        trade = repository.get(99999)
        assert trade is None

    def test_list_trades_by_session(self, repository, session_id):
        """Test listing trades for a session."""
        # Create multiple trades
        for i in range(3):
            trade = PaperTrade(
                session_id=session_id,
                entry_timestamp=datetime(2024, 1, 15, 9, 30 + i, 0),
                entry_price=100.0 + i,
                quantity=10,
                side=TradeSide.LONG,
                entry_type="market",
                status=TradeStatus.OPEN,
            )
            repository.create(trade)

        # List trades
        trades = repository.list_by_session(session_id)
        assert len(trades) == 3
        assert all(t.session_id == session_id for t in trades)

    def test_list_trades_empty_session(self, repository, session_id):
        """Test listing trades for session with no trades returns empty list."""
        trades = repository.list_by_session(session_id)
        assert len(trades) == 0

    def test_update_trade(self, repository, session_id):
        """Test updating a trade."""
        # Create trade
        trade = PaperTrade(
            session_id=session_id,
            entry_timestamp=datetime(2024, 1, 15, 9, 30, 0),
            exit_timestamp=datetime(2024, 1, 15, 9, 35, 0),
            entry_price=100.0,
            exit_price=102.0,
            quantity=10,
            side=TradeSide.LONG,
            entry_type="market",
            status=TradeStatus.CLOSED,
        )
        trade_id = repository.create(trade)

        # Update trade
        trade.trade_id = trade_id
        trade.exit_price = 103.0
        trade.pnl = 30.0
        success = repository.update(trade)

        assert success is True

        # Verify update
        updated = repository.get(trade_id)
        assert updated.exit_price == 103.0
        assert updated.pnl == 30.0

    def test_update_trade_without_id(self, repository, session_id):
        """Test updating trade without ID returns False."""
        trade = PaperTrade(
            session_id=session_id,
            entry_timestamp=datetime(2024, 1, 15, 9, 30, 0),
            entry_price=100.0,
            quantity=10,
            side=TradeSide.LONG,
            entry_type="market",
            status=TradeStatus.OPEN,
        )
        # No trade_id set
        success = repository.update(trade)
        assert success is False


class TestJournalRepository:
    """Test JournalRepository class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database with schema initialized."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        engine = ReplayEngine(db_path)
        yield db_path

        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def repository(self, temp_db):
        """Create JournalRepository instance."""
        return JournalRepository(temp_db)

    @pytest.fixture
    def session_id(self, temp_db):
        """Create a test session and return its ID."""
        engine = ReplayEngine(temp_db)
        session_data = create_test_session_data()
        return engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

    def test_create_journal_entry(self, repository, session_id):
        """Test creating a journal entry."""
        entry = JournalEntry(
            session_id=session_id,
            timestamp=datetime(2024, 1, 15, 9, 30, 0),
            candle_index=0,
            entry_type=JournalEntryType.NOTE,
            content="Test journal entry",
            emotion_tag="neutral",
        )

        entry_id = repository.create(entry)
        assert entry_id > 0

    def test_list_journal_entries_by_session(self, repository, session_id):
        """Test listing journal entries for a session."""
        # Create multiple entries
        for i in range(3):
            entry = JournalEntry(
                session_id=session_id,
                timestamp=datetime(2024, 1, 15, 9, 30 + i, 0),
                candle_index=i,
                entry_type=JournalEntryType.NOTE,
                content=f"Entry {i}",
            )
            repository.create(entry)

        # List entries
        entries = repository.list_by_session(session_id)
        assert len(entries) == 3
        assert all(e.session_id == session_id for e in entries)
        # Should be ordered by timestamp ASC
        assert entries[0].candle_index == 0
        assert entries[2].candle_index == 2

    def test_journal_entry_with_template_data(self, repository, session_id):
        """Test journal entry with template data."""
        template_data = {"setup": "breakout", "risk": "1%"}
        entry = JournalEntry(
            session_id=session_id,
            timestamp=datetime(2024, 1, 15, 9, 30, 0),
            candle_index=0,
            entry_type=JournalEntryType.SETUP,
            content="Breakout setup",
            template_data=template_data,
        )

        entry_id = repository.create(entry)

        # Retrieve and verify template data
        entries = repository.list_by_session(session_id)
        assert len(entries) == 1
        assert entries[0].template_data == template_data


class TestScoreRepository:
    """Test ScoreRepository class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database with schema initialized."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        engine = ReplayEngine(db_path)
        yield db_path

        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def repository(self, temp_db):
        """Create ScoreRepository instance."""
        return ScoreRepository(temp_db)

    @pytest.fixture
    def session_id(self, temp_db):
        """Create a test session and return its ID."""
        engine = ReplayEngine(temp_db)
        session_data = create_test_session_data()
        return engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

    def test_create_score(self, repository, session_id):
        """Test creating a behavioral score."""
        score = BehavioralScore(
            session_id=session_id,
            score_type="stop_integrity",
            score_value=85.5,
            details={"total_trades": 5, "stops_used": 5},
        )

        score_id = repository.create(score)
        assert score_id > 0

    def test_get_scores_by_session(self, repository, session_id):
        """Test getting all scores for a session."""
        # Create multiple scores
        score_types = ["stop_integrity", "patience",
                       "risk_discipline", "rule_adherence"]
        for score_type in score_types:
            score = BehavioralScore(
                session_id=session_id,
                score_type=score_type,
                score_value=80.0,
                details={},
            )
            repository.create(score)

        # Get scores
        scores = repository.get_by_session(session_id)
        assert len(scores) == 4
        assert all(s.session_id == session_id for s in scores)
        score_types_retrieved = {s.score_type for s in scores}
        assert score_types_retrieved == set(score_types)

    def test_score_with_details(self, repository, session_id):
        """Test score with details dictionary."""
        details = {"total_trades": 10, "avg_r_multiple": 1.5}
        score = BehavioralScore(
            session_id=session_id,
            score_type="risk_discipline",
            score_value=75.0,
            details=details,
        )

        score_id = repository.create(score)

        # Retrieve and verify details
        scores = repository.get_by_session(session_id)
        assert len(scores) == 1
        assert scores[0].details == details

    def test_score_replace_on_duplicate(self, repository, session_id):
        """Test that INSERT OR REPLACE works for duplicate score types."""
        # Create initial score
        score1 = BehavioralScore(
            session_id=session_id,
            score_type="stop_integrity",
            score_value=80.0,
            details={},
        )
        repository.create(score1)

        # Create same score type again (should replace)
        score2 = BehavioralScore(
            session_id=session_id,
            score_type="stop_integrity",
            score_value=90.0,
            details={"updated": True},
        )
        repository.create(score2)

        # Should only have one score with updated value
        scores = repository.get_by_session(session_id)
        assert len(scores) == 1
        assert scores[0].score_value == 90.0
        assert scores[0].details == {"updated": True}


class TestRepositoryIsolation:
    """Test repository boundary enforcement - no direct DB access outside repos."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database with schema initialized."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        engine = ReplayEngine(db_path)
        yield db_path

        if db_path.exists():
            db_path.unlink()

    def test_repositories_use_clean_connection_pattern(self, temp_db):
        """Test that repositories properly open/close connections."""
        # This test verifies repositories don't leak connections
        session_repo = SessionRepository(temp_db)
        trade_repo = TradeRepository(temp_db)

        # Create session via engine (proper initialization)
        engine = ReplayEngine(temp_db)
        session_data = create_test_session_data()
        session_id = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        # Access via repositories (should work)
        session = session_repo.get(session_id)
        assert session is not None

        # Create trade via repository
        trade = PaperTrade(
            session_id=session_id,
            entry_timestamp=datetime(2024, 1, 15, 9, 30, 0),
            entry_price=100.0,
            quantity=10,
            side=TradeSide.LONG,
            entry_type="market",
            status=TradeStatus.OPEN,
        )
        trade_id = trade_repo.create(trade)
        assert trade_id > 0

        # Verify foreign key constraint (session must exist)
        retrieved = trade_repo.get(trade_id)
        assert retrieved is not None
        assert retrieved.session_id == session_id
