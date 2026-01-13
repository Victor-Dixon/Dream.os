#!/usr/bin/env python3
"""
Canonical Dashboard Loader - Analytics Dashboard Generator
===========================================================

<!-- SSOT Domain: analytics -->

Generates HTML analytics dashboard for Output Flywheel metrics visualization.
Uses canonical metrics_client.py for data access.

Replaces:
- analytics_dashboard.py

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .metrics_client import MetricsClient


class DashboardLoader:
    """Canonical dashboard loader for analytics visualization."""

    def __init__(self, metrics_dir: Path = None, output_path: Path = None):
        """Initialize dashboard loader."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent
        if output_path is None:
            output_path = metrics_dir / "dashboard.html"
        
        self.metrics_dir = metrics_dir
        self.output_path = output_path
        self.client = MetricsClient(metrics_dir)

    def generate_dashboard(self):
        """Generate complete dashboard HTML."""
        metrics = self.client.get_current_metrics()
        weekly_summary = self.client.generate_weekly_summary()
        weekly_summaries = self.client.metrics_data.get("weekly_summaries", [])
        
        html = self._generate_html(metrics, weekly_summary, weekly_summaries)
        
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ Dashboard generated: {self.output_path}")

    def _generate_html(
        self,
        current_metrics: Dict[str, Any],
        weekly_summary: Dict[str, Any],
        weekly_summaries: List[Dict[str, Any]],
    ) -> str:
        """Generate HTML content."""
        weeks_data = weekly_summaries[-12:] if len(weekly_summaries) > 12 else weekly_summaries
        artifacts_data = [w.get("artifacts_per_week", 0) for w in weeks_data]
        publication_rates = [w.get("publication_rate", 0) for w in weeks_data]
        week_labels = [w.get("week_start", "")[:10] for w in weeks_data]
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Output Flywheel - Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a; color: #e0e0e0; padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 40px; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .subtitle {{ color: #888; font-size: 1.1em; }}
        .metrics-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px; margin-bottom: 40px;
        }}
        .metric-card {{
            background: #1a1a1a; border-radius: 12px; padding: 24px;
            border: 1px solid #333; transition: transform 0.2s;
        }}
        .metric-card:hover {{ transform: translateY(-4px); border-color: #667eea; }}
        .metric-label {{ color: #888; font-size: 0.9em; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; color: #667eea; }}
        .metric-target {{ color: #4caf50; font-size: 0.85em; margin-top: 8px; }}
        .charts-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px; margin-bottom: 40px;
        }}
        .chart-container {{
            background: #1a1a1a; border-radius: 12px; padding: 24px;
            border: 1px solid #333;
        }}
        .chart-title {{ color: #e0e0e0; font-size: 1.2em; margin-bottom: 20px; }}
        .footer {{
            text-align: center; color: #888; padding: 20px;
            border-top: 1px solid #333; margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Output Flywheel Analytics</h1>
            <div class="subtitle">Metrics & Performance Dashboard</div>
            <div class="subtitle" style="margin-top: 10px;">
                Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Artifacts Per Week</div>
                <div class="metric-value">{weekly_summary.get('artifacts_per_week', 0)}</div>
                <div class="metric-target">Target: 2+ artifacts/week</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Repos with Clean READMEs</div>
                <div class="metric-value">{weekly_summary.get('repos_with_clean_readmes', 0)}</div>
                <div class="metric-target">Growing repository quality</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Trading Days Documented</div>
                <div class="metric-value">{weekly_summary.get('trading_days_documented', 0)}</div>
                <div class="metric-target">All trading days</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Publication Rate</div>
                <div class="metric-value">{weekly_summary.get('publication_rate', 0):.1f}%</div>
                <div class="metric-target">Target: 90%</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">Artifacts Per Week Trend</div>
                <canvas id="artifactsChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Publication Rate Trend</div>
                <canvas id="publicationChart"></canvas>
            </div>
        </div>
    </div>
    
    <div class="footer">
        Output Flywheel v1.0 | Generated by Agent-5 (Business Intelligence Specialist)
    </div>
    
    <script>
        const artifactsCtx = document.getElementById('artifactsChart').getContext('2d');
        new Chart(artifactsCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(week_labels)},
                datasets: [{{
                    label: 'Artifacts Per Week',
                    data: {json.dumps(artifacts_data)},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }}, {{
                    label: 'Target (2)',
                    data: Array({len(week_labels)}).fill(2),
                    borderColor: '#4caf50',
                    borderDash: [5, 5],
                    pointRadius: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{ legend: {{ labels: {{ color: '#e0e0e0' }} }} }},
                scales: {{
                    y: {{ beginAtZero: true, ticks: {{ color: '#888' }}, grid: {{ color: '#333' }} }},
                    x: {{ ticks: {{ color: '#888' }}, grid: {{ color: '#333' }} }}
                }}
            }}
        }});
        
        const publicationCtx = document.getElementById('publicationChart').getContext('2d');
        new Chart(publicationCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(week_labels)},
                datasets: [{{
                    label: 'Publication Rate (%)',
                    data: {json.dumps(publication_rates)},
                    borderColor: '#764ba2',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    tension: 0.4,
                    fill: true
                }}, {{
                    label: 'Target (90%)',
                    data: Array({len(week_labels)}).fill(90),
                    borderColor: '#4caf50',
                    borderDash: [5, 5],
                    pointRadius: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{ legend: {{ labels: {{ color: '#e0e0e0' }} }} }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{ color: '#888', callback: function(value) {{ return value + '%'; }} }},
                        grid: {{ color: '#333' }}
                    }},
                    x: {{ ticks: {{ color: '#888' }}, grid: {{ color: '#333' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html


def main():
    """CLI interface for dashboard generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Output Flywheel Analytics Dashboard")
    parser.add_argument("--metrics-dir", type=str, default="systems/output_flywheel", help="Metrics directory")
    parser.add_argument("--output", type=str, default="systems/output_flywheel/dashboard.html", help="Output HTML file")
    
    args = parser.parse_args()
    loader = DashboardLoader(Path(args.metrics_dir), Path(args.output))
    loader.generate_dashboard()


if __name__ == "__main__":
    main()


