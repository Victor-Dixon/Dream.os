#!/usr/bin/env python3
"""
Training System for Dreamscape
==============================

Consolidated training and data generation system combining:
- training_data_generator.py
- training_data_orchestrator.py
- generate_training_data.py
- agent_trainer.py
- train_my_first_agent.py
- intelligent_agent_system.py

This module provides comprehensive training capabilities for AI agents,
data generation, and model optimization.
"""

import os
import sys
import json
import asyncio
import logging
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Configuration for training sessions."""
    model_name: str = "gpt-4o"
    max_tokens: int = 4000
    temperature: float = 0.7
    batch_size: int = 10
    epochs: int = 5
    learning_rate: float = 0.001
    validation_split: float = 0.2
    early_stopping_patience: int = 3
    save_best_model: bool = True
    output_dir: str = "outputs/training"

@dataclass
class TrainingData:
    """Represents a training data sample."""
    id: str
    input_text: str
    output_text: str
    category: str
    quality_score: float
    source: str
    created_at: datetime
    metadata: Dict[str, Any] = None

@dataclass
class TrainingResult:
    """Result of a training session."""
    session_id: str
    model_name: str
    start_time: datetime
    end_time: datetime
    epochs_completed: int
    final_loss: float
    validation_accuracy: float
    training_samples: int
    validation_samples: int
    model_path: str
    metrics: Dict[str, float]

@dataclass
class AgentPersonality:
    """Personality configuration for AI agents."""
    communication_style: str = "professional"
    expertise_domains: List[str] = None
    response_length: str = "medium"
    formality_level: str = "balanced"
    creativity_level: float = 0.7
    technical_depth: str = "intermediate"
    humor_level: float = 0.3
    empathy_level: float = 0.8
    
    def __post_init__(self):
        if self.expertise_domains is None:
            self.expertise_domains = ["general", "technology", "problem_solving"]

class TrainingDataGenerator:
    """Generates training data from conversations and templates."""
    
    def __init__(self, memory_manager=None, template_engine=None):
        """Initialize the training data generator."""
        self.memory_manager = memory_manager
        self.template_engine = template_engine
        self.output_dir = Path("outputs/training_data")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_from_conversations(self, conversations: List[Dict], 
                                  categories: List[str] = None) -> List[TrainingData]:
        """Generate training data from conversations."""
        training_data = []
        
        for conv in conversations:
            # Extract conversation pairs
            messages = conv.get('messages', [])
            for i in range(len(messages) - 1):
                if messages[i]['role'] == 'user' and messages[i+1]['role'] == 'assistant':
                    training_data.append(TrainingData(
                        id=f"{conv['id']}_{i}",
                        input_text=messages[i]['content'],
                        output_text=messages[i+1]['content'],
                        category=conv.get('category', 'general'),
                        quality_score=self._calculate_quality_score(messages[i+1]['content']),
                        source=conv.get('source', 'unknown'),
                        created_at=datetime.fromisoformat(conv.get('timestamp', datetime.now().isoformat())),
                        metadata={'conversation_id': conv['id'], 'message_index': i}
                    ))
        
        return training_data
    
    def generate_from_templates(self, templates: List[Dict]) -> List[TrainingData]:
        """Generate training data from templates."""
        training_data = []
        
        for template in templates:
            # Create variations of the template
            variations = self._create_template_variations(template)
            
            for i, variation in enumerate(variations):
                training_data.append(TrainingData(
                    id=f"template_{template['id']}_{i}",
                    input_text=variation['input'],
                    output_text=variation['output'],
                    category=template.get('category', 'template'),
                    quality_score=template.get('success_rate', 0.8),
                    source='template',
                    created_at=datetime.now(),
                    metadata={'template_id': template['id'], 'variation': i}
                ))
        
        return training_data
    
    def _calculate_quality_score(self, text: str) -> float:
        """Calculate quality score for training data."""
        # Simple heuristic based on length and content
        if not text or len(text.strip()) < 10:
            return 0.1
        
        # Length factor
        length_score = min(len(text) / 1000, 1.0)
        
        # Content factor (basic checks)
        content_score = 0.5
        if any(keyword in text.lower() for keyword in ['help', 'assist', 'explain', 'guide']):
            content_score += 0.2
        if len(text.split()) > 20:
            content_score += 0.3
        
        return min(length_score + content_score, 1.0)
    
    def _create_template_variations(self, template: Dict) -> List[Dict]:
        """Create variations of a template for training."""
        variations = []
        base_content = template.get('content', '')
        
        # Simple variations
        variations.append({
            'input': f"Please help me with: {base_content}",
            'output': base_content
        })
        
        variations.append({
            'input': f"I need assistance with: {base_content}",
            'output': base_content
        })
        
        return variations
    
    def save_training_data(self, data: List[TrainingData], filename: str = None) -> str:
        """Save training data to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_data_{timestamp}.jsonl"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(asdict(item), default=str) + '\n')
        
        logger.info(f"Saved {len(data)} training samples to {filepath}")
        return str(filepath)

