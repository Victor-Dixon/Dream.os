# main.py V2 Compliance Refactoring - Integration Review Plan

**Date:** 2025-12-19  
**Agents:** Agent-1 (Integration Review) + Agent-2 (Architecture)  
**Status:** 🔄 **INTEGRATION REVIEW ACTIVE**  
**File:** `main.py`  
**Violations:** 468 lines (target <500, but 6 function violations), needs modularization

---

## 🎯 Objective

Refactor `main.py` into modular components while maintaining integration compatibility:
- Extract agent mode selection → `agent_mode_selector` module
- Extract bot startup logic → `bot_startup` module
- Extract status checking → `status_checker` module

---

## 📊 Current Structure Analysis

### **File Statistics:**
- **Total Lines:** 468
- **V2 Compliance:** ⚠️ 6 function violations
- **Target:** <500 lines (file size OK, but function violations need addressing)

### **Current Components:**

1. **ServiceManager Class** (lines 46-337)
   - `__init__()` - Initialization
   - `setup_agent_mode_manager()` - Agent mode manager setup
   - `select_agent_mode()` - **Agent mode selection (lines 67-121)** → Extract to `agent_mode_selector`
   - `start_message_queue()` - Message queue startup
   - `start_twitch_bot()` - Twitch bot startup
   - `start_discord_bot()` - **Discord bot startup (lines 178-208)** → Extract to `bot_startup`
   - `check_status()` - **Status checking (lines 210-249)** → Extract to `status_checker`
   - `_check_process()` - Process checking helper
   - `_save_pid()` - PID file management
   - `_cleanup_pid()` - PID cleanup
   - `stop_all()` - Service shutdown

2. **main() Function** (lines 340-461)
   - Argument parsing
   - Service manager initialization
   - Service startup orchestration

---

## 🔄 Refactoring Plan

### **Module 1: agent_mode_selector.py**

**Location:** `src/core/agent_mode_selector.py`  
**Purpose:** Handle agent mode selection logic

**Extracted Functions:**
- `setup_agent_mode_manager()` - Setup agent mode manager
- `select_agent_mode()` - Interactive agent mode selection
- `get_current_mode()` - Get current agent mode
- `get_available_modes()` - Get available modes
- `set_agent_mode()` - Set agent mode

**Integration Points:**
- `src.core.agent_mode_manager` - Agent mode manager dependency
- `ServiceManager` - Integration with service manager

**Integration Checkpoint 1.1:** Agent Mode Selector Module
- ✅ Module created and functional
- ✅ Agent mode manager integration verified
- ✅ ServiceManager integration maintained
- ✅ Backward compatibility preserved

---

### **Module 2: bot_startup.py**

**Location:** `src/core/bot_startup.py`  
**Purpose:** Handle bot startup logic

**Extracted Functions:**
- `start_message_queue()` - Start message queue processor
- `start_twitch_bot()` - Start Twitch bot
- `start_discord_bot()` - Start Discord bot
- `start_all_services()` - Start all services
- `stop_all_services()` - Stop all services

**Integration Points:**
- `tools/start_message_queue_processor.py` - Message queue script
- `tools/START_CHAT_BOT_NOW.py` - Twitch bot script
- `tools/run_unified_discord_bot_with_restart.py` - Discord bot script
- `src/discord_commander/unified_discord_bot.py` - Discord bot alternative
- Environment variables (TWITCH_CHANNEL, TWITCH_ACCESS_TOKEN, DISCORD_BOT_TOKEN)
- PID file management

**Integration Checkpoint 2.1:** Bot Startup Module
- ✅ Module created and functional
- ✅ Service script integration verified
- ✅ Environment variable integration verified
- ✅ PID file management integrated
- ✅ ServiceManager integration maintained
- ✅ Backward compatibility preserved

---

### **Module 3: status_checker.py**

**Location:** `src/core/status_checker.py`  
**Purpose:** Handle service status checking

**Extracted Functions:**
- `check_status()` - Check all service statuses
- `check_message_queue_status()` - Check message queue status
- `check_twitch_bot_status()` - Check Twitch bot status
- `check_discord_bot_status()` - Check Discord bot status
- `_check_process()` - Process checking helper
- `_get_service_info()` - Get service information

**Integration Points:**
- `psutil` - Process checking
- PID file management (`pids/` directory)
- Environment variables (for configuration display)
- ServiceManager - Integration with service manager

**Integration Checkpoint 3.1:** Status Checker Module
- ✅ Module created and functional
- ✅ Process checking integration verified
- ✅ PID file management integrated
- ✅ Environment variable integration verified
- ✅ ServiceManager integration maintained
- ✅ Backward compatibility preserved

---

### **Refactored main.py**

**Target Size:** <200 lines (after extraction)  
**Purpose:** Entry point and orchestration

**Remaining Components:**
- Argument parsing
- ServiceManager initialization (minimal)
- Module imports and integration
- Main orchestration logic

**Integration Points:**
- `src.core.agent_mode_selector` - Agent mode selection
- `src.core.bot_startup` - Bot startup
- `src.core.status_checker` - Status checking
- `ServiceManager` - Service management (simplified)

**Integration Checkpoint 4.1:** Refactored main.py
- ✅ File size reduced to <200 lines
- ✅ All function violations resolved
- ✅ Module integration verified
- ✅ Backward compatibility preserved
- ✅ CLI interface unchanged

---

## 🔄 Integration Checkpoints

### **Checkpoint 1: Pre-Refactoring Integration Baseline**

**Status:** ⏳ **PENDING**

**Validation Areas:**
1. Current integration points documented
2. Dependencies identified
3. Integration test baseline created
4. Backward compatibility requirements defined

