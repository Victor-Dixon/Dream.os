"""
<!-- SSOT Domain: discord -->

Carmyn Preferences Manager - Self-Improving Template System
===========================================================

Manages Carmyn's preferences and working guidelines.
Self-improving system that updates preferences based on interactions.

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-03
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Path to Carmyn's preferences file
PREFERENCES_FILE = Path("agent_workspaces/Agent-7/carmyn_preferences.json")


def load_preferences() -> Dict[str, Any]:
    """Load Carmyn's preferences from JSON file."""
    try:
        if PREFERENCES_FILE.exists():
            with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Preferences file not found: {PREFERENCES_FILE}")
            return {}
    except Exception as e:
        logger.error(f"Error loading preferences: {e}")
        return {}


def save_preferences(prefs: Dict[str, Any]) -> bool:
    """Save Carmyn's preferences to JSON file."""
    try:
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        prefs["last_updated"] = datetime.now().isoformat()
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Preferences saved to {PREFERENCES_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving preferences: {e}")
        return False


def update_interaction_history(interaction_note: str) -> bool:
    """
    Update interaction history and increment counter.
    This makes the system self-improving by tracking interactions.
    """
    try:
        prefs = load_preferences()
        if not prefs:
            return False
        
        # Update interaction history
        history = prefs.get("interaction_history", {})
        history["total_interactions"] = history.get("total_interactions", 0) + 1
        history["last_interaction"] = datetime.now().isoformat()
        
        # Add note if provided
        if interaction_note:
            notes = history.get("notes", [])
            notes.append({
                "timestamp": datetime.now().isoformat(),
                "note": interaction_note
            })
            # Keep only last 50 notes
            history["notes"] = notes[-50:]
        
        prefs["interaction_history"] = history
        return save_preferences(prefs)
    except Exception as e:
        logger.error(f"Error updating interaction history: {e}")
        return False


def update_preference(key_path: str, value: Any) -> bool:
    """
    Update a specific preference by key path (e.g., "preferences.communication_style").
    This enables self-improvement by updating preferences based on interactions.
    """
    try:
        prefs = load_preferences()
        if not prefs:
            return False
        
        # Navigate to the key path
        keys = key_path.split(".")
        current = prefs
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Update the value
        current[keys[-1]] = value
        prefs["preferences_updated_at"] = datetime.now().isoformat()
        
        return save_preferences(prefs)
    except Exception as e:
        logger.error(f"Error updating preference {key_path}: {e}")
        return False


def format_preferences_message() -> str:
    """
    Format Carmyn's preferences into a message template for Agent-7.
    This is the self-improving template that gets sent to Agent-7's inbox.
    """
    prefs = load_preferences()
    if not prefs:
        return "⚠️ Preferences file not found. Please initialize Carmyn's preferences."
    
    profile = prefs.get("profile", {})
    preferences = prefs.get("preferences", {})
    guidelines = prefs.get("working_guidelines", {})
    history = prefs.get("interaction_history", {})
    
    message = f"""# 💖 MESSAGE FROM CARMYN TO AGENT-7

**From**: {profile.get('name', 'Carmyn')} ({profile.get('discord_username', 'CARYMN')})
**To**: Agent-7 (Web Development Specialist)
**Priority**: normal
**Message Type**: carmyn_to_agent
**Timestamp**: {datetime.now().isoformat()}

---

## 🌟 CARMYN'S PREFERENCES & WORKING GUIDELINES

### 🎵 Profile
- **Name**: {profile.get('name', 'Carmyn')}
- **Role**: {profile.get('role', 'Featured DJ • Music Artist • Rising Star')}
- **Website**: {profile.get('website', 'https://prismblossom.online/carmyn')}
- **Main Site**: {profile.get('main_site', 'https://prismblossom.online')}

### 💖 Preferences
- **Music Genres**: {', '.join(preferences.get('music_genres', []))}
- **Communication Style**: {preferences.get('communication_style', 'Friendly and encouraging')}
- **Working Style**: {preferences.get('working_style', 'Still learning and growing - always improving')}
- **Vibe**: {preferences.get('vibe', 'Positive, creative, and always ready to share amazing music')}
- **Preferred Tone**: {preferences.get('preferred_tone', 'Supportive and enthusiastic')}

### 🎯 How to Work with Carmyn
{chr(10).join(f"- {guideline}" for guideline in guidelines.get('how_to_work_with_carmyn', []))}

### 📝 Things to Remember
{chr(10).join(f"- {item}" for item in guidelines.get('things_to_remember', []))}

### 📊 Interaction History
- **Total Interactions**: {history.get('total_interactions', 0)}
- **Last Interaction**: {history.get('last_interaction', 'Never')}
- **Template Version**: {prefs.get('template_version', '1.0.0')}

---

## 🚀 SELF-IMPROVING SYSTEM

This template is self-improving! As you work with Carmyn:
1. Update preferences based on what works well
2. Add notes to interaction_history when you learn something new
3. Refine working_guidelines based on successful interactions
4. The system will remember and improve over time!

**Remember**: This is a living document that evolves with each interaction. Update it to reflect how to best work with Carmyn!

---

*Message sent via !carmyn command personalized button*
*Template Version: {prefs.get('template_version', '1.0.0')}*
*WE. ARE. SWARM. ⚡🔥*
"""
    
    return message

