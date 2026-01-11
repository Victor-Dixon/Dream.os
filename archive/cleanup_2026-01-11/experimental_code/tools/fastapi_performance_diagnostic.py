#!/usr/bin/env python3
"""
FastAPI Performance Diagnostic Tool
====================================

<!-- SSOT Domain: infrastructure -->

Diagnoses FastAPI performance issues and provides optimization recommendations.

V2 Compliance | Author: Agent-4 | Date: 2026-01-07
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import psutil
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class PerformanceDiagnostic:
    """Comprehensive performance diagnostic result."""
    timestamp: str
    system_health: Dict[str, Any]
    fastapi_status: Dict[str, Any]
    endpoint_performance: Dict[str, Any]
    recommendations: List[str]
    alerts: List[str]


class FastAPIPerformanceDiagnostic:
    """
    Comprehensive diagnostic tool for FastAPI performance issues.

    Analyzes:
    - System resource usage
    - FastAPI server status
    - Endpoint response times
    - Database connections
    - Memory usage patterns
    """

    def __init__(self, fastapi_url: str = "http://localhost:8000"):
        self.fastapi_url = fastapi_url.rstrip('/')
        self.diagnostic_results: Optional[PerformanceDiagnostic] = None

    async def run_full_diagnostic(self) -> PerformanceDiagnostic:
        """
        Run comprehensive FastAPI performance diagnostic.

        Returns:
            Complete performance diagnostic results
        """
        logger.info("🔍 Starting FastAPI performance diagnostic...")

        # Run all diagnostic checks in parallel
        tasks = [
            self._check_system_health(),
            self._check_fastapi_status(),
            self._test_endpoint_performance(),
            self._analyze_resource_usage()
        ]

        results = await asyncio.gather(*tasks)

        # Unpack results
        system_health, fastapi_status, endpoint_perf, resource_analysis = results

        # Generate recommendations and alerts
        recommendations = self._generate_recommendations(system_health, fastapi_status, endpoint_perf)
        alerts = self._generate_alerts(system_health, fastapi_status, endpoint_perf)

        diagnostic = PerformanceDiagnostic(
            timestamp=datetime.now().isoformat(),
            system_health=system_health,
            fastapi_status=fastapi_status,
            endpoint_performance=endpoint_perf,
            recommendations=recommendations,
            alerts=alerts
        )

        self.diagnostic_results = diagnostic

        logger.info("✅ FastAPI performance diagnostic complete")

        return diagnostic

    async def _check_system_health(self) -> Dict[str, Any]:
        """Check overall system health metrics."""
        logger.debug("Checking system health...")

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "usage_percent": memory.percent
        }

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_usage = {
            "total_gb": round(disk.total / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "usage_percent": disk.percent
        }

        # Network connections
        connections = psutil.net_connections()
        listening_ports = [conn.laddr.port for conn in connections
                          if conn.status == 'LISTEN' and conn.laddr]

        return {
            "cpu_usage_percent": cpu_percent,
            "memory": memory_usage,
            "disk": disk_usage,
            "listening_ports": listening_ports,
            "fastapi_ports": [8000, 8001],  # Common FastAPI ports
            "health_score": self._calculate_system_health_score(cpu_percent, memory.percent, disk.percent)
        }

    async def _check_fastapi_status(self) -> Dict[str, Any]:
        """Check FastAPI server status and configuration."""
        logger.debug("Checking FastAPI server status...")

        status_info = {
            "server_running": False,
            "health_endpoint": None,
            "response_time": None,
            "server_info": None,
            "error": None
        }

        try:
            start_time = time.time()

            # Try multiple common FastAPI ports
            for port in [8000, 8001, 5000]:
                try:
                    url = f"http://localhost:{port}/health"
                    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                        async with session.get(url) as response:
                            response_time = time.time() - start_time

                            if response.status == 200:
                                status_info.update({
                                    "server_running": True,
                                    "health_endpoint": url,
                                    "response_time": round(response_time, 3),
                                    "server_info": {
                                        "port": port,
                                        "status_code": response.status,
                                        "headers": dict(response.headers)
                                    }
                                })
                                break
                            else:
                                status_info["error"] = f"Health endpoint returned status {response.status}"

                except aiohttp.ClientConnectorError:
                    continue  # Try next port
                except Exception as e:
                    status_info["error"] = f"Connection error: {e}"
                    break

        except Exception as e:
            status_info["error"] = f"Diagnostic error: {e}"

        return status_info

    async def _test_endpoint_performance(self) -> Dict[str, Any]:
        """Test performance of key FastAPI endpoints."""
        logger.debug("Testing endpoint performance...")

        endpoints = [
            "/health",
            "/docs",
            "/openapi.json",
            "/trades",
            "/strategies"
        ]

        results = {}

        for endpoint in endpoints:
            result = await self._test_single_endpoint(endpoint)
            results[endpoint] = result

        # Calculate performance summary
        response_times = [r.get("response_time", 0) for r in results.values() if r.get("success")]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        slow_endpoints = [ep for ep, result in results.items()
                         if result.get("response_time", 0) > 2.0]

        return {
            "endpoint_results": results,
            "summary": {
                "total_endpoints": len(endpoints),
                "successful_endpoints": sum(1 for r in results.values() if r.get("success")),
                "failed_endpoints": sum(1 for r in results.values() if not r.get("success")),
                "average_response_time": round(avg_response_time, 3),
                "slow_endpoints": slow_endpoints,
                "slow_count": len(slow_endpoints)
            }
        }

    async def _test_single_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Test a single endpoint performance."""
        result = {
            "endpoint": endpoint,
            "success": False,
            "response_time": None,
            "status_code": None,
            "error": None
        }

        try:
            start_time = time.time()
            url = f"{self.fastapi_url}{endpoint}"

            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    response_time = time.time() - start_time

                    result.update({
                        "success": True,
                        "response_time": round(response_time, 3),
                        "status_code": response.status
                    })

        except Exception as e:
            result["error"] = str(e)

        return result

    async def _analyze_resource_usage(self) -> Dict[str, Any]:
        """Analyze system resource usage patterns."""
        logger.debug("Analyzing resource usage...")

        # Get process information for Python/FastAPI processes
        python_processes = []
        fastapi_processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    python_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent'],
                        'cmdline': proc.info['cmdline']
                    })

                    # Check if it's likely a FastAPI process
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(keyword in cmdline.lower() for keyword in ['fastapi', 'uvicorn', 'main:app']):
                        fastapi_processes.append(proc.info)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return {
            "python_processes": python_processes,
            "fastapi_processes": fastapi_processes,
            "process_count": len(python_processes),
            "fastapi_process_count": len(fastapi_processes)
        }

    def _calculate_system_health_score(self, cpu: float, memory: float, disk: float) -> float:
        """Calculate overall system health score (0-100)."""
        # Weights: CPU 30%, Memory 40%, Disk 30%
        cpu_score = max(0, 100 - cpu * 2)  # Penalize high CPU
        memory_score = max(0, 100 - memory * 1.5)  # Penalize high memory usage
        disk_score = max(0, 100 - disk * 2)  # Penalize high disk usage

        return round((cpu_score * 0.3 + memory_score * 0.4 + disk_score * 0.3), 1)

    def _generate_recommendations(self, system: Dict, fastapi: Dict, endpoints: Dict) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []

        # System-level recommendations
        if system.get("cpu_usage_percent", 0) > 80:
            recommendations.append("⚡ HIGH CPU usage detected - consider optimizing FastAPI worker processes")

        if system.get("memory", {}).get("usage_percent", 0) > 85:
            recommendations.append("🧠 High memory usage - check for memory leaks in FastAPI application")

        if system.get("disk", {}).get("usage_percent", 0) > 90:
            recommendations.append("💾 Critical disk space - clear logs and temporary files")

        # FastAPI-specific recommendations
        if not fastapi.get("server_running"):
            recommendations.append("🚨 FastAPI server not running - check server startup and configuration")
            return recommendations  # Can't provide other recommendations if server is down

        if fastapi.get("response_time", 0) > 2.0:
            recommendations.append("🐌 Slow health endpoint - optimize database connections and middleware")

        # Endpoint performance recommendations
        summary = endpoints.get("summary", {})
        if summary.get("slow_endpoints"):
            slow_count = len(summary["slow_endpoints"])
            recommendations.append(f"📊 {slow_count} endpoints responding slowly - implement caching and database optimization")

        if summary.get("failed_endpoints", 0) > 0:
            failed_count = summary["failed_endpoints"]
            recommendations.append(f"❌ {failed_count} endpoints failing - check database connectivity and error handling")

        # Resource usage recommendations
        fastapi_processes = system.get("fastapi_processes", [])
        if len(fastapi_processes) == 0:
            recommendations.append("🔍 No FastAPI processes found - verify server is running with correct startup command")
        elif len(fastapi_processes) > 1:
            recommendations.append("⚠️ Multiple FastAPI processes detected - ensure proper load balancing")

        return recommendations or ["✅ System performing well - no immediate optimizations needed"]

    def _generate_alerts(self, system: Dict, fastapi: Dict, endpoints: Dict) -> List[str]:
        """Generate critical alerts requiring immediate attention."""
        alerts = []

        # Critical system alerts
        if system.get("memory", {}).get("usage_percent", 0) > 95:
            alerts.append("🚨 CRITICAL: Memory usage >95% - immediate action required")

        if system.get("disk", {}).get("usage_percent", 0) > 95:
            alerts.append("🚨 CRITICAL: Disk space <5% - system stability at risk")

        # FastAPI alerts
        if not fastapi.get("server_running"):
            alerts.append("🚨 CRITICAL: FastAPI server is not running")

        if fastapi.get("response_time", 0) > 10.0:
            alerts.append("🚨 CRITICAL: Health endpoint >10s - server may be unresponsive")

        # Endpoint alerts
        summary = endpoints.get("summary", {})
        failed_count = summary.get("failed_endpoints", 0)
        if failed_count > 2:
            alerts.append(f"🚨 CRITICAL: {failed_count} endpoints failing - service degradation")

        return alerts or ["✅ No critical alerts - system operating normally"]


