# Output Flywheel - End-of-Session Integration Guide

**Version**: 1.0  
**Status**: Production-Ready  
**Last Updated**: 2025-12-02  
**Author**: Agent-7 (Web Development Specialist)  
**Purpose**: Practical, step-by-step guide for agents to integrate Output Flywheel at end-of-session

---

## 🎯 **QUICK START**

At the end of your work session, follow these steps:

1. **Collect session data** (duration, files changed, commits, etc.)
2. **Assemble work_session.json** using the templates below
3. **Save session file** to `systems/output_flywheel/outputs/sessions/`
4. **Run pipeline**: `python tools/run_output_flywheel.py --session-file path/to/work_session.json`
5. **Verify artifacts** were generated
6. **Queue for publication** using `tools/run_publication.py` (Phase 3)

---

## 📋 **STEP-BY-STEP: BUILD SESSION**

### **Step 1: Collect Session Data**

During your work session, track:
- **Duration**: How long did you work? (in minutes)
- **Files Changed**: Which files did you modify/create?
- **Commits**: Git commit hashes and messages
- **Lines Added/Removed**: Code change metrics
- **Repo Path**: Full path to repository

### **Step 2: Assemble work_session.json**

```python
import json
import uuid
from datetime import datetime
from pathlib import Path

def create_build_session(
    agent_id: str,
    repo_path: str,
    duration_minutes: int,
    files_changed: list,
    commits: list,
    lines_added: int = 0,
    lines_removed: int = 0
):
    """Create work_session.json for build session."""
    
    session_id = str(uuid.uuid4())
    
    session = {
        "session_id": session_id,
        "session_type": "build",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": agent_id,
        "metadata": {
            "duration_minutes": duration_minutes,
            "files_changed": len(files_changed),
            "commits": len(commits),
            "lines_added": lines_added,
            "lines_removed": lines_removed
        },
        "source_data": {
            "repo_path": repo_path,
            "git_commits": commits  # List of commit dicts
        },
        "artifacts": {},
        "pipeline_status": {
            "build_artifact": "pending",
            "trade_artifact": "not_applicable",
            "life_aria_artifact": "not_applicable"
        }
    }
    
    return session
```

### **Step 3: Real Example - Build Session**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "session_type": "build",
  "timestamp": "2025-12-02T05:20:00Z",
  "agent_id": "Agent-7",
  "metadata": {
    "duration_minutes": 120,
    "files_changed": 8,
    "commits": 3,
    "lines_added": 450,
    "lines_removed": 120
  },
  "source_data": {
    "repo_path": "D:/Agent_Cellphone_V2_Repository",
    "git_commits": [
      {
        "hash": "abc123def456",
        "message": "feat: Add Phase 3 publication system",
        "author": "Agent-7",
        "timestamp": "2025-12-02T05:15:00Z",
        "files": [
          "systems/output_flywheel/publication/publish_queue_manager.py",
          "systems/output_flywheel/publication/github_publisher.py"
        ]
      },
      {
        "hash": "def456ghi789",
        "message": "feat: Add website publisher",
        "author": "Agent-7",
        "timestamp": "2025-12-02T05:18:00Z",
        "files": [
          "systems/output_flywheel/publication/website_publisher.py"
        ]
      }
    ]
  },
  "artifacts": {},
  "pipeline_status": {
    "build_artifact": "pending",
    "trade_artifact": "not_applicable",
    "life_aria_artifact": "not_applicable"
  }
}
```

### **Step 4: Save and Run**

```python
# Save session file
sessions_dir = Path("systems/output_flywheel/outputs/sessions")
sessions_dir.mkdir(parents=True, exist_ok=True)
session_file = sessions_dir / f"{session_id}_build.json"
session_file.write_text(json.dumps(session, indent=2))

