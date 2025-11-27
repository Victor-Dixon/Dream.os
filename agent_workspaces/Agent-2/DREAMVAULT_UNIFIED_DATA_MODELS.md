# DreamVault Unified Data Models - Agent-2

**Date**: 2025-11-26  
**Agent**: Agent-2 (Architecture & Design Specialist)  
**Status**: ✅ **DATA MODEL DESIGN IN PROGRESS**

---

## 🗄️ **UNIFIED DATA MODEL ARCHITECTURE**

### **Core Principles**
1. **Single Source of Truth**: One model per entity
2. **Normalization**: Eliminate data duplication
3. **Versioning**: Support model evolution
4. **Validation**: Strong type checking
5. **Migration**: Smooth schema transitions

---

## 📊 **CORE DATA MODELS**

### **1. User Model** (Shared)

```python
@dataclass
class User:
    id: str
    email: str
    username: str
    preferences: UserPreferences
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage"""
        pass
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create from dictionary"""
        pass

@dataclass
class UserPreferences:
    theme: str
    notifications: bool
    portfolio_defaults: dict
    ai_assistant_config: dict
```

**Database Schema**:
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    preferences JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

---

### **2. Portfolio Models** (from DreamBank)

```python
@dataclass
class Portfolio:
    id: str
    user_id: str
    name: str
    description: Optional[str]
    stocks: List[Stock]
    cash_balance: float
    total_value: float
    config: PortfolioConfig
    created_at: datetime
    updated_at: datetime
    
    def calculate_total_value(self) -> float:
        """Calculate current portfolio value"""
        pass
    
    def get_performance(self) -> PerformanceMetrics:
        """Get portfolio performance metrics"""
        pass

@dataclass
class Stock:
    symbol: str
    company_name: str
    quantity: int
    purchase_price: float
    current_price: float
    purchase_date: datetime
    sector: Optional[str]
    industry: Optional[str]
    
    def get_gain_loss(self) -> float:
        """Calculate gain/loss"""
        return (self.current_price - self.purchase_price) * self.quantity

@dataclass
class PortfolioConfig:
    risk_tolerance: str  # conservative, moderate, aggressive
    rebalance_frequency: str  # daily, weekly, monthly
    auto_trade: bool
    notification_settings: dict
```

**Database Schema**:
```sql
CREATE TABLE portfolios (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cash_balance DECIMAL(15, 2) DEFAULT 0,
    total_value DECIMAL(15, 2) DEFAULT 0,
    config JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE stocks (
    id VARCHAR(36) PRIMARY KEY,
    portfolio_id VARCHAR(36) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    company_name VARCHAR(255),
    quantity INT NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    current_price DECIMAL(10, 2),
    purchase_date DATE NOT NULL,
    sector VARCHAR(100),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);
```

---

### **3. AI Conversation Models** (from DigitalDreamscape + Thea)

```python
@dataclass
class Conversation:
    id: str
    user_id: str
    title: Optional[str]
    messages: List[Message]
    context: ConversationContext
    state: ConversationState
    config: ConversationConfig
    created_at: datetime
    updated_at: datetime
    
    def add_message(self, message: Message) -> None:
        """Add message to conversation"""
        pass
    
    def get_context(self) -> dict:
        """Get conversation context for AI"""
        pass

@dataclass
class Message:
    id: str
    conversation_id: str
    role: MessageRole  # user, assistant, system
    content: str
    content_type: str  # text, image, audio, etc.
    metadata: dict
    timestamp: datetime
    
    def to_ai_format(self) -> dict:
        """Convert to AI model format"""
        pass

@dataclass
class ConversationContext:
    user_profile: dict
    conversation_history: List[dict]
    current_topic: Optional[str]
    entities: List[dict]
    intent: Optional[str]
    sentiment: Optional[str]

@dataclass
class ConversationState:
    status: str  # active, paused, completed
    current_step: Optional[str]
    variables: dict
    flags: dict
```

**Database Schema**:
```sql
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(255),
    context JSON,
    state JSON,
    config JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50) DEFAULT 'text',
    metadata JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

---

### **4. Shared Models**

```python
@dataclass
class PerformanceMetrics:
    total_return: float
    total_return_percent: float
    daily_return: float
    volatility: float
    sharpe_ratio: Optional[float]
    period: str  # 1d, 1w, 1m, 1y, all

@dataclass
class APIResponse:
    success: bool
    data: Optional[dict]
    error: Optional[str]
    timestamp: datetime
    
@dataclass
class ValidationResult:
    valid: bool
    errors: List[str]
    warnings: List[str]
```

---

## 🔄 **DATA MIGRATION STRATEGY**

### **Migration Plan**

**Phase 1: Schema Creation**
1. Create unified database schema
2. Create migration scripts
3. Backup existing data

**Phase 2: Data Transformation**
1. Transform DreamBank portfolio data
2. Transform DigitalDreamscape conversation data
3. Transform Thea conversation data
4. Merge user data

**Phase 3: Validation**
1. Validate data integrity
2. Check referential integrity
3. Verify data completeness
4. Test data access

**Phase 4: Cutover**
1. Switch to unified models
2. Update application code
3. Monitor for issues
4. Rollback plan ready

---

## 🧪 **MODEL VALIDATION**

### **Validation Rules**

**User Model**:
- Email must be valid format
- Username must be unique
- Preferences must match schema

**Portfolio Model**:
- User must exist
- Stock quantities must be positive
- Prices must be positive
- Dates must be valid

**Conversation Model**:
- User must exist
- Messages must be in chronological order
- Context must be valid JSON
- State must match schema

---

## 📋 **IMPLEMENTATION CHECKLIST**

- [ ] Define all data models
- [ ] Create database schemas
- [ ] Create migration scripts
- [ ] Create validation rules
- [ ] Create model serialization
- [ ] Create model deserialization
- [ ] Create unit tests for models
- [ ] Create integration tests

---

**Status**: ✅ **DATA MODEL DESIGN IN PROGRESS**  
**Last Updated**: 2025-11-26 10:59:13 (Local System Time)

