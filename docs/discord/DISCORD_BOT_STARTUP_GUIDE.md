# Discord Bot Startup Guide

**Date:** 2025-12-22  
**Agent:** Agent-5 (Business Intelligence Specialist)

## Quick Start

### 1. Verify .env File Configuration

The Discord bot requires `DISCORD_BOT_TOKEN` in the `.env` file at the repository root.

**Check if .env exists:**
```powershell
Test-Path .env
```

**Check if token is set:**
```powershell
Select-String -Path .env -Pattern "^DISCORD_BOT_TOKEN"
```

### 2. Required .env Configuration

Your `.env` file should contain:
```
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here  # Optional
```

### 3. Start Discord System

```bash
python tools/start_discord_system.py
```

This starts:
- **Message Queue Processor** - Handles incoming messages from the unified messaging system
- **Discord Bot Runner** - Connects to Discord and processes commands

### 4. Verify Startup

The script should output:
```
🚀 Starting Discord System...
📬 Starting message queue processor...
✅ Queue processor started (PID: xxxx)
🤖 Starting Discord bot...
✅ Discord bot started (PID: xxxx)
```

## Troubleshooting

### Issue: "DISCORD_BOT_TOKEN not set in environment"

**Solution:**
1. Verify `.env` file exists in repository root
2. Verify `DISCORD_BOT_TOKEN` is set in `.env`
3. Verify `python-dotenv` is installed: `pip install python-dotenv`
4. The bot runner now loads `.env` automatically (updated 2025-12-22)

### Issue: "Invalid Discord token"

**Solution:**
- Verify the token in `.env` is correct
- Token should not have quotes: `DISCORD_BOT_TOKEN=actual_token_here`
- Token should be on a single line

### Issue: Bot starts but doesn't connect

**Solution:**
- Check Discord bot has proper permissions in Discord Developer Portal
- Verify bot has been added to your Discord server
- Check if required intents are enabled in Discord Developer Portal

## Code Changes (2025-12-22)

Updated `src/discord_commander/bot_runner.py` to load `.env` file before reading `DISCORD_BOT_TOKEN`:

```python
# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Continuing without .env support...")
```

This ensures the `.env` file is loaded before attempting to read the token.

## Logs

Discord bot logs are written to:
- `runtime/logs/discord_bot_YYYYMMDD.log`

Check logs for detailed error messages:
```powershell
Get-Content runtime\logs\discord_bot_*.log -Tail 50
```

## Status

- ✅ `.env` file loading added to `bot_runner.py`
- ✅ Startup script ready (`tools/start_discord_system.py`)
- ⚠️ Verify `.env` contains `DISCORD_BOT_TOKEN`

---

*Guide created: 2025-12-22*  
*Next: Verify token is set in .env and test startup*

