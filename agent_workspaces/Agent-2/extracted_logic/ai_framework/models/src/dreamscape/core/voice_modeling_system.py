#!/usr/bin/env python3
"""
Voice Modeling System for Dreamscape
====================================

Enables users and agents to model their communication style for personalized content generation.
Features:
- Personality analysis and style extraction
- Voice training from conversation history
- Content generation with voice consistency
- Multi-voice support for different contexts
"""

import os
import sys
import json
import logging
import re
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict, field
import numpy as np
from textblob import TextBlob
import sqlite3

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class VoiceProfile:
    """Voice profile for a user or agent."""
    id: str
    name: str
    type: str  # 'user' or 'agent'
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Communication style characteristics
    tone: str = "professional"  # formal, casual, enthusiastic, technical, etc.
    writing_style: str = "conversational"  # academic, technical, creative, etc.
    response_length: str = "medium"  # short, medium, long
    formality_level: str = "balanced"  # formal, casual, balanced
    creativity_level: float = 0.7  # 0.0 to 1.0
    technical_depth: str = "intermediate"  # beginner, intermediate, advanced, expert
    humor_level: float = 0.3  # 0.0 to 1.0
    empathy_level: float = 0.8  # 0.0 to 1.0
    
    # Language patterns
    vocabulary_complexity: str = "moderate"  # simple, moderate, complex
    sentence_structure: str = "varied"  # simple, compound, varied
    punctuation_style: str = "standard"  # minimal, standard, expressive
    emoji_usage: float = 0.2  # 0.0 to 1.0
    
    # Domain expertise
    expertise_domains: List[str] = field(default_factory=lambda: ["general"])
    technical_terms: List[str] = field(default_factory=list)
    preferred_topics: List[str] = field(default_factory=list)
    
    # Communication patterns
    greeting_style: str = "professional"
    closing_style: str = "professional"
    question_style: str = "direct"
    explanation_style: str = "detailed"
    
    # Voice training data
    training_samples: List[Dict] = field(default_factory=list)
    confidence_score: float = 0.0  # 0.0 to 1.0
    sample_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert voice profile to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tone': self.tone,
            'writing_style': self.writing_style,
            'response_length': self.response_length,
            'formality_level': self.formality_level,
            'creativity_level': self.creativity_level,
            'technical_depth': self.technical_depth,
            'humor_level': self.humor_level,
            'empathy_level': self.empathy_level,
            'vocabulary_complexity': self.vocabulary_complexity,
            'sentence_structure': self.sentence_structure,
            'punctuation_style': self.punctuation_style,
            'emoji_usage': self.emoji_usage,
            'expertise_domains': self.expertise_domains,
            'technical_terms': self.technical_terms,
            'preferred_topics': self.preferred_topics,
            'greeting_style': self.greeting_style,
            'closing_style': self.closing_style,
            'question_style': self.question_style,
            'explanation_style': self.explanation_style,
            'training_samples': self.training_samples,
            'confidence_score': self.confidence_score,
            'sample_count': self.sample_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceProfile':
        """Create voice profile from dictionary."""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)

@dataclass
class VoiceTrainingConfig:
    """Configuration for voice training."""
    min_samples: int = 10
    max_samples: int = 100
    confidence_threshold: float = 0.7
    analysis_depth: str = "comprehensive"  # basic, standard, comprehensive
    update_frequency: str = "adaptive"  # daily, weekly, adaptive
    enable_learning: bool = True

