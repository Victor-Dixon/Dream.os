# Discord Mock Strategy Fix - StopIteration Error Resolution
**Date**: 2025-12-14  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Context**: Fix Discord command test StopIteration errors and Cog mock issues

---

## 📋 Executive Summary

**Issue**: Discord command tests failing with `StopIteration` errors due to `commands.Cog` mock not properly supporting inheritance.

**Root Cause**: The `MockCog` class in `discord_test_utils.py` doesn't properly handle inheritance and attribute access, causing issues when `MessagingCommands(commands.Cog)` tries to initialize.

**Solution**: Create a proper mock Cog class that supports inheritance, attribute storage, and proper initialization.

---

## 🔍 Problem Analysis

### Current Issue

1. **MockCog Class Too Simple**:
   ```python
   class MockCog:
       """Mock Cog class for testing."""
       def __init__(self, *args, **kwargs):
           pass  # ❌ Doesn't store attributes
   ```

2. **Inheritance Problem**:
   - `MessagingCommands(commands.Cog)` expects `super().__init__()` to work
   - MockCog doesn't properly support attribute access
   - Causes `StopIteration` when Python tries to resolve attributes

3. **Real Discord Module Conflict**:
   - `MessagingCommands` imports real discord module
   - Mocks are set up in `sys.modules` but conflict with real imports
   - Need to ensure mocks are set up before any discord imports

---

## 🔧 Solution: Enhanced MockCog Class

### Fix 1: Proper MockCog Implementation

**Update `tests/utils/discord_test_utils.py`:**

```python
def setup_discord_mocks():
    """
    Setup Discord module mocks before importing Discord-related code.
    
    This must be called BEFORE importing any Discord modules in test files.
    """
    # Create a proper Cog class that can be inherited from
    class MockCog:
        """Mock Cog class for testing that properly supports inheritance."""
        def __init__(self, *args, **kwargs):
            """Initialize mock Cog - store args/kwargs if needed."""
            # Store any attributes that might be set
            self._args = args
            self._kwargs = kwargs
            # Allow attributes to be set dynamically
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def __getattr__(self, name):
            """Allow dynamic attribute access."""
            # Return None for undefined attributes (common in mocks)
            return None
    
    mock_discord = MagicMock()
    mock_discord.Client = MagicMock()
    mock_discord.Embed = MagicMock()
    
    # Make Embed work as a class that can be instantiated
    def create_embed(*args, **kwargs):
        embed = MagicMock()
        embed.title = kwargs.get('title', '')
        embed.description = kwargs.get('description', '')
        embed.color = kwargs.get('color', MagicMock())
        embed.add_field = MagicMock()
        embed.timestamp = kwargs.get('timestamp')
        return embed
    mock_discord.Embed = create_embed
    
    mock_discord.Color = MagicMock()
    mock_discord.Color.green = lambda: MagicMock()
    mock_discord.Color.red = lambda: MagicMock()
    mock_discord.Color.blue = lambda: MagicMock()
    mock_discord.ui = MagicMock()
    mock_discord.ui.View = MagicMock()
    mock_discord.ui.Modal = MagicMock()
    mock_discord.ui.Button = MagicMock()
    mock_discord.ui.Select = MagicMock()
    mock_discord.Activity = MagicMock()
    mock_discord.ActivityType = MagicMock()
    mock_discord.utils = MagicMock()
    mock_discord.utils.utcnow = MagicMock()
    mock_discord.Intents = MagicMock()
    mock_discord.Intents.default = MagicMock(return_value=MagicMock())
    
    # Set up sys.modules BEFORE any discord imports
    sys.modules['discord'] = mock_discord
    
    mock_ext = MagicMock()
    sys.modules['discord.ext'] = mock_ext
    
    mock_commands = MagicMock()
    mock_commands.Bot = MagicMock()
    mock_commands.Cog = MockCog  # Use proper MockCog class
    mock_commands.Context = MagicMock()
    
    # Make commands.command a no-op decorator (for tests)
    def noop_command(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    mock_commands.command = noop_command
    
    sys.modules['discord.ext.commands'] = mock_commands
```

### Fix 2: Ensure Mocks Are Set Up First

**In `tests/discord/test_messaging_commands.py`:**

The current setup is correct - `setup_discord_mocks()` is called before imports. However, we should ensure it's more robust:

```python
# Set pytest environment variable BEFORE imports
os.environ["PYTEST_CURRENT_TEST"] = "test"

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# IMPORTANT: Setup Discord mocks BEFORE any discord imports
_discord_utils_path = _project_root / "tests" / "utils" / "discord_test_utils.py"
spec = importlib.util.spec_from_file_location("discord_test_utils", _discord_utils_path)
discord_test_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discord_test_utils)
setup_discord_mocks = discord_test_utils.setup_discord_mocks

# Setup mocks IMMEDIATELY
setup_discord_mocks()  # ✅ Called before any discord imports

# NOW import Discord-related modules
from src.discord_commander.messaging_commands import MessagingCommands
```

