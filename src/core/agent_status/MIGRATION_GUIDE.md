# Agent Status API Migration Guide

## Overview

The agent status system has been consolidated from **4 separate implementations** into **1 unified API**. This reduces complexity by ~75% while maintaining all functionality.

## Before (4 Separate APIs)

```python
# OLD WAY - 4 different imports and APIs

# 1. Reading individual status
from src.core.agent_status.reader import AgentStatusReader
reader = AgentStatusReader()
status = reader.read_status("Agent-1")

# 2. Reading all statuses
from src.core.agent_status.reader import read_all_agent_status
all_statuses = read_all_agent_status()

# 3. Swarm aggregation
from src.core.agent_status.aggregator import SwarmStateAggregator
aggregator = SwarmStateAggregator()
swarm_state = aggregator.aggregate_swarm_state()

# 4. File watching
from src.core.agent_status.watcher import StatusFileWatcher
watcher = StatusFileWatcher()
watcher.register_callback("Agent-1", my_callback)
watcher.start_watching()
```

## After (1 Unified API)

```python
# NEW WAY - Single import, single API

from src.core.agent_status import UnifiedStatusReader

reader = UnifiedStatusReader()

# All operations through single interface
status = reader.get_agent_status("Agent-1")
all_statuses = reader.get_all_agent_statuses()
swarm_state = reader.get_swarm_state()

# File watching included
reader.watch_status_changes(my_callback)
reader.start_watching()
```

## API Comparison

| Operation | Old Way | New Way |
|-----------|---------|---------|
| Get single status | `AgentStatusReader().read_status()` | `reader.get_agent_status()` |
| Get all statuses | `read_all_agent_status()` | `reader.get_all_agent_statuses()` |
| Get swarm state | `SwarmStateAggregator().aggregate_swarm_state()` | `reader.get_swarm_state()` |
| Watch changes | `StatusFileWatcher().register_callback()` | `reader.watch_status_changes()` |
| Cache management | `StatusCache().invalidate()` | `reader.invalidate_cache()` |

## Convenience Functions

For simple operations, use convenience functions:

```python
from src.core.agent_status import get_agent_status, get_all_agent_statuses, get_swarm_state

# No need to create reader instance
status = get_agent_status("Agent-1")
all_statuses = get_all_agent_statuses()
swarm_state = get_swarm_state()
```

## Advanced Features

### Automatic Caching
```python
reader = UnifiedStatusReader(cache_ttl=10.0)  # 10 second cache
status = reader.get_agent_status("Agent-1")    # Cached automatically
```

### File Watching with Callbacks
```python
def on_status_change(agent_id, old_status, new_status):
    print(f"{agent_id} status changed!")

reader.watch_status_changes(on_status_change)
reader.start_watching()  # Runs in background thread
```

### Async Support
```python
# For async contexts
status = await reader.get_agent_status_async("Agent-1")
all_statuses = await reader.get_all_agent_statuses_async()
```

### Cache Management
```python
# Invalidate specific agent
reader.invalidate_cache("Agent-1")

# Invalidate all
reader.invalidate_cache()

# Get cache statistics
stats = reader.get_cache_stats()
```

## Migration Steps

### Phase 1: Replace Imports (Low Risk)
```python
# Replace these imports:
- from src.core.agent_status.reader import AgentStatusReader, read_all_agent_status
- from src.core.agent_status.aggregator import SwarmStateAggregator
- from src.core.agent_status.watcher import StatusFileWatcher
- from src.core.agent_status.cache import StatusCache

# With this single import:
from src.core.agent_status import UnifiedStatusReader
```

### Phase 2: Update Instantiation (Low Risk)
```python
# Replace multiple instances:
reader = AgentStatusReader()
aggregator = SwarmStateAggregator()
watcher = StatusFileWatcher()
cache = StatusCache()

# With single instance:
reader = UnifiedStatusReader()  # Includes all functionality
```

### Phase 3: Update Method Calls (Medium Risk)
```python
# Replace these patterns:
reader.read_status(agent_id)
read_all_agent_status()
aggregator.aggregate_swarm_state()
watcher.register_callback(agent_id, callback)

# With unified calls:
reader.get_agent_status(agent_id)
reader.get_all_agent_statuses()
reader.get_swarm_state()
reader.watch_status_changes(callback)
```

### Phase 4: Remove Legacy Code (Low Risk)
Once all usage is migrated, legacy implementations can be marked as deprecated and eventually removed.

## Backward Compatibility

Legacy APIs remain available but are deprecated:

```python
# Still works but deprecated
from src.core.agent_status import AgentStatusReader, StatusFileWatcher  # ⚠️ Deprecated

# New recommended way
from src.core.agent_status import UnifiedStatusReader  # ✅ Recommended
```

## Benefits

- **75% fewer imports** - 4 imports → 1 import
- **Single API surface** - No need to know which class does what
- **Automatic integration** - Caching, watching, and aggregation work together
- **Better performance** - Shared caching and optimized operations
- **Thread safety** - All operations are thread-safe
- **Async support** - Native async/await support
- **Resource management** - Automatic cleanup with context managers

## Testing

The unified API has been tested with existing agent workspaces and maintains full compatibility with current status.json formats.

```bash
# Test the unified API
cd /path/to/repo
python -c "
from src.core.agent_status import UnifiedStatusReader
reader = UnifiedStatusReader()
print('Agents found:', len(reader.get_all_agent_statuses()))
print('Swarm state:', reader.get_swarm_state()['summary'])
"
```

## Questions?

If you encounter issues during migration:
1. Check the convenience functions for simple use cases
2. Use `force_refresh=True` if caching causes issues
3. The API is fully backward compatible during transition
4. All original functionality is preserved