#!/usr/bin/env python3
"""
Validate PHP Syntax via MCP Tool
Quick utility to test PHP syntax validation MCP server
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    """Test PHP syntax validation via MCP."""
    site_key = sys.argv[1] if len(sys.argv) > 1 else "weareswarm.online"
    file_path = sys.argv[2] if len(sys.argv) > 2 else "wp-content/themes/swarm/functions.php"
    
    print(f"🔍 Testing PHP syntax validation for {site_key}")
    print(f"   File: {file_path}")
    
    try:
        from mcp_servers.validation_audit_server import check_php_syntax
        
        result = check_php_syntax(site_key, file_path)
        
        print(f"\n📊 Result:")
        print(json.dumps(result, indent=2))
        
        if result.get("success") and result.get("valid"):
            print(f"\n✅ PHP syntax is valid")
            return 0
        elif result.get("success"):
            print(f"\n❌ PHP syntax error:")
            if result.get("line_number"):
                print(f"   Line: {result['line_number']}")
            if result.get("error_message"):
                print(f"   Error: {result['error_message']}")
            return 1
        else:
            print(f"\n❌ Validation failed: {result.get('error', 'Unknown error')}")
            return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

