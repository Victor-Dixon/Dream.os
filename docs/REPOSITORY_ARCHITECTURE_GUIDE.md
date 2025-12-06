# 📚 Repository Architecture Guide

**Date**: 2025-12-04  
**Author**: Agent-8 (Testing & Quality Assurance Specialist)  
**Status**: ✅ **ACTIVE DOCUMENTATION**

---

## 🎯 Overview

This guide explains the repository architecture patterns used in the codebase, including when to use which implementation and how they relate to SSOT principles.

---

## 🏗️ Architecture Layers

### **1. Domain Layer (Ports)**

**Location**: `src/domain/ports/`

**Purpose**: Define interfaces (Protocols) that the domain layer depends on.

**Files**:
- `agent_repository.py` - Agent persistence interface
- `task_repository.py` - Task persistence interface

**Characteristics**:
- ✅ Protocol-based (using `typing.Protocol`)
- ✅ Domain-driven design
- ✅ Hexagonal architecture ports
- ✅ SSOT Domain: `domain`

**Example**:
```python
class AgentRepository(Protocol):
    """Port for agent persistence operations."""
    
    def get(self, agent_id: AgentId) -> Agent | None:
        """Retrieve an agent by its identifier."""
        ...
```

**When to Use**:
- Domain layer code should depend on these ports
- Never import concrete implementations in domain layer
- Use for dependency injection

---

### **2. Infrastructure Layer (Adapters)**

**Location**: `src/infrastructure/persistence/`

**Purpose**: Concrete implementations of domain ports using various persistence mechanisms.

#### **2.1 Database-Based Repositories**

**Files**:
- `base_repository.py` - Abstract base class for database repositories
- `agent_repository.py` - SQLite implementation (via BaseRepository)
- `task_repository.py` - SQLite implementation (via BaseRepository)
- `sqlite_agent_repo.py` - Direct SQLite implementation
- `sqlite_task_repo.py` - Direct SQLite implementation

**Characteristics**:
- ✅ Extends `BaseRepository[T]` or implements domain ports directly
- ✅ Uses SQLite for persistence
- ✅ SSOT Domain: `infrastructure`
- ✅ Implements domain port interfaces

**When to Use**:
- Production persistence
- When you need ACID transactions
- When you need complex queries
- When data volume is significant

**Example**:
```python
class AgentRepository(BaseRepository[Agent]):
    """Repository for Agent entities using SQLite."""
    
    def __init__(self, db_connection: DatabaseConnection):
        super().__init__(db_connection)
        self._ensure_schema()
```

#### **2.2 File-Based Repositories**

**Location**: `src/repositories/`

**Files**:
- `base_file_repository.py` - Abstract base class for file-based repositories
- `agent_repository.py` - File-based workspace operations
- `contract_repository.py` - JSON file storage
- `message_repository.py` - JSON file storage
- `activity_repository.py` - JSON file storage
- `metrics_repository.py` - JSON file storage

**Characteristics**:
- ✅ Uses JSON files for persistence
- ✅ Extends `BaseFileRepository` (for new implementations)
- ✅ SSOT Domain: `data`
- ✅ Simpler than database, good for small datasets

**When to Use**:
- Development/testing
- Small datasets (<1000 items)
- Simple data structures
- When you don't need transactions
- Workspace/file system operations

**Example**:
```python
class ContractRepository(BaseFileRepository):
    """Repository for contract data using JSON files."""
    
    def _get_default_data(self) -> dict[str, Any]:
        return {"contracts": [], "metadata": {"version": "1.0"}}
    
    def _get_data_key(self) -> str:
        return "contracts"
```

---

## 🔄 Repository Patterns

### **Pattern 1: Port/Adapter (Hexagonal Architecture)**

**Structure**:
```
Domain Layer (Ports)
    ↓ depends on
Infrastructure Layer (Adapters)
    ↓ implements
Persistence (Database/File)
```

**Benefits**:
- ✅ Domain layer is independent of infrastructure
- ✅ Easy to swap implementations
- ✅ Testable (can mock ports)
- ✅ Follows SOLID principles

**Example Flow**:
1. Domain defines `AgentRepository` protocol
2. Infrastructure implements `SqliteAgentRepository(AgentRepository)`
3. Dependency injection provides adapter to domain

---

### **Pattern 2: Base Repository**

**Purpose**: Consolidate common operations.

**Types**:
- `BaseRepository[T]` - For database repositories
- `BaseFileRepository` - For file-based repositories

**Benefits**:
- ✅ Reduces code duplication
- ✅ Standardizes operations
- ✅ Consistent error handling
- ✅ Easier maintenance

---

### **Pattern 3: Multiple Implementations**

**Why Multiple Implementations?**:

1. **Different Purposes**:
   - Database: Entity persistence (Agent, Task entities)
   - File-based: Workspace operations, simple data storage

2. **Different Use Cases**:
   - Production: Database (ACID, transactions)
   - Development: File-based (simpler, faster setup)

3. **Architecture Layers**:
   - Domain ports: Interfaces
   - Infrastructure: Concrete implementations

**Example**: `AgentRepository`
- `src/domain/ports/agent_repository.py` - Interface
- `src/infrastructure/persistence/agent_repository.py` - Database implementation
- `src/repositories/agent_repository.py` - File-based workspace operations

