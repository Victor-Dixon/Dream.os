#!/usr/bin/env python3
"""
Revenue Engine Production Deployment Verification
Infrastructure Block 4 + Block 5 Integration
Agent-3 (Infrastructure & DevOps) - 2026-01-07

Comprehensive verification of Revenue Engine production deployment.
Validates all infrastructure components and application functionality.
"""

import requests
import time
import json
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | VERIFY | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

class RevenueEngineVerifier:
    """Revenue Engine production deployment verifier."""

    def __init__(self, base_url: str = "https://revenue-engine.tradingrobotplug.com"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = True  # SSL verification
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": base_url,
            "tests": [],
            "summary": {"passed": 0, "failed": 0, "total": 0}
        }

    def log_test_result(self, test_name: str, passed: bool,
                       response_time: float, details: Dict = None):
        """Log individual test result."""
        result = {
            "test": test_name,
            "passed": passed,
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }

        self.results["tests"].append(result)

        if passed:
            self.results["summary"]["passed"] += 1
            logger.info(f"✅ {test_name}: {response_time*1000:.1f}ms")
        else:
            self.results["summary"]["failed"] += 1
            logger.error(f"❌ {test_name}: {response_time*1000:.1f}ms - {details}")

        self.results["summary"]["total"] += 1

    def make_request(self, endpoint: str, method: str = "GET",
                    headers: Dict = None, data: Dict = None,
                    expected_status: int = 200) -> Tuple[bool, float, Dict]:
        """Make HTTP request and measure response time."""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers or {},
                json=data,
                timeout=10
            )

            response_time = time.time() - start_time

            success = response.status_code == expected_status
            details = {
                "status_code": response.status_code,
                "expected": expected_status,
                "content_length": len(response.content),
                "headers": dict(response.headers)
            }

            # Add error details if failed
            if not success:
                try:
                    error_data = response.json()
                    details["error"] = error_data
                except:
                    details["error"] = response.text[:200]

            return success, response_time, details

        except Exception as e:
            response_time = time.time() - start_time
            return False, response_time, {"error": str(e), "exception": type(e).__name__}

    def test_health_endpoints(self) -> bool:
        """Test all health and monitoring endpoints."""
        logger.info("🔍 Testing Health Endpoints")

        endpoints = [
            ("/health", "Application Health"),
            ("/api/v1/health", "API Health"),
            ("/metrics", "Prometheus Metrics"),
            ("/status", "Service Status")
        ]

        all_passed = True
        for endpoint, description in endpoints:
            success, response_time, details = self.make_request(endpoint)
            self.log_test_result(f"Health: {description}", success, response_time, details)
            if not success:
                all_passed = False

        return all_passed

    def test_ssl_security(self) -> bool:
        """Test SSL/TLS configuration and security headers."""
        logger.info("🔒 Testing SSL/TLS Security")

        # Test HTTPS enforcement
        success, response_time, details = self.make_request("/")
        ssl_valid = details.get("status_code") == 200

        # Check security headers
        headers = details.get("headers", {})
        security_headers = {
            "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
            "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
            "X-Frame-Options": headers.get("X-Frame-Options"),
            "X-XSS-Protection": headers.get("X-XSS-Protection"),
            "Content-Security-Policy": headers.get("Content-Security-Policy")
        }

        security_passed = all([
            security_headers["Strict-Transport-Security"] is not None,
            security_headers["X-Content-Type-Options"] == "nosniff",
            security_headers["X-Frame-Options"] == "DENY"
        ])

        self.log_test_result("SSL: HTTPS Enforcement", ssl_valid, response_time,
                           {"security_headers": security_headers})
        self.log_test_result("SSL: Security Headers", security_passed, 0,
                           {"security_headers": security_headers})

        return ssl_valid and security_passed

    def test_api_endpoints(self) -> bool:
        """Test Revenue Engine API endpoints."""
        logger.info("🔗 Testing API Endpoints")

        # Test endpoints without authentication
        public_endpoints = [
            ("/api/v1/status", "GET", "API Status"),
            ("/api/v1/info", "GET", "API Information"),
        ]

        # Test endpoints requiring authentication
        auth_endpoints = [
            ("/api/v1/revenue/metrics", "GET", "Revenue Metrics"),
            ("/api/v1/revenue/analytics", "GET", "Revenue Analytics"),
            ("/api/v1/revenue/reports", "POST", "Revenue Reports"),
        ]

        all_passed = True

        # Test public endpoints
        for endpoint, method, description in public_endpoints:
            success, response_time, details = self.make_request(endpoint, method)
            self.log_test_result(f"API: {description}", success, response_time, details)
            if not success:
                all_passed = False

        # Test authenticated endpoints (will fail without token, but should get 401)
        for endpoint, method, description in auth_endpoints:
            success, response_time, details = self.make_request(
                endpoint, method, expected_status=401
            )
            # 401 is expected for unauthenticated requests
            auth_protected = details.get("status_code") == 401
            self.log_test_result(f"Auth: {description}", auth_protected, response_time, details)
            if not auth_protected:
                all_passed = False

        return all_passed

    def test_performance_metrics(self) -> bool:
        """Test performance requirements (<250ms response time)."""
        logger.info("⚡ Testing Performance Metrics")

        # Test multiple requests to measure performance
        test_endpoints = ["/health", "/api/v1/status", "/api/v1/info"]
        performance_results = []

        for endpoint in test_endpoints:
            times = []
            for _ in range(5):  # 5 requests per endpoint
                success, response_time, _ = self.make_request(endpoint)
                if success:
                    times.append(response_time * 1000)  # Convert to ms

            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                performance_results.append({
                    "endpoint": endpoint,
                    "avg_ms": round(avg_time, 2),
                    "max_ms": round(max_time, 2),
                    "within_limit": max_time < 250
                })

        # Check if all endpoints meet performance requirements
        all_within_limit = all(r["within_limit"] for r in performance_results)
        avg_response_time = sum(r["avg_ms"] for r in performance_results) / len(performance_results)

        self.log_test_result("Performance: <250ms Limit", all_within_limit, avg_response_time / 1000,
                           {"endpoint_results": performance_results})

        return all_within_limit

    def test_enterprise_features(self) -> bool:
        """Test enterprise features (JWT, analytics, async processing)."""
        logger.info("🏢 Testing Enterprise Features")

        # Test JWT token generation (mock test)
        jwt_headers = {"Authorization": "Bearer mock.jwt.token"}
        success, response_time, details = self.make_request(
            "/api/v1/revenue/protected", headers=jwt_headers, expected_status=401
        )
        # Should fail with mock token but validate JWT processing
        jwt_processed = "token" in details.get("error", "").lower()

        # Test analytics endpoints
        analytics_success, analytics_time, analytics_details = self.make_request(
            "/api/v1/analytics/dashboard"
        )

        # Test async processing capability
        async_success, async_time, async_details = self.make_request(
            "/api/v1/async/status"
        )

        features_results = {
            "jwt_processing": jwt_processed,
            "analytics_endpoints": analytics_success,
            "async_processing": async_success
        }

        all_features_working = all(features_results.values())

        self.log_test_result("Enterprise: JWT Processing", jwt_processed, response_time,
                           {"jwt_details": details})
        self.log_test_result("Enterprise: Analytics", analytics_success, analytics_time,
                           {"analytics_details": analytics_details})
        self.log_test_result("Enterprise: Async Processing", async_success, async_time,
                           {"async_details": async_details})

        return all_features_working

    def test_infrastructure_integration(self) -> bool:
        """Test infrastructure integration (service mesh, caching, database)."""
        logger.info("🏗️ Testing Infrastructure Integration")

        # Test service mesh routing (via headers)
        mesh_headers = {"X-Request-ID": "test-mesh-routing"}
        mesh_success, mesh_time, mesh_details = self.make_request(
            "/api/v1/test", headers=mesh_headers
        )

        # Test caching headers
        cache_headers = {"Cache-Control": "no-cache"}
        cache_success, cache_time, cache_details = self.make_request(
            "/api/v1/cached", headers=cache_headers
        )

        # Test database connectivity
        db_success, db_time, db_details = self.make_request("/api/v1/db/status")

        infrastructure_results = {
            "service_mesh": mesh_success,
            "caching": cache_success,
            "database": db_success
        }

        all_infrastructure_working = all(infrastructure_results.values())

        self.log_test_result("Infrastructure: Service Mesh", mesh_success, mesh_time,
                           {"mesh_details": mesh_details})
        self.log_test_result("Infrastructure: Caching", cache_success, cache_time,
                           {"cache_details": cache_details})
        self.log_test_result("Infrastructure: Database", db_success, db_time,
                           {"db_details": db_details})

        return all_infrastructure_working

    def run_full_verification(self) -> Dict[str, Any]:
        """Run complete verification suite."""
        logger.info("🎯 STARTING REVENUE ENGINE DEPLOYMENT VERIFICATION")

        tests = [
            ("Health Endpoints", self.test_health_endpoints),
            ("SSL Security", self.test_ssl_security),
            ("API Endpoints", self.test_api_endpoints),
            ("Performance Metrics", self.test_performance_metrics),
            ("Enterprise Features", self.test_enterprise_features),
            ("Infrastructure Integration", self.test_infrastructure_integration)
        ]

        all_passed = True
        for test_name, test_func in tests:
            logger.info(f"📋 Running {test_name}")
            try:
                passed = test_func()
                if not passed:
                    all_passed = False
            except Exception as e:
                logger.error(f"Test {test_name} failed with exception: {e}")
                self.log_test_result(f"Exception: {test_name}", False, 0,
                                   {"exception": str(e)})
                all_passed = False

        # Generate final report
        self.results["overall_success"] = all_passed
        self.results["verification_duration"] = str(datetime.now() -
                                                   datetime.fromisoformat(self.results["timestamp"]))

        # Save results
        report_file = Path(f"reports/revenue_engine_verification_{int(time.time())}.json")
        report_file.parent.mkdir(exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"📊 Verification complete. Report saved to {report_file}")
        logger.info(f"Results: {self.results['summary']['passed']}/{self.results['summary']['total']} tests passed")

        if all_passed:
            logger.info("🎉 Revenue Engine production verification PASSED!")
        else:
            logger.error("❌ Revenue Engine production verification FAILED!")

        return self.results

def main():
    """Main verification execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Revenue Engine Deployment Verification")
    parser.add_argument("--url", default="https://revenue-engine.tradingrobotplug.com",
                       help="Base URL for verification")
    parser.add_argument("--output", help="Output file for results")

    args = parser.parse_args()

    verifier = RevenueEngineVerifier(args.url)
    results = verifier.run_full_verification()

    # Print summary
    summary = results["summary"]
    print("
📊 VERIFICATION SUMMARY"    print(f"Total Tests: {summary['total']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {(summary['passed']/summary['total']*100):.1f}%")

    if results["overall_success"]:
        print("🎉 VERIFICATION PASSED - Revenue Engine is production-ready!")
        return 0
    else:
        print("❌ VERIFICATION FAILED - Check logs for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())