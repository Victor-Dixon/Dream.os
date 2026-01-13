# Agent Status Monitor System Analysis

**Date:** 2025-12-31  
**Requested By:** User (dadudekc)  
**Analyzed By:** Agent-2 (Architecture & Design Specialist)

## 🔍 Findings: Multiple Implementations Found

The agent status monitoring system consists of **6 distinct implementations** with overlapping functionality but different purposes and integration points.

---

## Implementation Overview

### Implementation 1: `src/discord_commander/status_change_monitor.py`

**Author:** Agent-4 (Captain), Refactored by Agent-1 (V2 Compliance)  
**Date:** 2025-12-30  
**V2 Compliant:** Yes (272 lines)  
**SSOT Domain:** discord

**Purpose:** Real-time Discord bot integration for monitoring agent status.json changes and posting automatic updates.

**How it works:**
1. Monitors all agent status.json files (Agent-1 through Agent-8) via file modification timestamps
2. Detects changes in key fields: `status`, `current_phase`, `current_mission`, `points_earned`, `completed_tasks`, `current_tasks`
3. Debounces updates (5-second threshold) to prevent spam
4. Posts Discord embeds via `StatusEmbedFactory` when changes detected
5. Integrates with `ResumerHandler` for inactivity detection
6. Supports persistent dashboard updates (placeholder implementation)
7. Runs as async Discord bot task loop (5-second intervals)

**Key Features:**
- ✅ Real-time file change detection (mtime-based)
- ✅ Debouncing to prevent spam
- ✅ Retry logic for JSON reading (3 attempts)
- ✅ Discord embed generation via helper module
- ✅ Inactivity detection integration
- ✅ Persistent dashboard support (stub)

**Dependencies:**
- Discord.py (discord.ext.tasks)
- `src.discord_commander.monitor.status_embeds.StatusEmbedFactory`
- `src.discord_commander.monitor.resumer_logic.ResumerHandler`

**Integration Points:**
- Discord bot lifecycle (starts with bot)
- Agent workspace file system (`agent_workspaces/Agent-X/status.json`)
- Discord channels (agent-status, captain-updates, swarm-status)

**Bugs/Issues:**
- Dashboard update logic is placeholder (line 220-231)
- Inactivity checks hook exists but activity_detector was disabled
- Hardcoded agent list (Agent-1 through Agent-8)
- No configuration for check intervals or debounce thresholds

**Code Quality:**
- Well-structured with clear separation (helpers extracted)
- Proper error handling with retry logic
- V2 compliant (under 400 lines)
- Type hints included
- Async/await properly used

---

### Implementation 2: `tools/system_health_dashboard.py`

**Author:** Agent-2 (Architecture & Design)  
**Date:** 2025-12-28  
**V2 Compliant:** Yes (329 lines)  
**SSOT Domain:** tools

**Purpose:** Comprehensive system health monitoring dashboard for services, resources, and agent coordinates.

**How it works:**
1. Monitors system services (message_queue, discord_bot, twitch_bot) via PID tracking
2. Checks system resources (CPU, memory, disk) using psutil
3. Validates agent coordinates (PyAutoGUI screen bounds)
4. Tracks alerts with severity levels (critical, warning, error, info)
5. Provides console dashboard output
6. Runs as background thread with configurable interval (30 seconds default)

**Key Features:**
- ✅ Service health monitoring (PID existence, zombie detection)
- ✅ System resource monitoring (CPU, memory, disk)
- ✅ Agent coordinate validation
- ✅ Alert system with severity levels
- ✅ Console dashboard output
- ✅ Thread-based monitoring loop

**Dependencies:**
- psutil (process and system monitoring)
- pyautogui (coordinate validation)

**Integration Points:**
- System process monitoring
- Agent coordinate system
- Service PID tracking

**Bugs/Issues:**
- Hardcoded service list (message_queue, discord_bot, twitch_bot)
- Hardcoded agent coordinates (should read from config)
- Incomplete alert messages (lines 100, 102, 123, 125, 127 - missing format strings)
- Missing sys import (line 199 references sys.version_info)
- Disk usage check uses hardcoded '/' path (Windows incompatible)

**Code Quality:**
- Good structure with clear separation
- Proper threading implementation
- V2 compliant
- Missing type hints
- Some incomplete error messages

