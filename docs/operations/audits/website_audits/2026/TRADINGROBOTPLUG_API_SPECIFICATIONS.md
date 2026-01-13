# TradingRobotPlug.com - API Specifications (OpenAPI/Swagger)

**Date**: 2025-12-27  
**Author**: Agent-2 (Architecture & Design Specialist)  
**Related**: `TRADINGROBOTPLUG_PLATFORM_ARCHITECTURE_PLAN.md`, `TRADINGROBOTPLUG_COMPONENT_INTERFACE_SPECIFICATIONS.md`  
**Status**: ✅ COMPLETE - API Specifications Defined

---

## Executive Summary

This document defines the RESTful API specifications for the TradingRobotPlug platform using OpenAPI 3.0 format. These specifications enable consistent API implementation, client integration, and documentation generation.

**API Base Path**: `/wp-json/tradingrobotplug/v1`

**API Version**: `v1`

**Content Type**: `application/json`

---

## OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: TradingRobotPlug API
  description: RESTful API for TradingRobotPlug automated trading tools platform
  version: 1.0.0
  contact:
    name: TradingRobotPlug API Support
    url: https://tradingrobotplug.com/api-docs
servers:
  - url: https://tradingrobotplug.com/wp-json/tradingrobotplug/v1
    description: Production server
  - url: http://localhost/wp-json/tradingrobotplug/v1
    description: Local development server
paths:
  /stock-data:
    get:
      summary: Get all stock data
      description: Retrieve all available stock data entries
      operationId: getAllStockData
      tags:
        - Stock Data
      parameters:
        - name: limit
          in: query
          description: Maximum number of results to return
          required: false
          schema:
            type: integer
            default: 100
            minimum: 1
            maximum: 1000
        - name: offset
          in: query
          description: Number of results to skip
          required: false
          schema:
            type: integer
            default: 0
            minimum: 0
        - name: symbol
          in: query
          description: Filter by trading symbol
          required: false
          schema:
            type: string
            example: TSLA
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/StockData'
                  total:
                    type: integer
                    description: Total number of records
                  limit:
                    type: integer
                  offset:
                    type: integer
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /stock-data/{symbol}:
    get:
      summary: Get stock data by symbol
      description: Retrieve stock data for a specific trading symbol
      operationId: getStockDataBySymbol
      tags:
        - Stock Data
      parameters:
        - name: symbol
          in: path
          required: true
          description: Trading symbol (e.g., TSLA, QQQ, SPY)
          schema:
            type: string
            pattern: '^[A-Z]{1,5}$'
            example: TSLA
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StockData'
        '404':
          $ref: '#/components/responses/NotFound'
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /strategies:
    get:
      summary: List all strategies
      description: Retrieve all trading strategies
      operationId: listStrategies
      tags:
        - Strategies
      parameters:
        - name: status
          in: query
          description: Filter by strategy status
          required: false
          schema:
            type: string
            enum: [active, inactive, paused]
        - name: limit
          in: query
          description: Maximum number of results to return
          required: false
          schema:
            type: integer
            default: 50
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  strategies:
                    type: array
                    items:
                      $ref: '#/components/schemas/Strategy'
                  total:
                    type: integer
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /strategies/{id}:
    get:
      summary: Get strategy by ID
      description: Retrieve details for a specific trading strategy
      operationId: getStrategyById
      tags:
        - Strategies
      parameters:
        - name: id
          in: path
          required: true
          description: Strategy identifier
          schema:
            type: string
            example: strategy_001
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Strategy'
        '404':
          $ref: '#/components/responses/NotFound'
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /trades:
    get:
      summary: Get trade history
      description: Retrieve trade history with optional filtering
      operationId: getTradeHistory
      tags:
        - Trades
      parameters:
        - name: symbol
          in: query
          description: Filter by trading symbol
          required: false
          schema:
            type: string
            example: TSLA
        - name: strategy_id
          in: query
          description: Filter by strategy ID
          required: false
          schema:
            type: string
            example: strategy_001
        - name: start_date
          in: query
          description: Start date for filtering (ISO 8601 format)
          required: false
          schema:
            type: string
            format: date-time
            example: '2025-12-01T00:00:00Z'
        - name: end_date
          in: query
          description: End date for filtering (ISO 8601 format)
          required: false
          schema:
            type: string
            format: date-time
            example: '2025-12-27T23:59:59Z'
        - name: limit
          in: query
          description: Maximum number of results to return
          required: false
          schema:
            type: integer
            default: 50
            minimum: 1
            maximum: 100
        - name: offset
          in: query
          description: Number of results to skip
          required: false
          schema:
            type: integer
            default: 0
            minimum: 0
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  trades:
                    type: array
                    items:
                      $ref: '#/components/schemas/Trade'
                  total:
                    type: integer
                  limit:
                    type: integer
                  offset:
                    type: integer
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /trades/{id}:
    get:
      summary: Get trade by ID
      description: Retrieve details for a specific trade
      operationId: getTradeById
      tags:
        - Trades
      parameters:
        - name: id
          in: path
          required: true
          description: Trade identifier
          schema:
            type: string
            example: trade_001
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Trade'
        '404':
          $ref: '#/components/responses/NotFound'
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /performance:
    get:
      summary: Get performance metrics
      description: Retrieve overall performance metrics
      operationId: getPerformanceMetrics
      tags:
        - Performance
      parameters:
        - name: period
          in: query
          description: Time period for performance metrics
          required: false
          schema:
            type: string
            enum: [1d, 7d, 30d, 90d, 1y, all]
            default: 30d
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PerformanceMetrics'
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'
  
  /performance/{strategy_id}:
    get:
      summary: Get strategy performance metrics
      description: Retrieve performance metrics for a specific strategy
      operationId: getStrategyPerformance
      tags:
        - Performance
      parameters:
        - name: strategy_id
          in: path
          required: true
          description: Strategy identifier
          schema:
            type: string
            example: strategy_001
        - name: period
          in: query
          description: Time period for performance metrics
          required: false
          schema:
            type: string
            enum: [1d, 7d, 30d, 90d, 1y, all]
            default: 30d
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PerformanceMetrics'
        '404':
          $ref: '#/components/responses/NotFound'
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalServerError'

