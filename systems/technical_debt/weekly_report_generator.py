#!/usr/bin/env python3
"""
Technical Debt Weekly Report Generator
======================================

<!-- SSOT Domain: analytics -->

Generates weekly progress reports for technical debt reduction.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: MEDIUM
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

from debt_tracker import TechnicalDebtTracker


class WeeklyReportGenerator:
    """Generates weekly technical debt reports."""

    def __init__(self, tracker: TechnicalDebtTracker):
        """Initialize report generator."""
        self.tracker = tracker
        self.reports_dir = tracker.debt_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly progress report."""
        report = self.tracker.generate_weekly_report()
        
        # Calculate weekly metrics
        weekly_resolutions = report.get("weekly_resolutions", [])
        total_weekly_resolutions = sum(r.get("resolved", 0) for r in weekly_resolutions)
        
        report["weekly_metrics"] = {
            "total_resolved": total_weekly_resolutions,
            "categories_resolved": len(set(r.get("category") for r in weekly_resolutions)),
        }
        
        return report

    def save_report(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Save report to file."""
        if filename is None:
            week_start = datetime.fromisoformat(report["report_period"]["week_start"])
            filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.json"
        
        report_path = self.reports_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        return report_path

    def generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate markdown version of report."""
        week_start = datetime.fromisoformat(report["report_period"]["week_start"]).strftime("%Y-%m-%d")
        week_end = datetime.fromisoformat(report["report_period"]["week_end"]).strftime("%Y-%m-%d")
        
        markdown = f"""# Technical Debt Weekly Report

**Report Period**: {week_start} to {week_end}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 Summary

- **Total Debt Items**: {report['summary']['total']}
- **Resolved**: {report['summary']['resolved']}
- **Pending**: {report['summary']['pending']}
- **Reduction Rate**: {report['summary']['reduction_rate']}%

---

## 📈 Weekly Progress

- **Total Resolved This Week**: {report['weekly_metrics']['total_resolved']}
- **Categories Active**: {report['weekly_metrics']['categories_resolved']}

### Resolutions This Week

"""
        
        if report.get("weekly_resolutions"):
            for resolution in report["weekly_resolutions"]:
                date = datetime.fromisoformat(resolution["date"]).strftime("%Y-%m-%d")
                markdown += f"- **{date}**: {resolution['category']} - {resolution['resolved']} items resolved\n"
        else:
            markdown += "- No resolutions recorded this week\n"
        
        markdown += "\n---\n\n## 📋 Category Status\n\n"
        
        for category, data in report["categories"].items():
            total = data.get("total", 0)
            resolved = data.get("resolved", 0)
            pending = total - resolved
            progress = (resolved / total * 100) if total > 0 else 0
            
            markdown += f"""### {category.replace('_', ' ').title()}

- **Total**: {total}
- **Resolved**: {resolved}
- **Pending**: {pending}
- **Progress**: {progress:.1f}%

"""
        
        markdown += "\n---\n\n## ✅ Active Tasks\n\n"
        
        if report.get("active_tasks"):
            for task in report["active_tasks"]:
                markdown += f"""- **{task.get('task', 'Unknown')}**
  - Agent: {task.get('agent_id', 'Unknown')}
  - Status: {task.get('status', 'unknown')}
  - Progress: {task.get('progress', 0)}%

"""
        else:
            markdown += "- No active tasks\n"
        
        markdown += "\n---\n\n🐝 **WE. ARE. SWARM. ⚡🔥**\n"
        
        return markdown

    def save_markdown_report(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Save markdown report to file."""
        markdown = self.generate_markdown_report(report)
        
        if filename is None:
            week_start = datetime.fromisoformat(report["report_period"]["week_start"])
            filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.md"
        
        report_path = self.reports_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        return report_path


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Technical Debt Weekly Report Generator")
    parser.add_argument("--generate", action="store_true", help="Generate weekly report")
    parser.add_argument("--markdown", action="store_true", help="Generate markdown report")
    
    args = parser.parse_args()
    
    tracker = TechnicalDebtTracker()
    generator = WeeklyReportGenerator(tracker)
    
    if args.generate:
        report = generator.generate_weekly_report()
        json_path = generator.save_report(report)
        print(f"✅ Weekly report generated: {json_path}")
        
        if args.markdown:
            md_path = generator.save_markdown_report(report)
            print(f"✅ Markdown report generated: {md_path}")


if __name__ == "__main__":
    main()


