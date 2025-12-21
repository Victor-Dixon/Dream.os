# Hostinger API Key Setup Guide

## How to Get Hostinger API Key

### Step 1: Log into Hostinger
1. Go to: https://hpanel.hostinger.com/
2. Log in with your Hostinger account credentials

### Step 2: Navigate to API Section
1. Look for **"API"** or **"Developer"** section in the control panel
2. Or go directly to: https://developers.hostinger.com/
3. You may need to enable API access first

### Step 3: Generate API Key
1. Click **"Create API Key"** or **"Generate Key"**
2. Give it a name (e.g., "Agent Cellphone V2")
3. Set permissions (at minimum: read access to hosting/FTP info)
4. Copy the API key (you'll only see it once!)

### Step 4: Add to .env File
1. Open `.env` file in repository root
2. Add this line:
   ```
   HOSTINGER_API_KEY=your_api_key_here
   ```
3. Save the file

### Alternative: Set as Environment Variable
```bash
# Windows PowerShell
$env:HOSTINGER_API_KEY="your_api_key_here"

# Windows CMD
set HOSTINGER_API_KEY=your_api_key_here

# Linux/Mac
export HOSTINGER_API_KEY=your_api_key_here
```

## Verify API Key Works

```bash
# Test API connection
python tools/hostinger_api_helper.py --list-domains
```

If successful, you'll see a list of all your domains.

## Troubleshooting

**"HOSTINGER_API_KEY not set" error:**
- Verify the key is in `.env` file
- Check for typos (no spaces around `=`)
- Restart terminal/IDE after adding to `.env`

**"API request failed" or "403 Forbidden":**
- Verify API key is correct
- Check API key has proper permissions
- Try regenerating the key

**"No domains found":**
- API key may not have domain listing permissions
- Try discovering credentials for a specific domain instead

## Next Steps

Once API key is set:
1. List domains: `python tools/hostinger_api_helper.py --list-domains`
2. Discover credentials: `python tools/hostinger_api_helper.py --domain yoursite.com --update-env`
3. Credentials will be saved to `.env` file
4. Copy to `sites.json` for site-specific config

---

**Note:** If you can't find the API section, you may need to:
- Contact Hostinger support to enable API access
- Use Option B (manual method) instead
- Check Hostinger documentation for API setup





