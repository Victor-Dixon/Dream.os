#!/usr/bin/env python3
"""
Debug MCP Servers - Diagnose MCP server connectivity and configuration issues
"""

import json
import subprocess
import sys
from pathlib import Path

def load_mcp_config():
    """Load MCP server configuration"""
    config_path = Path(__file__).parent.parent / "mcp_servers" / "all_mcp_servers.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def test_server_import(server_path):
    """Test if server file can be imported"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import sys; sys.path.insert(0, '{Path(server_path).parent.parent}'); exec(open('{server_path}').read())"],
            capture_output=True,
            timeout=5,
            cwd=Path(server_path).parent.parent
        )
        return result.returncode == 0, result.stdout.decode(), result.stderr.decode()
    except Exception as e:
        return False, "", str(e)

def test_server_file_exists(server_path):
    """Check if server file exists"""
    path = Path(server_path)
    return path.exists(), path.is_file()

def main():
    print("🔍 MCP Server Debugging Tool")
    print("="*60)
    
    config = load_mcp_config()
    servers = config.get("mcpServers", {})
    
    if not servers:
        print("❌ No MCP servers configured in all_mcp_servers.json")
        return
    
    print(f"\n📋 Found {len(servers)} configured MCP servers:\n")
    
    issues = []
    
    for server_name, server_config in servers.items():
        print(f"🔍 Testing: {server_name}")
        print(f"   Description: {server_config.get('description', 'N/A')}")
        
        # Check command
        command = server_config.get('command', '')
        args = server_config.get('args', [])
        print(f"   Command: {command}")
        print(f"   Args: {args}")
        
        if args:
            server_path = args[0] if isinstance(args, list) else args
            exists, is_file = test_server_file_exists(server_path)
            
            if not exists:
                print(f"   ❌ Server file not found: {server_path}")
                issues.append(f"{server_name}: File not found - {server_path}")
            elif not is_file:
                print(f"   ❌ Path is not a file: {server_path}")
                issues.append(f"{server_name}: Path is not a file - {server_path}")
            else:
                print(f"   ✅ Server file exists: {server_path}")
                
                # Try to import/parse the file
                try:
                    with open(server_path, 'r') as f:
                        content = f.read()
                        # Basic syntax check
                        compile(content, server_path, 'exec')
                        print(f"   ✅ Python syntax valid")
                except SyntaxError as e:
                    print(f"   ❌ Python syntax error: {e}")
                    issues.append(f"{server_name}: Syntax error - {e}")
                except Exception as e:
                    print(f"   ⚠️  Could not parse file: {e}")
        
        print()
    
    print("="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ All MCP server files exist and have valid syntax")
    
    print("\n💡 Next Steps:")
    print("   1. Verify MCP servers are registered in Cursor MCP settings")
    print("   2. Check Cursor MCP server logs for connection errors")
    print("   3. Ensure Python dependencies are installed")
    print("   4. Test server startup manually: python <server_file>")

if __name__ == '__main__':
    main()
