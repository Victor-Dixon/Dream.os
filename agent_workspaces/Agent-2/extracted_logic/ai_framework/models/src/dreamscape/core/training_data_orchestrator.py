"""
Training Data Orchestrator Module

This module provides a high-level interface for training data extraction and management.
It orchestrates the generation, processing, and export of training data for AI agents.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .training_system import TrainingDataOrchestrator, TrainingData, TrainingConfig

logger = logging.getLogger(__name__)

def run_structured_training_data_extraction(
    memory_manager=None,
    template_engine=None,
    output_dir: str = "outputs/training",
    categories: List[str] = None,
    max_samples_per_category: int = 100,
    include_conversations: bool = True,
    include_templates: bool = True
) -> Dict[str, Any]:
    """
    Run structured training data extraction with comprehensive configuration.
    
    Args:
        memory_manager: Memory manager instance for accessing conversations
        template_engine: Template engine instance for accessing templates
        output_dir: Directory to save extracted training data
        categories: List of categories to include in extraction
        max_samples_per_category: Maximum samples per category
        include_conversations: Whether to include conversation data
        include_templates: Whether to include template data
        
    Returns:
        Dictionary containing extraction results and metadata
    """
    try:
        logger.info("Starting structured training data extraction")
        
        # Initialize orchestrator
        orchestrator = TrainingDataOrchestrator(memory_manager, template_engine)
        
        # Generate comprehensive dataset
        all_data = orchestrator.generate_comprehensive_dataset(
            include_conversations=include_conversations,
            include_templates=include_templates,
            categories=categories
        )
        
        logger.info(f"Generated {len(all_data)} total training samples")
        
        # Create balanced dataset
        balanced_data = orchestrator.create_balanced_dataset(
            all_data, 
            max_per_category=max_samples_per_category
        )
        
        logger.info(f"Created balanced dataset with {len(balanced_data)} samples")
        
        # Save training data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"training_data_{timestamp}.jsonl"
        
        output_path = orchestrator.generator.save_training_data(
            balanced_data, 
            filename
        )
        
        # Generate summary statistics
        category_counts = {}
        quality_scores = []
        
        for item in balanced_data:
            if item.category not in category_counts:
                category_counts[item.category] = 0
            category_counts[item.category] += 1
            quality_scores.append(item.quality_score)
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        result = {
            "success": True,
            "total_samples": len(balanced_data),
            "output_file": output_path,
            "category_distribution": category_counts,
            "average_quality_score": avg_quality,
            "extraction_timestamp": timestamp,
            "categories_included": categories or ["all"],
            "conversations_included": include_conversations,
            "templates_included": include_templates
        }
        
        logger.info(f"Training data extraction completed successfully: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Training data extraction failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "total_samples": 0,
            "output_file": None
        }

# Re-export the main class for convenience
__all__ = ['TrainingDataOrchestrator', 'run_structured_training_data_extraction'] 