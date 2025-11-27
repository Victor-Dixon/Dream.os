#!/usr/bin/env python3
"""
Training Data Extraction - Training Data Generator

This module generates structured training data from analyzed conversations,
including data formatting, quality filtering, and export to various formats.

Features:
- Training data generation from conversations
- Quality filtering and validation
- Multiple export formats (JSONL, CSV, JSON)
- Data augmentation and preprocessing
- Training data statistics and analytics
"""

import json
import csv
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sqlite3
from pathlib import Path
import re
import uuid


class TrainingDataFormat(Enum):
    """Training data export formats"""
    JSONL = "jsonl"
    CSV = "csv"
    JSON = "json"
    TXT = "txt"


class DataQualityFilter(Enum):
    """Data quality filter levels"""
    ALL = "all"
    HIGH_QUALITY = "high_quality"
    EXCELLENT_ONLY = "excellent_only"
    FILTERED = "filtered"


@dataclass
class TrainingExample:
    """Individual training example"""
    id: str
    conversation_id: str
    turn_id: str
    user_input: str
    ai_response: str
    intent: str
    quality_score: float
    context: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class TrainingDataset:
    """Complete training dataset"""
    id: str
    name: str
    description: str
    examples: List[TrainingExample]
    statistics: Dict[str, Any]
    created_at: datetime
    metadata: Dict[str, Any]


