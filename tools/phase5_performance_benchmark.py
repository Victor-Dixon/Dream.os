#!/usr/bin/env python3
"""
Phase 5 Infrastructure Performance Benchmark Tool
Comprehensive performance testing and validation of enterprise infrastructure
"""

import asyncio
import aiohttp
import time
import statistics
import json
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import logging
import psycopg2
import redis

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkResult:
    test_name: str
    duration: float
    requests_per_second: float
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p95_response_time: float
    p99_response_time: float
    success_rate: float
    error_count: int
    timestamp: str

class Phase5PerformanceBenchmark:
    def __init__(self, duration: int = 60, concurrency: int = 10):
        self.duration = duration
        self.concurrency = concurrency
        self.results = []

    async def benchmark_http_endpoint(self, url: str, test_name: str) -> BenchmarkResult:
        """Benchmark HTTP endpoint performance"""
        start_time = time.time()
        end_time = start_time + self.duration

        response_times = []
        error_count = 0
        request_count = 0

        async def make_request(session):
            nonlocal error_count, request_count
            try:
                req_start = time.time()
                async with session.get(url) as response:
                    req_end = time.time()
                    if response.status == 200:
                        response_times.append(req_end - req_start)
                    else:
                        error_count += 1
                request_count += 1
            except Exception:
                error_count += 1

        async with aiohttp.ClientSession() as session:
            tasks = []

            while time.time() < end_time:
                # Create concurrent requests
                for _ in range(self.concurrency):
                    if time.time() < end_time:
                        task = asyncio.create_task(make_request(session))
                        tasks.append(task)

                # Wait for current batch to complete
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
                    tasks = []

                # Small delay to prevent overwhelming
                await asyncio.sleep(0.01)

        # Calculate statistics
        total_time = time.time() - start_time
        successful_requests = len(response_times)
        total_requests = successful_requests + error_count

        if response_times:
            avg_response_time = statistics.mean(response_times) * 1000
            min_response_time = min(response_times) * 1000
            max_response_time = max(response_times) * 1000
            p95_response_time = statistics.quantiles(response_times, n=20)[18] * 1000
            p99_response_time = statistics.quantiles(response_times, n=100)[98] * 1000
            requests_per_second = successful_requests / total_time
            success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
        else:
            avg_response_time = min_response_time = max_response_time = p95_response_time = p99_response_time = 0
            requests_per_second = 0
            success_rate = 0

        return BenchmarkResult(
            test_name=test_name,
            duration=round(total_time, 2),
            requests_per_second=round(requests_per_second, 2),
            avg_response_time=round(avg_response_time, 2),
            min_response_time=round(min_response_time, 2),
            max_response_time=round(max_response_time, 2),
            p95_response_time=round(p95_response_time, 2),
            p99_response_time=round(p99_response_time, 2),
            success_rate=round(success_rate, 2),
            error_count=error_count,
            timestamp=datetime.now().isoformat()
        )

    def benchmark_postgresql_performance(self) -> BenchmarkResult:
        """Benchmark PostgreSQL performance"""
        start_time = time.time()

        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="tradingrobotplug",
                user="postgres",
                password="postgres"
            )

            cursor = conn.cursor()

            # Create test table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_test (
                    id SERIAL PRIMARY KEY,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Clear previous test data
            cursor.execute("DELETE FROM performance_test")

            # Benchmark INSERT operations
            insert_times = []
            for i in range(1000):
                insert_start = time.time()
                cursor.execute("INSERT INTO performance_test (data) VALUES (%s)", [f"test_data_{i}"])
                insert_end = time.time()
                insert_times.append(insert_end - insert_start)

            conn.commit()

            # Benchmark SELECT operations
            select_times = []
            for _ in range(1000):
                select_start = time.time()
                cursor.execute("SELECT * FROM performance_test WHERE id = %s", [1])
                cursor.fetchone()
                select_end = time.time()
                select_times.append(select_end - select_start)

            cursor.close()
            conn.close()

            total_time = time.time() - start_time

            # Calculate statistics
            all_times = insert_times + select_times
            avg_response_time = statistics.mean(all_times) * 1000
            min_response_time = min(all_times) * 1000
            max_response_time = max(all_times) * 1000
            p95_response_time = statistics.quantiles(all_times, n=20)[18] * 1000
            p99_response_time = statistics.quantiles(all_times, n=100)[98] * 1000

            return BenchmarkResult(
                test_name="PostgreSQL Performance",
                duration=round(total_time, 2),
                requests_per_second=round(2000 / total_time, 2),
                avg_response_time=round(avg_response_time, 2),
                min_response_time=round(min_response_time, 2),
                max_response_time=round(max_response_time, 2),
                p95_response_time=round(p95_response_time, 2),
                p99_response_time=round(p99_response_time, 2),
                success_rate=100.0,
                error_count=0,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            total_time = time.time() - start_time
            return BenchmarkResult(
                test_name="PostgreSQL Performance",
                duration=round(total_time, 2),
                requests_per_second=0,
                avg_response_time=0,
                min_response_time=0,
                max_response_time=0,
                p95_response_time=0,
                p99_response_time=0,
                success_rate=0,
                error_count=1,
                timestamp=datetime.now().isoformat()
            )

    def benchmark_redis_performance(self) -> BenchmarkResult:
        """Benchmark Redis performance"""
        start_time = time.time()

        try:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)

            # Clear previous test data
            r.flushdb()

            # Benchmark SET operations
            set_times = []
            for i in range(10000):
                set_start = time.time()
                r.set(f"key_{i}", f"value_{i}")
                set_end = time.time()
                set_times.append(set_end - set_start)

            # Benchmark GET operations
            get_times = []
            for i in range(10000):
                get_start = time.time()
                r.get(f"key_{i}")
                get_end = time.time()
                get_times.append(get_end - get_start)

            r.close()

            total_time = time.time() - start_time

            # Calculate statistics
            all_times = set_times + get_times
            avg_response_time = statistics.mean(all_times) * 1000
            min_response_time = min(all_times) * 1000
            max_response_time = max(all_times) * 1000
            p95_response_time = statistics.quantiles(all_times, n=20)[18] * 1000
            p99_response_time = statistics.quantiles(all_times, n=100)[98] * 1000

            return BenchmarkResult(
                test_name="Redis Performance",
                duration=round(total_time, 2),
                requests_per_second=round(20000 / total_time, 2),
                avg_response_time=round(avg_response_time, 2),
                min_response_time=round(min_response_time, 2),
                max_response_time=round(max_response_time, 2),
                p95_response_time=round(p95_response_time, 2),
                p99_response_time=round(p99_response_time, 2),
                success_rate=100.0,
                error_count=0,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            total_time = time.time() - start_time
            return BenchmarkResult(
                test_name="Redis Performance",
                duration=round(total_time, 2),
                requests_per_second=0,
                avg_response_time=0,
                min_response_time=0,
                max_response_time=0,
                p95_response_time=0,
                p99_response_time=0,
                success_rate=0,
                error_count=1,
                timestamp=datetime.now().isoformat()
            )

    async def run_comprehensive_benchmark(self) -> Dict:
        """Run comprehensive performance benchmark"""
        logger.info(f"🚀 Starting Phase 5 Performance Benchmark ({self.duration}s, {self.concurrency} concurrency)...")

        # Define endpoints to benchmark
        endpoints = [
            ("FastAPI Main", "http://localhost:8001/"),
            ("FastAPI Health", "http://localhost:8001/health"),
            ("Flask App", "http://localhost:5000/"),
            ("Kong Gateway", "http://localhost:8000/"),
            ("Nginx Reverse Proxy", "http://localhost:8080/"),
            ("CDN Assets", "http://localhost:8080/cdn-assets/test"),
        ]

        # Run HTTP benchmarks concurrently
        http_tasks = [self.benchmark_http_endpoint(url, name) for name, url in endpoints]
        http_results = await asyncio.gather(*http_tasks)

        # Run database benchmarks in thread pool
        with ThreadPoolExecutor(max_workers=2) as executor:
            loop = asyncio.get_event_loop()
            postgres_task = loop.run_in_executor(executor, self.benchmark_postgresql_performance)
            redis_task = loop.run_in_executor(executor, self.benchmark_redis_performance)

            db_results = await asyncio.gather(postgres_task, redis_task)

        # Combine all results
        all_results = http_results + list(db_results)
        self.results = all_results

        # Calculate summary statistics
        total_requests_per_second = sum(r.requests_per_second for r in all_results)
        avg_response_time = statistics.mean(r.avg_response_time for r in all_results if r.avg_response_time > 0)
        total_errors = sum(r.error_count for r in all_results)
        total_success_rate = statistics.mean(r.success_rate for r in all_results)

        summary = {
            "timestamp": datetime.now().isoformat(),
            "benchmark_duration_seconds": self.duration,
            "concurrency_level": self.concurrency,
            "total_endpoints_tested": len(endpoints),
            "total_requests_per_second": round(total_requests_per_second, 2),
            "average_response_time_ms": round(avg_response_time, 2),
            "total_errors": total_errors,
            "average_success_rate": round(total_success_rate, 2),
            "performance_rating": self._calculate_performance_rating(all_results)
        }

        return {
            "summary": summary,
            "results": [asdict(result) for result in all_results]
        }

    def _calculate_performance_rating(self, results: List[BenchmarkResult]) -> str:
        """Calculate overall performance rating"""
        if not results:
            return "UNKNOWN"

        avg_rps = statistics.mean(r.requests_per_second for r in results)
        avg_response_time = statistics.mean(r.avg_response_time for r in results if r.avg_response_time > 0)
        error_rate = sum(r.error_count for r in results) / sum(r.requests_per_second * r.duration for r in results) if results else 1

        # Performance thresholds (adjustable based on requirements)
        if avg_rps > 1000 and avg_response_time < 50 and error_rate < 0.01:
            return "EXCELLENT"
        elif avg_rps > 500 and avg_response_time < 100 and error_rate < 0.05:
            return "VERY_GOOD"
        elif avg_rps > 200 and avg_response_time < 200 and error_rate < 0.1:
            return "GOOD"
        elif avg_rps > 50 and avg_response_time < 500 and error_rate < 0.2:
            return "FAIR"
        else:
            return "NEEDS_IMPROVEMENT"

    def print_report(self, data: Dict):
        """Print comprehensive performance benchmark report"""
        print("\n" + "="*100)
        print("⚡ PHASE 5 INFRASTRUCTURE PERFORMANCE BENCHMARK REPORT")
        print("="*100)

        summary = data["summary"]
        print(f"🎯 PERFORMANCE RATING: {summary['performance_rating']}")
        print(f"⏱️  BENCHMARK DURATION: {summary['benchmark_duration_seconds']} seconds")
        print(f"🔄 CONCURRENCY LEVEL: {summary['concurrency_level']}")
        print(f"📊 ENDPOINTS TESTED: {summary['total_endpoints_tested']}")
        print(",.2f"        print(".2f"        print(f"📈 AVERAGE SUCCESS RATE: {summary['average_success_rate']}%")
        print(f"❌ TOTAL ERRORS: {summary['total_errors']}")

        print("\n" + "-"*100)
        print("📋 ENDPOINT PERFORMANCE DETAILS")
        print("-"*100)
        print("<25")
        print("-"*100)

        for result in data["results"]:
            status_indicator = "✅" if result["success_rate"] > 95 else "⚠️" if result["success_rate"] > 80 else "❌"
            print("<25")

        print("\n" + "="*100)

    def save_report(self, data: Dict, filename: str = None):
        """Save benchmark report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase5_performance_benchmark_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"📄 Report saved to: {filename}")

async def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Phase 5 Infrastructure Performance Benchmark')
    parser.add_argument('--duration', type=int, default=60, help='Benchmark duration in seconds')
    parser.add_argument('--concurrency', type=int, default=10, help='Concurrent requests per endpoint')
    parser.add_argument('--output', type=str, help='Output filename for JSON report')

    args = parser.parse_args()

    benchmark = Phase5PerformanceBenchmark(duration=args.duration, concurrency=args.concurrency)

    try:
        results = await benchmark.run_comprehensive_benchmark()
        benchmark.print_report(results)
        benchmark.save_report(results, args.output)

    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())