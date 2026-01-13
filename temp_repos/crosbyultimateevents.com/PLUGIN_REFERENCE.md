# Plugin Reference Guide
## Complete List of Plugins Referenced and Used

**Date:** December 2024  
**Project:** Crosby Ultimate Events Website

---

## Overview

This document provides a comprehensive list of all plugins referenced, used, or integrated in the Crosby Ultimate Events website project.

---

## Active Plugins

### 1. Crosby Business Plan Plugin (`crosby-business-plan`)

**Status:** ✅ Active/Referenced  
**Type:** Custom WordPress Plugin  
**Location:** `wordpress-plugins/crosby-business-plan/`

#### Plugin Details

- **Plugin Name:** Crosby Ultimate Events - Business Plan
- **Version:** 1.0.0
- **Author:** DaDudeKC
- **Text Domain:** `crosby-business-plan`
- **Main File:** `crosby-business-plan.php`

#### Functionality

- **Primary Purpose:** Displays business plan content on WordPress pages
- **Shortcode:** `[crosby_business_plan]`
- **Shortcode Options:**
  - `[crosby_business_plan]` - Display full business plan
  - `[crosby_business_plan section="executive"]` - Display specific section
  - `[crosby_business_plan download="false"]` - Hide download link

#### Available Sections

The plugin supports displaying these sections:
- `executive` - Executive Summary
- `company` - Company Description
- `products` - Products & Services
- `market` - Market Analysis
- `marketing` - Marketing & Sales Strategy
- `operations` - Operations Plan
- `financial` - Financial Projections
- `management` - Management Team
- `risks` - Risk Analysis
- `growth` - Growth Strategy
- `timeline` - Implementation Timeline
- `metrics` - Key Metrics

#### Plugin Structure

```
wordpress-plugins/crosby-business-plan/
├── crosby-business-plan.php          # Main plugin file
├── assets/
│   └── style.css                     # Plugin styles
├── templates/
│   └── business-plan-display.php    # Business plan template
├── INSTALLATION.md                   # Installation instructions
└── README.md                         # Plugin documentation
```

#### Plugin Constants

- `CROSBY_BP_VERSION` - Plugin version (1.0.0)
- `CROSBY_BP_PLUGIN_DIR` - Plugin directory path
- `CROSBY_BP_PLUGIN_URL` - Plugin URL

#### Plugin Class

- **Class Name:** `Crosby_Business_Plan`
- **Check if active:** `class_exists('Crosby_Business_Plan')`

#### WordPress Hooks Used

- `init` - Initialize plugin
- `wp_enqueue_scripts` - Enqueue styles
- `admin_menu` - Add admin settings page

#### Admin Features

- Settings page at: **Settings → Business Plan**
- Provides usage instructions
- Lists available shortcode options
- Shows available sections

#### Integration Points

**Theme Integration:**
- Theme `functions.php` does NOT directly reference this plugin
- Plugin works independently via shortcode
- Can be integrated using helper functions (see `PLUGIN_THEME_INTEGRATION.md`)

**Usage Examples:**

1. **In Page Content:**
   ```
   [crosby_business_plan]
   ```

2. **In Theme Template (PHP):**
   ```php
   <?php echo do_shortcode('[crosby_business_plan]'); ?>
   ```

3. **With Section Filter:**
   ```php
   <?php echo do_shortcode('[crosby_business_plan section="executive"]'); ?>
   ```

#### Deployment & Management Scripts

**Deployment Scripts:**
- `deploy_business_plan_plugin.py` - Deploys plugin to WordPress site
- `verify_plugin_files.py` - Verifies plugin files on server
- `check_plugin_status.py` - Checks plugin activation status

**Testing Scripts:**
- `test_plugin_output.php` - Tests plugin output
- `debug_plugin.php` - Debug plugin functionality
- `test_shortcode_direct.py` - Tests shortcode execution

#### Documentation Files