class TrainingDataGenerator:
    """Generates training data from analyzed conversations"""
    
    def __init__(self, db_path: str = "conversation_analysis.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the training data database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS training_datasets (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    examples TEXT NOT NULL,
                    statistics TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """)
            conn.commit()
    
    def generate_training_data(self, conversation_ids: List[str] = None, 
                             quality_filter: DataQualityFilter = DataQualityFilter.HIGH_QUALITY,
                             max_examples: int = None) -> TrainingDataset:
        """Generate training data from conversations"""
        from conversation_analyzer import ConversationAnalyzer
        
        analyzer = ConversationAnalyzer(self.db_path)
        
        # Get conversations
        if conversation_ids:
            conversations = [analyzer.get_conversation(cid) for cid in conversation_ids if analyzer.get_conversation(cid)]
        else:
            conversations = analyzer.get_all_conversations()
        
        # Generate examples from conversations
        examples = []
        for conversation in conversations:
            conversation_examples = self._extract_training_examples(conversation, quality_filter)
            examples.extend(conversation_examples)
        
        # Apply quality filtering
        examples = self._apply_quality_filter(examples, quality_filter)
        
        # Limit examples if specified
        if max_examples and len(examples) > max_examples:
            examples = random.sample(examples, max_examples)
        
        # Generate statistics
        statistics = self._generate_statistics(examples)
        
        # Create dataset
        dataset = TrainingDataset(
            id=str(uuid.uuid4()),
            name=f"Training Dataset {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=f"Generated from {len(conversations)} conversations with {quality_filter.value} quality filter",
            examples=examples,
            statistics=statistics,
            created_at=datetime.now(),
            metadata={
                "conversation_count": len(conversations),
                "quality_filter": quality_filter.value,
                "max_examples": max_examples
            }
        )
        
        return dataset
    
    def _extract_training_examples(self, conversation, quality_filter: DataQualityFilter) -> List[TrainingExample]:
        """Extract training examples from a conversation"""
        examples = []
        
        for turn in conversation.turns:
            # Create training example
            example = TrainingExample(
                id=str(uuid.uuid4()),
                conversation_id=conversation.id,
                turn_id=turn.id,
                user_input=turn.user_message.content,
                ai_response=turn.ai_response.content,
                intent=turn.user_intent.intent_type.value,
                quality_score=self._calculate_overall_quality_score(turn.response_analysis),
                context={
                    "conversation_type": conversation.conversation_type.value,
                    "difficulty_level": conversation.difficulty_level,
                    "topics": conversation.topics,
                    "user_intent_confidence": turn.user_intent.confidence,
                    "response_quality": turn.response_analysis.quality.value,
                    "relevance_score": turn.response_analysis.relevance_score,
                    "helpfulness_score": turn.response_analysis.helpfulness_score,
                    "clarity_score": turn.response_analysis.clarity_score,
                    "completeness_score": turn.response_analysis.completeness_score
                },
                metadata={
                    "conversation_title": conversation.title,
                    "turn_number": conversation.turns.index(turn) + 1,
                    "message_count": len(conversation.messages),
                    "created_at": conversation.created_at.isoformat()
                }
            )
            
            examples.append(example)
        
        return examples
    
    def _calculate_overall_quality_score(self, response_analysis) -> float:
        """Calculate overall quality score from response analysis"""
        scores = [
            response_analysis.relevance_score,
            response_analysis.helpfulness_score,
            response_analysis.clarity_score,
            response_analysis.completeness_score
        ]
        
        # Weight the scores (relevance and helpfulness are more important)
        weights = [0.3, 0.3, 0.2, 0.2]
        weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        
        return weighted_score
    
    def _apply_quality_filter(self, examples: List[TrainingExample], 
                            quality_filter: DataQualityFilter) -> List[TrainingExample]:
        """Apply quality filtering to examples"""
        if quality_filter == DataQualityFilter.ALL:
            return examples
        
        elif quality_filter == DataQualityFilter.HIGH_QUALITY:
            return [ex for ex in examples if ex.quality_score >= 0.6]
        
        elif quality_filter == DataQualityFilter.EXCELLENT_ONLY:
            return [ex for ex in examples if ex.quality_score >= 0.8]
        
        elif quality_filter == DataQualityFilter.FILTERED:
            # Custom filtering logic
            filtered = []
            for ex in examples:
                # Filter out very short responses
                if len(ex.ai_response.split()) < 10:
                    continue
                
                # Filter out very long responses
                if len(ex.ai_response.split()) > 1000:
                    continue
                
                # Filter out low quality responses
                if ex.quality_score < 0.4:
                    continue
                
                # Filter out inappropriate content
                if self._contains_inappropriate_content(ex.ai_response):
                    continue
                
                filtered.append(ex)
            
            return filtered
        
        return examples
    
    def _contains_inappropriate_content(self, text: str) -> bool:
        """Check if text contains inappropriate content"""
        inappropriate_patterns = [
            r'\b(i don\'t know|cannot|unable|sorry)\b',
            r'\b(error|problem|issue|broken|failed)\b',
            r'\b(offensive|inappropriate|unprofessional)\b'
        ]
        
        text_lower = text.lower()
        for pattern in inappropriate_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def _generate_statistics(self, examples: List[TrainingExample]) -> Dict[str, Any]:
        """Generate statistics for the training dataset"""
        if not examples:
            return {}
        
        # Basic statistics
        total_examples = len(examples)
        avg_quality_score = sum(ex.quality_score for ex in examples) / total_examples
        
        # Intent distribution
        intent_counts = {}
        for ex in examples:
            intent_counts[ex.intent] = intent_counts.get(ex.intent, 0) + 1
        
        # Quality distribution
        quality_ranges = {
            "excellent": len([ex for ex in examples if ex.quality_score >= 0.8]),
            "good": len([ex for ex in examples if 0.6 <= ex.quality_score < 0.8]),
            "average": len([ex for ex in examples if 0.4 <= ex.quality_score < 0.6]),
            "poor": len([ex for ex in examples if ex.quality_score < 0.4])
        }
        
        # Response length statistics
        response_lengths = [len(ex.ai_response.split()) for ex in examples]
        avg_response_length = sum(response_lengths) / len(response_lengths)
        min_response_length = min(response_lengths)
        max_response_length = max(response_lengths)
        
        # User input length statistics
        input_lengths = [len(ex.user_input.split()) for ex in examples]
        avg_input_length = sum(input_lengths) / len(input_lengths)
        
        return {
            "total_examples": total_examples,
            "average_quality_score": round(avg_quality_score, 3),
            "intent_distribution": intent_counts,
            "quality_distribution": quality_ranges,
            "response_length": {
                "average": round(avg_response_length, 1),
                "minimum": min_response_length,
                "maximum": max_response_length
            },
            "input_length": {
                "average": round(avg_input_length, 1)
            }
        }
    
    def export_dataset(self, dataset: TrainingDataset, format: TrainingDataFormat, 
                      output_path: str) -> str:
        """Export dataset to specified format"""
        if format == TrainingDataFormat.JSONL:
            return self._export_jsonl(dataset, output_path)
        elif format == TrainingDataFormat.CSV:
            return self._export_csv(dataset, output_path)
        elif format == TrainingDataFormat.JSON:
            return self._export_json(dataset, output_path)
        elif format == TrainingDataFormat.TXT:
            return self._export_txt(dataset, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_jsonl(self, dataset: TrainingDataset, output_path: str) -> str:
        """Export dataset to JSONL format"""
        if not output_path.endswith('.jsonl'):
            output_path += '.jsonl'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in dataset.examples:
                json_line = {
                    "id": example.id,
                    "user_input": example.user_input,
                    "ai_response": example.ai_response,
                    "intent": example.intent,
                    "quality_score": example.quality_score,
                    "context": example.context,
                    "metadata": example.metadata
                }
                f.write(json.dumps(json_line, ensure_ascii=False) + '\n')
        
        return output_path
    
    def _export_csv(self, dataset: TrainingDataset, output_path: str) -> str:
        """Export dataset to CSV format"""
        if not output_path.endswith('.csv'):
            output_path += '.csv'
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'id', 'user_input', 'ai_response', 'intent', 'quality_score',
                'conversation_type', 'difficulty_level', 'topics',
                'relevance_score', 'helpfulness_score', 'clarity_score', 'completeness_score'
            ])
            
            # Write data
            for example in dataset.examples:
                writer.writerow([
                    example.id,
                    example.user_input,
                    example.ai_response,
                    example.intent,
                    example.quality_score,
                    example.context.get('conversation_type', ''),
                    example.context.get('difficulty_level', ''),
                    ';'.join(example.context.get('topics', [])),
                    example.context.get('relevance_score', 0),
                    example.context.get('helpfulness_score', 0),
                    example.context.get('clarity_score', 0),
                    example.context.get('completeness_score', 0)
                ])
        
        return output_path
    
    def _export_json(self, dataset: TrainingDataset, output_path: str) -> str:
        """Export dataset to JSON format"""
        if not output_path.endswith('.json'):
            output_path += '.json'
        
        dataset_dict = {
            "id": dataset.id,
            "name": dataset.name,
            "description": dataset.description,
            "statistics": dataset.statistics,
            "created_at": dataset.created_at.isoformat(),
            "metadata": dataset.metadata,
            "examples": [
                {
                    "id": ex.id,
                    "user_input": ex.user_input,
                    "ai_response": ex.ai_response,
                    "intent": ex.intent,
                    "quality_score": ex.quality_score,
                    "context": ex.context,
                    "metadata": ex.metadata
                }
                for ex in dataset.examples
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset_dict, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def _export_txt(self, dataset: TrainingDataset, output_path: str) -> str:
        """Export dataset to plain text format"""
        if not output_path.endswith('.txt'):
            output_path += '.txt'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Training Dataset: {dataset.name}\n")
            f.write(f"Description: {dataset.description}\n")
            f.write(f"Created: {dataset.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Examples: {len(dataset.examples)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, example in enumerate(dataset.examples, 1):
                f.write(f"Example {i}:\n")
                f.write(f"Intent: {example.intent}\n")
                f.write(f"Quality Score: {example.quality_score:.3f}\n")
                f.write(f"User Input: {example.user_input}\n")
                f.write(f"AI Response: {example.ai_response}\n")
                f.write("-" * 40 + "\n\n")
        
        return output_path
    
    def save_dataset(self, dataset: TrainingDataset):
        """Save dataset to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO training_datasets 
                (id, name, description, examples, statistics, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                dataset.id,
                dataset.name,
                dataset.description,
                json.dumps([{
                    'id': ex.id,
                    'conversation_id': ex.conversation_id,
                    'turn_id': ex.turn_id,
                    'user_input': ex.user_input,
                    'ai_response': ex.ai_response,
                    'intent': ex.intent,
                    'quality_score': ex.quality_score,
                    'context': ex.context,
                    'metadata': ex.metadata
                } for ex in dataset.examples]),
                json.dumps(dataset.statistics),
                dataset.created_at.isoformat(),
                json.dumps(dataset.metadata)
            ))
            conn.commit()
    
    def get_dataset(self, dataset_id: str) -> Optional[TrainingDataset]:
        """Get dataset by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM training_datasets WHERE id = ?", (dataset_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_dataset(row)
        return None
    
    def get_all_datasets(self) -> List[TrainingDataset]:
        """Get all datasets"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM training_datasets ORDER BY created_at DESC")
            return [self._row_to_dataset(row) for row in cursor.fetchall()]
    
    def _row_to_dataset(self, row) -> TrainingDataset:
        """Convert database row to TrainingDataset object"""
        examples_data = json.loads(row[3])
        
        examples = []
        for ex_data in examples_data:
            example = TrainingExample(
                id=ex_data['id'],
                conversation_id=ex_data['conversation_id'],
                turn_id=ex_data['turn_id'],
                user_input=ex_data['user_input'],
                ai_response=ex_data['ai_response'],
                intent=ex_data['intent'],
                quality_score=ex_data['quality_score'],
                context=ex_data['context'],
                metadata=ex_data['metadata']
            )
            examples.append(example)
        
        return TrainingDataset(
            id=row[0],
            name=row[1],
            description=row[2],
            examples=examples,
            statistics=json.loads(row[4]),
            created_at=datetime.fromisoformat(row[5]),
            metadata=json.loads(row[6])
        )


