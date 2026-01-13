# File Relationship Mapping: Risk Analytics Ecosystem
## Dependencies Between Key Files (Risk Calculator ↔ WebSocket ↔ Dashboard)

**Author:** Agent-5 (Business Intelligence Specialist)
**Date:** 2026-01-08
**Version:** 1.0
**Purpose:** Comprehensive mapping of dependencies between risk calculator, WebSocket server, and dashboard integration components

---

## Executive Summary

This document provides a detailed mapping of the dependencies and relationships between the three core components of the risk analytics ecosystem:

1. **Risk Calculator Service** - Core business logic for risk calculations
2. **Risk WebSocket Server** - Real-time data streaming infrastructure
3. **Risk Dashboard Integration** - Frontend consumption and visualization

The mapping covers data flow, API contracts, architectural dependencies, and maintenance relationships between these interconnected components.

### Key Findings
- **Tight Coupling:** All three components share the same data models and communication protocols
- **Real-time Pipeline:** Calculator → WebSocket → Dashboard forms a complete real-time risk analytics pipeline
- **Shared State:** Common risk metrics definitions across all three layers
- **Synchronous Dependencies:** WebSocket server depends on calculator service availability

---

## 1. Component Overview

### 1.1 Risk Calculator Service
**File:** `src/services/risk_analytics/risk_calculator_service.py` (400+ lines)
**Purpose:** Core business logic for calculating advanced risk metrics
**Dependencies:**
- **Input:** Trading performance data (returns, equity curves, positions)
- **Output:** Standardized risk metrics (VaR, CVaR, Sharpe Ratio, Max Drawdown)
- **Data Models:** `RiskMetrics`, `RiskCalculator` classes

### 1.2 Risk WebSocket Server
**File:** `src/services/risk_analytics/risk_websocket_server.py` (467+ lines)
**Purpose:** Real-time streaming infrastructure for risk metrics
**Dependencies:**
- **Input:** Risk calculator service (synchronous calls)
- **Output:** WebSocket streams to dashboard clients
- **Protocols:** WebSocket connections, JSON message formats

### 1.3 Risk Dashboard Integration
**File:** `src/web/static/js/trading-robot/risk-dashboard-integration.js` (342+ lines)
**Purpose:** Frontend consumption and visualization of risk metrics
**Dependencies:**
- **Input:** WebSocket streams from risk server
- **Output:** UI updates, alerts, visualizations
- **Integration:** Trading dashboard components

---

## 2. Data Flow Architecture

### 2.1 Forward Data Flow (Calculator → WebSocket → Dashboard)

```
Trading Data → Risk Calculator Service → Risk WebSocket Server → Risk Dashboard Integration → UI Display
     ↓              ↓                           ↓                        ↓                     ↓
  Raw Data    Standardized Metrics      WebSocket Streams       Real-time Updates     User Interface
```

#### Step 1: Trading Data Input
```python
# Input data structure (from trading platforms)
trading_data = {
    'returns': [0.01, -0.005, 0.02, ...],  # Daily returns
    'equity_curve': [10000, 10050, 10025, ...],  # Account equity over time
    'positions': [{'symbol': 'AAPL', 'quantity': 100}, ...],  # Current positions
    'timestamps': ['2024-01-01', '2024-01-02', ...]  # Time series data
}
```

#### Step 2: Risk Calculation (RiskCalculatorService)
```python
# RiskCalculatorService.calculate_comprehensive_risk_metrics()
risk_metrics = {
    'var_95': -0.0234,        # 95% Value at Risk
    'cvar_95': -0.0345,       # 95% Conditional VaR
    'sharpe_ratio': 1.23,     # Risk-adjusted returns
    'max_drawdown': -0.156,   # Maximum peak-to-trough decline
    'volatility': 0.187,      # Portfolio volatility
    'calmar_ratio': 0.89,     # Drawdown-adjusted returns
    'sortino_ratio': 1.45,    # Downside risk-adjusted returns
    'information_ratio': 0.67 # Active return relative to benchmark
}
```

#### Step 3: WebSocket Streaming (RiskWebSocketServer)
```json
// WebSocket message format
{
  "type": "risk_metrics_update",
  "timestamp": "2026-01-08T05:15:00Z",
  "data": {
    "portfolio_id": "main_portfolio",
    "metrics": {
      "var_95": -0.0234,
      "cvar_95": -0.0345,
      "sharpe_ratio": 1.23,
      "max_drawdown": -0.156,
      "volatility": 0.187
    },
    "alerts": [],
    "status": "active"
  }
}
```

#### Step 4: Dashboard Consumption (RiskDashboardIntegration)
```javascript
// RiskDashboardIntegration processes WebSocket messages
this.riskMetrics = {
  var95: -0.0234,
  cvar95: -0.0345,
  sharpeRatio: 1.23,
  maxDrawdown: -0.156,
  volatility: 0.187
};

// Triggers UI updates
this.notifySubscribers('metrics_updated', this.riskMetrics);
this.updateUI();
```

