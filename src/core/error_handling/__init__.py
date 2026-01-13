<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/build-tsla-morning-report-system
# V2 Compliance Error Handling Framework
# ======================================
#
# Centralized error handling with comprehensive logging, recovery, and monitoring.
# This module provides the core error handling infrastructure for the Agent Cellphone V2 system.

from .error_handling import (
    # Core classes
    ErrorHandler, ErrorSeverity, ErrorCategory, ErrorContext, ErrorReport,

    # Global functions
    get_error_handler,

    # Decorators and context managers
    handle_errors, error_context,

    # Utility functions
    safe_dict_access, safe_list_access, validate_json_data,
    validate_python_syntax, validate_project_syntax,
)

# Import circuit breaker from existing implementation
try:
    from .circuit_breaker.implementation import CircuitBreaker
    from .circuit_breaker.protocol import ICircuitBreaker
    from .circuit_breaker.provider import CircuitBreakerProvider
except ImportError:
    # Fallback for missing circuit breaker
    CircuitBreaker = None
    ICircuitBreaker = None
    CircuitBreakerProvider = None

<<<<<<< HEAD
# SSOT Domain: core
# V2 Error Handling Framework

__all__ = [
    # Core classes
    'ErrorHandler', 'ErrorSeverity', 'ErrorCategory', 'ErrorContext', 'ErrorReport',

    # Global functions
    'get_error_handler',

    # Decorators and context managers
    'handle_errors', 'error_context',

    # Utility functions
    'safe_dict_access', 'safe_list_access', 'validate_json_data',
    'validate_python_syntax', 'validate_project_syntax',

    # Circuit breaker (backward compatibility)
    'CircuitBreaker', 'ICircuitBreaker', 'CircuitBreakerProvider',
=======
from . import specialized_handlers
from . import retry_safety_engine
from . import retry_mechanisms
from . import recovery_strategies
from . import error_response_models
from . import error_reporting_utilities
from . import error_reporting_reporter
from . import error_reporting_core
from . import error_models_enums
from . import error_models_core
from . import error_intelligence
from . import error_handling_system
from . import error_handling_models
from . import error_handling_core
from . import error_execution
from . import error_exceptions
from . import error_decision_models
from . import error_context_models
from . import error_config
from . import error_classification
from . import coordination_strategies
from . import coordination_decorator
from . import component_management
from .circuit_breaker.implementation import CircuitBreaker
from .circuit_breaker.protocol import ICircuitBreaker
from .circuit_breaker.provider import CircuitBreakerProvider
=======
>>>>>>> origin/codex/build-tsla-morning-report-system
# SSOT Domain: core
# V2 Error Handling Framework

__all__ = [
<<<<<<< HEAD
    'CircuitBreakerProvider',
    'ICircuitBreaker',
    'CircuitBreaker',  # Backward compatibility via lazy import
    'component_management',
    'coordination_decorator',
    # 'coordination_error_handler',  # Merged into component_management
    'coordination_strategies',
    'error_classification',
    'error_config',
    'error_context_models',
    'error_decision_models',
    'error_exceptions',
    'error_execution',
    'error_handling_core',
    'error_handling_models',
    'error_handling_system',
    'error_intelligence',
    'error_models_core',
    'error_models_enums',
    'error_reporting_core',
    'error_reporting_reporter',
    'error_reporting_utilities',
    'error_response_models',
    'recovery_strategies',
    'retry_mechanisms',
    'retry_safety_engine',
    'specialized_handlers',
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    # Core classes
    'ErrorHandler', 'ErrorSeverity', 'ErrorCategory', 'ErrorContext', 'ErrorReport',

    # Global functions
    'get_error_handler',

    # Decorators and context managers
    'handle_errors', 'error_context',

    # Utility functions
    'safe_dict_access', 'safe_list_access', 'validate_json_data',
    'validate_python_syntax', 'validate_project_syntax',

    # Circuit breaker (backward compatibility)
    'CircuitBreaker', 'ICircuitBreaker', 'CircuitBreakerProvider',
>>>>>>> origin/codex/build-tsla-morning-report-system
]
