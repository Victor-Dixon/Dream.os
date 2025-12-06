# 🔧 IDENTICAL CODE BLOCKS CONSOLIDATION PLAN
**Agent-5 Business Intelligence Analysis**  
**Date**: 2025-12-04  
**Total Identical Code Blocks**: 88 occurrences across 10 unique block patterns

---

## 📊 EXECUTIVE SUMMARY

**Block Analysis**:
- **10 unique block patterns** identified
- **88 total occurrences** across codebase
- **High-impact blocks**: 6 patterns (39 occurrences)
- **Medium-impact blocks**: 3 patterns (9 occurrences)
- **Low-impact blocks**: 1 pattern (test code, acceptable duplication)

**Consolidation Strategy**:
1. **SSOT Utilities**: Create reusable utility modules
2. **Constants**: Extract to shared constants files
3. **Base Classes**: Create base classes with shared methods
4. **Test Helpers**: Create test utility modules

**Target**: Reduce 88 occurrences to <10 (89% reduction)

---

## 🚨 TIER 1: HIGH-IMPACT BLOCKS (Priority: IMMEDIATE)

### **Block 1: Validation Error Printing** 
**Hash**: `1b58ef4a` | **Occurrences**: 6 | **Impact**: HIGH

**Locations**:
1. `tools/communication/message_validator.py:177`
2. `tools/communication/coordination_validator.py:184`
3. `tools/communication/multi_agent_validator.py:115`
4. *(3 more occurrences - need to identify)*

**Code Pattern**:
```python
if self.errors:
    print("❌ VALIDATION ERRORS:")
    for error in self.errors:
        print(f"  • {error}")
if self.warnings:
    print("⚠️  WARNINGS:")
    for warning in self.warnings:
        print(f"  • {warning}")
if not self.errors and not self.warnings:
    print("✅ All validations passed!")
```

**SSOT Candidate**: `src/core/utils/validation_utils.py`

**Consolidation Strategy**:
```python
# src/core/utils/validation_utils.py
"""Validation utility functions - SSOT for validation output formatting."""

from typing import List, Optional


def print_validation_report(
    errors: Optional[List[str]] = None,
    warnings: Optional[List[str]] = None,
    success_message: str = "✅ All validations passed!",
) -> None:
    """
    Print formatted validation report.
    
    Args:
        errors: List of error messages
        warnings: List of warning messages
        success_message: Message to display when no errors/warnings
    """
    if errors:
        print("❌ VALIDATION ERRORS:")
        for error in errors:
            print(f"  • {error}")
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  • {warning}")
    if not errors and not warnings:
        print(success_message)


class ValidationReporter:
    """Mixin class for validators to use print_validation_report."""
    
    def print_report(self) -> None:
        """Print validation report using errors and warnings attributes."""
        print_validation_report(
            errors=getattr(self, 'errors', None),
            warnings=getattr(self, 'warnings', None),
        )
```

**Migration Plan**:
1. Create `src/core/utils/validation_utils.py`
2. Update all validator classes to inherit from `ValidationReporter` or call `print_validation_report()`
3. Remove duplicate code blocks
4. Update imports

**Files to Update**: 6 files  
**Estimated Time**: 2 hours  
**Risk**: LOW  
**Impact**: HIGH (standardizes validation output)

---

### **Block 2: Agent List Constant**
**Hash**: `dd569d8d` | **Occurrences**: 5 | **Impact**: HIGH

**Locations**:
1. `src/core/messaging_core.py:352`
2. `src/services/messaging_infrastructure.py:1228`
3. `tools/captain_check_agent_status.py:69`
4. *(2 more occurrences - need to identify)*

**Code Pattern**:
```python
agents = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]
```

**SSOT Candidate**: `src/core/constants/agent_constants.py`

**Consolidation Strategy**:
```python
# src/core/constants/agent_constants.py
"""Agent constants - SSOT for agent identifiers."""

# All agents in the swarm
AGENT_LIST = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]

# Agent IDs as tuple for immutability
AGENT_IDS = tuple(AGENT_LIST)

# Agent count
AGENT_COUNT = len(AGENT_LIST)

# Agent roles mapping (if needed)
AGENT_ROLES = {
    "Agent-1": "Integration & Core Systems",
    "Agent-2": "Architecture & Design",
    "Agent-3": "Infrastructure & DevOps",
    "Agent-4": "Captain (Strategic Oversight)",
    "Agent-5": "Business Intelligence",
    "Agent-6": "Coordination & Communication",
    "Agent-7": "Web Development",
    "Agent-8": "SSOT & System Integration",
}
```

