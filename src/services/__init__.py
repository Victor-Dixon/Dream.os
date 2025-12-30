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