---

## 🎯 Alternative Solution: Patch Strategy

If the above doesn't work, use `unittest.mock.patch` to patch before import:

### Option A: Module-Level Patching

```python
"""Tests for discord_commander/messaging_commands.py."""
import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Set pytest environment variable
os.environ["PYTEST_CURRENT_TEST"] = "test"

_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Patch discord module BEFORE import
with patch.dict('sys.modules', {
    'discord': MagicMock(),
    'discord.ext': MagicMock(),
    'discord.ext.commands': MagicMock(),
}):
    from src.discord_commander.messaging_commands import MessagingCommands
```

### Option B: Pytest Fixture Patching

```python
@pytest.fixture(autouse=True, scope="module")
def setup_discord_mocks_module():
    """Set up Discord mocks at module level."""
    from tests.utils.discord_test_utils import setup_discord_mocks
    setup_discord_mocks()
    yield
    # Cleanup if needed
```

---

## 🔍 StopIteration Error Specific Fix

The `StopIteration` error typically occurs when:

1. **Iterator Protocol Issues**: A mock is used in a `for` loop or `in` check
2. **Attribute Resolution**: Python tries to resolve attributes and hits an iterator

**Fix for StopIteration**:

```python
class MockCog:
    """Mock Cog class that prevents StopIteration errors."""
    def __init__(self, *args, **kwargs):
        """Initialize - store attributes properly."""
        # Don't iterate over kwargs in a way that causes StopIteration
        for key, value in kwargs.items():
            if not key.startswith('_'):
                setattr(self, key, value)
    
    def __getattr__(self, name):
        """Prevent StopIteration on attribute access."""
        # Return a MagicMock for undefined attributes
        mock_attr = MagicMock()
        setattr(self, name, mock_attr)
        return mock_attr
    
    def __iter__(self):
        """Prevent StopIteration in iteration contexts."""
        # Return empty iterator
        return iter([])
    
    def __contains__(self, item):
        """Prevent StopIteration in 'in' checks."""
        return False
```

---

## ✅ Recommended Implementation Strategy

### Step 1: Update MockCog Class

Update `tests/utils/discord_test_utils.py` with the enhanced `MockCog` class that:
- ✅ Properly supports inheritance
- ✅ Stores initialization arguments
- ✅ Prevents StopIteration errors
- ✅ Allows dynamic attribute access

### Step 2: Verify Mock Setup Order

Ensure `setup_discord_mocks()` is called:
- ✅ Before any discord imports
- ✅ At module level (not in fixtures)
- ✅ Only once per test module

### Step 3: Test the Fix

Run the test suite:
```bash
pytest tests/discord/test_messaging_commands.py -v
```

### Step 4: If Still Failing, Use Patch Strategy

If direct mocking still fails:
- Use `unittest.mock.patch` to patch `sys.modules` before imports
- Or use pytest fixtures with `autouse=True`

---

## 📊 Test Patterns After Fix

### Expected Test Pattern

```python
def test_init(self, mock_bot, mock_messaging_controller):
    """Test MessagingCommands initialization."""
    commands = MessagingCommands(mock_bot, mock_messaging_controller)
    assert commands.bot == mock_bot  # ✅ Should pass
    assert commands.messaging_controller == mock_messaging_controller
    assert commands.logger is not None
```

### Async Test Pattern

```python
@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_message_agent_success(self, messaging_commands, mock_ctx, mock_messaging_controller):
    """Test message_agent command with successful send."""
    mock_messaging_controller.send_agent_message = AsyncMock(return_value=True)
    
    await messaging_commands.message_agent(mock_ctx, "Agent-1", "Test message", "NORMAL")
    
    mock_messaging_controller.send_agent_message.assert_called_once()
    mock_ctx.send.assert_called_once()
```

---

## 🎯 Architecture Compliance

### Clean Architecture Principles

1. **SSOT for Mocks**: All Discord mocks in `discord_test_utils.py`
2. **Separation of Concerns**: Mock setup separate from test logic
3. **Dependency Injection**: Tests inject mocks via fixtures
4. **Testability**: Mocks support full test scenarios

### SOLID Principles

- **Single Responsibility**: MockCog only handles Cog mocking
- **Open/Closed**: Extensible via inheritance
- **Liskov Substitution**: MockCog can replace real Cog
- **Interface Segregation**: Only mocks what's needed
- **Dependency Inversion**: Tests depend on mocks, not real Discord

---

## 📝 Implementation Checklist

- [ ] Update `MockCog` class in `discord_test_utils.py`
- [ ] Add `__getattr__` to prevent StopIteration
- [ ] Add `__iter__` to prevent iteration errors
- [ ] Verify `setup_discord_mocks()` is called before imports
- [ ] Test all 17 Discord command tests
- [ ] Verify no StopIteration errors
- [ ] Document any remaining issues

---

**Agent-2**: Discord mock fix guidance provided. Enhanced MockCog class should resolve StopIteration errors. Ready for Agent-1 implementation.