# Run pipeline
import subprocess
result = subprocess.run(
    ["python", "tools/run_output_flywheel.py", "--session-file", str(session_file)],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ Artifacts generated successfully!")
else:
    print(f"❌ Pipeline failed: {result.stderr}")
```

---

## 📋 **STEP-BY-STEP: TRADE SESSION**

### **Step 1: Collect Trading Data**

Track:
- **Trades Executed**: List of all trades
- **Total P&L**: Profit/loss for session
- **Win Rate**: Percentage of winning trades
- **Market Conditions**: Volatility, trend, volume

### **Step 2: Real Example - Trade Session**

```json
{
  "session_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "session_type": "trade",
  "timestamp": "2025-12-02T05:20:00Z",
  "agent_id": "Agent-5",
  "metadata": {
    "duration_minutes": 180,
    "trades_executed": 5,
    "total_pnl": 325.75,
    "win_rate": 80.0,
    "max_drawdown": 50.00
  },
  "source_data": {
    "trades": [
      {
        "symbol": "AAPL",
        "action": "buy",
        "quantity": 10,
        "price": 175.50,
        "timestamp": "2025-12-02T03:00:00Z",
        "profit_loss": 25.00,
        "exit_price": 178.00,
        "exit_timestamp": "2025-12-02T03:45:00Z"
      },
      {
        "symbol": "MSFT",
        "action": "sell",
        "quantity": 5,
        "price": 380.25,
        "timestamp": "2025-12-02T04:00:00Z",
        "profit_loss": 50.00,
        "exit_price": 370.25,
        "exit_timestamp": "2025-12-02T04:30:00Z"
      }
    ],
    "market_conditions": {
      "volatility": "moderate",
      "trend": "bullish",
      "volume": "high",
      "market_sentiment": "positive"
    }
  },
  "artifacts": {},
  "pipeline_status": {
    "build_artifact": "not_applicable",
    "trade_artifact": "pending",
    "life_aria_artifact": "not_applicable"
  }
}
```

---

## 📋 **STEP-BY-STEP: LIFE/ARIA SESSION**

### **Step 1: Collect Aria/Life Data**

Track:
- **Conversations**: Aria conversations or life session notes
- **Artifacts Created**: Games, websites, or other creations
- **Screenshots**: Paths to screenshots or images
- **Session Notes**: Key insights or learnings

### **Step 2: Real Example - Life/Aria Session**

```json
{
  "session_id": "c3d4e5f6-a7b8-9012-cdef-345678901234",
  "session_type": "life_aria",
  "timestamp": "2025-12-02T05:20:00Z",
  "agent_id": "Agent-7",
  "metadata": {
    "duration_minutes": 90,
    "artifacts_created": 1,
    "screenshots_taken": 5
  },
  "source_data": {
    "conversations": [
      {
        "source": "aria",
        "content": "Built a new interactive game using React and Three.js. Features include real-time multiplayer, physics simulation, and dynamic lighting.",
        "timestamp": "2025-12-02T03:00:00Z",
        "artifacts": [
          {
            "type": "game",
            "name": "SpaceExplorer",
            "path": "D:/games/SpaceExplorer",
            "technologies": ["React", "Three.js", "WebSocket"]
          }
        ]
      }
    ],
    "screenshots": [
      "screenshots/gameplay_001.png",
      "screenshots/gameplay_002.png",
      "screenshots/gameplay_003.png"
    ]
  },
  "artifacts": {},
  "pipeline_status": {
    "build_artifact": "not_applicable",
    "trade_artifact": "not_applicable",
    "life_aria_artifact": "pending"
  }
}
```

---

## 🔧 **COMMON PATTERNS & BEST PRACTICES**

### **Pattern 1: Python Helper Function**

```python
from pathlib import Path
import json
import uuid
from datetime import datetime

def end_of_session_integration(
    agent_id: str,
    session_type: str,
    metadata: dict,
    source_data: dict
):
    """Standard end-of-session integration pattern."""
    
    # 1. Generate session ID
    session_id = str(uuid.uuid4())
    
    # 2. Assemble session
    session = {
        "session_id": session_id,
        "session_type": session_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_id": agent_id,
        "metadata": metadata,
        "source_data": source_data,
        "artifacts": {},
        "pipeline_status": {
            "build_artifact": "pending" if session_type == "build" else "not_applicable",
            "trade_artifact": "pending" if session_type == "trade" else "not_applicable",
            "life_aria_artifact": "pending" if session_type == "life_aria" else "not_applicable"
        }
    }
    
    # 3. Save session file
    sessions_dir = Path("systems/output_flywheel/outputs/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / f"{session_id}_{session_type}.json"
    session_file.write_text(json.dumps(session, indent=2))
    
    # 4. Run pipeline
    import subprocess
    result = subprocess.run(
        ["python", "tools/run_output_flywheel.py", "--session-file", str(session_file)],
        capture_output=True,
        text=True,
        timeout=300  # 5 minute timeout
    )
    
    if result.returncode == 0:
        # 5. Load updated session to get artifact paths
        updated_session = json.loads(session_file.read_text())
        artifacts = updated_session.get("artifacts", {})
        
        # 6. Queue for publication (Phase 3)
        queue_artifacts_for_publication(artifacts)
        
        return artifacts
    else:
        print(f"❌ Pipeline failed: {result.stderr}")
        return None

def queue_artifacts_for_publication(artifacts: dict):
    """Queue generated artifacts for publication (Phase 3)."""
    import subprocess
    
    for artifact_type, artifact_info in artifacts.items():
        if artifact_info.get("generated") and artifact_info.get("path"):
            # Add to publication queue
            subprocess.run([
                "python", "tools/run_publication.py", "--add-entry",
                "--type", artifact_type,
                "--file", artifact_info["path"],
                "--targets", "github,website" if artifact_type == "readme" else "website"
            ])
```

### **Pattern 2: Git Commit Collection**

```python
import subprocess
from pathlib import Path

def collect_git_commits(repo_path: Path, since: str = None):
    """Collect git commits for session."""
    commits = []
    
    # Get commit log
    cmd = ["git", "log", "--pretty=format:%H|%an|%ae|%ad|%s", "--date=iso"]
    if since:
        cmd.extend([f"--since={since}"])
    
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        
        parts = line.split('|')
        if len(parts) >= 5:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "email": parts[2],
                "timestamp": parts[3] + "Z",
                "message": parts[4],
                "files": get_commit_files(repo_path, parts[0])
            })
    
    return commits

