# Phase 2 Integration Execution Plan

**Agent**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-01  
**Status**: ✅ **EXECUTING**  
**Priority**: HIGH  
**Coordinated with**: Agent-2 (Architecture & Design Specialist)

---

## 🎯 EXECUTIVE SUMMARY

**Phase 2 Tasks**:
1. ⏳ Message Queue Integration → Register in UnifiedSystemIntegration
2. ⏳ API Client Integration → Register API clients
3. ⏳ Database Integration → Register database connections

**Goal**: Integrate existing systems into UnifiedSystemIntegration framework for unified management.

---

## 📋 TASK 1: Message Queue Integration (HIGH)

### **Target**: `src/architecture/system_integration.py`

### **Integration Point**: `src/core/message_queue.py`

### **Implementation Steps**:

1. **Add auto-registration method**:
```python
def register_message_queue(self, queue_instance: Any = None) -> bool:
    """Register message queue system in integration framework."""
    try:
        # Import message queue
        from src.core.message_queue import MessageQueue
        
        # Get or create queue instance
        if queue_instance is None:
            queue_instance = MessageQueue()
        
        # Register as message queue endpoint
        queue_url = f"file://{queue_instance.config.queue_directory}"
        return self.register_endpoint(
            "message_queue",
            IntegrationType.MESSAGE_QUEUE,
            queue_url
        )
    except Exception as e:
        self.logger.error(f"Failed to register message queue: {e}")
        return False
```

2. **Add health check for message queue**:
```python
def check_message_queue_health(self) -> dict[str, Any]:
    """Check message queue health."""
    if "message_queue" not in self.endpoints:
        return {'error': "Message queue not registered"}
    
    try:
        from src.core.message_queue import MessageQueue
        queue = MessageQueue()
        stats = queue.get_statistics()
        
        # Update endpoint status
        endpoint = self.endpoints["message_queue"]
        endpoint.status = IntegrationStatus.CONNECTED
        endpoint.last_checked = datetime.now().isoformat()
        endpoint.response_time = 0.1
        
        return {
            'endpoint': 'message_queue',
            'status': 'connected',
            'queue_size': stats.get('queue_size', 0),
            'pending_messages': stats.get('pending_messages', 0),
            'last_checked': endpoint.last_checked
        }
    except Exception as e:
        self.logger.error(f"Message queue health check failed: {e}")
        self.endpoints["message_queue"].status = IntegrationStatus.ERROR
        return {'error': str(e), 'endpoint': 'message_queue'}
```

---

## 📋 TASK 2: API Client Integration (MEDIUM)

### **Integration Points**:
- `src/shared_utils/api_client.py` - General API client
- Trading robot API clients (if any)

### **Implementation Steps**:

1. **Add API client registration**:
```python
def register_api_client(self, name: str, base_url: str) -> bool:
    """Register an API client in integration framework."""
    return self.register_endpoint(
        f"api_{name}",
        IntegrationType.API,
        base_url
    )
```

2. **Auto-register existing API clients**:
```python
def auto_register_api_clients(self) -> dict[str, bool]:
    """Auto-register existing API clients."""
    results = {}
    
    # Register shared API client
    try:
        from src.shared_utils.api_client import APIClient
        # Get base URL from config or default
        base_url = "https://api.example.com"  # Update with actual URL
        results['shared_api'] = self.register_api_client('shared', base_url)
    except Exception as e:
        self.logger.warning(f"Could not register shared API client: {e}")
        results['shared_api'] = False
    
    return results
```

---

## 📋 TASK 3: Database Integration (MEDIUM)

### **Integration Points**:
- `src/infrastructure/persistence/database_connection.py` - Main database connection
- `src/ai_training/dreamvault/database.py` - DreamVault database

### **Implementation Steps**:

1. **Add database registration**:
```python
def register_database(self, name: str, connection_string: str) -> bool:
    """Register a database connection in integration framework."""
    return self.register_endpoint(
        f"database_{name}",
        IntegrationType.DATABASE,
        connection_string
    )
```

2. **Auto-register existing databases**:
```python
def auto_register_databases(self) -> dict[str, bool]:
    """Auto-register existing database connections."""
    results = {}
    
    # Register persistence database
    try:
        from src.infrastructure.persistence.database_connection import DatabaseConnection
        from src.infrastructure.persistence.persistence_models import PersistenceConfig
        config = PersistenceConfig()
        db_url = f"sqlite://{config.db_path}"
        results['persistence_db'] = self.register_database('persistence', db_url)
    except Exception as e:
        self.logger.warning(f"Could not register persistence database: {e}")
        results['persistence_db'] = False
    
    # Register DreamVault database
    try:
        import os
        db_url = os.getenv("DATABASE_URL", "sqlite:///data/dreamvault.db")
        results['dreamvault_db'] = self.register_database('dreamvault', db_url)
    except Exception as e:
        self.logger.warning(f"Could not register DreamVault database: {e}")
        results['dreamvault_db'] = False
    
    return results
```

---

## 🚀 EXECUTION PLAN

### **Step 1: Message Queue Integration** (30 min)
1. Add `register_message_queue()` method
2. Add `check_message_queue_health()` method
3. Test registration and health check
4. Verify backward compatibility

### **Step 2: API Client Integration** (30 min)
1. Add `register_api_client()` method
2. Add `auto_register_api_clients()` method
3. Test API client registration
4. Verify backward compatibility

### **Step 3: Database Integration** (30 min)
1. Add `register_database()` method
2. Add `auto_register_databases()` method
3. Test database registration
4. Verify backward compatibility

### **Step 4: Integration Testing** (30 min)
1. Test all integrations together
2. Verify health checks work
3. Test unified status reporting
4. Verify no breaking changes

---

## ✅ SUCCESS CRITERIA

### **Message Queue Integration**:
- ✅ Message queue registered in UnifiedSystemIntegration
- ✅ Health check works
- ✅ Status reporting functional
- ✅ Backward compatible

### **API Client Integration**:
- ✅ API clients registered
- ✅ Health checks work
- ✅ Status reporting functional
- ✅ Backward compatible

### **Database Integration**:
- ✅ Databases registered
- ✅ Health checks work
- ✅ Status reporting functional
- ✅ Backward compatible

---

**Plan Created By**: Agent-1 (Integration & Core Systems Specialist)  
**Date**: 2025-12-01  
**Status**: ✅ **EXECUTING**  
**Next Step**: Implement Step 1 - Message Queue Integration

🐝 **WE. ARE. SWARM. ⚡🔥**

