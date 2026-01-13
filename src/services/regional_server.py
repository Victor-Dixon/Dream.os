#!/usr/bin/env python3
"""
Regional Server - Simple API Server
====================================

Provides basic regional information API endpoints.
Implements /api/regions and /api/regions/code/{code} endpoints.

V2 Compliant: Yes (<400 lines)
Author: Agent-8 (Quality Assurance & Tooling Specialist)
Date: 2026-01-08
"""

from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import uvicorn
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Regional Server",
    description="Simple API server for regional information",
    version="1.0.0"
)

# Sample regional data
REGIONS_DATA = {
    "US": {
        "name": "United States",
        "code": "US",
        "continent": "North America",
        "population": 331900000,
        "capital": "Washington, D.C.",
        "languages": ["English"],
        "currency": "USD"
    },
    "CA": {
        "name": "Canada",
        "code": "CA",
        "continent": "North America",
        "population": 38000000,
        "capital": "Ottawa",
        "languages": ["English", "French"],
        "currency": "CAD"
    },
    "GB": {
        "name": "United Kingdom",
        "code": "GB",
        "continent": "Europe",
        "population": 67000000,
        "capital": "London",
        "languages": ["English"],
        "currency": "GBP"
    },
    "DE": {
        "name": "Germany",
        "code": "DE",
        "continent": "Europe",
        "population": 83000000,
        "capital": "Berlin",
        "languages": ["German"],
        "currency": "EUR"
    },
    "FR": {
        "name": "France",
        "code": "FR",
        "continent": "Europe",
        "population": 67000000,
        "capital": "Paris",
        "languages": ["French"],
        "currency": "EUR"
    },
    "JP": {
        "name": "Japan",
        "code": "JP",
        "continent": "Asia",
        "population": 125800000,
        "capital": "Tokyo",
        "languages": ["Japanese"],
        "currency": "JPY"
    }
}


@app.get("/api/regions")
async def get_regions() -> List[Dict[str, Any]]:
    """
    Get all regions.

    Returns a list of all available regions with basic information.
    """
    regions_list = []
    for code, data in REGIONS_DATA.items():
        regions_list.append({
            "code": code,
            "name": data["name"],
            "continent": data["continent"],
            "population": data["population"]
        })

    logger.info(f"Returning {len(regions_list)} regions")
    return regions_list


@app.get("/api/regions/code/{code}")
async def get_region_by_code(code: str) -> Dict[str, Any]:
    """
    Get region information by country code.

    Args:
        code: Two-letter country code (e.g., 'US', 'CA', 'GB')

    Returns:
        Detailed region information

    Raises:
        HTTPException: If region code is not found
    """
    code_upper = code.upper()

    if code_upper not in REGIONS_DATA:
        logger.warning(f"Region code '{code}' not found")
        raise HTTPException(
            status_code=404,
            detail=f"Region with code '{code}' not found"
        )

    region_data = REGIONS_DATA[code_upper].copy()
    logger.info(f"Returning region data for {code_upper}: {region_data['name']}")
    return region_data


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns basic service health information.
    """
    return {
        "status": "healthy",
        "service": "regional-server",
        "version": "1.0.0"
    }


def start_server(host: str = "localhost", port: int = 5000):
    """
    Start the Regional Server.

    Args:
        host: Host to bind to (default: localhost)
        port: Port to bind to (default: 5000)
    """
    logger.info(f"Starting Regional Server on {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    # Start server on port 5001 since 5000 is already in use
    start_server(port=5001)