**Success Criteria:**
- ✅ All integration points documented
- ✅ All dependencies identified
- ✅ Integration test baseline created
- ✅ Backward compatibility requirements defined

---

### **Checkpoint 2: Agent Mode Selector Module Integration**

**Status:** ⏳ **PENDING**

**Validation Areas:**
1. Module created and functional
2. Agent mode manager integration verified
3. ServiceManager integration maintained
4. Backward compatibility preserved

**Success Criteria:**
- ✅ Module created and functional
- ✅ Agent mode manager integration verified
- ✅ ServiceManager integration maintained
- ✅ Backward compatibility preserved

---

### **Checkpoint 3: Bot Startup Module Integration**

**Status:** ⏳ **PENDING**

**Validation Areas:**
1. Module created and functional
2. Service script integration verified
3. Environment variable integration verified
4. PID file management integrated
5. ServiceManager integration maintained
6. Backward compatibility preserved

**Success Criteria:**
- ✅ Module created and functional
- ✅ Service script integration verified
- ✅ Environment variable integration verified
- ✅ PID file management integrated
- ✅ ServiceManager integration maintained
- ✅ Backward compatibility preserved

---

### **Checkpoint 4: Status Checker Module Integration**

**Status:** ⏳ **PENDING**

**Validation Areas:**
1. Module created and functional
2. Process checking integration verified
3. PID file management integrated
4. Environment variable integration verified
5. ServiceManager integration maintained
6. Backward compatibility preserved

**Success Criteria:**
- ✅ Module created and functional
- ✅ Process checking integration verified
- ✅ PID file management integrated
- ✅ Environment variable integration verified
- ✅ ServiceManager integration maintained
- ✅ Backward compatibility preserved

---

### **Checkpoint 5: Refactored main.py Integration**

**Status:** ⏳ **PENDING**

**Validation Areas:**
1. File size reduced to <200 lines
2. All function violations resolved
3. Module integration verified
4. Backward compatibility preserved
5. CLI interface unchanged

**Success Criteria:**
- ✅ File size reduced to <200 lines
- ✅ All function violations resolved
- ✅ Module integration verified
- ✅ Backward compatibility preserved
- ✅ CLI interface unchanged

---

### **Checkpoint 6: Post-Refactoring Integration Validation**

**Status:** ⏳ **PENDING**

**Validation Areas:**
1. All services start correctly
2. Agent mode selection works
3. Status checking works
4. Service management works
5. Integration tests pass
6. No regression in functionality

**Success Criteria:**
- ✅ All services start correctly
- ✅ Agent mode selection works
- ✅ Status checking works
- ✅ Service management works
- ✅ Integration tests pass
- ✅ No regression in functionality

---

## 📋 Integration Test Plan

### **Test 1: Agent Mode Selection Integration**

**Objective:** Verify agent mode selection works after refactoring

**Test Cases:**
1. Setup agent mode manager
2. Select agent mode interactively
3. Get current mode
4. Get available modes
5. Set agent mode

**Expected Results:**
- All agent mode operations work correctly
- Integration with agent_mode_manager maintained
- ServiceManager integration maintained

---

### **Test 2: Bot Startup Integration**

**Objective:** Verify bot startup works after refactoring

**Test Cases:**
1. Start message queue processor
2. Start Twitch bot
3. Start Discord bot
4. Start all services
5. Stop all services

**Expected Results:**
- All services start correctly
- Environment variables loaded correctly
- PID files created correctly
- Service scripts executed correctly

---

### **Test 3: Status Checking Integration**

**Objective:** Verify status checking works after refactoring

**Test Cases:**
1. Check message queue status
2. Check Twitch bot status
3. Check Discord bot status
4. Check all service statuses
5. Verify process checking

**Expected Results:**
- All status checks work correctly
- Process checking works correctly
- PID file reading works correctly
- Environment variable display works correctly

---

### **Test 4: CLI Interface Integration**

**Objective:** Verify CLI interface works after refactoring

**Test Cases:**
1. `python main.py` - Start all services
2. `python main.py --status` - Check status
3. `python main.py --select-mode` - Select agent mode
4. `python main.py --message-queue` - Start message queue
5. `python main.py --twitch` - Start Twitch bot
6. `python main.py --discord` - Start Discord bot

**Expected Results:**
- All CLI commands work correctly
- Output format unchanged
- Error handling works correctly
- Backward compatibility maintained

---

## 🎯 Success Metrics

1. **V2 Compliance:**
   - File size: <200 lines (main.py)
   - Function violations: 0
   - All modules <300 lines

2. **Integration Quality:**
   - All integration points functional
   - Backward compatibility preserved
   - No regression in functionality

3. **Code Quality:**
   - Modular structure clear
   - Separation of concerns achieved
   - Maintainability improved

---

## 🚀 Next Steps

1. **Immediate:**
   - ✅ Integration review plan created
   - ⏳ Coordinate with Agent-2 for architecture guidance
   - ⏳ Begin Checkpoint 1: Pre-Refactoring Integration Baseline

2. **Refactoring Phase:**
   - Create agent_mode_selector module
   - Create bot_startup module
   - Create status_checker module
   - Refactor main.py

3. **Integration Validation:**
   - Execute integration checkpoints
   - Run integration tests
   - Validate backward compatibility

---

**Status:** ✅ **INTEGRATION REVIEW PLAN CREATED** | 🔄 **AWAITING ARCHITECTURE GUIDANCE**  
**Next:** Coordinate with Agent-2 for architecture guidance, then begin refactoring

🐝 **WE. ARE. SWARM. ⚡**

