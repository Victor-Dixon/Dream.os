"""
Enhanced Player Progress System for Dream.OS
============================================

Integrates with prompting and response receiving logic to provide dynamic,
content-aware player progression based on actual conversation analysis.
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# from dreamscape.core.mmorpg_system import MMORPGEngine  # TODO: Use mmorpg_system after consolidation
from .models import Skill, SkillType
from dreamscape.core.memory import MemoryManager

logger = logging.getLogger(__name__)

class ProgressTrigger(Enum):
    """Types of progress triggers that can award XP and skills."""
    CONVERSATION_ANALYSIS = "conversation_analysis"
    BREAKTHROUGH_DISCOVERY = "breakthrough_discovery"
    SKILL_APPLICATION = "skill_application"
    PROBLEM_SOLVING = "problem_solving"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    INNOVATION = "innovation"
    MENTORSHIP = "mentorship"
    SYSTEM_ARCHITECTURE = "system_architecture"
    CODE_REVIEW = "code_review"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    COLLABORATION = "collaboration"

@dataclass
class ProgressEvent:
    """Represents a progress event that awards XP and skills."""
    trigger: ProgressTrigger
    xp_amount: int
    skill_rewards: Dict[str, int]
    description: str
    conversation_id: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

class EnhancedProgressSystem:
    """
    Enhanced progress system that analyzes conversations and responses
    to provide dynamic, content-aware player progression.
    """
    
    def __init__(self, mmorpg_engine: Any, memory_manager: MemoryManager):
        self.mmorpg_engine = mmorpg_engine
        self.memory_manager = memory_manager
        
        # Progress tracking
        self.progress_events: List[ProgressEvent] = []
        self.daily_progress: Dict[str, int] = {}
        
        # Content analysis patterns
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
        
        # Difficulty multipliers based on content complexity
        self.complexity_multipliers = {
            "simple": 1.0,
            "moderate": 1.5,
            "complex": 2.0,
            "expert": 3.0,
            "master": 4.0
        }
    
    def analyze_conversation_for_progress(self, conversation_id: str, conversation_content: str) -> ProgressEvent:
        """
        Analyze a conversation to determine appropriate progress rewards.
        """
        try:
            # Analyze content for skill applications
            skill_applications = self._detect_skill_applications(conversation_content)
            
            # Determine complexity level
            complexity = self._assess_complexity(conversation_content)
            
            # Identify progress triggers
            triggers = self._identify_progress_triggers(conversation_content)
            
            # Calculate XP based on content analysis
            base_xp = self._calculate_base_xp(conversation_content, skill_applications, triggers)
            complexity_multiplier = self.complexity_multipliers.get(complexity, 1.0)
            total_xp = int(base_xp * complexity_multiplier)
            
            # Calculate skill rewards
            skill_rewards = self._calculate_skill_rewards(skill_applications, triggers, complexity)
            
            # Create progress event
            event = ProgressEvent(
                trigger=triggers[0] if triggers else ProgressTrigger.CONVERSATION_ANALYSIS,
                xp_amount=total_xp,
                skill_rewards=skill_rewards,
                description=self._generate_progress_description(triggers, skill_applications, complexity),
                conversation_id=conversation_id,
                timestamp=datetime.now(),
                metadata={
                    "complexity": complexity,
                    "skill_applications": skill_applications,
                    "triggers": [t.value for t in triggers],
                    "word_count": len(conversation_content.split()),
                    "message_count": conversation_content.count("User:") + conversation_content.count("Assistant:")
                }
            )
            
            logger.info(f"Progress event created: {event.description} (+{total_xp} XP)")
            return event
            
        except Exception as e:
            logger.error(f"Failed to analyze conversation for progress: {e}")
            # Return basic progress event
            return ProgressEvent(
                trigger=ProgressTrigger.CONVERSATION_ANALYSIS,
                xp_amount=10,
                skill_rewards={},
                description="Basic conversation analysis",
                conversation_id=conversation_id,
                timestamp=datetime.now()
            )
    
    def process_ai_response_for_progress(self, conversation_id: str, ai_response: str, 
                                       original_prompt: str = None) -> ProgressEvent:
        """
        Analyze AI response to determine additional progress rewards.
        """
        try:
            # Analyze response quality and helpfulness
            response_quality = self._assess_response_quality(ai_response, original_prompt)
            
            # Detect knowledge sharing and mentorship
            knowledge_indicators = self._detect_knowledge_sharing(ai_response)
            
            # Calculate response-based XP
            base_xp = 5  # Base XP for receiving a response
            quality_bonus = response_quality * 10  # 0-50 XP based on quality
            knowledge_bonus = len(knowledge_indicators) * 5  # 5 XP per knowledge indicator
            
            total_xp = base_xp + quality_bonus + knowledge_bonus
            
            # Determine skill rewards based on response content
            skill_rewards = {}
            if knowledge_indicators:
                skill_rewards["knowledge_sharing"] = len(knowledge_indicators)
            
            # Create progress event
            event = ProgressEvent(
                trigger=ProgressTrigger.KNOWLEDGE_SHARING if knowledge_indicators else ProgressTrigger.CONVERSATION_ANALYSIS,
                xp_amount=total_xp,
                skill_rewards=skill_rewards,
                description=f"AI response analysis (Quality: {response_quality:.1f}/5.0)",
                conversation_id=conversation_id,
                timestamp=datetime.now(),
                metadata={
                    "response_quality": response_quality,
                    "knowledge_indicators": knowledge_indicators,
                    "response_length": len(ai_response)
                }
            )
            
            logger.info(f"Response progress event: {event.description} (+{total_xp} XP)")
            return event
            
        except Exception as e:
            logger.error(f"Failed to analyze AI response for progress: {e}")
            return None
    
    def apply_progress_event(self, event: ProgressEvent, override_daily_limit: bool = False) -> bool:
        """
        Apply a progress event to the MMORPG engine.
        
        Args:
            event: The progress event to apply
            override_daily_limit: If True, bypass daily XP limits (for first ingestion)
        """
        try:
            # Check daily limits (unless overridden for first ingestion)
            if not override_daily_limit:
                today = datetime.now().date().isoformat()
                daily_xp = self.daily_progress.get(today, 0)
                
                # Daily XP limit (prevent grinding)
                max_daily_xp = 1000
                if daily_xp + event.xp_amount > max_daily_xp:
                    event.xp_amount = max(0, max_daily_xp - daily_xp)
                    if event.xp_amount == 0:
                        logger.info(f"Daily XP limit reached for {today}")
                        return False
            else:
                logger.info(f"Daily XP limit overridden for first ingestion (+{event.xp_amount} XP)")
                today = datetime.now().date().isoformat()
                daily_xp = self.daily_progress.get(today, 0)
            
            # Apply XP and skills using XP dispatcher
            from dreamscape.mmorpg.xp_dispatcher import XPDispatcher
            dispatcher = XPDispatcher(self.mmorpg_engine)
            
            success = dispatcher.dispatch(
                event.xp_amount,
                skill_rewards=event.skill_rewards,
                source=f"enhanced_progress_{event.trigger.value}"
            )
            
            if success:
                # Update daily progress
                self.daily_progress[today] = daily_xp + event.xp_amount
                
                # Store progress event
                self.progress_events.append(event)
                
                logger.info(f"Progress applied: {event.description} (+{event.xp_amount} XP)")
                return True
            else:
                logger.warning(f"Failed to apply progress event: {event.description}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to apply progress event: {e}")
            return False
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of recent progress activity.
        """
        try:
            today = datetime.now().date()
            week_ago = today - timedelta(days=7)
            
            recent_events = [
                event for event in self.progress_events
                if event.timestamp.date() >= week_ago
            ]
            
            total_xp_gained = sum(event.xp_amount for event in recent_events)
            total_events = len(recent_events)
            
            # Group by trigger type
            trigger_counts = {}
            for event in recent_events:
                trigger = event.trigger.value
                trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
            
            # Most active skills
            skill_gains = {}
            for event in recent_events:
                for skill, amount in event.skill_rewards.items():
                    skill_gains[skill] = skill_gains.get(skill, 0) + amount
            
            return {
                "total_xp_gained": total_xp_gained,
                "total_events": total_events,
                "daily_xp": self.daily_progress.get(today.isoformat(), 0),
                "trigger_breakdown": trigger_counts,
                "skill_gains": skill_gains,
                "recent_events": [
                    {
                        "trigger": event.trigger.value,
                        "xp": event.xp_amount,
                        "description": event.description,
                        "timestamp": event.timestamp.isoformat()
                    }
                    for event in recent_events[-10:]  # Last 10 events
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get progress summary: {e}")
            return {}
    
    def is_first_ingestion(self, conversation_count: int) -> bool:
        """
        Determine if this appears to be a first ingestion based on conversation count.
        
        Args:
            conversation_count: Number of conversations to be processed
            
        Returns:
            True if this appears to be a first ingestion
        """
        # If more than 50 conversations to process, likely first ingestion
        return conversation_count > 50
    
    def get_daily_xp_status(self) -> Dict[str, Any]:
        """
        Get current daily XP status and limits.
        
        Returns:
            Dictionary with daily XP information
        """
        today = datetime.now().date().isoformat()
        daily_xp = self.daily_progress.get(today, 0)
        max_daily_xp = 1000
        
        return {
            "today": today,
            "current_xp": daily_xp,
            "max_xp": max_daily_xp,
            "remaining_xp": max_daily_xp - daily_xp,
            "percentage_used": (daily_xp / max_daily_xp) * 100 if max_daily_xp > 0 else 0
        }
    
    def _detect_skill_applications(self, content: str) -> List[str]:
        """Detect which skills are being applied in the content."""
        content_lower = content.lower()
        detected_skills = []
        
        for skill, patterns in self.skill_patterns.items():
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    detected_skills.append(skill)
                    break
        
        return detected_skills
    
    def _assess_complexity(self, content: str) -> str:
        """Assess the complexity level of the content."""
        word_count = len(content.split())
        message_count = content.count("User:") + content.count("Assistant:")
        
        # Simple heuristics for complexity assessment
        if word_count > 1000 and message_count > 10:
            return "master"
        elif word_count > 500 and message_count > 5:
            return "expert"
        elif word_count > 200 and message_count > 3:
            return "complex"
        elif word_count > 100:
            return "moderate"
        else:
            return "simple"
    
    def _identify_progress_triggers(self, content: str) -> List[ProgressTrigger]:
        """Identify progress triggers in the content."""
        triggers = []
        content_lower = content.lower()
        
        # Problem solving
        if any(word in content_lower for word in ["problem", "issue", "bug", "error", "fix"]):
            triggers.append(ProgressTrigger.PROBLEM_SOLVING)
        
        # Innovation
        if any(word in content_lower for word in ["innovative", "creative", "new approach", "breakthrough"]):
            triggers.append(ProgressTrigger.INNOVATION)
        
        # System architecture
        if any(word in content_lower for word in ["architecture", "design", "system", "structure"]):
            triggers.append(ProgressTrigger.SYSTEM_ARCHITECTURE)
        
        # Code review
        if any(word in content_lower for word in ["review", "code review", "refactor", "improve"]):
            triggers.append(ProgressTrigger.CODE_REVIEW)
        
        # Debugging
        if any(word in content_lower for word in ["debug", "troubleshoot", "diagnose"]):
            triggers.append(ProgressTrigger.DEBUGGING)
        
        # Optimization
        if any(word in content_lower for word in ["optimize", "performance", "efficiency"]):
            triggers.append(ProgressTrigger.OPTIMIZATION)
        
        # Documentation
        if any(word in content_lower for word in ["document", "comment", "explain", "guide"]):
            triggers.append(ProgressTrigger.DOCUMENTATION)
        
        # Testing
        if any(word in content_lower for word in ["test", "testing", "validate", "verify"]):
            triggers.append(ProgressTrigger.TESTING)
        
        # Collaboration
        if any(word in content_lower for word in ["collaborate", "team", "work together", "share"]):
            triggers.append(ProgressTrigger.COLLABORATION)
        
        return triggers if triggers else [ProgressTrigger.CONVERSATION_ANALYSIS]
    
    def _calculate_base_xp(self, content: str, skill_applications: List[str], 
                          triggers: List[ProgressTrigger]) -> int:
        """Calculate base XP based on content analysis."""
        base_xp = 10  # Base XP for any conversation
        
        # Skill application bonus
        skill_bonus = len(skill_applications) * 5
        
        # Trigger bonus
        trigger_bonus = len(triggers) * 3
        
        # Content length bonus (diminishing returns)
        word_count = len(content.split())
        length_bonus = min(20, word_count // 50)  # Max 20 XP for length
        
        return base_xp + skill_bonus + trigger_bonus + length_bonus
    
    def _calculate_skill_rewards(self, skill_applications: List[str], 
                               triggers: List[ProgressTrigger], complexity: str) -> Dict[str, int]:
        """Calculate skill rewards based on applications and triggers."""
        skill_rewards = {}
        
        # Reward for skill applications
        for skill in skill_applications:
            skill_rewards[skill] = skill_rewards.get(skill, 0) + 1
        
        # Reward for triggers
        for trigger in triggers:
            if trigger == ProgressTrigger.SYSTEM_ARCHITECTURE:
                skill_rewards["architecture"] = skill_rewards.get("architecture", 0) + 2
            elif trigger == ProgressTrigger.PROBLEM_SOLVING:
                skill_rewards["debugging"] = skill_rewards.get("debugging", 0) + 2
            elif trigger == ProgressTrigger.OPTIMIZATION:
                skill_rewards["optimization"] = skill_rewards.get("optimization", 0) + 2
        
        # Complexity bonus
        if complexity in ["expert", "master"]:
            for skill in skill_rewards:
                skill_rewards[skill] += 1
        
        return skill_rewards
    
    def _assess_response_quality(self, response: str, original_prompt: str = None) -> float:
        """Assess the quality of an AI response (0.0 to 5.0)."""
        quality_score = 2.5  # Base score
        
        # Length bonus
        response_length = len(response.split())
        if response_length > 100:
            quality_score += 0.5
        if response_length > 300:
            quality_score += 0.5
        
        # Code presence bonus
        if "```" in response:
            quality_score += 0.5
        
        # Explanation bonus
        if any(word in response.lower() for word in ["because", "reason", "explain", "why", "how"]):
            quality_score += 0.5
        
        # Specificity bonus
        if any(word in response.lower() for word in ["specifically", "for example", "such as", "including"]):
            quality_score += 0.5
        
        return min(5.0, quality_score)
    
    def _detect_knowledge_sharing(self, response: str) -> List[str]:
        """Detect knowledge sharing indicators in the response."""
        indicators = []
        response_lower = response.lower()
        
        # Teaching indicators
        if any(phrase in response_lower for phrase in ["here's how", "you can", "to do this", "the way to"]):
            indicators.append("teaching")
        
        # Explanation indicators
        if any(phrase in response_lower for phrase in ["this works because", "the reason is", "this happens when"]):
            indicators.append("explanation")
        
        # Best practice indicators
        if any(phrase in response_lower for phrase in ["best practice", "recommended", "should", "always"]):
            indicators.append("best_practices")
        
        # Example indicators
        if any(phrase in response_lower for phrase in ["for example", "here's an example", "let's say"]):
            indicators.append("examples")
        
        return indicators
    
    def _generate_progress_description(self, triggers: List[ProgressTrigger], 
                                     skill_applications: List[str], complexity: str) -> str:
        """Generate a description for the progress event."""
        trigger_names = [t.value.replace("_", " ").title() for t in triggers]
        skill_names = [s.replace("_", " ").title() for s in skill_applications]
        
        description = f"{trigger_names[0]} activity"
        
        if skill_applications:
            description += f" involving {', '.join(skill_names[:3])}"
        
        description += f" ({complexity} complexity)"
        
        return description 