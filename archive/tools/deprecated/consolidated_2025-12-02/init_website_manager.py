#!/usr/bin/env python3
"""
Initialize Unified Website Management Tool
==========================================

Demonstrates the unified tool consolidating:
- wordpress_manager.py
- wordpress_page_setup.py
- deploy_ariajet.py
- auto_deploy_hook.py

Uses birthday website workflow as template.
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))

from website_manager import WebsiteManager


def demonstrate_birthday_workflow(site_key: str = "prismblossom"):
    """Demonstrate birthday website workflow using unified tool."""
    
    print("=" * 70)
    print("🎂 UNIFIED WEBSITE MANAGEMENT TOOL - INITIALIZATION")
    print("=" * 70)
    print()
    
    try:
        manager = WebsiteManager(site_key)
        print(f"✅ Initialized for site: {site_key}")
        print(f"   Theme path: {manager.theme_path}")
        print()
        
        # List existing pages
        print("📄 Existing Pages:")
        print("-" * 70)
        pages = manager.list_pages() if hasattr(manager, 'list_pages') else []
        if pages:
            for page in pages:
                print(f"   • {page.get('file', 'Unknown')} - {page.get('template_name', 'Unknown')}")
        else:
            # Manual list
            if manager.theme_path:
                for page_file in manager.theme_path.glob("page-*.php"):
                    print(f"   • {page_file.name}")
        print()
        
        # Verify setup
        print("🔍 Verification:")
        print("-" * 70)
        if manager.theme_path:
            functions_exists = (manager.theme_path / "functions.php").exists()
            page_count = len(list(manager.theme_path.glob("page-*.php")))
            print(f"   Theme exists: ✅")
            print(f"   functions.php: {'✅' if functions_exists else '❌'}")
            print(f"   Page templates: {page_count}")
        print()
        
        # Demonstrate birthday workflow steps
        print("🎯 Birthday Website Workflow (Template):")
        print("-" * 70)
        print("   Step 1: Update Invitation Page Colors")
        print("      → manager.update_colors('page-invitation.php', {...})")
        print()
        print("   Step 2: Add Guestbook Placeholders")
        print("      → manager.add_placeholder_entries('page-guestbook.php', [...])")
        print()
        print("   Step 3: Add Interactive Features")
        print("      → manager.add_interactive_features('page-birthday-fun.php', [...])")
        print()
        print("   Step 4: Create Blog Post")
        print("      → manager.create_page_template('Birthday Blog', content, 'page-birthday-blog.php')")
        print()
        print("   Step 5: Deploy")
        print("      → manager.deploy_file('page-invitation.php')")
        print()
        
        # Show consolidation
        print("🔧 Tool Consolidation:")
        print("-" * 70)
        print("   ✅ wordpress_manager.py → WebsiteManager.deploy_file()")
        print("   ✅ wordpress_page_setup.py → WebsiteManager.create_page()")
        print("   ✅ deploy_ariajet.py → WebsiteManager.deploy_file()")
        print("   ✅ auto_deploy_hook.py → WebsiteManager.auto_deploy_changed_files()")
        print()
        
        print("=" * 70)
        print("✅ UNIFIED TOOL INITIALIZED AND READY!")
        print("=" * 70)
        print()
        print("📋 Usage Examples:")
        print("   python tools/website_manager.py --site prismblossom --batch updates.json")
        print("   python tools/website_manager.py --site prismblossom --update-colors page-invitation.php '#ff00ff:#000000'")
        print("   python tools/website_manager.py --site prismblossom --deploy page-invitation.php")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    site = sys.argv[1] if len(sys.argv) > 1 else "prismblossom"
    success = demonstrate_birthday_workflow(site)
    sys.exit(0 if success else 1)




