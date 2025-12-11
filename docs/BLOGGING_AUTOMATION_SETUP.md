# Blogging Automation Setup Guide

**Date**: 2025-12-11  
**Author**: Agent-2 (Architecture & Design Specialist)

---

## 🚀 **QUICK START**

### **Step 1: Create WordPress Application Passwords**

For each WordPress site, create an Application Password:

1. Log into WordPress admin (e.g., `https://yoursite.com/wp-admin`)
2. Go to **Users → Profile**
3. Scroll to **Application Passwords** section
4. Enter a name (e.g., "Blogging Automation")
5. Click **Add New Application Password**
6. Copy the generated password (you won't see it again!)

### **Step 2: Create Configuration File**

Copy the example configuration:

```bash
cp .deploy_credentials/blogging_api.json.example .deploy_credentials/blogging_api.json
```

Edit `.deploy_credentials/blogging_api.json` and fill in:
- `username`: Your WordPress username
- `app_password`: The application password from Step 1

### **Step 3: Test API Connectivity**

```bash
python tools/unified_blogging_automation.py \
  --site freerideinvestor \
  --title "Test Post" \
  --content "This is a test" \
  --purpose trading_education \
  --status draft \
  --dry-run
```

### **Step 4: Publish Your First Post**

```bash
python tools/unified_blogging_automation.py \
  --site freerideinvestor \
  --title "Trading Strategy: [Your Title]" \
  --content templates/blogging/trading_education.md \
  --purpose trading_education \
  --status publish
```

---

## 📋 **SITE CONFIGURATION**

### **freerideinvestor.com**
- **Purpose**: Trading Education
- **Categories**: Trading Education, Market Analysis
- **Tags**: trading, education, analysis
- **Status**: ⚠️ HTTP 500 error - needs fix first

### **prismblossom.online**
- **Purpose**: Personal Updates
- **Categories**: Personal
- **Tags**: personal, update
- **Status**: ✅ Operational

### **weareswarm.online**
- **Purpose**: Swarm System Updates
- **Categories**: System Updates, Architecture
- **Tags**: swarm, system, updates
- **Status**: ✅ Operational

### **weareswarm.site**
- **Purpose**: Swarm System Updates (mirror)
- **Categories**: System Updates, Architecture
- **Tags**: swarm, system, updates
- **Status**: ✅ Operational

### **tradingrobotplug.com**
- **Purpose**: Plugin Updates
- **Categories**: Plugin Updates, Changelog
- **Tags**: plugin, update, changelog
- **Status**: ✅ Operational

### **southwestsecret.com**
- **Purpose**: Music Releases
- **Categories**: Music, Releases
- **Tags**: music, release, dj
- **Status**: ⚠️ WordPress theme needs deployment first

---

## 🔧 **ADVANCED USAGE**

### **Publish to All Sites**

```bash
python tools/unified_blogging_automation.py \
  --all-sites \
  --title "System Update" \
  --content "Update content here" \
  --status draft
```

### **Content Adaptation**

The tool automatically adapts content based on site purpose:

- **Raw**: "New feature X released"
- **weareswarm.online**: Technical deep-dive with architecture details
- **freerideinvestor.com**: Trading application of feature X
- **tradingrobotplug.com**: Plugin integration guide

### **Scheduled Publishing**

Posts can be created as drafts and scheduled via WordPress admin, or use WordPress REST API scheduling endpoints (future enhancement).

---

## 🛠️ **TROUBLESHOOTING**

### **Authentication Failed**
- Verify application password is correct
- Ensure username matches WordPress admin username
- Check that Application Password feature is enabled

### **Permission Denied**
- Ensure user has Administrator role
- Check that `DISALLOW_FILE_EDIT` is not set in wp-config.php
- Verify REST API is enabled (should be by default)

### **API Not Available**
- Check site URL is correct
- Verify WordPress REST API: `https://yoursite.com/wp-json/`
- Check for security plugins blocking REST API

---

## 📊 **INTEGRATION POINTS**

### **Devlog System**
- Auto-post devlogs to weareswarm.online
- Integration: `tools/devlog_manager.py` → `tools/unified_blogging_automation.py`

### **Swarm Brain**
- Archive all blog posts
- Search content across sites
- Track engagement metrics

### **Discord**
- Auto-share posts to relevant channels
- Notifications for published posts

---

## 🎯 **NEXT STEPS**

1. ✅ Tool created (`tools/unified_blogging_automation.py`)
2. ✅ Templates created (`templates/blogging/`)
3. ⏳ Configuration file setup (requires WordPress credentials)
4. ⏳ API connectivity testing
5. ⏳ Integration with devlog system
6. ⏳ Discord auto-sharing

---

**Status**: ✅ **TOOL READY** - Awaiting WordPress credentials for configuration

🐝 **WE. ARE. SWARM. ⚡🔥**