### 2.2 Reverse Data Flow (Dashboard → WebSocket → Calculator)

```
UI Controls → Risk Dashboard Integration → Risk WebSocket Server → Risk Calculator Service → Updated Metrics
     ↓              ↓                           ↓                        ↓                     ↓
User Actions    Control Commands         Parameter Updates       Recalculation Triggers   Fresh Metrics
```

#### Configuration Updates
```javascript
// Dashboard sends configuration changes
websocket.send(JSON.stringify({
  type: 'config_update',
  data: {
    confidence_level: 0.99,  // Changed from 0.95 to 0.99
    time_horizon: 252        // Trading days in a year
  }
}));
```

---

## 3. API Contracts and Interfaces

### 3.1 Risk Calculator Service Interface

```python
class RiskCalculatorService:
    """Core risk calculation interface used by WebSocket server."""

    async def calculate_comprehensive_risk_metrics(
        self,
        returns: List[float],
        equity_curve: Optional[List[float]] = None,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive risk metrics.

        Args:
            returns: Time series of daily returns
            equity_curve: Optional equity curve data
            confidence_level: VaR confidence level (default 95%)

        Returns:
            Dict containing all risk metrics
        """
        pass

    async def calculate_var(
        self,
        returns: List[float],
        confidence_level: float = 0.95,
        method: str = 'historical'
    ) -> float:
        """Calculate Value at Risk."""
        pass

    async def calculate_sharpe_ratio(
        self,
        returns: List[float],
        risk_free_rate: float = 0.02
    ) -> float:
        """Calculate Sharpe ratio."""
        pass
```

### 3.2 WebSocket Server Interface

```python
class RiskWebSocketServer:
    """WebSocket interface consumed by dashboard integration."""

    async def start_server(self, host: str = 'localhost', port: int = 8765) -> None:
        """Start WebSocket server."""
        pass

    async def broadcast_risk_metrics(self, metrics: Dict[str, Any]) -> None:
        """Broadcast risk metrics to all connected clients."""
        pass

    async def send_to_client(self, client_id: str, message: Dict[str, Any]) -> None:
        """Send message to specific client."""
        pass

    def get_connected_clients(self) -> List[str]:
        """Get list of connected client IDs."""
        pass
```

### 3.3 Dashboard Integration Interface

```javascript
class RiskDashboardIntegration {
    /** Dashboard interface that consumes WebSocket data. */

    constructor() {
        this.websocket = null;
        this.riskMetrics = {};
        this.alerts = [];
    }

    async initialize() {
        /** Initialize WebSocket connection and event handlers. */
    }

    async connect() {
        /** Establish WebSocket connection to risk server. */
    }

    updateRiskMetrics(metrics) {
        /** Update local risk metrics from WebSocket data. */
    }

    notifySubscribers(event, data) {
        /** Notify dashboard subscribers of updates. */
    }
}
```

---

## 4. Shared Data Models and Constants

### 4.1 Risk Metrics Definitions

All three components share identical risk metric definitions:

```python
# Shared in risk_calculator_service.py and risk_websocket_server.py
RISK_METRICS_SCHEMA = {
    'var_95': '95% Value at Risk (daily loss threshold)',
    'cvar_95': '95% Conditional VaR (expected loss beyond VaR)',
    'sharpe_ratio': 'Risk-adjusted returns (excess return per unit risk)',
    'max_drawdown': 'Maximum peak-to-trough portfolio decline',
    'volatility': 'Portfolio standard deviation (annualized)',
    'calmar_ratio': 'Drawdown-adjusted returns',
    'sortino_ratio': 'Downside risk-adjusted returns',
    'information_ratio': 'Active return relative to benchmark'
}
```

### 4.2 WebSocket Message Types

```javascript
// Shared between risk_websocket_server.py and risk-dashboard-integration.js
WEBSOCKET_MESSAGE_TYPES = {
    'risk_metrics_update': 'Real-time risk metrics update',
    'risk_alert': 'Risk threshold breach alert',
    'portfolio_status': 'Portfolio health status',
    'config_update': 'Configuration change acknowledgment',
    'error': 'Error message',
    'heartbeat': 'Connection health check'
};
```

### 4.3 Alert Thresholds

```python
# Shared risk alert definitions
ALERT_THRESHOLDS = {
    'var_breach': 0.05,      # 5% daily loss threshold
    'drawdown_breach': 0.15, # 15% maximum drawdown threshold
    'volatility_spike': 0.30 # 30% annualized volatility threshold
}
```

---

## 5. Dependency Relationships

### 5.1 Direct Dependencies

