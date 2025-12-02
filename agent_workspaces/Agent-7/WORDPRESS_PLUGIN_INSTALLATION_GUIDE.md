# WordPress Plugin Installation Guide

**Plugin**: Theme File Editor API  
**Purpose**: Enable REST API deployment of theme files  
**Date**: 2025-12-02  
**Agent**: Agent-7 (Web Development Specialist)

---

## 📋 **QUICK START**

### **For Immediate Deployment** (2-3 minutes per site):

1. **Upload Plugin** to WordPress site
2. **Activate Plugin** in WordPress Admin
3. **Create Application Password** for API authentication
4. **Deploy Files** using REST API tool

---

## 🚀 **INSTALLATION STEPS**

### **Step 1: Upload Plugin**

**Option A: Via FTP/SFTP** (Recommended)
```bash
# Upload plugin folder to WordPress site
scp -r websites/wordpress-plugins/theme-file-editor-api \
  user@yoursite.com:/path/to/wp-content/plugins/
```

**Option B: Via WordPress Admin**
1. Zip the plugin folder: `theme-file-editor-api.zip`
2. Go to WordPress Admin → Plugins → Add New
3. Click "Upload Plugin"
4. Select zip file and install

**Option C: Via SSH**
```bash
# Copy plugin to server
scp -r websites/wordpress-plugins/theme-file-editor-api \
  user@yoursite.com:/var/www/html/wp-content/plugins/
```

### **Step 2: Activate Plugin**

1. Go to WordPress Admin → Plugins
2. Find "Theme File Editor API"
3. Click "Activate"

### **Step 3: Verify Installation**

**Check REST API Endpoint**:
```bash
curl https://yoursite.com/wp-json/theme-file-editor/v1/update-file
```

**Expected Response**: HTTP 401 (Unauthorized) - means endpoint exists ✅  
**If 404**: Plugin not activated or not installed ❌

### **Step 4: Create Application Password**

1. Go to WordPress Admin → Users → Your Profile
2. Scroll to "Application Passwords" section
3. Enter name: "REST API Deployment"
4. Click "Add New Application Password"
5. **Copy the password** (shown only once!)
6. Save it securely (you'll need it for API calls)

**Note**: Use Application Password, NOT your regular WordPress password

---

## 🔧 **CONFIGURATION**

### **Required Settings**

1. **Enable File Editing**:
   - Check `wp-config.php` for `DISALLOW_FILE_EDIT`
   - If set to `true`, remove it or set to `false`:
   ```php
   // Remove this line or set to false:
   define('DISALLOW_FILE_EDIT', false);
   ```

2. **User Permissions**:
   - User must have Administrator role
   - Or custom role with `edit_theme_options` capability

3. **File Permissions** (if needed):
   ```bash
   # Theme directory should be writable
   chmod 755 /path/to/wp-content/themes/your-theme/
   chmod 644 /path/to/wp-content/themes/your-theme/functions.php
   ```

---

## 📝 **USAGE**

### **Deploy File via REST API**

**Using Python Tool**:
```bash
python tools/deploy_via_wordpress_rest_api.py \
  --site https://freerideinvestor.com \
  --theme freerideinvestor \
  --file D:/websites/FreeRideInvestor/functions.php \
  --username your_username \
  --password your_application_password
```

**Using cURL**:
```bash
curl -X POST https://yoursite.com/wp-json/theme-file-editor/v1/update-file \
  -u "username:application_password" \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "freerideinvestor",
    "file": "functions.php",
    "content": "<?php\n// Your file content\n"
  }'
```

---

## 🔒 **SECURITY**

### **Security Features**

- ✅ Requires WordPress authentication
- ✅ Requires `edit_theme_options` capability
- ✅ Validates file paths (prevents directory traversal)
- ✅ Only allows safe file types (php, css, js, txt)
- ✅ Ensures files are within theme directory

### **Security Recommendations**

1. **Use Application Passwords**: Never use your main WordPress password
2. **HTTPS Only**: Always use HTTPS for API calls
3. **Limit Access**: Only grant to trusted users
4. **Monitor Usage**: Check WordPress logs regularly
5. **Keep Updated**: Update WordPress and plugins regularly

---

## 🐛 **TROUBLESHOOTING**

### **Error: "Plugin endpoint not found" (404)**

**Solution**:
- Verify plugin is activated
- Check plugin file is in correct location
- Clear WordPress cache

### **Error: "Authentication failed" (401)**

**Solution**:
- Verify username is correct
- Verify application password is correct (not regular password)
- Check password wasn't revoked

### **Error: "Permission denied" (403)**

**Solution**:
- Ensure user has Administrator role
- Check `DISALLOW_FILE_EDIT` is not set in `wp-config.php`
- Verify user has `edit_theme_options` capability

### **Error: "File editing is disabled"**

**Solution**:
- Remove `DISALLOW_FILE_EDIT` from `wp-config.php`
- Or set to `false`: `define('DISALLOW_FILE_EDIT', false);`

### **Error: "File is not writable"**

**Solution**:
- Check file permissions: `chmod 644 functions.php`
- Check directory permissions: `chmod 755 theme-directory/`
- Verify file ownership matches web server user

---

## 📊 **SITES TO INSTALL ON**

### **Priority Sites**:

1. **freerideinvestor.com**
   - Theme: `freerideinvestor`
   - File: `functions.php`
   - Status: ⏳ Pending installation

2. **prismblossom.online**
   - Theme: `prismblossom`
   - File: `functions.php`
   - Status: ⏳ Pending installation

### **Installation Checklist**:

- [ ] Upload plugin to site
- [ ] Activate plugin
- [ ] Create application password
- [ ] Test endpoint availability
- [ ] Verify file editing is enabled
- [ ] Test deployment with dry-run
- [ ] Document credentials securely

---

## ✅ **VERIFICATION**

### **After Installation**:

1. **Test Endpoint**:
   ```bash
   curl https://yoursite.com/wp-json/theme-file-editor/v1/update-file
   ```
   Should return: HTTP 401 (endpoint exists) ✅

2. **Test Authentication**:
   ```bash
   python tools/deploy_via_wordpress_rest_api.py \
     --site https://yoursite.com \
     --theme your-theme \
     --file test.php \
     --dry-run
   ```
   Should show: "✅ Theme File Editor API plugin detected" ✅

3. **Test Deployment** (with small test file):
   ```bash
   python tools/deploy_via_wordpress_rest_api.py \
     --site https://yoursite.com \
     --theme your-theme \
     --file test.php \
     --username your_username \
     --password your_app_password
   ```

---

## 📚 **REFERENCE**

- **Plugin Location**: `websites/wordpress-plugins/theme-file-editor-api/`
- **Plugin README**: `websites/wordpress-plugins/theme-file-editor-api/README.md`
- **Deployment Tool**: `tools/deploy_via_wordpress_rest_api.py`
- **API Documentation**: See plugin README for full API details

---

**Guide Created**: 2025-12-02  
**Agent**: Agent-7 (Web Development Specialist)

🐝 **WE. ARE. SWARM. ⚡🔥**