**Note**: These serve different purposes and are not true duplicates.

---

## 📋 SSOT Compliance

### **SSOT Domain Tags**

All repository files must include SSOT domain tags:

```python
"""
Repository Description

<!-- SSOT Domain: infrastructure -->
"""
```

**Domain Assignments**:
- `infrastructure` - Database persistence layer
- `domain` - Domain port interfaces
- `data` - File-based repositories
- `integration` - Integration-specific repositories (e.g., metrics)

### **SSOT Principles**

1. **Single Source of Truth**: Each repository type has one authoritative implementation
2. **Domain Ownership**: Clear domain assignment via SSOT tags
3. **No Duplication**: Avoid duplicate implementations for the same purpose
4. **Documentation**: Document when to use which implementation

---

## 🚀 Usage Guidelines

### **When to Use Database Repositories**

✅ Use when:
- Production environment
- Need ACID transactions
- Complex queries required
- Large datasets (>1000 items)
- Need concurrent access
- Data integrity critical

❌ Don't use when:
- Development/testing (unless testing database features)
- Simple data structures
- Small datasets
- File system operations

---

### **When to Use File-Based Repositories**

✅ Use when:
- Development/testing
- Small datasets (<1000 items)
- Simple data structures
- Workspace/file operations
- No transaction requirements
- Quick prototyping

❌ Don't use when:
- Production (unless specific use case)
- Large datasets
- Need transactions
- Concurrent writes
- Complex queries

---

### **When to Use Domain Ports**

✅ Always use in:
- Domain layer code
- Business logic
- Use cases
- Services (when possible)

**Example**:
```python
# ✅ Good - depends on port
def assign_task(agent_repo: AgentRepository, task_repo: TaskRepository):
    agent = agent_repo.get(agent_id)
    task = task_repo.get(task_id)
    # ... business logic

# ❌ Bad - depends on concrete implementation
def assign_task(agent_repo: SqliteAgentRepository, task_repo: SqliteTaskRepository):
    # ... business logic
```

---

## 🔧 Migration Path

### **From File-Based to Database**

1. **Create Database Implementation**:
   - Implement domain port
   - Use `BaseRepository[T]` if applicable
   - Add schema creation

2. **Update Dependency Injection**:
   - Change adapter registration
   - Update configuration

3. **Migrate Data** (if needed):
   - Export from file-based
   - Import to database
   - Verify data integrity

4. **Update Tests**:
   - Use database test fixtures
   - Update mocks if needed

---

## 📊 Repository Comparison

| Feature | Database | File-Based |
|---------|----------|------------|
| **Persistence** | SQLite | JSON files |
| **Transactions** | ✅ Yes | ❌ No |
| **Concurrent Access** | ✅ Yes | ⚠️ Limited |
| **Query Complexity** | ✅ High | ❌ Low |
| **Setup Complexity** | ⚠️ Medium | ✅ Low |
| **Performance (Large Data)** | ✅ Fast | ❌ Slow |
| **Performance (Small Data)** | ⚠️ Medium | ✅ Fast |
| **Data Integrity** | ✅ High | ⚠️ Medium |
| **Best For** | Production | Development/Testing |

---

## 🧪 Testing

### **Testing Ports**

Use mocks/stubs for domain ports:
```python
class MockAgentRepository:
    def get(self, agent_id: AgentId) -> Agent | None:
        return Agent(id=agent_id, name="Test Agent")
```

### **Testing Implementations**

Test concrete implementations:
```python
def test_agent_repository_save():
    repo = SqliteAgentRepository(":memory:")
    agent = Agent(id="test", name="Test")
    repo.save(agent)
    assert repo.get(AgentId("test")) == agent
```

---

## 📝 Best Practices

1. **Always Use Ports in Domain Layer**
   - Never import concrete implementations
   - Use dependency injection

2. **Choose Right Implementation**
   - Database for production
   - File-based for development/testing

3. **Extend Base Classes**
   - Use `BaseRepository[T]` for database
   - Use `BaseFileRepository` for file-based

4. **Add SSOT Tags**
   - All repository files need SSOT domain tags
   - Document domain ownership

5. **Document Purpose**
   - Explain when to use which implementation
   - Document migration paths

---

## 🔗 Related Documentation

- [SSOT Protocol](../runtime/agent_comms/SSOT_PROTOCOL.md)
- [Repository Duplication Analysis](../../agent_workspaces/Agent-8/REPOSITORY_LAYER_DUPLICATION_ANALYSIS.md)
- [Hexagonal Architecture Guide](https://alistair.cockburn.us/hexagonal-architecture/)

---

## 📊 Summary

**Repository Types**:
- **Domain Ports**: Interfaces (Protocol)
- **Database Repositories**: SQLite implementations
- **File-Based Repositories**: JSON file implementations

**SSOT Domains**:
- `domain` - Port interfaces
- `infrastructure` - Database implementations
- `data` - File-based implementations

**Key Principle**: Domain depends on ports, infrastructure implements ports.

---

**Status**: ✅ **ACTIVE** - Keep this guide updated as architecture evolves

🐝 **WE. ARE. SWARM. ⚡🔥**

