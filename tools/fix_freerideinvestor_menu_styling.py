#!/usr/bin/env python3
"""
Fix freerideinvestor.com menu styling and theme consistency.

This tool:
1. Analyzes homepage styling (CSS variables, gradient effects, hover states)
2. Updates navigation menu to match homepage stunning design
3. Ensures theme consistency across ALL pages (homepage, blog, about, contact)
"""

import os
import re
from pathlib import Path

# Paths
WEBSITE_ROOT = Path(r"D:\websites\websites\freerideinvestor.com")
THEME_DIR = WEBSITE_ROOT / "wp" / "wp-content" / "themes" / "freerideinvestor-modern"
CSS_DIR = THEME_DIR / "css" / "styles"
NAVIGATION_CSS = CSS_DIR / "components" / "_navigation.css"
HEADER_FOOTER_CSS = CSS_DIR / "layout" / "_header-footer.css"
HOME_PAGE_CSS = CSS_DIR / "pages" / "_home-page.css"
VARIABLES_CSS = CSS_DIR / "base" / "_variables.css"

# Homepage styling patterns extracted from _home-page.css
HOMEPAGE_STYLING = {
    "accent_color": "#2ecc71",  # Green accent
    "accent_dark": "#27ae60",   # Darker green
    "gradient_hero": "linear-gradient(135deg, #28b463, #27ae60)",
    "gradient_section": "linear-gradient(145deg, #121212, #1a1a1a)",
    "gradient_button": "linear-gradient(145deg, #27ae60, #2ecc71)",
    "gradient_button_hover": "linear-gradient(145deg, #2ecc71, #27ae60)",
    "text_light": "#f0f0f0",
    "text_muted": "#bbbbbb",
    "border_radius": "12px",
    "box_shadow": "0 8px 16px rgba(0, 0, 0, 0.4)",
    "box_shadow_hover": "0 12px 24px rgba(0, 0, 0, 0.6)",
    "transition": "all 0.3s ease",
    "transform_hover": "translateY(-5px) scale(1.05)",
}

def read_file(file_path):
    """Read file content."""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    """Write file content."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated: {file_path}")

def analyze_homepage_styling():
    """Analyze homepage CSS to extract styling patterns."""
    print("🔍 Analyzing homepage styling...")
    
    home_css = read_file(HOME_PAGE_CSS)
    if not home_css:
        return None
    
    # Extract key styling patterns
    patterns = {
        "gradients": re.findall(r'linear-gradient\([^)]+\)', home_css),
        "colors": re.findall(r'#[0-9a-fA-F]{6}', home_css),
        "border_radius": re.findall(r'border-radius:\s*(\d+px)', home_css),
        "box_shadows": re.findall(r'box-shadow:\s*([^;]+)', home_css),
    }
    
    print(f"✅ Found {len(patterns['gradients'])} gradients, {len(patterns['colors'])} colors")
    return patterns

def create_navigation_fix():
    """Create updated navigation CSS matching homepage styling."""
    print("🎨 Creating navigation styling fix...")
    
    nav_css = f"""/*--------------------------------------------------------------
  Navigation Menu - Updated to Match Homepage Stunning Design
  Generated: 2025-12-25
--------------------------------------------------------------*/

/* Navigation List Styling */
.main-nav .nav-list {{
  list-style: none;
  display: flex;
  gap: var(--spacing-sm);
  padding: 0;
  margin: 0;
  flex-wrap: wrap;
  align-items: center;
}}

/* Navigation Links - Match Homepage Stunning Design */
.main-nav .nav-list li a {{
  display: inline-block !important;
  padding: 12px 24px !important;
  border-radius: {HOMEPAGE_STYLING['border_radius']} !important;
  color: {HOMEPAGE_STYLING['text_light']} !important;
  text-decoration: none !important;
  font-weight: 600 !important;
  background: rgba(46, 204, 113, 0.1) !important; /* Green tint matching homepage */
  border: 1px solid rgba(46, 204, 113, 0.2) !important;
  transition: {HOMEPAGE_STYLING['transition']} !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 0.95rem;
}}

/* Hover and Focus States - Match Homepage Button Effects */
.main-nav .nav-list li a:hover,
.main-nav .nav-list li a:focus {{
  background: {HOMEPAGE_STYLING['gradient_button']} !important;
  color: #ffffff !important;
  border-color: {HOMEPAGE_STYLING['accent_color']} !important;
  transform: translateY(-3px) !important;
  box-shadow: {HOMEPAGE_STYLING['box_shadow']} !important;
  outline: none !important;
}}

/* Active Navigation Link - Match Homepage CTA Button */
.main-nav .nav-list li a.active,
.main-nav .nav-list li.current-menu-item > a,
.main-nav .nav-list li.current_page_item > a {{
  background: {HOMEPAGE_STYLING['gradient_button']} !important;
  color: #ffffff !important;
  border-color: {HOMEPAGE_STYLING['accent_color']} !important;
  box-shadow: {HOMEPAGE_STYLING['box_shadow']} !important;
  font-weight: 700 !important;
  transform: translateY(-2px) !important;
}}

