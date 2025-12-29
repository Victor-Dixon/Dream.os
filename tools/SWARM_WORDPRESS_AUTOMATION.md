# Swarm to WordPress Automation

## Overview

This automation system connects swarm workflows to WordPress, automatically creating content on **all 4 sites** from:

1. **Session Closures** → Experiments & Projects (dadudekc.com) + Trading Journals (freerideinvestor.com) + Backtests (tradingrobotplug.com) + Docs (weareswarm.online)
2. **Devlogs** → Blog Posts (all sites)
3. **Status Updates** → Resume Items (future)

## SSOT Alignment

Per the SSOT whiteboard:
- ✅ **"Dreamvault + ChatGPT conversation history = blogging for dadudekc"** → Devlogs become blog posts
- ✅ **"plans + learnings from experiments = content"** → Session closures become experiments
- ✅ **"demos of projects = content"** → Completed closures become projects
- ✅ **"skills learned = added to resume"** → Future: Extract skills from closures → resume items

## Multi-Site Content Generation

**Integrated with `multi_site_content_generator.py`** for SSOT routing:

One source entry (session closure) → **4 site-specific formats**:
- **dadudekc.com**: Builder voice (experiments, projects)
- **freerideinvestor.com**: Trading journal format
- **tradingrobotplug.com**: Backtest/iteration format
- **weareswarm.online**: Docs + implementation + promo

## How It Works

### 1. Session Closures → All 4 Sites

**Input**: `agent_workspaces/Agent-X/session_closures/*.md`

**Output** (via multi-site generator):
- **dadudekc.com**: Experiment post (builder voice, short lines)
- **freerideinvestor.com**: Trading journal post (if trading-related)
- **tradingrobotplug.com**: Backtest/iteration post (if trading-related)
- **weareswarm.online**: Docs post (what we built, how it works)

### 2. Devlogs → Blog Posts

**Input**: `agent_workspaces/Agent-X/devlogs/*.md`

**Output**:
- Standard WordPress post on all sites

## Usage

### Setup

1. **Set WordPress credentials** (Application Passwords):
```bash
export DADUDEKC_WP_USERNAME="your-username"
export DADUDEKC_WP_PASSWORD="your-application-password"
export FREERIDEINVESTOR_WP_USERNAME="your-username"
export FREERIDEINVESTOR_WP_PASSWORD="your-application-password"
export TRADINGROBOTPLUG_WP_USERNAME="your-username"
export TRADINGROBOTPLUG_WP_PASSWORD="your-application-password"
export WEARESWARM_WP_USERNAME="your-username"
export WEARESWARM_WP_PASSWORD="your-application-password"
```

2. **One-time run** (multi-site enabled):
```bash
python tools/swarm_to_wordpress_automation.py --once
```

3. **Watch mode** (continuous, multi-site):
```bash
python tools/swarm_to_wordpress_automation.py --watch --interval 300
```

4. **Disable multi-site** (basic formatting only):
```bash
python tools/swarm_to_wordpress_automation.py --once --no-multi-site
```

5. **Filter by agent**:
```bash
python tools/swarm_to_wordpress_automation.py --agent Agent-7 --once
```

6. **Process devlogs**:
```bash
python tools/swarm_to_wordpress_automation.py --devlogs --once
```

## State Tracking

The tool tracks processed files in `.swarm_wp_automation_state.json` to prevent duplicates:
- `processed_closures`: List of processed session closure files
- `processed_devlogs`: List of processed devlog files
- `last_check`: Timestamp of last check

## Integration with Dynamic Content System

Once posts are created, the dynamic content system on `dadudekc.com` automatically:
- ✅ Shows experiments in Experiments Feed
- ✅ Shows projects in Project Demos
- ✅ Calculates proof metrics from actual data
- ✅ Updates homepage dynamically

## Multi-Site Routing Logic

The automation uses `multi_site_content_generator.py` to:

1. **Parse source payload** (session closure content)
2. **Extract information** (actions, artifacts, learnings, etc.)
3. **Format for each site**:
   - **dadudekc.com**: Builder voice, short lines, direct
   - **freerideinvestor.com**: Trading journal (requires 4-6 screenshots)
   - **tradingrobotplug.com**: Backtest/iteration format
   - **weareswarm.online**: Docs + implementation + promo
4. **Post to all applicable sites** automatically

## Future Enhancements

### Resume Auto-Compilation
- Extract skills from session closures
- Auto-create resume items
- Compile resume PDF weekly

### GitHub Integration
- Auto-create projects from GitHub repos
- Link projects to GitHub automatically
- Update project status from repo activity

### weareswarm.online Integration
- Pull experiments from build feed
- Sync status across platforms
- Cross-link content

### Dreamvault Integration
- Auto-blog from conversation history
- Extract insights automatically
- Create content from ChatGPT conversations

## Files

- `tools/swarm_to_wordpress_automation.py` - Main automation script
- `tools/multi_site_content_generator.py` - SSOT routing generator (integrated)
- `.swarm_wp_automation_state.json` - State tracking (gitignored)

## Requirements

- Python 3.8+
- `requests` library
- WordPress REST API access
- Application passwords for all 4 WordPress sites

## Notes

- The tool is **idempotent**: Running multiple times won't create duplicates
- Files are tracked by relative path to prevent reprocessing
- WordPress credentials should be stored securely (env vars, not in code)
- Multi-site generation is **enabled by default** (use `--no-multi-site` to disable)
