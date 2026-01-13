# SFTP Credentials - Direct Links & Quick Access

**Date**: 2025-12-02  
**Site**: freerideinvestor.com  
**Status**: 🔧 **NEEDS MANUAL VERIFICATION**

---

## 🔗 **DIRECT LINKS**

### **Hostinger Control Panel**:
👉 **https://hpanel.hostinger.com/**

### **FTP Accounts Section** (Direct):
👉 **https://hpanel.hostinger.com/files/ftp-accounts**

### **File Manager** (Alternative):
👉 **https://hpanel.hostinger.com/files/file-manager**

---

## 📋 **QUICK STEPS**

1. **Click**: https://hpanel.hostinger.com/files/ftp-accounts
2. **Find**: `freerideinvestor.com` domain
3. **Copy**: FTP Username and Password
4. **Update**: `.env` file with credentials
5. **Test**: `python tools/sftp_credential_troubleshooter.py --save-report`

---

## 🔧 **CURRENT STATUS**

**API Test Results**:
- ✅ API connection working (Bearer token valid)
- ⚠️ VPS API doesn't provide shared hosting SFTP credentials
- ✅ Fallback: Using known host `157.173.214.121:65002`
- ❌ Username/Password: Must get from Hostinger control panel

**What We Know**:
- **Host**: `157.173.214.121` ✅ (confirmed)
- **Port**: `65002` ✅ (correct)
- **Username**: ❓ Need to verify in Hostinger panel
- **Password**: ❓ Need to verify/reset in Hostinger panel

---

## 📝 **UPDATE .ENV**

After getting credentials from Hostinger:

```env
HOSTINGER_HOST=157.173.214.121
HOSTINGER_USER=[USERNAME_FROM_HOSTINGER]
HOSTINGER_PASS=[PASSWORD_FROM_HOSTINGER]
HOSTINGER_PORT=65002
HOSTINGER_API_KEY=xxOVtoufulp3BCN3wj73kWNnGCqhXoGNVtyVRiG7448147b3
```

---

## 🚀 **AFTER UPDATING**

```bash
# Test connection
python tools/sftp_credential_troubleshooter.py --save-report

# Deploy
python tools/wordpress_manager.py --site freerideinvestor --deploy-file D:/websites/FreeRideInvestor/functions.php
```

---

**Main Link**: **https://hpanel.hostinger.com/files/ftp-accounts**

🐝 **WE. ARE. SWARM. ⚡🔥**

