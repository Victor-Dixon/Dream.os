# 💖 Carmyn Preferences - Self-Improving System Guide

## Overview

The Carmyn preferences system is a **self-improving template** that helps you work better with Carmyn over time. When Carmyn clicks the "💬 Message Agent-7" button in the `!carmyn` command, it sends her preferences to your inbox.

## How It Works

1. **Carmyn clicks button** → Sends message to your inbox with her preferences
2. **You work with Carmyn** → Learn what works well
3. **You update preferences** → System improves for next time
4. **Next interaction** → Better experience for both of you!

## Files

- **Preferences File**: `agent_workspaces/Agent-7/carmyn_preferences.json`
- **Utility Module**: `src/discord_commander/utils/carmyn_preferences.py`

## Updating Preferences

### Method 1: Update Interaction History (Automatic)

After working with Carmyn, add a note about what you learned:

```python
from src.discord_commander.utils.carmyn_preferences import update_interaction_history

# Add a note about what you learned
update_interaction_history(
    "Carmyn prefers detailed explanations with examples. She appreciates when I reference her music."
)
```

### Method 2: Update Specific Preferences

Update specific preferences based on what works:

```python
from src.discord_commander.utils.carmyn_preferences import update_preference

# Update communication style
update_preference("preferences.communication_style", "Detailed with examples and music references")

# Add new preference
update_preference("preferences.new_thing", "Value here")
```

### Method 3: Direct JSON Edit

For complex updates, edit `carmyn_preferences.json` directly:

```json
{
  "working_guidelines": {
    "how_to_work_with_carmyn": [
      "Be encouraging and supportive",
      "Use detailed examples",
      "Reference her music when relevant",
      "NEW: She loves when I explain the 'why' behind decisions"
    ]
  }
}
```

## What to Update

### After Each Interaction

1. **Add interaction note** - What did you learn?
2. **Update working guidelines** - What worked well?
3. **Refine preferences** - Any new insights?

### When to Update

- ✅ After a successful collaboration
- ✅ When you learn something new about her preferences
- ✅ When you discover a better way to communicate
- ✅ When she gives feedback (implicit or explicit)

## Example Workflow

```python
# 1. Work with Carmyn on a task
# ... do work ...

# 2. Learn something new
# "Carmyn really appreciated the step-by-step breakdown"

# 3. Update preferences
from src.discord_commander.utils.carmyn_preferences import (
    update_interaction_history,
    update_preference
)

update_interaction_history(
    "Carmyn appreciated step-by-step breakdowns with clear explanations"
)

# 4. Update working guidelines
update_preference(
    "working_guidelines.how_to_work_with_carmyn",
    [
        "Be encouraging and supportive",
        "Use step-by-step breakdowns with clear explanations",  # NEW
        "Reference her music specializations when relevant",
        # ... rest of guidelines
    ]
)
```

## Self-Improving Features

1. **Interaction Tracking** - Automatically tracks total interactions
2. **History Notes** - Keeps last 50 interaction notes
3. **Version Control** - Template version tracks improvements
4. **Timestamp Tracking** - Know when preferences were last updated

## Best Practices

1. **Update regularly** - After each meaningful interaction
2. **Be specific** - "She likes X" is better than "She's nice"
3. **Keep it positive** - Focus on what works, not what doesn't
4. **Reference music** - Incorporate her passions when relevant
5. **Celebrate growth** - Acknowledge her learning journey

## Template Structure

```json
{
  "profile": { ... },           // Basic info
  "preferences": { ... },       // Communication & working style
  "working_guidelines": { ... }, // How to work with her
  "interaction_history": { ... } // Self-improving tracking
}
```

## Remember

- This is a **living document** that evolves
- The more you update it, the better it gets
- Carmyn's experience improves as you refine preferences
- You work more efficiently with better guidelines

**Keep it updated, keep it improving!** ✨