- `PLUGIN_THEME_INTEGRATION.md` - Integration guide
- `PLUGIN_DEPLOYMENT_GUIDE.md` - Deployment instructions
- `TROUBLESHOOTING_PLUGIN.md` - Troubleshooting guide
- `QUICK_FIX_TEMPLATE_ERROR.md` - Quick fix guide

---

## Plugin Dependencies

### WordPress Requirements

- **WordPress Version:** 5.0+ (recommended)
- **PHP Version:** 7.4+ (required)
- **No external plugin dependencies**

### Theme Compatibility

- **Theme:** `crosbyultimateevents` (custom theme)
- **Compatibility:** ✅ Fully compatible
- **Integration:** Independent (works via shortcode)

---

## Plugin Usage in Codebase

### Direct References

**Plugin Class References:**
- `Crosby_Business_Plan` class defined in `crosby-business-plan.php`
- Checked via `class_exists('Crosby_Business_Plan')` in integration code

**Shortcode References:**
- Shortcode: `crosby_business_plan`
- Registered via: `add_shortcode('crosby_business_plan', ...)`
- Used in: Page content, theme templates, test files

**File References:**
- Main plugin file: `wordpress-plugins/crosby-business-plan/crosby-business-plan.php`
- Template file: `wordpress-plugins/crosby-business-plan/templates/business-plan-display.php`
- Stylesheet: `wordpress-plugins/crosby-business-plan/assets/style.css`

### Indirect References

**Theme Files:**
- `functions.php` - No direct plugin references (independent design)
- Theme templates - Can use shortcode but don't require plugin

**Documentation:**
- Multiple markdown files reference plugin usage
- Integration guides explain plugin-theme relationship

---

## Plugin Status Checks

### How to Check if Plugin is Active

**Method 1: Class Check**
```php
if (class_exists('Crosby_Business_Plan')) {
    // Plugin is active
}
```

**Method 2: Shortcode Check**
```php
if (shortcode_exists('crosby_business_plan')) {
    // Plugin is active
}
```

**Method 3: Function Check (if helper added)**
```php
if (function_exists('crosby_is_business_plan_active')) {
    if (crosby_is_business_plan_active()) {
        // Plugin is active
    }
}
```

### Command Line Checks

**Via WP-CLI:**
```bash
wp plugin list --status=active
wp plugin is-active crosby-business-plan
```

**Via Python Script:**
```bash
python check_plugin_status.py --site crosbyultimateevents.com
```

---

## Plugin Installation & Activation

### Installation Path

```
/wp-content/plugins/crosby-business-plan/
```

### Activation

1. Upload plugin files to `/wp-content/plugins/crosby-business-plan/`
2. Go to WordPress Admin → Plugins
3. Find "Crosby Ultimate Events - Business Plan"
4. Click "Activate"

### Deployment

Use the deployment script:
```bash
python deploy_business_plan_plugin.py --site crosbyultimateevents.com
```

---

## Plugin Configuration

### Settings Location

**WordPress Admin:** Settings → Business Plan

### Configuration Options

Currently, the plugin uses default settings. No configuration options are available in the admin panel (settings page is informational only).

### Customization

- **Styles:** Edit `assets/style.css`
- **Content:** Edit `templates/business-plan-display.php`
- **Functionality:** Edit `crosby-business-plan.php`

---

## Plugin Integration Status

### Current Integration Level

**Status:** ⚠️ Independent (Not Fully Integrated)

- ✅ Plugin works independently
- ✅ Theme works independently
- ⚠️ No automatic integration
- ✅ Can be integrated via shortcode

### Integration Options

See `PLUGIN_THEME_INTEGRATION.md` for:
- Integration methods
- Code examples
- Best practices
- Helper functions

---

## Other Plugins Referenced

### None Found

**Search Results:**
- No other WordPress plugins found in this codebase
- No third-party plugin dependencies
- No plugin conflicts detected

**Note:** This project only uses the custom `crosby-business-plan` plugin. No other plugins are referenced or required.

---

## Plugin Files Summary

