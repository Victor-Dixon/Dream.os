#!/usr/bin/env python3
"""
Create ICP Definitions for Revenue Engine Websites
BRAND-03 Fix - Tier 2 Foundation

Creates ICP definitions using WordPress REST API via deployer infrastructure.

Creates ICP definitions for:
- freerideinvestor.com
- dadudekc.com
- crosbyultimateevents.com

Usage:
    python tools/create_icp_definitions.py --site freerideinvestor.com
    python tools/create_icp_definitions.py --all
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
    from requests.auth import HTTPBasicAuth
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("❌ 'requests' library not installed. Install with: pip install requests")

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def _normalize_site_key(site_key: str) -> str:
    """Normalize a domain/site key into an ENV-safe token."""
    token = re.sub(r"[^A-Za-z0-9]+", "_", site_key).upper().strip("_")
    return token or "SITE"

def load_site_configs():
    """Load site configurations from configs/site_configs.json"""
    # Check websites repository first
    websites_root = Path('D:/websites')
    if not websites_root.exists():
        websites_root = project_root.parent / 'websites'
    
    config_path = websites_root / 'configs' / 'site_configs.json'
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Could not load site_configs.json: {e}")
            return {}
    return {}

def create_icp_via_rest_api(site_domain: str) -> bool:
    """Create ICP definition using WordPress REST API."""
    if not REQUESTS_AVAILABLE:
        print("❌ 'requests' library required")
        return False
    
    site_configs = load_site_configs()
    site_config = site_configs.get(site_domain, {})
    rest_api = site_config.get('rest_api', {})
    
    username = rest_api.get('username')
    app_password = rest_api.get('app_password')
    site_url = rest_api.get('site_url', site_config.get('site_url', f"https://{site_domain}"))
    
    # Allow environment-variable overrides
    norm = _normalize_site_key(site_domain)
    username = os.getenv(f"{norm}_WP_USERNAME") or os.getenv("WP_USERNAME") or username
    app_password = os.getenv(f"{norm}_WP_APP_PASSWORD") or os.getenv("WP_APP_PASSWORD") or app_password
    site_url = os.getenv(f"{norm}_WP_SITE_URL") or os.getenv("WP_SITE_URL") or site_url
    
    if not username or not app_password:
        print(f"❌ Missing REST API credentials for {site_domain}")
        print("   Add username/app_password to configs/site_configs.json OR set env vars:")
        print(f"   - {norm}_WP_USERNAME and {norm}_WP_APP_PASSWORD")
        return False
    
    # ICP content definitions (enhanced with detailed content from ICP_DEFINITION.md files)
    icp_content = {
        'freerideinvestor.com': {
            'title': 'FreeRide Investor Ideal Customer Profile',
            'content': '''<h2>For Active Traders Struggling with Inconsistent Results</h2>
<p>For active traders (day/swing traders, $10K-$500K accounts) struggling with inconsistent results, we eliminate guesswork and provide proven trading strategies.</p>
<p><strong>Your outcome:</strong> Consistent edge, reduced losses, trading confidence.</p>
<h3>We eliminate:</h3>
<ul>
<li>Inconsistent trading results and guesswork</li>
<li>Emotional trading decisions</li>
<li>Lack of proven strategies</li>
<li>Unclear entry/exit signals</li>
</ul>
<h3>You get:</h3>
<ul>
<li>Consistent trading edge with proven strategies</li>
<li>Reduced losses through disciplined approach</li>
<li>Trading confidence from clear methodology</li>
<li>Systematic approach to market opportunities</li>
</ul>''',
            'target_demographic': 'Active traders (day/swing traders, $10K-$500K accounts)',
            'pain_points': 'inconsistent results, guesswork, emotional trading, lack of proven strategies',
            'desired_outcomes': 'consistent edge, reduced losses, trading confidence, systematic approach'
        },
        'dadudekc.com': {
            'title': 'DaDudeKC Ideal Customer Profile',
            'content': '''<h2>For Service Business Owners Drowning in Manual Tasks</h2>
<p>For service business owners ($50K-$500K revenue) drowning in manual workflows, we eliminate workflow bottlenecks and deliver working automations in 2 weeks.</p>
<p><strong>Your outcome:</strong> 10+ hours/week back, scalable operations, peace of mind.</p>
<h3>We eliminate:</h3>
<ul>
<li>Manual workflows stealing 5-15 hours/week</li>
<li>Follow-ups, scheduling, invoicing bottlenecks</li>
<li>Lack of systems and processes</li>
<li>Technical barriers to automation</li>
<li>Scaling challenges without hiring</li>
</ul>
<h3>You get:</h3>
<ul>
<li>10+ hours/week back through automation</li>
<li>Scalable operations without hiring</li>
<li>Peace of mind from automated workflows</li>
<li>Zero technical knowledge required</li>
<li>Working automations delivered in 2 weeks</li>
</ul>''',
            'target_demographic': 'Service business owners ($50K-$500K revenue, 2-20 people teams)',
            'pain_points': 'manual workflows (5-15 hours/week), follow-ups/scheduling/invoicing bottlenecks, lack of systems, technical barriers, scaling challenges',
            'desired_outcomes': '10+ hours/week back, scalable operations, peace of mind, zero technical knowledge required, working automations in 2 weeks'
        },
        'crosbyultimateevents.com': {
            'title': 'Crosby Ultimate Events Ideal Customer Profile',
            'content': '''<h2>For Busy Professionals Who Value Quality</h2>
<p>For affluent professionals ($150K+ income, ages 35-65) who value time and quality, we eliminate event planning stress and deliver unforgettable experiences.</p>
<p><strong>Your outcome:</strong> Flawless events that impress guests while you enjoy the moment.</p>
<h3>We eliminate:</h3>
<ul>
<li>Event planning stress and coordination headaches</li>
<li>Managing multiple vendors (chef, planner, decorator, etc.)</li>
<li>Fear of things going wrong on the big day</li>
<li>Generic catering that doesn't match the occasion</li>
</ul>
<h3>You get:</h3>
<ul>
<li>Flawless events that impress guests</li>
<li>Ability to enjoy the moment instead of managing logistics</li>
<li>One trusted partner handling everything</li>
<li>Memorable culinary experiences</li>
<li>Peace of mind knowing every detail is covered</li>
</ul>''',
            'target_demographic': 'Affluent professionals ($150K+ income, ages 35-65, urban/suburban areas)',
            'pain_points': 'event planning stress, coordination headaches, managing multiple vendors, fear of things going wrong, generic catering',
            'desired_outcomes': 'flawless events, ability to enjoy the moment, one trusted partner, memorable experiences, peace of mind'
        }
    }
    
    if site_domain not in icp_content:
        print(f"❌ No ICP content defined for {site_domain}")
        return False
    
    icp_data = icp_content[site_domain]
    
    print(f"📝 Creating ICP definition via REST API...")
    print(f"   Site: {site_url}")
    print(f"   Title: {icp_data['title']}")
    
    try:
        # WordPress REST API endpoint for Custom Post Type
        api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/icp_definition"
        
        auth = HTTPBasicAuth(username, app_password)
        
        # Check if ICP already exists
        check_response = requests.get(
            api_url,
            auth=auth,
            params={'per_page': 1, 'meta_key': 'site_assignment', 'meta_value': site_domain},
            timeout=30
        )
        
        post_id = None
        if check_response.status_code == 200:
            existing = check_response.json()
            if existing:
                post_id = existing[0].get('id')
                print(f"   Found existing ICP (ID: {post_id}), updating...")
        
        # Prepare post data
        post_data = {
            'title': icp_data['title'],
            'content': icp_data['content'],
            'status': 'publish',
            'meta': {
                'target_demographic': icp_data['target_demographic'],
                'pain_points': icp_data['pain_points'],
                'desired_outcomes': icp_data['desired_outcomes'],
                'site_assignment': site_domain
            }
        }
        
        if post_id:
            # Update existing
            response = requests.post(
                f"{api_url}/{post_id}",
                auth=auth,
                json=post_data,
                timeout=30
            )
        else:
            # Create new
            response = requests.post(
                api_url,
                auth=auth,
                json=post_data,
                timeout=30
            )
        
        if response.status_code in [200, 201]:
            post = response.json()
            post_id = post.get('id', post_id)
            
            # Update meta fields using ACF or custom meta endpoint
            # WordPress REST API doesn't directly support custom meta in post creation
            # Meta fields need to be set via ACF REST API or custom endpoint
            print(f"✅ ICP definition created successfully!")
            print(f"   Post ID: {post_id}")
            print(f"   ⚠️  Note: Meta fields (target_demographic, pain_points, desired_outcomes)")
            print(f"      may need to be set manually in WordPress admin or via ACF REST API")
            return True
        else:
            print(f"❌ Failed to create ICP definition: {response.status_code}")
            error_text = response.text[:500] if hasattr(response, 'text') else str(response.content[:500])
            print(f"   {error_text}")
            
            # Check if Custom Post Type endpoint exists
            if response.status_code == 404:
                print(f"   ⚠️  Custom Post Type 'icp_definition' REST API endpoint not found")
                print(f"   Possible causes:")
                print(f"   1. Theme with Custom Post Type not deployed yet")
                print(f"   2. Custom Post Type not registered with 'show_in_rest' => true")
                print(f"   Solution: Deploy theme first, then run this tool")
            elif response.status_code == 500:
                print(f"   ⚠️  Server error - Custom Post Type may not be registered")
                print(f"   Solution: Ensure theme is deployed and Custom Post Type is registered")
                print(f"   Check: Theme functions.php should register 'icp_definition' post type")
            
            return False
            
    except Exception as e:
        print(f"❌ REST API error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_icp_for_site(site_domain):
    """Create ICP definition for a specific site"""
    print(f"\n📋 Creating ICP definition for {site_domain}...")
    return create_icp_via_rest_api(site_domain)

def main():
    parser = argparse.ArgumentParser(description='Create ICP definitions for revenue engine websites')
    parser.add_argument('--site', choices=['freerideinvestor.com', 'dadudekc.com', 'crosbyultimateevents.com'],
                       help='Create ICP for specific site')
    parser.add_argument('--all', action='store_true', help='Create ICP for all sites')
    
    args = parser.parse_args()
    
    if not args.site and not args.all:
        parser.print_help()
        sys.exit(1)
    
    sites = []
    if args.all:
        sites = ['freerideinvestor.com', 'dadudekc.com', 'crosbyultimateevents.com']
    else:
        sites = [args.site]
    
    results = {}
    for site in sites:
        results[site] = create_icp_for_site(site)
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    for site, success in results.items():
        status = "✅ COMPLETE" if success else "❌ FAILED"
        print(f"{site}: {status}")
    
    if all(results.values()):
        print("\n✅ All ICP definitions created successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Some ICP definitions failed. Check output above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

