# Pipeline & Processor Interface Contracts

**Date**: 2025-12-02  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **INTERFACE SPECIFICATION**  
**Priority**: HIGH

---

## 🎯 **PURPOSE**

This document defines the exact interface contracts, type signatures, and pseudo-code for all pipelines and processors. Agent-1 will implement these interfaces.

---

## 📋 **BASE INTERFACES**

### **BaseProcessor (Abstract)**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseProcessor(ABC):
    """Base class for all processors."""
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return result."""
        pass
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data. Returns True if valid."""
        # Default implementation
        return True
```

---

## 🔧 **PROCESSOR INTERFACES**

### **1. RepoScanner**

**File**: `processors/repo_scanner.py`

```python
from typing import Dict, Any, List
from pathlib import Path

class RepoScanner(BaseProcessor):
    """S1: Scan repository structure and extract metadata."""
    
    def scan(self, repo_path: str) -> Dict[str, Any]:
        """
        Scan repository and extract metadata.
        
        Args:
            repo_path: Path to repository root
            
        Returns:
            {
                "repo_name": str,
                "repo_path": str,
                "structure": Dict,
                "commits": List[Dict],
                "stats": {
                    "files_changed": int,
                    "lines_added": int,
                    "lines_removed": int,
                    "commits": int
                },
                "project_type": str
            }
        """
        # Pseudo-code:
        # 1. Get repo name from path
        # 2. Scan directory structure (files, dirs)
        # 3. Get git commits (last 10-20 commits)
        # 4. Calculate stats from commits
        # 5. Detect project type (Python, JS, etc.)
        # 6. Return structured data
        pass
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface method - calls scan()."""
        repo_path = data.get("repo_path")
        return self.scan(repo_path)
```

---

### **2. StoryExtractor**

**File**: `processors/story_extractor.py`

```python
from typing import Dict, Any, List

class StoryExtractor(BaseProcessor):
    """S2: Extract narrative story from commits and conversations."""
    
    def extract(
        self,
        commits: List[Dict[str, Any]],
        conversations: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract narrative story from source data.
        
        Args:
            commits: List of commit dictionaries
            conversations: Optional list of conversation dictionaries
            
        Returns:
            {
                "overview": str,
                "key_features": List[str],
                "problem": str,
                "solution": str,
                "lessons": List[str]
            }
        """
        # Pseudo-code:
        # 1. Parse commit messages for features/changes
        # 2. Extract problem statements from conversations
        # 3. Identify solution patterns
        # 4. Generate overview text
        # 5. Extract lessons learned
        # 6. Return structured narrative
        pass
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface method - calls extract()."""
        commits = data.get("commits", [])
        conversations = data.get("conversations", [])
        return self.extract(commits, conversations)
```

---

### **3. ReadmeGenerator**

**File**: `processors/readme_generator.py`

```python
from typing import Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class ReadmeGenerator(BaseProcessor):
    """S3: Generate README.md from template and data."""
    
    def __init__(self, template_dir: str = "systems/output_flywheel/templates"):
        """Initialize with template directory."""
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate(
        self,
        repo_data: Dict[str, Any],
        story_data: Dict[str, Any],
        output_path: str = None
    ) -> str:
        """
        Generate README.md from template.
        
        Args:
            repo_data: Output from RepoScanner
            story_data: Output from StoryExtractor
            output_path: Optional output path (default: repo root)
            
        Returns:
            Path to generated README.md
        """
        # Pseudo-code:
        # 1. Load README.md.j2 template
        # 2. Merge repo_data + story_data into template context
        # 3. Render template
        # 4. Write to output_path (or repo root)
        # 5. Return file path
        pass
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface method - calls generate()."""
        repo_data = data.get("repo_data")
        story_data = data.get("story_data")
        output_path = data.get("output_path")
        path = self.generate(repo_data, story_data, output_path)
        return {"readme_path": path}
```

---

### **4. BuildLogGenerator**

**File**: `processors/build_log_generator.py`

```python
from typing import Dict, Any
from pathlib import Path

