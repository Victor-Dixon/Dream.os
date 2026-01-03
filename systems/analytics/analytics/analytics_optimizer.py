#!/usr/bin/env python3
"""
Analytics Optimizer - Performance optimization for analytics features
===================================================================

Provides performance optimizations for:
- Topic analysis caching and parallel processing
- Time series data optimization
- Memory management and cleanup
- Export performance improvements
"""

import logging
import time
import threading
from typing import Dict, List, Optional, Any, Callable
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
from functools import lru_cache, wraps
import hashlib
import json

# Optional dependencies for advanced optimizations
try:
    import numpy as np
    import pandas as pd
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
    ADVANCED_OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    ADVANCED_OPTIMIZATIONS_AVAILABLE = False
    logging.warning("Advanced optimizations not available. Install numpy and pandas for full functionality.")

logger = logging.getLogger(__name__)


class AnalyticsCache:
    """LRU cache for analytics results."""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache = OrderedDict()
        self.lock = threading.Lock()
    
    def _generate_key(self, data: Any, method: str, **kwargs) -> str:
        """Generate cache key from data and parameters."""
        # Create a hash of the data and parameters
        key_data = {
            'data_hash': self._hash_data(data),
            'method': method,
            'kwargs': sorted(kwargs.items())
        }
        return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
    
    def _hash_data(self, data: Any) -> str:
        """Generate hash for data."""
        if isinstance(data, list):
            # Hash the first few items and length for performance
            sample_data = data[:10] if len(data) > 10 else data
            return hashlib.md5(str(sample_data).encode()).hexdigest()
        else:
            return hashlib.md5(str(data).encode()).hexdigest()
    
    def get(self, data: Any, method: str, **kwargs) -> Optional[Any]:
        """Get cached result."""
        key = self._generate_key(data, method, **kwargs)
        
        with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                result = self.cache.pop(key)
                self.cache[key] = result
                logger.debug(f"Cache hit for key: {key[:8]}...")
                return result
        
        logger.debug(f"Cache miss for key: {key[:8]}...")
        return None
    
    def set(self, data: Any, method: str, result: Any, **kwargs) -> None:
        """Set cached result."""
        key = self._generate_key(data, method, **kwargs)
        
        with self.lock:
            if key in self.cache:
                # Update existing entry
                self.cache.pop(key)
            elif len(self.cache) >= self.max_size:
                # Remove least recently used
                self.cache.popitem(last=False)
            
            self.cache[key] = result
            logger.debug(f"Cached result for key: {key[:8]}...")
    
    def clear(self) -> None:
        """Clear all cached results."""
        with self.lock:
            self.cache.clear()
        logger.info("Analytics cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'utilization': len(self.cache) / self.max_size
            }