async def main():
    """Command-line interface for FastAPI performance diagnostic."""
    import argparse

    parser = argparse.ArgumentParser(description="FastAPI Performance Diagnostic Tool")
    parser.add_argument("--url", type=str, default="http://localhost:8000",
                       help="FastAPI server URL (default: http://localhost:8000)")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    # Run diagnostic
    diagnostic = FastAPIPerformanceDiagnostic(args.url)
    result = await diagnostic.run_full_diagnostic()

    # Output results
    if args.json:
        output = json.dumps(asdict(result), indent=2)
    else:
        output = f"""
🔍 FASTAPI PERFORMANCE DIAGNOSTIC REPORT
=========================================

📊 System Health:
- CPU Usage: {result.system_health.get('cpu_usage_percent', 'N/A')}%
- Memory: {result.system_health.get('memory', {}).get('usage_percent', 'N/A')}% used ({result.system_health.get('memory', {}).get('used_gb', 'N/A')}GB/{result.system_health.get('memory', {}).get('total_gb', 'N/A')}GB)
- Disk: {result.system_health.get('disk', {}).get('usage_percent', 'N/A')}% used ({result.system_health.get('disk', {}).get('free_gb', 'N/A')}GB free)
- Health Score: {result.system_health.get('health_score', 'N/A')}/100

🚀 FastAPI Status:
- Server Running: {'✅ YES' if result.fastapi_status.get('server_running') else '❌ NO'}
- Health Endpoint: {result.fastapi_status.get('health_endpoint', 'N/A')}
- Response Time: {result.fastapi_status.get('response_time', 'N/A')}s
- Error: {result.fastapi_status.get('error', 'None')}

📈 Endpoint Performance:
- Total Endpoints Tested: {result.endpoint_performance.get('summary', {}).get('total_endpoints', 0)}
- Successful: {result.endpoint_performance.get('summary', {}).get('successful_endpoints', 0)}
- Failed: {result.endpoint_performance.get('summary', {}).get('failed_endpoints', 0)}
- Average Response Time: {result.endpoint_performance.get('summary', {}).get('average_response_time', 'N/A')}s
- Slow Endpoints (>2s): {len(result.endpoint_performance.get('summary', {}).get('slow_endpoints', []))}

🚨 Critical Alerts:
{chr(10).join(f"  • {alert}" for alert in result.alerts)}

💡 Recommendations:
{chr(10).join(f"  • {rec}" for rec in result.recommendations)}

📅 Report Generated: {result.timestamp}
"""

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ Diagnostic report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    asyncio.run(main())