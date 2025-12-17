#!/usr/bin/env python3
"""
Fix Business Plan Page
======================

Ensures the business plan page has the correct shortcode.

Usage:
    python fix_business_plan_page.py --site crosbyultimateevents.com
"""

import sys
from pathlib import Path

# Add tools to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "tools"))

try:
    from wordpress_manager import WordPressManager
    HAS_WP_MANAGER = True
except ImportError:
    HAS_WP_MANAGER = False
    print("Warning: wordpress_manager not available")


def fix_business_plan_page(site_name: str = "crosbyultimateevents.com"):
    """Ensure business plan page has the shortcode."""
    
    if not HAS_WP_MANAGER:
        print("❌ WordPress manager not available")
        return False
    
    print(f"🔧 Fixing business plan page for {site_name}...\n")
    
    try:
        manager = WordPressManager(site_name)
        
        # Check if page exists
        print("1. Checking if page exists...")
        page_check = manager.wp_cli("post list --post_type=page --name=crosby_business_plan --format=json")
        
        import json
        pages = json.loads(page_check[0]) if page_check[0].strip() else []
        
        if pages:
            page_id = pages[0].get('ID')
            page_title = pages[0].get('post_title', 'Business Plan')
            page_content = pages[0].get('post_content', '')
            
            print(f"   ✅ Page found: '{page_title}' (ID: {page_id})")
            print(f"   Current content length: {len(page_content)} characters")
            
            # Check if shortcode exists
            if '[crosby_business_plan' in page_content:
                print("   ✅ Shortcode already exists in page content")
                print("\n   💡 If content isn't showing, possible issues:")
                print("      1. Page template might not process shortcodes")
                print("      2. Theme might be filtering content")
                print("      3. PHP error in template (check error logs)")
                
                # Try to update page to ensure it's published
                print("\n   🔄 Ensuring page is published...")
                update_result = manager.wp_cli(f"post update {page_id} --post_status=publish")
                if update_result[2] == 0:
                    print("   ✅ Page status updated")
                
            else:
                print("   ⚠️  Shortcode NOT found in page content")
                print("   🔄 Adding shortcode to page...")
                
                # Add shortcode to content
                new_content = f"[crosby_business_plan]\n\n{page_content}".strip()
                update_result = manager.wp_cli(
                    f'post update {page_id} --post_content="{new_content.replace(chr(34), chr(92)+chr(34))}"'
                )
                
                if update_result[2] == 0:
                    print("   ✅ Shortcode added to page!")
                    print("   💡 Clear cache and refresh the page")
                else:
                    print(f"   ❌ Failed to update page: {update_result[1]}")
                    # Try alternative method
                    print("   🔄 Trying alternative update method...")
                    # Use eval to update
                    eval_cmd = f'eval \'$post = get_post({page_id}); $post->post_content = "[crosby_business_plan]\\n\\n" . $post->post_content; wp_update_post($post); echo "UPDATED";\''
                    alt_result = manager.wp_cli(eval_cmd)
                    if 'UPDATED' in alt_result[0]:
                        print("   ✅ Page updated via alternative method!")
                    else:
                        print(f"   ❌ Alternative method failed: {alt_result[1]}")
        else:
            print("   ❌ Page not found")
            print("   🔄 Creating business plan page...")
            
            create_result = manager.wp_cli(
                'post create --post_type=page --post_title="Business Plan" '
                '--post_name="crosby_business_plan" --post_status=publish '
                '--post_content="[crosby_business_plan]"'
            )
            
            if create_result[2] == 0:
                print("   ✅ Business plan page created!")
                page_id = create_result[0].strip().split()[-1] if create_result[0] else None
                if page_id:
                    print(f"   Page ID: {page_id}")
            else:
                print(f"   ❌ Failed to create page: {create_result[1]}")
        
        # Flush cache
        print("\n2. Flushing cache...")
        manager.purge_caches()
        print("   ✅ Cache flushed")
        
        print("\n✅ Done! Check the page at:")
        print(f"   https://{site_name}/crosby_business_plan/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix Business Plan Page")
    parser.add_argument(
        "--site",
        default="crosbyultimateevents.com",
        help="WordPress site name"
    )
    
    args = parser.parse_args()
    fix_business_plan_page(args.site)

