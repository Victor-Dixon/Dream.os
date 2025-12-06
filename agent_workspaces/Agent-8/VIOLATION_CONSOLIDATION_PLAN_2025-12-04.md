# 🚨 SSOT VIOLATION CONSOLIDATION PLAN

**Date**: 2025-12-04  
**Agent**: Agent-8 (Testing & Quality Assurance Specialist)  
**Priority**: 🚨 **CRITICAL**  
**Status**: 📋 **PLANNING PHASE**

---

## 🎯 MISSION OBJECTIVE

**Consolidate SSOT violations for**:
1. **Config class** (5 locations) - SSOT violation
2. **SearchResult** (7 locations) - Consolidate duplicates
3. **SearchQuery** (7 locations) - Consolidate duplicates
4. **Identify SSOT** for search/vector models

---

## 📊 VIOLATION ANALYSIS

### **1. Config Class SSOT Violations (5 locations)**

#### **Location 1-4: Pydantic Config Classes** (`src/message_task/schemas.py`)
- **Lines**: 28, 47, 75, 92
- **Type**: Nested Pydantic `Config` classes
- **Purpose**: Pydantic model configuration (`arbitrary_types_allowed = True`)
- **SSOT Status**: ⚠️ **VIOLATION** - Should use shared Pydantic config
- **Impact**: LOW (Pydantic-specific, but should be consolidated)

**Current Structure**:
```python
class InboundMessage(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class ParsedTask(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class TaskStateTransition(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class TaskCompletionReport(BaseModel):
    class Config:
        arbitrary_types_allowed = True
```

**SSOT Solution**: Create shared Pydantic config base class or use `model_config` (Pydantic v2)

---

#### **Location 5: ShadowArchive Config** (`src/ai_training/dreamvault/config.py`)
- **Line**: 11
- **Type**: Standalone configuration manager class
- **Purpose**: YAML-based config management for ShadowArchive
- **SSOT Status**: ⚠️ **VIOLATION** - Should use unified config system
- **Impact**: MEDIUM (Domain-specific, but should align with SSOT)

**Current Structure**:
```python
class Config:
    """Configuration manager for ShadowArchive."""
    def __init__(self, config_path: str | None = None):
        self.config_path = config_path or "configs/ingest.yaml"
        self.config = self._load_config()
```

**SSOT Solution**: Migrate to `src/core/config_ssot.py` or create adapter

---

### **2. SearchResult Consolidation (7 locations)**

#### **Location 1: Core Vector Database (Simple)** (`src/core/vector_database.py:39`)
```python
class SearchResult:
    def __init__(self, document_id: str, content: str, similarity_score: float, metadata: Dict[str, Any]):
        self.document_id = document_id
        self.content = content
        self.similarity_score = similarity_score
        self.metadata = metadata
```
- **Type**: Simple class (non-dataclass)
- **Fields**: `document_id`, `content`, `similarity_score`, `metadata`

---

#### **Location 2: Core Vector Database (Dataclass)** (`src/core/vector_database.py:215`)
```python
@dataclass
class SearchResult:
    document: VectorDocument
    score: float
    metadata: Dict[str, Any]
```
- **Type**: Dataclass
- **Fields**: `document` (VectorDocument), `score`, `metadata`
- **⚠️ CONFLICT**: Different structure than Location 1!

---

#### **Location 3: Services Vector Models** (`src/services/models/vector_models.py:104`)
```python
@dataclass
class SearchResult:
    document_id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]
```
- **Type**: Dataclass
- **Fields**: `document_id`, `content`, `similarity_score`, `metadata`
- **Similar to**: Location 1

---

#### **Location 4: Web Vector Database Models** (`src/web/vector_database/models.py:75`)
```python
@dataclass
class SearchResult:
    id: str
    title: str
    content: str
    collection: str
    relevance: float
    tags: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    size: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    score: float | None = None
```
- **Type**: Dataclass
- **Fields**: `id`, `title`, `content`, `collection`, `relevance`, `tags`, `created_at`, `updated_at`, `size`, `metadata`, `score`
- **⚠️ DIFFERENT**: Web-specific fields (title, collection, tags, etc.)

---

#### **Location 5: Intelligent Context Search Models** (`src/core/intelligent_context/search_models.py:21`)
```python
@dataclass
class SearchResult:
    result_id: str
    content: str
    relevance_score: float
    source_type: str
    source_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
```
- **Type**: Dataclass
- **Fields**: `result_id`, `content`, `relevance_score`, `source_type`, `source_id`, `metadata`, `timestamp`
- **⚠️ DIFFERENT**: Context-specific fields (source_type, source_id, timestamp)

