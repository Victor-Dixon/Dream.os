# 30-Day Launch System - Quick Reference

## 🚀 Daily Commands

```bash
# View today's tasks
python tools/30day_launch_system.py --tasks

# Track progress
python tools/30day_launch_system.py --progress

# Update metrics (after completing activities)
python tools/30day_launch_system.py --update dms:10
python tools/30day_launch_system.py --update calls:2
python tools/30day_launch_system.py --update consults:1
python tools/30day_launch_system.py --update deposits:1

# Get DM script
python tools/30day_launch_system.py --dm-script

# Advance to next day (end of day)
python tools/30day_launch_system.py --advance

# Publish blog post (Days 8, 11, 18, 23)
python tools/30day_launch_system.py --publish-blog 8 "Title" content.md
```

## 📊 Weekly Targets

| Metric | Weekly Target | Track With |
|--------|--------------|------------|
| DMs | 70 | `--update dms:10` |
| Calls | 10 | `--update calls:1` |
| Consults | 5 | `--update consults:1` |
| Deposits | 2 | `--update deposits:1` |

## 📅 Blog Post Schedule

- **Day 8**: Blog post #1
- **Day 11**: Blog post #2  
- **Day 18**: Blog post #3
- **Day 23**: Blog post #4

All posts publish to `crosbyultimateevents.com` automatically.

## 💬 DM Script (Quick Copy)

**Opener**: Yo quick question—what do you do + how are you currently getting customers?

**Diagnose**: What have you tried? What's working even a little?

**Pitch**: I can package this into 3 tiers + build your site + give you a 30-day play to get your first paying clients.

**Close**: Want me to draft your packages today? I'll send a quick blueprint.

## 📋 Typical Daily Workflow

1. **Morning**: `--tasks` (see what to do today)
2. **Throughout day**: `--update` (track as you go)
3. **Evening**: `--progress` (check status)
4. **End of day**: `--advance` (move to next day)

## 🎯 Key Days

- **Day 1**: Foundation (niche, packages, pricing)
- **Day 4**: Website goes live
- **Day 6**: First outreach (20 DMs)
- **Day 7**: First calls (5 calls, 2 consults)
- **Day 8**: First blog post
- **Day 12**: First consult day
- **Day 19**: Big outreach sprint (50 DMs)
- **Day 30**: Results recap

---

**Pro Tip**: Run `python tools/30day_launch_system.py` (no args) to see tasks + progress at once!
