#!/usr/bin/env python3
"""
MMORPG Resume Weaponizer
========================

This module contains ONLY resume optimization and weaponization logic.
Following the Single Responsibility Principle - this module only handles resume targeting and optimization.
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..models import ResumeSkill, Project, Achievement

class ResumeWeaponizer:
    """
    Optimizes resumes for specific job roles and requirements.
    """
    
    def __init__(self):
        """Initialize the resume weaponizer."""
        self.role_keywords = {
            "software_engineer": ["coding", "programming", "development", "software", "code", "debug", "test"],
            "data_scientist": ["data", "analysis", "machine learning", "statistics", "python", "r", "sql"],
            "devops_engineer": ["deployment", "ci/cd", "docker", "kubernetes", "aws", "cloud", "infrastructure"],
            "product_manager": ["product", "management", "strategy", "roadmap", "user experience", "market"],
            "ui_ux_designer": ["design", "user interface", "user experience", "prototype", "wireframe", "figma"],
            "security_engineer": ["security", "cybersecurity", "penetration testing", "vulnerability", "compliance"],
            "system_architect": ["architecture", "system design", "scalability", "performance", "integration"],
            "qa_engineer": ["testing", "quality assurance", "automation", "test cases", "bug tracking"],
            "full_stack_developer": ["frontend", "backend", "full stack", "web development", "javascript", "python"],
            "mobile_developer": ["mobile", "ios", "android", "react native", "swift", "kotlin"]
        }
        
    def weaponize_resume(self, skills: List[ResumeSkill], projects: List[Project], achievements: List[Achievement], target_role: str = "Software Engineer") -> Dict[str, Any]:
        """
        Optimize resume content for a specific target role.
        
        Args:
            skills: List of skills to optimize
            projects: List of projects to optimize
            achievements: List of achievements to optimize
            target_role: The target job role
            
        Returns:
            Dictionary containing weaponized resume data and optimization metrics
        """
        role_keywords = self._extract_role_keywords(target_role)
        
        # Weaponize each component
        weaponized_skills = self._weaponize_skills(skills, target_role)
        weaponized_projects = self._weaponize_projects(projects, target_role)
        weaponized_achievements = self._weaponize_achievements(achievements, target_role)
        
        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(
            weaponized_skills, weaponized_projects, weaponized_achievements, target_role
        )
        
        return {
            "target_role": target_role,
            "role_keywords": role_keywords,
            "weaponized_skills": weaponized_skills,
            "weaponized_projects": weaponized_projects,
            "weaponized_achievements": weaponized_achievements,
            "optimization_score": optimization_score,
            "optimization_timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_recommendations(optimization_score, role_keywords)
        }
        
    def _weaponize_skills(self, skills: List[ResumeSkill], target_role: str) -> List[Dict[str, Any]]:
        """Optimize skills for the target role."""
        role_keywords = self._extract_role_keywords(target_role)
        weaponized_skills = []
        
        for skill in skills:
            relevance_score = self._calculate_skill_relevance(skill.name, role_keywords)
            
            weaponized_skill = {
                "original_skill": skill,
                "relevance_score": relevance_score,
                "optimization_suggestions": [],
                "priority": "high" if relevance_score > 0.7 else "medium" if relevance_score > 0.4 else "low"
            }
            
            # Generate optimization suggestions
            if relevance_score < 0.5:
                weaponized_skill["optimization_suggestions"].append(
                    f"Consider highlighting related {target_role.lower()} skills"
                )
            elif relevance_score > 0.8:
                weaponized_skill["optimization_suggestions"].append(
                    "This skill is highly relevant - emphasize it prominently"
                )
                
            weaponized_skills.append(weaponized_skill)
            
        # Sort by relevance score (highest first)
        weaponized_skills.sort(key=lambda x: x["relevance_score"], reverse=True)
        return weaponized_skills
        
    def _weaponize_projects(self, projects: List[Project], target_role: str) -> List[Dict[str, Any]]:
        """Optimize projects for the target role."""
        role_keywords = self._extract_role_keywords(target_role)
        weaponized_projects = []
        
        for project in projects:
            relevance_score = self._calculate_project_relevance(project, role_keywords)
            
            weaponized_project = {
                "original_project": project,
                "relevance_score": relevance_score,
                "optimized_description": self._enhance_project_description(
                    project.description, role_keywords, relevance_score
                ),
                "optimization_suggestions": [],
                "priority": "high" if relevance_score > 0.7 else "medium" if relevance_score > 0.4 else "low"
            }
            
            # Generate optimization suggestions
            if relevance_score < 0.5:
                weaponized_project["optimization_suggestions"].append(
                    "Consider reframing project to highlight relevant technologies"
                )
            elif relevance_score > 0.8:
                weaponized_project["optimization_suggestions"].append(
                    "This project is highly relevant - feature it prominently"
                )
                
            weaponized_projects.append(weaponized_project)
            
        # Sort by relevance score (highest first)
        weaponized_projects.sort(key=lambda x: x["relevance_score"], reverse=True)
        return weaponized_projects
        
    def _weaponize_achievements(self, achievements: List[Achievement], target_role: str) -> List[Dict[str, Any]]:
        """Optimize achievements for the target role."""
        role_keywords = self._extract_role_keywords(target_role)
        weaponized_achievements = []
        
        for achievement in achievements:
            relevance_score = self._calculate_achievement_relevance(achievement, role_keywords)
            
            weaponized_achievement = {
                "original_achievement": achievement,
                "relevance_score": relevance_score,
                "optimization_suggestions": [],
                "priority": "high" if relevance_score > 0.7 else "medium" if relevance_score > 0.4 else "low"
            }
            
            # Generate optimization suggestions
            if relevance_score < 0.5:
                weaponized_achievement["optimization_suggestions"].append(
                    "Consider how this achievement demonstrates transferable skills"
                )
            elif relevance_score > 0.8:
                weaponized_achievement["optimization_suggestions"].append(
                    "This achievement is highly relevant - emphasize the impact"
                )
                
            weaponized_achievements.append(weaponized_achievement)
            
        # Sort by relevance score (highest first)
        weaponized_achievements.sort(key=lambda x: x["relevance_score"], reverse=True)
        return weaponized_achievements
        
    def _extract_role_keywords(self, target_role: str) -> List[str]:
        """Extract relevant keywords for the target role."""
        target_role_lower = target_role.lower()
        
        # Check for exact matches
        for role, keywords in self.role_keywords.items():
            if role in target_role_lower or any(keyword in target_role_lower for keyword in keywords):
                return keywords
                
        # If no exact match, extract keywords from the role name
        extracted_keywords = []
        common_tech_keywords = [
            "python", "javascript", "java", "c++", "react", "angular", "vue", "node.js",
            "docker", "kubernetes", "aws", "azure", "gcp", "sql", "nosql", "mongodb",
            "machine learning", "ai", "data science", "devops", "agile", "scrum"
        ]
        
        for keyword in common_tech_keywords:
            if keyword in target_role_lower:
                extracted_keywords.append(keyword)
                
        return extracted_keywords if extracted_keywords else ["software", "development", "engineering"]
        
    def _calculate_skill_relevance(self, skill_name: str, role_keywords: List[str]) -> float:
        """Calculate how relevant a skill is to the target role."""
        skill_lower = skill_name.lower()
        
        # Check for exact keyword matches
        for keyword in role_keywords:
            if keyword in skill_lower:
                return 0.9
                
        # Check for partial matches
        for keyword in role_keywords:
            if any(word in skill_lower for word in keyword.split()):
                return 0.7
                
        # Check for related terms
        related_terms = {
            "coding": ["programming", "development", "software"],
            "data": ["analysis", "analytics", "science"],
            "security": ["cybersecurity", "penetration", "vulnerability"],
            "testing": ["qa", "quality", "automation"],
            "design": ["ui", "ux", "interface", "experience"]
        }
        
        for category, terms in related_terms.items():
            if category in skill_lower or any(term in skill_lower for term in terms):
                for keyword in role_keywords:
                    if category in keyword or any(term in keyword for term in terms):
                        return 0.6
                        
        return 0.2  # Default low relevance
        
    def _calculate_project_relevance(self, project: Project, role_keywords: List[str]) -> float:
        """Calculate how relevant a project is to the target role."""
        project_text = f"{project.name} {project.description} {' '.join(project.technologies)}".lower()
        
        # Count keyword matches
        matches = 0
        for keyword in role_keywords:
            if keyword in project_text:
                matches += 1
                
        # Calculate relevance score
        if matches == 0:
            return 0.1
        elif matches == 1:
            return 0.4
        elif matches == 2:
            return 0.6
        elif matches >= 3:
            return 0.9
        else:
            return 0.3
            
    def _calculate_achievement_relevance(self, achievement: Achievement, role_keywords: List[str]) -> float:
        """Calculate how relevant an achievement is to the target role."""
        achievement_text = f"{achievement.name} {achievement.description}".lower()
        
        # Count keyword matches
        matches = 0
        for keyword in role_keywords:
            if keyword in achievement_text:
                matches += 1
                
        # Calculate relevance score
        if matches == 0:
            return 0.2
        elif matches == 1:
            return 0.5
        elif matches >= 2:
            return 0.8
        else:
            return 0.3
            
    def _enhance_project_description(self, description: str, role_keywords: List[str], relevance_score: float) -> str:
        """Enhance project description with role-relevant keywords."""
        if relevance_score > 0.7:
            # Already highly relevant, just ensure keywords are prominent
            enhanced = description
            for keyword in role_keywords:
                if keyword in description.lower():
                    # Make keyword more prominent
                    enhanced = enhanced.replace(keyword, f"**{keyword}**")
            return enhanced
        elif relevance_score > 0.4:
            # Moderately relevant, add some context
            enhanced = description
            relevant_keywords = [kw for kw in role_keywords if kw in description.lower()]
            if relevant_keywords:
                enhanced += f" (Utilized {', '.join(relevant_keywords)})"
            return enhanced
        else:
            # Low relevance, suggest reframing
            return f"{description} [Consider highlighting transferable skills relevant to this role]"
            
    def _calculate_optimization_score(self, weaponized_skills: List[Dict], weaponized_projects: List[Dict], weaponized_achievements: List[Dict], target_role: str) -> float:
        """Calculate overall optimization score for the resume."""
        if not weaponized_skills and not weaponized_projects and not weaponized_achievements:
            return 0.0
            
        # Calculate weighted average of relevance scores
        total_score = 0.0
        total_weight = 0.0
        
        # Skills weight: 0.4
        for skill in weaponized_skills:
            total_score += skill["relevance_score"] * 0.4
            total_weight += 0.4
            
        # Projects weight: 0.4
        for project in weaponized_projects:
            total_score += project["relevance_score"] * 0.4
            total_weight += 0.4
            
        # Achievements weight: 0.2
        for achievement in weaponized_achievements:
            total_score += achievement["relevance_score"] * 0.2
            total_weight += 0.2
            
        return total_score / total_weight if total_weight > 0 else 0.0
        
    def _generate_recommendations(self, optimization_score: float, role_keywords: List[str]) -> List[str]:
        """Generate recommendations based on optimization score."""
        recommendations = []
        
        if optimization_score < 0.3:
            recommendations.extend([
                "Consider adding more projects that utilize relevant technologies",
                "Focus on developing skills that align with the target role",
                "Highlight transferable skills from existing experience"
            ])
        elif optimization_score < 0.6:
            recommendations.extend([
                "Enhance project descriptions with role-specific keywords",
                "Consider taking courses or certifications in relevant areas",
                "Emphasize achievements that demonstrate role-relevant skills"
            ])
        elif optimization_score < 0.8:
            recommendations.extend([
                "Fine-tune project descriptions to better highlight relevant technologies",
                "Consider adding more specific technical achievements",
                "Ensure all relevant skills are prominently featured"
            ])
        else:
            recommendations.extend([
                "Resume is well-optimized for the target role",
                "Consider adding recent projects or achievements to stay current",
                "Focus on demonstrating impact and results in project descriptions"
            ])
            
        return recommendations
        
    def export_weaponized_resume(self, weaponized_data: Dict[str, Any], output_path: str, format_type: str = 'json') -> bool:
        """
        Export weaponized resume data to a file.
        
        Args:
            weaponized_data: The weaponized resume data
            output_path: Path where to save the file
            format_type: Output format ('json', 'markdown')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if format_type == 'json':
                content = json.dumps(weaponized_data, indent=2, default=str)
            elif format_type == 'markdown':
                content = self._generate_weaponized_report(weaponized_data)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
                
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error exporting weaponized resume: {e}")
            return False
            
    def _generate_weaponized_report(self, weaponized_data: Dict[str, Any]) -> str:
        """Generate a markdown report of the weaponized resume."""
        content = []
        
        content.append("# Resume Weaponization Report")
        content.append(f"**Target Role:** {weaponized_data['target_role']}")
        content.append(f"**Optimization Score:** {weaponized_data['optimization_score']:.2f}/1.0")
        content.append(f"**Generated:** {weaponized_data['optimization_timestamp']}")
        content.append("")
        
        # Role Keywords
        content.append("## Target Role Keywords")
        content.append(", ".join(weaponized_data['role_keywords']))
        content.append("")
        
        # Skills Analysis
        content.append("## Skills Analysis")
        for skill in weaponized_data['weaponized_skills'][:5]:  # Top 5
            content.append(f"### {skill['original_skill'].name}")
            content.append(f"- **Relevance Score:** {skill['relevance_score']:.2f}")
            content.append(f"- **Priority:** {skill['priority']}")
            if skill['optimization_suggestions']:
                content.append("- **Suggestions:**")
                for suggestion in skill['optimization_suggestions']:
                    content.append(f"  - {suggestion}")
            content.append("")
            
        # Projects Analysis
        content.append("## Projects Analysis")
        for project in weaponized_data['weaponized_projects'][:3]:  # Top 3
            content.append(f"### {project['original_project'].name}")
            content.append(f"- **Relevance Score:** {project['relevance_score']:.2f}")
            content.append(f"- **Priority:** {project['priority']}")
            content.append(f"- **Optimized Description:** {project['optimized_description']}")
            if project['optimization_suggestions']:
                content.append("- **Suggestions:**")
                for suggestion in project['optimization_suggestions']:
                    content.append(f"  - {suggestion}")
            content.append("")
            
        # Recommendations
        content.append("## Recommendations")
        for i, recommendation in enumerate(weaponized_data['recommendations'], 1):
            content.append(f"{i}. {recommendation}")
        content.append("")
        
        return "\n".join(content) 