**Migration Plan**:
1. Create `src/core/constants/agent_constants.py`
2. Replace all hardcoded agent lists with `from src.core.constants.agent_constants import AGENT_LIST`
3. Update all files
4. Remove duplicate code blocks

**Files to Update**: 5 files  
**Estimated Time**: 1 hour  
**Risk**: LOW  
**Impact**: HIGH (single source of truth for agent list)

---

### **Block 3: Directory Removal Utility**
**Hash**: `79a28ea5` | **Occurrences**: 5 | **Impact**: HIGH

**Locations**:
1. `tools/resolve_merge_conflicts.py:45`
2. `tools/complete_merge_into_main.py:39`
3. `tools/review_dreamvault_integration.py:70`
4. *(2 more occurrences - need to identify)*

**Code Pattern**:
```python
if dir_path.exists():
    print(f"🧹 Removing existing {name} directory: {dir_path}")
    try:
        shutil.rmtree(dir_path, ignore_errors=True)
        time.sleep(0.5)
        if dir_path.exists():
            def remove_readonly(func, path, exc):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(dir_path, onerror=remove_readonly)
            time.sleep(0.5)
    except Exception as e:
        print(f"⚠️ Cleanup warning for {name}: {e}")
```

**SSOT Candidate**: `src/core/utils/file_utils.py`

**Consolidation Strategy**:
```python
# src/core/utils/file_utils.py
"""File and directory utilities - SSOT for file operations."""

import os
import shutil
import stat
import time
from pathlib import Path
from typing import Optional


def ensure_directory_removed(
    dir_path: Path,
    name: Optional[str] = None,
    retry_delay: float = 0.5,
    max_retries: int = 2,
) -> bool:
    """
    Ensure directory is completely removed, handling readonly files.
    
    Args:
        dir_path: Path to directory to remove
        name: Optional name for logging
        retry_delay: Delay between retry attempts
        max_retries: Maximum number of retry attempts
        
    Returns:
        True if directory was removed, False otherwise
    """
    if not dir_path.exists():
        return True
    
    display_name = name or str(dir_path)
    print(f"🧹 Removing existing {display_name} directory: {dir_path}")
    
    try:
        # First attempt: standard removal
        shutil.rmtree(dir_path, ignore_errors=True)
        time.sleep(retry_delay)
        
        # If still exists, try with readonly handler
        if dir_path.exists():
            def remove_readonly(func, path, exc):
                """Handle readonly files on Windows."""
                os.chmod(path, stat.S_IWRITE)
                func(path)
            
            shutil.rmtree(dir_path, onerror=remove_readonly)
            time.sleep(retry_delay)
        
        # Final check
        if dir_path.exists():
            print(f"⚠️ Warning: Could not fully remove {display_name} directory")
            return False
        
        return True
        
    except Exception as e:
        print(f"⚠️ Cleanup warning for {display_name}: {e}")
        return False
```

**Migration Plan**:
1. Create/update `src/core/utils/file_utils.py`
2. Replace all duplicate directory removal code
3. Update imports
4. Test on Windows (readonly file handling)

**Files to Update**: 5 files  
**Estimated Time**: 2 hours  
**Risk**: MEDIUM (Windows readonly file handling)  
**Impact**: HIGH (standardizes file operations)

---

### **Block 4: send_message Function Signature**
**Hash**: `c183edd6` | **Occurrences**: 4 | **Impact**: MEDIUM-HIGH

**Locations**:
1. `src/core/messaging_core.py:114`
2. `src/core/stress_testing/messaging_core_protocol.py:24`
3. `src/core/stress_testing/mock_messaging_core.py:46`
4. *(1 more occurrence - need to identify)*

**Code Pattern**:
```python
def send_message(
    self,
    content: str,
    sender: str,
    recipient: str,
    message_type: UnifiedMessageType,
    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
    tags: list[UnifiedMessageTag] | None = None,
    metadata: dict[str, Any] | None = None,
) -> bool:
```

**SSOT Candidate**: `src/core/messaging/messaging_protocol.py` (Protocol/Interface)

