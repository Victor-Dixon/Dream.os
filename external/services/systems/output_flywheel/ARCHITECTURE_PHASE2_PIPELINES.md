# Dream.OS Output Flywheel v1.0 - Phase 2 Pipeline Architecture

**Date**: 2025-12-02  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **PHASE 2 ARCHITECTURE BLUEPRINT**  
**Priority**: HIGH

---

## 🎯 **OVERVIEW**

Phase 2 implements the core pipelines and processors that transform `work_session.json` into artifacts. This architecture ensures clean implementation, SSOT compliance, and seamless integration with Phase 3 publication.

---

## 📊 **DATA FLOW ARCHITECTURE**

```
work_session.json (input)
    ↓
Pipeline Orchestrator
    ↓
Processors (S1-S6 or T1-T5)
    ↓
Artifact Generation (templates + data)
    ↓
Artifacts (markdown files)
    ↓
Manifest System (SSOT tracking)
    ↓
publish_queue (JSON files)
    ↓
Phase 3 Publication (Agent-7)
```

---

## 🔄 **PIPELINE ARCHITECTURE**

### **1. Build → Artifact Pipeline**

**File**: `pipelines/build_artifact.py`  
**Class**: `BuildArtifactPipeline`  
**Max Lines**: <300

**Flow**:
```
S1: RepoScanner.scan() → repo_data
    ↓
S2: StoryExtractor.extract() → narrative_data
    ↓
S3: ReadmeGenerator.generate() → README.md
    ↓
S4: BuildLogGenerator.generate() → build-log.md
    ↓
S5: SocialGenerator.generate() → social_post.md
    ↓
S6: ManifestSystem.mark_ready() → publish_queue entry
```

**Input**: `work_session.json` with `session_type: "build"`  
**Output**: Updated `work_session.json` with artifact paths + manifest entry

---

### **2. Trade → Artifact Pipeline**

**File**: `pipelines/trade_artifact.py`  
**Class**: `TradeArtifactPipeline`  
**Max Lines**: <300

**Flow**:
```
T1: TradeProcessor.normalize() → normalized_trades
    ↓
T2: TradeProcessor.summarize() → session_summary
    ↓
T3: TradeProcessor.extract_lessons() → lessons_learned
    ↓
T4: TradeJournalGenerator.generate() → trade_journal.md
    ↓
T5: SocialGenerator.generate_trade_thread() → social_trade_thread.md
    ↓
ManifestSystem.mark_ready() → publish_queue entry
```

**Input**: `work_session.json` with `session_type: "trade"`  
**Output**: Updated `work_session.json` with artifact paths + manifest entry

---

### **3. Life/Aria → Artifact Pipeline**

**File**: `pipelines/life_aria_artifact.py`  
**Class**: `LifeAriaArtifactPipeline`  
**Max Lines**: <300

**Flow**:
```
Extract session data → session_data
    ↓
DevlogGenerator.generate() → devlog_entry.md
    ↓
ScreenshotGalleryGenerator.generate() → screenshot_notes.md
    ↓
SocialGenerator.generate() → social_post.md
    ↓
ManifestSystem.mark_ready() → publish_queue entry
```

**Input**: `work_session.json` with `session_type: "life_aria"`  
**Output**: Updated `work_session.json` with artifact paths + manifest entry

---

## 🔧 **PROCESSOR ARCHITECTURE**

### **Processor Base Pattern**

All processors follow this pattern:
- **Pure functions** where possible (<30 lines each)
- **Small orchestrator classes** (<200 lines)
- **No circular dependencies**
- **V2 compliance**: <300 lines/file, <30 lines/function

### **Processors Directory Structure**

```
processors/
├── __init__.py                 # Exports
├── base_processor.py           # Base class (abstract)
├── repo_scanner.py             # S1: Repo Scan
├── story_extractor.py          # S2: Story Extraction
├── readme_generator.py         # S3: README Generation
├── build_log_generator.py      # S4: Build-log Generation
├── social_generator.py         # S5: Social Post Generation
└── trade_processor.py          # T1-T5: Trade Processing
```

---

### **1. RepoScanner (S1)**

**File**: `processors/repo_scanner.py`  
**Class**: `RepoScanner`  
**Function**: `scan(repo_path: str) -> Dict[str, Any]`

