#!/usr/bin/env python3
"""
Universal Project Scanner Tool
==============================

A tool to scan any project and get AI-powered guidance.

Features:
- Multi-language project analysis (Python, Rust, JS, TS)
- Function/class/route extraction
- Thea integration for guidance
- Configurable project paths
- Caching for performance

Usage:
    python tools/project_scanner.py /path/to/project
    python tools/project_scanner.py /path/to/project --no-thea
    python tools/project_scanner.py --help

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    """Main CLI entry point for project scanning."""
    parser = argparse.ArgumentParser(
        description="Universal Project Scanner with AI Guidance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  python tools/project_scanner.py

  # Scan specific project
  python tools/project_scanner.py /path/to/my/project

  # Scan without Thea guidance
  python tools/project_scanner.py /path/to/project --no-thea

  # Force fresh scan (ignore cache)
  python tools/project_scanner.py /path/to/project --force

  # Save results to specific file
  python tools/project_scanner.py /path/to/project --output scan_results.json
        """
    )

    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to project to scan (default: current directory)"
    )

    parser.add_argument(
        "--no-thea",
        action="store_true",
        help="Skip sending results to Thea for guidance"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force fresh scan (ignore cached results)"
    )

    parser.add_argument(
        "--output",
        help="Save results to specific JSON file"
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed output"
    )

    args = parser.parse_args()

    try:
        # Add project root to path
        project_root = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(project_root))

        # Import scanner integration
        from src.core.project_scanner_integration import ProjectScannerIntegration

        # Initialize scanner
        scanner = ProjectScannerIntegration(project_root)

        # Resolve project path
        project_path = Path(args.project_path).resolve()

        if not args.quiet:
            print(f"🔍 Scanning project: {project_path}")
            if args.force:
                print("⚡ Force rescan enabled")
            if not args.no_thea:
                print("🤖 Will request Thea guidance")

        # Perform scan
        results = scanner.scan_project(
            project_path=project_path,
            send_to_thea=not args.no_thea,
            force_rescan=args.force
        )

        if "error" in results:
            print(f"❌ Scan failed: {results['error']}", file=sys.stderr)
            return 1

        # Display results
        if not args.quiet:
            metadata = results.get("scan_metadata", {})
            scan_data = results.get("scan_data", {})

            print("\n✅ Project scan completed!")
            print(f"📊 Files analyzed: {len(scan_data)}")
            print(f"⏰ Scan duration: {metadata.get('scan_duration', 'Unknown')}s")
            print(f"📁 Project: {metadata.get('project_path', 'Unknown')}")

            # Show languages detected
            languages = set()
            for file_data in scan_data.values():
                if isinstance(file_data, dict):
                    lang = file_data.get("language")
                    if lang:
                        languages.add(lang)

            if languages:
                print(f"💻 Languages: {', '.join(sorted(languages))}")

            # Show Thea guidance if available
            thea_guidance = results.get("thea_guidance")
            if thea_guidance and "error" not in thea_guidance:
                priority_tasks = thea_guidance.get("priority_tasks", [])
                if priority_tasks:
                    print(f"\n🎯 Thea Guidance - Priority Tasks:")
                    for i, task in enumerate(priority_tasks[:5], 1):
                        print(f"   {i}. {task}")

                architectural_notes = thea_guidance.get("architectural_notes", [])
                if architectural_notes and not args.quiet:
                    print(f"\n🏗️  Architectural Notes:")
                    for note in architectural_notes[:3]:
                        print(f"   • {note}")

        # Save to output file if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            if not args.quiet:
                print(f"\n💾 Results saved to: {output_path}")

        # Cache location info
        if not args.quiet:
            cache_info = scanner.get_scan_history()
            cache_location = cache_info.get("cache_location", "Unknown")
            print(f"\n📂 Cached results: {cache_location}")

        return 0

    except ImportError as e:
        print(f"❌ Import error: {e}", file=sys.stderr)
        print("💡 Make sure you're running from the Agent Cellphone V2 repository root", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())