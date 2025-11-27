#!/usr/bin/env python3
"""
Agent Devlog Trainer
Trains an AI agent on user conversation patterns to generate devlogs in their style
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# EDIT START: Fix import for ContextUtils to avoid 'src.' fallback
# def _try_import_context_utils():
#     try:
#         from dreamscape.core.utils.context_utils import ContextUtils
#     except ImportError:
#         from src.dreamscape.core.utils.context_utils import ContextUtils
#     return ContextUtils

# EDIT START: Import YAML extraction utility
def _try_import_context_utils():
    from dreamscape.core.utils.context_utils import ContextUtils, extract_last_yaml_block
    return ContextUtils, extract_last_yaml_block
# EDIT END

# EDIT START: MMORPG modular import refactor and expansion
# Old (if present):
# from dreamscape.core.mmorpg.mmorpg_engine import MMORPGEngine
# from dreamscape.core.mmorpg.models import QuestType, Quest
# from dreamscape.core.mmorpg_engine import MMORPGEngine
# New modular imports (expand as needed for future devlog/game integration):
# Core engine
# from dreamscape.core.mmorpg.engine.game_engine import MMORPGEngine
# Progression and combat engines
# from dreamscape.core.mmorpg.engine.progression_engine import ProgressionEngine
# from dreamscape.core.mmorpg.engine.combat_engine import CombatEngine
# Models
# from dreamscape.core.mmorpg.models.character import Character
# from dreamscape.core.mmorpg.models.skill import Skill
# from dreamscape.core.mmorpg.models.quest import Quest, QuestType
# from dreamscape.core.mmorpg.models.achievement import Achievement
# from dreamscape.core.mmorpg.models.progression import Progression
# Systems
# from dreamscape.core.mmorpg.systems.skill_system import SkillSystem
# from dreamscape.core.mmorpg.systems.quest_system import QuestSystem
# from dreamscape.core.mmorpg.systems.achievement_system import AchievementSystem
# from dreamscape.core.mmorpg.systems.inventory_system import InventorySystem
# Resume
# from dreamscape.core.mmorpg.resume.resume_generator import ResumeGenerator
# from dreamscape.core.mmorpg.resume.skill_mapper import SkillMapper
# Progress tracking
# from dreamscape.core.mmorpg.progress.progress_tracker import ProgressTracker
# Backward compatibility shim (if needed)
# from dreamscape.core.mmorpg_system import MMORPGEngine as LegacyMMORPGEngine
# (No direct usage in this file yet, but ready for future expansion.)
# EDIT END

class AgentDevlogTrainer:
    """Trains an agent on user conversation patterns for devlog generation"""
    
    def __init__(self):
        self.project_root = project_root
        self.data_dir = project_root / "data"
        self.conversations_dir = self.data_dir / "conversations"
        self.processed_dir = self.data_dir / "processed_conversations"
        self.agent_dir = project_root / "outputs" / "trained_agents"
        self.devlog_dir = project_root / "outputs" / "devlogs"
        
        # Create directories
        for dir_path in [self.processed_dir, self.agent_dir, self.devlog_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # User profile for training
        self.user_profile = self._load_user_profile()
    
    def _load_user_profile(self) -> Dict:
        """Load or create user profile for training"""
        profile_file = self.agent_dir / "user_profile.json"
        
        if profile_file.exists():
            with open(profile_file, 'r') as f:
                return json.load(f)
        
        # Create default profile
        profile = {
            "name": "Dream.OS Developer",
            "style_characteristics": {
                "tone": "enthusiastic and technical",
                "writing_style": "conversational with technical depth",
                "interests": ["AI", "game development", "system architecture", "innovation"],
                "common_topics": ["Dream.OS", "AI agents", "MMORPG", "memory systems"],
                "communication_patterns": {
                    "sentence_length": "medium to long",
                    "technical_detail": "high",
                    "enthusiasm_level": "high",
                    "problem_solving_approach": "systematic"
                }
            },
            "devlog_preferences": {
                "format": "narrative with technical insights",
                "sections": ["overview", "technical_details", "challenges", "next_steps"],
                "length": "medium (500-1000 words)",
                "tone": "excited about progress, honest about challenges"
            },
            "training_data": {
                "conversations_analyzed": 0,
                "patterns_extracted": 0,
                "last_training": None
            }
        }
        
        # Save profile
        with open(profile_file, 'w') as f:
            json.dump(profile, f, indent=2)
        
        return profile
    
    def analyze_conversation_style(self, conversation_data: Dict) -> Dict:
        """Analyze conversation to extract user's communication style"""
        analysis = {
            "message_count": 0,
            "avg_message_length": 0,
            "technical_terms": [],
            "enthusiasm_indicators": [],
            "problem_solving_patterns": [],
            "common_topics": [],
            "writing_style": {},
            "interests": set()
        }
        
        total_length = 0
        messages = []
        
        # Extract user messages
        for message in conversation_data.get("messages", []):
            if message.get("role") == "user":
                content = message.get("content", "")
                messages.append(content)
                total_length += len(content)
                analysis["message_count"] += 1
                
                # Analyze technical terms
                tech_terms = self._extract_technical_terms(content)
                analysis["technical_terms"].extend(tech_terms)
                
                # Analyze enthusiasm
                enthusiasm = self._detect_enthusiasm(content)
                if enthusiasm:
                    analysis["enthusiasm_indicators"].append(enthusiasm)
                
                # Extract topics
                topics = self._extract_topics(content)
                analysis["interests"].update(topics)
        
        # Calculate averages
        if analysis["message_count"] > 0:
            analysis["avg_message_length"] = total_length / analysis["message_count"]
        
        # Analyze writing style
        analysis["writing_style"] = self._analyze_writing_style(messages)
        
        # Convert sets to lists for JSON serialization
        analysis["interests"] = list(analysis["interests"])
        
        return analysis
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract technical terms from text"""
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+\.\w+\b',   # Dotted terms
            r'\b(API|SDK|GUI|CLI|REST|JSON|XML|SQL|HTTP|HTTPS|TCP|UDP)\b',
            r'\b(algorithm|function|method|class|object|interface|database|server|client)\b',
            r'\b(memory|vector|index|query|cache|optimization|performance|scalability)\b'
        ]
        
        terms = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.extend(matches)
        
        return list(set(terms))
    
    def _detect_enthusiasm(self, text: str) -> Optional[str]:
        """Detect enthusiasm indicators in text"""
        enthusiasm_patterns = [
            (r'\b(excited|amazing|awesome|incredible|fantastic|brilliant)\b', 'positive'),
            (r'\b(wow|wow!|amazing!|incredible!)\b', 'excited'),
            (r'\b(love|adore|enjoy|fascinated by)\b', 'passionate'),
            (r'\b(breakthrough|revolutionary|game-changing)\b', 'innovative')
        ]
        
        for pattern, category in enthusiasm_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return category
        
        return None
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics of interest from text"""
        topic_patterns = [
            r'\b(AI|artificial intelligence|machine learning|ML)\b',
            r'\b(game|gaming|MMORPG|RPG|quest|character)\b',
            r'\b(system|architecture|design|development|coding|programming)\b',
            r'\b(memory|database|storage|vector|index)\b',
            r'\b(agent|bot|automation|workflow)\b',
            r'\b(innovation|creativity|problem solving)\b'
        ]
        
        topics = []
        for pattern in topic_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            topics.extend(matches)
        
        return list(set(topics))
    
    def _analyze_writing_style(self, messages: List[str]) -> Dict:
        """Analyze writing style patterns"""
        if not messages:
            return {}
        
        all_text = " ".join(messages)
        
        style = {
            "avg_sentence_length": 0,
            "uses_emojis": False,
            "uses_technical_terms": False,
            "uses_questions": False,
            "uses_exclamations": False,
            "paragraph_style": "single" if len(messages) <= 1 else "multiple"
        }
        
        # Analyze sentence length
        sentences = re.split(r'[.!?]+', all_text)
        sentence_lengths = [len(s.strip().split()) for s in sentences if s.strip()]
        if sentence_lengths:
            style["avg_sentence_length"] = sum(sentence_lengths) / len(sentence_lengths)
        
        # Analyze patterns
        style["uses_emojis"] = bool(re.search(r'[😀-🙏🌀-🗿]', all_text))
        style["uses_technical_terms"] = bool(re.search(r'\b[A-Z]{2,}\b', all_text))
        style["uses_questions"] = bool(re.search(r'\?', all_text))
        style["uses_exclamations"] = bool(re.search(r'!', all_text))
        
        return style
    
    def train_on_conversations(self, conversation_files: List[Path]) -> Dict:
        """Train the agent on multiple conversations"""
        print(f"🎓 Training agent on {len(conversation_files)} conversations...")
        
        training_data = {
            "conversations_analyzed": 0,
            "total_messages": 0,
            "style_patterns": [],
            "technical_vocabulary": set(),
            "topic_interests": set(),
            "enthusiasm_patterns": [],
            "writing_characteristics": []
        }
        
        for conv_file in conversation_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    conversation = json.load(f)
                
                # Analyze conversation
                analysis = self.analyze_conversation_style(conversation)
                
                # Accumulate training data
                training_data["conversations_analyzed"] += 1
                training_data["total_messages"] += analysis["message_count"]
                training_data["style_patterns"].append(analysis["writing_style"])
                training_data["technical_vocabulary"].update(analysis["technical_terms"])
                training_data["topic_interests"].update(analysis["interests"])
                training_data["enthusiasm_patterns"].extend(analysis["enthusiasm_indicators"])
                
                print(f"  ✅ Analyzed: {conv_file.name}")
                
            except Exception as e:
                print(f"  ❌ Failed to analyze {conv_file.name}: {e}")
        
        # Convert sets to lists
        training_data["technical_vocabulary"] = list(training_data["technical_vocabulary"])
        training_data["topic_interests"] = list(training_data["topic_interests"])
        
        # Update user profile
        self._update_user_profile(training_data)
        
        # Save training data
        training_file = self.agent_dir / f"training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(training_file, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        print(f"🎉 Training completed! Analyzed {training_data['conversations_analyzed']} conversations")
        return training_data
    
    def _update_user_profile(self, training_data: Dict):
        """Update user profile with training insights"""
        # Update style characteristics
        if training_data["style_patterns"]:
            avg_sentence_length = sum(p.get("avg_sentence_length", 0) for p in training_data["style_patterns"]) / len(training_data["style_patterns"])
            
            self.user_profile["style_characteristics"]["communication_patterns"]["sentence_length"] = "long" if avg_sentence_length > 20 else "medium" if avg_sentence_length > 10 else "short"
        
        # Update interests
        if training_data["topic_interests"]:
            self.user_profile["style_characteristics"]["interests"] = list(training_data["topic_interests"])
        
        # Update technical vocabulary
        if training_data["technical_vocabulary"]:
            self.user_profile["style_characteristics"]["technical_vocabulary"] = training_data["technical_vocabulary"]
        
        # Update training metadata
        self.user_profile["training_data"]["conversations_analyzed"] = training_data["conversations_analyzed"]
        self.user_profile["training_data"]["patterns_extracted"] = len(training_data["style_patterns"])
        self.user_profile["training_data"]["last_training"] = datetime.now().isoformat()
        
        # Save updated profile
        profile_file = self.agent_dir / "user_profile.json"
        with open(profile_file, 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def generate_devlog_prompt(self, topic: str, context: str = "") -> str:
        """Generate a devlog prompt based on user's style"""
        prompt = f"""You are {self.user_profile['name']}, a passionate developer working on Dream.OS. 

Based on your communication style and interests, write a devlog entry about: {topic}

Your writing characteristics:
- Tone: {self.user_profile['style_characteristics']['tone']}
- Writing style: {self.user_profile['style_characteristics']['writing_style']}
- Technical detail level: {self.user_profile['style_characteristics']['communication_patterns']['technical_detail']}
- Enthusiasm level: {self.user_profile['style_characteristics']['communication_patterns']['enthusiasm_level']}

Your interests: {', '.join(self.user_profile['style_characteristics']['interests'])}

Devlog format preferences:
- Format: {self.user_profile['devlog_preferences']['format']}
- Length: {self.user_profile['devlog_preferences']['length']}
- Tone: {self.user_profile['devlog_preferences']['tone']}

Context: {context}

Write a devlog entry that sounds exactly like you would write it, incorporating your typical enthusiasm, technical depth, and writing style."""
        
        return prompt
    
    def generate_devlog(self, topic: str, context: str = "", use_ai: bool = True) -> str:
        """Generate a devlog entry in the user's style"""
        if use_ai:
            # This would integrate with an AI service like OpenAI
            # For now, we'll create a template-based devlog
            return self._generate_template_devlog(topic, context)
        else:
            return self._generate_template_devlog(topic, context)
    
    def _generate_template_devlog(self, topic: str, context: str) -> str:
        """Generate a devlog using templates based on user's style, with automated state/context injection and YAML extraction."""
        # EDIT START: Automated YAML extraction for structured devlog
        ContextUtils, extract_last_yaml_block = _try_import_context_utils()
        context_utils = ContextUtils()
        # Try to load the most recent conversation for context
        recent_convs = list(self.conversations_dir.glob("*.json"))
        recent_convs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        conversation_data = None
        conversation_text = None
        if recent_convs:
            try:
                with open(recent_convs[0], 'r', encoding='utf-8') as f:
                    conversation_data = json.load(f)
                    # Try to get full conversation text (content or messages)
                    if isinstance(conversation_data, dict):
                        if 'content' in conversation_data:
                            conversation_text = conversation_data['content']
                        elif 'messages' in conversation_data:
                            conversation_text = '\n'.join(m.get('content','') for m in conversation_data['messages'] if 'content' in m)
            except Exception:
                conversation_data = None
        structured = extract_last_yaml_block(conversation_text or "") if conversation_text else None
        if structured:
            # Use Jinja template with structured YAML fields
            from jinja2 import Environment, FileSystemLoader
            env = Environment(loader=FileSystemLoader('templates'))
            try:
                template = env.get_template('devlog_template.md.j2')
                devlog = template.render(**structured)
                return devlog
            except Exception:
                pass  # fallback below if template fails
        # Fallback: use comprehensive context as before
        comprehensive_context = context_utils.get_comprehensive_context(conversation_data or {})
        # EDIT END
        enthusiasm_level = self.user_profile["style_characteristics"]["communication_patterns"]["enthusiasm_level"]
        technical_level = self.user_profile["style_characteristics"]["communication_patterns"]["technical_detail"]
        if enthusiasm_level == "high":
            intro = f"🎉 Wow! What an incredible breakthrough we've made with {topic}! I'm absolutely thrilled to share this progress with you."
        else:
            intro = f"Today I want to share some significant progress on {topic}."
        if technical_level == "high":
            technical_section = f"""
## Technical Deep Dive

The implementation involved several key components:
- **Core Architecture**: We've built a robust foundation that scales beautifully
- **Performance Optimization**: Achieved remarkable efficiency improvements
- **Integration Points**: Seamless connectivity with existing systems
"""
        else:
            technical_section = f"""
## What We Built

We've created a solid foundation for {topic} that integrates well with our existing systems.
"""
        context_block = f"\n---\n**Context & Game State:**\n{json.dumps(comprehensive_context, indent=2, ensure_ascii=False)}\n---\n"
        devlog = f"""# Devlog: {topic.title()}

{intro}

{context}

{technical_section}
{context_block}
## Challenges & Solutions

Every great project comes with its challenges, and this was no exception. We faced some interesting technical hurdles, but the solutions we found were even more exciting!

## Next Steps

I'm incredibly excited about where this is going. The foundation we've built opens up so many possibilities for future development.

---

*Generated by Dream.OS Agent Trainer - Learning from your style!* 🚀
"""
        return devlog
    
    def save_devlog(self, devlog_content: str, topic: str) -> Path:
        """Save devlog to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"devlog_{topic.lower().replace(' ', '_')}_{timestamp}.md"
        devlog_file = self.devlog_dir / filename
        # EDIT START: Ensure devlog directory exists before saving
        self.devlog_dir.mkdir(parents=True, exist_ok=True)
        # EDIT END
        with open(devlog_file, 'w', encoding='utf-8') as f:
            f.write(devlog_content)
        return devlog_file

def main():
    """Test the agent trainer"""
    trainer = AgentDevlogTrainer()
    
    # Find conversation files
    conversation_files = list(trainer.conversations_dir.glob("*.json"))
    
    if not conversation_files:
        print("No conversation files found. Please run the ChatGPT scraper first.")
        return
    
    print(f"Found {len(conversation_files)} conversation files")
    
    # Train on conversations
    training_data = trainer.train_on_conversations(conversation_files)
    
    # Generate a test devlog
    test_topic = "Enhanced Discord Integration"
    test_context = "Successfully implemented multi-modal Discord showcase with custom scenarios and analytics."
    
    devlog = trainer.generate_devlog(test_topic, test_context)
    devlog_file = trainer.save_devlog(devlog, test_topic)
    
    print(f"\n📝 Generated devlog: {devlog_file}")
    print("\nDevlog Preview:")
    print("=" * 50)
    print(devlog[:500] + "..." if len(devlog) > 500 else devlog)

if __name__ == "__main__":
    main() 