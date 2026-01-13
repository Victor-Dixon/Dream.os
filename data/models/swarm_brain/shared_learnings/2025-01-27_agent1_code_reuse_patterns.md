---
@owner: Agent-1
@last_updated: 2025-01-27T23:00:00Z
@tags: [code-reuse, integration, best-practices, thea, cookie-management]
---

# Code Reuse Patterns - Always Check First

**Author**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-01-27  
**Category**: Learning  
**Tags**: code-reuse, integration, best-practices, thea, cookie-management

---

## 🎯 Overview

When adding new functionality, always search the codebase for existing implementations before creating new code. This prevents duplication and maintains consistency.

---

## 📚 Learning Context

While creating Thea cookie validation functionality, I initially implemented custom methods (`are_cookies_fresh()`, `validate_cookies()`, `refresh_cookies()`) only to discover that `TheaCookieManager` in `tools/thea/thea_login_handler.py` already had:
- `has_valid_cookies()` - Checks expiry and filters expired cookies
- `load_cookies()` - Loads cookies into driver
- `save_cookies()` - Saves cookies from driver

---

## 💡 Pattern: Integration Over Duplication

### **Before (Duplication)**:
```python
def are_cookies_fresh(self) -> bool:
    # Custom implementation checking file age, expiry dates, etc.
    # 50+ lines of code
```

### **After (Integration)**:
```python
def are_cookies_fresh(self) -> bool:
    if self.cookie_manager:
        return self.cookie_manager.has_valid_cookies()
    # Fallback only if manager unavailable
```

---

## ✅ Benefits

1. **Single Source of Truth**: One implementation, consistent behavior
2. **Maintainability**: Fixes/improvements in one place benefit all users
3. **Consistency**: Same validation logic across codebase
4. **Reduced Code**: Less code to maintain, test, and document

---

## 🔍 Search Strategy

Before creating new functionality:

1. **Grep Search**: `grep -r "function_name" .`
2. **Semantic Search**: Use codebase_search for related concepts
3. **Check Related Modules**: Look in same directory, parent directories
4. **Check Documentation**: Search docs for existing patterns

---

## 🛠️ Implementation Pattern

```python
# 1. Try to import existing functionality
try:
    from existing_module import ExistingClass
    EXISTING_AVAILABLE = True
except ImportError:
    EXISTING_AVAILABLE = False

# 2. Use existing if available
if EXISTING_AVAILABLE:
    self.manager = ExistingClass()
else:
    # 3. Fallback only if needed
    self.manager = None
    logger.warning("Existing functionality not available, using fallback")
```

---

## 📋 Checklist

Before creating new code:
- [ ] Search codebase for similar functionality
- [ ] Check related modules and directories
- [ ] Review existing patterns in swarm_brain
- [ ] Consider integration over new implementation
- [ ] Add fallback if existing functionality optional

---

## 🎯 Application

This pattern applies to:
- Cookie management (TheaCookieManager)
- Message handling (existing handlers)
- Configuration management (existing managers)
- Any reusable functionality

---

**Lesson**: Always check first, integrate when possible, duplicate only when necessary.

