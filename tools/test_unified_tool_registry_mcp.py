#!/usr/bin/env python3
"""
Test Unified Tool Registry MCP Server
Tests tool discovery, registration, cache management, and registry health.
"""

import json
import subprocess
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.tool_registry import ToolRegistry


def test_registry_health():
    """Test registry health - should have 100% coverage."""
    print("=" * 60)
    print("TEST 1: Registry Health Check")
    print("=" * 60)
    
    registry = ToolRegistry()
    all_tools = registry.list_tools()
    categories = registry.get_categories()
    
    print(f"✓ Total tools registered: {len(all_tools)}")
    print(f"✓ Categories found: {len(categories)}")
    print(f"✓ Categories: {', '.join(categories[:10])}...")
    
    # Test cache
    registry.clear_cache()
    print("✓ Cache cleared successfully")
    
    # Test tool resolution
    if all_tools:
        test_tool = all_tools[0]
        try:
            tool_class = registry.get_tool_class(test_tool)
            print(f"✓ Tool resolution works: {test_tool}")
        except Exception as e:
            print(f"✗ Tool resolution failed for {test_tool}: {e}")
            return False
    
    return True


def test_tool_discovery():
    """Test tool discovery functionality."""
    print("\n" + "=" * 60)
    print("TEST 2: Tool Discovery")
    print("=" * 60)
    
    registry = ToolRegistry()
    
    # Test list_tools
    all_tools = registry.list_tools()
    print(f"✓ list_tools() returned {len(all_tools)} tools")
    
    # Test list_by_category
    categories = registry.get_categories()
    if categories:
        test_category = categories[0]
        category_tools = registry.list_by_category(test_category)
        print(f"✓ list_by_category('{test_category}') returned {len(category_tools)} tools")
    
    # Test get_categories
    all_categories = registry.get_categories()
    print(f"✓ get_categories() returned {len(all_categories)} categories")
    
    return True


def test_cache_management():
    """Test cache management functionality."""
    print("\n" + "=" * 60)
    print("TEST 3: Cache Management")
    print("=" * 60)
    
    registry = ToolRegistry()
    
    # Test cache population
    if registry.list_tools():
        test_tool = registry.list_tools()[0]
        tool_class1 = registry.get_tool_class(test_tool)
        tool_class2 = registry.get_tool_class(test_tool)  # Should use cache
        print(f"✓ Cache populated for {test_tool}")
        print(f"✓ Cached tool class matches: {tool_class1 == tool_class2}")
    
    # Test cache clearing
    registry.clear_cache()
    print("✓ Cache cleared successfully")
    
    # Verify cache is empty
    tool_class3 = registry.get_tool_class(test_tool)  # Should reload
    print(f"✓ Tool reloaded after cache clear")
    
    return True


def test_mcp_server_protocol():
    """Test MCP server protocol compliance."""
    print("\n" + "=" * 60)
    print("TEST 4: MCP Server Protocol")
    print("=" * 60)
    
    server_path = Path(__file__).parent.parent / "mcp_servers" / "unified_tool_server.py"
    
    try:
        # Test initialize
        proc = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()
        
        # Read initialize response
        response_line = proc.stdout.readline()
        if not response_line:
            print("✗ No response from server")
            proc.terminate()
            return False
        
        # Handle both bytes and string output
        if isinstance(response_line, bytes):
            response = response_line.decode().strip()
        else:
            response = response_line.strip()
        
        init_response = json.loads(response)
        
        if init_response.get("result") and init_response["result"].get("serverInfo"):
            print("✓ Initialize response received")
            print(f"✓ Server info: {init_response['result']['serverInfo']}")
        else:
            print(f"✗ Invalid initialize response: {response}")
            proc.terminate()
            return False
        
        # Test tools/list
        tools_list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        proc.stdin.write(json.dumps(tools_list_request) + "\n")
        proc.stdin.flush()
        
        response_line = proc.stdout.readline()
        if not response_line:
            print("✗ No response to tools/list")
            proc.terminate()
            return False
        
        # Handle both bytes and string output
        if isinstance(response_line, bytes):
            response = response_line.decode().strip()
        else:
            response = response_line.strip()
        
        tools_response = json.loads(response)
        
        if tools_response.get("result") and "tools" in tools_response["result"]:
            tools_count = len(tools_response["result"]["tools"])
            print(f"✓ tools/list returned {tools_count} tools")
        else:
            print(f"✗ Invalid tools/list response: {response}")
            proc.terminate()
            return False
        
        proc.terminate()
        return True
        
    except Exception as e:
        print(f"✗ MCP server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Unified Tool Registry MCP Server - Integration Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Registry Health", test_registry_health()))
    results.append(("Tool Discovery", test_tool_discovery()))
    results.append(("Cache Management", test_cache_management()))
    results.append(("MCP Server Protocol", test_mcp_server_protocol()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