class VoiceAnalyzer:
    """Analyzes communication patterns to extract voice characteristics."""
    
    def __init__(self):
        """Initialize the voice analyzer."""
        self.emoji_patterns = {
            'enthusiastic': ['🚀', '💪', '🔥', '⭐', '🎉', '✨'],
            'technical': ['⚙️', '🔧', '📊', '💻', '🔍', '📈'],
            'friendly': ['😊', '👍', '🙂', '👋', '💡', '🎯'],
            'professional': ['📋', '✅', '📝', '🔗', '📌', '💼']
        }
        
        self.tone_indicators = {
            'formal': ['therefore', 'consequently', 'furthermore', 'moreover'],
            'casual': ['hey', 'cool', 'awesome', 'great', 'nice'],
            'technical': ['implementation', 'architecture', 'optimization', 'algorithm'],
            'enthusiastic': ['amazing', 'incredible', 'fantastic', 'excellent', 'brilliant']
        }
    
    def analyze_conversation_style(self, messages: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation style from message history."""
        if not messages:
            return {}
        
        analysis = {
            'tone': self._analyze_tone(messages),
            'writing_style': self._analyze_writing_style(messages),
            'response_length': self._analyze_response_length(messages),
            'formality_level': self._analyze_formality(messages),
            'creativity_level': self._analyze_creativity(messages),
            'technical_depth': self._analyze_technical_depth(messages),
            'humor_level': self._analyze_humor(messages),
            'empathy_level': self._analyze_empathy(messages),
            'vocabulary_complexity': self._analyze_vocabulary(messages),
            'sentence_structure': self._analyze_sentence_structure(messages),
            'punctuation_style': self._analyze_punctuation(messages),
            'emoji_usage': self._analyze_emoji_usage(messages),
            'expertise_domains': self._extract_expertise_domains(messages),
            'technical_terms': self._extract_technical_terms(messages),
            'preferred_topics': self._extract_preferred_topics(messages),
            'communication_patterns': self._analyze_communication_patterns(messages)
        }
        
        return analysis
    
    def _analyze_tone(self, messages: List[Dict]) -> str:
        """Analyze the overall tone of messages."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        all_text_lower = all_text.lower()
        
        tone_scores = {}
        for tone, indicators in self.tone_indicators.items():
            score = sum(1 for indicator in indicators if indicator in all_text_lower)
            tone_scores[tone] = score
        
        if not tone_scores:
            return 'neutral'
        
        dominant_tone = max(tone_scores, key=tone_scores.get)
        return dominant_tone if tone_scores[dominant_tone] > 0 else 'neutral'
    
    def _analyze_writing_style(self, messages: List[Dict]) -> str:
        """Analyze writing style characteristics."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Analyze sentence complexity
        sentences = re.split(r'[.!?]+', all_text)
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
        
        # Analyze paragraph structure
        paragraphs = all_text.split('\n\n')
        avg_paragraph_length = np.mean([len(p.split()) for p in paragraphs if p.strip()])
        
        if avg_sentence_length > 20 or avg_paragraph_length > 100:
            return 'academic'
        elif avg_sentence_length < 10:
            return 'conversational'
        else:
            return 'technical'
    
    def _analyze_response_length(self, messages: List[Dict]) -> str:
        """Analyze typical response length."""
        lengths = [len(msg.get('content', '').split()) for msg in messages]
        avg_length = np.mean(lengths)
        
        if avg_length < 20:
            return 'short'
        elif avg_length > 100:
            return 'long'
        else:
            return 'medium'
    
    def _analyze_formality(self, messages: List[Dict]) -> str:
        """Analyze formality level."""
        formal_indicators = ['therefore', 'consequently', 'furthermore', 'moreover', 'thus']
        casual_indicators = ['hey', 'cool', 'awesome', 'great', 'nice', 'yeah']
        
        all_text = ' '.join([msg.get('content', '') for msg in messages]).lower()
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in all_text)
        casual_count = sum(1 for indicator in casual_indicators if indicator in all_text)
        
        if formal_count > casual_count * 2:
            return 'formal'
        elif casual_count > formal_count * 2:
            return 'casual'
        else:
            return 'balanced'
    
    def _analyze_creativity(self, messages: List[Dict]) -> float:
        """Analyze creativity level (0.0 to 1.0)."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Creativity indicators
        creative_indicators = [
            'imagine', 'creative', 'innovative', 'unique', 'original',
            'artistic', 'inspiring', 'visionary', 'breakthrough', 'revolutionary'
        ]
        
        creative_count = sum(1 for indicator in creative_indicators 
                           if indicator.lower() in all_text.lower())
        
        # Normalize to 0.0-1.0 scale
        max_possible = len(creative_indicators)
        creativity_score = min(creative_count / max_possible, 1.0)
        
        return creativity_score
    
    def _analyze_technical_depth(self, messages: List[Dict]) -> str:
        """Analyze technical depth level."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Technical indicators by level
        beginner_terms = ['basic', 'simple', 'easy', 'fundamental']
        intermediate_terms = ['implementation', 'architecture', 'design', 'system']
        advanced_terms = ['optimization', 'algorithm', 'complexity', 'scalability']
        expert_terms = ['theoretical', 'research', 'novel', 'breakthrough']
        
        scores = {
            'beginner': sum(1 for term in beginner_terms if term in all_text.lower()),
            'intermediate': sum(1 for term in intermediate_terms if term in all_text.lower()),
            'advanced': sum(1 for term in advanced_terms if term in all_text.lower()),
            'expert': sum(1 for term in expert_terms if term in all_text.lower())
        }
        
        if not any(scores.values()):
            return 'beginner'
        
        dominant_level = max(scores, key=scores.get)
        return dominant_level
    
    def _analyze_humor(self, messages: List[Dict]) -> float:
        """Analyze humor level (0.0 to 1.0)."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Humor indicators
        humor_indicators = ['haha', 'lol', '😄', '😊', '😆', '😂', 'funny', 'joke', 'humor']
        
        humor_count = sum(1 for indicator in humor_indicators 
                         if indicator.lower() in all_text.lower())
        
        # Normalize to 0.0-1.0 scale
        max_possible = len(humor_indicators)
        humor_score = min(humor_count / max_possible, 1.0)
        
        return humor_score
    
    def _analyze_empathy(self, messages: List[Dict]) -> float:
        """Analyze empathy level (0.0 to 1.0)."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Empathy indicators
        empathy_indicators = [
            'understand', 'feel', 'experience', 'support', 'help',
            'care', 'concern', 'appreciate', 'value', 'respect'
        ]
        
        empathy_count = sum(1 for indicator in empathy_indicators 
                           if indicator.lower() in all_text.lower())
        
        # Normalize to 0.0-1.0 scale
        max_possible = len(empathy_indicators)
        empathy_score = min(empathy_count / max_possible, 1.0)
        
        return empathy_score
    
    def _analyze_vocabulary(self, messages: List[Dict]) -> str:
        """Analyze vocabulary complexity."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        words = all_text.split()
        
        if not words:
            return 'simple'
        
        # Calculate average word length
        avg_word_length = np.mean([len(word) for word in words])
        
        if avg_word_length < 4:
            return 'simple'
        elif avg_word_length > 7:
            return 'complex'
        else:
            return 'moderate'
    
    def _analyze_sentence_structure(self, messages: List[Dict]) -> str:
        """Analyze sentence structure complexity."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        sentences = re.split(r'[.!?]+', all_text)
        
        if not sentences:
            return 'simple'
        
        # Analyze sentence complexity
        complex_sentences = 0
        for sentence in sentences:
            if sentence.strip():
                # Count clauses and conjunctions
                clauses = len(re.findall(r'[,;:]', sentence))
                if clauses > 2:
                    complex_sentences += 1
        
        complexity_ratio = complex_sentences / len(sentences)
        
        if complexity_ratio < 0.2:
            return 'simple'
        elif complexity_ratio > 0.6:
            return 'compound'
        else:
            return 'varied'
    
    def _analyze_punctuation(self, messages: List[Dict]) -> str:
        """Analyze punctuation style."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Count different punctuation types
        exclamation_count = all_text.count('!')
        question_count = all_text.count('?')
        ellipsis_count = all_text.count('...')
        
        total_sentences = len(re.split(r'[.!?]+', all_text))
        
        if total_sentences == 0:
            return 'standard'
        
        expressive_ratio = (exclamation_count + ellipsis_count) / total_sentences
        
        if expressive_ratio > 0.3:
            return 'expressive'
        elif exclamation_count + question_count < total_sentences * 0.1:
            return 'minimal'
        else:
            return 'standard'
    
    def _analyze_emoji_usage(self, messages: List[Dict]) -> float:
        """Analyze emoji usage frequency (0.0 to 1.0)."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Count emojis
        emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿]', all_text))
        
        # Normalize by text length
        word_count = len(all_text.split())
        if word_count == 0:
            return 0.0
        
        emoji_ratio = emoji_count / word_count
        return min(emoji_ratio * 100, 1.0)  # Scale appropriately
    
    def _extract_expertise_domains(self, messages: List[Dict]) -> List[str]:
        """Extract expertise domains from messages."""
        all_text = ' '.join([msg.get('content', '') for msg in messages]).lower()
        
        domains = {
            'technology': ['programming', 'software', 'code', 'development', 'tech'],
            'ai': ['artificial intelligence', 'machine learning', 'ai', 'ml', 'neural'],
            'business': ['business', 'strategy', 'management', 'leadership', 'entrepreneur'],
            'science': ['research', 'scientific', 'experiment', 'analysis', 'data'],
            'creative': ['design', 'art', 'creative', 'visual', 'aesthetic'],
            'education': ['learning', 'teaching', 'education', 'knowledge', 'study']
        }
        
        found_domains = []
        for domain, keywords in domains.items():
            if any(keyword in all_text for keyword in keywords):
                found_domains.append(domain)
        
        return found_domains if found_domains else ['general']
    
    def _extract_technical_terms(self, messages: List[Dict]) -> List[str]:
        """Extract technical terms from messages."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Technical term patterns
        technical_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+\.\w+\b',   # Namespace patterns
            r'\b\w+\(\)\b',    # Function calls
            r'\b\d+\.\d+\b',   # Version numbers
        ]
        
        technical_terms = set()
        for pattern in technical_patterns:
            matches = re.findall(pattern, all_text)
            technical_terms.update(matches)
        
        return list(technical_terms)[:20]  # Limit to top 20
    
    def _extract_preferred_topics(self, messages: List[Dict]) -> List[str]:
        """Extract preferred topics from messages."""
        all_text = ' '.join([msg.get('content', '') for msg in messages])
        
        # Topic extraction based on frequency
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        preferred_topics = [word for word, freq in sorted_words[:10] if freq > 2]
        
        return preferred_topics
    
    def _analyze_communication_patterns(self, messages: List[Dict]) -> Dict[str, str]:
        """Analyze communication patterns."""
        patterns = {
            'greeting_style': 'professional',
            'closing_style': 'professional',
            'question_style': 'direct',
            'explanation_style': 'detailed'
        }
        
        # Analyze greetings
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        for msg in messages[:3]:  # Check first few messages
            content = msg.get('content', '').lower()
            if any(greeting in content for greeting in greetings):
                if any(casual in content for casual in ['hey', 'hi']):
                    patterns['greeting_style'] = 'casual'
                else:
                    patterns['greeting_style'] = 'formal'
                break
        
        # Analyze questions
        question_indicators = ['what', 'how', 'why', 'when', 'where', '?']
        question_count = sum(1 for msg in messages 
                           if any(indicator in msg.get('content', '').lower() 
                                 for indicator in question_indicators))
        
        if question_count > len(messages) * 0.3:
            patterns['question_style'] = 'inquisitive'
        else:
            patterns['question_style'] = 'direct'
        
        return patterns

