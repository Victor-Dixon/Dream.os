# 🎯 SSOT for Vector/Search Models

**Date**: 2025-12-04  
**Status**: ✅ **ACTIVE**  
**Maintained By**: Agent-8 (Testing & Quality Assurance Specialist)

---

## 📋 OVERVIEW

This document defines the **Single Source of Truth (SSOT)** for vector database and search models across the codebase.

---

## 🔍 SSOT LOCATIONS

### **SearchResult SSOT**

**Location**: `src/services/models/vector_models.py`

**Class**: `SearchResult`

**Usage**:
```python
from src.services.models.vector_models import SearchResult

result = SearchResult(
    document_id="doc123",
    content="Document content",
    similarity_score=0.95,
    metadata={"source": "vector_db"}
)
```

**Features**:
- ✅ Supports all variant fields (web, intelligent context, core, etc.)
- ✅ Backward compatibility properties
- ✅ Field aliases for different use cases
- ✅ `to_dict()` method

---

### **SearchQuery SSOT**

**Location**: `src/services/models/vector_models.py`

**Class**: `SearchQuery`

**Usage**:
```python
from src.services.models.vector_models import SearchQuery, SearchType

query = SearchQuery(
    query_text="search term",
    search_type=SearchType.SIMILARITY,
    limit=10,
    similarity_threshold=0.7
)
```

**Features**:
- ✅ Supports all variant fields
- ✅ Backward compatibility fields (`query`, `threshold`, `metadata_filter`, `agent_id`)
- ✅ Property aliases

---

### **Pydantic Config SSOT**

**Location**: `src/core/pydantic_config.py`

**Classes**: `PydanticConfigV1`, `BasePydanticConfig`

**Usage**:
```python
from pydantic import BaseModel
from src.core.pydantic_config import PydanticConfigV1

class MyModel(BaseModel):
    class Config(PydanticConfigV1):
        pass
```

---

## ⚠️ DEPRECATED CLASSES

The following classes are **DEPRECATED** and will be removed in a future version:

### **SearchResult Deprecated Locations**:
1. ❌ `src/core/vector_database.py` - Use SSOT instead
2. ❌ `src/core/intelligent_context/search_models.py` - Use SSOT instead
3. ❌ `src/core/intelligent_context/context_results.py` - Use SSOT instead
4. ❌ `src/core/intelligent_context/unified_intelligent_context/models.py` - Use SSOT instead
5. ❌ `src/web/vector_database/models.py` - Use SSOT instead (shim maintained)

### **SearchQuery Deprecated Locations**:
1. ❌ `src/core/vector_database.py` - Use SSOT instead
2. ❌ Fallback stubs in `src/services/learning_recommender.py` - Use SSOT instead
3. ❌ Fallback stubs in `src/services/agent_management.py` - Use SSOT instead

### **Config Deprecated Locations**:
1. ❌ `src/message_task/schemas.py` - Pydantic Config classes (now use SSOT)
2. ⚠️ `src/ai_training/dreamvault/config.py` - Domain-specific, migration path documented

---

## 🔄 MIGRATION GUIDE

### **Migrating SearchResult**:

**Before**:
```python
from src.core.intelligent_context.search_models import SearchResult

result = SearchResult(
    result_id="id",
    content="content",
    relevance_score=0.9,
    source_type="type",
    source_id="sid"
)
```

**After**:
```python
from src.services.models.vector_models import SearchResult

result = SearchResult(
    document_id="id",  # or use result_id (alias)
    content="content",
    similarity_score=0.9,  # or use relevance_score (alias)
    metadata={},
    result_id="id",  # alias supported
    source_type="type",
    source_id="sid",
    relevance_score=0.9  # alias supported
)
```

---

### **Migrating SearchQuery**:

**Before**:
```python
from src.core.vector_database import SearchQuery

query = SearchQuery(
    query_text="term",
    threshold=0.7,
    metadata_filter={"key": "value"}
)
```

**After**:
```python
from src.services.models.vector_models import SearchQuery

query = SearchQuery(
    query_text="term",
    similarity_threshold=0.7,  # or use threshold (alias)
    filters={"key": "value"}  # or use metadata_filter (alias)
)
```

---

## ✅ VERIFICATION

To verify SSOT compliance:

1. **Run import chain validator**:
   ```bash
   python tools/import_chain_validator.py
   ```

2. **Check for duplicate definitions**:
   ```bash
   grep -r "class SearchResult" src/
   grep -r "class SearchQuery" src/
   ```

3. **Verify imports**:
   All imports should point to `src.services.models.vector_models`

---

## 📝 NOTES

- **Backward Compatibility**: All deprecated classes maintain backward compatibility through shims
- **Deprecation Warnings**: Deprecated classes emit `DeprecationWarning` when instantiated
- **Migration Timeline**: Deprecated classes will be removed in a future major version

---

**Last Updated**: 2025-12-04  
**Next Review**: After Phase 6 SSOT Verification

🐝 **WE. ARE. SWARM. ⚡🔥**

