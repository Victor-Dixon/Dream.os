# API Ecosystem Specification
==============================

**Agent Cellphone V2 REST API & SDK**
**Version 2.0.0 - Phase 3 Ecosystem Expansion**

## Overview

The Agent Cellphone V2 API Ecosystem provides comprehensive REST APIs, SDKs, and developer tools for building integrations, automation, and custom applications on top of the Agent Cellphone platform.

## Core API Architecture

### 🏗️ API Design Principles

- **RESTful Design**: Resource-based URLs with standard HTTP methods
- **JSON API**: Consistent JSON request/response format
- **Versioning**: API versioning in URL paths (`/v2/`)
- **Authentication**: Token-based authentication with role-based permissions
- **Rate Limiting**: Intelligent rate limiting with burst handling
- **Documentation**: OpenAPI/Swagger documentation with interactive testing

### 🌐 Base API Configuration

```
Protocol: HTTPS
Base URL: https://api.agent-cellphone.dev/v2/
Content-Type: application/json
Authentication: Bearer Token
Rate Limits:
  - Free Tier: 1,000 requests/hour
  - Developer Tier: 10,000 requests/hour
  - Enterprise Tier: 100,000 requests/hour
```

## REST API Specification

### 🔐 Authentication & Authorization

#### API Key Management

```http
POST /v2/auth/api-keys
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "name": "My Integration",
  "permissions": ["read:agents", "write:tasks"],
  "rate_limit_tier": "developer"
}
```

#### Token Authentication

