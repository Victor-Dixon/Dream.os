# 🚀 Complete Discord Bot Setup Guide for Dream.os Agents

## 🎯 Overview
This guide will get your Dream.os Discord bot fully operational for agent communication and coordination.

## 📋 Prerequisites
- Discord account
- Server where you have admin permissions
- Bot token from Discord Developer Portal

## 🔧 Step-by-Step Setup

### Step 1: Create Discord Application
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name: `Dream.os Agent Controller`
4. Go to "Bot" section
5. Click "Add Bot"
6. Copy the bot token (save it securely!)

### Step 2: Configure Bot Permissions
1. In Bot section, enable these privileges:
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Read Message History
   - ✅ Read Messages/View Channels
   - ✅ Mention Everyone (optional)

### Step 3: Generate Invite Link
1. Go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Use Slash Commands
   - ✅ Read Message History
   - ✅ Read Messages/View Channels
4. Copy the generated URL
5. Paste URL in browser and invite bot to your server

### Step 4: Configure Dream.os
```bash
cd /home/dream/Development/Dream.os
nano .env
```

Replace this line:
```
DISCORD_BOT_TOKEN=PASTE_YOUR_DISCORD_BOT_TOKEN_HERE
```

With your real token:
```
DISCORD_BOT_TOKEN=YOUR_ACTUAL_DISCORD_BOT_TOKEN_HERE
```

### Step 5: Start Discord Service
```bash
cd /home/dream/Development/Dream.os
source venv/bin/activate
python main.py --discord --background
```

### Step 6: Verify Bot is Online
Check status:
```bash
python main.py --status
🟢 discord: RUNNING (PID: xxxxx)
```

Bot should appear online in your Discord server.

## 🤖 Available Agent Commands

Once configured, agents can use these Discord slash commands:

### Core Commands
- `/agent status` - Check agent system status
- `/agent message <agent> <message>` - Send message to specific agent
- `/agent broadcast <message>` - Send to all agents

### GitHub Integration
- `/github setup` - Professional repository setup
- `/github analyze <repo>` - Repository health analysis  
- `/github issue <repo> <title> <body>` - Create GitHub issue
- `/github ci <repo> <language>` - Setup CI/CD workflow

### System Management
- `/system health` - Overall system health
- `/system services` - Service status
- `/system restart` - Restart services

## 🔍 Testing the Setup

### Test 1: Bot Responsiveness
In Discord, type:
```
/agent status
```

Bot should respond with system information.

### Test 2: Agent Communication
```
/agent broadcast Hello Dream.os agents!
```

Should queue messages to all 8 agents.

### Test 3: GitHub Integration
```
/github analyze Victor-Dixon/AgentTools
```

Should provide repository health analysis.

## 🚨 Troubleshooting

### Bot Not Responding
```bash
# Check if service is running
python main.py --status

# Check logs
tail -f logs/*.log

# Restart service
python main.py --stop
python main.py --discord --background
```

### Invalid Token Error
- Verify token is correct (starts with M, N, or O)
- Check token permissions in Discord Developer Portal
- Ensure bot is invited to server with proper permissions

### Commands Not Registering
- Bot needs `applications.commands` scope
- Restart bot after configuration changes
- Wait up to 1 hour for global command registration

## 🎯 Advanced Configuration

### Custom Agent Commands
Edit `src/discord_commander/commands/` to add new commands.

### Channel-Specific Behavior
Set `DISCORD_CHANNEL_ID` in .env for default channel.

### Multiple Servers
Bot can join multiple servers with the same token.

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# System health
curl http://localhost:5000/health

# Discord bot status
python main.py --status
```

### Log Monitoring
```bash
# View all logs
tail -f logs/*.log

# Discord specific logs
tail -f runtime/logs/discord.log
```

### Performance Tuning
- Adjust rate limits in config
- Monitor API usage in Discord Developer Portal
- Scale services as needed

## 🎉 Success Indicators

✅ Bot appears online in Discord server
✅ `/agent status` command works
✅ Messages can be sent to agents
✅ GitHub integration responds
✅ Web dashboard shows active services

## 🚀 Next Steps After Setup

1. **Invite Team Members** - Add collaborators to server
2. **Configure Agent Roles** - Set up agent permissions
3. **Set Up GitHub Integration** - Add GITHUB_TOKEN
4. **Create Agent Workflows** - Design automated processes
5. **Monitor & Scale** - Track performance and expand

---

**🎯 Your Dream.os Discord bot will enable seamless AI agent coordination and GitHub automation through natural Discord commands!**
