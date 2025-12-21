# Test Architecture Review & Best Practices
**Date**: 2025-12-14  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Context**: Coordination with Agent-1 on V2 Compliance & Test Infrastructure

---

## 📋 Executive Summary

This document provides architecture guidance for:
1. Discord command test patterns
2. Async mocking best practices
3. Test stalling investigation
4. V2 compliance test architecture recommendations

---

## 🔍 Current State Analysis

### Discord Command Testing Patterns

**Current Pattern (test_messaging_commands.py):**
```python
@pytest.mark.asyncio
async def test_message_agent_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
    """Test message_agent command with successful send."""
    mock_messaging_controller.send_agent_message = AsyncMock(return_value=True)
    
    await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "NORMAL")
    
    mock_messaging_controller.send_agent_message.assert_called_once_with(...)
    mock_ctx.send.assert_called_once()
```

**Strengths:**
- ✅ Uses `@pytest.mark.asyncio` correctly
- ✅ Uses `AsyncMock` for async methods
- ✅ Centralized mock creation via `discord_test_utils` (SSOT)
- ✅ Clear fixture-based setup

**Areas for Improvement:**
- ⚠️ Need timeout handling for async operations
- ⚠️ Need cleanup patterns for event loops
- ⚠️ Missing assertion patterns for async callbacks

---

## 🎯 Best Practices: Async Mocking

### 1. AsyncMock Usage Patterns

**✅ GOOD: Explicit AsyncMock for async methods**
```python
mock_messaging_controller.send_agent_message = AsyncMock(return_value=True)
await messaging_commands.message_agent(...)
mock_messaging_controller.send_agent_message.assert_called_once()
```

**❌ BAD: Using MagicMock for async methods**
```python
mock_messaging_controller.send_agent_message = MagicMock(return_value=True)  # Won't work!
```

### 2. Async Context Managers

**✅ GOOD: Async context manager mocking**
```python
from unittest.mock import AsyncMock

async with AsyncMock() as mock_context:
    mock_context.__aenter__ = AsyncMock(return_value=mock_context)
    mock_context.__aexit__ = AsyncMock(return_value=False)
    # Test async context manager usage
```

### 3. Async Iterators

**✅ GOOD: Async iterator mocking**
```python
async def async_gen():
    yield "item1"
    yield "item2"

mock_iterator = AsyncMock()
mock_iterator.__aiter__ = AsyncMock(return_value=async_gen())
```

### 4. Event Loop Management

**✅ GOOD: Using pytest-asyncio (already in use)**
```python
@pytest.mark.asyncio
async def test_async_operation():
    # pytest-asyncio handles event loop creation/cleanup
    result = await some_async_function()
    assert result is not None
```

**⚠️ WARNING: Manual event loop management**
```python
# Avoid this pattern - pytest-asyncio handles it
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# ... test code ...
loop.close()  # Can cause issues if not cleaned up properly
```

---

## 🛠️ Test Stalling Investigation

### Problem: Tests Stall When Terminal Canceled

**Root Causes:**
1. **Unclosed event loops** - Async operations not properly awaited/cleaned up
2. **Background tasks** - Tasks created but not canceled on test cleanup
3. **Resource leaks** - Connections/sockets not closed
4. **Timeout issues** - Async operations waiting indefinitely

### Solutions:

#### 1. Add Timeout Decorators

```python
import asyncio
import pytest

@pytest.mark.asyncio
@pytest.mark.timeout(5)  # Fail test if it takes >5 seconds
async def test_with_timeout():
    result = await some_async_function()
    assert result is not None
```

#### 2. Cleanup Patterns

```python
@pytest.fixture
async def cleanup_resources():
    """Fixture to ensure cleanup after async tests."""
    yield
    # Cleanup code runs after test
    await cleanup_async_resources()
```

#### 3. Task Cancellation

```python
@pytest.mark.asyncio
async def test_with_background_tasks():
    task = asyncio.create_task(background_operation())
    try:
        result = await test_operation()
        assert result is not None
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
```

#### 4. Async Context Manager for Resources

```python
@pytest.mark.asyncio
async def test_with_managed_resources():
    async with managed_connection() as conn:
        result = await conn.execute(...)
        assert result is not None
    # Connection automatically closed
```

---

## 📐 Architecture Recommendations

### 1. Test Structure Pattern

