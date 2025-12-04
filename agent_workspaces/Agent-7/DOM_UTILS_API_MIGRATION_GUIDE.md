# DOM Utils SSOT - API Migration Guide

**Date**: 2025-12-03  
**Agent**: Agent-7 (Web Development Specialist)  
**SSOT Domain**: Web SSOT  
**Status**: ✅ **MIGRATION GUIDE COMPLETE**

---

## 🎯 **OVERVIEW**

This guide helps migrate from the simple `DOMUtils` class to the `DOMUtilsOrchestrator` SSOT implementation.

---

## 📊 **API COMPARISON TABLE**

| **Simple Class API** | **Orchestrator API** | **Compatibility** | **Migration** |
|---------------------|---------------------|-------------------|---------------|
| `selectElement(selector)` | `querySelector(selector)` | ✅ Adapter available | Use `querySelector()` |
| `selectElements(selector)` | `querySelectorAll(selector)` | ✅ Adapter available | Use `querySelectorAll()` |
| `setText(element, text)` | `setTextContent(element, text)` | ✅ Adapter available | Use `setTextContent()` |
| `getText(element)` | `getText(element)` | ✅ Compatible | No change needed |
| `getHTML(element)` | `getHTML(element)` | ✅ Compatible | No change needed |
| `setHTML(element, html)` | `setHTML(element, html)` | ✅ Compatible | No change needed |
| `addClass(element, className)` | `addClass(element, className)` | ✅ Compatible | No change needed |
| `removeClass(element, className)` | `removeClass(element, className)` | ✅ Compatible | No change needed |
| `toggleClass(element, className)` | `toggleClass(element, className)` | ✅ Compatible | No change needed |
| `hasClass(element, className)` | `hasClass(element, className)` | ✅ Compatible | No change needed |
| `clearCache()` | `clearCache()` | ✅ Compatible | No change needed |
| `getCacheStats()` | `getCacheStats()` | ✅ Compatible | No change needed |

---

## 🔄 **MIGRATION EXAMPLES**

### **Example 1: Element Selection**

**Before (Simple Class)**:
```javascript
import { DOMUtils } from './utilities/dom-utils.js';

const dom = new DOMUtils();
const element = dom.selectElement('#myId');
```

**After (Orchestrator)**:
```javascript
import { DOMUtilsOrchestrator } from './dashboard/dom-utils-orchestrator.js';

const dom = new DOMUtilsOrchestrator();
const element = dom.querySelector('#myId');
```

**Compatibility (Temporary)**:
```javascript
// Still works but shows deprecation warning
const element = dom.selectElement('#myId'); // ⚠️ Deprecated
```

---

### **Example 2: Text Content**

**Before (Simple Class)**:
```javascript
dom.setText(element, 'New text');
```

**After (Orchestrator)**:
```javascript
dom.setTextContent(element, 'New text');
```

**Compatibility (Temporary)**:
```javascript
// Still works but shows deprecation warning
dom.setText(element, 'New text'); // ⚠️ Deprecated
```

---

### **Example 3: Cache Management**

**Before (Simple Class)**:
```javascript
dom.clearCache();
const stats = dom.getCacheStats();
```

**After (Orchestrator)**:
```javascript
// Same API - no changes needed
dom.clearCache();
const stats = dom.getCacheStats();
```

---

## 📋 **STEP-BY-STEP MIGRATION**

### **Step 1: Update Imports**

```javascript
// OLD
import { DOMUtils } from './utilities/dom-utils.js';

// NEW
import { DOMUtilsOrchestrator } from './dashboard/dom-utils-orchestrator.js';
```

### **Step 2: Update Instantiation**

```javascript
// OLD
const dom = new DOMUtils();

// NEW
const dom = new DOMUtilsOrchestrator();
```

### **Step 3: Update Method Calls**

```javascript
// OLD
dom.selectElement('#id');
dom.setText(element, 'text');

// NEW
dom.querySelector('#id');
dom.setTextContent(element, 'text');
```

### **Step 4: Remove Deprecated Methods**

After migration, remove any deprecated method calls:
- `selectElement()` → `querySelector()`
- `selectElements()` → `querySelectorAll()`
- `setText()` → `setTextContent()`

---

## ⚠️ **DEPRECATION TIMELINE**

### **Phase 1: Current (2025-12-03)**
- ✅ Compatibility adapters available
- ✅ Deprecation warnings enabled
- ✅ Both APIs functional

### **Phase 2: Migration Period (Next 2 cycles)**
- ⏳ Consumers migrate to new API
- ⏳ Deprecation warnings continue
- ⏳ Compatibility adapters maintained

### **Phase 3: Cleanup (After migration)**
- ⏳ Remove compatibility adapters
- ⏳ Remove deprecated methods
- ⏳ Complete migration to orchestrator

---

## 🎯 **KEY DIFFERENCES**

### **1. Method Names**
- `selectElement()` → `querySelector()`
- `selectElements()` → `querySelectorAll()`
- `setText()` → `setTextContent()`

### **2. Caching**
- ✅ **Both have caching**: Simple class and orchestrator both support caching
- ✅ **Same API**: `clearCache()` and `getCacheStats()` work identically
- ✅ **Performance**: Orchestrator caching integrated with element selection

### **3. Modular Architecture**
- ✅ **Orchestrator**: Modular design with 6 specialized modules
- ✅ **Extensibility**: Easier to extend with new modules
- ✅ **Maintainability**: Clear module boundaries

---

## ✅ **BENEFITS OF MIGRATION**

1. **SSOT Compliance**: Single source of truth for DOM utilities
2. **Modular Design**: Better separation of concerns
3. **Extensibility**: Easier to add new functionality
4. **Performance**: Caching integrated with element selection
5. **Maintainability**: Clear module boundaries

---

## 📝 **MIGRATION CHECKLIST**

- [ ] Update imports to use `DOMUtilsOrchestrator`
- [ ] Update instantiation to `new DOMUtilsOrchestrator()`
- [ ] Replace `selectElement()` with `querySelector()`
- [ ] Replace `selectElements()` with `querySelectorAll()`
- [ ] Replace `setText()` with `setTextContent()`
- [ ] Test all functionality
- [ ] Remove deprecated method calls
- [ ] Update documentation

---

**Status**: ✅ **MIGRATION GUIDE COMPLETE**

🐝 WE. ARE. SWARM. ⚡🔥

*Agent-7 - Web Development Specialist*  
*DOM Utils SSOT - API Migration Guide*