class VoiceModelingSystem:
    """Main voice modeling system for creating and managing voice profiles."""
    
    def __init__(self, db_path: str = "data/voice_profiles.db"):
        """Initialize the voice modeling system."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.analyzer = VoiceAnalyzer()
        self.voice_profiles: Dict[str, VoiceProfile] = {}
        
        self.init_database()
        self.load_voice_profiles()
    
    def init_database(self):
        """Initialize the voice profiles database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS voice_profiles (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    profile_data TEXT NOT NULL
                )
            """)
            conn.commit()
    
    def load_voice_profiles(self):
        """Load voice profiles from database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM voice_profiles")
            for row in cursor.fetchall():
                profile_data = json.loads(row[5])
                profile = VoiceProfile.from_dict(profile_data)
                self.voice_profiles[profile.id] = profile
    
    def save_voice_profile(self, profile: VoiceProfile):
        """Save voice profile to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO voice_profiles 
                (id, name, type, created_at, updated_at, profile_data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                profile.id,
                profile.name,
                profile.type,
                profile.created_at.isoformat(),
                profile.updated_at.isoformat(),
                json.dumps(profile.to_dict())
            ))
            conn.commit()
        
        self.voice_profiles[profile.id] = profile
    
    def create_voice_profile(self, name: str, profile_type: str = "user") -> VoiceProfile:
        """Create a new voice profile."""
        profile_id = f"{profile_type}_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        profile = VoiceProfile(
            id=profile_id,
            name=name,
            type=profile_type
        )
        
        self.save_voice_profile(profile)
        return profile
    
    def train_voice_from_conversations(self, profile_id: str, conversations: List[Dict], 
                                     config: VoiceTrainingConfig = None) -> bool:
        """Train a voice profile from conversation history."""
        if profile_id not in self.voice_profiles:
            logger.error(f"Voice profile {profile_id} not found")
            return False
        
        config = config or VoiceTrainingConfig()
        profile = self.voice_profiles[profile_id]
        
        try:
            # Extract messages from conversations
            all_messages = []
            for conv in conversations:
                messages = conv.get('messages', [])
                all_messages.extend(messages)
            
            if len(all_messages) < config.min_samples:
                logger.warning(f"Insufficient samples for training: {len(all_messages)} < {config.min_samples}")
                return False
            
            # Analyze communication style
            analysis = self.analyzer.analyze_conversation_style(all_messages)
            
            # Update voice profile with analysis results
            profile.tone = analysis.get('tone', profile.tone)
            profile.writing_style = analysis.get('writing_style', profile.writing_style)
            profile.response_length = analysis.get('response_length', profile.response_length)
            profile.formality_level = analysis.get('formality_level', profile.formality_level)
            profile.creativity_level = analysis.get('creativity_level', profile.creativity_level)
            profile.technical_depth = analysis.get('technical_depth', profile.technical_depth)
            profile.humor_level = analysis.get('humor_level', profile.humor_level)
            profile.empathy_level = analysis.get('empathy_level', profile.empathy_level)
            profile.vocabulary_complexity = analysis.get('vocabulary_complexity', profile.vocabulary_complexity)
            profile.sentence_structure = analysis.get('sentence_structure', profile.sentence_structure)
            profile.punctuation_style = analysis.get('punctuation_style', profile.punctuation_style)
            profile.emoji_usage = analysis.get('emoji_usage', profile.emoji_usage)
            profile.expertise_domains = analysis.get('expertise_domains', profile.expertise_domains)
            profile.technical_terms = analysis.get('technical_terms', profile.technical_terms)
            profile.preferred_topics = analysis.get('preferred_topics', profile.preferred_topics)
            
            # Update communication patterns
            patterns = analysis.get('communication_patterns', {})
            profile.greeting_style = patterns.get('greeting_style', profile.greeting_style)
            profile.closing_style = patterns.get('closing_style', profile.closing_style)
            profile.question_style = patterns.get('question_style', profile.question_style)
            profile.explanation_style = patterns.get('explanation_style', profile.explanation_style)
            
            # Store training samples
            profile.training_samples = all_messages[:config.max_samples]
            profile.sample_count = len(profile.training_samples)
            
            # Calculate confidence score
            profile.confidence_score = min(profile.sample_count / config.min_samples, 1.0)
            
            # Update timestamp
            profile.updated_at = datetime.now()
            
            # Save updated profile
            self.save_voice_profile(profile)
            
            logger.info(f"Voice profile {profile_id} trained successfully with {profile.sample_count} samples")
            return True
            
        except Exception as e:
            logger.error(f"Error training voice profile {profile_id}: {e}")
            return False
    
    def generate_content_with_voice(self, profile_id: str, prompt: str, 
                                  content_type: str = "response") -> str:
        """Generate content using a specific voice profile."""
        if profile_id not in self.voice_profiles:
            logger.error(f"Voice profile {profile_id} not found")
            return ""
        
        profile = self.voice_profiles[profile_id]
        
        # Create voice-specific prompt
        voice_prompt = self._create_voice_prompt(profile, prompt, content_type)
        
        # For now, return the voice prompt (in production, this would call an AI service)
        return voice_prompt
    
    def _create_voice_prompt(self, profile: VoiceProfile, prompt: str, content_type: str) -> str:
        """Create a voice-specific prompt for content generation."""
        voice_instructions = f"""
