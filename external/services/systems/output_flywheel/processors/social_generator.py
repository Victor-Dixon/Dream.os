"""
Social Post Generator Processor (S5)
===================================

Renders a social-ready post (main + optional thread) from story data
using the `social_post.md.j2` template.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    HAS_JINJA2 = True
except Exception:  # pragma: no cover
    HAS_JINJA2 = False
    Environment = None  # type: ignore


def _build_env(template_dir: Path) -> Any:
    if not HAS_JINJA2:
        raise RuntimeError("jinja2 is required to render social templates")
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _build_main_post(story: Dict[str, Any]) -> str:
    overview = story.get("overview") or ""
    lessons = story.get("lessons") or []
    if not lessons:
        return overview[:240]

    lesson_titles = [l.get("title") for l in lessons if isinstance(l, dict)]
    lesson_part = "; ".join(title for title in lesson_titles if title)[:120]
    base = overview[:140]
    if lesson_part:
        return f"{base} | Key lessons: {lesson_part}"
    return base


def _build_thread_posts(story: Dict[str, Any]) -> List[str]:
    posts: List[str] = []
    for lesson in story.get("lessons") or []:
        if not isinstance(lesson, dict):
            continue
        title = lesson.get("title") or "Lesson"
        description = lesson.get("description") or ""
        text = f"{title}: {description}"
        posts.append(text[:260])
    return posts


def generate_social_post(
    story: Dict[str, Any],
    output_dir: Path,
    template_path: Path,
    platform: str = "twitter",
    session_id: Optional[str] = None,
    hashtags: Optional[List[str]] = None,
    mentions: Optional[List[str]] = None,
) -> Path:
    """
    Generate a social post artifact using the configured template.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    env = _build_env(template_path.parent)
    template = env.get_template(template_path.name)

    main_post = _build_main_post(story)
    thread_posts = _build_thread_posts(story)

    if hashtags is None:
        hashtags = ["DreamOS", "buildinpublic"]

    context: Dict[str, Any] = {
        "title": story.get("title") or "Dream.OS Session",
        "platform": platform,
        "post_type": "Thread" if thread_posts else "Single",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "main_post": main_post,
        "thread_posts": thread_posts,
        "hashtags": hashtags,
        "mentions": mentions or [],
        "character_count": len(main_post),
        "session_id": session_id or "unknown-session",
    }

    file_path = output_dir / f"social_post_{context['session_id']}.md"
    file_path.write_text(template.render(**context), encoding="utf-8")
    logger.info("Social post generated at %s", file_path)
    return file_path


