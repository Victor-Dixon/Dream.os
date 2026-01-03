#!/usr/bin/env python3
"""
Memory Weaponizer
Orchestrates the complete memory weaponization pipeline for Dream.OS
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from ..manager import MemoryManager
from ..search import VectorMemory
from ..processing import MemoryContentProcessor
from .config import WeaponizationConfig
from .data_extractor import DataExtractor
from .episode_generator import EpisodeGenerator
from .helpers import (
    get_date_range, extract_topics, detect_languages,
    calculate_daily_stats, calculate_agent_performance, calculate_conversation_trends,
    generate_blog_posts, generate_social_posts, create_api_script
)

logger = logging.getLogger(__name__)

class MemoryWeaponizer:
    """Orchestrates the complete memory weaponization pipeline."""
    
    def __init__(self, config: Optional[WeaponizationConfig] = None):
        """
        Initialize the memory weaponizer.
        
        Args:
            config: Weaponization configuration
        """
        self.config = config or WeaponizationConfig()
        self.memory_manager = MemoryManager()
        self.vector_memory = VectorMemory()
        self.content_processor = MemoryContentProcessor()
        self.data_extractor = DataExtractor()
        self.episode_generator = EpisodeGenerator()
        
        # Setup output directories
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "episodes").mkdir(exist_ok=True)
        (self.output_dir / "analytics").mkdir(exist_ok=True)
        (self.output_dir / "content").mkdir(exist_ok=True)
        (self.output_dir / "api").mkdir(exist_ok=True)
    
    def weaponize_full_pipeline(self) -> Dict[str, Any]:
        """
        Run the complete weaponization pipeline.
        
        Returns:
            Dictionary with pipeline results
        """
        logger.info("🚀 Starting memory weaponization pipeline")
        
        try:
            results = {}
            
            # Step 1: Analyze corpus
            logger.info("📊 Step 1: Analyzing conversation corpus")
            results["corpus_analysis"] = self._analyze_corpus()
            
            # Step 2: Build vector index
            logger.info("🔍 Step 2: Building vector index")
            results["vector_index"] = self._build_vector_index()
            
            # Step 3: Generate training data
            logger.info("🎓 Step 3: Generating training data")
            results["training_data"] = self._generate_training_data()
            
            # Step 4: Create episodes
            logger.info("📺 Step 4: Creating episodes")
            results["episodes"] = self._create_episodes()
            
            # Step 5: Generate analytics
            logger.info("📈 Step 5: Generating analytics")
            results["analytics"] = self._generate_analytics()
            
            # Step 6: Generate content
            logger.info("📝 Step 6: Generating content")
            results["content"] = self._generate_content()
            
            # Step 7: Deploy context injection API
            logger.info("🔌 Step 7: Deploying context injection API")
            results["api"] = self._deploy_context_injection_api()
            
            # Save results
            self._save_results(results)
            
            logger.info("✅ Memory weaponization pipeline completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"❌ Memory weaponization pipeline failed: {e}")
            raise
    
    def _analyze_corpus(self) -> Dict[str, Any]:
        """Analyze the conversation corpus."""
        conversations = self.memory_manager.get_all_conversations()
        stats = {
            "total_conversations": len(conversations),
            "total_messages": sum(len(conv.get('messages', [])) for conv in conversations),
            "date_range": get_date_range(conversations),
            "topics": extract_topics(conversations),
            "languages": detect_languages(conversations)
        }
        return stats
    
    def _build_vector_index(self) -> Dict[str, Any]:
        """Build vector index for semantic search."""
        conversations = self.memory_manager.get_all_conversations()
        
        # Extract text content
        texts = []
        for conv in conversations:
            messages = conv.get('messages', [])
            content = ' '.join([msg.get('content', '') for msg in messages])
            if content.strip():
                texts.append(content)
        
        # Build vector index
        if texts:
            self.vector_memory.build_index(texts)
            return {"status": "success", "documents_indexed": len(texts)}
        else:
            return {"status": "no_content", "documents_indexed": 0}
    
    def _generate_training_data(self) -> Dict[str, Any]:
        """Generate training data from conversations."""
        conversations = self.memory_manager.get_all_conversations()
        
        training_data = []
        for conv in conversations:
            # Extract user messages for training
            user_messages = [
                msg.get('content', '') 
                for msg in conv.get('messages', []) 
                if msg.get('role') == 'user'
            ]
            
            if user_messages:
                training_data.append({
                    'conversation_id': conv.get('id'),
                    'messages': user_messages,
                    'topics': conv.get('topics', [])
                })
        
        # Save training data
        training_file = self.output_dir / "training_data.json"
        with open(training_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        return {
            "status": "success",
            "training_examples": len(training_data),
            "file": str(training_file)
        }
    
    def _create_episodes(self) -> Dict[str, Any]:
        """Create episodes from conversations."""
        conversations = self.memory_manager.get_all_conversations()
        
        episodes = []
        for conv in conversations:
            episode = self.episode_generator.create_episode(conv)
            if episode:
                episodes.append(episode)
        
        # Save episodes
        episodes_file = self.output_dir / "episodes" / "episodes.json"
        with open(episodes_file, 'w') as f:
            json.dump(episodes, f, indent=2)
        
        return {
            "status": "success",
            "episodes_created": len(episodes),
            "file": str(episodes_file)
        }
    
    def _generate_analytics(self) -> Dict[str, Any]:
        """Generate analytics from conversations."""
        conversations = self.memory_manager.get_all_conversations()
        
        analytics = {
            "daily_stats": calculate_daily_stats(conversations),
            "agent_performance": calculate_agent_performance(conversations),
            "conversation_trends": calculate_conversation_trends(conversations),
            "topics_analysis": {
                "topics": extract_topics(conversations),
                "languages": detect_languages(conversations)
            }
        }
        
        # Save analytics
        analytics_file = self.output_dir / "analytics" / "analytics.json"
        with open(analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        return {
            "status": "success",
            "file": str(analytics_file)
        }
    
    def _generate_content(self) -> Dict[str, Any]:
        """Generate content from conversations."""
        conversations = self.memory_manager.get_all_conversations()
        
        content = {
            "blog_posts": generate_blog_posts(conversations),
            "social_posts": generate_social_posts(conversations)
        }
        
        # Save content
        content_file = self.output_dir / "content" / "generated_content.json"
        with open(content_file, 'w') as f:
            json.dump(content, f, indent=2)
        
        return {
            "status": "success",
            "blog_posts": len(content["blog_posts"]),
            "social_posts": len(content["social_posts"]),
            "file": str(content_file)
        }
    
    def _deploy_context_injection_api(self) -> Dict[str, Any]:
        """Deploy context injection API."""
        api_script = create_api_script()
        api_file = self.output_dir / "api" / "context_injection_api.py"
        
        with open(api_file, 'w') as f:
            f.write(api_script)
        
        logger.info("Context injection API deployed")
        return {"status": "success", "file": str(api_file)}
    
    def _save_results(self, results: Dict[str, Any]):
        """Save weaponization results."""
        results_file = self.output_dir / "weaponization_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {results_file}") 