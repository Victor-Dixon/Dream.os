#!/usr/bin/env python3
"""
RBAC Manager - Phase 5 Advanced Security
========================================

Role-Based Access Control system for enterprise authorization.
Provides granular permission management and access control enforcement.

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

from enum import Enum
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    VIEWER = "viewer"
    GUEST = "guest"

class Resource(str, Enum):
    """Protected resource enumeration."""
    REVENUE_ENGINE = "revenue_engine"
    ANALYTICS = "analytics"
    USERS = "users"
    SYSTEM = "system"
    CONFIG = "config"
    LOGS = "logs"

class Action(str, Enum):
    """Action enumeration."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    MANAGE = "manage"

@dataclass
class Permission:
    """Permission definition."""
    resource: str
    action: str

    def __str__(self):
        return f"{self.resource}:{self.action}"

    def matches(self, other: 'Permission') -> bool:
        """Check if this permission matches another permission."""
        return self.resource == other.resource and (
            self.action == other.action or self.action == "*" or other.action == "*"
        )

class RBACManager:
    """
    Role-Based Access Control Manager

    Provides enterprise-grade authorization with hierarchical roles
    and granular permission management.
    """

    def __init__(self):
        """Initialize RBAC manager with default role permissions."""
        self.role_permissions: Dict[UserRole, Set[Permission]] = {}
        self.role_hierarchy: Dict[UserRole, Set[UserRole]] = {}
        self._initialize_default_permissions()
        self._initialize_role_hierarchy()

        logger.info("✅ RBAC Manager initialized")

    def _initialize_default_permissions(self):
        """Initialize default permissions for each role."""
        # Admin: Full access to everything
        self.role_permissions[UserRole.ADMIN] = {
            Permission("*", "*"),  # Wildcard permission
        }

        # Analyst: Read/write analytics, read revenue data
        self.role_permissions[UserRole.ANALYST] = {
            Permission(Resource.REVENUE_ENGINE, Action.READ),
            Permission(Resource.ANALYTICS, Action.READ),
            Permission(Resource.ANALYTICS, Action.CREATE),
            Permission(Resource.ANALYTICS, Action.UPDATE),
            Permission(Resource.LOGS, Action.READ),
        }

        # Developer: Code and system access
        self.role_permissions[UserRole.DEVELOPER] = {
            Permission(Resource.REVENUE_ENGINE, Action.READ),
            Permission(Resource.ANALYTICS, Action.READ),
            Permission(Resource.SYSTEM, Action.READ),
            Permission(Resource.CONFIG, Action.READ),
            Permission(Resource.LOGS, Action.READ),
        }

        # Viewer: Read-only access
        self.role_permissions[UserRole.VIEWER] = {
            Permission(Resource.REVENUE_ENGINE, Action.READ),
            Permission(Resource.ANALYTICS, Action.READ),
            Permission(Resource.LOGS, Action.READ),
        }

        # Guest: Minimal access
        self.role_permissions[UserRole.GUEST] = {
            Permission(Resource.REVENUE_ENGINE, Action.READ),
        }

    def _initialize_role_hierarchy(self):
        """Initialize role hierarchy (higher roles inherit lower role permissions)."""
        self.role_hierarchy = {
            UserRole.ADMIN: {UserRole.ANALYST, UserRole.DEVELOPER, UserRole.VIEWER, UserRole.GUEST},
            UserRole.ANALYST: {UserRole.VIEWER, UserRole.GUEST},
            UserRole.DEVELOPER: {UserRole.VIEWER, UserRole.GUEST},
            UserRole.VIEWER: {UserRole.GUEST},
            UserRole.GUEST: set(),
        }

    def get_role_permissions(self, role: UserRole) -> Set[Permission]:
        """
        Get all permissions for a role including inherited permissions.

        Args:
            role: User role

        Returns:
            Set of all permissions for the role
        """
        permissions = self.role_permissions.get(role, set()).copy()

        # Add inherited permissions
        for inherited_role in self.role_hierarchy.get(role, set()):
            permissions.update(self.role_permissions.get(inherited_role, set()))

        return permissions

    def has_permission(self, user_role: UserRole, resource: str, action: str) -> bool:
        """
        Check if a user role has permission for a specific action on a resource.

        Args:
            user_role: User's role
            resource: Target resource
            action: Requested action

        Returns:
            True if permission granted
        """
        requested_permission = Permission(resource, action)
        user_permissions = self.get_role_permissions(user_role)

        # Check for exact match or wildcard permissions
        for permission in user_permissions:
            if permission.matches(requested_permission):
                return True

        return False

    def add_role_permission(self, role: UserRole, permission: Permission):
        """
        Add a permission to a role.

        Args:
            role: Target role
            permission: Permission to add
        """
        if role not in self.role_permissions:
            self.role_permissions[role] = set()

        self.role_permissions[role].add(permission)
        logger.info(f"✅ Added permission {permission} to role {role}")

    def remove_role_permission(self, role: UserRole, permission: Permission):
        """
        Remove a permission from a role.

        Args:
            role: Target role
            permission: Permission to remove
        """
        if role in self.role_permissions:
            self.role_permissions[role].discard(permission)
            logger.info(f"✅ Removed permission {permission} from role {role}")

    def create_custom_role(self, role_name: str, permissions: List[Permission],
                          inherits_from: Optional[UserRole] = None):
        """
        Create a custom role with specific permissions.

        Args:
            role_name: Name of the custom role
            permissions: List of permissions for the role
            inherits_from: Optional parent role to inherit from
        """
        custom_role = UserRole(role_name)
        self.role_permissions[custom_role] = set(permissions)

        if inherits_from:
            self.role_hierarchy[custom_role] = {inherits_from}
            # Add inherited permissions
            inherited_permissions = self.get_role_permissions(inherits_from)
            self.role_permissions[custom_role].update(inherited_permissions)

        logger.info(f"✅ Created custom role {custom_role} with {len(permissions)} permissions")

    def validate_access(self, user_role: UserRole, resource: str, action: str,
                       context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Validate access with detailed response.

        Args:
            user_role: User's role
            resource: Target resource
            action: Requested action
            context: Optional context information

        Returns:
            Access validation result
        """
        has_access = self.has_permission(user_role, resource, action)

        result = {
            "allowed": has_access,
            "role": user_role,
            "resource": resource,
            "action": action,
            "timestamp": __import__('time').time(),
        }

        if context:
            result["context"] = context

        if not has_access:
            result["reason"] = f"Role {user_role} lacks permission for {action} on {resource}"

        logger.info(f"🔐 Access {'GRANTED' if has_access else 'DENIED'}: {user_role} -> {resource}:{action}")

        return result

    def get_role_matrix(self) -> Dict[str, List[str]]:
        """
        Get permission matrix for all roles.

        Returns:
            Dictionary mapping roles to their permissions
        """
        matrix = {}
        for role in UserRole:
            permissions = self.get_role_permissions(role)
            matrix[role.value] = [str(p) for p in sorted(permissions, key=str)]

        return matrix

# Global RBAC manager instance
rbac_manager = RBACManager()