import sys
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_servers.validation_audit_server import check_php_syntax

def test_php_syntax():
    site_key = "tradingrobotplug.com"
    file_path = "domains/tradingrobotplug.com/public_html/wp-content/themes/tradingrobotplug-theme/functions.php"
    
    print(f"Testing PHP syntax check for {site_key} -> {file_path}")
    result = check_php_syntax(site_key, file_path)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_php_syntax()

