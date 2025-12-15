# 📊 Cycle Accomplishments Dual Posting

**Automatically posts cycle accomplishments to both Discord and weareswarm.online**

## Quick Start

```bash
# Post to both Discord and website (recommended)
python tools/post_cycle_accomplishments_dual.py
```

This single command will:
1. ✅ Generate a fresh cycle accomplishments report (if needed)
2. ✅ Format it as a mobile-friendly blog post
3. ✅ Post to Discord with embed + attachment
4. ✅ Post to weareswarm.online as a blog post

---

## Usage Options

### Standard Usage (Both Platforms)
```bash
python tools/post_cycle_accomplishments_dual.py
```

### With Cycle ID
```bash
python tools/post_cycle_accomplishments_dual.py --cycle C-123
```

### Reuse Existing Report
```bash
python tools/post_cycle_accomplishments_dual.py --no-generate
```

### Discord Only
```bash
python tools/post_cycle_accomplishments_dual.py --discord-only
```

### Website Only
```bash
python tools/post_cycle_accomplishments_dual.py --website-only
```

### Custom Discord Channel
```bash
python tools/post_cycle_accomplishments_dual.py --channel YOUR_CHANNEL_ID
```

---

## Features

### ✅ Mobile-Friendly Template
- Responsive design with `clamp()` for font sizes
- Touch-friendly spacing and layouts
- Optimized for mobile viewing (primary access method)
- Grid layouts that stack on mobile

### ✅ Mode-Aware
- Only includes active agents (respects 4-agent mode)
- Automatically adapts to current agent mode configuration

### ✅ Standardized Format
- Consistent styling across all posts
- Agent color coding for visual distinction
- Summary cards with key metrics
- Professional presentation

### ✅ Dual Posting
- Posts to Discord for team visibility
- Posts to website for public documentation
- Synchronized content across platforms

---

## Mobile Optimization

The template uses:
- **Responsive Typography**: `clamp(1em, 2.5vw, 1.1em)` for adaptive font sizes
- **Flexible Grids**: `repeat(auto-fit, minmax(150px, 1fr))` for responsive layouts
- **Touch-Friendly**: Generous padding and spacing
- **Optimized Images**: Efficient CSS for fast loading

---

## Template Structure

1. **Hero Section**: Gradient header with cycle ID and date
2. **Introduction**: Brief context about the cycle
3. **Summary Cards**: Key metrics (agents, tasks, achievements, points)
4. **Agent Accomplishments**: Per-agent breakdown with color coding
5. **Conclusion**: Summary and closing statement

---

## Requirements

- ✅ `DISCORD_BOT_TOKEN` set in `.env`
- ✅ WordPress credentials configured for weareswarm.online
- ✅ `discord.py` installed (`pip install discord.py`)
- ✅ `tools/unified_blogging_automation.py` available

---

## Output

**Discord:**
- Embed with summary statistics
- Full markdown report attached as file
- Posted to default channel or specified channel

**Website:**
- Published blog post on weareswarm.online
- Mobile-friendly formatting
- Publicly accessible
- SEO optimized

---

## Agent Color Coding

- Agent-1: Purple (#667eea)
- Agent-2: Dark Purple (#764ba2)
- Agent-3: Blue (#4facfe)
- Agent-4: Pink (#f093fb)
- Agent-5: Green (#43e97b)
- Agent-6: Coral (#fa709a)
- Agent-7: Amber (#f59e0b)
- Agent-8: Cyan (#30cfd0)

---

## Integration with Workflow

This tool can be:
- ✅ Run manually when needed
- ✅ Scheduled via cron/Task Scheduler
- ✅ Integrated into cycle completion workflows
- ✅ Triggered automatically by orchestrator

**Example Cron (daily at 9 AM):**
```bash
0 9 * * * cd /path/to/repo && python tools/post_cycle_accomplishments_dual.py
```

---

**🐝 WE. ARE. SWARM. AUTONOMOUS. POWERFUL. ⚡🔥🚀**


