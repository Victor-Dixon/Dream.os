# BaseHandler + AvailabilityMixin Migration Pattern

**Date**: 2025-12-06  
**Author**: Agent-7 (Web Development Specialist)  
**Reference**: `agent_workspaces/Agent-8/HANDLER_CONSOLIDATION_COMPLETE.md`  
**Status**: ✅ **DOCUMENTATION COMPLETE**

---

## 📋 **OVERVIEW**

This pattern consolidates handler development by using `BaseHandler` and `AvailabilityMixin` to eliminate duplication and standardize error handling, response formatting, and availability checks.

**Benefits**:
- **30-33% code reduction** across all handlers
- **100% elimination** of error handling duplication
- **100% elimination** of response formatting duplication
- **73% reduction** in availability check duplication
- Standardized logging and error handling
- Better testability with instance methods

---

## 🏗️ **ARCHITECTURE**

### **BaseHandler**

**Location**: `src/core/base/base_handler.py`

**Provides**:
- Consolidated initialization (via InitializationMixin)
- Error handling (via ErrorHandlingMixin)
- Response formatting (`format_response()`)
- Error response formatting (`handle_error()`)
- Logging initialization
- Request validation (`validate_request()`)

### **AvailabilityMixin**

**Location**: `src/core/base/availability_mixin.py`

**Provides**:
- Service/module availability checking (`check_availability()`)
- Standardized 503 responses for unavailable services

---

## 📝 **PATTERN IMPLEMENTATION**

### **1. Handler Class Structure**

```python
from flask import jsonify, request
from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

class MyHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for my operations."""
    
    def __init__(self):
        """Initialize handlers."""
        super().__init__("MyHandlers")
```

**Key Points**:
- Inherit from `BaseHandler` and `AvailabilityMixin`
- Call `super().__init__()` with handler name
- Handler name used for logging identification

---

### **2. Handler Method Pattern**

#### **Before (Static Methods - OLD PATTERN)**:
```python
class SomeHandlers:
    @staticmethod
    def handle_something(request) -> tuple:
        if not SERVICE_AVAILABLE:
            return jsonify({"success": False, "error": "Service not available"}), 503
        try:
            result = service.do_something()
            return jsonify({"success": True, "data": result}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
```

#### **After (BaseHandler Pattern - NEW PATTERN)**:
```python
class SomeHandlers(BaseHandler, AvailabilityMixin):
    def __init__(self):
        super().__init__("SomeHandlers")
    
    def handle_something(self, request) -> tuple:
        # Check availability using mixin
        availability_error = self.check_availability(
            SERVICE_AVAILABLE,
            "Service"
        )
        if availability_error:
            return availability_error
        
        try:
            # Business logic
            result = service.do_something()
            
            # Format response using base handler
            response = self.format_response(result, success=True)
            return jsonify(response), 200
        except Exception as e:
            # Handle error using base handler
            error_response = self.handle_error(e, "handle_something")
            return jsonify(error_response), 500
```

---

### **3. Availability Check Pattern**

#### **Before**:
```python
if not SERVICE_AVAILABLE:
    return jsonify({"success": False, "error": "Service not available"}), 503
```

#### **After**:
```python
availability_error = self.check_availability(
    SERVICE_AVAILABLE,
    "Service"
)
if availability_error:
    return availability_error
```

**Benefits**:
- Standardized error messages
- Consistent response format
- Reduced duplication (73% reduction)

---

### **4. Error Handling Pattern**

#### **Before**:
```python
except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 500
```

#### **After**:
```python
except Exception as e:
    error_response = self.handle_error(e, "method_name")
    return jsonify(error_response), 500
```

**Benefits**:
- Centralized error logging
- Consistent error response format
- Context information included

---

### **5. Response Formatting Pattern**

#### **Before**:
```python
return jsonify({"success": True, "data": result}), 200
```

#### **After**:
```python
response = self.format_response(result, success=True)
return jsonify(response), 200
```

**Benefits**:
- Consistent response structure
- Handler name automatically included
- Easy to extend

---

### **6. Route Pattern**

#### **Before (Static Methods)**:
```python
from src.web.some_handlers import SomeHandlers

@route_bp.route("/something", methods=["POST"])
def handle():
    return SomeHandlers.handle_something(request)
```

#### **After (Handler Instance)**:
```python
from src.web.some_handlers import SomeHandlers

# Create handler instance
some_handlers = SomeHandlers()

@route_bp.route("/something", methods=["POST"])
def handle():
    return some_handlers.handle_something(request)
```

**Key Points**:
- Create handler instance at module level
- Use instance methods instead of static methods
- Better for dependency injection and testing

---

## 📚 **COMPLETE EXAMPLE**

### **Handler Implementation**:
```python
"""
My Service Handlers - Web Layer
================================

Handler classes for my service operations.

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin.
"""

from flask import jsonify, request
from typing import Tuple, Any

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

# Lazy import with availability flag
try:
    from src.services.my_service import MyService
    MY_SERVICE_AVAILABLE = True
except ImportError:
    MY_SERVICE_AVAILABLE = False


class MyServiceHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for my service operations."""
    
    def __init__(self):
        """Initialize my service handlers."""
        super().__init__("MyServiceHandlers")
    
    def _get_service(self):
        """Get service instance (lazy import pattern)."""
        if MY_SERVICE_AVAILABLE:
            return MyService()
        return None
    
    def handle_operation(self, request) -> Tuple[Any, int]:
        """
        Handle my service operation.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability
        availability_error = self.check_availability(
            MY_SERVICE_AVAILABLE,
            "MyService"
        )
        if availability_error:
            return availability_error
        
        try:
            # Parse request
            data = request.get_json() or {}
            param = data.get("param")
            
            if not param:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="param is required"
                )
                return jsonify(error_response), 400
            
            # Get service and execute
            service = self._get_service()
            result = service.operation(param)
            
            # Format response
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_operation")
            return jsonify(error_response), 500
```

