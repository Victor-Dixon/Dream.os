#!/usr/bin/env python3
"""
Unit Tests for Processing Coordinator
======================================
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.core.analytics.coordinators.processing_coordinator import ProcessingCoordinator


class TestProcessingCoordinator:
    """Tests for ProcessingCoordinator."""

    def test_initialization(self):
        """Test coordinator initialization."""
        coordinator = ProcessingCoordinator()
        assert coordinator.config == {}
        assert coordinator.processors == {}
        assert coordinator.stats["total_processed"] == 0

    def test_initialization_with_config(self):
        """Test initialization with config."""
        config = {"test": "value"}
        coordinator = ProcessingCoordinator(config=config)
        assert coordinator.config == config

    def test_initialization_with_processors(self):
        """Test initialization with processors."""
        processors = {"test": MagicMock()}
        coordinator = ProcessingCoordinator(processors=processors)
        assert coordinator.processors == processors

    def test_register_processor(self):
        """Test registering a processor."""
        coordinator = ProcessingCoordinator()
        mock_processor = MagicMock()
        coordinator.register_processor("test_processor", mock_processor)
        assert "test_processor" in coordinator.processors
        assert coordinator.processors["test_processor"] == mock_processor

    @pytest.mark.asyncio
    async def test_process_data_success(self):
        """Test processing data successfully."""
        coordinator = ProcessingCoordinator()
        result = await coordinator.process_data({"test": "data"})
        assert result["processed"] is True
        assert coordinator.stats["total_processed"] == 1
        assert coordinator.stats["successful"] == 1

    @pytest.mark.asyncio
    async def test_process_data_with_processor(self):
        """Test processing data with registered processor."""
        coordinator = ProcessingCoordinator()
        mock_processor = MagicMock()
        mock_processor.process = AsyncMock(return_value={"result": "test"})
        coordinator.register_processor("test", mock_processor)
        
        result = await coordinator.process_data({"test": "data"})
        assert result["processed"] is True
        assert "test_result" in result
        assert result["test_result"] == {"result": "test"}
        mock_processor.process.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_data_multiple_processors(self):
        """Test processing with multiple processors."""
        coordinator = ProcessingCoordinator()
        proc1 = MagicMock()
        proc1.process = AsyncMock(return_value={"result1": "value1"})
        proc2 = MagicMock()
        proc2.process = AsyncMock(return_value={"result2": "value2"})
        coordinator.register_processor("proc1", proc1)
        coordinator.register_processor("proc2", proc2)
        
        result = await coordinator.process_data({"test": "data"})
        assert "proc1_result" in result
        assert "proc2_result" in result

    @pytest.mark.asyncio
    async def test_process_data_processor_error(self):
        """Test handling processor errors."""
        coordinator = ProcessingCoordinator()
        mock_processor = MagicMock()
        mock_processor.process = AsyncMock(side_effect=Exception("Test error"))
        coordinator.register_processor("test", mock_processor)
        
        result = await coordinator.process_data({"test": "data"})
        assert result["processed"] is False
        assert "error" in result
        assert coordinator.stats["failed"] == 1

    @pytest.mark.asyncio
    async def test_process_data_processor_no_process_method(self):
        """Test with processor that has no process method."""
        coordinator = ProcessingCoordinator()
        mock_processor = MagicMock(spec=[])  # No process method
        coordinator.register_processor("test", mock_processor)
        
        result = await coordinator.process_data({"test": "data"})
        assert result["processed"] is True
        assert coordinator.stats["successful"] == 1

    def test_get_processing_stats_empty(self):
        """Test getting stats with no processing."""
        coordinator = ProcessingCoordinator()
        stats = coordinator.get_processing_stats()
        assert stats["total_processed"] == 0
        assert stats["success_rate"] == 0

    def test_get_processing_stats_with_processing(self):
        """Test getting stats after processing."""
        coordinator = ProcessingCoordinator()
        coordinator.stats["total_processed"] = 10
        coordinator.stats["successful"] = 8
        coordinator.stats["failed"] = 2
        
        stats = coordinator.get_processing_stats()
        assert stats["total_processed"] == 10
        assert stats["successful"] == 8
        assert stats["failed"] == 2
        assert stats["success_rate"] == 80.0

    def test_get_processing_stats_includes_timestamp(self):
        """Test stats include timestamp."""
        coordinator = ProcessingCoordinator()
        stats = coordinator.get_processing_stats()
        assert "timestamp" in stats
        assert isinstance(stats["timestamp"], str)

    def test_reset_stats(self):
        """Test resetting statistics."""
        coordinator = ProcessingCoordinator()
        coordinator.stats["total_processed"] = 10
        coordinator.stats["successful"] = 8
        coordinator.stats["failed"] = 2
        
        coordinator.reset_stats()
        assert coordinator.stats["total_processed"] == 0
        assert coordinator.stats["successful"] == 0
        assert coordinator.stats["failed"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

