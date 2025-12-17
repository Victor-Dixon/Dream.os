# Quick Fix: "Business plan template not found" Error

## Problem
The plugin is showing the error: **"Error: Business plan template not found. Please check plugin installation."**

This means the template file `templates/business-plan-display.php` is missing on the server.

## Solution: Redeploy the Plugin

The template file exists locally but wasn't deployed to the server. You need to redeploy the plugin.

### Step 1: Verify Local Files

First, verify the template file exists locally:

```bash
# From repository root
python temp_repos/crosbyultimateevents.com/deploy_business_plan_plugin.py --list-files
```

You should see:
```
📦 Plugin Files:
   ✅ crosby-business-plan.php (X bytes)
   ✅ assets/style.css (X bytes)
   ✅ templates/business-plan-display.php (X bytes)  ← This is the important one
```

### Step 2: Redeploy Plugin

Deploy the plugin to include all files:

```bash
# From repository root
python temp_repos/crosbyultimateevents.com/deploy_business_plan_plugin.py --site crosbyultimateevents.com
```

This will upload all plugin files including the template.

### Step 3: Verify Files on Server

Check that files were deployed correctly:

```bash
python temp_repos/crosbyultimateevents.com/verify_plugin_files.py --site crosbyultimateevents.com
```

You should see all files marked with ✅.

### Step 4: Test the Plugin

1. Go to WordPress Admin → Plugins
2. Ensure "Crosby Ultimate Events - Business Plan" is **activated**
3. Create or edit a page
4. Add the shortcode: `[crosby_business_plan]`
5. Save and view the page

## Alternative: Manual Upload

If the deployment script doesn't work, manually upload the template file:

1. **Via SFTP/FTP:**
   - Connect to your server
   - Navigate to `/wp-content/plugins/crosby-business-plan/`
   - Create `templates/` directory if it doesn't exist
   - Upload `business-plan-display.php` to `templates/` directory
   - Set file permissions to 644

2. **Via WordPress Admin (File Manager):**
   - Use a file manager plugin
   - Navigate to plugin directory
   - Upload the template file

## Expected File Structure on Server

```
/wp-content/plugins/crosby-business-plan/
├── crosby-business-plan.php          ← Main plugin file
├── assets/
│   └── style.css                     ← Plugin styles
└── templates/
    └── business-plan-display.php     ← Template file (THIS WAS MISSING)
```

## After Fixing

Once the template file is uploaded:

1. **Clear WordPress cache** (if using caching plugin)
2. **Clear browser cache** (Ctrl+F5 or Cmd+Shift+R)
3. **Test the shortcode** on a page
4. The business plan content should now display

## Still Not Working?

If after redeploying the template file still doesn't work:

1. **Enable WordPress Debug Mode:**
   Add to `wp-config.php`:
   ```php
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   ```

2. **Check Error Logs:**
   - Check `wp-content/debug.log`
   - Check server error logs

3. **Verify File Permissions:**
   - Files should be 644
   - Directories should be 755

4. **Check File Path:**
   The plugin looks for the template at:
   ```
   /wp-content/plugins/crosby-business-plan/templates/business-plan-display.php
   ```
   
   Verify this exact path exists on your server.

## Quick Command Reference

```bash
# List plugin files (local)
python temp_repos/crosbyultimateevents.com/deploy_business_plan_plugin.py --list-files

# Deploy plugin (to server)
python temp_repos/crosbyultimateevents.com/deploy_business_plan_plugin.py --site crosbyultimateevents.com

# Verify files on server
python temp_repos/crosbyultimateevents.com/verify_plugin_files.py --site crosbyultimateevents.com

# Check plugin status
python temp_repos/crosbyultimateevents.com/check_plugin_status.py --site crosbyultimateevents.com
```

---

**Last Updated:** December 2024