---

#### **Location 6: Intelligent Context Unified** (`src/core/intelligent_context/unified_intelligent_context/models.py:48`)
```python
@dataclass
class SearchResult:
    result_id: str
    title: str = ""
    description: str = ""
    relevance_score: float = 0.0
    context_type: ContextType | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
```
- **Type**: Dataclass
- **Fields**: `result_id`, `title`, `description`, `relevance_score`, `context_type`, `metadata`, `timestamp`
- **⚠️ DIFFERENT**: Unified context fields (title, description, context_type)

---

#### **Location 7: Context Results** (`src/core/intelligent_context/context_results.py:24`)
```python
@dataclass
class SearchResult:
    result_id: str
    content: str
    relevance_score: float
    source_type: str
    source_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
```
- **Type**: Dataclass
- **Fields**: `result_id`, `content`, `relevance_score`, `source_type`, `source_id`, `metadata`, `timestamp`
- **⚠️ DUPLICATE**: Identical to Location 5!

---

### **3. SearchQuery Consolidation (5+ locations found)**

#### **Location 1: Core Vector Database** (`src/core/vector_database.py:196`)
```python
@dataclass
class SearchQuery:
    query_text: str
    limit: int = 10
    threshold: float = 0.0
    search_type: Optional['SearchType'] = None
    metadata_filter: Optional[Dict[str, Any]] = None
```
- **Type**: Dataclass
- **Fields**: `query_text`, `limit`, `threshold`, `search_type`, `metadata_filter`

---

#### **Location 2: Services Vector Models** (`src/services/models/vector_models.py:93`)
```python
@dataclass
class SearchQuery:
    query_text: str
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    similarity_threshold: float = 0.0
    filters: Optional[Dict[str, Any]] = None
```
- **Type**: Dataclass
- **Fields**: `query_text`, `search_type`, `limit`, `similarity_threshold`, `filters`
- **⚠️ SIMILAR**: Minor field name differences (`threshold` vs `similarity_threshold`, `metadata_filter` vs `filters`)

---

#### **Location 3: Services Vector Database Init** (`src/services/vector_database/__init__.py:42`)
```python
@dataclass
class SearchQuery:
    """Minimal SearchQuery for fallback."""
    query: str = ""
    limit: int = 10
```
- **Type**: Fallback stub (when imports fail)
- **Fields**: `query`, `limit`
- **⚠️ FALLBACK**: Minimal structure for error handling

---

#### **Location 4: Agent Management** (`src/services/agent_management.py:46`)
```python
@dataclass
class SearchQuery:
    query: str
    limit: int = 10
    agent_id: str | None = None
    metadata: dict[str, Any] | None = None
```
- **Type**: Fallback stub (when imports fail)
- **Fields**: `query`, `limit`, `agent_id`, `metadata`
- **⚠️ FALLBACK**: Domain-specific fields (agent_id)

---

#### **Location 5: Learning Recommender** (`src/services/learning_recommender.py:34`)
```python
@dataclass
class SearchQuery:
    query: str
    limit: int = 10
    agent_id: str | None = None
    metadata: dict[str, Any] | None = None
```
- **Type**: Fallback stub (when imports fail)
- **Fields**: `query`, `limit`, `agent_id`, `metadata`
- **⚠️ FALLBACK**: Identical to Location 4

---

**Additional Query-Related Classes Found**:
- `SearchRequest` in `src/web/vector_database/models.py` (may be related)
- `TradingQueryOperations`, `InMemoryQueryOperations` (different purpose)
- `ResultsQueryHelper`, `MonitoringQuery` (different purpose)

**Note**: User reported 7 locations. Found 5 SearchQuery class definitions. May include:
- `SearchRequest` (web models)
- Function parameters/variables
- Type hints
- Other query-related classes

**Action**: Analyze all 5 SearchQuery classes and determine if `SearchRequest` should be consolidated

---

## 🎯 SSOT IDENTIFICATION

### **Recommended SSOT Locations**:

#### **1. SearchResult SSOT**
**Recommended**: `src/services/models/vector_models.py`
- **Rationale**: 
  - Most complete structure
  - Used by services layer (core functionality)
  - Already has proper typing
  - Can be extended for domain-specific needs

**Alternative**: `src/core/vector_database.py` (if we want core-level SSOT)

---

