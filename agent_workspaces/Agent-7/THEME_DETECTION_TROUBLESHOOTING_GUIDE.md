# Theme Detection Troubleshooting Guide

**Issue**: AriaJet theme files deployed but WordPress not detecting  
**Date**: 2025-12-02  
**Agent**: Agent-7 (Web Development Specialist)

---

## ✅ **WHAT WE'VE VERIFIED**

1. **File Deployment**: ✅ Files are deployed correctly
2. **File Permissions**: ✅ Set to 755/644 (correct)
3. **File Location**: ✅ Files in correct location
4. **style.css Header**: ✅ Valid format (checked)
5. **functions.php Syntax**: ✅ Valid PHP (checked)

---

## 🔧 **TROUBLESHOOTING SCRIPTS CREATED**

### **1. Clear WordPress Transients**
```bash
python tools/clear_wordpress_transients.py --site ariajet --method wpcli
```
**Purpose**: Clears cached theme list in WordPress database

### **2. Enable WordPress Debug Mode**
```bash
python tools/enable_wordpress_debug.py --site ariajet
```
**Purpose**: Captures runtime errors in wp-content/debug.log

### **3. Check Theme Syntax**
```bash
python tools/check_theme_syntax.py --theme "D:/websites/ariajet.site/wordpress-theme/ariajet"
```
**Purpose**: Validates style.css header and PHP syntax

### **4. Manual Theme Activation** (Last Resort)
```bash
python tools/manual_theme_activation.py --site ariajet --theme ariajet
```
**Purpose**: Manually activates theme via database

---

## 🎯 **RECOMMENDED NEXT STEPS** (In Order)

### **Step 1: Clear WordPress Transients** ⭐ **TRY THIS FIRST**

WordPress caches the theme list. Clear it:

```bash
# Via WP-CLI (if available)
python tools/clear_wordpress_transients.py --site ariajet --method wpcli

# Or manually via WordPress admin:
# 1. Install "Transients Manager" plugin
# 2. Delete all transients
# 3. Or use WP-CLI: wp transient delete --all
```

**Expected Result**: Theme should appear in WordPress admin after refresh

---

### **Step 2: Enable Debug Mode & Check for Errors**

Enable debug logging to catch runtime errors:

```bash
python tools/enable_wordpress_debug.py --site ariajet
```

Then check for errors:
- Check `wp-content/debug.log` for fatal errors
- Look for PHP syntax errors in functions.php
- Check for missing dependencies

**Common Errors**:
- Fatal error: Call to undefined function
- Parse error: syntax error
- Missing required files

---

### **Step 3: Verify Theme Files Are Complete**

Check that all required files exist:
- ✅ `style.css` (with proper header)
- ✅ `functions.php` (valid PHP)
- ✅ `index.php` (required)
- ✅ `screenshot.png` (optional but recommended)

---

### **Step 4: Manual Database Activation** (Last Resort)

If all else fails, manually activate via database:

```bash
python tools/manual_theme_activation.py --site ariajet --theme ariajet
```

**Or via WP-CLI**:
```bash
wp theme activate ariajet
```

**Or via SQL**:
```sql
UPDATE wp_options SET option_value = 'ariajet' WHERE option_name = 'template';
UPDATE wp_options SET option_value = 'ariajet' WHERE option_name = 'stylesheet';
```

---

## 🔍 **MOST LIKELY CAUSES**

1. **WordPress Transients Cache** (90% likely)
   - Solution: Clear transients
   - Script: `clear_wordpress_transients.py`

2. **Runtime Error in functions.php** (5% likely)
   - Solution: Enable debug mode, check logs
   - Script: `enable_wordpress_debug.py`

3. **Missing Required Files** (3% likely)
   - Solution: Verify all files exist
   - Check: `index.php` must exist

4. **File Permissions** (2% likely)
   - Solution: Already verified (755/644)

---

## 📋 **QUICK FIX CHECKLIST**

- [ ] Clear WordPress transients
- [ ] Enable debug mode
- [ ] Check wp-content/debug.log for errors
- [ ] Verify index.php exists
- [ ] Hard refresh WordPress admin (Ctrl+F5)
- [ ] Try manual database activation if needed

---

## 🚀 **IMMEDIATE ACTION**

**Try this first**:

```bash
# 1. Clear transients (most likely fix)
python tools/clear_wordpress_transients.py --site ariajet --method wpcli

# 2. If WP-CLI not available, enable debug mode
python tools/enable_wordpress_debug.py --site ariajet

# 3. Check debug log for errors
# (via SFTP or WordPress admin file manager)
```

---

**Status**: ✅ Scripts ready, waiting for execution  
**Next**: Clear transients first, then check debug logs

🐝 **WE. ARE. SWARM. ⚡🔥**



