#!/usr/bin/env python3
"""
Quantum Trading FastAPI Service - Phase 6 Revolutionary Trading Intelligence
=============================================================================

FastAPI service exposing quantum trading API for TradingRobotPlug integration.
Provides REST endpoints for quantum-enhanced trading signals and analytics.

<!-- SSOT Domain: quantum -->
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from src.quantum.quantum_trading_api import get_quantum_trading_api

logger = logging.getLogger(__name__)


# Pydantic models for API requests/responses
class MarketData(BaseModel):
    """Market data input model."""
    price: float = Field(..., description="Current price")
    volume: int = Field(..., description="Trading volume")
    change_percent: float = Field(..., description="Price change percentage")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    pe_ratio: Optional[float] = Field(None, description="Price-to-earnings ratio")
    volatility: Optional[float] = Field(None, description="Volatility index")


class TradingSignalRequest(BaseModel):
    """Trading signal request model."""
    symbol: str = Field(..., description="Trading symbol (e.g., 'AAPL', 'BTC/USD')")
    market_data: MarketData = Field(..., description="Current market data")


class MarketAnalysisRequest(BaseModel):
    """Market analysis request model."""
    symbol: str = Field(..., description="Trading symbol")
    market_data: MarketData = Field(..., description="Current market data")


class PortfolioHolding(BaseModel):
    """Portfolio holding model."""
    symbol: str = Field(..., description="Trading symbol")
    quantity: float = Field(..., description="Quantity held")
    current_price: float = Field(..., description="Current price per unit")


class PortfolioRequest(BaseModel):
    """Portfolio analysis request model."""
    holdings: List[PortfolioHolding] = Field(..., description="List of portfolio holdings")


class TradingSignalResponse(BaseModel):
    """Trading signal response model."""
    symbol: str
    action: str
    confidence: float
    quantum_amplification: float
    swarm_consensus: int
    risk_level: str
    timestamp: str
    reasoning: str


class MarketAnalysisResponse(BaseModel):
    """Market analysis response model."""
    symbol: str
    trend_direction: str
    volatility_index: float
    quantum_confidence: float
    swarm_prediction: str
    risk_assessment: Dict[str, Any]
    timestamp: str


class PortfolioResponse(BaseModel):
    """Portfolio analysis response model."""
    rebalancing_actions: List[Dict[str, Any]]
    risk_adjustments: List[Dict[str, Any]]
    quantum_opportunities: List[Dict[str, Any]]
    diversification_score: float
    overall_confidence: float


class TradingMetricsResponse(BaseModel):
    """Trading metrics response model."""
    signals_generated: int
    successful_predictions: int
    quantum_accuracy: float
    active_signals: int
    cached_analyses: int
    swarm_intelligence: Dict[str, Any]


# Global quantum trading API instance
quantum_api = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager for quantum API initialization."""
    global quantum_api

    # Startup: Initialize quantum trading API
    logger.info("🚀 Initializing Quantum Trading API...")
    try:
        quantum_api = await get_quantum_trading_api()
        logger.info("✅ Quantum Trading API initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Quantum Trading API: {e}")
        quantum_api = None

    yield

    # Shutdown: Cleanup if needed
    logger.info("🛑 Quantum Trading Service shutting down")


# Create FastAPI app
app = FastAPI(
    title="Quantum Trading API",
    description="Revolutionary quantum-enhanced trading intelligence for TradingRobotPlug",
    version="6.0.0",
    lifespan=lifespan
)

# Add CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Quantum Trading API",
        "version": "6.0.0",
        "description": "Revolutionary quantum-enhanced trading intelligence",
        "status": "operational" if quantum_api else "initializing",
        "endpoints": {
            "GET /": "API information",
            "POST /trading-signal": "Get quantum trading signal",
            "POST /market-analysis": "Get quantum market analysis",
            "POST /portfolio-analysis": "Get portfolio optimization",
            "GET /metrics": "Get trading performance metrics",
            "GET /health": "Service health check"
        }
    }


@app.post("/trading-signal", response_model=TradingSignalResponse)
async def get_trading_signal(request: TradingSignalRequest):
    """
    Get quantum-enhanced trading signal.

    Generates AI-powered trading recommendations using swarm intelligence
    and quantum coordination algorithms.
    """
    if not quantum_api:
        raise HTTPException(status_code=503, detail="Quantum Trading API not initialized")

    try:
        # Convert request to dict format
        market_data_dict = {
            'price': request.market_data.price,
            'volume': request.market_data.volume,
            'change_percent': request.market_data.change_percent,
            'market_cap': request.market_data.market_cap,
            'pe_ratio': request.market_data.pe_ratio
        }

        # Get quantum trading signal
        signal = await quantum_api.get_trading_signal(request.symbol, market_data_dict)

        # Convert to response format
        response = TradingSignalResponse(
            symbol=signal.symbol,
            action=signal.action,
            confidence=signal.confidence,
            quantum_amplification=signal.quantum_amplification,
            swarm_consensus=signal.swarm_consensus,
            risk_level=signal.risk_level,
            timestamp=signal.timestamp.isoformat(),
            reasoning=signal.reasoning
        )

        logger.info(f"⚡ Quantum signal generated for {request.symbol}: {signal.action} ({signal.confidence:.2f})")
        return response

    except Exception as e:
        logger.error(f"❌ Error generating trading signal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate trading signal: {str(e)}")


