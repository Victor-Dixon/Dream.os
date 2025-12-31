# TradingRobotPlug Phase 3 - Post-FastAPI Deployment Verification Plan

## Overview
Verification checklist for WordPress REST API endpoints after FastAPI deployment.

## Pre-Deployment Status (Verified ✅)
- ✅ Plugin deployed (18 files via SFTP)
- ✅ Plugin activated via WP-CLI
- ✅ All endpoints registered and accessible
- ✅ No 404 errors
- ✅ Test results: 5 passed, 2 skipped (account/positions - FastAPI connection needed)

## Post-Deployment Verification Checklist

### 1. Account Endpoint
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/account`
- **FastAPI Endpoint**: `GET /api/v1/account/info`
- **Expected**: 200 OK with account information object
- **Current**: 500 (FastAPI connection error - expected until deployed)
- **Verification**: 
  - [ ] Returns 200 (not 500)
  - [ ] Response contains account information
  - [ ] Response format matches WordPress expectations

### 2. Positions Endpoint
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/positions`
- **FastAPI Endpoint**: `GET /api/v1/positions`
- **Expected**: 200 OK with positions array/object
- **Current**: 500 (FastAPI connection error - expected until deployed)
- **Verification**:
  - [ ] Returns 200 (not 500)
  - [ ] Response contains positions data
  - [ ] Response format matches WordPress expectations

### 3. Trades Endpoint
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/trades`
- **FastAPI Endpoint**: `GET /api/v1/trades`
- **Expected**: 200 OK with trades array and total count
- **Current**: 500 (FastAPI connection error - expected until deployed)
- **Verification**:
  - [ ] Returns 200 (not 500)
  - [ ] Response contains trades array
  - [ ] Symbol filter works correctly
  - [ ] Response format: `{trades: [], total: N}`

### 4. Orders Endpoint
- **WordPress Endpoint**: `POST /wp-json/tradingrobotplug/v1/orders`
- **FastAPI Endpoint**: `POST /api/v1/orders/submit`
- **Expected**: 200 OK with order confirmation
- **Current**: 400 (validation error - working correctly)
- **Verification**:
  - [ ] Returns 200 with valid order data (not 400)
  - [ ] Returns 400 with invalid/missing fields (validation working)
  - [ ] Response contains order confirmation

### 5. Strategies List Endpoint
- **WordPress Endpoint**: `GET /wp-json/tradingrobotplug/v1/strategies`
- **FastAPI Endpoint**: `GET /api/v1/strategies/list`
- **Expected**: 200 OK with strategies array
- **Current**: 200 (working - may be using mock data)
- **Verification**:
  - [ ] Returns 200
  - [ ] Response contains strategies array
  - [ ] Response format: `{strategies: [], total: N}`

### 6. Strategy Execute Endpoint
- **WordPress Endpoint**: `POST /wp-json/tradingrobotplug/v1/strategies/execute`
- **FastAPI Endpoint**: `POST /api/v1/strategies/execute`
- **Expected**: 200 OK with execution result
- **Current**: 500 (FastAPI connection error - expected until deployed)
- **Verification**:
  - [ ] Returns 200 with valid strategy_id (not 500)
  - [ ] Returns 400 with missing strategy_id (validation working)
  - [ ] Response contains execution result

## FastAPI Configuration Verification

### Base URL
- **WordPress Option**: `tradingrobotplug_fastapi_url`
- **Default**: `http://localhost:8001`
- **Production**: Configure via WordPress admin or WP-CLI
- **Verification**: FastAPI accessible at configured URL

### Authentication
- **WordPress Option**: `tradingrobotplug_fastapi_key`
- **Method**: Bearer token in Authorization header
- **Verification**: Authentication working if required

## Verification Commands

### Test All Endpoints
```bash
# Account
curl https://tradingrobotplug.com/wp-json/tradingrobotplug/v1/account

# Positions
curl https://tradingrobotplug.com/wp-json/tradingrobotplug/v1/positions

# Trades
curl https://tradingrobotplug.com/wp-json/tradingrobotplug/v1/trades

# Strategies
curl https://tradingrobotplug.com/wp-json/tradingrobotplug/v1/strategies

# Orders (POST with body)
curl -X POST https://tradingrobotplug.com/wp-json/tradingrobotplug/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"symbol":"TSLA","side":"buy","quantity":10,"order_type":"market"}'
```

## Success Criteria

- ✅ All endpoints return 200 (not 500)
- ✅ Response formats match WordPress expectations
- ✅ Error handling works correctly (400 for validation, 500 for server errors)
- ✅ FastAPI connection established
- ✅ Authentication working if required

## Integration Status

- ✅ WordPress plugin deployed
- ✅ WordPress plugin activated
- ✅ REST API endpoints registered
- ✅ Pre-deployment testing complete (5 passed, 2 skipped)
- ⏳ FastAPI deployment pending
- ⏳ Post-deployment verification pending
- ⏳ End-to-end integration testing pending


