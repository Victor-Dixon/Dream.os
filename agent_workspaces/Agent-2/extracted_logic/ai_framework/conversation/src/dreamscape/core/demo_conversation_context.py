#!/usr/bin/env python3
"""
Conversation Context Integration Demo
Demonstrates how ChatGPT AI uses actual conversation workflow context 
to create truly unique content based on work history.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

class ConversationContextDemo:
    """Demonstrates conversation context integration for personalized content."""
    
    def __init__(self):
        self.conversation_data = []
        self.work_themes = []
        
    def load_conversation_history(self):
        """Load and analyze conversation history for context."""
        print("🔍 Loading conversation history for context...")
        
        # Load conversation data
        conversation_files = [
            "outputs/conversations_20250628_015943.json",
            "outputs/example_conversations_20250628_020007.json"
        ]
        
        for file_path in conversation_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self.conversation_data.extend(data)
                        else:
                            self.conversation_data.append(data)
                    print(f"✅ Loaded {len(data) if isinstance(data, list) else 1} conversations from {file_path}")
                except Exception as e:
                    print(f"⚠️ Error loading {file_path}: {e}")
        
        # Extract work themes from conversation titles
        self.work_themes = self._extract_work_themes()
        print(f"🎯 Identified {len(self.work_themes)} key work themes")
        
    def _extract_work_themes(self):
        """Extract key themes from conversation titles."""
        themes = []
        for conv in self.conversation_data:
            if 'title' in conv:
                title = conv['title'].lower()
                
                # Categorize by work themes
                if any(word in title for word in ['dream.os', 'dreamos', 'scraper', 'scraping']):
                    themes.append('AI Development & Automation')
                elif any(word in title for word in ['bot', 'backtest', 'trading', 'tsla']):
                    themes.append('Trading & Financial Analysis')
                elif any(word in title for word in ['roadmap', 'prd', 'plan', 'strategy']):
                    themes.append('Project Planning & Strategy')
                elif any(word in title for word in ['persona', 'identity', 'analysis']):
                    themes.append('Personal Development & Analysis')
                elif any(word in title for word in ['beta', 'checklist', 'improvement']):
                    themes.append('Quality Assurance & Optimization')
                else:
                    themes.append('General Problem Solving')
        
        # Get unique themes with counts
        theme_counts = {}
        for theme in themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        return list(theme_counts.keys())
    
    def create_contextual_prompt(self, template_type, **kwargs):
        """Create a prompt that incorporates conversation workflow context."""
        
        # Get recent conversation titles for context
        recent_titles = [conv.get('title', '') for conv in self.conversation_data[:10]]
        
        context_prompt = f"""
You are an AI assistant who has been working closely with me on various projects. 
Based on our recent conversation history, you understand my work patterns and interests.

Recent work themes from our conversations:
{', '.join(self.work_themes)}

Recent conversation topics:
{', '.join(recent_titles[:5])}

Please respond to the following request in a way that reflects our collaborative work history 
and builds upon the patterns and themes we've established together.
"""
        
        return context_prompt
    
    def generate_contextual_template(self, template_type, **kwargs):
        """Generate a contextual template with conversation history integration."""
        
        # Create contextual prompt
        context_prompt = self.create_contextual_prompt(template_type, **kwargs)
        
        # Create template content based on type
        if template_type == "skill_up":
            template_content = f"""
🎮 **DREAMSCAPE SKILL PROGRESSION**

Player: {kwargs.get('player_name', 'Victor')}
Skill: {kwargs.get('skill_name', 'Unknown')}
New Level: {kwargs.get('new_level', 1)}
Milestone: {kwargs.get('milestone', 'Basic Achievement')}

🎯 **SKILL UP ACHIEVED!**

{kwargs.get('player_name', 'Victor')} has successfully leveled up their {kwargs.get('skill_name', 'Unknown')} skill to level {kwargs.get('new_level', 1)}!

**Milestone Unlocked:** {kwargs.get('milestone', 'Basic Achievement')}

This represents a significant advancement in their journey. The AI assistant recognizes this achievement and provides personalized guidance based on our collaborative work history.

Please provide:
1. A personalized congratulatory message
2. Specific advice for the next level
3. How this skill relates to our recent work together
4. Recommended next steps based on our conversation history
"""
        elif template_type == "equipment_gain":
            template_content = f"""
⚔️ **DREAMSCAPE EQUIPMENT ACQUISITION**

Player: {kwargs.get('player_name', 'Victor')}
Equipment: {kwargs.get('equipment_name', 'Unknown Item')}
Rarity: {kwargs.get('rarity', 'Common')}
Description: {kwargs.get('description', 'A mysterious item')}

🎁 **NEW EQUIPMENT OBTAINED!**

{kwargs.get('player_name', 'Victor')} has acquired the {kwargs.get('equipment_name', 'Unknown Item')} - a {kwargs.get('rarity', 'Common')} item!

