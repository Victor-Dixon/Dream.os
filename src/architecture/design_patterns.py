"""
Unified Design Patterns - KISS Principle Implementation
======================================================

Essential design patterns consolidated into a single, simple module.
Provides usable base classes that consolidate existing patterns in codebase.

SSOT Domain: architecture

Follows KISS principle: Keep It Simple, Stupid.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist) - KISS Leadership
License: MIT
"""
import logging
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, TypeVar, Generic
logger = logging.getLogger(__name__)

T = TypeVar('T')


class PatternType(Enum):
    """Design pattern type enumeration."""
    SINGLETON = 'singleton'
    FACTORY = 'factory'
    OBSERVER = 'observer'
    STRATEGY = 'strategy'
    ADAPTER = 'adapter'


@dataclass
class DesignPattern:
    """Design pattern data structure."""
    name: str
    pattern_type: PatternType
    description: str
    implementation: str
    use_cases: list[str]


# ============================================================================
# USABLE BASE CLASSES - Consolidate existing patterns
# ============================================================================

class Singleton:
    """
    Thread-safe Singleton base class.
    
    Consolidates existing singleton patterns (_config_manager, _instance patterns).
    Usage:
        class MyConfig(Singleton):
            def __init__(self):
                if not hasattr(self, '_initialized'):
                    self.value = "config"
                    self._initialized = True
    """
    _instances: dict[type, Any] = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class Factory(Generic[T]):
    """
    Generic Factory base class.
    
    Consolidates existing factory patterns (TradingDependencyContainer, ManagerRegistry).
    
    Usage:
        # Example: Create factory and register creators
        factory = Factory[MyClass]()
        factory.register('type1', lambda: MyType1Class())  # Example class name
        obj = factory.create('type1')
    """
    def __init__(self):
        """Initialize factory."""
        self._creators: dict[str, Callable[[], T]] = {}
        self.logger = logging.getLogger(__name__)

    def register(self, name: str, creator: Callable[[], T]) -> None:
        """Register a factory creator function."""
        self._creators[name] = creator
        self.logger.debug(f"Registered factory creator: {name}")

    def create(self, name: str) -> T | None:
        """Create object using registered creator."""
        if name not in self._creators:
            self.logger.error(f"Factory creator not found: {name}")
            return None
        try:
            return self._creators[name]()
        except Exception as e:
            self.logger.error(f"Factory creation failed for {name}: {e}")
            return None


class Observer(ABC):
    """
    Abstract Observer base class.
    
    Consolidates OrchestratorEvents pattern.
    Usage:
        class MyObserver(Observer):
            def update(self, data):
                print(f"Received: {data}")
    """
    @abstractmethod
    def update(self, data: Any = None) -> None:
        """Called when subject notifies observers."""
        pass


class Subject:
    """
    Subject base class for Observer pattern.
    
    Consolidates OrchestratorEvents pattern.
    
    Usage:
        # Example: Create subject and attach observer
        subject = Subject()
        observer = MyObserver()  # Example: class MyObserver(Observer)
        subject.attach(observer)
        subject.notify("data")
    """
    def __init__(self):
        """Initialize subject."""
        self._observers: list[Observer] = []
        self._lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
                self.logger.debug("Observer attached")

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
                self.logger.debug("Observer detached")

    def notify(self, data: Any = None) -> None:
        """Notify all observers."""
        with self._lock:
            observers = list(self._observers)
        for observer in observers:
            try:
                observer.update(data)
            except Exception as e:
                self.logger.error(f"Observer update failed: {e}")


# ============================================================================
# PATTERN DOCUMENTATION - Reference implementations
# ============================================================================

