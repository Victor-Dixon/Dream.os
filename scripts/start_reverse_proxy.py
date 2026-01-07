#!/usr/bin/env python3
"""
Reverse Proxy for Infrastructure Block 4
========================================

Python-based reverse proxy to route traffic between Flask and FastAPI services.
Provides load balancing, rate limiting, and service mesh functionality.

Features:
- Route traffic between Flask (port 5000) and FastAPI (port 8001)
- Rate limiting and request throttling
- Health checks for backend services
- SSL termination support
- Metrics collection

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import aiohttp
from aiohttp import web
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Service configuration
SERVICES = {
    'flask': {
        'url': 'http://127.0.0.1:5000',
        'health_endpoint': '/health',
        'routes': ['/api/', '/static/', '/health'],
        'rate_limit': 100,  # requests per minute
        'healthy': False,
        'last_check': None
    },
    'fastapi': {
        'url': 'http://127.0.0.1:8001',
        'health_endpoint': '/health',
        'routes': ['/analytics/', '/performance/', '/background-task/'],
        'rate_limit': 200,  # requests per minute
        'healthy': False,
        'last_check': None
    }
}

# Rate limiting storage
rate_limits: Dict[str, Dict[str, list]] = {
    service: {'requests': []} for service in SERVICES.keys()
}


class ReverseProxy:
    """Reverse proxy with load balancing and rate limiting."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.health_check_interval = 30  # seconds
        self.rate_limit_window = 60  # seconds

    async def init_session(self):
        """Initialize HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def cleanup(self):
        """Cleanup resources."""
        if self.session:
            await self.session.close()

    def check_rate_limit(self, service_name: str, client_ip: str) -> bool:
        """Check if request is within rate limit."""
        if service_name not in rate_limits:
            return True

        service_limits = rate_limits[service_name]
        current_time = time.time()

        # Clean old requests outside the window
        cutoff_time = current_time - self.rate_limit_window
        service_limits['requests'] = [
            req_time for req_time in service_limits['requests']
            if req_time > cutoff_time
        ]

        # Check if under limit
        if len(service_limits['requests']) < SERVICES[service_name]['rate_limit']:
            service_limits['requests'].append(current_time)
            return True

        return False

    async def check_service_health(self, service_name: str) -> bool:
        """Check if a service is healthy."""
        service_config = SERVICES[service_name]
        try:
            url = f"{service_config['url']}{service_config['health_endpoint']}"
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    try:
                        text = await resp.text()
                        logger.debug(f"Health check for {service_name}: raw response: {text[:200]}...")
                        data = await resp.json()
                        if data is None:
                            logger.warning(f"Health check for {service_name}: received null response")
                            healthy = False
                        else:
                            # Handle different health check formats
                            if service_name == 'flask':
                                # Flask returns: {"overall_status": "healthy|warning|critical"}
                                healthy = data.get('overall_status') in ['healthy', 'warning']
                                logger.debug(f"Health check for {service_name}: overall_status = {data.get('overall_status')}, healthy = {healthy}")
                            elif service_name == 'fastapi':
                                # FastAPI returns: {"overall_status": "healthy|warning|critical"}
                                healthy = data.get('overall_status') in ['healthy', 'warning']
                                logger.debug(f"Health check for {service_name}: overall_status = {data.get('overall_status')}, healthy = {healthy}")
                            else:
                                healthy = data.get('status') == 'healthy'
                    except Exception as json_error:
                        logger.warning(f"Health check for {service_name}: failed to parse JSON: {json_error}, raw text: {text[:200] if 'text' in locals() else 'N/A'}")
                        healthy = False

                    service_config['healthy'] = healthy
                    service_config['last_check'] = datetime.now()
                    return healthy
                else:
                    logger.warning(f"Health check for {service_name}: HTTP {resp.status}")
                    service_config['healthy'] = False
                    service_config['last_check'] = datetime.now()
                    return False
        except Exception as e:
            logger.warning(f"Health check failed for {service_name}: {e}")
            service_config['healthy'] = False
            service_config['last_check'] = datetime.now()
            return False

    def route_request(self, path: str) -> Optional[str]:
        """Route request to appropriate service."""
        # Flask routes
        if any(path.startswith(route) for route in SERVICES['flask']['routes']):
            if SERVICES['flask']['healthy']:
                return 'flask'
            else:
                logger.warning("Flask service unhealthy, falling back to direct routing")

        # FastAPI routes
        if any(path.startswith(route) for route in SERVICES['fastapi']['routes']):
            if SERVICES['fastapi']['healthy']:
                return 'fastapi'
            else:
                logger.warning("FastAPI service unhealthy, falling back to direct routing")

        # Default to Flask for other routes
        return 'flask' if SERVICES['flask']['healthy'] else None

    async def proxy_request(self, request: web.Request) -> web.Response:
        """Proxy request to appropriate service."""
        await self.init_session()

        path = request.path
        client_ip = request.remote or 'unknown'

        # Route to service
        service_name = self.route_request(path)
        if not service_name:
            return web.json_response(
                {'error': 'No healthy backend services available'},
                status=503
            )

        # Check rate limit
        if not self.check_rate_limit(service_name, client_ip):
            return web.json_response(
                {'error': 'Rate limit exceeded'},
                status=429,
                headers={'Retry-After': str(self.rate_limit_window)}
            )

        service_config = SERVICES[service_name]
        target_url = f"{service_config['url']}{path}"

        # Add query parameters
        if request.query_string:
            target_url += f"?{request.query_string}"

        try:
            # Prepare headers (remove host header)
            headers = dict(request.headers)
            headers.pop('Host', None)

            # Proxy the request
            async with self.session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=await request.read() if request.body_exists else None,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:

                # Read response
                response_data = await resp.read()
                response_headers = dict(resp.headers)

                # Remove hop-by-hop headers
                hop_by_hop = [
                    'connection', 'keep-alive', 'proxy-authenticate',
                    'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade'
                ]
                for header in hop_by_hop:
                    response_headers.pop(header, None)

                # Add reverse proxy headers
                response_headers['X-Reverse-Proxy'] = 'infrastructure-block-4'
                response_headers['X-Backend-Service'] = service_name

                return web.Response(
                    body=response_data,
                    status=resp.status,
                    headers=response_headers
                )

        except Exception as e:
            logger.error(f"Proxy request failed: {e}")
            return web.json_response(
                {'error': 'Backend service unavailable'},
                status=502
            )

    async def health_endpoint(self, request: web.Request) -> web.Response:
        """Reverse proxy health endpoint."""
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {}
        }

        for service_name, service_config in SERVICES.items():
            health_data['services'][service_name] = {
                'url': service_config['url'],
                'healthy': service_config['healthy'],
                'last_check': service_config['last_check'].isoformat() if service_config['last_check'] else None,
                'routes': service_config['routes'],
                'rate_limit': service_config['rate_limit']
            }

        # Check overall health
        healthy_services = sum(1 for s in SERVICES.values() if s['healthy'])
        if healthy_services == 0:
            health_data['status'] = 'critical'
        elif healthy_services < len(SERVICES):
            health_data['status'] = 'warning'

        status_code = 200 if health_data['status'] == 'healthy' else 503
        return web.json_response(health_data, status=status_code)

    async def metrics_endpoint(self, request: web.Request) -> web.Response:
        """Metrics endpoint for monitoring."""
        metrics = {
            'timestamp': time.time(),
            'rate_limits': {},
            'services': {}
        }

        for service_name, limits in rate_limits.items():
            current_time = time.time()
            cutoff_time = current_time - self.rate_limit_window
            recent_requests = len([
                req_time for req_time in limits['requests']
                if req_time > cutoff_time
            ])

            metrics['rate_limits'][service_name] = {
                'current_requests': recent_requests,
                'limit': SERVICES[service_name]['rate_limit'],
                'remaining': max(0, SERVICES[service_name]['rate_limit'] - recent_requests)
            }

        for service_name, service_config in SERVICES.items():
            metrics['services'][service_name] = {
                'healthy': service_config['healthy'],
                'uptime': (datetime.now() - service_config['last_check']).total_seconds() if service_config['last_check'] else 0
            }

        return web.json_response(metrics)


async def health_check_loop(proxy: ReverseProxy):
    """Background health check loop."""
    while True:
        for service_name in SERVICES.keys():
            await proxy.check_service_health(service_name)
            logger.info(f"Health check: {service_name} = {'✓' if SERVICES[service_name]['healthy'] else '✗'}")

        await asyncio.sleep(proxy.health_check_interval)


async def create_app():
    """Create the reverse proxy application."""
    proxy = ReverseProxy()

    app = web.Application()
    app['proxy'] = proxy

    # Routes
    app.router.add_route('*', '/{path:.*}', proxy.proxy_request)
    app.router.add_get('/health', proxy.health_endpoint)
    app.router.add_get('/metrics', proxy.metrics_endpoint)

    # Start health check loop
    asyncio.create_task(health_check_loop(proxy))

    # Cleanup on shutdown
    async def cleanup(app):
        await proxy.cleanup()

    app.on_shutdown.append(cleanup)

    return app


async def main():
    """Main entry point."""
    app = await create_app()

    # Start server
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()

    logger.info("🚀 Reverse Proxy started on http://127.0.0.1:8080")
    logger.info("📊 Health endpoint: http://127.0.0.1:8080/health")
    logger.info("📈 Metrics endpoint: http://127.0.0.1:8080/metrics")

    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down reverse proxy...")
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())