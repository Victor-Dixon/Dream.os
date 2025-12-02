# SFTP/FTP Credentials Found - freerideinvestor.com

**Date**: 2025-12-02  
**Source**: Hostinger Control Panel (FTP Accounts page)

## ✅ Correct Credentials

| Field | Value |
|-------|-------|
| **Host** | `157.173.214.121` |
| **Port** | `21` |
| **Username** | `u996867598.freerideinvestor.com` |
| **Password** | *Not displayed* (use "Change FTP password" to reset) |
| **Upload Folder** | `public_html` |

## ❌ Previous Incorrect Values

| Field | Incorrect Value | Correct Value |
|-------|----------------|--------------|
| **Username** | `dadudekc` | `u996867598.freerideinvestor.com` |
| **Port** | `65002` | `21` |

## 🔧 Next Steps

1. **Update `.env` file** with correct credentials:
   ```
   HOSTINGER_HOST=157.173.214.121
   HOSTINGER_PORT=21
   HOSTINGER_USERNAME=u996867598.freerideinvestor.com
   HOSTINGER_PASSWORD=<current password or reset via Hostinger>
   ```

2. **If password is unknown**: Click "Change FTP password" button in Hostinger control panel to reset it.

3. **Test SFTP connection** with corrected credentials using `tools/sftp_credential_troubleshooter.py`.

4. **Deploy via SFTP** once connection is verified.

## 📍 Hostinger Control Panel Location

- **URL**: https://hpanel.hostinger.com/websites/freerideinvestor.com/files/ftp-accounts
- **Navigation**: Websites → freerideinvestor.com → Tool → FTP Account

## 📝 Notes

- The username format is `u{account_id}.{domain}` (not the email prefix).
- Standard FTP port is `21` (not `65002`).
- Password is not displayed for security reasons - must be reset if unknown.

