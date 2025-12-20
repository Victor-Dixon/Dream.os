# Trading Robot Plug Backend API - Endpoint Design & Authentication Flow

**Date:** 2025-12-19  
**Agents:** Agent-1 (Integration Review) + Agent-7 (Web Development) + Agent-2 (Architecture)  
**Status:** 🔄 **API DESIGN COORDINATION ACTIVE**  
**Purpose:** Define API contract for WordPress plugin integration with backend API

---

## 🎯 Objective

Design comprehensive backend API endpoints and authentication flow for Trading Robot Plug WordPress plugin integration:
- User management API endpoints
- Performance tracking API endpoints
- Subscription management API endpoints
- Authentication flow (JWT-based)
- API contract specification

---

## 🔐 Authentication Flow

### **Authentication Architecture**

**Method:** JWT (JSON Web Tokens)  
**Flow Type:** OAuth 2.0 Resource Owner Password Credentials (simplified for WordPress plugin)

### **Authentication Endpoints**

#### **1. User Registration**
```
POST /api/v1/auth/register
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "subscription_tier": "free"  // Optional, defaults to "free"
}

Response (201 Created):
{
  "user_id": 123,
  "email": "user@example.com",
  "username": "username",
  "subscription_tier": "free",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### **2. User Login**
```
POST /api/v1/auth/login
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",  // or "username": "username"
  "password": "secure_password"
}

Response (200 OK):
{
  "user_id": 123,
  "email": "user@example.com",
  "username": "username",
  "subscription_tier": "mid",
  "subscription_status": "active",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### **3. Token Refresh**
```
POST /api/v1/auth/refresh
Content-Type: application/json
Authorization: Bearer {refresh_token}

Request Body:
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### **4. Token Validation**
```
GET /api/v1/auth/validate
Authorization: Bearer {access_token}

Response (200 OK):
{
  "valid": true,
  "user_id": 123,
  "expires_at": "2025-12-19T17:30:00Z"
}

Response (401 Unauthorized):
{
  "valid": false,
  "error": "Token expired or invalid"
}
```

#### **5. User Logout**
```
POST /api/v1/auth/logout
Authorization: Bearer {access_token}

Response (200 OK):
{
  "message": "Successfully logged out"
}
```

---

## 👤 User Management API Endpoints

### **User Profile Endpoints**

#### **1. Get User Profile**
```
GET /api/v1/users/{user_id}
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "email": "user@example.com",
  "username": "username",
  "subscription_tier": "mid",
  "subscription_status": "active",
  "subscription_start_date": "2025-11-01",
  "subscription_end_date": "2025-12-01",
  "created_at": "2025-10-15T10:00:00Z",
  "updated_at": "2025-12-19T15:30:00Z"
}
```

#### **2. Update User Profile**
```
PUT /api/v1/users/{user_id}
Authorization: Bearer {access_token}
Content-Type: application/json

Request Body:
{
  "username": "new_username",  // Optional
  "email": "new_email@example.com"  // Optional
}

Response (200 OK):
{
  "user_id": 123,
  "email": "new_email@example.com",
  "username": "new_username",
  "updated_at": "2025-12-19T15:35:00Z"
}
```

#### **3. Change Password**
```
POST /api/v1/users/{user_id}/change-password
Authorization: Bearer {access_token}
Content-Type: application/json

Request Body:
{
  "current_password": "old_password",
  "new_password": "new_secure_password"
}

