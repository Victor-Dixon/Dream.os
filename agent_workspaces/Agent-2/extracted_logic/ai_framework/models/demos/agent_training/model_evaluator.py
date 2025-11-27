"""
Model Evaluator - Comprehensive model testing and benchmarking system
Handles model evaluation, performance analysis, and benchmarking
"""

import json
import time
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import logging
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EvaluationTest:
    """Test case for model evaluation"""
    test_id: str
    name: str
    description: str
    input_data: List[str]
    expected_outputs: List[str]
    test_type: str  # 'accuracy', 'performance', 'robustness', 'custom'
    category: str   # 'general', 'domain_specific', 'edge_cases'
    difficulty: str # 'easy', 'medium', 'hard'

@dataclass
class EvaluationResult:
    """Result of a single evaluation test"""
    test_id: str
    model_id: str
    test_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    response_time: float
    throughput: float  # responses per second
    error_rate: float
    confidence_scores: List[float]
    timestamp: str
    metadata: Dict[str, Any]

@dataclass
class BenchmarkResult:
    """Comprehensive benchmark results"""
    benchmark_id: str
    model_id: str
    benchmark_name: str
    overall_score: float
    accuracy_score: float
    performance_score: float
    robustness_score: float
    efficiency_score: float
    test_results: List[EvaluationResult]
    summary_stats: Dict[str, float]
    timestamp: str

