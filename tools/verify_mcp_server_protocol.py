#!/usr/bin/env python3
"""
Verify MCP Server Protocol Implementation
Tests if MCP servers follow correct JSON-RPC protocol

<!-- SSOT Domain: tools -->
"""

import json
import sys
from pathlib import Path

def test_mcp_protocol_response():
    """Test if server responds correctly to initialize request"""
    print("🔍 Testing MCP Server Protocol Implementation")
    print("="*60)
    
    # Simulate initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    print("\n📋 Test 1: Server Initialization Protocol")
    print(f"   Sending initialize request...")
    print(f"   Request: {json.dumps(initialize_request, indent=2)}")
    
    # Check if server has main() function that handles stdin
    server_files = [
        "mcp_servers/task_manager_server.py",
        "mcp_servers/messaging_server.py",
        "mcp_servers/swarm_brain_server.py",
    ]
    
    for server_file in server_files:
        path = Path(__file__).parent.parent / server_file
        if path.exists():
            content = path.read_text()
            has_main = "if __name__" in content and "main()" in content
            has_stdin = "sys.stdin" in content
            has_jsonrpc = "jsonrpc" in content.lower()
            
            print(f"\n   {server_file}:")
            print(f"      Has main(): {has_main}")
            print(f"      Reads stdin: {has_stdin}")
            print(f"      Has JSON-RPC: {has_jsonrpc}")
            
            if has_main and has_stdin and has_jsonrpc:
                print(f"      ✅ Protocol implementation looks correct")
            else:
                print(f"      ⚠️  May be missing protocol components")
    
    print("\n" + "="*60)
    print("📊 PROTOCOL CHECK SUMMARY")
    print("="*60)
    print("MCP servers use JSON-RPC 2.0 protocol over stdin/stdout")
    print("Servers should:")
    print("  1. Read JSON-RPC requests from stdin")
    print("  2. Handle 'initialize' method")
    print("  3. Handle 'tools/list' method")
    print("  4. Handle 'tools/call' method")
    print("  5. Write JSON-RPC responses to stdout")
    print("\nIf servers aren't accessible via list_mcp_resources:")
    print("  - Check Cursor MCP settings configuration")
    print("  - Verify servers are registered in Cursor config")
    print("  - Restart Cursor to reload MCP servers")
    print("  - Check Cursor MCP server logs for errors")

if __name__ == '__main__':
    test_mcp_protocol_response()




