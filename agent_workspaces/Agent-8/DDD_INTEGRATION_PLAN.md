# 🏗️ DDD Architecture Integration Plan

**Date**: 2025-12-01  
**Agent**: Agent-8 (SSOT & System Integration Specialist)  
**Status**: 📋 **PLANNING**  
**Priority**: HIGH

---

## 🎯 OBJECTIVE

**Migrate from SimpleTask implementation to professional DDD architecture.**

The project currently has:
- ✅ **Simple Implementation**: `SimpleTask` + `SimpleTaskRepository` (working, lightweight)
- ✅ **DDD Implementation**: Full domain entities, use cases, services (complete, not integrated)

**Goal**: Integrate the DDD architecture professionally, replacing the simple implementation.

---

## 📊 CURRENT STATE ANALYSIS

### **Simple Implementation** (Currently Used):

**Location**: `src/services/helpers/task_repo_loader.py`

**Components**:
- `SimpleTask` - Lightweight task class
- `SimpleTaskRepository` - SQLite-based repository
- Used by `TaskHandler` for CLI operations

**Pros**:
- ✅ Working and functional
- ✅ Lightweight (no heavy dependencies)
- ✅ Simple SQLite storage

**Cons**:
- ❌ No business rules validation
- ❌ No domain services (assignment scoring, etc.)
- ❌ No use case orchestration
- ❌ Duplicates domain logic

---

### **DDD Implementation** (Complete but Unused):

**Location**: `src/domain/`, `src/application/use_cases/`

**Components**:
- ✅ `Task` entity - Full business rules, validation
- ✅ `Agent` entity - Complete agent management
- ✅ `AssignTaskUseCase` - Professional orchestration
- ✅ `CompleteTaskUseCase` - Professional orchestration
- ✅ `AssignmentService` - Business logic (scoring, validation)
- ✅ Ports/Interfaces - Clean architecture

**Pros**:
- ✅ Complete business rules validation
- ✅ Domain services (assignment scoring, agent selection)
- ✅ Use case orchestration
- ✅ Clean architecture (ports/adapters)
- ✅ Professional DDD structure

**Cons**:
- ❌ Not integrated
- ❌ No repository implementation (only ports)
- ❌ Not wired up to CLI

---

## 🔄 INTEGRATION STRATEGY

### **Phase 1: Repository Implementation** ⏭️

**Create SQLite repository implementing domain ports:**

```python
# src/infrastructure/repositories/sqlite_task_repository.py
from src.domain.ports.task_repository import TaskRepository
from src.domain.entities.task import Task
from src.domain.value_objects.ids import TaskId

class SqliteTaskRepository(TaskRepository):
    """SQLite implementation of TaskRepository port."""
    # Implement all port methods using existing SQLite logic
```

**Action Items**:
1. Create `src/infrastructure/repositories/` directory
2. Implement `SqliteTaskRepository` (adapt existing SQLite code)
3. Implement `SqliteAgentRepository` (if needed)
4. Wire up to domain ports

---

### **Phase 2: Use Case Integration** ⏭️

**Update TaskHandler to use DDD use cases:**

```python
# src/services/handlers/task_handler.py
from src.application.use_cases.assign_task_uc import AssignTaskUseCase, AssignTaskRequest
from src.application.use_cases.complete_task_uc import CompleteTaskUseCase, CompleteTaskRequest

class TaskHandler:
    def _handle_get_next_task(self, args, repo, agent_id: str) -> bool:
        # Use AssignTaskUseCase instead of direct repo calls
        use_case = AssignTaskUseCase(...)
        request = AssignTaskRequest(task_id=..., agent_id=agent_id)
        response = use_case.execute(request)
        # Handle response
```

**Action Items**:
1. Update `TaskHandler` to use use cases
2. Wire up repositories to use cases
3. Add domain services (AssignmentService)
4. Add message bus (for domain events)
5. Add logger (for use cases)

---

### **Phase 3: Migration & Testing** ⏭️

**Migrate existing data and test:**

1. **Data Migration**:
   - Ensure existing SQLite schema is compatible
   - Migrate existing tasks if needed
   - Verify data integrity

2. **Testing**:
   - Test `--get-next-task` with DDD implementation
   - Test `--complete-task` with DDD implementation
   - Test `--list-tasks` with DDD implementation
   - Verify business rules are enforced

3. **Cleanup**:
   - Remove `SimpleTask` and `SimpleTaskRepository`
   - Update all imports
   - Remove duplicate code

---

## 📋 DETAILED ACTION PLAN

### **Step 1: Create Infrastructure Layer** ⏭️