class TrainingDataOrchestrator:
    """Orchestrates the generation and management of training data."""
    
    def __init__(self, memory_manager=None, template_engine=None):
        """Initialize the orchestrator."""
        self.memory_manager = memory_manager
        self.template_engine = template_engine
        self.generator = TrainingDataGenerator(memory_manager, template_engine)
        
    def generate_comprehensive_dataset(self, 
                                     include_conversations: bool = True,
                                     include_templates: bool = True,
                                     categories: List[str] = None) -> List[TrainingData]:
        """Generate a comprehensive training dataset."""
        all_data = []
        
        if include_conversations and self.memory_manager:
            # Get conversations
            conversations = self.memory_manager.get_conversations(limit=1000)
            conv_data = self.generator.generate_from_conversations(conversations, categories)
            all_data.extend(conv_data)
            logger.info(f"Generated {len(conv_data)} samples from conversations")
        
        if include_templates and self.template_engine:
            # Get templates
            templates = self.template_engine.find_templates(active_only=True)
            template_data = self.generator.generate_from_templates(templates)
            all_data.extend(template_data)
            logger.info(f"Generated {len(template_data)} samples from templates")
        
        # Filter by quality
        quality_data = [d for d in all_data if d.quality_score > 0.5]
        logger.info(f"Filtered to {len(quality_data)} high-quality samples")
        
        return quality_data
    
    def create_balanced_dataset(self, data: List[TrainingData], 
                               max_per_category: int = 100) -> List[TrainingData]:
        """Create a balanced dataset with equal representation per category."""
        category_data = {}
        
        for item in data:
            if item.category not in category_data:
                category_data[item.category] = []
            category_data[item.category].append(item)
        
        balanced_data = []
        for category, items in category_data.items():
            # Sort by quality and take top samples
            sorted_items = sorted(items, key=lambda x: x.quality_score, reverse=True)
            balanced_data.extend(sorted_items[:max_per_category])
        
        return balanced_data

class AgentTrainer:
    """Trains AI agents using generated training data."""
    
    def __init__(self, config: TrainingConfig = None):
        """Initialize the agent trainer."""
        self.config = config or TrainingConfig()
        self.training_history = []
        
    def train_agent(self, training_data: List[TrainingData], 
                   agent_name: str = "dreamscape_agent") -> TrainingResult:
        """Train an agent using the provided training data."""
        session_id = f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        logger.info(f"Starting training session {session_id} with {len(training_data)} samples")
        
        # Split data
        random.shuffle(training_data)
        split_idx = int(len(training_data) * (1 - self.config.validation_split))
        train_data = training_data[:split_idx]
        val_data = training_data[split_idx:]
        
        # Training loop
        best_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(self.config.epochs):
            # Simulate training (in real implementation, this would use actual ML framework)
            epoch_loss = self._train_epoch(train_data, epoch)
            val_accuracy = self._validate_epoch(val_data, epoch)
            
            logger.info(f"Epoch {epoch+1}/{self.config.epochs}: Loss={epoch_loss:.4f}, Val_Acc={val_accuracy:.4f}")
            
            # Early stopping
            if epoch_loss < best_loss:
                best_loss = epoch_loss
                patience_counter = 0
                if self.config.save_best_model:
                    self._save_model(session_id, epoch)
            else:
                patience_counter += 1
                if patience_counter >= self.config.early_stopping_patience:
                    logger.info(f"Early stopping at epoch {epoch+1}")
                    break
        
        end_time = datetime.now()
        
        result = TrainingResult(
            session_id=session_id,
            model_name=agent_name,
            start_time=start_time,
            end_time=end_time,
            epochs_completed=epoch + 1,
            final_loss=best_loss,
            validation_accuracy=val_accuracy,
            training_samples=len(train_data),
            validation_samples=len(val_data),
            model_path=f"models/{session_id}",
            metrics={'final_loss': best_loss, 'val_accuracy': val_accuracy}
        )
        
        self.training_history.append(result)
        self._save_training_result(result)
        
        logger.info(f"Training completed: {result}")
        return result
    
    def _train_epoch(self, data: List[TrainingData], epoch: int) -> float:
        """Train for one epoch."""
        # Simulate training loss
        base_loss = 0.5
        epoch_factor = 1.0 / (epoch + 1)
        noise = random.uniform(-0.1, 0.1)
        return max(0.01, base_loss * epoch_factor + noise)
    
    def _validate_epoch(self, data: List[TrainingData], epoch: int) -> float:
        """Validate for one epoch."""
        # Simulate validation accuracy
        base_accuracy = 0.7
        epoch_factor = 1.0 - (1.0 / (epoch + 1))
        noise = random.uniform(-0.05, 0.05)
        return min(1.0, base_accuracy + epoch_factor * 0.3 + noise)
    
    def _save_model(self, session_id: str, epoch: int):
        """Save the current model."""
        model_dir = Path(f"models/{session_id}")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        # In real implementation, save actual model weights
        model_info = {
            'session_id': session_id,
            'epoch': epoch,
            'saved_at': datetime.now().isoformat()
        }
        
        with open(model_dir / 'model_info.json', 'w') as f:
            json.dump(model_info, f, indent=2)
    
    def _save_training_result(self, result: TrainingResult):
        """Save training result to file."""
        results_dir = Path("outputs/training_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = results_dir / f"{result.session_id}.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(result), f, indent=2, default=str)

