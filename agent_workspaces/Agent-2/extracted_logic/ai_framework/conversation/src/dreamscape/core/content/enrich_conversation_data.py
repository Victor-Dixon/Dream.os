#!/usr/bin/env python3
"""
Enrich Conversation Data for Conversational AI Workflow
======================================================

This script ingests all existing conversation data and adds more real conversation context
to provide richer context for the conversational AI workflow system.

Features:
- Ingests all existing conversation JSON files
- Adds synthetic but realistic conversation data for testing
- Creates diverse conversation topics and contexts
- Updates the memory database with enriched data
- Provides rich context for the conversational AI workflow
"""

import sys
import json
import logging
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import random

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# EDIT START: Consolidation import update (Agent 5)
from dreamscape.core.memory import MemoryManager
# EDIT END
from dreamscape.core.conversation_system import ConversationStorage  # Consolidated import (was conversation_storage)

# Configure logging
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("enrich_conversations")

class ConversationDataEnricher:
    """Enriches conversation data with real and synthetic conversations."""
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.conversations_dir = Path("data/conversations")
        
        # Real conversation topics and contexts
        self.real_topics = [
            "Code Review and Optimization",
            "System Architecture Design",
            "API Development and Integration",
            "Database Schema Optimization",
            "Security Implementation",
            "Performance Tuning",
            "Testing Strategy",
            "Deployment Pipeline",
            "Monitoring and Logging",
            "Scalability Planning",
            "Machine Learning Integration",
            "Data Processing Pipeline",
            "Frontend Development",
            "Backend API Design",
            "DevOps Automation",
            "Cloud Infrastructure",
            "Microservices Architecture",
            "Event-Driven Systems",
            "Real-time Data Processing",
            "AI/ML Model Development"
        ]
        
        # Synthetic conversation contexts
        self.synthetic_contexts = [
            {
                "title": "Advanced Fintech Engine Development",
                "content": """User: I'm working on an advanced fintech engine that integrates multiple APIs for real-time stock data, sentiment analysis, and ML predictions. I need help with the architecture.

Assistant: That's an exciting project! Let me help you design a robust architecture for your fintech engine. Here's a comprehensive approach:

1. **API Integration Layer**: Create a unified interface for multiple data sources (Finnhub, NewsAPI, TwelveData, FRED)
2. **Data Processing Pipeline**: Implement real-time data processing with caching and rate limiting
3. **ML Prediction Engine**: Build a modular system for different prediction models
4. **Risk Management Module**: Add position sizing and stop-loss calculations
5. **Portfolio Optimization**: Integrate RL and GA for dynamic portfolio management

Key considerations:
- Use WAL mode for database concurrency
- Implement exponential backoff for API retries
- Add comprehensive error handling and logging
- Consider using message queues for real-time processing

Would you like me to help you implement any specific component?""",
                "tags": ["fintech", "api-integration", "ml", "architecture"]
            },
            {
                "title": "Dreamscape AI System Architecture",
                "content": """User: I'm building a Dreamscape AI system that processes conversations and creates an MMORPG-like experience. How should I structure the memory and processing components?

Assistant: Your Dreamscape AI system sounds fascinating! Here's a recommended architecture:

**Core Components:**
1. **Memory Manager**: Vector-based storage with FAISS indexing for semantic search
2. **Conversation Processor**: Extract insights, emotions, and narrative elements
3. **MMORPG Engine**: Transform conversations into quests, XP, and character progression
4. **Context Injection**: Real-time context awareness for AI interactions
5. **Discord Integration**: Real-time notifications and quest management

**Technical Implementation:**
- Use SQLite with WAL mode for concurrent access
- Implement connection pooling and retry logic
- Add vector embeddings for semantic similarity
- Create modular quest and skill systems
- Build real-time event processing

**Key Features:**
- Breakthrough memory extraction
- Dynamic quest generation
- Skill tree progression
- Real-time Discord notifications
- Context-aware AI responses

This creates a living, breathing AI system that learns from every interaction!""",
                "tags": ["ai", "mmorpg", "memory", "conversation-processing"]
            },
            {
                "title": "Conversational AI Workflow Design",
                "content": """User: I want to create a conversational AI workflow that can "speak" to my work and provide context-aware assistance. How should I approach this?

Assistant: Excellent idea! A conversational AI workflow that understands your work context is incredibly powerful. Here's how to build it:

**Core Architecture:**
1. **Context Engine**: Analyze conversation history and work patterns
2. **Session Management**: Maintain conversation state and context
3. **Work Pattern Analysis**: Identify recurring themes and workflows
4. **Suggestion Engine**: Provide actionable workflow recommendations
5. **Integration Layer**: Connect with existing tools and systems

**Implementation Strategy:**
- Use Jinja2 templates for dynamic prompt generation
- Implement session persistence for long conversations
- Add work pattern recognition algorithms
- Create context-aware response generation
- Build integration hooks for external tools

**Key Features:**
- Real-time context awareness
- Workflow suggestion engine
- Session memory and continuity
- Pattern recognition and analysis
- Seamless tool integration

This creates an AI assistant that truly understands your work and can provide meaningful, contextual assistance!""",
                "tags": ["conversational-ai", "workflow", "context", "assistance"]
            },
            {
                "title": "Database Concurrency and Performance",
                "content": """User: I'm experiencing database locking issues with SQLite in my multi-threaded application. How can I fix this?

Assistant: SQLite concurrency issues are common in multi-threaded applications. Here's a comprehensive solution:

**Root Causes:**
- Shared connections across threads
- Lack of proper connection management
- Missing WAL mode configuration
- No retry logic for busy databases

**Solutions:**

1. **Enable WAL Mode:**
```python
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.execute("PRAGMA cache_size=10000")
```

2. **Connection Management:**
```python
class ThreadSafeConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self._lock = threading.Lock()
    
    def get_connection(self):
        with self._lock:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            return conn
```

3. **Retry Logic with Exponential Backoff:**
```python
def execute_with_retry(conn, query, params=None, max_retries=5):
    for attempt in range(max_retries):
        try:
            if params:
                return conn.execute(query, params)
            else:
                return conn.execute(query)
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
```

4. **Connection Pooling:**
- Use connection pools to limit concurrent connections
- Implement proper connection cleanup
- Add connection health checks

This approach will eliminate locking issues and improve performance significantly!""",
                "tags": ["database", "concurrency", "sqlite", "performance"]
            },
            {
                "title": "GUI Framework Consistency and Modernization",
                "content": """User: My GUI application has mixed UI frameworks (PyQt6 and Tkinter). How can I standardize on PyQt6 and modernize the interface?

Assistant: Standardizing on PyQt6 is a great choice for modern GUI development! Here's how to migrate and modernize:

**Migration Strategy:**

1. **Framework Analysis:**
```python
# Identify Tkinter usage
import ast
import os

def find_tkinter_usage(directory):
    tkinter_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    if 'tkinter' in content or 'Tk()' in content:
                        tkinter_files.append(filepath)
    return tkinter_files
```

2. **PyQt6 Conversion Pattern:**
```python
# Old Tkinter
import tkinter as tk
root = tk.Tk()
button = tk.Button(root, text="Click me", command=callback)
button.pack()

# New PyQt6
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal

class ModernWidget(QWidget):
    button_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        button = QPushButton("Click me")
        button.clicked.connect(self.button_clicked.emit)
        layout.addWidget(button)
        self.setLayout(layout)
```

3. **Signal-Slot Architecture:**
```python
# Modern PyQt6 signal-slot pattern
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        # Create widgets
        self.button = QPushButton("Process Data")
        self.progress = QProgressBar()
        self.status_label = QLabel("Ready")
    
    def connect_signals(self):
        self.button.clicked.connect(self.process_data)
        self.button.clicked.connect(self.update_status)
    
    def process_data(self):
        # Handle button click
        pass
    
    def update_status(self):
        self.status_label.setText("Processing...")
```

4. **Modern UI Patterns:**
- Use QStackedWidget for tab-like interfaces
- Implement QThread for background processing
- Add QProgressDialog for long operations
- Use QMessageBox for user feedback
- Implement drag-and-drop with QMimeData

5. **Styling and Theming:**
```python
# Modern styling with QSS
app.setStyleSheet("""
QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QProgressBar {
    border: 2px solid #E0E0E0;
    border-radius: 4px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 2px;
}
""")
```

**Benefits of PyQt6:**
- Modern signal-slot architecture
- Better threading support
- Rich widget library
- Cross-platform consistency
- Professional appearance
- Excellent documentation

This migration will give you a modern, maintainable, and professional GUI application!""",
                "tags": ["gui", "pyqt6", "migration", "modernization"]
            }
        ]
    
    def ingest_existing_conversations(self) -> int:
        """Ingest all existing conversation files."""
        logger.info("📥 Starting ingestion of existing conversations...")
        
        if not self.conversations_dir.exists():
            logger.warning("❌ Conversations directory not found")
            return 0
        
        json_files = list(self.conversations_dir.glob("*.json"))
        logger.info(f"📁 Found {len(json_files)} conversation files")
        
        ingested_count = 0
        errors = []
        
        for file_path in json_files:
            try:
                logger.info(f"📥 Processing: {file_path.name}")
                
                # Load JSON file
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract conversation data
                conversation_id = data.get('id', file_path.stem)
                title = data.get('title', 'Untitled')
                url = data.get('url', '')
                extracted_at = data.get('extracted_at', datetime.now().isoformat())
                
                # Get content from full_conversation or messages
                content = data.get('full_conversation', '')
                if not content and 'messages' in data:
                    # If no full_conversation, combine messages
                    messages = data.get('messages', [])
                    if isinstance(messages, list):
                        content = '\n\n'.join(messages)
                
                # Create conversation data structure
                conversation_data = {
                    'id': conversation_id,
                    'title': title,
                    'url': url,
                    'timestamp': extracted_at,
                    'captured_at': extracted_at,
                    'model': 'gpt-4o',  # Default model
                    'content': content,
                    'message_count': len(data.get('messages', [])),
                    'word_count': len(content.split()) if content else 0,
                    'source': 'chatgpt'
                }
                
                # Store conversation
                if self.memory_manager.storage.store_conversation(conversation_data):
                    ingested_count += 1
                    logger.info(f"✅ Ingested: {title} (ID: {conversation_id})")
                else:
                    errors.append(f"Failed to store: {title}")
                    
            except Exception as e:
                error_msg = f"Failed to ingest {file_path.name}: {e}"
                errors.append(error_msg)
                logger.error(f"❌ {error_msg}")
        
        logger.info(f"🎉 Successfully ingested {ingested_count} conversations")
        if errors:
            logger.warning(f"⚠️ {len(errors)} errors occurred during ingestion")
        
        return ingested_count
    
    def add_synthetic_conversations(self, count: int = 20) -> int:
        """Add synthetic but realistic conversation data."""
        logger.info(f"🎭 Adding {count} synthetic conversations...")
        
        added_count = 0
        
        for i in range(count):
            try:
                # Select a random context
                context = random.choice(self.synthetic_contexts)
                
                # Generate conversation ID
                conversation_id = f"synthetic_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"
                
                # Create conversation data
                conversation_data = {
                    'id': conversation_id,
                    'title': context['title'],
                    'url': f"https://chatgpt.com/c/{conversation_id}",
                    'timestamp': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                    'captured_at': datetime.now().isoformat(),
                    'model': 'gpt-4o',
                    'content': context['content'],
                    'message_count': random.randint(5, 15),
                    'word_count': len(context['content'].split()),
                    'source': 'synthetic',
                    'tags': ','.join(context['tags'])
                }
                
                # Store conversation
                if self.memory_manager.storage.store_conversation(conversation_data):
                    added_count += 1
                    logger.info(f"✅ Added synthetic: {context['title']}")
                else:
                    logger.warning(f"⚠️ Failed to add synthetic: {context['title']}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to add synthetic conversation {i}: {e}")
        
        logger.info(f"🎭 Successfully added {added_count} synthetic conversations")
        return added_count
    
    def add_real_topic_conversations(self, count: int = 15) -> int:
        """Add conversations based on real development topics."""
        logger.info(f"💻 Adding {count} real topic conversations...")
        
        added_count = 0
        
        for i in range(count):
            try:
                # Select a random topic
                topic = random.choice(self.real_topics)
                
                # Generate realistic conversation content
                content = self._generate_realistic_conversation(topic)
                
                # Generate conversation ID
                conversation_id = f"topic_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"
                
                # Create conversation data
                conversation_data = {
                    'id': conversation_id,
                    'title': f"{topic} - Development Discussion",
                    'url': f"https://chatgpt.com/c/{conversation_id}",
                    'timestamp': (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                    'captured_at': datetime.now().isoformat(),
                    'model': 'gpt-4o',
                    'content': content,
                    'message_count': random.randint(8, 20),
                    'word_count': len(content.split()),
                    'source': 'real_topic',
                    'tags': f"development,{topic.lower().replace(' ', '_')}"
                }
                
                # Store conversation
                if self.memory_manager.storage.store_conversation(conversation_data):
                    added_count += 1
                    logger.info(f"✅ Added topic: {topic}")
                else:
                    logger.warning(f"⚠️ Failed to add topic: {topic}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to add topic conversation {i}: {e}")
        
        logger.info(f"💻 Successfully added {added_count} topic conversations")
        return added_count
    
    def _generate_realistic_conversation(self, topic: str) -> str:
        """Generate realistic conversation content for a given topic."""
        
        conversation_templates = {
            "Code Review and Optimization": """User: I have this code that's working but I think it could be optimized. Can you help me review it?

[Code snippet provided]

Assistant: Looking at your code, I can see several optimization opportunities:

1. **Algorithm Complexity**: The nested loop creates O(n²) complexity. Consider using a hash map for O(n) lookup.
2. **Memory Usage**: You're creating unnecessary intermediate lists. Use generators for better memory efficiency.
3. **Error Handling**: Add proper exception handling for edge cases.
4. **Code Structure**: Break down the large function into smaller, testable units.

Here's an optimized version:
[Optimized code provided]

The key improvements:
- Reduced time complexity from O(n²) to O(n)
- Improved memory efficiency by 60%
- Better error handling and edge case coverage
- More maintainable and testable code structure

Would you like me to explain any of these optimizations in more detail?""",
            
            "System Architecture Design": """User: I'm designing a new system architecture and need help with the overall structure. The system needs to handle real-time data processing, user authentication, and API integrations.

Assistant: Great! Let me help you design a robust system architecture. Here's a comprehensive approach:

**High-Level Architecture:**
1. **API Gateway Layer**: Handle authentication, rate limiting, and request routing
2. **Microservices Layer**: Separate services for different business domains
3. **Message Queue System**: Use Kafka/RabbitMQ for real-time data processing
4. **Database Layer**: Primary database + read replicas for scalability
5. **Caching Layer**: Redis for session management and data caching

**Key Design Principles:**
- **Separation of Concerns**: Each service has a single responsibility
- **Loose Coupling**: Services communicate via well-defined APIs
- **High Availability**: Implement circuit breakers and health checks
- **Scalability**: Horizontal scaling with load balancers
- **Security**: Implement OAuth2, JWT tokens, and API key management

**Technology Stack Recommendations:**
- **Backend**: Node.js/Python with FastAPI/Express
- **Database**: PostgreSQL for primary, Redis for caching
- **Message Queue**: Apache Kafka for real-time processing
- **Monitoring**: Prometheus + Grafana for observability
- **Deployment**: Docker + Kubernetes for containerization

Would you like me to dive deeper into any specific component?""",
            
            "API Development and Integration": """User: I'm building a REST API that needs to integrate with multiple third-party services. What's the best approach for handling authentication, rate limiting, and error handling?

Assistant: Excellent question! Building a robust API with multiple integrations requires careful planning. Here's a comprehensive approach:

**Authentication Strategy:**
1. **API Key Management**: Use secure key storage with encryption
2. **OAuth2 Integration**: Implement OAuth2 flows for third-party services
3. **JWT Tokens**: Use JWT for session management and authorization
4. **Rate Limiting**: Implement per-user and per-endpoint rate limits

**Error Handling Best Practices:**
```python
class APIError(Exception):
    def __init__(self, message, status_code, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            raise APIError(f"External service error: {e}", 502)
        except ValidationError as e:
            raise APIError(f"Validation error: {e}", 400)
        except Exception as e:
            raise APIError(f"Internal server error: {e}", 500)
    return wrapper
```

**Rate Limiting Implementation:**
```python
from functools import wraps
import time
import redis

def rate_limit(limit=100, window=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"rate_limit:{func.__name__}:{user_id}"
            current = redis_client.get(key)
            
            if current and int(current) >= limit:
                raise APIError("Rate limit exceeded", 429)
            
            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            pipe.execute()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**Integration Patterns:**
1. **Circuit Breaker**: Prevent cascade failures
2. **Retry Logic**: Exponential backoff for transient failures
3. **Timeout Management**: Set appropriate timeouts for each service
4. **Fallback Mechanisms**: Graceful degradation when services are unavailable

This approach ensures your API is robust, scalable, and maintainable!""",
            
            "Database Schema Optimization": """User: My database queries are getting slow as the data grows. How can I optimize the schema and queries for better performance?

Assistant: Database optimization is crucial for application performance! Here's a systematic approach:

**Schema Optimization:**
1. **Indexing Strategy**: Create indexes on frequently queried columns
2. **Normalization**: Balance between normalization and denormalization
3. **Data Types**: Use appropriate data types to reduce storage
4. **Partitioning**: Partition large tables by date or other criteria

**Query Optimization:**
```sql
-- Before: Slow query with multiple joins
SELECT u.name, p.title, c.content
FROM users u
JOIN posts p ON u.id = p.user_id
JOIN comments c ON p.id = c.post_id
WHERE u.created_at > '2024-01-01';

-- After: Optimized with proper indexing
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);

-- Use covering indexes for frequently accessed data
CREATE INDEX idx_user_posts_covering ON posts(user_id, title, created_at);
```

**Performance Monitoring:**
```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- Monitor slow queries
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

**Advanced Optimization Techniques:**
1. **Query Caching**: Cache frequently executed queries
2. **Connection Pooling**: Reuse database connections
3. **Read Replicas**: Distribute read load across multiple databases
4. **Materialized Views**: Pre-compute complex aggregations
5. **Database Sharding**: Split data across multiple databases

**Monitoring and Maintenance:**
- Set up automated vacuum and analyze jobs
- Monitor index usage and remove unused indexes
- Track query performance over time
- Implement database health checks

This comprehensive approach will significantly improve your database performance!""",
            
            "Security Implementation": """User: I need to implement comprehensive security measures for my web application. What are the essential security practices I should follow?

Assistant: Security is paramount for any web application! Here's a comprehensive security implementation guide:

**Authentication & Authorization:**
1. **Password Security**: Use bcrypt with high cost factors
2. **Multi-Factor Authentication**: Implement TOTP or SMS-based 2FA
3. **Session Management**: Use secure, HTTP-only cookies with CSRF protection
4. **Role-Based Access Control**: Implement fine-grained permissions

**Input Validation & Sanitization:**
```python
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=8), required=True)
    username = fields.Str(validate=validate.Regexp(r'^[a-zA-Z0-9_]+$'))

def validate_input(data, schema):
    try:
        return schema.load(data)
    except ValidationError as e:
        raise APIError(f"Validation error: {e.messages}", 400)
```

**SQL Injection Prevention:**
```python
# Use parameterized queries
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# Use ORM with proper escaping
User.query.filter_by(email=email).first()
```

**XSS Protection:**
```python
# Sanitize user input
from bleach import clean

def sanitize_html(content):
    return clean(content, tags=[], strip=True)

# Use Content Security Policy headers
response.headers['Content-Security-Policy'] = "default-src 'self'"
```

**API Security:**
1. **Rate Limiting**: Prevent abuse and brute force attacks
2. **API Key Management**: Secure storage and rotation of API keys
3. **Request Signing**: Sign requests to prevent tampering
4. **HTTPS Only**: Enforce HTTPS for all communications

**Data Protection:**
```python
# Encrypt sensitive data
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

# Hash passwords
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
```

**Security Headers:**
```python
# Implement security headers
response.headers.update({
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
})
```

**Monitoring & Logging:**
- Log all authentication attempts
- Monitor for suspicious activity patterns
- Implement intrusion detection
- Regular security audits and penetration testing

This comprehensive security approach will protect your application from most common threats!"""
        }
        
        # Get template for the topic or use a generic one
        template = conversation_templates.get(topic, conversation_templates["Code Review and Optimization"])
        
        # Add some variation to make it more realistic
        variations = [
            "Can you help me with this?",
            "I'm stuck on this part.",
            "What do you think about this approach?",
            "Is there a better way to do this?",
            "I need some guidance on this."
        ]
        
        # Add a follow-up question
        follow_ups = [
            "Thanks! That's really helpful.",
            "I'll implement these suggestions.",
            "Can you explain that in more detail?",
            "What about edge cases?",
            "How would you test this?"
        ]
        
        # Create the conversation
        conversation = f"""User: {random.choice(variations)}

{template}

User: {random.choice(follow_ups)}

Assistant: You're welcome! Feel free to reach out if you need any clarification or run into issues during implementation. Good luck with your project!"""
        
        return conversation
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about the conversation database."""
        try:
            conversations = self.memory_manager.get_all_conversations()
            
            stats = {
                'total_conversations': len(conversations),
                'sources': {},
                'recent_conversations': len(self.memory_manager.get_recent_conversations(limit=50)),
                'total_words': sum(conv.get('word_count', 0) for conv in conversations),
                'total_messages': sum(conv.get('message_count', 0) for conv in conversations)
            }
            
            # Count by source
            for conv in conversations:
                source = conv.get('source', 'unknown')
                stats['sources'][source] = stats['sources'].get(source, 0) + 1
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get conversation stats: {e}")
            return {}
    
    def run_enrichment(self, add_synthetic: bool = True, add_topics: bool = True) -> Dict[str, Any]:
        """Run the complete conversation enrichment process."""
        logger.info("🚀 Starting conversation data enrichment...")
        
        results = {
            'existing_ingested': 0,
            'synthetic_added': 0,
            'topics_added': 0,
            'total_conversations': 0,
            'errors': []
        }
        
        try:
            # Step 1: Ingest existing conversations
            results['existing_ingested'] = self.ingest_existing_conversations()
            
            # Step 2: Add synthetic conversations
            if add_synthetic:
                results['synthetic_added'] = self.add_synthetic_conversations(count=20)
            
            # Step 3: Add topic-based conversations
            if add_topics:
                results['topics_added'] = self.add_real_topic_conversations(count=15)
            
            # Step 4: Get final stats
            stats = self.get_conversation_stats()
            results['total_conversations'] = stats.get('total_conversations', 0)
            results['stats'] = stats
            
            logger.info("🎉 Conversation enrichment completed successfully!")
            logger.info(f"📊 Final stats: {stats}")
            
        except Exception as e:
            error_msg = f"Enrichment process failed: {e}"
            results['errors'].append(error_msg)
            logger.error(f"❌ {error_msg}")
        
        return results

def main():
    """Main function to run the conversation enrichment."""
    print("🤖 Conversation Data Enrichment Tool")
    print("=" * 50)
    
    try:
        # Initialize memory manager
        with MemoryManager("dreamos_memory.db") as memory_manager:
            enricher = ConversationDataEnricher(memory_manager)
            
            # Run enrichment
            results = enricher.run_enrichment(
                add_synthetic=True,
                add_topics=True
            )
            
            # Display results
            print("\n📊 Enrichment Results:")
            print(f"✅ Existing conversations ingested: {results['existing_ingested']}")
            print(f"🎭 Synthetic conversations added: {results['synthetic_added']}")
            print(f"💻 Topic conversations added: {results['topics_added']}")
            print(f"📈 Total conversations: {results['total_conversations']}")
            
            if results.get('stats'):
                stats = results['stats']
                print(f"\n📈 Detailed Statistics:")
                print(f"   Total words: {stats.get('total_words', 0):,}")
                print(f"   Total messages: {stats.get('total_messages', 0):,}")
                print(f"   Recent conversations: {stats.get('recent_conversations', 0)}")
                
                if stats.get('sources'):
                    print(f"   Sources:")
                    for source, count in stats['sources'].items():
                        print(f"     {source}: {count}")
            
            if results['errors']:
                print(f"\n⚠️ Errors encountered: {len(results['errors'])}")
                for error in results['errors']:
                    print(f"   - {error}")
            
            print("\n🎉 Enrichment completed! Your conversational AI workflow now has rich context data.")
            
    except Exception as e:
        logger.error(f"❌ Main process failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 