**Files to Create**:
- `src/infrastructure/__init__.py`
- `src/infrastructure/repositories/__init__.py`
- `src/infrastructure/repositories/sqlite_task_repository.py`
- `src/infrastructure/repositories/sqlite_agent_repository.py`

**Implementation**:
- Adapt existing SQLite code from `task_repo_loader.py`
- Implement domain ports (`TaskRepository`, `AgentRepository`)
- Use domain entities (`Task`, `Agent`) instead of `SimpleTask`

---

### **Step 2: Create Adapters for Use Cases** ⏭️

**Files to Create/Update**:
- `src/infrastructure/adapters/__init__.py`
- `src/infrastructure/adapters/message_bus_adapter.py` (simple implementation)
- `src/infrastructure/adapters/logger_adapter.py` (use Python logging)

**Implementation**:
- Simple message bus (can be in-memory for now)
- Logger adapter wrapping Python logging
- Wire up to use cases

---

### **Step 3: Update TaskHandler** ⏭️

**File to Update**: `src/services/handlers/task_handler.py`

**Changes**:
- Replace `SimpleTaskRepository` with `SqliteTaskRepository`
- Replace direct repo calls with use case calls
- Use `AssignTaskUseCase` for `--get-next-task`
- Use `CompleteTaskUseCase` for `--complete-task`
- Keep CLI formatting logic (that's fine)

---

### **Step 4: Remove Simple Implementation** ⏭️

**Files to Remove**:
- `src/services/helpers/task_repo_loader.py` (after migration)

**Update Imports**:
- Find all imports of `SimpleTask` or `SimpleTaskRepository`
- Replace with domain entities and repositories

---

## 🎯 BENEFITS OF INTEGRATION

### **1. Business Rules Enforcement**:
- ✅ Task validation (title, priority)
- ✅ Assignment validation (agent capacity, capabilities)
- ✅ Completion validation (must be assigned)

### **2. Professional Architecture**:
- ✅ Clean separation of concerns
- ✅ Domain logic in domain layer
- ✅ Use cases orchestrate business logic
- ✅ Infrastructure adapts to domain

### **3. Extensibility**:
- ✅ Easy to add new use cases
- ✅ Easy to swap repositories (SQLite → PostgreSQL, etc.)
- ✅ Easy to add domain services
- ✅ Easy to add domain events

### **4. Testability**:
- ✅ Domain logic is testable in isolation
- ✅ Use cases are testable with mocks
- ✅ Repositories are testable independently

---

## ⚠️ RISKS & MITIGATION

### **Risk 1: Breaking Existing Functionality**

**Mitigation**:
- Keep existing SQLite schema (compatible)
- Test thoroughly before removing simple implementation
- Gradual migration (feature flag if needed)

### **Risk 2: Increased Complexity**

**Mitigation**:
- DDD architecture is actually simpler long-term
- Clear separation of concerns
- Better maintainability

### **Risk 3: Missing Dependencies**

**Mitigation**:
- Create simple adapters (message bus, logger)
- Can start with minimal implementations
- Add complexity as needed

---

## 📊 SUCCESS CRITERIA

### **Functional**:
- ✅ `--get-next-task` works with DDD implementation
- ✅ `--complete-task` works with DDD implementation
- ✅ `--list-tasks` works with DDD implementation
- ✅ Business rules are enforced (validation errors)
- ✅ Assignment scoring works (if agent selection added)

### **Architectural**:
- ✅ Domain entities used instead of SimpleTask
- ✅ Use cases orchestrate business logic
- ✅ Repositories implement domain ports
- ✅ No duplicate task/agent logic

### **Code Quality**:
- ✅ SimpleTask removed
- ✅ All imports updated
- ✅ No duplicate code
- ✅ Tests pass

---

## 🚀 IMPLEMENTATION ORDER

1. **Create Infrastructure Layer** (repositories, adapters)
2. **Update TaskHandler** (use use cases)
3. **Test Integration** (verify functionality)
4. **Remove Simple Implementation** (cleanup)
5. **Update Documentation** (reflect new architecture)

---

## 📝 NOTES

- **Existing SQLite schema is compatible** - domain entities match
- **Can migrate gradually** - no need for big bang
- **Simple adapters are fine** - can improve later
- **Domain events are optional** - can start simple

---

## 🎉 CONCLUSION

**Status**: 📋 **READY FOR IMPLEMENTATION**

The DDD architecture is complete and ready for integration. This will:
- ✅ Replace simple implementation with professional architecture
- ✅ Enforce business rules properly
- ✅ Enable future extensibility
- ✅ Follow clean architecture principles

**Next Step**: Begin Phase 1 - Create Infrastructure Layer

---

🐝 WE. ARE. SWARM. ⚡🔥

**Agent-8 - SSOT & System Integration Specialist**  
*Integrating Professional DDD Architecture*

