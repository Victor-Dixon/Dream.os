# AriaJet Theme Detection Fix

**Date**: 2025-12-02  
**Root Cause**: WordPress not detecting theme despite correct deployment

---

## ✅ **CONFIRMED**

1. Files ARE deployed correctly to `/public_html/wp-content/themes/ariajet/`
2. All 10 files present on server
3. Same WordPress installation (not different server)
4. Style.css has correct theme header

---

## 🔍 **NON-OBVIOUS ISSUES TO CHECK**

### **1. PHP Syntax Error in functions.php**
- WordPress scans `style.css` first, but if `functions.php` has a fatal error, theme won't load
- **Check**: Run `php -l functions.php` to verify syntax

### **2. WordPress Theme Cache**
- WordPress caches theme list
- **Fix**: Delete `wp-content/cache/` or use `wp cache flush` command

### **3. File Permissions**
- WordPress needs read access (644 for files, 755 for directories)
- **Check**: Verify permissions via FTP

### **4. Style.css Header Format**
- WordPress is VERY strict about header format
- Must have exact format: `Theme Name: ariajet` (no extra spaces, correct case)
- **Check**: Verify header matches WordPress requirements exactly

### **5. WordPress Multi-Site Configuration**
- If multi-site, themes might need to be "network enabled"
- **Check**: Look for `MULTISITE` in wp-config.php

### **6. Plugin Conflict**
- A plugin might be blocking theme detection
- **Check**: Deactivate all plugins temporarily

---

## 🛠️ **IMMEDIATE FIXES TO TRY**

### **Fix 1: Force WordPress to Rescan Themes**

Add this to `wp-config.php` temporarily:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
```

Then check `/wp-content/debug.log` for theme-related errors.

### **Fix 2: Verify Style.css Header**

The header MUST be exactly:
```css
/*
Theme Name: ariajet
Theme URI: https://ariajet.site
Author: Aria
...
*/
```

No extra spaces, correct format.

### **Fix 3: Check PHP Errors**

WordPress won't show a theme if `functions.php` has fatal errors. Check:
- PHP syntax errors
- Missing required WordPress functions
- Fatal errors in theme initialization

### **Fix 4: Manual Theme Activation via Database**

If all else fails, activate via database:
```sql
UPDATE wp_options SET option_value = 'ariajet' WHERE option_name = 'template';
UPDATE wp_options SET option_value = 'ariajet' WHERE option_name = 'stylesheet';
```

---

## 🎯 **MOST LIKELY CAUSE**

**PHP fatal error in `functions.php` preventing WordPress from reading the theme header.**

WordPress workflow:
1. Scans `/wp-content/themes/` for directories
2. Reads `style.css` header
3. If `functions.php` exists, includes it
4. If `functions.php` has fatal error, theme is marked as broken and hidden

**Solution**: Check `functions.php` for syntax errors or missing dependencies.

---

**Next Step**: Verify `functions.php` has no PHP errors preventing theme detection.

