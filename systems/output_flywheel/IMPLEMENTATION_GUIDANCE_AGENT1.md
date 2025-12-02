# Implementation Guidance for Agent-1

**Date**: 2025-12-02  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **IMPLEMENTATION GUIDE**  
**Priority**: HIGH

---

## 🎯 **PURPOSE**

This document provides exact implementation guidance for Agent-1 to build Phase 2 pipelines and processors cleanly, following V2 compliance and avoiding common pitfalls.

---

## 📋 **EXACT FILE LIST TO CREATE**

### **Pipeline Files** (3 files, <300 lines each):
1. `pipelines/build_artifact.py` - Build → Artifact pipeline (S1-S6)
2. `pipelines/trade_artifact.py` - Trade → Artifact pipeline (T1-T5)
3. `pipelines/life_aria_artifact.py` - Life/Aria → Artifact pipeline

### **Processor Files** (8 files, <300 lines each):
1. `processors/__init__.py` - Exports all processors
2. `processors/base_processor.py` - Abstract base class
3. `processors/repo_scanner.py` - S1: Repo Scan
4. `processors/story_extractor.py` - S2: Story Extraction
5. `processors/readme_generator.py` - S3: README Generation
6. `processors/build_log_generator.py` - S4: Build-log Generation
7. `processors/social_generator.py` - S5: Social Post Generation
8. `processors/trade_processor.py` - T1-T5: Trade Processing

### **Orchestrator File** (1 file, <300 lines):
1. `pipelines/orchestrator.py` - Main entry point for all pipelines

**Total**: 12 files to implement

---

## 🏗️ **RECOMMENDED PATTERNS**

### **Pattern 1: Small Orchestrator Classes + Pure Functions**

**✅ GOOD Example**:
```python
# pipelines/build_artifact.py (<300 lines)
class BuildArtifactPipeline:
    """Orchestrates S1-S6 steps."""
    
    def __init__(self, repo_scanner, story_extractor, ...):
        # Dependency injection - no global imports
        self.repo_scanner = repo_scanner
        self.story_extractor = story_extractor
        # ...
    
    def process(self, work_session: Dict) -> Dict:
        """Main pipeline method - <30 lines."""
        # S1
        repo_data = self.repo_scanner.scan(work_session["source_data"]["repo_path"])
        # S2
        story_data = self.story_extractor.extract(
            repo_data["commits"],
            work_session["source_data"].get("conversations", [])
        )
        # S3-S6 continue...
        return updated_work_session

# processors/story_extractor.py (<300 lines)
class StoryExtractor(BaseProcessor):
    """S2: Extract narrative from commits."""
    
    def extract(self, commits: List[Dict], conversations: List[Dict]) -> Dict:
        """Main extraction method - <30 lines."""
        overview = self._extract_overview(commits)  # Pure function
        features = self._extract_features(commits)  # Pure function
        # ...
        return {"overview": overview, "key_features": features, ...}
    
    def _extract_overview(self, commits: List[Dict]) -> str:
        """Pure function - <30 lines."""
        # Extract overview logic
        pass
```

**Why This Works**:
- Small orchestrator classes (<300 lines) coordinate flow
- Pure functions (<30 lines) contain logic
- Easy to test, maintain, and refactor
- No circular dependencies

---

### **Pattern 2: Dependency Injection**

**✅ GOOD Example**:
```python
# pipelines/orchestrator.py
class PipelineOrchestrator:
    """Main entry point for all pipelines."""
    
    def __init__(self, config_path: str = "systems/output_flywheel/config.yaml"):
        # Load config
        self.config = self._load_config(config_path)
        
        # Initialize processors (dependency injection)
        self.repo_scanner = RepoScanner()
        self.story_extractor = StoryExtractor()
        self.readme_generator = ReadmeGenerator(self.config["outputs"]["artifacts"])
        # ...
        
        # Initialize pipelines with processors
        self.build_pipeline = BuildArtifactPipeline(
            self.repo_scanner,
            self.story_extractor,
            self.readme_generator,
            # ...
        )
    
    def process_session(self, session_path: str) -> Dict:
        """Process work session through appropriate pipeline."""
        work_session = self._load_session(session_path)
        
        if work_session["session_type"] == "build":
            return self.build_pipeline.process(work_session)
        elif work_session["session_type"] == "trade":
            return self.trade_pipeline.process(work_session)
        # ...
```

**Why This Works**:
- No global state
- Easy to test (mock dependencies)
- Clear dependencies
- No circular imports

---

