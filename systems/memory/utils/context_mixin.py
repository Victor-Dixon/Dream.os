"""
Context Manager Mixin
====================

Provides common context manager functionality for database and resource management.
"""

class ContextManagerMixin:
    """Mixin providing standard context manager functionality."""
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()
    
    def close(self):
        """Close the resource. Override in subclasses."""
        pass
