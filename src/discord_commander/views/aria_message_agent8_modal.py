#!/usr/bin/env python3
"""
Aria Message Agent-8 Modal - Self-Improving Template
====================================================

Modal for Aria to message Agent-8 with her preferences included.
Template is self-improving - updates preferences based on interactions.

<!-- SSOT Domain: web -->

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import json
import logging
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


class AriaMessageAgent8Modal(discord.ui.Modal):
    """Modal for Aria to send messages to Agent-8 with preferences."""
    
    def __init__(self, preferences_path: Path = None):
        super().__init__(title="💬 Message Agent-8")
        self.preferences_path = preferences_path or Path(__file__).parent.parent.parent.parent / "agent_workspaces" / "Agent-8" / "aria_preferences.json"
        self.preferences = self._load_preferences()
        
        # Message input
        self.message_input = discord.ui.TextInput(
            label="Your Message to Agent-8",
            placeholder="What would you like Agent-8 to help with?",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.message_input)
    
    def _load_preferences(self) -> dict:
        """Load Aria's preferences."""
        try:
            if self.preferences_path.exists():
                return json.loads(self.preferences_path.read_text(encoding='utf-8'))
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
        
        # Default preferences
        return {
            "preferences": {
                "communication_style": "friendly and encouraging",
                "response_tone": "supportive and helpful",
                "work_approach": "creative and collaborative"
            },
            "interaction_history": {"total_interactions": 0}
        }
    
    def _build_message_template(self, user_message: str) -> str:
        """Build message template with preferences."""
        prefs = self.preferences.get("preferences", {})
        history = self.preferences.get("interaction_history", {})
        
        template = f"""**From**: Aria
**To**: Agent-8 (Testing & Quality Assurance Specialist)
**Priority**: NORMAL

**Aria's Message:**
{user_message}

**Aria's Preferences (for context):**
- **Communication Style**: {prefs.get('communication_style', 'friendly and encouraging')}
- **Response Tone**: {prefs.get('response_tone', 'supportive and helpful')}
- **Work Approach**: {prefs.get('work_approach', 'creative and collaborative')}
- **Project Focus**: {', '.join(prefs.get('project_focus', ['gaming', 'web development']))}
- **Interests**: {', '.join(prefs.get('interests', ['gaming', 'coding', 'design']))}

**Interaction History**: {history.get('total_interactions', 0)} previous interactions

**Note**: This template is self-improving - preferences update based on our interactions!

---
*Message sent via Aria's personalized !aria command*"""
        
        return template
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            user_message = self.message_input.value
            
            # Build message with preferences
            full_message = self._build_message_template(user_message)
            
            # Write directly to Agent-8's inbox (file-based messaging)
            success = self._write_to_inbox(full_message, user_message)
            
            if success:
                # Update interaction history
                self._update_interaction_history(user_message)
                
                # Send confirmation
                embed = discord.Embed(
                    title="✅ Message Sent!",
                    description=f"Your message has been sent to Agent-8's inbox!",
                    color=0x00FF00  # Green
                )
                embed.add_field(
                    name="📨 Message Preview",
                    value=user_message[:500] + ("..." if len(user_message) > 500 else ""),
                    inline=False
                )
                embed.add_field(
                    name="💡 Note",
                    value="Agent-8 will see your message with your preferences included!",
                    inline=False
                )
                embed.set_footer(text="Preferences are being updated based on this interaction! ✨")
                
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    f"❌ Error writing message to inbox. Check logs for details.",
                    ephemeral=True
                )
        
        except Exception as e:
            logger.error(f"Error in Aria message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}",
                    ephemeral=True
                )
    
    def _write_to_inbox(self, full_message: str, user_message: str) -> bool:
        """Write message directly to Agent-8's inbox folder."""
        try:
            # Use inbox utility for reliable delivery
            from src.utils.inbox_utility import create_inbox_message
            
            success = create_inbox_message(
                recipient="Agent-8",
                sender="Aria",
                content=full_message,
                priority="normal",
                message_type="text",
                tags=["aria", "preferences", "self-improving"]
            )
            
            if success:
                logger.info("✅ Message written to Agent-8 inbox via inbox utility")
            else:
                logger.warning("⚠️ Inbox utility failed, trying direct write...")
                # Fallback to direct write
                return self._write_to_inbox_direct(full_message)
            
            return success
        
        except ImportError:
            # Fallback if inbox utility not available
            logger.warning("⚠️ Inbox utility not available, using direct write...")
            return self._write_to_inbox_direct(full_message)
        except Exception as e:
            logger.error(f"Error writing to inbox: {e}", exc_info=True)
            # Try direct write as fallback
            return self._write_to_inbox_direct(full_message)
    
    def _write_to_inbox_direct(self, full_message: str) -> bool:
        """Direct file write fallback."""
        try:
            from datetime import datetime
            import uuid
            
            project_root = Path(__file__).parent.parent.parent.parent
            inbox_dir = project_root / "agent_workspaces" / "Agent-8" / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate message filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            message_id = str(uuid.uuid4())[:8]
            filename = f"ARIA_MESSAGE_{timestamp}_{message_id}.md"
            inbox_file = inbox_dir / filename
            
            # Format message with headers
            formatted_message = f"""# 💬 ARIA MESSAGE - TEXT

**From**: Aria
**To**: Agent-8
**Priority**: normal
**Message ID**: {message_id}
**Timestamp**: {datetime.now().isoformat()}

---

{full_message}

---
*Message delivered via Aria's personalized !aria command*"""
            
            # Write to inbox
            inbox_file.write_text(formatted_message, encoding='utf-8')
            logger.info(f"✅ Message written to Agent-8 inbox (direct): {inbox_file}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error in Aria message modal: {e}", exc_info=True)
            if not interaction.response.is_done():
                interaction.response.send_message(
                    f"❌ Error: {e}",
                    ephemeral=True
                )
    
    def _update_interaction_history(self, message: str):
        """Update interaction history and learn from the interaction."""
        try:
            history = self.preferences.get("interaction_history", {})
            history["total_interactions"] = history.get("total_interactions", 0) + 1
            history["last_interaction"] = str(Path(__file__).parent.parent.parent.parent / "agent_workspaces" / "Agent-8" / "aria_preferences.json")
            
            # Extract topics from message (simple keyword detection)
            topics = []
            message_lower = message.lower()
            if "game" in message_lower or "gaming" in message_lower:
                topics.append("gaming")
            if "wordpress" in message_lower or "theme" in message_lower:
                topics.append("wordpress")
            if "code" in message_lower or "coding" in message_lower:
                topics.append("coding")
            if "design" in message_lower:
                topics.append("design")
            
            if topics:
                existing_topics = history.get("topics_discussed", [])
                for topic in topics:
                    if topic not in existing_topics:
                        existing_topics.append(topic)
                history["topics_discussed"] = existing_topics
            
            self.preferences["interaction_history"] = history
            
            # Save updated preferences
            self.preferences_path.parent.mkdir(parents=True, exist_ok=True)
            self.preferences_path.write_text(
                json.dumps(self.preferences, indent=2),
                encoding='utf-8'
            )
            
            logger.info(f"Updated Aria's interaction history: {history['total_interactions']} interactions")
        
        except Exception as e:
            logger.error(f"Error updating interaction history: {e}", exc_info=True)

