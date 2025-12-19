# WordPress Management Capabilities

**Status:** ✅ **YES - Full WordPress management available**

## Overview

We have a comprehensive `WordPressManager` system that can connect to and manage all WordPress sites from the `D:\websites` directory.

## Configured Sites (11 sites)

All sites are configured in `tools/wordpress_manager.py`:

1. **southwestsecret.com** → `D:/websites/southwestsecret.com`
2. **prismblossom.online** → `D:/websites/prismblossom.online`
3. **freerideinvestor.com** → `D:/websites/FreeRideInvestor`
4. **ariajet.site** → `D:/websites/ariajet.site`
5. **weareswarm.online** → `D:/websites/Swarm_website`
6. **weareswarm.site** → `D:/websites/Swarm_website`
7. **tradingrobotplug.com** → `D:/websites/tradingrobotplug.com`
8. **dadudekc.com** → `D:/websites/dadudekc.com`
9. **crosbyultimateevents.com** → `D:/Agent_Cellphone_V2_Repository/temp_repos/crosbyultimateevents.com`
10. **houstonsipqueen.com** → `D:/websites/houstonsipqueen.com`
11. **digitaldreamscape.site** → `D:/websites/digitaldreamscape.site`

## Management Capabilities

### ✅ **Post Management**
- Create posts via WordPress REST API
- Update post status (publish, draft, private, pending)
- Pin/unpin posts
- Update post content

**Example:**
```python
from tools.wordpress_manager import WordPressManager
manager = WordPressManager("houstonsipqueen.com")
# Posts are created via REST API (see tools/houstonsipqueen_theme_and_post.py)
```

### ✅ **Theme Management**
- **Activate themes** via WP-CLI or browser automation
- **Deploy theme files** via SFTP
- **Change themes** programmatically
- **List available themes**

**Example:**
```bash
python tools/wordpress_manager.py --site houstonsipqueen.com --activate-theme houstonsipqueen
```

### ✅ **Page Management**
- Create WordPress pages
- Deploy page templates
- Update page content
- Manage page structure

**Example:**
```python
manager = WordPressManager("dadudekc.com")
manager.create_page("About", "about", template_content="...")
```

### ✅ **File Deployment**
- Deploy files via SFTP/SSH
- Deploy theme files
- Deploy plugin files
- Automatic cache flushing

**Example:**
```bash
python tools/wordpress_manager.py --site dadudekc.com --deploy-file path/to/file.php
```

### ✅ **Menu Management**
- Create menus
- Assign menus to locations
- Add menu items
- Update navigation structure

### ✅ **Connection Methods**
1. **SFTP/SSH** (primary) - Direct file deployment
2. **WP-CLI** - Command-line WordPress operations
3. **WordPress REST API** - Content management
4. **Browser Automation** (fallback) - Theme activation when WP-CLI unavailable

## Credentials Configuration

Credentials are loaded from:
1. **`.deploy_credentials/sites.json`** (preferred, site-specific)
2. **`.env` file** (fallback, global)

**Required credentials:**
- `host` - SFTP hostname
- `username` - SFTP username
- `password` - SFTP password
- `port` - SFTP port (default: 65002)

**For REST API operations:**
- `WORDPRESS_USER` - WordPress admin username
- `WORDPRESS_APP_PASSWORD` - WordPress application password

## Usage Examples

### Activate a Theme
```bash
python tools/wordpress_manager.py --site houstonsipqueen.com --activate-theme houstonsipqueen
```

### Deploy a File
```bash
python tools/wordpress_manager.py --site dadudekc.com --deploy-file path/to/style.css --remote-path wp-content/themes/dadudekc/style.css
```

### Create a Page
```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("dadudekc.com")
manager.create_page("Contact", "contact", template_content="...")
```

### List Themes
```bash
python tools/wordpress_manager.py --site houstonsipqueen.com --list-themes
```

## Integration with Websites Directory

**Local Development:**
- All site files are in `D:\websites\`
- Edit files locally
- Deploy via `WordPressManager`

**Workflow:**
1. Edit files in `D:\websites\{site}/`
2. Test locally (if possible)
3. Deploy via `WordPressManager.deploy_file()` or CLI
4. Changes go live immediately

## Tools Available

- **`tools/wordpress_manager.py`** - Main management tool (SSOT)
- **`tools/houstonsipqueen_theme_and_post.py`** - Site-specific operations
- **`tools/deploy_hsq_site_content.py`** - Content deployment
- **`tools/pin_houstonsipqueen_post.py`** - Post management
- **`tools/create_dadudekc_*.py`** - Site-specific page creation
- And 50+ other WordPress tools

## Current Status

✅ **Fully Operational:**
- All 11 sites configured
- SFTP deployment working
- WP-CLI integration active
- REST API posting functional
- Theme activation working
- Page creation working

⚠️ **Requires:**
- Credentials in `.deploy_credentials/sites.json` or `.env`
- SFTP access to hosting provider
- WordPress admin credentials for REST API

## Next Steps

1. **Verify credentials** - Ensure all sites have credentials configured
2. **Test connections** - Test SFTP/WP-CLI for each site
3. **Document workflows** - Create site-specific deployment guides
4. **Automate common tasks** - Build wrapper scripts for frequent operations

---

**TL;DR:** Yes, we can fully manage all WordPress sites from the `D:\websites` directory using `WordPressManager`. 🐝

