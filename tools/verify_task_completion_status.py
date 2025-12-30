#!/usr/bin/env python3
"""
Task Completion Status Verifier
Verifies if assigned tasks are already complete before starting work.

Usage:
    python tools/verify_task_completion_status.py --task "Infrastructure Refactoring" --file src/core/messaging_pyautogui.py
    python tools/verify_task_completion_status.py --task "WP-CLI MCP Server" --file mcp_servers/wp_cli_manager_server.py
"""

import argparse
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def verify_file_exists(file_path: str) -> dict:
    """Verify file exists and get basic stats."""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return {
            "exists": False,
            "error": f"File not found: {file_path}"
        }
    
    stat = full_path.stat()
    return {
        "exists": True,
        "path": str(full_path),
        "size_bytes": stat.st_size,
        "size_lines": _count_lines(full_path)
    }


def _count_lines(file_path: Path) -> int:
    """Count lines in file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def verify_refactoring_status(file_path: str, expected_services: list = None) -> dict:
    """Verify refactoring status by checking for service imports."""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return {"error": "File not found"}
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            "file_exists": True,
            "line_count": len(content.splitlines()),
            "services_found": []
        }
        
        if expected_services:
            for service in expected_services:
                if service in content:
                    results["services_found"].append(service)
        
        return results
    except Exception as e:
        return {"error": str(e)}


def verify_mcp_server(file_path: str) -> dict:
    """Verify MCP server implementation."""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return {"error": "File not found"}
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for MCP server indicators
        has_main = "def main()" in content or "if __name__" in content
        has_tools = "tools_definitions" in content or "tool_map" in content
        has_jsonrpc = "jsonrpc" in content.lower()
        
        return {
            "file_exists": True,
            "size_bytes": full_path.stat().st_size,
            "has_main": has_main,
            "has_tools": has_tools,
            "has_jsonrpc": has_jsonrpc,
            "is_mcp_server": has_main and has_tools and has_jsonrpc
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Verify task completion status")
    parser.add_argument("--task", required=True, help="Task name/description")
    parser.add_argument("--file", required=True, help="File path to verify")
    parser.add_argument("--type", choices=["refactoring", "mcp_server", "generic"], 
                       default="generic", help="Verification type")
    parser.add_argument("--services", nargs="+", help="Expected service names (for refactoring type)")
    
    args = parser.parse_args()
    
    print(f"🔍 Verifying task: {args.task}")
    print(f"📁 File: {args.file}\n")
    
    if args.type == "refactoring":
        result = verify_refactoring_status(args.file, args.services)
    elif args.type == "mcp_server":
        result = verify_mcp_server(args.file)
    else:
        result = verify_file_exists(args.file)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print("✅ Verification Results:")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    if args.type == "refactoring" and args.services:
        expected_count = len(args.services)
        found_count = len(result.get("services_found", []))
        if found_count == expected_count:
            print(f"\n✅ All {expected_count} services found - refactoring complete")
        else:
            print(f"\n⚠️  Only {found_count}/{expected_count} services found")
    
    if args.type == "mcp_server" and result.get("is_mcp_server"):
        print("\n✅ MCP server implementation verified")


if __name__ == "__main__":
    main()