You are {profile.name}, with the following communication style:

**Voice Characteristics:**
- Tone: {profile.tone}
- Writing Style: {profile.writing_style}
- Response Length: {profile.response_length}
- Formality Level: {profile.formality_level}
- Creativity Level: {profile.creativity_level}
- Technical Depth: {profile.technical_depth}
- Humor Level: {profile.humor_level}
- Empathy Level: {profile.empathy_level}

**Language Patterns:**
- Vocabulary Complexity: {profile.vocabulary_complexity}
- Sentence Structure: {profile.sentence_structure}
- Punctuation Style: {profile.punctuation_style}
- Emoji Usage: {profile.emoji_usage}

**Expertise & Interests:**
- Domains: {', '.join(profile.expertise_domains)}
- Technical Terms: {', '.join(profile.technical_terms[:5])}
- Preferred Topics: {', '.join(profile.preferred_topics[:5])}

**Communication Patterns:**
- Greeting Style: {profile.greeting_style}
- Closing Style: {profile.closing_style}
- Question Style: {profile.question_style}
- Explanation Style: {profile.explanation_style}

**Task:**
Generate a {content_type} for the following prompt while maintaining {profile.name}'s voice:

{prompt}

Respond in {profile.name}'s authentic voice, incorporating their typical communication patterns, vocabulary choices, and style characteristics.
"""
        
        return voice_instructions
    
    def get_voice_profile(self, profile_id: str) -> Optional[VoiceProfile]:
        """Get a voice profile by ID."""
        return self.voice_profiles.get(profile_id)
    
    def list_voice_profiles(self, profile_type: str = None) -> List[VoiceProfile]:
        """List all voice profiles, optionally filtered by type."""
        profiles = list(self.voice_profiles.values())
        if profile_type:
            profiles = [p for p in profiles if p.type == profile_type]
        return profiles
    
    def delete_voice_profile(self, profile_id: str) -> bool:
        """Delete a voice profile."""
        if profile_id not in self.voice_profiles:
            return False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM voice_profiles WHERE id = ?", (profile_id,))
                conn.commit()
            
            del self.voice_profiles[profile_id]
            return True
            
        except Exception as e:
            logger.error(f"Error deleting voice profile {profile_id}: {e}")
            return False
    
    def update_voice_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
        """Update a voice profile with new characteristics."""
        if profile_id not in self.voice_profiles:
            return False
        
        profile = self.voice_profiles[profile_id]
        
        # Update allowed fields
        allowed_fields = [
            'tone', 'writing_style', 'response_length', 'formality_level',
            'creativity_level', 'technical_depth', 'humor_level', 'empathy_level',
            'vocabulary_complexity', 'sentence_structure', 'punctuation_style',
            'emoji_usage', 'expertise_domains', 'technical_terms', 'preferred_topics',
            'greeting_style', 'closing_style', 'question_style', 'explanation_style'
        ]
        
        for field, value in updates.items():
            if field in allowed_fields and hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.now()
        self.save_voice_profile(profile)
        
        return True

# Example usage and testing
if __name__ == "__main__":
    # Initialize voice modeling system
    voice_system = VoiceModelingSystem()
    
    # Create a voice profile
    profile = voice_system.create_voice_profile("Victor", "user")
    print(f"Created voice profile: {profile.name} ({profile.id})")
    
    # Example conversation data for training
    sample_conversations = [
        {
            'id': 'conv_1',
            'title': 'AI Development Discussion',
            'messages': [
                {'role': 'user', 'content': 'Hey! I\'m working on this amazing AI project and need some help with the architecture.'},
                {'role': 'assistant', 'content': 'That sounds fantastic! 🚀 I\'d love to help you design the architecture. What kind of AI project are you building?'},
                {'role': 'user', 'content': 'It\'s a conversational AI system that processes conversations and creates an MMORPG-like experience. Pretty cool, right?'},
                {'role': 'assistant', 'content': 'Wow, that\'s incredibly innovative! 💡 A conversational AI with MMORPG elements - that\'s definitely cutting-edge stuff.'}
            ]
        }
    ]
    
    # Train the voice profile
    success = voice_system.train_voice_from_conversations(profile.id, sample_conversations)
    print(f"Voice training {'successful' if success else 'failed'}")
    
    # Generate content with the voice
    content = voice_system.generate_content_with_voice(
        profile.id, 
        "Explain how to implement a machine learning pipeline",
        "explanation"
    )
    print(f"Generated content with voice:\n{content}") 