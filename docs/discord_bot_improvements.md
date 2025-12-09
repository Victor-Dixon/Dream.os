# Discord Bot Improvements - Agent Input Handling

## Issue: Agent Input Length Limits

### Problem
JetFuelMessageModal uses manual text input for agent selection with character limits that cause Discord API errors (50035) when users type long agent ID strings.

### Current Fix (Temporary)
- Increased `max_length` from 20 → 50 → 200 characters
- Allows multiple agent IDs: "Agent-1, Agent-2, Agent-3, Agent-4"

### Long-term Solution Needed
Replace manual text input with Select dropdown in JetFuelMessageModal:

```python
# Current (problematic)
include_agent_selection=True  # Creates text input with length limits

# Better solution
# Use Select dropdown like MessagingControllerView
self.agent_select = discord.ui.Select(
    placeholder="🎯 Select agent for Jet Fuel...",
    options=self._create_agent_options(),
    custom_id="jetfuel_agent_select",
)
```

### Benefits
- ✅ No length limit issues
- ✅ Consistent UX with regular messaging
- ✅ Prevents invalid agent ID inputs
- ✅ Better user experience

### Implementation
1. Remove `include_agent_selection=True` from JetFuelMessageModal
2. Add Select component with agent options
3. Update callback to use `self.agent_select.values[0]`
4. Maintain Jet Fuel branding and messaging

## Created: 2025-12-08
## Status: Recommended for future sprint

