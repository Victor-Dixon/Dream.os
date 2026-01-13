#!/usr/bin/env python3
"""
Template Manager
===============

High-level template management, creation, documentation, and archiving operations.
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from .template_engine import PromptTemplateEngine
from .template_models import PromptTemplate, TemplateVersion, TemplateCategory

logger = logging.getLogger(__name__)


class TemplateUsageGuide:
    """Provides usage guidance and best practices for templates."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the usage guide."""
        self.template_engine = template_engine

    def get_usage_recommendations(self, template_id: str) -> Dict:
        """Get usage recommendations for a specific template."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                return {"error": f"Template {template_id} not found"}
            
            recommendations = {
                "template_id": template_id,
                "template_name": template.name,
                "recommendations": []
            }
            
            # Analyze template type
            if template.type == "quest_generation":
                recommendations["recommendations"].extend([
                    "Use clear, specific quest objectives",
                    "Include difficulty levels and rewards",
                    "Consider player progression context"
                ])
            elif template.type == "content_creation":
                recommendations["recommendations"].extend([
                    "Provide detailed content requirements",
                    "Include tone and style guidelines",
                    "Specify target audience and length"
                ])
            elif template.type == "response_analysis":
                recommendations["recommendations"].extend([
                    "Include context for better analysis",
                    "Specify analysis depth and focus areas",
                    "Provide examples of desired insights"
                ])
            
            # Analyze performance
            if template.success_rate < 0.7:
                recommendations["recommendations"].append(
                    f"Template has low success rate ({template.success_rate:.1%}) - consider revision"
                )
            
            if template.usage_count < 5:
                recommendations["recommendations"].append(
                    "Template has low usage - test with more scenarios"
                )
            
            # Variable analysis
            if template.variables:
                recommendations["variable_guidance"] = {
                    "required_variables": template.variables,
                    "tips": [
                        "Ensure all required variables are provided",
                        "Use descriptive variable names",
                        "Provide fallback values for optional variables"
                    ]
                }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get usage recommendations: {e}")
            return {"error": str(e)}

    def get_best_practices(self) -> List[Dict]:
        """Get general best practices for template usage."""
        return [
            {
                "category": "Template Design",
                "practices": [
                    "Keep templates focused on a single purpose",
                    "Use clear, descriptive variable names",
                    "Include helpful comments in complex templates",
                    "Test templates with various input scenarios"
                ]
            },
            {
                "category": "Variable Management",
                "practices": [
                    "Validate required variables before rendering",
                    "Provide sensible default values",
                    "Use consistent naming conventions",
                    "Document variable purposes and expected formats"
                ]
            },
            {
                "category": "Performance",
                "practices": [
                    "Monitor template success rates regularly",
                    "Optimize complex templates for faster rendering",
                    "Use versioning for major template changes",
                    "Archive unused or deprecated templates"
                ]
            },
            {
                "category": "Maintenance",
                "practices": [
                    "Regularly review and update templates",
                    "Track usage patterns and success metrics",
                    "Backup templates before major changes",
                    "Document template evolution and changes"
                ]
            }
        ]


class TemplateCreator:
    """Handles template creation and management."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the template creator."""
        self.template_engine = template_engine

    def create_custom_template(
        self,
        name: str,
        content: str,
        template_type: str = "custom",
        description: str = None,
        variables: List[str] = None,
    ) -> str:
        """Create a custom template."""
        try:
            template_id = f"custom_{uuid.uuid4().hex[:8]}"
            
            template = PromptTemplate(
                id=template_id,
                type=template_type,
                name=name,
                content=content,
                description=description,
                variables=variables or [],
                metadata={
                    "created_by": "template_creator",
                    "creation_method": "custom",
                    "tags": ["custom", template_type]
                }
            )
            
            template_id = self.template_engine.create_template(template)
            logger.info(f"Created custom template: {template_id}")
            
            return template_id
            
        except Exception as e:
            logger.error(f"Failed to create custom template: {e}")
            raise

    def create_personal_template(
        self,
        name: str,
        content: str,
        user_id: str = "default",
        description: str = None,
        variables: List[str] = None,
    ) -> str:
        """Create a personal template for a specific user."""
        try:
            template_id = f"personal_{user_id}_{uuid.uuid4().hex[:8]}"
            
            template = PromptTemplate(
                id=template_id,
                type="personal",
                name=name,
                content=content,
                description=description,
                variables=variables or [],
                metadata={
                    "created_by": "template_creator",
                    "creation_method": "personal",
                    "user_id": user_id,
                    "tags": ["personal", user_id]
                }
            )
            
            template_id = self.template_engine.create_template(template)
            logger.info(f"Created personal template for user {user_id}: {template_id}")
            
            return template_id
            
        except Exception as e:
            logger.error(f"Failed to create personal template: {e}")
            raise

    def create_template_from_file(self, file_path: str, template_type: str = "file") -> str:
        """Create a template from a file."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Template file not found: {file_path}")
            
            content = file_path.read_text(encoding='utf-8')
            name = file_path.stem
            
            return self.create_custom_template(
                name=name,
                content=content,
                template_type=template_type,
                description=f"Template created from file: {file_path.name}",
                variables=self._extract_variables_from_content(content)
            )
            
        except Exception as e:
            logger.error(f"Failed to create template from file: {e}")
            raise

    def _extract_variables_from_content(self, content: str) -> List[str]:
        """Extract variable names from template content."""
        import re
        
        # Find Jinja2 variables {{ variable_name }}
        jinja_vars = re.findall(r'\{\{\s*(\w+)\s*\}\}', content)
        
        # Find Jinja2 blocks {% for variable in variables %}
        jinja_blocks = re.findall(r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}', content)
        
        variables = set(jinja_vars)
        for var in jinja_blocks:
            variables.add(var[1])  # Add the list variable name
        
        return list(variables)


class TemplateDocumentation:
    """Handles template documentation and metadata."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the documentation manager."""
        self.template_engine = template_engine

    def add_documentation(self, template_id: str, documentation: Dict) -> bool:
        """Add documentation to a template."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                logger.error(f"Template {template_id} not found")
                return False
            
            # Update template metadata with documentation
            updated_metadata = template.metadata.copy()
            updated_metadata.update({
                "documentation": documentation,
                "documentation_updated": datetime.now().isoformat()
            })
            
            # Create new version with updated metadata
            version = TemplateVersion(
                template_id=template_id,
                version=f"{template.version}.1",  # Increment minor version
                content=template.content,
                changes="Added documentation",
                performance_data=template.metadata.get("performance_data", {}),
                created_by="template_documentation",
                is_active=True
            )
            
            # Update the template
            success = self.template_engine.create_version(version)
            if success:
                logger.info(f"Added documentation to template {template_id}")
                return True
            else:
                logger.error(f"Failed to create version for template {template_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to add documentation: {e}")
            return False

    def get_documentation(self, template_id: str) -> Dict:
        """Get documentation for a template."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                return {"error": f"Template {template_id} not found"}
            
            documentation = template.metadata.get("documentation", {})
            
            return {
                "template_id": template_id,
                "template_name": template.name,
                "documentation": documentation,
                "last_updated": template.metadata.get("documentation_updated"),
                "template_info": {
                    "type": template.type,
                    "version": template.version,
                    "created_at": template.created_at.isoformat() if template.created_at else None,
                    "updated_at": template.updated_at.isoformat() if template.updated_at else None
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get documentation: {e}")
            return {"error": str(e)}

    def generate_documentation_template(self, template_id: str) -> Dict:
        """Generate a documentation template for a template."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                return {"error": f"Template {template_id} not found"}
            
            doc_template = {
                "purpose": "Describe the main purpose of this template",
                "usage_scenarios": [
                    "List common use cases for this template"
                ],
                "required_variables": {
                    var: "Describe what this variable should contain"
                    for var in (template.variables or [])
                },
                "optional_variables": {
                    "variable_name": "Describe optional variables"
                },
                "examples": [
                    {
                        "variables": {
                            "example_var": "example_value"
                        },
                        "expected_output": "Example of expected rendered output"
                    }
                ],
                "best_practices": [
                    "List best practices for using this template"
                ],
                "limitations": [
                    "List any limitations or constraints"
                ],
                "related_templates": [
                    "List related or similar templates"
                ]
            }
            
            return {
                "template_id": template_id,
                "template_name": template.name,
                "documentation_template": doc_template
            }
            
        except Exception as e:
            logger.error(f"Failed to generate documentation template: {e}")
            return {"error": str(e)}


class LegacyTemplateArchiver:
    """Handles archiving of legacy or deprecated templates."""
    
    def __init__(self, template_engine: PromptTemplateEngine):
        """Initialize the archiver."""
        self.template_engine = template_engine

    def archive_template(self, template_id: str, reason: str = "Legacy") -> bool:
        """Archive a template with a reason."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                logger.error(f"Template {template_id} not found")
                return False
            
            # Create archive version
            archive_version = TemplateVersion(
                template_id=template_id,
                version=f"{template.version}_archived",
                content=template.content,
                changes=f"Archived: {reason}",
                performance_data={
                    "archive_reason": reason,
                    "archive_date": datetime.now().isoformat(),
                    "final_usage_count": template.usage_count,
                    "final_success_rate": template.success_rate
                },
                created_by="template_archiver",
                is_active=False  # Archive versions are inactive
            )
            
            # Create the archive version
            success = self.template_engine.create_version(archive_version)
            if not success:
                logger.error(f"Failed to create archive version for {template_id}")
                return False
            
            # Update template metadata
            updated_metadata = template.metadata.copy()
            updated_metadata.update({
                "archived": True,
                "archive_reason": reason,
                "archive_date": datetime.now().isoformat(),
                "archived_by": "template_archiver"
            })
            
            # Create final version marking as archived
            final_version = TemplateVersion(
                template_id=template_id,
                version=f"{template.version}_final",
                content=template.content,
                changes=f"Template archived: {reason}",
                performance_data=updated_metadata,
                created_by="template_archiver",
                is_active=False
            )
            
            success = self.template_engine.create_version(final_version)
            if success:
                logger.info(f"Successfully archived template {template_id}: {reason}")
                return True
            else:
                logger.error(f"Failed to create final version for archived template {template_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to archive template: {e}")
            return False

    def get_archived_templates(self) -> List[Dict]:
        """Get list of archived templates."""
        try:
            # Get all templates and filter for archived ones
            all_templates = self.template_engine.find_templates(active_only=False)
            
            archived = []
            for template in all_templates:
                if template.metadata.get("archived", False):
                    archived.append({
                        "template_id": template.id,
                        "template_name": template.name,
                        "archive_reason": template.metadata.get("archive_reason"),
                        "archive_date": template.metadata.get("archive_date"),
                        "final_usage_count": template.usage_count,
                        "final_success_rate": template.success_rate,
                        "version": template.version
                    })
            
            return archived
            
        except Exception as e:
            logger.error(f"Failed to get archived templates: {e}")
            return []

    def restore_template(self, template_id: str) -> bool:
        """Restore an archived template."""
        try:
            template = self.template_engine.get_template(template_id)
            if not template:
                logger.error(f"Template {template_id} not found")
                return False
            
            if not template.metadata.get("archived", False):
                logger.warning(f"Template {template_id} is not archived")
                return False
            
            # Update metadata to remove archived status
            updated_metadata = template.metadata.copy()
            updated_metadata.update({
                "archived": False,
                "restored_date": datetime.now().isoformat(),
                "restored_by": "template_archiver"
            })
            
            # Create restoration version
            restore_version = TemplateVersion(
                template_id=template_id,
                version=f"{template.version}_restored",
                content=template.content,
                changes="Template restored from archive",
                performance_data=updated_metadata,
                created_by="template_archiver",
                is_active=True
            )
            
            success = self.template_engine.create_version(restore_version)
            if success:
                logger.info(f"Successfully restored template {template_id}")
                return True
            else:
                logger.error(f"Failed to restore template {template_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to restore template: {e}")
            return False 