### **Pattern 3: Template Rendering**

**✅ GOOD Example**:
```python
# processors/readme_generator.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class ReadmeGenerator(BaseProcessor):
    """S3: Generate README.md from template."""
    
    def __init__(self, template_dir: str, output_dir: str):
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate(self, repo_data: Dict, story_data: Dict) -> str:
        """Generate README.md - <30 lines."""
        template = self.env.get_template("README.md.j2")
        context = {**repo_data, **story_data}
        content = template.render(context)
        
        output_path = Path(self.output_dir) / f"readme_{repo_data['repo_name']}.md"
        output_path.write_text(content, encoding="utf-8")
        return str(output_path)
```

**Why This Works**:
- Uses existing Jinja2 templates
- Clean separation of data and presentation
- Easy to modify templates without code changes

---

## 🚨 **PITFALLS TO AVOID**

### **❌ Pitfall 1: Tight Coupling to Discord**

**BAD**:
```python
# ❌ DON'T DO THIS
from src.discord_commander import DiscordBot

class SocialGenerator:
    def generate(self, story_data):
        # Directly posts to Discord
        bot = DiscordBot()
        bot.post_message(...)
```

**GOOD**:
```python
# ✅ DO THIS INSTEAD
class SocialGenerator:
    def generate(self, story_data):
        # Generate markdown file only
        # Phase 3 will handle publication
        return self._render_template(story_data)
```

**Why**: Keeps pipelines decoupled from publication. Phase 3 handles publication.

---

### **❌ Pitfall 2: Duplication**

**BAD**:
```python
# ❌ DON'T DUPLICATE LOGIC
class BuildArtifactPipeline:
    def _extract_overview(self, commits):
        # Duplicate logic from StoryExtractor
        pass

class TradeArtifactPipeline:
    def _extract_overview(self, trades):
        # Same logic duplicated
        pass
```

**GOOD**:
```python
# ✅ REUSE PROCESSORS
class BuildArtifactPipeline:
    def __init__(self, story_extractor):
        self.story_extractor = story_extractor  # Reuse
    
    def process(self, session):
        story_data = self.story_extractor.extract(...)
```

**Why**: DRY principle - single source of truth for logic.

---

### **❌ Pitfall 3: Large Functions**

**BAD**:
```python
# ❌ DON'T CREATE 100+ LINE FUNCTIONS
def process_build_session(session):
    # 100+ lines of logic
    # Hard to test, maintain, understand
    pass
```

**GOOD**:
```python
# ✅ BREAK INTO SMALL FUNCTIONS
def process_build_session(session):
    """Orchestrator - <30 lines."""
    repo_data = scan_repo(session["repo_path"])  # <30 lines
    story_data = extract_story(repo_data)  # <30 lines
    readme = generate_readme(repo_data, story_data)  # <30 lines
    return {"artifacts": [readme]}
```

**Why**: V2 compliance, easier testing, better readability.

---

### **❌ Pitfall 4: Circular Dependencies**

**BAD**:
```python
# ❌ DON'T CREATE CIRCULAR IMPORTS
# processors/repo_scanner.py
from pipelines.build_artifact import BuildArtifactPipeline

# pipelines/build_artifact.py
from processors.repo_scanner import RepoScanner
```

**GOOD**:
```python
# ✅ ONE-WAY DEPENDENCIES
# pipelines/build_artifact.py
from processors.repo_scanner import RepoScanner  # OK

# processors/repo_scanner.py
# No imports from pipelines - OK
```

**Why**: Prevents import errors and tight coupling.

---

### **❌ Pitfall 5: Global State**

**BAD**:
```python
# ❌ DON'T USE GLOBAL STATE
config = load_config()  # Global

class RepoScanner:
    def scan(self, path):
        return scan_with_config(path, config)  # Uses global
```

**GOOD**:
```python
# ✅ USE DEPENDENCY INJECTION
class RepoScanner:
    def __init__(self, config):
        self.config = config  # Injected
    
    def scan(self, path):
        return scan_with_config(path, self.config)
```

**Why**: Testable, no hidden dependencies, clear interfaces.

---

## 🔗 **INTEGRATION POINTS**

### **1. End-of-Session Integration**

**How Agents Will Use**:
```python
# In agent end-of-session code
from systems.output_flywheel.pipelines.orchestrator import PipelineOrchestrator

orchestrator = PipelineOrchestrator()
result = orchestrator.process_session("work_session.json")
# result contains updated work_session with artifact paths
```

