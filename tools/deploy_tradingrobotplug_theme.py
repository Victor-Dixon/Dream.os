#!/usr/bin/env python3
"""
Deploy TradingRobotPlug Theme to Live Server
============================================

Deploys complete theme to live server with verification.

V2 Compliance | Author: Agent-3 | Date: 2025-12-26
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

project_root = Path(__file__).parent.parent
theme_path = Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme")

def get_theme_files():
    """Get list of theme files to deploy."""
    if not theme_path.exists():
        logger.error(f"❌ Theme path not found: {theme_path}")
        return []
    
    # Key files for deployment
    key_files = [
        "functions.php",
        "front-page.php",
        "style.css",
        "header.php",
        "footer.php",
        "index.php",
    ]
    
    # Inc directory files
    inc_files = [
        "inc/template-helpers.php",
        "inc/forms.php",
        "inc/analytics.php",
        "inc/rest-api.php",
        "inc/dashboard-api.php",
        "inc/asset-enqueue.php",
        "inc/theme-setup.php",
    ]
    
    # Assets
    asset_files = [
        "assets/css/custom.css",
        "assets/js/main.js",
    ]
    
    all_files = key_files + inc_files + asset_files
    
    # Verify files exist
    existing_files = []
    missing_files = []
    
    for file_path in all_files:
        full_path = theme_path / file_path
        if full_path.exists():
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    if missing_files:
        logger.warning(f"⚠️  Missing files: {missing_files}")
    
    logger.info(f"✅ Found {len(existing_files)}/{len(all_files)} theme files")
    return existing_files

def generate_deployment_plan():
    """Generate deployment plan."""
    files = get_theme_files()
    
    plan = {
        "site": "tradingrobotplug.com",
        "theme": "tradingrobotplug-theme",
        "timestamp": datetime.now().isoformat(),
        "deployment_type": "remote",
        "files_to_deploy": files,
        "total_files": len(files),
        "deployment_methods": [
            "SFTP/File Manager (recommended)",
            "WordPress Admin Theme Editor",
            "SSH + rsync/scp",
            "Git deployment (if configured)"
        ],
        "verification_steps": [
            "Verify theme active in WordPress Admin",
            "Check front-page.php loads correctly",
            "Verify hero section visible",
            "Verify waitlist form functional",
            "Clear all caches",
            "Test form submission"
        ]
    }
    
    return plan

def create_deployment_instructions(plan: dict) -> str:
    """Create deployment instructions."""
    instructions = f"""
# TradingRobotPlug.com Theme Deployment Instructions
## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Site:** tradingrobotplug.com  
**Theme:** tradingrobotplug-theme  
**Files to Deploy:** {plan['total_files']} files

---

## Deployment Methods

### Option 1: SFTP/File Manager (RECOMMENDED)

1. **Connect to server via SFTP or hosting File Manager**
2. **Navigate to:** `wp-content/themes/tradingrobotplug-theme/`
3. **Upload/Update files:**
"""
    
    for file_path in plan['files_to_deploy']:
        instructions += f"   - `{file_path}`\n"
    
    instructions += f"""
4. **Verify theme activation:**
   - Login: https://tradingrobotplug.com/wp-admin
   - Navigate: Appearance → Themes
   - Verify "tradingrobotplug-theme" is active

5. **Clear cache:**
   - Clear browser cache
   - Clear WordPress cache (if plugin installed)
   - Clear CDN cache (if applicable)

### Option 2: WordPress Admin Theme Editor

1. **Login:** https://tradingrobotplug.com/wp-admin
2. **Navigate:** Appearance → Theme Editor
3. **Select theme:** tradingrobotplug-theme
4. **Edit files directly** (not recommended for large deployments)

### Option 3: SSH + rsync/scp

```bash
# From local machine
cd D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/
rsync -avz tradingrobotplug-theme/ user@server:/path/to/wp-content/themes/tradingrobotplug-theme/

# Or using scp
scp -r tradingrobotplug-theme/ user@server:/path/to/wp-content/themes/
```

---

## Critical Files to Deploy

### Core Theme Files:
- `functions.php` - Modular functions, analytics, REST API
- `front-page.php` - Hero section, waitlist form (WEB-01, WEB-04)
- `style.css` - Theme styles
- `header.php` - Site header
- `footer.php` - Site footer

### Template Helpers:
- `inc/template-helpers.php` - Template loading logic (FIXED - handles front-page.php)
- `inc/forms.php` - Form handlers
- `inc/analytics.php` - GA4/Pixel integration
- `inc/rest-api.php` - REST API endpoints
- `inc/dashboard-api.php` - Dashboard API
- `inc/asset-enqueue.php` - Asset loading
- `inc/theme-setup.php` - Theme setup

### Assets:
- `assets/css/custom.css` - Custom styles
- `assets/js/main.js` - JavaScript

---

## Verification Checklist

- [ ] Theme files uploaded to server
- [ ] Theme active in WordPress Admin
- [ ] `front-page.php` loads correctly
- [ ] Hero section visible on homepage
- [ ] Waitlist form functional
- [ ] Contact form works
- [ ] CSS styling applied
- [ ] JavaScript functional
- [ ] All caches cleared
- [ ] Mobile responsive
- [ ] No console errors

---

## Post-Deployment Verification

1. **Visit homepage:** https://tradingrobotplug.com
2. **Check hero section:** Should display optimized hero with CTAs
3. **Check waitlist form:** Should be visible and functional
4. **Test form submission:** Submit test email
5. **Check console:** No JavaScript errors
6. **Mobile test:** Verify responsive design

---

## Architecture Validation (Agent-2)

After deployment, Agent-2 will validate:
- Theme structure alignment
- Modular functions.php compliance
- REST API endpoint configuration
- Design pattern consistency

---

**Deployment Plan Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agent-3 (Infrastructure & DevOps)**  
**Status:** ✅ Ready for deployment execution
"""
    
    return instructions

def main():
    """Main execution."""
    logger.info("🚀 TradingRobotPlug Theme Deployment Plan")
    logger.info("=" * 60)
    
    plan = generate_deployment_plan()
    
    if not plan['files_to_deploy']:
        logger.error("❌ No theme files found")
        return
    
    # Save deployment plan
    plan_path = project_root / "reports/tradingrobotplug_theme_deployment_plan.json"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    logger.info(f"📊 Deployment plan saved: {plan_path}")
    
    # Create instructions
    instructions = create_deployment_instructions(plan)
    instructions_path = project_root / "docs/website_audits/2026/TRADINGROBOTPLUG_THEME_DEPLOYMENT_INSTRUCTIONS.md"
    instructions_path.parent.mkdir(parents=True, exist_ok=True)
    instructions_path.write_text(instructions, encoding='utf-8')
    logger.info(f"📋 Instructions saved: {instructions_path}")
    
    logger.info(f"\n✅ Deployment plan complete")
    logger.info(f"   Files to deploy: {plan['total_files']}")
    logger.info(f"   Instructions: {instructions_path}")

if __name__ == "__main__":
    main()