class UnifiedDesignPatterns:
    """
    Unified Design Patterns - Essential patterns only.

    Consolidates all design patterns into a single, simple module
    following KISS principles.
    """

    def __init__(self):
        """Initialize unified design patterns."""
        self.patterns: dict[str, DesignPattern] = {}
        self.logger = logging.getLogger(__name__)
        self._initialize_patterns()

    def _initialize_patterns(self):
        """Initialize essential design patterns."""
        self.patterns['singleton'] = DesignPattern(name='Singleton',
            pattern_type=PatternType.SINGLETON, description=
            'Ensure only one instance of a class exists', implementation=
            """class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance"""
            , use_cases=['Configuration managers', 'Database connections',
            'Logging systems'])
        self.patterns['factory'] = DesignPattern(name='Factory',
            pattern_type=PatternType.FACTORY, description=
            'Create objects without specifying their exact class',
            implementation=
            """class ObjectFactory:
    @staticmethod
    def create_object(object_type):
        if object_type == 'type1':
            return Type1Object()
        elif object_type == 'type2':
            return Type2Object()
        return None"""
            , use_cases=['Object creation', 'Plugin systems',
            'Database drivers'])
        self.patterns['observer'] = DesignPattern(name='Observer',
            pattern_type=PatternType.OBSERVER, description=
            'Notify multiple objects about state changes', implementation=
            """class Subject:
    def __init__(self):
        self._observers = []
    def attach(self, observer):
        self._observers.append(observer)
    def notify(self):
        for observer in self._observers:
            observer.update()"""
            , use_cases=['Event systems', 'Model-View architectures',
            'Notification systems'])

    def get_pattern(self, name: str) ->(DesignPattern | None):
        """Get design pattern by name."""
        return self.patterns.get(name.lower())

    def list_patterns(self) ->list[DesignPattern]:
        """List all available design patterns."""
        return list(self.patterns.values())

    def get_pattern_by_type(self, pattern_type: PatternType) ->list[
        DesignPattern]:
        """Get patterns by type."""
        return [pattern for pattern in self.patterns.values() if pattern.
            pattern_type == pattern_type]

    def apply_pattern(self, pattern_name: str, context: dict[str, Any]) ->dict[
        str, Any]:
        """Apply design pattern in given context."""
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            return {'error': f"Pattern '{pattern_name}' not found"}
        try:
            result = {'pattern': pattern.name, 'type': pattern.pattern_type
                .value, 'applied': True, 'context': context, 'timestamp':
                datetime.now().isoformat()}
            self.logger.info(f'✅ Applied pattern: {pattern.name}')
            return result
        except Exception as e:
            self.logger.error(f'❌ Failed to apply pattern {pattern_name}: {e}')
            return {'error': str(e), 'pattern': pattern_name}

    def get_pattern_recommendations(self, use_case: str) ->list[DesignPattern]:
        """Get pattern recommendations for specific use case."""
        recommendations = []
        for pattern in self.patterns.values():
            if any(use_case.lower() in case.lower() for case in pattern.
                use_cases):
                recommendations.append(pattern)
        return recommendations


def main():
    """Main function for unified design patterns."""
    logger.info('🎨 Unified Design Patterns - KISS Implementation')
    logger.info('=' * 50)
    patterns = UnifiedDesignPatterns()
    available_patterns = patterns.list_patterns()
    logger.info(f'📋 Available patterns: {len(available_patterns)}')
    for pattern in available_patterns:
        logger.info(f'  • {pattern.name} ({pattern.pattern_type.value})')
    recommendations = patterns.get_pattern_recommendations('configuration')
    logger.info(
        f"\n💡 Recommendations for 'configuration': {len(recommendations)}")
    for rec in recommendations:
        logger.info(f'  • {rec.name}: {rec.description}')
    return {'patterns_count': len(available_patterns), 'recommendations':
        len(recommendations)}


if __name__ == '__main__':
    main()


# ============================================================================
# EXPORTS - Usable classes and documentation
# ============================================================================

__all__ = [
    'PatternType',
    'DesignPattern',
    'UnifiedDesignPatterns',
    'Singleton',  # Usable base class
    'Factory',    # Usable base class
    'Observer',   # Usable base class
    'Subject',    # Usable base class
]
