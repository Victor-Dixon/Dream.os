import sys
from pathlib import Path
import json
import os

# Add project root and websites root to path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root.parent / "websites"))

# Import function directly from the file
# We need to make sure we don't trigger the __init__.py of mcp_servers
import importlib.util
spec = importlib.util.spec_from_file_location("validation_audit_server", project_root / "mcp_servers" / "validation_audit_server.py")
validation_audit_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation_audit_server)

def test_php_syntax():
    site_key = "tradingrobotplug.com"
    # Adjusted path based on sites.json
    file_path = "domains/tradingrobotplug.com/public_html/wp-content/themes/tradingrobotplug-theme/functions.php"
    
    print(f"Testing PHP syntax check for {site_key} -> {file_path}")
    result = validation_audit_server.check_php_syntax(site_key, file_path)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_php_syntax()

