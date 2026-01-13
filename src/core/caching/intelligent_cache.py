#!/usr/bin/env python3
"""
Intelligent Cache - Smart Caching for Orchestration Performance
===============================================================

Advanced caching system with intelligent invalidation, predictive loading,
and performance optimization for agent coordination.

FEATURES:
- Intelligent cache invalidation based on data dependencies
- Predictive caching for frequently accessed patterns
- TTL-based expiration with smart refresh
- Memory-efficient LRU eviction
- Cache analytics and optimization recommendations
- Distributed cache awareness (for future scaling)

Author: Agent-5 (Infrastructure Automation Specialist - Phase 2 Lead)
Date: 2026-01-13
Phase: Phase 2 - Scalability & Performance Optimization
"""

import asyncio
import hashlib
import json
import logging
import time
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Intelligent cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    accessed_at: float
    access_count: int = 0
    ttl: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    size_bytes: int = 0
    hit_rate: float = 0.0

    @property
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.ttl is None:
            return False
        return (time.time() - self.created_at) > self.ttl

    @property
    def age_seconds(self) -> float:
        """Get entry age in seconds."""
        return time.time() - self.created_at

    @property
    def last_access_seconds(self) -> float:
        """Get seconds since last access."""
        return time.time() - self.accessed_at


class IntelligentCache:
    """
    Intelligent caching system with advanced features.

    Features:
    - Dependency-based invalidation
    - Predictive loading
    - TTL with smart refresh
    - Memory-efficient LRU eviction
    - Performance analytics
    - Cache warming strategies
    """

    def __init__(self, max_size: int = 1000, default_ttl: float = 300, enable_predictive: bool = True):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.enable_predictive = enable_predictive

        # Core cache storage (LRU ordered)
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.dependencies: Dict[str, set] = defaultdict(set)  # key -> set of dependent keys

        # Analytics and optimization
        self.access_patterns: Dict[str, List[float]] = defaultdict(list)  # key -> access timestamps
        self.predictive_cache: set = set()  # Keys predicted to be needed soon

        # Background tasks
        self.cleanup_task: Optional[asyncio.Task] = None
        self.predictive_task: Optional[asyncio.Task] = None

        # Thread pool for compute-intensive operations
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="cache")

    def start_background_tasks(self):
        """Start background cache maintenance tasks."""
        if not self.cleanup_task or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())

        if self.enable_predictive and (not self.predictive_task or self.predictive_task.done()):
            self.predictive_task = asyncio.create_task(self._predictive_loading_loop())

    def stop_background_tasks(self):
        """Stop background cache maintenance tasks."""
        if self.cleanup_task and not self.cleanup_task.done():
            self.cleanup_task.cancel()

        if self.predictive_task and not self.predictive_task.done():
            self.predictive_task.cancel()

    async def _cleanup_loop(self):
        """Background cleanup loop."""
        while True:
            try:
                await asyncio.sleep(60)  # Cleanup every minute
                await self._cleanup_expired()
                await self._evict_lru_if_needed()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cache cleanup error: {e}")

    async def _predictive_loading_loop(self):
        """Background predictive loading loop."""
        while True:
            try:
                await asyncio.sleep(300)  # Analyze patterns every 5 minutes
                await self._analyze_patterns()
                await self._warm_predictive_cache()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Predictive loading error: {e}")

    def generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        # Convert args and kwargs to stable string representation
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with intelligent access tracking."""
        if key not in self.cache:
            return None

        entry = self.cache[key]

        # Check expiration
        if entry.is_expired:
            await self.invalidate(key)
            return None

        # Update access tracking
        entry.accessed_at = time.time()
        entry.access_count += 1
        self.access_patterns[key].append(time.time())

        # Move to end (most recently used)
        self.cache.move_to_end(key)

        # Update hit rate
        total_accesses = len(self.access_patterns[key])
        entry.hit_rate = min(1.0, total_accesses / max(1, total_accesses + len([k for k in self.cache.keys() if k != key and key in self.access_patterns.get(k, [])])))

        return entry.value

    async def set(self, key: str, value: Any, ttl: Optional[float] = None, dependencies: Optional[List[str]] = None, tags: Optional[List[str]] = None) -> bool:
        """Set value in cache with metadata."""
        # Calculate size
        size_bytes = self._calculate_size(value)

        # Check if we need to evict before adding
        if len(self.cache) >= self.max_size and key not in self.cache:
            await self._evict_lru()

        entry = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            accessed_at=time.time(),
            ttl=ttl or self.default_ttl,
            dependencies=dependencies or [],
            tags=tags or [],
            size_bytes=size_bytes
        )

        # Update dependencies
        for dep in entry.dependencies:
            self.dependencies[dep].add(key)

        self.cache[key] = entry
        self.cache.move_to_end(key)  # Mark as recently used

        logger.debug(f"✅ Cached key '{key}' (size: {size_bytes} bytes, ttl: {entry.ttl}s)")
        return True

    async def invalidate(self, key: str) -> int:
        """Invalidate cache entry and its dependents."""
        if key not in self.cache:
            return 0

        # Remove entry
        del self.cache[key]

        # Invalidate dependents
        invalidated = 0
        if key in self.dependencies:
            dependent_keys = self.dependencies[key].copy()
            for dep_key in dependent_keys:
                if dep_key in self.cache:
                    del self.cache[dep_key]
                    invalidated += 1
                    logger.debug(f"🗑️ Invalidated dependent key '{dep_key}'")

            del self.dependencies[key]

        logger.debug(f"🗑️ Invalidated cache key '{key}' and {invalidated} dependents")
        return invalidated + 1

    async def invalidate_by_tag(self, tag: str) -> int:
        """Invalidate all entries with specific tag."""
        keys_to_remove = [key for key, entry in self.cache.items() if tag in entry.tags]

        invalidated = 0
        for key in keys_to_remove:
            await self.invalidate(key)
            invalidated += 1

        logger.debug(f"🏷️ Invalidated {invalidated} entries with tag '{tag}'")
        return invalidated

    async def _cleanup_expired(self) -> int:
        """Clean up expired entries."""
        expired_keys = [key for key, entry in self.cache.items() if entry.is_expired]

        cleaned = 0
        for key in expired_keys:
            await self.invalidate(key)
            cleaned += 1

        if cleaned > 0:
            logger.debug(f"🧹 Cleaned up {cleaned} expired cache entries")

        return cleaned

    async def _evict_lru(self) -> bool:
        """Evict least recently used entry."""
        if not self.cache:
            return False

        # Find LRU entry (first in ordered dict)
        lru_key, lru_entry = next(iter(self.cache.items()))

        # But prefer to evict entries that are also expired or have low hit rates
        for key, entry in self.cache.items():
            if entry.is_expired or entry.hit_rate < 0.1:
                lru_key = key
                break

        await self.invalidate(lru_key)
        logger.debug(f"🗑️ Evicted LRU cache entry '{lru_key}'")
        return True

    async def _evict_lru_if_needed(self) -> int:
        """Evict LRU entries if cache is over capacity."""
        evicted = 0
        while len(self.cache) > self.max_size:
            await self._evict_lru()
            evicted += 1

        if evicted > 0:
            logger.debug(f"🗑️ Evicted {evicted} entries to maintain cache size")

        return evicted

    def _calculate_size(self, value: Any) -> int:
        """Calculate approximate memory size of value."""
        try:
            # Simple size calculation - can be enhanced
            if isinstance(value, (str, bytes)):
                return len(value)
            elif isinstance(value, (list, tuple)):
                return sum(self._calculate_size(item) for item in value)
            elif isinstance(value, dict):
                return sum(len(str(k)) + self._calculate_size(v) for k, v in value.items())
            else:
                # Estimate object size
                return len(str(value))
        except:
            return 1024  # Default estimate

    async def _analyze_patterns(self):
        """Analyze access patterns for predictive caching."""
        if len(self.access_patterns) < 10:
            return  # Need minimum data for analysis

        # Identify frequently accessed keys
        frequent_keys = []
        for key, accesses in self.access_patterns.items():
            if len(accesses) > 5:  # Accessed more than 5 times
                # Calculate access frequency (accesses per hour)
                if accesses:
                    time_span = max(accesses) - min(accesses)
                    if time_span > 0:
                        frequency = len(accesses) / (time_span / 3600)  # per hour
                        if frequency > 0.5:  # More than once every 2 hours
                            frequent_keys.append((key, frequency))

        # Sort by frequency and take top candidates
        frequent_keys.sort(key=lambda x: x[1], reverse=True)
        top_candidates = frequent_keys[:5]  # Top 5 most frequent

        # Update predictive cache
        self.predictive_cache = {key for key, _ in top_candidates}

        if self.predictive_cache:
            logger.debug(f"🔮 Predictive cache updated with {len(self.predictive_cache)} keys")

    async def _warm_predictive_cache(self):
        """Warm predictive cache with frequently accessed data."""
        # This would be implemented based on specific caching strategies
        # For now, just log the predictive keys
        if self.predictive_cache:
            logger.debug(f"🔥 Warming predictive cache: {list(self.predictive_cache)}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        total_entries = len(self.cache)
        total_size = sum(entry.size_bytes for entry in self.cache.values())
        expired_entries = sum(1 for entry in self.cache.values() if entry.is_expired)

        # Hit rate calculation
        total_accesses = sum(len(accesses) for accesses in self.access_patterns.values())
        cache_hits = sum(entry.access_count for entry in self.cache.values())
        hit_rate = cache_hits / max(1, total_accesses)

        # Access pattern analysis
        most_accessed = max(self.access_patterns.items(), key=lambda x: len(x[1]), default=(None, []))
        least_accessed = min(self.access_patterns.items(), key=lambda x: len(x[1]), default=(None, []))

        return {
            "total_entries": total_entries,
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "expired_entries": expired_entries,
            "hit_rate": hit_rate,
            "most_accessed_key": most_accessed[0] if most_accessed[0] else None,
            "most_accessed_count": len(most_accessed[1]),
            "least_accessed_key": least_accessed[0] if least_accessed[0] else None,
            "least_accessed_count": len(least_accessed[1]),
            "predictive_cache_size": len(self.predictive_cache),
            "dependency_relationships": len(self.dependencies)
        }

    def get_performance_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        stats = self.get_cache_stats()

        # Size recommendations
        if stats['total_entries'] > self.max_size * 0.9:
            recommendations.append(f"Cache near capacity ({stats['total_entries']}/{self.max_size}). Consider increasing max_size or implementing more aggressive eviction.")

        # Hit rate recommendations
        if stats['hit_rate'] < 0.5:
            recommendations.append(".2f"            recommendations.append("Consider increasing TTL or implementing better cache warming strategies.")

        # Size recommendations
        if stats['total_size_mb'] > 100:  # 100MB
            recommendations.append(".2f"
        # Predictive cache recommendations
        if not self.predictive_cache and self.enable_predictive:
            recommendations.append("Enable predictive caching to improve hit rates for frequently accessed data.")

        # Dependency recommendations
        if stats['dependency_relationships'] > stats['total_entries'] * 2:
            recommendations.append("High dependency complexity detected. Consider simplifying cache invalidation strategy.")

        return recommendations or ["Cache performance is optimal"]


class OrchestrationCache(IntelligentCache):
    """
    Specialized cache for orchestration operations.

    Optimized for agent coordination patterns with domain-specific features.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orchestration_patterns: Dict[str, Dict[str, Any]] = {}

    async def cache_orchestration_result(self, operation: str, params: Dict[str, Any], result: Any, ttl: float = 300) -> bool:
        """Cache orchestration operation result with intelligent key generation."""
        key = self._generate_orchestration_key(operation, params)

        # Add orchestration-specific metadata
        dependencies = self._extract_dependencies(operation, params)
        tags = [operation, "orchestration"]

        # Cache pattern for future optimization
        self.orchestration_patterns[operation] = {
            'last_params': params,
            'last_result_type': type(result).__name__,
            'frequency': self.orchestration_patterns.get(operation, {}).get('frequency', 0) + 1,
            'avg_execution_time': 0  # Would be updated with actual timing
        }

        return await self.set(key, result, ttl=ttl, dependencies=dependencies, tags=tags)

    async def get_orchestration_result(self, operation: str, params: Dict[str, Any]) -> Optional[Any]:
        """Get cached orchestration result."""
        key = self._generate_orchestration_key(operation, params)
        return await self.get(key)

    def _generate_orchestration_key(self, operation: str, params: Dict[str, Any]) -> str:
        """Generate cache key for orchestration operations."""
        # Include operation type and key parameters
        key_data = {
            'operation': operation,
            'agents': sorted(params.get('agents', [])),
            'task_count': len(params.get('tasks', [])),
            'coordination_state': params.get('coordination_state', {}).get('phase', 'unknown')
        }
        return self.generate_key(operation, **key_data)

    def _extract_dependencies(self, operation: str, params: Dict[str, Any]) -> List[str]:
        """Extract cache dependencies from orchestration parameters."""
        dependencies = []

        # Agent dependencies
        agents = params.get('agents', [])
        for agent in agents:
            if isinstance(agent, dict):
                agent_id = agent.get('id', agent.get('agent_id', str(agent)))
                dependencies.append(f"agent:{agent_id}")

        # Task dependencies
        tasks = params.get('tasks', [])
        for task in tasks:
            if isinstance(task, dict):
                task_id = task.get('id', task.get('task_id', str(task)))
                dependencies.append(f"task:{task_id}")

        return dependencies


# Global cache instances
_orchestration_cache = None

def get_orchestration_cache() -> OrchestrationCache:
    """Get the global orchestration cache instance."""
    global _orchestration_cache
    if _orchestration_cache is None:
        _orchestration_cache = OrchestrationCache(max_size=500, default_ttl=600)  # 10 minute TTL
    return _orchestration_cache

def start_cache_monitoring():
    """Start cache background monitoring."""
    cache = get_orchestration_cache()
    cache.start_background_tasks()

def stop_cache_monitoring():
    """Stop cache background monitoring."""
    cache = get_orchestration_cache()
    cache.stop_background_tasks()