class BuildLogGenerator(BaseProcessor):
    """S4: Generate build-log.md file."""
    
    def generate(
        self,
        repo_data: Dict[str, Any],
        session_data: Dict[str, Any]
    ) -> str:
        """
        Generate build-log.md file.
        
        Args:
            repo_data: Output from RepoScanner
            session_data: Work session data
            
        Returns:
            Path to generated build-log.md
        """
        # Pseudo-code:
        # 1. Extract commit history from repo_data
        # 2. Extract file changes from session_data
        # 3. Format as markdown
        # 4. Write to outputs/artifacts/build-log_xxx.md
        # 5. Return file path
        pass
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface method - calls generate()."""
        repo_data = data.get("repo_data")
        session_data = data.get("session_data")
        path = self.generate(repo_data, session_data)
        return {"build_log_path": path}
```

---

### **5. SocialGenerator**

**File**: `processors/social_generator.py`

```python
from typing import Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class SocialGenerator(BaseProcessor):
    """S5: Generate social post from story data."""
    
    def __init__(self, template_dir: str = "systems/output_flywheel/templates"):
        """Initialize with template directory."""
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate(
        self,
        story_data: Dict[str, Any],
        platform: str = "twitter",
        template_path: str = "social_post.md.j2"
    ) -> str:
        """
        Generate social post from story.
        
        Args:
            story_data: Output from StoryExtractor
            platform: Target platform (twitter, linkedin, etc.)
            template_path: Template file path
            
        Returns:
            Path to generated social_post.md
        """
        # Pseudo-code:
        # 1. Load social_post.md.j2 template
        # 2. Format story_data for platform (character limits, etc.)
        # 3. Create thread if needed (split into multiple posts)
        # 4. Render template
        # 5. Write to outputs/artifacts/social_xxx.md
        # 6. Return file path
        pass
    
    def generate_trade_thread(
        self,
        trade_data: Dict[str, Any],
        platform: str = "twitter"
    ) -> str:
        """
        Generate trade thread for social media.
        
        Args:
            trade_data: Normalized trade data
            platform: Target platform
            
        Returns:
            Path to generated social_trade_thread.md
        """
        # Pseudo-code:
        # 1. Format trade summary for thread
        # 2. Create thread posts (one per trade or summary)
        # 3. Add hashtags and mentions
        # 4. Write to outputs/artifacts/social_trade_xxx.md
        # 5. Return file path
        pass
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface method - calls generate()."""
        story_data = data.get("story_data")
        platform = data.get("platform", "twitter")
        path = self.generate(story_data, platform)
        return {"social_post_path": path}
```

---

### **6. TradeProcessor**

**File**: `processors/trade_processor.py`

```python
from typing import Dict, Any, List

