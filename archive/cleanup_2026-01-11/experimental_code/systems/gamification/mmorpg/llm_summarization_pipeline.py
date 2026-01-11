#!/usr/bin/env python3
"""
LLM Self-Summarization and Active Learning Pipeline - Agent 2
============================================================

AI-driven conversation summarization with learning feedback loops.
Integrates with existing skill extraction and knowledge graph systems.
"""

import logging
import json
import sqlite3
import threading
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import hashlib
import re

from dreamscape.core.memory import MemoryManager
from dreamscape.core.utils.context_utils import split_json_txt_blocks
from .enhanced_skill_resume_system import EnhancedSkillResumeSystem, AISkillAnalysis

logger = logging.getLogger(__name__)

class SummarizationType(Enum):
    """Types of summarization."""
    SKILL_EXTRACTION = "skill_extraction"
    LEARNING_INSIGHTS = "learning_insights"
    PROJECT_SUMMARY = "project_summary"
    CONVERSATION_HIGHLIGHTS = "conversation_highlights"
    KNOWLEDGE_SYNTHESIS = "knowledge_synthesis"

class SummarizationQuality(Enum):
    """Quality levels for summarization."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNUSABLE = "unusable"

@dataclass
class ConversationSummary:
    """Summary of a conversation."""
    conversation_id: str
    summary_type: SummarizationType
    content: str
    key_insights: List[str]
    skill_relevance: Dict[str, float]  # skill_name -> relevance_score
    learning_points: List[str]
    confidence_score: float
    quality_rating: SummarizationQuality
    metadata: Dict[str, Any]
    created_at: datetime
    feedback_score: Optional[float] = None
    user_corrections: List[str] = None
    ai_improvements: List[str] = None
    
    def __post_init__(self):
        if self.user_corrections is None:
            self.user_corrections = []
        if self.ai_improvements is None:
            self.ai_improvements = []

@dataclass
class LearningFeedback:
    """Feedback for improving summarization quality."""
    summary_id: str
    user_rating: int  # 1-5 scale
    user_comments: str
    correction_suggestions: List[str]
    improvement_areas: List[str]
    feedback_timestamp: datetime
    applied_to_model: bool = False

@dataclass
class ActiveLearningExample:
    """Example for active learning."""
    conversation_id: str
    original_content: str
    generated_summary: str
    corrected_summary: str
    skill_labels: Dict[str, str]  # skill_name -> proficiency_level
    learning_outcome: str
    quality_improvement: float

class LLMSummarizationPipeline:
    """
    LLM self-summarization and active learning pipeline.
    
    Integrates with existing skill extraction and knowledge graph systems
    to provide AI-driven conversation summarization with continuous learning.
    """
    
    def __init__(self, memory_manager: MemoryManager, 
                 enhanced_skill_system: EnhancedSkillResumeSystem,
                 db_path: str = "llm_summarization.db"):
        """Initialize the summarization pipeline."""
        self.memory_manager = memory_manager
        self.enhanced_skill_system = enhanced_skill_system
        self.db_path = db_path
        
        # Active learning components
        self.feedback_queue = queue.Queue()
        self.learning_examples: List[ActiveLearningExample] = []
        self.quality_metrics: Dict[str, float] = {}
        
        # Summarization templates and prompts
        self.summarization_templates = self._load_summarization_templates()
        
        # Initialize database
        self.init_database()
        
        # Start feedback processing thread
        self.feedback_thread = threading.Thread(target=self._process_feedback_loop, daemon=True)
        self.feedback_thread.start()
        
        logger.info("🤖 LLM Summarization Pipeline initialized")
    
    def init_database(self):
        """Initialize the database for summarization and learning."""
        with sqlite3.connect(self.db_path) as conn:
            # Summaries table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation_summaries (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    summary_type TEXT,
                    content TEXT,
                    key_insights TEXT,
                    skill_relevance TEXT,
                    learning_points TEXT,
                    confidence_score REAL,
                    quality_rating TEXT,
                    metadata TEXT,
                    created_at TIMESTAMP,
                    feedback_score REAL,
                    user_corrections TEXT,
                    ai_improvements TEXT
                )
            """)
            
            # Learning feedback table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_feedback (
                    id TEXT PRIMARY KEY,
                    summary_id TEXT,
                    user_rating INTEGER,
                    user_comments TEXT,
                    correction_suggestions TEXT,
                    improvement_areas TEXT,
                    feedback_timestamp TIMESTAMP,
                    applied_to_model BOOLEAN DEFAULT 0
                )
            """)
            
            # Active learning examples table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS active_learning_examples (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    original_content TEXT,
                    generated_summary TEXT,
                    corrected_summary TEXT,
                    skill_labels TEXT,
                    learning_outcome TEXT,
                    quality_improvement REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Quality metrics table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS quality_metrics (
                    id TEXT PRIMARY KEY,
                    metric_name TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def _load_summarization_templates(self) -> Dict[str, str]:
        """Load summarization templates for different types."""
        return {
            SummarizationType.SKILL_EXTRACTION.value: """
            Analyze this conversation and extract technical skills demonstrated:
            
            Conversation: {conversation_content}
            
            Provide a structured summary including:
            1. Key technical skills identified
            2. Proficiency level assessment
            3. Evidence from conversation
            4. Learning insights
            5. Skill relationships and dependencies
            
            Format as JSON with the following structure:
            {{
                "skills": [
                    {{
                        "name": "skill_name",
                        "proficiency": "beginner|intermediate|advanced|expert",
                        "confidence": 0.0-1.0,
                        "evidence": ["evidence1", "evidence2"],
                        "learning_insights": ["insight1", "insight2"]
                    }}
                ],
                "skill_relationships": [{"skill1": "skill2", "relationship": "dependency"}],
                "overall_assessment": "summary_text"
            }}
            """,
            
            SummarizationType.LEARNING_INSIGHTS.value: """
            Extract learning insights and knowledge gains from this conversation:
            
            Conversation: {conversation_content}
            
            Focus on:
            1. New concepts learned
            2. Problem-solving approaches
            3. Best practices identified
            4. Areas for further study
            5. Practical applications
            
            Format as structured text with clear sections.
            """,
            
            SummarizationType.PROJECT_SUMMARY.value: """
            Create a project summary from this conversation:
            
            Conversation: {conversation_content}
            
            Include:
            1. Project overview and goals
            2. Technical challenges addressed
            3. Solutions implemented
            4. Technologies used
            5. Outcomes and results
            6. Lessons learned
            
            Format as a professional project summary.
            """,
            
            SummarizationType.CONVERSATION_HIGHLIGHTS.value: """
            Extract key highlights and main points from this conversation:
            
            Conversation: {conversation_content}
            
            Identify:
            1. Main topics discussed
            2. Key decisions made
            3. Important insights shared
            4. Action items or next steps
            5. Notable achievements or progress
            
            Provide a concise, well-structured summary.
            """,
            
            SummarizationType.KNOWLEDGE_SYNTHESIS.value: """
            Synthesize knowledge and create connections from this conversation:
            
            Conversation: {conversation_content}
            
            Focus on:
            1. Knowledge integration across topics
            2. Pattern recognition
            3. Conceptual connections
            4. Meta-learning insights
            5. Knowledge gaps identified
            
            Create a synthesis that connects different pieces of knowledge.
            """
        }
    
    def summarize_conversation(self, conversation_id: str, 
                             summary_type: SummarizationType = SummarizationType.SKILL_EXTRACTION,
                             use_active_learning: bool = True) -> ConversationSummary:
        """
        Summarize a conversation using AI with optional active learning.
        
        Args:
            conversation_id: ID of the conversation to summarize
            summary_type: Type of summarization to perform
            use_active_learning: Whether to use active learning improvements
            
        Returns:
            ConversationSummary object
        """
        try:
            # Get conversation content
            conversation = self.memory_manager.get_conversation(conversation_id)
            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found")
            
            conversation_content = conversation.get('content', '')
            
            # Generate initial summary
            summary = self._generate_ai_summary(conversation_content, summary_type)
            
            # Apply active learning improvements if enabled
            if use_active_learning:
                summary = self._apply_active_learning_improvements(summary, conversation_content)
            
            # Extract skill relevance
            skill_relevance = self._extract_skill_relevance(summary, conversation_content)
            
            # Assess quality
            quality_rating = self._assess_summary_quality(summary, conversation_content)
            
            # Create summary object
            conversation_summary = ConversationSummary(
                conversation_id=conversation_id,
                summary_type=summary_type,
                content=summary,
                key_insights=self._extract_key_insights(summary),
                skill_relevance=skill_relevance,
                learning_points=self._extract_learning_points(summary),
                confidence_score=self._calculate_confidence_score(summary, conversation_content),
                quality_rating=quality_rating,
                metadata={
                    'summary_length': len(summary),
                    'conversation_length': len(conversation_content),
                    'active_learning_applied': use_active_learning,
                    'processing_timestamp': datetime.now().isoformat()
                },
                created_at=datetime.now()
            )
            
            # Store in database
            self._store_summary(conversation_summary)
            
            # Update skill system with new insights
            self._update_skill_system(conversation_summary)
            
            logger.info(f"✅ Generated {summary_type.value} summary for conversation {conversation_id}")
            return conversation_summary
            
        except Exception as e:
            logger.error(f"❌ Failed to summarize conversation {conversation_id}: {e}")
            raise
    
    def _generate_ai_summary(self, conversation_content: str, summary_type: SummarizationType) -> str:
        """Generate AI summary using templates and context."""
        try:
            # Get template for summary type
            template = self.summarization_templates.get(summary_type.value, "")
            if not template:
                raise ValueError(f"No template found for summary type: {summary_type.value}")
            
            # Parse JSON/TXT blocks from conversation content
            content_split = split_json_txt_blocks(conversation_content)
            
            # Prepare content for template
            formatted_content = ""
            if content_split['txt_blocks']:
                formatted_content += "\n".join(content_split['txt_blocks'])
            if content_split['json_blocks']:
                formatted_content += "\n\nStructured Data:\n" + "\n".join(content_split['json_blocks'])
            
            # Format template with content
            prompt = template.format(conversation_content=formatted_content[:5000])  # Limit content length
            
            # Integrate with AdvancedReasoningEngine for real LLM summarization
            try:
                # Import AI reasoning engine
                from src.ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine, ReasoningContext, ReasoningMode, ResponseFormat

                # Create AI reasoning context
                ai_context = ReasoningContext(
                    query=prompt,
                    mode=ReasoningMode.ANALYTICAL if summary_type in [SummarizationType.SKILL_EXTRACTION, SummarizationType.LEARNING_INSIGHTS] else ReasoningMode.STRATEGIC,
                    format=ResponseFormat.TEXT
                )

                # Initialize AI engine and generate summary
                ai_engine = AdvancedReasoningEngine()
                ai_result = ai_engine.reason(ai_context)

                summary = ai_result.response
                logger.info(f"Generated AI summary for {summary_type.value}: {len(summary)} characters")

            except Exception as ai_error:
                logger.warning(f"AI summarization failed, falling back to mock: {ai_error}")
                # Fallback to mock summary if AI fails
                summary = self._generate_mock_summary(conversation_content, summary_type)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return f"Error generating summary: {str(e)}"
    
    def _generate_mock_summary(self, conversation_content: str, summary_type: SummarizationType) -> str:
        """Generate a mock summary for testing purposes."""
        if summary_type == SummarizationType.SKILL_EXTRACTION:
            return """
            {
                "skills": [
                    {
                        "name": "Python Programming",
                        "proficiency": "intermediate",
                        "confidence": 0.8,
                        "evidence": ["Discussed advanced Python patterns", "Implemented complex algorithms"],
                        "learning_insights": ["Understanding of design patterns", "Algorithm optimization techniques"]
                    },
                    {
                        "name": "System Architecture",
                        "proficiency": "advanced",
                        "confidence": 0.9,
                        "evidence": ["Designed scalable system", "Discussed microservices"],
                        "learning_insights": ["Distributed system design", "Service communication patterns"]
                    }
                ],
                "skill_relationships": [
                    {"Python Programming": "System Architecture", "relationship": "enables"}
                ],
                "overall_assessment": "Strong technical foundation with focus on system design and Python development."
            }
            """
        elif summary_type == SummarizationType.LEARNING_INSIGHTS:
            return """
            Learning Insights:
            
            New Concepts Learned:
            - Advanced Python design patterns
            - Microservices architecture principles
            - Distributed system communication
            
            Problem-Solving Approaches:
            - Systematic analysis of complex problems
            - Iterative solution development
            - Performance optimization techniques
            
            Best Practices Identified:
            - Code modularity and reusability
            - System scalability considerations
            - Testing and validation strategies
            
            Areas for Further Study:
            - Cloud-native development
            - Advanced data structures
            - System monitoring and observability
            """
        else:
            return f"Summary of conversation focusing on {summary_type.value}: {conversation_content[:200]}..."
    
    def _apply_active_learning_improvements(self, summary: str, original_content: str) -> str:
        """Apply active learning improvements to the summary."""
        try:
            # Find similar examples in learning database
            similar_examples = self._find_similar_learning_examples(original_content)
            
            if not similar_examples:
                return summary
            
            # Apply improvements based on similar examples
            improved_summary = summary
            
            for example in similar_examples[:3]:  # Use top 3 similar examples
                if example.quality_improvement > 0.1:  # Only apply if significant improvement
                    improved_summary = self._apply_example_improvements(
                        improved_summary, example
                    )
            
            return improved_summary
            
        except Exception as e:
            logger.error(f"Error applying active learning improvements: {e}")
            return summary
    
    def _find_similar_learning_examples(self, content: str) -> List[ActiveLearningExample]:
        """Find similar learning examples for active learning."""
        try:
            # Simple similarity based on content length and key terms
            content_length = len(content)
            key_terms = self._extract_key_terms(content)
            
            similar_examples = []
            
            for example in self.learning_examples:
                # Calculate similarity score
                length_similarity = 1.0 - abs(content_length - len(example.original_content)) / max(content_length, len(example.original_content))
                term_similarity = len(set(key_terms) & set(self._extract_key_terms(example.original_content))) / max(len(key_terms), 1)
                
                overall_similarity = (length_similarity + term_similarity) / 2
                
                if overall_similarity > 0.3:  # Similarity threshold
                    similar_examples.append((example, overall_similarity))
            
            # Sort by similarity and return top examples
            similar_examples.sort(key=lambda x: x[1], reverse=True)
            return [example for example, score in similar_examples[:5]]
            
        except Exception as e:
            logger.error(f"Error finding similar learning examples: {e}")
            return []
    
    def _extract_key_terms(self, content: str) -> List[str]:
        """Extract key terms from content for similarity matching."""
        # Simple key term extraction
        words = re.findall(r'\b\w+\b', content.lower())
        # Filter out common words and short terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        key_terms = [word for word in words if len(word) > 3 and word not in stop_words]
        return list(set(key_terms))[:20]  # Limit to top 20 terms
    
    def _apply_example_improvements(self, summary: str, example: ActiveLearningExample) -> str:
        """Apply improvements from a learning example."""
        try:
            # Simple improvement: if the corrected summary is significantly different,
            # apply some of its structure or insights
            if example.quality_improvement > 0.2:
                # Extract key improvements from the corrected summary
                corrected_insights = self._extract_key_insights(example.corrected_summary)
                original_insights = self._extract_key_insights(example.generated_summary)
                
                # Find new insights that weren't in the original
                new_insights = [insight for insight in corrected_insights if insight not in original_insights]
                
                if new_insights:
                    # Add new insights to the current summary
                    summary += "\n\nAdditional Insights:\n" + "\n".join(f"- {insight}" for insight in new_insights[:3])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error applying example improvements: {e}")
            return summary
    
    def _extract_skill_relevance(self, summary: str, conversation_content: str) -> Dict[str, float]:
        """Extract skill relevance scores from summary and conversation."""
        try:
            # Use existing skill extraction system
            skills = self.enhanced_skill_system.analyze_conversation_for_skills(
                "temp_id", conversation_content
            )
            
            skill_relevance = {}
            for skill in skills:
                skill_relevance[skill.skill_name] = skill.confidence
            
            return skill_relevance
            
        except Exception as e:
            logger.error(f"Error extracting skill relevance: {e}")
            return {}
    
    def _extract_key_insights(self, summary: str) -> List[str]:
        """Extract key insights from summary."""
        try:
            # Simple insight extraction
            lines = summary.split('\n')
            insights = []
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or 
                           any(keyword in line.lower() for keyword in ['insight', 'learned', 'discovered', 'found'])):
                    insights.append(line)
            
            return insights[:10]  # Limit to top 10 insights
            
        except Exception as e:
            logger.error(f"Error extracting key insights: {e}")
            return []
    
    def _extract_learning_points(self, summary: str) -> List[str]:
        """Extract learning points from summary."""
        try:
            # Extract learning points from summary
            learning_points = []
            
            # Look for learning-related patterns
            learning_patterns = [
                r'learned\s+([^.]*)',
                r'discovered\s+([^.]*)',
                r'found\s+([^.]*)',
                r'understood\s+([^.]*)',
                r'realized\s+([^.]*)'
            ]
            
            for pattern in learning_patterns:
                matches = re.finditer(pattern, summary, re.IGNORECASE)
                for match in matches:
                    learning_points.append(match.group(1).strip())
            
            return learning_points[:5]  # Limit to top 5 learning points
            
        except Exception as e:
            logger.error(f"Error extracting learning points: {e}")
            return []
    
    def _calculate_confidence_score(self, summary: str, original_content: str) -> float:
        """Calculate confidence score for the summary."""
        try:
            # Simple confidence calculation based on summary quality indicators
            confidence_factors = []
            
            # Length ratio (summary should be reasonable length)
            length_ratio = len(summary) / max(len(original_content), 1)
            if 0.1 <= length_ratio <= 0.5:
                confidence_factors.append(0.8)
            else:
                confidence_factors.append(0.4)
            
            # Content coverage (summary should mention key terms from original)
            original_terms = set(self._extract_key_terms(original_content))
            summary_terms = set(self._extract_key_terms(summary))
            coverage = len(original_terms & summary_terms) / max(len(original_terms), 1)
            confidence_factors.append(min(coverage * 2, 1.0))
            
            # Structure quality (summary should have some structure)
            if any(marker in summary for marker in ['•', '-', '1.', '2.', '3.']):
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.6)
            
            return sum(confidence_factors) / len(confidence_factors)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def _assess_summary_quality(self, summary: str, original_content: str) -> SummarizationQuality:
        """Assess the quality of the summary."""
        try:
            confidence_score = self._calculate_confidence_score(summary, original_content)
            
            if confidence_score >= 0.8:
                return SummarizationQuality.EXCELLENT
            elif confidence_score >= 0.6:
                return SummarizationQuality.GOOD
            elif confidence_score >= 0.4:
                return SummarizationQuality.FAIR
            elif confidence_score >= 0.2:
                return SummarizationQuality.POOR
            else:
                return SummarizationQuality.UNUSABLE
                
        except Exception as e:
            logger.error(f"Error assessing summary quality: {e}")
            return SummarizationQuality.FAIR
    
    def _store_summary(self, summary: ConversationSummary):
        """Store summary in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO conversation_summaries 
                    (id, conversation_id, summary_type, content, key_insights, skill_relevance,
                     learning_points, confidence_score, quality_rating, metadata, created_at,
                     feedback_score, user_corrections, ai_improvements)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    summary.conversation_id,
                    summary.conversation_id,
                    summary.summary_type.value,
                    summary.content,
                    json.dumps(summary.key_insights),
                    json.dumps(summary.skill_relevance),
                    json.dumps(summary.learning_points),
                    summary.confidence_score,
                    summary.quality_rating.value,
                    json.dumps(summary.metadata),
                    summary.created_at.isoformat(),
                    summary.feedback_score,
                    json.dumps(summary.user_corrections),
                    json.dumps(summary.ai_improvements)
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing summary: {e}")
    
    def _update_skill_system(self, summary: ConversationSummary):
        """Update the skill system with new insights from summary."""
        try:
            # Extract skills from summary and update the skill system
            for skill_name, relevance_score in summary.skill_relevance.items():
                if relevance_score > 0.5:  # Only update if relevance is high enough
                    # Update skill analysis in the enhanced skill system
                    if hasattr(self.enhanced_skill_system, 'skill_analysis_cache'):
                        if skill_name in self.enhanced_skill_system.skill_analysis_cache:
                            skill_analysis = self.enhanced_skill_system.skill_analysis_cache[skill_name]
                            skill_analysis.confidence = max(skill_analysis.confidence, relevance_score)
                            skill_analysis.evidence.append(f"Enhanced by summarization: {summary.conversation_id}")
                            skill_analysis.last_used = datetime.now()
            
            logger.info(f"Updated skill system with insights from summary {summary.conversation_id}")
            
        except Exception as e:
            logger.error(f"Error updating skill system: {e}")
    
    def submit_feedback(self, summary_id: str, user_rating: int, 
                       user_comments: str = "", correction_suggestions: List[str] = None,
                       improvement_areas: List[str] = None) -> bool:
        """
        Submit feedback for a summary to improve the learning system.
        
        Args:
            summary_id: ID of the summary being rated
            user_rating: User rating (1-5 scale)
            user_comments: User comments
            correction_suggestions: Suggested corrections
            improvement_areas: Areas for improvement
            
        Returns:
            True if feedback was submitted successfully
        """
        try:
            feedback = LearningFeedback(
                summary_id=summary_id,
                user_rating=user_rating,
                user_comments=user_comments,
                correction_suggestions=correction_suggestions or [],
                improvement_areas=improvement_areas or [],
                feedback_timestamp=datetime.now()
            )
            
            # Add to feedback queue for processing
            self.feedback_queue.put(feedback)
            
            # Store in database
            self._store_feedback(feedback)
            
            logger.info(f"✅ Feedback submitted for summary {summary_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to submit feedback: {e}")
            return False
    
    def _store_feedback(self, feedback: LearningFeedback):
        """Store feedback in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO learning_feedback 
                    (id, summary_id, user_rating, user_comments, correction_suggestions,
                     improvement_areas, feedback_timestamp, applied_to_model)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    feedback.summary_id,
                    feedback.summary_id,
                    feedback.user_rating,
                    feedback.user_comments,
                    json.dumps(feedback.correction_suggestions),
                    json.dumps(feedback.improvement_areas),
                    feedback.feedback_timestamp.isoformat(),
                    feedback.applied_to_model
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing feedback: {e}")
    
    def _process_feedback_loop(self):
        """Background thread for processing feedback and improving the model."""
        logger.info("🔄 Starting feedback processing loop")
        
        while True:
            try:
                # Get feedback from queue
                feedback = self.feedback_queue.get(timeout=60)  # Wait up to 60 seconds
                
                # Process feedback
                self._process_single_feedback(feedback)
                
                # Mark as processed
                self.feedback_queue.task_done()
                
            except queue.Empty:
                # No feedback in queue, continue
                continue
            except Exception as e:
                logger.error(f"Error in feedback processing loop: {e}")
    
    def _process_single_feedback(self, feedback: LearningFeedback):
        """Process a single feedback item."""
        try:
            # Get the original summary
            summary = self._get_summary(feedback.summary_id)
            if not summary:
                logger.warning(f"Summary {feedback.summary_id} not found for feedback processing")
                return
            
            # Create learning example
            learning_example = ActiveLearningExample(
                conversation_id=summary.conversation_id,
                original_content=self._get_conversation_content(summary.conversation_id),
                generated_summary=summary.content,
                corrected_summary=self._generate_corrected_summary(summary, feedback),
                skill_labels=summary.skill_relevance,
                learning_outcome=self._extract_learning_outcome(feedback),
                quality_improvement=self._calculate_quality_improvement(feedback)
            )
            
            # Add to learning examples
            self.learning_examples.append(learning_example)
            
            # Store in database
            self._store_learning_example(learning_example)
            
            # Update quality metrics
            self._update_quality_metrics(feedback)
            
            # Mark feedback as applied
            self._mark_feedback_applied(feedback.summary_id)
            
            logger.info(f"✅ Processed feedback for summary {feedback.summary_id}")
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
    
    def _get_summary(self, summary_id: str) -> Optional[ConversationSummary]:
        """Get summary from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM conversation_summaries WHERE id = ?
                """, (summary_id,))
                row = cursor.fetchone()
                
                if row:
                    return ConversationSummary(
                        conversation_id=row[1],
                        summary_type=SummarizationType(row[2]),
                        content=row[3],
                        key_insights=json.loads(row[4]),
                        skill_relevance=json.loads(row[5]),
                        learning_points=json.loads(row[6]),
                        confidence_score=row[7],
                        quality_rating=SummarizationQuality(row[8]),
                        metadata=json.loads(row[9]),
                        created_at=datetime.fromisoformat(row[10]),
                        feedback_score=row[11],
                        user_corrections=json.loads(row[12]) if row[12] else [],
                        ai_improvements=json.loads(row[13]) if row[13] else []
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error getting summary: {e}")
            return None
    
    def _get_conversation_content(self, conversation_id: str) -> str:
        """Get conversation content from memory manager."""
        try:
            conversation = self.memory_manager.get_conversation(conversation_id)
            return conversation.get('content', '') if conversation else ''
        except Exception as e:
            logger.error(f"Error getting conversation content: {e}")
            return ''
    
    def _generate_corrected_summary(self, summary: ConversationSummary, 
                                  feedback: LearningFeedback) -> str:
        """Generate corrected summary based on feedback."""
        try:
            corrected_summary = summary.content
            
            # Apply correction suggestions
            for suggestion in feedback.correction_suggestions:
                # Simple correction application (in a real system, this would be more sophisticated)
                if "add" in suggestion.lower():
                    corrected_summary += f"\n\nAdditional point: {suggestion}"
                elif "remove" in suggestion.lower():
                    # Remove problematic content
                    corrected_summary = re.sub(r'problematic.*?content', '', corrected_summary, flags=re.IGNORECASE)
                elif "improve" in suggestion.lower():
                    corrected_summary += f"\n\nImproved: {suggestion}"
            
            return corrected_summary
            
        except Exception as e:
            logger.error(f"Error generating corrected summary: {e}")
            return summary.content
    
    def _extract_learning_outcome(self, feedback: LearningFeedback) -> str:
        """Extract learning outcome from feedback."""
        try:
            if feedback.user_rating >= 4:
                return "High quality summary, minimal improvements needed"
            elif feedback.user_rating >= 3:
                return "Good summary with some areas for improvement"
            elif feedback.user_rating >= 2:
                return "Fair summary requiring significant improvements"
            else:
                return "Poor summary requiring major revisions"
                
        except Exception as e:
            logger.error(f"Error extracting learning outcome: {e}")
            return "Unknown learning outcome"
    
    def _calculate_quality_improvement(self, feedback: LearningFeedback) -> float:
        """Calculate quality improvement based on feedback."""
        try:
            # Simple quality improvement calculation
            base_quality = 0.5  # Assume base quality
            user_rating_normalized = feedback.user_rating / 5.0
            
            improvement = user_rating_normalized - base_quality
            
            # Consider correction suggestions as additional improvement potential
            if feedback.correction_suggestions:
                improvement += len(feedback.correction_suggestions) * 0.1
            
            return max(0.0, min(1.0, improvement))
            
        except Exception as e:
            logger.error(f"Error calculating quality improvement: {e}")
            return 0.0
    
    def _store_learning_example(self, example: ActiveLearningExample):
        """Store learning example in database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO active_learning_examples 
                    (id, conversation_id, original_content, generated_summary, corrected_summary,
                     skill_labels, learning_outcome, quality_improvement, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    example.conversation_id,
                    example.conversation_id,
                    example.original_content,
                    example.generated_summary,
                    example.corrected_summary,
                    json.dumps(example.skill_labels),
                    example.learning_outcome,
                    example.quality_improvement,
                    example.created_at.isoformat()
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing learning example: {e}")
    
    def _update_quality_metrics(self, feedback: LearningFeedback):
        """Update quality metrics based on feedback."""
        try:
            # Update average rating
            current_avg = self.quality_metrics.get('average_rating', 0.0)
            total_feedback = self.quality_metrics.get('total_feedback', 0)
            
            new_avg = (current_avg * total_feedback + feedback.user_rating) / (total_feedback + 1)
            
            self.quality_metrics['average_rating'] = new_avg
            self.quality_metrics['total_feedback'] = total_feedback + 1
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO quality_metrics (id, metric_name, metric_value, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (
                    f"avg_rating_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'average_rating',
                    new_avg,
                    datetime.now().isoformat()
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating quality metrics: {e}")
    
    def _mark_feedback_applied(self, summary_id: str):
        """Mark feedback as applied to the model."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE learning_feedback 
                    SET applied_to_model = 1 
                    WHERE summary_id = ?
                """, (summary_id,))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error marking feedback as applied: {e}")
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get statistics about the summarization system."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get summary counts by type
                cursor = conn.execute("""
                    SELECT summary_type, COUNT(*) as count 
                    FROM conversation_summaries 
                    GROUP BY summary_type
                """)
                summary_counts = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Get average quality ratings
                cursor = conn.execute("""
                    SELECT AVG(feedback_score) as avg_score, COUNT(*) as total_feedback
                    FROM conversation_summaries 
                    WHERE feedback_score IS NOT NULL
                """)
                quality_stats = cursor.fetchone()
                
                # Get recent activity
                cursor = conn.execute("""
                    SELECT COUNT(*) as recent_count
                    FROM conversation_summaries 
                    WHERE created_at > datetime('now', '-7 days')
                """)
                recent_activity = cursor.fetchone()[0]
                
                return {
                    'summary_counts': summary_counts,
                    'average_quality_score': quality_stats[0] if quality_stats[0] else 0.0,
                    'total_feedback': quality_stats[1] if quality_stats[1] else 0,
                    'recent_activity': recent_activity,
                    'learning_examples_count': len(self.learning_examples),
                    'quality_metrics': self.quality_metrics
                }
                
        except Exception as e:
            logger.error(f"Error getting summary statistics: {e}")
            return {}
    
    def batch_summarize_conversations(self, conversation_ids: List[str], 
                                    summary_type: SummarizationType = SummarizationType.SKILL_EXTRACTION) -> List[ConversationSummary]:
        """
        Summarize multiple conversations in batch.
        
        Args:
            conversation_ids: List of conversation IDs to summarize
            summary_type: Type of summarization to perform
            
        Returns:
            List of ConversationSummary objects
        """
        summaries = []
        
        for conversation_id in conversation_ids:
            try:
                summary = self.summarize_conversation(conversation_id, summary_type)
                summaries.append(summary)
            except Exception as e:
                logger.error(f"Failed to summarize conversation {conversation_id}: {e}")
                continue
        
        logger.info(f"✅ Batch summarization complete: {len(summaries)}/{len(conversation_ids)} successful")
        return summaries 