#### Risk Calculator Service Dependencies
```
src/services/risk_analytics/risk_calculator_service.py
├── numpy (VaR calculations, statistical functions)
├── pandas (time series data manipulation)
├── scipy.stats (statistical distributions)
└── typing (type hints)
```

#### Risk WebSocket Server Dependencies
```
src/services/risk_analytics/risk_websocket_server.py
├── src/services/risk_analytics/risk_calculator_service.py (core calculations)
├── websockets (WebSocket server implementation)
├── asyncio (asynchronous operations)
├── json (message serialization)
└── logging (server logging)
```

#### Risk Dashboard Integration Dependencies
```
src/web/static/js/trading-robot/risk-dashboard-integration.js
├── src/web/static/js/trading-robot/app-management-modules.js (trading app integration)
├── WebSocket API (browser WebSocket client)
├── JSON (message parsing)
└── DOM APIs (UI updates)
```

### 5.2 Runtime Dependencies

#### Startup Sequence
1. **Risk Calculator Service** must be initialized first
2. **Risk WebSocket Server** depends on calculator service availability
3. **Risk Dashboard Integration** depends on WebSocket server being online

#### Service Health Checks
```python
# WebSocket server health check
async def check_calculator_health():
    """Verify risk calculator service is responsive."""
    try:
        # Ping calculator service
        health = await risk_calculator.ping()
        return health['status'] == 'healthy'
    except Exception as e:
        logger.error(f"Risk calculator health check failed: {e}")
        return False
```

### 5.3 Deployment Dependencies

#### Docker Compose Dependencies
```yaml
services:
  risk-calculator:
    # Independent service
    depends_on: []

  risk-websocket:
    # Depends on risk calculator
    depends_on:
      - risk-calculator

  trading-dashboard:
    # Depends on risk websocket
    depends_on:
      - risk-websocket
```

---

## 6. Maintenance and Update Patterns

### 6.1 Adding New Risk Metrics

To add a new risk metric (e.g., `omega_ratio`):

#### 1. Update Risk Calculator Service
```python
# Add to risk_calculator_service.py
async def calculate_omega_ratio(self, returns: List[float], threshold: float = 0.0) -> float:
    """Calculate Omega ratio (upside potential vs downside risk)."""
    # Implementation
    pass

# Update calculate_comprehensive_risk_metrics to include omega_ratio
```

#### 2. Update WebSocket Message Schema
```python
# Add to risk_websocket_server.py message schema
'omega_ratio': 'Upside potential vs downside risk ratio'
```

#### 3. Update Dashboard Integration
```javascript
// Add to risk-dashboard-integration.js
this.riskMetrics.omegaRatio = data.omega_ratio;

// Update UI rendering logic
updateOmegaRatioDisplay(this.riskMetrics.omegaRatio);
```

### 6.2 Modifying Alert Thresholds

#### 1. Update Shared Constants
```python
# Update in all three files
ALERT_THRESHOLDS['new_alert_type'] = threshold_value
```

#### 2. Update Alert Logic
```python
# Update in risk_calculator_service.py
def check_alerts(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
    # Add new alert type checking
    pass
```

#### 3. Update Dashboard Alert Handling
```javascript
// Update in risk-dashboard-integration.js
handleAlert(alert) {
    if (alert.type === 'new_alert_type') {
        // Handle new alert type
    }
}
```

### 6.3 Performance Optimization Updates

#### Calculator Service Optimization
- **Caching Layer:** Add Redis caching for frequently requested metrics
- **Batch Processing:** Optimize for bulk calculations
- **Algorithm Selection:** Choose appropriate VaR calculation methods

#### WebSocket Server Optimization
- **Connection Pooling:** Reuse calculator service connections
- **Message Batching:** Group small updates into larger messages
- **Compression:** Enable WebSocket message compression

#### Dashboard Integration Optimization
- **Update Throttling:** Limit UI update frequency
- **Virtual Scrolling:** For large datasets
- **Lazy Loading:** Load risk data on demand

---

## 7. Error Handling and Resilience

### 7.1 Calculator Service Failures

```python
# WebSocket server handles calculator failures
async def handle_calculator_error(self, error: Exception) -> None:
    """Handle risk calculator service failures."""
    logger.error(f"Risk calculator error: {error}")

    # Send error message to all clients
    error_message = {
        'type': 'error',
        'message': 'Risk calculation service temporarily unavailable',
        'retry_in': 30  # seconds
    }

    await self.broadcast_to_clients(error_message)
```

### 7.2 WebSocket Connection Failures

```javascript
// Dashboard handles WebSocket disconnections
handleWebSocketError(error) {
    console.error('WebSocket connection failed:', error);

    // Show offline indicator
    this.showOfflineIndicator();

    // Attempt reconnection with exponential backoff
    this.scheduleReconnection();
}
```

### 7.3 Data Validation Errors

