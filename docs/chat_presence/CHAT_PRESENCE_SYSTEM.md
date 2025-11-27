# 🎤 Chat Presence & OBS Caption System

Complete implementation of chat presence for Twitch/Discord and OBS caption → agent response loop.

## 📋 Overview

Two integrated systems:

1. **Chat Presence** - Agents respond to Twitch/Discord chat with personalities
2. **OBS Caption Loop** - Your voice → captions → agent actions

## 🏗️ Architecture

### System 1: Chat Presence

```
Twitch/Discord Chat → Message Interpreter → Agent Selection → 
Personality Formatting → Chat Scheduler → Response Delivery
```

**Components:**
- `twitch_bridge.py` - Twitch IRC connection
- `message_interpreter.py` - Decides which agent responds
- `agent_personality.py` - 8 agent personality profiles
- `chat_scheduler.py` - Fair rotation and cooldown management
- `chat_presence_orchestrator.py` - Main coordinator

### System 2: OBS Caption Loop

```
OBS Captions → Caption Listener → Caption Interpreter → 
Intent Classification → Agent Routing → Action Execution
```

**Components:**
- `caption_listener.py` - OBS WebSocket/file listener
- `caption_interpreter.py` - Speech → intent mapping
- `speech_log_manager.py` - Caption logging to devlogs/memory

## 🚀 Quick Start

### Installation

```bash
# Install required dependencies
pip install websockets irc

# For OBS WebSocket (if using)
pip install obs-websocket-py  # Optional
```

### Basic Usage

```python
from src.services.chat_presence import ChatPresenceOrchestrator

# Configure
twitch_config = {
    "username": "your_bot_username",
    "oauth_token": "oauth:xxxxx",  # Get from https://twitchapps.com/tmi/
    "channel": "your_channel_name",
}

obs_config = {
    "host": "localhost",
    "port": 4455,
    "password": None,  # If OBS WebSocket requires password
}

# Start orchestrator
orchestrator = ChatPresenceOrchestrator(
    twitch_config=twitch_config,
    obs_config=obs_config,
)

await orchestrator.start()
```

## 📡 Twitch Setup

### 1. Get OAuth Token

1. Visit: https://twitchapps.com/tmi/
2. Authorize your bot account
3. Copy the OAuth token (format: `oauth:xxxxx`)

### 2. Configure Bot

```python
twitch_config = {
    "username": "YourBotName",
    "oauth_token": "oauth:your_token_here",
    "channel": "your_channel",  # Without # prefix
}
```

### 3. Commands

Viewers can use:
- `!agent1` - Direct message to Agent-1
- `!agent-7` - Direct message to Agent-7
- `!team` - Broadcast to all agents
- `!swarm` - Broadcast to all agents

## 🎤 OBS Setup

### Option 1: WebSocket (Recommended)

1. **OBS Studio:**
   - Tools → WebSocket Server Settings
   - Enable WebSocket server
   - Port: 4455 (default)
   - Password: (optional)

2. **OBS Caption Plugin:**
   - Install OBS Caption plugin
   - Configure to output to WebSocket
   - Or use built-in caption source

3. **Configure Listener:**
```python
obs_config = {
    "host": "localhost",
    "port": 4455,
    "password": None,  # If set in OBS
}
```

### Option 2: File Output (Fallback)

1. **OBS Settings:**
   - Output → Recording → Caption Output
   - Set file path (e.g., `C:/obs_captions.txt`)

2. **Use File Listener:**
```python
from src.obs import OBSCaptionFileListener

listener = OBSCaptionFileListener(
    caption_file_path="C:/obs_captions.txt",
    on_caption=handle_caption,
)

await listener.listen()
```

## 🎭 Agent Personalities

Each agent has a unique personality:

| Agent | Role | Tone | Emoji Usage |
|-------|------|------|-------------|
| Agent-1 | Integration | Technical | Moderate |
| Agent-2 | Architecture | Analytical | Light |
| Agent-3 | DevOps | Professional | Moderate |
| Agent-4 | Captain | Professional | Moderate |
| Agent-5 | Business Intelligence | Analytical | Light |
| Agent-6 | Coordination | Friendly | Heavy |
| Agent-7 | Web Development | Enthusiastic | Heavy |
| Agent-8 | SSOT | Technical | Moderate |

### Customizing Personalities

Edit `src/services/chat_presence/agent_personality.py`:

```python
AGENT_PERSONALITIES["Agent-7"] = AgentPersonality(
    agent_id="Agent-7",
    agent_name="Web Development Specialist",
    role="Web Development",
    tone=PersonalityTone.ENTHUSIASTIC,
    greeting_style="Energetic and web-focused",
    response_prefixes=["🌐", "⚡", "✨"],
    response_suffixes=["UI updated!", "Feature deployed!"],
    emoji_usage="heavy",
    technical_depth="medium",
    max_response_length=200,
    personality_traits=["enthusiastic", "web-focused"],
)
```

