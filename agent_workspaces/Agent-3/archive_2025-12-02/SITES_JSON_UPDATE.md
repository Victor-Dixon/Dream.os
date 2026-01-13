# Sites.json Update - AriaJet Configuration

**Date**: 2025-12-02  
**Status**: ✅ **UPDATED**

---

## ✅ **CHANGES MADE**

### **AriaJet Entries Fixed**

**Before**:
- `remote_path`: `/public_html` ❌ (incorrect)

**After**:
- `remote_path`: `/public_html/wp-content/themes/ariajet` ✅ (correct)
- `port`: `21` (FTP, added for consistency)

---

## 📋 **UPDATED CONFIGURATION**

```json
{
  "ariajet": {
    "host": "",
    "username": "",
    "password": "",
    "port": 21,
    "remote_path": "/public_html/wp-content/themes/ariajet"
  },
  "ariajet.site": {
    "host": "",
    "username": "",
    "password": "",
    "port": 21,
    "remote_path": "/public_html/wp-content/themes/ariajet"
  },
  "prismblossom": {
    "host": "",
    "username": "",
    "password": "",
    "port": 22,
    "remote_path": "/public_html/wp-content/themes/prismblossom"
  },
  "prismblossom.online": {
    "host": "",
    "username": "",
    "password": "",
    "port": 22,
    "remote_path": "/public_html/wp-content/themes/prismblossom"
  }
}
```

---

## 🔧 **NEXT STEPS**

To add credentials for ariajet.site:

1. **Get FTP credentials from Hostinger**:
   - Navigate to Hostinger control panel
   - Find ariajet.site domain
   - Get FTP account details

2. **Update sites.json**:
   ```json
   "ariajet": {
     "host": "157.173.214.121",
     "username": "u996867598.ariajet.site",
     "password": "your_password",
     "port": 21,
     "remote_path": "/public_html/wp-content/themes/ariajet"
   }
   ```

3. **Or use shared credentials**:
   - If ariajet.site uses same server as freerideinvestor.com
   - Can use `.env` credentials (HOSTINGER_HOST, HOSTINGER_USER, etc.)
   - FTP deployer will fall back to `.env` if site-specific credentials are empty

---

**Status**: ✅ **Configuration updated - Ready for credential addition**

