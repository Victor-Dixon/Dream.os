# 🔑 How to Get SFTP Credentials (30 seconds)

## **Step 1: Log into Hostinger**
👉 https://hpanel.hostinger.com/

## **Step 2: Get Credentials**
1. Click **Files** → **FTP Accounts**
2. Find your domain
3. Copy these 4 values:
   - **FTP Username** (not your email!)
   - **FTP Password** (click "Show" or reset if needed)
   - **FTP Host** (IP address)
   - **FTP Port** (should be `65002`)

## **Step 3: Add to .env File**
Open `.env` in repository root, add:
```env
HOSTINGER_HOST=157.173.214.121
HOSTINGER_USER=your_username_here
HOSTINGER_PASS=your_password_here
HOSTINGER_PORT=65002
```

## **Step 4: Test**
```bash
python tools/sftp_credential_troubleshooter.py
```

✅ **Done!** Credentials are now ready to use.

---

**💡 Tip**: Username might be different from your email (check Hostinger exactly as shown)

**🐝 WE. ARE. SWARM. ⚡🔥**

