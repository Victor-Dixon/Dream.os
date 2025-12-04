# WordPress Deployer Usage Guide

**Author**: Agent-7 (Web Development Specialist)  
**Date**: 2025-12-01  
**Status**: ✅ **FIXED & ENHANCED**

---

## 📋 **OVERVIEW**

The WordPress Deployer is a comprehensive tool for managing WordPress sites, including:
- Page creation and deployment
- Theme replacement and activation
- File deployment via SFTP/SSH
- WP-CLI command execution
- Database table creation
- Menu management

---

## 🔧 **SETUP & CONFIGURATION**

### **1. Credential Configuration**

The deployer supports two methods for credentials:

#### **Method 1: Site-Specific Credentials (Recommended)**

Create `.deploy_credentials/sites.json`:

```json
{
  "prismblossom": {
    "host": "your-server.com",
    "username": "your-username",
    "password": "your-password",
    "port": 65002,
    "remote_path": "/public_html/wp-content/themes/prismblossom"
  },
  "freerideinvestor": {
    "host": "your-server.com",
    "username": "your-username",
    "password": "your-password",
    "port": 65002,
    "remote_path": "/public_html/wp-content/themes/freerideinvestor"
  }
}
```

**Important**: All fields must be non-empty strings. Empty strings will be rejected.

#### **Method 2: Shared Environment Variables**

Create `.env` file in project root:

```env
HOSTINGER_HOST=your-server.com
HOSTINGER_USER=your-username
HOSTINGER_PASS=your-password
HOSTINGER_PORT=65002
```

**Alternative variable names** (also supported):
- `SSH_HOST`, `SSH_USER`, `SSH_PASS`, `SSH_PORT`
- `HOST`, `USERNAME`, `PASSWORD`, `PORT`

**Note**: The deployer checks multiple locations for `.env`:
- `D:/Agent_Cellphone_V2_Repository/.env`
- `./.env` (current directory)
- `D:/websites/.env`
- `tools/../.env`

---

## 🚀 **USAGE EXAMPLES**

### **1. Basic Page Creation**

```python
from tools.wordpress_manager import WordPressManager
from pathlib import Path

# Initialize manager
manager = WordPressManager("prismblossom")

# Create a new page
manager.create_page("About Us", "about-us")

# Deploy the page template
theme_path = manager.get_theme_path()
page_file = theme_path / "page-about-us.php"
manager.deploy_file(page_file)
```

### **2. Theme Replacement**

```python
from tools.wordpress_manager import WordPressManager
from pathlib import Path

manager = WordPressManager("prismblossom")

# Connect to server
if manager.connect():
    # Replace entire theme (with backup)
    new_theme_path = Path("D:/websites/new-theme")
    manager.replace_theme(new_theme_path, backup=True)
    
    # Activate the theme
    manager.activate_theme("prismblossom")
    
    # Disconnect
    manager.disconnect()
```

### **3. List Available Themes**

```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("prismblossom")

if manager.connect():
    themes = manager.list_themes()
    for theme in themes:
        status = "✅ Active" if theme.get('status') == 'active' else "  "
        print(f"{status} {theme.get('name')} - {theme.get('version')}")
    manager.disconnect()
```

### **4. Deploy Single File**

```python
from tools.wordpress_manager import WordPressManager
from pathlib import Path

manager = WordPressManager("prismblossom")

# Deploy specific file
theme_path = manager.get_theme_path()
functions_file = theme_path / "functions.php"
manager.deploy_file(functions_file)

# Or deploy with custom remote path
manager.deploy_file(functions_file, "/public_html/wp-content/themes/prismblossom/functions.php")
```

### **5. Deploy All Theme Files**

```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("prismblossom")

if manager.connect():
    # Deploy all PHP files
    count = manager.deploy_theme("*.php")
    print(f"✅ Deployed {count} PHP files")
    
    # Deploy all CSS files
    count = manager.deploy_theme("*.css")
    print(f"✅ Deployed {count} CSS files")
    
    manager.disconnect()
```

### **6. WP-CLI Commands**

```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("prismblossom")

if manager.connect():
    # Execute WP-CLI command
    stdout, stderr, code = manager.wp_cli("plugin list")
    if code == 0:
        print(stdout)
    else:
        print(f"Error: {stderr}")
    
    manager.disconnect()
```

### **7. Database Table Creation**

