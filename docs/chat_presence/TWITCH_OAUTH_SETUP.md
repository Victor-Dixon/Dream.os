# 🔐 Twitch OAuth Setup Guide

**Proper OAuth 2.0 Integration - No Third-Party Services**

This guide walks you through creating your own Twitch OAuth application and integrating it properly.

---

## 📋 Step 1: Create Twitch OAuth Application

1. **Go to Twitch Developers Console:**
   - Visit: https://dev.twitch.tv/console/apps
   - Log in with your Twitch account

2. **Register New Application:**
   - Click "Register Your Application"
   - Fill in:
     - **Name:** Agent Cellphone Chat Bot (or your preferred name)
     - **OAuth Redirect URLs:** `http://localhost:3000/callback`
     - **Category:** Chat Bot
   - Click "Create"

3. **Save Credentials:**
   - **Client ID:** Copy this (you'll need it)
   - **Client Secret:** Click "New Secret" and copy immediately (only shown once!)

---

## 🔧 Step 2: Configure Application

### Option A: Environment Variables (.env file)

Add to your `.env` file:

```bash
# Twitch OAuth Application Credentials
TWITCH_CLIENT_ID=your_client_id_here
TWITCH_CLIENT_SECRET=your_client_secret_here
TWITCH_REDIRECT_URI=http://localhost:3000/callback

# After OAuth flow completes, this will be set automatically
TWITCH_ACCESS_TOKEN=oauth:your_access_token_here
```

### Option B: Configuration File

Create `config/twitch_oauth.json`:

```json
{
  "client_id": "your_client_id_here",
  "client_secret": "your_client_secret_here",
  "redirect_uri": "http://localhost:3000/callback",
  "scopes": ["chat:read", "chat:edit", "channel:moderate"]
}
```

---

## 🚀 Step 3: Run OAuth Flow

### Interactive Token Generation

Run the OAuth flow tool:

```bash
python tools/twitch_oauth_setup.py
```

This will:
1. Open your browser to Twitch authorization
2. You authorize the application
3. Receive the access token automatically
4. Save it to your `.env` file

### Manual Flow

If you prefer manual setup:

```python
from src.services.chat_presence.twitch_oauth import get_oauth_token_interactive

token = get_oauth_token_interactive(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

print(f"Access token: {token}")
```

---

## ✅ Step 4: Use Token

Once you have the access token, use it in your chat presence:

```bash
# Token is automatically saved to .env as TWITCH_ACCESS_TOKEN
python tools/chat_presence_cli.py --twitch-only
```

Or manually set in `.env`:

```bash
TWITCH_ACCESS_TOKEN=oauth:your_token_here
TWITCH_CHANNEL=your_channel_name
```

---

## 🔄 Token Refresh

Access tokens expire. The system can automatically refresh them:

- Tokens are valid for ~60 days
- Refresh tokens don't expire (unless revoked)
- System will automatically refresh when needed

---

## 🛡️ Security Best Practices

1. **Never commit secrets to git:**
   - Add `.env` to `.gitignore`
   - Don't share client secrets publicly

2. **Use environment variables:**
   - Store secrets in `.env` file
   - Load via `python-dotenv`

3. **Rotate secrets if compromised:**
   - Go to Twitch Developer Console
   - Generate new client secret
   - Update your `.env` file

4. **Scope permissions minimally:**
   - Only request scopes you need
   - Review permissions regularly

---

## 📚 Required OAuth Scopes

Minimum required scopes for chat bot:

- `chat:read` - Read chat messages
- `chat:edit` - Send chat messages
- `channel:moderate` - Moderate channel (optional)

---

## 🐛 Troubleshooting

**"Invalid redirect URI":**
- Make sure redirect URI in code matches Twitch app settings exactly
- Default: `http://localhost:3000/callback`

**"Invalid client":**
- Check client ID and secret are correct
- Ensure app is registered in Twitch Developer Console

**"Token expired":**
- Run OAuth flow again to get new token
- System can auto-refresh if refresh token available

---

## 📖 API Documentation

- Twitch OAuth: https://dev.twitch.tv/docs/authentication/
- Twitch IRC: https://dev.twitch.tv/docs/irc/
- Developer Forums: https://discuss.dev.twitch.tv/

---

**This is the proper, secure way to integrate Twitch OAuth!** ✅

