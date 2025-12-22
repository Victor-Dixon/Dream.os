# SSOT Patterns Reference Guide

**Author:** Agent-8 (SSOT & System Integration Specialist)  
**Date:** 2025-01-27  
**Status:** ACTIVE

---

## 🎯 PURPOSE

Reference guide for SSOT (Single Source of Truth) patterns used across the codebase.
Ensures consistency and prevents violations.

---

## 📋 CORE SSOT PATTERNS

### **1. Repository Pattern**

**Purpose:** Single source of truth for data access.

**Pattern:**
```python
class MessageRepository:
    """SSOT for message data operations."""
    
    def __init__(self, data_file: str = "data/message_history.json"):
        self.data_file = Path(data_file)
    
    def save_message(self, message: dict) -> bool:
        """Save message - ONLY data operations, no business logic."""
        # Load, append, save - that's it
        pass
    
    def get_message_history(self, limit: int = 100) -> List[dict]:
        """Get message history - ONLY data retrieval."""
        pass
```

**Rules:**
- ✅ Data access only (load, save, query)
- ❌ No business logic
- ❌ No validation (except data format)
- ❌ No calculations

**Examples:**
- ✅ `src/repositories/message_repository.py` - MessageRepository
- ✅ `src/repositories/` - All repositories follow this pattern

---

### **2. Service Pattern**

**Purpose:** Business logic layer that uses repositories.

**Pattern:**
```python
class MessagingService:
    """Business logic for messaging."""
    
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository  # Injected dependency
    
    def send_message(self, content: str, sender: str, recipient: str) -> bool:
        """Send message - business logic here."""
        # Validate, process, then use repository
        message = self._validate_message(content, sender, recipient)
        return self.message_repository.save_message(message)
```

**Rules:**
- ✅ Business logic only
- ✅ Uses repositories for data access
- ❌ No direct file I/O
- ❌ No direct database access

**Examples:**
- ✅ `src/core/messaging_core.py` - Uses MessageRepository
- ✅ `src/services/` - All services follow this pattern

---

### **3. Configuration Pattern**

**Purpose:** Single source of truth for configuration.

**Pattern:**
```python
# Single config file
class UnifiedConfig:
    """SSOT for all configuration."""
    
    AGENT_COORDINATES = {...}  # Single definition
    MESSAGE_TYPES = {...}      # Single definition
    PRIORITIES = {...}         # Single definition
```

**Rules:**
- ✅ One config file per domain
- ✅ Constants defined once
- ❌ No duplicate constants
- ❌ No scattered config

**Examples:**
- ✅ `src/core/unified_config.py` - Unified configuration
- ✅ `cursor_agent_coords.json` - Single coordinate source

---

### **4. Dependency Injection Pattern**

**Purpose:** Ensure SSOT through dependency injection.

**Pattern:**
```python
class UnifiedMessagingCore:
    """SSOT for messaging functionality."""
    
    def __init__(self, message_repository: MessageRepository = None):
        # Inject dependency - allows testing and SSOT enforcement
        if message_repository is None:
            from ..repositories.message_repository import MessageRepository
            self.message_repository = MessageRepository()
        else:
            self.message_repository = message_repository  # Use injected
```

**Rules:**
- ✅ Accept dependencies in `__init__`
- ✅ Create default if not provided
- ❌ Don't create new instances in methods
- ❌ Don't bypass injected dependencies

**Examples:**
- ✅ `UnifiedMessagingCore` - Injects MessageRepository
- ✅ `MessageQueue` - Injects MessageRepository
- ✅ `MessageQueueProcessor` - Injects MessageRepository

---

## 🔍 SSOT VIOLATION PATTERNS

### **Violation 1: Duplicate Class Definitions**

**Problem:**
```python
# File 1: tools/categories/captain_tools.py
class LeaderboardUpdateTool(IToolAdapter):
    ...

# File 2: tools/categories/captain_coordination_tools.py
class LeaderboardUpdaterTool(IToolAdapter):  # ❌ DUPLICATE
    ...
```

