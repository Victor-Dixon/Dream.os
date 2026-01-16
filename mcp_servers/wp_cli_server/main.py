#!/usr/bin/env python3
"""
WP-CLI MCP Server Main Entry Point
===================================

<!-- SSOT Domain: web -->

Main entry point for running the WP-CLI MCP server as a standalone service.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from .mcp_server import WPCliMCPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for WP-CLI MCP server."""
    parser = argparse.ArgumentParser(description="WP-CLI MCP Server")
    parser.add_argument(
        "--wordpress-path",
        type=Path,
        help="Path to WordPress installation root"
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List available MCP tools and exit"
    )
    parser.add_argument(
        "--server-info",
        action="store_true",
        help="Show server information and exit"
    )

    args = parser.parse_args()

    # Initialize server
    server = WPCliMCPServer(args.wordpress_path)

    if args.list_tools:
        # List available tools
        tools = server.get_available_tools()
        print(json.dumps({
            "tools": tools,
            "count": len(tools)
        }, indent=2))
        return

    if args.server_info:
        # Show server information
        info = server.get_server_info()
        print(json.dumps(info, indent=2))
        return

    # Interactive mode - accept tool execution requests from stdin
    logger.info("WP-CLI MCP Server started. Waiting for tool execution requests...")

    try:
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                tool_name = request.get("tool")
                parameters = request.get("parameters", {})

                if not tool_name:
                    response = {"error": "Missing 'tool' field in request"}
                else:
                    response = server.execute_tool(tool_name, parameters)

                # Send response
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"Invalid JSON: {e}"}), flush=True)
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                print(json.dumps({"error": f"Processing error: {e}"}), flush=True)

    except KeyboardInterrupt:
        logger.info("WP-CLI MCP Server shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()