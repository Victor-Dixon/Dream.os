# WordPress Application Password Setup Guide

**Date**: 2025-12-11  
**Author**: Agent-2 (Architecture & Design Specialist)

---

## 🎯 **PURPOSE**

This guide provides step-by-step instructions for creating Application Passwords for WordPress sites to enable REST API authentication for the blogging automation tool.

---

## 📋 **REQUIREMENTS**

- Administrator access to WordPress admin panel
- WordPress 5.6+ (Application Passwords feature)
- Access to all 6 WordPress sites

---

## 🚀 **STEP-BY-STEP INSTRUCTIONS**

### **For Each WordPress Site:**

#### **1. Log into WordPress Admin**
- Navigate to: `https://yoursite.com/wp-admin`
- Log in with your administrator account

#### **2. Navigate to Profile**
- Click **Users** in the left sidebar
- Click **Profile** (or your username)

#### **3. Find Application Passwords Section**
- Scroll down to the **Application Passwords** section
- Located near the bottom of the profile page

#### **4. Create New Application Password**
- Enter a descriptive name: `Blogging Automation` (or similar)
- Click **Add New Application Password**
- **IMPORTANT**: Copy the generated password immediately!
  - Format: `xxxx xxxx xxxx xxxx xxxx xxxx` (24 characters with spaces)
  - You won't be able to see it again after leaving the page
  - Remove spaces when using in config file

#### **5. Save Credentials Securely**
- Store the password securely (password manager recommended)
- Add to `.deploy_credentials/blogging_api.json`

---

## 📝 **SITES TO CONFIGURE**

Configure Application Passwords for these 6 sites:

1. **freerideinvestor.com**
   - URL: `https://freerideinvestor.com/wp-admin`
   - Purpose: Trading education content

2. **prismblossom.online**
   - URL: `https://prismblossom.online/wp-admin`
   - Purpose: Personal updates

3. **weareswarm.online**
   - URL: `https://weareswarm.online/wp-admin`
   - Purpose: Swarm system updates

4. **weareswarm.site**
   - URL: `https://weareswarm.site/wp-admin`
   - Purpose: Swarm system updates (mirror)

5. **tradingrobotplug.com**
   - URL: `https://tradingrobotplug.com/wp-admin`
   - Purpose: Plugin updates

6. **southwestsecret.com**
   - URL: `https://southwestsecret.com/wp-admin`
   - Purpose: Music releases
   - **Note**: WordPress theme needs deployment first

---

## ⚙️ **CONFIGURATION FILE**

After creating Application Passwords, update:

**File**: `.deploy_credentials/blogging_api.json`

**For each site, replace**:
```json
{
  "site_id": {
    "username": "REPLACE_WITH_WORDPRESS_USERNAME",
    "app_password": "REPLACE_WITH_APPLICATION_PASSWORD"
  }
}
```

**Example**:
```json
{
  "weareswarm.online": {
    "site_url": "https://weareswarm.online",
    "username": "admin",
    "app_password": "abcd1234efgh5678ijkl9012",
    "purpose": "swarm_system",
    "categories": ["System Updates", "Architecture"],
    "default_tags": ["swarm", "system", "updates"]
  }
}
```

**Important Notes**:
- Remove spaces from the Application Password
- Username is case-sensitive
- Each site can use different credentials
- Keep this file secure (it's in `.deploy_credentials/` which should be gitignored)

---

## ✅ **VERIFICATION**

After configuring credentials, test connectivity:

```bash
# Test all sites
python tools/test_blogging_api_connectivity.py

# Test specific site
python tools/test_blogging_api_connectivity.py --site weareswarm.online
```

Expected output for successful configuration:
```
🔍 Testing weareswarm.online (https://weareswarm.online)...
   ✅ REST API: Available (WP 6.4.2)
   ✅ Authentication: Success (User: Admin, Role: administrator)
   ✅ weareswarm.online: FULLY OPERATIONAL
```

---

## 🛠️ **TROUBLESHOOTING**

### **Application Passwords Section Not Visible**
- Ensure WordPress version is 5.6 or higher
- Check that you're logged in as Administrator
- Verify the feature isn't disabled by a plugin

### **Authentication Fails**
- Verify username is correct (case-sensitive)
- Ensure Application Password has no spaces
- Check that the password was copied completely (24 characters)
- Verify user has Administrator role

### **REST API Not Available**
- Test REST API endpoint: `https://yoursite.com/wp-json/`
- Check for security plugins blocking REST API
- Verify WordPress is properly installed

### **Permission Denied**
- Ensure user has Administrator role
- Check that REST API is enabled (default in WordPress)
- Verify no security plugins are blocking API access

---

## 🔒 **SECURITY NOTES**

1. **Application Passwords are site-specific**
   - Each WordPress site needs its own Application Password
   - Passwords cannot be reused across sites

2. **Revoke if compromised**
   - If a password is compromised, revoke it in WordPress admin
   - Create a new Application Password
   - Update `.deploy_credentials/blogging_api.json`

3. **File Security**
   - `.deploy_credentials/blogging_api.json` should be in `.gitignore`
   - Never commit credentials to version control
   - Use secure storage for backup copies

4. **Best Practices**
   - Use descriptive names for Application Passwords
   - Revoke unused Application Passwords regularly
   - Monitor API access logs in WordPress

---

## 📊 **QUICK REFERENCE**

| Site | Admin URL | Status |
|------|-----------|--------|
| freerideinvestor.com | `/wp-admin` | ⚠️ HTTP 500 (needs fix) |
| prismblossom.online | `/wp-admin` | ✅ Operational |
| weareswarm.online | `/wp-admin` | ✅ Operational |
| weareswarm.site | `/wp-admin` | ✅ Operational |
| tradingrobotplug.com | `/wp-admin` | ✅ Operational |
| southwestsecret.com | `/wp-admin` | ⚠️ Theme deployment needed |

---

**Status**: 📋 **READY FOR SETUP** - Follow steps above to configure all sites

🐝 **WE. ARE. SWARM. ⚡🔥**
