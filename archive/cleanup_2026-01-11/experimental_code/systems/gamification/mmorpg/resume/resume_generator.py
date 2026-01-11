"""
MMORPG Resume Generator
Contains the resume generation system for the Dreamscape MMORPG.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import asdict

logger = logging.getLogger(__name__)


class ResumeGenerator:
    """Generate resumes in multiple formats."""
    
    def __init__(self):
        """Initialize the resume generator."""
        pass

    def generate_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any], format_type: str = 'markdown') -> str:
        """Generate a resume in the specified format."""
        try:
            if format_type == 'markdown':
                return self._generate_markdown_resume(skills, projects, achievements)
            elif format_type == 'html':
                return self._generate_html_resume(skills, projects, achievements)
            elif format_type == 'json':
                return self._generate_json_resume(skills, projects, achievements)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
        except Exception as e:
            logger.error(f"❌ Failed to generate resume: {e}")
            return f"Error generating resume: {e}"

    def _generate_markdown_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any]) -> str:
        """Generate a markdown resume."""
        resume = []
        resume.append("# Thea Player - Software Architect & AI Specialist")
        resume.append("")
        resume.append("*Building autonomous systems and AI-driven solutions*")
        resume.append("")
        
        # Skills section
        resume.append("## Skills")
        resume.append("")
        skill_categories = {}
        for skill in skills:
            if skill.get('category') not in skill_categories:
                skill_categories[skill.get('category', 'general')] = []
            skill_categories[skill.get('category', 'general')].append(skill)
        
        for category, category_skills in skill_categories.items():
            resume.append(f"### {category.title()}")
            for skill in category_skills:
                current_level = skill.get('current_level', 0)
                current_xp = skill.get('experience_points', 0)
                next_level_xp = skill.get('next_level_xp', 1)
                progress = (current_xp / next_level_xp) * 100 if next_level_xp > 0 else 0
                resume.append(f"- **{skill.get('name', 'Unknown')}**: Level {current_level} ({progress:.1f}% to next level)")
            resume.append("")
        
        # Experience section
        if projects:
            resume.append("## Experience")
            resume.append("")
            for project in projects:
                resume.append(f"### {project.get('name', 'Unknown Project')}")
                start_date = project.get('start_date', 'Unknown')
                end_date = project.get('end_date', 'Present')
                resume.append(f"*{start_date} - {end_date}*")
                resume.append("")
                resume.append(project.get('description', 'No description available'))
                resume.append("")
                
                technologies = project.get('technologies', [])
                if technologies:
                    resume.append(f"**Technologies**: {', '.join(technologies)}")
                    resume.append("")
                
                impact_description = project.get('impact_description', '')
                if impact_description:
                    resume.append(f"**Impact**: {impact_description}")
                    resume.append("")
        
        # Achievements section
        if achievements:
            resume.append("## Key Achievements")
            resume.append("")
            achievement_categories = {}
            for achievement in achievements:
                category = achievement.get('category', 'general')
                if category not in achievement_categories:
                    achievement_categories[category] = []
                achievement_categories[category].append(achievement)
            
            for category, category_achievements in achievement_categories.items():
                resume.append(f"### {category.title()}")
                for achievement in category_achievements:
                    resume.append(f"- **{achievement.get('name', 'Unknown')}**: {achievement.get('description', 'No description')}")
                resume.append("")
        
        return "\n".join(resume)

    def _generate_html_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any]) -> str:
        """Generate an HTML resume."""
        html = []
        html.append("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Thea Player - Resume</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
                h2 { color: #34495e; margin-top: 30px; }
                h3 { color: #7f8c8d; }
                .skill { margin: 10px 0; }
                .project { margin: 20px 0; padding: 15px; background: #f8f9fa; }
                .achievement { margin: 10px 0; }
            </style>
        </head>
        <body>
        """)
        
        html.append("<h1>Thea Player - Software Architect & AI Specialist</h1>")
        html.append("<p><em>Building autonomous systems and AI-driven solutions</em></p>")
        
        # Skills section
        html.append("<h2>Skills</h2>")
        skill_categories = {}
        for skill in skills:
            category = skill.get('category', 'general')
            if category not in skill_categories:
                skill_categories[category] = []
            skill_categories[category].append(skill)
        
        for category, category_skills in skill_categories.items():
            html.append(f"<h3>{category.title()}</h3>")
            for skill in category_skills:
                current_level = skill.get('current_level', 0)
                current_xp = skill.get('experience_points', 0)
                next_level_xp = skill.get('next_level_xp', 1)
                progress = (current_xp / next_level_xp) * 100 if next_level_xp > 0 else 0
                html.append(f'<div class="skill"><strong>{skill.get("name", "Unknown")}</strong>: Level {current_level} ({progress:.1f}% to next level)</div>')
        
        # Experience section
        if projects:
            html.append("<h2>Experience</h2>")
            for project in projects:
                html.append(f'<div class="project">')
                html.append(f"<h3>{project.get('name', 'Unknown Project')}</h3>")
                start_date = project.get('start_date', 'Unknown')
                end_date = project.get('end_date', 'Present')
                html.append(f"<p><em>{start_date} - {end_date}</em></p>")
                html.append(f"<p>{project.get('description', 'No description available')}</p>")
                
                technologies = project.get('technologies', [])
                if technologies:
                    html.append(f"<p><strong>Technologies:</strong> {', '.join(technologies)}</p>")
                
                impact_description = project.get('impact_description', '')
                if impact_description:
                    html.append(f"<p><strong>Impact:</strong> {impact_description}</p>")
                html.append("</div>")
        
        # Achievements section
        if achievements:
            html.append("<h2>Key Achievements</h2>")
            achievement_categories = {}
            for achievement in achievements:
                category = achievement.get('category', 'general')
                if category not in achievement_categories:
                    achievement_categories[category] = []
                achievement_categories[category].append(achievement)
            
            for category, category_achievements in achievement_categories.items():
                html.append(f"<h3>{category.title()}</h3>")
                for achievement in category_achievements:
                    html.append(f'<div class="achievement"><strong>{achievement.get("name", "Unknown")}</strong>: {achievement.get("description", "No description")}</div>')
        
        html.append("</body></html>")
        return "\n".join(html)

    def _generate_json_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any]) -> str:
        """Generate a JSON resume."""
        resume_data = {
            "header": {
                "name": "Thea Player",
                "title": "Software Architect & AI Specialist",
                "tagline": "Building autonomous systems and AI-driven solutions"
            },
            "skills": skills,
            "projects": projects,
            "achievements": achievements,
            "generated_at": datetime.now().isoformat()
        }
        return json.dumps(resume_data, indent=2)

    def export_resume(self, content: str, output_path: str) -> bool:
        """Export a resume to a file."""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Resume exported to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to export resume: {e}")
            return False 