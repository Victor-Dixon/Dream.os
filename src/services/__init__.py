<<<<<<< HEAD
# <!-- SSOT Domain: integration -->
# LAZY IMPORTS: Services are imported only when needed to prevent automatic system initialization

import importlib
from typing import Any

# Service availability flags
LEARNING_RECOMMENDER_AVAILABLE = False
PERFORMANCE_ANALYZER_AVAILABLE = False
RECOMMENDATION_ENGINE_AVAILABLE = False
WORK_INDEXER_AVAILABLE = False

def _lazy_import(module_name: str) -> Any:
    """Import a module only when first accessed."""
    try:
        return importlib.import_module(f'.{module_name}', __name__)
    except ImportError:
        return None

# Lazy service getters
def get_learning_recommender():
    """Lazy import learning recommender."""
    module = _lazy_import('learning_recommender')
    global LEARNING_RECOMMENDER_AVAILABLE
    LEARNING_RECOMMENDER_AVAILABLE = module is not None
    return module

def get_performance_analyzer():
    """Lazy import performance analyzer."""
    module = _lazy_import('performance_analyzer')
    global PERFORMANCE_ANALYZER_AVAILABLE
    PERFORMANCE_ANALYZER_AVAILABLE = module is not None
    return module

def get_recommendation_engine():
    """Lazy import recommendation engine."""
    module = _lazy_import('recommendation_engine')
    global RECOMMENDATION_ENGINE_AVAILABLE
    RECOMMENDATION_ENGINE_AVAILABLE = module is not None
    return module

def get_work_indexer():
    """Lazy import work indexer."""
    module = _lazy_import('work_indexer')
    global WORK_INDEXER_AVAILABLE
    WORK_INDEXER_AVAILABLE = module is not None
    return module

__all__ = [
    'get_learning_recommender',
    'get_performance_analyzer',
    'get_recommendation_engine',
    'get_work_indexer',
    'LEARNING_RECOMMENDER_AVAILABLE',
    'PERFORMANCE_ANALYZER_AVAILABLE',
    'RECOMMENDATION_ENGINE_AVAILABLE',
    'WORK_INDEXER_AVAILABLE',
]
=======
# <!-- SSOT Domain: integration -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import agent_management
from . import agent_vector_utils
from . import architectural_models
from . import architectural_principles
from . import architectural_principles_data
# from . import compliance_validator  # DELETED - File does not exist
from . import config
from . import constants
from . import contract_service
from . import coordinator
from . import hard_onboarding_service
from . import learning_recommender
from . import message_batching_service
from . import message_identity_clarification
# from . import messaging_cli  # Commented out per user request
from . import messaging_cli_formatters
from . import messaging_cli_handlers
from . import messaging_cli_parser
from . import messaging_discord
from . import messaging_handlers
from . import messaging_infrastructure
from . import onboarding_template_loader
from . import overnight_command_handler
from . import performance_analyzer
from . import recommendation_engine
from . import role_command_handler
from . import soft_onboarding_service
from . import status_embedding_indexer
from . import swarm_intelligence_manager
from . import unified_messaging_service
# from . import unified_onboarding_service  # DELETED 2025-12-02 (duplicate)
# from . import vector_database_service_unified  # TEMPORARILY DISABLED - Circular import blocking messaging CLI
# from . import vector_integration_unified  # DELETED 2025-12-02 (duplicate)
# from . import vector_models_and_embedding_unified  # DELETED 2025-12-02 (duplicate)
from . import work_indexer

__all__ = [
    'agent_management',
    'agent_vector_utils',
    'architectural_models',
    'architectural_principles',
    'architectural_principles_data',
    # 'compliance_validator',  # DELETED - File does not exist
    'config',
    'constants',
    'contract_service',
    'coordinator',
    'hard_onboarding_service',
    'learning_recommender',
    'message_batching_service',
    'message_identity_clarification',
    'messaging_cli',
    'messaging_cli_formatters',
    'messaging_cli_handlers',
    'messaging_cli_parser',
    'messaging_discord',
    'messaging_handlers',
    'messaging_infrastructure',
    'onboarding_template_loader',
    'overnight_command_handler',
    'performance_analyzer',
    'recommendation_engine',
    'role_command_handler',
    'soft_onboarding_service',
    'status_embedding_indexer',
    'swarm_intelligence_manager',
    'unified_messaging_service',
    # 'unified_onboarding_service',  # DELETED 2025-12-02 (duplicate)
    # 'vector_database_service_unified',  # TEMPORARILY DISABLED - Circular import blocking messaging CLI
    # 'vector_integration_unified',  # DELETED 2025-12-02 (duplicate)
    # 'vector_models_and_embedding_unified',  # DELETED 2025-12-02 (duplicate)
    'work_indexer',
]
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
