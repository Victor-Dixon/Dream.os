#!/usr/bin/env python3
"""
Template System
==============

Main interface for the modular template system.
This file provides integration and backward compatibility for all template components.

Components:
- template_models.py: Data models and enums
- template_engine.py: Core rendering and database operations
- template_processors.py: Analytics, response management, debugging
- template_manager.py: High-level management, creation, documentation
"""

import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Import all components
from .template_models import (
    PromptTemplate, TemplateVersion, TemplateUsage, TemplateMetrics,
    PerformanceReport, TemplateCategory, MetricType,
    _safe_templateusage_from_dict, _safe_fromisoformat
)
from .template_engine import PromptTemplateEngine, render_template
from .template_processors import (
    TemplateResponseManager, TemplatePerformanceAnalytics,
    TemplateDebugger, ContextualTemplateSender
)
from .template_manager import (
    TemplateUsageGuide, TemplateCreator, TemplateDocumentation,
    LegacyTemplateArchiver
)

# Configure logging
logger = logging.getLogger(__name__)


class TemplateSystem:
    """Main template system interface that integrates all components."""
    
    def __init__(self, db_path: str = None):
        """Initialize the template system with all components."""
        self.engine = PromptTemplateEngine(db_path)
        
        # Initialize all processors
        self.response_manager = TemplateResponseManager(self.engine)
        self.analytics = TemplatePerformanceAnalytics(self.engine)
        self.debugger = TemplateDebugger(self.engine)
        self.contextual_sender = ContextualTemplateSender(self.engine)
        
        # Initialize all managers
        self.usage_guide = TemplateUsageGuide(self.engine)
        self.creator = TemplateCreator(self.engine)
        self.documentation = TemplateDocumentation(self.engine)
        self.archiver = LegacyTemplateArchiver(self.engine)
        
        logger.info("Template system initialized with all components")

    # Core Engine Methods (delegated)
    def create_template(self, template: PromptTemplate) -> str:
        """Create a new template."""
        return self.engine.create_template(template)

    def get_template(self, template_id: str, version: Optional[str] = None) -> Optional[PromptTemplate]:
        """Get a template by ID."""
        return self.engine.get_template(template_id, version)

    def render_template(self, template_id: str, variables: Dict, version: Optional[str] = None) -> str:
        """Render a template with variables."""
        return self.engine.render_template(template_id, variables, version)

    def find_templates(self, template_type: Optional[str] = None, 
                      min_success_rate: Optional[float] = None, 
                      active_only: bool = True) -> List[PromptTemplate]:
        """Find templates based on criteria."""
        return self.engine.find_templates(template_type, min_success_rate, active_only)

    # Response Management Methods
    def process_response(self, template_id: str, response: str, success: bool = True) -> Dict:
        """Process a template response."""
        return self.response_manager.process_template_response(template_id, response, success)

    def get_performance(self, template_id: str) -> Dict:
        """Get performance metrics for a template."""
        return self.response_manager.get_template_performance(template_id)

    # Analytics Methods
    def record_usage(self, usage: TemplateUsage):
        """Record template usage for analytics."""
        self.analytics.record_template_usage(usage)

    def get_analytics(self, template_id: str) -> Optional[TemplateMetrics]:
        """Get analytics for a template."""
        return self.analytics.get_template_metrics(template_id)

    def generate_report(self, time_period: str = "30d") -> PerformanceReport:
        """Generate performance report."""
        return self.analytics.generate_performance_report(time_period)

    def get_top_performers(self, limit: int = 10) -> List[TemplateMetrics]:
        """Get top performing templates."""
        return self.analytics.get_top_performers(limit)

    def get_needs_optimization(self, priority: str = "high") -> List[TemplateMetrics]:
        """Get templates that need optimization."""
        return self.analytics.get_needs_optimization(priority)

    # Debugging Methods
    def debug_template(self, template_id: str, variables: Dict) -> Dict:
        """Debug template rendering."""
        return self.debugger.debug_template_rendering(template_id, variables)

    # Contextual Sending Methods
    def send_with_context(self, template_id: str, context: Dict, 
                         additional_vars: Dict = None) -> str:
        """Send template with contextual information."""
        return self.contextual_sender.send_with_context(template_id, context, additional_vars)

    # Usage Guide Methods
    def get_recommendations(self, template_id: str) -> Dict:
        """Get usage recommendations for a template."""
        return self.usage_guide.get_usage_recommendations(template_id)

    def get_best_practices(self) -> List[Dict]:
        """Get general best practices."""
        return self.usage_guide.get_best_practices()

    # Creation Methods
    def create_custom_template(self, name: str, content: str, 
                              template_type: str = "custom", 
                              description: str = None, 
                              variables: List[str] = None) -> str:
        """Create a custom template."""
        return self.creator.create_custom_template(name, content, template_type, 
                                                 description, variables)

    def create_personal_template(self, name: str, content: str, 
                                user_id: str = "default", 
                                description: str = None, 
                                variables: List[str] = None) -> str:
        """Create a personal template."""
        return self.creator.create_personal_template(name, content, user_id, 
                                                   description, variables)

    def create_from_file(self, file_path: str, template_type: str = "file") -> str:
        """Create template from file."""
        return self.creator.create_template_from_file(file_path, template_type)

    # Documentation Methods
    def add_documentation(self, template_id: str, documentation: Dict) -> bool:
        """Add documentation to a template."""
        return self.documentation.add_documentation(template_id, documentation)

    def get_documentation(self, template_id: str) -> Dict:
        """Get documentation for a template."""
        return self.documentation.get_documentation(template_id)

    def generate_doc_template(self, template_id: str) -> Dict:
        """Generate documentation template."""
        return self.documentation.generate_documentation_template(template_id)

    # Archiving Methods
    def archive_template(self, template_id: str, reason: str = "Legacy") -> bool:
        """Archive a template."""
        return self.archiver.archive_template(template_id, reason)

    def get_archived_templates(self) -> List[Dict]:
        """Get list of archived templates."""
        return self.archiver.get_archived_templates()

    def restore_template(self, template_id: str) -> bool:
        """Restore an archived template."""
        return self.archiver.restore_template(template_id)

    # Utility Methods
    def close(self):
        """Close the template system and clean up resources."""
        self.engine.close()
        logger.info("Template system closed")

    def get_system_info(self) -> Dict:
        """Get system information and statistics."""
        try:
            templates = self.find_templates(active_only=True)
            archived = self.get_archived_templates()
            
            return {
                "active_templates": len(templates),
                "archived_templates": len(archived),
                "total_templates": len(templates) + len(archived),
                "system_status": "operational",
                "components": {
                    "engine": "initialized",
                    "analytics": "initialized",
                    "response_manager": "initialized",
                    "debugger": "initialized",
                    "usage_guide": "initialized",
                    "creator": "initialized",
                    "documentation": "initialized",
                    "archiver": "initialized"
                }
            }
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {"error": str(e)}