```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("prismblossom")

# Create table code (adds to functions.php)
columns = {
    "id": "bigint(20) NOT NULL AUTO_INCREMENT",
    "name": "varchar(255) NOT NULL",
    "email": "varchar(255) NOT NULL",
    "created_at": "datetime DEFAULT CURRENT_TIMESTAMP",
    "PRIMARY KEY": "(id)"
}
manager.create_table("guestbook", columns)
```

### **8. Menu Management**

```python
from tools.wordpress_manager import WordPressManager

manager = WordPressManager("prismblossom")

# Add page to navigation menu
manager.add_to_menu("about-us", "About Us")
```

---

## 🛠️ **CLI USAGE**

### **Command-Line Interface**

```bash
# List themes
python tools/wordpress_manager.py --site prismblossom --list-themes

# Activate theme
python tools/wordpress_manager.py --site prismblossom --activate-theme prismblossom

# Replace theme
python tools/wordpress_manager.py --site prismblossom --replace-theme "D:/websites/new-theme"

# Deploy file
python tools/wordpress_manager.py --site prismblossom --deploy-file "functions.php"
```

---

## 🐛 **TROUBLESHOOTING**

### **Issue: "No credentials available"**

**Solution**:
1. Check `.deploy_credentials/sites.json` exists and has valid credentials
2. Check `.env` file exists with `HOSTINGER_*` variables
3. Verify credentials are not empty strings

**Error Message Example**:
```
Missing credentials for prismblossom: HOSTINGER_HOST/SSH_HOST, HOSTINGER_PASS/SSH_PASS
```

### **Issue: "Connection failed"**

**Possible Causes**:
1. **Authentication failed**: Username/password incorrect
2. **Host/Port incorrect**: Verify server address and port
3. **Firewall blocking**: Ensure SFTP/SSH port is open
4. **Network issues**: Check internet connection

**Error Message Example**:
```
Authentication failed for username@host:port
Please verify username and password are correct
```

### **Issue: "paramiko not installed"**

**Solution**:
```bash
pip install paramiko
```

### **Issue: "Theme directory not found"**

**Solution**:
1. Verify local theme path exists
2. Check site configuration in `SITE_CONFIGS`
3. Ensure theme structure matches expected layout

---

## 📊 **SUPPORTED SITES**

Current site configurations:

- **prismblossom** / **prismblossom.online**
  - Local: `D:/websites/prismblossom.online`
  - Theme: `prismblossom`
  - Remote: `/public_html/wp-content/themes/prismblossom`

- **freerideinvestor** / **FreeRideInvestor**
  - Local: `D:/websites/FreeRideInvestor`
  - Theme: `freerideinvestor`
  - Remote: `/public_html/wp-content/themes/freerideinvestor`

- **southwestsecret**
  - Local: `D:/websites/southwestsecret.com`
  - Theme: `southwestsecret`
  - Remote: `/public_html/wp-content/themes/southwestsecret`

---

## 🔍 **DEBUGGING**

### **Run Debug Tool**

```bash
# Full debug report
python tools/debug_wordpress_deployer.py

# Test actual deployment (requires credentials)
python tools/debug_wordpress_deployer.py --test-deploy
```

### **Enable Debug Logging**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from tools.wordpress_manager import WordPressManager
manager = WordPressManager("prismblossom")
```

---

## ✅ **FEATURES**

| Feature | Status | Description |
|---------|--------|-------------|
| Page Creation | ✅ Working | Creates templates + functions.php code |
| File Deployment | ✅ Working | SFTP file upload |
| Theme Replacement | ✅ Added | Replace entire theme with backup |
| Theme Activation | ✅ Added | Activate theme via WP-CLI |
| Theme Listing | ✅ Added | List all available themes |
| Menu Management | ✅ Working | Adds pages to menus |
| Database Tables | ✅ Working | Creates table code |
| WP-CLI Commands | ✅ Working | Execute WP-CLI remotely |

---

## 📝 **NOTES**

- **Default Port**: Hostinger SFTP uses port `65002` (not standard SSH port 22)
- **Backup**: Theme replacement automatically creates backups
- **Validation**: Credentials are validated for non-empty values
- **Error Messages**: Enhanced error messages show exactly what's missing

---

## 🚀 **NEXT STEPS**

1. **Configure Credentials**: Add valid credentials to `.deploy_credentials/sites.json` or `.env`
2. **Test Connection**: Run `python tools/debug_wordpress_deployer.py --test-deploy`
3. **Deploy Files**: Start deploying theme files to live sites

---

**🐝 WE. ARE. SWARM. ⚡🔥**