class TradeProcessor(BaseProcessor):
    """T1-T5: Process trading session data."""
    
    def normalize(self, trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        T1: Normalize trade data format.
        
        Args:
            trades: Raw trade data from session
            
        Returns:
            List of normalized trade dictionaries
        """
        # Pseudo-code:
        # 1. Validate trade data structure
        # 2. Normalize field names (symbol, action, quantity, price)
        # 3. Calculate derived fields (profit_loss, timestamp)
        # 4. Return normalized list
        pass
    
    def summarize(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        T2: Summarize trading session.
        
        Args:
            trades: Normalized trade data
            
        Returns:
            {
                "total_trades": int,
                "total_pnl": float,
                "win_rate": float,
                "best_trade": Dict,
                "worst_trade": Dict
            }
        """
        # Pseudo-code:
        # 1. Calculate total P&L
        # 2. Calculate win rate
        # 3. Find best/worst trades
        # 4. Return summary dictionary
        pass
    
    def extract_lessons(
        self,
        trades: List[Dict[str, Any]],
        summary: Dict[str, Any]
    ) -> List[str]:
        """
        T3: Extract lessons learned from trading session.
        
        Args:
            trades: Normalized trade data
            summary: Summary from summarize()
            
        Returns:
            List of lesson strings
        """
        # Pseudo-code:
        # 1. Analyze winning trades (patterns)
        # 2. Analyze losing trades (mistakes)
        # 3. Extract key insights
        # 4. Return list of lessons
        pass
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Interface method - processes all T1-T3 steps."""
        trades = data.get("trades", [])
        normalized = self.normalize(trades)
        summary = self.summarize(normalized)
        lessons = self.extract_lessons(normalized, summary)
        return {
            "normalized_trades": normalized,
            "summary": summary,
            "lessons": lessons
        }
```

---

## 🔄 **PIPELINE INTERFACES**

### **BuildArtifactPipeline**

**File**: `pipelines/build_artifact.py`

```python
from typing import Dict, Any
from pathlib import Path

class BuildArtifactPipeline:
    """Build → Artifact Pipeline (S1-S6)."""
    
    def __init__(
        self,
        repo_scanner,
        story_extractor,
        readme_generator,
        build_log_generator,
        social_generator,
        manifest_system
    ):
        """Initialize with processor dependencies."""
        self.repo_scanner = repo_scanner
        self.story_extractor = story_extractor
        self.readme_generator = readme_generator
        self.build_log_generator = build_log_generator
        self.social_generator = social_generator
        self.manifest = manifest_system
    
    def process(self, work_session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process build session through S1-S6 pipeline.
        
        Args:
            work_session: Complete work_session.json data
            
        Returns:
            Updated work_session with artifact paths
        """
        # Pseudo-code S1-S6:
        # S1: repo_data = self.repo_scanner.scan(repo_path)
        # S2: story_data = self.story_extractor.extract(commits, conversations)
        # S3: readme_path = self.readme_generator.generate(repo_data, story_data)
        # S4: build_log_path = self.build_log_generator.generate(repo_data, work_session)
        # S5: social_path = self.social_generator.generate(story_data)
        # S6: self.manifest.mark_ready(work_session["session_id"], artifacts)
        # 
        # Update work_session["artifacts"] with paths
        # Update work_session["pipeline_status"]["build_artifact"] = "complete"
        # Return updated work_session
        pass
```

---

### **TradeArtifactPipeline**

**File**: `pipelines/trade_artifact.py`

```python
from typing import Dict, Any

class TradeArtifactPipeline:
    """Trade → Artifact Pipeline (T1-T5)."""
    
    def __init__(
        self,
        trade_processor,
        trade_journal_generator,
        social_generator,
        manifest_system
    ):
        """Initialize with processor dependencies."""
        self.trade_processor = trade_processor
        self.trade_journal_generator = trade_journal_generator
        self.social_generator = social_generator
        self.manifest = manifest_system
    
    def process(self, work_session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process trade session through T1-T5 pipeline.
        
        Args:
            work_session: Complete work_session.json data
            
        Returns:
            Updated work_session with artifact paths
        """
        # Pseudo-code T1-T5:
        # T1-T3: processed = self.trade_processor.process(trades)
        #   - normalized_trades = processed["normalized_trades"]
        #   - summary = processed["summary"]
        #   - lessons = processed["lessons"]
        # T4: journal_path = self.trade_journal_generator.generate(processed, work_session)
        # T5: social_path = self.social_generator.generate_trade_thread(processed)
        # 
        # self.manifest.mark_ready(work_session["session_id"], artifacts)
        # Update work_session["artifacts"] with paths
        # Update work_session["pipeline_status"]["trade_artifact"] = "complete"
        # Return updated work_session
        pass
```

---

### **LifeAriaArtifactPipeline**

**File**: `pipelines/life_aria_artifact.py`

```python
from typing import Dict, Any

class LifeAriaArtifactPipeline:
    """Life/Aria → Artifact Pipeline."""
    
    def __init__(
        self,
        devlog_generator,
        screenshot_generator,
        social_generator,
        manifest_system
    ):
        """Initialize with processor dependencies."""
        self.devlog_generator = devlog_generator
        self.screenshot_generator = screenshot_generator
        self.social_generator = social_generator
        self.manifest = manifest_system
    
    def process(self, work_session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process life/aria session.
        
        Args:
            work_session: Complete work_session.json data
            
        Returns:
            Updated work_session with artifact paths
        """
        # Pseudo-code:
        # Extract session data from work_session
        # devlog_path = self.devlog_generator.generate(session_data)
        # screenshot_path = self.screenshot_generator.generate(session_data)
        # social_path = self.social_generator.generate(session_data)
        # 
        # self.manifest.mark_ready(work_session["session_id"], artifacts)
        # Update work_session["artifacts"] with paths
        # Update work_session["pipeline_status"]["life_aria_artifact"] = "complete"
        # Return updated work_session
        pass
```

---

## 🔗 **MANIFEST SYSTEM INTEGRATION**

**How to Call Manifest**:

```python
from systems.output_flywheel.manifest_system import ManifestSystem

manifest = ManifestSystem()

# After generating artifacts
artifacts = [
    {"type": "readme", "path": "outputs/artifacts/readme_xxx.md"},
    {"type": "blog_post", "path": "outputs/artifacts/blog_xxx.md"}
]

manifest.add_artifacts(session_id, artifacts)
manifest.mark_ready_for_publication(session_id)
```

---

## 📤 **PUBLICATION QUEUE INTEGRATION**

**How to Call Publication Queue**:

```python
from systems.output_flywheel.publication.publish_queue_manager import PublishQueueManager

queue = PublishQueueManager()

# After manifest marks ready
queue.add_to_queue(session_id, artifacts)
# This creates PUBLISH_QUEUE JSON file for Phase 3
```

---

## 🎯 **IMPLEMENTATION PATTERNS**

### **Recommended Pattern: Small Orchestrator + Pure Functions**

```python
# ✅ GOOD: Small orchestrator class
class BuildArtifactPipeline:
    def __init__(self, processors):
        self.processors = processors  # Dependency injection
    
    def process(self, session):
        # Orchestrate calls, <30 lines
        step1 = self.processors.repo_scanner.scan(...)
        step2 = self.processors.story_extractor.extract(...)
        # ...

# ✅ GOOD: Pure function processor
def extract_overview(commits: List[Dict]) -> str:
    """Extract overview text from commits."""
    # Pure function, <30 lines
    messages = [c["message"] for c in commits]
    return " ".join(messages[:5])
```

### **Pitfalls to Avoid**:

1. **❌ Tight Coupling to Discord**: Don't import Discord-specific code
2. **❌ Duplication**: Reuse processors across pipelines
3. **❌ Large Functions**: Keep functions <30 lines
4. **❌ Circular Dependencies**: Processors don't import pipelines
5. **❌ Global State**: Use dependency injection

---

## 📋 **EXACT FILE LIST FOR AGENT-1**

### **Pipeline Files** (3 files):
1. `pipelines/build_artifact.py` (<300 lines)
2. `pipelines/trade_artifact.py` (<300 lines)
3. `pipelines/life_aria_artifact.py` (<300 lines)

### **Processor Files** (7 files):
1. `processors/__init__.py` (exports)
2. `processors/base_processor.py` (abstract base class)
3. `processors/repo_scanner.py` (<300 lines)
4. `processors/story_extractor.py` (<300 lines)
5. `processors/readme_generator.py` (<300 lines)
6. `processors/build_log_generator.py` (<300 lines)
7. `processors/social_generator.py` (<300 lines)
8. `processors/trade_processor.py` (<300 lines)

### **Orchestrator File** (1 file):
1. `pipelines/orchestrator.py` (main entry point, <300 lines)

**Total**: 11 files to implement

---

**Status**: ✅ **INTERFACE SPECIFICATION COMPLETE**

🐝 **WE. ARE. SWARM. ⚡🔥**

