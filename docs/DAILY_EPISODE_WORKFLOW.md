=======
<!-- SSOT Domain: documentation -->

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
# Daily Episode Workflow

**Purpose**: Automate the generation of Digital Dreamscape daily episodes from agent cycle accomplishments

**Date**: 2025-12-22

---

## Overview

The Daily Episode workflow transforms agent work into narrative:

1. **Extract** cycle accomplishments from agent status.json files
2. **Generate** narrative using Ollama (uncensored AI)
3. **Create** blog post for Digital Dreamscape

---

## Workflow Steps

### 1. Extract Cycle Accomplishments

**Tool**: `tools/generate_daily_episode.py`

**What it extracts**:
* Completed tasks from all agents
* Achievements from all agents
* Contract completions
* Coordination activities

**From**: `agent_workspaces/{Agent-X}/status.json`

### 2. Generate Narrative with Ollama

**Model**: Ollama (default: mistral)

**Process**:
* Formats accomplishments for prompt
* Sends to Ollama with narrative prompt
* Receives generated story
* Falls back to template if Ollama unavailable

**Prompt Style**:
* Written as Thea (Narrative + Coherence Authority)
* Narrative, engaging, meaningful
* Shows how execution becomes story
* Digital Dreamscape blog post format

### 3. Create Blog Post

**Location**: `digitaldreamscape.site/blog/XXX-daily-episode-YYYY-MM-DD.md`

**Format**:
* Episode number (auto-incremented)
* Date
* Frontmatter (title, date, episode number)
* Generated narrative content

---

## Usage

### Basic Usage

```bash
cd D:\Agent_Cellphone_V2_Repository
python tools/generate_daily_episode.py
```

### With Date

```bash
python tools/generate_daily_episode.py --date 2025-12-22
```

### With Custom Model

```bash
python tools/generate_daily_episode.py --model llama2
```

### With Custom Paths

```bash
python tools/generate_daily_episode.py \
  --workspaces agent_workspaces \
  --blog-dir D:/websites/websites/digitaldreamscape.site/blog
```

---

## Integration with Cycle Accomplishments

### Quick Start Guide Integration

The Quick Start guides now include cycle accomplishments in the daily operations checklist:

**End of Cycle**:
- [ ] Update status.json with final state
- [ ] Report completions to Captain (A2C)
- [ ] Mark tasks complete in MASTER_TASK_LOG.md
- [ ] **Prepare for next cycle** (status.json ready for extraction)

### Automated Extraction

The tool automatically:
* Scans all agent status.json files
* Extracts accomplishments from the last 24 hours
* Groups by agent
* Formats for narrative generation

---

## Ollama Setup

### Installation

```bash
# Install Ollama
# See: https://ollama.ai

# Pull model
ollama pull mistral
```

### Model Options

* `mistral` (default) - Good balance of quality and speed
* `llama2` - Alternative option
* `llama3` - Latest option
* Custom models as needed

### Fallback

If Ollama is not available, the tool generates a template narrative that:
* Still captures accomplishments
* Maintains blog post format
* Can be enhanced manually

---

## Blog Post Format

### Frontmatter

```yaml
---
title: Daily Episode - YYYY-MM-DD
date: YYYY-MM-DD
episode: XXX
---
```

### Content Structure

1. **Title** - Daily Episode - Date
2. **Introduction** - Narrative hook
3. **Main Story** - Weaved accomplishments
4. **Conclusion** - What this means for Digital Dreamscape

### Example Output

```markdown
---
title: Daily Episode - 2025-12-22
date: 2025-12-22
episode: 006
---

# Daily Episode - 2025-12-22

**Date**: 2025-12-22

---

## The Swarm's Work Becomes Story

Today in the Digital Dreamscape, the Swarm continued building...

[Generated narrative content]

---

*This is how execution becomes narrative. This is how work becomes story. This is the Digital Dreamscape.*
```

---

## Scheduling

### Daily Automation

**Option 1: Cron/Scheduled Task**

```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/repo && python tools/generate_daily_episode.py
```

**Option 2: GitHub Actions**

```yaml
name: Daily Episode
on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Episode
        run: python tools/generate_daily_episode.py
```

**Option 3: Manual**

Run when needed:
```bash
python tools/generate_daily_episode.py
```

---

## Integration Points

### With Canon Automation

* Daily episodes can reference canon events
* Canon extraction can feed into episode generation
* Episodes become part of Digital Dreamscape narrative

### With Agent Work

* Agents update status.json → Accomplishments extracted
* Accomplishments → Narrative generated
* Narrative → Blog post created
* Blog post → Part of Digital Dreamscape story

### With Quick Start Guides

* Quick Start guides codify cycle operations
* Cycle operations → Status updates
* Status updates → Accomplishments
* Accomplishments → Daily episodes

---

## Benefits

### For Victor

* **Automated narrative** - No manual writing needed
* **Daily episodes** - Consistent content generation
* **Story from work** - Real accomplishments become narrative

### For The Swarm

* **Work becomes story** - Accomplishments have narrative weight
* **Automatic recognition** - No need to manually report
* **Canon integration** - Episodes feed into canon

### For Digital Dreamscape

* **Living narrative** - Daily updates keep world alive
* **Real story** - Based on actual work, not fiction
* **Consistent content** - Regular episodes maintain engagement

---

## Future Enhancements

**Potential additions**:
* Image generation for episodes
* Multi-model narrative generation
* Episode quality scoring
* Automatic WordPress publishing
* Episode archive and search
* Integration with canon timeline

---

## Troubleshooting

### Ollama Not Found

**Error**: `FileNotFoundError: ollama`

**Solution**: Install Ollama and ensure it's in PATH

### No Accomplishments Found

**Warning**: `⚠️  No accomplishments found`

**Solution**: Check agent status.json files are updated

### Blog Directory Not Found

**Error**: `FileNotFoundError: blog directory`

**Solution**: Check `--blog-dir` path is correct

---

## Summary

**The Daily Episode workflow**:
1. ✅ Extracts accomplishments from agent work
2. ✅ Generates narrative with Ollama
3. ✅ Creates blog post for Digital Dreamscape
4. ✅ Integrates with Quick Start guides
5. ✅ Automates narrative from execution

**Result**: Daily episodes that transform work into story.

---

*Part of the Digital Dreamscape narrative automation system*

