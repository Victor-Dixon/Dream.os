"""
Tests for replay_engine.py - ReplayEngine and ReplaySessionState classes.

Target: ≥85% coverage, deterministic replay validation
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from src.services.trader_replay.replay_engine import ReplayEngine, ReplaySessionState, ReplayState
from src.services.trader_replay.models import Candle
from tests.fixtures.trader_replay import create_test_candles, create_test_session_data


class TestReplayEngine:
    """Test ReplayEngine class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)
        yield db_path
        if db_path.exists():
            db_path.unlink()

    @pytest.fixture
    def engine(self, temp_db):
        """Create ReplayEngine instance."""
        return ReplayEngine(temp_db)

    @pytest.fixture
    def session_data(self):
        """Create test session data."""
        return create_test_session_data(symbol="TEST", candle_count=12)

    def test_create_session_stores_snapshot_metadata(self, engine, session_data):
        """Test that creating a session stores snapshot metadata."""
        session_id = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        assert session_id > 0

        session_info = engine.get_session_info(session_id)
        assert session_info["symbol"] == "TEST"
        assert session_info["session_date"] == "2024-01-15"
        assert session_info["timeframe"] == "1m"
        assert session_info["candle_count"] == 12

    def test_step_advances_index_once(self, engine, session_data):
        """Test that step advances index by one."""
        session_id = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        initial_state = engine.get_replay_state(session_id)
        assert initial_state.current_index == 0

        # Step forward
        new_state = engine.step_replay(session_id, direction="forward")
        assert new_state.current_index == 1
        assert len(new_state.visible_candles) == 2

        # Step forward again
        new_state = engine.step_replay(session_id, direction="forward")
        assert new_state.current_index == 2
        assert len(new_state.visible_candles) == 3

    def test_step_back_retreats_index(self, engine, session_data):
        """Test that step_back retreats index by one."""
        session_id = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        # Advance a few steps
        engine.step_replay(session_id, direction="forward")
        engine.step_replay(session_id, direction="forward")
        state = engine.get_replay_state(session_id)
        assert state.current_index == 2

        # Step back
        new_state = engine.step_replay(session_id, direction="backward")
        assert new_state.current_index == 1
        assert len(new_state.visible_candles) == 2

    def test_jump_to_time_sets_correct_index(self, engine, session_data):
        """Test that jump_to_time sets correct index."""
        session_id = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        # Get a timestamp from the middle
        target_time = datetime.fromisoformat(session_data["candles"][5]["timestamp"])

        # Jump to time
        state = engine.get_replay_state(session_id)
        session_state = engine._active_sessions[session_id]
        candles = session_state.jump_to_time(target_time)

        assert len(candles) == 6  # Up to index 5 (0-indexed)
        assert session_state.current_index == 5

    def test_pause_does_not_advance(self, engine, session_data):
        """Test that pause does not advance replay."""
        session_id = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        initial_state = engine.get_replay_state(session_id)
        initial_index = initial_state.current_index

        # Pause
        engine.pause_replay(session_id)

        # Check state hasn't advanced
        state = engine.get_replay_state(session_id)
        assert state.current_index == initial_index
        assert state.is_playing is False

    def test_deterministic_replay_same_input_same_output(self, engine, session_data):
        """Test that replay is deterministic (same input → same output)."""
        # Create two identical sessions
        session_id_1 = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        session_id_2 = engine.create_session(
            symbol=session_data["symbol"],
            session_date=session_data["session_date"],
            timeframe=session_data["timeframe"],
            candles=session_data["candles"],
        )

        # Both should have same candle count
        info_1 = engine.get_session_info(session_id_1)
        info_2 = engine.get_session_info(session_id_2)

        assert info_1["candle_count"] == info_2["candle_count"]
        assert info_1["candle_count"] == len(session_data["candles"])

        # Step both forward same amount
        for _ in range(5):
            engine.step_replay(session_id_1, direction="forward")
            engine.step_replay(session_id_2, direction="forward")

        state_1 = engine.get_replay_state(session_id_1)
        state_2 = engine.get_replay_state(session_id_2)

        # Should be at same index
        assert state_1.current_index == state_2.current_index
        assert len(state_1.visible_candles) == len(state_2.visible_candles)

        # Candles should be identical
        for c1, c2 in zip(state_1.visible_candles, state_2.visible_candles):
            assert c1.timestamp == c2.timestamp
            assert c1.open == c2.open
            assert c1.high == c2.high
            assert c1.low == c2.low
            assert c1.close == c2.close



