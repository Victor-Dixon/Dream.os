#!/usr/bin/env python3
"""
Integration Tests for Training Data Extraction System
====================================================

Tests the complete training data extraction workflow including:
- Orchestration logic
- Data generation
- GUI components
- Error handling
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any

from dreamscape.core.training_system import TrainingDataOrchestrator
from dreamscape.core.training_system import TrainingDataGenerator
# EDIT START: Consolidation import update (Agent 5)
from dreamscape.core.memory_system import MemoryManager
# EDIT END


class TestTrainingDataOrchestrator:
    """Test the training data orchestrator functionality."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_memory_manager(self):
        """Create a mock memory manager with test conversations."""
        mock_manager = Mock(spec=MemoryManager)
        
        # Mock conversations
        test_conversations = [
            {
                "id": "conv_1",
                "title": "Python Web Development",
                "content": "User: How do I create a Flask web app?\nAssistant: Here's how to create a Flask web app...",
                "timestamp": "2024-01-01T10:00:00Z"
            },
            {
                "id": "conv_2", 
                "title": "JavaScript Debugging",
                "content": "User: I'm getting an error in my JavaScript code.\nAssistant: Let me help you debug that...",
                "timestamp": "2024-01-01T11:00:00Z"
            },
            {
                "id": "conv_3",
                "title": "Database Design",
                "content": "User: What's the best way to design a database schema?\nAssistant: Here are some best practices...",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        ]
        
        mock_manager.get_conversations.return_value = test_conversations
        return mock_manager
    
    @pytest.fixture
    def orchestrator(self, mock_memory_manager):
        """Create an orchestrator with mocked dependencies."""
        with patch('dreamscape.core.training_data_orchestrator.MemoryManager', return_value=mock_memory_manager):
            return TrainingDataOrchestrator()
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization."""
        assert orchestrator is not None
        assert hasattr(orchestrator, 'memory_manager')
        assert hasattr(orchestrator, 'generator')
    
    def test_get_conversations_by_ids(self, orchestrator, mock_memory_manager):
        """Test getting conversations by specific IDs."""
        conversation_ids = ["conv_1", "conv_3"]
        conversations = orchestrator._get_conversations_by_ids(conversation_ids)
        
        assert len(conversations) == 2
        assert conversations[0]["id"] == "conv_1"
        assert conversations[1]["id"] == "conv_3"
    
    def test_extract_conversation_data_success(self, orchestrator, temp_output_dir):
        """Test successful conversation data extraction."""
        conversation = {
            "id": "test_conv",
            "title": "Test Conversation",
            "content": "This is a test conversation about Python programming."
        }
        
        result = orchestrator._extract_conversation_data(conversation, Path(temp_output_dir))
        
        assert result["success"] is True
        assert result["conversation_id"] == "test_conv"
        assert "raw_data_path" in result
        assert "structured_data_path" in result
        assert "structured_data" in result
        
        # Check that files were created
        assert Path(result["raw_data_path"]).exists()
        assert Path(result["structured_data_path"]).exists()
    
    def test_extract_conversation_data_no_content(self, orchestrator, temp_output_dir):
        """Test conversation extraction with no content."""
        conversation = {
            "id": "empty_conv",
            "title": "Empty Conversation",
            "content": ""
        }
        
        result = orchestrator._extract_conversation_data(conversation, Path(temp_output_dir))
        
        assert result["success"] is False
        assert "No content found" in result["error"]
    
    def test_generate_summary_report(self, orchestrator):
        """Test summary report generation."""
        extraction_results = [
            {
                "success": True,
                "conversation_id": "conv_1",
                "content_length": 100,
                "structured_data": {"summary": "Test summary"}
            },
            {
                "success": True,
                "conversation_id": "conv_2", 
                "content_length": 200,
                "structured_data": {"summary": "Another summary"}
            },
            {
                "success": False,
                "conversation_id": "conv_3",
                "error": "Extraction failed"
            }
        ]
        
        report = orchestrator._generate_summary_report(
            total_conversations=3,
            successful_extractions=2,
            failed_extractions=1,
            extraction_time=5.5,
            extraction_results=extraction_results
        )
        
        assert "extraction_summary" in report
        assert "field_analysis" in report
        assert "extraction_metadata" in report
        
        summary = report["extraction_summary"]
        assert summary["total_conversations"] == 3
        assert summary["successful_extractions"] == 2
        assert summary["failed_extractions"] == 1
        assert summary["success_rate_percentage"] == 66.67
        assert summary["extraction_time_seconds"] == 5.5
    
    def test_analyze_extracted_fields(self, orchestrator):
        """Test field analysis functionality."""
        extraction_results = [
            {
                "success": True,
                "structured_data": {
                    "summary": "Test summary",
                    "key_topics": ["Python", "Web Development"],
                    "user_intent": "learning",
                    "assistant_actions": ["provided_tutorial"],
                    "skills_demonstrated": [{"skill": "Python", "level": "intermediate"}],
                    "code_examples": [{"language": "Python", "purpose": "web app"}],
                    "best_practices": ["use virtual environments"],
                    "pitfalls": ["circular imports"],
                    "personality_traits": ["helpful", "patient"],
                    "difficulty_level": "intermediate",
                    "conversation_type": "tutorial"
                }
            },
            {
                "success": True,
                "structured_data": {
                    "summary": "Another summary",
                    "key_topics": ["JavaScript"],
                    "user_intent": "debugging",
                    "assistant_actions": ["debugged_code"],
                    "skills_demonstrated": [{"skill": "JavaScript", "level": "beginner"}],
                    "code_examples": [{"language": "JavaScript", "purpose": "debugging"}],
                    "best_practices": ["use console.log"],
                    "pitfalls": ["undefined variables"],
                    "personality_traits": ["helpful"],
                    "difficulty_level": "beginner",
                    "conversation_type": "debugging"
                }
            }
        ]
        
        field_analysis = orchestrator._analyze_extracted_fields(extraction_results)
        
        assert "summary" in field_analysis
        assert "key_topics" in field_analysis
        assert "user_intent" in field_analysis
        
        # Check summary field analysis
        summary_analysis = field_analysis["summary"]
        assert summary_analysis["present_count"] == 2
        assert summary_analysis["present_percentage"] == 100.0
        assert len(summary_analysis["sample_values"]) == 2


class TestTrainingDataGenerator:
    """Test the training data generator functionality."""
    
    @pytest.fixture
    def generator(self):
        """Create a training data generator."""
        return TrainingDataGenerator()
    
    def test_generator_initialization(self, generator):
        """Test generator initialization."""
        assert generator is not None
        assert hasattr(generator, 'training_prompts')
        assert len(generator.training_prompts) > 0
    
    def test_generate_structured_summary(self, generator):
        """Test structured summary generation."""
        content = "This is a conversation about Python web development with Flask framework."
        
        result = generator.generate_structured_summary(content)
        
        assert isinstance(result, dict)
        assert "summary" in result
        assert "key_topics" in result
        assert "user_intent" in result
        assert "assistant_actions" in result
        assert "skills_demonstrated" in result
        assert "code_examples" in result
        assert "best_practices" in result
        assert "pitfalls" in result
        assert "personality_traits" in result
        assert "difficulty_level" in result
        assert "conversation_type" in result
    
    def test_create_enhanced_fallback_structure(self, generator):
        """Test enhanced fallback structure creation."""
        content = "Python web development tutorial with Flask and SQLAlchemy"
        
        result = generator._create_enhanced_fallback_structure(content)
        
        assert result["summary"] is not None
        assert "Python" in result["key_topics"]
        assert result["difficulty_level"] in ["beginner", "intermediate", "expert"]
        assert result["conversation_type"] in ["tutorial", "debugging", "design", "general"]
        assert "extraction_method" in result
    
    def test_language_detection(self, generator):
        """Test programming language detection."""
        # Test Python detection
        python_content = "Python programming with Django framework"
        python_result = generator._create_enhanced_fallback_structure(python_content)
        assert "Python" in python_result["key_topics"]
        
        # Test JavaScript detection
        js_content = "JavaScript debugging with console.log"
        js_result = generator._create_enhanced_fallback_structure(js_content)
        assert "JavaScript" in js_result["key_topics"]
        
        # Test SQL detection
        sql_content = "SQL database queries and optimization"
        sql_result = generator._create_enhanced_fallback_structure(sql_content)
        assert "SQL" in sql_result["key_topics"]
    
    def test_difficulty_level_detection(self, generator):
        """Test difficulty level detection."""
        # Test beginner detection
        beginner_content = "Basic Python tutorial for beginners"
        beginner_result = generator._create_enhanced_fallback_structure(beginner_content)
        assert beginner_result["difficulty_level"] == "beginner"
        
        # Test intermediate detection
        intermediate_content = "Advanced web development with complex architecture"
        intermediate_result = generator._create_enhanced_fallback_structure(intermediate_content)
        assert intermediate_result["difficulty_level"] == "intermediate"
        
        # Test expert detection
        expert_content = "Expert-level enterprise software design"
        expert_result = generator._create_enhanced_fallback_structure(expert_content)
        assert expert_result["difficulty_level"] == "expert"
    
    def test_conversation_type_detection(self, generator):
        """Test conversation type detection."""
        # Test tutorial detection
        tutorial_content = "How to learn Python programming tutorial"
        tutorial_result = generator._create_enhanced_fallback_structure(tutorial_content)
        assert tutorial_result["conversation_type"] == "tutorial"
        
        # Test debugging detection
        debug_content = "Error in my code, need to fix this bug"
        debug_result = generator._create_enhanced_fallback_structure(debug_content)
        assert debug_result["conversation_type"] == "debugging"
        
        # Test design detection
        design_content = "Database schema design and architecture"
        design_result = generator._create_enhanced_fallback_structure(design_content)
        assert design_result["conversation_type"] == "design"


class TestTrainingDataExtractionWorkflow:
    """Test the complete training data extraction workflow."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_memory_manager(self):
        """Create a mock memory manager."""
        mock_manager = Mock(spec=MemoryManager)
        mock_manager.get_conversations.return_value = [
            {
                "id": "test_conv_1",
                "title": "Test Conversation 1",
                "content": "Python web development tutorial with Flask framework."
            },
            {
                "id": "test_conv_2",
                "title": "Test Conversation 2", 
                "content": "JavaScript debugging techniques and best practices."
            }
        ]
        return mock_manager
    
    def test_run_structured_training_data_extraction(self, temp_output_dir, mock_memory_manager):
        """Test the complete extraction workflow."""
        with patch('dreamscape.core.training_data_orchestrator.MemoryManager', return_value=mock_memory_manager):
            progress_calls = []
            
            def progress_callback(current: int, total: int, message: str):
                progress_calls.append((current, total, message))
            
            result = run_structured_training_data_extraction(
                output_dir=temp_output_dir,
                max_conversations=2,
                progress_callback=progress_callback
            )
            
            # Check result structure
            assert result["success"] is True
            assert "output_directory" in result
            assert "statistics" in result
            assert "extraction_results" in result
            
            # Check statistics
            stats = result["statistics"]
            assert "extraction_summary" in stats
            assert "field_analysis" in stats
            assert "extraction_metadata" in stats
            
            summary = stats["extraction_summary"]
            assert summary["total_conversations"] == 2
            assert summary["successful_extractions"] == 2
            assert summary["failed_extractions"] == 0
            
            # Check progress callback was called
            assert len(progress_calls) > 0
            
            # Check output files were created
            output_path = Path(temp_output_dir)
            assert (output_path / "extraction_report.json").exists()
            
            # Check individual conversation files
            extraction_results = result["extraction_results"]
            assert len(extraction_results) == 2
            
            for result_item in extraction_results:
                assert result_item["success"] is True
                assert Path(result_item["raw_data_path"]).exists()
                assert Path(result_item["structured_data_path"]).exists()
    
    def test_extraction_with_no_conversations(self, temp_output_dir):
        """Test extraction when no conversations are available."""
        with patch('dreamscape.core.training_data_orchestrator.MemoryManager') as mock_mm_class:
            mock_manager = Mock(spec=MemoryManager)
            mock_manager.get_conversations.return_value = []
            mock_mm_class.return_value = mock_manager
            
            result = run_structured_training_data_extraction(
                output_dir=temp_output_dir,
                max_conversations=10
            )
            
            assert result["success"] is False
            assert "No conversations found" in result["error"]
    
    def test_extraction_with_specific_conversation_ids(self, temp_output_dir, mock_memory_manager):
        """Test extraction with specific conversation IDs."""
        with patch('dreamscape.core.training_data_orchestrator.MemoryManager', return_value=mock_memory_manager):
            conversation_ids = ["test_conv_1"]
            
            result = run_structured_training_data_extraction(
                output_dir=temp_output_dir,
                conversation_ids=conversation_ids
            )
            
            assert result["success"] is True
            stats = result["statistics"]["extraction_summary"]
            assert stats["total_conversations"] == 1
            assert stats["successful_extractions"] == 1


class TestTrainingDataExtractionErrorHandling:
    """Test error handling in training data extraction."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_extraction_with_invalid_output_directory(self):
        """Test extraction with invalid output directory."""
        # Try to use a directory that can't be created
        # Use a path with invalid characters that will cause an error on Windows
        invalid_dir = "C:/invalid/path/with/invalid/chars/*?<>|"
        
        with patch('dreamscape.core.training_data_orchestrator.MemoryManager') as mock_mm_class:
            mock_manager = Mock()
            mock_manager.get_conversations.return_value = [
                {"id": "test", "title": "Test", "content": "Test content"}
            ]
            mock_mm_class.return_value = mock_manager
            
            # This should fail gracefully
            result = run_structured_training_data_extraction(
                output_dir=invalid_dir,
                max_conversations=1
            )
            
            # The result should indicate failure
            assert result["success"] is False
    
    def test_extraction_with_corrupted_conversation_data(self, temp_output_dir):
        """Test extraction with corrupted conversation data."""
        with patch('dreamscape.core.training_data_orchestrator.MemoryManager') as mock_mm_class:
            mock_manager = Mock(spec=MemoryManager)
            # Conversation with missing required fields
            mock_manager.get_conversations.return_value = [
                {"id": "corrupted", "title": "Corrupted"}  # Missing content
            ]
            mock_mm_class.return_value = mock_manager
            
            result = run_structured_training_data_extraction(
                output_dir=temp_output_dir,
                max_conversations=1
            )
            
            # Should complete but with failed extractions
            assert result["success"] is True
            stats = result["statistics"]["extraction_summary"]
            assert stats["failed_extractions"] == 1
            assert stats["successful_extractions"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 