# 📊 Cycle Accomplishments Report Procedure

## Quick Command

```bash
python tools/post_cycle_report_to_discord.py
```

This single command will:
1. ✅ Generate a fresh cycle accomplishments report (if one doesn't exist for today)
2. ✅ Post it to Discord automatically

---

## Detailed Procedure

### Option 1: Generate and Post (Recommended)
```bash
# Generate fresh report + post to Discord
python tools/post_cycle_report_to_discord.py
```

### Option 2: Use Existing Report
```bash
# Reuse today's report (skip generation)
python tools/post_cycle_report_to_discord.py --no-generate
```

### Option 3: Custom Channel
```bash
# Post to specific Discord channel
python tools/post_cycle_report_to_discord.py --channel YOUR_CHANNEL_ID
```

---

## Manual Steps (If Needed)

### Step 1: Generate Report Only
```bash
python tools/generate_cycle_accomplishments_report.py
```
Report will be saved to: `docs/archive/cycles/CYCLE_ACCOMPLISHMENTS_YYYY-MM-DD_HH-MM-SS.md`

### Step 2: Post to Discord
```bash
python tools/post_cycle_report_to_discord.py --no-generate
```

---

## Requirements

- ✅ `DISCORD_BOT_TOKEN` set in `.env` file
- ✅ `discord.py` installed (`pip install discord.py`)
- ✅ Agent status files exist in `agent_workspaces/{Agent-X}/status.json`

---

## What the Report Includes

- **Agent Activity Summary**: Status of all 8 agents
- **Completed Tasks**: All tasks completed across the swarm
- **Achievements**: Milestones and accomplishments
- **Points Earned**: Total points across all agents
- **Statistics**: Agent counts, task counts, progress metrics

---

## Output

- **File**: Saved to `docs/archive/cycles/`
- **Discord**: Posted to channel `1394677708167970917` (default)
- **Format**: Markdown file attached to Discord embed

---

## Examples

```bash
# Standard usage (generate + post)
python tools/post_cycle_report_to_discord.py

# Use existing report
python tools/post_cycle_report_to_discord.py --no-generate

# Custom channel
python tools/post_cycle_report_to_discord.py --channel 1234567890
```