---

### Implementation 3: `tools/discord_health_monitor.py`

**Author:** Agent-2 (Architecture & Design)  
**Date:** 2025-12-28  
**V2 Compliant:** Yes (178 lines)  
**SSOT Domain:** tools

**Purpose:** Specialized Discord bot health monitoring to prevent heartbeat timeouts and detect bot failures.

**How it works:**
1. Monitors Discord bot process via PID
2. Tracks heartbeat timestamps
3. Detects heartbeat timeouts (60-second threshold)
4. Attempts recovery (heartbeat restart, graceful restart)
5. Monitors bot responsiveness (CPU, memory usage)
6. Triggers shutdown on unrecoverable failures

**Key Features:**
- ✅ Process existence monitoring
- ✅ Heartbeat timeout detection
- ✅ Recovery mechanisms (heartbeat restart, graceful restart)
- ✅ Resource usage monitoring
- ✅ Thread-based monitoring loop

**Dependencies:**
- psutil (process monitoring)

**Integration Points:**
- Discord bot process (PID-based)
- System shutdown mechanism (stub)

**Bugs/Issues:**
- Recovery mechanisms are stubs (lines 94-103, 105-113)
- Shutdown trigger is stub (line 115-118)
- Incomplete warning messages (lines 130, 132 - missing format strings)
- No actual heartbeat restart implementation
- No graceful restart implementation

**Code Quality:**
- Clean structure
- Proper threading
- V2 compliant
- Missing type hints
- Recovery logic incomplete

---

### Implementation 4: `tools/coordination_status_summary.py`

**Author:** Unknown  
**Date:** Unknown  
**V2 Compliant:** Yes (38 lines)  
**SSOT Domain:** tools

**Purpose:** Quick summary tool for extracting active coordinations from Agent-4 status.json.

**How it works:**
1. Reads Agent-4 status.json
2. Extracts `active_coordinations` field
3. Filters for ACTIVE/IN_PROGRESS status
4. Prints formatted summary to console

**Key Features:**
- ✅ Simple, focused tool
- ✅ Fast coordination visibility
- ✅ Minimal dependencies

**Dependencies:**
- None (standard library only)

**Integration Points:**
- Agent-4 status.json only

**Bugs/Issues:**
- Hardcoded to Agent-4 only
- No error handling for missing fields
- Console output only (no structured output)

**Code Quality:**
- Very simple, single-purpose
- V2 compliant
- No type hints
- Minimal error handling

---

### Implementation 5: `src/utils/agent_queue_status.py`

**Author:** Agent-4 (Captain)  
**Date:** 2025-11-27  
**V2 Compliant:** Yes (261 lines)  
**SSOT Domain:** core

**Purpose:** Manages agent Cursor queue status to prevent queue buildup and optimize message delivery.

**How it works:**
1. Tracks agent queue status (full/available) in status.json
2. Maintains in-memory cache for quick lookups
3. Persists cache to `runtime/agent_queue_status.json`
4. Provides methods: `mark_full()`, `mark_available()`, `is_full()`, `get_status()`
5. Cache refresh mechanism (5-minute TTL)

**Key Features:**
- ✅ Queue status tracking
- ✅ In-memory cache with file persistence
- ✅ Cache TTL (5 minutes)
- ✅ Prevents PyAutoGUI queue buildup

**Dependencies:**
- None (standard library only)

**Integration Points:**
- Agent status.json files
- Message delivery system (PyAutoGUI vs inbox routing)

**Bugs/Issues:**
- Cache TTL logic could be improved
- No automatic cache refresh mechanism
- Single cache file for all agents (could be per-agent)

**Code Quality:**
- Clean class-based design
- Proper caching strategy
- V2 compliant
- Type hints included
- Good error handling

---

### Implementation 6: `tools/categories/swarm_state_reader.py`

**Author:** Agent-8 (SSOT & System Integration)  
**Date:** Unknown  
**V2 Compliant:** Yes (167 lines)  
**SSOT Domain:** tools

**Purpose:** Reads and parses complete swarm state from all agent workspaces for mission control and analysis.