class TrainingDataGeneratorDemo:
    """Demo class for training data generator"""
    
    def __init__(self):
        self.generator = TrainingDataGenerator()
    
    def run_training_data_generation_demo(self):
        """Demonstrate training data generation"""
        print("=== Training Data Generation Demo ===\n")
        
        # Generate training data from existing conversations
        dataset = self.generator.generate_training_data(
            quality_filter=DataQualityFilter.HIGH_QUALITY,
            max_examples=50
        )
        
        print(f"Generated Dataset: {dataset.name}")
        print(f"Description: {dataset.description}")
        print(f"Total Examples: {len(dataset.examples)}")
        print(f"Created: {dataset.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show statistics
        stats = dataset.statistics
        print(f"\nStatistics:")
        print(f"  Average Quality Score: {stats.get('average_quality_score', 0):.3f}")
        print(f"  Intent Distribution: {stats.get('intent_distribution', {})}")
        print(f"  Quality Distribution: {stats.get('quality_distribution', {})}")
        print(f"  Average Response Length: {stats.get('response_length', {}).get('average', 0):.1f} words")
        print(f"  Average Input Length: {stats.get('input_length', {}).get('average', 0):.1f} words")
        
        # Show sample examples
        print(f"\nSample Examples:")
        for i, example in enumerate(dataset.examples[:3], 1):
            print(f"\nExample {i}:")
            print(f"  Intent: {example.intent}")
            print(f"  Quality Score: {example.quality_score:.3f}")
            print(f"  User Input: {example.user_input[:100]}...")
            print(f"  AI Response: {example.ai_response[:100]}...")
        
        # Save dataset
        self.generator.save_dataset(dataset)
        print(f"\nDataset saved with ID: {dataset.id}")
        
        return dataset
    
    def run_export_demo(self, dataset: TrainingDataset):
        """Demonstrate dataset export"""
        print("\n=== Dataset Export Demo ===\n")
        
        # Export to different formats
        export_formats = [
            TrainingDataFormat.JSONL,
            TrainingDataFormat.CSV,
            TrainingDataFormat.JSON,
            TrainingDataFormat.TXT
        ]
        
        for format_type in export_formats:
            try:
                output_path = f"training_dataset_{format_type.value}"
                exported_path = self.generator.export_dataset(dataset, format_type, output_path)
                print(f"Exported to {format_type.value.upper()}: {exported_path}")
                
                # Show file size
                file_size = Path(exported_path).stat().st_size
                print(f"  File size: {file_size:,} bytes")
                
            except Exception as e:
                print(f"Failed to export {format_type.value}: {e}")
        
        print()
    
    def run_quality_filtering_demo(self):
        """Demonstrate quality filtering"""
        print("=== Quality Filtering Demo ===\n")
        
        # Generate datasets with different quality filters
        filters = [
            DataQualityFilter.ALL,
            DataQualityFilter.HIGH_QUALITY,
            DataQualityFilter.EXCELLENT_ONLY,
            DataQualityFilter.FILTERED
        ]
        
        for filter_type in filters:
            dataset = self.generator.generate_training_data(
                quality_filter=filter_type,
                max_examples=20
            )
            
            print(f"Filter: {filter_type.value}")
            print(f"  Examples: {len(dataset.examples)}")
            print(f"  Average Quality: {dataset.statistics.get('average_quality_score', 0):.3f}")
            print(f"  Quality Distribution: {dataset.statistics.get('quality_distribution', {})}")
            print()
    
    def run_dataset_management_demo(self):
        """Demonstrate dataset management"""
        print("=== Dataset Management Demo ===\n")
        
        # Get all datasets
        datasets = self.generator.get_all_datasets()
        print(f"Total datasets: {len(datasets)}")
        
        for dataset in datasets:
            print(f"\nDataset: {dataset.name}")
            print(f"  ID: {dataset.id}")
            print(f"  Examples: {len(dataset.examples)}")
            print(f"  Created: {dataset.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Average Quality: {dataset.statistics.get('average_quality_score', 0):.3f}")
        
        print()


def main():
    """Main demo function"""
    demo = TrainingDataGeneratorDemo()
    
    try:
        # Run demos
        dataset = demo.run_training_data_generation_demo()
        demo.run_export_demo(dataset)
        demo.run_quality_filtering_demo()
        demo.run_dataset_management_demo()
        
        print("=== Training Data Generator Demo Complete ===")
        print("Training data generation system is working correctly!")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 