Response (200 OK):
{
  "message": "Password changed successfully"
}
```

---

## 📊 Performance Tracking API Endpoints

### **Performance Metrics Endpoints**

#### **1. Get User Performance (Daily)**
```
GET /api/v1/performance/{user_id}/daily?date=2025-12-19
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "period": "daily",
  "date": "2025-12-19",
  "metrics": {
    "trade_count": 5,
    "win_count": 3,
    "loss_count": 2,
    "win_rate": 60.0,
    "total_pnl": 125.50,
    "profit_factor": 1.85,
    "sharpe_ratio": 1.42,
    "max_drawdown": -2.5,
    "avg_trade_size": 500.00,
    "best_trade_pnl": 75.00,
    "worst_trade_pnl": -25.00
  },
  "updated_at": "2025-12-19T16:30:00Z"
}
```

#### **2. Get User Performance (Weekly)**
```
GET /api/v1/performance/{user_id}/weekly?week=2025-W50
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "period": "weekly",
  "week": "2025-W50",
  "metrics": {
    "trade_count": 25,
    "win_count": 15,
    "loss_count": 10,
    "win_rate": 60.0,
    "total_pnl": 625.50,
    "profit_factor": 1.85,
    "sharpe_ratio": 1.42,
    "max_drawdown": -5.0,
    "avg_trade_size": 500.00,
    "best_trade_pnl": 150.00,
    "worst_trade_pnl": -50.00
  },
  "updated_at": "2025-12-19T16:30:00Z"
}
```

#### **3. Get User Performance (Monthly)**
```
GET /api/v1/performance/{user_id}/monthly?month=2025-12
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "period": "monthly",
  "month": "2025-12",
  "metrics": {
    "trade_count": 100,
    "win_count": 60,
    "loss_count": 40,
    "win_rate": 60.0,
    "total_pnl": 2500.50,
    "profit_factor": 1.85,
    "sharpe_ratio": 1.42,
    "max_drawdown": -10.0,
    "avg_trade_size": 500.00,
    "best_trade_pnl": 300.00,
    "worst_trade_pnl": -100.00
  },
  "updated_at": "2025-12-19T16:30:00Z"
}
```

#### **4. Get User Performance (All-Time)**
```
GET /api/v1/performance/{user_id}/all-time
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "period": "all-time",
  "metrics": {
    "trade_count": 500,
    "win_count": 300,
    "loss_count": 200,
    "win_rate": 60.0,
    "total_pnl": 12500.50,
    "profit_factor": 1.85,
    "sharpe_ratio": 1.42,
    "max_drawdown": -15.0,
    "avg_trade_size": 500.00,
    "best_trade_pnl": 500.00,
    "worst_trade_pnl": -200.00
  },
  "updated_at": "2025-12-19T16:30:00Z"
}
```

#### **5. Get Plugin-Specific Performance**
```
GET /api/v1/performance/{user_id}/plugin/{plugin_id}/daily?date=2025-12-19
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "plugin_id": "tsla_improved_strategy",
  "period": "daily",
  "date": "2025-12-19",
  "metrics": {
    "trade_count": 3,
    "win_count": 2,
    "loss_count": 1,
    "win_rate": 66.67,
    "total_pnl": 75.50,
    "profit_factor": 2.0,
    "sharpe_ratio": 1.5,
    "max_drawdown": -1.5,
    "avg_trade_size": 500.00,
    "best_trade_pnl": 50.00,
    "worst_trade_pnl": -15.00
  },
  "updated_at": "2025-12-19T16:30:00Z"
}
```

#### **6. Get Public Leaderboard**
```
GET /api/v1/performance/public/leaderboard?period=all-time&limit=100
Authorization: Bearer {access_token}  // Optional for public endpoint

Response (200 OK):
{
  "period": "all-time",
  "leaderboard": [
    {
      "rank": 1,
      "user_id": null,  // Anonymized
      "username": "user_****",  // Anonymized
      "total_pnl": 50000.00,
      "win_rate": 65.0,
      "trade_count": 1000,
      "profit_factor": 2.0
    },
    // ... more entries
  ],
  "updated_at": "2025-12-19T16:30:00Z"
}
```

---

## 💳 Subscription Management API Endpoints

### **Subscription Endpoints**

#### **1. Get User Subscription**
```
GET /api/v1/subscriptions/{user_id}
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "subscription_tier": "mid",
  "subscription_status": "active",
  "subscription_start_date": "2025-11-01",
  "subscription_end_date": "2025-12-01",
  "auto_renew": true,
  "payment_method": "credit_card",  // or "paypal", "stripe"
  "next_billing_date": "2025-12-01",
  "created_at": "2025-10-15T10:00:00Z",
  "updated_at": "2025-12-19T15:30:00Z"
}
```

#### **2. Upgrade Subscription**
```
POST /api/v1/subscriptions/{user_id}/upgrade
Authorization: Bearer {access_token}
Content-Type: application/json

Request Body:
{
  "target_tier": "premium",  // "low", "mid", "premium"
  "payment_method": "stripe",
  "payment_token": "tok_visa_..."  // Payment provider token
}

Response (200 OK):
{
  "user_id": 123,
  "previous_tier": "mid",
  "new_tier": "premium",
  "subscription_status": "active",
  "subscription_start_date": "2025-12-19",
  "subscription_end_date": "2026-01-19",
  "next_billing_date": "2026-01-19",
  "transaction_id": "txn_1234567890"
}
```

#### **3. Cancel Subscription**
```
POST /api/v1/subscriptions/{user_id}/cancel
Authorization: Bearer {access_token}