components:
  schemas:
    StockData:
      type: object
      required:
        - symbol
        - price
        - timestamp
      properties:
        symbol:
          type: string
          description: Trading symbol
          example: TSLA
        price:
          type: number
          format: float
          description: Current price
          example: 250.50
        timestamp:
          type: string
          format: date-time
          description: Data timestamp
          example: '2025-12-27T12:00:00Z'
        volume:
          type: integer
          description: Trading volume
          example: 1000000
        open:
          type: number
          format: float
          description: Opening price
          example: 248.00
        high:
          type: number
          format: float
          description: Daily high price
          example: 252.00
        low:
          type: number
          format: float
          description: Daily low price
          example: 247.50
        close:
          type: number
          format: float
          description: Closing price
          example: 250.50
    
    Strategy:
      type: object
      required:
        - id
        - name
        - status
      properties:
        id:
          type: string
          description: Unique strategy identifier
          example: strategy_001
        name:
          type: string
          description: Strategy name
          example: Moving Average Crossover
        description:
          type: string
          description: Strategy description
          example: Simple moving average crossover strategy
        status:
          type: string
          enum: [active, inactive, paused]
          description: Strategy status
          example: active
        version:
          type: string
          description: Strategy version
          example: '1.0.0'
        config:
          type: object
          description: Strategy configuration
          additionalProperties: true
        performance:
          $ref: '#/components/schemas/PerformanceMetrics'
        created_at:
          type: string
          format: date-time
          description: Creation timestamp
          example: '2025-12-01T00:00:00Z'
        updated_at:
          type: string
          format: date-time
          description: Last update timestamp
          example: '2025-12-27T12:00:00Z'
    
    Trade:
      type: object
      required:
        - trade_id
        - symbol
        - price
        - quantity
        - timestamp
      properties:
        trade_id:
          type: string
          description: Unique trade identifier
          example: trade_001
        symbol:
          type: string
          description: Trading symbol
          example: TSLA
        price:
          type: number
          format: float
          description: Execution price
          example: 250.50
        quantity:
          type: integer
          description: Trade quantity
          example: 100
        order_type:
          type: string
          enum: [buy, sell]
          description: Order type
          example: buy
        timestamp:
          type: string
          format: date-time
          description: Execution timestamp
          example: '2025-12-27T12:00:00Z'
        strategy_id:
          type: string
          description: Strategy identifier
          example: strategy_001
        status:
          type: string
          enum: [open, closed, cancelled]
          description: Trade status
          example: closed
        fill_price:
          type: number
          format: float
          description: Actual fill price
          example: 250.50
        slippage:
          type: number
          format: float
          description: Slippage amount
          example: 0.10
        pnl:
          type: number
          format: float
          description: Profit/loss
          example: 50.00
    
    PerformanceMetrics:
      type: object
      required:
        - strategy_id
        - period
      properties:
        strategy_id:
          type: string
          description: Strategy identifier (null for overall metrics)
          nullable: true
          example: strategy_001
        period:
          type: string
          description: Time period
          example: 30d
        win_rate:
          type: number
          format: float
          description: Win rate (0.0-1.0)
          example: 0.65
        total_trades:
          type: integer
          description: Total number of trades
          example: 100
        total_return:
          type: number
          format: float
          description: Total return percentage
          example: 15.5
        sharpe_ratio:
          type: number
          format: float
          description: Sharpe ratio
          example: 1.2
        max_drawdown:
          type: number
          format: float
          description: Maximum drawdown percentage
          example: 5.0
        avg_trade_return:
          type: number
          format: float
          description: Average trade return
          example: 0.15
        profit_factor:
          type: number
          format: float
          description: Profit factor
          example: 1.5
        period_start:
          type: string
          format: date-time
          description: Period start timestamp
          example: '2025-11-27T00:00:00Z'
        period_end:
          type: string
          format: date-time
          description: Period end timestamp
          example: '2025-12-27T23:59:59Z'
    
    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
              description: Error code
              example: INVALID_SYMBOL
            message:
              type: string
              description: Human-readable error message
              example: Invalid trading symbol provided
            details:
              type: object
              description: Additional error details
              additionalProperties: true
            timestamp:
              type: string
              format: date-time
              description: Error timestamp
              example: '2025-12-27T12:00:00Z'
  
  responses:
    BadRequest:
      description: Bad request - Invalid parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: INVALID_PARAMETER
              message: Invalid parameter provided
              timestamp: '2025-12-27T12:00:00Z'
    
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: NOT_FOUND
              message: Resource not found
              timestamp: '2025-12-27T12:00:00Z'
    
    InternalServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: INTERNAL_ERROR
              message: An internal error occurred
              timestamp: '2025-12-27T12:00:00Z'
  
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for authentication
security:
  - ApiKeyAuth: []

