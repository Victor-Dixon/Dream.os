# File Relationship Mapping: Risk Calculator ↔ WebSocket ↔ Dashboard

**Author:** Agent-5 (Business Intelligence Specialist)
**Created:** 2026-01-07
**Purpose:** Comprehensive dependency mapping for risk analytics ecosystem

---

## Executive Summary

This document maps the critical file relationships in the risk analytics ecosystem, showing how the **Risk Calculator**, **WebSocket Server**, and **Dashboard Components** interconnect to deliver real-time risk metrics to trading applications.

### Key Dependency Flow
```
Risk Calculator Service → WebSocket Server → Dashboard Integration → Dashboard UI
       ↓                        ↓                        ↓
   Calculates Metrics     Streams Live Data       Consumes & Displays
```

---

## 1. Risk Calculator Service (`src/services/risk_analytics/risk_calculator_service.py`)

### Primary Function
Core risk calculation engine implementing advanced financial risk metrics.

### Key Dependencies & Relationships

#### **Outbound Dependencies** (What this service uses)
```python
# No external service dependencies - standalone calculation engine
# Uses numpy, pandas for computations
# Uses internal data structures only
```

#### **Inbound Dependencies** (What uses this service)
```python
# WebSocket Server Integration
├── src/services/risk_analytics/risk_websocket_server.py
│   └── Line 64: from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService, RiskMetrics
│   └── Line 90: self.risk_calculator = RiskCalculatorService()
│   └── Line 163-193: Uses RiskCalculatorService for metric calculations

# API Endpoints
├── src/services/risk_analytics/risk_api_endpoints.py
│   └── REST API endpoints for risk calculations
│   └── Exposes RiskCalculatorService methods via HTTP

# Testing & Validation
├── tests/unit/services/test_risk_*.py
│   └── Unit tests for risk calculation algorithms
│   └── Validates calculation accuracy
```

#### **Data Flow Relationships**
```
Input: Trading returns, equity curves, benchmark data
↓
Processing: VaR, CVaR, Sharpe, Sortino, Calmar, Information ratios
↓
Output: RiskMetrics dataclass with comprehensive risk analysis
↓
Consumption: WebSocket server for real-time streaming
```

---

## 2. WebSocket Server (`src/services/risk_analytics/risk_websocket_server.py`)

### Primary Function
Real-time streaming server for risk metrics with <100ms latency.

### Key Dependencies & Relationships

#### **Outbound Dependencies** (What this server uses)
```python
# Risk Calculator Service
├── src/services/risk_analytics/risk_calculator_service.py
│   └── Line 64: import RiskCalculatorService, RiskMetrics
│   └── Line 90: self.risk_calculator = RiskCalculatorService()
│   └── Methods: _generate_live_risk_data(), _generate_dashboard_data()

# WebSocket Infrastructure
├── websockets (external library)
│   └── Async WebSocket server implementation
│   └── Connection management and messaging

# AsyncIO Infrastructure
├── asyncio (standard library)
│   └── Event loop management
│   └── Concurrent connection handling
```

#### **Inbound Dependencies** (What connects to this server)
```python
# Dashboard Integration (JavaScript)
├── src/web/static/js/trading-robot/risk-dashboard-integration.js
│   └── Line 54: this.wsUrl = 'ws://localhost:8765/ws/risk/live'
│   └── WebSocket client connection and message handling

# Trading Dashboard
├── src/web/static/js/trading-robot/trading-dashboard.js
│   └── Consumes risk data via RiskDashboardIntegration
│   └── Displays real-time risk metrics in UI

# Dashboard UI Components
├── src/web/static/js/dashboard.js
│   └── Main dashboard integration point
│   └── Routes risk data to appropriate UI components

# Alert System
├── src/web/static/js/trading-robot/risk-alerts.js
│   └── Consumes alert stream from /ws/risk/alerts endpoint
│   └── Displays risk threshold violations
```

#### **Connection Endpoints**
```
/ws/risk/live     → Live risk metrics (1Hz updates)
/ws/risk/dashboard → Enhanced dashboard data with charts
/ws/risk/alerts   → Real-time risk alerts and notifications
```

---

## 3. Dashboard Integration (`src/web/static/js/trading-robot/risk-dashboard-integration.js`)

### Primary Function
JavaScript client for consuming WebSocket risk data and integrating with trading dashboard.

