# 🔍 Phase 2: Web/Config Dependency Map

**Created**: 2025-01-28  
**Agent**: Agent-7 (Web Development Specialist)  
**Status**: ✅ COMPLETE  
**Purpose**: Map all web routes, services, and APIs dependent on config for Phase 2 migration testing

---

## 📊 **DEPENDENCY OVERVIEW**

### **Config Files Being Migrated**:
1. `src/core/config/config_manager.py` (785 lines) - HIGH PRIORITY
2. `src/core/config.py` (240 lines) - HIGH PRIORITY  
3. `runtime/core/utils/config.py` (225 lines) - MEDIUM PRIORITY
4. `chat_mate/config/chat_mate_config.py` (23 lines) - LOW PRIORITY
5. `Scripts/Utilities/config_handling/config.py` (TROOP) - LOW PRIORITY

### **Target**: `src/core/config_ssot.py` (unified config system)

---

## 🌐 **WEB ROUTES DEPENDENCIES**

### **1. trading_robot/web/dashboard.py**
- **Config Import**: `from config.settings import config`
- **Usage**: Dashboard configuration, settings access
- **Priority**: HIGH (web interface)
- **Testing Required**: ✅ Dashboard routes, API endpoints

### **2. trading_robot/web/dashboard_routes.py** (if exists)
- **Config Usage**: FastAPI routes using config
- **Priority**: HIGH
- **Testing Required**: ✅ All FastAPI routes, WebSocket endpoints

---

## 🔧 **SERVICE LAYER DEPENDENCIES**

### **1. src/services/config.py**
- **Config Import**: `from src.core.config_core import get_config`
- **Usage**: Service-level config accessor
- **Priority**: HIGH (core service dependency)
- **Testing Required**: ✅ Service initialization, config accessors

### **2. src/services/chatgpt/session.py**
- **Config Import**: `from ...core.config_ssot import get_unified_config`
- **Usage**: ChatGPT session configuration
- **Priority**: MEDIUM
- **Testing Required**: ✅ Session creation, config access

### **3. src/services/chatgpt/navigator.py**
- **Config Import**: `from ...core.config_ssot import get_unified_config`
- **Usage**: ChatGPT navigation configuration
- **Priority**: MEDIUM
- **Testing Required**: ✅ Navigation functionality

### **4. src/services/chatgpt/extractor.py**
- **Config Import**: `from ...core.config_ssot import get_unified_config`
- **Usage**: ChatGPT extraction configuration
- **Priority**: MEDIUM
- **Testing Required**: ✅ Extraction functionality

### **5. src/services/agent_management.py**
- **Config Usage**: Load agent assignments from configuration
- **Priority**: HIGH (agent coordination)
- **Testing Required**: ✅ Agent assignment loading

### **6. src/services/learning_recommender.py**
- **Config Usage**: Load config from file if provided
- **Priority**: LOW
- **Testing Required**: ✅ Config file loading

---

## 🔌 **API ENDPOINT DEPENDENCIES**

### **Web APIs**:
- Dashboard API endpoints (via dashboard.py)
- FastAPI routes (if dashboard_routes.py exists)
- WebSocket connections
- Authentication/authorization config

### **Service APIs**:
- ChatGPT service endpoints
- Agent management APIs
- Learning recommender APIs

---

## 📋 **CONFIG USAGE PATTERNS**

### **Pattern 1: Direct Import**
```python
from src.core.config_core import get_config
from ...core.config_ssot import get_unified_config
from config.settings import config
```

### **Pattern 2: Service Config Accessor**
```python
# Via src/services/config.py
from src.services.config import get_config
```

### **Pattern 3: Runtime Config**
```python
# Via runtime/core/utils/config.py
from runtime.core.utils.config import get_config
```

---

## 🧪 **INTEGRATION TESTING PRIORITIES**

### **HIGH PRIORITY** (Test Immediately):
1. ✅ `trading_robot/web/dashboard.py` - Web interface
2. ✅ `src/services/config.py` - Core service dependency
3. ✅ `src/services/agent_management.py` - Agent coordination

### **MEDIUM PRIORITY** (Test After High Priority):
1. ✅ `src/services/chatgpt/*` - ChatGPT services
2. ✅ FastAPI routes (if dashboard_routes.py exists)

### **LOW PRIORITY** (Test After Medium Priority):
1. ✅ `src/services/learning_recommender.py` - Optional feature

---

## 🎯 **TESTING STRATEGY**

### **Phase 2.1: Pre-Migration Baseline**
- Document current config usage
- Create test baseline
- Identify critical paths

### **Phase 2.2: Post-Migration Validation**
- Test each service after migration
- Verify web routes functional
- Validate API endpoints
- Check error handling

### **Phase 2.3: Regression Testing**
- Full integration test suite
- Performance validation
- Backward compatibility verification

---

## 📊 **DEPENDENCY GRAPH**

```
config_ssot.py (Target)
├── src/services/config.py (HIGH)
│   └── All services using config
├── trading_robot/web/dashboard.py (HIGH)
│   └── Web interface, API endpoints
├── src/services/chatgpt/* (MEDIUM)
│   ├── session.py
│   ├── navigator.py
│   └── extractor.py
├── src/services/agent_management.py (HIGH)
└── src/services/learning_recommender.py (LOW)
```

---

## ✅ **STATUS**

- [x] Web routes identified
- [x] Services mapped
- [x] Config usage patterns documented
- [x] Dependency graph created
- [x] Testing priorities established

**Next**: Create integration test suite

---

**Last Updated**: 2025-01-28  
**Agent**: Agent-7 (Web Development Specialist)