tags:
  - name: Stock Data
    description: Stock market data endpoints
  - name: Strategies
    description: Trading strategy endpoints
  - name: Trades
    description: Trade history endpoints
  - name: Performance
    description: Performance metrics endpoints
```

---

## API Endpoint Summary

### Stock Data Endpoints

- `GET /stock-data` - Get all stock data (with pagination and filtering)
- `GET /stock-data/{symbol}` - Get stock data for specific symbol

### Strategy Endpoints

- `GET /strategies` - List all strategies (with status filtering)
- `GET /strategies/{id}` - Get strategy by ID

### Trade Endpoints

- `GET /trades` - Get trade history (with filtering by symbol, strategy, date range)
- `GET /trades/{id}` - Get trade by ID

### Performance Endpoints

- `GET /performance` - Get overall performance metrics
- `GET /performance/{strategy_id}` - Get strategy-specific performance metrics

---

## Data Models

### StockData

Represents stock market data for a trading symbol.

**Fields**:
- `symbol` (string, required) - Trading symbol
- `price` (float, required) - Current price
- `timestamp` (datetime, required) - Data timestamp
- `volume` (integer) - Trading volume
- `open` (float) - Opening price
- `high` (float) - Daily high price
- `low` (float) - Daily low price
- `close` (float) - Closing price

### Strategy

Represents a trading strategy.

**Fields**:
- `id` (string, required) - Unique strategy identifier
- `name` (string, required) - Strategy name
- `description` (string) - Strategy description
- `status` (enum, required) - Strategy status (active, inactive, paused)
- `version` (string) - Strategy version
- `config` (object) - Strategy configuration
- `performance` (PerformanceMetrics) - Performance metrics
- `created_at` (datetime) - Creation timestamp
- `updated_at` (datetime) - Last update timestamp

### Trade

Represents a trade execution.

**Fields**:
- `trade_id` (string, required) - Unique trade identifier
- `symbol` (string, required) - Trading symbol
- `price` (float, required) - Execution price
- `quantity` (integer, required) - Trade quantity
- `order_type` (enum, required) - Order type (buy, sell)
- `timestamp` (datetime, required) - Execution timestamp
- `strategy_id` (string) - Strategy identifier
- `status` (enum) - Trade status (open, closed, cancelled)
- `fill_price` (float) - Actual fill price
- `slippage` (float) - Slippage amount
- `pnl` (float) - Profit/loss

### PerformanceMetrics

Represents performance metrics for a strategy or overall system.

**Fields**:
- `strategy_id` (string, nullable) - Strategy identifier (null for overall metrics)
- `period` (string, required) - Time period (1d, 7d, 30d, 90d, 1y, all)
- `win_rate` (float) - Win rate (0.0-1.0)
- `total_trades` (integer) - Total number of trades
- `total_return` (float) - Total return percentage
- `sharpe_ratio` (float) - Sharpe ratio
- `max_drawdown` (float) - Maximum drawdown percentage
- `avg_trade_return` (float) - Average trade return
- `profit_factor` (float) - Profit factor
- `period_start` (datetime) - Period start timestamp
- `period_end` (datetime) - Period end timestamp

---

## Error Handling

All endpoints return standard error responses:

- `400 Bad Request` - Invalid parameters or request format
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server-side error

Error response format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {},
    "timestamp": "2025-12-27T12:00:00Z"
  }
}
```

