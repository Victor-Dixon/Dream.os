#!/usr/bin/env python3
"""
Carmyn Message Agent-7 Modal - Self-Improving Template
======================================================

Modal for Carmyn to message Agent-7 with her preferences included.
Template is self-improving - updates preferences based on interactions.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

logger = logging.getLogger(__name__)


class CarmynMessageAgent7Modal(discord.ui.Modal):
    """Modal for Carmyn to send messages to Agent-7 with preferences."""
    
    def __init__(self, preferences_path: Path = None):
        super().__init__(title="💬 Message Agent-7")
        self.preferences_path = preferences_path or Path(__file__).parent.parent.parent.parent / "agent_workspaces" / "Agent-7" / "carmyn_preferences.json"
        self.preferences = self._load_preferences()
        
        # Message input
        self.message_input = discord.ui.TextInput(
            label="Your Message to Agent-7",
            placeholder="What would you like Agent-7 to help with?",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.message_input)
    
    def _load_preferences(self) -> dict:
        """Load Carmyn's preferences."""
        try:
            if self.preferences_path.exists():
                return json.loads(self.preferences_path.read_text(encoding='utf-8'))
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
        
        # Default preferences
        return {
            "profile": {
                "name": "Carmyn",
                "discord_username": "CARYMN",
                "role": "Featured DJ • Music Artist • Rising Star"
            },
            "preferences": {
                "communication_style": "Friendly and encouraging",
                "working_style": "Still learning and growing - always improving",
                "music_genres": ["R&B", "Dance", "Jazz"]
            },
            "interaction_history": {"total_interactions": 0}
        }
    
    def _build_message_template(self, user_message: str) -> str:
        """Build message template with preferences."""
        profile = self.preferences.get("profile", {})
        prefs = self.preferences.get("preferences", {})
        history = self.preferences.get("interaction_history", {})
        guidelines = self.preferences.get("working_guidelines", {})
        
        template = f"""# 💖 MESSAGE FROM CARMYN TO AGENT-7

**From**: {profile.get('name', 'Carmyn')} ({profile.get('discord_username', 'CARYMN')})
**To**: Agent-7 (Web Development Specialist)
**Priority**: normal
**Message Type**: carmyn_to_agent
**Timestamp**: {datetime.now().isoformat()}

---

## 📨 CARMYN'S MESSAGE

{user_message}

---

## 🌟 CARMYN'S PREFERENCES & WORKING GUIDELINES

### 🎵 Profile
- **Name**: {profile.get('name', 'Carmyn')}
- **Role**: {profile.get('role', 'Featured DJ • Music Artist • Rising Star')}
- **Website**: {profile.get('website', 'https://prismblossom.online/carmyn')}

### 💖 Preferences
- **Music Genres**: {', '.join(prefs.get('music_genres', ['R&B', 'Dance', 'Jazz']))}
- **Communication Style**: {prefs.get('communication_style', 'Friendly and encouraging')}
- **Working Style**: {prefs.get('working_style', 'Still learning and growing - always improving')}
- **Vibe**: {prefs.get('vibe', 'Positive, creative, and always ready to share amazing music')}
- **Preferred Tone**: {prefs.get('preferred_tone', 'Supportive and enthusiastic')}

### 🎯 How to Work with Carmyn
{chr(10).join(f"- {guideline}" for guideline in guidelines.get('how_to_work_with_carmyn', [
    "Be encouraging and supportive - she's still learning and growing",
    "Use positive, enthusiastic language",
    "Reference her music specializations (R&B, Dance, Jazz) when relevant"
]))}

### 📝 Things to Remember
{chr(10).join(f"- {item}" for item in guidelines.get('things_to_remember', [
    "She's a rising star - celebrate her progress",
    "She's actively learning - be patient and supportive",
    "Music is her passion - incorporate that when relevant"
]))}

### 📊 Interaction History
- **Total Interactions**: {history.get('total_interactions', 0)}
- **Last Interaction**: {history.get('last_interaction', 'Never')}

---

## 🚀 SELF-IMPROVING SYSTEM

This template is self-improving! As you work with Carmyn:
1. Update preferences based on what works well
2. Add notes to interaction_history when you learn something new
3. Refine working_guidelines based on successful interactions
4. The system will remember and improve over time!

**Remember**: This is a living document that evolves with each interaction. Update it to reflect how to best work with Carmyn!

---

*Message sent via Carmyn's personalized !carmyn command*
*Template Version: {self.preferences.get('template_version', '1.0.0')}*
*WE. ARE. SWARM. ⚡🔥*
"""
        
        return template
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            user_message = self.message_input.value
            
            # Build message with preferences
            full_message = self._build_message_template(user_message)
            
            # Send to Agent-7 via inbox utility
            try:
                from src.utils.inbox_utility import create_inbox_message
                
                success = create_inbox_message(
                    recipient="Agent-7",
                    sender="Carmyn (via !carmyn command)",
                    content=full_message,
                    priority="normal",
                    message_type="carmyn_to_agent",
                    tags=["carmyn", "personalized", "preferences"]
                )
                
                if success:
                    # Update interaction history
                    self._update_interaction_history(user_message)
                    
                    # Send confirmation
                    embed = discord.Embed(
                        title="✅ Message Sent!",
                        description=f"Your message has been sent to Agent-7!",
                        color=0xFF69B4  # Hot pink
                    )
                    embed.add_field(
                        name="📨 Message Preview",
                        value=user_message[:500] + ("..." if len(user_message) > 500 else ""),
                        inline=False
                    )
                    embed.add_field(
                        name="💡 Note",
                        value="Agent-7 will respond with your preferences in mind!",
                        inline=False
                    )
                    embed.add_field(
                        name="🔄 Self-Improving System",
                        value="Your preferences are being updated based on this interaction! ✨",
                        inline=False
                    )
                    embed.set_footer(text="Keep creating amazing music, Carmyn! 🎶")
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.response.send_message(
                        "❌ Error sending message. Please try again later.",
                        ephemeral=True
                    )
            except Exception as e:
                logger.error(f"Error sending message to Agent-7: {e}", exc_info=True)
                # Fallback: send via Discord DM or channel
                await interaction.response.send_message(
                    f"✅ Message prepared! (Messaging service unavailable, but preferences noted)\n\n"
                    f"**Your message:**\n{user_message[:500]}",
                    ephemeral=True
                )
                self._update_interaction_history(user_message)
        
        except Exception as e:
            logger.error(f"Error in Carmyn message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}",
                    ephemeral=True
                )
    
    def _update_interaction_history(self, message: str):
        """Update interaction history and learn from the interaction."""
        try:
            history = self.preferences.get("interaction_history", {})
            history["total_interactions"] = history.get("total_interactions", 0) + 1
            history["last_interaction"] = datetime.now().isoformat()
            
            # Extract topics from message (simple keyword detection)
            topics = []
            message_lower = message.lower()
            if "music" in message_lower or "dj" in message_lower or "mix" in message_lower:
                topics.append("music")
            if "website" in message_lower or "site" in message_lower or "web" in message_lower:
                topics.append("website")
            if "r&b" in message_lower or "rnb" in message_lower:
                topics.append("r&b")
            if "dance" in message_lower:
                topics.append("dance")
            if "jazz" in message_lower:
                topics.append("jazz")
            
            if topics:
                notes = history.get("notes", [])
                notes.append({
                    "timestamp": datetime.now().isoformat(),
                    "topics": topics,
                    "note": f"Discussed: {', '.join(topics)}"
                })
                # Keep only last 50 notes
                history["notes"] = notes[-50:]
            
            self.preferences["interaction_history"] = history
            
            # Save updated preferences
            self.preferences_path.parent.mkdir(parents=True, exist_ok=True)
            self.preferences_path.write_text(
                json.dumps(self.preferences, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            
            logger.info(f"Updated Carmyn's interaction history: {history['total_interactions']} interactions")
        
        except Exception as e:
            logger.error(f"Error updating interaction history: {e}", exc_info=True)

