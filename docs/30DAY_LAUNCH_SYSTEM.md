# 30-Day Launch System Guide

## Overview

The **DaDudeKC 30-Day Launch System** is designed to get your first paying clients and establish a repeatable lead flow in 30 days.

**Goal**: Get first paying clients + repeatable lead flow

## Quick Start

### 1. Initialize the Program

```bash
python tools/30day_launch_system.py --init
```

This creates your tracking file at `.deploy_credentials/30day_launch_tracker.json`

### 2. View Today's Tasks

```bash
python tools/30day_launch_system.py --tasks
```

### 3. Track Your Progress

```bash
# View progress report
python tools/30day_launch_system.py --progress

# Update metrics (e.g., sent 10 DMs)
python tools/30day_launch_system.py --update dms:10

# Update calls
python tools/30day_launch_system.py --update calls:2
```

### 4. Get DM Script

```bash
python tools/30day_launch_system.py --dm-script
```

### 5. Publish Blog Posts (Days 8, 11, 18, 23)

```bash
python tools/30day_launch_system.py --publish-blog 8 "Blog Post Title" path/to/content.md
```

### 6. Advance to Next Day

```bash
python tools/30day_launch_system.py --advance
```

## Program Structure

### Week 1: Foundation
- **Days 1-7**: Setup, packages, website, initial content
- **Focus**: Get everything ready to launch

### Week 2: Leads
- **Days 8-14**: Daily outreach + blog posts
- **Focus**: Generate leads and book consults

### Week 3: Systemize
- **Days 15-21**: Create SOPs, follow-ups, proof
- **Focus**: Make processes repeatable

### Week 4: Scale
- **Days 22-30**: Ads, partnerships, batch content
- **Focus**: Scale what's working

## Weekly Targets

- **DMs**: 70 per week
- **Calls**: 10 per week
- **Consults**: 5 per week
- **Deposits**: 2 per week

## Blog Post Schedule

Automated blog posts are scheduled for:
- **Day 8**: Blog post #1
- **Day 11**: Blog post #2
- **Day 18**: Blog post #3
- **Day 23**: Blog post #4

All blog posts are automatically published to `crosbyultimateevents.com` via the blogging API.

## DM Script Template

**Opener**: "Yo quick question—what do you do + how are you currently getting customers?"

**Diagnose**: "What have you tried? What's working even a little?"

**Pitch**: "I can package this into 3 tiers + build your site + give you a 30-day play to get your first paying clients."

**Close**: "Want me to draft your packages today? I'll send a quick blueprint."

## Daily Workflow

1. **Morning**: Check today's tasks (`--tasks`)
2. **Throughout Day**: Update metrics as you complete activities (`--update`)
3. **Evening**: Review progress (`--progress`)
4. **End of Day**: Advance to next day (`--advance`)

## Integration with Blogging API

The system is integrated with the unified blogging automation tool. Blog posts scheduled for days 8, 11, 18, and 23 can be published directly to your WordPress site using:

```bash
python tools/30day_launch_system.py --publish-blog [DAY] "[TITLE]" [CONTENT_FILE]
```

The content file can be Markdown or HTML. The system will automatically:
- Convert Markdown to HTML if needed
- Publish to the configured site (default: `crosbyultimateevents.com`)
- Track publication status in the tracker

## Tips

1. **Batch Similar Tasks**: Group similar activities together (e.g., all DMs in one block)
2. **Track in Real-Time**: Update metrics as you go, not at the end of the day
3. **Use Templates**: Save time with the DM script template
4. **Review Weekly**: Use weekly reviews to adjust strategy
5. **Collect Proof**: Screenshot wins, testimonials, and results as you go

## Troubleshooting

### Blog Post Publishing Fails

1. Check WordPress credentials in `.deploy_credentials/blogging_api.json`
2. Test connectivity: `python tools/test_blogging_api_connectivity.py --site crosbyultimateevents.com`
3. Ensure WordPress REST API is enabled on your site

### Progress Not Saving

- Check file permissions on `.deploy_credentials/30day_launch_tracker.json`
- Ensure the `.deploy_credentials` directory exists

## Next Steps After 30 Days

On day 30, you'll review:
- Total clients acquired
- Revenue generated
- What worked best
- What to improve
- Next 30-day goals

---

**Remember**: Consistency beats perfection. Focus on completing tasks daily rather than making everything perfect.