**Consolidation Strategy**:
```python
# src/core/messaging/messaging_protocol.py
"""Messaging protocol interface - SSOT for messaging method signatures."""

from typing import Protocol, Any
from src.core.messaging_protocol_models import (
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)


class MessagingProtocol(Protocol):
    """Protocol for messaging implementations."""
    
    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: list[UnifiedMessageTag] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """
        Send a message using the unified messaging system.
        
        Args:
            content: Message content
            sender: Sender identifier
            recipient: Recipient identifier
            message_type: Type of message
            priority: Message priority
            tags: Optional message tags
            metadata: Optional metadata
            
        Returns:
            True if message sent successfully
        """
        ...
```

**Migration Plan**:
1. Create protocol interface
2. Update all messaging implementations to follow protocol
3. Use protocol for type hints
4. Ensure consistency across implementations

**Files to Update**: 4 files  
**Estimated Time**: 3 hours  
**Risk**: MEDIUM (interface changes)  
**Impact**: MEDIUM-HIGH (ensures messaging consistency)

---

### **Block 5: Vector Database Import Pattern**
**Hash**: `bd538728` | **Occurrences**: 3 | **Impact**: MEDIUM-HIGH

**Locations**:
1. `src/services/performance_analyzer.py:16`
2. `src/services/recommendation_engine.py:16`
3. `src/services/swarm_intelligence_manager.py:16`

**Code Pattern**:
```python
try:
    from .vector_database_service_unified import (
        get_vector_database_service,
        search_vector_database,
    )
    from .vector_database.vector_database_models import SearchQuery
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    def get_vector_database_service():
        return None
    def search_vector_database(query):
        return []
```

**SSOT Candidate**: `src/services/vector_database/__init__.py`

**Consolidation Strategy**:
```python
# src/services/vector_database/__init__.py
"""Vector database service - SSOT for vector DB imports."""

from typing import Optional, List, Any

# Try to import vector database service
try:
    from .vector_database_service_unified import (
        get_vector_database_service,
        search_vector_database,
    )
    from .vector_database_models import SearchQuery
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    
    # Fallback implementations
    def get_vector_database_service() -> None:
        """Fallback when vector DB unavailable."""
        return None
    
    def search_vector_database(query: Any) -> List[Any]:
        """Fallback when vector DB unavailable."""
        return []
    
    # Create minimal SearchQuery for type hints
    from dataclasses import dataclass
    
    @dataclass
    class SearchQuery:
        """Minimal SearchQuery for fallback."""
        query: str = ""
        limit: int = 10
```

**Migration Plan**:
1. Create/update `src/services/vector_database/__init__.py`
2. Replace all duplicate import blocks with: `from src.services.vector_database import ...`
3. Update all service files
4. Test with and without vector DB available

**Files to Update**: 3 files  
**Estimated Time**: 2 hours  
**Risk**: LOW  
**Impact**: MEDIUM-HIGH (standardizes vector DB availability handling)

---

### **Block 6: GitHub Token Extraction**
**Hash**: `7a8778c5` | **Occurrences**: 3 | **Impact**: MEDIUM-HIGH

**Locations**:
1. `tools/repo_safe_merge.py:83`
2. `tools/git_based_merge_primary.py:34`
3. `tools/repo_safe_merge_v2.py:49`

**Code Pattern**:
```python
env_file = project_root / ".env"
if env_file.exists():
    try:
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
```

**SSOT Candidate**: `src/core/utils/github_utils.py`

**Consolidation Strategy**:
```python
# src/core/utils/github_utils.py
"""GitHub utilities - SSOT for GitHub operations."""

import os
from pathlib import Path
from typing import Optional


def get_github_token(project_root: Optional[Path] = None) -> Optional[str]:
    """
    Get GitHub token from environment or .env file.
    
    Args:
        project_root: Optional project root path (defaults to repo root)
        
    Returns:
        GitHub token if found, None otherwise
    """
    # Check environment variables first
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    # Check .env file
    if project_root is None:
        # Find project root (directory containing .env)
        project_root = Path(__file__).parent.parent.parent.parent
    
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    
    return None
```

**Migration Plan**:
1. Create/update `src/core/utils/github_utils.py`
2. Replace all duplicate `get_github_token()` implementations
3. Update imports
4. Test token extraction

**Files to Update**: 3 files  
**Estimated Time**: 1.5 hours  
**Risk**: LOW  
**Impact**: MEDIUM-HIGH (standardizes GitHub token handling)

---

## 🔧 TIER 2: MEDIUM-IMPACT BLOCKS (Priority: HIGH)

### **Block 7: GitHub PR Creation Headers**
**Hash**: `7328062d` | **Occurrences**: 3 | **Impact**: MEDIUM

