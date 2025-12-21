# FreeRideInvestor wp-admin Redirect Loop Fix

**Date**: 2025-12-11  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Issue**: wp-admin redirect loop (exceeds 30 redirects)  
**URL**: https://freerideinvestor.com/wp-admin/

---

## Diagnosis

**Current Status**:
- ✅ Homepage: HTTP 200 (working)
- ❌ wp-admin: Redirect loop (exceeds 30 redirects)
- ✅ REST API: HTTP 200 (working)

**This is NOT the previous HTTP 500 error** - this is a redirect loop issue.

---

## Root Causes (Most Likely)

1. **WordPress Site URL Misconfiguration**
   - `WP_SITEURL` and `WP_HOME` in wp-config.php don't match
   - Site URL set to HTTP but site is HTTPS (or vice versa)

2. **.htaccess Redirect Loop**
   - Force HTTPS redirect conflicting with WordPress redirects
   - Multiple redirect rules conflicting

3. **Plugin Causing Redirect**
   - Security plugin forcing redirects
   - Maintenance mode plugin active
   - SSL/HTTPS enforcement plugin

4. **Cookie/Session Issues**
   - WordPress cookies not being set correctly
   - Domain mismatch in cookies

---

## Fix Steps

### Fix 1: Check WordPress Site URL Configuration (MOST COMMON)

**Via Hostinger File Manager**:
1. Navigate to `public_html/wp-config.php`
2. Check/add these lines (BEFORE `/* That's all, stop editing! */`):

```php
// Fix redirect loop - ensure URLs match
define('WP_HOME','https://freerideinvestor.com');
define('WP_SITEURL','https://freerideinvestor.com');
```

**OR via Database** (if you can access phpMyAdmin):
```sql
UPDATE wp_options SET option_value = 'https://freerideinvestor.com' WHERE option_name = 'home';
UPDATE wp_options SET option_value = 'https://freerideinvestor.com' WHERE option_name = 'siteurl';
```

### Fix 2: Check .htaccess File

**Via Hostinger File Manager**:
1. Navigate to `public_html/.htaccess`
2. **Temporarily rename** to `.htaccess.bak` to test
3. Try accessing wp-admin
4. If it works, the .htaccess has a redirect loop
5. Restore .htaccess and fix redirect rules

**Common .htaccess redirect loop causes**:
- Multiple `RewriteRule` redirects to HTTPS
- Conflicting redirect rules
- WordPress permalink rules conflicting with custom redirects

### Fix 3: Disable Plugins (If URL fix doesn't work)

**Via Hostinger File Manager**:
1. Navigate to `public_html/wp-content/plugins/`
2. Rename `plugins` → `plugins-disabled`
3. Try accessing wp-admin
4. If it works, re-enable plugins one by one to find culprit

**Most likely culprits**:
- Security plugins (Wordfence, iThemes Security)
- SSL/HTTPS enforcement plugins
- Maintenance mode plugins

### Fix 4: Check wp-config.php for Redirect Issues

**Look for these in wp-config.php**:
```php
// Remove or fix these if they exist:
define('FORCE_SSL_ADMIN', true);  // May cause issues if SSL not properly configured
define('COOKIE_DOMAIN', '.freerideinvestor.com');  // May cause cookie issues
```

### Fix 5: Clear WordPress Cache (If Using Caching)

**Via REST API** (since REST API works):
```bash
curl -X POST https://freerideinvestor.com/wp-json/wp/v2/cache/flush
```

**OR via File Manager**:
- Delete `wp-content/cache/` folder contents
- Delete `wp-content/advanced-cache.php` if exists

---

## Quick Diagnostic Commands

### Check Site URL via REST API:
```bash
curl https://freerideinvestor.com/wp-json/wp/v2/
# Look for "home" and "siteurl" in response
```

### Check if it's an .htaccess issue:
```bash
# Temporarily disable .htaccess
mv .htaccess .htaccess.bak
# Test wp-admin
# If it works, .htaccess is the problem
```

---

## Recommended Fix Order

1. **First**: Fix WordPress Site URL in wp-config.php (Fix 1)
2. **Second**: Test .htaccess by temporarily disabling it (Fix 2)
3. **Third**: Disable plugins to test (Fix 3)
4. **Fourth**: Check wp-config.php for redirect settings (Fix 4)

---

## Status

🟡 **BLOCKED** - Requires Hostinger File Manager or SFTP access to:
- Edit wp-config.php
- Check/rename .htaccess
- Disable plugins
- Access database (optional)

**Cannot proceed without server access.**

---

## Next Steps

1. ✅ **Diagnostic complete** - Redirect loop identified
2. ⏳ **Fix WordPress Site URL** - Access Hostinger File Manager
3. ⏳ **Test wp-admin** - Verify redirect loop is fixed
4. ⏳ **If still broken** - Try .htaccess fix
5. ⏳ **If still broken** - Disable plugins to test

---

**Created By**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-12-11