### Key Dependencies & Relationships

#### **Outbound Dependencies** (What this integration uses)
```javascript
// WebSocket Server
├── ws://localhost:8765/ws/risk/live
│   └── Real-time risk metrics streaming
│   └── Heartbeat and connection management

// Trading Robot Modules
├── src/web/static/js/trading-robot/app-management-modules.js
│   └── Line 36: import { AppManagementModules }
│   └── Integration with main trading application
```

#### **Inbound Dependencies** (What uses this integration)
```javascript
// Trading Dashboard Main
├── src/web/static/js/trading-robot/trading-dashboard.js
│   └── Primary consumer of risk metrics
│   └── Displays VaR, Sharpe, drawdown in trading interface

// Dashboard State Manager
├── src/web/static/js/dashboard-state-manager.js
│   └── Global state management for dashboard data
│   └── Risk metrics integration point

// Risk Alerts System
├── src/web/static/js/trading-robot/risk-alerts.js
│   └── Consumes alert data from integration
│   └── Displays threshold violation notifications

// Chart Components
├── src/web/static/js/trading-robot/risk-charts.js
│   └── Visualizes risk metrics (VaR trends, Sharpe history)
│   └── Real-time chart updates from WebSocket data
```

#### **Subscriber Pattern Implementation**
```javascript
// Publisher-Subscriber pattern for risk updates
const unsubscribe = riskDashboardIntegration.subscribe((update) => {
    // Handle risk metrics updates
    // Update UI components
    // Trigger alerts
});
```

---

## 4. Cross-Component Data Flow Architecture

### Real-Time Risk Pipeline
```
1. Risk Calculator Service
   ├── Calculates metrics from trading data
   ├── Generates RiskMetrics objects
   └── Passes to WebSocket server

2. WebSocket Server
   ├── Receives RiskMetrics from calculator
   ├── Formats for real-time streaming
   ├── Maintains persistent connections
   └── Streams to dashboard clients

3. Dashboard Integration
   ├── Connects to WebSocket endpoints
   ├── Parses incoming risk data
   ├── Manages connection lifecycle
   └── Publishes to dashboard components

4. Dashboard UI Components
   ├── Subscribe to risk updates
   ├── Render real-time metrics
   ├── Display alerts and warnings
   └── Update charts and indicators
```

### Error Handling Chain
```
Calculator Errors → WebSocket Logging → Dashboard Error Display
Timeout Issues → Reconnection Logic → Fallback UI States
Data Validation → Alert Generation → User Notifications
```

---

## 5. Configuration and Constants

### Risk Thresholds (Shared Across Components)
```python
# Defined in risk_calculator_service.py
DEFAULT_THRESHOLDS = {
    'var_95': 0.20,        # 20% VaR threshold
    'max_drawdown': 0.10,  # 10% drawdown threshold
    'sharpe_ratio_min': 1.0  # Minimum Sharpe ratio
}

# Used in risk_websocket_server.py for alert generation
# Used in risk-dashboard-integration.js for client-side alerts
```

### WebSocket Configuration
```python
# Server configuration (risk_websocket_server.py)
WEBSOCKET_CONFIG = {
    'host': 'localhost',
    'port': 8765,
    'heartbeat_interval': 30,
    'update_interval': 1.0,  # 1Hz updates
    'max_reconnect_attempts': 5
}

# Client configuration (risk-dashboard-integration.js)
WEBSOCKET_CLIENT_CONFIG = {
    'url': 'ws://localhost:8765/ws/risk/live',
    'reconnect_delay': 3000,
    'connection_timeout': 10000
}
```

---

## 6. Testing and Validation Relationships

### Unit Testing Structure
```
tests/unit/services/
├── test_risk_calculator_service.py
│   └── Tests calculation algorithms
│   └── Validates mathematical accuracy
│
tests/unit/services/
├── test_risk_websocket_server.py
│   └── Tests WebSocket server functionality
│   └── Validates connection handling
│
tests/integration/
├── test_risk_analytics_integration.py
│   └── Tests calculator ↔ WebSocket integration
│   └── Validates end-to-end data flow
```

### Integration Testing
```
tests/integration/
├── test_risk_dashboard_integration.py
│   └── Tests WebSocket ↔ Dashboard communication
│   └── Validates real-time data updates
│
tests/e2e/
├── test_risk_analytics_e2e.py
│   └── Full end-to-end testing
│   └── Calculator → WebSocket → Dashboard → UI
```

