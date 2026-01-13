# AI Integration Quickstart - Immediate Enterprise AI Utilization

## 🎯 **5-Minute AI Integration Setup**

Your system already has **complete enterprise AI infrastructure**. This guide gets you utilizing it immediately.

---

## **Step 1: Verify AI Infrastructure Status** (30 seconds)

```bash
# Check AI service availability
python tools/ai_integration_status_checker.py --check-all

# Expected output: AI services ready (ignore import path warnings for now)
```

**✅ What you have:**
- Advanced Reasoning Engine (5-mode LLM reasoning)
- Vector Database Service (semantic search)
- Web AI APIs (`/ai/reason`, `/ai/semantic-search`, `/ai/reason/stream`)

---

## **Step 2: Test AI Capabilities** (2 minutes)

### Test Reasoning Engine
```bash
# Via web API (recommended)
curl -X POST http://localhost:8000/ai/reason \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze this Python code for optimization opportunities",
    "code": "def slow_function(n): return sum(range(n))",
    "mode": "technical"
  }'
```

### Test Semantic Search
```bash
# Via web API
curl -X POST http://localhost:8000/ai/semantic-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "vector database integration",
    "limit": 5
  }'
```

### Test Streaming Responses
```bash
# Via web API with streaming
curl -X POST http://localhost:8000/ai/reason/stream \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain swarm coordination principles",
    "mode": "strategic"
  }'
```

---

## **Step 3: Integrate AI into Your Workflow** (2 minutes)

### For Code Analysis
```python
from src.ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine

engine = AdvancedReasoningEngine()
result = engine.reason(
    query="Optimize this function",
    code="def process_data(data): return [x*2 for x in data]",
    mode="technical"
)
print(result.analysis)
```

### For Semantic Search
```python
from src.services.vector.vector_database_service import VectorDatabaseService

vdb = VectorDatabaseService()
results = vdb.semantic_search(
    query="error handling patterns",
    limit=10
)
for result in results:
    print(f"Match: {result.content} (score: {result.score})")
```

### For Task Reasoning
```python
from src.services.swarm_intelligence_manager import SwarmIntelligenceManager

intelligence = SwarmIntelligenceManager()
insights = intelligence.analyze_task_complexity(
    task_description="Implement user authentication system",
    constraints=["security", "scalability", "user experience"]
)
print(insights.recommendations)
```

---

## **Available AI Services & Capabilities**

| Service | Purpose | API Endpoint | Integration Method |
|---------|---------|--------------|-------------------|
| **AdvancedReasoningEngine** | Multi-mode LLM reasoning | `/ai/reason` | Direct import + API |
| **VectorDatabaseService** | Semantic search & storage | `/ai/semantic-search` | Direct import + API |
| **SwarmIntelligenceManager** | Task analysis & insights | N/A | Direct import |
| **PerformanceAnalyzer** | System performance analysis | N/A | Direct import |
| **LearningRecommender** | Learning path optimization | N/A | Direct import |
| **RecommendationEngine** | Workflow recommendations | N/A | Direct import |

---

## **Common Integration Patterns**

### Pattern 1: Code Review Assistant
```python
# Integrate AI reasoning into code review workflow
def review_code_changes(changes):
    engine = AdvancedReasoningEngine()
    analysis = engine.reason(
        query=f"Review these code changes for quality and security: {changes}",
        mode="technical"
    )
    return analysis.issues, analysis.recommendations
```

### Pattern 2: Task Planning Intelligence
```python
# Use AI for task breakdown and planning
def plan_complex_task(task_description):
    intelligence = SwarmIntelligenceManager()
    plan = intelligence.generate_task_plan(
        description=task_description,
        team_capabilities=["python", "ai", "coordination"],
        timeline_days=7
    )
    return plan.steps, plan.dependencies, plan.risks
```

### Pattern 3: Knowledge Discovery
```python
# Leverage semantic search for knowledge discovery
def find_relevant_knowledge(query, context):
    vdb = VectorDatabaseService()
    results = vdb.semantic_search(
        query=f"{query} in context of {context}",
        filters={"domain": "relevant_domain"},
        limit=15
    )
    return [r.content for r in results if r.score > 0.7]
```

---

## **Troubleshooting Quick Reference**

### Issue: Import Errors
```bash
# Check import path setup
python tools/import_path_fix.py --test

# Fix import paths
python tools/import_path_fix.py --fix
```

### Issue: AI Services Not Responding
```bash
# Check service health
python tools/ai_integration_status_checker.py --check-all

# Restart services
python src/main.py --services ai,vector-db
```

### Issue: Vector Database Connection
```bash
# Diagnose vector database
python tools/vector_db_troubleshooter.py --diagnose

# Test basic connectivity
python -c "from src.services.vector.vector_database_service import VectorDatabaseService; vdb = VectorDatabaseService(); print('Connected:', vdb.health_check())"
```

---

## **Next Steps for Advanced Utilization**

1. **Explore 5 Reasoning Modes**: `analytical`, `creative`, `technical`, `strategic`, `simple`
2. **Implement Caching**: Use response caching for frequently asked queries
3. **Batch Processing**: Leverage batch operations for multiple queries
4. **Custom Embeddings**: Fine-tune semantic search for your domain
5. **Integration Monitoring**: Track AI service usage with metrics

---

## **Success Metrics**

After following this guide, you should be able to:
- ✅ Make API calls to AI reasoning endpoints
- ✅ Perform semantic searches across the codebase
- ✅ Integrate AI capabilities into your workflows
- ✅ Utilize all 6 major AI services

**Time to AI Integration**: 5 minutes
**Infrastructure Status**: ✅ Complete & Ready
**Utilization Potential**: Transform any workflow with enterprise AI

---

*Quickstart Version: 1.0*
*Last Updated: 2026-01-08*
*AI Infrastructure: Fully Operational*