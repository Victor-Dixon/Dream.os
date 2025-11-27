# 🧪 Testing Patterns Guide - New Pattern

**Date**: 2025-11-24  
**Agent**: Agent-6 (Coordination & Communication Specialist)  
**Status**: ✅ **ACTIVE**

---

## 🎯 **NEW TESTING PATTERN**

### **Pattern Overview**:
- **Framework**: pytest
- **Structure**: Class-based test organization
- **Fixtures**: Use pytest fixtures for setup
- **Mocking**: unittest.mock for dependencies
- **Async**: pytest.mark.asyncio for async tests

---

## 📋 **TEST STRUCTURE**

### **Standard Test Class Pattern**:

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

# Skip if required modules not available
try:
    from src.core.module_to_test import ClassToTest
except ImportError:
    pytest.skip("Required modules not available", allow_module_level=True)


class TestClassName:
    """Test suite for ClassName."""
    
    @pytest.fixture
    def test_instance(self):
        """Create test instance."""
        return ClassToTest()
    
    @pytest.fixture
    def sample_data(self):
        """Sample test data."""
        return {
            "key": "value"
        }
    
    def test_basic_functionality(self, test_instance, sample_data):
        """Test basic functionality."""
        result = test_instance.method(sample_data)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_functionality(self, test_instance):
        """Test async functionality."""
        result = await test_instance.async_method()
        assert result is not None
```

---

## 🔧 **KEY PATTERNS**

### **1. Fixture Pattern**:
```python
@pytest.fixture
def test_instance(self):
    """Create test instance."""
    return ClassToTest()
```

### **2. Mock Pattern**:
```python
@patch('module.dependency')
def test_with_mock(self, mock_dependency):
    """Test with mocked dependency."""
    mock_dependency.return_value = "mocked"
    result = test_instance.method()
    assert result == "expected"
```

### **3. Async Pattern**:
```python
@pytest.mark.asyncio
async def test_async(self, test_instance):
    """Test async method."""
    result = await test_instance.async_method()
    assert result is not None
```

### **4. Skip Pattern**:
```python
try:
    from src.core.module import Class
except ImportError:
    pytest.skip("Required modules not available", allow_module_level=True)
```

---

## 📊 **TEST ORGANIZATION**

### **Directory Structure**:
```
tests/
├── unit/
│   ├── core/
│   │   ├── test_module.py
│   │   └── test_another.py
│   └── services/
│       └── test_service.py
├── integration/
│   └── test_integration.py
└── conftest.py
```

### **Test Naming**:
- **File**: `test_module_name.py`
- **Class**: `TestClassName`
- **Method**: `test_functionality_description`

---

## ✅ **BEST PRACTICES**

1. **Use Fixtures**: For reusable test data and instances
2. **Mock Dependencies**: Isolate unit under test
3. **Clear Names**: Descriptive test names
4. **Async Support**: Use `@pytest.mark.asyncio` for async
5. **Skip Gracefully**: Handle missing dependencies
6. **Assert Clearly**: Use meaningful assertions

---

## 🎯 **EXAMPLES**

### **Example 1: Unit Test**:
```python
class TestMessageQueue:
    @pytest.fixture
    def queue(self):
        return MessageQueue()
    
    def test_enqueue(self, queue):
        queue_id = queue.enqueue({"test": "data"})
        assert queue_id is not None
```

### **Example 2: Integration Test**:
```python
@pytest.mark.asyncio
async def test_message_delivery():
    queue = MessageQueue()
    processor = MessageQueueProcessor(queue)
    await processor.process_batch()
    assert queue.get_statistics()["delivered"] > 0
```

---

## 🐝 **WE. ARE. SWARM.**

**Status**: ✅ **ACTIVE PATTERN**  
**Framework**: pytest  
**Structure**: Class-based with fixtures

**Agent-6 (Coordination & Communication Specialist)**  
**Testing Patterns Guide - 2025-11-24**


