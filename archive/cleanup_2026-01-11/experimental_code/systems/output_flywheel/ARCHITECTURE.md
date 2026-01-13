# Dream.OS Output Flywheel v1.0 - System Architecture

**Date**: 2025-12-01  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **PHASE 1 SCAFFOLDING**  
**Priority**: HIGH

---

## 🎯 **SYSTEM OVERVIEW**

The Output Flywheel automatically transforms meaningful work sessions into public, monetizable artifacts:
- **Portfolio artifacts** (GitHub/README/demo)
- **Written artifacts** (blog/journal)
- **Social artifacts** (tweet/thread/short-form script)

---

## 📁 **DIRECTORY STRUCTURE**

```
systems/output_flywheel/
├── ARCHITECTURE.md              # This file
├── config.yaml                  # Configuration (source paths, output paths, toggles)
├── schemas/
│   └── work_session.json        # Work session schema definition
├── templates/
│   ├── README.md.j2             # README template (Jinja2)
│   ├── blog_post.md.j2          # Blog/journal template
│   ├── social_post.md.j2        # Social post template
│   └── trade_journal.md.j2      # Trade journal template
├── pipelines/
│   ├── build_artifact.py        # Build → Artifact pipeline (S1-S6)
│   ├── trade_artifact.py        # Trade → Artifact pipeline (T1-T5)
│   └── life_aria_artifact.py    # Life/Aria → Artifact pipeline
├── processors/
│   ├── repo_scanner.py          # S1: Repo Scan
│   ├── story_extractor.py       # S2: Story Extraction
│   ├── readme_generator.py      # S3: README Generation
│   ├── build_log_generator.py   # S4: Build-log Generation
│   ├── social_generator.py      # S5: Social Post Generation
│   └── trade_processor.py       # T1-T5: Trade Processing
└── outputs/
    ├── artifacts/               # Generated artifacts
    ├── publish_queue/           # PUBLISH_QUEUE JSON files
    └── sessions/                # work_session.json files
```

---

## 📊 **WORK SESSION SCHEMA**

### **work_session.json Structure**

```json
{
  "session_id": "uuid",
  "session_type": "build|trade|life_aria",
  "timestamp": "ISO 8601",
  "agent_id": "Agent-X",
  "metadata": {
    "duration_minutes": 120,
    "files_changed": 15,
    "commits": 3,
    "trades_executed": 2
  },
  "source_data": {
    "repo_path": "/path/to/repo",
    "git_commits": [...],
    "trades": [...],
    "conversations": [...]
  },
  "artifacts": {
    "readme": {
      "generated": true,
      "path": "outputs/artifacts/readme_xxx.md",
      "status": "ready|published"
    },
    "blog_post": {
      "generated": true,
      "path": "outputs/artifacts/blog_xxx.md",
      "status": "ready|published"
    },
    "social_post": {
      "generated": true,
      "path": "outputs/artifacts/social_xxx.md",
      "status": "ready|published"
    },
    "trade_journal": {
      "generated": true,
      "path": "outputs/artifacts/trade_xxx.md",
      "status": "ready|published"
    }
  },
  "pipeline_status": {
    "build_artifact": "complete|pending|failed",
    "trade_artifact": "complete|pending|failed",
    "life_aria_artifact": "complete|pending|failed"
  }
}
```

---

## 🔄 **PIPELINE FLOW ARCHITECTURE**

### **1. Build → Artifact Pipeline**

**Trigger**: New repo OR substantial change OR new feature

**Steps**:
- **S1: Repo Scan** → Analyze repo structure, commits, files
- **S2: Story Extraction** → Extract narrative from commits/conversations
- **S3: README Generation** → Generate/update README.md
- **S4: Build-log Generation** → Create build-log file
- **S5: Social Post Generation** → Create social post outline
- **S6: Mark Ready** → Add to PUBLISH_QUEUE

**Outputs**:
- `README.md` (updated)
- `build-log.md`
- `social_post_outline.md`

---

### **2. Trade → Artifact Pipeline**

**Trigger**: Trading session with ≥1 executed trade

**Steps**:
- **T1: Normalize** → Normalize trade data format
- **T2: Summarize** → Summarize trading session
- **T3: Extract Lessons** → Extract key lessons learned
- **T4: Journal** → Generate trading journal entry
- **T5: Social** → Generate social trade thread

**Outputs**:
- `trading_journal_YYYY-MM-DD.md`
- `social_trade_thread.md`

---

### **3. Life/Aria → Artifact Pipeline**

**Trigger**: New game/website/session built with Aria

**Steps**:
- Extract session data
- Generate devlog entry
- Create screenshot gallery notes
- Generate social post

**Outputs**:
- `devlog_entry.md`
- `screenshot_gallery_notes.md`
- `social_post.md`

---

## ⚙️ **CONFIGURATION ARCHITECTURE**

### **config.yaml Structure**

```yaml
# Source Paths
sources:
  repos:
    - path: "D:/Agent_Cellphone_V2_Repository"
      watch: true
    - path: "D:/DreamVault"
      watch: false
  trading_data:
    path: "trading_robot/logs"
  conversations:
    path: "swarm_brain/conversations"

# Output Paths
outputs:
  artifacts: "systems/output_flywheel/outputs/artifacts"
  publish_queue: "systems/output_flywheel/outputs/publish_queue"
  sessions: "systems/output_flywheel/outputs/sessions"

# Toggles
features:
  auto_generate_readme: true
  auto_generate_blog: true
  auto_generate_social: true
  auto_generate_trade_journal: true
  auto_publish: false  # Manual review first

# Pipeline Triggers
triggers:
  build_artifact:
    - "new_repo"
    - "substantial_change"  # >10 files changed
    - "new_feature"  # Major feature commit
  trade_artifact:
    - "trades_executed"  # ≥1 trade
  life_aria_artifact:
    - "new_game"
    - "new_website"
    - "aria_session"

# Output Formats
formats:
  readme:
    style: "professional"
    include_badges: true
    include_demo: true
  blog_post:
    style: "narrative"
    include_code_snippets: true
    include_screenshots: true
  social_post:
    platform: "twitter"
    max_length: 280
    include_thread: true
  trade_journal:
    style: "analytical"
    include_charts: true
    include_lessons: true
```

---

## 🔌 **INTEGRATION POINTS**

### **Agent Integration**
- Agents assemble `work_session.json` at end-of-session
- Integration with existing agent status system
- Session manifest system for tracking

### **Publication Integration**
- PUBLISH_QUEUE JSON format
- GitHub publication automation
- Website publication (markdown → HTML)
- Social post draft system

---

## 📊 **METRICS & TRACKING**

### **Key Metrics**
- `artifacts_per_week`: Number of artifacts generated
- `repos_with_clean_readmes`: Repos with updated READMEs
- `trading_days_documented`: Trading days with journal entries
- `publication_rate`: Percentage of artifacts published

---

## 🎯 **NEXT STEPS**

1. ✅ System architecture designed
2. ⏳ Create templates (README, blog, social, trade journal)
3. ⏳ Create config.yaml with all settings
4. ⏳ Implement pipeline processors
5. ⏳ Create CLI entry-point

---

**Status**: ✅ **ARCHITECTURE DESIGN COMPLETE**

🐝 **WE. ARE. SWARM. ⚡🔥**

