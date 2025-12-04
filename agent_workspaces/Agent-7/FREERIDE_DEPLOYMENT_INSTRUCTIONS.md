# FreeRideInvestor functions.php Deployment Instructions

**Date**: 2025-12-01  
**File**: `websites/FreeRideInvestor/functions.php`  
**Purpose**: Remove all Developer Tools links from navigation menu

---

## 📋 **DEPLOYMENT STEPS**

### **Step 1: Deploy functions.php**

**File to Deploy**: `D:\websites\FreeRideInvestor\functions.php`

**Deployment Methods**:

#### **Option A: FTP/SFTP (Recommended)**
1. Connect to your hosting server via FTP/SFTP
2. Navigate to: `/public_html/wp-content/themes/freerideinvestor/`
3. Upload `functions.php` (overwrite existing file)
4. Verify file permissions (should be 644 or 755)

#### **Option B: WordPress Admin**
1. Log into WordPress admin
2. Go to **Appearance > Theme Editor**
3. Select **freerideinvestor** theme
4. Click **functions.php** in the file list
5. Replace entire contents with updated `functions.php`
6. Click **Update File**

#### **Option C: WordPress Deployer (If Credentials Available)**
```bash
# Once credentials are configured in .deploy_credentials/sites.json or .env
python tools/deploy_freeride_functions.py
```

---

### **Step 2: Clear WordPress Menu Cache**

After deploying `functions.php`, clear the menu cache:

1. **WordPress Admin Method**:
   - Go to **Appearance > Menus**
   - Click **Save Menu** (even if no changes) - this refreshes the cache
   - Or go to **Settings > Permalinks** and click **Save Changes**

2. **Plugin Method** (if using caching plugin):
   - Clear all caches from your caching plugin
   - Examples: WP Super Cache, W3 Total Cache, WP Rocket

3. **Manual Method**:
   - Delete `wp-content/cache/` directory (if exists)
   - Or use WP-CLI: `wp cache flush`

---

### **Step 3: Verify Menu in WordPress Admin**

1. Go to **Appearance > Menus**
2. Select the **Primary Menu** (or menu assigned to "primary" location)
3. **Manually remove any Developer Tools items**:
   - Look for menu items with:
     - Title: "Developer Tool" or "Developer Tools"
     - URL containing: `/developer-tools` or `/developer-tool`
   - Check each menu item and delete any Developer Tools entries
4. Click **Save Menu**

---

### **Step 4: Verify on Live Site**

1. Visit `https://freerideinvestor.com`
2. Check the navigation menu
3. **Expected Result**: Zero "Developer Tool" links should appear
4. If links still appear:
   - Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
   - Check if menu cache was cleared
   - Verify `functions.php` was uploaded correctly

---

## 🔍 **WHAT THE FIX DOES**

The updated `functions.php` includes:

1. **Enhanced Menu Filter** (`freeride_dedupe_developer_tools_menu`):
   - Removes ALL menu items with "Developer Tool" in title
   - Removes ALL menu items with `/developer-tools` in URL
   - Removes ALL menu items with "developer" in post name/slug
   - Checks page object IDs for developer pages
   - Priority: 999 (runs after other filters)

2. **HTML Output Filter** (`freeride_remove_developer_tools_from_menu_html`):
   - Additional safety filter that removes Developer Tools from HTML output
   - Catches any items that slip through the objects filter

---

## ⚠️ **TROUBLESHOOTING**

### **If Developer Tools Links Still Appear After Deployment**:

1. **Check File Upload**:
   - Verify `functions.php` was uploaded to correct location
   - Check file modification date matches your local file
   - Verify file size matches (should be ~53KB)

2. **Check Menu Cache**:
   - Clear all caches again
   - Try accessing site in incognito/private window
   - Check if caching plugin is active

3. **Check WordPress Menu**:
   - Go to **Appearance > Menus**
   - Manually remove Developer Tools items from menu
   - Save menu

4. **Check Filter Priority**:
   - The filter uses priority 999 to run after other filters
   - If another plugin uses higher priority, it might interfere

5. **Check Theme Location**:
   - Verify menu is assigned to "primary" location
   - Filter only works on "primary" menu location

---

## 📝 **VERIFICATION CHECKLIST**

- [ ] `functions.php` deployed to `/wp-content/themes/freerideinvestor/functions.php`
- [ ] File permissions correct (644 or 755)
- [ ] WordPress menu cache cleared
- [ ] Caching plugin cache cleared (if applicable)
- [ ] Developer Tools items removed from WordPress menu admin
- [ ] Menu saved in WordPress admin
- [ ] Live site checked - no Developer Tools links visible
- [ ] Browser cache cleared and site rechecked

---

## 🚀 **QUICK DEPLOYMENT COMMAND** (If Credentials Available)

Once credentials are configured:

```bash
# Deploy functions.php
python tools/deploy_freeride_functions.py

# Or use WordPress manager directly
python tools/wordpress_manager.py --site freerideinvestor --deploy
```

---

**Status**: ✅ **READY FOR DEPLOYMENT**  
**File**: `websites/FreeRideInvestor/functions.php`  
**Size**: 53,088 bytes

**🐝 WE. ARE. SWARM. ⚡🔥**



