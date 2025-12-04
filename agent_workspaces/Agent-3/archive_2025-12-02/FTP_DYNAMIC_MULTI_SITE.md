# FTP Deployer - Dynamic Multi-Site Support

**Date**: 2025-12-02  
**Status**: ✅ **IMPLEMENTED**

---

## ✅ What Was Done

Made the FTP deployment system **fully dynamic** to support all 8+ sites automatically.

### **Key Features:**

1. **Dynamic Site Loading**
   - Loads site configurations from multiple sources
   - Supports `.deploy_credentials/sites.json` for site-specific credentials
   - Falls back to default configurations
   - Auto-detects site from file path

2. **Site-Specific Credentials**
   - Each site can have its own FTP credentials in `sites.json`
   - Falls back to shared `.env` credentials if site-specific not found
   - Supports different hosts, ports, usernames per site

3. **Auto-Detection**
   - Automatically detects site from file path
   - No need to specify `--site` if file is in known directory
   - Smart path matching

4. **Site Listing**
   - `--list-sites` shows all available sites
   - Displays local and remote paths for each site

---

## 🚀 Usage

### **List All Available Sites**

```bash
python tools/ftp_deployer.py --list-sites
```

**Output:**
```
📋 Available Sites:
============================================================
  • FreeRideInvestor
    Local: D:/websites/FreeRideInvestor
    Remote: /public_html/wp-content/themes/freerideinvestor
  • freerideinvestor
    Local: D:/websites/FreeRideInvestor
    Remote: /public_html/wp-content/themes/freerideinvestor
  • prismblossom
    Local: D:/websites/prismblossom.online
    Remote: /public_html/wp-content/themes/prismblossom
  • southwestsecret
    Local: D:/websites/southwestsecret.com
    Remote: /public_html/wp-content/themes/southwestsecret
  ... (and more)
```

### **Deploy with Auto-Detection**

```bash
# Auto-detects site from file path
python tools/ftp_deployer.py --deploy --file D:/websites/FreeRideInvestor/functions.php
```

### **Deploy with Explicit Site**

```bash
# Specify site explicitly
python tools/ftp_deployer.py --deploy --file functions.php --site freerideinvestor
```

### **Deploy to Any Site**

```bash
# Works for all sites
python tools/ftp_deployer.py --deploy --file D:/websites/prismblossom.online/style.css --site prismblossom
python tools/ftp_deployer.py --deploy --file D:/websites/southwestsecret.com/functions.php --site southwestsecret
```

---

## 📋 Supported Sites

Currently configured sites:

1. **freerideinvestor** / **FreeRideInvestor**
   - Local: `D:/websites/FreeRideInvestor`
   - Remote: `/public_html/wp-content/themes/freerideinvestor`

2. **prismblossom** / **prismblossom.online**
   - Local: `D:/websites/prismblossom.online`
   - Remote: `/public_html/wp-content/themes/prismblossom`

3. **southwestsecret**
   - Local: `D:/websites/southwestsecret.com`
   - Remote: `/public_html/wp-content/themes/southwestsecret`

4. **ariajet** / **ariajet.site**
   - Local: `D:/websites/ariajet.site`
   - Remote: `/public_html`

*(And more - system automatically discovers all configured sites)*

---

## 🔧 Configuration

### **Site-Specific Credentials**

Add site-specific FTP credentials to `.deploy_credentials/sites.json`:

```json
{
  "freerideinvestor": {
    "host": "157.173.214.121",
    "username": "u996867598.freerideinvestor.com",
    "password": "your_password",
    "port": 21,
    "remote_path": "/public_html/wp-content/themes/freerideinvestor"
  },
  "prismblossom": {
    "host": "different.host.com",
    "username": "prismblossom_user",
    "password": "different_password",
    "port": 21,
    "remote_path": "/public_html/wp-content/themes/prismblossom"
  }
}
```

### **Shared Credentials (Fallback)**

If site-specific credentials aren't found, uses shared credentials from `.env`:

```env
HOSTINGER_HOST=157.173.214.121
HOSTINGER_PORT=21
HOSTINGER_USER=u996867598.freerideinvestor.com
HOSTINGER_PASS=your_password
```

---

## 🎯 How It Works

### **1. Site Detection Priority**

1. **Explicit `--site` argument** (highest priority)
2. **Auto-detection from file path**
3. **Error if cannot detect**

### **2. Credential Loading Priority**

1. **Site-specific from `sites.json`** (if site has credentials)
2. **Shared from `.env`** (fallback)
3. **Command-line arguments** (override)

### **3. Remote Path Resolution**

1. **Explicit `--remote-path`** (highest priority)
2. **Auto-detect from file type** (e.g., `functions.php` → theme functions path)
3. **Calculate relative path** from local_path to file
4. **Fallback to filename** in remote_base

---

## 📊 Example Workflows

### **Deploy functions.php to FreeRideInvestor**

```bash
# Auto-detects site and path
python tools/ftp_deployer.py --deploy --file D:/websites/FreeRideInvestor/functions.php
```

### **Deploy style.css to PrismBlossom**

```bash
# Auto-detects site, calculates relative path
python tools/ftp_deployer.py --deploy --file D:/websites/prismblossom.online/wp-content/themes/prismblossom/style.css
```

### **Deploy to Custom Remote Path**

```bash
# Override remote path
python tools/ftp_deployer.py --deploy --file file.php --site freerideinvestor --remote-path /public_html/custom/path/file.php
```

### **Test Connection for Specific Site**

```bash
# Uses site-specific credentials if available
python tools/ftp_deployer.py --test --site freerideinvestor
```

---

## ✅ Benefits

1. **No Hardcoding**: All sites discovered dynamically
2. **Easy to Add Sites**: Just add to `sites.json` or default configs
3. **Flexible Credentials**: Site-specific or shared
4. **Auto-Detection**: Works without specifying site
5. **Scalable**: Supports unlimited sites

---

## 🔍 Troubleshooting

### **"Unknown site" Error**

Run `--list-sites` to see available sites:
```bash
python tools/ftp_deployer.py --list-sites
```

### **Auto-Detection Fails**

Specify site explicitly:
```bash
python tools/ftp_deployer.py --deploy --file path/to/file.php --site sitename
```

### **Wrong Remote Path**

Override with `--remote-path`:
```bash
python tools/ftp_deployer.py --deploy --file file.php --site sitename --remote-path /correct/path/file.php
```

---

## ✅ Status: FULLY DYNAMIC

The FTP deployment system now supports **all sites dynamically** with:
- ✅ Auto-detection from file paths
- ✅ Site-specific or shared credentials
- ✅ Dynamic site configuration loading
- ✅ Easy site discovery (`--list-sites`)
- ✅ Scalable to unlimited sites

**Ready for production use across all 8+ sites!**

