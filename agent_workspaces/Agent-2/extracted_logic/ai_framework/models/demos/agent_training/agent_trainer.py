"""
Agent Trainer - Core training and evaluation system for AI agents
Handles training data preparation, model training, evaluation, and deployment
"""

import json
import pickle
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Configuration for agent training"""
    model_type: str = "gpt-3.5-turbo"
    max_epochs: int = 10
    batch_size: int = 32
    learning_rate: float = 0.001
    validation_split: float = 0.2
    early_stopping_patience: int = 3
    min_quality_score: float = 0.7
    max_training_samples: int = 10000
    use_augmentation: bool = True
    augmentation_factor: int = 2

@dataclass
class TrainingMetrics:
    """Training performance metrics"""
    epoch: int
    loss: float
    accuracy: float
    validation_loss: float
    validation_accuracy: float
    learning_rate: float
    timestamp: str

@dataclass
class AgentModel:
    """Trained agent model information"""
    model_id: str
    name: str
    description: str
    model_type: str
    training_config: TrainingConfig
    performance_metrics: Dict[str, float]
    training_data_stats: Dict[str, Any]
    created_at: str
    version: str = "1.0.0"
    status: str = "trained"

class AgentTrainer:
    """Main agent training system"""
    
    def __init__(self, data_dir: str = "training_data", models_dir: str = "trained_models"):
        self.data_dir = Path(data_dir)
        self.models_dir = Path(models_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.db_path = self.data_dir / "agent_training.db"
        self._init_database()
        
        # Training state
        self.current_model = None
        self.training_history = []
        
    def _init_database(self):
        """Initialize training database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create models table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                model_type TEXT NOT NULL,
                training_config TEXT,
                performance_metrics TEXT,
                training_data_stats TEXT,
                created_at TEXT NOT NULL,
                version TEXT DEFAULT '1.0.0',
                status TEXT DEFAULT 'trained'
            )
        """)
        
        # Create training history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id TEXT NOT NULL,
                epoch INTEGER NOT NULL,
                loss REAL NOT NULL,
                accuracy REAL NOT NULL,
                validation_loss REAL,
                validation_accuracy REAL,
                learning_rate REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (model_id) REFERENCES models (model_id)
            )
        """)
        
        # Create evaluation results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id TEXT NOT NULL,
                test_name TEXT NOT NULL,
                accuracy REAL NOT NULL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                response_time REAL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (model_id) REFERENCES models (model_id)
            )
        """)
        
        conn.commit()
        conn.close()
        
    def prepare_training_data(self, conversations: List[Dict], config: TrainingConfig) -> Tuple[List, List]:
        """Prepare training data from conversations"""
        logger.info("Preparing training data...")
        
        training_data = []
        validation_data = []
        
        for conv in conversations:
            # Extract high-quality conversation pairs
            if self._is_high_quality_conversation(conv, config.min_quality_score):
                pairs = self._extract_conversation_pairs(conv)
                training_data.extend(pairs)
        
        # Apply data augmentation if enabled
        if config.use_augmentation:
            training_data = self._augment_training_data(training_data, config.augmentation_factor)
        
        # Limit training samples
        if len(training_data) > config.max_training_samples:
            training_data = training_data[:config.max_training_samples]
        
        # Split into training and validation
        split_idx = int(len(training_data) * (1 - config.validation_split))
        train_data = training_data[:split_idx]
        val_data = training_data[split_idx:]
        
        logger.info(f"Prepared {len(train_data)} training samples and {len(val_data)} validation samples")
        
        return train_data, val_data
    
    def _is_high_quality_conversation(self, conversation: Dict, min_score: float) -> bool:
        """Check if conversation meets quality threshold"""
        # Check for quality indicators
        quality_indicators = [
            conversation.get('quality_score', 0),
            conversation.get('response_quality', 0),
            conversation.get('engagement_score', 0)
        ]
        
        avg_quality = sum(quality_indicators) / len(quality_indicators)
        return avg_quality >= min_score
    
    def _extract_conversation_pairs(self, conversation: Dict) -> List[Tuple[str, str]]:
        """Extract input-output pairs from conversation"""
        pairs = []
        messages = conversation.get('messages', [])
        
        for i in range(len(messages) - 1):
            if messages[i].get('role') == 'user' and messages[i + 1].get('role') == 'assistant':
                input_text = messages[i].get('content', '')
                output_text = messages[i + 1].get('content', '')
                
                if input_text.strip() and output_text.strip():
                    pairs.append((input_text, output_text))
        
        return pairs
    
    def _augment_training_data(self, data: List[Tuple[str, str]], factor: int) -> List[Tuple[str, str]]:
        """Apply data augmentation techniques"""
        augmented_data = data.copy()
        
        for _ in range(factor - 1):
            for input_text, output_text in data:
                # Simple augmentation: add noise, rephrase, etc.
                augmented_input = self._augment_text(input_text)
                augmented_output = self._augment_text(output_text)
                augmented_data.append((augmented_input, augmented_output))
        
        return augmented_data
    
    def _augment_text(self, text: str) -> str:
        """Apply text augmentation techniques"""
        # Simple augmentation - in practice, use more sophisticated methods
        import random
        
        augmentations = [
            lambda t: t + " [context]",
            lambda t: "[enhanced] " + t,
            lambda t: t.replace(".", "!") if "." in t else t,
            lambda t: t.upper() if random.random() < 0.1 else t
        ]
        
        return random.choice(augmentations)(text)
    
    def train_agent(self, training_data: List[Tuple[str, str]], config: TrainingConfig, 
                   model_name: str = "Custom Agent", description: str = "") -> AgentModel:
        """Train a new agent model"""
        logger.info(f"Starting training for model: {model_name}")
        
        # Generate model ID
        model_id = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare data
        conversations = [{'messages': [{'role': 'user', 'content': inp}, {'role': 'assistant', 'content': out}]} 
                        for inp, out in training_data]
        train_data, val_data = self.prepare_training_data(conversations, config)
        
        # Initialize training metrics
        self.training_history = []
        best_validation_loss = float('inf')
        patience_counter = 0
        
        # Training loop
        for epoch in range(config.max_epochs):
            # Simulate training (in practice, use actual model training)
            train_loss, train_acc = self._simulate_training_epoch(train_data, epoch)
            val_loss, val_acc = self._simulate_validation_epoch(val_data, epoch)
            
            # Record metrics
            metrics = TrainingMetrics(
                epoch=epoch + 1,
                loss=train_loss,
                accuracy=train_acc,
                validation_loss=val_loss,
                validation_accuracy=val_acc,
                learning_rate=config.learning_rate,
                timestamp=datetime.now().isoformat()
            )
            
            self.training_history.append(metrics)
            
            # Early stopping check
            if val_loss < best_validation_loss:
                best_validation_loss = val_loss
                patience_counter = 0
            else:
                patience_counter += 1
                
            if patience_counter >= config.early_stopping_patience:
                logger.info(f"Early stopping at epoch {epoch + 1}")
                break
        
        # Create model object
        final_metrics = self.training_history[-1] if self.training_history else None
        performance_metrics = {
            'final_loss': final_metrics.loss if final_metrics else 0.0,
            'final_accuracy': final_metrics.accuracy if final_metrics else 0.0,
            'best_validation_accuracy': max([m.validation_accuracy for m in self.training_history]) if self.training_history else 0.0,
            'training_epochs': len(self.training_history),
            'early_stopped': patience_counter >= config.early_stopping_patience
        }
        
        training_data_stats = {
            'total_samples': len(train_data) + len(val_data),
            'training_samples': len(train_data),
            'validation_samples': len(val_data),
            'augmentation_factor': config.augmentation_factor if config.use_augmentation else 1
        }
        
        model = AgentModel(
            model_id=model_id,
            name=model_name,
            description=description,
            model_type=config.model_type,
            training_config=config,
            performance_metrics=performance_metrics,
            training_data_stats=training_data_stats,
            created_at=datetime.now().isoformat()
        )
        
        # Save model
        self._save_model(model)
        self.current_model = model
        
        logger.info(f"Training completed. Model ID: {model_id}")
        return model
    
    def _simulate_training_epoch(self, data: List[Tuple[str, str]], epoch: int) -> Tuple[float, float]:
        """Simulate training epoch (replace with actual training)"""
        # Simulate training progress
        base_loss = 2.0 - (epoch * 0.15)
        base_acc = 0.3 + (epoch * 0.06)
        
        # Add some randomness
        import random
        loss = max(0.1, base_loss + random.uniform(-0.1, 0.1))
        accuracy = min(0.95, base_acc + random.uniform(-0.05, 0.05))
        
        return loss, accuracy
    
    def _simulate_validation_epoch(self, data: List[Tuple[str, str]], epoch: int) -> Tuple[float, float]:
        """Simulate validation epoch (replace with actual validation)"""
        # Similar to training but with slightly different metrics
        base_loss = 2.1 - (epoch * 0.14)
        base_acc = 0.28 + (epoch * 0.055)
        
        import random
        loss = max(0.1, base_loss + random.uniform(-0.15, 0.15))
        accuracy = min(0.93, base_acc + random.uniform(-0.08, 0.08))
        
        return loss, accuracy
    
    def _save_model(self, model: AgentModel):
        """Save model to database and filesystem"""
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO models 
            (model_id, name, description, model_type, training_config, 
             performance_metrics, training_data_stats, created_at, version, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            model.model_id, model.name, model.description, model.model_type,
            json.dumps(asdict(model.training_config)),
            json.dumps(model.performance_metrics),
            json.dumps(model.training_data_stats),
            model.created_at, model.version, model.status
        ))
        
        # Save training history
        for metrics in self.training_history:
            cursor.execute("""
                INSERT INTO training_history 
                (model_id, epoch, loss, accuracy, validation_loss, validation_accuracy, learning_rate, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                model.model_id, metrics.epoch, metrics.loss, metrics.accuracy,
                metrics.validation_loss, metrics.validation_accuracy, metrics.learning_rate, metrics.timestamp
            ))
        
        conn.commit()
        conn.close()
        
        # Save model file
        model_file = self.models_dir / f"{model.model_id}.pkl"
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)
    
    def evaluate_model(self, model_id: str, test_data: List[Tuple[str, str]]) -> Dict[str, float]:
        """Evaluate a trained model"""
        logger.info(f"Evaluating model: {model_id}")
        
        # Load model
        model = self._load_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        # Simulate evaluation
        correct = 0
        total = len(test_data)
        response_times = []
        
        for input_text, expected_output in test_data:
            start_time = datetime.now()
            
            # Simulate model prediction
            predicted_output = self._simulate_model_prediction(input_text, model)
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            response_times.append(response_time)
            
            # Simple accuracy check (in practice, use more sophisticated metrics)
            if self._calculate_similarity(predicted_output, expected_output) > 0.7:
                correct += 1
        
        # Calculate metrics
        accuracy = correct / total if total > 0 else 0.0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        
        metrics = {
            'accuracy': accuracy,
            'precision': accuracy,  # Simplified
            'recall': accuracy,     # Simplified
            'f1_score': accuracy,   # Simplified
            'response_time': avg_response_time,
            'total_samples': total
        }
        
        # Save evaluation results
        self._save_evaluation_results(model_id, "comprehensive_test", metrics)
        
        return metrics
    
    def _simulate_model_prediction(self, input_text: str, model: AgentModel) -> str:
        """Simulate model prediction (replace with actual inference)"""
        # Simple simulation - in practice, use actual model inference
        responses = [
            f"Based on your input: {input_text[:50]}...",
            f"I understand you're asking about: {input_text[:30]}...",
            f"Here's my response to: {input_text[:40]}...",
            f"Let me help you with: {input_text[:35]}..."
        ]
        
        import random
        return random.choice(responses)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        # Simple similarity calculation
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _save_evaluation_results(self, model_id: str, test_name: str, metrics: Dict[str, float]):
        """Save evaluation results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO evaluation_results 
            (model_id, test_name, accuracy, precision, recall, f1_score, response_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            model_id, test_name, metrics['accuracy'], metrics['precision'],
            metrics['recall'], metrics['f1_score'], metrics['response_time'],
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _load_model(self, model_id: str) -> Optional[AgentModel]:
        """Load model from database and filesystem"""
        # Try loading from file first
        model_file = self.models_dir / f"{model_id}.pkl"
        if model_file.exists():
            with open(model_file, 'rb') as f:
                return pickle.load(f)
        
        # Fallback to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM models WHERE model_id = ?", (model_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Reconstruct model from database
            config_dict = json.loads(row[4])
            config = TrainingConfig(**config_dict)
            
            return AgentModel(
                model_id=row[0],
                name=row[1],
                description=row[2],
                model_type=row[3],
                training_config=config,
                performance_metrics=json.loads(row[5]),
                training_data_stats=json.loads(row[6]),
                created_at=row[7],
                version=row[8],
                status=row[9]
            )
        
        return None
    
    def get_model_list(self) -> List[AgentModel]:
        """Get list of all trained models"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM models ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        models = []
        for row in rows:
            config_dict = json.loads(row[4])
            config = TrainingConfig(**config_dict)
            
            model = AgentModel(
                model_id=row[0],
                name=row[1],
                description=row[2],
                model_type=row[3],
                training_config=config,
                performance_metrics=json.loads(row[5]),
                training_data_stats=json.loads(row[6]),
                created_at=row[7],
                version=row[8],
                status=row[9]
            )
            models.append(model)
        
        return models
    
    def get_training_history(self, model_id: str) -> List[TrainingMetrics]:
        """Get training history for a model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT epoch, loss, accuracy, validation_loss, validation_accuracy, 
                   learning_rate, timestamp
            FROM training_history 
            WHERE model_id = ? 
            ORDER BY epoch
        """, (model_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            metrics = TrainingMetrics(
                epoch=row[0],
                loss=row[1],
                accuracy=row[2],
                validation_loss=row[3],
                validation_accuracy=row[4],
                learning_rate=row[5],
                timestamp=row[6]
            )
            history.append(metrics)
        
        return history
    
    def delete_model(self, model_id: str) -> bool:
        """Delete a trained model"""
        try:
            # Delete from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM models WHERE model_id = ?", (model_id,))
            cursor.execute("DELETE FROM training_history WHERE model_id = ?", (model_id,))
            cursor.execute("DELETE FROM evaluation_results WHERE model_id = ?", (model_id,))
            
            conn.commit()
            conn.close()
            
            # Delete model file
            model_file = self.models_dir / f"{model_id}.pkl"
            if model_file.exists():
                model_file.unlink()
            
            logger.info(f"Model {model_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting model {model_id}: {e}")
            return False

def demo_agent_trainer():
    """Demo the agent trainer functionality"""
    print("=== Agent Trainer Demo ===\n")
    
    # Initialize trainer
    trainer = AgentTrainer()
    
    # Create sample training data
    sample_conversations = [
        {
            'messages': [
                {'role': 'user', 'content': 'What is machine learning?'},
                {'role': 'assistant', 'content': 'Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.'}
            ],
            'quality_score': 0.9,
            'response_quality': 0.85,
            'engagement_score': 0.8
        },
        {
            'messages': [
                {'role': 'user', 'content': 'How do neural networks work?'},
                {'role': 'assistant', 'content': 'Neural networks are computing systems inspired by biological brains, consisting of interconnected nodes that process information through weighted connections.'}
            ],
            'quality_score': 0.8,
            'response_quality': 0.9,
            'engagement_score': 0.75
        },
        {
            'messages': [
                {'role': 'user', 'content': 'Explain deep learning'},
                {'role': 'assistant', 'content': 'Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data.'}
            ],
            'quality_score': 0.85,
            'response_quality': 0.8,
            'engagement_score': 0.9
        }
    ]
    
    # Convert to training pairs
    training_pairs = []
    for conv in sample_conversations:
        messages = conv['messages']
        for i in range(len(messages) - 1):
            if messages[i]['role'] == 'user' and messages[i + 1]['role'] == 'assistant':
                training_pairs.append((messages[i]['content'], messages[i + 1]['content']))
    
    print(f"Created {len(training_pairs)} training pairs")
    
    # Configure training
    config = TrainingConfig(
        model_type="gpt-3.5-turbo",
        max_epochs=5,
        batch_size=16,
        learning_rate=0.001,
        validation_split=0.2,
        early_stopping_patience=2,
        min_quality_score=0.7,
        max_training_samples=100,
        use_augmentation=True,
        augmentation_factor=2
    )
    
    print(f"Training configuration: {config}")
    
    # Train model
    print("\n--- Starting Training ---")
    model = trainer.train_agent(
        training_pairs, 
        config, 
        model_name="AI Assistant Trainer",
        description="Trained on educational conversations about AI and ML"
    )
    
    print(f"\nTraining completed!")
    print(f"Model ID: {model.model_id}")
    print(f"Final Accuracy: {model.performance_metrics['final_accuracy']:.3f}")
    print(f"Best Validation Accuracy: {model.performance_metrics['best_validation_accuracy']:.3f}")
    
    # Evaluate model
    print("\n--- Evaluating Model ---")
    test_data = [
        ("What is artificial intelligence?", "AI is the simulation of human intelligence in machines."),
        ("How does supervised learning work?", "Supervised learning uses labeled data to train models."),
        ("Explain reinforcement learning", "Reinforcement learning learns through trial and error with rewards.")
    ]
    
    evaluation_results = trainer.evaluate_model(model.model_id, test_data)
    print(f"Evaluation Results:")
    for metric, value in evaluation_results.items():
        print(f"  {metric}: {value:.3f}")
    
    # Get model list
    print("\n--- Model Management ---")
    models = trainer.get_model_list()
    print(f"Total trained models: {len(models)}")
    for m in models:
        print(f"  - {m.name} (ID: {m.model_id}) - Accuracy: {m.performance_metrics['final_accuracy']:.3f}")
    
    # Get training history
    print("\n--- Training History ---")
    history = trainer.get_training_history(model.model_id)
    print(f"Training epochs: {len(history)}")
    for metrics in history:
        print(f"  Epoch {metrics.epoch}: Loss={metrics.loss:.3f}, Acc={metrics.accuracy:.3f}, Val_Acc={metrics.validation_accuracy:.3f}")
    
    print("\n=== Demo Completed ===")

if __name__ == "__main__":
    demo_agent_trainer() 