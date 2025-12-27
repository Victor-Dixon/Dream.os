#!/usr/bin/env python3
"""
Detect dadudekc.com WordPress Theme Structure
==============================================

Attempts to detect WordPress theme structure for dadudekc.com via:
1. Local file system check
2. Remote WordPress REST API query
3. Common hosting patterns

V2 Compliance | Author: Agent-3 | Date: 2025-12-26
"""

import sys
from pathlib import Path
import json
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

project_root = Path(__file__).parent.parent
site_path = Path("D:/websites/websites/dadudekc.com")

def check_local_wordpress():
    """Check for local WordPress installation."""
    wp_paths = [
        site_path / "wp",
        site_path / "wordpress",
        site_path / "public_html" / "wp",
        site_path / "wp-content",
    ]
    
    for wp_path in wp_paths:
        if wp_path.exists():
            # Check for theme directory
            themes_path = wp_path / "wp-content/themes" if "wp-content" not in str(wp_path) else wp_path / "themes"
            if themes_path.exists():
                themes = [d.name for d in themes_path.iterdir() if d.is_dir() and (d / "style.css").exists()]
                return {
                    "found": True,
                    "wp_path": str(wp_path),
                    "themes_path": str(themes_path),
                    "themes": themes,
                    "type": "local"
                }
    
    return {"found": False, "type": "local"}

def check_wordpress_rest_api():
    """Check WordPress REST API for theme info."""
    base_urls = [
        "https://dadudekc.com",
        "https://www.dadudekc.com",
    ]
    
    for base_url in base_urls:
        try:
            # Try to access WordPress REST API
            api_url = f"{base_url}/wp-json/wp/v2"
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ WordPress REST API accessible: {api_url}")
                
                # Try to get theme info (requires authentication or public endpoint)
                # Most sites don't expose theme info via REST API without auth
                return {
                    "found": True,
                    "api_url": api_url,
                    "type": "remote_api",
                    "note": "REST API accessible, but theme info requires admin access"
                }
        except Exception as e:
            logger.debug(f"REST API check failed for {base_url}: {e}")
    
    return {"found": False, "type": "remote_api"}

def get_common_hosting_patterns():
    """Return common WordPress hosting theme paths."""
    return {
        "common_paths": [
            "/wp-content/themes/[ACTIVE_THEME]/",
            "/public_html/wp-content/themes/[ACTIVE_THEME]/",
            "/www/wp-content/themes/[ACTIVE_THEME]/",
            "/httpdocs/wp-content/themes/[ACTIVE_THEME]/",
        ],
        "detection_methods": [
            "WordPress Admin → Appearance → Theme Editor (shows active theme)",
            "SFTP/File Manager → wp-content/themes/ directory",
            "SSH → ls wp-content/themes/",
            "WordPress CLI → wp theme list",
        ]
    }

def generate_deployment_guidance():
    """Generate deployment guidance for Agent-7."""
    local_check = check_local_wordpress()
    api_check = check_wordpress_rest_api()
    hosting_patterns = get_common_hosting_patterns()
    
    guidance = {
        "site": "dadudekc.com",
        "timestamp": datetime.now().isoformat(),
        "local_wordpress": local_check,
        "remote_api": api_check,
        "hosting_patterns": hosting_patterns,
        "recommended_approach": []
    }
    
    if local_check["found"]:
        guidance["recommended_approach"] = [
            "✅ Local WordPress installation found",
            f"   Theme path: {local_check['themes_path']}",
            f"   Available themes: {', '.join(local_check['themes'])}",
            "   Deploy directly to local theme directory"
        ]
    else:
        guidance["recommended_approach"] = [
            "⚠️  No local WordPress installation found",
            "   dadudekc.com is a remote WordPress site",
            "",
            "📋 DEPLOYMENT METHODS (in order of preference):",
            "",
            "1. WordPress Admin Theme Editor:",
            "   - Login: https://dadudekc.com/wp-admin",
            "   - Navigate: Appearance → Theme Editor",
            "   - Active theme name shown at top",
            "   - Create/edit files in active theme",
            "",
            "2. SFTP/File Manager:",
            "   - Connect via hosting control panel SFTP",
            "   - Navigate to: wp-content/themes/[ACTIVE_THEME]/",
            "   - Upload/create template files",
            "",
            "3. SSH + WP-CLI (if available):",
            "   - SSH into server",
            "   - Run: wp theme list (shows active theme)",
            "   - Navigate to: wp-content/themes/[ACTIVE_THEME]/",
            "",
            "4. Hosting Control Panel File Manager:",
            "   - Login to hosting control panel",
            "   - Navigate to File Manager",
            "   - Find wp-content/themes/ directory",
            "   - Identify active theme folder",
        ]
    
    return guidance

