#!/usr/bin/env python3
"""
Infrastructure Tools - Agent Toolbelt V2
========================================

Infrastructure analysis and optimization tools for agents.
Created based on Agent-3 session learnings.

Author: Agent-3 (Infrastructure & DevOps) - Toolbelt Expansion
License: MIT
"""

import logging
from pathlib import Path
from typing import Any

from ..adapters.base_adapter import IToolAdapter, ToolResult, ToolSpec

logger = logging.getLogger(__name__)


class OrchestratorScanTool(IToolAdapter):
    """Scan all orchestrators for violations and performance issues."""

    def get_name(self) -> str:
        return "orchestrator_scan"

    def get_description(self) -> str:
        return "Scan all orchestrator files for V2 violations and performance bottlenecks"

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="orchestrator_scan",
            version="1.0.0",
            category="infrastructure",
            summary="Scan all orchestrator files for V2 violations and performance bottlenecks",
            required_params=[],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters (no required params for this tool)."""
        return (True, [])

    def execute(
        self, params: dict[str, Any] = None, context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Execute orchestrator scan."""
        try:
            violations = []
            all_orchestrators = []

            # Find all orchestrator files
            patterns = ["*orchestrat*.py"]
            for pattern in patterns:
                files = list(Path(".").rglob(pattern))
                for f in files:
                    if f.is_file():
                        try:
                            lines = len(open(f).readlines())
                            all_orchestrators.append((str(f), lines))

                            # Check for violations
                            if lines > 400:
                                violations.append(
                                    {
                                        "file": str(f),
                                        "lines": lines,
                                        "severity": "CRITICAL",
                                        "over_limit": lines - 400,
                                    }
                                )
                            elif lines > 300:
                                violations.append(
                                    {
                                        "file": str(f),
                                        "lines": lines,
                                        "severity": "HIGH",
                                        "over_limit": lines - 300,
                                    }
                                )
                            elif lines > 250:
                                violations.append(
                                    {
                                        "file": str(f),
                                        "lines": lines,
                                        "severity": "MEDIUM",
                                        "approaching_limit": 400 - lines,
                                    }
                                )
                        except:
                            pass

            # Sort by line count
            all_orchestrators.sort(key=lambda x: x[1], reverse=True)
            violations.sort(key=lambda x: x.get("lines", 0), reverse=True)

            output = {
                "total_orchestrators": len(all_orchestrators),
                "violations": violations,
                "violation_count": len(violations),
                "top_10_largest": [
                    {"file": f, "lines": lines} for f, lines in all_orchestrators[:10]
                ],
            }
            return ToolResult(success=True, output=output)

        except Exception as e:
            logger.error(f"Orchestrator scan failed: {e}")
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class FileLineCounterTool(IToolAdapter):
    """Quick line count for files (V2 compliance checking)."""

    def get_name(self) -> str:
        return "file_lines"

    def get_description(self) -> str:
        return "Count lines in file(s) for V2 compliance verification"

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="file_lines",
            version="1.0.0",
            category="infrastructure",
            summary="Count lines in file(s) for V2 compliance verification",
            required_params=["files"],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(
        self, params: dict[str, Any] = None, context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Execute line count."""
        try:
            if params is None:
                params = {}
            files = params.get("files", [])
            if isinstance(files, str):
                files = [files]

            results = []
            for filepath in files:
                try:
                    lines = len(open(filepath).readlines())
                    compliant = lines <= 400
                    results.append(
                        {
                            "file": filepath,
                            "lines": lines,
                            "v2_compliant": compliant,
                            "buffer": 400 - lines if compliant else None,
                            "over_by": lines - 400 if not compliant else None,
                        }
                    )
                except Exception as e:
                    results.append({"file": filepath, "error": str(e)})

            output = {
                "results": results,
                "total_files": len(results),
                "compliant_count": sum(1 for r in results if r.get("v2_compliant")),
            }
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class ModuleExtractorPlannerTool(IToolAdapter):
    """Analyze file and suggest extraction opportunities."""

    def get_name(self) -> str:
        return "extract_planner"

    def get_description(self) -> str:
        return "Analyze file and suggest modular extraction plan"

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="extract_planner",
            version="1.0.0",
            category="infrastructure",
            summary="Analyze file and suggest modular extraction plan",
            required_params=["file"],
            optional_params={},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        spec = self.get_spec()
        return spec.validate_params(params)

    def execute(
        self, params: dict[str, Any] = None, context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Execute extraction planning."""
        try:
            if params is None:
                params = {}
            filepath = params.get("file")
            if not filepath:
                return ToolResult(
                    success=False, output=None, error_message="No file specified", exit_code=1
                )

            with open(filepath) as f:
                content = f.read()
                lines = content.splitlines()

            # Count classes and functions
            classes = [l.strip() for l in lines if l.strip().startswith("class ")]
            functions = [l.strip() for l in lines if "def " in l and not l.strip().startswith("#")]
            imports = [l.strip() for l in lines if l.strip().startswith(("import ", "from "))]

            # Suggest extractions
            suggestions = []

            if len(classes) > 5:
                suggestions.append(
                    {
                        "type": "class_extraction",
                        "reason": f"{len(classes)} classes (>5 limit)",
                        "recommendation": "Extract classes into logical groups",
                    }
                )

            if len(functions) > 30:
                suggestions.append(
                    {
                        "type": "function_extraction",
                        "reason": f"{len(functions)} functions (high count)",
                        "recommendation": "Group related functions into modules",
                    }
                )

            if len(lines) > 400:
                suggestions.append(
                    {
                        "type": "file_size",
                        "reason": f"{len(lines)} lines (>400 V2 limit)",
                        "recommendation": f"Extract {len(lines) - 400}+ lines",
                    }
                )

            output = {
                "file": filepath,
                "metrics": {
                    "lines": len(lines),
                    "classes": len(classes),
                    "functions": len(functions),
                    "imports": len(imports),
                },
                "class_list": classes[:20],  # First 20
                "function_list": functions[:20],
                "suggestions": suggestions,
                "needs_extraction": len(suggestions) > 0,
            }
            return ToolResult(success=True, output=output)

        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class ROICalculatorTool(IToolAdapter):
    """Calculate ROI for refactoring tasks."""

    def get_name(self) -> str:
        return "roi_calculator"

    def get_description(self) -> str:
        return "Calculate ROI for refactoring tasks (points/complexity)"

    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="roi_calculator", version="1.0.0", category="infrastructure",
            summary="Calculate ROI for refactoring tasks",
            required_params=["points", "complexity"],
            optional_params={"v2_impact": 0, "autonomy_impact": 0},
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return self.get_spec().validate_params(params)

    def execute(
        self, params: dict[str, Any] = None, context: dict[str, Any] | None = None
    ) -> ToolResult:
        try:
            params = params or {}
            reward = params.get("points", 0) + (params.get("v2_impact", 0) * 100) + (params.get("autonomy_impact", 0) * 200)
            roi = reward / max(params.get("complexity", 1), 1)
            return ToolResult(success=True, output={
                **params, "reward": reward, "roi": round(roi, 2),
                "rating": "EXCELLENT" if roi > 20 else "GOOD" if roi > 15 else "FAIR" if roi > 10 else "LOW"
            })
        except Exception as e:
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class WorkspaceHealthMonitorTool(IToolAdapter):
    """Monitor workspace health for agent workspaces."""
    def get_name(self) -> str:
        return "workspace_health_monitor"
    def get_description(self) -> str:
        return "Monitor agent workspace health (inbox, status, recommendations)"
    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="workspace_health_monitor", version="1.0.0", category="infrastructure",
            summary="Monitor agent workspace health", required_params=[],
            optional_params={"agent_id": None, "check_all": False})
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])
    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
            from workspace_health_monitor import WorkspaceHealthMonitor
            params = params or {}
            monitor = WorkspaceHealthMonitor()
            if params.get("check_all"):
                results = monitor.check_all_workspaces()
                output = {"mode": "all", "results": {k: {"score": v.health_score, "inbox": v.inbox_count,
                    "old": v.old_messages, "status_ok": v.status_file_current, "recs": v.recommendations}
                    for k, v in results.items()}}
            elif params.get("agent_id"):
                h = monitor.check_agent_workspace(params["agent_id"])
                output = {"agent_id": params["agent_id"], "score": h.health_score,
                    "inbox": h.inbox_count, "old": h.old_messages, "recs": h.recommendations}
            else:
                return ToolResult(success=False, output=None,
                    error_message="Must specify agent_id or check_all=True", exit_code=1)
            return ToolResult(success=True, output=output)
        except Exception as e:
            logger.error(f"Workspace health monitor failed: {e}")
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)

