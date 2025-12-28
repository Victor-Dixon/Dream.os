#!/usr/bin/env python3
"""
Test MCP Server Connectivity
Tests if MCP servers can be imported and basic functions work

SSOT TOOL METADATA
Purpose: Quick local smoke test to verify MCP server modules import and basic APIs are callable.
Description: Imports key `mcp_servers.*_server` modules and calls a small subset of functions to validate wiring.
Usage:
  - python tools/test_mcp_server_connectivity.py
  - python tools/test_mcp_server_connectivity.py > connectivity.log
Author: Swarm (maintainers)
Date: 2025-12-28
Tags: ssot, mcp, connectivity, smoke-test
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_server_imports():
    """Test importing all MCP server modules"""
    print("🔍 Testing MCP Server Imports")
    print("="*60)
    
    servers = {
        'task_manager': 'mcp_servers.task_manager_server',
        'messaging': 'mcp_servers.messaging_server',
        'website_manager': 'mcp_servers.website_manager_server',
        'swarm_brain': 'mcp_servers.swarm_brain_server',
        'git_operations': 'mcp_servers.git_operations_server',
        'v2_compliance': 'mcp_servers.v2_compliance_server',
    }
    
    results = {}
    
    for name, module_path in servers.items():
        try:
            module = __import__(module_path, fromlist=[''])
            results[name] = {'success': True, 'error': None}
            print(f"✅ {name}: Import successful")
        except Exception as e:
            results[name] = {'success': False, 'error': str(e)}
            print(f"❌ {name}: Import failed - {e}")
    
    print()
    return results

def test_task_manager_functions():
    """Test task manager server functions"""
    print("🔍 Testing Task Manager Functions")
    print("="*60)
    
    try:
        from mcp_servers import task_manager_server as tm
        
        # Test get_tasks
        print("Testing get_tasks('INBOX')...")
        result = tm.get_tasks('INBOX')
        if result.get('success'):
            print(f"✅ get_tasks successful: {len(result.get('tasks', []))} tasks found")
        else:
            print(f"❌ get_tasks failed: {result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"❌ Task manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_git_operations_functions():
    """Test git operations server functions"""
    print("\n🔍 Testing Git Operations Functions")
    print("="*60)
    
    try:
        from mcp_servers import git_operations_server as go
        
        # Test get_recent_commits
        print("Testing get_recent_commits()...")
        result = go.get_recent_commits(agent_id=None, hours=24, file_pattern=None)
        if result.get('success'):
            commits = result.get('commits', [])
            print(f"✅ get_recent_commits successful: {len(commits)} commits found")
        else:
            print(f"❌ get_recent_commits failed: {result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"❌ Git operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔍 MCP Server Connectivity Test")
    print("="*60)
    print()
    
    # Test imports
    import_results = test_server_imports()
    
    # Test function calls
    print()
    task_manager_ok = test_task_manager_functions()
    git_ops_ok = test_git_operations_functions()
    
    print()
    print("="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    import_success = sum(1 for r in import_results.values() if r['success'])
    print(f"Imports: {import_success}/{len(import_results)} successful")
    print(f"Task Manager Functions: {'✅' if task_manager_ok else '❌'}")
    print(f"Git Operations Functions: {'✅' if git_ops_ok else '❌'}")
    
    print("\n💡 If MCP servers aren't accessible via list_mcp_resources:")
    print("   1. Check Cursor MCP settings configuration")
    print("   2. Verify servers are registered in Cursor config")
    print("   3. Check Cursor MCP server logs")
    print("   4. Restart Cursor to reload MCP servers")

if __name__ == '__main__':
    main()
