"""
MMORPG Progression System
Contains the enhanced progress system for the Dreamscape MMORPG.
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from ..models import ProgressEvent, ProgressTrigger

logger = logging.getLogger(__name__)


class EnhancedProgressSystem:
    """
    Enhanced progress system that analyzes conversations and responses
    to provide dynamic, content-aware player progression.
    """
    
    def __init__(self, mmorpg_engine: Any, memory_manager: Any):
        """Initialize the enhanced progress system."""
        self.mmorpg_engine = mmorpg_engine
        self.memory_manager = memory_manager
        self.progress_events: List[ProgressEvent] = []
        self.daily_progress: Dict[str, int] = {}
        self.skill_patterns = {
            "python": ["python", "django", "flask", "pandas", "numpy", "matplotlib"],
            "javascript": ["javascript", "node.js", "react", "vue", "angular", "typescript"],
            "architecture": ["architecture", "design pattern", "microservices", "api", "rest"],
            "testing": ["test", "unit test", "integration test", "tdd", "bdd", "pytest"],
            "debugging": ["debug", "error", "bug", "fix", "issue", "problem"],
            "optimization": ["optimize", "performance", "efficiency", "speed", "memory"],
            "documentation": ["document", "readme", "api doc", "comment", "guide"],
            "deployment": ["deploy", "ci/cd", "docker", "kubernetes", "aws", "azure"],
            "security": ["security", "authentication", "authorization", "encryption", "vulnerability"],
            "database": ["sql", "database", "query", "schema", "migration", "orm"]
        }
        self.complexity_multipliers = {
            "simple": 1.0,
            "moderate": 1.5,
            "complex": 2.0,
            "expert": 3.0,
            "master": 4.0
        }

    def analyze_conversation(self, conversation_text: str, conversation_id: str) -> Dict[str, Any]:
        """Analyze a conversation for progress triggers and skill patterns."""
        analysis_result = {
            'triggers': [],
            'skills_detected': [],
            'complexity_level': 'simple',
            'xp_award': 0,
            'skill_rewards': {}
        }

        # Detect progress triggers
        for trigger in ProgressTrigger:
            if self._detect_trigger(conversation_text, trigger):
                analysis_result['triggers'].append(trigger.value)

        # Detect skill patterns
        for skill_name, patterns in self.skill_patterns.items():
            if self._detect_skill_pattern(conversation_text, patterns):
                analysis_result['skills_detected'].append(skill_name)
                analysis_result['skill_rewards'][skill_name] = 10

        # Determine complexity level
        analysis_result['complexity_level'] = self._determine_complexity(conversation_text)

        # Calculate XP award
        base_xp = len(analysis_result['triggers']) * 5 + len(analysis_result['skills_detected']) * 3
        complexity_multiplier = self.complexity_multipliers.get(analysis_result['complexity_level'], 1.0)
        analysis_result['xp_award'] = int(base_xp * complexity_multiplier)

        return analysis_result

    def _detect_trigger(self, text: str, trigger: ProgressTrigger) -> bool:
        """Detect if a specific progress trigger is present in the text."""
        trigger_patterns = {
            ProgressTrigger.CONVERSATION_ANALYSIS: [r'analyze', r'analysis', r'conversation'],
            ProgressTrigger.BREAKTHROUGH_DISCOVERY: [r'breakthrough', r'discovery', r'found', r'discovered'],
            ProgressTrigger.SKILL_APPLICATION: [r'applied', r'used', r'implemented', r'utilized'],
            ProgressTrigger.PROBLEM_SOLVING: [r'solved', r'fixed', r'resolved', r'problem'],
            ProgressTrigger.KNOWLEDGE_SHARING: [r'shared', r'explained', r'teach', r'guide'],
            ProgressTrigger.INNOVATION: [r'innovative', r'creative', r'new approach', r'novel'],
            ProgressTrigger.MENTORSHIP: [r'mentor', r'guide', r'help', r'assist'],
            ProgressTrigger.SYSTEM_ARCHITECTURE: [r'architecture', r'design', r'system', r'structure'],
            ProgressTrigger.CODE_REVIEW: [r'review', r'code review', r'feedback', r'critique'],
            ProgressTrigger.DEBUGGING: [r'debug', r'error', r'bug', r'fix'],
            ProgressTrigger.OPTIMIZATION: [r'optimize', r'performance', r'efficiency', r'improve'],
            ProgressTrigger.DOCUMENTATION: [r'document', r'readme', r'comment', r'guide'],
            ProgressTrigger.TESTING: [r'test', r'unit test', r'integration', r'verify'],
            ProgressTrigger.DEPLOYMENT: [r'deploy', r'production', r'release', r'launch'],
            ProgressTrigger.COLLABORATION: [r'collaborate', r'team', r'work together', r'partner']
        }

        patterns = trigger_patterns.get(trigger, [])
        text_lower = text.lower()
        
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return True
        return False

    def _detect_skill_pattern(self, text: str, patterns: List[str]) -> bool:
        """Detect if skill patterns are present in the text."""
        text_lower = text.lower()
        for pattern in patterns:
            if pattern.lower() in text_lower:
                return True
        return False

    def _determine_complexity(self, text: str) -> str:
        """Determine the complexity level of the conversation."""
        word_count = len(text.split())
        
        if word_count < 50:
            return "simple"
        elif word_count < 200:
            return "moderate"
        elif word_count < 500:
            return "complex"
        elif word_count < 1000:
            return "expert"
        else:
            return "master"

    def award_progress(self, conversation_id: str, analysis_result: Dict[str, Any]) -> bool:
        """Award progress based on analysis results."""
        try:
            # Create progress event
            event = ProgressEvent(
                trigger=ProgressTrigger.CONVERSATION_ANALYSIS,  # Default trigger
                xp_amount=analysis_result['xp_award'],
                skill_rewards=analysis_result['skill_rewards'],
                description=f"Conversation analysis: {len(analysis_result['triggers'])} triggers, {len(analysis_result['skills_detected'])} skills",
                conversation_id=conversation_id,
                timestamp=datetime.now(),
                metadata=analysis_result
            )

            # Add to progress events
            self.progress_events.append(event)

            # Update daily progress
            today = datetime.now().date().isoformat()
            self.daily_progress[today] = self.daily_progress.get(today, 0) + analysis_result['xp_award']

            # Award XP to player
            if self.mmorpg_engine:
                self.mmorpg_engine.add_xp_to_player(analysis_result['xp_award'])

            logger.info(f"Awarded {analysis_result['xp_award']} XP for conversation {conversation_id}")
            return True

        except Exception as e:
            logger.error(f"Error awarding progress: {e}")
            return False

    def get_daily_progress(self, date: str = None) -> int:
        """Get daily progress for a specific date."""
        if date is None:
            date = datetime.now().date().isoformat()
        return self.daily_progress.get(date, 0)

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of progress events."""
        total_events = len(self.progress_events)
        total_xp = sum(event.xp_amount for event in self.progress_events)
        total_skills = sum(len(event.skill_rewards) for event in self.progress_events)
        
        return {
            'total_events': total_events,
            'total_xp': total_xp,
            'total_skills': total_skills,
            'daily_progress': dict(self.daily_progress),
            'recent_events': [
                {
                    'trigger': event.trigger.value,
                    'xp_amount': event.xp_amount,
                    'description': event.description,
                    'timestamp': event.timestamp.isoformat()
                }
                for event in self.progress_events[-10:]  # Last 10 events
            ]
        }

    def clear_progress_events(self) -> None:
        """Clear all progress events."""
        self.progress_events.clear()

    def export_progress_data(self) -> Dict[str, Any]:
        """Export progress data for persistence."""
        return {
            'progress_events': [
                {
                    'trigger': event.trigger.value,
                    'xp_amount': event.xp_amount,
                    'skill_rewards': event.skill_rewards,
                    'description': event.description,
                    'conversation_id': event.conversation_id,
                    'timestamp': event.timestamp.isoformat(),
                    'metadata': event.metadata
                }
                for event in self.progress_events
            ],
            'daily_progress': dict(self.daily_progress)
        }

    def load_progress_data(self, data: Dict[str, Any]) -> bool:
        """Load progress data from persistence."""
        try:
            self.progress_events.clear()
            self.daily_progress.clear()

            # Load progress events
            for event_data in data.get('progress_events', []):
                event = ProgressEvent(
                    trigger=ProgressTrigger(event_data['trigger']),
                    xp_amount=event_data['xp_amount'],
                    skill_rewards=event_data['skill_rewards'],
                    description=event_data['description'],
                    conversation_id=event_data['conversation_id'],
                    timestamp=datetime.fromisoformat(event_data['timestamp']),
                    metadata=event_data.get('metadata', {})
                )
                self.progress_events.append(event)

            # Load daily progress
            self.daily_progress.update(data.get('daily_progress', {}))

            return True

        except Exception as e:
            logger.error(f"Error loading progress data: {e}")
            return False 