#!/usr/bin/env python3
"""
Phase 5 Infrastructure Health Check Tool
Comprehensive validation of enterprise infrastructure components
"""

import asyncio
import aiohttp
import psycopg2
import redis
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class HealthCheckResult:
    service: str
    status: str
    response_time: float
    details: Dict
    timestamp: str

class Phase5HealthChecker:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        self.previous_results = []  # Track trends over multiple runs

    async def check_service_health(self, service_name: str, url: str, timeout: int = 10) -> HealthCheckResult:
        """Check HTTP service health"""
        start_time = datetime.now()

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.get(url) as response:
                    response_time = (datetime.now() - start_time).total_seconds() * 1000

                    if response.status == 200:
                        status = "HEALTHY"
                        details = {
                            "status_code": response.status,
                            "content_type": response.headers.get('Content-Type', 'N/A'),
                            "server": response.headers.get('Server', 'N/A')
                        }
                    else:
                        status = "UNHEALTHY"
                        details = {
                            "status_code": response.status,
                            "error": f"HTTP {response.status}"
                        }
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            status = "UNHEALTHY"
            details = {"error": str(e)}

        return HealthCheckResult(
            service=service_name,
            status=status,
            response_time=round(response_time, 2),
            details=details,
            timestamp=datetime.now().isoformat()
        )

    def check_postgresql_health(self) -> HealthCheckResult:
        """Check PostgreSQL database health"""
        start_time = datetime.now()

        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="tradingrobotplug",
                user="postgres",
                password="postgres"
            )

            cursor = conn.cursor()
            cursor.execute("SELECT version(), current_database(), pg_postmaster_start_time()")
            version, database, start_time_db = cursor.fetchone()

            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
            active_connections = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            response_time = (datetime.now() - start_time).total_seconds() * 1000
            status = "HEALTHY"
            details = {
                "version": version.split()[1],
                "database": database,
                "active_connections": active_connections,
                "uptime": str(datetime.now() - start_time_db)
            }

        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            status = "UNHEALTHY"
            details = {"error": str(e)}

        return HealthCheckResult(
            service="PostgreSQL",
            status=status,
            response_time=round(response_time, 2),
            details=details,
            timestamp=datetime.now().isoformat()
        )

    def check_redis_health(self) -> HealthCheckResult:
        """Check Redis cache health"""
        start_time = datetime.now()

        try:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            info = r.info()

            response_time = (datetime.now() - start_time).total_seconds() * 1000
            status = "HEALTHY"
            details = {
                "version": info.get('redis_version', 'N/A'),
                "uptime_days": info.get('uptime_in_days', 0),
                "connected_clients": info.get('connected_clients', 0),
                "used_memory_human": info.get('used_memory_human', 'N/A'),
                "total_connections_received": info.get('total_connections_received', 0)
            }

            r.close()

        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            status = "UNHEALTHY"
            details = {"error": str(e)}

        return HealthCheckResult(
            service="Redis",
            status=status,
            response_time=round(response_time, 2),
            details=details,
            timestamp=datetime.now().isoformat()
        )

    def check_ssl_certificates(self) -> HealthCheckResult:
        """Check SSL certificate validity"""
        start_time = datetime.now()

        try:
            import ssl
            import socket

            context = ssl.create_default_context()
            with socket.create_connection(("localhost", 8080)) as sock:
                with context.wrap_socket(sock, server_hostname="localhost") as ssock:
                    cert = ssock.getpeercert()

                    # Check certificate validity
                    import datetime
                    not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_remaining = (not_after - datetime.datetime.now()).days

                    response_time = (datetime.now() - start_time).total_seconds() * 1000
                    status = "HEALTHY" if days_remaining > 30 else "WARNING"
                    details = {
                        "issuer": dict(cert['issuer'][0]),
                        "subject": dict(cert['subject'][0]),
                        "not_after": cert['notAfter'],
                        "days_remaining": days_remaining,
                        "cipher": ssock.cipher()
                    }

        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            status = "UNHEALTHY"
            details = {"error": str(e)}

        return HealthCheckResult(
            service="SSL Certificate",
            status=status,
            response_time=round(response_time, 2),
            details=details,
            timestamp=datetime.now().isoformat()
        )

    async def run_comprehensive_check(self) -> Dict:
        """Run comprehensive health check of all Phase 5 components"""
        logger.info("🚀 Starting Phase 5 Infrastructure Health Check...")

        # Define services to check
        services = [
            ("FastAPI", "http://localhost:8001/health"),
            ("Flask App", "http://localhost:5000/health"),
            ("Kong Gateway", "http://localhost:8000/status"),
            ("Nginx Reverse Proxy", "http://localhost:8080/health"),
            ("Prometheus", "http://localhost:9090/-/healthy"),
            ("Grafana", "http://localhost:3000/api/health"),
        ]

        # Run HTTP service checks concurrently
        http_checks = [self.check_service_health(name, url) for name, url in services]
        http_results = await asyncio.gather(*http_checks)

        # Run database checks in thread pool
        with ThreadPoolExecutor(max_workers=2) as executor:
            loop = asyncio.get_event_loop()
            postgres_future = loop.run_in_executor(executor, self.check_postgresql_health)
            redis_future = loop.run_in_executor(executor, self.check_redis_health)
            ssl_future = loop.run_in_executor(executor, self.check_ssl_certificates)

            db_results = await asyncio.gather(postgres_future, redis_future, ssl_future)

        # Combine all results
        all_results = http_results + list(db_results)
        self.results = all_results

        # Calculate summary statistics
        total_checks = len(all_results)
        healthy_count = len([r for r in all_results if r.status == "HEALTHY"])
        unhealthy_count = len([r for r in all_results if r.status == "UNHEALTHY"])
        warning_count = len([r for r in all_results if r.status == "WARNING"])

        avg_response_time = sum(r.response_time for r in all_results) / total_checks

        summary = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "total_services": total_checks,
            "healthy_services": healthy_count,
            "unhealthy_services": unhealthy_count,
            "warning_services": warning_count,
            "average_response_time_ms": round(avg_response_time, 2),
            "overall_status": "HEALTHY" if unhealthy_count == 0 and warning_count == 0 else
                           "WARNING" if unhealthy_count == 0 else "UNHEALTHY"
        }

        # Analyze trends
        trends = self.analyze_trends()

        return {
            "summary": summary,
            "results": [asdict(result) for result in all_results],
            "trends": trends
        }

    def analyze_trends(self) -> Dict:
        """Analyze health trends across multiple runs"""
        if len(self.previous_results) < 2:
            return {"trend_available": False, "message": "Need at least 2 runs for trend analysis"}

        current_summary = self.results
        previous_summary = self.previous_results[-1]

        # Compare key metrics
        trends = {
            "trend_available": True,
            "response_time_change": current_summary["avg_response_time"] - previous_summary.get("avg_response_time", 0),
            "success_rate_change": current_summary["avg_success_rate"] - previous_summary.get("avg_success_rate", 0),
            "healthy_services_change": len([r for r in self.results if r["status"] == "HEALTHY"]) -
                                     len([r for r in previous_summary.get("results", []) if r.get("status") == "HEALTHY"]),
            "analysis": "stable"
        }

        # Determine trend
        if trends["response_time_change"] > 50:  # Response time increased significantly
            trends["analysis"] = "degrading"
        elif trends["response_time_change"] < -20:  # Response time improved
            trends["analysis"] = "improving"
        elif trends["success_rate_change"] < -5:  # Success rate dropped
            trends["analysis"] = "concerning"
        elif trends["healthy_services_change"] > 0:  # More healthy services
            trends["analysis"] = "improving"
        elif trends["healthy_services_change"] < 0:  # Fewer healthy services
            trends["analysis"] = "degrading"

        return trends

    def save_trend_data(self, data: Dict):
        """Save current results for trend analysis"""
        summary = {
            "timestamp": data["summary"]["timestamp"],
            "avg_response_time": data["summary"]["average_response_time_ms"],
            "avg_success_rate": data["summary"]["average_success_rate"],
            "results": [{"service": r["service"], "status": r["status"]} for r in data["results"]]
        }
        self.previous_results.append(summary)

        # Keep only last 10 runs for trend analysis
        if len(self.previous_results) > 10:
            self.previous_results.pop(0)

    def print_report(self, data: Dict):
        """Print comprehensive health check report"""
        print("\n" + "="*80)
        print("🏥 PHASE 5 INFRASTRUCTURE HEALTH CHECK REPORT")
        print("="*80)

        summary = data["summary"]
        print(f"📊 OVERALL STATUS: {summary['overall_status']}")
        print(f"⏱️  CHECK DURATION: {summary['duration_seconds']:.2f} seconds")
        print(f"📈 SERVICES CHECKED: {summary['total_services']}")
        print(f"✅ HEALTHY: {summary['healthy_services']}")
        print(f"⚠️  WARNING: {summary['warning_services']}")
        print(f"❌ UNHEALTHY: {summary['unhealthy_services']}")
        print(f"⚡ AVG RESPONSE TIME: {summary['avg_response_time_ms']:.2f}ms")
        print(f"📊 AVG SUCCESS RATE: {summary['avg_success_rate']:.1f}%")
        print("\n" + "-"*80)
        print("📋 SERVICE DETAILS")
        print("-"*80)

        for result in data["results"]:
            status_emoji = "✅" if result["status"] == "HEALTHY" else "⚠️" if result["status"] == "WARNING" else "❌"
            print(f"{status_emoji} {result['service']:<20} | {result['status']:<8} | {result['response_time']:>6.1f}ms")
            if result["details"].get("error"):
                print(f"   Error: {result['details']['error']}")

        # Print trend analysis if available
        if data.get('trends', {}).get('trend_available'):
            print("\n" + "-"*80)
            print("📈 TREND ANALYSIS")
            print("-"*80)
            trends = data['trends']
            if trends['analysis'] == 'improving':
                print("📈 TREND: Improving performance")
            elif trends['analysis'] == 'degrading':
                print("📉 TREND: Performance degrading")
            elif trends['analysis'] == 'concerning':
                print("⚠️  TREND: Concerning degradation")
            else:
                print("➡️  TREND: Stable performance")

            if abs(trends['response_time_change']) > 10:
                direction = "increased" if trends['response_time_change'] > 0 else "decreased"
                print(f"⚡ Response time {direction} by {abs(trends['response_time_change']):.1f}ms")

            if abs(trends['success_rate_change']) > 2:
                direction = "increased" if trends['success_rate_change'] > 0 else "decreased"
                print(f"📊 Success rate {direction} by {abs(trends['success_rate_change']):.1f}%")

            if trends['healthy_services_change'] != 0:
                direction = "more" if trends['healthy_services_change'] > 0 else "fewer"
                print(f"📈 {abs(trends['healthy_services_change'])} {direction} healthy services")
        else:
            print("\n" + "-"*80)
            print("📈 TREND ANALYSIS: Run multiple times for trend data")
            print("-"*80)

        print("\n" + "="*80)

    def save_report(self, data: Dict, filename: str = None):
        """Save health check report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase5_health_check_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"📄 Report saved to: {filename}")

async def main():
    """Main execution function"""
    checker = Phase5HealthChecker()

    try:
        results = await checker.run_comprehensive_check()
        checker.save_trend_data(results)  # Save for trend analysis
        checker.print_report(results)
        checker.save_report(results)

        # Exit with appropriate code based on health status
        summary = results["summary"]
        if summary["unhealthy_services"] > 0:
            sys.exit(1)  # Critical failures
        elif summary["warning_services"] > 0:
            sys.exit(2)  # Warnings present
        else:
            sys.exit(0)  # All healthy

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())