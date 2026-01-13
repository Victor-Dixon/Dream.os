"""
Enhanced Skill Tree and Resume Builder System
============================================

Integrates with prompting and response receiving logic to provide dynamic,
AI-powered skill detection and resume building based on conversation analysis.
"""

import logging
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

from dreamscape.core.memory import MemoryManager
# Removed top-level import to avoid circular import - will use lazy loading
from .enhanced_progress_system import EnhancedProgressSystem, ProgressTrigger
from dreamscape.core.legacy.resume_tracker import ResumeTracker
from .models import Skill, Project, Achievement, KnowledgeNode
from .analysis import KnowledgeGraphBackend
from .mmorpg_engine import MMORPGEngine

logger = logging.getLogger(__name__)

@dataclass
class AISkillAnalysis:
    """AI-analyzed skill information."""
    skill_name: str
    category: str
    proficiency_level: str  # 'beginner', 'intermediate', 'advanced', 'expert'
    confidence: float
    evidence: List[str]
    conversation_ids: List[str]
    last_used: datetime
    ai_insights: Dict[str, Any]
    skill_relationships: List[str]
    learning_path: List[str]

@dataclass
class AIProjectAnalysis:
    """AI-analyzed project information."""
    project_name: str
    description: str
    technologies: List[str]
    complexity_level: str  # 'simple', 'moderate', 'complex', 'enterprise'
    impact_score: float  # 0.0 to 1.0
    team_size: int
    role: str
    duration_days: int
    conversation_ids: List[str]
    ai_insights: Dict[str, Any]
    achievements: List[str]

@dataclass
class SkillTreeNode:
    """Node in the enhanced skill tree."""
    skill_name: str
    level: int
    xp: int
    category: str
    dependencies: List[str]
    unlocks: List[str]
    ai_confidence: float
    last_updated: datetime
    metadata: Dict[str, Any]

