# Enhanced Unified GitHub Tools - Usage Guide

**Date**: 2025-12-10  
**Author**: Agent-1 (Integration & Core Systems Specialist)  
**Status**: ✅ **IMPLEMENTATION COMPLETE**

---

## 📋 **OVERVIEW**

Enhanced unified GitHub tools provide:
- ✅ **Auto-switching** between REST API and GraphQL API
- ✅ **Intelligent queuing** when rate-limited
- ✅ **Automatic retry** when rate limits reset
- ✅ **Graceful degradation** - operations never lost

---

## 🚀 **QUICK START**

### **1. Check Rate Limits**
```bash
python tools/enhanced_unified_github.py rate-limits
```

**Output**:
```
🔍 Checking rate limits...

✅ rest: 4850/5000 remaining
❌ graphql: 0/5000 remaining (reset in 3420s)
✅ gh_cli: 1250/5000 remaining (reset in 3420s)

🎯 Best API for PR creation: rest
```

---

### **2. Create PR (Auto-Switching)**
```bash
python tools/enhanced_unified_github.py create-pr \
  DreamVault "Merge DreamBank" "dreambank:main" "main" "PR body text"
```

**Behavior**:
- Automatically selects API with most remaining requests
- Falls back to alternative API if first fails
- Queues operation if both APIs rate-limited
- Returns queue ID for tracking

---

### **3. Merge PR**
```bash
python tools/enhanced_unified_github.py merge-pr DreamVault 1 merge
```

**Behavior**:
- Uses REST API (most reliable for merging)
- Queues if rate-limited
- Retries automatically when limits reset

---

### **4. Process Queue (Automatic Retry)**
```bash
# Process queue once
python tools/github_queue_processor.py --max-items 10

# Continuous processing (checks every 5 minutes)
python tools/github_queue_processor.py --continuous --interval 300

# Wait for rate limit reset before processing
python tools/github_queue_processor.py --wait-for-reset
```

---

## 🔧 **USAGE IN CODE**

### **Python API**

```python
from tools.enhanced_unified_github import EnhancedUnifiedGitHub

# Initialize
github = EnhancedUnifiedGitHub(owner="Dadudekc")

# Check rate limits
limits = github.check_rate_limits()
for name, limit in limits.items():
    print(f"{name}: {limit.remaining}/{limit.limit}")

# Create PR (auto-switching + queuing)
result = github.create_pr(
    repo="DreamVault",
    title="Merge DreamBank",
    body="Consolidation merge",
    head="dreambank:main",
    base="main",
    queue_on_failure=True  # Queue if rate-limited
)

if result.get("success"):
    print(f"✅ PR created: {result['pr_url']}")
elif result.get("queued"):
    print(f"⏳ Queued: {result['queue_id']}")
    print(f"   Error: {result['error']}")

# Merge PR
result = github.merge_pr(
    repo="DreamVault",
    pr_number=1,
    merge_method="merge",
    queue_on_failure=True
)
```

---

## 📊 **HOW AUTO-SWITCHING WORKS**

### **Selection Logic**:

1. **Check All APIs**: REST, GraphQL, GitHub CLI
2. **Filter Available**: Only APIs with remaining requests > 10
3. **Select Best**:
   - PR Creation/Merging: Prefer REST (more reliable)
   - Queries: Prefer GraphQL (more efficient)
   - Default: API with most remaining requests

### **Fallback Chain**:

```
Try Selected API
  ↓ (if rate-limited)
Try Fallback API
  ↓ (if still rate-limited)
Queue Operation
  ↓ (when rate limit resets)
Automatic Retry
```

---

## 🔄 **QUEUE PROCESSING**

### **Manual Processing**:
```bash
# Process queue once
python tools/github_queue_processor.py
```

### **Automatic Processing**:
```bash
# Continuous mode (checks every 5 minutes)
python tools/github_queue_processor.py --continuous --interval 300

# With max cycles
python tools/github_queue_processor.py --continuous --max-cycles 10
```

### **Queue Statistics**:
```python
from src.core.deferred_push_queue import get_deferred_push_queue

queue = get_deferred_push_queue()
stats = queue.get_stats()

print(f"Pending: {stats['pending']}")
print(f"Failed: {stats['failed']}")
print(f"Completed: {stats['completed']}")
```

---

## 🎯 **INTEGRATION EXAMPLES**

### **Replace Existing Tools**:

**Before** (using `gh` CLI):
```python
subprocess.run(["gh", "pr", "create", ...])
```

**After** (using enhanced tool):
```python
from tools.enhanced_unified_github import EnhancedUnifiedGitHub

github = EnhancedUnifiedGitHub()
result = github.create_pr(...)
```

---

### **Update repo_safe_merge.py**:

Replace `gh pr` commands with:
```python
from tools.enhanced_unified_github import EnhancedUnifiedGitHub

github = EnhancedUnifiedGitHub()

# Create PR
result = github.create_pr(repo, title, body, head, base)
if result.get("queued"):
    logger.info(f"Queued for retry: {result['queue_id']}")

# Merge PR
result = github.merge_pr(repo, pr_number, "merge")
```

---

## 📋 **BENEFITS**

### **Before Enhanced Tools**:
- ❌ Single API (GraphQL via CLI)
- ❌ Fails when rate-limited
- ❌ Manual retry required
- ❌ Operations lost on failure

### **After Enhanced Tools**:
- ✅ **2x Capacity**: REST + GraphQL (10,000/hour combined)
- ✅ **Auto-Switching**: Always uses best available API
- ✅ **Queuing**: Operations never lost
- ✅ **Automatic Retry**: Processes queue when limits reset

---

## 🚨 **RATE LIMIT HANDLING**

### **When Rate-Limited**:

1. **Immediate**: Try alternative API
2. **If Both Exhausted**: Queue operation
3. **Auto-Retry**: Queue processor retries when limits reset
4. **Never Lost**: All operations preserved

### **Queue Status**:
- **Pending**: Waiting for retry
- **Retrying**: Currently being processed
- **Completed**: Successfully processed
- **Failed**: Max retries exceeded (requires manual intervention)

---

## 📝 **EXAMPLE WORKFLOW**

### **Complete PR Creation with Queue**:

```python
from tools.enhanced_unified_github import EnhancedUnifiedGitHub

github = EnhancedUnifiedGitHub()

# Try to create PR
result = github.create_pr(
    repo="DreamVault",
    title="Merge DreamBank",
    body="...",
    head="dreambank:main",
    base="main"
)

if result.get("success"):
    print(f"✅ PR created: {result['pr_url']}")
elif result.get("queued"):
    print(f"⏳ Queued (ID: {result['queue_id']})")
    print("   Will retry automatically when rate limits reset")
    
    # Optionally process queue now (if limits reset)
    from tools.github_queue_processor import GitHubQueueProcessor
    processor = GitHubQueueProcessor()
    stats = processor.process_queue()
```

---

**Generated by**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-10  
**Status**: ✅ **READY FOR USE**

🐝 **WE. ARE. SWARM. ⚡🔥**