class IntelligentAgentSystem:
    """Manages intelligent agents and their interactions."""
    
    def __init__(self, memory_manager=None):
        """Initialize the intelligent agent system."""
        self.memory_manager = memory_manager
        self.agents = {}
        self.agent_configs = {}
        
    def create_agent(self, agent_id: str, agent_type: str = "conversational",
                    config: Dict[str, Any] = None) -> str:
        """Create a new intelligent agent."""
        if agent_id in self.agents:
            raise ValueError(f"Agent {agent_id} already exists")
        
        agent_config = {
            'id': agent_id,
            'type': agent_type,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'model': 'gpt-4o',
            'max_tokens': 4000,
            'temperature': 0.7
        }
        
        if config:
            agent_config.update(config)
        
        self.agent_configs[agent_id] = agent_config
        self.agents[agent_id] = self._initialize_agent(agent_config)
        
        logger.info(f"Created agent {agent_id} of type {agent_type}")
        return agent_id
    
    def _initialize_agent(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize an agent with the given configuration."""
        return {
            'config': config,
            'conversation_history': [],
            'performance_metrics': {
                'total_interactions': 0,
                'successful_responses': 0,
                'average_response_time': 0.0
            },
            'specialized_knowledge': {},
            'created_at': datetime.now()
        }
    
    def train_agent(self, agent_id: str, training_data: List[TrainingData]) -> bool:
        """Train a specific agent with training data."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        trainer = AgentTrainer()
        result = trainer.train_agent(training_data, agent_id)
        
        # Update agent with training results
        self.agents[agent_id]['training_results'] = asdict(result)
        self.agents[agent_id]['last_trained'] = datetime.now().isoformat()
        
        logger.info(f"Trained agent {agent_id}: {result}")
        return True
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent information."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents."""
        return [
            {
                'id': agent_id,
                'type': agent['config']['type'],
                'status': agent['config']['status'],
                'created_at': agent['created_at'].isoformat(),
                'total_interactions': agent['performance_metrics']['total_interactions']
            }
            for agent_id, agent in self.agents.items()
        ]

# Convenience functions
def generate_training_data(memory_manager=None, template_engine=None, 
                          output_file: str = None) -> str:
    """Generate training data and save to file."""
    orchestrator = TrainingDataOrchestrator(memory_manager, template_engine)
    data = orchestrator.generate_comprehensive_dataset()
    
    generator = TrainingDataGenerator(memory_manager, template_engine)
    return generator.save_training_data(data, output_file)

def train_agent(agent_id: str, training_data: List[TrainingData], 
                config: TrainingConfig = None) -> TrainingResult:
    """Train an agent with the given data."""
    trainer = AgentTrainer(config)
    return trainer.train_agent(training_data, agent_id)

def create_and_train_agent(agent_id: str, training_data: List[TrainingData],
                          agent_type: str = "conversational") -> bool:
    """Create and train an agent in one step."""
    agent_system = IntelligentAgentSystem()
    agent_system.create_agent(agent_id, agent_type)
    return agent_system.train_agent(agent_id, training_data)

# Export main classes
__all__ = [
    'TrainingConfig',
    'TrainingData',
    'TrainingResult',
    'TrainingDataGenerator',
    'TrainingDataOrchestrator',
    'AgentTrainer',
    'IntelligentAgentSystem',
    'generate_training_data',
    'train_agent',
    'create_and_train_agent'
] 