# Global instance for backward compatibility
_template_system = None


def get_template_system(db_path: str = None) -> TemplateSystem:
    """Get the global template system instance."""
    global _template_system
    if _template_system is None:
        _template_system = TemplateSystem(db_path)
    return _template_system


# Backward compatibility functions
def create_template(template: PromptTemplate) -> str:
    """Create a template (backward compatibility)."""
    return get_template_system().create_template(template)


def get_template(template_id: str, version: Optional[str] = None) -> Optional[PromptTemplate]:
    """Get a template (backward compatibility)."""
    return get_template_system().get_template(template_id, version)


def find_templates(template_type: Optional[str] = None, 
                  min_success_rate: Optional[float] = None, 
                  active_only: bool = True) -> List[PromptTemplate]:
    """Find templates (backward compatibility)."""
    return get_template_system().find_templates(template_type, min_success_rate, active_only)


def process_template_response(template_id: str, response: str, success: bool = True) -> Dict:
    """Process template response (backward compatibility)."""
    return get_template_system().process_response(template_id, response, success)


def get_template_performance(template_id: str) -> Dict:
    """Get template performance (backward compatibility)."""
    return get_template_system().get_performance(template_id)


def record_template_usage(usage: TemplateUsage):
    """Record template usage (backward compatibility)."""
    get_template_system().record_usage(usage)


def generate_performance_report(time_period: str = "30d") -> PerformanceReport:
    """Generate performance report (backward compatibility)."""
    return get_template_system().generate_report(time_period)


def debug_template_rendering(template_id: str, variables: Dict) -> Dict:
    """Debug template rendering (backward compatibility)."""
    return get_template_system().debug_template(template_id, variables)


def create_custom_template(name: str, content: str, 
                          template_type: str = "custom", 
                          description: str = None, 
                          variables: List[str] = None) -> str:
    """Create custom template (backward compatibility)."""
    return get_template_system().create_custom_template(name, content, template_type, 
                                                       description, variables)


def archive_template(template_id: str, reason: str = "Legacy") -> bool:
    """Archive template (backward compatibility)."""
    return get_template_system().archive_template(template_id, reason)


# Main function for testing
def main():
    """Main function for testing the template system."""
    try:
        # Initialize system
        system = TemplateSystem()
        
        # Test system info
        info = system.get_system_info()
        print("Template System Info:")
        print(f"Active templates: {info['active_templates']}")
        print(f"Archived templates: {info['archived_templates']}")
        print(f"Total templates: {info['total_templates']}")
        
        # Test creating a simple template
        template_id = system.create_custom_template(
            name="Test Template",
            content="Hello {{ name }}, welcome to {{ platform }}!",
            template_type="test",
            description="A simple test template",
            variables=["name", "platform"]
        )
        
        print(f"Created template: {template_id}")
        
        # Test rendering
        rendered = system.render_template(template_id, {
            "name": "User",
            "platform": "Dreamscape"
        })
        print(f"Rendered: {rendered}")
        
        # Test response processing
        result = system.process_response(template_id, rendered, True)
        print(f"Response processed: {result}")
        
        # Test debugging
        debug_info = system.debug_template(template_id, {
            "name": "Debug User",
            "platform": "Debug Platform"
        })
        print(f"Debug info: {debug_info}")
        
        # Test recommendations
        recommendations = system.get_recommendations(template_id)
        print(f"Recommendations: {recommendations}")
        
        # Clean up
        system.close()
        
        print("Template system test completed successfully!")
        
    except Exception as e:
        logger.error(f"Template system test failed: {e}")
        print(f"Test failed: {e}")


if __name__ == "__main__":
    main()
