# 🚀 Agent Cellphone V2 - Quick Start Guide

**Get your multi-agent system running in under 15 minutes**

[![Docker](https://img.shields.io/badge/Docker-Recommended-blue)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)

---

## 📋 Prerequisites

### Option 1: Docker (Recommended)
- [Docker Desktop](https://docker.com/get-started) installed and running
- 4GB RAM available
- 10GB disk space

### Option 2: Native Python
- Python 3.11 or higher
- pip package manager
- Git (optional, for cloning)

---

## ⚡ Quick Installation

### Docker Installation (Recommended)

```bash
# 1. Clone or download the repository
git clone https://github.com/your-org/agent-cellphone-v2.git
cd agent-cellphone-v2

# 2. Run the installation script
./install.sh --docker

# 3. Configure your environment
nano .env.docker  # Edit with your API keys

# 4. Start the system
docker-compose up -d

# 5. Check status
docker-compose ps
```

### Native Python Installation

```bash
# 1. Clone or download the repository
git clone https://github.com/your-org/agent-cellphone-v2.git
cd agent-cellphone-v2

# 2. Run the installation script
./install.sh

# 3. Configure your environment
nano .env  # Edit with your API keys

# 4. Start the system
python main.py --background

# 5. Check status
python main.py --status
```

### Windows Installation

```batch
# 1. Download and extract the repository
# 2. Run the installer
install.bat

# 3. Configure environment
notepad .env  # Edit with your API keys

# 4. Start the system
python main.py --background

# 5. Check status
python main.py --status
```

---

## 🔧 Configuration

### Required Environment Variables

Edit your `.env` file with these essential settings:

```bash
# Discord Bot (Required for agent communication)
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# Twitch Bot (Optional, for streaming integration)
TWITCH_CHANNEL=your_twitch_channel
TWITCH_ACCESS_TOKEN=oauth:your_twitch_token

# Database (Auto-configured in Docker)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agent_cellphone
DB_USER=agent
DB_PASSWORD=your_secure_password

# Web Interface
SECRET_KEY=your_random_secret_key_here
```

### Getting Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Copy the token
5. Invite bot to your server with proper permissions

---

## 🎯 First Run

### Start the System

```bash
# Docker
docker-compose up -d

# Native
python main.py --background
```

### Access the Web Interface

- **Web Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Check System Status

```bash
# View all services
python main.py --status

# Start specific agents
python main.py --start-agents 1,2,3,4

# View agent mode
python main.py --select-mode
```

---

## 🤖 Agent Management

### Agent Modes

The system supports different agent configurations:

- **4-agent**: Core agents (Agent-1, Agent-2, Agent-3, Agent-4)
- **8-agent**: Full swarm (all agents active)

```bash
# Switch to 8-agent mode
python main.py --select-mode
# Select option 2 for 8-agent mode
```

### Agent Workspaces

Each agent has its own workspace at `agent_workspaces/Agent-X/`:
- `status.json` - Agent status and configuration
- `inbox/` - Incoming messages and tasks
- `archive/` - Completed work history

### Communicating with Agents

```bash
# Send message to specific agent
python -m src.services.messaging_cli -a Agent-1 -m "Hello Agent-1"

# Send to all active agents
python -m src.services.messaging_cli --bulk -m "System update completed"
```

---

## 📊 Monitoring & Troubleshooting

### View Logs

```bash
# Docker logs
docker-compose logs -f agent-cellphone

# Native logs
tail -f logs/*.log

# Service-specific logs
tail -f runtime/logs/message_queue.log
```

### Health Checks

```bash
# System health
curl http://localhost:8000/health

# Database connection
python -c "from src.core.database import test_connection; test_connection()"

# Agent status
python main.py --status
```

### Common Issues

**❌ Services not starting**
```bash
# Check configuration
python main.py --status

# View detailed logs
docker-compose logs agent-cellphone
```

**❌ Agents not responding**
```bash
# Check agent mode
python main.py --select-mode

# Restart agents
python main.py --start-agents 1,2,3,4
```

**❌ Database connection failed**
```bash
# Docker: Check database service
docker-compose ps postgres

# Reset database
docker-compose restart postgres
```

---

## 🛠️ Development & Customization

### Project Structure

```
agent-cellphone-v2/
├── src/                    # Core application code
│   ├── core/              # Core services and utilities
│   ├── services/          # Business logic services
│   └── discord_commander/ # Discord bot integration
├── agent_workspaces/      # Agent-specific data
├── config/                # Configuration files
├── tools/                 # Utility scripts
├── docs/                  # Documentation
└── docker-compose.yml     # Docker orchestration
```

### Adding New Agents

```bash
# 1. Create agent workspace
mkdir agent_workspaces/Agent-9

# 2. Initialize status
echo '{"agent_id": "Agent-9", "status": "ACTIVE"}' > agent_workspaces/Agent-9/status.json

# 3. Update agent registry
python scripts/agent_onboarding.py --register Agent-9
```

### Custom Commands

```bash
# List available commands
python main.py --help

# Development mode
AGENT_CELLPHONE_ENV=development python main.py

# Debug logging
AGENT_CELLPHONE_ENV=development python main.py --background
```

---

## 📚 Advanced Usage

### Backup & Restore

```bash
# Backup data (Docker)
docker run --rm -v agent-cellphone-v2_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# Restore data
docker run --rm -v agent-cellphone-v2_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
```

### Scaling

```bash
# Scale services (Docker)
docker-compose up -d --scale agent-cellphone=3

# Load balancer configuration
# Add nginx or traefik for production scaling
```

### Integration APIs

```python
# Python API usage
from src.services.messaging_core import send_message

send_message(
    recipient="Agent-1",
    content="Process this task",
    priority="urgent"
)
```

---

## 🆘 Support & Resources

### Documentation
- [Full Documentation](https://docs.agent-cellphone-v2.com)
- [API Reference](https://docs.agent-cellphone-v2.com/api)
- [Troubleshooting Guide](https://docs.agent-cellphone-v2.com/troubleshooting)

### Community
- [Discord Server](https://discord.gg/agent-cellphone)
- [GitHub Issues](https://github.com/your-org/agent-cellphone-v2/issues)
- [Discussion Forum](https://forum.agent-cellphone-v2.com)

### Professional Support
- Enterprise deployment assistance
- Custom agent development
- Training and consulting

---

## 🎉 You're All Set!

Your Agent Cellphone V2 system is now running. The agents will begin coordinating automatically based on their configured roles and the tasks you assign them.

**Next steps:**
1. Explore the web dashboard
2. Send your first message to an agent
3. Monitor system performance
4. Customize agent behaviors

Happy automating! 🤖✨