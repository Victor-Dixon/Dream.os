#!/usr/bin/env python3
"""
Debug ICP REST API Endpoint for freerideinvestor.com
Diagnoses 500 error by testing endpoint availability and configuration.
"""

import json
import sys
from pathlib import Path

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    print("❌ 'requests' library required. Install with: pip install requests")
    sys.exit(1)

def load_site_configs():
    """Load site configurations from configs/site_configs.json"""
    websites_root = Path('D:/websites')
    if not websites_root.exists():
        websites_root = Path(__file__).parent.parent.parent / 'websites'
    
    config_path = websites_root / 'configs' / 'site_configs.json'
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Could not load site_configs.json: {e}")
            return {}
    return {}

def debug_icp_endpoint(site_domain='freerideinvestor.com'):
    """Debug ICP REST API endpoint to diagnose 500 error"""
    site_configs = load_site_configs()
    site_config = site_configs.get(site_domain, {})
    rest_api = site_config.get('rest_api', {})
    
    username = rest_api.get('username')
    app_password = rest_api.get('app_password')
    site_url = rest_api.get('site_url', site_config.get('site_url', f"https://{site_domain}"))
    
    if not username or not app_password:
        print(f"❌ Missing REST API credentials for {site_domain}")
        print("   Check configs/site_configs.json")
        return False
    
    auth = HTTPBasicAuth(username, app_password)
    base_url = site_url.rstrip('/')
    
    print(f"🔍 Debugging ICP REST API endpoint for {site_domain}")
    print(f"   Site URL: {base_url}")
    print(f"   Username: {username}")
    print()
    
    # Test 1: Check if WordPress REST API is accessible
    print("📋 Test 1: WordPress REST API Base")
    try:
        response = requests.get(f"{base_url}/wp-json/", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ WordPress REST API accessible (200)")
            namespaces = response.json().get('namespaces', [])
            print(f"   Available namespaces: {', '.join(namespaces[:5])}...")
        else:
            print(f"   ❌ WordPress REST API returned {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error accessing WordPress REST API: {e}")
        return False
    
    print()
    
    # Test 2: Check if wp/v2 namespace exists
    print("📋 Test 2: WordPress REST API v2 Namespace")
    try:
        response = requests.get(f"{base_url}/wp-json/wp/v2", timeout=10)
        if response.status_code == 200:
            print(f"   ✅ wp/v2 namespace accessible (200)")
            routes = list(response.json().keys())
            print(f"   Available routes: {len(routes)} routes")
            if 'icp_definition' in routes:
                print(f"   ✅ 'icp_definition' route found!")
            else:
                print(f"   ❌ 'icp_definition' route NOT found")
                print(f"   Sample routes: {', '.join(routes[:10])}")
        else:
            print(f"   ❌ wp/v2 namespace returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing wp/v2 namespace: {e}")
    
    print()
    
    # Test 3: Try to access icp_definition endpoint directly
    print("📋 Test 3: ICP Definition Endpoint Direct Access")
    icp_endpoint = f"{base_url}/wp-json/wp/v2/icp_definition"
    try:
        response = requests.get(icp_endpoint, auth=auth, timeout=10)
        print(f"   Endpoint: {icp_endpoint}")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Endpoint accessible (200)")
            data = response.json()
            print(f"   Response type: {type(data)}")
            if isinstance(data, list):
                print(f"   Found {len(data)} existing ICP definitions")
            elif isinstance(data, dict):
                print(f"   Response keys: {list(data.keys())}")
        elif response.status_code == 404:
            print(f"   ❌ Endpoint not found (404)")
            print(f"   ⚠️  Custom Post Type 'icp_definition' not registered or REST API not enabled")
            print(f"   Solution: Check theme functions.php for:")
            print(f"      register_post_type('icp_definition', ['show_in_rest' => true, ...])")
        elif response.status_code == 500:
            print(f"   ❌ Server error (500)")
            print(f"   ⚠️  Custom Post Type may be registered but has PHP error")
            print(f"   Response: {response.text[:500]}")
            print(f"   Solution: Check WordPress error logs for PHP errors")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
    except Exception as e:
        print(f"   ❌ Error accessing endpoint: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test 4: Try POST to create (this is what fails)
    print("📋 Test 4: POST Request (This is what fails)")
    try:
        test_data = {
            'title': 'Test ICP Definition',
            'content': 'Test content',
            'status': 'draft'
        }
        response = requests.post(icp_endpoint, auth=auth, json=test_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"   ✅ POST successful!")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ POST failed: {response.status_code}")
            print(f"   Response headers: {dict(response.headers)}")
            print(f"   Response body: {response.text[:1000]}")
            
            # Try to parse error details
            try:
                error_data = response.json()
                if 'code' in error_data:
                    print(f"   Error code: {error_data.get('code')}")
                if 'message' in error_data:
                    print(f"   Error message: {error_data.get('message')}")
                if 'data' in error_data:
                    print(f"   Error data: {error_data.get('data')}")
            except:
                pass
    except Exception as e:
        print(f"   ❌ Error during POST: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("="*60)
    print("📊 DIAGNOSIS SUMMARY")
    print("="*60)
    print("If endpoint returns 404: Custom Post Type not registered or REST API disabled")
    print("If endpoint returns 500: PHP error in theme or Custom Post Type registration")
    print("Check WordPress error logs for detailed PHP error messages")
    print("Verify theme functions.php has: 'show_in_rest' => true in register_post_type()")

if __name__ == '__main__':
    debug_icp_endpoint()

