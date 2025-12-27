#!/usr/bin/env python3
"""
Deep Debug freerideinvestor.com 500 Error
Tests WordPress REST API at multiple levels to identify root cause.
"""

import json
import sys
from pathlib import Path

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("❌ 'requests' library required")
    sys.exit(1)

def load_site_configs():
    """Load site configurations"""
    websites_root = Path('D:/websites')
    if not websites_root.exists():
        websites_root = Path(__file__).parent.parent.parent / 'websites'
    
    config_path = websites_root / 'configs' / 'site_configs.json'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Could not load config: {e}")
            return {}
    return {}

def test_site_health(site_url):
    """Test basic site accessibility"""
    print("🔍 Testing Site Health")
    print("="*60)
    
    # Test 1: Basic HTTP access
    print("\n📋 Test 1: Basic HTTP Access")
    try:
        response = requests.get(site_url, timeout=10, allow_redirects=True)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Site accessible")
            print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"   Content length: {len(response.text)} bytes")
        else:
            print(f"   ⚠️  Site returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: WordPress admin-ajax.php (common WordPress endpoint)
    print("\n📋 Test 2: WordPress Admin AJAX")
    try:
        ajax_url = f"{site_url.rstrip('/')}/wp-admin/admin-ajax.php"
        response = requests.get(ajax_url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:  # Normal for GET without action
            print(f"   ✅ Admin AJAX accessible (400 is expected for GET)")
        elif response.status_code == 200:
            print(f"   ✅ Admin AJAX accessible")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: WordPress REST API discovery
    print("\n📋 Test 3: WordPress REST API Discovery")
    rest_url = f"{site_url.rstrip('/')}/wp-json/"
    try:
        response = requests.get(rest_url, timeout=10)
        print(f"   URL: {rest_url}")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"   Content-Length: {response.headers.get('Content-Length', 'N/A')}")
        
        if response.status_code == 500:
            print(f"   ❌ REST API returning 500 (PHP error)")
            print(f"   Response body length: {len(response.text)} bytes")
            if response.text:
                print(f"   Response preview: {response.text[:500]}")
            else:
                print(f"   ⚠️  Empty response body (common with fatal PHP errors)")
        elif response.status_code == 200:
            print(f"   ✅ REST API accessible")
            try:
                data = response.json()
                print(f"   Namespaces: {len(data.get('namespaces', []))} found")
            except:
                print(f"   ⚠️  Response not valid JSON")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Check if it's a plugin/theme conflict
    print("\n📋 Test 4: Testing Alternative Endpoints")
    endpoints_to_test = [
        ('/wp-json/wp/v2', 'REST API v2 base'),
        ('/wp-json/wp/v2/posts', 'Posts endpoint'),
        ('/wp-json/wp/v2/pages', 'Pages endpoint'),
    ]
    
    for endpoint, name in endpoints_to_test:
        try:
            url = f"{site_url.rstrip('/')}{endpoint}"
            response = requests.get(url, timeout=10)
            print(f"   {name}: {response.status_code}")
            if response.status_code == 500:
                print(f"      ❌ Also returning 500")
            elif response.status_code == 200:
                print(f"      ✅ Accessible")
        except Exception as e:
            print(f"   {name}: Error - {e}")
    
    print("\n" + "="*60)
    print("📊 DIAGNOSIS")
    print("="*60)
    print("If ALL REST API endpoints return 500:")
    print("  1. PHP fatal error in theme functions.php")
    print("  2. PHP fatal error in active plugin")
    print("  3. WordPress core issue")
    print("  4. Server PHP configuration problem")
    print("\nNext steps:")
    print("  1. Check WordPress error logs (wp-content/debug.log)")
    print("  2. Enable WP_DEBUG in wp-config.php")
    print("  3. Check theme functions.php for syntax errors")
    print("  4. Deactivate plugins one by one to find conflict")
    print("  5. Check server PHP error logs")

if __name__ == '__main__':
    site_configs = load_site_configs()
    site_config = site_configs.get('freerideinvestor.com', {})
    rest_api = site_config.get('rest_api', {})
    site_url = rest_api.get('site_url', site_config.get('site_url', 'https://freerideinvestor.com'))
    
    test_site_health(site_url)

