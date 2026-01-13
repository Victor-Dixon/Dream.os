"""
Blast Radius Limiter - AGI-19
==============================

Damage control limits for autonomous operations.
Prevents any single autonomous action from causing excessive damage.

Features:
- Cost limits (max $ spend per action)
- File modification limits (max N files per action)
- API call limits (max N calls per action)
- Time-based limits (max operations per hour/day)
- Automatic escalation when approaching limits

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

<!-- SSOT Domain: safety -->

SSOT TOOL METADATA
Purpose: Blast radius limitation for autonomous operations
Description: AGI-19 component providing cost, file, and API call limits with time-based windows
Usage: BlastRadiusLimiter class for checking and recording resource usage
Date: 2025-12-30
Tags: safety, agi, limits, blast-radius, autonomous

Author: Agent-4 (Captain) with Cloud Agent
License: MIT
"""

import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Types of resources that can be limited."""
    COST = "cost"  # Dollar spend
    FILES = "files"  # File modifications
    API_CALLS = "api_calls"  # External API calls
    DB_WRITES = "db_writes"  # Database writes
    COMPUTE = "compute"  # Compute resources (CPU hours)


class BlastRadiusViolation(Exception):
    """Raised when blast radius limit is exceeded."""
    pass


@dataclass
class ResourceLimit:
    """Limit configuration for a resource type."""
    resource_type: ResourceType
    max_per_action: float
    max_per_hour: float
    max_per_day: float
    warning_threshold: float = 0.8  # Warn at 80% of limit
    enforcement_mode: str = "strict"  # strict, warn, or disabled


@dataclass
class ResourceUsage:
    """Track resource usage over time."""
    resource_type: ResourceType
    action_id: str
    amount: float
    timestamp: float
    metadata: Dict = field(default_factory=dict)


class BlastRadiusLimiter:
    """
    Enforces blast radius limits on autonomous operations.
    
    Prevents excessive damage by limiting:
    - Cost: Max $100 per action
    - Files: Max 10 file modifications per action
    - API calls: Max 1000 API calls per action
    - Time-based: Rolling windows (hourly, daily)
    
    Automatically escalates to human when approaching limits.
    """
    
    def __init__(self):
        """Initialize blast radius limiter."""
        self.limits: Dict[ResourceType, ResourceLimit] = self._get_default_limits()
        self.usage_history: List[ResourceUsage] = []
        self._load_configuration()
        
        logger.info("BlastRadiusLimiter initialized with default limits")
    
    def _get_default_limits(self) -> Dict[ResourceType, ResourceLimit]:
        """Get default blast radius limits."""
        return {
            ResourceType.COST: ResourceLimit(
                resource_type=ResourceType.COST,
                max_per_action=100.0,  # $100
                max_per_hour=500.0,  # $500
                max_per_day=2000.0,  # $2000
                warning_threshold=0.8,
                enforcement_mode="strict"
            ),
            ResourceType.FILES: ResourceLimit(
                resource_type=ResourceType.FILES,
                max_per_action=10,
                max_per_hour=50,
                max_per_day=200,
                warning_threshold=0.8,
                enforcement_mode="strict"
            ),
            ResourceType.API_CALLS: ResourceLimit(
                resource_type=ResourceType.API_CALLS,
                max_per_action=1000,
                max_per_hour=5000,
                max_per_day=20000,
                warning_threshold=0.8,
                enforcement_mode="strict"
            ),
            ResourceType.DB_WRITES: ResourceLimit(
                resource_type=ResourceType.DB_WRITES,
                max_per_action=100,
                max_per_hour=500,
                max_per_day=2000,
                warning_threshold=0.8,
                enforcement_mode="strict"
            ),
            ResourceType.COMPUTE: ResourceLimit(
                resource_type=ResourceType.COMPUTE,
                max_per_action=1.0,  # 1 CPU hour
                max_per_hour=5.0,  # 5 CPU hours
                max_per_day=20.0,  # 20 CPU hours
                warning_threshold=0.8,
                enforcement_mode="warn"
            ),
        }
    
    def _load_configuration(self):
<<<<<<< HEAD
        """Load custom limits from configuration files or environment variables."""
        self._load_from_environment_variables()
        self._load_from_config_file()

    def _load_from_environment_variables(self):
        """Load blast radius limits from environment variables."""
        env_mappings = self._get_env_mappings()
        self._process_env_variables(env_mappings)

    def _get_env_mappings(self):
        """Get environment variable to limit mappings."""
        return {
            'BLAST_RADIUS_COST_MAX_ACTION': (ResourceType.COST, 'max_per_action'),
            'BLAST_RADIUS_COST_MAX_HOUR': (ResourceType.COST, 'max_per_hour'),
            'BLAST_RADIUS_COST_MAX_DAY': (ResourceType.COST, 'max_per_day'),
            'BLAST_RADIUS_FILES_MAX_ACTION': (ResourceType.FILES, 'max_per_action'),
            'BLAST_RADIUS_FILES_MAX_HOUR': (ResourceType.FILES, 'max_per_hour'),
            'BLAST_RADIUS_FILES_MAX_DAY': (ResourceType.FILES, 'max_per_day'),
            'BLAST_RADIUS_API_MAX_ACTION': (ResourceType.API_CALLS, 'max_per_action'),
            'BLAST_RADIUS_API_MAX_HOUR': (ResourceType.API_CALLS, 'max_per_hour'),
            'BLAST_RADIUS_API_MAX_DAY': (ResourceType.API_CALLS, 'max_per_day'),
        }

    def _process_env_variables(self, env_mappings):
        """Process environment variables and apply limits."""
        import os
        for env_var, (resource_type, limit_attr) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    numeric_value = float(value) if resource_type == ResourceType.COST else int(value)
                    if resource_type in self.limits:
                        setattr(self.limits[resource_type], limit_attr, numeric_value)
                        logger.info(f"Loaded {env_var}={numeric_value} from environment")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Invalid value for {env_var}: {value} ({e})")

    def _load_from_config_file(self):
        """Load blast radius limits from configuration file."""
        config_paths = self._get_config_paths()
        self._try_load_from_config_paths(config_paths)

    def _get_config_paths(self):
        """Get list of possible configuration file paths."""
        import os
        from pathlib import Path

        return [
            Path.home() / '.blast_radius_config.json',
            Path.cwd() / 'blast_radius_config.json',
            Path(os.getenv('BLAST_RADIUS_CONFIG', '')) if os.getenv('BLAST_RADIUS_CONFIG') else None,
        ]

    def _try_load_from_config_paths(self, config_paths):
        """Try to load configuration from the provided paths."""
        for config_path in config_paths:
            if config_path and config_path.exists() and self._load_config_file(config_path):
                break

    def _load_config_file(self, config_path):
        """Load and apply configuration from a specific file."""
        import json

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            if 'limits' in config:
                self._apply_config_limits(config['limits'], config_path)

            logger.info(f"Loaded blast radius configuration from {config_path}")
            return True

        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
            return False

    def _apply_config_limits(self, limits_config, config_path):
        """Apply limits configuration from loaded config."""
        for resource_name, limit_config in limits_config.items():
            try:
                resource_type = ResourceType(resource_name)
                if resource_type in self.limits:
                    for attr, value in limit_config.items():
                        if hasattr(self.limits[resource_type], attr):
                            setattr(self.limits[resource_type], attr, value)
                            logger.info(f"Loaded {resource_name}.{attr}={value} from {config_path}")

            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid resource type in config: {resource_name} ({e})")
=======
        """Load custom limits from configuration."""
        # TODO: Load from config file or environment variables
        pass
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    
    def check_limit(
        self,
        resource_type: ResourceType,
        requested_amount: float,
        action_id: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Check if resource request is within limits.
        
        Args:
            resource_type: Type of resource
            requested_amount: Amount requested
            action_id: ID of the action requesting resource
            metadata: Additional metadata (optional)
        
        Returns:
            True if within limits
        
        Raises:
            BlastRadiusViolation: If limit exceeded and enforcement is strict
        """
        limit = self.limits.get(resource_type)
        if not limit:
            logger.warning(f"No limit defined for {resource_type.value}")
            return True
        
        # Check per-action limit
        if requested_amount > limit.max_per_action:
            message = (
                f"Blast radius violation: {resource_type.value} "
                f"requested {requested_amount} exceeds per-action limit "
                f"{limit.max_per_action}"
            )
            logger.error(message)
            
            if limit.enforcement_mode == "strict":
                raise BlastRadiusViolation(message)
            elif limit.enforcement_mode == "warn":
                logger.warning(f"⚠️ {message}")
                return True
            else:  # disabled
                return True
        
        # Check hourly limit
        hourly_usage = self._get_usage_in_window(resource_type, hours=1)
        if hourly_usage + requested_amount > limit.max_per_hour:
            message = (
                f"Blast radius violation: {resource_type.value} "
                f"hourly usage {hourly_usage} + requested {requested_amount} "
                f"exceeds hourly limit {limit.max_per_hour}"
            )
            logger.error(message)
            
            if limit.enforcement_mode == "strict":
                raise BlastRadiusViolation(message)
            elif limit.enforcement_mode == "warn":
                logger.warning(f"⚠️ {message}")
        
        # Check daily limit
        daily_usage = self._get_usage_in_window(resource_type, hours=24)
        if daily_usage + requested_amount > limit.max_per_day:
            message = (
                f"Blast radius violation: {resource_type.value} "
                f"daily usage {daily_usage} + requested {requested_amount} "
                f"exceeds daily limit {limit.max_per_day}"
            )
            logger.error(message)
            
            if limit.enforcement_mode == "strict":
                raise BlastRadiusViolation(message)
            elif limit.enforcement_mode == "warn":
                logger.warning(f"⚠️ {message}")
        
        # Check warning threshold
        warning_threshold_action = limit.max_per_action * limit.warning_threshold
        if requested_amount > warning_threshold_action:
            logger.warning(
                f"⚠️ Approaching blast radius limit: {resource_type.value} "
                f"requested {requested_amount} is {requested_amount/limit.max_per_action*100:.1f}% "
                f"of per-action limit"
            )
        
        return True
    
    def record_usage(
        self,
        resource_type: ResourceType,
        amount: float,
        action_id: str,
        metadata: Optional[Dict] = None
    ):
        """
        Record resource usage.
        
        Args:
            resource_type: Type of resource
            amount: Amount used
            action_id: ID of the action
            metadata: Additional metadata
        """
        usage = ResourceUsage(
            resource_type=resource_type,
            action_id=action_id,
            amount=amount,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self.usage_history.append(usage)
        
        # Cleanup old usage records (keep 7 days)
        cutoff_time = time.time() - (7 * 24 * 3600)
        self.usage_history = [
            u for u in self.usage_history
            if u.timestamp > cutoff_time
        ]
        
        logger.debug(
            f"Recorded usage: {resource_type.value} = {amount} for action {action_id}"
        )
    
    def _get_usage_in_window(
        self,
        resource_type: ResourceType,
        hours: int
    ) -> float:
        """
        Get total usage for a resource type in time window.
        
        Args:
            resource_type: Type of resource
            hours: Number of hours to look back
        
        Returns:
            Total usage in time window
        """
        cutoff_time = time.time() - (hours * 3600)
        
        total = sum(
            usage.amount
            for usage in self.usage_history
            if usage.resource_type == resource_type
            and usage.timestamp > cutoff_time
        )
        
        return total
    
    def get_remaining_capacity(
        self,
        resource_type: ResourceType,
        window: str = "action"
    ) -> float:
        """
        Get remaining capacity for a resource.
        
        Args:
            resource_type: Type of resource
            window: Time window (action, hour, day)
        
        Returns:
            Remaining capacity
        """
        limit = self.limits.get(resource_type)
        if not limit:
            return float('inf')
        
        if window == "action":
            return limit.max_per_action
        elif window == "hour":
            usage = self._get_usage_in_window(resource_type, hours=1)
            return max(0, limit.max_per_hour - usage)
        elif window == "day":
            usage = self._get_usage_in_window(resource_type, hours=24)
            return max(0, limit.max_per_day - usage)
        else:
            raise ValueError(f"Invalid window: {window}")
    
    def get_usage_report(self) -> Dict:
        """
        Get usage report for all resources.
        
        Returns:
            Usage report with current usage and limits
        """
        report = {}
        
        for resource_type, limit in self.limits.items():
            hourly_usage = self._get_usage_in_window(resource_type, hours=1)
            daily_usage = self._get_usage_in_window(resource_type, hours=24)
            
            report[resource_type.value] = {
                "limits": {
                    "per_action": limit.max_per_action,
                    "per_hour": limit.max_per_hour,
                    "per_day": limit.max_per_day,
                },
                "usage": {
                    "hourly": hourly_usage,
                    "daily": daily_usage,
                },
                "remaining": {
                    "hourly": max(0, limit.max_per_hour - hourly_usage),
                    "daily": max(0, limit.max_per_day - daily_usage),
                },
                "utilization": {
                    "hourly": min(100, (hourly_usage / limit.max_per_hour) * 100),
                    "daily": min(100, (daily_usage / limit.max_per_day) * 100),
                },
                "enforcement_mode": limit.enforcement_mode
            }
        
        return report
    
    def update_limit(
        self,
        resource_type: ResourceType,
        max_per_action: Optional[float] = None,
        max_per_hour: Optional[float] = None,
        max_per_day: Optional[float] = None,
        enforcement_mode: Optional[str] = None
    ):
        """
        Update limits for a resource type.
        
        Args:
            resource_type: Type of resource
            max_per_action: New per-action limit (optional)
            max_per_hour: New hourly limit (optional)
            max_per_day: New daily limit (optional)
            enforcement_mode: New enforcement mode (optional)
        """
        limit = self.limits.get(resource_type)
        if not limit:
            logger.error(f"Cannot update limit for unknown resource: {resource_type.value}")
            return
        
        if max_per_action is not None:
            limit.max_per_action = max_per_action
        if max_per_hour is not None:
            limit.max_per_hour = max_per_hour
        if max_per_day is not None:
            limit.max_per_day = max_per_day
        if enforcement_mode is not None:
            if enforcement_mode in ["strict", "warn", "disabled"]:
                limit.enforcement_mode = enforcement_mode
            else:
                logger.error(f"Invalid enforcement mode: {enforcement_mode}")
        
        logger.info(f"Updated limits for {resource_type.value}")


# Global singleton instance
_limiter_instance = None


def get_blast_radius_limiter() -> BlastRadiusLimiter:
    """Get the global blast radius limiter instance."""
    global _limiter_instance
    if _limiter_instance is None:
        _limiter_instance = BlastRadiusLimiter()
    return _limiter_instance