#### **2. SearchQuery SSOT**
**Recommended**: `src/services/models/vector_models.py`
- **Rationale**:
  - Already has SearchResult SSOT
  - Consistent with services layer
  - Proper typing and defaults

**Alternative**: `src/core/vector_database.py` (if we want core-level SSOT)

---

#### **3. Config Class SSOT**

**For Pydantic Config**:
- **Recommended**: Create `src/core/pydantic_config.py` with shared config
- **Rationale**: Pydantic-specific, should be reusable

**For ShadowArchive Config**:
- **Recommended**: Migrate to `src/core/config_ssot.py` or create adapter
- **Rationale**: Should use unified config system

---

## 📋 CONSOLIDATION PLAN

### **Phase 1: Analysis & Planning** ✅ **COMPLETE**
- [x] Identify all Config class violations (5 locations)
- [x] Identify all SearchResult locations (7 locations)
- [x] Identify all SearchQuery locations (2 found, search for more)
- [x] Analyze field differences
- [x] Identify SSOT candidates
- [x] Create consolidation plan

---

### **Phase 2: SearchQuery Deep Search** 🔄 **IN PROGRESS**
- [ ] Search for all `SearchQuery` references (functions, variables, type hints)
- [ ] Identify if user meant 7 different query-related classes
- [ ] Document all findings

---

### **Phase 3: SSOT Selection & Creation**
- [ ] **3.1**: Select SSOT location for SearchResult
  - [ ] Decision: `src/services/models/vector_models.py` or `src/core/vector_database.py`
  - [ ] Create unified SearchResult with all necessary fields
  - [ ] Add backward compatibility shims

- [ ] **3.2**: Select SSOT location for SearchQuery
  - [ ] Decision: `src/services/models/vector_models.py` or `src/core/vector_database.py`
  - [ ] Create unified SearchQuery with all necessary fields
  - [ ] Add backward compatibility shims

- [ ] **3.3**: Create Pydantic Config SSOT
  - [ ] Create `src/core/pydantic_config.py`
  - [ ] Define shared Pydantic config class
  - [ ] Update Pydantic models to use shared config

- [ ] **3.4**: Migrate ShadowArchive Config
  - [ ] Create adapter for `src/ai_training/dreamvault/config.py`
  - [ ] Or migrate to `src/core/config_ssot.py`
  - [ ] Update imports

---

### **Phase 4: Import Updates**
- [ ] **4.1**: Update all SearchResult imports
  - [ ] Update 7 locations to use SSOT
  - [ ] Add backward compatibility shims where needed
  - [ ] Verify functionality

- [ ] **4.2**: Update all SearchQuery imports
  - [ ] Update all locations to use SSOT
  - [ ] Add backward compatibility shims where needed
  - [ ] Verify functionality

- [ ] **4.3**: Update Pydantic Config usage
  - [ ] Update 4 Pydantic models to use shared config
  - [ ] Verify Pydantic validation still works

- [ ] **4.4**: Update ShadowArchive Config
  - [ ] Update imports/adapter
  - [ ] Verify functionality

---

### **Phase 5: Archive & Cleanup**
- [ ] **5.1**: Archive duplicate SearchResult classes
  - [ ] Move to `deprecated/` or mark as deprecated
  - [ ] Add deprecation warnings
  - [ ] Update documentation

- [ ] **5.2**: Archive duplicate SearchQuery classes
  - [ ] Move to `deprecated/` or mark as deprecated
  - [ ] Add deprecation warnings
  - [ ] Update documentation

- [ ] **5.3**: Remove duplicate Config classes
  - [ ] Remove Pydantic Config duplicates (after migration)
  - [ ] Remove ShadowArchive Config (after migration)

---

### **Phase 6: SSOT Verification**
- [ ] **6.1**: Verify SearchResult SSOT compliance
  - [ ] Run import chain validator
  - [ ] Verify no duplicate definitions
  - [ ] Test all consumers

- [ ] **6.2**: Verify SearchQuery SSOT compliance
  - [ ] Run import chain validator
  - [ ] Verify no duplicate definitions
  - [ ] Test all consumers

- [ ] **6.3**: Verify Config SSOT compliance
  - [ ] Verify Pydantic config consolidation
  - [ ] Verify ShadowArchive config migration
  - [ ] Test all consumers

---

## 🔧 IMPLEMENTATION DETAILS

### **Unified SearchResult Structure**