---

## Authentication

API uses API key authentication via header:

```
X-API-Key: your-api-key-here
```

---

## Rate Limiting

- **Rate Limit**: 100 requests per minute per API key
- **Rate Limit Header**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Pagination

Endpoints that return lists support pagination:

- `limit` - Maximum number of results (default: varies by endpoint)
- `offset` - Number of results to skip (default: 0)

Response includes:
- `total` - Total number of records
- `limit` - Current limit
- `offset` - Current offset

---

## Filtering

Endpoints support filtering via query parameters:

- **Stock Data**: `symbol`
- **Strategies**: `status`
- **Trades**: `symbol`, `strategy_id`, `start_date`, `end_date`
- **Performance**: `period`

---

## Implementation Notes

1. **WordPress REST API**: Endpoints should be registered using WordPress REST API registration
2. **Data Validation**: All input parameters should be validated before processing
3. **Error Handling**: Consistent error response format across all endpoints
4. **Performance**: Consider caching for frequently accessed data
5. **Security**: API key authentication required for all endpoints
6. **Documentation**: OpenAPI spec can be used to generate interactive API documentation

---

## Approval Status

**Status**: ✅ **COMPLETE**

**Architecture Compliance**: ✅ **COMPLIANT**

**Ready for Implementation**: ✅ **YES**

---

**Specifications Complete**: 2025-12-27  
**Author**: Agent-2 (Architecture & Design Specialist)  
**Next Action**: Agent-7 implements API endpoints per specifications

