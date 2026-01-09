#!/usr/bin/env python3
"""
Technical Debt Daily Report Generator (2x Daily)
==================================================

<!-- SSOT Domain: analytics -->

Generates daily progress reports for technical debt reduction.
Runs 2x daily: Morning (9:00 AM) and Afternoon (3:00 PM).

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-02
Priority: HIGH
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from systems.technical_debt.debt_tracker import TechnicalDebtTracker


class DailyReportGenerator:
    """Generates daily technical debt reports (2x daily)."""

    def __init__(self, tracker: TechnicalDebtTracker = None):
        """Initialize report generator."""
        if tracker is None:
            debt_dir = Path(__file__).parent
            tracker = TechnicalDebtTracker(debt_dir)
        
        self.tracker = tracker
        self.reports_dir = tracker.debt_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_daily_report(self, report_time: str = None) -> Dict[str, Any]:
        """
        Generate daily progress report.
        
        Args:
            report_time: "morning" or "afternoon" (default: auto-detect)
        """
        if report_time is None:
            current_hour = datetime.now().hour
            report_time = "morning" if current_hour < 12 else "afternoon"
        
        # Get current date
        today = datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        
        # Generate report from tracker
        report = self.tracker.generate_weekly_report()  # Uses same data structure
        
        # Override with daily-specific metadata
        report["report_type"] = "daily"
        report["report_time"] = report_time
        report["report_date"] = date_str
        report["generated_at"] = datetime.now().isoformat()
        
        # Calculate daily metrics (last 24 hours)
        yesterday = today - timedelta(days=1)
        daily_resolutions = [
            r for r in report.get("weekly_resolutions", [])
            if datetime.fromisoformat(r["date"]) >= yesterday
        ]
        
        total_daily_resolutions = sum(r.get("resolved", 0) for r in daily_resolutions)
        
        report["daily_metrics"] = {
            "total_resolved_24h": total_daily_resolutions,
            "categories_active_24h": len(set(r.get("category") for r in daily_resolutions)),
            "report_time": report_time,
        }
        
        return report

    def save_report(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Save report to file."""
        if filename is None:
            date_str = report["report_date"]
            report_time = report["report_time"]
            filename = f"daily_report_{date_str}_{report_time}.json"
        
        report_path = self.reports_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        return report_path

    def generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate markdown version of report."""
        date_str = report["report_date"]
        report_time = report["report_time"].title()
        
        markdown = f"""# Technical Debt Daily Report - {report_time}

**Report Date**: {date_str}  
**Report Time**: {report_time}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 Summary

- **Total Debt Items**: {report['summary']['total']}
- **Resolved**: {report['summary']['resolved']}
- **Pending**: {report['summary']['pending']}
- **Reduction Rate**: {report['summary']['reduction_rate']}%

---

## 📈 Daily Progress (Last 24 Hours)

- **Total Resolved**: {report['daily_metrics']['total_resolved_24h']}
- **Categories Active**: {report['daily_metrics']['categories_active_24h']}

---

## 📋 Category Status

"""
        
        for category, data in report["categories"].items():
            total = data.get("total", 0)
            resolved = data.get("resolved", 0)
            pending = total - resolved
            progress = (resolved / total * 100) if total > 0 else 0
            
            status_emoji = "✅" if pending == 0 else "⚠️" if pending < total * 0.5 else "🔴"
            
            markdown += f"""### {status_emoji} {category.replace('_', ' ').title()}

- **Total**: {total}
- **Resolved**: {resolved}
- **Pending**: {pending}
- **Progress**: {progress:.1f}%

"""
        
        markdown += "\n---\n\n"
        markdown += f"**Next Report**: {'Afternoon' if report_time == 'Morning' else 'Tomorrow Morning'}\n"
        markdown += "\n🐝 **WE. ARE. SWARM. ⚡🔥**\n"
        
        return markdown

    def save_markdown_report(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Save markdown report to file."""
        if filename is None:
            date_str = report["report_date"]
            report_time = report["report_time"]
            filename = f"DAILY_REPORT_{date_str}_{report_time.upper()}.md"
        
        report_path = self.reports_dir / filename
        markdown = self.generate_markdown_report(report)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        return report_path


def main():
    """CLI interface for daily report generation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate daily technical debt report (2x daily)"
    )
    parser.add_argument(
        "--time",
        choices=["morning", "afternoon"],
        default=None,
        help="Report time (morning/afternoon, default: auto-detect)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="Output format (default: both)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: systems/technical_debt/reports)"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = DailyReportGenerator()
    
    if args.output_dir:
        generator.reports_dir = Path(args.output_dir)
        generator.reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate report
    print(f"📊 Generating {args.time or 'auto-detected'} daily report...")
    report = generator.generate_daily_report(args.time)
    
    # Save reports
    if args.format in ["json", "both"]:
        json_path = generator.save_report(report)
        print(f"✅ JSON report saved: {json_path}")
    
    if args.format in ["markdown", "both"]:
        md_path = generator.save_markdown_report(report)
        print(f"✅ Markdown report saved: {md_path}")
    
    # Print summary
    print(f"\n📈 Daily Metrics:")
    print(f"   - Resolved (24h): {report['daily_metrics']['total_resolved_24h']}")
    print(f"   - Categories Active: {report['daily_metrics']['categories_active_24h']}")
    print(f"   - Total Pending: {report['summary']['pending']}")
    
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()