**Recommended SSOT** (`src/services/models/vector_models.py`):
```python
@dataclass
class SearchResult:
    """Unified search result model - SSOT for all vector/search operations."""
    
    # Core fields (required)
    document_id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]
    
    # Optional fields (for different use cases)
    title: str | None = None
    collection: str | None = None
    source_type: str | None = None
    source_id: str | None = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    timestamp: datetime | None = None
    score: float | None = None  # Alias for similarity_score
    relevance: float | None = None  # Alias for similarity_score
    context_type: Any | None = None  # For intelligent context
    description: str | None = None  # For unified context
    size: str | None = None  # For web models
```

**Backward Compatibility**:
- Create shims for each domain-specific variant
- Use `__getattr__` for field aliases
- Provide conversion methods

---

### **Unified SearchQuery Structure**

**Recommended SSOT** (`src/services/models/vector_models.py`):
```python
@dataclass
class SearchQuery:
    """Unified search query model - SSOT for all vector/search operations."""
    
    query_text: str
    search_type: SearchType = SearchType.SIMILARITY
    limit: int = 10
    similarity_threshold: float = 0.0
    threshold: float | None = None  # Alias for similarity_threshold
    filters: Optional[Dict[str, Any]] = None
    metadata_filter: Optional[Dict[str, Any]] = None  # Alias for filters
```

**Backward Compatibility**:
- Support both `threshold` and `similarity_threshold`
- Support both `filters` and `metadata_filter`
- Provide conversion methods

---

### **Pydantic Config SSOT**

**Recommended** (`src/core/pydantic_config.py`):
```python
"""Shared Pydantic configuration - SSOT for Pydantic models."""

from pydantic import ConfigDict

# Pydantic v2 style (recommended)
BasePydanticConfig = ConfigDict(
    arbitrary_types_allowed=True,
    validate_assignment=True,
    use_enum_values=True,
)

# Pydantic v1 style (for backward compatibility)
class PydanticConfigV1:
    """Pydantic v1 config class."""
    arbitrary_types_allowed = True
```

**Usage**:
```python
from src.core.pydantic_config import BasePydanticConfig

class InboundMessage(BaseModel):
    model_config = BasePydanticConfig
    # ... fields
```

---

## 📊 IMPACT ANALYSIS

### **Files Affected**:

**SearchResult** (7 files):
1. `src/core/vector_database.py` (2 instances - need to consolidate)
2. `src/services/models/vector_models.py` (SSOT candidate)
3. `src/web/vector_database/models.py`
4. `src/core/intelligent_context/search_models.py`
5. `src/core/intelligent_context/unified_intelligent_context/models.py`
6. `src/core/intelligent_context/context_results.py`

**SearchQuery** (5+ files):
1. `src/core/vector_database.py` (full dataclass)
2. `src/services/models/vector_models.py` (SSOT candidate - full dataclass)
3. `src/services/vector_database/__init__.py` (fallback stub)
4. `src/services/agent_management.py` (fallback stub)
5. `src/services/learning_recommender.py` (fallback stub)
6. `src/web/vector_database/models.py` (SearchRequest - related)

**Config** (2 files):
1. `src/message_task/schemas.py` (4 Pydantic Config classes)
2. `src/ai_training/dreamvault/config.py` (1 Config class)

---

### **Risk Assessment**:

**HIGH RISK**:
- SearchResult has conflicting structures (Location 1 vs Location 2 in same file!)
- Web models have domain-specific fields
- Intelligent context has domain-specific fields

**MEDIUM RISK**:
- SearchQuery field name differences
- Pydantic Config migration (v1 vs v2)

**LOW RISK**:
- ShadowArchive Config migration (isolated domain)

---

## ✅ SUCCESS CRITERIA

1. ✅ All Config class violations resolved
2. ✅ All SearchResult duplicates consolidated to SSOT
3. ✅ All SearchQuery duplicates consolidated to SSOT
4. ✅ SSOT locations identified and documented
5. ✅ Backward compatibility maintained
6. ✅ All imports updated
7. ✅ All tests passing
8. ✅ SSOT verification complete

---

## 🚀 NEXT STEPS

1. **Immediate**: Complete Phase 2 (SearchQuery deep search)
2. **Next**: Phase 3 (SSOT selection & creation)
3. **Then**: Phase 4 (Import updates)
4. **Finally**: Phase 5 & 6 (Archive & verification)

---

**Status**: 📋 **PLANNING COMPLETE** - Ready for implementation

🐝 **WE. ARE. SWARM. ⚡🔥**

