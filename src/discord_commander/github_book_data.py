"""
GitHub Book Data Loader - Agent Cellphone V2
===========================================

SSOT Domain: git

Data loading and processing for GitHub repository analysis and book display.

Features:
- Repository data loading and caching
- Analysis result processing
- Goldmine discovery extraction
- Performance metrics calculation

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class GitHubBookData:
    """
    Loads and processes GitHub repository analysis data for book display.
    """

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Path("data/github_analysis.json")
        self._data = None
        self._processed_data = None

    def load_data(self) -> Dict[str, Any]:
        """Load raw GitHub analysis data from file."""
        if self._data is not None:
            return self._data

        try:
            if self.data_path.exists():
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                logger.info(f"Loaded GitHub data from {self.data_path}")
            else:
                logger.warning(f"GitHub data file not found: {self.data_path}")
                self._data = self._get_default_data()
        except Exception as e:
            logger.error(f"Failed to load GitHub data: {e}")
            self._data = self._get_default_data()

        return self._data

    def _get_default_data(self) -> Dict[str, Any]:
        """Return default empty data structure."""
        return {
            "timestamp": "2025-01-01T00:00:00Z",
            "total_repos": 0,
            "repositories": [],
            "analysis_summary": {},
            "goldmines": [],
            "performance_metrics": {}
        }

    def get_processed_data(self) -> Dict[str, Any]:
        """Get processed and formatted data for display."""
        if self._processed_data is not None:
            return self._processed_data

        raw_data = self.load_data()
        self._processed_data = self._process_data(raw_data)
        return self._processed_data

    def _process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw data into display-ready format."""
        processed = {
            "metadata": self._extract_metadata(raw_data),
            "chapters": self._create_chapters(raw_data),
            "goldmines": self._extract_goldmines(raw_data),
            "summary": self._create_summary(raw_data),
            "navigation": self._create_navigation(raw_data)
        }
        return processed

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata for display."""
        return {
            "timestamp": data.get("timestamp", "Unknown"),
            "total_repos": data.get("total_repos", 0),
            "analysis_version": data.get("analysis_version", "1.0"),
            "agent": data.get("agent", "Unknown")
        }

    def _create_chapters(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create chapter structure for navigation."""
        chapters = []
        repositories = data.get("repositories", [])

        # Group repositories by categories
        categories = {}
        for repo in repositories:
            category = repo.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(repo)

        # Create chapters for each category
        chapter_num = 1
        for category, repos in categories.items():
            chapter = {
                "number": chapter_num,
                "title": f"Chapter {chapter_num}: {category}",
                "category": category,
                "repositories": repos,
                "summary": self._create_chapter_summary(repos)
            }
            chapters.append(chapter)
            chapter_num += 1

        return chapters

    def _create_chapter_summary(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create summary statistics for a chapter."""
        if not repos:
            return {"total": 0, "stars": 0, "forks": 0, "languages": []}

        total_stars = sum(repo.get("stars", 0) for repo in repos)
        total_forks = sum(repo.get("forks", 0) for repo in repos)
        languages = list(set(repo.get("language", "Unknown") for repo in repos))

        return {
            "total": len(repos),
            "stars": total_stars,
            "forks": total_forks,
            "languages": languages
        }

    def _extract_goldmines(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract goldmine discoveries."""
        goldmines = data.get("goldmines", [])

        # Process and format goldmines
        processed_goldmines = []
        for gm in goldmines:
            processed_gm = {
                "title": gm.get("title", "Untitled Discovery"),
                "description": gm.get("description", ""),
                "category": gm.get("category", "General"),
                "priority": gm.get("priority", "Medium"),
                "repository": gm.get("repository", ""),
                "details": gm.get("details", {})
            }
            processed_goldmines.append(processed_gm)

        return processed_goldmines

    def _create_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create overall analysis summary."""
        analysis_summary = data.get("analysis_summary", {})
        performance_metrics = data.get("performance_metrics", {})

        return {
            "total_repositories": data.get("total_repos", 0),
            "analysis_duration": performance_metrics.get("duration_seconds", 0),
            "success_rate": analysis_summary.get("success_rate", 0),
            "top_languages": analysis_summary.get("top_languages", []),
            "most_active_categories": analysis_summary.get("categories", []),
            "goldmine_count": len(data.get("goldmines", []))
        }

    def _create_navigation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create navigation structure."""
        chapters = self._create_chapters(data)
        total_chapters = len(chapters)

        return {
            "total_chapters": total_chapters,
            "chapter_titles": [ch["title"] for ch in chapters],
            "categories": list(set(ch["category"] for ch in chapters)),
            "has_goldmines": len(data.get("goldmines", [])) > 0
        }

    def search_repositories(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search repositories by name or description."""
        data = self.get_processed_data()
        results = []

        for chapter in data["chapters"]:
            if category and chapter["category"] != category:
                continue

            for repo in chapter["repositories"]:
                name = repo.get("name", "").lower()
                description = repo.get("description", "").lower()
                query_lower = query.lower()

                if query_lower in name or query_lower in description:
                    results.append({
                        "repository": repo,
                        "chapter": chapter["number"],
                        "category": chapter["category"]
                    })

        return results

    def get_chapter_data(self, chapter_number: int) -> Optional[Dict[str, Any]]:
        """Get data for a specific chapter."""
        data = self.get_processed_data()
        chapters = data.get("chapters", [])

        if 1 <= chapter_number <= len(chapters):
            return chapters[chapter_number - 1]
        return None

    def get_goldmine_data(self, goldmine_index: int) -> Optional[Dict[str, Any]]:
        """Get data for a specific goldmine."""
        data = self.get_processed_data()
        goldmines = data.get("goldmines", [])

        if 0 <= goldmine_index < len(goldmines):
            return goldmines[goldmine_index]
        return None