## 🧠 Caption Interpretation

The caption interpreter recognizes:

### Agent Names
- "agent one", "agent-1", "agent1" → Agent-1
- "captain" → Agent-4
- "web agent" → Agent-7

### Intents
- **Agent Instruction**: "tell agent one to check the repo"
- **Task Assignment**: "task agent-7 to update the UI"
- **Devlog Update**: "log this as a devlog"
- **Broadcast**: "all agents scan the codebase"
- **Tool Trigger**: "run the scanner", "check status"

### Examples

```
"okay agent four check the repository for missing tests"
→ Intent: AGENT_INSTRUCTION
→ Target: Agent-4
→ Action: message

"all agents I need you to scan for V2 violations"
→ Intent: BROADCAST
→ Target: All agents
→ Action: message

"agent seven update the dashboard UI"
→ Intent: TASK_ASSIGNMENT
→ Target: Agent-7
→ Action: task
```

## 📝 Speech Logging

All captions are logged to:

1. **Devlogs** - `devlogs/{timestamp}_speech_caption.md`
2. **Memory** - `swarm_brain/knowledge_base.json` (speech_logs array)

Recent captions available via:
```python
from src.obs import SpeechLogManager

manager = SpeechLogManager()
recent = manager.get_recent_captions(limit=10)
```

## 🔧 Configuration

### Environment Variables

```bash
# Twitch
TWITCH_BOT_USERNAME=YourBotName
TWITCH_OAUTH_TOKEN=oauth:xxxxx
TWITCH_CHANNEL=your_channel

# OBS
OBS_WEBSOCKET_HOST=localhost
OBS_WEBSOCKET_PORT=4455
OBS_WEBSOCKET_PASSWORD=
```

### Configuration File

Create `config/chat_presence.json`:

```json
{
  "twitch": {
    "username": "YourBotName",
    "oauth_token": "oauth:xxxxx",
    "channel": "your_channel"
  },
  "obs": {
    "host": "localhost",
    "port": 4455,
    "password": null
  },
  "scheduler": {
    "cooldown_seconds": 30
  }
}
```

## 🎯 Integration with Messaging Core

The system integrates with the existing SSOT messaging core:

```python
from src.core.messaging_core import send_message
from src.core.messaging_models_core import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)

# Captions automatically route through messaging core
send_message(
    content="Caption interpreted as task",
    sender="HUMAN",
    recipient="Agent-7",
    message_type=UnifiedMessageType.HUMAN_TO_AGENT,
    priority=UnifiedMessagePriority.REGULAR,
)
```

## 🐛 Troubleshooting

### Twitch Connection Issues

1. **Check OAuth token** - Must be in format `oauth:xxxxx`
2. **Verify channel name** - Without `#` prefix
3. **Check bot permissions** - Bot must be in channel

### OBS Connection Issues

1. **WebSocket not connecting:**
   - Verify OBS WebSocket server is enabled
   - Check port (default: 4455)
   - Verify firewall settings

2. **No captions received:**
   - Check OBS caption plugin is active
   - Verify caption source is configured
   - Check file path (if using file listener)

### Agent Not Responding

1. **Check cooldown** - Agent may be on cooldown (30s default)
2. **Verify personality match** - Message may not match agent expertise
3. **Check logs** - Review interpreter decisions

## 📊 Monitoring

### Activity Stats

```python
from src.services.chat_presence import ChatScheduler

scheduler = ChatScheduler()
stats = scheduler.get_agent_activity_stats()

for agent_id, stats in stats.items():
    print(f"{agent_id}: {stats['total_responses']} responses")
```

### Logs

All activity is logged:
- Twitch messages: `INFO` level
- OBS captions: `INFO` level
- Agent responses: `INFO` level
- Errors: `ERROR` level

## 🔮 Future Enhancements

- [ ] LLM integration for intelligent responses
- [ ] Discord bot extension (beyond devlog monitoring)
- [ ] Response history and context window
- [ ] Multi-channel support
- [ ] Custom command registration
- [ ] Response templates per agent
- [ ] Activity analytics dashboard

## 📚 API Reference

See individual module documentation:
- `src/services/chat_presence/` - Chat presence components
- `src/obs/` - OBS integration components

## 🤝 Contributing

When extending the system:

1. **V2 Compliance** - Keep files <400 lines
2. **Single Responsibility** - One purpose per module
3. **SSOT Integration** - Use messaging_core for delivery
4. **Personality Consistency** - Maintain agent voices

---

**Author:** Agent-7 (Web Development Specialist)  
**License:** MIT  
**Status:** ✅ Production Ready