def get_commit_files(repo_path: Path, commit_hash: str):
    """Get files changed in commit."""
    result = subprocess.run(
        ["git", "show", "--name-only", "--pretty=format:", commit_hash],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
```

### **Pattern 3: Session Duration Tracking**

```python
import time
from datetime import datetime

class SessionTracker:
    """Track session duration and metrics."""
    
    def __init__(self, agent_id: str, session_type: str):
        self.agent_id = agent_id
        self.session_type = session_type
        self.start_time = time.time()
        self.files_changed = []
        self.commits = []
    
    def add_file_changed(self, file_path: str):
        """Track file change."""
        self.files_changed.append(file_path)
    
    def add_commit(self, commit_hash: str, message: str):
        """Track commit."""
        self.commits.append({
            "hash": commit_hash,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    
    def get_duration_minutes(self) -> int:
        """Get session duration in minutes."""
        return int((time.time() - self.start_time) / 60)
    
    def create_session(self, repo_path: str = None, source_data: dict = None):
        """Create work_session.json from tracked data."""
        import uuid
        
        session = {
            "session_id": str(uuid.uuid4()),
            "session_type": self.session_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_id": self.agent_id,
            "metadata": {
                "duration_minutes": self.get_duration_minutes(),
                "files_changed": len(self.files_changed),
                "commits": len(self.commits)
            },
            "source_data": source_data or {
                "repo_path": repo_path,
                "git_commits": self.commits
            },
            "artifacts": {},
            "pipeline_status": {
                "build_artifact": "pending" if self.session_type == "build" else "not_applicable",
                "trade_artifact": "pending" if self.session_type == "trade" else "not_applicable",
                "life_aria_artifact": "pending" if self.session_type == "life_aria" else "not_applicable"
            }
        }
        
        return session

# Usage:
tracker = SessionTracker("Agent-7", "build")
tracker.add_file_changed("src/feature.py")
tracker.add_commit("abc123", "Add feature")
session = tracker.create_session(repo_path="D:/Agent_Cellphone_V2_Repository")
```

---

## 🐛 **TROUBLESHOOTING**

### **Issue 1: Session File Not Found**

**Error**: `Session file not found: path/to/session.json`

**Solution**:
- Verify file path is correct
- Ensure file exists before running pipeline
- Check file permissions

```python
session_file = Path("systems/output_flywheel/outputs/sessions/session.json")
if not session_file.exists():
    print(f"❌ Session file not found: {session_file}")
    # Create it first
```

### **Issue 2: Invalid Session JSON**

**Error**: `Invalid session data` or JSON parsing errors

**Solution**:
- Validate against schema: `systems/output_flywheel/schemas/work_session.json`
- Ensure all required fields are present
- Check JSON syntax (commas, quotes, brackets)

```python
import json
from jsonschema import validate

# Load schema
schema = json.loads(Path("systems/output_flywheel/schemas/work_session.json").read_text())

# Validate session
try:
    validate(instance=session, schema=schema)
    print("✅ Session data valid")
except Exception as e:
    print(f"❌ Validation error: {e}")
```

### **Issue 3: Pipeline Timeout**

**Error**: Pipeline takes too long or times out

**Solution**:
- Increase timeout (default: 300 seconds)
- Check for large repositories or many commits
- Verify templates exist and are accessible

```python
result = subprocess.run(
    ["python", "tools/run_output_flywheel.py", "--session-file", str(session_file)],
    timeout=600  # 10 minutes
)
```

### **Issue 4: Artifacts Not Generated**

**Error**: Pipeline runs but no artifacts created

**Solution**:
- Check pipeline status in updated session file
- Verify output directory exists and is writable
- Check for template errors or missing data

```python
# After running pipeline, check updated session
updated_session = json.loads(session_file.read_text())
artifacts = updated_session.get("artifacts", {})
pipeline_status = updated_session.get("pipeline_status", {})

if pipeline_status.get("build_artifact") == "failed":
    print("❌ Build pipeline failed")
    # Check error details in session metadata
```

---

## ✅ **INTEGRATION CHECKLIST**

### **Before Integration**
- [ ] Review this guide
- [ ] Understand your session type (build/trade/life_aria)
- [ ] Identify where to call pipeline (end-of-session hook)
- [ ] Set up session tracking (if needed)

### **During Integration**
- [ ] Collect session data during work
- [ ] Assemble work_session.json at end-of-session
- [ ] Save session file to correct location
- [ ] Run pipeline with session file
- [ ] Verify artifacts generated
- [ ] Queue artifacts for publication (Phase 3)

### **After Integration**
- [ ] Test with sample session data
- [ ] Verify artifacts are generated correctly
- [ ] Check artifact quality (formatting, content)
- [ ] Monitor pipeline execution time
- [ ] Document any custom patterns

---

## 📚 **REFERENCES**

- **Integration Guide**: `docs/organization/OUTPUT_FLYWHEEL_AGENT_INTEGRATION.md`
- **Schema**: `systems/output_flywheel/schemas/work_session.json`
- **CLI Tool**: `tools/run_output_flywheel.py`
- **Publication CLI**: `tools/run_publication.py` (Phase 3)
- **Architecture**: `systems/output_flywheel/ARCHITECTURE.md`

---

## 🎯 **QUICK REFERENCE**

### **Minimal Build Session**

```json
{
  "session_id": "uuid-here",
  "session_type": "build",
  "timestamp": "2025-12-02T05:20:00Z",
  "agent_id": "Agent-X",
  "metadata": {
    "duration_minutes": 60,
    "files_changed": 5,
    "commits": 2
  },
  "source_data": {
    "repo_path": "D:/path/to/repo",
    "git_commits": []
  },
  "artifacts": {},
  "pipeline_status": {
    "build_artifact": "pending",
    "trade_artifact": "not_applicable",
    "life_aria_artifact": "not_applicable"
  }
}
```

### **Command to Run**

```bash
python tools/run_output_flywheel.py --session-file systems/output_flywheel/outputs/sessions/{session_id}_build.json
```

---

**Guide Created**: 2025-12-02 05:20:00  
**Author**: Agent-7 (Web Development Specialist)  
**Status**: Production-Ready ✅

🐝 **WE. ARE. SWARM. ⚡🔥**

