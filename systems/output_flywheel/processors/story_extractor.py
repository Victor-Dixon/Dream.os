"""
Story Extractor Processor (S2)
==============================

Turns raw repo / session data into a narrative-friendly structure
for README, blog posts, and social content.

This is intentionally lightweight: it does not attempt deep NLP, but
extracts headlines, bullet points, and simple metrics from the
`work_session.json`-style data or a repo scan result.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class StoryLesson:
    title: str
    description: str


@dataclass
class StorySummary:
    title: str
    overview: str
    problem: Optional[str]
    solution: Optional[str]
    lessons: List[StoryLesson]
    next_steps: List[str]


def _default_title(session_type: str, repo_name: Optional[str]) -> str:
    if session_type == "trade":
        return "Trading Session Summary"
    if session_type == "life_aria":
        return "Aria Build Session Summary"
    if repo_name:
        return f"{repo_name} - Build Session"
    return "Build Session Summary"


def _derive_overview(session: Dict[str, Any]) -> str:
    metadata = session.get("metadata", {}) or {}
    files_changed = metadata.get("files_changed")
    commits = metadata.get("commits")
    duration = metadata.get("duration_minutes")

    parts: List[str] = []
    if files_changed:
        parts.append(f"touched {files_changed} files")
    if commits:
        parts.append(f"made {commits} commits")
    if duration:
        parts.append(f"over {duration} minutes")

    base = "This session focused on meaningful work in the Dream.OS ecosystem"
    if parts:
        return f"{base}, where the agent {', '.join(parts)}."
    return base + "."


def _default_lessons(session_type: str) -> List[StoryLesson]:
    if session_type == "trade":
        return [
            StoryLesson(
                title="Risk Management",
                description="Position sizing and stop placement are as important as entry timing.",
            )
        ]
    if session_type == "life_aria":
        return [
            StoryLesson(
                title="Rapid Prototyping",
                description="Small, iterative experiments with Aria lead to better designs.",
            )
        ]
    return [
        StoryLesson(
            title="Iterative Development",
            description="Short feedback cycles produce more reliable features.",
        )
    ]


def _default_next_steps(session_type: str) -> List[str]:
    if session_type == "trade":
        return [
            "Review trade journal for recurring patterns.",
            "Tighten risk parameters for next session.",
        ]
    if session_type == "life_aria":
        return [
            "Polish UX for the current build.",
            "Capture screenshots and short clips for the portfolio.",
        ]
    return [
        "Refine recently added features based on feedback.",
        "Improve documentation and developer onboarding.",
    ]


def extract_story_from_session(session: Dict[str, Any]) -> StorySummary:
    """
    Main S2 entry point: extract a StorySummary from a work_session dict.
    """
    session_type = session.get("session_type", "build")
    source_data = session.get("source_data") or {}
    repo_path = source_data.get("repo_path")
    repo_name = None
    if isinstance(repo_path, str) and repo_path:
        repo_name = repo_path.rstrip("/").split("/")[-1]

    custom_overview = session.get("overview")
    custom_problem = session.get("problem")
    custom_solution = session.get("solution")

    lessons_raw = session.get("lessons") or []
    lessons: List[StoryLesson] = []
    for item in lessons_raw:
        if not isinstance(item, dict):
            continue
        title = item.get("title") or "Lesson"
        description = item.get("description") or ""
        lessons.append(StoryLesson(title=title, description=description))

    if not lessons:
        lessons = _default_lessons(session_type)

    next_steps = session.get("next_steps") or _default_next_steps(session_type)

    summary = StorySummary(
        title=_default_title(session_type, repo_name),
        overview=custom_overview or _derive_overview(session),
        problem=custom_problem,
        solution=custom_solution,
        lessons=lessons,
        next_steps=[str(step) for step in next_steps],
    )

    logger.info(
        "Story extracted for session %s (type=%s)", session.get("session_id"), session_type
    )
    return summary


def story_to_dict(summary: StorySummary) -> Dict[str, Any]:
    """Convert StorySummary to a plain dict for templates."""
    return {
        "title": summary.title,
        "overview": summary.overview,
        "problem": summary.problem,
        "solution": summary.solution,
        "lessons": [
            {"title": lesson.title, "description": lesson.description}
            for lesson in summary.lessons
        ],
        "next_steps": summary.next_steps,
    }


