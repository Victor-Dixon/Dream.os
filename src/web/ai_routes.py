#!/usr/bin/env python3
"""
AI Routes - Modular FastAPI Routes
===================================

<!-- SSOT Domain: web -->

AI-related API routes extracted from monolithic fastapi_app.py.

V2 Compliant: Modular routes
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    suggestions: Optional[List[str]] = None

class ReasoningRequest(BaseModel):
    query: str
    mode: Optional[str] = "analytical"
    format: Optional[str] = "text"
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ReasoningResponse(BaseModel):
    response: str
    confidence: float
    reasoning_steps: List[str]
    sources: List[str]
    tokens_used: int
    processing_time: float
    metadata: Dict[str, Any]

class SemanticSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10
    use_reasoning: Optional[bool] = True
    context: Optional[Dict[str, Any]] = None

class SemanticSearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_found: int
    query_enhanced: bool
    processing_time: float

# Router
router = APIRouter()

# AI Service dependency (placeholder - would be injected)
ai_service = None
try:
    from src.services.ai_service import AIService
    ai_service = AIService()
except ImportError:
    logger.warning("⚠️ AI service not available - using mock responses")

@router.post("/chat")
async def chat_endpoint(message: ChatMessage, background_tasks: BackgroundTasks):
    """AI chat endpoint."""
    try:
        if not ai_service:
            # Mock response for development
            return ChatResponse(
                response="AI service not configured. This is a mock response.",
                conversation_id=message.conversation_id or "mock-conversation",
                suggestions=["Try configuring the AI service", "Check service dependencies"]
            )

        # Real AI service integration
        response = await ai_service.generate_response(
            message=message.message,
            conversation_id=message.conversation_id,
            context=message.context
        )

        return ChatResponse(
            response=response.get("content", "No response generated"),
            conversation_id=response.get("conversation_id", message.conversation_id),
            suggestions=response.get("suggestions", [])
        )

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.post("/chat/new")
async def new_chat_session():
    """Create new chat session."""
    try:
        if ai_service:
            session_id = await ai_service.create_session()
        else:
            # Mock session creation
            import uuid
            session_id = str(uuid.uuid4())

        return {
            "session_id": session_id,
            "status": "created",
            "message": "New chat session initialized"
        }

    except Exception as e:
        logger.error(f"New chat session error: {e}")
        raise HTTPException(status_code=500, detail=f"Session creation error: {str(e)}")

@router.get("/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """Get chat history for conversation."""
    try:
        if ai_service:
            history = await ai_service.get_history(conversation_id)
        else:
            # Mock history
            history = [
                {"role": "system", "content": "Mock chat history", "timestamp": "2026-01-08T00:00:00Z"}
            ]

        return {
            "conversation_id": conversation_id,
            "history": history,
            "count": len(history)
        }

    except Exception as e:
        logger.error(f"Chat history error: {e}")
        raise HTTPException(status_code=500, detail=f"History retrieval error: {str(e)}")

@router.post("/reason", response_model=ReasoningResponse)
async def reason_endpoint(request: ReasoningRequest):
    """Advanced reasoning endpoint using the AI reasoning engine."""
    try:
        # Import reasoning engine
        from src.ai_training.dreamvault.advanced_reasoning import (
            AdvancedReasoningEngine,
            ReasoningContext,
            ReasoningMode,
            ResponseFormat
        )

        # Map string modes to enums
        mode_map = {
            "simple": ReasoningMode.SIMPLE,
            "analytical": ReasoningMode.ANALYTICAL,
            "creative": ReasoningMode.CREATIVE,
            "technical": ReasoningMode.TECHNICAL,
            "strategic": ReasoningMode.STRATEGIC
        }

        format_map = {
            "text": ResponseFormat.TEXT,
            "json": ResponseFormat.JSON,
            "markdown": ResponseFormat.MARKDOWN,
            "structured": ResponseFormat.STRUCTURED
        }

        # Create reasoning engine
        engine = AdvancedReasoningEngine()

        # Create reasoning context
        context = ReasoningContext(
            query=request.query,
            mode=mode_map.get(request.mode, ReasoningMode.ANALYTICAL),
            format=format_map.get(request.format, ResponseFormat.TEXT),
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            context_data=request.context
        )

        # Perform reasoning
        result = engine.reason(context)

        return ReasoningResponse(
            response=result.response,
            confidence=result.confidence,
            reasoning_steps=result.reasoning_steps,
            sources=result.sources,
            tokens_used=result.tokens_used,
            processing_time=result.processing_time,
            metadata=result.metadata
        )

    except Exception as e:
        logger.error(f"Reasoning endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Reasoning error: {str(e)}")

@router.post("/reason/stream")
async def reason_stream_endpoint(request: ReasoningRequest):
    """Streaming reasoning endpoint for real-time responses."""
    try:
        # Import reasoning engine
        from src.ai_training.dreamvault.advanced_reasoning import (
            AdvancedReasoningEngine,
            ReasoningContext,
            ReasoningMode,
            ResponseFormat
        )

        async def generate_response():
            # Map modes and formats
            mode_map = {
                "simple": ReasoningMode.SIMPLE,
                "analytical": ReasoningMode.ANALYTICAL,
                "creative": ReasoningMode.CREATIVE,
                "technical": ReasoningMode.TECHNICAL,
                "strategic": ReasoningMode.STRATEGIC
            }

            format_map = {
                "text": ResponseFormat.TEXT,
                "json": ResponseFormat.JSON,
                "markdown": ResponseFormat.MARKDOWN,
                "structured": ResponseFormat.STRUCTURED
            }

            # Create reasoning context
            context = ReasoningContext(
                query=request.query,
                mode=mode_map.get(request.mode, ReasoningMode.ANALYTICAL),
                format=format_map.get(request.format, ResponseFormat.TEXT),
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                context_data=request.context
            )

            # Perform reasoning
            engine = AdvancedReasoningEngine()
            result = engine.reason(context)

            # Stream response chunks
            response_chunks = result.response.split(' ')
            for i, chunk in enumerate(response_chunks):
                if i > 0:
                    yield ' '

                # Send metadata with first chunk
                if i == 0:
                    metadata = {
                        "confidence": result.confidence,
                        "reasoning_steps": result.reasoning_steps,
                        "tokens_used": result.tokens_used,
                        "processing_time": result.processing_time
                    }
                    yield f"data: {json.dumps({'chunk': chunk, 'metadata': metadata})}\n\n"
                else:
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            # Send completion signal
            yield f"data: {json.dumps({'done': True})}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"}
        )

    except Exception as e:
        logger.error(f"Streaming reasoning endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Streaming reasoning error: {str(e)}")

@router.post("/semantic-search", response_model=SemanticSearchResponse)
async def semantic_search_endpoint(request: SemanticSearchRequest):
    """AI-powered semantic search endpoint."""
    try:
        # Import vector database service
        from src.services.vector.vector_database_service import VectorDatabaseService

        # Create vector service
        vector_service = VectorDatabaseService()

        # Perform semantic search
        results = vector_service.semantic_search(
            query=request.query,
            limit=request.limit,
            use_reasoning=request.use_reasoning,
            context=request.context
        )

        return SemanticSearchResponse(
            results=results.get("results", []),
            total_found=results.get("total_found", 0),
            query_enhanced=results.get("query_enhanced", False),
            processing_time=results.get("processing_time", 0.0)
        )

    except Exception as e:
        logger.error(f"Semantic search endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Semantic search error: {str(e)}")

@router.get("/reason/stats")
async def reasoning_stats_endpoint():
    """Get reasoning engine performance statistics."""
    try:
        from src.ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine

        engine = AdvancedReasoningEngine()
        stats = engine.get_performance_stats()

        return {
            "status": "operational" if stats["llm_available"] else "degraded",
            "cache_size": stats["cache_size"],
            "llm_available": stats["llm_available"],
            "default_model": stats["default_model"],
            "supported_modes": stats["supported_modes"],
            "supported_formats": stats["supported_formats"],
            "cache_ttl_seconds": stats["cache_ttl"]
        }

    except Exception as e:
        logger.error(f"Reasoning stats endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Stats retrieval error: {str(e)}")

logger.info("✅ AI routes module initialized with reasoning endpoints")

__all__ = ["router"]