**Solution:**
- ✅ Consolidate into single class
- ✅ Use one location as SSOT
- ✅ Deprecate duplicate

---

### **Violation 2: Multiple Repository Instances**

**Problem:**
```python
def send_message(...):
    # ❌ Creating new instance instead of using injected
    repo = MessageRepository()  # Should use self.message_repository
    repo.save_message(...)
```

**Solution:**
- ✅ Use injected `self.message_repository`
- ✅ Pass repository through constructor
- ✅ Don't create new instances

---

### **Violation 3: Scattered Configuration**

**Problem:**
```python
# File 1: config.py
AGENT_COORDINATES = {...}

# File 2: settings.py
AGENT_COORDINATES = {...}  # ❌ DUPLICATE

# File 3: constants.py
AGENT_COORDINATES = {...}  # ❌ DUPLICATE
```

**Solution:**
- ✅ Single config file
- ✅ Import from SSOT location
- ✅ No duplicate definitions

---

### **Violation 4: Direct File I/O in Services**

**Problem:**
```python
class MessagingService:
    def save_message(self, message):
        # ❌ Direct file I/O - should use repository
        with open("data/messages.json", "w") as f:
            json.dump(message, f)
```

**Solution:**
- ✅ Use repository for data access
- ✅ Service handles business logic only
- ✅ Repository handles data operations

---

## ✅ SSOT COMPLIANCE CHECKLIST

### **For Repositories:**
- [ ] Only data access operations (load, save, query)
- [ ] No business logic
- [ ] No validation (except data format)
- [ ] Single instance per entity type

### **For Services:**
- [ ] Uses repositories for data access
- [ ] No direct file I/O
- [ ] No direct database access
- [ ] Business logic only

### **For Configuration:**
- [ ] Single config file per domain
- [ ] Constants defined once
- [ ] No duplicate definitions
- [ ] Imported from SSOT location

### **For Dependency Injection:**
- [ ] Dependencies injected in `__init__`
- [ ] Default creation if not provided
- [ ] Use injected dependencies, don't create new
- [ ] No bypassing injected dependencies

---

## 🛠️ SSOT VALIDATION TOOLS

### **Tool 1: Detect Violations**
```bash
python -m tools.toolbelt ssot.detect_violations --directory src
```

**Detects:**
- Duplicate classes
- Duplicate functions
- Multiple repositories
- Scattered configuration
- Duplicate constants

### **Tool 2: Validate Patterns**
```bash
python -m tools.toolbelt ssot.validate_patterns --file_path src/repositories/message_repository.py --pattern_type repository
```

**Validates:**
- Repository pattern compliance
- Service pattern compliance
- Config pattern compliance

---

## 📊 SSOT METRICS

### **Good Metrics:**
- ✅ 1 repository per entity type
- ✅ 1 config file per domain
- ✅ Services use repositories (no direct I/O)
- ✅ Dependencies injected (not created)

### **Bad Metrics:**
- ❌ Multiple repositories for same entity
- ❌ Scattered configuration files
- ❌ Direct file I/O in services
- ❌ Creating new instances instead of using injected

---

## 🎯 SSOT ENFORCEMENT

### **Automated:**
- ✅ SSOT validation tools (`ssot.detect_violations`, `ssot.validate_patterns`)
- ✅ Pre-commit hooks (can be added)
- ✅ CI/CD checks (can be added)

### **Manual:**
- ✅ Code reviews check SSOT compliance
- ✅ Architecture reviews verify patterns
- ✅ Documentation updated when patterns change

---

## 📚 RELATED DOCUMENTATION

- `docs/ssot/SSOT_ENFORCEMENT_GUIDE.md` - Enforcement procedures
- `docs/architecture/REPOSITORY_PATTERN.md` - Repository pattern details
- `docs/architecture/SERVICE_PATTERN.md` - Service pattern details

---

**Status:** ✅ ACTIVE  
**Last Updated:** 2025-01-27  
**Maintained By:** Agent-8 (SSOT & System Integration Specialist)

---

**🐝 WE. ARE. SWARM. SSOT COMPLIANT.** ⚡🔥🚀