**How it works:**
1. Reads all agent status.json files (Agent-1 through Agent-8)
2. Aggregates swarm state: agents, active_missions, completed_today, total_points
3. Reads agent context (status, inbox count, recent messages)
4. Analyzes available work (V2 violations, captain orders)
5. Provides agent specialty mapping

**Key Features:**
- ✅ Complete swarm state aggregation
- ✅ Agent context reading (status + inbox)
- ✅ Available work analysis
- ✅ Agent specialty mapping

**Dependencies:**
- None (standard library only)

**Integration Points:**
- All agent workspaces
- Project analysis files
- Captain execution orders

**Bugs/Issues:**
- Hardcoded agent list
- Simplified available work analysis (stub-like)
- No error handling for missing files
- Silent failures (try/except with pass)

**Code Quality:**
- Functional approach
- V2 compliant
- No type hints
- Minimal error handling

---

## 📊 Comparison Matrix

| Feature | Status Change Monitor | System Health Dashboard | Discord Health Monitor | Coordination Summary | Queue Status | Swarm State Reader |
|---------|----------------------|------------------------|----------------------|---------------------|--------------|-------------------|
| **Author** | Agent-4/Agent-1 | Agent-2 | Agent-2 | Unknown | Agent-4 | Agent-8 |
| **V2 Compliant** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Lines of Code** | 272 | 329 | 178 | 38 | 261 | 167 |
| **Type Hints** | ✅ Yes | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Real-time Monitoring** | ✅ Yes (5s) | ✅ Yes (30s) | ✅ Yes (30s) | ❌ No | ❌ No | ❌ No |
| **Discord Integration** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **File Change Detection** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **System Resource Monitoring** | ❌ No | ✅ Yes | ✅ Yes (bot only) | ❌ No | ❌ No | ❌ No |
| **Service Health** | ❌ No | ✅ Yes | ✅ Yes (bot only) | ❌ No | ❌ No | ❌ No |
| **Queue Status** | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Swarm Aggregation** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Inactivity Detection** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Alert System** | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Dashboard Output** | ✅ Yes (stub) | ✅ Yes | ❌ No | ✅ Yes (console) | ❌ No | ❌ No |
| **Cross-Platform** | ✅ Yes | ⚠️ Partial | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🎯 Key Differences

### 1. **Monitoring Scope**
- **Status Change Monitor:** Agent status.json file changes only
- **System Health Dashboard:** System services, resources, coordinates
- **Discord Health Monitor:** Discord bot process health only
- **Coordination Summary:** Agent-4 coordinations only
- **Queue Status:** Cursor queue status only
- **Swarm State Reader:** Complete swarm state aggregation

### 2. **Real-time vs On-Demand**
- **Real-time:** Status Change Monitor, System Health Dashboard, Discord Health Monitor
- **On-demand:** Coordination Summary, Queue Status, Swarm State Reader

### 3. **Integration Points**
- **Discord Bot:** Status Change Monitor (integrated), others standalone
- **File System:** All read status.json, different purposes
- **System Services:** System Health Dashboard, Discord Health Monitor

### 4. **Output Channels**
- **Discord:** Status Change Monitor only
- **Console:** System Health Dashboard, Coordination Summary
- **API/Data:** Queue Status, Swarm State Reader

---

## 🚨 Issues & Concerns

### Duplication
- **Status Reading:** All implementations read status.json files independently
- **Agent List:** Hardcoded Agent-1 through Agent-8 in multiple places
- **Error Handling:** Inconsistent error handling patterns

### Missing Features
- **Status Change Monitor:** Dashboard update logic incomplete
- **System Health Dashboard:** Incomplete alert messages, missing sys import
- **Discord Health Monitor:** Recovery mechanisms are stubs
- **Coordination Summary:** Hardcoded to Agent-4 only
- **Swarm State Reader:** Simplified work analysis

### Cross-Platform Issues
- **System Health Dashboard:** Hardcoded '/' disk path (Windows incompatible)
- **Status Change Monitor:** Should work cross-platform (Path-based)

### Maintenance Burden
- **6 separate implementations** mean 6 places to update when status.json format changes
- **No shared status reading library** (each reads independently)
- **Inconsistent error handling** across implementations

---

## 💡 Recommendations

### Option 1: Create Unified Status Reading Library (Recommended)

