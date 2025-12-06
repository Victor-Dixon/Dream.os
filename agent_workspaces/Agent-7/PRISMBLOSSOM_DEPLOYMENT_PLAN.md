# prismblossom.online Deployment Plan
**Date**: 2025-01-27  
**Based on**: freerideinvestor deployment process documentation  
**Status**: Ready to deploy when credentials available

---

## 🎯 Deployment Objective

Deploy 4 WordPress page templates to `prismblossom.online`:
1. `page-invitation.php` - Birthday Invitation page (black & gold theme)
2. `page-guestbook.php` - Guestbook page (with placeholders)
3. `page-birthday-fun.php` - Birthday Fun page (interactive features)
4. `page-birthday-blog.php` - Blog post template

---

## 📋 Deployment Process (From freerideinvestor Pattern)

### Step 1: Verify Configuration
- ✅ `prismblossom` already in `SITE_CONFIGS`
- ✅ Local path: `D:/websites/prismblossom.online`
- ✅ Theme name: `prismblossom`
- ✅ Remote path: `/public_html/wp-content/themes/prismblossom`

### Step 2: Credential Access
- Uses **shared Hostinger environment variables** (same as freerideinvestor)
- Environment variables checked:
  - `HOSTINGER_HOST` or `SSH_HOST`
  - `HOSTINGER_USER` or `SSH_USER`
  - `HOSTINGER_PASS` or `SSH_PASS`
  - `HOSTINGER_PORT` or `SSH_PORT` (default: 65002)
- Falls back to `sites.json` if env vars not set

### Step 3: Deployment Script
```python
from tools.wordpress_manager import WordPressManager
from pathlib import Path

manager = WordPressManager("prismblossom")

files_to_deploy = [
    Path("D:/websites/prismblossom.online/wordpress-theme/prismblossom/page-invitation.php"),
    Path("D:/websites/prismblossom.online/wordpress-theme/prismblossom/page-guestbook.php"),
    Path("D:/websites/prismblossom.online/wordpress-theme/prismblossom/page-birthday-fun.php"),
    Path("D:/websites/prismblossom.online/wordpress-theme/prismblossom/page-birthday-blog.php")
]

if manager.connect():
    for file_path in files_to_deploy:
        manager.deploy_file(file_path)
    manager.disconnect()
```

### Step 4: Verification
- Check WordPress admin (pages should appear)
- Check frontend (pages should render correctly)
- Verify black & gold theme applied
- Test interactive features on Birthday Fun page

---

## 🔑 Key Learnings from freerideinvestor

1. **Shared Credentials**: All Hostinger sites use same env vars
2. **Port 65002**: Standard Hostinger SSH port (not 22)
3. **Same Process**: Identical deployment method for all Hostinger sites
4. **Automated**: No human interaction needed once credentials set

---

## 📝 Deployment Checklist

- [ ] Verify credentials available (env vars or sites.json)
- [ ] Confirm all 4 files exist locally
- [ ] Run deployment script
- [ ] Verify files deployed successfully
- [ ] Test pages on live site
- [ ] Confirm theme colors (black & gold)
- [ ] Test interactive features
- [ ] Post devlog to Discord

---

**Status**: 📝 **PLAN READY** - Deployment process documented, ready to execute when credentials available

---

*Documented by Agent-7* 🐝⚡







