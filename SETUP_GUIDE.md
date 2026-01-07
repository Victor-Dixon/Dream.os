# dream.os Setup Guide

## Quick Start

1. **Run the Setup Wizard** (Recommended):
   ```bash
   python setup_wizard.py
   ```
   This interactive wizard will guide you through configuring all necessary settings.

2. **Start Services**:
   ```bash
   python main.py --background
   ```

3. **Check Status**:
   ```bash
   python main.py --status
   ```

## Setup Wizard Features

The setup wizard (`setup_wizard.py`) provides an interactive interface to configure:

### 🌍 Environment Settings
- Environment selection (development/staging/production)
- Debug mode and logging configuration

### 🔑 API Keys & Tokens
- Discord Bot Token
- Twitch Access Token and Channel
- OpenAI API Key (optional)

### ⚙️ Service Configuration
- Message Queue Service
- Discord Bot
- Twitch Bot
- FastAPI Service
- Web Server (Flask)
- Auto Gas Pipeline

### 🌐 Network Settings
- FastAPI port (default: 8001)
- Flask port (default: 5000)
- Web host configuration
- CORS origins

### ⚡ Advanced Settings
- Max workers for concurrent processing
- Request timeouts
- Rate limiting configuration

## Configuration Validation

The setup wizard automatically validates your configuration and warns about:

- Missing API keys for enabled services
- Port conflicts
- Invalid URL formats
- Missing dependencies

## Setup Wizard Commands

```bash
# Interactive setup (recommended)
python setup_wizard.py

# Validate existing configuration
python setup_wizard.py --validate

# Reset configuration to defaults
python setup_wizard.py --reset
```

## Environment Variables

The setup wizard creates a `.env` file with all necessary environment variables:

```bash
# Environment
ENV=development
DEBUG=false
LOG_LEVEL=INFO

# API Keys
DISCORD_TOKEN=your_discord_token
TWITCH_ACCESS_TOKEN=your_twitch_token
TWITCH_CHANNEL=your_channel
OPENAI_API_KEY=your_openai_key

# Network
FASTAPI_PORT=8001
FLASK_PORT=5000
WEB_HOST=localhost

# Advanced
MAX_WORKERS=4
REQUEST_TIMEOUT=30
```

## Service Dependencies

Some services require specific configuration:

- **Discord Bot**: Requires `DISCORD_TOKEN`
- **Twitch Bot**: Requires `TWITCH_ACCESS_TOKEN` and `TWITCH_CHANNEL`
- **Message Queue**: Always enabled (core service)
- **FastAPI/Web Server**: Always enabled (core services)

## Troubleshooting

### Configuration Issues
Run validation to check for problems:
```bash
python setup_wizard.py --validate
```

### Reset Configuration
If you need to start over:
```bash
python setup_wizard.py --reset
```

### Service Won't Start
1. Check configuration: `python setup_wizard.py --validate`
2. Check service logs in the `logs/` directory
3. Ensure required API keys are set
4. Verify ports are not in use by other services

## Next Steps

After setup is complete:

1. **Start Services**: `python main.py --background`
2. **Monitor Status**: `python main.py --status`
3. **View Logs**: Check `logs/` directory
4. **Access Web Interface**: Open http://localhost:5000
5. **Access API Docs**: Open http://localhost:8001/docs

## Support

If you encounter issues:

1. Run the setup wizard again: `python setup_wizard.py`
2. Check the validation output for specific errors
3. Review the logs for detailed error messages
4. Ensure all required dependencies are installed

---

**V2 Compliance**: This setup guide follows dream.os standards and is automatically maintained.