### **Route Implementation**:
```python
"""
My Service Routes
=================

Flask routes for my service operations.

V2 Compliance: < 300 lines, route definitions.
"""

from flask import Blueprint, jsonify

from src.web.my_service_handlers import MyServiceHandlers

# Create blueprint
my_service_bp = Blueprint("my_service", __name__, url_prefix="/api/my-service")

# Create handler instance (BaseHandler pattern)
my_service_handlers = MyServiceHandlers()


@my_service_bp.route("/operation", methods=["POST"])
def operation():
    """Handle my service operation."""
    return my_service_handlers.handle_operation(request)


@my_service_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "my_service"}), 200
```

---

## ✅ **MIGRATION CHECKLIST**

### **Step 1: Update Imports**
- [ ] Import `BaseHandler` from `src.core.base.base_handler`
- [ ] Import `AvailabilityMixin` from `src.core.base.availability_mixin`
- [ ] Remove static method decorators

### **Step 2: Update Class Declaration**
- [ ] Change class to inherit from `BaseHandler, AvailabilityMixin`
- [ ] Add `__init__()` method calling `super().__init__(handler_name)`
- [ ] Remove `@staticmethod` decorators

### **Step 3: Update Handler Methods**
- [ ] Replace availability checks with `self.check_availability()`
- [ ] Replace error handling with `self.handle_error()`
- [ ] Replace response formatting with `self.format_response()`
- [ ] Change method signature: remove `@staticmethod`, add `self`

### **Step 4: Update Route Files**
- [ ] Create handler instance: `my_handlers = MyHandlers()`
- [ ] Update route handlers to use instance: `my_handlers.handle_method(request)`

### **Step 5: Testing**
- [ ] Verify all endpoints work correctly
- [ ] Test error handling
- [ ] Test availability checks
- [ ] Verify response format
- [ ] Check logging output

### **Step 6: Documentation**
- [ ] Update handler docstrings
- [ ] Update route docstrings
- [ ] Verify V2 compliance (LOC < 300)

---

## 🎯 **BEST PRACTICES**

### **1. Handler Initialization**
```python
def __init__(self):
    """Initialize handlers."""
    super().__init__("HandlerName")  # Use descriptive name
```

### **2. Availability Checks**
```python
# Always check at method start
availability_error = self.check_availability(
    SERVICE_AVAILABLE,
    "ServiceName"  # Clear service name
)
if availability_error:
    return availability_error
```

### **3. Error Handling**
```python
# Always use handle_error for exceptions
except Exception as e:
    error_response = self.handle_error(e, "method_name")
    return jsonify(error_response), 500
```

### **4. Response Formatting**
```python
# Use format_response for success
response = self.format_response(result, success=True)
return jsonify(response), 200

# Use format_response for errors (validation)
error_response = self.format_response(
    None,
    success=False,
    error="Error message"
)
return jsonify(error_response), 400
```

### **5. Lazy Imports**
```python
# At module level
try:
    from src.services.my_service import MyService
    MY_SERVICE_AVAILABLE = True
except ImportError:
    MY_SERVICE_AVAILABLE = False

# In handler method
def _get_service(self):
    if MY_SERVICE_AVAILABLE:
        return MyService()
    return None
```

---

## 📊 **MIGRATION RESULTS** (Reference)

**Handlers Migrated**: 10 handlers  
**Code Reduction**: 30.5% average (30-33% per handler)  
**Lines Before**: ~1,110 lines  
**Lines After**: ~772 lines  
**Reduction**: ~338 lines eliminated

**Duplication Eliminated**:
- ✅ 100% error handling duplication
- ✅ 100% response formatting duplication
- ✅ 73% availability check duplication
- ✅ 100% static method pattern

---

## 🔍 **TROUBLESHOOTING**

### **Issue: Import Errors**
**Solution**: Ensure `src.core.base.base_handler` and `src.core.base.availability_mixin` are importable.

### **Issue: Handler Not Initialized**
**Solution**: Ensure `super().__init__()` is called in `__init__()`.

### **Issue: Response Format Mismatch**
**Solution**: Use `self.format_response()` consistently - don't manually create response dicts.

### **Issue: Availability Check Not Working**
**Solution**: Ensure availability flag is set correctly and `check_availability()` is called before service usage.

---

## 📚 **REFERENCES**

- **BaseHandler**: `src/core/base/base_handler.py`
- **AvailabilityMixin**: `src/core/base/availability_mixin.py`
- **Consolidation Report**: `agent_workspaces/Agent-8/HANDLER_CONSOLIDATION_COMPLETE.md`
- **Example Handlers**:
  - `src/web/agent_management_handlers.py`
  - `src/web/integrations_handlers.py`
  - `src/web/scheduler_handlers.py`

---

**Status**: ✅ **PATTERN DOCUMENTED**  
**Use**: Reference for all future handler development

🐝 **WE. ARE. SWARM. ⚡🔥🚀**