def main():
    """Main execution."""
    logger.info("🔍 Detecting dadudekc.com WordPress Theme Structure")
    logger.info("=" * 60)
    
    guidance = generate_deployment_guidance()
    
    # Print summary
    print("\n" + "=" * 60)
    print("WordPress Theme Structure Detection")
    print("=" * 60)
    
    if guidance["local_wordpress"]["found"]:
        print("✅ Local WordPress installation found")
        print(f"   Theme path: {guidance['local_wordpress']['themes_path']}")
        print(f"   Available themes: {', '.join(guidance['local_wordpress']['themes'])}")
    else:
        print("⚠️  No local WordPress installation found")
        print("   dadudekc.com requires remote deployment")
        print("\n📋 Recommended deployment methods:")
        for method in guidance["recommended_approach"][3:]:  # Skip first 3 lines
            print(f"   {method}")
    
    # Save guidance
    report_path = project_root / "docs/website_audits/2026/dadudekc.com_WORDPRESS_THEME_STRUCTURE.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report_content = f"""# dadudekc.com WordPress Theme Structure
## Detection Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Site:** dadudekc.com  
**Purpose:** Deploy Tier 1 Quick Wins (WEB-01 hero/CTA + WEB-04 contact form)

---

## Detection Results

### Local WordPress Installation
```json
{json.dumps(guidance['local_wordpress'], indent=2)}
```

### Remote WordPress API
```json
{json.dumps(guidance['remote_api'], indent=2)}
```

---

## Deployment Guidance

"""
    
    for line in guidance["recommended_approach"]:
        report_content += f"{line}\n"
    
    report_content += f"""

---

## Common Hosting Theme Paths

"""
    for path in guidance["hosting_patterns"]["common_paths"]:
        report_content += f"- `{path}`\n"
    
    report_content += f"""

## Theme Detection Methods

"""
    for method in guidance["hosting_patterns"]["detection_methods"]:
        report_content += f"- {method}\n"
    
    report_content += f"""

---

## Files Ready for Deployment

**Location:** `D:/websites/websites/tier1_quick_wins_output/dadudekc.com/`

1. **hero-section.php** - Hero/CTA optimization (WEB-01)
2. **hero-optimization.css** - Hero styling
3. **contact-form.php** - Low-friction contact form (WEB-04)
4. **DEPLOYMENT_INSTRUCTIONS.md** - Detailed deployment guide

---

## Next Steps for Agent-7

1. **Identify Active Theme:**
   - Login to WordPress Admin: https://dadudekc.com/wp-admin
   - Navigate: Appearance → Themes
   - Note the active theme name

2. **Deploy Files:**
   - Use WordPress Admin Theme Editor, SFTP, or File Manager
   - Create/edit files in: `wp-content/themes/[ACTIVE_THEME]/`
   - Create `template-parts/` directory if needed

3. **Integration:**
   - Update `front-page.php` or homepage template to include:
     - `<?php get_template_part('template-parts/hero-section'); ?>`
     - `<?php get_template_part('template-parts/contact-form'); ?>`
   - Enqueue CSS in `functions.php`

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agent-3 (Infrastructure & DevOps)**  
**Status:** ✅ Theme structure detection complete
"""
    
    report_path.write_text(report_content, encoding='utf-8')
    logger.info(f"\n📊 Report saved: {report_path}")
    
    # Save JSON for programmatic access
    json_path = project_root / "reports/dadudekc_wordpress_structure.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(guidance, indent=2), encoding='utf-8')
    logger.info(f"📊 JSON saved: {json_path}")

if __name__ == "__main__":
    main()

