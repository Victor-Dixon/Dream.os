#!/usr/bin/env python3
"""
Migrate Tools to MCP Servers
Analyzes scattered tools and generates MCP server code
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Set

PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
MCP_SERVERS_DIR = PROJECT_ROOT / "mcp_servers"


def find_tool_functions(file_path: Path) -> List[Dict]:
    """Find tool functions in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
    except Exception as e:
        return []
    
    tools = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if function looks like a tool
            docstring = ast.get_docstring(node)
            if docstring or len(node.args.args) > 0:
                tools.append({
                    "name": node.name,
                    "file": str(file_path.relative_to(PROJECT_ROOT)),
                    "line": node.lineno,
                    "docstring": docstring,
                    "parameters": [arg.arg for arg in node.args.args]
                })
    
    return tools


def scan_tools_directory() -> Dict[str, List[Dict]]:
    """Scan tools directory for all tool functions."""
    tools_by_category = {}
    
    # Scan standalone tools
    standalone_tools = []
    for file_path in TOOLS_DIR.glob("*.py"):
        if file_path.name.startswith("__"):
            continue
        tool_functions = find_tool_functions(file_path)
        if tool_functions:
            standalone_tools.extend(tool_functions)
    
    tools_by_category["standalone"] = standalone_tools
    
    # Scan category tools
    categories_dir = TOOLS_DIR / "categories"
    if categories_dir.exists():
        for category_file in categories_dir.glob("*.py"):
            if category_file.name.startswith("__"):
                continue
            category_name = category_file.stem
            tool_functions = find_tool_functions(category_file)
            if tool_functions:
                tools_by_category[category_name] = tool_functions
    
    return tools_by_category


def generate_mcp_server_code(tools: List[Dict], server_name: str) -> str:
    """Generate MCP server code for a list of tools."""
    server_code = f'''#!/usr/bin/env python3
"""
{server_name.title()} MCP Server
Auto-generated from tool migration
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import tool functions
'''
    
    # Add imports
    imported_files = set()
    for tool in tools:
        file_path = tool["file"]
        if file_path not in imported_files:
            module_path = file_path.replace("/", ".").replace(".py", "")
            server_code += f"from {module_path} import {tool['name']}\n"
            imported_files.add(file_path)
    
    server_code += '''

def main():
    """MCP server main loop."""
    # Initialize response
    print(json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "''' + server_name + '''", "version": "1.0.0"}
        }
    }))
    
    # Handle requests
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                # Route to appropriate tool function
'''
    
    # Add tool routing
    for tool in tools:
        server_code += f'''                if tool_name == "{tool['name']}":
                    result = {tool['name']}(**arguments)
'''
    
    server_code += '''                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
                }))
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {"code": -32603, "message": str(e)}
            }))

if __name__ == "__main__":
    main()
'''
    
    return server_code


def main():
    """Main migration function."""
    print("🔍 Scanning tools directory...")
    tools_by_category = scan_tools_directory()
    
    print(f"\n📊 Found {sum(len(tools) for tools in tools_by_category.values())} tools across {len(tools_by_category)} categories")
    
    # Generate migration report
    report = {
        "total_tools": sum(len(tools) for tools in tools_by_category.values()),
        "categories": {},
        "recommendations": []
    }
    
    for category, tools in tools_by_category.items():
        report["categories"][category] = {
            "count": len(tools),
            "tools": [t["name"] for t in tools]
        }
    
    # Save report
    report_path = PROJECT_ROOT / "docs" / "TOOL_MIGRATION_REPORT.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Migration report saved to: {report_path}")
    print("\n📋 Next Steps:")
    print("   1. Review migration report")
    print("   2. Create MCP servers for each category")
    print("   3. Migrate tools to MCP servers")
    print("   4. Update tool registry")
    print("   5. Deprecate standalone scripts")


if __name__ == "__main__":
    main()

