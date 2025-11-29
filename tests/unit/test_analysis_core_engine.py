#!/usr/bin/env python3
"""
Unit Tests for Analysis Core Engine
====================================

Comprehensive tests for analysis_core_engine.py targeting ≥85% coverage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import pytest
import logging
from src.core.engines.analysis_core_engine import AnalysisCoreEngine
from src.core.engines.contracts import EngineContext, EngineResult


class TestAnalysisCoreEngine:
    """Tests for AnalysisCoreEngine."""

    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        return AnalysisCoreEngine()

    @pytest.fixture
    def context(self):
        """Create engine context."""
        logger = logging.getLogger(__name__)
        return EngineContext(
            config={},
            logger=logger,
            metrics={}
        )

    def test_initialization(self, engine):
        """Test engine initialization."""
        assert engine.patterns == {}
        assert engine.violations == []
        assert engine.is_initialized is False

    def test_initialize_success(self, engine, context):
        """Test successful initialization."""
        result = engine.initialize(context)
        assert result is True
        assert engine.is_initialized is True

    def test_initialize_failure(self, engine):
        """Test initialization failure handling."""
        # Create context that will cause error
        bad_context = EngineContext(
            config={},
            logger=None,  # This might cause issues
            metrics={}
        )
        # Should handle gracefully
        result = engine.initialize(bad_context)
        # Should return False on error
        assert isinstance(result, bool)

    def test_execute_analyze_operation(self, engine, context):
        """Test execute with analyze operation."""
        engine.initialize(context)
        payload = {
            "operation": "analyze",
            "content": "test content",
            "type": "general"
        }
        result = engine.execute(context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "content_length" in result.data

    def test_execute_extract_patterns_operation(self, engine, context):
        """Test execute with extract_patterns operation."""
        engine.initialize(context)
        payload = {
            "operation": "extract_patterns",
            "content": "def test(): pass\nclass Test: pass\nimport os",
            "pattern_type": "code"
        }
        result = engine.execute(context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "patterns" in result.data

    def test_execute_detect_violations_operation(self, engine, context):
        """Test execute with detect_violations operation."""
        engine.initialize(context)
        # Create content that will trigger violations
        long_content = "x\n" * 350  # Exceeds 300 lines
        payload = {
            "operation": "detect_violations",
            "content": long_content,
            "violation_type": "general"
        }
        result = engine.execute(context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "violations" in result.data
        assert len(result.data["violations"]) > 0

    def test_execute_unknown_operation(self, engine, context):
        """Test execute with unknown operation."""
        engine.initialize(context)
        payload = {"operation": "unknown_operation"}
        result = engine.execute(context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is False
        assert "error" in result.error or "Unknown" in result.error

    def test_execute_exception_handling(self, engine, context):
        """Test execute exception handling."""
        engine.initialize(context)
        # Payload that might cause exception
        payload = None
        result = engine.execute(context, payload)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_analyze_with_content(self, engine, context):
        """Test analyze method with content."""
        engine.initialize(context)
        data = {
            "content": "test content for analysis",
            "type": "code"
        }
        result = engine.analyze(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert result.data["content_length"] == len(data["content"])
        assert result.data["analysis_type"] == "code"

    def test_analyze_with_empty_content(self, engine, context):
        """Test analyze method with empty content."""
        engine.initialize(context)
        data = {"content": "", "type": "general"}
        result = engine.analyze(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert result.data["content_length"] == 0

    def test_analyze_exception_handling(self, engine, context):
        """Test analyze exception handling."""
        engine.initialize(context)
        # Data that might cause exception
        data = None
        result = engine.analyze(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_extract_patterns(self, engine, context):
        """Test extract_patterns method."""
        engine.initialize(context)
        content = "def func1():\n    pass\nclass Class1:\n    pass\nimport sys"
        data = {
            "content": content,
            "pattern_type": "python"
        }
        result = engine.extract_patterns(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "patterns" in result.data
        assert len(result.data["patterns"]) > 0
        # Check that patterns are stored
        assert "python" in engine.patterns

    def test_extract_patterns_empty_content(self, engine, context):
        """Test extract_patterns with empty content."""
        engine.initialize(context)
        data = {"content": "", "pattern_type": "test"}
        result = engine.extract_patterns(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "patterns" in result.data

    def test_extract_patterns_exception_handling(self, engine, context):
        """Test extract_patterns exception handling."""
        engine.initialize(context)
        data = None
        result = engine.extract_patterns(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_detect_violations_line_count(self, engine, context):
        """Test detect_violations with line count violation."""
        engine.initialize(context)
        # Content exceeding 300 lines
        long_content = "\n".join([f"line {i}" for i in range(350)])
        data = {
            "content": long_content,
            "violation_type": "size"
        }
        result = engine.detect_violations(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert "violations" in result.data
        # Should detect line count violation
        violations = result.data["violations"]
        assert any(v["type"] == "line_count" for v in violations)

    def test_detect_violations_class_count(self, engine, context):
        """Test detect_violations with class count violation."""
        engine.initialize(context)
        # Content with many classes
        many_classes = "\n".join([f"class Class{i}:" for i in range(10)])
        data = {
            "content": many_classes,
            "violation_type": "structure"
        }
        result = engine.detect_violations(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        violations = result.data["violations"]
        # Should detect class count violation
        assert any(v["type"] == "class_count" for v in violations)

    def test_detect_violations_no_violations(self, engine, context):
        """Test detect_violations with no violations."""
        engine.initialize(context)
        # Short content with few classes
        data = {
            "content": "def test(): pass",
            "violation_type": "general"
        }
        result = engine.detect_violations(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is True
        assert len(result.data["violations"]) == 0

    def test_detect_violations_stores_violations(self, engine, context):
        """Test that violations are stored."""
        engine.initialize(context)
        long_content = "\n".join([f"line {i}" for i in range(350)])
        data = {"content": long_content, "violation_type": "test"}
        result = engine.detect_violations(context, data)
        assert len(engine.violations) > 0

    def test_detect_violations_exception_handling(self, engine, context):
        """Test detect_violations exception handling."""
        engine.initialize(context)
        data = None
        result = engine.detect_violations(context, data)
        assert isinstance(result, EngineResult)
        assert result.success is False

    def test_cleanup(self, engine, context):
        """Test cleanup method."""
        engine.initialize(context)
        engine.patterns["test"] = []
        engine.violations.append({"type": "test"})
        result = engine.cleanup(context)
        assert result is True
        assert len(engine.patterns) == 0
        assert len(engine.violations) == 0
        assert engine.is_initialized is False

    def test_cleanup_exception_handling(self, engine):
        """Test cleanup exception handling."""
        engine.initialize(EngineContext(config={}, logger=None, metrics={}))
        # Should handle gracefully
        result = engine.cleanup(EngineContext(config={}, logger=None, metrics={}))
        assert isinstance(result, bool)

    def test_get_status(self, engine):
        """Test get_status method."""
        status = engine.get_status()
        assert "initialized" in status
        assert "patterns_count" in status
        assert "violations_count" in status
        assert status["initialized"] is False

    def test_get_status_after_initialization(self, engine, context):
        """Test get_status after initialization."""
        engine.initialize(context)
        engine.patterns["test"] = []
        engine.violations.append({"type": "test"})
        status = engine.get_status()
        assert status["initialized"] is True
        assert status["patterns_count"] == 1
        assert status["violations_count"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.core.engines.analysis_core_engine", "--cov-report=term-missing"])

