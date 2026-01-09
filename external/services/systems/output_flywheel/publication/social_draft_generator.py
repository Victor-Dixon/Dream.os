"""
Social Draft Generator - Phase 3
=================================

Generates social media post drafts from artifacts.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class SocialDraftGenerator:
    """Generates social media post drafts."""
    
    def __init__(self, output_path: Optional[Path] = None, draft_mode: bool = True):
        """Initialize social draft generator."""
        if output_path is None:
            output_path = Path("systems/output_flywheel/outputs/artifacts/social_drafts")
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.draft_mode = draft_mode
    
    def _extract_summary(self, content: str, max_length: int = 200) -> str:
        """Extract summary from content."""
        # Remove markdown headers
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)
        
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        
        # Remove links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Truncate to max length
        if len(content) > max_length:
            content = content[:max_length].rsplit(' ', 1)[0] + "..."
        
        return content
    
    def _generate_hashtags(self, content: str, count: int = 3) -> List[str]:
        """Generate hashtags from content."""
        # Simple keyword extraction
        words = re.findall(r'\b[a-z]{4,}\b', content.lower())
        
        # Common tech hashtags
        tech_keywords = {
            'python': '#Python',
            'javascript': '#JavaScript',
            'react': '#React',
            'github': '#GitHub',
            'coding': '#Coding',
            'development': '#Dev',
            'trading': '#Trading',
            'ai': '#AI',
            'machine': '#MachineLearning',
            'web': '#WebDev'
        }
        
        hashtags = []
        for word in words:
            if word in tech_keywords:
                hashtag = tech_keywords[word]
                if hashtag not in hashtags:
                    hashtags.append(hashtag)
        
        # Fill remaining slots with generic tags
        generic_tags = ['#Tech', '#Code', '#Development', '#Programming']
        for tag in generic_tags:
            if len(hashtags) >= count:
                break
            if tag not in hashtags:
                hashtags.append(tag)
        
        return hashtags[:count]
    
    def _format_twitter(self, summary: str, hashtags: List[str], max_length: int = 280) -> str:
        """Format content for Twitter."""
        hashtag_text = ' '.join(hashtags)
        available_length = max_length - len(hashtag_text) - 2  # Space and newline
        
        if len(summary) > available_length:
            summary = summary[:available_length - 3] + "..."
        
        return f"{summary}\n\n{hashtag_text}"
    
    def _format_linkedin(self, summary: str, hashtags: List[str]) -> str:
        """Format content for LinkedIn."""
        hashtag_text = ' '.join(hashtags)
        return f"{summary}\n\n{hashtag_text}"
    
    def generate_draft(
        self,
        artifact_type: str,
        artifact_path: str,
        platform: str = "twitter",
        max_length: int = 280,
        hashtag_count: int = 3,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate social media draft."""
        source_file = Path(artifact_path)
        if not source_file.exists():
            return {
                "success": False,
                "error": f"Artifact file not found: {artifact_path}"
            }
        
        # Read content
        try:
            content = source_file.read_text(encoding="utf-8")
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read artifact: {e}"
            }
        
        # Extract summary
        summary = self._extract_summary(content, max_length=max_length)
        
        # Generate hashtags
        hashtags = self._generate_hashtags(content, count=hashtag_count)
        
        # Format for platform
        if platform == "twitter":
            draft_content = self._format_twitter(summary, hashtags, max_length)
        elif platform == "linkedin":
            draft_content = self._format_linkedin(summary, hashtags)
        else:
            draft_content = f"{summary}\n\n{' '.join(hashtags)}"
        
        # Determine output filename
        output_filename = f"{source_file.stem}_{platform}_draft.txt"
        output_file = self.output_path / output_filename
        
        # Write draft file
        try:
            output_file.write_text(draft_content, encoding="utf-8")
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to write draft file: {e}"
            }
        
        return {
            "success": True,
            "status": "draft" if self.draft_mode else "ready",
            "message": f"Social draft generated for {platform}",
            "output_path": str(output_file),
            "content_length": len(draft_content),
            "platform": platform
        }