**Recommended Structure:**
```
tests/
├── unit/
│   ├── discord/
│   │   ├── test_messaging_commands.py
│   │   ├── test_discord_service.py
│   │   └── conftest.py  # Shared fixtures
│   └── services/
│       ├── test_contract_manager.py
│       └── conftest.py
├── integration/
│   └── test_discord_integration.py
└── utils/
    └── discord_test_utils.py  # SSOT for Discord mocks
```

### 2. Fixture Organization

**Create `tests/discord/conftest.py`:**
```python
"""Shared fixtures for Discord tests."""
import pytest
from tests.utils.discord_test_utils import (
    create_mock_discord_bot,
    create_mock_discord_context,
    create_mock_messaging_controller,
)

@pytest.fixture
def mock_bot():
    """Shared mock Discord bot."""
    return create_mock_discord_bot()

@pytest.fixture
def mock_ctx():
    """Shared mock Discord context."""
    return create_mock_discord_context()

@pytest.fixture
def mock_messaging_controller():
    """Shared mock messaging controller."""
    return create_mock_messaging_controller()
```

### 3. Async Test Utilities

**Create `tests/utils/async_test_utils.py`:**
```python
"""Utilities for async testing."""
import asyncio
import pytest
from typing import AsyncGenerator

@pytest.fixture
async def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    # Cleanup: cancel all pending tasks
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    # Wait for all tasks to be canceled
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)
    loop.close()

async def run_with_timeout(coro, timeout=5.0):
    """Run async function with timeout."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        pytest.fail(f"Test timed out after {timeout} seconds")
```

---

## 🔧 Contract Manager Test Patterns

### Current Issues (Based on Test File)

**Pattern to Fix:**
```python
def test_contract_manager_method(self):
    manager = ContractManager()
    # Synchronous test, but manager might have async dependencies
```

**Recommended Pattern:**
```python
@pytest.mark.asyncio
async def test_contract_manager_async(self):
    """Test async contract manager operations."""
    manager = ContractManager()
    # If manager has async methods, use AsyncMock
    manager.async_method = AsyncMock(return_value=result)
    result = await manager.async_method(...)
    assert result is not None
```

---

## 📊 Test Coverage Goals

### V2 Compliance Test Requirements

1. **Function Coverage**: ≥85% for all public methods
2. **Branch Coverage**: ≥80% for decision points
3. **Async Coverage**: All async methods must have async tests
4. **Error Path Coverage**: All exception handlers tested

### Test Method Count Targets

- **Discord Commands**: 15+ test methods (✅ Achieved)
- **Contract Manager**: 15+ test methods (Needs verification)
- **Messaging Infrastructure**: 20+ test methods (Agent-1 working on this)

---

## 🚀 Implementation Checklist

### Phase 1: Async Mocking Standardization
- [ ] Create `tests/utils/async_test_utils.py`
- [ ] Update all Discord command tests to use timeout decorators
- [ ] Add cleanup fixtures for async resources
- [ ] Document async mocking patterns in codebase

### Phase 2: Test Stalling Fixes
- [ ] Add `@pytest.mark.timeout` to all async tests
- [ ] Implement task cancellation in fixtures
- [ ] Add resource cleanup in `conftest.py`
- [ ] Test with terminal cancellation scenarios

### Phase 3: Contract Manager Tests
- [ ] Review contract manager test failures
- [ ] Apply async mocking patterns
- [ ] Add missing test coverage
- [ ] Verify all async methods have tests

### Phase 4: Integration Test Patterns
- [ ] Create Discord integration test suite
- [ ] Add async integration test patterns
- [ ] Document integration test best practices

---

## 📝 Key Takeaways

1. **Always use `AsyncMock` for async methods** - Never use `MagicMock`
2. **Use `@pytest.mark.asyncio`** - Let pytest-asyncio manage event loops
3. **Add timeouts** - Use `@pytest.mark.timeout` to prevent infinite waits
4. **Clean up resources** - Cancel tasks, close connections in fixtures
5. **Centralize mock creation** - Use SSOT pattern (discord_test_utils)
6. **Test async patterns** - Context managers, iterators, generators

---

## 🔗 Related Documentation

- `tests/utils/discord_test_utils.py` - SSOT for Discord mocks
- `tests/discord/test_messaging_commands.py` - Reference implementation
- `pytest-asyncio` documentation - Event loop management

---

**Agent-2**: Architecture review complete, ready for Agent-1 implementation
