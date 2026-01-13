#!/usr/bin/env python3
"""
Topic Analyzer - Core module for topic extraction and analysis
============================================================

Provides functionality to:
- Extract topics from conversation content using TF-IDF
- Generate topic clouds with frequency data
- Analyze topic trends over time
- Export topic data for visualization
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import json
from pathlib import Path

# Optional dependencies for advanced topic analysis
try:
    import numpy as np
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    ADVANCED_ANALYSIS_AVAILABLE = True
except ImportError:
    ADVANCED_ANALYSIS_AVAILABLE = False
    logging.warning("Advanced topic analysis not available. Install scikit-learn for full functionality.")

# EDIT START: Use parse_date_safe from common_utils for all date parsing
from dreamscape.core.utils.common_utils import parse_date_safe
# EDIT END

logger = logging.getLogger(__name__)


class TopicAnalyzer:
    """Core topic analysis functionality."""
    
    def __init__(self):
        self.vectorizer = None
        self.lda_model = None
        self.stop_words = self._load_stop_words()
        
    def _load_stop_words(self) -> set:
        """Load common stop words for filtering."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers',
            'ours', 'theirs', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when',
            'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'now', 'then', 'here', 'there', 'when', 'where',
            'why', 'how', 'again', 'ever', 'far', 'late', 'never', 'next', 'once',
            'soon', 'still', 'then', 'today', 'tomorrow', 'yesterday', 'above', 'below',
            'down', 'up', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such'
        }
    
    def extract_topics_simple(self, texts: List[str], max_topics: int = 50) -> List[Dict[str, Any]]:
        """
        Extract topics using simple word frequency analysis.
        
        Args:
            texts: List of text documents to analyze
            max_topics: Maximum number of topics to return
            
        Returns:
            List of topic dictionaries with 'word', 'frequency', and 'weight'
        """
        if not texts:
            return []
        
        # Combine all texts
        combined_text = ' '.join(texts).lower()
        
        # Extract words (simple approach)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', combined_text)
        
        # Filter out stop words and count frequencies
        word_counts = Counter()
        for word in words:
            if word not in self.stop_words and len(word) > 2:
                word_counts[word] += 1
        
        # Get top topics
        topics = []
        for word, count in word_counts.most_common(max_topics):
            # Calculate weight (normalized frequency)
            weight = count / len(texts)
            topics.append({
                'word': word,
                'frequency': count,
                'weight': round(weight, 4),
                'percentage': round((count / sum(word_counts.values())) * 100, 2)
            })
        
        return topics
    
    def extract_topics_advanced(self, texts: List[str], max_topics: int = 50, 
                              min_frequency: int = 2) -> List[Dict[str, Any]]:
        """
        Extract topics using TF-IDF analysis (requires scikit-learn).
        
        Args:
            texts: List of text documents to analyze
            max_topics: Maximum number of topics to return
            min_frequency: Minimum word frequency to include
            
        Returns:
            List of topic dictionaries with advanced metrics
        """
        if not ADVANCED_ANALYSIS_AVAILABLE:
            logger.warning("Advanced analysis not available, falling back to simple analysis")
            return self.extract_topics_simple(texts, max_topics)
        
        if not texts:
            return []
        
        try:
            # Initialize TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=max_topics * 2,
                min_df=min_frequency,
                max_df=0.95,
                stop_words='english',
                ngram_range=(1, 2),  # Include bigrams
                lowercase=True
            )
            
            # Fit and transform
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Calculate average TF-IDF scores
            avg_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Create topic list
            topics = []
            for i, (feature, score) in enumerate(zip(feature_names, avg_scores)):
                if score > 0:
                    # Count frequency
                    frequency = sum(1 for text in texts if feature.lower() in text.lower())
                    
                    topics.append({
                        'word': feature,
                        'frequency': frequency,
                        'weight': round(float(score), 4),
                        'tfidf_score': round(float(score), 4),
                        'percentage': round((frequency / len(texts)) * 100, 2)
                    })
            
            # Sort by TF-IDF score and return top topics
            topics.sort(key=lambda x: x['tfidf_score'], reverse=True)
            return topics[:max_topics]
            
        except Exception as e:
            logger.error(f"Advanced topic extraction failed: {e}")
            return self.extract_topics_simple(texts, max_topics)
    
    def analyze_topic_trends(self, conversations: List[Dict[str, Any]], 
                           days: int = 30) -> Dict[str, Any]:
        """
        Analyze topic trends over time.
        
        Args:
            conversations: List of conversation dictionaries with 'content' and 'created_at'
            days: Number of days to analyze
            
        Returns:
            Dictionary with daily topic trends
        """
        if not conversations:
            return {}
        
        # Group conversations by date
        daily_topics = defaultdict(list)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for conv in conversations:
            try:
                # Parse date
                conv_date = parse_date_safe(conv.get('created_at'))
                
                # Filter by date range
                if conv_date >= cutoff_date:
                    date_key = conv_date.strftime('%Y-%m-%d')
                    content = conv.get('content', '')
                    if content:
                        daily_topics[date_key].append(content)
            except Exception as e:
                logger.warning(f"Error processing conversation date: {e}")
                continue
        
        # Analyze topics for each day
        trends = {}
        for date, texts in daily_topics.items():
            if texts:
                topics = self.extract_topics_simple(texts, max_topics=20)
                trends[date] = {
                    'conversation_count': len(texts),
                    'top_topics': topics[:10],
                    'total_words': sum(len(text.split()) for text in texts)
                }
        
        return trends
    
    def generate_topic_cloud_data(self, topics: List[Dict[str, Any]], 
                                max_size: int = 100) -> List[Dict[str, Any]]:
        """
        Generate data optimized for topic cloud visualization.
        
        Args:
            topics: List of topic dictionaries
            max_size: Maximum number of topics to include
            
        Returns:
            List of topic cloud data points
        """
        if not topics:
            return []
        
        # Sort by frequency and take top topics
        sorted_topics = sorted(topics, key=lambda x: x['frequency'], reverse=True)[:max_size]
        
        # Calculate size ranges for visualization
        max_freq = max(topic['frequency'] for topic in sorted_topics) if sorted_topics else 1
        
        cloud_data = []
        for topic in sorted_topics:
            # Calculate relative size (1-100)
            relative_size = int((topic['frequency'] / max_freq) * 100)
            relative_size = max(10, min(100, relative_size))  # Clamp between 10-100
            
            cloud_data.append({
                'text': topic['word'],
                'size': relative_size,
                'frequency': topic['frequency'],
                'weight': topic['weight'],
                'percentage': topic['percentage']
            })
        
        return cloud_data
    
    def export_topics_csv(self, topics: List[Dict[str, Any]], file_path: str) -> str:
        """
        Export topics to CSV format.
        
        Args:
            topics: List of topic dictionaries
            file_path: Output file path
            
        Returns:
            Path to exported file
        """
        try:
            import csv
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['word', 'frequency', 'weight', 'percentage'])
                writer.writeheader()
                
                for topic in topics:
                    writer.writerow({
                        'word': topic['word'],
                        'frequency': topic['frequency'],
                        'weight': topic['weight'],
                        'percentage': topic['percentage']
                    })
            
            logger.info(f"Topics exported to CSV: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to export topics to CSV: {e}")
            raise
    
    def export_topics_json(self, topics: List[Dict[str, Any]], file_path: str) -> str:
        """
        Export topics to JSON format.
        
        Args:
            topics: List of topic dictionaries
            file_path: Output file path
            
        Returns:
            Path to exported file
        """
        try:
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_topics': len(topics),
                'topics': topics
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Topics exported to JSON: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to export topics to JSON: {e}")
            raise
    
    def get_conversation_topics(self, conversations: List[Dict[str, Any]], 
                              method: str = 'simple', max_topics: int = 50) -> Dict[str, Any]:
        """
        Get topics from conversation data.
        
        Args:
            conversations: List of conversation dictionaries
            method: 'simple' or 'advanced' analysis method
            max_topics: Maximum number of topics to extract
            
        Returns:
            Dictionary with topic analysis results
        """
        if not conversations:
            return {
                'topics': [],
                'total_conversations': 0,
                'total_words': 0,
                'analysis_method': method
            }
        
        # Extract text content
        texts = []
        total_words = 0
        
        for conv in conversations:
            content = conv.get('content', '')
            if content:
                texts.append(content)
                total_words += len(content.split())
        
        # Extract topics
        if method == 'advanced' and ADVANCED_ANALYSIS_AVAILABLE:
            topics = self.extract_topics_advanced(texts, max_topics)
        else:
            topics = self.extract_topics_simple(texts, max_topics)
        
        return {
            'topics': topics,
            'total_conversations': len(conversations),
            'analyzed_conversations': len(texts),
            'total_words': total_words,
            'analysis_method': method,
            'timestamp': datetime.now().isoformat()
        } 