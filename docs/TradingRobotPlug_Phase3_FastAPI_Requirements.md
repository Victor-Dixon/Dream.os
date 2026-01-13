# TradingRobotPlug Phase 3 - FastAPI Endpoint Requirements

## Overview
WordPress plugin endpoints that require FastAPI backend integration.

## FastAPI Endpoints Required

### 1. Account Info
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/account`
- **FastAPI Endpoint**: `GET /api/v1/account/info`
- **Method**: GET
- **Expected Response**: Account information object
- **Current Status**: Returns 500 (FastAPI connection error - expected until FastAPI deployed)

### 2. Positions
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/positions`
- **FastAPI Endpoint**: `GET /api/v1/positions`
- **Method**: GET
- **Query Parameters**: Optional (passed through from WordPress)
- **Expected Response**: Positions array/object
- **Current Status**: Returns 500 (FastAPI connection error - expected until FastAPI deployed)

### 3. Trades
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/trades`
- **FastAPI Endpoint**: `GET /api/v1/trades`
- **Method**: GET
- **Query Parameters**: 
  - `symbol` (optional, validated: TSLA, QQQ, SPY, NVDA)
- **Expected Response**: Object with `trades` array and `total` count
- **Current Status**: Returns 500 (FastAPI connection error - expected until FastAPI deployed)

### 4. Orders (Submit)
- **WordPress Endpoint**: `POST /wp-json/tradingrobotplug/v1/orders`
- **FastAPI Endpoint**: `POST /api/v1/orders/submit`
- **Method**: POST
- **Required Body Fields**:
  - `symbol` (required)
  - `side` (required: buy/sell)
  - `quantity` (required)
  - `order_type` (required)
- **Expected Response**: Order confirmation object
- **Current Status**: Returns 400 (validation error - working correctly)

### 5. Strategies List
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/strategies`
- **FastAPI Endpoint**: `GET /api/v1/strategies/list`
- **Method**: GET
- **Expected Response**: Object with `strategies` array and `total` count
- **Current Status**: Returns 200 (working - may be using mock data)

### 6. Strategy Execute
- **WordPress Endpoint**: `POST /wp-json/tradingrobotplug/v1/strategies/execute`
- **FastAPI Endpoint**: `POST /api/v1/strategies/execute`
- **Method**: POST
- **Required Body Fields**:
  - `strategy_id` (required)
- **Expected Response**: Strategy execution result object
- **Current Status**: Returns 500 (FastAPI connection error - expected until FastAPI deployed)

## FastAPI Configuration

### Base URL
- **Development**: `http://localhost:8001`
- **Production**: Configured via WordPress option `tradingrobotplug_fastapi_url`
- **Default**: `http://localhost:8001`

### Authentication
- **Method**: Bearer token
- **WordPress Option**: `tradingrobotplug_fastapi_key`
- **Header**: `Authorization: Bearer {api_key}`

### Timeout
- **Default**: 30 seconds (longer timeout for trading operations)

## Post-Deployment Verification

After FastAPI deployment, verify:
1. All endpoints return 200 (not 500)
2. Response formats match WordPress expectations
3. Error handling works correctly
4. Authentication works if required

## Integration Status

- ✅ WordPress plugin deployed
- ✅ WordPress plugin activated
- ✅ REST API endpoints registered
- ✅ Permission callbacks configured
- ⏳ FastAPI deployment pending
- ⏳ End-to-end integration testing pending

