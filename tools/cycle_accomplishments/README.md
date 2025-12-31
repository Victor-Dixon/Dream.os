# Cycle Accomplishments Report Generator

Modular implementation combining best features from v1.0 and v2.0.

**Protocol:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0  
**Protocol Status:** ACTIVE  
**Protocol Documentation:** [docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md](../../docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md)  
**Author:** Agent-7 (Web Development Specialist)  
**Date:** 2025-12-30  
**V2 Compliant:** Yes  
**SSOT Domain:** tools

## Features

- ✅ **Comprehensive Reports**: Detailed markdown reports with all agent accomplishments
- ✅ **Blog Post Generation**: Victor-voiced narrative blog posts for autoblogger
- ✅ **Enhanced Discord Posting**: Chunked messages + file uploads
- ✅ **Block Status**: Includes Swarm Phase 3 block status from MASTER_TASK_LOG.md
- ✅ **Active Tasks Grouping**: Groups active tasks by status
- ✅ **Cross-Platform**: Works on Windows, Linux, and macOS
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Type Hints**: Full type annotation support

## Usage

### Basic Usage (All Features)

```bash
python -m tools.cycle_accomplishments.main
```

This will:
1. Collect status from all agents (Agent-1 through Agent-8)
2. Generate comprehensive markdown report
3. Generate Victor-voiced blog post
4. Post summary, per-agent details, and full report file to Discord (Agent-4 channel)

### Options

```bash
# Skip blog post generation
python -m tools.cycle_accomplishments.main --no-blog

# Skip Discord posting
python -m tools.cycle_accomplishments.main --no-discord

# Skip per-agent details in Discord (summary and file only)
python -m tools.cycle_accomplishments.main --no-details

# Skip file upload to Discord (summary and details only)
python -m tools.cycle_accomplishments.main --no-file

# Specify workspace root
python -m tools.cycle_accomplishments.main --workspace-root /path/to/workspace

# Post to different agent channel
python -m tools.cycle_accomplishments.main --agent-id Agent-5
```

## Module Structure

```
tools/cycle_accomplishments/
├── __init__.py           # Package initialization
├── data_collector.py     # Collect agent status from workspaces
├── report_generator.py   # Generate markdown reports
├── blog_generator.py     # Generate Victor-voiced blog posts
├── discord_poster.py     # Handle Discord posting
├── main.py              # CLI entrypoint
└── README.md            # This file
```

## Output Files

### Report
- **Location:** `reports/cycle_accomplishments_YYYYMMDD_HHMMSS.md`
- **Format:** Markdown
- **Content:** Comprehensive agent accomplishments, active tasks, block status

### Blog Post
- **Location:** `docs/blog/cycle_accomplishments_YYYY-MM-DD.md`
- **Format:** Markdown with frontmatter
- **Content:** Victor-voiced narrative version for autoblogger

## Migration from Old Implementations

### From `generate_cycle_accomplishments_report.py` (v1.0)

**Old:**
```bash
python tools/generate_cycle_accomplishments_report.py
```

**New:**
```bash
python -m tools.cycle_accomplishments.main
```

**Changes:**
- Blog post generation now included (use `--no-blog` to skip)
- Enhanced Discord posting (chunked + file upload)
- More detailed reports (20 tasks vs 10, 15 achievements vs 5)

### From `unified_cycle_accomplishments_report.py` (v2.0)

**Old:**
```bash
python tools/unified_cycle_accomplishments_report.py
```

**New:**
```bash
python -m tools.cycle_accomplishments.main
```

**Changes:**
- Fixed hardcoded `/workspace` path (now uses relative paths)
- Added block status from MASTER_TASK_LOG.md
- Added active tasks grouping by status
- Better modular architecture

## Dependencies

- `pathlib` (standard library)
- `json` (standard library)
- `datetime` (standard library)
- `yaml` (for voice profile loading)
- `tools.categories.communication_tools.DiscordRouterPoster` (for Discord posting)

## Protocol

**Version:** 2.0  
**Protocol Name:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION  
**Protocol Status:** ACTIVE  
**Full Documentation:** [docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md](../../docs/CYCLE_ACCOMPLISHMENTS_REPORT_PROTOCOL.md)

This implementation follows the Cycle Accomplishments Report Protocol v2.0, which defines:
- Standard process for generating cycle summaries
- Data sources and output formats
- Discord posting integration
- Error handling requirements
- Protocol compliance standards

### Data Sources

- `agent_workspaces/Agent-{1-8}/status.json` - Agent status files
- `MASTER_TASK_LOG.md` - Block status (if available)
- `config/voice_profiles/victor_voice_profile.yaml` - Voice profile for blog posts

### Output Channels

- **Reports:** `reports/` directory
- **Blog Posts:** `docs/blog/` directory
- **Discord:** Agent-4 channel (configurable via `--agent-id`)

## V2 Compliance

✅ All modules are V2 compliant:
- Functions under 30 lines
- Files under 400 lines
- Clear separation of concerns
- Type hints included
- Proper error handling

## Troubleshooting

### Discord Posting Not Available

If you see `⚠️  Discord posting not available`, ensure:
- `tools.categories.communication_tools.DiscordRouterPoster` is importable
- Discord credentials are configured

### Voice Profile Not Found

If blog posts don't use Victor voice:
- Check that `config/voice_profiles/victor_voice_profile.yaml` exists
- Blog will still generate but with basic lowercase transformation

### No Agent Status Found

If no agents are found:
- Verify `agent_workspaces/Agent-{1-8}/status.json` files exist
- Check workspace root path (use `--workspace-root` if needed)

## License

Part of the Agent Cellphone V2 Repository.

