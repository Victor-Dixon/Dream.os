# <!-- SSOT Domain: integration -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import agent_management

# Optional import for agent_vector_utils (may require chromadb)
try:
    from . import agent_vector_utils
    AGENT_VECTOR_UTILS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Agent vector utils not available: {e}")
    AGENT_VECTOR_UTILS_AVAILABLE = False
from . import architectural_models
from . import architectural_principles
from . import architectural_principles_data
# PHASE 4 CONSOLIDATION: Unified handler modules
from . import unified_cli_handlers
from . import unified_command_handlers
from . import unified_messaging_handlers
from . import unified_onboarding_handlers
from . import unified_service_managers

# from . import compliance_validator  # DELETED - File does not exist
from . import config
from . import constants
from . import contract_service
from . import coordinator
from . import hard_onboarding_service

# Optional imports for services that require chromadb/onnxruntime
try:
    from . import learning_recommender
    LEARNING_RECOMMENDER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Learning recommender not available: {e}")
    LEARNING_RECOMMENDER_AVAILABLE = False
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

# Optional import for performance_analyzer (requires vector database)
try:
    from . import performance_analyzer
    PERFORMANCE_ANALYZER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Performance analyzer not available: {e}")
    PERFORMANCE_ANALYZER_AVAILABLE = False
# Optional import for recommendation_engine (requires vector database)
try:
    from . import recommendation_engine
    RECOMMENDATION_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Recommendation engine not available: {e}")
    RECOMMENDATION_ENGINE_AVAILABLE = False

from . import soft_onboarding_service
from . import status_embedding_indexer
from . import unified_messaging_service
# from . import unified_onboarding_service  # DELETED 2025-12-02 (duplicate)
# from . import vector_database_service_unified  # TEMPORARILY DISABLED - Circular import blocking messaging CLI
# from . import vector_integration_unified  # DELETED 2025-12-02 (duplicate)
# from . import vector_models_and_embedding_unified  # DELETED 2025-12-02 (duplicate)
from . import work_indexer

__all__ = [
    # PHASE 4 CONSOLIDATION: Unified handler modules
    'unified_cli_handlers',
    'unified_command_handlers',
    'unified_messaging_handlers',
    'unified_onboarding_handlers',
    'unified_service_managers',

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
    'performance_analyzer',
    'recommendation_engine',
    'soft_onboarding_service',
    'status_embedding_indexer',
    'unified_messaging_service',
    # 'unified_onboarding_service',  # DELETED 2025-12-02 (duplicate)
    # PHASE 4 CONSOLIDATION: Removed consolidated modules
    # 'overnight_command_handler',  # Consolidated into unified_command_handlers
    # 'role_command_handler',       # Consolidated into unified_command_handlers
    # 'swarm_intelligence_manager', # Consolidated into unified_service_managers
    # 'vector_database_service_unified',  # TEMPORARILY DISABLED - Circular import blocking messaging CLI
    # 'vector_integration_unified',  # DELETED 2025-12-02 (duplicate)
    #     'vector_models_and_embedding_unified',  # DELETED 2025-12-02 (duplicate)
]

# Optional imports for services that require vector database
try:
    from . import work_indexer
    WORK_INDEXER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Work indexer not available: {e}")
    WORK_INDEXER_AVAILABLE = False
