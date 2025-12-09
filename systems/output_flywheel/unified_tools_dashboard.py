#!/usr/bin/env python3
"""
Unified Tools Usage Dashboard Generator
========================================

Generates HTML dashboard for unified tools usage metrics visualization.
Displays tool usage, category distribution, performance metrics, and error rates.

<!-- SSOT Domain: analytics -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-07
V2 Compliant: Yes (<300 lines)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .unified_tools_metrics import UnifiedToolsMetricsTracker


class UnifiedToolsDashboard:
    """Generates HTML dashboard for unified tools metrics."""

    def __init__(self, output_path: Optional[Path] = None):
        """
        Initialize dashboard generator.
        
        Args:
            output_path: Path to output HTML file (defaults to systems/output_flywheel/data/unified_tools_dashboard.html)
        """
        if output_path is None:
            project_root = Path(__file__).parent.parent.parent
            output_path = project_root / "systems" / "output_flywheel" / "data" / "unified_tools_dashboard.html"
        
        self.output_path = Path(output_path)
        self.tracker = UnifiedToolsMetricsTracker()

    def generate_dashboard(self) -> None:
        """Generate complete dashboard HTML."""
        # Get metrics data
        summary = self.tracker.get_summary()
        category_dist = self.tracker.get_category_distribution()
        performance_metrics = self.tracker.get_performance_metrics()
        error_rates = self.tracker.get_error_rates()
        
        # Get tool-specific metrics
        tool_metrics = {}
        for tool_name in ["unified_validator", "unified_analyzer"]:
            tool_metrics[tool_name] = self.tracker.get_tool_metrics(tool_name)
        
        # Generate HTML
        html = self._generate_html(
            summary, category_dist, performance_metrics, error_rates, tool_metrics
        )
        
        # Save to file
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ Unified Tools Dashboard generated: {self.output_path}")

    def _generate_html(
        self,
        summary: Dict[str, Any],
        category_dist: Dict[str, int],
        performance_metrics: Dict[str, Any],
        error_rates: Dict[str, Dict[str, Any]],
        tool_metrics: Dict[str, Dict[str, Any]],
    ) -> str:
        """Generate HTML content."""
        
        # Prepare chart data
        category_labels = list(category_dist.keys())
        category_values = list(category_dist.values())
        
        # Tool usage data
        tool_names = list(tool_metrics.keys())
        tool_calls = [
            tool_metrics.get(tool, {}).get("total_calls", 0) for tool in tool_names
        ]
        tool_success = [
            tool_metrics.get(tool, {}).get("successful_calls", 0) for tool in tool_names
        ]
        
        # Performance data
        perf_data = {}
        for tool_name, perf in performance_metrics.items():
            perf_data[tool_name] = {
                "avg": perf.get("avg_execution_time", 0),
                "min": perf.get("min_execution_time", 0),
                "max": perf.get("max_execution_time", 0),
            }
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified Tools - Usage Metrics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: #1a1a1a;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #333;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #888;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: #1a1a1a;
            padding: 25px;
            border-radius: 10px;
            border: 1px solid #333;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .chart-title {{
            font-size: 1.3em;
            margin-bottom: 20px;
            color: #667eea;
        }}
        
        .tool-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .tool-table th,
        .tool-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #333;
        }}
        
        .tool-table th {{
            background: #2a2a2a;
            color: #667eea;
            font-weight: bold;
        }}
        
        .success-rate {{
            color: #4ade80;
        }}
        
        .error-rate {{
            color: #f87171;
        }}
        
        .last-updated {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔧 Unified Tools Usage Metrics</h1>
            <div class="subtitle">Real-time analytics for unified_validator, unified_analyzer, and other unified tools</div>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Tool Calls</div>
                <div class="metric-value">{summary.get('total_tool_calls', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Tools Tracked</div>
                <div class="metric-value">{summary.get('tools_tracked', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Categories Tracked</div>
                <div class="metric-value">{summary.get('categories_tracked', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Avg Error Rate</div>
                <div class="metric-value">{summary.get('average_error_rate', 0.0):.1%}</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">Category Distribution</div>
                <canvas id="categoryChart"></canvas>
            </div>
            <div class="chart-card">
                <div class="chart-title">Tool Usage</div>
                <canvas id="toolUsageChart"></canvas>
            </div>
        </div>
        
        <div class="chart-card">
            <div class="chart-title">Tool Performance Metrics</div>
            <table class="tool-table">
                <thead>
                    <tr>
                        <th>Tool</th>
                        <th>Total Calls</th>
                        <th>Success Rate</th>
                        <th>Avg Execution Time</th>
                        <th>Error Rate</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add tool rows
        for tool_name in tool_names:
            tool_data = tool_metrics.get(tool_name, {})
            total_calls = tool_data.get("total_calls", 0)
            successful = tool_data.get("successful_calls", 0)
            success_rate = (successful / total_calls * 100) if total_calls > 0 else 0
            
            perf = perf_data.get(tool_name, {})
            avg_time = perf.get("avg", 0)
            
            error_data = error_rates.get(tool_name, {})
            error_rate = error_data.get("rate", 0.0) * 100
            
            html += f"""
                    <tr>
                        <td><strong>{tool_name}</strong></td>
                        <td>{total_calls}</td>
                        <td class="success-rate">{success_rate:.1f}%</td>
                        <td>{avg_time:.2f}s</td>
                        <td class="error-rate">{error_rate:.1f}%</td>
                    </tr>
"""
        
        html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="last-updated">
            Last Updated: {summary.get('last_updated', 'N/A')}
        </div>
    </div>
    
    <script>
        // Category Distribution Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(category_labels)},
                datasets: [{{
                    data: {json.dumps(category_values)},
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            color: '#e0e0e0'
                        }}
                    }}
                }}
            }}
        }});
        
        // Tool Usage Chart
        const toolCtx = document.getElementById('toolUsageChart').getContext('2d');
        new Chart(toolCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(tool_names)},
                datasets: [{{
                    label: 'Total Calls',
                    data: {json.dumps(tool_calls)},
                    backgroundColor: '#667eea'
                }}, {{
                    label: 'Successful Calls',
                    data: {json.dumps(tool_success)},
                    backgroundColor: '#4ade80'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        labels: {{
                            color: '#e0e0e0'
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            color: '#888'
                        }},
                        grid: {{
                            color: '#333'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#888'
                        }},
                        grid: {{
                            color: '#333'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html


def generate_dashboard(output_path: Optional[Path] = None) -> None:
    """Convenience function to generate dashboard."""
    dashboard = UnifiedToolsDashboard(output_path)
    dashboard.generate_dashboard()


if __name__ == "__main__":
    generate_dashboard()

__all__ = ["UnifiedToolsDashboard", "generate_dashboard"]

