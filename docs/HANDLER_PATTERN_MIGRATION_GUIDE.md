# Handler Pattern Migration Guide - Quick Reference

**Date**: 2025-12-06  
**Author**: Agent-7 (Web Development Specialist)  
**Status**: ✅ **QUICK REFERENCE CREATED**

---

## 🚀 **QUICK START**

### **Pattern**: BaseHandler + AvailabilityMixin

**Full Documentation**: `swarm_brain/patterns/BASEHANDLER_AVAILABILITYMIXIN_MIGRATION_PATTERN.md`

---

## 📝 **BASIC TEMPLATE**

```python
from flask import jsonify, request
from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

# Lazy import
try:
    from src.services.my_service import MyService
    MY_SERVICE_AVAILABLE = True
except ImportError:
    MY_SERVICE_AVAILABLE = False


class MyHandlers(BaseHandler, AvailabilityMixin):
    """Handler class."""
    
    def __init__(self):
        super().__init__("MyHandlers")
    
    def handle_operation(self, request) -> tuple:
        # Check availability
        availability_error = self.check_availability(
            MY_SERVICE_AVAILABLE,
            "MyService"
        )
        if availability_error:
            return availability_error
        
        try:
            # Business logic
            result = service.operation()
            response = self.format_response(result, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_operation")
            return jsonify(error_response), 500
```

---

## ✅ **MIGRATION CHECKLIST**

1. [ ] Inherit from `BaseHandler, AvailabilityMixin`
2. [ ] Add `__init__()` with `super().__init__(handler_name)`
3. [ ] Replace availability checks with `check_availability()`
4. [ ] Replace error handling with `handle_error()`
5. [ ] Replace response formatting with `format_response()`
6. [ ] Update routes to use handler instance
7. [ ] Test all endpoints

---

## 📚 **FULL DOCUMENTATION**

See: `swarm_brain/patterns/BASEHANDLER_AVAILABILITYMIXIN_MIGRATION_PATTERN.md`

🐝 **WE. ARE. SWARM. ⚡🔥🚀**


