#!/usr/bin/env python3
"""
Technical Debt Markers Analysis Tool
====================================

Analyzes and categorizes TODO/FIXME/BUG/DEPRECATED/REFACTOR markers
across the codebase.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: LOW - Documentation & Cleanup
"""

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Priority levels
PRIORITY_P0 = "P0 - Critical"
PRIORITY_P1 = "P1 - High"
PRIORITY_P2 = "P2 - Medium"
PRIORITY_P3 = "P3 - Low"


class TechnicalDebtMarkerAnalyzer:
    """Analyzes technical debt markers in codebase."""

    # Marker patterns with priorities
    MARKER_PATTERNS = {
        "BUG": {
            "pattern": re.compile(r"BUG[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P0,
            "color": "🔴",
        },
        "FIXME": {
            "pattern": re.compile(r"FIXME[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P0,
            "color": "🔴",
        },
        "TODO": {
            "pattern": re.compile(r"TODO[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P1,
            "color": "🟠",
        },
        "DEPRECATED": {
            "pattern": re.compile(r"DEPRECATED[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P2,
            "color": "🟡",
        },
        "REFACTOR": {
            "pattern": re.compile(r"REFACTOR[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P3,
            "color": "🔵",
        },
        "HACK": {
            "pattern": re.compile(r"HACK[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P2,
            "color": "🟡",
        },
        "XXX": {
            "pattern": re.compile(r"XXX[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P2,
            "color": "🟡",
        },
        "NOTE": {
            "pattern": re.compile(r"NOTE[:\s]+(.+)", re.IGNORECASE),
            "priority": PRIORITY_P3,
            "color": "⚪",
        },
    }

    def __init__(self, project_root: str = "."):
        """Initialize analyzer."""
        self.project_root = Path(project_root)
        self.markers: List[Dict[str, Any]] = []
        self.file_extensions = [".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c"]

    def find_source_files(self) -> List[Path]:
        """Find all source files to analyze."""
        source_files = []
        
        # Skip these directories
        skip_dirs = {
            ".git", "__pycache__", "node_modules", ".venv", "venv",
            "htmlcov", ".pytest_cache", "dist", "build", ".tox"
        }
        
        for ext in self.file_extensions:
            for file_path in self.project_root.rglob(f"*{ext}"):
                # Skip if in skip directory
                if any(skip in str(file_path) for skip in skip_dirs):
                    continue
                source_files.append(file_path)
        
        return sorted(source_files)

    def analyze_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze a single file for technical debt markers."""
        markers_found = []
        
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")
            
            for line_num, line in enumerate(lines, 1):
                for marker_type, marker_info in self.MARKER_PATTERNS.items():
                    match = marker_info["pattern"].search(line)
                    if match:
                        marker_text = match.group(1).strip()
                        
                        markers_found.append({
                            "file_path": str(file_path),
                            "relative_path": str(file_path.relative_to(self.project_root)),
                            "line_number": line_num,
                            "marker_type": marker_type,
                            "priority": marker_info["priority"],
                            "color": marker_info["color"],
                            "marker_text": marker_text[:200],  # Limit length
                            "full_line": line.strip()[:200],
                        })
        
        except Exception as e:
            # Skip files that can't be read
            pass
        
        return markers_found

    def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze entire codebase for technical debt markers."""
        print("🔍 Analyzing codebase for technical debt markers...")
        
        source_files = self.find_source_files()
        print(f"📁 Found {len(source_files)} source files to analyze\n")
        
        total_markers = 0
        markers_by_type = defaultdict(int)
        markers_by_priority = defaultdict(int)
        files_with_markers = defaultdict(set)
        
        for i, file_path in enumerate(source_files, 1):
            if i % 100 == 0:
                print(f"  Analyzing file {i}/{len(source_files)}...")
            
            file_markers = self.analyze_file(file_path)
            
            for marker in file_markers:
                self.markers.append(marker)
                total_markers += 1
                markers_by_type[marker["marker_type"]] += 1
                markers_by_priority[marker["priority"]] += 1
                files_with_markers[marker["marker_type"]].add(marker["relative_path"])
        
        print(f"\n✅ Analysis complete! Found {total_markers} markers in {sum(len(files) for files in files_with_markers.values())} files\n")
        
        return {
            "summary": {
                "total_markers": total_markers,
                "files_analyzed": len(source_files),
                "files_with_markers": sum(len(set(m["relative_path"] for m in self.markers if m["marker_type"] == mt)) for mt in markers_by_type.keys()),
                "analysis_date": datetime.now().isoformat(),
            },
            "by_type": {
                marker_type: {
                    "count": count,
                    "files_affected": len(files_with_markers[marker_type]),
                    "priority": self.MARKER_PATTERNS[marker_type]["priority"],
                }
                for marker_type, count in markers_by_type.items()
            },
            "by_priority": dict(markers_by_priority),
            "markers": self.markers,
        }

    def categorize_markers(self) -> Dict[str, Any]:
        """Categorize markers by various dimensions."""
        categories = {
            "by_type": defaultdict(list),
            "by_priority": defaultdict(list),
            "by_file_extension": defaultdict(list),
            "critical_files": [],  # Files with multiple high-priority markers
        }
        
        # Count markers per file
        file_marker_counts = defaultdict(int)
        file_high_priority_counts = defaultdict(int)
        
        for marker in self.markers:
            marker_type = marker["marker_type"]
            priority = marker["priority"]
            file_path = marker["relative_path"]
            
            categories["by_type"][marker_type].append(marker)
            categories["by_priority"][priority].append(marker)
            
            # Get file extension
            file_ext = Path(file_path).suffix
            categories["by_file_extension"][file_ext].append(marker)
            
            # Count markers per file
            file_marker_counts[file_path] += 1
            if priority in [PRIORITY_P0]:
                file_high_priority_counts[file_path] += 1
        
        # Identify critical files (multiple high-priority markers)
        for file_path, count in file_high_priority_counts.items():
            if count >= 3:  # 3+ critical markers
                categories["critical_files"].append({
                    "file_path": file_path,
                    "critical_markers": count,
                    "total_markers": file_marker_counts[file_path],
                })
        
        # Sort critical files by marker count
        categories["critical_files"].sort(key=lambda x: x["critical_markers"], reverse=True)
        
        return categories

    def generate_prioritized_list(self) -> List[Dict[str, Any]]:
        """Generate prioritized list of markers to address."""
        # Priority order
        priority_order = [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]
        
        prioritized = []
        for priority in priority_order:
            priority_markers = [m for m in self.markers if m["priority"] == priority]
            # Sort by file path for consistency
            priority_markers.sort(key=lambda x: x["relative_path"])
            prioritized.extend(priority_markers)
        
        return prioritized

    def save_results(self, results: Dict[str, Any], output_path: Path):
        """Save analysis results to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Results saved to: {output_path}")

    def generate_report(self, results: Dict[str, Any], report_path: Path):
        """Generate markdown report."""
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        summary = results["summary"]
        by_type = results["by_type"]
        by_priority = results["by_priority"]
        
        report = f"""# Technical Debt Markers Analysis Report

**Generated**: {summary['analysis_date']}  
**Total Markers Found**: {summary['total_markers']}  
**Files Analyzed**: {summary['files_analyzed']}  
**Files with Markers**: {summary['files_with_markers']}

---

## 📊 Summary by Type

"""
        
        # Sort by count
        sorted_types = sorted(by_type.items(), key=lambda x: x[1]["count"], reverse=True)
        
        for marker_type, info in sorted_types:
            report += f"""
### {marker_type}

- **Count**: {info['count']}
- **Files Affected**: {info['files_affected']}
- **Priority**: {info['priority']}

"""
        
        report += "\n---\n\n## 📊 Summary by Priority\n\n"
        
        priority_order = [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]
        for priority in priority_order:
            if priority in by_priority:
                count = by_priority[priority]
                report += f"- **{priority}**: {count} markers\n"
        
        report += "\n---\n\n## 🎯 Recommended Actions\n\n"
        report += "1. Address all P0 (Critical) markers first\n"
        report += "2. Review P1 (High) markers for planning\n"
        report += "3. Schedule P2/P3 markers for cleanup cycles\n"
        report += "4. Track resolution progress in technical debt tracker\n\n"
        
        report += "---\n\n🐝 **WE. ARE. SWARM. ⚡🔥**\n"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✅ Report saved to: {report_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Technical Debt Markers Analysis Tool")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("agent_workspaces/Agent-5/technical_debt_markers_analysis.json"),
        help="Output JSON file path"
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("agent_workspaces/Agent-5/TECHNICAL_DEBT_MARKERS_REPORT.md"),
        help="Output markdown report path"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="Project root directory"
    )
    
    args = parser.parse_args()
    
    print("🔍 TECHNICAL DEBT MARKERS ANALYSIS")
    print("=" * 60)
    print()
    
    analyzer = TechnicalDebtMarkerAnalyzer(project_root=args.project_root)
    
    # Analyze codebase
    results = analyzer.analyze_codebase()
    
    # Categorize markers
    categories = analyzer.categorize_markers()
    results["categories"] = categories
    
    # Generate prioritized list
    prioritized = analyzer.generate_prioritized_list()
    results["prioritized_list"] = prioritized[:50]  # Top 50 for summary
    
    # Save results
    analyzer.save_results(results, args.output)
    
    # Generate report
    analyzer.generate_report(results, args.report)
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Markers: {results['summary']['total_markers']}")
    print(f"Files with Markers: {results['summary']['files_with_markers']}")
    
    print("\nBy Type:")
    for marker_type, info in sorted(results["by_type"].items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {marker_type}: {info['count']} markers ({info['files_affected']} files)")
    
    print("\nBy Priority:")
    for priority in [PRIORITY_P0, PRIORITY_P1, PRIORITY_P2, PRIORITY_P3]:
        if priority in results["by_priority"]:
            print(f"  {priority}: {results['by_priority'][priority]} markers")
    
    if categories["critical_files"]:
        print(f"\n🚨 Critical Files (3+ P0 markers): {len(categories['critical_files'])}")
        for critical in categories["critical_files"][:5]:
            print(f"  - {critical['file_path']}: {critical['critical_markers']} critical markers")
    
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()


