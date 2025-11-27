# Integration Templates - Swarm Reference

**Date**: 2025-11-26  
**Created By**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **TEMPLATES READY**  
**For**: Swarm-wide integration work

---

## 🎯 **INTEGRATION TEMPLATES**

### **Template 1: Repository Integration Template**

```markdown
# [Repository Name] Integration Plan

**Target SSOT**: [SSOT Repository]  
**Source Repos**: [List of source repos]  
**Status**: ⏳ IN PROGRESS

## Phase 0: Pre-Integration Cleanup
- [ ] Detect venv files
- [ ] Detect duplicates
- [ ] Remove venv files
- [ ] Resolve duplicates
- [ ] Check integration issues

## Phase 1: Pattern Extraction
- [ ] Extract patterns
- [ ] Categorize patterns
- [ ] Document patterns
- [ ] Map to services

## Phase 2: Service Integration
- [ ] Review existing services
- [ ] Enhance services
- [ ] Test integration

## Phase 3: Testing & Validation
- [ ] Create tests
- [ ] Test functionality
- [ ] Update documentation
```

---

### **Template 2: Service Enhancement Template**

```python
"""
[Service Name] - Enhanced Service
=================================

Enhanced with patterns from [Merged Repos].
"""

from typing import Dict, Any, Optional
from .base_service import BaseService

class EnhancedService(BaseService):
    """Enhanced service with integrated patterns."""
    
    def __init__(self, repository=None, pattern_handler=None):
        super().__init__(repository)
        self.pattern_handler = pattern_handler
    
    def existing_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Existing method - maintain compatibility."""
        # Existing logic
        pass
    
    def new_pattern_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """New method from merged repo pattern."""
        # New pattern logic
        pass
```

---

### **Template 3: Pattern Extraction Template**

```markdown
# Pattern Extraction Report - [Repository Name]

**Date**: [Date]  
**Repository**: [Repository Name]  
**Status**: ✅ COMPLETE

## Patterns Extracted

### Pattern 1: [Pattern Name]
- **Type**: [Service/Data/API/Test]
- **Files**: [List of files]
- **Classes**: [List of classes]
- **Functions**: [List of functions]
- **Integration Point**: [Service/Component]

### Pattern 2: [Pattern Name]
- **Type**: [Service/Data/API/Test]
- **Files**: [List of files]
- **Classes**: [List of classes]
- **Functions**: [List of functions]
- **Integration Point**: [Service/Component]

## Service Mapping

| Pattern | Target Service | Enhancement Plan |
|---------|---------------|------------------|
| Pattern 1 | Service A | Add method X |
| Pattern 2 | Service B | Add method Y |
```

---

### **Template 4: Integration Test Template**

```python
"""
Integration Tests for [Service Name]
====================================
"""

import pytest
from unittest.mock import Mock, patch
from services.enhanced_service import EnhancedService

class TestEnhancedService:
    """Integration tests for enhanced service."""
    
    def test_existing_method_compatibility(self):
        """Test existing method maintains compatibility."""
        service = EnhancedService()
        result = service.existing_method({"key": "value"})
        assert result["success"] is True
    
    def test_new_pattern_method(self):
        """Test new pattern method."""
        service = EnhancedService()
        result = service.new_pattern_method({"key": "value"})
        assert result["success"] is True
    
    def test_backward_compatibility(self):
        """Test backward compatibility."""
        service = EnhancedService()
        # Test that existing code still works
        pass
```

---

### **Template 5: Integration Checklist Template**

```markdown
# Integration Checklist - [Repository Name]

## Pre-Integration
- [ ] Repository cloned
- [ ] Venv files detected and removed
- [ ] Duplicates detected and resolved
- [ ] Integration issues checked

## Pattern Extraction
- [ ] Patterns extracted
- [ ] Patterns categorized
- [ ] Patterns documented
- [ ] Patterns mapped to services

## Service Integration
- [ ] Existing services reviewed
- [ ] Services enhanced
- [ ] Backward compatibility maintained
- [ ] Service interfaces updated

## Testing
- [ ] Unit tests created
- [ ] Integration tests created
- [ ] Tests passing
- [ ] Coverage adequate

## Documentation
- [ ] Service documentation updated
- [ ] Integration documentation created
- [ ] Usage examples provided
- [ ] Architecture docs updated
```

---

## 📋 **TEMPLATE USAGE**

### **For Repository Integration**:
1. Copy Template 1
2. Fill in repository details
3. Follow phase-by-phase process
4. Update status as you progress

### **For Service Enhancement**:
1. Copy Template 2
2. Implement service enhancement
3. Add new pattern methods
4. Maintain backward compatibility

### **For Pattern Extraction**:
1. Copy Template 3
2. Extract patterns from repos
3. Document patterns
4. Map to services

### **For Testing**:
1. Copy Template 4
2. Create integration tests
3. Test compatibility
4. Test new functionality

### **For Tracking**:
1. Copy Template 5
2. Use as checklist
3. Track progress
4. Mark complete

---

**Status**: ✅ **TEMPLATES READY**  
**Last Updated**: 2025-11-26 14:35:00 (Local System Time)

