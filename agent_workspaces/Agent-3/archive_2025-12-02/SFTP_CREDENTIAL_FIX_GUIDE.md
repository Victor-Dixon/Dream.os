# SFTP Credential Fix Guide - Agent-3

**Date**: 2025-12-02  
**Site**: freerideinvestor.com  
**Status**: 🔧 **CREDENTIALS NEED FIXING**

---

## 🔍 **CURRENT STATUS**

### **Current Credentials** (from .env):
- **Host**: `157.173.214.121` ✅ (discovered via Hostinger API)
- **Port**: `65002` ✅ (correct for Hostinger SFTP)
- **Username**: `dadudekc` ⚠️ (may be incorrect format)
- **Password**: `[12 characters]` ⚠️ (authentication failing)

### **Test Results**:
- ❌ All credential variations failed
- ✅ Server reachable (OpenSSH_8.7)
- ❌ Authentication failed for all username/password combinations

---

## 🔧 **HOW TO FIX SFTP CREDENTIALS**

### **Step 1: Log into Hostinger Control Panel**

1. Go to: https://hpanel.hostinger.com/
2. Log in with your Hostinger account credentials

### **Step 2: Find SFTP Credentials**

**Option A: FTP Accounts (Recommended)**
1. Navigate to: **Files** → **FTP Accounts**
2. Look for your domain: `freerideinvestor.com`
3. Find the SFTP account details:
   - **FTP Username** (this is what you need - may be different from email)
   - **FTP Password** (may need to reset if forgotten)
   - **FTP Host** (should match `157.173.214.121` or similar)
   - **FTP Port** (should be `65002` for SFTP)

**Option B: File Manager**
1. Navigate to: **Files** → **File Manager**
2. Look for SFTP/FTP connection details in the interface

**Option C: Hosting Settings**
1. Navigate to: **Hosting** → **Manage** → **Your Domain**
2. Look for **FTP/SFTP** section
3. Find connection details

### **Step 3: Verify SFTP is Enabled**

1. Check if SFTP is enabled for your account
2. Some Hostinger plans may only have FTP (not SFTP)
3. If SFTP is not available, we'll need to use FTP or WordPress Admin method

### **Step 4: Get Correct Username Format**

**Common Hostinger Username Formats**:
- `cpanel_username` (cPanel username, not email)
- `u1234567` (numeric prefix)
- `username@domain.com` (email format - less common)
- `domain_username` (domain-based)

**Important**: The username might be different from your Hostinger login email!

### **Step 5: Reset Password (If Needed)**

1. In **FTP Accounts**, find your SFTP account
2. Click **Reset Password** or **Change Password**
3. Generate a new password
4. **Save the password immediately** (you won't see it again)

---

## 📝 **UPDATE .ENV FILE**

Once you have the correct credentials:

1. **Open**: `.env` file in the repository root
2. **Update** these lines:
   ```env
   HOSTINGER_HOST=157.173.214.121
   HOSTINGER_USER=[CORRECT_USERNAME_FROM_HOSTINGER]
   HOSTINGER_PASS=[CORRECT_PASSWORD_FROM_HOSTINGER]
   HOSTINGER_PORT=65002
   ```
3. **Save** the file

---

## ✅ **TEST CONNECTION**

After updating credentials, test the connection:

```bash
python tools/sftp_credential_troubleshooter.py --save-report
```

**Expected Result**: ✅ Connection successful!

---

## 🚀 **DEPLOY AFTER FIX**

Once credentials are fixed:

```bash
python tools/wordpress_manager.py --site freerideinvestor --deploy
```

Or deploy specific file:

```bash
python tools/wordpress_manager.py --site freerideinvestor --deploy-file D:/websites/FreeRideInvestor/functions.php
```

---

## 🔍 **TROUBLESHOOTING**

### **If Username Still Wrong**:
- Try the cPanel username (different from Hostinger login)
- Check if username needs domain suffix
- Verify in Hostinger control panel exactly what username format is shown

### **If Password Still Wrong**:
- Reset password in Hostinger control panel
- Make sure no special characters are being escaped incorrectly
- Copy password directly from Hostinger (don't retype)

### **If SFTP Not Available**:
- Use FTP instead (port 21, different protocol)
- Or use WordPress Admin automation method
- Or use Hostinger File Manager (web-based)

---

## 📋 **CHECKLIST**

- [ ] Logged into Hostinger control panel
- [ ] Found FTP/SFTP account section
- [ ] Identified correct username format
- [ ] Verified/reset password
- [ ] Updated .env file with correct credentials
- [ ] Tested connection with troubleshooter tool
- [ ] Connection successful ✅
- [ ] Ready to deploy

---

**Created By**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-12-02

🐝 **WE. ARE. SWARM. ⚡🔥**

