# synthetic_github.py Refactoring Plan
**Date**: 2025-12-13  
**Agent**: Agent-1  
**File**: src/core/synthetic_github.py (1,043 lines)

## Current Issues

1. **Duplicate class definitions** detected:
   - `GitHubSandboxMode` appears at lines 30 and 551
   - `SyntheticGitHub` appears at lines 125 and 646
   - `get_synthetic_github()` appears at lines 516 and 1037

2. **V2 Violation**: 1,043 lines (3.5x limit of 300 lines)

## Proposed Module Structure

### Module 1: `src/core/github/sandbox_manager.py` (~200 lines)
- `GitHubSandboxMode` class (single instance, remove duplicate)
- Sandbox mode detection and configuration
- Auto-detection logic

### Module 2: `src/core/github/synthetic_client.py` (~250 lines)
- `SyntheticGitHub` class (single instance, remove duplicate)
- Main GitHub client interface
- API method routing
- Local/remote decision logic

### Module 3: `src/core/github/local_router.py` (~280 lines)
- Local storage routing
- Cache management
- Local-first strategy implementation
- Integration with local_repo_layer

### Module 4: `src/core/github/remote_router.py` (~200 lines)
- Remote GitHub API calls
- Rate limiting
- Error handling
- GitHub API client wrapper

### Module 5: `src/core/github/__init__.py` (~50 lines)
- Public API exports
- `get_synthetic_github()` factory function (single instance)
- Module initialization

**Total**: ~980 lines (reduced from 1,043, ~6% reduction)

## Implementation Steps

1. **Create module directory**: `src/core/github/`
2. **Extract sandbox_manager.py** (remove duplicate)
3. **Extract synthetic_client.py** (remove duplicate, keep main class)
4. **Extract local_router.py** (local-first logic)
5. **Extract remote_router.py** (GitHub API calls)
6. **Create __init__.py** (exports and factory)
7. **Update imports** across codebase
8. **Remove original file** after validation

## Dependencies

- `src/core/local_repo_layer.py`
- `src/core/deferred_push_queue.py`
- `src/core/config/timeout_constants.py`



