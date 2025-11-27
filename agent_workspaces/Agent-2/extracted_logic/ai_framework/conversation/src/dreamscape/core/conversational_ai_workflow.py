#!/usr/bin/env python3
"""
Conversational AI Workflow for Dreamscape
=========================================

This module provides a conversational AI workflow that can "speak" to your work
and provide context-aware assistance based on conversation history and work patterns.

Features:
- Context-aware AI responses based on conversation history
- Work pattern analysis and workflow suggestions
- Session management for long conversations
- Integration with existing Dreamscape systems
- Rich context from real and synthetic conversations
"""

import sys
import json
import logging
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import random
from jinja2 import Template, Environment, FileSystemLoader
import types

# Configure logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("conversational_ai")

class ConversationalAIWorkflow:
    """Conversational AI workflow that understands work context and provides assistance."""
    
    def __init__(self, templates_dir: str = "templates", context_dataset_path: str = "data/rich_context_dataset/rich_context_dataset.json"):
        self.templates_dir = Path(templates_dir)
        self.context_dataset_path = Path(context_dataset_path)
        self.env = Environment(loader=FileSystemLoader(str(self.templates_dir)))
        
        # Load rich context dataset
        self.rich_context = self._load_rich_context()
        
        # Session state
        self.current_session = None
        self.session_history = []
        self.work_patterns = {}
        
        logger.info("🤖 Conversational AI Workflow initialized")
        logger.info(f"📊 Loaded {len(self.rich_context.get('conversations', []))} conversations for context")
    
    def _load_rich_context(self) -> Dict[str, Any]:
        """Load the rich context dataset."""
        try:
            if self.context_dataset_path.exists():
                with open(self.context_dataset_path, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
                logger.info(f"✅ Loaded rich context dataset: {context_data.get('metadata', {}).get('total_conversations', 0)} conversations")
                return context_data
            else:
                logger.warning(f"⚠️ Rich context dataset not found at {self.context_dataset_path}")
                return {"conversations": [], "metadata": {}}
        except Exception as e:
            logger.error(f"❌ Failed to load rich context dataset: {e}")
            return {"conversations": [], "metadata": {}}
    
    def start_session(self, user_context: str = "", session_id: str = None) -> Dict[str, Any]:
        """Start a new conversational session."""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Load session initialization template
        template = self.env.get_template("session_init.j2")
        
        # Get relevant context from rich dataset
        relevant_context = self._get_relevant_context(user_context)
        
        # Analyze work patterns for session context
        work_analysis = self.analyze_work_patterns([])  # Empty at session start
        if not work_analysis or 'patterns' not in work_analysis:
            work_analysis = types.SimpleNamespace(patterns={})
        else:
            work_analysis = types.SimpleNamespace(**work_analysis)
        
        # Generate session initialization
        session_init = template.render(
            session_id=session_id,
            user_context=user_context,
            relevant_context=relevant_context,
            timestamp=datetime.now().isoformat(),
            work_analysis=work_analysis,
            session_context=None
        )
        
        # Create session state
        self.current_session = {
            'id': session_id,
            'started_at': datetime.now().isoformat(),
            'user_context': user_context,
            'conversation_history': [],
            'work_patterns': {},
            'context_summary': relevant_context
        }
        
        self.session_history.append(self.current_session)
        
        logger.info(f"🚀 Started new session: {session_id}")
        
        return {
            'session_id': session_id,
            'initialization': session_init,
            'context_summary': relevant_context
        }
    
    def _get_relevant_context(self, user_context: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant context from the rich dataset based on user context."""
        if not user_context or not self.rich_context.get('conversations'):
            return []
        
        # Simple keyword matching for relevance
        user_words = set(user_context.lower().split())
        relevant_conversations = []
        
        for conv in self.rich_context['conversations']:
            title = conv.get('title', '').lower()
            content = conv.get('content', '').lower()
            tags = conv.get('tags', '').lower()
            
            # Calculate relevance score
            relevance_score = 0
            for word in user_words:
                if word in title:
                    relevance_score += 3
                if word in content:
                    relevance_score += 1
                if word in tags:
                    relevance_score += 2
            
            if relevance_score > 0:
                relevant_conversations.append({
                    'conversation': conv,
                    'relevance_score': relevance_score
                })
        
        # Sort by relevance and return top matches
        relevant_conversations.sort(key=lambda x: x['relevance_score'], reverse=True)
        return [item['conversation'] for item in relevant_conversations[:limit]]
    
    def analyze_work_patterns(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze work patterns from conversation history."""
        if not conversation_history:
            return {}
        
        # Load work analysis template
        template = self.env.get_template("work_analysis.j2")
        
        # Extract patterns
        patterns = {
            'topics': {},
            'technologies': {},
            'challenges': {},
            'solutions': {},
            'time_patterns': {},
            'complexity_levels': []
        }
        
        # Analyze each conversation
        for conv in conversation_history:
            content = conv.get('content', '').lower()
            
            # Topic analysis
            for topic in ['api', 'database', 'frontend', 'backend', 'ml', 'ai', 'testing', 'deployment']:
                if topic in content:
                    patterns['topics'][topic] = patterns['topics'].get(topic, 0) + 1
            
            # Technology analysis
            for tech in ['python', 'javascript', 'sqlite', 'postgresql', 'docker', 'kubernetes', 'react', 'vue']:
                if tech in content:
                    patterns['technologies'][tech] = patterns['technologies'].get(tech, 0) + 1
            
            # Challenge analysis
            for challenge in ['error', 'bug', 'issue', 'problem', 'difficulty', 'complexity']:
                if challenge in content:
                    patterns['challenges'][challenge] = patterns['challenges'].get(challenge, 0) + 1
        
        # Generate analysis
        analysis = template.render(
            patterns=patterns,
            total_conversations=len(conversation_history),
            analysis_timestamp=datetime.now().isoformat()
        )
        
        return {
            'patterns': patterns,
            'analysis': analysis,
            'summary': self._generate_pattern_summary(patterns)
        }
    
    def analyze_work_patterns_from_question(self, question: str) -> Dict[str, Any]:
        """Analyze work patterns based on a question and current session context."""
        # Use current session conversation history if available
        conversation_history = []
        if self.current_session:
            conversation_history = self.current_session.get('conversation_history', [])
        
        # If no conversation history, analyze from rich context dataset
        if not conversation_history and self.rich_context.get('conversations'):
            # Convert rich context conversations to conversation history format
            for conv in self.rich_context['conversations'][:10]:  # Use first 10 conversations
                conversation_history.append({
                    'content': conv.get('content', ''),
                    'role': 'user',
                    'timestamp': conv.get('timestamp', '')
                })
        
        # Analyze patterns from available data
        patterns = self.analyze_work_patterns(conversation_history)
        
        # Add question-specific analysis
        if question:
            question_lower = question.lower()
            
            # Add question context to patterns
            if 'improve' in question_lower or 'optimize' in question_lower:
                patterns['patterns']['focus_areas'] = ['optimization', 'efficiency', 'performance']
            elif 'error' in question_lower or 'bug' in question_lower:
                patterns['patterns']['focus_areas'] = ['debugging', 'troubleshooting', 'error_handling']
            elif 'workflow' in question_lower:
                patterns['patterns']['focus_areas'] = ['process_improvement', 'automation', 'efficiency']
        
        return patterns
    
    def _generate_pattern_summary(self, patterns: Dict[str, Any]) -> str:
        """Generate a summary of work patterns."""
        summary_parts = []
        
        if patterns.get('topics'):
            top_topics = sorted(patterns['topics'].items(), key=lambda x: x[1], reverse=True)[:3]
            summary_parts.append(f"Primary focus areas: {', '.join([topic for topic, _ in top_topics])}")
        
        if patterns.get('technologies'):
            top_tech = sorted(patterns['technologies'].items(), key=lambda x: x[1], reverse=True)[:3]
            summary_parts.append(f"Key technologies: {', '.join([tech for tech, _ in top_tech])}")
        
        if patterns.get('challenges'):
            top_challenges = sorted(patterns['challenges'].items(), key=lambda x: x[1], reverse=True)[:3]
            summary_parts.append(f"Common challenges: {', '.join([challenge for challenge, _ in top_challenges])}")
        
        return "; ".join(summary_parts) if summary_parts else "No clear patterns detected"
    
    def generate_workflow_suggestions(self, user_query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate workflow suggestions based on user query and context."""
        # Load workflow suggestions template
        template = self.env.get_template("workflow_suggestions.j2")
        
        # Get relevant context
        relevant_context = self._get_relevant_context(user_query, limit=3)
        
        # Generate suggestions based on query type
        suggestions = []
        
        # Analyze query type
        query_lower = user_query.lower()
        
        if any(word in query_lower for word in ['error', 'bug', 'issue', 'problem']):
            suggestions.append({
                'type': 'troubleshooting',
                'title': 'Debugging Workflow',
                'description': 'Systematic approach to identify and resolve issues',
                'steps': [
                    'Check error logs and stack traces',
                    'Reproduce the issue in isolation',
                    'Identify root cause through debugging',
                    'Implement fix with proper testing',
                    'Document the solution for future reference'
                ]
            })
        
        if any(word in query_lower for word in ['optimize', 'performance', 'speed', 'efficiency']):
            suggestions.append({
                'type': 'optimization',
                'title': 'Performance Optimization Workflow',
                'description': 'Methodical approach to improve system performance',
                'steps': [
                    'Profile and identify bottlenecks',
                    'Analyze resource usage patterns',
                    'Implement targeted optimizations',
                    'Measure performance improvements',
                    'Monitor for regressions'
                ]
            })
        
        if any(word in query_lower for word in ['architecture', 'design', 'structure']):
            suggestions.append({
                'type': 'architecture',
                'title': 'System Design Workflow',
                'description': 'Comprehensive approach to system architecture',
                'steps': [
                    'Define requirements and constraints',
                    'Create high-level architecture diagrams',
                    'Design component interfaces',
                    'Plan data flow and integration',
                    'Document design decisions'
                ]
            })
        
        if any(word in query_lower for word in ['test', 'testing', 'quality']):
            suggestions.append({
                'type': 'testing',
                'title': 'Testing Strategy Workflow',
                'description': 'Comprehensive testing approach',
                'steps': [
                    'Define test requirements and scope',
                    'Create unit tests for core functionality',
                    'Implement integration tests',
                    'Set up automated testing pipeline',
                    'Monitor test coverage and quality metrics'
                ]
            })
        
        # Add generic suggestion if no specific type detected
        if not suggestions:
            suggestions.append({
                'type': 'general',
                'title': 'General Development Workflow',
                'description': 'Standard development process',
                'steps': [
                    'Analyze requirements and constraints',
                    'Plan implementation approach',
                    'Implement core functionality',
                    'Add error handling and validation',
                    'Test thoroughly and document'
                ]
            })
        
        # Use context or default work_analysis
        if context and 'patterns' in context:
            work_analysis = types.SimpleNamespace(**context)
        else:
            work_analysis = types.SimpleNamespace(patterns={})
        
        # Generate suggestions using template
        suggestions_text = template.render(
            user_query=user_query,
            suggestions=suggestions,
            relevant_context=relevant_context,
            timestamp=datetime.now().isoformat(),
            work_analysis=work_analysis,
            session_context=self.current_session,
            suggestions_obj={'context_used': relevant_context}
        )
        
        return {
            'suggestions': suggestions,
            'formatted_suggestions': suggestions_text,
            'context_used': relevant_context
        }
    
    def process_user_message(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """Process a user message and generate a context-aware response."""
        if not self.current_session or (session_id and self.current_session['id'] != session_id):
            # Start new session if needed
            self.start_session(message, session_id)
        
        # Add message to conversation history
        self.current_session['conversation_history'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Analyze work patterns
        work_analysis = self.analyze_work_patterns(self.current_session['conversation_history'])
        
        # Generate workflow suggestions
        suggestions = self.generate_workflow_suggestions(message, work_analysis)
        
        # Generate context-aware response
        response = self._generate_context_aware_response(message, work_analysis, suggestions)
        
        # Add response to conversation history
        self.current_session['conversation_history'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update work patterns
        self.current_session['work_patterns'] = work_analysis['patterns']
        
        return {
            'response': response,
            'session_id': self.current_session['id'],
            'work_analysis': work_analysis,
            'suggestions': suggestions,
            'context_used': suggestions['context_used']
        }
    
    def _generate_context_aware_response(self, message: str, work_analysis: Dict[str, Any], suggestions: Dict[str, Any]) -> str:
        """Generate a context-aware response based on the message and analysis."""
        # Load conversational workflow template
        template = self.env.get_template("conversational_workflow.j2")
        
        # Generate response using template
        response = template.render(
            user_message=message,
            work_analysis=work_analysis,
            suggestions=suggestions,
            session_context=self.current_session,
            timestamp=datetime.now().isoformat()
        )
        
        return response
    
    def save_session_summary(self, session_id: str = None) -> Dict[str, Any]:
        """Save a summary of the current session."""
        if not self.current_session:
            return {'error': 'No active session'}
        
        if session_id and self.current_session['id'] != session_id:
            return {'error': 'Session ID mismatch'}
        
        # Create session summary
        summary = {
            'session_id': self.current_session['id'],
            'started_at': self.current_session['started_at'],
            'ended_at': datetime.now().isoformat(),
            'total_messages': len(self.current_session['conversation_history']),
            'user_context': self.current_session['user_context'],
            'work_patterns': self.current_session['work_patterns'],
            'conversation_summary': self._summarize_conversation(self.current_session['conversation_history'])
        }
        
        # Save to file
        summary_file = Path(f"data/session_summaries/{self.current_session['id']}_summary.json")
        summary_file.parent.mkdir(exist_ok=True)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved session summary: {summary_file}")
        
        return {
            'summary': summary,
            'file_path': str(summary_file)
        }
    
    def _summarize_conversation(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Create a summary of the conversation."""
        if not conversation_history:
            return "No conversation history"
        
        user_messages = [msg['content'] for msg in conversation_history if msg['role'] == 'user']
        assistant_messages = [msg['content'] for msg in conversation_history if msg['role'] == 'assistant']
        
        summary = f"Conversation with {len(user_messages)} user messages and {len(assistant_messages)} assistant responses. "
        
        if user_messages:
            # Extract key topics from user messages
            all_user_text = ' '.join(user_messages).lower()
            topics = []
            
            for topic in ['api', 'database', 'frontend', 'backend', 'ml', 'ai', 'testing', 'deployment', 'optimization', 'architecture']:
                if topic in all_user_text:
                    topics.append(topic)
            
            if topics:
                summary += f"Key topics discussed: {', '.join(topics)}. "
        
        summary += f"Session duration: {self._calculate_session_duration()}"
        
        return summary
    
    def _calculate_session_duration(self) -> str:
        """Calculate the duration of the current session."""
        if not self.current_session:
            return "Unknown"
        
        start_time = datetime.fromisoformat(self.current_session['started_at'])
        end_time = datetime.now()
        duration = end_time - start_time
        
        if duration.total_seconds() < 60:
            return f"{int(duration.total_seconds())} seconds"
        elif duration.total_seconds() < 3600:
            return f"{int(duration.total_seconds() // 60)} minutes"
        else:
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            return f"{hours} hours {minutes} minutes"
    
    def get_session_stats(self, session_id: str = None) -> Dict[str, Any]:
        """Get statistics for the current or specified session."""
        if not self.current_session:
            return {'error': 'No active session'}
        
        if session_id and self.current_session['id'] != session_id:
            return {'error': 'Session ID mismatch'}
        
        conversation_history = self.current_session['conversation_history']
        
        stats = {
            'session_id': self.current_session['id'],
            'total_messages': len(conversation_history),
            'user_messages': len([msg for msg in conversation_history if msg['role'] == 'user']),
            'assistant_messages': len([msg for msg in conversation_history if msg['role'] == 'assistant']),
            'session_duration': self._calculate_session_duration(),
            'work_patterns': self.current_session['work_patterns'],
            'context_summary': self.current_session['context_summary']
        }
        
        return stats

def main():
    """Demo function to showcase the conversational AI workflow."""
    print("🤖 Conversational AI Workflow Demo")
    print("=" * 50)
    
    try:
        # Initialize workflow
        workflow = ConversationalAIWorkflow()
        
        # Start session
        session = workflow.start_session("I'm working on a Python API that needs to handle concurrent database operations")
        print(f"🚀 Session started: {session['session_id']}")
        print(f"📊 Context loaded: {len(session['context_summary'])} relevant conversations")
        
        # Process some example messages
        example_messages = [
            "I'm getting database locking errors when multiple users access the API simultaneously",
            "How can I optimize the database queries for better performance?",
            "What's the best way to structure the API endpoints for scalability?",
            "I need help with testing the concurrent operations"
        ]
        
        for i, message in enumerate(example_messages, 1):
            print(f"\n💬 Message {i}: {message}")
            
            response = workflow.process_user_message(message)
            
            print(f"🤖 Response: {response['response'][:200]}...")
            print(f"📈 Work patterns detected: {len(response['work_analysis']['patterns'])}")
            print(f"💡 Suggestions generated: {len(response['suggestions']['suggestions'])}")
        
        # Get session stats
        stats = workflow.get_session_stats()
        print(f"\n📊 Session Statistics:")
        print(f"   Total messages: {stats['total_messages']}")
        print(f"   Session duration: {stats['session_duration']}")
        print(f"   Work patterns: {len(stats['work_patterns'])}")
        
        # Save session summary
        summary = workflow.save_session_summary()
        print(f"\n💾 Session summary saved: {summary['file_path']}")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 