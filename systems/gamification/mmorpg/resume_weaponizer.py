#!/usr/bin/env python3
"""
Dream.OS Resume Weaponizer
==========================

Automatically extracts skills, projects, and knowledge from conversation corpus
to build comprehensive resumes and skill databases.
"""

import json
import logging
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path

from dreamscape.core.memory import MemoryManager
from .resume_tracker import ResumeTracker
from .models import Achievement, Skill, Project
from .template_engine import render_template

logger = logging.getLogger(__name__)

@dataclass
class ExtractedSkill:
    """Extracted skill from conversation."""
    name: str
    category: str
    confidence: float
    evidence: List[str]
    conversation_ids: List[str]
    last_used: str
    proficiency_level: str  # 'beginner', 'intermediate', 'advanced', 'expert'

@dataclass
class ExtractedProject:
    """Extracted project from conversation."""
    name: str
    description: str
    technologies: List[str]
    start_date: str
    end_date: Optional[str]
    status: str
    impact: str
    conversation_ids: List[str]
    team_size: int
    role: str

@dataclass
class ExtractedKnowledge:
    """Extracted knowledge from conversation."""
    topic: str
    category: str
    description: str
    key_points: List[str]
    conversation_ids: List[str]
    confidence: float
    last_updated: str

class ResumeWeaponizer:
    """
    Weaponizes conversation corpus to extract resume-worthy content.
    """
    
    def __init__(self, memory_manager: MemoryManager, resume_tracker: ResumeTracker):
        """
        Initialize the resume weaponizer.
        
        Args:
            memory_manager: Memory manager for conversation access
            resume_tracker: Resume tracker for storing extracted data
        """
        self.memory_manager = memory_manager
        self.resume_tracker = resume_tracker
        
        # Skill extraction patterns
        self.skill_patterns = {
            'technical': {
                'programming_languages': [
                    r'\b(python|javascript|typescript|java|c\+\+|c#|go|rust|php|ruby|swift|kotlin)\b',
                    r'\b(html|css|sql|bash|powershell|docker|kubernetes)\b'
                ],
                'frameworks': [
                    r'\b(react|vue|angular|node\.js|express|django|flask|fastapi|spring|laravel)\b',
                    r'\b(tensorflow|pytorch|scikit-learn|pandas|numpy|matplotlib)\b'
                ],
                'databases': [
                    r'\b(postgresql|mysql|mongodb|redis|sqlite|elasticsearch|neo4j)\b'
                ],
                'cloud_platforms': [
                    r'\b(aws|azure|gcp|heroku|digitalocean|vercel|netlify)\b'
                ],
                'tools': [
                    r'\b(git|docker|jenkins|github|gitlab|jira|confluence|figma)\b'
                ]
            },
            'ai_ml': {
                'ai_models': [
                    r'\b(chatgpt|gpt-4|gpt-3|claude|bard|llama|bert|transformer)\b'
                ],
                'ai_concepts': [
                    r'\b(prompt engineering|fine-tuning|embedding|vector|semantic search)\b',
                    r'\b(machine learning|deep learning|neural network|nlp|computer vision)\b'
                ],
                'ai_tools': [
                    r'\b(openai|anthropic|hugging face|langchain|pinecone|weaviate)\b'
                ]
            },
            'soft_skills': {
                'leadership': [
                    r'\b(lead|manage|coordinate|mentor|guide|supervise|delegate)\b'
                ],
                'communication': [
                    r'\b(present|explain|document|teach|collaborate|negotiate)\b'
                ],
                'problem_solving': [
                    r'\b(debug|troubleshoot|analyze|optimize|improve|solve)\b'
                ],
                'project_management': [
                    r'\b(plan|organize|schedule|track|monitor|deliver)\b'
                ]
            }
        }
        
        # Project extraction patterns
        self.project_patterns = {
            'project_indicators': [
                r'\b(build|create|develop|implement|design|architect)\s+(\w+(?:\s+\w+)*)',
                r'\b(project|system|application|platform|tool|framework)\s+(?:called|named)?\s*(\w+(?:\s+\w+)*)',
                r'\b(working on|building|developing)\s+(\w+(?:\s+\w+)*)'
            ],
            'technology_indicators': [
                r'\b(using|with|built in|developed with)\s+(\w+(?:\s+\w+)*)',
                r'\b(tech stack|technology|framework|library|tool)\s*[:\-]\s*(\w+(?:\s+\w+)*)'
            ]
        }
        
        # Knowledge extraction patterns
        self.knowledge_patterns = {
            'concept_indicators': [
                r'\b(learned|discovered|found out|realized)\s+(\w+(?:\s+\w+)*)',
                r'\b(understanding|knowledge|expertise|experience)\s+(?:in|with)\s+(\w+(?:\s+\w+)*)',
                r'\b(studied|researched|explored)\s+(\w+(?:\s+\w+)*)'
            ]
        }
    
    def weaponize_corpus(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Main weaponization pipeline - extracts all resume content from corpus.
        
        Args:
            limit: Optional limit on number of conversations to process
            
        Returns:
            Dictionary with extracted skills, projects, and knowledge
        """
        logger.info("🚀 Starting Resume Weaponization Pipeline")
        
        try:
            # Get conversations to process
            conversations = self.memory_manager.get_all_conversations()
            if limit:
                conversations = conversations[:limit]
            
            logger.info(f"📊 Processing {len(conversations)} conversations")
            
            # Extract content
            extracted_skills = self._extract_skills_from_corpus(conversations)
            extracted_projects = self._extract_projects_from_corpus(conversations)
            extracted_knowledge = self._extract_knowledge_from_corpus(conversations)
            
            # Store in resume tracker
            self._store_extracted_content(extracted_skills, extracted_projects, extracted_knowledge)
            
            # Generate comprehensive resume
            resume_content = self._generate_comprehensive_resume(
                extracted_skills, extracted_projects, extracted_knowledge
            )
            
            # Create skill tree/knowledge database
            skill_tree = self._create_skill_tree(extracted_skills, extracted_knowledge)
            
            result = {
                'skills_extracted': len(extracted_skills),
                'projects_extracted': len(extracted_projects),
                'knowledge_extracted': len(extracted_knowledge),
                'resume_content': resume_content,
                'skill_tree': skill_tree,
                'summary': self._generate_summary(extracted_skills, extracted_projects, extracted_knowledge)
            }
            
            logger.info(f"✅ Resume Weaponization Complete: {result['skills_extracted']} skills, {result['projects_extracted']} projects")
            return result
            
        except Exception as e:
            logger.error(f"❌ Resume weaponization failed: {e}")
            raise
    
    def generate_resume(self, config: Dict[str, Any]) -> str:
        """
        Generate a resume based on configuration and extracted data.
        
        Args:
            config: Configuration dictionary with name, email, preferences, etc.
            
        Returns:
            Generated resume content as string
        """
        try:
            # Get current extracted data
            skills = self.resume_tracker.get_skills()
            projects = self.resume_tracker.get_projects()
            
            # Convert to extracted format for resume generation
            extracted_skills = []
            for skill in skills:
                extracted_skills.append(ExtractedSkill(
                    name=skill.name,
                    category=skill.category,
                    confidence=0.8,  # Default confidence
                    evidence=[],
                    conversation_ids=[],
                    last_used=skill.last_updated,
                    proficiency_level=self._get_proficiency_level(skill.current_level)
                ))
            
            extracted_projects = []
            for project in projects:
                extracted_projects.append(ExtractedProject(
                    name=project.name,
                    description=project.description,
                    technologies=project.technologies,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    status=project.status,
                    impact=project.impact_description or "Medium",
                    conversation_ids=[],
                    team_size=project.team_size,
                    role=project.role
                ))
            
            # Generate resume content
            resume_content = self._generate_comprehensive_resume(
                extracted_skills, extracted_projects, []
            )
            
            # Customize based on config
            if config.get('name'):
                resume_content = resume_content.replace("# Resume", f"# {config['name']}")
            
            if config.get('email'):
                # Add contact info if not present
                if "Contact Information" not in resume_content:
                    contact_section = f"\n## Contact Information\n- Email: {config['email']}\n"
                    if config.get('phone'):
                        contact_section += f"- Phone: {config['phone']}\n"
                    if config.get('location'):
                        contact_section += f"- Location: {config['location']}\n"
                    
                    # Insert after title
                    lines = resume_content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('# ') and not line.startswith('## '):
                            lines.insert(i + 1, contact_section)
                            break
                    resume_content = '\n'.join(lines)
            
            return resume_content
            
        except Exception as e:
            logger.error(f"❌ Resume generation failed: {e}")
            return f"# {config.get('name', 'Resume')}\n\nError generating resume: {e}"
    
    def _get_proficiency_level(self, level: int) -> str:
        """Convert skill level to proficiency description."""
        if level >= 8:
            return "expert"
        elif level >= 6:
            return "advanced"
        elif level >= 4:
            return "intermediate"
        else:
            return "beginner"
    
    def _extract_skills_from_corpus(self, conversations: List[Dict]) -> List[ExtractedSkill]:
        """Extract skills from conversation corpus."""
        skills_dict = {}
        
        for conv in conversations:
            conv_id = conv['id']
            content = conv.get('content', '')
            title = conv.get('title', '')
            full_text = f"{title} {content}".lower()
            
            # Extract skills by category
            for category, patterns in self.skill_patterns.items():
                for skill_type, regex_patterns in patterns.items():
                    for pattern in regex_patterns:
                        matches = re.finditer(pattern, full_text, re.IGNORECASE)
                        for match in matches:
                            skill_name = match.group(0).title()
                            
                            if skill_name not in skills_dict:
                                skills_dict[skill_name] = ExtractedSkill(
                                    name=skill_name,
                                    category=category,
                                    confidence=0.0,
                                    evidence=[],
                                    conversation_ids=[],
                                    last_used=conv.get('created_at', ''),
                                    proficiency_level='intermediate'
                                )
                            
                            skill = skills_dict[skill_name]
                            skill.conversation_ids.append(conv_id)
                            skill.evidence.append(f"Found in: {title}")
                            
                            # Update confidence based on frequency
                            skill.confidence = min(1.0, len(skill.conversation_ids) * 0.1)
                            
                            # Update proficiency based on context
                            if len(skill.conversation_ids) > 5:
                                skill.proficiency_level = 'advanced'
                            if len(skill.conversation_ids) > 10:
                                skill.proficiency_level = 'expert'
        
        return list(skills_dict.values())
    
    def _extract_projects_from_corpus(self, conversations: List[Dict]) -> List[ExtractedProject]:
        """Extract projects from conversation corpus."""
        projects_dict = {}
        
        for conv in conversations:
            conv_id = conv['id']
            content = conv.get('content', '')
            title = conv.get('title', '')
            
            # Look for project indicators
            for pattern in self.project_patterns['project_indicators']:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    project_name = match.group(2).title()
                    
                    if project_name not in projects_dict:
                        # Extract technologies
                        technologies = self._extract_technologies_from_content(content)
                        
                        projects_dict[project_name] = ExtractedProject(
                            name=project_name,
                            description=self._generate_project_description(content, project_name),
                            technologies=technologies,
                            start_date=conv.get('created_at', ''),
                            end_date=None,
                            status='active',
                            impact=self._assess_project_impact(content),
                            conversation_ids=[conv_id],
                            team_size=self._estimate_team_size(content),
                            role='Developer'
                        )
                    else:
                        projects_dict[project_name].conversation_ids.append(conv_id)
        
        return list(projects_dict.values())
    
    def _extract_knowledge_from_corpus(self, conversations: List[Dict]) -> List[ExtractedKnowledge]:
        """Extract knowledge from conversation corpus."""
        knowledge_dict = {}
        
        for conv in conversations:
            conv_id = conv['id']
            content = conv.get('content', '')
            
            # Look for knowledge indicators
            for pattern in self.knowledge_patterns['concept_indicators']:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    topic = match.group(2).title()
                    
                    if topic not in knowledge_dict:
                        knowledge_dict[topic] = ExtractedKnowledge(
                            topic=topic,
                            category=self._categorize_knowledge(topic),
                            description=self._extract_knowledge_description(content, topic),
                            key_points=self._extract_key_points(content),
                            conversation_ids=[conv_id],
                            confidence=0.5,
                            last_updated=conv.get('created_at', '')
                        )
                    else:
                        knowledge_dict[topic].conversation_ids.append(conv_id)
                        knowledge_dict[topic].confidence = min(1.0, len(knowledge_dict[topic].conversation_ids) * 0.1)
        
        return list(knowledge_dict.values())
    
    def _extract_technologies_from_content(self, content: str) -> List[str]:
        """Extract technologies mentioned in content."""
        technologies = []
        tech_patterns = [
            r'\b(python|javascript|react|node\.js|django|flask|postgresql|mongodb|aws|docker)\b',
            r'\b(git|github|jenkins|jira|figma|chatgpt|openai|tensorflow|pandas)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            technologies.extend([match.title() for match in matches])
        
        return list(set(technologies))
    
    def _generate_project_description(self, content: str, project_name: str) -> str:
        """Generate project description from content."""
        # Look for sentences mentioning the project
        sentences = re.split(r'[.!?]+', content)
        project_sentences = []
        
        for sentence in sentences:
            if project_name.lower() in sentence.lower():
                project_sentences.append(sentence.strip())
        
        if project_sentences:
            return project_sentences[0][:200] + "..."
        
        return f"Project involving {project_name.lower()}"
    
    def _assess_project_impact(self, content: str) -> str:
        """Assess project impact from content."""
        impact_keywords = {
            'high': ['significant', 'major', 'critical', 'important', 'successful'],
            'medium': ['improved', 'enhanced', 'optimized', 'streamlined'],
            'low': ['basic', 'simple', 'minor', 'small']
        }
        
        content_lower = content.lower()
        for impact_level, keywords in impact_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return impact_level
        
        return 'medium'
    
    def _estimate_team_size(self, content: str) -> int:
        """Estimate team size from content."""
        team_indicators = [
            r'\b(team|collaborate|partner|colleague)\b',
            r'\b(we|us|our)\b',
            r'\b(developer|engineer|designer|manager)\b'
        ]
        
        team_mentions = 0
        for pattern in team_indicators:
            team_mentions += len(re.findall(pattern, content, re.IGNORECASE))
        
        if team_mentions > 5:
            return 3
        elif team_mentions > 2:
            return 2
        else:
            return 1
    
    def _categorize_knowledge(self, topic: str) -> str:
        """Categorize knowledge topic."""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['ai', 'ml', 'machine learning', 'neural']):
            return 'AI/ML'
        elif any(word in topic_lower for word in ['web', 'frontend', 'backend', 'api']):
            return 'Web Development'
        elif any(word in topic_lower for word in ['database', 'sql', 'nosql']):
            return 'Database'
        elif any(word in topic_lower for word in ['cloud', 'aws', 'azure', 'deployment']):
            return 'DevOps'
        else:
            return 'General'
    
    def _extract_knowledge_description(self, content: str, topic: str) -> str:
        """Extract knowledge description from content."""
        sentences = re.split(r'[.!?]+', content)
        topic_sentences = []
        
        for sentence in sentences:
            if topic.lower() in sentence.lower():
                topic_sentences.append(sentence.strip())
        
        if topic_sentences:
            return topic_sentences[0][:150] + "..."
        
        return f"Knowledge about {topic.lower()}"
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content."""
        key_points = []
        
        # Look for bullet points or numbered lists
        bullet_patterns = [
            r'^\s*[-*•]\s+(.+)$',
            r'^\s*\d+\.\s+(.+)$'
        ]
        
        lines = content.split('\n')
        for line in lines:
            for pattern in bullet_patterns:
                match = re.match(pattern, line)
                if match:
                    key_points.append(match.group(1).strip())
                    break
        
        return key_points[:5]  # Limit to 5 key points
    
    def _store_extracted_content(self, skills: List[ExtractedSkill], 
                               projects: List[ExtractedProject], 
                               knowledge: List[ExtractedKnowledge]):
        """Store extracted content in resume tracker."""
        try:
            # Store skills
            for skill in skills:
                if skill.confidence > 0.3:  # Only store confident skills
                    self.resume_tracker.add_skill(
                        name=skill.name,
                        category=skill.category,
                        current_level=min(100, int(skill.confidence * 100)),
                        description=f"Extracted from {len(skill.conversation_ids)} conversations"
                    )
            
            # Store projects
            for project in projects:
                self.resume_tracker.add_project(
                    name=project.name,
                    description=project.description,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    status=project.status,
                    technologies=project.technologies,
                    impact_description=project.impact,
                    team_size=project.team_size,
                    role=project.role
                )
            
            # Store achievements for high-confidence skills
            for skill in skills:
                if skill.confidence > 0.7:
                    self.resume_tracker.add_achievement(
                        name=f"Mastered {skill.name}",
                        description=f"Demonstrated expertise in {skill.name} across {len(skill.conversation_ids)} conversations",
                        category="skill",
                        difficulty=3,
                        xp_reward=50,
                        evidence=f"Conversation IDs: {', '.join(skill.conversation_ids[:5])}"
                    )
            
            logger.info(f"✅ Stored {len(skills)} skills, {len(projects)} projects in resume tracker")
            
        except Exception as e:
            logger.error(f"❌ Failed to store extracted content: {e}")
    
    def _generate_comprehensive_resume(self, skills: List[ExtractedSkill], 
                                     projects: List[ExtractedProject], 
                                     knowledge: List[ExtractedKnowledge]) -> str:
        """Generate comprehensive resume from extracted content."""
        try:
            # Group skills by category
            skill_categories = {}
            for skill in skills:
                if skill.category not in skill_categories:
                    skill_categories[skill.category] = []
                skill_categories[skill.category].append(skill)
            
            # Generate resume sections
            resume_sections = []
            
            # Skills section
            resume_sections.append("## Skills")
            for category, category_skills in skill_categories.items():
                resume_sections.append(f"\n### {category.title()}")
                for skill in sorted(category_skills, key=lambda x: x.confidence, reverse=True)[:10]:
                    resume_sections.append(f"- **{skill.name}**: {skill.proficiency_level.title()} ({skill.confidence:.1%} confidence)")
            
            # Projects section
            resume_sections.append("\n## Projects")
            for project in sorted(projects, key=lambda x: len(x.conversation_ids), reverse=True)[:10]:
                resume_sections.append(f"\n### {project.name}")
                resume_sections.append(f"**Technologies:** {', '.join(project.technologies)}")
                resume_sections.append(f"**Description:** {project.description}")
                resume_sections.append(f"**Impact:** {project.impact.title()}")
                resume_sections.append(f"**Team Size:** {project.team_size} people")
            
            # Knowledge section
            resume_sections.append("\n## Knowledge Areas")
            knowledge_by_category = {}
            for knowledge_item in knowledge:
                if knowledge_item.category not in knowledge_by_category:
                    knowledge_by_category[knowledge_item.category] = []
                knowledge_by_category[knowledge_item.category].append(knowledge_item)
            
            for category, category_knowledge in knowledge_by_category.items():
                resume_sections.append(f"\n### {category}")
                for item in sorted(category_knowledge, key=lambda x: x.confidence, reverse=True)[:5]:
                    resume_sections.append(f"- **{item.topic}**: {item.description}")
            
            return "\n".join(resume_sections)
            
        except Exception as e:
            logger.error(f"❌ Failed to generate resume: {e}")
            return f"Error generating resume: {e}"
    
    def _create_skill_tree(self, skills: List[ExtractedSkill], 
                          knowledge: List[ExtractedKnowledge]) -> Dict[str, Any]:
        """Create skill tree/knowledge database structure."""
        skill_tree = {
            'technical': {
                'programming_languages': [],
                'frameworks': [],
                'databases': [],
                'cloud_platforms': [],
                'tools': []
            },
            'ai_ml': {
                'ai_models': [],
                'ai_concepts': [],
                'ai_tools': []
            },
            'soft_skills': {
                'leadership': [],
                'communication': [],
                'problem_solving': [],
                'project_management': []
            },
            'knowledge_areas': {}
        }
        
        # Populate skill tree
        for skill in skills:
            if skill.confidence > 0.3:
                skill_info = {
                    'name': skill.name,
                    'proficiency': skill.proficiency_level,
                    'confidence': skill.confidence,
                    'evidence_count': len(skill.conversation_ids)
                }
                
                # Map to appropriate category
                if skill.category in skill_tree:
                    for subcategory in skill_tree[skill.category]:
                        if any(pattern in skill.name.lower() for pattern in self.skill_patterns[skill.category].get(subcategory, [])):
                            skill_tree[skill.category][subcategory].append(skill_info)
                            break
        
        # Add knowledge areas
        for knowledge_item in knowledge:
            if knowledge_item.category not in skill_tree['knowledge_areas']:
                skill_tree['knowledge_areas'][knowledge_item.category] = []
            
            skill_tree['knowledge_areas'][knowledge_item.category].append({
                'topic': knowledge_item.topic,
                'description': knowledge_item.description,
                'confidence': knowledge_item.confidence,
                'key_points': knowledge_item.key_points
            })
        
        return skill_tree
    
    def _generate_summary(self, skills: List[ExtractedSkill], 
                         projects: List[ExtractedProject], 
                         knowledge: List[ExtractedKnowledge]) -> str:
        """Generate summary of weaponization results."""
        total_skills = len(skills)
        high_confidence_skills = len([s for s in skills if s.confidence > 0.7])
        total_projects = len(projects)
        total_knowledge = len(knowledge)
        
        summary = f"""
## Resume Weaponization Summary

### Skills Extracted
- **Total Skills:** {total_skills}
- **High Confidence:** {high_confidence_skills}
- **Categories:** {len(set(s.category for s in skills))}

### Projects Identified
- **Total Projects:** {total_projects}
- **Active Projects:** {len([p for p in projects if p.status == 'active'])}

### Knowledge Areas
- **Total Knowledge Items:** {total_knowledge}
- **Categories:** {len(set(k.category for k in knowledge))}

### Top Skills by Confidence
{chr(10).join([f"- {s.name} ({s.confidence:.1%})" for s in sorted(skills, key=lambda x: x.confidence, reverse=True)[:10]])}

### Most Referenced Projects
{chr(10).join([f"- {p.name} ({len(p.conversation_ids)} conversations)" for p in sorted(projects, key=lambda x: len(x.conversation_ids), reverse=True)[:5]])}
"""
        
        return summary
    
    def generate_resume_prompt(self, target_role: str = "Software Engineer") -> str:
        """
        Generate a ChatGPT prompt to create a resume based on extracted content.
        
        Args:
            target_role: Target role for the resume
            
        Returns:
            Formatted prompt for ChatGPT
        """
        try:
            # Get current resume data
            skills = self.resume_tracker.get_skills()
            projects = self.resume_tracker.get_projects()
            achievements = self.resume_tracker.get_achievements()
            
            # Handle case where no data is available
            if not skills and not projects and not achievements:
                return f"""
# Resume Generation Request

## Target Role: {target_role}

## Available Data:
No skills, projects, or achievements have been extracted yet.

## Instructions:
Please create a professional resume for the {target_role} position. Since no specific data is available, focus on:

1. General technical skills relevant to the role
2. Professional experience and education
3. Key accomplishments and achievements
4. Professional formatting and structure

Please format the resume in Markdown and include all relevant sections (Summary, Skills, Experience, Projects, Education).

Note: Run the resume weaponization process first to extract specific skills and projects from your conversation corpus.
"""
            
            prompt = f"""
# Resume Generation Request

## Target Role: {target_role}

## Available Skills ({len(skills)} total):
{chr(10).join([f"- {s.name} (Level {s.current_level}/{s.max_level})" for s in skills[:20]])}

## Available Projects ({len(projects)} total):
{chr(10).join([f"- {p.name}: {p.description[:100]}..." for p in projects[:10]])}

## Available Achievements ({len(achievements)} total):
{chr(10).join([f"- {a.name}: {a.description}" for a in achievements[:10]])}

## Instructions:
Please create a professional resume for the {target_role} position using the skills, projects, and achievements listed above. 

Focus on:
1. Relevant technical skills for the role
2. Projects that demonstrate problem-solving and technical expertise
3. Quantifiable achievements and impact
4. Professional formatting and structure

Please format the resume in Markdown and include all relevant sections (Summary, Skills, Experience, Projects, Education).
"""
            
            return prompt
            
        except Exception as e:
            logger.error(f"❌ Failed to generate resume prompt: {e}")
            return f"Error generating prompt: {e}"
    
    def export_skill_database(self, output_path: str = "outputs/skill_database.json"):
        """Export skill database to JSON file."""
        try:
            skills = self.resume_tracker.get_skills()
            projects = self.resume_tracker.get_projects()
            achievements = self.resume_tracker.get_achievements()
            
            skill_database = {
                'metadata': {
                    'exported_at': datetime.now().isoformat(),
                    'total_skills': len(skills),
                    'total_projects': len(projects),
                    'total_achievements': len(achievements)
                },
                'skills': [asdict(skill) for skill in skills],
                'projects': [asdict(project) for project in projects],
                'achievements': [asdict(achievement) for achievement in achievements]
            }
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(skill_database, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Skill database exported to {output_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to export skill database: {e}")
            raise 