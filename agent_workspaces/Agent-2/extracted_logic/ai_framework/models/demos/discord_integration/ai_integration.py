"""
AI Integration for Discord Bot
AI-powered response generation and conversation analysis
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

# Dream.OS imports
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# EDIT START: Consolidate memory imports to use memory_system (core consolidation)
from dreamscape.core.memory_system import MemoryManager  # Updated for consolidated memory system
# EDIT END
from src.dreamscape.core.enhanced_progress_system import EnhancedProgressSystem
from src.dreamscape.core.skill_manager import SkillManager

class AIIntegration:
    """AI integration for Discord bot responses"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.memory_manager = None
        self.enhanced_progress_system = None
        self.skill_manager = None
        
        # Response templates
        self.response_templates = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What would you like to discuss?",
                "Greetings! I'm here to assist you.",
                "Hey! Ready to help with anything you need."
            ],
            'farewell': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! Feel free to come back anytime.",
                "Farewell! Looking forward to our next chat."
            ],
            'thanks': [
                "You're welcome! Happy to help.",
                "No problem at all!",
                "Glad I could assist you!",
                "Anytime! That's what I'm here for."
            ],
            'question': [
                "That's an interesting question. Let me think about that...",
                "I'd be happy to help with that!",
                "Great question! Here's what I can tell you...",
                "Let me provide some information on that..."
            ],
            'progress': [
                "That's great progress! Keep up the good work!",
                "Excellent! You're making real strides forward.",
                "Impressive! Your hard work is paying off.",
                "Fantastic! You're on the right track."
            ],
            'skill_detected': [
                "I noticed you mentioned {skill}. That's a valuable skill!",
                "Great to see you working with {skill}!",
                "Your knowledge of {skill} is impressive!",
                "Keep developing your {skill} skills!"
            ],
            'encouragement': [
                "You've got this! Keep pushing forward.",
                "Every step counts toward your goals.",
                "You're doing great! Don't give up.",
                "Your persistence will pay off!"
            ],
            'error': [
                "I'm sorry, I didn't quite understand that. Could you rephrase?",
                "Let me try to help, but I need a bit more clarity.",
                "I'm having trouble processing that. Can you explain differently?",
                "Could you provide more context so I can better assist you?"
            ]
        }
        
        # Conversation context
        self.conversation_contexts = {}
        self.context_ttl = timedelta(hours=1)
        
    async def initialize(self):
        """Initialize Dream.OS components"""
        try:
            self.memory_manager = MemoryManager()
            self.enhanced_progress_system = EnhancedProgressSystem()
            self.skill_manager = SkillManager()
            logging.info("AI Integration initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize AI Integration: {e}")
    
    async def generate_response(self, message_data: Dict, analysis: Dict) -> Dict:
        """Generate AI response based on message and analysis"""
        try:
            # Get conversation context
            user_id = message_data['user_id']
            context = await self._get_conversation_context(user_id)
            
            # Determine response type
            response_type = await self._determine_response_type(analysis)
            
            # Generate response content
            response_content = await self._generate_response_content(
                message_data, analysis, context, response_type
            )
            
            # Update context
            await self._update_conversation_context(user_id, message_data, response_content)
            
            # Process for Dream.OS features
            await self._process_for_dreamos(message_data, analysis, response_content)
            
            return {
                'content': response_content,
                'type': response_type,
                'confidence': analysis.get('intent', {}).get('confidence', 0.5),
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id
            }
            
        except Exception as e:
            logging.error(f"Error generating AI response: {e}")
            return {
                'content': "I'm sorry, I encountered an error. Please try again.",
                'type': 'error',
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat(),
                'user_id': message_data.get('user_id', 'unknown')
            }
    
    async def _get_conversation_context(self, user_id: str) -> List[Dict]:
        """Get conversation context for user"""
        if user_id in self.conversation_contexts:
            context_data = self.conversation_contexts[user_id]
            if datetime.now() - context_data['timestamp'] < self.context_ttl:
                return context_data['messages']
            else:
                del self.conversation_contexts[user_id]
        
        return []
    
    async def _determine_response_type(self, analysis: Dict) -> str:
        """Determine the type of response to generate"""
        intent = analysis.get('intent', {})
        primary_intent = intent.get('primary_intent', 'general')
        
        # Map intents to response types
        intent_mapping = {
            'greeting': 'greeting',
            'farewell': 'farewell',
            'thanks': 'thanks',
            'question': 'question',
            'command': 'command',
            'agreement': 'agreement',
            'disagreement': 'disagreement',
            'complaint': 'error',
            'suggestion': 'encouragement'
        }
        
        return intent_mapping.get(primary_intent, 'general')
    
    async def _generate_response_content(self, message_data: Dict, analysis: Dict, 
                                       context: List[Dict], response_type: str) -> str:
        """Generate the actual response content"""
        
        # Check for skill indicators
        skill_indicators = analysis.get('skill_indicators', [])
        if skill_indicators and response_type == 'general':
            skill = skill_indicators[0]['skill']
            template = random.choice(self.response_templates['skill_detected'])
            return template.format(skill=skill)
        
        # Check for progress indicators
        progress_indicators = analysis.get('progress_indicators', [])
        if progress_indicators and response_type == 'general':
            return random.choice(self.response_templates['progress'])
        
        # Use template for response type
        if response_type in self.response_templates:
            return random.choice(self.response_templates[response_type])
        
        # Generate contextual response
        return await self._generate_contextual_response(message_data, analysis, context)
    
    async def _generate_contextual_response(self, message_data: Dict, analysis: Dict, 
                                          context: List[Dict]) -> str:
        """Generate contextual response based on conversation history"""
        
        content = message_data.get('content', '').lower()
        
        # Check for specific topics
        topics = analysis.get('topics', [])
        if topics:
            topic = topics[0]
            if topic == 'programming':
                return "I see you're interested in programming! What language or framework are you working with?"
            elif topic == 'gaming':
                return "Gaming is a great way to develop problem-solving skills! What games do you enjoy?"
            elif topic == 'music':
                return "Music is wonderful! Are you a musician or just enjoy listening?"
            elif topic == 'technology':
                return "Technology is fascinating! What aspect interests you most?"
        
        # Check sentiment
        sentiment = analysis.get('sentiment', {})
        if sentiment.get('sentiment') == 'negative':
            return random.choice(self.response_templates['encouragement'])
        
        # Default response
        return "That's interesting! Tell me more about that."
    
    async def _update_conversation_context(self, user_id: str, message_data: Dict, response_content: str):
        """Update conversation context for user"""
        if user_id not in self.conversation_contexts:
            self.conversation_contexts[user_id] = {
                'messages': [],
                'timestamp': datetime.now()
            }
        
        # Add user message
        self.conversation_contexts[user_id]['messages'].append({
            'role': 'user',
            'content': message_data.get('content', ''),
            'timestamp': message_data.get('timestamp', datetime.now().isoformat())
        })
        
        # Add bot response
        self.conversation_contexts[user_id]['messages'].append({
            'role': 'assistant',
            'content': response_content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent messages (last 20)
        if len(self.conversation_contexts[user_id]['messages']) > 20:
            self.conversation_contexts[user_id]['messages'] = self.conversation_contexts[user_id]['messages'][-20:]
        
        # Update timestamp
        self.conversation_contexts[user_id]['timestamp'] = datetime.now()
    
    async def _process_for_dreamos(self, message_data: Dict, analysis: Dict, response_content: str):
        """Process message and response for Dream.OS features"""
        try:
            # Store in memory manager
            if self.memory_manager:
                conversation_data = {
                    'user_id': message_data['user_id'],
                    'username': message_data.get('username', 'Unknown'),
                    'channel_id': message_data.get('channel_id'),
                    'channel_name': message_data.get('channel_name'),
                    'guild_id': message_data.get('guild_id'),
                    'guild_name': message_data.get('guild_name'),
                    'messages': [
                        {
                            'role': 'user',
                            'content': message_data.get('content', ''),
                            'timestamp': message_data.get('timestamp')
                        },
                        {
                            'role': 'assistant',
                            'content': response_content,
                            'timestamp': datetime.now().isoformat()
                        }
                    ],
                    'analysis': analysis
                }
                
                await self.memory_manager.store_conversation(conversation_data)
            
            # Process for skill detection
            if self.skill_manager and analysis.get('skill_indicators'):
                await self.skill_manager.analyze_conversation([message_data])
            
            # Process for progress tracking
            if self.enhanced_progress_system and analysis.get('progress_indicators'):
                await self.enhanced_progress_system.analyze_conversation([message_data])
                
        except Exception as e:
            logging.error(f"Error processing for Dream.OS: {e}")
    
    async def get_user_progress(self, user_id: str) -> Dict:
        """Get user progress from Dream.OS"""
        try:
            if self.enhanced_progress_system:
                return await self.enhanced_progress_system.get_user_progress(user_id)
            return {}
        except Exception as e:
            logging.error(f"Error getting user progress: {e}")
            return {}
    
    async def get_user_skills(self, user_id: str) -> List[Dict]:
        """Get user skills from Dream.OS"""
        try:
            if self.skill_manager:
                return await self.skill_manager.get_user_skills(user_id)
            return []
        except Exception as e:
            logging.error(f"Error getting user skills: {e}")
            return []
    
    async def generate_summary(self, user_id: str) -> str:
        """Generate conversation summary for user"""
        try:
            context = await self._get_conversation_context(user_id)
            if not context:
                return "No recent conversation history available."
            
            # Create summary
            user_messages = [msg for msg in context if msg['role'] == 'user']
            bot_messages = [msg for msg in context if msg['role'] == 'assistant']
            
            summary = f"Recent conversation summary:\n"
            summary += f"- {len(user_messages)} messages from you\n"
            summary += f"- {len(bot_messages)} responses from me\n"
            
            if user_messages:
                last_message = user_messages[-1]['content']
                if len(last_message) > 100:
                    last_message = last_message[:100] + "..."
                summary += f"- Last topic: {last_message}\n"
            
            return summary
            
        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            return "Unable to generate summary at this time."
    
    async def cleanup_old_contexts(self):
        """Clean up old conversation contexts"""
        cutoff = datetime.now() - self.context_ttl
        to_remove = []
        
        for user_id, context_data in self.conversation_contexts.items():
            if context_data['timestamp'] < cutoff:
                to_remove.append(user_id)
        
        for user_id in to_remove:
            del self.conversation_contexts[user_id]
        
        if to_remove:
            logging.info(f"Cleaned up {len(to_remove)} old conversation contexts")
    
    async def get_ai_stats(self) -> Dict:
        """Get AI integration statistics"""
        return {
            'active_contexts': len(self.conversation_contexts),
            'context_ttl_seconds': self.context_ttl.total_seconds(),
            'response_templates': len(self.response_templates),
            'memory_manager_available': self.memory_manager is not None,
            'progress_tracker_available': self.enhanced_progress_system is not None,
            'skill_manager_available': self.skill_manager is not None
        } 