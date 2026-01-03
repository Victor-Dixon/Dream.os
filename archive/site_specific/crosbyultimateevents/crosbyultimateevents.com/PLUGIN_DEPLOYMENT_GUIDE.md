# Business Plan Plugin Deployment Guide

## Overview

The WordPress Manager has been extended with plugin deployment support. You can now deploy WordPress plugins just like themes!

## What Was Added

### New WordPress Manager Features

1. **`get_plugin_path(plugin_name)`** - Locates plugin directory
2. **`deploy_plugin_file(local_path, plugin_name, ...)`** - Deploys single plugin file
3. **`deploy_plugin(plugin_name, ...)`** - Deploys entire plugin directory

### CLI Arguments

- `--deploy-plugin PLUGIN_NAME` - Deploy entire plugin
- `--deploy-plugin-file PATH` - Deploy single plugin file
- `--plugin-name NAME` - Required with `--deploy-plugin-file`

## Usage Examples

### Deploy Business Plan Plugin

**Option 1: Using the deployment script (Recommended)**
```bash
# From repository root
python archive/site_specific/crosbyultimateevents/deploy_business_plan_plugin.py --site crosbyultimateevents.com

# Dry-run (test without deploying)
python archive/site_specific/crosbyultimateevents/deploy_business_plan_plugin.py --site crosbyultimateevents.com --dry-run

# List plugin files
python archive/site_specific/crosbyultimateevents/deploy_business_plan_plugin.py --list-files
```

**Option 2: Using WordPress Manager directly**
```bash
# Deploy entire plugin
python tools/wordpress_manager.py --site crosbyultimateevents.com --deploy-plugin crosby-business-plan

# Deploy single file
python tools/wordpress_manager.py --site crosbyultimateevents.com --deploy-plugin-file path/to/file.php --plugin-name crosby-business-plan

# Dry-run
python tools/wordpress_manager.py --site crosbyultimateevents.com --deploy-plugin crosby-business-plan --dry-run
```

**Option 3: Using Python API**
```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("crosbyultimateevents.com")
files_deployed = manager.deploy_plugin("crosby-business-plan")
print(f"Deployed {files_deployed} files")
```

## Plugin Structure

The plugin is located at:
```
archive/site_specific/crosbyultimateevents/wordpress-plugins/crosby-business-plan/
├── crosby-business-plan.php (main plugin file)
├── assets/
│   └── style.css (styling)
├── templates/
│   └── business-plan-display.php (display template)
├── README.md (documentation)
└── INSTALLATION.md (setup guide)
```

## Deployment Process

1. **Connect to WordPress server** via SFTP (uses credentials from `.deploy_credentials/sites.json` or `.env`)
2. **Upload plugin files** to `/wp-content/plugins/crosby-business-plan/`
3. **Auto-flush cache** after successful deployment
4. **Activate plugin** in WordPress Admin → Plugins

## After Deployment

1. **Activate the Plugin:**
   - Go to WordPress Admin → Plugins
   - Find "Crosby Ultimate Events - Business Plan"
   - Click "Activate"

2. **Add to a Page:**
   - Create or edit a page
   - Add shortcode: `[crosby_business_plan]`
   - Publish the page

3. **Display Specific Section:**
   ```
   [crosby_business_plan section="executive"]
   [crosby_business_plan section="financial"]
   ```

## Plugin Features

- ✅ Full business plan display
- ✅ Section-by-section viewing
- ✅ Professional styling
- ✅ Table of contents navigation
- ✅ Print-friendly layout
- ✅ Mobile responsive
- ✅ SEO-friendly structure

## Troubleshooting

### Plugin Not Found
```
❌ Plugin directory not found: crosby-business-plan
```
**Solution:** Check that plugin exists at:
```
archive/site_specific/crosbyultimateevents/wordpress-plugins/crosby-business-plan/
```

### Connection Failed
```
❌ Connection failed to host:port
```
**Solution:** 
1. Check credentials in `.deploy_credentials/sites.json` or `.env`
2. Verify SFTP port (default: 65002 for Hostinger)
3. Check firewall settings

### Files Not Deploying
**Solution:**
1. Use `--dry-run` to test first
2. Check file permissions
3. Verify remote directory exists
4. Review deployment logs

## Manual Deployment (Fallback)

If automated deployment fails:

1. **Zip the plugin:**
   ```bash
   cd archive/site_specific/crosbyultimateevents/wordpress-plugins
   zip -r crosby-business-plan.zip crosby-business-plan/
   ```

2. **Upload via WordPress Admin:**
   - Go to Plugins → Add New
   - Click "Upload Plugin"
   - Select the zip file
   - Click "Install Now"
   - Activate the plugin

3. **Or via SFTP:**
   - Upload entire `crosby-business-plan` folder to `/wp-content/plugins/`
   - Set proper file permissions (755 for directories, 644 for files)

## Next Steps

After successful deployment:

1. ✅ Plugin deployed
2. ⏭️ Activate in WordPress Admin
3. ⏭️ Create "Business Plan" page
4. ⏭️ Add shortcode `[crosby_business_plan]`
5. ⏭️ Test on frontend
6. ⏭️ Add to navigation menu (optional)

---

**Created:** December 2024  
**Plugin Version:** 1.0.0  
**WordPress Manager:** Extended with plugin support