**Structure:**
```
src/core/agent_status/
├── __init__.py
├── status_reader.py      # Unified status.json reading with caching
├── status_watcher.py     # File change detection (extracted from StatusChangeMonitor)
├── status_aggregator.py  # Swarm state aggregation (from SwarmStateReader)
└── status_cache.py       # Shared caching layer
```

**Benefits:**
- Single source of truth for status reading
- Shared caching reduces file I/O
- Consistent error handling
- Easier to maintain when status.json format changes

**Migration:**
- Extract status reading logic from all 6 implementations
- Create unified library
- Update all implementations to use library
- Maintain backward compatibility during transition

### Option 2: Consolidate Monitoring Tools

**Structure:**
```
tools/monitoring/
├── __init__.py
├── agent_status_monitor.py    # Real-time status monitoring (from StatusChangeMonitor)
├── system_health_monitor.py   # System health (from SystemHealthDashboard)
├── discord_health_monitor.py  # Discord bot health (existing)
├── queue_status_monitor.py    # Queue status (from AgentQueueStatus)
└── swarm_state_reader.py      # Swarm aggregation (existing)
```

**Benefits:**
- Grouped by purpose
- Easier to discover related tools
- Shared utilities possible

### Option 3: Hybrid Approach (Best of Both)

**Recommended Structure:**
```
src/core/agent_status/          # Core library
├── __init__.py
├── reader.py                    # Unified status reading
├── watcher.py                   # File change detection
├── aggregator.py                # Swarm state aggregation
└── cache.py                     # Caching layer

tools/monitoring/                # Monitoring tools
├── __init__.py
├── agent_status_monitor.py      # Uses core library
├── system_health_dashboard.py   # Uses core library
├── discord_health_monitor.py    # Uses core library
└── coordination_summary.py      # Uses core library
```

**Features:**
- ✅ Core library for shared functionality
- ✅ Tools use core library (no duplication)
- ✅ Clear separation of concerns
- ✅ Easy to maintain and extend

---

## 🔧 Immediate Actions Required

1. **Fix Critical Bugs:**
   - System Health Dashboard: Fix incomplete alert messages (lines 100, 102, 123, 125, 127)
   - System Health Dashboard: Add missing sys import
   - System Health Dashboard: Fix hardcoded '/' disk path for Windows
   - Discord Health Monitor: Fix incomplete warning messages (lines 130, 132)

2. **Create Status Reading Library:**
   - Extract common status reading logic
   - Implement shared caching
   - Create unified error handling

3. **Consolidate Agent List:**
   - Create single source for agent IDs (Agent-1 through Agent-8)
   - Update all implementations to use shared source

4. **Complete Stub Implementations:**
   - Status Change Monitor: Complete dashboard update logic
   - Discord Health Monitor: Implement recovery mechanisms
   - Swarm State Reader: Enhance work analysis

5. **Add Type Hints:**
   - System Health Dashboard
   - Discord Health Monitor
   - Coordination Summary
   - Swarm State Reader

---

## 📝 Additional Notes

### Status Change Monitor Integration
- Integrated with Discord bot lifecycle
- Uses Discord.py tasks for async monitoring
- Extracted helpers for V2 compliance (status_embeds.py, resumer_logic.py)

### System Health Dashboard
- Thread-based monitoring (non-blocking)
- Console output for visibility
- Alert system with severity levels

### Queue Status System
- Prevents Cursor queue buildup
- Used by messaging system for delivery routing
- Cache-based for performance

### Swarm State Reader
- Used by mission control systems
- Provides complete swarm context
- Analyzes available work

---

## ✅ Conclusion

**Current State:** Six distinct implementations with overlapping functionality but different purposes. Each serves a specific monitoring need but shares common patterns (status.json reading, agent list).

**Recommended Path:** Create unified status reading library (Option 1 or Option 3) to eliminate duplication while maintaining specialized monitoring tools for different purposes.

**Priority:** Medium-High (duplication creates maintenance burden, but each tool serves distinct purpose)

**Next Steps:**
1. Fix critical bugs in System Health Dashboard and Discord Health Monitor
2. Create unified status reading library
3. Migrate implementations to use library
4. Add type hints to all implementations
5. Complete stub implementations

---

*Analysis completed: 2025-12-31*  
*Next Review: After consolidation decision*