### Core Plugin Files

| File | Purpose | Location |
|------|---------|----------|
| `crosby-business-plan.php` | Main plugin file | `wordpress-plugins/crosby-business-plan/` |
| `business-plan-display.php` | Template file | `wordpress-plugins/crosby-business-plan/templates/` |
| `style.css` | Plugin styles | `wordpress-plugins/crosby-business-plan/assets/` |

### Supporting Files

| File | Purpose | Location |
|------|---------|----------|
| `INSTALLATION.md` | Installation guide | `wordpress-plugins/crosby-business-plan/` |
| `README.md` | Plugin documentation | `wordpress-plugins/crosby-business-plan/` |

### Management Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `deploy_business_plan_plugin.py` | Deploy plugin | `temp_repos/crosbyultimateevents.com/` |
| `verify_plugin_files.py` | Verify files | `temp_repos/crosbyultimateevents.com/` |
| `check_plugin_status.py` | Check status | `temp_repos/crosbyultimateevents.com/` |
| `test_plugin_output.php` | Test output | `temp_repos/crosbyultimateevents.com/` |
| `debug_plugin.php` | Debug plugin | `temp_repos/crosbyultimateevents.com/` |

### Documentation Files

| File | Purpose | Location |
|------|---------|----------|
| `PLUGIN_THEME_INTEGRATION.md` | Integration guide | `temp_repos/crosbyultimateevents.com/` |
| `PLUGIN_DEPLOYMENT_GUIDE.md` | Deployment guide | `temp_repos/crosbyultimateevents.com/` |
| `TROUBLESHOOTING_PLUGIN.md` | Troubleshooting | `temp_repos/crosbyultimateevents.com/` |
| `QUICK_FIX_TEMPLATE_ERROR.md` | Quick fixes | `temp_repos/crosbyultimateevents.com/` |

---

## Plugin Usage Statistics

### Shortcode Usage

- **Primary Usage:** Page content via shortcode
- **Secondary Usage:** Theme template integration (optional)
- **Tertiary Usage:** Admin settings page (informational)

### Integration Points

- **Theme Templates:** Can use shortcode (optional)
- **Page Content:** Direct shortcode usage
- **Widgets:** Can use shortcode in text widgets
- **Custom Code:** Via `do_shortcode()` function

---

## Recommendations

### Current State

✅ **Strengths:**
- Plugin is well-structured
- Good separation of concerns
- Comprehensive documentation
- Deployment scripts available

⚠️ **Areas for Improvement:**
- No direct theme integration
- No helper functions in theme
- No automatic styling coordination

### Suggested Enhancements

1. **Add Helper Functions to Theme:**
   - Add plugin check function to `functions.php`
   - Add business plan display helper
   - Add business plan link helper

2. **Styling Coordination:**
   - Coordinate colors between plugin and theme
   - Use CSS variables for consistency
   - Add theme-specific overrides

3. **Enhanced Integration:**
   - Add business plan link to footer
   - Add business plan sections to relevant pages
   - Create dedicated business plan page template

---

## Quick Reference

### Plugin Check
```php
class_exists('Crosby_Business_Plan')
```

### Shortcode Usage
```
[crosby_business_plan]
[crosby_business_plan section="executive"]
```

### PHP Usage
```php
echo do_shortcode('[crosby_business_plan]');
```

### Plugin Path
```
/wp-content/plugins/crosby-business-plan/
```

### Admin Settings
```
Settings → Business Plan
```

---

## Related Documentation

- **Integration Guide:** `PLUGIN_THEME_INTEGRATION.md`
- **Deployment Guide:** `PLUGIN_DEPLOYMENT_GUIDE.md`
- **Troubleshooting:** `TROUBLESHOOTING_PLUGIN.md`
- **Quick Fixes:** `QUICK_FIX_TEMPLATE_ERROR.md`

---

**Last Updated:** December 2024  
**Maintained By:** Development Team  
**Plugin Version:** 1.0.0