class ModelEvaluator:
    """Comprehensive model evaluation and benchmarking system"""
    
    def __init__(self, data_dir: str = "evaluation_data", results_dir: str = "evaluation_results"):
        self.data_dir = Path(data_dir)
        self.results_dir = Path(results_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self.db_path = self.data_dir / "model_evaluation.db"
        self._init_database()
        
        # Load test suites
        self.test_suites = self._load_test_suites()
        
    def _init_database(self):
        """Initialize evaluation database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create evaluation tests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_tests (
                test_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                input_data TEXT,
                expected_outputs TEXT,
                test_type TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL
            )
        """)
        
        # Create evaluation results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT NOT NULL,
                model_id TEXT NOT NULL,
                test_name TEXT NOT NULL,
                accuracy REAL NOT NULL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                response_time REAL,
                throughput REAL,
                error_rate REAL,
                confidence_scores TEXT,
                timestamp TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (test_id) REFERENCES evaluation_tests (test_id)
            )
        """)
        
        # Create benchmark results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_results (
                benchmark_id TEXT PRIMARY KEY,
                model_id TEXT NOT NULL,
                benchmark_name TEXT NOT NULL,
                overall_score REAL NOT NULL,
                accuracy_score REAL NOT NULL,
                performance_score REAL NOT NULL,
                robustness_score REAL NOT NULL,
                efficiency_score REAL NOT NULL,
                summary_stats TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_test_suites(self) -> Dict[str, List[EvaluationTest]]:
        """Load predefined test suites"""
        test_suites = {
            'general_knowledge': [
                EvaluationTest(
                    test_id="gk_001",
                    name="Basic Knowledge Questions",
                    description="Test basic knowledge across various domains",
                    input_data=[
                        "What is the capital of France?",
                        "Who wrote Romeo and Juliet?",
                        "What is the chemical symbol for gold?",
                        "How many planets are in our solar system?",
                        "What year did World War II end?"
                    ],
                    expected_outputs=[
                        "Paris",
                        "William Shakespeare",
                        "Au",
                        "8",
                        "1945"
                    ],
                    test_type="accuracy",
                    category="general",
                    difficulty="easy"
                )
            ],
            'reasoning': [
                EvaluationTest(
                    test_id="reasoning_001",
                    name="Logical Reasoning",
                    description="Test logical reasoning and problem-solving abilities",
                    input_data=[
                        "If all roses are flowers and some flowers are red, can we conclude that some roses are red?",
                        "A train leaves station A at 2 PM traveling 60 mph. Another train leaves station B at 3 PM traveling 80 mph. If the stations are 300 miles apart, when will they meet?",
                        "If 3 workers can complete a task in 6 days, how many days will it take 2 workers to complete the same task?"
                    ],
                    expected_outputs=[
                        "No, we cannot conclude that some roses are red from the given premises.",
                        "The trains will meet at 5:30 PM.",
                        "It will take 9 days for 2 workers to complete the task."
                    ],
                    test_type="accuracy",
                    category="general",
                    difficulty="medium"
                )
            ],
            'creativity': [
                EvaluationTest(
                    test_id="creative_001",
                    name="Creative Writing",
                    description="Test creative writing and storytelling abilities",
                    input_data=[
                        "Write a short story about a robot learning to paint.",
                        "Create a poem about artificial intelligence.",
                        "Describe a futuristic city in 100 words."
                    ],
                    expected_outputs=[
                        "A creative story about a robot learning to paint",
                        "A poem about artificial intelligence",
                        "A description of a futuristic city"
                    ],
                    test_type="accuracy",
                    category="general",
                    difficulty="hard"
                )
            ],
            'performance': [
                EvaluationTest(
                    test_id="perf_001",
                    name="Response Time Test",
                    description="Test response time under various conditions",
                    input_data=["Hello"] * 100,  # 100 simple requests
                    expected_outputs=["Hi there"] * 100,
                    test_type="performance",
                    category="general",
                    difficulty="easy"
                )
            ],
            'robustness': [
                EvaluationTest(
                    test_id="robust_001",
                    name="Edge Case Handling",
                    description="Test handling of edge cases and unusual inputs",
                    input_data=[
                        "",  # Empty input
                        "A" * 1000,  # Very long input
                        "!@#$%^&*()",  # Special characters
                        "1234567890",  # Numbers only
                        "   spaces   ",  # Extra spaces
                        "UPPERCASE ONLY",
                        "mixed CASE input"
                    ],
                    expected_outputs=[
                        "Empty input detected",
                        "Long input processed",
                        "Special characters handled",
                        "Numbers processed",
                        "Spaces normalized",
                        "Case handled",
                        "Mixed case processed"
                    ],
                    test_type="robustness",
                    category="edge_cases",
                    difficulty="medium"
                )
            ]
        }
        
        return test_suites
    
    def run_single_test(self, test: EvaluationTest, model_predictor) -> EvaluationResult:
        """Run a single evaluation test"""
        logger.info(f"Running test: {test.name}")
        
        start_time = time.time()
        predictions = []
        confidence_scores = []
        errors = 0
        
        for i, input_text in enumerate(test.input_data):
            try:
                # Simulate model prediction
                prediction_start = time.time()
                prediction = self._simulate_model_prediction(input_text, model_predictor)
                prediction_time = time.time() - prediction_start
                
                predictions.append(prediction)
                confidence_scores.append(self._calculate_confidence(prediction))
                
            except Exception as e:
                logger.error(f"Error in prediction {i}: {e}")
                predictions.append("ERROR")
                confidence_scores.append(0.0)
                errors += 1
        
        total_time = time.time() - start_time
        
        # Calculate metrics
        accuracy = self._calculate_accuracy(predictions, test.expected_outputs)
        precision, recall, f1_score = self._calculate_precision_recall_f1(
            predictions, test.expected_outputs
        )
        
        response_time = total_time / len(test.input_data) if test.input_data else 0
        throughput = len(test.input_data) / total_time if total_time > 0 else 0
        error_rate = errors / len(test.input_data) if test.input_data else 0
        
        result = EvaluationResult(
            test_id=test.test_id,
            model_id="demo_model",  # In practice, get from model_predictor
            test_name=test.name,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            response_time=response_time,
            throughput=throughput,
            error_rate=error_rate,
            confidence_scores=confidence_scores,
            timestamp=datetime.now().isoformat(),
            metadata={
                'test_type': test.test_type,
                'category': test.category,
                'difficulty': test.difficulty,
                'total_samples': len(test.input_data)
            }
        )
        
        return result
    
    def _simulate_model_prediction(self, input_text: str, model_predictor) -> str:
        """Simulate model prediction (replace with actual model inference)"""
        # Simple simulation - in practice, use actual model inference
        import random
        
        if not input_text.strip():
            return "Empty input detected"
        
        if len(input_text) > 500:
            return "Long input processed"
        
        if input_text.isupper():
            return "Uppercase input processed"
        
        if input_text.isdigit():
            return "Numeric input processed"
        
        # Simulate different response types
        responses = [
            f"I understand: {input_text[:50]}...",
            f"Here's my response to: {input_text[:40]}...",
            f"Based on your input: {input_text[:45]}...",
            f"Let me help you with: {input_text[:35]}..."
        ]
        
        return random.choice(responses)
    
    def _calculate_confidence(self, prediction: str) -> float:
        """Calculate confidence score for a prediction"""
        # Simple confidence calculation based on response characteristics
        if not prediction or prediction == "ERROR":
            return 0.0
        
        # Higher confidence for longer, more detailed responses
        confidence = min(1.0, len(prediction) / 100.0)
        
        # Boost confidence for certain response patterns
        if "I understand" in prediction or "Here's my response" in prediction:
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _calculate_accuracy(self, predictions: List[str], expected: List[str]) -> float:
        """Calculate accuracy between predictions and expected outputs"""
        if not predictions or not expected:
            return 0.0
        
        correct = 0
        for pred, exp in zip(predictions, expected):
            if self._calculate_similarity(pred, exp) > 0.7:
                correct += 1
        
        return correct / len(predictions)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _calculate_precision_recall_f1(self, predictions: List[str], expected: List[str]) -> Tuple[float, float, float]:
        """Calculate precision, recall, and F1 score"""
        # Simplified calculation - in practice, use more sophisticated metrics
        accuracy = self._calculate_accuracy(predictions, expected)
        
        # For simplicity, assume precision and recall are similar to accuracy
        precision = accuracy
        recall = accuracy
        
        # Calculate F1 score
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0.0
        
        return precision, recall, f1_score
    
    def run_benchmark_suite(self, suite_name: str, model_predictor) -> BenchmarkResult:
        """Run a complete benchmark suite"""
        logger.info(f"Running benchmark suite: {suite_name}")
        
        if suite_name not in self.test_suites:
            raise ValueError(f"Test suite '{suite_name}' not found")
        
        tests = self.test_suites[suite_name]
        results = []
        
        for test in tests:
            result = self.run_single_test(test, model_predictor)
            results.append(result)
            self._save_evaluation_result(result)
        
        # Calculate overall scores
        accuracy_score = np.mean([r.accuracy for r in results])
        performance_score = np.mean([1.0 / (r.response_time + 0.1) for r in results])  # Inverse of response time
        robustness_score = 1.0 - np.mean([r.error_rate for r in results])
        efficiency_score = np.mean([r.throughput for r in results]) / 100.0  # Normalized throughput
        
        overall_score = (accuracy_score + performance_score + robustness_score + efficiency_score) / 4.0
        
        # Calculate summary statistics
        summary_stats = {
            'total_tests': len(results),
            'avg_accuracy': accuracy_score,
            'avg_response_time': np.mean([r.response_time for r in results]),
            'avg_throughput': np.mean([r.throughput for r in results]),
            'avg_error_rate': np.mean([r.error_rate for r in results]),
            'best_test': max(results, key=lambda r: r.accuracy).test_name,
            'worst_test': min(results, key=lambda r: r.accuracy).test_name
        }
        
        benchmark_result = BenchmarkResult(
            benchmark_id=f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_id="demo_model",
            benchmark_name=suite_name,
            overall_score=overall_score,
            accuracy_score=accuracy_score,
            performance_score=performance_score,
            robustness_score=robustness_score,
            efficiency_score=efficiency_score,
            test_results=results,
            summary_stats=summary_stats,
            timestamp=datetime.now().isoformat()
        )
        
        self._save_benchmark_result(benchmark_result)
        
        return benchmark_result
    
    def run_comprehensive_evaluation(self, model_predictor) -> Dict[str, BenchmarkResult]:
        """Run evaluation across all test suites"""
        logger.info("Running comprehensive evaluation across all test suites")
        
        all_results = {}
        
        for suite_name in self.test_suites.keys():
            try:
                result = self.run_benchmark_suite(suite_name, model_predictor)
                all_results[suite_name] = result
                logger.info(f"Completed {suite_name}: Overall Score = {result.overall_score:.3f}")
            except Exception as e:
                logger.error(f"Error running suite {suite_name}: {e}")
        
        return all_results
    
    def _save_evaluation_result(self, result: EvaluationResult):
        """Save evaluation result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO evaluation_results 
            (test_id, model_id, test_name, accuracy, precision, recall, f1_score,
             response_time, throughput, error_rate, confidence_scores, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.test_id, result.model_id, result.test_name, result.accuracy,
            result.precision, result.recall, result.f1_score, result.response_time,
            result.throughput, result.error_rate, json.dumps(result.confidence_scores),
            result.timestamp, json.dumps(result.metadata)
        ))
        
        conn.commit()
        conn.close()
    
    def _save_benchmark_result(self, result: BenchmarkResult):
        """Save benchmark result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO benchmark_results 
            (benchmark_id, model_id, benchmark_name, overall_score, accuracy_score,
             performance_score, robustness_score, efficiency_score, summary_stats, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.benchmark_id, result.model_id, result.benchmark_name, result.overall_score,
            result.accuracy_score, result.performance_score, result.robustness_score,
            result.efficiency_score, json.dumps(result.summary_stats), result.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def get_evaluation_history(self, model_id: str = None) -> List[EvaluationResult]:
        """Get evaluation history for a model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if model_id:
            cursor.execute("""
                SELECT test_id, model_id, test_name, accuracy, precision, recall, f1_score,
                       response_time, throughput, error_rate, confidence_scores, timestamp, metadata
                FROM evaluation_results 
                WHERE model_id = ? 
                ORDER BY timestamp DESC
            """, (model_id,))
        else:
            cursor.execute("""
                SELECT test_id, model_id, test_name, accuracy, precision, recall, f1_score,
                       response_time, throughput, error_rate, confidence_scores, timestamp, metadata
                FROM evaluation_results 
                ORDER BY timestamp DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            result = EvaluationResult(
                test_id=row[0],
                model_id=row[1],
                test_name=row[2],
                accuracy=row[3],
                precision=row[4],
                recall=row[5],
                f1_score=row[6],
                response_time=row[7],
                throughput=row[8],
                error_rate=row[9],
                confidence_scores=json.loads(row[10]),
                timestamp=row[11],
                metadata=json.loads(row[12])
            )
            results.append(result)
        
        return results
    
    def get_benchmark_history(self, model_id: str = None) -> List[BenchmarkResult]:
        """Get benchmark history for a model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if model_id:
            cursor.execute("""
                SELECT benchmark_id, model_id, benchmark_name, overall_score, accuracy_score,
                       performance_score, robustness_score, efficiency_score, summary_stats, timestamp
                FROM benchmark_results 
                WHERE model_id = ? 
                ORDER BY timestamp DESC
            """, (model_id,))
        else:
            cursor.execute("""
                SELECT benchmark_id, model_id, benchmark_name, overall_score, accuracy_score,
                       performance_score, robustness_score, efficiency_score, summary_stats, timestamp
                FROM benchmark_results 
                ORDER BY timestamp DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            result = BenchmarkResult(
                benchmark_id=row[0],
                model_id=row[1],
                benchmark_name=row[2],
                overall_score=row[3],
                accuracy_score=row[4],
                performance_score=row[5],
                robustness_score=row[6],
                efficiency_score=row[7],
                test_results=[],  # Would need separate query to populate
                summary_stats=json.loads(row[8]),
                timestamp=row[9]
            )
            results.append(result)
        
        return results
    
    def generate_evaluation_report(self, benchmark_results: Dict[str, BenchmarkResult]) -> str:
        """Generate a comprehensive evaluation report"""
        report = []
        report.append("# Model Evaluation Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall summary
        overall_scores = [r.overall_score for r in benchmark_results.values()]
        avg_overall = np.mean(overall_scores)
        
        report.append("## Overall Summary")
        report.append(f"- **Average Overall Score**: {avg_overall:.3f}")
        report.append(f"- **Number of Test Suites**: {len(benchmark_results)}")
        report.append(f"- **Best Performing Suite**: {max(benchmark_results.items(), key=lambda x: x[1].overall_score)[0]}")
        report.append("")
        
        # Detailed results by suite
        report.append("## Detailed Results")
        for suite_name, result in benchmark_results.items():
            report.append(f"### {suite_name.replace('_', ' ').title()}")
            report.append(f"- **Overall Score**: {result.overall_score:.3f}")
            report.append(f"- **Accuracy Score**: {result.accuracy_score:.3f}")
            report.append(f"- **Performance Score**: {result.performance_score:.3f}")
            report.append(f"- **Robustness Score**: {result.robustness_score:.3f}")
            report.append(f"- **Efficiency Score**: {result.efficiency_score:.3f}")
            report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        if avg_overall < 0.5:
            report.append("- **Critical**: Model needs significant improvement across all metrics")
        elif avg_overall < 0.7:
            report.append("- **Warning**: Model shows moderate performance, consider retraining")
        elif avg_overall < 0.9:
            report.append("- **Good**: Model performs well, minor optimizations recommended")
        else:
            report.append("- **Excellent**: Model performs exceptionally well")
        
        return "\n".join(report)

def demo_model_evaluator():
    """Demo the model evaluator functionality"""
    print("=== Model Evaluator Demo ===\n")
    
    # Initialize evaluator
    evaluator = ModelEvaluator()
    
    # Create a simple model predictor (simulation)
    class DemoModelPredictor:
        def predict(self, input_text):
            return evaluator._simulate_model_prediction(input_text, self)
    
    model_predictor = DemoModelPredictor()
    
    print("Available test suites:")
    for suite_name in evaluator.test_suites.keys():
        print(f"  - {suite_name}")
    
    # Run individual test
    print("\n--- Running Single Test ---")
    test = evaluator.test_suites['general_knowledge'][0]
    result = evaluator.run_single_test(test, model_predictor)
    
    print(f"Test: {result.test_name}")
    print(f"Accuracy: {result.accuracy:.3f}")
    print(f"Response Time: {result.response_time:.3f}s")
    print(f"Throughput: {result.throughput:.1f} responses/sec")
    print(f"Error Rate: {result.error_rate:.3f}")
    
    # Run benchmark suite
    print("\n--- Running Benchmark Suite ---")
    benchmark_result = evaluator.run_benchmark_suite('general_knowledge', model_predictor)
    
    print(f"Benchmark: {benchmark_result.benchmark_name}")
    print(f"Overall Score: {benchmark_result.overall_score:.3f}")
    print(f"Accuracy Score: {benchmark_result.accuracy_score:.3f}")
    print(f"Performance Score: {benchmark_result.performance_score:.3f}")
    print(f"Robustness Score: {benchmark_result.robustness_score:.3f}")
    print(f"Efficiency Score: {benchmark_result.efficiency_score:.3f}")
    
    # Run comprehensive evaluation
    print("\n--- Running Comprehensive Evaluation ---")
    all_results = evaluator.run_comprehensive_evaluation(model_predictor)
    
    print("Comprehensive Results:")
    for suite_name, result in all_results.items():
        print(f"  {suite_name}: {result.overall_score:.3f}")
    
    # Generate report
    print("\n--- Generating Evaluation Report ---")
    report = evaluator.generate_evaluation_report(all_results)
    print(report)
    
    # Save report
    report_file = evaluator.results_dir / f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")
    
    print("\n=== Demo Completed ===")

if __name__ == "__main__":
    demo_model_evaluator() 