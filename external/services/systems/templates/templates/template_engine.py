#!/usr/bin/env python3
"""
Template Engine
==============

Core template rendering and database operations for the template system.
"""

import json
import logging
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union
from jinja2 import Environment, BaseLoader, TemplateNotFound

from dreamscape.core.utils.database_mixin import DatabaseCleanupMixin
from dreamscape.core.config import TEMPLATES_DB_PATH
from .template_models import PromptTemplate, TemplateVersion

logger = logging.getLogger(__name__)


class PromptTemplateEngine(DatabaseCleanupMixin):
    """Core template engine for rendering and database operations."""
    
    def __init__(self, db_path: Union[str, Path] = TEMPLATES_DB_PATH):
        """Initialize the template engine with thread-local database connection."""
        self.db_path = Path(db_path)
        self._local = threading.local()
        self.jinja_env = Environment(
            loader=BaseLoader(), 
            autoescape=False, 
            trim_blocks=True, 
            lstrip_blocks=True
        )

    @property
    def conn(self):
        """Get a thread-local SQLite connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(
                str(self.db_path), 
                check_same_thread=False
            )
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    def create_template(self, template: PromptTemplate) -> str:
        """Create a new prompt template."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO prompt_templates (
                    id, parent_id, type, name, description, content,
                    variables, metadata, version, created_at, updated_at,
                    is_active, success_rate, usage_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    template.id,
                    template.parent_id,
                    template.type,
                    template.name,
                    template.description,
                    template.content,
                    json.dumps(template.variables or []),
                    json.dumps(template.metadata or {}),
                    template.version,
                    template.created_at or datetime.now(),
                    template.updated_at or datetime.now(),
                    template.is_active,
                    template.success_rate,
                    template.usage_count,
                ),
            )

            # Create initial version
            cursor.execute(
                """
                INSERT INTO template_versions (
                    template_id, version, content, created_at, is_active
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (template.id, template.version, template.content, datetime.now(), True),
            )

            self.conn.commit()
            return template.id
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to create template: {e}")

    def get_template(
        self, template_id: str, version: Optional[str] = None
    ) -> Optional[PromptTemplate]:
        """Retrieve a template by ID and optionally specific version."""
        cursor = self.conn.cursor()

        if version:
            cursor.execute(
                """
                SELECT t.*, v.content as version_content
                FROM prompt_templates t
                JOIN template_versions v ON t.id = v.template_id
                WHERE t.id = ? AND v.version = ? AND v.is_active = 1
            """,
                (template_id, version),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM prompt_templates WHERE id = ? AND is_active = 1
            """,
                (template_id,),
            )

        row = cursor.fetchone()
        if not row:
            return None

        return PromptTemplate(
            id=row["id"],
            type=row["type"],
            name=row["name"],
            content=row.get("version_content", row["content"]),
            parent_id=row["parent_id"],
            description=row["description"],
            variables=json.loads(row["variables"]) if row["variables"] else [],
            metadata=json.loads(row["metadata"]) if row["metadata"] else {},
            version=row["version"],
            created_at=(
                datetime.fromisoformat(row["created_at"]) if row["created_at"] else None
            ),
            updated_at=(
                datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None
            ),
            is_active=bool(row["is_active"]),
            success_rate=float(row["success_rate"]),
            usage_count=int(row["usage_count"]),
        )

    def create_version(self, version: TemplateVersion) -> bool:
        """Create a new version of an existing template."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO template_versions (
                    template_id, version, content, changes, performance_data,
                    created_at, created_by, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    version.template_id,
                    version.version,
                    version.content,
                    version.changes,
                    json.dumps(version.performance_data or {}),
                    version.created_at or datetime.now(),
                    version.created_by,
                    version.is_active,
                ),
            )

            # Update main template
            cursor.execute(
                """
                UPDATE prompt_templates 
                SET version = ?, updated_at = ?
                WHERE id = ?
            """,
                (version.version, datetime.now(), version.template_id),
            )

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to create version: {e}")

    def render_template(
        self, template_id: str, variables: Dict, version: Optional[str] = None
    ) -> str:
        """Render a template with the given variables."""
        template = self.get_template(template_id, version)
        if not template:
            raise TemplateNotFound(f"Template {template_id} not found")

        try:
            jinja_template = self.jinja_env.from_string(template.content)
            rendered = jinja_template.render(**variables)

            # Update usage stats
            self._update_usage_stats(template_id)

            return rendered
        except Exception as e:
            raise Exception(f"Failed to render template: {e}")

    def _update_usage_stats(self, template_id: str) -> None:
        """Update template usage statistics."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE prompt_templates 
            SET usage_count = usage_count + 1, updated_at = ?
            WHERE id = ?
        """,
            (datetime.now(), template_id),
        )
        self.conn.commit()

    def update_success_rate(self, template_id: str, success: bool) -> None:
        """Update template success rate based on usage outcome."""
        cursor = self.conn.cursor()

        # Get current stats
        cursor.execute(
            """
            SELECT success_rate, usage_count FROM prompt_templates WHERE id = ?
        """,
            (template_id,),
        )
        row = cursor.fetchone()
        if not row:
            return

        current_success_rate = float(row["success_rate"])
        usage_count = int(row["usage_count"])

        # Calculate new success rate
        if success:
            new_success_rate = (current_success_rate * usage_count + 1) / (usage_count + 1)
        else:
            new_success_rate = (current_success_rate * usage_count) / (usage_count + 1)

        # Update the template
        cursor.execute(
            """
            UPDATE prompt_templates 
            SET success_rate = ?, updated_at = ?
            WHERE id = ?
        """,
            (new_success_rate, datetime.now(), template_id),
        )
        self.conn.commit()

    def get_template_versions(self, template_id: str) -> List[TemplateVersion]:
        """Get all versions of a template."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM template_versions 
            WHERE template_id = ? 
            ORDER BY created_at DESC
        """,
            (template_id,),
        )

        versions = []
        for row in cursor.fetchall():
            versions.append(
                TemplateVersion(
                    template_id=row["template_id"],
                    version=row["version"],
                    content=row["content"],
                    changes=row["changes"],
                    performance_data=json.loads(row["performance_data"]) if row["performance_data"] else {},
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
                    created_by=row["created_by"],
                    is_active=bool(row["is_active"]),
                )
            )

        return versions

    def get_template_hierarchy(self, template_id: str) -> List[PromptTemplate]:
        """Get the full hierarchy of a template (parent chain)."""
        hierarchy = []
        current_id = template_id

        while current_id:
            template = self.get_template(current_id)
            if template:
                hierarchy.append(template)
                current_id = template.parent_id
            else:
                break

        return list(reversed(hierarchy))  # Return from root to leaf

    def find_templates(
        self,
        template_type: Optional[str] = None,
        min_success_rate: Optional[float] = None,
        active_only: bool = True,
    ) -> List[PromptTemplate]:
        """Find templates based on criteria."""
        cursor = self.conn.cursor()

        query = "SELECT * FROM prompt_templates WHERE 1=1"
        params = []

        if template_type:
            query += " AND type = ?"
            params.append(template_type)

        if min_success_rate is not None:
            query += " AND success_rate >= ?"
            params.append(min_success_rate)

        if active_only:
            query += " AND is_active = 1"

        query += " ORDER BY usage_count DESC, success_rate DESC"

        cursor.execute(query, params)

        templates = []
        for row in cursor.fetchall():
            templates.append(
                PromptTemplate(
                    id=row["id"],
                    type=row["type"],
                    name=row["name"],
                    content=row["content"],
                    parent_id=row["parent_id"],
                    description=row["description"],
                    variables=json.loads(row["variables"]) if row["variables"] else [],
                    metadata=json.loads(row["metadata"]) if row["metadata"] else {},
                    version=row["version"],
                    created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
                    updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
                    is_active=bool(row["is_active"]),
                    success_rate=float(row["success_rate"]),
                    usage_count=int(row["usage_count"]),
                )
            )

        return templates

    def close(self):
        """Close the database connection."""
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None


# Convenience function for simple template rendering
def render_template(template_id: str, variables: Dict) -> str:
    """Convenience function to render a template."""
    engine = PromptTemplateEngine()
    try:
        return engine.render_template(template_id, variables)
    finally:
        engine.close()