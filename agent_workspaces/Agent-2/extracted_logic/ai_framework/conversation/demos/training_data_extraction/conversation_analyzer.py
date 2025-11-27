#!/usr/bin/env python3
"""
Training Data Extraction - Conversation Analyzer

This module analyzes conversations and extracts structured training data
for AI model training, including conversation patterns, intent recognition,
and response quality assessment.

Features:
- Conversation structure analysis
- Intent and entity extraction
- Response quality assessment
- Training data generation
- Export to multiple formats
"""

import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import sqlite3
from pathlib import Path
import random


class ConversationType(Enum):
    """Types of conversations"""
    Q_A = "question_answer"
    TUTORIAL = "tutorial"
    TROUBLESHOOTING = "troubleshooting"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    CASUAL = "casual"


class IntentType(Enum):
    """Types of user intents"""
    QUESTION = "question"
    REQUEST = "request"
    CLARIFICATION = "clarification"
    FEEDBACK = "feedback"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    GREETING = "greeting"
    FAREWELL = "farewell"


class ResponseQuality(Enum):
    """Response quality levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    INAPPROPRIATE = "inappropriate"


@dataclass
class Message:
    """Individual message in a conversation"""
    id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class Intent:
    """Extracted intent from a message"""
    intent_type: IntentType
    confidence: float
    entities: List[str]
    keywords: List[str]
    context: Dict[str, Any]


@dataclass
class ResponseAnalysis:
    """Analysis of an AI response"""
    quality: ResponseQuality
    relevance_score: float
    helpfulness_score: float
    clarity_score: float
    completeness_score: float
    issues: List[str]
    suggestions: List[str]


@dataclass
class ConversationTurn:
    """A turn in the conversation (user message + AI response)"""
    id: str
    user_message: Message
    ai_response: Message
    user_intent: Intent
    response_analysis: ResponseAnalysis
    context: Dict[str, Any]


@dataclass
class Conversation:
    """Complete conversation with analysis"""
    id: str
    title: str
    conversation_type: ConversationType
    messages: List[Message]
    turns: List[ConversationTurn]
    summary: str
    topics: List[str]
    difficulty_level: str
    created_at: datetime
    metadata: Dict[str, Any]


class ConversationAnalyzer:
    """Analyzes conversations and extracts training data"""
    
    def __init__(self, db_path: str = "conversation_analysis.db"):
        self.db_path = db_path
        self._init_database()
        self._load_analysis_patterns()
    
    def _init_database(self):
        """Initialize the analysis database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    conversation_type TEXT NOT NULL,
                    messages TEXT NOT NULL,
                    turns TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    topics TEXT NOT NULL,
                    difficulty_level TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS training_data (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    turn_id TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    quality_score REAL NOT NULL,
                    context TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id)
                )
            """)
            conn.commit()
    
    def _load_analysis_patterns(self):
        """Load patterns for intent recognition and analysis"""
        self.intent_patterns = {
            IntentType.QUESTION: [
                r'\b(what|how|why|when|where|who|which|can|could|would|will|do|does|did|is|are|was|were)\b',
                r'\?',
                r'\b(explain|describe|tell|show|help)\b'
            ],
            IntentType.REQUEST: [
                r'\b(please|can you|could you|would you|will you)\b',
                r'\b(create|make|build|generate|write|code|implement)\b',
                r'\b(need|want|require|looking for)\b'
            ],
            IntentType.CLARIFICATION: [
                r'\b(clarify|explain|elaborate|expand|detail|specify)\b',
                r'\b(what do you mean|not sure|confused|unclear)\b',
                r'\b(can you clarify|please explain|what does that mean)\b'
            ],
            IntentType.FEEDBACK: [
                r'\b(feedback|suggest|improve|better|good|bad|great|terrible)\b',
                r'\b(like|dislike|love|hate|prefer)\b',
                r'\b(works|doesn\'t work|helpful|useless)\b'
            ],
            IntentType.COMPLAINT: [
                r'\b(problem|issue|error|bug|broken|wrong|failed)\b',
                r'\b(not working|doesn\'t work|broken|faulty)\b',
                r'\b(annoying|frustrating|difficult|confusing)\b'
            ],
            IntentType.COMPLIMENT: [
                r'\b(thanks|thank you|appreciate|great job|excellent|amazing)\b',
                r'\b(perfect|brilliant|outstanding|fantastic|wonderful)\b',
                r'\b(helpful|useful|valuable|beneficial)\b'
            ],
            IntentType.GREETING: [
                r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
                r'\b(greetings|howdy|yo|sup)\b'
            ],
            IntentType.FAREWELL: [
                r'\b(goodbye|bye|see you|farewell|take care|until next time)\b',
                r'\b(thanks|thank you|appreciate it)\b'
            ]
        }
        
        self.quality_indicators = {
            ResponseQuality.EXCELLENT: {
                'keywords': ['comprehensive', 'detailed', 'thorough', 'complete', 'accurate'],
                'patterns': [r'\b\d+\s+words?\b', r'\b\d+\s+paragraphs?\b'],
                'min_length': 100,
                'max_length': 1000
            },
            ResponseQuality.GOOD: {
                'keywords': ['helpful', 'useful', 'relevant', 'appropriate', 'clear'],
                'patterns': [r'\b\d+\s+words?\b'],
                'min_length': 50,
                'max_length': 500
            },
            ResponseQuality.AVERAGE: {
                'keywords': ['basic', 'simple', 'general', 'standard'],
                'patterns': [],
                'min_length': 20,
                'max_length': 200
            },
            ResponseQuality.POOR: {
                'keywords': ['unclear', 'vague', 'confusing', 'incomplete'],
                'patterns': [],
                'min_length': 0,
                'max_length': 50
            },
            ResponseQuality.INAPPROPRIATE: {
                'keywords': ['offensive', 'inappropriate', 'unprofessional', 'rude'],
                'patterns': [],
                'min_length': 0,
                'max_length': 1000
            }
        }
    
    def analyze_conversation(self, messages: List[Dict[str, Any]], title: str = "") -> Conversation:
        """Analyze a conversation and extract structured data"""
        # Convert messages to Message objects
        conversation_messages = []
        for msg in messages:
            message = Message(
                id=str(uuid.uuid4()),
                role=msg.get('role', 'unknown'),
                content=msg.get('content', ''),
                timestamp=datetime.fromisoformat(msg.get('timestamp', datetime.now().isoformat())),
                metadata=msg.get('metadata', {})
            )
            conversation_messages.append(message)
        
        # Determine conversation type
        conversation_type = self._determine_conversation_type(conversation_messages)
        
        # Extract conversation turns
        turns = self._extract_conversation_turns(conversation_messages)
        
        # Generate summary
        summary = self._generate_conversation_summary(conversation_messages)
        
        # Extract topics
        topics = self._extract_conversation_topics(conversation_messages)
        
        # Determine difficulty level
        difficulty_level = self._determine_difficulty_level(conversation_messages)
        
        # Create conversation object
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=title or f"Conversation {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            conversation_type=conversation_type,
            messages=conversation_messages,
            turns=turns,
            summary=summary,
            topics=topics,
            difficulty_level=difficulty_level,
            created_at=datetime.now(),
            metadata={}
        )
        
        return conversation
    
    def _determine_conversation_type(self, messages: List[Message]) -> ConversationType:
        """Determine the type of conversation"""
        content = " ".join([msg.content.lower() for msg in messages])
        
        # Count keywords for each type
        type_scores = {
            ConversationType.Q_A: 0,
            ConversationType.TUTORIAL: 0,
            ConversationType.TROUBLESHOOTING: 0,
            ConversationType.CREATIVE: 0,
            ConversationType.ANALYTICAL: 0,
            ConversationType.CASUAL: 0
        }
        
        # Q&A indicators
        qa_keywords = ['question', 'answer', 'ask', 'respond', 'explain', 'what', 'how', 'why']
        type_scores[ConversationType.Q_A] = sum(content.count(word) for word in qa_keywords)
        
        # Tutorial indicators
        tutorial_keywords = ['tutorial', 'guide', 'step', 'instruction', 'learn', 'teach', 'example']
        type_scores[ConversationType.TUTORIAL] = sum(content.count(word) for word in tutorial_keywords)
        
        # Troubleshooting indicators
        trouble_keywords = ['problem', 'error', 'issue', 'fix', 'debug', 'troubleshoot', 'broken']
        type_scores[ConversationType.TROUBLESHOOTING] = sum(content.count(word) for word in trouble_keywords)
        
        # Creative indicators
        creative_keywords = ['create', 'design', 'build', 'make', 'generate', 'write', 'compose']
        type_scores[ConversationType.CREATIVE] = sum(content.count(word) for word in creative_keywords)
        
        # Analytical indicators
        analytical_keywords = ['analyze', 'compare', 'evaluate', 'assess', 'review', 'examine', 'study']
        type_scores[ConversationType.ANALYTICAL] = sum(content.count(word) for word in analytical_keywords)
        
        # Casual indicators
        casual_keywords = ['hello', 'hi', 'thanks', 'goodbye', 'nice', 'great', 'cool']
        type_scores[ConversationType.CASUAL] = sum(content.count(word) for word in casual_keywords)
        
        # Return the type with highest score
        return max(type_scores, key=type_scores.get)
    
    def _extract_conversation_turns(self, messages: List[Message]) -> List[ConversationTurn]:
        """Extract conversation turns (user message + AI response pairs)"""
        turns = []
        
        for i in range(0, len(messages) - 1, 2):
            if i + 1 < len(messages):
                user_message = messages[i]
                ai_response = messages[i + 1]
                
                # Ensure proper role assignment
                if user_message.role != "user" or ai_response.role != "assistant":
                    continue
                
                # Extract user intent
                user_intent = self._extract_intent(user_message.content)
                
                # Analyze AI response
                response_analysis = self._analyze_response(ai_response.content, user_message.content)
                
                # Create turn
                turn = ConversationTurn(
                    id=str(uuid.uuid4()),
                    user_message=user_message,
                    ai_response=ai_response,
                    user_intent=user_intent,
                    response_analysis=response_analysis,
                    context={}
                )
                
                turns.append(turn)
        
        return turns
    
    def _extract_intent(self, message_content: str) -> Intent:
        """Extract intent from a message"""
        content_lower = message_content.lower()
        
        # Find matching intents
        intent_scores = {}
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, content_lower)
                score += len(matches)
            intent_scores[intent_type] = score
        
        # Get the most likely intent
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(1.0, intent_scores[primary_intent] / 10.0)  # Normalize confidence
        else:
            primary_intent = IntentType.QUESTION  # Default
            confidence = 0.1
        
        # Extract entities (simple keyword extraction)
        entities = self._extract_entities(message_content)
        
        # Extract keywords
        keywords = self._extract_keywords(message_content)
        
        return Intent(
            intent_type=primary_intent,
            confidence=confidence,
            entities=entities,
            keywords=keywords,
            context={}
        )
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract entities from content (simplified)"""
        # Simple entity extraction - in a real system, this would use NER
        entities = []
        
        # Extract potential entities (capitalized words, numbers, etc.)
        words = content.split()
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w]', '', word)
            
            # Check for potential entities
            if (clean_word and len(clean_word) > 2 and 
                (clean_word[0].isupper() or clean_word.isdigit() or 
                 clean_word.lower() in ['python', 'javascript', 'html', 'css', 'sql', 'api'])):
                entities.append(clean_word)
        
        return list(set(entities))  # Remove duplicates
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content"""
        # Simple keyword extraction - in a real system, this would use TF-IDF or similar
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        words = re.findall(r'\b\w+\b', content.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return most common keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(10)]
    
    def _analyze_response(self, response_content: str, user_message: str) -> ResponseAnalysis:
        """Analyze the quality of an AI response"""
        content_lower = response_content.lower()
        user_lower = user_message.lower()
        
        # Calculate quality scores
        relevance_score = self._calculate_relevance_score(response_content, user_message)
        helpfulness_score = self._calculate_helpfulness_score(response_content)
        clarity_score = self._calculate_clarity_score(response_content)
        completeness_score = self._calculate_completeness_score(response_content)
        
        # Determine overall quality
        overall_score = (relevance_score + helpfulness_score + clarity_score + completeness_score) / 4
        
        if overall_score >= 0.8:
            quality = ResponseQuality.EXCELLENT
        elif overall_score >= 0.6:
            quality = ResponseQuality.GOOD
        elif overall_score >= 0.4:
            quality = ResponseQuality.AVERAGE
        elif overall_score >= 0.2:
            quality = ResponseQuality.POOR
        else:
            quality = ResponseQuality.INAPPROPRIATE
        
        # Identify issues
        issues = self._identify_response_issues(response_content)
        
        # Generate suggestions
        suggestions = self._generate_improvement_suggestions(response_content, issues)
        
        return ResponseAnalysis(
            quality=quality,
            relevance_score=relevance_score,
            helpfulness_score=helpfulness_score,
            clarity_score=clarity_score,
            completeness_score=completeness_score,
            issues=issues,
            suggestions=suggestions
        )
    
    def _calculate_relevance_score(self, response: str, user_message: str) -> float:
        """Calculate how relevant the response is to the user message"""
        response_words = set(re.findall(r'\b\w+\b', response.lower()))
        user_words = set(re.findall(r'\b\w+\b', user_message.lower()))
        
        if not user_words:
            return 0.0
        
        # Calculate word overlap
        overlap = len(response_words.intersection(user_words))
        relevance = min(1.0, overlap / len(user_words))
        
        return relevance
    
    def _calculate_helpfulness_score(self, response: str) -> float:
        """Calculate how helpful the response is"""
        helpful_indicators = [
            'here\'s', 'you can', 'to do this', 'solution', 'answer',
            'example', 'code', 'step', 'guide', 'tutorial', 'help'
        ]
        
        harmful_indicators = [
            'i don\'t know', 'cannot', 'unable', 'sorry', 'error',
            'problem', 'issue', 'broken', 'failed'
        ]
        
        content_lower = response.lower()
        
        helpful_count = sum(content_lower.count(indicator) for indicator in helpful_indicators)
        harmful_count = sum(content_lower.count(indicator) for indicator in harmful_indicators)
        
        # Normalize scores
        helpful_score = min(1.0, helpful_count / 5.0)
        harmful_score = min(1.0, harmful_count / 3.0)
        
        return max(0.0, helpful_score - harmful_score)
    
    def _calculate_clarity_score(self, response: str) -> float:
        """Calculate how clear and understandable the response is"""
        # Check for clear structure
        has_structure = bool(re.search(r'\b\d+\.\b|\b•\b|\b-\b|\b:\b', response))
        
        # Check for appropriate length
        word_count = len(response.split())
        length_score = 1.0 if 20 <= word_count <= 500 else 0.5 if 10 <= word_count <= 1000 else 0.2
        
        # Check for technical terms (might indicate complexity)
        technical_terms = len(re.findall(r'\b[A-Z]{2,}\b|\b[a-z]+_[a-z]+\b', response))
        technical_score = max(0.0, 1.0 - (technical_terms / 10.0))
        
        return (has_structure + length_score + technical_score) / 3
    
    def _calculate_completeness_score(self, response: str) -> float:
        """Calculate how complete the response is"""
        # Check for comprehensive coverage
        completeness_indicators = [
            'first', 'second', 'finally', 'in conclusion', 'summary',
            'additionally', 'furthermore', 'moreover', 'also'
        ]
        
        content_lower = response.lower()
        indicator_count = sum(content_lower.count(indicator) for indicator in completeness_indicators)
        
        # Check response length (longer responses tend to be more complete)
        word_count = len(response.split())
        length_score = min(1.0, word_count / 200.0)
        
        # Check for code blocks or examples
        has_examples = bool(re.search(r'```|`.*`|example|code', content_lower))
        
        return min(1.0, (indicator_count / 3.0 + length_score + (0.3 if has_examples else 0.0)) / 3)
    
    def _identify_response_issues(self, response: str) -> List[str]:
        """Identify issues with the response"""
        issues = []
        content_lower = response.lower()
        
        # Check for common issues
        if len(response.split()) < 10:
            issues.append("Response too short")
        
        if len(response.split()) > 1000:
            issues.append("Response too long")
        
        if re.search(r'\b(i don\'t know|cannot|unable|sorry)\b', content_lower):
            issues.append("Unhelpful response")
        
        if not re.search(r'\b(here|this|that|it|solution|answer)\b', content_lower):
            issues.append("Lacks direct addressing")
        
        if re.search(r'\b(error|problem|issue|broken)\b', content_lower):
            issues.append("Contains error indicators")
        
        return issues
    
    def _generate_improvement_suggestions(self, response: str, issues: List[str]) -> List[str]:
        """Generate suggestions for improving the response"""
        suggestions = []
        
        for issue in issues:
            if issue == "Response too short":
                suggestions.append("Add more detail and examples")
            elif issue == "Response too long":
                suggestions.append("Be more concise and focused")
            elif issue == "Unhelpful response":
                suggestions.append("Provide specific guidance or alternatives")
            elif issue == "Lacks direct addressing":
                suggestions.append("Directly address the user's question")
            elif issue == "Contains error indicators":
                suggestions.append("Provide constructive solutions instead of just stating problems")
        
        return suggestions
    
    def _generate_conversation_summary(self, messages: List[Message]) -> str:
        """Generate a summary of the conversation"""
        if not messages:
            return "Empty conversation"
        
        # Extract key information
        user_messages = [msg.content for msg in messages if msg.role == "user"]
        ai_messages = [msg.content for msg in messages if msg.role == "assistant"]
        
        # Simple summary generation
        summary_parts = []
        
        if user_messages:
            first_user_msg = user_messages[0][:100] + "..." if len(user_messages[0]) > 100 else user_messages[0]
            summary_parts.append(f"User asked: {first_user_msg}")
        
        if ai_messages:
            summary_parts.append(f"AI provided {len(ai_messages)} responses")
        
        summary_parts.append(f"Total messages: {len(messages)}")
        
        return " | ".join(summary_parts)
    
    def _extract_conversation_topics(self, messages: List[Message]) -> List[str]:
        """Extract main topics from the conversation"""
        all_content = " ".join([msg.content for msg in messages])
        
        # Simple topic extraction based on common keywords
        topic_keywords = {
            'programming': ['code', 'program', 'function', 'class', 'variable', 'python', 'javascript'],
            'technology': ['tech', 'software', 'hardware', 'computer', 'system', 'application'],
            'help': ['help', 'assist', 'support', 'guide', 'tutorial', 'explain'],
            'problem': ['problem', 'issue', 'error', 'bug', 'fix', 'troubleshoot'],
            'creative': ['create', 'design', 'build', 'make', 'generate', 'write'],
            'analysis': ['analyze', 'review', 'evaluate', 'assess', 'examine', 'study']
        }
        
        topics = []
        content_lower = all_content.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ['general']
    
    def _determine_difficulty_level(self, messages: List[Message]) -> str:
        """Determine the difficulty level of the conversation"""
        all_content = " ".join([msg.content for msg in messages])
        content_lower = all_content.lower()
        
        # Count technical terms
        technical_terms = len(re.findall(r'\b[A-Z]{2,}\b|\b[a-z]+_[a-z]+\b|\b\d+\.\d+\b', content_lower))
        
        # Count code blocks
        code_blocks = len(re.findall(r'```|`.*`', content_lower))
        
        # Determine difficulty
        if technical_terms > 20 or code_blocks > 3:
            return "advanced"
        elif technical_terms > 10 or code_blocks > 1:
            return "intermediate"
        else:
            return "beginner"
    
    def save_conversation(self, conversation: Conversation):
        """Save conversation to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO conversations 
                (id, title, conversation_type, messages, turns, summary, topics, difficulty_level, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                conversation.id,
                conversation.title,
                conversation.conversation_type.value,
                json.dumps([{
                    'id': msg.id,
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'metadata': msg.metadata
                } for msg in conversation.messages]),
                json.dumps([{
                    'id': turn.id,
                    'user_message_id': turn.user_message.id,
                    'ai_response_id': turn.ai_response.id,
                    'user_intent': {
                        'intent_type': turn.user_intent.intent_type.value,
                        'confidence': turn.user_intent.confidence,
                        'entities': turn.user_intent.entities,
                        'keywords': turn.user_intent.keywords,
                        'context': turn.user_intent.context
                    },
                    'response_analysis': {
                        'quality': turn.response_analysis.quality.value,
                        'relevance_score': turn.response_analysis.relevance_score,
                        'helpfulness_score': turn.response_analysis.helpfulness_score,
                        'clarity_score': turn.response_analysis.clarity_score,
                        'completeness_score': turn.response_analysis.completeness_score,
                        'issues': turn.response_analysis.issues,
                        'suggestions': turn.response_analysis.suggestions
                    },
                    'context': turn.context
                } for turn in conversation.turns]),
                conversation.summary,
                json.dumps(conversation.topics),
                conversation.difficulty_level,
                conversation.created_at.isoformat(),
                json.dumps(conversation.metadata)
            ))
            conn.commit()
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_conversation(row)
        return None
    
    def get_all_conversations(self) -> List[Conversation]:
        """Get all conversations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM conversations ORDER BY created_at DESC")
            return [self._row_to_conversation(row) for row in cursor.fetchall()]
    
    def _row_to_conversation(self, row) -> Conversation:
        """Convert database row to Conversation object"""
        messages_data = json.loads(row[3])
        turns_data = json.loads(row[4])
        
        # Reconstruct messages
        messages = []
        for msg_data in messages_data:
            message = Message(
                id=msg_data['id'],
                role=msg_data['role'],
                content=msg_data['content'],
                timestamp=datetime.fromisoformat(msg_data['timestamp']),
                metadata=msg_data['metadata']
            )
            messages.append(message)
        
        # Reconstruct turns
        turns = []
        for turn_data in turns_data:
            # Find corresponding messages
            user_message = next((msg for msg in messages if msg.id == turn_data['user_message_id']), None)
            ai_response = next((msg for msg in messages if msg.id == turn_data['ai_response_id']), None)
            
            if user_message and ai_response:
                user_intent_data = turn_data['user_intent']
                user_intent = Intent(
                    intent_type=IntentType(user_intent_data['intent_type']),
                    confidence=user_intent_data['confidence'],
                    entities=user_intent_data['entities'],
                    keywords=user_intent_data['keywords'],
                    context=user_intent_data['context']
                )
                
                response_analysis_data = turn_data['response_analysis']
                response_analysis = ResponseAnalysis(
                    quality=ResponseQuality(response_analysis_data['quality']),
                    relevance_score=response_analysis_data['relevance_score'],
                    helpfulness_score=response_analysis_data['helpfulness_score'],
                    clarity_score=response_analysis_data['clarity_score'],
                    completeness_score=response_analysis_data['completeness_score'],
                    issues=response_analysis_data['issues'],
                    suggestions=response_analysis_data['suggestions']
                )
                
                turn = ConversationTurn(
                    id=turn_data['id'],
                    user_message=user_message,
                    ai_response=ai_response,
                    user_intent=user_intent,
                    response_analysis=response_analysis,
                    context=turn_data['context']
                )
                turns.append(turn)
        
        return Conversation(
            id=row[0],
            title=row[1],
            conversation_type=ConversationType(row[2]),
            messages=messages,
            turns=turns,
            summary=row[5],
            topics=json.loads(row[6]),
            difficulty_level=row[7],
            created_at=datetime.fromisoformat(row[8]),
            metadata=json.loads(row[9])
        )


class ConversationAnalyzerDemo:
    """Demo class for conversation analyzer"""
    
    def __init__(self):
        self.analyzer = ConversationAnalyzer()
    
    def run_basic_analysis_demo(self):
        """Demonstrate basic conversation analysis"""
        print("=== Basic Conversation Analysis Demo ===\n")
        
        # Sample conversation
        sample_messages = [
            {
                "role": "user",
                "content": "How do I create a Python function that calculates the factorial of a number?",
                "timestamp": datetime.now().isoformat(),
                "metadata": {}
            },
            {
                "role": "assistant",
                "content": "Here's how to create a Python function for calculating factorial:\n\n```python\ndef factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\n# Example usage\nprint(factorial(5))  # Output: 120\n```\n\nThis function uses recursion to calculate the factorial. It handles the base cases (0 and 1) and recursively multiplies the number by the factorial of (n-1).",
                "timestamp": datetime.now().isoformat(),
                "metadata": {}
            },
            {
                "role": "user",
                "content": "Can you explain how the recursion works step by step?",
                "timestamp": datetime.now().isoformat(),
                "metadata": {}
            },
            {
                "role": "assistant",
                "content": "Let me break down how the recursion works step by step for factorial(5):\n\n1. factorial(5) calls factorial(4)\n2. factorial(4) calls factorial(3)\n3. factorial(3) calls factorial(2)\n4. factorial(2) calls factorial(1)\n5. factorial(1) returns 1 (base case)\n6. factorial(2) returns 2 * 1 = 2\n7. factorial(3) returns 3 * 2 = 6\n8. factorial(4) returns 4 * 6 = 24\n9. factorial(5) returns 5 * 24 = 120\n\nEach function call waits for the result of the recursive call before multiplying by its own number.",
                "timestamp": datetime.now().isoformat(),
                "metadata": {}
            }
        ]
        
        # Analyze conversation
        conversation = self.analyzer.analyze_conversation(sample_messages, "Python Factorial Tutorial")
        
        # Display results
        print(f"Conversation: {conversation.title}")
        print(f"Type: {conversation.conversation_type.value}")
        print(f"Difficulty: {conversation.difficulty_level}")
        print(f"Topics: {', '.join(conversation.topics)}")
        print(f"Summary: {conversation.summary}")
        print(f"Turns: {len(conversation.turns)}")
        
        # Show turn analysis
        for i, turn in enumerate(conversation.turns, 1):
            print(f"\nTurn {i}:")
            print(f"  User Intent: {turn.user_intent.intent_type.value} (confidence: {turn.user_intent.confidence:.2f})")
            print(f"  Response Quality: {turn.response_analysis.quality.value}")
            print(f"  Relevance: {turn.response_analysis.relevance_score:.2f}")
            print(f"  Helpfulness: {turn.response_analysis.helpfulness_score:.2f}")
            print(f"  Clarity: {turn.response_analysis.clarity_score:.2f}")
            print(f"  Completeness: {turn.response_analysis.completeness_score:.2f}")
            
            if turn.response_analysis.issues:
                print(f"  Issues: {', '.join(turn.response_analysis.issues)}")
        
        # Save conversation
        self.analyzer.save_conversation(conversation)
        print(f"\nConversation saved with ID: {conversation.id}")
        
        print()
    
    def run_intent_extraction_demo(self):
        """Demonstrate intent extraction"""
        print("=== Intent Extraction Demo ===\n")
        
        test_messages = [
            "How do I install Python on Windows?",
            "Can you help me debug this code?",
            "Thanks for the great explanation!",
            "I'm having trouble with this error message",
            "Hello, I need some assistance",
            "Please create a function that sorts a list",
            "What does this error mean?",
            "Goodbye and thanks for your help!"
        ]
        
        for message in test_messages:
            intent = self.analyzer._extract_intent(message)
            print(f"Message: {message}")
            print(f"  Intent: {intent.intent_type.value}")
            print(f"  Confidence: {intent.confidence:.2f}")
            print(f"  Keywords: {intent.keywords[:5]}")
            print(f"  Entities: {intent.entities[:3]}")
            print()
    
    def run_quality_assessment_demo(self):
        """Demonstrate response quality assessment"""
        print("=== Response Quality Assessment Demo ===\n")
        
        test_responses = [
            "Here's a comprehensive solution with detailed explanations and examples...",
            "I don't know how to help with that.",
            "You can try this approach: [detailed explanation with code examples]",
            "Sorry, I can't help you with that problem.",
            "The answer is 42.",
            "This is a complex topic that requires careful consideration. Let me break it down step by step with examples and best practices..."
        ]
        
        user_message = "How do I implement a binary search algorithm?"
        
        for i, response in enumerate(test_responses, 1):
            analysis = self.analyzer._analyze_response(response, user_message)
            print(f"Response {i}: {response[:50]}...")
            print(f"  Quality: {analysis.quality.value}")
            print(f"  Relevance: {analysis.relevance_score:.2f}")
            print(f"  Helpfulness: {analysis.helpfulness_score:.2f}")
            print(f"  Clarity: {analysis.clarity_score:.2f}")
            print(f"  Completeness: {analysis.completeness_score:.2f}")
            
            if analysis.issues:
                print(f"  Issues: {', '.join(analysis.issues)}")
            if analysis.suggestions:
                print(f"  Suggestions: {', '.join(analysis.suggestions)}")
            print()
    
    def run_conversation_management_demo(self):
        """Demonstrate conversation management"""
        print("=== Conversation Management Demo ===\n")
        
        # Get all conversations
        conversations = self.analyzer.get_all_conversations()
        print(f"Total conversations: {len(conversations)}")
        
        for conv in conversations:
            print(f"\nConversation: {conv.title}")
            print(f"  Type: {conv.conversation_type.value}")
            print(f"  Difficulty: {conv.difficulty_level}")
            print(f"  Topics: {', '.join(conv.topics)}")
            print(f"  Messages: {len(conv.messages)}")
            print(f"  Turns: {len(conv.turns)}")
            print(f"  Created: {conv.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        print()


def main():
    """Main demo function"""
    demo = ConversationAnalyzerDemo()
    
    try:
        # Run demos
        demo.run_basic_analysis_demo()
        demo.run_intent_extraction_demo()
        demo.run_quality_assessment_demo()
        demo.run_conversation_management_demo()
        
        print("=== Conversation Analyzer Demo Complete ===")
        print("Conversation analysis system is working correctly!")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 