class AnalyticsOptimizer:
    """Performance optimizer for analytics features."""
    
    def __init__(self):
        self.cache = AnalyticsCache(max_size=200)
        self.performance_metrics = defaultdict(list)
        self.optimization_enabled = True
        
    def enable_optimizations(self, enabled: bool = True):
        """Enable or disable optimizations."""
        self.optimization_enabled = enabled
        logger.info(f"Analytics optimizations {'enabled' if enabled else 'disabled'}")
    
    def performance_monitor(self, func: Callable) -> Callable:
        """Decorator to monitor function performance."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.optimization_enabled:
                return func(*args, **kwargs)
            
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Record performance metric
            self.performance_metrics[func.__name__].append(execution_time)
            
            # Log slow operations
            if execution_time > 1.0:  # Log operations taking more than 1 second
                logger.warning(f"Slow operation detected: {func.__name__} took {execution_time:.2f}s")
            
            return result
        return wrapper
    
    def cached_operation(self, cache_key: str = None):
        """Decorator for cached operations."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.optimization_enabled:
                    return func(*args, **kwargs)
                
                # Use provided cache key or generate from function name
                key = cache_key or func.__name__
                
                # Try to get from cache
                cached_result = self.cache.get(args[0] if args else None, key, **kwargs)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                self.cache.set(args[0] if args else None, key, result, **kwargs)
                
                return result
            return wrapper
        return decorator
    
    def parallel_processing(self, max_workers: int = 4):
        """Decorator for parallel processing."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(data: List[Any], *args, **kwargs):
                if not self.optimization_enabled or not ADVANCED_OPTIMIZATIONS_AVAILABLE:
                    return func(data, *args, **kwargs)
                
                # Split data into chunks for parallel processing
                chunk_size = max(1, len(data) // max_workers)
                chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = [executor.submit(func, chunk, *args, **kwargs) for chunk in chunks]
                    results = [future.result() for future in futures]
                
                # Combine results
                return self._combine_results(results)
            return wrapper
        return decorator
    
    def _combine_results(self, results: List[Any]) -> Any:
        """Combine results from parallel processing."""
        if not results:
            return []
        
        # Handle different result types
        if isinstance(results[0], dict):
            # Combine dictionaries
            combined = {}
            for result in results:
                combined.update(result)
            return combined
        elif isinstance(results[0], list):
            # Combine lists
            return [item for sublist in results for item in sublist]
        else:
            # Return as is
            return results
    
    def optimize_topic_analysis(self, conversations: List[Dict[str, Any]], 
                              method: str = 'simple', max_topics: int = 50) -> Dict[str, Any]:
        """Optimized topic analysis with caching and parallel processing."""
        from dreamscape.core.topic_analyzer import TopicAnalyzer
        
        analyzer = TopicAnalyzer()
        
        @self.cached_operation("topic_analysis")
        @self.performance_monitor
        def analyze_topics(conv_data, analysis_method, max_topic_count):
            return analyzer.get_conversation_topics(conv_data, method=analysis_method, max_topics=max_topic_count)
        
        return analyze_topics(conversations, method, max_topics)
    
    def optimize_time_series_analysis(self, conversations: List[Dict[str, Any]], 
                                    period: str = 'daily', days: int = 30) -> Dict[str, Any]:
        """Optimized time series analysis with caching."""
        from dreamscape.core.time_series_analyzer import TimeSeriesAnalyzer
        
        analyzer = TimeSeriesAnalyzer()
        
        @self.cached_operation("time_series_analysis")
        @self.performance_monitor
        def analyze_time_series(conv_data, time_period, day_count):
            return analyzer.get_conversation_time_series(conv_data, period=time_period, days=day_count)
        
        return analyze_time_series(conversations, period, days)
    
    def optimize_export(self, data: Any, file_path: str, format: str = 'csv') -> str:
        """Optimized export with performance monitoring."""
        from dreamscape.core.export_manager import ExportManager
        
        export_manager = ExportManager()
        
        @self.performance_monitor
        def export_data(export_data, path, export_format):
            if format == 'csv':
                return export_manager.export_analytics_data(export_data, path, 'csv')
            elif format == 'json':
                return export_manager.export_analytics_data(export_data, path, 'json')
            elif format == 'pdf':
                return export_manager.export_analytics_data(export_data, path, 'pdf')
            else:
                raise ValueError(f"Unsupported format: {format}")
        
        return export_data(data, file_path, format)
    
    def batch_processing(self, conversations: List[Dict[str, Any]], 
                        operations: List[str]) -> Dict[str, Any]:
        """Process multiple analytics operations in batch."""
        results = {}
        
        for operation in operations:
            try:
                if operation == 'topic_analysis':
                    results[operation] = self.optimize_topic_analysis(conversations)
                elif operation == 'time_series_analysis':
                    results[operation] = self.optimize_time_series_analysis(conversations)
                elif operation == 'trend_analysis':
                    time_series = self.optimize_time_series_analysis(conversations)
                    results[operation] = time_series.get('trends', {})
                else:
                    logger.warning(f"Unknown operation: {operation}")
            except Exception as e:
                logger.error(f"Failed to process operation {operation}: {e}")
                results[operation] = None
        
        return results
    
    def memory_optimization(self, conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize memory usage for large conversation datasets."""
        if not ADVANCED_OPTIMIZATIONS_AVAILABLE:
            return conversations
        
        try:
            # Convert to pandas DataFrame for memory optimization
            df = pd.DataFrame(conversations)
            
            # Optimize data types
            df['message_count'] = pd.to_numeric(df['message_count'], downcast='integer')
            df['word_count'] = pd.to_numeric(df['word_count'], downcast='integer')
            
            # Convert back to list of dictionaries
            optimized_conversations = df.to_dict('records')
            
            logger.info(f"Memory optimization: reduced memory usage for {len(conversations)} conversations")
            return optimized_conversations
            
        except Exception as e:
            logger.warning(f"Memory optimization failed: {e}")
            return conversations
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report."""
        report = {
            'cache_stats': self.cache.get_stats(),
            'performance_metrics': {},
            'optimization_status': self.optimization_enabled
        }
        
        # Calculate performance statistics
        for operation, times in self.performance_metrics.items():
            if times:
                report['performance_metrics'][operation] = {
                    'count': len(times),
                    'average_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_time': sum(times)
                }
        
        return report
    
    def clear_cache(self):
        """Clear all caches."""
        self.cache.clear()
        self.performance_metrics.clear()
        logger.info("All caches and performance metrics cleared")
    
    def optimize_for_large_datasets(self, conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Special optimizations for large datasets."""
        if len(conversations) < 1000:
            # No special optimization needed for small datasets
            return self.batch_processing(conversations, ['topic_analysis', 'time_series_analysis'])
        
        logger.info(f"Applying large dataset optimizations for {len(conversations)} conversations")
        
        # Memory optimization
        optimized_conversations = self.memory_optimization(conversations)
        
        # Parallel processing for large datasets
        @self.parallel_processing(max_workers=4)
        def process_chunk(chunk_data):
            return self.batch_processing(chunk_data, ['topic_analysis', 'time_series_analysis'])
        
        # Split data into chunks
        chunk_size = len(optimized_conversations) // 4
        chunks = [optimized_conversations[i:i + chunk_size] 
                 for i in range(0, len(optimized_conversations), chunk_size)]
        
        # Process chunks in parallel
        chunk_results = process_chunk(chunks)
        
        # Combine results
        combined_results = {}
        for operation in ['topic_analysis', 'time_series_analysis']:
            if operation in chunk_results[0]:
                combined_results[operation] = self._combine_operation_results(
                    [chunk[operation] for chunk in chunk_results if chunk[operation]]
                )
        
        return combined_results
    
    def _combine_operation_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine results from different chunks."""
        if not results:
            return {}
        
        if 'topics' in results[0]:
            # Combine topic analysis results
            all_topics = []
            total_conversations = 0
            total_words = 0
            
            for result in results:
                all_topics.extend(result.get('topics', []))
                total_conversations += result.get('total_conversations', 0)
                total_words += result.get('total_words', 0)
            
            # Aggregate topic frequencies
            topic_freq = defaultdict(int)
            for topic in all_topics:
                topic_freq[topic['word']] += topic['frequency']
            
            # Create combined result
            combined_topics = []
            for word, freq in sorted(topic_freq.items(), key=lambda x: x[1], reverse=True):
                combined_topics.append({
                    'word': word,
                    'frequency': freq,
                    'weight': freq / total_conversations,
                    'percentage': (freq / sum(topic_freq.values())) * 100
                })
            
            return {
                'topics': combined_topics,
                'total_conversations': total_conversations,
                'total_words': total_words,
                'analysis_method': 'optimized_batch'
            }
        
        elif 'time_series' in results[0]:
            # Combine time series results
            all_time_series = []
            all_chart_data = {}
            all_trends = {}
            
            for result in results:
                all_time_series.extend(result.get('time_series', []))
                
                # Combine chart data
                for metric, data in result.get('chart_data', {}).items():
                    if metric not in all_chart_data:
                        all_chart_data[metric] = {'labels': [], 'data': []}
                    all_chart_data[metric]['labels'].extend(data.get('labels', []))
                    all_chart_data[metric]['data'].extend(data.get('data', []))
                
                # Combine trends (take average)
                for metric, trend in result.get('trends', {}).items():
                    if metric not in all_trends:
                        all_trends[metric] = trend
                    else:
                        # Average the trends
                        all_trends[metric]['change_percentage'] = (
                            all_trends[metric]['change_percentage'] + trend['change_percentage']
                        ) / 2
            
            return {
                'time_series': all_time_series,
                'chart_data': all_chart_data,
                'trends': all_trends,
                'period': 'optimized_batch'
            }
        
        return results[0] if results else {}


# Global optimizer instance
analytics_optimizer = AnalyticsOptimizer()


def get_optimizer() -> AnalyticsOptimizer:
    """Get the global analytics optimizer instance."""
    return analytics_optimizer 