**Implementation**:
- Create `pipelines/orchestrator.py` as main entry point
- Load work_session.json
- Route to appropriate pipeline based on session_type
- Return updated work_session.json

---

### **2. Agent-5 Monitoring Integration**

**Metrics to Track**:
```python
# In pipeline orchestrator
from systems.output_flywheel.metrics_tracker import MetricsTracker

metrics = MetricsTracker()
metrics.record_artifact_generated("readme", session_id)
metrics.record_pipeline_complete("build_artifact", success=True)
```

**Implementation**:
- Use existing `metrics_tracker.py` (Agent-5 created)
- Call `record_artifact_generated()` after each artifact
- Call `record_pipeline_complete()` after pipeline finishes
- No additional code needed - just call existing methods

---

### **3. Manifest System Integration**

**How to Call**:
```python
# After generating artifacts
from systems.output_flywheel.manifest_system import ManifestSystem

manifest = ManifestSystem()
manifest.add_artifacts(session_id, artifacts)
manifest.mark_ready_for_publication(session_id)
```

**Implementation**:
- Use existing `manifest_system.py` (Agent-8 created)
- Call after all artifacts generated
- No additional code needed - just call existing methods

---

### **4. Publication Queue Integration**

**How to Call**:
```python
# After manifest marks ready
from systems.output_flywheel.publication.publish_queue_manager import PublishQueueManager

queue = PublishQueueManager()
queue.add_to_queue(session_id, artifacts)
```

**Implementation**:
- Use existing `publish_queue_manager.py` (Agent-7 created)
- Call after manifest marks ready
- No additional code needed - just call existing methods

---

## 📊 **TESTING STRATEGY**

### **Unit Tests**:
- Test each processor independently
- Mock dependencies
- Test pure functions with sample data

### **Integration Tests**:
- Test full pipeline with sample work_session.json
- Verify artifacts generated correctly
- Verify manifest updated

### **Example Test**:
```python
def test_build_pipeline():
    # Setup
    repo_scanner = MockRepoScanner()
    story_extractor = MockStoryExtractor()
    pipeline = BuildArtifactPipeline(repo_scanner, story_extractor, ...)
    
    # Execute
    result = pipeline.process(sample_work_session)
    
    # Verify
    assert result["artifacts"]["readme"]["generated"] == True
    assert result["pipeline_status"]["build_artifact"] == "complete"
```

---

## 🎯 **IMPLEMENTATION CHECKLIST**

### **Phase 1: Setup**
- [ ] Create `processors/` directory structure
- [ ] Create `pipelines/` directory structure
- [ ] Create `processors/base_processor.py` (abstract base)
- [ ] Create `processors/__init__.py` (exports)

### **Phase 2: Processors**
- [ ] Implement `RepoScanner` (S1)
- [ ] Implement `StoryExtractor` (S2)
- [ ] Implement `ReadmeGenerator` (S3)
- [ ] Implement `BuildLogGenerator` (S4)
- [ ] Implement `SocialGenerator` (S5)
- [ ] Implement `TradeProcessor` (T1-T5)

### **Phase 3: Pipelines**
- [ ] Implement `BuildArtifactPipeline` (S1-S6)
- [ ] Implement `TradeArtifactPipeline` (T1-T5)
- [ ] Implement `LifeAriaArtifactPipeline`

### **Phase 4: Orchestrator**
- [ ] Implement `PipelineOrchestrator` (main entry point)
- [ ] Integrate with manifest system
- [ ] Integrate with metrics tracker
- [ ] Integrate with publication queue

### **Phase 5: Testing**
- [ ] Unit tests for all processors
- [ ] Integration tests for all pipelines
- [ ] End-to-end test with sample work_session.json

---

## 📝 **CODE QUALITY REQUIREMENTS**

1. **File Size**: <300 lines per file
2. **Function Size**: <30 lines per function
3. **No Circular Dependencies**: One-way imports only
4. **Type Hints**: Use type hints for all functions
5. **Docstrings**: Document all public methods
6. **Error Handling**: Graceful degradation (log errors, continue)

---

## 🔗 **REFERENCES**

- **Architecture**: `ARCHITECTURE_PHASE2_PIPELINES.md`
- **Interfaces**: `pipelines/PIPELINE_INTERFACES.md`
- **Schema**: `schemas/work_session.json`
- **Templates**: `templates/*.j2`
- **Config**: `config.yaml`

---

**Status**: ✅ **IMPLEMENTATION GUIDE COMPLETE**

🐝 **WE. ARE. SWARM. ⚡🔥**

