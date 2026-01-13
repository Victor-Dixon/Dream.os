"""
Trend Analyzer - V2 Compliance Module
=====================================

<!-- SSOT Domain: analytics -->

Trend analysis functionality for analytics.

V2 Compliance: < 300 lines, single responsibility, trend analysis.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
import statistics
from typing import Any

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Trend analysis functionality."""

    def __init__(self):
        """Initialize trend analyzer."""
        self.logger = logger

    def analyze_trends(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze trends in data."""
        try:
            if not data:
                return {"error": "No data provided"}

            # Extract numeric values for trend analysis
            numeric_values = []
            for item in data:
                for value in item.values():
                    if isinstance(value, (int, float)):
                        numeric_values.append(value)

            if len(numeric_values) < 2:
                return {"message": "Insufficient data for trend analysis"}

            # Calculate trend direction and slope
            trend_direction = self._calculate_trend_direction(numeric_values)
            trend_strength = self._calculate_trend_strength(numeric_values)
            trend_slope = self._calculate_trend_slope(numeric_values)

            return {
                "direction": trend_direction,
                "strength": trend_strength,
                "slope": trend_slope,
                "data_points": len(numeric_values),
                "mean": round(statistics.mean(numeric_values), 3),
                "median": round(statistics.median(numeric_values), 3),
            }
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {e}")
            return {"error": str(e)}

    def _calculate_trend_direction(self, values: list[float]) -> str:
        """Calculate trend direction (increasing, decreasing, stable)."""
        try:
            if len(values) < 2:
                return "stable"

            # Simple linear regression slope
            n = len(values)
            x_mean = (n - 1) / 2
            y_mean = statistics.mean(values)

            numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))

            if denominator == 0:
                return "stable"

            slope = numerator / denominator

            # Determine direction based on slope
            if slope > 0.01:
                return "increasing"
            elif slope < -0.01:
                return "decreasing"
            else:
                return "stable"
        except Exception as e:
            self.logger.error(f"Error calculating trend direction: {e}")
            return "unknown"

    def _calculate_trend_strength(self, values: list[float]) -> float:
        """Calculate trend strength (0-1 scale)."""
        try:
            if len(values) < 3:
                return 0.0

            # Use coefficient of variation as a measure of trend strength
            mean_val = statistics.mean(values)
            if mean_val == 0:
                return 0.0

            stdev_val = statistics.stdev(values) if len(values) > 1 else 0
            cv = abs(stdev_val / mean_val) if mean_val != 0 else 0

            # Convert to strength (higher variation = stronger trend if consistent direction)
            strength = min(1.0, cv * 2)  # Scale to 0-1 range

            return round(strength, 3)
        except Exception as e:
            self.logger.error(f"Error calculating trend strength: {e}")
            return 0.0

    def _calculate_trend_slope(self, values: list[float]) -> float:
        """Calculate trend slope."""
        try:
            if len(values) < 2:
                return 0.0

            n = len(values)
            x_mean = (n - 1) / 2
            y_mean = statistics.mean(values)

            numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))

            if denominator == 0:
                return 0.0

            slope = numerator / denominator
            return round(slope, 3)
        except Exception as e:
            self.logger.error(f"Error calculating trend slope: {e}")
            return 0.0


__all__ = ["TrendAnalyzer"]

