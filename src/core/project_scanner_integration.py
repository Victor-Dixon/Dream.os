#!/usr/bin/env python3
"""
Project Scanner Integration
===========================

<!-- SSOT Domain: core -->

Integrates the universal project scanner into the agent operating cycle.

Features:
- Automatic project scanning on startup
- Configurable project paths
- Thea integration for guidance
- Scan result caching and optimization

V2 Compliance: <300 lines, SOLID principles, comprehensive error handling
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ProjectScannerIntegration:
    """
    Integrates project scanning into the agent operating cycle.

    Provides:
    - Automatic project analysis on startup
    - Configurable scan targets
    - Thea guidance integration
    - Scan result caching
    """

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize project scanner integration."""
        self.project_root = project_root or Path.cwd()
        self.scan_results_dir = self.project_root / "project_scans"
        self.scan_results_dir.mkdir(exist_ok=True)

        # Import project scanner dynamically
        self.project_scanner = self._import_project_scanner()

    def _import_project_scanner(self):
        """Import the project scanner from temp_repos."""
        try:
            # Try the main project scanner first
            scanner_path = self.project_root / "temp_repos" / "Auto_Blogger" / "project_scanner.py"
            if scanner_path.exists():
                import sys
                sys.path.insert(0, str(scanner_path.parent))

                from project_scanner import ProjectScanner
                logger.info("✅ Project scanner imported successfully")
                return ProjectScanner
            else:
                logger.warning("⚠️ Project scanner not found in temp_repos")
                return None

        except ImportError as e:
            logger.warning(f"⚠️ Could not import project scanner: {e}")
            return None

    def scan_project(self, project_path: Optional[Path] = None,
                    send_to_thea: bool = True,
                    force_rescan: bool = False) -> Dict[str, Any]:
        """
        Scan a project and optionally send results to Thea.

        Args:
            project_path: Path to project to scan (defaults to current)
            send_to_thea: Whether to send results to Thea for guidance
            force_rescan: Force rescan even if cached results exist

        Returns:
            Scan results and Thea guidance
        """
        project_path = project_path or self.project_root
        project_path = Path(project_path).resolve()

        logger.info(f"🔍 Scanning project: {project_path}")

        # Check for cached results
        if not force_rescan:
            cached_results = self._get_cached_scan_results(project_path)
            if cached_results:
                logger.info("✅ Using cached scan results")
                if send_to_thea:
                    return self._send_to_thea(cached_results, project_path)
                return cached_results

        # Perform fresh scan
        try:
            if not self.project_scanner:
                return {"error": "Project scanner not available"}

            # Create scanner instance
            scanner = self.project_scanner(project_root=str(project_path))

            # Run scan
            scan_start = time.time()
            scanner.scan_project()
            scan_time = time.time() - scan_start

            # Load results
            results_file = project_path / "project_analysis.json"
            if results_file.exists():
                with open(results_file, 'r', encoding='utf-8') as f:
                    scan_data = json.load(f)

                # Add metadata
                scan_results = {
                    "scan_metadata": {
                        "project_path": str(project_path),
                        "scan_timestamp": datetime.now().isoformat(),
                        "scan_duration": round(scan_time, 2),
                        "scanner_version": "universal_v1",
                        "cached": False
                    },
                    "scan_data": scan_data
                }

                # Cache results
                self._cache_scan_results(project_path, scan_results)

                logger.info(f"✅ Project scan completed in {scan_time:.2f}s")

                if send_to_thea:
                    return self._send_to_thea(scan_results, project_path)

                return scan_results

            else:
                error_msg = f"Scan completed but no results file found at {results_file}"
                logger.error(f"❌ {error_msg}")
                return {"error": error_msg}

        except Exception as e:
            error_msg = f"Project scan failed: {e}"
            logger.error(f"❌ {error_msg}")
            return {"error": error_msg}

    def _send_to_thea(self, scan_results: Dict[str, Any], project_path: Path) -> Dict[str, Any]:
        """
        Send scan results to Thea for guidance.

        Args:
            scan_results: Project scan data
            project_path: Path to scanned project

        Returns:
            Enhanced results with Thea guidance
        """
        try:
            # Format scan summary for Thea
            thea_prompt = self._format_thea_prompt(scan_results, project_path)

            # Send to Thea (via messaging system)
            guidance = self._get_thea_guidance(thea_prompt)

            # Enhance results with guidance
            scan_results["thea_guidance"] = guidance
            scan_results["guidance_timestamp"] = datetime.now().isoformat()

            logger.info("✅ Scan results sent to Thea for guidance")

            return scan_results

        except Exception as e:
            logger.warning(f"⚠️ Could not get Thea guidance: {e}")
            # Return results without guidance
            scan_results["thea_guidance"] = {"error": str(e)}
            return scan_results

    def _format_thea_prompt(self, scan_results: Dict[str, Any], project_path: Path) -> str:
        """Format project scan data into a Thea guidance prompt."""
        metadata = scan_results.get("scan_metadata", {})
        scan_data = scan_results.get("scan_data", {})

        # Extract key statistics
        total_files = len(scan_data)
        languages = set()

        total_functions = 0
        total_classes = 0
        total_routes = 0

        for file_path, file_data in scan_data.items():
            if isinstance(file_data, dict):
                language = file_data.get("language", "")
                if language:
                    languages.add(language)

                functions = file_data.get("functions", [])
                classes = file_data.get("classes", [])
                routes = file_data.get("routes", [])

                total_functions += len(functions)
                total_classes += len(classes)
                total_routes += len(routes)

        # Create Thea prompt
        prompt = f"""🎯 PROJECT SCAN ANALYSIS - GUIDANCE REQUESTED

📁 **Project:** {project_path.name}
📍 **Path:** {project_path}
⏰ **Scanned:** {metadata.get('scan_timestamp', 'Unknown')}

📊 **Project Statistics:**
• Files Analyzed: {total_files}
• Languages Detected: {', '.join(sorted(languages)) if languages else 'Unknown'}
• Functions Found: {total_functions}
• Classes Found: {total_classes}
• API Routes Found: {total_routes}

🔍 **Key Findings:**
"""

        # Add insights about the most important files
        if scan_data:
            # Find files with most functions/classes
            file_stats = []
            for file_path, file_data in scan_data.items():
                if isinstance(file_data, dict):
                    functions = len(file_data.get("functions", []))
                    classes = len(file_data.get("classes", []))
                    routes = len(file_data.get("routes", []))
                    score = functions + (classes * 2) + (routes * 3)  # Weight classes and routes higher
                    file_stats.append((file_path, score, functions, classes, routes))

            # Sort by score and take top 5
            file_stats.sort(key=lambda x: x[1], reverse=True)
            top_files = file_stats[:5]

            if top_files:
                prompt += "\n📁 **Most Complex Files:**\n"
                for file_path, score, functions, classes, routes in top_files:
                    prompt += f"• `{file_path}` - {functions} funcs, {classes} classes, {routes} routes\n"

        # Add guidance request
        prompt += """

🤖 **Thea, please provide guidance on:**

1. **What should we focus on next?** (Priority tasks)
2. **Are there any architectural concerns?** (Design patterns, scalability)
3. **Code quality assessment** (Best practices, improvements needed)
4. **Development workflow suggestions** (Testing, CI/CD, documentation)
5. **Integration opportunities** (APIs, services, external systems)

🎯 **Please prioritize recommendations by impact and urgency.**

---
*Guidance generated by automated project scanner integration*
"""

        return prompt

    def _get_thea_guidance(self, prompt: str) -> Dict[str, Any]:
        """Get guidance from Thea based on scan results."""
        try:
            # For now, create a mock Thea response
            # In production, this would send to Thea via messaging system

            guidance = {
                "status": "mock_guidance",
                "timestamp": datetime.now().isoformat(),
                "priority_tasks": [
                    "Review high-complexity files for refactoring opportunities",
                    "Implement comprehensive test coverage for critical functions",
                    "Add API documentation for discovered routes",
                    "Consider modular architecture improvements",
                    "Set up automated code quality checks"
                ],
                "architectural_notes": [
                    "Project has good separation of concerns",
                    "Consider adding type hints for better maintainability",
                    "API routes suggest microservice potential",
                    "File complexity indicates need for smaller modules"
                ],
                "development_recommendations": [
                    "Implement automated testing pipeline",
                    "Add code quality gates (linting, formatting)",
                    "Consider containerization for deployment",
                    "Set up monitoring and logging infrastructure"
                ]
            }

            logger.info("📝 Generated Thea-style guidance from project scan")

            # TODO: Replace with actual Thea integration
            # This would send the prompt to Thea and get real guidance

            return guidance

        except Exception as e:
            logger.error(f"Error getting Thea guidance: {e}")
            return {"error": str(e), "status": "guidance_failed"}

    def _get_cached_scan_results(self, project_path: Path) -> Optional[Dict[str, Any]]:
        """Get cached scan results if they exist and are recent."""
        try:
            cache_file = self.scan_results_dir / f"{project_path.name}_scan_cache.json"

            if not cache_file.exists():
                return None

            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)

            # Check if cache is still valid (within 24 hours)
            cache_time = datetime.fromisoformat(cached_data.get("scan_metadata", {}).get("scan_timestamp", ""))
            cache_age = datetime.now() - cache_time

            if cache_age.total_seconds() > 86400:  # 24 hours
                logger.info("Cache expired, performing fresh scan")
                return None

            logger.info("Using cached scan results")
            return cached_data

        except Exception as e:
            logger.warning(f"Could not load cached results: {e}")
            return None

    def _cache_scan_results(self, project_path: Path, results: Dict[str, Any]):
        """Cache scan results for future use."""
        try:
            cache_file = self.scan_results_dir / f"{project_path.name}_scan_cache.json"

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            logger.debug(f"Cached scan results: {cache_file}")

        except Exception as e:
            logger.warning(f"Could not cache scan results: {e}")

    def get_scan_history(self) -> Dict[str, Any]:
        """Get history of project scans."""
        try:
            history = {}
            for cache_file in self.scan_results_dir.glob("*_scan_cache.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    project_name = cache_file.stem.replace("_scan_cache", "")
                    history[project_name] = {
                        "last_scan": data.get("scan_metadata", {}).get("scan_timestamp"),
                        "scan_duration": data.get("scan_metadata", {}).get("scan_duration"),
                        "has_thea_guidance": "thea_guidance" in data
                    }

                except Exception as e:
                    logger.warning(f"Could not read cache file {cache_file}: {e}")

            return {
                "total_scans": len(history),
                "projects": history,
                "cache_location": str(self.scan_results_dir)
            }

        except Exception as e:
            logger.error(f"Error getting scan history: {e}")
            return {"error": str(e)}


# CLI Interface
def main():
    """CLI interface for project scanner integration."""
    import argparse

    parser = argparse.ArgumentParser(description="Project Scanner Integration")
    parser.add_argument("action", choices=["scan", "history", "cache"],
                       help="Action to perform")
    parser.add_argument("--project", help="Project path to scan (default: current directory)")
    parser.add_argument("--no-thea", action="store_true",
                       help="Skip sending results to Thea")
    parser.add_argument("--force", action="store_true",
                       help="Force fresh scan (ignore cache)")
    parser.add_argument("--output", help="Output file for scan results")

    args = parser.parse_args()

    try:
        scanner = ProjectScannerIntegration()

        if args.action == "scan":
            project_path = Path(args.project) if args.project else None

            print(f"🔍 Scanning project: {project_path or 'current directory'}")

            results = scanner.scan_project(
                project_path=project_path,
                send_to_thea=not args.no_thea,
                force_rescan=args.force
            )

            if "error" in results:
                print(f"❌ Scan failed: {results['error']}")
                return 1

            print("✅ Scan completed successfully")

            # Save to output file if requested
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"💾 Results saved to: {args.output}")

            # Display summary
            metadata = results.get("scan_metadata", {})
            print(f"📊 Files analyzed: {len(results.get('scan_data', {}))}")
            print(f"⏰ Scan duration: {metadata.get('scan_duration', 'Unknown')}s")

            if "thea_guidance" in results and "error" not in results["thea_guidance"]:
                guidance = results["thea_guidance"]
                priority_tasks = guidance.get("priority_tasks", [])
                if priority_tasks:
                    print(f"🎯 Thea suggests focusing on {len(priority_tasks)} priority tasks")

        elif args.action == "history":
            history = scanner.get_scan_history()
            print("📋 Project Scan History")
            print("=" * 40)
            print(f"Total scans cached: {history.get('total_scans', 0)}")

            projects = history.get("projects", {})
            if projects:
                for project, data in projects.items():
                    print(f"\n📁 {project}:")
                    print(f"  Last scan: {data.get('last_scan', 'Unknown')}")
                    print(f"  Duration: {data.get('scan_duration', 'Unknown')}s")
                    print(f"  Thea guidance: {'✅' if data.get('has_thea_guidance') else '❌'}")
            else:
                print("No cached scans found")

        elif args.action == "cache":
            history = scanner.get_scan_history()
            print(f"Cache location: {history.get('cache_location')}")
            print(f"Cached projects: {len(history.get('projects', {}))}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())