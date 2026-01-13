#!/usr/bin/env python3
"""
Time Series Analyzer - Core module for time-based data analysis
==============================================================

Provides functionality to:
- Generate time-series data from conversations
- Calculate daily/weekly/monthly statistics
- Create trend analysis for various metrics
- Export time-series data for charting
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, Counter
from datetime import datetime, timedelta, date
import json
from pathlib import Path

# Optional dependencies for advanced time series analysis
try:
    import numpy as np
    import pandas as pd
    ADVANCED_ANALYSIS_AVAILABLE = True
except ImportError:
    ADVANCED_ANALYSIS_AVAILABLE = False
    logging.warning("Advanced time series analysis not available. Install pandas for full functionality.")

from dreamscape.core.utils.common_utils import parse_date_safe

logger = logging.getLogger(__name__)


class TimeSeriesAnalyzer:
    """Core time series analysis functionality."""
    
    def __init__(self):
        self.date_format = '%Y-%m-%d'
        
    def get_daily_conversation_stats(self, conversations: List[Dict[str, Any]], 
                                   days: int = 30) -> List[Dict[str, Any]]:
        """
        Generate daily conversation statistics.
        
        Args:
            conversations: List of conversation dictionaries
            days: Number of days to analyze
            
        Returns:
            List of daily statistics dictionaries
        """
        if not conversations:
            return []
        
        # Initialize date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Group conversations by date
        daily_stats = defaultdict(lambda: {
            'date': '',
            'conversation_count': 0,
            'total_messages': 0,
            'total_words': 0,
            'avg_message_length': 0,
            'models_used': Counter(),
            'sources': Counter()
        })
        
        # Process conversations
        for conv in conversations:
            conv_date = parse_date_safe(conv.get('created_at', ''))
            if conv_date:
                date_key = conv_date.date()
                if start_date <= date_key <= end_date:
                    date_str = date_key.strftime(self.date_format)
                    
                    if date_str not in daily_stats:
                        daily_stats[date_str]['date'] = date_str
                    
                    daily_stats[date_str]['conversation_count'] += 1
                    daily_stats[date_str]['total_messages'] += conv.get('message_count', 0)
                    daily_stats[date_str]['total_words'] += conv.get('word_count', 0)
                    
                    # Track models and sources
                    model = conv.get('model', 'Unknown')
                    daily_stats[date_str]['models_used'][model] += 1
                    
                    source = conv.get('source', 'Unknown')
                    daily_stats[date_str]['sources'][source] += 1
        
        # Fill in missing dates and calculate averages
        result = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime(self.date_format)
            
            if date_str in daily_stats:
                stats = daily_stats[date_str]
                # Calculate average message length
                if stats['total_messages'] > 0:
                    stats['avg_message_length'] = round(stats['total_words'] / stats['total_messages'], 1)
                
                # Convert counters to dictionaries
                stats['models_used'] = dict(stats['models_used'])
                stats['sources'] = dict(stats['sources'])
                
                result.append(stats)
            else:
                # Add zero stats for missing dates
                result.append({
                    'date': date_str,
                    'conversation_count': 0,
                    'total_messages': 0,
                    'total_words': 0,
                    'avg_message_length': 0,
                    'models_used': {},
                    'sources': {}
                })
            
            current_date += timedelta(days=1)
        
        return result
    
    def get_weekly_stats(self, conversations: List[Dict[str, Any]], 
                        weeks: int = 12) -> List[Dict[str, Any]]:
        """
        Generate weekly conversation statistics.
        
        Args:
            conversations: List of conversation dictionaries
            weeks: Number of weeks to analyze
            
        Returns:
            List of weekly statistics dictionaries
        """
        if not conversations:
            return []
        
        # Initialize date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(weeks=weeks)
        
        # Group conversations by week
        weekly_stats = defaultdict(lambda: {
            'week_start': '',
            'week_end': '',
            'conversation_count': 0,
            'total_messages': 0,
            'total_words': 0,
            'avg_message_length': 0,
            'models_used': Counter(),
            'sources': Counter()
        })
        
        # Process conversations
        for conv in conversations:
            conv_date = parse_date_safe(conv.get('created_at', ''))
            if conv_date:
                conv_date_obj = conv_date.date()
                if start_date <= conv_date_obj <= end_date:
                    # Get week start (Monday)
                    week_start = conv_date_obj - timedelta(days=conv_date_obj.weekday())
                    week_end = week_start + timedelta(days=6)
                    week_key = week_start.strftime(self.date_format)
                    
                    if week_key not in weekly_stats:
                        weekly_stats[week_key]['week_start'] = week_start.strftime(self.date_format)
                        weekly_stats[week_key]['week_end'] = week_end.strftime(self.date_format)
                    
                    weekly_stats[week_key]['conversation_count'] += 1
                    weekly_stats[week_key]['total_messages'] += conv.get('message_count', 0)
                    weekly_stats[week_key]['total_words'] += conv.get('word_count', 0)
                    
                    # Track models and sources
                    model = conv.get('model', 'Unknown')
                    weekly_stats[week_key]['models_used'][model] += 1
                    
                    source = conv.get('source', 'Unknown')
                    weekly_stats[week_key]['sources'][source] += 1
        
        # Convert to list and calculate averages
        result = []
        for week_key, stats in sorted(weekly_stats.items()):
            # Calculate average message length
            if stats['total_messages'] > 0:
                stats['avg_message_length'] = round(stats['total_words'] / stats['total_messages'], 1)
            
            # Convert counters to dictionaries
            stats['models_used'] = dict(stats['models_used'])
            stats['sources'] = dict(stats['sources'])
            
            result.append(stats)
        
        return result
    
    def get_monthly_stats(self, conversations: List[Dict[str, Any]], 
                         months: int = 12) -> List[Dict[str, Any]]:
        """
        Generate monthly conversation statistics.
        
        Args:
            conversations: List of conversation dictionaries
            months: Number of months to analyze
            
        Returns:
            List of monthly statistics dictionaries
        """
        if not conversations:
            return []
        
        # Initialize date range
        end_date = datetime.now().date()
        start_date = end_date.replace(day=1) - timedelta(days=months * 30)
        
        # Group conversations by month
        monthly_stats = defaultdict(lambda: {
            'month': '',
            'year': 0,
            'conversation_count': 0,
            'total_messages': 0,
            'total_words': 0,
            'avg_message_length': 0,
            'models_used': Counter(),
            'sources': Counter()
        })
        
        # Process conversations
        for conv in conversations:
            conv_date = parse_date_safe(conv.get('created_at', ''))
            if conv_date:
                conv_date_obj = conv_date.date()
                if start_date <= conv_date_obj <= end_date:
                    month_key = f"{conv_date_obj.year}-{conv_date_obj.month:02d}"
                    
                    if month_key not in monthly_stats:
                        monthly_stats[month_key]['month'] = conv_date_obj.strftime('%B')
                        monthly_stats[month_key]['year'] = conv_date_obj.year
                    
                    monthly_stats[month_key]['conversation_count'] += 1
                    monthly_stats[month_key]['total_messages'] += conv.get('message_count', 0)
                    monthly_stats[month_key]['total_words'] += conv.get('word_count', 0)
                    
                    # Track models and sources
                    model = conv.get('model', 'Unknown')
                    monthly_stats[month_key]['models_used'][model] += 1
                    
                    source = conv.get('source', 'Unknown')
                    monthly_stats[month_key]['sources'][source] += 1
        
        # Convert to list and calculate averages
        result = []
        for month_key, stats in sorted(monthly_stats.items()):
            # Calculate average message length
            if stats['total_messages'] > 0:
                stats['avg_message_length'] = round(stats['total_words'] / stats['total_messages'], 1)
            
            # Convert counters to dictionaries
            stats['models_used'] = dict(stats['models_used'])
            stats['sources'] = dict(stats['sources'])
            
            result.append(stats)
        
        return result
    
    def generate_chart_data(self, time_series_data: List[Dict[str, Any]], 
                           metric: str = 'conversation_count') -> Dict[str, Any]:
        """
        Generate data optimized for chart visualization.
        
        Args:
            time_series_data: List of time series statistics
            metric: Metric to chart ('conversation_count', 'total_messages', 'total_words')
            
        Returns:
            Dictionary with chart data
        """
        if not time_series_data:
            return {
                'labels': [],
                'data': [],
                'metric': metric,
                'total': 0,
                'average': 0
            }
        
        labels = []
        data = []
        
        for item in time_series_data:
            # Determine label based on data structure
            if 'date' in item:
                labels.append(item['date'])
            elif 'week_start' in item:
                labels.append(item['week_start'])
            elif 'month' in item:
                labels.append(f"{item['month']} {item['year']}")
            else:
                labels.append(str(len(labels) + 1))
            
            # Get metric value
            value = item.get(metric, 0)
            data.append(value)
        
        total = sum(data)
        average = total / len(data) if data else 0
        
        return {
            'labels': labels,
            'data': data,
            'metric': metric,
            'total': total,
            'average': round(average, 2),
            'min_value': min(data) if data else 0,
            'max_value': max(data) if data else 0
        }
    
    def calculate_trends(self, time_series_data: List[Dict[str, Any]], 
                        metric: str = 'conversation_count') -> Dict[str, Any]:
        """
        Calculate trend analysis for time series data.
        
        Args:
            time_series_data: List of time series statistics
            metric: Metric to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        if not time_series_data or len(time_series_data) < 2:
            return {
                'trend': 'stable',
                'change_percentage': 0,
                'growth_rate': 0,
                'volatility': 0
            }
        
        # Extract metric values
        values = [item.get(metric, 0) for item in time_series_data]
        
        # Calculate basic statistics
        total = sum(values)
        average = total / len(values)
        
        # Calculate trend
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = sum(first_half) / len(first_half) if first_half else 0
        second_avg = sum(second_half) / len(second_half) if second_half else 0
        
        if first_avg == 0:
            change_percentage = 100 if second_avg > 0 else 0
        else:
            change_percentage = ((second_avg - first_avg) / first_avg) * 100
        
        # Determine trend direction
        if change_percentage > 10:
            trend = 'increasing'
        elif change_percentage < -10:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        # Calculate growth rate (simple linear regression)
        growth_rate = 0
        if len(values) > 1:
            x = list(range(len(values)))
            y = values
            
            # Simple linear regression
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x[i] * y[i] for i in range(n))
            sum_x2 = sum(x[i] ** 2 for i in range(n))
            
            if n * sum_x2 - sum_x ** 2 != 0:
                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
                growth_rate = slope
        
        # Calculate volatility (standard deviation)
        if len(values) > 1:
            variance = sum((v - average) ** 2 for v in values) / len(values)
            volatility = variance ** 0.5
        else:
            volatility = 0
        
        return {
            'trend': trend,
            'change_percentage': round(change_percentage, 2),
            'growth_rate': round(growth_rate, 4),
            'volatility': round(volatility, 2),
            'total': total,
            'average': round(average, 2),
            'min_value': min(values),
            'max_value': max(values)
        }
    
    def export_time_series_csv(self, time_series_data: List[Dict[str, Any]], 
                              file_path: str) -> str:
        """
        Export time series data to CSV format.
        
        Args:
            time_series_data: List of time series statistics
            file_path: Output file path
            
        Returns:
            Path to exported file
        """
        try:
            import csv
            
            if not time_series_data:
                raise ValueError("No data to export")
            
            # Get all possible fieldnames
            fieldnames = set()
            for item in time_series_data:
                fieldnames.update(item.keys())
            
            # Sort fieldnames for consistent output
            fieldnames = sorted(list(fieldnames))
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in time_series_data:
                    # Convert any non-serializable values to strings
                    row = {}
                    for field in fieldnames:
                        value = item.get(field, '')
                        if isinstance(value, (dict, list)):
                            value = json.dumps(value)
                        row[field] = value
                    writer.writerow(row)
            
            logger.info(f"Time series data exported to CSV: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to export time series data to CSV: {e}")
            raise
    
    def export_time_series_json(self, time_series_data: List[Dict[str, Any]], 
                               file_path: str) -> str:
        """
        Export time series data to JSON format.
        
        Args:
            time_series_data: List of time series statistics
            file_path: Output file path
            
        Returns:
            Path to exported file
        """
        try:
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_records': len(time_series_data),
                'data': time_series_data
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Time series data exported to JSON: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to export time series data to JSON: {e}")
            raise
    
    def get_conversation_time_series(self, conversations: List[Dict[str, Any]], 
                                   period: str = 'daily', 
                                   days: int = 30) -> Dict[str, Any]:
        """
        Get time series data from conversation data.
        
        Args:
            conversations: List of conversation dictionaries
            period: 'daily', 'weekly', or 'monthly'
            days: Number of days to analyze (for daily/weekly)
            
        Returns:
            Dictionary with time series analysis results
        """
        if not conversations:
            return {
                'time_series': [],
                'chart_data': {},
                'trends': {},
                'total_conversations': 0,
                'period': period
            }
        
        # Generate time series data based on period
        if period == 'daily':
            time_series = self.get_daily_conversation_stats(conversations, days)
        elif period == 'weekly':
            time_series = self.get_weekly_stats(conversations, days // 7)
        elif period == 'monthly':
            time_series = self.get_monthly_stats(conversations, days // 30)
        else:
            raise ValueError(f"Invalid period: {period}. Must be 'daily', 'weekly', or 'monthly'")
        
        # Generate chart data for different metrics
        chart_data = {
            'conversations': self.generate_chart_data(time_series, 'conversation_count'),
            'messages': self.generate_chart_data(time_series, 'total_messages'),
            'words': self.generate_chart_data(time_series, 'total_words')
        }
        
        # Calculate trends
        trends = {
            'conversations': self.calculate_trends(time_series, 'conversation_count'),
            'messages': self.calculate_trends(time_series, 'total_messages'),
            'words': self.calculate_trends(time_series, 'total_words')
        }
        
        return {
            'time_series': time_series,
            'chart_data': chart_data,
            'trends': trends,
            'total_conversations': len(conversations),
            'period': period,
            'timestamp': datetime.now().isoformat()
        } 