@app.post("/market-analysis", response_model=MarketAnalysisResponse)
async def get_market_analysis(request: MarketAnalysisRequest):
    """
    Get comprehensive quantum market analysis.

    Provides AI-driven market trend analysis with swarm consensus
    and quantum confidence scoring.
    """
    if not quantum_api:
        raise HTTPException(status_code=503, detail="Quantum Trading API not initialized")

    try:
        # Convert request to dict format
        market_data_dict = {
            'price': request.market_data.price,
            'volume': request.market_data.volume,
            'change_percent': request.market_data.change_percent,
            'market_cap': request.market_data.market_cap,
            'pe_ratio': request.market_data.pe_ratio
        }

        # Get quantum market analysis
        analysis = await quantum_api.get_market_analysis(request.symbol, market_data_dict)

        # Convert to response format
        response = MarketAnalysisResponse(
            symbol=analysis.symbol,
            trend_direction=analysis.trend_direction,
            volatility_index=analysis.volatility_index,
            quantum_confidence=analysis.quantum_confidence,
            swarm_prediction=analysis.swarm_prediction,
            risk_assessment=analysis.risk_assessment,
            timestamp=analysis.timestamp.isoformat()
        )

        logger.info(f"📊 Quantum analysis completed for {request.symbol}: {analysis.trend_direction}")
        return response

    except Exception as e:
        logger.error(f"❌ Error performing market analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze market: {str(e)}")


@app.post("/portfolio-analysis", response_model=PortfolioResponse)
async def get_portfolio_analysis(request: PortfolioRequest):
    """
    Get quantum portfolio optimization recommendations.

    Analyzes entire portfolio and provides AI-driven rebalancing
    and optimization suggestions.
    """
    if not quantum_api:
        raise HTTPException(status_code=503, detail="Quantum Trading API not initialized")

    try:
        # Convert request to dict format
        portfolio_dict = [
            {
                'symbol': holding.symbol,
                'quantity': holding.quantity,
                'current_price': holding.current_price
            }
            for holding in request.holdings
        ]

        # Get portfolio recommendations
        recommendations = await quantum_api.get_portfolio_recommendations(portfolio_dict)

        # Convert to response format
        response = PortfolioResponse(**recommendations)

        logger.info(f"💼 Portfolio analysis completed for {len(request.holdings)} holdings")
        return response

    except Exception as e:
        logger.error(f"❌ Error analyzing portfolio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze portfolio: {str(e)}")


@app.get("/metrics", response_model=TradingMetricsResponse)
async def get_trading_metrics():
    """
    Get comprehensive trading performance metrics.

    Returns real-time statistics on quantum trading performance,
    swarm intelligence effectiveness, and system health.
    """
    if not quantum_api:
        raise HTTPException(status_code=503, detail="Quantum Trading API not initialized")

    try:
        metrics = quantum_api.get_trading_metrics()
        response = TradingMetricsResponse(**metrics)

        return response

    except Exception as e:
        logger.error(f"❌ Error retrieving trading metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")


@app.get("/health")
async def health_check():
    """Service health check endpoint."""
    return {
        "status": "healthy" if quantum_api else "initializing",
        "timestamp": datetime.now().isoformat(),
        "service": "Quantum Trading API",
        "version": "6.0.0",
        "quantum_intelligence": "active" if quantum_api else "initializing",
        "uptime": "operational"
    }


@app.post("/batch-signals")
async def get_batch_trading_signals(requests: List[TradingSignalRequest]):
    """
    Get trading signals for multiple symbols in batch.

    Optimized for bulk analysis with quantum parallel processing.
    """
    if not quantum_api:
        raise HTTPException(status_code=503, detail="Quantum Trading API not initialized")

    try:
        results = []

        # Process signals concurrently for better performance
        tasks = []
        for req in requests:
            market_data_dict = {
                'price': req.market_data.price,
                'volume': req.market_data.volume,
                'change_percent': req.market_data.change_percent,
                'market_cap': req.market_data.market_cap,
                'pe_ratio': req.market_data.pe_ratio
            }

            task = quantum_api.get_trading_signal(req.symbol, market_data_dict)
            tasks.append(task)

        # Execute all tasks concurrently
        signals = await asyncio.gather(*tasks)

        # Convert to response format
        for req, signal in zip(requests, signals):
            response = TradingSignalResponse(
                symbol=signal.symbol,
                action=signal.action,
                confidence=signal.confidence,
                quantum_amplification=signal.quantum_amplification,
                swarm_consensus=signal.swarm_consensus,
                risk_level=signal.risk_level,
                timestamp=signal.timestamp.isoformat(),
                reasoning=signal.reasoning
            )
            results.append(response)

        logger.info(f"⚡ Batch quantum signals generated for {len(requests)} symbols")
        return {"signals": [signal.dict() for signal in results]}

    except Exception as e:
        logger.error(f"❌ Error in batch signal generation: {e}")
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")


def start_quantum_trading_service(host: str = "127.0.0.1", port: int = 8000):
    """
    Start the Quantum Trading FastAPI service.

    Args:
        host: Host address to bind to
        port: Port number to listen on
    """
    logger.info(f"🚀 Starting Quantum Trading Service on {host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        reload=False  # Disable reload for production
    )


if __name__ == "__main__":
    # Start the service directly
    start_quantum_trading_service()