**Description:** {kwargs.get('description', 'A mysterious item')}

This equipment represents a powerful tool that can enhance their capabilities. Based on our work history together, this item should integrate seamlessly with their existing toolkit.

Please provide:
1. A detailed analysis of how this equipment complements their current setup
2. Strategic advice on optimal usage
3. Connection to our recent collaborative projects
4. Potential synergies with existing tools and skills
"""
        elif template_type == "dreamscape":
            template_content = f"""
🌌 **DREAMSCAPE ANALYSIS**

Player: {kwargs.get('player_name', 'Victor')}
Current Level: {kwargs.get('current_level', 1)}
Experience Points: {kwargs.get('experience_points', 0)}
Recent Achievements: {', '.join(kwargs.get('recent_achievements', []))}

📊 **COMPREHENSIVE PROGRESS REPORT**

{kwargs.get('player_name', 'Victor')} has reached level {kwargs.get('current_level', 1)} with {kwargs.get('experience_points', 0)} experience points.

**Recent Achievements:**
{', '.join(kwargs.get('recent_achievements', []))}

Based on our extensive conversation history and collaborative work, this represents a significant milestone in their development journey.

Please provide:
1. A comprehensive analysis of their progress trajectory
2. Personalized insights based on our work patterns
3. Strategic recommendations for continued growth
4. How their achievements align with our collaborative goals
5. Next-level objectives that build on our established themes
"""
        else:
            template_content = kwargs.get('content', '')
        
        # Combine context with template
        full_prompt = f"{context_prompt}\n\n{template_content}"
        
        return full_prompt
    
    def demonstrate_contextual_templates(self):
        """Demonstrate the contextual template generation."""
        
        print(f"🎮 Sending contextual templates with conversation context...")
        print(f"📝 Context: {len(self.work_themes)} work themes, {len(self.conversation_data)} conversations")
        print(f"🔗 Recent topics: {', '.join([conv.get('title', '')[:30] for conv in self.conversation_data[:3]])}")
        
        # Generate contextual templates
        templates = []
        
        # Template 1: Skill up with context
        skill_template = self.generate_contextual_template(
            "skill_up",
            player_name="Victor",
            skill_name="AI Development",
            new_level=15,
            milestone="Advanced ChatGPT Integration"
        )
        templates.append(("Skill Up", skill_template))
        
        # Template 2: Equipment gain with context
        equipment_template = self.generate_contextual_template(
            "equipment_gain",
            player_name="Victor",
            equipment_name="Conversation Context Analyzer",
            rarity="Legendary",
            description="A powerful tool that analyzes conversation history to create personalized content"
        )
        templates.append(("Equipment Gain", equipment_template))
        
        # Template 3: Dreamscape analysis with context
        dreamscape_template = self.generate_contextual_template(
            "dreamscape",
            player_name="Victor",
            current_level=25,
            experience_points=15000,
            recent_achievements=["Built AI Scraper", "Created Template System", "Integrated Context"]
        )
        templates.append(("Dreamscape Analysis", dreamscape_template))
        
        # Display the contextual templates
        for i, (template_name, template_content) in enumerate(templates, 1):
            print(f"\n{'='*60}")
            print(f"🎯 TEMPLATE {i}: {template_name.upper()}")
            print(f"{'='*60}")
            print(template_content)
            print(f"\n📝 This template incorporates:")
            print(f"   • {len(self.work_themes)} identified work themes")
            print(f"   • {len(self.conversation_data)} conversation history items")
            print(f"   • Recent conversation topics for context")
            print(f"   • Personalized guidance based on collaborative history")
        
        return templates

def main():
    """Main demonstration function."""
    print("🎮 Starting Conversation Context Integration Demo")
    print("=" * 60)
    
    demo = ConversationContextDemo()
    
    # Load conversation history
    demo.load_conversation_history()
    
    if not demo.conversation_data:
        print("❌ No conversation data found. Please run a scraper first to collect conversation history.")
        return
    
    # Demonstrate contextual templates
    templates = demo.demonstrate_contextual_templates()
    
    # Summary
    print("\n🎯 Conversation Context Integration Summary")
    print("=" * 60)
    print(f"📊 Work Themes Identified: {len(demo.work_themes)}")
    print(f"💬 Conversations Analyzed: {len(demo.conversation_data)}")
    print(f"🎮 Templates Generated: {len(templates)}")
    
    print("\n🎉 Conversation context integration demo completed!")
    print("\n💡 KEY INSIGHTS:")
    print("• The AI now has access to your actual work history")
    print("• Templates are personalized based on your conversation patterns")
    print("• Content creation leverages your collaborative work themes")
    print("• Each template builds upon your established work relationships")
    print("\n🚀 NEXT STEPS:")
    print("• Use these contextual templates with ChatGPT")
    print("• The AI will respond with truly personalized content")
    print("• Your conversation history creates unique, meaningful interactions")

if __name__ == "__main__":
    main() 