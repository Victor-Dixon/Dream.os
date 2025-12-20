# SMTP Configuration Guide

**Author**: Agent-8 (SSOT & System Integration Specialist)  
**Date**: 2025-12-20

## Quick Setup

### 1. Copy Environment Template
```bash
cd trading_robot
cp env.example .env
```

### 2. Edit .env File
Add your SMTP credentials:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@tradingrobotplug.com
FROM_NAME=Trading Robot Team
```

### 3. Test Configuration
```bash
python trading_robot/email_campaigns/run_campaigns.py
```

---

## Gmail Setup (Recommended for Testing)

### Step 1: Enable 2-Step Verification
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled

### Step 2: Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Other (Custom name)"
3. Enter "Trading Robot Campaigns"
4. Click "Generate"
5. Copy the 16-character password (no spaces)

### Step 3: Configure .env
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # Use the 16-char password
FROM_EMAIL=your-email@gmail.com  # Must match SMTP_USER for Gmail
FROM_NAME=Trading Robot Team
```

---

## SendGrid Setup (Recommended for Production)

### Step 1: Create SendGrid Account
1. Sign up at [SendGrid](https://sendgrid.com)
2. Verify your email address

### Step 2: Create API Key
1. Go to Settings → API Keys
2. Click "Create API Key"
3. Name: "Trading Robot Campaigns"
4. Permissions: "Mail Send" (Full Access)
5. Copy the API key

### Step 3: Configure .env
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key-here
FROM_EMAIL=noreply@tradingrobotplug.com
FROM_NAME=Trading Robot Team
```

---

## Mailgun Setup (Production Alternative)

### Step 1: Create Mailgun Account
1. Sign up at [Mailgun](https://www.mailgun.com)
2. Verify your domain

### Step 2: Get SMTP Credentials
1. Go to Sending → Domain Settings
2. Click "SMTP credentials"
3. Copy username and password

### Step 3: Configure .env
```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
FROM_EMAIL=noreply@tradingrobotplug.com
FROM_NAME=Trading Robot Team
```

---

## AWS SES Setup (Enterprise)

### Step 1: Set Up AWS SES
1. Create AWS account
2. Go to SES → SMTP Settings
3. Create SMTP credentials

### Step 2: Verify Email/Domain
1. Verify sending email address or domain
2. Move out of sandbox (if needed)

### Step 3: Configure .env
```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com  # Use your region
SMTP_PORT=587
SMTP_USER=your-ses-smtp-username
SMTP_PASSWORD=your-ses-smtp-password
FROM_EMAIL=noreply@tradingrobotplug.com
FROM_NAME=Trading Robot Team
```

---

## Testing

### Test Email Sending
```python
from trading_robot.email_campaigns import EmailService
import os

email_service = EmailService(
    smtp_host=os.getenv("SMTP_HOST"),
    smtp_port=int(os.getenv("SMTP_PORT", "587")),
    smtp_user=os.getenv("SMTP_USER"),
    smtp_password=os.getenv("SMTP_PASSWORD"),
    from_email=os.getenv("FROM_EMAIL"),
)

# Test send
success = email_service.send_email(
    to_email="test@example.com",
    subject="Test Email",
    html_body="<h1>Test</h1><p>This is a test email.</p>",
    text_body="Test\n\nThis is a test email.",
)

print("✅ Email sent successfully" if success else "❌ Email failed")
```

### Test Campaign System
```bash
python trading_robot/email_campaigns/run_campaigns.py
```

---

## Troubleshooting

### Gmail: "Username and Password not accepted"
- ✅ Use App Password, not regular password
- ✅ Enable 2-Step Verification first
- ✅ FROM_EMAIL must match SMTP_USER for Gmail

### "Connection refused" or "Timeout"
- ✅ Check SMTP_HOST and SMTP_PORT
- ✅ Verify firewall allows outbound SMTP
- ✅ Try port 465 (SSL) instead of 587 (TLS)

### "Authentication failed"
- ✅ Verify SMTP_USER and SMTP_PASSWORD
- ✅ Check for extra spaces in password
- ✅ Ensure credentials are correct for provider

### Emails going to spam
- ✅ Use production SMTP provider (SendGrid/Mailgun)
- ✅ Verify SPF/DKIM records for your domain
- ✅ Use verified FROM_EMAIL domain

---

## Security Best Practices

1. **Never commit .env to git** - Already in .gitignore
2. **Use App Passwords** - Never use regular passwords
3. **Rotate credentials** - Change passwords periodically
4. **Limit permissions** - Use least privilege for SMTP accounts
5. **Monitor usage** - Check SMTP provider logs for suspicious activity

---

## Environment Variables Summary

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SMTP_HOST` | Yes | `smtp.gmail.com` | SMTP server hostname |
| `SMTP_PORT` | Yes | `587` | SMTP server port |
| `SMTP_USER` | Yes | - | SMTP username/email |
| `SMTP_PASSWORD` | Yes | - | SMTP password/app password |
| `FROM_EMAIL` | Yes | - | Sender email address |
| `FROM_NAME` | No | `Trading Robot Team` | Sender display name |

---

**Need Help?** Check the main documentation: `trading_robot/ENV_SETUP_DOCUMENTATION.md`

