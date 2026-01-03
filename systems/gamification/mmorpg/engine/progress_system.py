"""
MMORPG Progress System
Contains the enhanced progress tracking system for the Dreamscape MMORPG.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import os

from ..models import (
    ProgressTrigger, ProgressEvent, Player, Quest, Skill,
    AISkillAnalysis, AIProjectAnalysis
)


class EnhancedProgressSystem:
    """Enhanced progress tracking system for MMORPG."""
    
    def __init__(self, mmorpg_engine: Any, memory_manager: Any):
        """Initialize the enhanced progress system."""
        self.mmorpg_engine = mmorpg_engine
        self.memory_manager = memory_manager
        self.progress_events = []
        self.skill_analyses = {}
        self.project_analyses = {}
        self.progress_file = "enhanced_progress.json"
        
    def record_progress_event(self, trigger: ProgressTrigger, xp_amount: int, 
                            skill_rewards: Dict[str, int], description: str, 
                            conversation_id: str, metadata: Dict[str, Any] = None) -> bool:
        """Record a progress event."""
        try:
            event = ProgressEvent(
                trigger=trigger,
                xp_amount=xp_amount,
                skill_rewards=skill_rewards,
                description=description,
                conversation_id=conversation_id,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            
            self.progress_events.append(event)
            
            # Update player XP
            player = self.mmorpg_engine.get_player()
            if player:
                player.add_xp(xp_amount)
                
            # Update skills
            for skill_name, skill_xp in skill_rewards.items():
                skill = self.mmorpg_engine.get_skill_by_name(skill_name)
                if skill:
                    skill.add_experience(skill_xp)
                    
            return True
        except Exception as e:
            print(f"Error recording progress event: {e}")
            return False
            
    def get_progress_events(self, days: int = 7) -> List[ProgressEvent]:
        """Get progress events from the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [event for event in self.progress_events if event.timestamp >= cutoff_date]
        
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of progress events."""
        if not self.progress_events:
            return {}
            
        total_xp = sum(event.xp_amount for event in self.progress_events)
        total_events = len(self.progress_events)
        
        # Group by trigger type
        trigger_counts = {}
        for event in self.progress_events:
            trigger_name = event.trigger.value
            trigger_counts[trigger_name] = trigger_counts.get(trigger_name, 0) + 1
            
        # Get recent activity
        recent_events = self.get_progress_events(days=1)
        recent_xp = sum(event.xp_amount for event in recent_events)
        
        return {
            'total_xp_earned': total_xp,
            'total_events': total_events,
            'recent_xp_earned': recent_xp,
            'recent_events': len(recent_events),
            'trigger_breakdown': trigger_counts,
            'last_event': self.progress_events[-1].timestamp.isoformat() if self.progress_events else None
        }
        
    def analyze_skill_progress(self, skill_name: str, conversation_ids: List[str] = None) -> Optional[AISkillAnalysis]:
        """Analyze progress for a specific skill."""
        try:
            # Get skill from engine
            skill = self.mmorpg_engine.get_skill_by_name(skill_name)
            if not skill:
                return None
                
            # Get related progress events
            skill_events = []
            for event in self.progress_events:
                if skill_name in event.skill_rewards:
                    if not conversation_ids or event.conversation_id in conversation_ids:
                        skill_events.append(event)
                        
            if not skill_events:
                return None
                
            # Calculate proficiency level
            total_skill_xp = sum(event.skill_rewards.get(skill_name, 0) for event in skill_events)
            if total_skill_xp < 100:
                proficiency = 'beginner'
            elif total_skill_xp < 500:
                proficiency = 'intermediate'
            elif total_skill_xp < 1000:
                proficiency = 'advanced'
            else:
                proficiency = 'expert'
                
            # Calculate confidence based on consistency
            recent_events = [e for e in skill_events if e.timestamp >= datetime.now() - timedelta(days=7)]
            confidence = min(len(recent_events) / 10.0, 1.0)  # Cap at 1.0
            confidence = max(confidence, 0.1)  # Minimum 0.1
            
            # Get evidence from events
            evidence = [event.description for event in skill_events[-5:]]  # Last 5 events
            
            # Get conversation IDs
            event_conversation_ids = list(set(event.conversation_id for event in skill_events))
            
            # Get last used time
            last_used = max(event.timestamp for event in skill_events)
            
            # Create AI insights
            ai_insights = {
                'total_skill_xp': total_skill_xp,
                'event_count': len(skill_events),
                'recent_activity': len(recent_events),
                'proficiency_trend': 'increasing' if len(recent_events) > len(skill_events) // 2 else 'stable'
            }
            
            # Determine skill relationships (placeholder)
            skill_relationships = []
            
            # Create learning path (placeholder)
            learning_path = [f"Practice {skill_name} in real projects", 
                           f"Review {skill_name} concepts", 
                           f"Apply {skill_name} in new contexts"]
            
            analysis = AISkillAnalysis(
                skill_name=skill_name,
                category='technical',  # Default category
                proficiency_level=proficiency,
                confidence=confidence,
                evidence=evidence,
                conversation_ids=event_conversation_ids,
                last_used=last_used,
                ai_insights=ai_insights,
                skill_relationships=skill_relationships,
                learning_path=learning_path
            )
            
            self.skill_analyses[skill_name] = analysis
            return analysis
            
        except Exception as e:
            print(f"Error analyzing skill progress: {e}")
            return None
            
    def analyze_project_progress(self, project_name: str, conversation_ids: List[str] = None) -> Optional[AIProjectAnalysis]:
        """Analyze progress for a specific project."""
        try:
            # Get project-related events
            project_events = []
            for event in self.progress_events:
                if project_name.lower() in event.description.lower():
                    if not conversation_ids or event.conversation_id in conversation_ids:
                        project_events.append(event)
                        
            if not project_events:
                return None
                
            # Calculate complexity level based on XP earned
            total_project_xp = sum(event.xp_amount for event in project_events)
            if total_project_xp < 50:
                complexity = 'simple'
            elif total_project_xp < 200:
                complexity = 'moderate'
            elif total_project_xp < 500:
                complexity = 'complex'
            else:
                complexity = 'enterprise'
                
            # Calculate impact score
            impact_score = min(total_project_xp / 1000.0, 1.0)  # Normalize to 0-1
            
            # Estimate team size and role (placeholder)
            team_size = 1  # Default to solo
            role = "Developer"  # Default role
            
            # Calculate duration
            if len(project_events) > 1:
                start_time = min(event.timestamp for event in project_events)
                end_time = max(event.timestamp for event in project_events)
                duration_days = (end_time - start_time).days
            else:
                duration_days = 1
                
            # Get conversation IDs
            event_conversation_ids = list(set(event.conversation_id for event in project_events))
            
            # Create AI insights
            ai_insights = {
                'total_project_xp': total_project_xp,
                'event_count': len(project_events),
                'duration_days': duration_days,
                'complexity_factors': ['xp_earned', 'event_frequency']
            }
            
            # Get achievements (placeholder)
            achievements = []
            
            # Determine technologies (placeholder)
            technologies = []
            
            analysis = AIProjectAnalysis(
                project_name=project_name,
                description=f"Project involving {project_name}",
                technologies=technologies,
                complexity_level=complexity,
                impact_score=impact_score,
                team_size=team_size,
                role=role,
                duration_days=duration_days,
                conversation_ids=event_conversation_ids,
                ai_insights=ai_insights,
                achievements=achievements
            )
            
            self.project_analyses[project_name] = analysis
            return analysis
            
        except Exception as e:
            print(f"Error analyzing project progress: {e}")
            return None
            
    def save_progress_data(self, file_path: str = None) -> bool:
        """Save progress data to file."""
        try:
            if file_path is None:
                file_path = self.progress_file
                
            data = {
                'progress_events': [event.__dict__ for event in self.progress_events],
                'skill_analyses': {name: analysis.__dict__ for name, analysis in self.skill_analyses.items()},
                'project_analyses': {name: analysis.__dict__ for name, analysis in self.project_analyses.items()},
                'last_updated': datetime.now().isoformat()
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
            
        except Exception as e:
            print(f"Error saving progress data: {e}")
            return False
            
    def load_progress_data(self, file_path: str = None) -> bool:
        """Load progress data from file."""
        try:
            if file_path is None:
                file_path = self.progress_file
                
            if not os.path.exists(file_path):
                return False
                
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Reconstruct progress events
            self.progress_events = []
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
                
            # Reconstruct skill analyses
            self.skill_analyses = {}
            for name, analysis_data in data.get('skill_analyses', {}).items():
                analysis = AISkillAnalysis(
                    skill_name=analysis_data['skill_name'],
                    category=analysis_data['category'],
                    proficiency_level=analysis_data['proficiency_level'],
                    confidence=analysis_data['confidence'],
                    evidence=analysis_data['evidence'],
                    conversation_ids=analysis_data['conversation_ids'],
                    last_used=datetime.fromisoformat(analysis_data['last_used']),
                    ai_insights=analysis_data['ai_insights'],
                    skill_relationships=analysis_data['skill_relationships'],
                    learning_path=analysis_data['learning_path']
                )
                self.skill_analyses[name] = analysis
                
            # Reconstruct project analyses
            self.project_analyses = {}
            for name, analysis_data in data.get('project_analyses', {}).items():
                analysis = AIProjectAnalysis(
                    project_name=analysis_data['project_name'],
                    description=analysis_data['description'],
                    technologies=analysis_data['technologies'],
                    complexity_level=analysis_data['complexity_level'],
                    impact_score=analysis_data['impact_score'],
                    team_size=analysis_data['team_size'],
                    role=analysis_data['role'],
                    duration_days=analysis_data['duration_days'],
                    conversation_ids=analysis_data['conversation_ids'],
                    ai_insights=analysis_data['ai_insights'],
                    achievements=analysis_data['achievements']
                )
                self.project_analyses[name] = analysis
                
            return True
            
        except Exception as e:
            print(f"Error loading progress data: {e}")
            return False
            
    def get_skill_analysis(self, skill_name: str) -> Optional[AISkillAnalysis]:
        """Get skill analysis for a specific skill."""
        return self.skill_analyses.get(skill_name)
        
    def get_project_analysis(self, project_name: str) -> Optional[AIProjectAnalysis]:
        """Get project analysis for a specific project."""
        return self.project_analyses.get(project_name)
        
    def get_all_skill_analyses(self) -> Dict[str, AISkillAnalysis]:
        """Get all skill analyses."""
        return self.skill_analyses.copy()
        
    def get_all_project_analyses(self) -> Dict[str, AIProjectAnalysis]:
        """Get all project analyses."""
        return self.project_analyses.copy() 