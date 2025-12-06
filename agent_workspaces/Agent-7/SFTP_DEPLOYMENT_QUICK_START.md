# SFTP/SSH Deployment - Quick Start Guide

**Method**: Direct SFTP/SSH file upload  
**Tool**: `tools/wordpress_manager.py` or `tools/deploy_via_sftp.py`  
**Status**: ✅ **This is the method we've used successfully before**

---

## 🚀 **QUICK DEPLOYMENT**

### **Simple Command**:

```bash
python tools/deploy_via_sftp.py \
  --site freerideinvestor \
  --file D:/websites/FreeRideInvestor/functions.php
```

### **Or Use WordPress Manager Directly**:

```bash
python -m tools.wordpress_manager \
  --site freerideinvestor \
  --deploy-file functions.php
```

---

## 🔧 **CREDENTIALS SETUP**

### **Option 1: Site-Specific (Recommended)**

**File**: `.deploy_credentials/sites.json`

```json
{
  "freerideinvestor": {
    "host": "157.173.214.121",
    "username": "dadudekc",
    "password": "your_password_here",
    "port": 65002
  },
  "prismblossom.online": {
    "host": "your_host_ip",
    "username": "your_username",
    "password": "your_password",
    "port": 65002
  }
}
```

### **Option 2: Global .env File**

**File**: `.env`

```env
HOSTINGER_HOST=157.173.214.121
HOSTINGER_USER=dadudekc
HOSTINGER_PASS=your_password_here
HOSTINGER_PORT=65002
```

---

## ✅ **ADVANTAGES**

- ✅ **No plugins needed** - works on any WordPress site
- ✅ **Direct file upload** - fastest method
- ✅ **Fully automated** - no browser or manual steps
- ✅ **Proven method** - we've deployed successfully before
- ✅ **No WordPress admin access needed** - only SFTP/SSH

---

## 📋 **DEPLOYMENT STEPS**

1. **Configure Credentials**:
   - Add credentials to `.deploy_credentials/sites.json` or `.env`

2. **Deploy File**:
   ```bash
   python tools/deploy_via_sftp.py \
     --site freerideinvestor \
     --file D:/websites/FreeRideInvestor/functions.php
   ```

3. **Verify**:
   - Check file on server
   - Test website functionality

---

## 🐛 **TROUBLESHOOTING**

### **Error: "No credentials available"**

**Solution**: Add credentials to `.deploy_credentials/sites.json` or `.env`

### **Error: "Connection failed"**

**Check**:
- Host IP address is correct
- Username is correct
- Password is correct
- Port is correct (65002 for Hostinger SFTP)
- SFTP is enabled on hosting account

### **Error: "Authentication failed"**

**Try**:
- Verify password (may need special character escaping)
- Check username format (may need `u123456789` format for Hostinger)
- Verify SFTP is enabled (not just FTP)

---

## 📊 **CURRENT STATUS**

**Known Credentials**:
- ✅ Host: `157.173.214.121` (discovered)
- ✅ Username: `dadudekc` (extracted)
- ✅ Port: `65002` (set)
- ❌ Password: Needs verification or may need format adjustment

**Next Step**: Fix password or verify SFTP is enabled on Hostinger account

---

## 🎯 **USAGE EXAMPLES**

### **Deploy FreeRideInvestor functions.php**:

```bash
python tools/deploy_via_sftp.py \
  --site freerideinvestor \
  --file D:/websites/FreeRideInvestor/functions.php
```

### **Deploy prismblossom.online functions.php**:

```bash
python tools/deploy_via_sftp.py \
  --site prismblossom.online \
  --file D:/websites/prismblossom.online/wordpress-theme/prismblossom/functions.php
```

---

**This is the method we've used successfully before - no plugins needed!**

🐝 **WE. ARE. SWARM. ⚡🔥**