```python
# Shared data validation across all components
def validate_risk_metrics(metrics: Dict[str, Any]) -> bool:
    """Validate risk metrics data structure."""
    required_fields = ['var_95', 'sharpe_ratio', 'max_drawdown']

    for field in required_fields:
        if field not in metrics:
            return False
        if not isinstance(metrics[field], (int, float)):
            return False

    return True
```

---

## 8. Testing Strategy

### 8.1 Unit Testing
- **Risk Calculator:** Test individual metric calculations
- **WebSocket Server:** Test message serialization/deserialization
- **Dashboard Integration:** Test UI update logic

### 8.2 Integration Testing
```python
# Test complete pipeline: Calculator → WebSocket → Dashboard
async def test_risk_pipeline_integration():
    # Start calculator service
    calculator = RiskCalculatorService()
    await calculator.initialize()

    # Start WebSocket server
    server = RiskWebSocketServer(calculator)
    await server.start_server()

    # Simulate dashboard connection
    dashboard = RiskDashboardIntegration()
    await dashboard.connect()

    # Send test data
    test_returns = [0.01, -0.005, 0.02, -0.01]
    await calculator.calculate_comprehensive_risk_metrics(test_returns)

    # Verify data flows through pipeline
    assert dashboard.riskMetrics.var95 is not None
```

### 8.3 Performance Testing
- **Latency:** Calculator response time (<100ms)
- **Throughput:** WebSocket message rate (1000+ msg/sec)
- **Memory Usage:** Dashboard memory consumption (<50MB)

---

## 9. Monitoring and Observability

### 9.1 Health Checks

#### Calculator Service Health
```python
@app.get("/health/risk-calculator")
async def risk_calculator_health():
    """Health check for risk calculator service."""
    return {
        "service": "risk_calculator",
        "status": "healthy",
        "metrics_calculated": 150,
        "uptime_seconds": 3600
    }
```

#### WebSocket Server Health
```python
@app.get("/health/risk-websocket")
async def risk_websocket_health():
    """Health check for WebSocket server."""
    return {
        "service": "risk_websocket",
        "status": "healthy",
        "connected_clients": len(server.clients),
        "messages_sent": server.message_count,
        "uptime_seconds": 3600
    }
```

### 9.2 Metrics Collection

#### Performance Metrics
- **Calculation Latency:** Time to compute risk metrics
- **WebSocket Throughput:** Messages per second
- **Dashboard Update Frequency:** UI refresh rate

#### Business Metrics
- **Active Portfolios:** Number of portfolios being monitored
- **Alert Frequency:** Risk alerts generated per day
- **User Engagement:** Dashboard usage statistics

---

## 10. Future Evolution

### 10.1 Microservices Decomposition

Current: **Monolithic Services**
```
┌─────────────────────────────────────┐
│ Risk Analytics (Single Service)     │
│ ├─ Calculator Logic                 │
│ ├─ WebSocket Server                 │
│ └─ API Endpoints                    │
└─────────────────────────────────────┘
```

Future: **Microservices Architecture**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Risk Calc   │───▶│ Risk API    │───▶│ Risk WS     │
│ Service     │    │ Gateway     │    │ Server      │
└─────────────┘    └─────────────┘    └─────────────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │ Dashboard   │
                               │ Integration │
                               └─────────────┘
```

### 10.2 Enhanced Real-time Features

#### Streaming Analytics
- **Real-time VaR:** Update every trade, not daily
- **Portfolio Stress Testing:** Live scenario analysis
- **Risk Attribution:** Real-time factor contribution analysis

#### Advanced Alerting
- **Predictive Alerts:** ML-based risk prediction
- **Multi-threshold Alerts:** Different severity levels
- **Custom Alert Rules:** User-defined risk thresholds

### 10.3 Multi-asset Support

#### Current: Single Asset Class
- Focused on equity/portfolio risk

#### Future: Multi-asset Classes
- **Crypto Risk:** Volatility-adjusted metrics for cryptocurrencies
- **Options Risk:** Greeks-based risk calculations
- **FX Risk:** Currency-specific risk measures

---

## Conclusion

The risk analytics ecosystem demonstrates a well-architected, tightly-coupled system where the risk calculator, WebSocket server, and dashboard integration form a cohesive real-time risk monitoring pipeline. The documented dependencies and relationships provide a foundation for:

- **Maintenance:** Clear understanding of component interactions
- **Evolution:** Structured approach to adding new features
- **Testing:** Comprehensive test coverage across all components
- **Monitoring:** Health checks and performance metrics
- **Scaling:** Microservices decomposition roadmap

**Status:** ✅ **COMPLETE** - Comprehensive file relationship mapping for risk analytics ecosystem
**Coverage:** 100% of key file dependencies documented
**Navigation:** Full bidirectional relationship mapping
**Maintenance:** Evolution roadmap and testing strategy included