class EnhancedSkillResumeSystem:
    """
    Enhanced skill tree and resume builder that uses AI analysis
    for better content detection and progression tracking.
    """
    
    def __init__(self, memory_manager: MemoryManager, mmorpg_engine: Any, 
                 resume_tracker: ResumeTracker):
        self.memory_manager = memory_manager
        self.mmorpg_engine = mmorpg_engine
        self.resume_tracker = resume_tracker
        self.progress_system = EnhancedProgressSystem(mmorpg_engine, memory_manager)
        
        # AI analysis cache
        self.skill_analysis_cache: Dict[str, AISkillAnalysis] = {}
        self.project_analysis_cache: Dict[str, AIProjectAnalysis] = {}
        
        # Skill tree structure
        self.skill_tree: Dict[str, SkillTreeNode] = {}
        self.graph_backend = KnowledgeGraphBackend()
        
        # Enhanced skill patterns with AI insights
        self.enhanced_skill_patterns = {
            'programming_languages': {
                'python': {
                    'patterns': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
                    'related_skills': ['data_analysis', 'web_development', 'automation'],
                    'complexity_indicators': ['async', 'decorators', 'metaclasses', 'type hints']
                },
                'javascript': {
                    'patterns': ['javascript', 'node.js', 'react', 'vue', 'angular', 'typescript'],
                    'related_skills': ['frontend_development', 'backend_development', 'fullstack'],
                    'complexity_indicators': ['closures', 'prototypes', 'async/await', 'functional programming']
                },
                'java': {
                    'patterns': ['java', 'spring', 'maven', 'gradle', 'junit'],
                    'related_skills': ['enterprise_development', 'object_oriented_design'],
                    'complexity_indicators': ['design patterns', 'jvm tuning', 'microservices']
                }
            },
            'frameworks_libraries': {
                'web_frameworks': {
                    'patterns': ['react', 'vue', 'angular', 'django', 'flask', 'express'],
                    'related_skills': ['frontend_development', 'backend_development'],
                    'complexity_indicators': ['state management', 'routing', 'middleware']
                },
                'ai_ml_frameworks': {
                    'patterns': ['tensorflow', 'pytorch', 'scikit-learn', 'transformers'],
                    'related_skills': ['machine_learning', 'data_science', 'ai_development'],
                    'complexity_indicators': ['neural networks', 'fine-tuning', 'model deployment']
                }
            },
            'databases': {
                'sql_databases': {
                    'patterns': ['postgresql', 'mysql', 'sqlite', 'oracle'],
                    'related_skills': ['database_design', 'sql_optimization'],
                    'complexity_indicators': ['indexing', 'query optimization', 'stored procedures']
                },
                'nosql_databases': {
                    'patterns': ['mongodb', 'redis', 'elasticsearch', 'neo4j'],
                    'related_skills': ['data_modeling', 'distributed_systems'],
                    'complexity_indicators': ['sharding', 'replication', 'consistency models']
                }
            },
            'cloud_devops': {
                'cloud_platforms': {
                    'patterns': ['aws', 'azure', 'gcp', 'heroku', 'digitalocean'],
                    'related_skills': ['cloud_architecture', 'devops'],
                    'complexity_indicators': ['microservices', 'containerization', 'serverless']
                },
                'devops_tools': {
                    'patterns': ['docker', 'kubernetes', 'jenkins', 'gitlab', 'terraform'],
                    'related_skills': ['ci_cd', 'infrastructure_as_code'],
                    'complexity_indicators': ['orchestration', 'automation', 'monitoring']
                }
            },
            'ai_ml': {
                'ai_models': {
                    'patterns': ['chatgpt', 'gpt-4', 'claude', 'llama', 'bert'],
                    'related_skills': ['prompt_engineering', 'ai_integration'],
                    'complexity_indicators': ['fine-tuning', 'rag', 'multi-modal']
                },
                'ai_concepts': {
                    'patterns': ['machine learning', 'deep learning', 'nlp', 'computer vision'],
                    'related_skills': ['data_science', 'algorithm_design'],
                    'complexity_indicators': ['neural networks', 'transfer learning', 'model evaluation']
                }
            },
            'architecture': {
                'system_architecture': {
                    'patterns': ['architecture', 'architectural', 'system design', 'design patterns'],
                    'related_skills': ['software_design', 'system_planning'],
                    'complexity_indicators': ['microservices', 'distributed systems', 'scalability']
                },
                'software_design': {
                    'patterns': ['design', 'patterns', 'structure', 'organization'],
                    'related_skills': ['code_organization', 'maintainability'],
                    'complexity_indicators': ['clean code', 'solid principles', 'design patterns']
                }
            },
            'testing': {
                'testing_methods': {
                    'patterns': ['testing', 'test', 'qa', 'quality assurance'],
                    'related_skills': ['test_automation', 'quality_control'],
                    'complexity_indicators': ['unit testing', 'integration testing', 'test-driven development']
                },
                'debugging': {
                    'patterns': ['debugging', 'debug', 'troubleshooting', 'problem solving'],
                    'related_skills': ['error_handling', 'log_analysis'],
                    'complexity_indicators': ['stack traces', 'breakpoints', 'profiling']
                }
            },
            'optimization': {
                'performance_optimization': {
                    'patterns': ['optimization', 'optimize', 'performance', 'efficiency'],
                    'related_skills': ['performance_analysis', 'system_tuning'],
                    'complexity_indicators': ['profiling', 'benchmarking', 'algorithm optimization']
                }
            },
            'problem_solving': {
                'analytical_thinking': {
                    'patterns': ['problem solving', 'problem-solving', 'analysis', 'analytical'],
                    'related_skills': ['critical_thinking', 'logical_reasoning'],
                    'complexity_indicators': ['algorithm design', 'complex problem decomposition']
                }
            }
        }
    
    def analyze_conversation_for_skills(self, conversation_id: str, conversation_content: str) -> List[AISkillAnalysis]:
        """
        Analyze a conversation using AI-enhanced methods to extract skills.
        """
        try:
            # Use enhanced progress system for initial analysis
            progress_event = self.progress_system.analyze_conversation_for_progress(
                conversation_id, conversation_content
            )
            
            # Extract skills from progress event
            detected_skills = []
            for skill_name, skill_points in progress_event.skill_rewards.items():
                # Get or create skill analysis
                skill_analysis = self._get_or_create_skill_analysis(skill_name, conversation_id, conversation_content)
                
                # Create a copy to avoid modifying the cached object
                from copy import deepcopy
                skill_analysis = deepcopy(skill_analysis)
                
                # Update with new evidence
                skill_analysis.conversation_ids.append(conversation_id)
                skill_analysis.evidence.append(f"Detected in conversation: {conversation_id}")
                skill_analysis.last_used = datetime.now()
                
                # Update confidence based on progress event
                skill_analysis.confidence = min(1.0, skill_analysis.confidence + 0.1)
                
                # Analyze skill complexity and relationships
                self._analyze_skill_complexity(skill_analysis, conversation_content)
                self._analyze_skill_relationships(skill_analysis, conversation_content)
                
                detected_skills.append(skill_analysis)
            
            # Cache the analysis
            for skill_analysis in detected_skills:
                self.skill_analysis_cache[skill_analysis.skill_name] = skill_analysis
            
            logger.info(f"AI skill analysis completed for {len(detected_skills)} skills")
            return detected_skills
            
        except Exception as e:
            logger.error(f"Failed to analyze conversation for skills: {e}")
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return []
    
    def analyze_conversation_for_projects(self, conversation_id: str, conversation_content: str) -> List[AIProjectAnalysis]:
        """
        Analyze a conversation for project information using AI-enhanced methods.
        """
        try:
            projects = []
            
            # Use AI patterns to detect projects
            project_patterns = [
                r'\b(build|create|develop|implement|design|architect)\s+(\w+(?:\s+\w+)*)',
                r'\b(project|system|application|platform|tool|framework)\s+(?:called|named)?\s*(\w+(?:\s+\w+)*)',
                r'\b(working on|building|developing)\s+(\w+(?:\s+\w+)*)'
            ]
            
            for pattern in project_patterns:
                matches = re.finditer(pattern, conversation_content, re.IGNORECASE)
                for match in matches:
                    project_name = match.group(2).strip()
                    
                    # Create project analysis
                    project_analysis = AIProjectAnalysis(
                        project_name=project_name,
                        description=self._extract_project_description(conversation_content, project_name),
                        technologies=self._extract_technologies(conversation_content),
                        complexity_level=self._assess_project_complexity(conversation_content),
                        impact_score=self._assess_project_impact(conversation_content),
                        team_size=self._estimate_team_size(conversation_content),
                        role=self._extract_role(conversation_content),
                        duration_days=self._estimate_duration(conversation_content),
                        conversation_ids=[conversation_id],
                        ai_insights=self._generate_project_insights(conversation_content, project_name),
                        achievements=self._extract_achievements(conversation_content)
                    )
                    
                    projects.append(project_analysis)
            
            # Cache the analysis
            for project_analysis in projects:
                cache_key = f"{project_analysis.project_name}_{conversation_id}"
                self.project_analysis_cache[cache_key] = project_analysis
            
            logger.info(f"AI project analysis completed for {len(projects)} projects")
            return projects
            
        except Exception as e:
            logger.error(f"Failed to analyze conversation for projects: {e}")
            return []
    
    def build_enhanced_skill_tree(self) -> Dict[str, Any]:
        """
        Build an enhanced skill tree using AI analysis and conversation data.
        Surfaces all schema fields for downstream UI/graph use.
        """
        try:
            # Get all conversations for analysis
            conversations = self.memory_manager.get_recent_conversations(limit=1000)
            logger.info(f"Analyzing {len(conversations)} conversations for skill tree")
            
            # Analyze all conversations for skills
            all_skills = {}
            for conversation in conversations:
                try:
                    conversation_id = conversation.get('id')
                    conversation_content = conversation.get('content', '')
                    
                    if conversation_content:
                        skills = self.analyze_conversation_for_skills(conversation_id, conversation_content)
                        for skill in skills:
                            if skill.skill_name not in all_skills:
                                all_skills[skill.skill_name] = skill
                            else:
                                # Merge skill data
                                existing = all_skills[skill.skill_name]
                                existing.conversation_ids.extend(skill.conversation_ids)
                                if not isinstance(existing.evidence, list):
                                    existing.evidence = []
                                if not isinstance(skill.evidence, list):
                                    skill.evidence = []
                                existing.evidence.extend(skill.evidence)
                                existing.confidence = max(existing.confidence, skill.confidence)
                except Exception as conv_e:
                    logger.warning(f"Failed to analyze conversation {conversation.get('id', 'unknown')}: {conv_e}")
                    import traceback
                    logger.debug(f"Conversation analysis traceback: {traceback.format_exc()}")
                    continue
            logger.info(f"Found {len(all_skills)} unique skills")
            # Build skill tree structure
            self.graph_backend.nodes.clear()
            self.graph_backend.edges.clear()
            skill_tree = {
                'root_skills': {},
                'skill_relationships': {},
                'learning_paths': {},
                'expertise_areas': {},
                'skill_gaps': {},
                'recommendations': {},
                'nodes': [],  # For knowledge graph
                'edges': []   # For knowledge graph
            }
            # Organize skills by category
            for skill_name, skill_analysis in all_skills.items():
                try:
                    category = skill_analysis.category
                    if category not in skill_tree['root_skills']:
                        skill_tree['root_skills'][category] = []
                    # Create skill tree node
                    skill_node = SkillTreeNode(
                        skill_name=skill_name,
                        level=self._calculate_skill_level(skill_analysis),
                        xp=self._calculate_skill_xp(skill_analysis),
                        category=category,
                        dependencies=self._find_skill_dependencies(skill_analysis, all_skills),
                        unlocks=self._find_skill_unlocks(skill_analysis, all_skills),
                        ai_confidence=skill_analysis.confidence,
                        last_updated=skill_analysis.last_used,
                        metadata={
                            'proficiency_level': skill_analysis.proficiency_level,
                            'evidence_count': len(skill_analysis.evidence),
                            'conversation_count': len(skill_analysis.conversation_ids),
                            'ai_insights': skill_analysis.ai_insights
                        }
                    )
                    skill_tree['root_skills'][category].append(asdict(skill_node))
                    self.skill_tree[skill_name] = skill_node
                    self.graph_backend.add_node(
                        KnowledgeNode(
                            topic=skill_name,
                            category=category,
                            level=skill_node.level,
                            xp=skill_node.xp,
                            dependencies=skill_node.dependencies,
                            last_updated=skill_node.last_updated,
                        )
                    )
                except Exception as skill_e:
                    logger.warning(f"Failed to process skill {skill_name}: {skill_e}")
                    continue
            # Add edges for dependencies and unlocks
            for skill_name, skill_node in self.skill_tree.items():
                for dep in skill_node.dependencies:
                    skill_tree['edges'].append({'source': dep, 'target': skill_name, 'type': 'dependency'})
                    self.graph_backend.add_dependency(dep, skill_name)
                for unlock in skill_node.unlocks:
                    skill_tree['edges'].append({'source': skill_name, 'target': unlock, 'type': 'unlock'})
                    self.graph_backend.add_unlock(skill_name, unlock)
            # Generate skill relationships
            try:
                skill_tree['skill_relationships'] = self._generate_skill_relationships(all_skills)
            except Exception as e:
                logger.warning(f"Failed to generate skill relationships: {e}")
                skill_tree['skill_relationships'] = {}
            # Generate learning paths
            try:
                skill_tree['learning_paths'] = self._generate_learning_paths(all_skills)
            except Exception as e:
                logger.warning(f"Failed to generate learning paths: {e}")
                skill_tree['learning_paths'] = {}
            # Identify expertise areas
            try:
                skill_tree['expertise_areas'] = self._identify_expertise_areas(all_skills)
            except Exception as e:
                logger.warning(f"Failed to identify expertise areas: {e}")
                skill_tree['expertise_areas'] = {}
            # Identify skill gaps
            try:
                skill_tree['skill_gaps'] = self._identify_skill_gaps(all_skills)
            except Exception as e:
                logger.warning(f"Failed to identify skill gaps: {e}")
                skill_tree['skill_gaps'] = {}
            # Generate recommendations
            try:
                skill_tree['recommendations'] = self._generate_recommendations(all_skills)
            except Exception as e:
                logger.warning(f"Failed to generate recommendations: {e}")
                skill_tree['recommendations'] = {}
            logger.info(f"Enhanced skill tree built with {len(all_skills)} skills across {len(skill_tree['root_skills'])} categories")
            return skill_tree
        except Exception as e:
            logger.error(f"Failed to build enhanced skill tree: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'root_skills': {},
                'skill_relationships': {},
                'learning_paths': {},
                'expertise_areas': {},
                'skill_gaps': {},
                'recommendations': {},
                'nodes': [],
                'edges': [],
                'error': str(e)
            }
    
    def generate_enhanced_resume(self, target_role: str = "Software Engineer", 
                               experience_level: str = "mid-level") -> str:
        """
        Generate an enhanced resume using AI analysis and conversation data.
        """
        try:
            # Build skill tree
            skill_tree = self.build_enhanced_skill_tree()
            
            # Get project analysis
            projects = self._get_all_project_analysis()
            
            # Generate resume content
            resume_content = []
            
            # Header
            resume_content.append("# Professional Resume")
            resume_content.append("")
            resume_content.append("*Generated from AI-analyzed conversation data*")
            resume_content.append("")
            
            # Summary
            summary = self._generate_ai_summary(skill_tree, target_role, experience_level)
            resume_content.append("## Professional Summary")
            resume_content.append("")
            resume_content.append(summary)
            resume_content.append("")
            
            # Skills Section
            resume_content.append("## Technical Skills")
            resume_content.append("")
            
            for category, skills in skill_tree['root_skills'].items():
                if skills:
                    resume_content.append(f"### {category.title()}")
                    for skill in skills:
                        level_desc = self._get_skill_level_description(skill['level'])
                        resume_content.append(f"- **{skill['skill_name']}**: {level_desc} (Confidence: {skill['ai_confidence']:.1%})")
                    resume_content.append("")
            
            # Projects Section
            if projects:
                resume_content.append("## Key Projects")
                resume_content.append("")
                
                for project in projects[:5]:  # Top 5 projects
                    resume_content.append(f"### {project.project_name}")
                    resume_content.append(f"**Role**: {project.role} | **Team Size**: {project.team_size} | **Impact**: {project.impact_score:.1%}")
                    resume_content.append("")
                    resume_content.append(project.description)
                    resume_content.append("")
                    resume_content.append(f"**Technologies**: {', '.join(project.technologies)}")
                    resume_content.append("")
            
            # Expertise Areas
            if skill_tree['expertise_areas']:
                resume_content.append("## Areas of Expertise")
                resume_content.append("")
                
                for area, details in skill_tree['expertise_areas'].items():
                    resume_content.append(f"### {area}")
                    resume_content.append(details['description'])
                    resume_content.append("")
            
            # Achievements
            achievements = self._extract_achievements_from_skills(skill_tree)
            if achievements:
                resume_content.append("## Key Achievements")
                resume_content.append("")
                
                for achievement in achievements[:10]:  # Top 10 achievements
                    resume_content.append(f"- {achievement}")
                resume_content.append("")
            
            # Recommendations
            if skill_tree['recommendations']:
                resume_content.append("## Development Recommendations")
                resume_content.append("")
                
                for rec_type, recommendations in skill_tree['recommendations'].items():
                    resume_content.append(f"### {rec_type.title()}")
                    for rec in recommendations[:3]:  # Top 3 recommendations
                        resume_content.append(f"- {rec}")
                    resume_content.append("")
            
            return "\n".join(resume_content)
            
        except Exception as e:
            logger.error(f"Failed to generate enhanced resume: {e}")
            return "# Resume Generation Failed\n\nPlease try again later."
    
    def _get_or_create_skill_analysis(self, skill_name: str, conversation_id: str, 
                                     conversation_content: str) -> AISkillAnalysis:
        """Get existing skill analysis or create new one."""
        if skill_name in self.skill_analysis_cache:
            return self.skill_analysis_cache[skill_name]
        
        # Create new skill analysis
        category = self._categorize_skill(skill_name)
        proficiency = self._assess_proficiency_level(conversation_content, skill_name)
        
        return AISkillAnalysis(
            skill_name=skill_name,
            category=category,
            proficiency_level=proficiency,
            confidence=0.5,  # Base confidence
            evidence=[],
            conversation_ids=[],
            last_used=datetime.now(),
            ai_insights={},
            skill_relationships=[],
            learning_path=[]
        )
    
    def _categorize_skill(self, skill_name: str) -> str:
        """Categorize a skill based on patterns."""
        skill_lower = skill_name.lower()
        
        # First try exact pattern matching
        for category, subcategories in self.enhanced_skill_patterns.items():
            for subcategory, data in subcategories.items():
                if any(pattern in skill_lower for pattern in data['patterns']):
                    return category
        
        # If no exact match, try partial matching
        for category, subcategories in self.enhanced_skill_patterns.items():
            for subcategory, data in subcategories.items():
                for pattern in data['patterns']:
                    if pattern in skill_lower or skill_lower in pattern:
                        return category
        
        # If still no match, try to infer from skill name
        if any(word in skill_lower for word in ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust']):
            return 'programming_languages'
        elif any(word in skill_lower for word in ['react', 'vue', 'angular', 'django', 'flask', 'spring']):
            return 'frameworks_libraries'
        elif any(word in skill_lower for word in ['sql', 'database', 'postgres', 'mysql', 'mongodb']):
            return 'databases'
        elif any(word in skill_lower for word in ['aws', 'azure', 'docker', 'kubernetes', 'devops']):
            return 'cloud_devops'
        elif any(word in skill_lower for word in ['ai', 'ml', 'machine learning', 'neural', 'tensorflow']):
            return 'ai_ml'
        elif any(word in skill_lower for word in ['test', 'testing', 'qa', 'debug']):
            return 'testing'
        elif any(word in skill_lower for word in ['architect', 'design', 'pattern', 'system']):
            return 'architecture'
        else:
            return 'general'
    
    def _assess_proficiency_level(self, content: str, skill_name: str) -> str:
        """Assess proficiency level based on content analysis."""
        skill_lower = skill_name.lower()
        content_lower = content.lower()
        
        # Check for complexity indicators
        complexity_indicators = []
        for category, subcategories in self.enhanced_skill_patterns.items():
            for subcategory, data in subcategories.items():
                if any(pattern in skill_lower for pattern in data['patterns']):
                    complexity_indicators = data.get('complexity_indicators', [])
                    break
        
        # Count complexity indicators in content
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in content_lower)
        
        if complexity_count >= 3:
            return 'expert'
        elif complexity_count >= 2:
            return 'advanced'
        elif complexity_count >= 1:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _analyze_skill_complexity(self, skill_analysis: AISkillAnalysis, content: str):
        """Analyze skill complexity using AI patterns."""
        skill_lower = skill_analysis.skill_name.lower()
        
        for category, subcategories in self.enhanced_skill_patterns.items():
            for subcategory, data in subcategories.items():
                if any(pattern in skill_lower for pattern in data['patterns']):
                    complexity_indicators = data.get('complexity_indicators', [])
                    found_indicators = [indicator for indicator in complexity_indicators if indicator in content.lower()]
                    
                    skill_analysis.ai_insights['complexity_indicators'] = found_indicators
                    skill_analysis.ai_insights['complexity_score'] = len(found_indicators) / len(complexity_indicators)
                    break
    
    def _analyze_skill_relationships(self, skill_analysis: AISkillAnalysis, content: str):
        """Analyze skill relationships using AI patterns."""
        skill_lower = skill_analysis.skill_name.lower()
        
        for category, subcategories in self.enhanced_skill_patterns.items():
            for subcategory, data in subcategories.items():
                if any(pattern in skill_lower for pattern in data['patterns']):
                    related_skills = data.get('related_skills', [])
                    skill_analysis.skill_relationships = related_skills
                    break
    
    def _calculate_skill_level(self, skill_analysis: AISkillAnalysis) -> int:
        """Calculate skill level based on AI analysis."""
        base_level = {
            'beginner': 1,
            'intermediate': 3,
            'advanced': 6,
            'expert': 9
        }.get(skill_analysis.proficiency_level, 1)
        
        # Adjust based on confidence and evidence
        confidence_bonus = int(skill_analysis.confidence * 2)
        evidence_bonus = min(2, len(skill_analysis.evidence) // 5)
        
        return min(10, base_level + confidence_bonus + evidence_bonus)
    
    def _calculate_skill_xp(self, skill_analysis: AISkillAnalysis) -> int:
        """Calculate skill XP based on AI analysis."""
        base_xp = {
            'beginner': 100,
            'intermediate': 500,
            'advanced': 1000,
            'expert': 2000
        }.get(skill_analysis.proficiency_level, 100)
        
        # Adjust based on evidence and confidence
        evidence_multiplier = 1 + (len(skill_analysis.evidence) * 0.1)
        confidence_multiplier = 1 + skill_analysis.confidence
        
        return int(base_xp * evidence_multiplier * confidence_multiplier)
    
    def _find_skill_dependencies(self, skill_analysis: AISkillAnalysis, all_skills: Dict[str, AISkillAnalysis]=None) -> List[str]:
        """Find skill dependencies based on AI analysis and explicit relationships."""
        deps = set(skill_analysis.skill_relationships[:3])
        # If all_skills is provided, check for explicit reverse unlocks
        if all_skills:
            for other_name, other_skill in all_skills.items():
                if skill_analysis.skill_name in getattr(other_skill, 'unlocks', []):
                    deps.add(other_name)
        return list(deps)
    
    def _find_skill_unlocks(self, skill_analysis: AISkillAnalysis, all_skills: Dict[str, AISkillAnalysis]=None) -> List[str]:
        """Find skills that this skill unlocks (AI and explicit)."""
        unlocks = []
        if skill_analysis.proficiency_level in ['advanced', 'expert']:
            unlocks.extend(['Advanced ' + skill_analysis.skill_name, 'Expert ' + skill_analysis.skill_name])
        # If all_skills is provided, check for explicit dependencies
        if all_skills:
            for other_name, other_skill in all_skills.items():
                if skill_analysis.skill_name in getattr(other_skill, 'dependencies', []):
                    unlocks.append(other_name)
        return unlocks
    
    def _generate_skill_relationships(self, all_skills: Dict[str, AISkillAnalysis]) -> Dict[str, List[str]]:
        """Generate skill relationship graph."""
        relationships = {}
        
        for skill_name, skill_analysis in all_skills.items():
            relationships[skill_name] = skill_analysis.skill_relationships
        
        return relationships
    
    def _generate_learning_paths(self, all_skills: Dict[str, AISkillAnalysis]) -> Dict[str, List[str]]:
        """Generate learning paths for skill development."""
        learning_paths = {}
        
        for skill_name, skill_analysis in all_skills.items():
            if skill_analysis.proficiency_level in ['beginner', 'intermediate']:
                # Generate learning path to next level
                path = []
                if skill_analysis.proficiency_level == 'beginner':
                    path = [f"Practice {skill_name}", f"Build projects with {skill_name}", f"Study advanced {skill_name} concepts"]
                elif skill_analysis.proficiency_level == 'intermediate':
                    path = [f"Master advanced {skill_name} features", f"Contribute to {skill_name} projects", f"Teach {skill_name} to others"]
                
                learning_paths[skill_name] = path
        
        return learning_paths
    
    def _identify_expertise_areas(self, all_skills: Dict[str, AISkillAnalysis]) -> Dict[str, Dict[str, Any]]:
        """Identify areas of expertise based on skill analysis."""
        expertise_areas = {}
        
        # Group skills by category
        category_skills = {}
        for skill_name, skill_analysis in all_skills.items():
            category = skill_analysis.category
            if category not in category_skills:
                category_skills[category] = []
            category_skills[category].append(skill_analysis)
        
        # Identify expertise areas
        for category, skills in category_skills.items():
            if len(skills) >= 3:  # Need at least 3 skills in category
                expert_skills = [s for s in skills if s.proficiency_level in ['advanced', 'expert']]
                if len(expert_skills) >= 2:  # Need at least 2 expert skills
                    expertise_areas[category] = {
                        'description': f"Expert in {category} with {len(expert_skills)} advanced skills",
                        'skills': [s.skill_name for s in expert_skills],
                        'confidence': sum(s.confidence for s in expert_skills) / len(expert_skills)
                    }
        
        return expertise_areas
    
    def _identify_skill_gaps(self, all_skills: Dict[str, AISkillAnalysis]) -> Dict[str, List[str]]:
        """Identify skill gaps based on common industry requirements."""
        skill_gaps = {
            'critical_gaps': [],
            'recommended_gaps': [],
            'nice_to_have': []
        }
        
        # Define common skill requirements by category
        common_requirements = {
            'programming_languages': ['python', 'javascript', 'java', 'sql'],
            'frameworks_libraries': ['react', 'django', 'spring', 'tensorflow'],
            'databases': ['postgresql', 'mongodb', 'redis'],
            'cloud_devops': ['aws', 'docker', 'kubernetes'],
            'ai_ml': ['machine learning', 'prompt engineering', 'ai integration']
        }
        
        # Check for gaps
        for category, required_skills in common_requirements.items():
            existing_skills = [s.skill_name.lower() for s in all_skills.values() if s.category == category]
            
            for required_skill in required_skills:
                if required_skill not in existing_skills:
                    if category in ['programming_languages', 'frameworks_libraries']:
                        skill_gaps['critical_gaps'].append(required_skill)
                    elif category in ['databases', 'cloud_devops']:
                        skill_gaps['recommended_gaps'].append(required_skill)
                    else:
                        skill_gaps['nice_to_have'].append(required_skill)
        
        return skill_gaps
    
    def _generate_recommendations(self, all_skills: Dict[str, AISkillAnalysis]) -> Dict[str, List[str]]:
        """Generate recommendations based on skill analysis."""
        recommendations = {
            'skill_development': [],
            'project_ideas': [],
            'learning_resources': [],
            'career_advancement': []
        }
        
        # Skill development recommendations
        for skill_name, skill_analysis in all_skills.items():
            if skill_analysis.proficiency_level == 'beginner':
                recommendations['skill_development'].append(f"Focus on mastering {skill_name} fundamentals")
            elif skill_analysis.proficiency_level == 'intermediate':
                recommendations['skill_development'].append(f"Build advanced projects using {skill_name}")
        
        # Project ideas based on skills
        expert_skills = [s.skill_name for s in all_skills.values() if s.proficiency_level in ['advanced', 'expert']]
        if len(expert_skills) >= 2:
            recommendations['project_ideas'].append(f"Build a full-stack application using {', '.join(expert_skills[:2])}")
        
        # Learning resources
        for skill_name, skill_analysis in all_skills.items():
            if skill_analysis.proficiency_level in ['beginner', 'intermediate']:
                recommendations['learning_resources'].append(f"Take advanced courses in {skill_name}")
        
        # Career advancement
        if len([s for s in all_skills.values() if s.proficiency_level == 'expert']) >= 3:
            recommendations['career_advancement'].append("Consider senior/lead developer positions")
        
        return recommendations
    
    def _get_all_project_analysis(self) -> List[AIProjectAnalysis]:
        """Get all project analysis from cache."""
        return list(self.project_analysis_cache.values())
    
    def _generate_ai_summary(self, skill_tree: Dict[str, Any], target_role: str, 
                           experience_level: str) -> str:
        """Generate AI-powered professional summary."""
        expertise_areas = skill_tree.get('expertise_areas', {})
        total_skills = len(skill_tree.get('root_skills', {}))
        
        summary_parts = [
            f"Experienced {target_role} with expertise in {len(expertise_areas)} key areas",
            f"Demonstrated proficiency across {total_skills} technical skills",
            "Strong background in software development and system architecture"
        ]
        
        if expertise_areas:
            top_areas = list(expertise_areas.keys())[:3]
            summary_parts.append(f"Specialized in {', '.join(top_areas)}")
        
        summary_parts.append("Proven track record of delivering high-impact projects and solutions")
        
        return " ".join(summary_parts) + "."
    
    def _get_skill_level_description(self, level: int) -> str:
        """Get human-readable skill level description."""
        if level >= 9:
            return "Expert"
        elif level >= 6:
            return "Advanced"
        elif level >= 3:
            return "Intermediate"
        else:
            return "Beginner"
    
    def _extract_achievements_from_skills(self, skill_tree: Dict[str, Any]) -> List[str]:
        """Extract achievements from skill analysis."""
        achievements = []
        
        for category, skills in skill_tree.get('root_skills', {}).items():
            expert_skills = [s for s in skills if s['level'] >= 8]
            if expert_skills:
                achievements.append(f"Mastered {len(expert_skills)} {category} skills")
        
        expertise_areas = skill_tree.get('expertise_areas', {})
        for area, details in expertise_areas.items():
            achievements.append(f"Developed expertise in {area} with {details['confidence']:.1%} confidence")
        
        return achievements
    
    # Helper methods for project analysis
    def _extract_project_description(self, content: str, project_name: str) -> str:
        """Extract project description from content."""
        # Simple extraction - in reality, this would use more sophisticated NLP
        sentences = content.split('.')
        project_sentences = [s for s in sentences if project_name.lower() in s.lower()]
        
        if project_sentences:
            return project_sentences[0].strip()
        else:
            return f"Project involving {project_name}"
    
    def _extract_technologies(self, content: str) -> List[str]:
        """Extract technologies from content."""
        technologies = []
        
        for category, subcategories in self.enhanced_skill_patterns.items():
            for subcategory, data in subcategories.items():
                for pattern in data['patterns']:
                    if pattern in content.lower():
                        technologies.append(pattern.title())
        
        return list(set(technologies))  # Remove duplicates
    
    def _assess_project_complexity(self, content: str) -> str:
        """Assess project complexity based on content."""
        complexity_indicators = ['microservices', 'distributed', 'scalable', 'enterprise', 'architectural']
        found_indicators = sum(1 for indicator in complexity_indicators if indicator in content.lower())
        
        if found_indicators >= 3:
            return 'enterprise'
        elif found_indicators >= 2:
            return 'complex'
        elif found_indicators >= 1:
            return 'moderate'
        else:
            return 'simple'
    
    def _assess_project_impact(self, content: str) -> float:
        """Assess project impact score (0.0 to 1.0)."""
        impact_indicators = ['improved', 'increased', 'reduced', 'optimized', 'enhanced', 'solved']
        found_indicators = sum(1 for indicator in impact_indicators if indicator in content.lower())
        
        return min(1.0, found_indicators / 3.0)
    
    def _estimate_team_size(self, content: str) -> int:
        """Estimate team size from content."""
        team_indicators = ['team', 'collaborate', 'we', 'us', 'together']
        found_indicators = sum(1 for indicator in team_indicators if indicator in content.lower())
        
        if found_indicators >= 3:
            return 5  # Medium team
        elif found_indicators >= 1:
            return 3  # Small team
        else:
            return 1  # Solo
    
    def _extract_role(self, content: str) -> str:
        """Extract role from content."""
        role_indicators = {
            'lead': ['lead', 'senior', 'principal', 'architect'],
            'developer': ['developer', 'programmer', 'engineer'],
            'manager': ['manager', 'director', 'head']
        }
        
        content_lower = content.lower()
        for role, indicators in role_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                return role.title()
        
        return "Developer"
    
    def _estimate_duration(self, content: str) -> int:
        """Estimate project duration in days."""
        duration_indicators = ['weeks', 'months', 'years', 'long-term', 'ongoing']
        found_indicators = sum(1 for indicator in duration_indicators if indicator in content.lower())
        
        if found_indicators >= 2:
            return 90  # 3 months
        elif found_indicators >= 1:
            return 30  # 1 month
        else:
            return 7  # 1 week
    
    def _generate_project_insights(self, content: str, project_name: str) -> Dict[str, Any]:
        """Generate AI insights for project."""
        return {
            'complexity_score': self._assess_project_complexity(content),
            'impact_score': self._assess_project_impact(content),
            'team_collaboration': 'team' in content.lower(),
            'technical_challenges': len([w for w in content.lower().split() if w in ['challenge', 'problem', 'issue', 'bug']])
        }
    
    def _extract_achievements(self, content: str) -> List[str]:
        """Extract achievements from content."""
        achievement_patterns = [
            r'successfully\s+(\w+(?:\s+\w+)*)',
            r'achieved\s+(\w+(?:\s+\w+)*)',
            r'improved\s+(\w+(?:\s+\w+)*)',
            r'reduced\s+(\w+(?:\s+\w+)*)'
        ]
        
        achievements = []
        for pattern in achievement_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                achievements.append(match.group(0))
        
        return achievements[:5]  # Limit to top 5 achievements 

    def get_knowledge_graph(self) -> Dict[str, Any]:
        """Return a node/edge list representing the current knowledge graph."""
        return self.graph_backend.get_graph()