class WorkspaceAutoCleanerTool(IToolAdapter):
    """Automated workspace cleanup tool."""
    def get_name(self) -> str:
        return "workspace_auto_cleaner"
    def get_description(self) -> str:
        return "Automated workspace cleanup (archive old messages, clean temp files)"
    def get_spec(self) -> ToolSpec:
        return ToolSpec(name="workspace_auto_cleaner", version="1.0.0", category="infrastructure",
            summary="Automated workspace cleanup", required_params=["agent_id"],
            optional_params={"archive": False, "clean_temp": False, "full": False, "dry_run": True})
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return self.get_spec().validate_params(params)
    def execute(self, params: dict[str, Any] = None, context: dict[str, Any] | None = None) -> ToolResult:
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))
            from workspace_auto_cleaner import archive_old_messages, clean_temp_files, organize_workspace
            params = params or {}
            agent_id = params.get("agent_id")
            if not agent_id:
                return ToolResult(success=False, output=None, error_message="agent_id required", exit_code=1)
            dry_run = params.get("dry_run", True)
            full = params.get("full", False)
            results = {}
            if params.get("archive") or full:
                results["archived"] = archive_old_messages(agent_id, dry_run=dry_run)
            if params.get("clean_temp") or full:
                results["cleaned"] = clean_temp_files(agent_id, dry_run=dry_run)
            if full:
                results["organized"] = organize_workspace(agent_id, dry_run=dry_run)
            return ToolResult(success=True, output={"agent_id": agent_id, "dry_run": dry_run, "results": results})
        except Exception as e:
            logger.error(f"Workspace auto cleaner failed: {e}")
            return ToolResult(success=False, output=None, error_message=str(e), exit_code=1)


