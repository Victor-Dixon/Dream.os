# Devlog Poster Tool Instructions

**Tool Location:** `tools/devlog_poster.py`

## Usage

```bash
python tools/devlog_poster.py --agent Agent-X --file <devlog_path> [--title "Optional Title"]
```

## Examples

```bash
# Basic usage
python tools/devlog_poster.py --agent Agent-3 --file devlogs/2025-12-26_status.md

# With custom title
python tools/devlog_poster.py --agent Agent-7 --file agent_workspaces/Agent-7/devlogs/status.md --title "Agent-7 Status Update"
```

## How It Works

1. Reads devlog markdown file
2. Extracts title from `#` heading or uses filename if no heading
3. Truncates content if needed (Discord 2000 char limit)
4. Posts to **agent-specific Discord channel** (e.g., `#agent-3`) using Discord bot

## Requirements

- `DISCORD_BOT_TOKEN` must be set in `.env`
- Discord bot must have access to agent channels (e.g., `#agent-1`, `#agent-2`, etc.)
- `discord.py` must be installed: `pip install discord.py`

## Channel Format

- Posts go to channel named: `agent-{number}` (e.g., `agent-3` for Agent-3)
- Channel must exist in Discord server where bot is connected
- Each agent has their own devlog channel

## Error Handling

- Shows clear error if bot token not configured
- Shows error if file not found
- Shows error if channel not found (lists available channels)
- Shows error if file read fails
- Automatically truncates content if too long

## Status

✅ Tool ready for use! Posts to agent-specific Discord channels.

**Updated:** 2025-12-26 - Now uses Discord bot to post to agent-specific channels instead of router webhook.