**Locations**:
1. `tools/create_batch2_prs.py:58`
2. `tools/create_merge1_pr.py:58`
3. `tools/merge_prs_via_api.py:102`

**Code Pattern**:
```python
url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}
data = {
    "title": title,
    "body": body,
    "head": head,
    "base": base
}
```

**SSOT Candidate**: `src/core/utils/github_utils.py` (extend existing)

**Consolidation Strategy**:
```python
# Add to src/core/utils/github_utils.py

def create_github_pr_headers(token: str) -> dict[str, str]:
    """
    Create standard GitHub API headers for PR operations.
    
    Args:
        token: GitHub token
        
    Returns:
        Headers dictionary
    """
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }


def create_github_pr_url(owner: str, repo: str) -> str:
    """Create GitHub PR API URL."""
    return f"https://api.github.com/repos/{owner}/{repo}/pulls"


def create_pr_data(title: str, body: str, head: str, base: str) -> dict[str, str]:
    """Create PR data payload."""
    return {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
    }
```

**Migration Plan**:
1. Extend `src/core/utils/github_utils.py`
2. Replace duplicate header/data creation
3. Update all PR creation tools

**Files to Update**: 3 files  
**Estimated Time**: 1 hour  
**Risk**: LOW  
**Impact**: MEDIUM (standardizes GitHub API calls)

---

### **Block 8: GitHub PR List Check**
**Hash**: `c7401dbf` | **Occurrences**: 3 | **Impact**: MEDIUM

**Locations**:
1. `tools/create_batch2_prs.py:82`
2. `tools/create_merge1_pr.py:83`
3. `tools/merge_prs_via_api.py:126`

**Code Pattern**:
```python
list_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
list_response = requests.get(
    list_url,
    headers=headers,
    params={"head": f"{owner}:{head}", "state": "open"},
    timeout=30
)
```

**SSOT Candidate**: `src/core/utils/github_utils.py` (extend existing)

**Consolidation Strategy**:
```python
# Add to src/core/utils/github_utils.py

def check_existing_pr(
    owner: str,
    repo: str,
    head: str,
    token: str,
    timeout: int = 30,
) -> Optional[dict]:
    """
    Check if PR already exists for given head branch.
    
    Args:
        owner: Repository owner
        repo: Repository name
        head: Head branch name
        token: GitHub token
        timeout: Request timeout
        
    Returns:
        PR data if exists, None otherwise
    """
    import requests
    
    url = create_github_pr_url(owner, repo)
    headers = create_github_pr_headers(token)
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params={"head": f"{owner}:{head}", "state": "open"},
            timeout=timeout,
        )
        if response.status_code == 200:
            prs = response.json()
            return prs[0] if prs else None
    except Exception:
        pass
    
    return None
```

**Migration Plan**:
1. Extend `src/core/utils/github_utils.py`
2. Replace duplicate PR check code
3. Update all tools

**Files to Update**: 3 files  
**Estimated Time**: 1 hour  
**Risk**: LOW  
**Impact**: MEDIUM (standardizes PR checking)

---

## 🧪 TIER 3: TEST CODE BLOCKS (Priority: LOW - Acceptable Duplication)

### **Block 9: Test Response Element Finding**
**Hash**: `294bd627` | **Occurrences**: 4 | **Impact**: LOW

**Locations** (All in test files):
1. `agent_workspaces/Agent-2/extracted_logic/ai_framework/conversation/tests/unit/test_chat_navigation.py:217`
2. `agent_workspaces/Agent-2/extracted_logic/ai_framework/conversation/tests/unit/test_direct_chat.py:158`
3. `agent_workspaces/Agent-2/extracted_logic/ai_framework/conversation/tests/unit/test_final_chat.py:220`
4. *(1 more occurrence)*

**Code Pattern**:
```python
response_elements = []
for selector in response_selectors:
    try:
        elements = orch.driver.find_elements("css selector", selector)
        if elements:
            response_elements = elements
            print(f"✅ Found {len(elements)}")
```

**SSOT Candidate**: `tests/utils/test_helpers.py` (optional)

**Consolidation Strategy**: 
- **DECISION**: Keep as-is (test code duplication acceptable)
- OR create test helper if pattern expands

**Action**: Monitor - only consolidate if pattern expands beyond 5 occurrences

---

### **Block 10: Test Button Finding**
**Hash**: `935e54ad` | **Occurrences**: 3 | **Impact**: LOW