---

## 7. Performance and Scalability Relationships

### Latency Requirements
```
Risk Calculator: <10ms calculation time
WebSocket Server: <100ms end-to-end latency
Dashboard Integration: <50ms UI update time
Total Pipeline: <200ms from calculation to display
```

### Connection Management
```
WebSocket Server:
├── Heartbeat every 30 seconds
├── Ping/pong for connection health
├── Automatic cleanup of dead connections
├── Connection pooling for scalability

Dashboard Integration:
├── Automatic reconnection on failure
├── Exponential backoff strategy
├── Connection state management
├── Graceful degradation on disconnect
```

---

## 8. Deployment and Configuration Dependencies

### Environment Variables
```bash
# Risk Calculator Configuration
RISK_FREE_RATE=0.045
RISK_CALCULATION_TIMEOUT=5000

# WebSocket Server Configuration
WEBSOCKET_HOST=localhost
WEBSOCKET_PORT=8765
WEBSOCKET_MAX_CONNECTIONS=1000

# Dashboard Configuration
DASHBOARD_UPDATE_INTERVAL=1000
DASHBOARD_RISK_THRESHOLDS_ENABLED=true
```

### Database Schema Dependencies
```sql
-- Risk analytics database tables
CREATE TABLE risk_metrics (
    id SERIAL PRIMARY KEY,
    portfolio_id VARCHAR(255),
    calculation_date TIMESTAMP,
    var_95 DECIMAL,
    sharpe_ratio DECIMAL,
    max_drawdown DECIMAL
);

-- Required for historical risk calculations
CREATE TABLE trading_returns (
    id SERIAL PRIMARY KEY,
    portfolio_id VARCHAR(255),
    date DATE,
    return_value DECIMAL
);
```

---

## 9. Monitoring and Observability

### Metrics Collection Points
```
Risk Calculator Service:
├── Calculation latency
├── Algorithm accuracy validation
├── Memory usage during computations

WebSocket Server:
├── Active connections count
├── Message throughput (messages/second)
├── Connection success/failure rates
├── Latency percentiles

Dashboard Integration:
├── Connection uptime percentage
├── Message processing latency
├── UI update frequency
├── Error rates and recovery time
```

### Logging Integration
```
All components use structured logging:
├── Risk calculator: Calculation events and errors
├── WebSocket server: Connection lifecycle and message flow
├── Dashboard: User interactions and data updates
├── Unified logging system for correlation
```

---

## 10. Future Enhancement Dependencies

### Planned Integrations
```
Risk Calculator Enhancements:
├── Machine learning risk models
├── Alternative risk measures (ES, EVT)
├── Multi-asset portfolio risk
├── Stress testing scenarios

WebSocket Server Enhancements:
├── Binary message protocol for performance
├── Message compression
├── Authentication and authorization
├── Load balancing support

Dashboard Integration Enhancements:
├── Advanced charting libraries
├── Risk scenario modeling
├── Historical comparison tools
├── Alert customization and routing
```

---

## Navigation Index

### Related Documentation
- [Module Discovery Reference Guide](./MODULE_DISCOVERY_REFERENCE_GUIDE.md)
- [Risk Analytics Architecture](../analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md)
- [WebSocket Architecture Review](../analytics/AGENT2_WEBSOCKET_ARCHITECTURE_REVIEW.md)
- [Risk Dashboard Implementation](../analytics/risk_dashboard.html)

### Code Navigation
- **Risk Calculator**: `src/services/risk_analytics/risk_calculator_service.py`
- **WebSocket Server**: `src/services/risk_analytics/risk_websocket_server.py`
- **Dashboard Integration**: `src/web/static/js/trading-robot/risk-dashboard-integration.js`
- **Trading Dashboard**: `src/web/static/js/trading-robot/trading-dashboard.js`

### Testing Navigation
- **Unit Tests**: `tests/unit/services/test_risk_*.py`
- **Integration Tests**: `tests/integration/test_risk_analytics_integration.py`
- **E2E Tests**: `tests/e2e/test_risk_analytics_e2e.py`

---

**Note:** This mapping document should be updated whenever file relationships change or new components are added to the risk analytics ecosystem.