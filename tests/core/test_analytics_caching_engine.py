#!/usr/bin/env python3
"""
Unit Tests for Caching Engine
==============================

Comprehensive tests for caching_engine_fixed.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-28
"""

import pytest
from src.core.analytics.engines.caching_engine_fixed import CachingEngine


class TestCachingEngine:
    """Tests for CachingEngine."""

    def test_initialization(self):
        """Test cache engine initialization."""
        engine = CachingEngine()
        assert engine.config == {}
        assert len(engine.cache) == 0
        assert engine.max_size == 1000
        assert engine.stats["hits"] == 0
        assert engine.stats["misses"] == 0

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"test": "value"}
        engine = CachingEngine(config)
        assert engine.config == config

    def test_initialization_with_max_size(self):
        """Test initialization with custom max_size."""
        engine = CachingEngine(max_size=500)
        assert engine.max_size == 500

    def test_get_nonexistent_key(self):
        """Test getting non-existent key."""
        engine = CachingEngine()
        result = engine.get("nonexistent")
        assert result is None
        assert engine.stats["misses"] == 1

    def test_set_and_get(self):
        """Test setting and getting a value."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        result = engine.get("key1")
        assert result == "value1"
        assert engine.stats["hits"] == 1

    def test_get_moves_to_end_lru(self):
        """Test that get moves key to end (LRU behavior)."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.get("key1")  # Should move key1 to end
        # First key should now be key2 (not key1)
        first_key = next(iter(engine.cache))
        assert first_key == "key2"

    def test_set_updates_existing_key(self):
        """Test setting value for existing key."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        engine.set("key1", "value2")
        result = engine.get("key1")
        assert result == "value2"

    def test_set_increments_stats(self):
        """Test that set increments stats."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        assert engine.stats["sets"] == 1

    def test_lru_eviction(self):
        """Test LRU eviction when max_size exceeded."""
        engine = CachingEngine(max_size=3)
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.set("key3", "value3")
        engine.set("key4", "value4")  # Should evict key1
        assert "key1" not in engine.cache
        assert engine.stats["evictions"] == 1

    def test_lru_eviction_preserves_recently_used(self):
        """Test that LRU eviction preserves recently used keys."""
        engine = CachingEngine(max_size=2)
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.get("key1")  # Make key1 recently used
        engine.set("key3", "value3")  # Should evict key2, not key1
        assert "key1" in engine.cache
        assert "key2" not in engine.cache
        assert "key3" in engine.cache

    def test_delete_existing_key(self):
        """Test deleting existing key."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        result = engine.delete("key1")
        assert result is True
        assert "key1" not in engine.cache

    def test_delete_nonexistent_key(self):
        """Test deleting non-existent key."""
        engine = CachingEngine()
        result = engine.delete("nonexistent")
        assert result is False

    def test_delete_exception_handling(self):
        """Test delete exception handling."""
        engine = CachingEngine()
        # Should handle gracefully
        result = engine.delete(None)
        assert isinstance(result, bool)

    def test_clear(self):
        """Test clearing all cache entries."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.clear()
        assert len(engine.cache) == 0

    def test_clear_exception_handling(self):
        """Test clear exception handling."""
        engine = CachingEngine()
        # Should handle gracefully
        engine.clear()
        assert True  # No exception

    def test_get_stats_empty_cache(self):
        """Test getting stats with empty cache."""
        engine = CachingEngine()
        stats = engine.get_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["cache_size"] == 0
        assert stats["hit_rate"] == 0

    def test_get_stats_with_operations(self):
        """Test getting stats with cache operations."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        engine.get("key1")  # Hit
        engine.get("key2")  # Miss
        stats = engine.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["sets"] == 1
        assert stats["hit_rate"] == 0.5

    def test_get_stats_includes_evictions(self):
        """Test that stats include eviction count."""
        engine = CachingEngine(max_size=2)
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.set("key3", "value3")  # Evicts key1
        stats = engine.get_stats()
        assert stats["evictions"] == 1

    def test_get_stats_exception_handling(self):
        """Test get stats exception handling."""
        engine = CachingEngine()
        engine.stats = None  # Break it
        stats = engine.get_stats()
        assert stats == {}

    def test_get_status(self):
        """Test getting engine status."""
        engine = CachingEngine(max_size=100)
        engine.set("key1", "value1")
        status = engine.get_status()
        assert status["active"] is True
        assert status["cache_size"] == 1
        assert status["max_size"] == 100
        assert "utilization" in status
        assert status["memory_safe"] is True

    def test_get_status_shows_utilization(self):
        """Test that status shows cache utilization."""
        engine = CachingEngine(max_size=10)
        for i in range(5):
            engine.set(f"key{i}", f"value{i}")
        status = engine.get_status()
        assert "50.0%" in status["utilization"]

    def test_multiple_get_increases_hits(self):
        """Test that multiple gets increase hit count."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        engine.get("key1")
        engine.get("key1")
        engine.get("key1")
        assert engine.stats["hits"] == 3

    def test_cache_preserves_insertion_order(self):
        """Test that cache preserves insertion order (OrderedDict)."""
        engine = CachingEngine()
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.set("key3", "value3")
        keys = list(engine.cache.keys())
        assert keys == ["key1", "key2", "key3"]

    def test_set_over_capacity_evicts_lru(self):
        """Test that setting over capacity evicts least recently used."""
        engine = CachingEngine(max_size=2)
        engine.set("key1", "value1")
        engine.set("key2", "value2")
        engine.set("key3", "value3")  # Evicts key1
        assert len(engine.cache) == 2
        assert "key1" not in engine.cache


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.analytics.engines.caching_engine_fixed", "--cov-report=term-missing"])

