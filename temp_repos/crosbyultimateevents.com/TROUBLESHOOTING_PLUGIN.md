# Troubleshooting: Business Plan Plugin Not Displaying

## Common Issues and Solutions

### Issue: Nothing Displays When Using Shortcode

**Symptoms:**
- Shortcode `[crosby_business_plan]` shows as plain text
- Page is blank where shortcode should be
- No error messages visible

**Solutions:**

#### 1. Check Plugin is Activated

1. Go to WordPress Admin → Plugins
2. Look for "Crosby Ultimate Events - Business Plan"
3. Click "Activate" if it's not activated
4. If plugin is not listed, it needs to be deployed first

#### 2. Verify Shortcode Syntax

**Correct usage:**
```
[crosby_business_plan]
```

**Incorrect usage:**
```
[crosby-business-plan]  ❌ Wrong dash style
[crosby_businessplan]   ❌ Missing underscore
```

#### 3. Clear WordPress Cache

- If using a caching plugin (WP Super Cache, W3 Total Cache, etc.), clear the cache
- If using server-side caching, clear that as well
- Try accessing the page in an incognito/private browser window

#### 4. Check for Plugin Conflicts

1. Temporarily deactivate all other plugins
2. Test if business plan displays
3. If it works, reactivate plugins one by one to find the conflict

#### 5. Enable WordPress Debug Mode

Add to `wp-config.php`:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

Then check `wp-content/debug.log` for errors.

#### 6. Check Template File Exists

Verify the template file exists:
- Path: `/wp-content/plugins/crosby-business-plan/templates/business-plan-display.php`

If missing, redeploy the plugin.

#### 7. Test Shortcode Directly

Create a test page and add only:
```
[crosby_business_plan]
```

If it still doesn't work, try with PHP:
```php
<?php echo do_shortcode('[crosby_business_plan]'); ?>
```

#### 8. Check PHP Error Logs

- Check your hosting control panel for PHP error logs
- Look for errors related to the plugin
- Common issues: missing files, permission errors, PHP version compatibility

---

### Issue: Plugin Shows Error Message

**Error: "Business plan template not found"**

**Solution:**
- Plugin files are missing or not uploaded correctly
- Redeploy the plugin using the deployment script
- Check file permissions (should be 644 for files, 755 for directories)

**Error: "Business plan template returned empty content"**

**Solution:**
- Template file exists but has no content
- Check template file for PHP errors
- Verify file encoding (should be UTF-8)
- Check if template file is corrupted

---

### Issue: Content Displays But Looks Broken

**Symptoms:**
- Content appears but styling is missing
- Layout is broken
- Colors/fonts don't match

**Solutions:**

1. **Check CSS File Loading:**
   - Open page source (View → Page Source)
   - Search for `crosby-business-plan-style`
   - Verify CSS file URL is correct and accessible

2. **Clear Browser Cache:**
   - Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
   - Or clear browser cache completely

3. **Check for CSS Conflicts:**
   - Theme CSS might be overriding plugin styles
   - Check browser developer tools (F12) for CSS conflicts
   - Add custom CSS to override if needed

---

### Issue: Specific Section Not Displaying

**When using:** `[crosby_business_plan section="executive"]`

**Check:**
1. Section name spelling (case-sensitive)
2. Available sections:
   - executive
   - company
   - products
   - market
   - marketing
   - operations
   - financial
   - management
   - risks
   - growth
   - timeline
   - metrics

**Test with:**
```
[crosby_business_plan]
```
(Shows all sections - if this works, section-specific should work too)

---

## Quick Diagnostic Checklist

Run through this checklist:

- [ ] Plugin is installed and activated
- [ ] Shortcode syntax is correct: `[crosby_business_plan]`
- [ ] WordPress cache is cleared
- [ ] Browser cache is cleared
- [ ] No JavaScript errors in browser console (F12)
- [ ] No PHP errors in debug log
- [ ] Template file exists at correct path
- [ ] CSS file is loading (check page source)
- [ ] Tested on a simple page with only the shortcode
- [ ] WordPress and PHP are up to date

---

## Testing the Plugin

### Method 1: Direct PHP Test

Create a file `test-plugin.php` in WordPress root:

```php
<?php
require_once('wp-load.php');
if (class_exists('Crosby_Business_Plan')) {
    echo do_shortcode('[crosby_business_plan]');
} else {
    echo 'Plugin not active';
}
```

Access via: `yoursite.com/test-plugin.php`

**⚠️ Remember to delete this file after testing!**

### Method 2: WordPress Admin Test

1. Go to Settings → Business Plan
2. Check if admin page loads (confirms plugin is active)
3. Review usage instructions

### Method 3: WP-CLI Test

If you have WP-CLI access:

```bash
wp eval 'echo do_shortcode("[crosby_business_plan]");'
```

---

## Still Not Working?

If none of the above solutions work:

1. **Check Plugin Files:**
   - All plugin files are in `/wp-content/plugins/crosby-business-plan/`
   - Main file: `crosby-business-plan.php`
   - Template: `templates/business-plan-display.php`
   - CSS: `assets/style.css`

2. **Verify Plugin Header:**
   - Open `crosby-business-plan.php`
   - Check plugin header matches WordPress standards
   - Verify plugin name is correct

3. **Check WordPress Version:**
   - Plugin requires WordPress 5.0+
   - Update WordPress if outdated

4. **Check PHP Version:**
   - Plugin requires PHP 7.4+
   - Update PHP if outdated

5. **Contact Support:**
   - Provide:
     - WordPress version
     - PHP version
     - Plugin version
     - Error messages (if any)
     - Steps to reproduce

---

## Plugin Status Check

You can use the provided script to check plugin status:

```bash
python temp_repos/crosbyultimateevents.com/check_plugin_status.py --site crosbyultimateevents.com
```

This will check:
- If plugin is installed
- If plugin is activated
- If plugin files exist on server
- If plugin loads without errors

---

## Quick Fixes Summary

**If nothing displays:**
1. Activate plugin
2. Clear cache
3. Check shortcode syntax
4. Test on simple page

**If error message:**
1. Check error details
2. Verify files exist
3. Check file permissions
4. Redeploy plugin if needed

**If styling broken:**
1. Clear browser cache
2. Check CSS file loading
3. Check for CSS conflicts
4. Add custom CSS if needed

---

**Last Updated:** December 2024
