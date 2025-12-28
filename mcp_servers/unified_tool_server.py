#!/usr/bin/env python3
"""
Unified Tool MCP Server
Exposes all tools through a single MCP interface using tool registry
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.tool_registry import ToolRegistry
    from tools.adapters.error_types import ToolNotFoundError, ToolExecutionError
    HAS_TOOL_REGISTRY = True
except ImportError:
    HAS_TOOL_REGISTRY = False


def list_all_tools() -> Dict[str, Any]:
    """List all available tools from registry."""
    if not HAS_TOOL_REGISTRY:
        return {
            "success": False,
            "error": "Tool registry not available"
        }
    
    try:
        registry = ToolRegistry()
        tools = registry.list_tools()
        categories = registry.get_categories()
        
        # Group tools by category
        tools_by_category = {}
        for category in categories:
            tools_by_category[category] = registry.list_by_category(category)
        
        return {
            "success": True,
            "tools": tools,
            "categories": categories,
            "tools_by_category": tools_by_category,
            "total_count": len(tools)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_tool_info(tool_name: str) -> Dict[str, Any]:
    """Get tool metadata and documentation."""
    if not HAS_TOOL_REGISTRY:
        return {
            "success": False,
            "error": "Tool registry not available"
        }
    
    try:
        registry = ToolRegistry()
        tool_class = registry.get_tool_class(tool_name)
        tool_instance = tool_class()
        spec = tool_instance.get_spec()
        
        return {
            "success": True,
            "name": spec.name,
            "description": spec.description,
            "category": spec.category,
            "parameters": spec.parameters,
            "examples": spec.examples if hasattr(spec, 'examples') else []
        }
    except ToolNotFoundError as e:
        return {
            "success": False,
            "error": f"Tool not found: {tool_name}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def execute_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Execute a tool by name with provided parameters."""
    if not HAS_TOOL_REGISTRY:
        return {
            "success": False,
            "error": "Tool registry not available"
        }
    
    try:
        registry = ToolRegistry()
        tool_class = registry.get_tool_class(tool_name)
        tool_instance = tool_class()
        result = tool_instance.execute(**kwargs)
        
        return {
            "success": True,
            "tool": tool_name,
            "result": result
        }
    except ToolNotFoundError as e:
        return {
            "success": False,
            "error": f"Tool not found: {tool_name}"
        }
    except ToolExecutionError as e:
        return {
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def search_tools(query: str) -> Dict[str, Any]:
    """Search tools by name or description."""
    if not HAS_TOOL_REGISTRY:
        return {
            "success": False,
            "error": "Tool registry not available"
        }
    
    try:
        registry = ToolRegistry()
        all_tools = registry.list_tools()
        
        # Simple search by name/description
        matching_tools = []
        query_lower = query.lower()
        
        for tool_name in all_tools:
            if query_lower in tool_name.lower():
                matching_tools.append(tool_name)
            else:
                # Try to get tool info for description search
                try:
                    tool_info = get_tool_info(tool_name)
                    if tool_info.get("success"):
                        description = tool_info.get("description", "").lower()
                        if query_lower in description:
                            matching_tools.append(tool_name)
                except Exception:
                    continue
        
        return {
            "success": True,
            "query": query,
            "matches": matching_tools,
            "count": len(matching_tools)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# MCP Server Protocol
def main():
    """MCP server main loop."""
    # Send initialize response
    print(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "unified-tool-server",
                        "version": "1.0.0"
                    }
                }
            }
        )
    )

    # Handle tool calls
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "tools/list":
                # List all available tools
                tools_result = list_all_tools()
                
                # Convert to MCP tools format
                mcp_tools = []
                if tools_result.get("success"):
                    for tool_name in tools_result.get("tools", []):
                        tool_info = get_tool_info(tool_name)
                        if tool_info.get("success"):
                            mcp_tools.append({
                                "name": tool_info["name"],
                                "description": tool_info["description"],
                                "inputSchema": {
                                    "type": "object",
                                    "properties": tool_info.get("parameters", {}),
                                    "required": []
                                }
                            })
                
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "tools": mcp_tools
                            }
                        }
                    )
                )

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name == "list_all_tools":
                    result = list_all_tools()
                elif tool_name == "get_tool_info":
                    result = get_tool_info(arguments.get("tool_name", ""))
                elif tool_name == "execute_tool":
                    tool_to_execute = arguments.get("tool_name", "")
                    tool_args = arguments.get("parameters", {})
                    result = execute_tool(tool_to_execute, **tool_args)
                elif tool_name == "search_tools":
                    result = search_tools(arguments.get("query", ""))
                else:
                    # Try to execute as direct tool name
                    result = execute_tool(tool_name, **arguments)
                
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result)
                                    }
                                ]
                            }
                        }
                    )
                )

        except json.JSONDecodeError:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if 'request' in locals() else None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                )
            )
        except Exception as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if 'request' in locals() else None,
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }
                )
            )


if __name__ == "__main__":
    main()



