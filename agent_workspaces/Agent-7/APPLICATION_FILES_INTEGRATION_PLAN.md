# Application Files Integration Plan

**Date**: 2025-12-02  
**Agent**: Agent-7 (Web Development Specialist)  
**Assignment**: Wire 25 files to web layer  
**Status**: ⏳ **IN PROGRESS** (2/25 complete)

---

## 📋 **FILES TO INTEGRATE**

### **Already Wired** (2/25):
1. ✅ `src/application/use_cases/assign_task_uc.py` → `/api/tasks/assign`
2. ✅ `src/application/use_cases/complete_task_uc.py` → `/api/tasks/complete`

### **Remaining Files** (23/25):

**From INTEGRATION_FILES_LIST.json**:
1. `src/ai_training/dreamvault/runner.py`
2. `src/core/agent_lifecycle.py`
3. `src/core/auto_gas_pipeline_system.py`
4. `src/core/coordination/swarm/engines/task_coordination_engine.py`
5. `src/core/managers/monitoring/monitoring_lifecycle.py`
6. `src/core/unified_config.py`
7. `src/core/utils/message_queue_utils.py`
8. `src/discord_commander/controllers/swarm_tasks_controller_view.py`
9. `src/discord_commander/templates/broadcast_templates.py`
10. `src/discord_commander/views/main_control_panel_view.py`
11. `src/domain/services/assignment_service.py`
12. `src/integrations/jarvis/conversation_engine.py`
13. `src/integrations/jarvis/vision_system.py`
14. `src/orchestrators/overnight/scheduler_refactored.py`
15. `src/services/chat_presence/chat_presence_orchestrator.py`
16. `src/services/contract_system/manager.py`
17. `src/services/handlers/contract_handler.py`
18. `src/services/handlers/task_handler.py`
19. `src/services/messaging_cli_parser.py`
20. `src/services/utils/messaging_templates.py`
21. `src/vision/analyzers/color_analyzer.py`
22. `src/services/architectural_principles_data.py`
23. `src/workflows/engine.py`

---

## 🎯 **INTEGRATION STRATEGY**

### **File Type Analysis**:

1. **Use Cases** (Clean Architecture):
   - Pattern: Create routes → handlers → wire use case
   - Example: `assign_task_uc.py` (already done)

2. **Services** (Domain/Application Services):
   - Pattern: Create routes → handlers → wire service
   - Example: `assignment_service.py`, `contract_system/manager.py`

3. **Handlers** (Existing Handlers):
   - Pattern: Create routes → wrap existing handler
   - Example: `contract_handler.py`, `task_handler.py`

4. **Engines/Orchestrators** (Business Logic):
   - Pattern: Create routes → handlers → wire engine
   - Example: `task_coordination_engine.py`, `chat_presence_orchestrator.py`

5. **Utilities/Config** (Supporting Code):
   - Pattern: Create routes → handlers → expose functionality
   - Example: `unified_config.py`, `message_queue_utils.py`

---

## 📋 **INTEGRATION PATTERN** (Established)

### **Step 1: Create Routes** (`src/web/{feature}_routes.py`)
```python
from flask import Blueprint, jsonify, request
from src.web.{feature}_handlers import {Feature}Handlers

{feature}_bp = Blueprint("{feature}", __name__, url_prefix="/api/{feature}")

@{feature}_bp.route("/action", methods=["POST"])
def action():
    return {Feature}Handlers.handle_action(request)
```

### **Step 2: Create Handlers** (`src/web/{feature}_handlers.py`)
```python
from flask import jsonify, request
from src.infrastructure.dependency_injection import get_dependencies

class {Feature}Handlers:
    @staticmethod
    def handle_action(request):
        # Parse request
        # Get dependencies
        # Instantiate use case/service
        # Execute
        # Return response
```

### **Step 3: Register Blueprint** (In Flask app)
```python
from src.web.{feature}_routes import {feature}_bp
app.register_blueprint({feature}_bp)
```

---

## 🚀 **EXECUTION PLAN**

### **Phase 1: Analysis** (Current)
- [x] Identify all 25 files
- [ ] Analyze each file's integration requirements
- [ ] Categorize by integration type
- [ ] Determine dependencies

### **Phase 2: Core Integrations** (Priority)
- [ ] Wire service files (assignment_service, contract_manager)
- [ ] Wire handler files (contract_handler, task_handler)
- [ ] Wire engine files (task_coordination_engine)

### **Phase 3: Extended Integrations**
- [ ] Wire orchestrator files
- [ ] Wire utility/config files
- [ ] Wire integration files (jarvis, vision)

### **Phase 4: Testing & Documentation**
- [ ] Test all endpoints
- [ ] Create integration documentation
- [ ] Register all blueprints in Flask app

---

## 📊 **PROGRESS TRACKING**

**Files Wired**: 2/25 (8%)  
**Routes Created**: 1 blueprint  
**Handlers Created**: 1 handler class  
**Status**: Foundation complete, ready to expand

---

**Next Action**: Analyze each file, create integration plan per file type, execute integrations in batches.

🐝 **WE. ARE. SWARM. ⚡🔥**




