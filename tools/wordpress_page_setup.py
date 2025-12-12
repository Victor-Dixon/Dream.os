#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
WordPress Page Setup Tool (Expanded)
====================================

Automates WordPress page creation, database operations, menu management,
and content updates for agents.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <400 lines
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


class WordPressPageSetup:
    """Tool for agents to set up WordPress pages automatically."""
    
    # Site directory mapping
    SITE_MAPPING = {
        "southwestsecret": "D:/websites/southwestsecret.com",
        "carmyn": "D:/websites/southwestsecret.com",
        "aria": "D:/websites/southwestsecret.com",
        "prismblossom": "D:/websites/prismblossom.online",
        "prismblossom.online": "D:/websites/prismblossom.online",
    }
    
    def __init__(self, site_key: str = "southwestsecret"):
        """Initialize with site key."""
        self.site_key = site_key
        self.site_path = self.SITE_MAPPING.get(site_key)
        if not self.site_path or not Path(self.site_path).exists():
            raise ValueError(f"Site not found: {site_key}")
    
    def get_theme_path(self) -> Path:
        """Get WordPress theme directory path."""
        # Determine theme name based on site
        if self.site_key in ["prismblossom", "prismblossom.online"]:
            theme_name = "prismblossom"
        else:
            theme_name = "southwestsecret"
        
        theme_paths = [
            Path(self.site_path) / "wordpress-theme" / theme_name,
            Path(self.site_path) / "wp-content" / "themes" / theme_name,
        ]
        
        for path in theme_paths:
            if path.exists():
                return path
        
        raise FileNotFoundError(f"Theme directory not found for {self.site_key}")
    
    def create_page_template(self, page_name: str, template_content: str, 
                            template_name: Optional[str] = None) -> bool:
        """Create a WordPress page template file."""
        try:
            theme_path = self.get_theme_path()
            template_name = template_name or f"page-{page_name.lower().replace(' ', '-')}.php"
            template_file = theme_path / template_name
            
            # Write template file
            template_file.write_text(template_content, encoding='utf-8')
            print(f"✅ Created template: {template_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating template: {e}")
            return False
    
    def update_functions_php(self, function_code: str, function_name: str) -> bool:
        """Add or update a function in functions.php."""
        try:
            theme_path = self.get_theme_path()
            functions_file = theme_path / "functions.php"
            
            if not functions_file.exists():
                print(f"❌ functions.php not found at {functions_file}")
                return False
            
            content = functions_file.read_text(encoding='utf-8')
            
            # Check if function already exists
            if f"function {function_name}" in content:
                print(f"⚠️  Function {function_name} already exists. Skipping.")
                return True
            
            # Add function before closing PHP tag or at end
            if content.strip().endswith('?>'):
                content = content.rstrip('?>').rstrip() + f"\n\n{function_code}\n\n?>"
            else:
                content += f"\n\n{function_code}\n"
            
            functions_file.write_text(content, encoding='utf-8')
            print(f"✅ Added function {function_name} to functions.php")
            return True
        except Exception as e:
            print(f"❌ Error updating functions.php: {e}")
            return False
    
    def create_page_creation_function(self, page_name: str, page_slug: str, 
                                     template_name: str) -> str:
        """Generate WordPress page creation function code."""
        function_name = f"southwestsecret_create_{page_slug.replace('-', '_')}_page"
        
        code = f"""// Create {page_name} page on theme activation
function {function_name}() {{
    if (get_page_by_path('{page_slug}')) {{
        return; // Page already exists
    }}
    
    ${page_slug}_page = array(
        'post_title'    => '{page_name}',
        'post_name'     => '{page_slug}',
        'post_content'  => '',
        'post_status'   => 'publish',
        'post_type'     => 'page',
        'page_template' => '{template_name}'
    );
    
    wp_insert_post(${page_slug}_page);
}}
add_action('after_switch_theme', '{function_name}');"""
        
        return code
    
    def setup_page(self, page_name: str, page_slug: Optional[str] = None,
                  template_content: Optional[str] = None,
                  template_name: Optional[str] = None) -> bool:
        """Complete page setup: create template and add to functions.php."""
        page_slug = page_slug or page_name.lower().replace(' ', '-')
        template_name = template_name or f"page-{page_slug}.php"
        
        # Default template if none provided
        if not template_content:
            template_content = f"""<?php
/**
 * Template Name: {page_name}
 * 
 * @package SouthWestSecret
 */

get_header();
?>

<section class="{page_slug}-section">
    <div class="container">
        <h1 class="section-title">{page_name}</h1>
        <p>Content goes here...</p>
    </div>
</section>

<?php get_footer(); ?>"""
        
        # Create template file
        if not self.create_page_template(page_name, template_content, template_name):
            return False
        
        # Create page creation function
        function_code = self.create_page_creation_function(page_name, page_slug, template_name)
        
        # Add to functions.php
        if not self.update_functions_php(function_code, 
                                        f"southwestsecret_create_{page_slug.replace('-', '_')}_page"):
            return False
        
        print(f"✅ Page '{page_name}' setup complete!")
        print(f"   Template: {template_name}")
        print(f"   Slug: {page_slug}")
        print(f"   URL: /{page_slug}")
        return True
    
    def list_existing_pages(self) -> List[Dict[str, str]]:
        """List all existing page templates."""
        theme_path = self.get_theme_path()
        pages = []
        
        for template_file in theme_path.glob("page-*.php"):
            try:
                content = template_file.read_text(encoding='utf-8')
                # Extract template name
                template_name = None
                for line in content.split('\n'):
                    if 'Template Name:' in line:
                        template_name = line.split('Template Name:')[-1].strip()
                        break
                
                pages.append({
                    'file': template_file.name,
                    'template_name': template_name or 'Unknown',
                    'path': str(template_file)
                })
            except Exception as e:
                print(f"⚠️  Error reading {template_file}: {e}")
        
        return pages
    
    def add_to_menu(self, page_slug: str, menu_text: Optional[str] = None) -> bool:
        """Add page to WordPress navigation menu in functions.php."""
        try:
            theme_path = self.get_theme_path()
            functions_file = theme_path / "functions.php"
            
            if not functions_file.exists():
                return False
            
            content = functions_file.read_text(encoding='utf-8')
            menu_text = menu_text or page_slug.replace('-', ' ').title()
            
            # Check if menu function exists
            if 'southwestsecret_add_artist_menu_items' in content:
                # Find the function and add new menu item
                pattern = r'(southwestsecret_add_artist_menu_items\([^)]+\)\s*\{[^}]*)(\$items\s*\.=)'
                
                # Get page URL code
                page_url_code = f"""        // Get {menu_text} page URL
        ${page_slug}_page = get_page_by_path('{page_slug}');
        if (${page_slug}_page) {{
            ${page_slug}_url = get_permalink(${page_slug}_page->ID);
        }} else {{
            ${page_slug}_url = home_url('/{page_slug}');
        }}
        
        ${page_slug}_item = '<li><a href="' . esc_url(${page_slug}_url) . '">{menu_text}</a></li>';"""
                
                # Add before the items assignment
                if page_url_code not in content:
                    # Find where to insert (before $aria_item or $carmyn_item)
                    if '$aria_item' in content:
                        content = content.replace('$aria_item =', 
                                                 f"{page_url_code}\n\n        $aria_item =")
                    elif '$carmyn_item' in content:
                        content = content.replace('$carmyn_item =',
                                                 f"{page_url_code}\n\n        $carmyn_item =")
                    else:
                        # Add at end of function before return
                        content = content.replace('return $items;',
                                                f"{page_url_code}\n        return $items;")
                    
                    # Add to items concatenation
                    if f'${page_slug}_item' not in content:
                        if '. $aria_item . $carmyn_item' in content:
                            content = content.replace('. $aria_item . $carmyn_item',
                                                    f'. $aria_item . $carmyn_item . ${page_slug}_item')
                        elif '$aria_item' in content:
                            content = content.replace('$aria_item', 
                                                    f'$aria_item . ${page_slug}_item')
                        else:
                            content = content.replace('$items .=',
                                                    f"$items .= ${page_slug}_item . ")
                    
                    functions_file.write_text(content, encoding='utf-8')
                    print(f"✅ Added {menu_text} to navigation menu")
                    return True
                else:
                    print(f"⚠️  {menu_text} already in menu")
                    return True
            else:
                print("⚠️  Menu function not found. Creating new menu function...")
                # Create new menu function
                menu_function = f"""
// Add {menu_text} to navigation menu
function southwestsecret_add_{page_slug}_menu_item($items, $args) {{
    if ($args->theme_location == 'primary') {{
        ${page_slug}_page = get_page_by_path('{page_slug}');
        if (${page_slug}_page) {{
            ${page_slug}_url = get_permalink(${page_slug}_page->ID);
        }} else {{
            ${page_slug}_url = home_url('/{page_slug}');
        }}
        ${page_slug}_item = '<li><a href="' . esc_url(${page_slug}_url) . '">{menu_text}</a></li>';
        $items .= ${page_slug}_item;
    }}
    return $items;
}}
add_filter('wp_nav_menu_items', 'southwestsecret_add_{page_slug}_menu_item', 10, 2);"""
                return self.update_functions_php(menu_function, f"southwestsecret_add_{page_slug}_menu_item")
        except Exception as e:
            print(f"❌ Error adding to menu: {e}")
            return False
    
    def create_database_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """Generate code to create a WordPress database table."""
        try:
            theme_path = self.get_theme_path()
            functions_file = theme_path / "functions.php"
            
            if not functions_file.exists():
                return False
            
            content = functions_file.read_text(encoding='utf-8')
            function_name = f"southwestsecret_create_{table_name}_table"
            
            # Check if already exists
            if function_name in content:
                print(f"⚠️  Table {table_name} creation function already exists")
                return True
            
            # Generate column definitions
            column_defs = []
            for col_name, col_type in columns.items():
                column_defs.append(f"        {col_name} {col_type}")
            
            table_code = f"""// Create {table_name} database table on theme activation
function {function_name}() {{
    global $wpdb;
    $table_name = $wpdb->prefix . '{table_name}';
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE IF NOT EXISTS $table_name (
{chr(10).join(column_defs)}
    ) $charset_collate;";
    
    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}}
add_action('after_switch_theme', '{function_name}');"""
            
            return self.update_functions_php(table_code, function_name)
        except Exception as e:
            print(f"❌ Error creating database table code: {e}")
            return False
    
    def update_page_content(self, page_slug: str, new_content: str) -> bool:
        """Update content in a page template file."""
        try:
            theme_path = self.get_theme_path()
            template_file = theme_path / f"page-{page_slug}.php"
            
            if not template_file.exists():
                print(f"❌ Template file not found: {template_file}")
                return False
            
            content = template_file.read_text(encoding='utf-8')
            
            # Find and replace content between <section> tags or update specific parts
            # Simple approach: replace content in main section
            pattern = r'(<section[^>]*>.*?<div class="container">.*?)(<p>.*?</p>|Content goes here\.\.\.)(.*?</div>.*?</section>)'
            
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, 
                               r'\1' + new_content + r'\3',
                               content, flags=re.DOTALL)
            else:
                # Add content before closing section
                content = content.replace('</section>', 
                                        f'{new_content}\n</section>')
            
            template_file.write_text(content, encoding='utf-8')
            print(f"✅ Updated content in {template_file.name}")
            return True
        except Exception as e:
            print(f"❌ Error updating page content: {e}")
            return False
    
    def verify_setup(self) -> Dict[str, bool]:
        """Verify WordPress setup is complete."""
        results = {
            'theme_exists': False,
            'functions_php_exists': False,
            'pages_exist': False
        }
        
        try:
            theme_path = self.get_theme_path()
            results['theme_exists'] = theme_path.exists()
            
            functions_file = theme_path / "functions.php"
            results['functions_php_exists'] = functions_file.exists()
            
            pages = list(theme_path.glob("page-*.php"))
            results['pages_exist'] = len(pages) > 0
            results['page_count'] = len(pages)
            
        except Exception as e:
            print(f"⚠️  Error verifying setup: {e}")
        
        return results


def main():
    """CLI interface for WordPress page setup."""
    import argparse
    
    parser = argparse.ArgumentParser(description="WordPress Page Setup Tool")
    parser.add_argument('--site', default='southwestsecret', 
                       help='Site key (default: southwestsecret)')
    parser.add_argument('--list', action='store_true',
                       help='List existing pages')
    parser.add_argument('--create', type=str,
                       help='Create a new page (page name)')
    parser.add_argument('--slug', type=str,
                       help='Page slug (default: auto-generated from name)')
    parser.add_argument('--template', type=str,
                       help='Template file path (optional)')
    
    args = parser.parse_args()
    
    try:
        setup = WordPressPageSetup(args.site)
        
        if args.list:
            print(f"\n📄 Existing Pages for {args.site}:")
            print("=" * 70)
            pages = setup.list_existing_pages()
            for page in pages:
                print(f"  • {page['file']}")
                print(f"    Template: {page['template_name']}")
                print()
        
        elif args.create:
            success = setup.setup_page(
                page_name=args.create,
                page_slug=args.slug,
                template_content=Path(args.template).read_text() if args.template else None
            )
            sys.exit(0 if success else 1)
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

