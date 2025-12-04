<!-- SSOT Domain: architecture -->
# Service Architecture Patterns - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **ARCHITECTURE PATTERNS DOCUMENTED**  
**For**: Swarm-wide service architecture reference

---

## 🎯 **SERVICE ARCHITECTURE PRINCIPLES**

### **1. Service Enhancement Over Duplication**
- ✅ Enhance existing services
- ❌ Don't create duplicate services
- ✅ Maintain backward compatibility
- ✅ Update service interfaces

### **2. Unified Service Layer**
- ✅ Single service per domain
- ✅ Clear service boundaries
- ✅ Repository pattern for data access
- ✅ Dependency injection

### **3. Service Interface Design**
- ✅ Clear, consistent interfaces
- ✅ Error handling built-in
- ✅ Validation at boundaries
- ✅ Documentation required

---

## 🏗️ **SERVICE ARCHITECTURE PATTERNS**

### **Pattern 1: Base Service Pattern**

```python
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class BaseService(ABC):
    """Base service class with common functionality."""
    
    def __init__(self, repository=None):
        self.repository = repository
        self._initialized = False
    
    def initialize(self):
        """Initialize service."""
        if not self._initialized:
            self._do_initialize()
            self._initialized = True
    
    @abstractmethod
    def _do_initialize(self):
        """Service-specific initialization."""
        pass
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data."""
        # Common validation logic
        return True
    
    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors consistently."""
        return {"error": str(error), "success": False}
```

---

### **Pattern 2: Service Enhancement Pattern**

```python
class EnhancedService(BaseService):
    """Enhanced service with integrated patterns."""
    
    def __init__(self, repository=None, new_pattern_handler=None):
        super().__init__(repository)
        self.new_pattern_handler = new_pattern_handler
    
    def existing_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Existing method - maintain compatibility."""
        self.initialize()
        if not self.validate_input(data):
            return self.handle_error(ValueError("Invalid input"))
        
        # Existing logic
        result = self.repository.get(data)
        return {"success": True, "data": result}
    
    def new_pattern_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """New method from merged repo pattern."""
        self.initialize()
        if not self.validate_input(data):
            return self.handle_error(ValueError("Invalid input"))
        
        # New pattern logic
        if self.new_pattern_handler:
            result = self.new_pattern_handler.process(data)
            return {"success": True, "data": result}
        
        return self.handle_error(ValueError("Pattern handler not available"))
```

---

### **Pattern 3: Repository Pattern Integration**

```python
class ServiceWithRepository(BaseService):
    """Service using repository pattern."""
    
    def __init__(self, repository):
        super().__init__(repository)
        self.repository = repository
    
    def get_data(self, id: str) -> Optional[Dict[str, Any]]:
        """Get data using repository."""
        self.initialize()
        try:
            return self.repository.find_by_id(id)
        except Exception as e:
            return self.handle_error(e)
    
    def save_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save data using repository."""
        self.initialize()
        if not self.validate_input(data):
            return self.handle_error(ValueError("Invalid input"))
        
        try:
            result = self.repository.save(data)
            return {"success": True, "data": result}
        except Exception as e:
            return self.handle_error(e)
```

---

### **Pattern 4: Service Composition Pattern**

```python
class CompositeService(BaseService):
    """Service composed of multiple services."""
    
    def __init__(self, services: List[BaseService]):
        super().__init__()
        self.services = services
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process using composed services."""
        self.initialize()
        results = []
        
        for service in self.services:
            service.initialize()
            result = service.process(data)
            results.append(result)
        
        return {"success": True, "results": results}
```

---

## 📋 **SERVICE ARCHITECTURE CHECKLIST**

### **Service Design**:
- [ ] Inherits from BaseService
- [ ] Implements required methods
- [ ] Has clear responsibility
- [ ] Uses repository pattern
- [ ] Has error handling
- [ ] Has input validation
- [ ] Has documentation

### **Service Integration**:
- [ ] Enhances existing service (not duplicates)
- [ ] Maintains backward compatibility
- [ ] Updates service interface
- [ ] Adds new functionality
- [ ] Tests integration
- [ ] Updates documentation

---

## 🎯 **SERVICE ARCHITECTURE BEST PRACTICES**

### **Do**:
- ✅ Use BaseService pattern
- ✅ Enhance existing services
- ✅ Use repository pattern
- ✅ Implement error handling
- ✅ Document services

### **Don't**:
- ❌ Duplicate services
- ❌ Break backward compatibility
- ❌ Skip error handling
- ❌ Skip validation
- ❌ Skip documentation

---

**Status**: ✅ **ARCHITECTURE PATTERNS DOCUMENTED**  
**Last Updated**: 2025-11-26 14:35:00 (Local System Time)