Request Body:
{
  "reason": "No longer needed",  // Optional
  "cancel_immediately": false  // If true, cancel now; if false, cancel at end of billing period
}

Response (200 OK):
{
  "user_id": 123,
  "subscription_status": "cancelled",
  "subscription_end_date": "2025-12-01",  // End of current billing period
  "cancelled_at": "2025-12-19T15:30:00Z",
  "message": "Subscription will remain active until 2025-12-01"
}
```

#### **4. Reactivate Subscription**
```
POST /api/v1/subscriptions/{user_id}/reactivate
Authorization: Bearer {access_token}
Content-Type: application/json

Request Body:
{
  "payment_method": "stripe",
  "payment_token": "tok_visa_..."  // Payment provider token
}

Response (200 OK):
{
  "user_id": 123,
  "subscription_status": "active",
  "subscription_start_date": "2025-12-19",
  "subscription_end_date": "2026-01-19",
  "next_billing_date": "2026-01-19"
}
```

#### **5. Get Subscription History**
```
GET /api/v1/subscriptions/{user_id}/history
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "history": [
    {
      "tier": "free",
      "status": "active",
      "start_date": "2025-10-15",
      "end_date": "2025-11-01",
      "cancelled_at": null
    },
    {
      "tier": "mid",
      "status": "active",
      "start_date": "2025-11-01",
      "end_date": "2025-12-01",
      "cancelled_at": null
    }
  ]
}
```

---

## 🔌 Plugin Management API Endpoints

### **Plugin Access Endpoints**

#### **1. Get User Plugin Access**
```
GET /api/v1/plugins/{user_id}/access
Authorization: Bearer {access_token}

Response (200 OK):
{
  "user_id": 123,
  "plugins": [
    {
      "plugin_id": "tsla_improved_strategy",
      "access_level": "full",
      "purchased_at": "2025-11-01T10:00:00Z",
      "expires_at": null,
      "status": "active"
    },
    {
      "plugin_id": "trend_following",
      "access_level": "limited",
      "purchased_at": "2025-11-15T10:00:00Z",
      "expires_at": "2025-12-15T10:00:00Z",
      "status": "active"
    }
  ]
}
```

#### **2. Get Available Plugins**
```
GET /api/v1/plugins/available?tier=mid
Authorization: Bearer {access_token}  // Optional for public endpoint

Response (200 OK):
{
  "plugins": [
    {
      "plugin_id": "tsla_improved_strategy",
      "name": "TSLA Improved Strategy",
      "description": "Advanced TSLA trading strategy",
      "tier_requirements": ["low", "mid", "premium"],
      "price": null,  // Included in tier
      "performance_metrics": {
        "avg_win_rate": 65.0,
        "avg_profit_factor": 1.8,
        "total_users": 150
      }
    },
    {
      "plugin_id": "trend_following",
      "name": "Trend Following Strategy",
      "description": "Classic trend following strategy",
      "tier_requirements": ["free", "low", "mid", "premium"],
      "price": null,
      "performance_metrics": {
        "avg_win_rate": 58.0,
        "avg_profit_factor": 1.5,
        "total_users": 300
      }
    }
  ]
}
```

#### **3. Purchase Plugin Access**
```
POST /api/v1/plugins/{user_id}/purchase
Authorization: Bearer {access_token}
Content-Type: application/json

Request Body:
{
  "plugin_id": "tsla_improved_strategy",
  "payment_method": "stripe",
  "payment_token": "tok_visa_..."  // If plugin requires separate purchase
}