```http
GET /v2/agents
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 🤖 Agent Management API

#### List Agents
```http
GET /v2/agents
```

**Query Parameters:**
- `status` - Filter by status (active, inactive, busy)
- `specialty` - Filter by specialty (python, ai, web, etc.)
- `limit` - Maximum number of results (default: 50)
- `offset` - Pagination offset (default: 0)

**Response:**
```json
{
  "data": [
    {
      "id": "agent-1",
      "name": "Integration Specialist",
      "status": "active",
      "specialties": ["api", "backend", "integration"],
      "current_tasks": 2,
      "success_rate": 0.95,
      "performance_score": 1.2,
      "last_seen": "2024-01-13T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 8,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

#### Get Agent Details
```http
GET /v2/agents/{agent_id}
```

**Response:**
```json
{
  "id": "agent-1",
  "name": "Integration Specialist",
  "status": "active",
  "specialties": ["api", "backend", "integration"],
  "capabilities": {
    "max_concurrent_tasks": 5,
    "supported_languages": ["python", "javascript", "go"],
    "integrations": ["discord", "slack", "github"]
  },
  "performance_metrics": {
    "tasks_completed": 1250,
    "success_rate": 0.95,
    "average_response_time": 45.2,
    "current_workload": 2
  },
  "contact_info": {
    "discord_id": "agent_1#1234",
    "email": "agent-1@agent-cellphone.dev"
  }
}
```

#### Update Agent Configuration
```http
PUT /v2/agents/{agent_id}
Content-Type: application/json

{
  "status": "busy",
  "specialties": ["api", "backend", "integration", "database"],
  "max_concurrent_tasks": 7
}
```

### 📋 Task Management API

#### Create Task
```http
POST /v2/tasks
Content-Type: application/json

{
  "title": "Implement user authentication API",
  "description": "Create REST API endpoints for user registration and login",
  "priority": "high",
  "required_skills": ["api", "backend", "security"],
  "estimated_complexity": 3,
  "max_completion_time": 3600,
  "dependencies": [],
  "metadata": {
    "project": "user-management",
    "epic": "authentication-system"
  }
}
```

**Response:**
```json
{
  "id": "task_12345",
  "title": "Implement user authentication API",
  "status": "created",
  "created_at": "2024-01-13T10:30:00Z",
  "estimated_completion": "2024-01-13T11:30:00Z",
  "assigned_to": null,
  "created_by": "external_integration"
}
```

#### Query Tasks
```http
GET /v2/tasks?status=active&priority=high&assigned_to=agent-1
```

**Query Parameters:**
- `status` - Task status (created, assigned, in_progress, completed, failed)
- `priority` - Priority level (low, medium, high, urgent)
- `assigned_to` - Agent ID filter
- `created_by` - Creator filter
- `skill_required` - Required skill filter
- `limit` - Results limit (default: 50)
- `offset` - Pagination offset

#### Assign Task to Agent
```http
POST /v2/tasks/{task_id}/assign
Content-Type: application/json

{
  "agent_id": "agent-1",
  "assignment_reason": "Best match for API and backend skills",
  "expected_completion": "2024-01-13T12:00:00Z"
}
```

#### Update Task Status
```http
PUT /v2/tasks/{task_id}
Content-Type: application/json

{
  "status": "completed",
  "completion_notes": "Successfully implemented authentication API with JWT tokens",
  "actual_complexity": 3,
  "time_spent_seconds": 2400
}
```

### 🤝 Coordination API

#### Start Coordination Session
```http
POST /v2/coordination/sessions
Content-Type: application/json

{
  "title": "API + Frontend Integration Coordination",
  "participants": ["agent-1", "agent-7"],
  "objective": "Integrate user authentication API with frontend",
  "estimated_duration": 3600,
  "context": {
    "project": "user-management",
    "apis": ["POST /auth/register", "POST /auth/login"],
    "frontend_components": ["LoginForm", "RegisterForm"]
  }
}
```

**Response:**
```json
{
  "session_id": "coord_67890",
  "title": "API + Frontend Integration Coordination",
  "status": "active",
  "participants": ["agent-1", "agent-7"],
  "started_at": "2024-01-13T10:30:00Z",
  "coordination_intelligence": {
    "strategy": "bilateral_coordination",
    "confidence": 0.92,
    "risk_level": "low",
    "estimated_completion": "2024-01-13T11:30:00Z"
  }
}
```

#### Send Coordination Message
```http
POST /v2/coordination/sessions/{session_id}/messages
Content-Type: application/json

{
  "sender": "agent-1",
  "message_type": "progress_update",
  "content": "API endpoints implemented, ready for frontend integration",
  "attachments": [
    {
      "type": "code",
      "language": "python",
      "content": "def authenticate_user(credentials):\n    return jwt_token"
    }
  ]
}
```

#### Get Coordination History
```http
GET /v2/coordination/sessions/{session_id}/messages?limit=20&offset=0
```

### 🔌 Plugin Management API

#### List Available Plugins
```http
GET /v2/plugins
```

**Response:**
```json
{
  "data": [
    {
      "id": "discord-integration",
      "name": "Discord Integration",
      "version": "1.2.0",
      "description": "Seamless Discord communication integration",
      "author": "Agent-7",
      "capabilities": ["messaging", "coordination"],
      "install_count": 1250,
      "rating": 4.8,
      "tags": ["communication", "discord", "messaging"]
    },
    {
      "id": "github-integration",
      "name": "GitHub Integration",
      "version": "2.1.0",
      "description": "GitHub repository and issue management",
      "author": "Agent-8",
      "capabilities": ["integration", "automation"],
      "install_count": 890,
      "rating": 4.6,
      "tags": ["github", "repository", "issues"]
    }
  ]
}
```

#### Install Plugin
```http
POST /v2/plugins/install
Content-Type: application/json

{
  "plugin_id": "discord-integration",
  "version": "1.2.0",
  "configuration": {
    "bot_token": "discord_bot_token_here",
    "server_id": "discord_server_id"
  }
}
```

#### Configure Plugin
```http
PUT /v2/plugins/{plugin_id}/config
Content-Type: application/json

{
  "enabled": true,
  "configuration": {
    "webhook_url": "https://discord.com/api/webhooks/...",
    "channels": ["general", "coordination"]
  }
}
```

### 📊 Analytics API

#### Get System Performance Metrics
```http
GET /v2/analytics/performance?time_range=1h
```

**Response:**
```json
{
  "time_range": "1h",
  "metrics": {
    "orchestration_throughput": 18.5,
    "avg_response_time": 0.34,
    "error_rate": 0.02,
    "active_agents": 6,
    "concurrent_operations": 12,
    "scalability_score": 87.3
  },
  "trends": {
    "cpu_usage_change": 5.2,
    "memory_usage_change": -2.1,
    "throughput_change": 12.3
  }
}
```

#### Get Task Completion Analytics
```http
GET /v2/analytics/tasks?group_by=agent&time_range=7d
```

**Response:**
```json
{
  "time_range": "7d",
  "group_by": "agent",
  "data": [
    {
      "agent_id": "agent-1",
      "tasks_completed": 45,
      "success_rate": 0.96,
      "avg_completion_time": 1800,
      "specialties_performance": {
        "api": {"completed": 25, "success_rate": 0.98},
        "backend": {"completed": 20, "success_rate": 0.94}
      }
    }
  ]
}
```

## SDK Ecosystem

### Python SDK

```python
from agent_cellphone_sdk import AgentCellphoneClient

# Initialize client
client = AgentCellphoneClient(api_key="your_api_key")

# List available agents
agents = await client.agents.list(status="active", specialty="api")
print(f"Found {len(agents)} active API agents")

# Create a task
task = await client.tasks.create({
    "title": "Implement OAuth integration",
    "description": "Add Google OAuth login to user authentication",
    "priority": "high",
    "required_skills": ["api", "security", "oauth"]
})

# Monitor task progress
status = await client.tasks.get_status(task.id)
print(f"Task status: {status.state}")

# Start coordination session
session = await client.coordination.start_session({
    "title": "OAuth + Frontend Integration",
    "participants": ["agent-1", "agent-7"],
    "objective": "Integrate OAuth with frontend login"
})

# Send coordination message
await client.coordination.send_message(session.id, {
    "message_type": "progress_update",
    "content": "OAuth endpoints implemented, testing with Postman"
})

# Get analytics
performance = await client.analytics.get_performance(time_range="1h")
print(f"Current throughput: {performance.orchestration_throughput} ops/sec")
```

### JavaScript SDK

```javascript
import { AgentCellphoneClient } from 'agent-cellphone-sdk';

const client = new AgentCellphoneClient({
  apiKey: 'your_api_key'
});

// Async/await usage
async function manageTasks() {
  // Create task
  const task = await client.tasks.create({
    title: 'Implement real-time notifications',
    description: 'Add WebSocket notifications for user actions',
    priority: 'medium',
    requiredSkills: ['websocket', 'frontend', 'api']
  });

  // Assign to best agent
  await client.tasks.assign(task.id, {
    agentId: 'agent-7',
    reason: 'Best match for frontend and WebSocket skills'
  });

  // Monitor completion
  const status = await client.tasks.getStatus(task.id);
  console.log(`Task ${task.id} is ${status.state}`);
}

// WebSocket coordination
client.coordination.onMessage(sessionId, (message) => {
  console.log('New coordination message:', message);
});
```

### Go SDK

```go
package main

import (
    "context"
    "fmt"
    "log"

    ac "github.com/agent-cellphone/sdk-go"
)

func main() {
    client := ac.NewClient("your_api_key")

    // List agents
    agents, err := client.Agents.List(context.Background(), &ac.AgentFilter{
        Status: "active",
        Specialty: "api",
    })
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Found %d active API agents\n", len(agents))

    // Create task
    task, err := client.Tasks.Create(context.Background(), &ac.TaskRequest{
        Title: "Implement GraphQL API",
        Description: "Add GraphQL endpoint for user queries",
        Priority: ac.PriorityHigh,
        RequiredSkills: []string{"api", "graphql", "backend"},
    })
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Created task: %s\n", task.ID)
}
```

## Rate Limiting & Abuse Prevention

### Rate Limit Headers

```http
X-RateLimit-Limit: 10000
X-RateLimit-Remaining: 9995
X-RateLimit-Reset: 1640995200
X-RateLimit-Retry-After: 3600
```

### Burst Handling

- **Burst Allowance**: 200% of hourly limit for short bursts
- **Refill Rate**: Steady refill prevents complete exhaustion
- **Queue Management**: Excess requests queued during high load

## Error Handling

### Standard Error Response Format

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "details": {
      "limit": 10000,
      "remaining": 0,
      "reset_at": "2024-01-13T11:00:00Z",
      "retry_after": 3600
    },
    "request_id": "req_12345",
    "timestamp": "2024-01-13T10:30:00Z"
  }
}
```

### Common Error Codes

- `RATE_LIMIT_EXCEEDED` - Rate limit exceeded
- `INVALID_API_KEY` - Invalid or missing API key
- `INSUFFICIENT_PERMISSIONS` - API key lacks required permissions
- `RESOURCE_NOT_FOUND` - Requested resource doesn't exist
- `VALIDATION_ERROR` - Request validation failed
- `SERVICE_UNAVAILABLE` - Service temporarily unavailable

## Webhook System

### Webhook Registration

```http
POST /v2/webhooks
Content-Type: application/json

{
  "url": "https://my-app.com/webhooks/agent-cellphone",
  "events": ["task.completed", "coordination.started"],
  "secret": "webhook_secret_for_verification",
  "active": true
}
```

### Webhook Payload Format

```json
{
  "event": "task.completed",
  "timestamp": "2024-01-13T10:30:00Z",
  "data": {
    "task": {
      "id": "task_12345",
      "title": "Implement user authentication",
      "status": "completed",
      "completed_at": "2024-01-13T10:30:00Z",
      "assigned_to": "agent-1"
    }
  },
  "webhook_id": "wh_67890",
  "signature": "sha256=..."
}
```

## Developer Portal

### 📚 Documentation Features

- **Interactive API Explorer**: Test endpoints directly in browser
- **Code Examples**: Multi-language code samples
- **SDK Downloads**: Pre-built SDKs for popular languages
- **Plugin Marketplace**: Browse and install community plugins
- **Developer Community**: Forums and support channels

### 🏆 Developer Program

- **Free Tier**: 1,000 requests/hour for getting started
- **Developer Tier**: 10,000 requests/hour + priority support
- **Enterprise Tier**: Custom limits + dedicated support
- **Partner Program**: Revenue sharing for popular integrations

## Implementation Timeline

### Phase 1: Core API (Week 6.1-6.2)
- [ ] REST API specification and implementation
- [ ] Authentication and authorization system
- [ ] Rate limiting and abuse prevention
- [ ] Basic CRUD operations for agents and tasks

### Phase 2: Coordination API (Week 6.3-6.4)
- [ ] Coordination session management
- [ ] Message handling and history
- [ ] Real-time coordination intelligence
- [ ] Webhook system implementation

### Phase 3: SDK Ecosystem (Week 7.1-7.2)
- [ ] Python SDK development and testing
- [ ] JavaScript SDK development and testing
- [ ] Go SDK development and testing
- [ ] SDK documentation and examples

### Phase 4: Plugin API (Week 7.3-7.4)
- [ ] Plugin management API
- [ ] Plugin marketplace integration
- [ ] Plugin analytics and monitoring
- [ ] Security and validation framework

This API ecosystem specification provides the foundation for Agent Cellphone V2's developer platform, enabling community contributions and third-party integrations while maintaining security and performance standards.