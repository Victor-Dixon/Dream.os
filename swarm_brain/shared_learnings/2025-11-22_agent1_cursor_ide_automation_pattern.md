# Cursor IDE Automation Pattern

**Author**: Agent-1  
**Date**: 2025-11-22  
**Category**: Automation, IDE Integration  
**Tags**: automation, cursor, pyautogui, ide

---

## Problem

When message queue is empty in Cursor IDE, agents need to manually click to accept AI suggestions. This is slow and interrupts workflow.

---

## Solution Pattern

### Automation Flow
1. **Load Coordinates**: From `cursor_agent_coords.json` or `config/cursor_agent_coords.json`
2. **Navigate**: Move mouse to chat input coordinates
3. **Click**: Focus chat input
4. **Accept**: Press Ctrl+Enter to accept all changes

### Implementation
```python
# Pattern: Load → Navigate → Click → Accept
coordinates = load_coordinates()
pyautogui.moveTo(x, y, duration=0.2)
pyautogui.click(x, y)
pyautogui.hotkey('ctrl', 'enter')
```

### Tool: `tools/accept_agent_changes_cursor.py`
- **Features**:
  - Single agent or all agents support
  - Configurable delays
  - Agent listing command
  - Coordinate fallback (root → config)
- **Usage**: `python tools/accept_agent_changes_cursor.py --agent Agent-8`

---

## Integration

### Discord Bot Command
- **Command**: `!accept 1 2 3...` or `!accept all`
- **Implementation**: `src/discord_commander/automation_commands.py`
- **Flow**: Parse args → Map to Agent IDs → Execute tool → Report results

---

## Use Cases

1. **Rapid Change Acceptance**: When message queue is empty
2. **Remote Automation**: Trigger via Discord command
3. **Batch Operations**: Accept changes for multiple agents

---

## Files Created

- `tools/accept_agent_changes_cursor.py` - Main automation tool
- `src/discord_commander/automation_commands.py` - Discord integration

---

## Impact

- Eliminates manual clicking
- Enables remote automation
- Speeds up change acceptance workflow