class BrowserPoolManagerTool(IToolAdapter):
    """Manage browser instance pool for performance optimization."""

    def get_spec(self) -> ToolSpec:
        """Get tool specification."""
        return ToolSpec(
            name="browser.pool",
            version="1.0.0",
            category="infrastructure",
            summary="Manage browser instance pool for 20%+ performance improvement",
            required_params=[],
            optional_params={
                "pool_size": 3,
                "max_lifetime_minutes": 60,
                "max_usage_per_instance": 100,
                "headless": True,
                "action": "get",  # get, cleanup, status
            },
        )

    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate parameters."""
        return (True, [])  # No required params

    def execute(
        self, params: dict[str, Any], context: dict[str, Any] | None = None
    ) -> ToolResult:
        """Execute browser pool management."""
        try:
            import sys
            from pathlib import Path

            tools_path = Path(__file__).parent.parent.parent / "tools"
            sys.path.insert(0, str(tools_path))

            from browser_pool_manager import BrowserPoolManager

            pool_size = params.get("pool_size", 3)
            max_lifetime = params.get("max_lifetime_minutes", 60)
            max_usage = params.get("max_usage_per_instance", 100)
            headless = params.get("headless", True)
            action = params.get("action", "get")

            manager = BrowserPoolManager(
                pool_size=pool_size,
                max_lifetime_minutes=max_lifetime,
                max_usage_per_instance=max_usage,
                headless=headless,
            )

            if action == "get":
                browser = manager.get_browser()
                return ToolResult(
                    success=True,
                    output=f"Browser instance obtained from pool (size: {pool_size})",
                    exit_code=0,
                )
            elif action == "cleanup":
                manager.cleanup_expired()
                return ToolResult(
                    success=True,
                    output="Expired browser instances cleaned up",
                    exit_code=0,
                )
            elif action == "status":
                status = {
                    "pool_size": pool_size,
                    "active_instances": len(manager._pool),
                    "max_lifetime_minutes": max_lifetime,
                    "max_usage_per_instance": max_usage,
                }
                return ToolResult(success=True, output=status, exit_code=0)
            else:
                return ToolResult(
                    success=False,
                    output=None,
                    error_message=f"Unknown action: {action}",
                    exit_code=1,
                )
        except Exception as e:
            logger.error(f"Browser pool manager failed: {e}")
            return ToolResult(
                success=False, output=None, error_message=str(e), exit_code=1
            )


__all__ = [
    "OrchestratorScanTool",
    "FileLineCounterTool",
    "ModuleExtractorPlannerTool",
    "ROICalculatorTool",
    "WorkspaceHealthMonitorTool",
    "WorkspaceAutoCleanerTool",
    "BrowserPoolManagerTool",
]
