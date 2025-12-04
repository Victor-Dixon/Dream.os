# FTP/SFTP Credentials Discovery Guide

**Date**: 2025-12-02  
**Purpose**: How to find and verify FTP credentials for all sites

---

## 🔍 **HOW TO GET FTP CREDENTIALS FROM HOSTINGER**

### **Step 1: Log into Hostinger Control Panel**

👉 **https://hpanel.hostinger.com/**

---

### **Step 2: Navigate to FTP Accounts**

For **EACH domain**, follow these steps:

1. Click **"Websites"** in the left menu
2. Find your domain (e.g., `ariajet.site`, `freerideinvestor.com`)
3. Click on the **domain name**
4. Click **"Tools"** tab
5. Click **"FTP Account"** or **"FTP Accounts"**

---

### **Step 3: Find Credentials**

On the FTP Account page, you'll see:

- **FTP Host** (e.g., `157.173.214.121`)
- **FTP Port** (usually `21` for FTP, `22` for SFTP)
- **FTP Username** (format: `u{id}.{domain}`)
- **FTP Password** (click "Show" or "Change" to see/reset)

---

## 📋 **CREDENTIAL FORMATS**

### **Host Address**
- Usually: `157.173.214.121` (shared hosting IP)
- Sometimes: `ftp.{domain}` or just `{domain}`
- Check the exact value in Hostinger FTP Account page

### **Port Numbers**
- **Port 21** = Standard FTP (most common)
- **Port 22** = SFTP (Secure FTP)
- **Port 65002** = Hostinger SFTP (alternative)

### **Username Formats**
Common Hostinger formats:
- `u{account_id}.{domain}` (e.g., `u996867598.freerideinvestor.com`)
- `{cpanel_username}` (cPanel username)
- `{email_prefix}` (less common)

### **Password**
- Not displayed for security
- Click **"Change FTP password"** to reset if needed
- Use a strong password

---

## 🔗 **DIRECT LINKS TO FTP PAGES**

For each site, navigate to:

**Base URL Pattern**: `https://hpanel.hostinger.com/websites/{domain}/files/ftp-accounts`

**Example Links**:
- `ariajet.site`: https://hpanel.hostinger.com/websites/ariajet.site/files/ftp-accounts
- `freerideinvestor.com`: https://hpanel.hostinger.com/websites/freerideinvestor.com/files/ftp-accounts
- `prismblossom.online`: https://hpanel.hostinger.com/websites/prismblossom.online/files/ftp-accounts
- `southwestsecret.com`: https://hpanel.hostinger.com/websites/southwestsecret.com/files/ftp-accounts
- `tradingrobotplug.com`: https://hpanel.hostinger.com/websites/tradingrobotplug.com/files/ftp-accounts
- `weareswarm.site`: https://hpanel.hostinger.com/websites/weareswarm.site/files/ftp-accounts
- `dadudekc.com`: https://hpanel.hostinger.com/websites/dadudekc.com/files/ftp-accounts

---

## 🛠️ **USING THE DISCOVERY TOOL**

### **Check Status of All Sites**

```bash
python tools/discover_ftp_credentials.py --status
```

Shows which sites have credentials and which need them.

### **Show Discovery Guide**

```bash
python tools/discover_ftp_credentials.py --guide
```

### **Generate Hostinger Links**

```bash
python tools/discover_ftp_credentials.py --links
```

### **Test Credentials Before Adding**

```bash
python tools/discover_ftp_credentials.py --test ariajet.site \
  --host 157.173.214.121 \
  --username u996867598.ariajet.site \
  --password your_password \
  --port 21
```

---

## 📝 **UPDATING sites.json**

Once you have credentials:

1. Open `.deploy_credentials/sites.json`
2. Find the site entry
3. Update the fields:
   ```json
   "ariajet.site": {
     "host": "157.173.214.121",
     "username": "u996867598.ariajet.site",
     "password": "your_actual_password",
     "port": 21,
     "remote_path": "/public_html/wp-content/themes/ariajet"
   }
   ```
4. Save the file
5. Test with: `python tools/discover_ftp_credentials.py --test ariajet.site --host ... --username ... --password ... --port 21`

---

## ⚠️ **IMPORTANT NOTES**

1. **Same Server, Different Domains**: If multiple domains are on the same Hostinger account, they might share the same FTP host and username format
2. **Password Security**: Never commit passwords to git. Keep `sites.json` in `.gitignore` or use environment variables
3. **Port Selection**: Use port `21` for FTP, `22` for SFTP. Check Hostinger to confirm which is enabled
4. **Username Format**: The username format can vary. Always check the exact value in Hostinger

---

## ✅ **VERIFICATION CHECKLIST**

For each site, verify:
- [ ] Host address is correct (IP or domain)
- [ ] Port matches FTP type (21 for FTP, 22 for SFTP)
- [ ] Username format matches Hostinger display
- [ ] Password is correct (test connection)
- [ ] Remote path is correct (`/public_html/wp-content/themes/{theme_name}`)

---

**Tool**: `python tools/discover_ftp_credentials.py` - Run without arguments to see all information

