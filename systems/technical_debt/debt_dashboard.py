#!/usr/bin/env python3
"""
Technical Debt Dashboard
========================

<!-- SSOT Domain: analytics -->

Interactive HTML dashboard for visualizing technical debt
and tracking progress.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: MEDIUM
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from debt_tracker import TechnicalDebtTracker


class TechnicalDebtDashboard:
    """Generates interactive HTML dashboard for technical debt."""

    def __init__(self, tracker: TechnicalDebtTracker):
        """Initialize dashboard generator."""
        self.tracker = tracker
        self.dashboard_dir = tracker.debt_dir / "dashboard"
        self.dashboard_dir.mkdir(parents=True, exist_ok=True)

    def generate_html_dashboard(self) -> Path:
        """Generate interactive HTML dashboard."""
        dashboard_data = self.tracker.generate_dashboard_data()
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Debt Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            color: #333;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
        }}
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .category-section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .category-section h2 {{
            margin: 0 0 20px 0;
            color: #333;
        }}
        .category-item {{
            padding: 15px;
            border-left: 4px solid #007bff;
            background: #f8f9fa;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        .category-item h4 {{
            margin: 0 0 5px 0;
            color: #333;
        }}
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Technical Debt Dashboard</h1>
            <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Debt Items</h3>
                <div class="value">{dashboard_data['summary']['total']}</div>
            </div>
            <div class="stat-card">
                <h3>Resolved</h3>
                <div class="value">{dashboard_data['summary']['resolved']}</div>
            </div>
            <div class="stat-card">
                <h3>Pending</h3>
                <div class="value">{dashboard_data['summary']['pending']}</div>
            </div>
            <div class="stat-card">
                <h3>Reduction Rate</h3>
                <div class="value">{dashboard_data['summary']['reduction_rate']}%</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2>Debt by Category</h2>
            <canvas id="categoryChart" width="400" height="200"></canvas>
        </div>
        
        <div class="category-section">
            <h2>Category Breakdown</h2>
            {self._generate_category_html(dashboard_data['categories'])}
        </div>
        
        <div class="category-section">
            <h2>Active Tasks</h2>
            {self._generate_tasks_html(dashboard_data['active_tasks'])}
        </div>
    </div>
    
    <script>
        const categories = {json.dumps(dashboard_data['categories'], indent=2)};
        
        const ctx = document.getElementById('categoryChart').getContext('2d');
        const categoryChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: Object.keys(categories),
                datasets: [{{
                    label: 'Total',
                    data: Object.values(categories).map(c => c.total),
                    backgroundColor: 'rgba(0, 123, 255, 0.5)',
                }}, {{
                    label: 'Resolved',
                    data: Object.values(categories).map(c => c.resolved),
                    backgroundColor: 'rgba(40, 167, 69, 0.5)',
                }}, {{
                    label: 'Pending',
                    data: Object.values(categories).map(c => c.total - c.resolved),
                    backgroundColor: 'rgba(220, 53, 69, 0.5)',
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        dashboard_path = self.dashboard_dir / "index.html"
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return dashboard_path

    def _generate_category_html(self, categories: Dict[str, Any]) -> str:
        """Generate HTML for category breakdown."""
        html = ""
        for category, data in categories.items():
            total = data.get("total", 0)
            resolved = data.get("resolved", 0)
            pending = total - resolved
            progress = (resolved / total * 100) if total > 0 else 0
            
            html += f"""
            <div class="category-item">
                <h4>{category.replace('_', ' ').title()}</h4>
                <p>Total: {total} | Resolved: {resolved} | Pending: {pending}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
            </div>
            """
        return html

    def _generate_tasks_html(self, tasks: list) -> str:
        """Generate HTML for active tasks."""
        if not tasks:
            return "<p>No active tasks</p>"
        
        html = ""
        for task in tasks:
            html += f"""
            <div class="category-item">
                <h4>{task.get('task', 'Unknown Task')}</h4>
                <p>Agent: {task.get('agent_id', 'Unknown')} | Status: {task.get('status', 'unknown')} | Progress: {task.get('progress', 0)}%</p>
            </div>
            """
        return html


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Technical Debt Dashboard")
    parser.add_argument("--generate", action="store_true", help="Generate dashboard")
    
    args = parser.parse_args()
    
    tracker = TechnicalDebtTracker()
    dashboard = TechnicalDebtDashboard(tracker)
    
    if args.generate:
        dashboard_path = dashboard.generate_html_dashboard()
        print(f"✅ Dashboard generated: {dashboard_path}")


if __name__ == "__main__":
    main()