**Responsibilities**:
- Analyze repo structure (files, directories)
- Extract git commits (last N commits)
- Calculate stats (files changed, lines added/removed)
- Identify project type (Python, JS, etc.)

**Output**:
```python
{
    "repo_name": str,
    "repo_path": str,
    "structure": {...},
    "commits": [...],
    "stats": {
        "files_changed": int,
        "lines_added": int,
        "lines_removed": int,
        "commits": int
    },
    "project_type": str
}
```

---

### **2. StoryExtractor (S2)**

**File**: `processors/story_extractor.py`  
**Class**: `StoryExtractor`  
**Function**: `extract(commits: List, conversations: List) -> Dict[str, Any]`

**Responsibilities**:
- Extract narrative from commit messages
- Extract insights from conversations
- Identify key features/changes
- Generate overview text

**Output**:
```python
{
    "overview": str,
    "key_features": List[str],
    "problem": str,
    "solution": str,
    "lessons": List[str]
}
```

---

### **3. ReadmeGenerator (S3)**

**File**: `processors/readme_generator.py`  
**Class**: `ReadmeGenerator`  
**Function**: `generate(repo_data: Dict, story_data: Dict, template_path: str) -> str`

**Responsibilities**:
- Load Jinja2 template
- Render template with data
- Write to repo root (or output path)
- Return artifact path

**Output**: Path to generated README.md

---

### **4. BuildLogGenerator (S4)**

**File**: `processors/build_log_generator.py`  
**Class**: `BuildLogGenerator`  
**Function**: `generate(repo_data: Dict, session_data: Dict) -> str`

**Responsibilities**:
- Generate build-log markdown
- Include commit history
- Include file changes
- Include build/test results (if available)

**Output**: Path to generated build-log.md

---

### **5. SocialGenerator (S5)**

**File**: `processors/social_generator.py`  
**Class**: `SocialGenerator`  
**Function**: `generate(story_data: Dict, template_path: str, platform: str) -> str`

**Responsibilities**:
- Generate social post from story
- Format for platform (Twitter, LinkedIn, etc.)
- Create thread if needed
- Return artifact path

**Output**: Path to generated social_post.md

---

### **6. TradeProcessor (T1-T5)**

**File**: `processors/trade_processor.py`  
**Class**: `TradeProcessor`  
**Functions**:
- `normalize(trades: List) -> List[Dict]`
- `summarize(trades: List) -> Dict`
- `extract_lessons(trades: List, summary: Dict) -> List[str]`

**Responsibilities**:
- Normalize trade data format
- Summarize trading session
- Extract lessons learned
- Calculate performance metrics

**Output**: Normalized trades, summary, lessons

---

## 🔗 **INTEGRATION POINTS**

### **End-of-Session Integration**

**How Agents Use Output Flywheel**:
1. Agent completes work session
2. Agent assembles `work_session.json` with session data
3. Agent calls: `run_output_flywheel.py --session-file work_session.json`
4. Pipeline processes session → generates artifacts
5. Artifacts added to manifest + publish_queue
6. Agent continues with next task

**Integration Pattern**:
```python
# In agent end-of-session code
from systems.output_flywheel.pipelines import PipelineOrchestrator

orchestrator = PipelineOrchestrator()
result = orchestrator.process_session(work_session_path)
# result contains artifact paths and status
```

---

### **Agent-5 Monitoring Integration**

**Monitoring Points**:
1. **Session Processing**: Track sessions processed per agent
2. **Artifact Generation**: Track artifacts generated per type
3. **Pipeline Success Rate**: Track pipeline completion rates
4. **Publication Rate**: Track artifacts published vs. generated

**Metrics Collected**:
- `artifacts_per_week`: Total artifacts generated
- `repos_with_clean_readmes`: Repos with updated READMEs
- `trading_days_documented`: Trading days with journal entries
- `publication_rate`: Percentage of artifacts published
- `pipeline_success_rate`: Percentage of successful pipeline runs

**Integration**:
```python
# In pipeline orchestrator
from systems.output_flywheel.metrics_tracker import MetricsTracker

metrics = MetricsTracker()
metrics.record_artifact_generated(artifact_type, session_id)
metrics.record_pipeline_complete(pipeline_type, success=True)
```

---

