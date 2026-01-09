#!/usr/bin/env python3
"""
Memory Episode Generator
=======================

Generates MMORPG episodes from conversation corpus for weaponization.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class EpisodeGenerator:
    """Generates MMORPG episodes from conversation data."""
    
    def __init__(self):
        """Initialize the episode generator."""
        pass
    
    def create_episodes(self, conversations: List[Dict]) -> List[Dict]:
        """
        Create MMORPG episodes from conversations.
        
        Args:
            conversations: List of conversation dictionaries
            
        Returns:
            List of episode dictionaries
        """
        episodes = []
        
        for conv in conversations:
            episode = self._convert_to_episode(conv)
            if episode:
                episodes.append(episode)
        
        logger.info(f"Generated {len(episodes)} MMORPG episodes")
        return episodes
    
    def _convert_to_episode(self, conv: Dict) -> Optional[Dict]:
        """
        Convert a conversation to an MMORPG episode.
        
        Args:
            conv: Conversation dictionary
            
        Returns:
            Episode dictionary or None if conversion fails
        """
        try:
            messages = conv.get('messages', [])
            if not messages:
                return None
            
            # Extract key information
            title = conv.get('title', 'Unknown Quest')
            timestamp = conv.get('timestamp', datetime.now().isoformat())
            
            # Determine episode type
            episode_type = self._determine_episode_type(conv)
            
            # Extract quest objectives
            objectives = self._extract_objectives(messages)
            
            # Extract rewards
            rewards = self._extract_rewards(messages)
            
            # Create episode structure
            episode = {
                'id': f"episode_{conv.get('id', 'unknown')}",
                'title': title,
                'type': episode_type,
                'difficulty': self._assess_difficulty(conv),
                'objectives': objectives,
                'rewards': rewards,
                'conversation_id': conv.get('id'),
                'timestamp': timestamp,
                'duration': self._estimate_duration(messages),
                'success_rate': self._assess_success_rate(conv),
                'skills_required': self._extract_skills_required(conv),
                'quest_giver': 'User',
                'quest_taker': 'AI Assistant'
            }
            
            return episode
            
        except Exception as e:
            logger.error(f"Failed to convert conversation to episode: {e}")
            return None
    
    def _determine_episode_type(self, conv: Dict) -> str:
        """Determine the type of episode based on conversation content."""
        content = ' '.join([msg.get('content', '') for msg in conv.get('messages', [])])
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['error', 'bug', 'fix', 'problem', 'debug']):
            return 'bug_hunt'
        elif any(word in content_lower for word in ['create', 'build', 'make', 'implement']):
            return 'crafting'
        elif any(word in content_lower for word in ['learn', 'tutorial', 'guide', 'explain']):
            return 'training'
        elif any(word in content_lower for word in ['optimize', 'improve', 'enhance']):
            return 'optimization'
        elif any(word in content_lower for word in ['design', 'architecture', 'plan']):
            return 'planning'
        else:
            return 'general'
    
    def _extract_objectives(self, messages: List[Dict]) -> List[str]:
        """Extract quest objectives from messages."""
        objectives = []
        
        for msg in messages:
            content = msg.get('content', '')
            if msg.get('role') == 'user':
                # Look for objective-like statements
                if any(word in content.lower() for word in ['need', 'want', 'help', 'create', 'fix']):
                    objectives.append(content[:200] + '...' if len(content) > 200 else content)
        
        return objectives[:3]  # Limit to 3 objectives
    
    def _extract_rewards(self, messages: List[Dict]) -> Dict[str, Any]:
        """Extract quest rewards from messages."""
        rewards = {
            'experience': 0,
            'gold': 0,
            'items': [],
            'skills': []
        }
        
        # Analyze conversation success and length
        total_messages = len(messages)
        if total_messages > 10:
            rewards['experience'] = 100
        elif total_messages > 5:
            rewards['experience'] = 50
        else:
            rewards['experience'] = 25
        
        # Add gold based on complexity
        rewards['gold'] = rewards['experience'] * 2
        
        # Add skills based on content
        content = ' '.join([msg.get('content', '') for msg in messages])
        content_lower = content.lower()
        
        if 'python' in content_lower:
            rewards['skills'].append('Python Programming')
        if 'javascript' in content_lower:
            rewards['skills'].append('JavaScript Programming')
        if 'api' in content_lower:
            rewards['skills'].append('API Integration')
        if 'database' in content_lower:
            rewards['skills'].append('Database Management')
        if 'debug' in content_lower:
            rewards['skills'].append('Debugging')
        
        return rewards
    
    def _assess_difficulty(self, conv: Dict) -> str:
        """Assess the difficulty of the episode."""
        messages = conv.get('messages', [])
        total_length = sum(len(msg.get('content', '')) for msg in messages)
        
        if total_length > 5000:
            return 'hard'
        elif total_length > 2000:
            return 'medium'
        else:
            return 'easy'
    
    def _estimate_duration(self, messages: List[Dict]) -> int:
        """Estimate episode duration in minutes."""
        # Rough estimate: 1 minute per message
        return len(messages)
    
    def _assess_success_rate(self, conv: Dict) -> float:
        """Assess the success rate of the episode."""
        messages = conv.get('messages', [])
        if not messages:
            return 0.0
        
        # Simple heuristic: more assistant messages = higher success
        assistant_messages = sum(1 for msg in messages if msg.get('role') == 'assistant')
        total_messages = len(messages)
        
        if total_messages == 0:
            return 0.0
        
        success_rate = assistant_messages / total_messages
        return min(1.0, success_rate * 1.5)  # Boost success rate
    
    def _extract_skills_required(self, conv: Dict) -> List[str]:
        """Extract skills required for the episode."""
        skills = []
        content = ' '.join([msg.get('content', '') for msg in conv.get('messages', [])])
        content_lower = content.lower()
        
        # Programming languages
        if 'python' in content_lower:
            skills.append('Python')
        if 'javascript' in content_lower:
            skills.append('JavaScript')
        if 'java' in content_lower:
            skills.append('Java')
        if 'c++' in content_lower or 'cpp' in content_lower:
            skills.append('C++')
        
        # Technologies
        if 'api' in content_lower:
            skills.append('API Development')
        if 'database' in content_lower or 'sql' in content_lower:
            skills.append('Database Design')
        if 'web' in content_lower or 'html' in content_lower:
            skills.append('Web Development')
        if 'ai' in content_lower or 'machine learning' in content_lower:
            skills.append('AI/ML')
        
        return list(set(skills))  # Remove duplicates
    
    def generate_episode_summary(self, episodes: List[Dict]) -> Dict[str, Any]:
        """
        Generate summary statistics for episodes.
        
        Args:
            episodes: List of episode dictionaries
            
        Returns:
            Summary statistics
        """
        if not episodes:
            return {}
        
        total_episodes = len(episodes)
        total_experience = sum(ep.get('rewards', {}).get('experience', 0) for ep in episodes)
        total_gold = sum(ep.get('rewards', {}).get('gold', 0) for ep in episodes)
        
        # Episode types
        type_counts = {}
        for ep in episodes:
            ep_type = ep.get('type', 'unknown')
            type_counts[ep_type] = type_counts.get(ep_type, 0) + 1
        
        # Difficulty distribution
        difficulty_counts = {}
        for ep in episodes:
            difficulty = ep.get('difficulty', 'unknown')
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        # Average success rate
        avg_success_rate = sum(ep.get('success_rate', 0) for ep in episodes) / total_episodes
        
        return {
            'total_episodes': total_episodes,
            'total_experience': total_experience,
            'total_gold': total_gold,
            'type_distribution': type_counts,
            'difficulty_distribution': difficulty_counts,
            'average_success_rate': round(avg_success_rate, 2),
            'average_duration': sum(ep.get('duration', 0) for ep in episodes) / total_episodes
        } 