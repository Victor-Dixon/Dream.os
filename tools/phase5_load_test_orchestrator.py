#!/usr/bin/env python3
"""
Phase 5 Load Test Orchestrator
Automated load testing orchestration for enterprise infrastructure validation
"""

import asyncio
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import logging
import argparse
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class LoadTestScenario:
    name: str
    description: str
    duration: int
    concurrency: int
    target_rps: Optional[int]
    endpoints: List[str]
    success_criteria: Dict[str, float]

@dataclass
class LoadTestResult:
    scenario_name: str
    start_time: str
    end_time: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_second: float
    success_rate: float
    errors: List[str]
    passed_criteria: bool

class Phase5LoadTestOrchestrator:
    def __init__(self):
        self.scenarios = self._define_test_scenarios()
        self.results = []

    def _define_test_scenarios(self) -> List[LoadTestScenario]:
        """Define comprehensive load test scenarios"""
        return [
            LoadTestScenario(
                name="baseline_validation",
                description="Baseline performance validation for all services",
                duration=30,
                concurrency=5,
                target_rps=None,
                endpoints=[
                    "http://localhost:8080/",
                    "http://localhost:8001/health",
                    "http://localhost:5000/health",
                    "http://localhost:8000/status"
                ],
                success_criteria={
                    "avg_response_time": 500,  # ms
                    "success_rate": 99.5,      # %
                    "requests_per_second": 50   # rps
                }
            ),
            LoadTestScenario(
                name="api_gateway_stress",
                description="API Gateway stress testing with high concurrency",
                duration=60,
                concurrency=20,
                target_rps=200,
                endpoints=[
                    "http://localhost:8000/",
                    "http://localhost:8080/api/v1/health"
                ],
                success_criteria={
                    "avg_response_time": 1000,
                    "success_rate": 95.0,
                    "requests_per_second": 150
                }
            ),
            LoadTestScenario(
                name="fastapi_endurance",
                description="FastAPI endurance testing under sustained load",
                duration=120,
                concurrency=15,
                target_rps=100,
                endpoints=[
                    "http://localhost:8001/health",
                    "http://localhost:8001/docs",
                    "http://localhost:8080/api/v1/status"
                ],
                success_criteria={
                    "avg_response_time": 800,
                    "success_rate": 98.0,
                    "requests_per_second": 80
                }
            ),
            LoadTestScenario(
                name="cdn_performance",
                description="CDN performance testing with asset delivery",
                duration=45,
                concurrency=25,
                target_rps=300,
                endpoints=[
                    "http://localhost:8080/cdn-assets/test.css",
                    "http://localhost:8080/cdn-assets/test.js",
                    "http://localhost:8080/cdn-assets/test.json"
                ],
                success_criteria={
                    "avg_response_time": 200,
                    "success_rate": 99.0,
                    "requests_per_second": 250
                }
            ),
            LoadTestScenario(
                name="database_concurrency",
                description="Database concurrency and connection pooling validation",
                duration=90,
                concurrency=10,
                target_rps=50,
                endpoints=[
                    "http://localhost:8001/api/v1/db-test",
                    "http://localhost:8080/api/v1/db-status"
                ],
                success_criteria={
                    "avg_response_time": 1200,
                    "success_rate": 97.0,
                    "requests_per_second": 40
                }
            ),
            LoadTestScenario(
                name="circuit_breaker_validation",
                description="Circuit breaker pattern validation under failure conditions",
                duration=60,
                concurrency=30,
                target_rps=100,
                endpoints=[
                    "http://localhost:8080/api/circuit-test",
                    "http://localhost:8080/api/failover-test"
                ],
                success_criteria={
                    "avg_response_time": 1500,
                    "success_rate": 90.0,  # Lower threshold for circuit breaker testing
                    "requests_per_second": 60
                }
            )
        ]

    async def run_load_test_scenario(self, scenario: LoadTestScenario) -> LoadTestResult:
        """Run a single load test scenario using the performance benchmark tool"""
        logger.info(f"🚀 Starting load test scenario: {scenario.name}")

        start_time = datetime.now()

        # Build command for performance benchmark tool
        cmd = [
            "python", "tools/phase5_performance_benchmark.py",
            "--duration", str(scenario.duration),
            "--concurrency", str(scenario.concurrency)
        ]

        # Add output file
        output_file = f"load_test_{scenario.name}_{int(time.time())}.json"
        cmd.extend(["--output", output_file])

        try:
            # Run the performance benchmark
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd="."
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Load test failed: {error_msg}")
                return LoadTestResult(
                    scenario_name=scenario.name,
                    start_time=start_time.isoformat(),
                    end_time=datetime.now().isoformat(),
                    total_requests=0,
                    successful_requests=0,
                    failed_requests=0,
                    avg_response_time=0,
                    p95_response_time=0,
                    p99_response_time=0,
                    requests_per_second=0,
                    success_rate=0,
                    errors=[error_msg],
                    passed_criteria=False
                )

            # Parse results from output file
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    benchmark_data = json.load(f)

                summary = benchmark_data.get("summary", {})
                results = benchmark_data.get("results", [])

                # Aggregate results across all endpoints
                total_requests = sum(r.get("requests_per_second", 0) * scenario.duration for r in results)
                avg_response_time = summary.get("average_response_time_ms", 0)
                success_rate = summary.get("average_success_rate", 0)

                # Calculate p95 and p99 from individual results
                all_response_times = []
                for result in results:
                    # Approximate percentiles from available data
                    all_response_times.extend([result.get("avg_response_time", 0)] * int(result.get("requests_per_second", 1) * scenario.duration))

                if all_response_times:
                    sorted_times = sorted(all_response_times)
                    p95_idx = int(len(sorted_times) * 0.95)
                    p99_idx = int(len(sorted_times) * 0.99)
                    p95_response_time = sorted_times[min(p95_idx, len(sorted_times)-1)]
                    p99_response_time = sorted_times[min(p99_idx, len(sorted_times)-1)]
                else:
                    p95_response_time = p99_response_time = 0

                requests_per_second = summary.get("total_requests_per_second", 0)

                # Check success criteria
                passed_criteria = (
                    avg_response_time <= scenario.success_criteria.get("avg_response_time", float('inf')) and
                    success_rate >= scenario.success_criteria.get("success_rate", 0) and
                    requests_per_second >= scenario.success_criteria.get("requests_per_second", 0)
                )

                return LoadTestResult(
                    scenario_name=scenario.name,
                    start_time=start_time.isoformat(),
                    end_time=datetime.now().isoformat(),
                    total_requests=int(total_requests),
                    successful_requests=int(total_requests * success_rate / 100),
                    failed_requests=int(total_requests * (100 - success_rate) / 100),
                    avg_response_time=round(avg_response_time, 2),
                    p95_response_time=round(p95_response_time, 2),
                    p99_response_time=round(p99_response_time, 2),
                    requests_per_second=round(requests_per_second, 2),
                    success_rate=round(success_rate, 2),
                    errors=[],
                    passed_criteria=passed_criteria
                )

        except Exception as e:
            logger.error(f"Load test execution failed: {e}")
            return LoadTestResult(
                scenario_name=scenario.name,
                start_time=start_time.isoformat(),
                end_time=datetime.now().isoformat(),
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                avg_response_time=0,
                p95_response_time=0,
                p99_response_time=0,
                requests_per_second=0,
                success_rate=0,
                errors=[str(e)],
                passed_criteria=False
            )

    async def run_comprehensive_load_test_suite(self) -> Dict:
        """Run all load test scenarios"""
        logger.info("🎯 Starting Phase 5 Comprehensive Load Test Suite...")

        start_time = datetime.now()

        # Run all scenarios sequentially to avoid overwhelming the infrastructure
        results = []
        for scenario in self.scenarios:
            logger.info(f"\n{'='*60}")
            logger.info(f"Running Scenario: {scenario.name}")
            logger.info(f"Description: {scenario.description}")
            logger.info(f"Duration: {scenario.duration}s, Concurrency: {scenario.concurrency}")
            logger.info(f"{'='*60}")

            result = await self.run_load_test_scenario(scenario)
            results.append(result)

            # Brief pause between scenarios
            if scenario != self.scenarios[-1]:
                logger.info("⏳ Cooling down before next scenario...")
                await asyncio.sleep(10)

        end_time = datetime.now()

        # Calculate summary statistics
        total_scenarios = len(results)
        passed_scenarios = len([r for r in results if r.passed_criteria])
        total_requests = sum(r.total_requests for r in results)
        avg_success_rate = sum(r.success_rate for r in results) / total_scenarios if total_scenarios > 0 else 0

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_duration_seconds": (end_time - start_time).total_seconds(),
            "total_scenarios": total_scenarios,
            "passed_scenarios": passed_scenarios,
            "failed_scenarios": total_scenarios - passed_scenarios,
            "success_rate": round((passed_scenarios / total_scenarios) * 100, 1) if total_scenarios > 0 else 0,
            "total_requests": total_requests,
            "average_scenario_success_rate": round(avg_success_rate, 1),
            "load_test_rating": self._calculate_load_test_rating(results)
        }

        return {
            "summary": summary,
            "results": [asdict(result) for result in results]
        }

    def _calculate_load_test_rating(self, results: List[LoadTestResult]) -> str:
        """Calculate overall load test rating"""
        if not results:
            return "UNKNOWN"

        passed_count = len([r for r in results if r.passed_criteria])
        total_count = len(results)
        success_rate = passed_count / total_count

        avg_response_time = sum(r.avg_response_time for r in results) / total_count if total_count > 0 else 0
        avg_rps = sum(r.requests_per_second for r in results) / total_count if total_count > 0 else 0

        if success_rate >= 0.9 and avg_response_time < 500 and avg_rps > 100:
            return "EXCELLENT"
        elif success_rate >= 0.8 and avg_response_time < 800 and avg_rps > 50:
            return "VERY_GOOD"
        elif success_rate >= 0.7 and avg_response_time < 1200 and avg_rps > 25:
            return "GOOD"
        elif success_rate >= 0.5 and avg_response_time < 2000 and avg_rps > 10:
            return "FAIR"
        else:
            return "NEEDS_IMPROVEMENT"

    def print_report(self, data: Dict):
        """Print comprehensive load test report"""
        print("\n" + "="*100)
        print("🔥 PHASE 5 COMPREHENSIVE LOAD TEST REPORT")
        print("="*100)

        summary = data["summary"]
        print(f"🎯 LOAD TEST RATING: {summary['load_test_rating']}")
        print(f"⏱️  TOTAL DURATION: {summary['total_duration_seconds']:.1f} seconds")
        print(f"📊 SCENARIOS RUN: {summary['total_scenarios']}")
        print(f"✅ PASSED: {summary['passed_scenarios']}")
        print(f"❌ FAILED: {summary['failed_scenarios']}")
        print(".1f"        print(",.1f"        print(",.1f"        print(f"🚀 TOTAL REQUESTS: {summary['total_requests']:,}")

        print("\n" + "-"*100)
        print("📋 SCENARIO RESULTS")
        print("-"*100)
        print("<25")
        print("-"*100)

        for result in data["results"]:
            status_emoji = "✅" if result["passed_criteria"] else "❌"
            duration = datetime.fromisoformat(result["end_time"]) - datetime.fromisoformat(result["start_time"])
            print("<25")

        # Show failed scenarios with details
        failed_scenarios = [r for r in data["results"] if not r["passed_criteria"]]
        if failed_scenarios:
            print("\n" + "-"*100)
            print("❌ FAILED SCENARIO DETAILS")
            print("-"*100)
            for result in failed_scenarios:
                print(f"Scenario: {result['scenario_name']}")
                print(f"  Errors: {', '.join(result['errors'])}")
                print(f"  Success Rate: {result['success_rate']}%")
                print(f"  Avg Response Time: {result['avg_response_time']}ms")
                print(f"  Requests/sec: {result['requests_per_second']}")
                print()

        print("="*100)

    def save_report(self, data: Dict, filename: str = None):
        """Save load test report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase5_load_test_report_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"📄 Report saved to: {filename}")

async def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 5 Load Test Orchestrator')
    parser.add_argument('--scenario', type=str, help='Run specific scenario (default: all)')
    parser.add_argument('--output', type=str, help='Output filename for JSON report')
    parser.add_argument('--quick', action='store_true', help='Run quick validation (reduced duration)')

    args = parser.parse_args()

    orchestrator = Phase5LoadTestOrchestrator()

    # Modify scenarios for quick testing
    if args.quick:
        for scenario in orchestrator.scenarios:
            scenario.duration = max(10, scenario.duration // 4)
            scenario.concurrency = max(2, scenario.concurrency // 2)

    try:
        if args.scenario:
            # Run specific scenario
            scenario = next((s for s in orchestrator.scenarios if s.name == args.scenario), None)
            if not scenario:
                logger.error(f"Scenario '{args.scenario}' not found")
                sys.exit(1)

            logger.info(f"Running specific scenario: {args.scenario}")
            result = await orchestrator.run_load_test_scenario(scenario)
            data = {
                "summary": {
                    "timestamp": datetime.now().isoformat(),
                    "total_scenarios": 1,
                    "passed_scenarios": 1 if result.passed_criteria else 0,
                    "failed_scenarios": 0 if result.passed_criteria else 1,
                    "success_rate": 100.0 if result.passed_criteria else 0.0,
                    "load_test_rating": "PASS" if result.passed_criteria else "FAIL"
                },
                "results": [asdict(result)]
            }
        else:
            # Run comprehensive suite
            data = await orchestrator.run_comprehensive_load_test_suite()

        orchestrator.print_report(data)
        orchestrator.save_report(data, args.output)

        # Exit with appropriate code based on results
        summary = data["summary"]
        if summary["failed_scenarios"] > 0:
            sys.exit(1)  # Load test failures
        else:
            sys.exit(0)  # All tests passed

    except Exception as e:
        logger.error(f"Load test orchestration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())