# Agent Requests from Humans

**Date**: 2025-12-03  
**Status**: Active Requests

---

## 🎨 **AriaJet Theme Deployment - Aria's Work**

### **What's Done:**
- ✅ Theme files created (10 files)
- ✅ Theme deployed to server (10 files uploaded)
- ✅ Game HTML files ready (arias-wild-world.html, wildlife-adventure.html)

### **What We Need from Humans:**

#### **1. WordPress Installation Path** 🔴 CRITICAL
- **Issue**: Theme files are deployed but WordPress isn't detecting them
- **Root Cause**: Files may be in wrong WordPress installation path
- **What We Need**:
  - Confirm ariajet.site's actual WordPress installation path
  - Is it a separate WordPress install or part of a multi-site?
  - What's the correct FTP path to wp-content/themes/ for ariajet.site?
  - **Current deployment**: `/public_html/wp-content/themes/ariajet/` (may be wrong)

#### **2. WordPress REST API Credentials** 🟡 NEEDED FOR GAME POSTS
- **What We Need**:
  - WordPress username for ariajet.site
  - Application password (created in WordPress admin → Users → Your Profile → Application Passwords)
- **Add to `.env` file**:
  ```
  ARIAJET_SITE_URL=https://ariajet.site
  ARIAJET_WP_USERNAME=your_username_here
  ARIAJET_WP_APP_PASSWORD=your_app_password_here
  ```
- **Purpose**: To create game posts via REST API (Aria's Wild World, Wildlife Adventure)

#### **3. WordPress Theme Activation** 🟡 MANUAL OR CREDENTIALS
- **Option A**: Human activates theme manually in WordPress admin
- **Option B**: Provide credentials so we can activate via API/script

---

## 🔧 **General Agent Needs**

### **Discord Webhooks** ✅ MOSTLY CONFIGURED
- Agent-8 Discord webhook: ✅ Configured
- Other agents: Check if all webhooks are set in `.env`

### **FTP/SFTP Credentials** ✅ CONFIGURED
- Hostinger credentials: ✅ Set in `.env`
- May need ariajet.site-specific credentials if it's a different server

### **GitHub Access** ✅ CONFIGURED
- GitHub token: ✅ Set in `.env`
- Repository access: ✅ Working

---

## 📋 **Priority Summary**

### **HIGH PRIORITY** (Blocking Aria's Work):
1. **WordPress installation path for ariajet.site** - Need to know correct path
2. **WordPress REST API credentials** - For game post creation

### **MEDIUM PRIORITY**:
3. **Theme activation** - Can be done manually or via API if credentials provided

### **LOW PRIORITY**:
4. **Verify all Discord webhooks** - Most seem configured
5. **Check other site credentials** - If needed for future work

---

## 🎯 **Next Steps After Human Provides Info**

1. **Fix deployment path** → Redeploy theme to correct location
2. **Set up game posts** → Create WordPress posts for both games
3. **Verify theme activation** → Confirm theme is working in WordPress
4. **Test game display** → Verify games show correctly on site

---

## 📝 **How to Provide Info**

**Option 1**: Update `.env` file directly with credentials  
**Option 2**: Tell us the info and we'll update `.env`  
**Option 3**: Provide access to WordPress admin and we can create app password

---

**Last Updated**: 2025-12-03  
**Requested By**: Agent-8 (SSOT & System Integration Specialist)  
**For**: Aria (AriaJet Theme Deployment)