### **Feedback Collection for v1.1**

**Feedback Points**:
1. **Agent Feedback**: Agents provide feedback after using flywheel
2. **Artifact Quality**: Track artifact quality metrics
3. **Pipeline Performance**: Track processing time, errors
4. **Usage Patterns**: Track which pipelines are used most

**Feedback Collection**:
```python
# Feedback structure
{
    "session_id": str,
    "agent_id": str,
    "pipeline_type": str,
    "feedback": {
        "artifact_quality": int,  # 1-5
        "processing_time": float,
        "issues": List[str],
        "suggestions": List[str]
    },
    "timestamp": str
}
```

**Storage**: `systems/output_flywheel/outputs/feedback/feedback_*.json`

---

## 📋 **MANIFEST SYSTEM INTEGRATION**

**Purpose**: SSOT tracking of all artifacts (Agent-8 responsibility)

**Integration**:
```python
from systems.output_flywheel.manifest_system import ManifestSystem

manifest = ManifestSystem()
manifest.add_artifact(session_id, artifact_type, artifact_path)
manifest.mark_ready_for_publication(session_id)
```

**Manifest Entry**:
```json
{
    "session_id": "uuid",
    "artifacts": [
        {
            "type": "readme",
            "path": "outputs/artifacts/readme_xxx.md",
            "status": "ready",
            "generated_at": "ISO 8601"
        }
    ],
    "ready_for_publication": true
}
```

---

## 🚨 **V2 COMPLIANCE CONSTRAINTS**

### **File Size Limits**
- **Pipeline files**: <300 lines
- **Processor files**: <300 lines
- **Functions**: <30 lines each

### **Architecture Rules**
- **No circular dependencies**: Processors don't import pipelines
- **Pure functions preferred**: Processors use pure functions where possible
- **Small orchestrator classes**: Pipeline classes orchestrate, don't implement logic
- **Dependency injection**: Pass dependencies, don't import globally

### **Pattern Example**:
```python
# ✅ GOOD: Small orchestrator + pure functions
class BuildArtifactPipeline:
    def __init__(self, repo_scanner, story_extractor, ...):
        self.repo_scanner = repo_scanner
        # ...
    
    def process(self, session: Dict) -> Dict:
        repo_data = self.repo_scanner.scan(session["source_data"]["repo_path"])
        story_data = self.story_extractor.extract(...)
        # ...

# ✅ GOOD: Pure function
def extract_overview(commits: List[Dict]) -> str:
    """Extract overview from commits."""
    # <30 lines of logic
    return overview
```

---

## 🔄 **PUBLICATION QUEUE INTEGRATION**

**Purpose**: Queue artifacts for Phase 3 publication (Agent-7)

**Integration**:
```python
from systems.output_flywheel.publication.publish_queue_manager import PublishQueueManager

queue = PublishQueueManager()
queue.add_to_queue(session_id, artifacts)
```

**Queue Entry**:
```json
{
    "session_id": "uuid",
    "artifacts": [
        {
            "type": "readme",
            "path": "outputs/artifacts/readme_xxx.md",
            "target": "github",
            "status": "pending"
        }
    ],
    "created_at": "ISO 8601"
}
```

---

## 📊 **ERROR HANDLING**

**Pattern**: Graceful degradation
- If processor fails, log error and continue
- Mark failed artifacts in work_session.json
- Don't block entire pipeline

**Error Structure**:
```python
{
    "processor": "RepoScanner",
    "error": "str",
    "session_id": "uuid",
    "timestamp": "ISO 8601"
}
```

---

## 🎯 **NEXT STEPS FOR AGENT-1**

1. **Create Pipeline Files**: `build_artifact.py`, `trade_artifact.py`, `life_aria_artifact.py`
2. **Create Processor Files**: All 6 processor files
3. **Implement Base Processor**: Abstract base class
4. **Create Pipeline Orchestrator**: Main entry point
5. **Integrate with Manifest System**: Use existing manifest_system.py
6. **Integrate with Metrics**: Use existing metrics_tracker.py

**See**: `pipelines/PIPELINE_INTERFACES.md` for detailed interfaces

---

**Status**: ✅ **PHASE 2 ARCHITECTURE BLUEPRINT COMPLETE**

🐝 **WE. ARE. SWARM. ⚡🔥**

