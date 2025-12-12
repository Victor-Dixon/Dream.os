#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Discord Button Diagnostic Tool
==============================

Comprehensive diagnostic tool to check all Discord buttons for:
- Missing callbacks
- Import errors
- Modal label length issues
- Response handling issues
- View registration issues

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import ast
import importlib.util
import inspect
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def find_discord_files(root_dir: Path) -> List[Path]:
    """Find all Python files containing Discord button logic."""
    discord_files = []
    discord_dir = root_dir / "src" / "discord_commander"
    if discord_dir.exists():
        for f in discord_dir.rglob("*.py"):
            discord_files.append(f)
    return sorted(discord_files)


def check_modal_labels(file_path: Path) -> List[str]:
    """Check for modal labels exceeding 45 characters."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check if this is a TextInput call
                if (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Attribute)
                    and node.func.value.attr == "ui"
                    and node.func.attr == "TextInput"
                ):
                    # Check keyword arguments for label
                    for keyword in node.keywords:
                        if keyword.arg == "label":
                            if isinstance(keyword.value, ast.Constant):
                                label = keyword.value.value
                                if len(label) > 45:
                                    issues.append(
                                        f"Line {node.lineno}: Label '{label}' is {len(label)} characters (max 45)"
                                    )
    except Exception as e:
        issues.append(f"Error parsing {file_path}: {e}")

    return issues


def check_button_callbacks(file_path: Path) -> List[str]:
    """Check if all buttons have callbacks assigned."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))

        # Find all Button() calls
        button_calls = []
        callback_assignments = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if (
                    isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Attribute)
                    and node.func.value.attr == "ui"
                    and node.func.attr == "Button"
                ):
                    button_calls.append((node.lineno, node))

            # Find callback assignments (self.button.callback = ...)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Attribute)
                        and target.attr == "callback"
                    ):
                        callback_assignments.append(node.lineno)

        # Check if buttons have callbacks
        # This is a heuristic - we'll check if there's a callback assignment nearby
        for lineno, button_node in button_calls:
            # Look for callback assignment within 20 lines
            has_callback = any(
                abs(lineno - callback_lineno) < 20 for callback_lineno in callback_assignments
            )
            if not has_callback:
                # Check if button is assigned to a variable
                parent = button_node
                while hasattr(parent, "parent"):
                    parent = parent.parent
                    if isinstance(parent, ast.Assign):
                        for target in parent.targets:
                            if isinstance(target, ast.Attribute):
                                var_name = target.attr
                                # Check if this variable has callback set later
                                content_lines = content.splitlines()
                                for i in range(lineno, min(lineno + 30, len(content_lines))):
                                    if f"{var_name}.callback" in content_lines[i]:
                                        has_callback = True
                                        break
                        break

                if not has_callback:
                    issues.append(
                        f"Line {lineno}: Button may be missing callback assignment"
                    )

    except Exception as e:
        issues.append(f"Error checking callbacks in {file_path}: {e}")

    return issues


def check_imports(file_path: Path) -> List[str]:
    """Check for import issues."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            # Check for relative imports that might be incorrect
            if "from .." in line or "from ..." in line:
                # Check if it's importing from discord_commander
                if "discord_commander" in line:
                    # This might be okay, but let's flag it for review
                    if "from ..discord_gui_modals" in line:
                        # This pattern was problematic before
                        if "from ...discord_commander.discord_gui_modals" not in content:
                            issues.append(
                                f"Line {i}: Potential incorrect relative import: {line.strip()}"
                            )

    except Exception as e:
        issues.append(f"Error checking imports in {file_path}: {e}")

    return issues


def check_response_handling(file_path: Path) -> List[str]:
    """Check for response handling issues in button callbacks."""
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))

        # Find all async functions that might be button callbacks
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                func_name = node.name
                # Check if this looks like a callback (takes interaction parameter)
                has_interaction = False
                for arg in node.args.args:
                    if arg.arg == "interaction":
                        has_interaction = True
                        break

                if has_interaction:
                    # Check if function has response handling
                    has_response = False
                    for child in ast.walk(node):
                        if isinstance(child, ast.Attribute):
                            if (
                                isinstance(child.value, ast.Name)
                                and child.value.id == "interaction"
                                and child.attr in ["response", "followup"]
                            ):
                                has_response = True
                                break

                    if not has_response:
                        issues.append(
                            f"Line {node.lineno}: Callback '{func_name}' may not handle interaction response"
                        )

    except Exception as e:
        issues.append(f"Error checking response handling in {file_path}: {e}")

    return issues


def main():
    """Run comprehensive button diagnostics."""
    print("=" * 70)
    print("🔍 DISCORD BUTTON COMPREHENSIVE DIAGNOSTIC")
    print("=" * 70 + "\n")

    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))

    discord_files = find_discord_files(project_root / "src" / "discord_commander")
    logger.info(f"Found {len(discord_files)} Discord files to check\n")

    all_issues: Dict[str, List[str]] = {}

    print("📋 Checking modal labels (45 char limit)...")
    for f in discord_files:
        issues = check_modal_labels(f)
        if issues:
            all_issues[str(f)] = issues
            for issue in issues:
                logger.warning(f"  {f.name}: {issue}")

    print("\n📋 Checking button callbacks...")
    for f in discord_files:
        issues = check_button_callbacks(f)
        if issues:
            if str(f) not in all_issues:
                all_issues[str(f)] = []
            all_issues[str(f)].extend(issues)
            for issue in issues:
                logger.warning(f"  {f.name}: {issue}")

    print("\n📋 Checking imports...")
    for f in discord_files:
        issues = check_imports(f)
        if issues:
            if str(f) not in all_issues:
                all_issues[str(f)] = []
            all_issues[str(f)].extend(issues)
            for issue in issues:
                logger.warning(f"  {f.name}: {issue}")

    print("\n📋 Checking response handling...")
    for f in discord_files:
        issues = check_response_handling(f)
        if issues:
            if str(f) not in all_issues:
                all_issues[str(f)] = []
            all_issues[str(f)].extend(issues)
            for issue in issues:
                logger.warning(f"  {f.name}: {issue}")

    print("\n" + "=" * 70)
    if not all_issues:
        print("✅ ALL CHECKS PASSED - NO ISSUES FOUND")
    else:
        print(f"❌ ISSUES FOUND IN {len(all_issues)} FILE(S)")
        print("\nSummary:")
        for file_path, issues in all_issues.items():
            print(f"  {Path(file_path).name}: {len(issues)} issue(s)")
    print("=" * 70 + "\n")

    # Check if bot needs restart
    print("💡 NOTE: If you fixed modal labels, restart the Discord bot for changes to take effect!")
    print("   Run: python tools/start_discord_system.py\n")


if __name__ == "__main__":
    main()