Response (200 OK):
{
  "user_id": 123,
  "plugin_id": "tsla_improved_strategy",
  "access_level": "full",
  "purchased_at": "2025-12-19T15:30:00Z",
  "expires_at": null,
  "transaction_id": "txn_1234567890"
}
```

---

## 🔒 Security & Authentication Implementation

### **JWT Token Structure**

**Access Token Payload:**
```json
{
  "user_id": 123,
  "email": "user@example.com",
  "subscription_tier": "mid",
  "exp": 1734625800,  // Expiration timestamp
  "iat": 1734622200,  // Issued at timestamp
  "type": "access"
}
```

**Refresh Token Payload:**
```json
{
  "user_id": 123,
  "token_id": "uuid-v4",
  "exp": 1737214200,  // Longer expiration (30 days)
  "iat": 1734622200,
  "type": "refresh"
}
```

### **Token Security**

1. **Access Token:**
   - Expiration: 1 hour
   - Algorithm: HS256 (HMAC-SHA256)
   - Secret: Environment variable `JWT_SECRET_KEY`

2. **Refresh Token:**
   - Expiration: 30 days
   - Algorithm: HS256
   - Stored in database (can be revoked)

3. **Token Storage (WordPress Plugin):**
   - Store in WordPress user meta (encrypted)
   - Or use WordPress transients (with expiration)
   - Never store in cookies (use secure HTTP-only cookies if needed)

### **Rate Limiting**

**Rate Limits:**
- Authentication endpoints: 5 requests/minute per IP
- API endpoints: 100 requests/minute per user
- Performance endpoints: 60 requests/minute per user

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1734622800
```

### **Error Responses**

**Standard Error Format:**
```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Token expired or invalid",
    "details": {}
  }
}
```

**HTTP Status Codes:**
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## 🔄 WordPress Plugin Integration

### **API Client Implementation**

**WordPress Plugin API Client Class:**
```php
class TradingRobotPlug_API_Client {
    private $api_base_url = 'https://api.tradingrobotplug.com/api/v1';
    private $access_token = null;
    private $refresh_token = null;
    
    public function authenticate($email, $password) {
        // POST /api/v1/auth/login
        // Store tokens in WordPress user meta
    }
    
    public function refresh_token() {
        // POST /api/v1/auth/refresh
        // Update stored tokens
    }
    
    public function get_user_performance($user_id, $period, $date = null) {
        // GET /api/v1/performance/{user_id}/{period}
        // Handle token refresh if expired
    }
    
    public function get_subscription($user_id) {
        // GET /api/v1/subscriptions/{user_id}
    }
    
    // ... more methods
}
```

### **WordPress Plugin Authentication Flow**

1. **User Registration/Login:**
   - WordPress plugin calls `/api/v1/auth/register` or `/api/v1/auth/login`
   - Store tokens in WordPress user meta (encrypted)
   - Set WordPress user session

2. **API Requests:**
   - Retrieve access token from WordPress user meta
   - Include in `Authorization: Bearer {token}` header
   - If token expired, use refresh token to get new access token
   - Retry original request with new token

3. **Token Refresh:**
   - Check token expiration before each API call
   - If expired, call `/api/v1/auth/refresh` with refresh token
   - Update stored tokens
   - Continue with original request

---

## 📋 Integration Checkpoints

### **Checkpoint 1: API Contract Definition**

**Status:** ✅ **COMPLETE**

**Validation:**
- ✅ All API endpoints defined
- ✅ Request/response formats specified
- ✅ Authentication flow documented
- ✅ Error handling defined

---

### **Checkpoint 2: Backend API Implementation**

**Status:** ⏳ **PENDING**

**Validation:**
- ✅ Backend API endpoints implemented
- ✅ JWT authentication implemented
- ✅ Database schema created
- ✅ Rate limiting implemented
- ✅ Security measures in place

---

### **Checkpoint 3: WordPress Plugin API Client**

**Status:** ⏳ **PENDING**

**Validation:**
- ✅ API client class implemented
- ✅ Authentication flow implemented
- ✅ Token management implemented
- ✅ Error handling implemented

---

### **Checkpoint 4: Integration Testing**

**Status:** ⏳ **PENDING**

**Validation:**
- ✅ Authentication flow tested
- ✅ All API endpoints tested
- ✅ Token refresh tested
- ✅ Error handling tested
- ✅ Rate limiting tested

---

## 🚀 Next Steps

1. **Immediate:**
   - ✅ API contract defined
   - ⏳ Coordinate with Agent-7 for WordPress plugin development
   - ⏳ Coordinate with Agent-2 for architecture review
   - ⏳ Begin backend API implementation

2. **Backend API Development:**
   - Implement authentication endpoints
   - Implement user management endpoints
   - Implement performance tracking endpoints
   - Implement subscription management endpoints

3. **WordPress Plugin Development:**
   - Implement API client class
   - Implement authentication flow
   - Implement user dashboard integration
   - Implement performance dashboard integration

---

**Status:** ✅ **API CONTRACT DEFINED** | 🔄 **AWAITING COORDINATION**  
**Next:** Coordinate with Agent-7 and Agent-2, then begin implementation

🐝 **WE. ARE. SWARM. ⚡**