/*--------------------------------------------------------------
  Responsive Adjustments
--------------------------------------------------------------*/

/* Navigation List for Smaller Screens */
@media (max-width: 768px) {{
  .main-nav .nav-list {{
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs, 10px);
  }}

  .main-nav .nav-list li a {{
    width: 100%;
    text-align: left;
    padding: var(--spacing-xs, 10px) var(--spacing-sm, 16px);
  }}
}}

/* Optional: Adjust for Very Small Screens */
@media (max-width: 480px) {{
  .main-nav .nav-list {{
    gap: var(--spacing-xs, 5px);
  }}

  .main-nav .nav-list li a {{
    font-size: 0.9rem;
    padding: var(--spacing-xs, 8px) var(--spacing-sm, 12px);
  }}
}}
"""
    
    return nav_css

def update_header_styling():
    """Update header to match homepage gradient background."""
    print("🎨 Updating header styling...")
    
    header_css = f"""/* Site Header - Match Homepage Gradient Background */
.site-header {{
  background: {HOMEPAGE_STYLING['gradient_section']} !important;
  padding: var(--spacing-sm);
  border-bottom: 2px solid rgba(46, 204, 113, 0.2);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}}

/* Navigation Container */
.main-nav {{
  background: transparent;
}}

/* Footer */
.site-footer {{
  background: var(--color-dark-grey);
  padding: var(--spacing-sm);
  text-align: center;
}}

.footer-links {{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}}

.site-footer p {{
  color: var(--color-text-muted);
  font-size: 0.85rem;
}}

/* Global Spacing Fix for Sections and Footer */
.section:last-of-type {{
    margin-bottom: 40px;
}}

.site-main {{
    padding-bottom: 20px;
}}

.footer {{
    margin-top: 0;
    padding-top: 20px;
}}
"""
    
    return header_css

def create_theme_consistency_css():
    """Create CSS to ensure theme consistency across all pages."""
    print("🎨 Creating theme consistency CSS...")
    
    consistency_css = f"""/*--------------------------------------------------------------
  Theme Consistency - Apply Homepage Styling to All Pages
  Generated: 2025-12-25
--------------------------------------------------------------*/

/* Apply homepage gradient background to all page containers */
.page,
.single,
.archive,
.search-results {{
  background: {HOMEPAGE_STYLING['gradient_section']};
  min-height: 100vh;
}}

/* Consistent section styling */
.section,
.content-area {{
  background: {HOMEPAGE_STYLING['gradient_section']};
  border-radius: {HOMEPAGE_STYLING['border_radius']};
  padding: var(--spacing-md);
  margin: var(--spacing-md) 0;
  box-shadow: {HOMEPAGE_STYLING['box_shadow']};
}}

/* Consistent heading styling */
h1, h2, h3 {{
  color: {HOMEPAGE_STYLING['accent_color']};
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}}

/* Consistent link styling */
a {{
  color: {HOMEPAGE_STYLING['accent_color']};
  transition: {HOMEPAGE_STYLING['transition']};
}}

a:hover {{
  color: {HOMEPAGE_STYLING['accent_dark']};
  transform: translateY(-2px);
}}

/* Consistent button styling */
.button,
.btn,
.cta-button {{
  background: {HOMEPAGE_STYLING['gradient_button']};
  color: #ffffff;
  border-radius: {HOMEPAGE_STYLING['border_radius']};
  padding: 14px 28px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: {HOMEPAGE_STYLING['transition']};
  box-shadow: {HOMEPAGE_STYLING['box_shadow']};
  border: none;
  cursor: pointer;
}}

.button:hover,
.btn:hover,
.cta-button:hover {{
  background: {HOMEPAGE_STYLING['gradient_button_hover']};
  transform: {HOMEPAGE_STYLING['transform_hover']};
  box-shadow: {HOMEPAGE_STYLING['box_shadow_hover']};
}}
"""
    
    return consistency_css

def main():
    """Main execution."""
    print("🚀 Starting freerideinvestor.com menu styling fix...")
    print(f"📁 Theme directory: {THEME_DIR}")
    
    # Analyze homepage styling
    patterns = analyze_homepage_styling()
    
    # Create navigation fix
    nav_css = create_navigation_fix()
    write_file(NAVIGATION_CSS, nav_css)
    
    # Update header styling
    header_css = update_header_styling()
    write_file(HEADER_FOOTER_CSS, header_css)
    
    # Create theme consistency CSS
    consistency_css = create_theme_consistency_css()
    consistency_file = CSS_DIR / "components" / "_theme-consistency.css"
    write_file(consistency_file, consistency_css)
    
    print("\n✅ Menu styling fix complete!")
    print("\n📋 Next steps:")
    print("1. Verify navigation menu matches homepage styling")
    print("2. Test on all pages (homepage, blog, about, contact)")
    print("3. Ensure theme consistency across entire site")
    print("4. Deploy changes to production")

if __name__ == "__main__":
    main()

