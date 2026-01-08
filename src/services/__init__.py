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