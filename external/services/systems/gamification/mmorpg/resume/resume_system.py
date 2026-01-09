"""
MMORPG Resume System
Contains the resume generation and weaponization system for the Dreamscape MMORPG.
"""

from typing import Dict, List, Any, Optional
import sqlite3
import json
import os
from datetime import datetime

from ..models import Achievement, ResumeSkill, Project
from dreamscape.core.config import RESUME_DB_PATH


class ResumeTracker:
    """Tracks and manages resume data."""
    
    def __init__(self, db_path: str = str(RESUME_DB_PATH)):
        """Initialize the resume tracker."""
        self.db = ResumeDatabase(db_path)
        
    def add_achievement(self, achievement: Any) -> bool:
        """Add an achievement to the resume tracker."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO achievements 
                (id, name, description, category, difficulty, xp_reward, 
                 completed_at, evidence, tags, impact_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                achievement.id,
                achievement.name,
                achievement.description,
                achievement.category,
                achievement.difficulty,
                achievement.xp_reward,
                achievement.completed_at,
                achievement.evidence,
                json.dumps(achievement.tags),
                achievement.impact_score
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding achievement: {e}")
            return False
            
    def get_achievements(self, category: str = None, limit: int = 50) -> List[Any]:
        """Get achievements from the database."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = '''
                SELECT id, name, description, category, difficulty, xp_reward,
                       completed_at, evidence, tags, impact_score
                FROM achievements
            '''
            params = []
            
            if category:
                query += ' WHERE category = ?'
                params.append(category)
                
            query += ' ORDER BY completed_at DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            
            achievements = []
            for row in cursor.fetchall():
                achievement = Achievement(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    category=row[3],
                    difficulty=row[4],
                    xp_reward=row[5],
                    completed_at=row[6],
                    evidence=row[7],
                    tags=json.loads(row[8]) if row[8] else [],
                    impact_score=row[9]
                )
                achievements.append(achievement)
                
            return achievements
            
        except Exception as e:
            print(f"Error getting achievements: {e}")
            return []
            
    def add_project(self, project: Any) -> bool:
        """Add a project to the resume tracker."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO projects 
                (id, name, description, start_date, end_date, status,
                 technologies, achievements, impact_description, team_size, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project.id,
                project.name,
                project.description,
                project.start_date,
                project.end_date,
                project.status,
                json.dumps(project.technologies),
                json.dumps(project.achievements),
                project.impact_description,
                project.team_size,
                project.role
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding project: {e}")
            return False
            
    def get_projects(self, status: str = None, limit: int = 20) -> List[Any]:
        """Get projects from the database."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = '''
                SELECT id, name, description, start_date, end_date, status,
                       technologies, achievements, impact_description, team_size, role
                FROM projects
            '''
            params = []
            
            if status:
                query += ' WHERE status = ?'
                params.append(status)
                
            query += ' ORDER BY start_date DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            
            projects = []
            for row in cursor.fetchall():
                project = Project(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    start_date=row[3],
                    end_date=row[4],
                    status=row[5],
                    technologies=json.loads(row[6]) if row[6] else [],
                    achievements=json.loads(row[7]) if row[7] else [],
                    impact_description=row[8],
                    team_size=row[9],
                    role=row[10]
                )
                projects.append(project)
                
            return projects
            
        except Exception as e:
            print(f"Error getting projects: {e}")
            return []
            
    def get_skills(self) -> List[Any]:
        """Get skills from the database."""
        # Placeholder - would implement skill retrieval
        return []
        
    def generate_resume(self, format_type: str = 'markdown', include_achievements: bool = True) -> str:
        """Generate a resume in the specified format."""
        generator = ResumeGenerator()
        skills = self.get_skills()
        projects = self.get_projects()
        achievements = self.get_achievements() if include_achievements else []
        
        return generator.generate_resume(skills, projects, achievements, format_type)
        
    def export_resume(self, output_path: str, format_type: str = 'markdown') -> bool:
        """Export resume to file."""
        generator = ResumeGenerator()
        skills = self.get_skills()
        projects = self.get_projects()
        achievements = self.get_achievements()
        
        content = generator.generate_resume(skills, projects, achievements, format_type)
        return generator.export_resume(content, output_path)
        
    def get_resume_stats(self) -> Dict[str, Any]:
        """Get comprehensive resume statistics."""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Get achievement stats
            cursor.execute('SELECT COUNT(*) FROM achievements')
            total_achievements = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM achievements WHERE category = "project"')
            project_achievements = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM achievements WHERE category = "skill"')
            skill_achievements = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(impact_score) FROM achievements')
            avg_impact = cursor.fetchone()[0] or 0
            
            # Get project stats
            cursor.execute('SELECT COUNT(*) FROM projects')
            total_projects = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM projects WHERE status = "completed"')
            completed_projects = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(team_size) FROM projects')
            avg_team_size = cursor.fetchone()[0] or 1
            
            return {
                'total_achievements': total_achievements,
                'project_achievements': project_achievements,
                'skill_achievements': skill_achievements,
                'average_impact_score': round(avg_impact, 2),
                'total_projects': total_projects,
                'completed_projects': completed_projects,
                'completion_rate': round(completed_projects / total_projects * 100, 2) if total_projects > 0 else 0,
                'average_team_size': round(avg_team_size, 1)
            }
            
        except Exception as e:
            print(f"Error getting resume stats: {e}")
            return {}
            
    def close(self):
        """Close the database connection."""
        self.db.close()


class ResumeDatabase:
    """Manages resume database operations."""
    
    def __init__(self, db_path: str = str(RESUME_DB_PATH)):
        """Initialize the resume database."""
        self.db_path = db_path
        self._init_database()
        
    def _init_database(self):
        """Initialize the database schema."""
        try:
            conn = self.get_connection()
            self._create_schema(conn)
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
            
    def _create_schema(self, conn):
        """Create the database schema."""
        cursor = conn.cursor()
        
        # Create achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                difficulty INTEGER,
                xp_reward INTEGER,
                completed_at TEXT,
                evidence TEXT,
                tags TEXT,
                impact_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT,
                technologies TEXT,
                achievements TEXT,
                impact_description TEXT,
                team_size INTEGER,
                role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create skills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                current_level INTEGER DEFAULT 0,
                max_level INTEGER DEFAULT 100,
                current_xp INTEGER DEFAULT 0,
                next_level_xp INTEGER DEFAULT 100,
                description TEXT,
                last_updated TEXT,
                achievements TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
        
    def close(self):
        """Close the database connection."""
        # SQLite connections are closed automatically when the object is garbage collected
        pass


class ResumeGenerator:
    """Generates resumes in various formats."""
    
    def __init__(self):
        """Initialize the resume generator."""
        pass
        
    def generate_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any], format_type: str = 'markdown') -> str:
        """Generate a resume in the specified format."""
        if format_type == 'markdown':
            return self._generate_markdown_resume(skills, projects, achievements)
        elif format_type == 'html':
            return self._generate_html_resume(skills, projects, achievements)
        elif format_type == 'json':
            return self._generate_json_resume(skills, projects, achievements)
        else:
            return self._generate_markdown_resume(skills, projects, achievements)
            
    def _generate_markdown_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any]) -> str:
        """Generate a markdown resume."""
        resume = []
        
        # Header
        resume.append("# Software Architect Resume")
        resume.append("")
        resume.append("*Generated by Dreamscape MMORPG System*")
        resume.append("")
        
        # Skills Section
        if skills:
            resume.append("## Skills")
            resume.append("")
            
            # Group skills by category
            skill_categories = {}
            for skill in skills:
                category = getattr(skill, 'category', 'Other')
                if category not in skill_categories:
                    skill_categories[category] = []
                skill_categories[category].append(skill)
                
            for category, category_skills in skill_categories.items():
                resume.append(f"### {category.title()} Skills")
                for skill in category_skills:
                    level = getattr(skill, 'current_level', 0)
                    resume.append(f"- **{skill.name}**: Level {level}")
                resume.append("")
                
        # Projects Section
        if projects:
            resume.append("## Projects")
            resume.append("")
            
            for project in projects:
                resume.append(f"### {project.name}")
                resume.append(f"*{project.start_date} - {project.end_date or 'Present'}*")
                resume.append("")
                resume.append(project.description)
                resume.append("")
                
                if project.technologies:
                    resume.append(f"**Technologies**: {', '.join(project.technologies)}")
                    resume.append("")
                    
                if project.impact_description:
                    resume.append(f"**Impact**: {project.impact_description}")
                    resume.append("")
                    
        # Achievements Section
        if achievements:
            resume.append("## Achievements")
            resume.append("")
            
            # Group by category
            achievement_categories = {}
            for achievement in achievements:
                category = achievement.category
                if category not in achievement_categories:
                    achievement_categories[category] = []
                achievement_categories[category].append(achievement)
                
            for category, category_achievements in achievement_categories.items():
                resume.append(f"### {category.title()} Achievements")
                for achievement in category_achievements:
                    difficulty = achievement.get_difficulty_label()
                    impact = achievement.get_impact_label()
                    resume.append(f"- **{achievement.name}** ({difficulty}, {impact} impact)")
                    resume.append(f"  {achievement.description}")
                resume.append("")
                
        return "\n".join(resume)
        
    def _generate_html_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any]) -> str:
        """Generate an HTML resume."""
        html = []
        
        # HTML header
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("    <meta charset='UTF-8'>")
        html.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append("    <title>Software Architect Resume</title>")
        html.append("    <style>")
        html.append("        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }")
        html.append("        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }")
        html.append("        h2 { color: #34495e; margin-top: 30px; }")
        html.append("        h3 { color: #7f8c8d; }")
        html.append("        .skill-category { margin-bottom: 20px; }")
        html.append("        .project { margin-bottom: 25px; padding: 15px; border-left: 3px solid #3498db; }")
        html.append("        .achievement { margin-bottom: 10px; }")
        html.append("        .difficulty { color: #e74c3c; font-weight: bold; }")
        html.append("        .impact { color: #27ae60; font-weight: bold; }")
        html.append("    </style>")
        html.append("</head>")
        html.append("<body>")
        
        # Header
        html.append("    <h1>Software Architect Resume</h1>")
        html.append("    <p><em>Generated by Dreamscape MMORPG System</em></p>")
        
        # Skills Section
        if skills:
            html.append("    <h2>Skills</h2>")
            
            skill_categories = {}
            for skill in skills:
                category = getattr(skill, 'category', 'Other')
                if category not in skill_categories:
                    skill_categories[category] = []
                skill_categories[category].append(skill)
                
            for category, category_skills in skill_categories.items():
                html.append(f"    <div class='skill-category'>")
                html.append(f"        <h3>{category.title()} Skills</h3>")
                html.append("        <ul>")
                for skill in category_skills:
                    level = getattr(skill, 'current_level', 0)
                    html.append(f"            <li><strong>{skill.name}</strong>: Level {level}</li>")
                html.append("        </ul>")
                html.append("    </div>")
                
        # Projects Section
        if projects:
            html.append("    <h2>Projects</h2>")
            
            for project in projects:
                html.append("    <div class='project'>")
                html.append(f"        <h3>{project.name}</h3>")
                html.append(f"        <p><em>{project.start_date} - {project.end_date or 'Present'}</em></p>")
                html.append(f"        <p>{project.description}</p>")
                
                if project.technologies:
                    html.append(f"        <p><strong>Technologies</strong>: {', '.join(project.technologies)}</p>")
                    
                if project.impact_description:
                    html.append(f"        <p><strong>Impact</strong>: {project.impact_description}</p>")
                    
                html.append("    </div>")
                
        # Achievements Section
        if achievements:
            html.append("    <h2>Achievements</h2>")
            
            achievement_categories = {}
            for achievement in achievements:
                category = achievement.category
                if category not in achievement_categories:
                    achievement_categories[category] = []
                achievement_categories[category].append(achievement)
                
            for category, category_achievements in achievement_categories.items():
                html.append(f"    <h3>{category.title()} Achievements</h3>")
                html.append("    <ul>")
                for achievement in category_achievements:
                    difficulty = achievement.get_difficulty_label()
                    impact = achievement.get_impact_label()
                    html.append(f"        <li class='achievement'>")
                    html.append(f"            <strong>{achievement.name}</strong> ")
                    html.append(f"            (<span class='difficulty'>{difficulty}</span>, ")
                    html.append(f"            <span class='impact'>{impact} impact</span>)")
                    html.append(f"            <br>{achievement.description}")
                    html.append("        </li>")
                html.append("    </ul>")
                
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)
        
    def _generate_json_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any]) -> str:
        """Generate a JSON resume."""
        resume_data = {
            "title": "Software Architect Resume",
            "generated_by": "Dreamscape MMORPG System",
            "generated_at": datetime.now().isoformat(),
            "skills": [skill.__dict__ for skill in skills],
            "projects": [project.__dict__ for project in projects],
            "achievements": [achievement.__dict__ for achievement in achievements]
        }
        
        return json.dumps(resume_data, indent=2)
        
    def export_resume(self, content: str, output_path: str) -> bool:
        """Export resume content to file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error exporting resume: {e}")
            return False


class ResumeWeaponizer:
    """Weaponizes resumes for specific job roles."""
    
    def __init__(self):
        """Initialize the resume weaponizer."""
        self.role_keywords = {
            "Software Architect": [
                "architecture", "design", "patterns", "system", "scalability",
                "performance", "security", "integration", "microservices",
                "cloud", "aws", "azure", "gcp", "docker", "kubernetes"
            ],
            "Senior Developer": [
                "development", "coding", "programming", "debugging", "testing",
                "refactoring", "optimization", "code review", "mentoring",
                "agile", "scrum", "git", "ci/cd", "automation"
            ],
            "DevOps Engineer": [
                "devops", "deployment", "infrastructure", "automation", "ci/cd",
                "docker", "kubernetes", "aws", "azure", "gcp", "monitoring",
                "logging", "security", "compliance", "terraform"
            ]
        }
        
    def weaponize_resume(self, skills: List[Any], projects: List[Any], achievements: List[Any], target_role: str = "Software Architect") -> Dict[str, Any]:
        """Weaponize resume for a specific role."""
        weaponized_data = {
            "target_role": target_role,
            "optimization_score": 0.0,
            "weaponized_skills": [],
            "weaponized_projects": [],
            "weaponized_achievements": [],
            "role_keywords": [],
            "recommendations": []
        }
        
        # Extract role keywords
        role_keywords = self._extract_role_keywords(target_role)
        weaponized_data["role_keywords"] = role_keywords
        
        # Weaponize skills
        weaponized_data["weaponized_skills"] = self._weaponize_skills(skills, target_role)
        
        # Weaponize projects
        weaponized_data["weaponized_projects"] = self._weaponize_projects(projects, target_role)
        
        # Weaponize achievements
        weaponized_data["weaponized_achievements"] = self._weaponize_achievements(achievements, target_role)
        
        # Calculate optimization score
        weaponized_data["optimization_score"] = self._calculate_optimization_score(
            skills, projects, achievements, target_role
        )
        
        # Generate recommendations
        weaponized_data["recommendations"] = self._generate_recommendations(
            weaponized_data, target_role
        )
        
        return weaponized_data
        
    def _weaponize_skills(self, skills: List[Any], target_role: str) -> List[Dict[str, Any]]:
        """Weaponize skills for the target role."""
        weaponized_skills = []
        role_keywords = self._extract_role_keywords(target_role)
        
        for skill in skills:
            relevance_score = self._calculate_skill_relevance(skill.name, role_keywords)
            
            weaponized_skill = {
                "original_skill": skill.__dict__,
                "relevance_score": relevance_score,
                "weaponized_description": f"Expert-level {skill.name} with {skill.current_level} years of experience",
                "role_alignment": "High" if relevance_score > 0.7 else "Medium" if relevance_score > 0.4 else "Low"
            }
            
            weaponized_skills.append(weaponized_skill)
            
        # Sort by relevance score
        weaponized_skills.sort(key=lambda x: x["relevance_score"], reverse=True)
        return weaponized_skills
        
    def _weaponize_projects(self, projects: List[Any], target_role: str) -> List[Dict[str, Any]]:
        """Weaponize projects for the target role."""
        weaponized_projects = []
        role_keywords = self._extract_role_keywords(target_role)
        
        for project in projects:
            relevance_score = self._calculate_project_relevance(project, role_keywords)
            
            # Enhance project description
            enhanced_description = self._enhance_project_description(
                project.description, role_keywords, relevance_score
            )
            
            weaponized_project = {
                "original_project": project.__dict__,
                "relevance_score": relevance_score,
                "weaponized_description": enhanced_description,
                "role_alignment": "High" if relevance_score > 0.7 else "Medium" if relevance_score > 0.4 else "Low"
            }
            
            weaponized_projects.append(weaponized_project)
            
        # Sort by relevance score
        weaponized_projects.sort(key=lambda x: x["relevance_score"], reverse=True)
        return weaponized_projects
        
    def _weaponize_achievements(self, achievements: List[Any], target_role: str) -> List[Dict[str, Any]]:
        """Weaponize achievements for the target role."""
        weaponized_achievements = []
        role_keywords = self._extract_role_keywords(target_role)
        
        for achievement in achievements:
            relevance_score = self._calculate_achievement_relevance(achievement, role_keywords)
            
            weaponized_achievement = {
                "original_achievement": achievement.__dict__,
                "relevance_score": relevance_score,
                "role_alignment": "High" if relevance_score > 0.7 else "Medium" if relevance_score > 0.4 else "Low"
            }
            
            weaponized_achievements.append(weaponized_achievement)
            
        # Sort by relevance score
        weaponized_achievements.sort(key=lambda x: x["relevance_score"], reverse=True)
        return weaponized_achievements
        
    def _extract_role_keywords(self, target_role: str) -> List[str]:
        """Extract keywords for the target role."""
        return self.role_keywords.get(target_role, [])
        
    def _calculate_skill_relevance(self, skill_name: str, role_keywords: List[str]) -> float:
        """Calculate skill relevance to role keywords."""
        skill_lower = skill_name.lower()
        matches = sum(1 for keyword in role_keywords if keyword.lower() in skill_lower)
        return min(matches / len(role_keywords), 1.0) if role_keywords else 0.0
        
    def _calculate_project_relevance(self, project: Any, role_keywords: List[str]) -> float:
        """Calculate project relevance to role keywords."""
        project_text = f"{project.description} {' '.join(project.technologies)}".lower()
        matches = sum(1 for keyword in role_keywords if keyword.lower() in project_text)
        return min(matches / len(role_keywords), 1.0) if role_keywords else 0.0
        
    def _calculate_achievement_relevance(self, achievement: Any, role_keywords: List[str]) -> float:
        """Calculate achievement relevance to role keywords."""
        achievement_text = f"{achievement.name} {achievement.description}".lower()
        matches = sum(1 for keyword in role_keywords if keyword.lower() in achievement_text)
        return min(matches / len(role_keywords), 1.0) if role_keywords else 0.0
        
    def _enhance_project_description(self, description: str, role_keywords: List[str], relevance_score: float) -> str:
        """Enhance project description with role-specific language."""
        enhanced = description
        
        # Add role-specific enhancements based on relevance
        if relevance_score > 0.7:
            enhanced += f" This project demonstrates strong {', '.join(role_keywords[:3])} capabilities."
        elif relevance_score > 0.4:
            enhanced += f" Involved aspects of {', '.join(role_keywords[:2])}."
            
        return enhanced
        
    def _calculate_optimization_score(self, skills: List[Any], projects: List[Any], achievements: List[Any], target_role: str) -> float:
        """Calculate overall optimization score for the target role."""
        role_keywords = self._extract_role_keywords(target_role)
        
        # Calculate skill optimization
        skill_scores = [self._calculate_skill_relevance(skill.name, role_keywords) for skill in skills]
        avg_skill_score = sum(skill_scores) / len(skill_scores) if skill_scores else 0
        
        # Calculate project optimization
        project_scores = [self._calculate_project_relevance(project, role_keywords) for project in projects]
        avg_project_score = sum(project_scores) / len(project_scores) if project_scores else 0
        
        # Calculate achievement optimization
        achievement_scores = [self._calculate_achievement_relevance(achievement, role_keywords) for achievement in achievements]
        avg_achievement_score = sum(achievement_scores) / len(achievement_scores) if achievement_scores else 0
        
        # Weighted average
        total_score = (avg_skill_score * 0.3 + avg_project_score * 0.5 + avg_achievement_score * 0.2)
        return min(total_score, 1.0)
        
    def _generate_recommendations(self, weaponized_data: Dict[str, Any], target_role: str) -> List[str]:
        """Generate recommendations for improving the resume."""
        recommendations = []
        optimization_score = weaponized_data["optimization_score"]
        
        if optimization_score < 0.5:
            recommendations.append(f"Focus on developing skills relevant to {target_role}")
            recommendations.append("Add more projects that align with the target role")
            recommendations.append("Highlight achievements that demonstrate role-specific capabilities")
        elif optimization_score < 0.8:
            recommendations.append("Consider adding more advanced projects in the target domain")
            recommendations.append("Enhance skill descriptions with role-specific terminology")
        else:
            recommendations.append("Resume is well-optimized for the target role")
            recommendations.append("Consider adding recent achievements to maintain relevance")
            
        return recommendations
        
    def export_weaponized_resume(self, weaponized_data: Dict[str, Any], output_path: str, format_type: str = 'json') -> bool:
        """Export weaponized resume data."""
        try:
            if format_type == 'json':
                content = json.dumps(weaponized_data, indent=2)
            else:
                content = self._generate_weaponized_report(weaponized_data)
                
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
        except Exception as e:
            print(f"Error exporting weaponized resume: {e}")
            return False
            
    def _generate_weaponized_report(self, weaponized_data: Dict[str, Any]) -> str:
        """Generate a human-readable weaponized resume report."""
        report = []
        
        report.append("# Weaponized Resume Report")
        report.append("")
        report.append(f"**Target Role**: {weaponized_data['target_role']}")
        report.append(f"**Optimization Score**: {weaponized_data['optimization_score']:.2%}")
        report.append("")
        
        # Skills section
        report.append("## Weaponized Skills")
        report.append("")
        for skill in weaponized_data['weaponized_skills'][:5]:  # Top 5
            report.append(f"- **{skill['original_skill']['name']}**")
            report.append(f"  - Relevance: {skill['relevance_score']:.2%}")
            report.append(f"  - Alignment: {skill['role_alignment']}")
            report.append(f"  - Enhanced: {skill['weaponized_description']}")
            report.append("")
            
        # Projects section
        report.append("## Weaponized Projects")
        report.append("")
        for project in weaponized_data['weaponized_projects'][:3]:  # Top 3
            report.append(f"- **{project['original_project']['name']}**")
            report.append(f"  - Relevance: {project['relevance_score']:.2%}")
            report.append(f"  - Alignment: {project['role_alignment']}")
            report.append(f"  - Enhanced: {project['weaponized_description']}")
            report.append("")
            
        # Recommendations
        report.append("## Recommendations")
        report.append("")
        for recommendation in weaponized_data['recommendations']:
            report.append(f"- {recommendation}")
            
        return "\n".join(report) 