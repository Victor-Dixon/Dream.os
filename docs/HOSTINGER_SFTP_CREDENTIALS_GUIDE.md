# Hostinger SFTP Credentials Guide

**Status:** ✅ **YES - We have tools to get SFTP credentials from Hostinger**

## Tools Available

### 1. **Hostinger API Helper** (Automated)
**File:** `tools/hostinger_api_helper.py`

**What it does:**
- Uses Hostinger API to automatically discover SFTP credentials
- Fetches FTP/SFTP info for domains
- Updates `.env` file with credentials
- Lists all domains in your account

**Requirements:**
- `HOSTINGER_API_KEY` in `.env` file
- Hostinger API access enabled

**Usage:**
```bash
# List all domains
python tools/hostinger_api_helper.py --list-domains

# Discover credentials for a specific domain
python tools/hostinger_api_helper.py --domain freerideinvestor.com --update-env

# Discover without updating .env (dry run)
python tools/hostinger_api_helper.py --domain houstonsipqueen.com
```

### 2. **Discover FTP Credentials** (Manual Guide)
**File:** `tools/discover_ftp_credentials.py`

**What it does:**
- Shows step-by-step guide for finding FTP credentials manually
- Lists sites needing credentials
- Generates direct links to Hostinger FTP pages
- Tests credentials

**Usage:**
```bash
# Show full guide
python tools/discover_ftp_credentials.py

# Show credential status for all sites
python tools/discover_ftp_credentials.py --status

# Generate Hostinger FTP links
python tools/discover_ftp_credentials.py --links

# Test credentials
python tools/discover_ftp_credentials.py --test mysite.com --host 157.173.214.121 --username u123456 --password mypass --port 65002
```

## Quick Start

### Option A: Automated (API)
1. **Get Hostinger API Key:**
   - Log into Hostinger: https://hpanel.hostinger.com/
   - Go to API section
   - Generate API key
   - Add to `.env`: `HOSTINGER_API_KEY=your_key_here`

2. **Discover credentials:**
   ```bash
   python tools/hostinger_api_helper.py --list-domains
   python tools/hostinger_api_helper.py --domain yoursite.com --update-env
   ```

3. **Update sites.json:**
   - Credentials will be in `.env` file
   - Copy to `.deploy_credentials/sites.json` for site-specific config

### Option B: Manual (Control Panel)
1. **Follow the guide:**
   ```bash
   python tools/discover_ftp_credentials.py --guide
   ```

2. **Get credentials from Hostinger:**
   - Log into: https://hpanel.hostinger.com/
   - Click "Websites" → Your domain → "Tools" → "FTP Account"
   - Copy: Host, Username, Password, Port

3. **Add to sites.json:**
   ```json
   {
     "yoursite.com": {
       "host": "157.173.214.121",
       "username": "u123456.yoursite.com",
       "password": "your_password",
       "port": 65002
     }
   }
   ```

## Credential Format

**For `.deploy_credentials/sites.json`:**
```json
{
  "houstonsipqueen.com": {
    "host": "157.173.214.121",
    "username": "u996867598.houstonsipqueen.com",
    "password": "your_sftp_password",
    "port": 65002,
    "remote_base": "domains/houstonsipqueen.com/public_html/wp-content/themes/houstonsipqueen"
  }
}
```

**Common Hostinger Values:**
- **Host:** Usually `157.173.214.121` or `ftp.hostinger.com`
- **Port:** `65002` (SFTP) or `21` (FTP)
- **Username:** Format `u{account_id}.{domain}` (e.g., `u996867598.freerideinvestor.com`)
- **Password:** Set in Hostinger control panel

## What Gets Discovered

The Hostinger API helper discovers:
- ✅ **Host** - SFTP server address
- ✅ **Port** - SFTP port (usually 65002)
- ⚠️ **Username** - May need manual lookup
- ⚠️ **Password** - Not in API (use existing or reset in Hostinger)

## Next Steps After Getting Credentials

1. **Test connection:**
   ```bash
   python tools/discover_ftp_credentials.py --test yoursite.com --host 157.173.214.121 --username u123 --password pass --port 65002
   ```

2. **Add to sites.json:**
   - Create/update `.deploy_credentials/sites.json`
   - Add credentials for each site

3. **Use WordPressManager:**
   ```python
   from tools.wordpress_manager import WordPressManager
   manager = WordPressManager("yoursite.com")
   manager.connect()  # Uses credentials from sites.json
   ```

## Troubleshooting

**API Key Issues:**
- Verify `HOSTINGER_API_KEY` in `.env`
- Check API key has proper permissions
- Try manual method if API fails

**Connection Issues:**
- Verify port (65002 for SFTP, 21 for FTP)
- Check username format (usually `u{id}.{domain}`)
- Test credentials manually first

**Missing Credentials:**
- Use `discover_ftp_credentials.py --guide` for manual steps
- Check Hostinger control panel directly
- Verify domain is in your Hostinger account

---

**TL;DR:** Use `hostinger_api_helper.py` with API key for automated discovery, or `discover_ftp_credentials.py` for manual guide. 🐝