**Locations** (All in test files):
1. `agent_workspaces/Agent-2/extracted_logic/ai_framework/conversation/tests/unit/test_chat_navigation.py:182`
2. `agent_workspaces/Agent-2/extracted_logic/ai_framework/conversation/tests/unit/test_final_chat.py:185`
3. `agent_workspaces/Agent-2/extracted_logic/ai_framework/conversation/tests/unit/test_working_chat.py:120`

**Code Pattern**:
```python
print("🔍 Looking for any button that might be send...")
try:
    all_buttons = orch.driver.find_elements("css selector", "button")
    for button in all_buttons:
        text = button.text.lower()
        aria_label = (butto
```

**SSOT Candidate**: `tests/utils/test_helpers.py` (optional)

**Consolidation Strategy**:
- **DECISION**: Keep as-is (test code duplication acceptable)
- OR create test helper if pattern expands

**Action**: Monitor - only consolidate if pattern expands beyond 5 occurrences

---

## 📋 CONSOLIDATION ROADMAP

### **Phase 1: High-Impact Utilities (Week 1)**
- [ ] Create `src/core/utils/validation_utils.py` (Block 1)
- [ ] Create `src/core/constants/agent_constants.py` (Block 2)
- [ ] Create/update `src/core/utils/file_utils.py` (Block 3)
- [ ] Create `src/core/utils/github_utils.py` (Blocks 6, 7, 8)
- [ ] Update all affected files (19 files total)

**Estimated Time**: 8-10 hours  
**Risk**: LOW-MEDIUM  
**Impact**: HIGH (39 occurrences → 0)

### **Phase 2: Protocol/Interface (Week 1-2)**
- [ ] Create `src/core/messaging/messaging_protocol.py` (Block 4)
- [ ] Create/update `src/services/vector_database/__init__.py` (Block 5)
- [ ] Update all implementations

**Estimated Time**: 5-6 hours  
**Risk**: MEDIUM  
**Impact**: MEDIUM-HIGH (7 occurrences → 0)

### **Phase 3: Test Helpers (Week 2) - OPTIONAL**
- [ ] Monitor test code duplication
- [ ] Create `tests/utils/test_helpers.py` if pattern expands
- [ ] Consolidate test blocks if >5 occurrences

**Estimated Time**: 2-3 hours (if needed)  
**Risk**: LOW  
**Impact**: LOW (acceptable duplication)

---

## 📊 SUCCESS METRICS

**Before Consolidation**:
- Identical Code Blocks: 88 occurrences
- Unique Patterns: 10
- High-Impact: 39 occurrences
- Medium-Impact: 9 occurrences
- Low-Impact (Test): 7 occurrences

**After Phase 1-2**:
- Identical Code Blocks: <10 occurrences (89% reduction)
- Unique Patterns: 2 (test code only)
- High-Impact: 0 occurrences (100% reduction)
- Medium-Impact: 0 occurrences (100% reduction)
- Low-Impact (Test): <10 occurrences (acceptable)

**Target**: 88 → <10 (89% reduction)

---

## 🎯 SSOT FILES TO CREATE

1. **`src/core/utils/validation_utils.py`** - Validation output formatting
2. **`src/core/constants/agent_constants.py`** - Agent list constants
3. **`src/core/utils/file_utils.py`** - File/directory operations
4. **`src/core/utils/github_utils.py`** - GitHub API utilities
5. **`src/core/messaging/messaging_protocol.py`** - Messaging protocol interface
6. **`src/services/vector_database/__init__.py`** - Vector DB import handling

---

## 🚨 RISK ASSESSMENT

### **Low Risk**:
- Validation utilities (simple function extraction)
- Agent constants (simple constant extraction)
- GitHub utilities (well-defined API patterns)

### **Medium Risk**:
- File utilities (Windows readonly handling)
- Messaging protocol (interface changes)
- Vector DB imports (dependency management)

### **Mitigation**:
- Comprehensive testing after each consolidation
- Gradual migration (one block at a time)
- Maintain backward compatibility where possible

---

## 📝 NEXT STEPS

1. **Immediate**: Begin Phase 1 - Create utility modules
2. **This Week**: Complete Phase 1 (high-impact blocks)
3. **Next Week**: Complete Phase 2 (protocol/interface)
4. **Ongoing**: Monitor test code duplication

---

**Report Generated By**: Agent-5 (Business Intelligence Specialist)  
**Date**: 2025-12-04  
**Status**: READY FOR EXECUTION

🐝 WE. ARE. SWARM. ⚡🔥


