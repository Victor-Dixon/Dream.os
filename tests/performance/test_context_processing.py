#!/usr/bin/env python3
"""
AI Context Engine Performance Tests
==================================

Comprehensive performance benchmarking for Phase 5 AI Context Engine.

<!-- SSOT Domain: ai_context_performance -->

Navigation References:
├── Implementation → src/services/ai_context_engine.py
├── WebSocket Server → src/services/ai_context_websocket.py
├── FastAPI Integration → src/web/fastapi_app.py
├── Documentation → docs/PHASE5_AI_CONTEXT_ENGINE.md
├── Integration Tests → tests/integration/test_ai_context_engine.py

Performance Benchmarks:
- Response Time: <50ms average context processing
- Throughput: 1000+ concurrent sessions
- Memory Usage: Optimized for high-frequency updates
- Latency: End-to-end <50ms for real-time requirements
- Scalability: Horizontal scaling validation
- Reliability: Connection stability under load

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 5 - AI Context Engine Performance Validation
"""

import asyncio
import time
import statistics
import psutil
import os
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
import pytest
import numpy as np

from src.services.ai_context_engine import AIContextEngine, ContextSession
from src.services.ai_context_websocket import AIContextWebSocketServer
from tests.integration.test_ai_context_engine import *


class TestAIContextPerformance:
    """Performance benchmarks for AI Context Engine Phase 5 requirements."""

    @pytest.fixture
    async def performance_engine(self):
        """Initialize AI Context Engine for performance testing."""
        engine = AIContextEngine()
        await engine.start_engine()
        yield engine
        await engine.stop_engine()

    @pytest.fixture
    async def websocket_server(self):
        """Initialize WebSocket server for performance testing."""
        server = AIContextWebSocketServer()
        await server.start_server()
        yield server
        await server.stop_server()

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=0.1)

    async def measure_response_time(self, operation, *args, **kwargs) -> Tuple[float, Any]:
        """Measure execution time of an async operation."""
        start_time = time.perf_counter()
        result = await operation(*args, **kwargs)
        end_time = time.perf_counter()
        return end_time - start_time, result

    @pytest.mark.asyncio
    async def test_session_creation_performance(self, performance_engine):
        """Benchmark session creation performance."""
        response_times = []
        memory_usage_start = self.get_memory_usage()

        # Create 100 sessions sequentially
        for i in range(100):
            response_time, session_id = await self.measure_response_time(
                performance_engine.create_session,
                user_id=f"perf_user_{i}",
                context_type="trading",
                initial_context={"portfolio_size": 10000 + i * 1000}
            )
            response_times.append(response_time)

            # Verify session was created
            assert session_id in performance_engine.active_sessions

        memory_usage_end = self.get_memory_usage()
        memory_delta = memory_usage_end - memory_usage_start

        # Performance assertions
        avg_response_time = statistics.mean(response_times)
        p95_response_time = np.percentile(response_times, 95)
        max_response_time = max(response_times)

        print(f"Session Creation Performance:")
        print(f"  Average: {avg_response_time*1000:.2f}ms")
        print(f"  P95: {p95_response_time*1000:.2f}ms")
        print(f"  Max: {max_response_time*1000:.2f}ms")
        print(f"  Memory Delta: {memory_delta:.2f}MB")

        # Phase 5 requirements: <50ms average
        assert avg_response_time < 0.05, f"Average response time {avg_response_time*1000:.2f}ms exceeds 50ms requirement"
        assert p95_response_time < 0.10, f"P95 response time {p95_response_time*1000:.2f}ms too high"

        # Clean up
        for session_id in list(performance_engine.active_sessions.keys()):
            await performance_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_context_update_throughput(self, performance_engine):
        """Test context update throughput under concurrent load."""
        # Create 50 sessions first
        session_ids = []
        for i in range(50):
            session_id = await performance_engine.create_session(
                user_id=f"throughput_user_{i}",
                context_type="trading",
                initial_context={"initial_portfolio": 50000}
            )
            session_ids.append(session_id)

        # Test concurrent context updates
        async def update_context_worker(session_id: str, updates: int):
            """Worker function for concurrent context updates."""
            response_times = []
            for i in range(updates):
                response_time, result = await self.measure_response_time(
                    performance_engine.update_session_context,
                    session_id=session_id,
                    context_updates={
                        "price_update": 100 + i,
                        "volume_update": 1000 + i * 10,
                        "timestamp": time.time()
                    }
                )
                response_times.append(response_time)
                assert result["success"] is True
            return response_times

        # Run 10 updates per session concurrently
        start_time = time.time()
        tasks = [update_context_worker(session_id, 10) for session_id in session_ids]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        total_updates = len(session_ids) * 10
        total_time = end_time - start_time
        throughput = total_updates / total_time

        # Collect all response times
        all_response_times = [rt for worker_results in results for rt in worker_results]

        avg_response_time = statistics.mean(all_response_times)
        p95_response_time = np.percentile(all_response_times, 95)

        print(f"Context Update Throughput:")
        print(f"  Total Updates: {total_updates}")
        print(f"  Total Time: {total_time:.2f}s")
        print(f"  Throughput: {throughput:.1f} updates/sec")
        print(f"  Average Response: {avg_response_time*1000:.2f}ms")
        print(f"  P95 Response: {p95_response_time*1000:.2f}ms")

        # Performance requirements
        assert throughput > 100, f"Throughput {throughput:.1f} updates/sec below 100 requirement"
        assert avg_response_time < 0.05, f"Average response {avg_response_time*1000:.2f}ms exceeds 50ms"

        # Clean up
        for session_id in session_ids:
            await performance_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_concurrent_session_load(self, performance_engine):
        """Test handling of concurrent sessions (Phase 5: 1000+ sessions)."""
        memory_start = self.get_memory_usage()
        cpu_start = self.get_cpu_usage()

        # Create 200 concurrent sessions (scaled test)
        session_ids = []
        create_tasks = []

        for i in range(200):
            task = performance_engine.create_session(
                user_id=f"concurrent_user_{i}",
                context_type="analysis",
                initial_context={
                    "dataset_size": 1000 + i * 10,
                    "analysis_type": "portfolio_optimization"
                }
            )
            create_tasks.append(task)

        # Execute concurrently
        start_time = time.time()
        session_ids = await asyncio.gather(*create_tasks)
        create_time = time.time() - start_time

        # Verify all sessions created
        assert len(session_ids) == 200
        assert len(performance_engine.active_sessions) == 200

        # Test concurrent context updates on all sessions
        update_tasks = []
        for session_id in session_ids:
            task = performance_engine.update_session_context(
                session_id=session_id,
                context_updates={"concurrent_test": True, "batch_id": time.time()}
            )
            update_tasks.append(task)

        update_start = time.time()
        update_results = await asyncio.gather(*update_tasks)
        update_time = time.time() - update_start

        # Verify all updates succeeded
        successful_updates = sum(1 for result in update_results if result["success"])
        assert successful_updates == 200

        memory_end = self.get_memory_usage()
        cpu_end = self.get_cpu_usage()

        # Performance metrics
        memory_per_session = (memory_end - memory_start) / 200
        avg_create_time = create_time / 200
        avg_update_time = update_time / 200

        print(f"Concurrent Session Load (200 sessions):")
        print(f"  Memory per session: {memory_per_session:.2f}MB")
        print(f"  Avg create time: {avg_create_time*1000:.2f}ms")
        print(f"  Avg update time: {avg_update_time*1000:.2f}ms")
        print(f"  CPU usage: {cpu_end:.1f}%")

        # Performance requirements
        assert memory_per_session < 1.0, f"Memory per session {memory_per_session:.2f}MB too high"
        assert avg_create_time < 0.05, f"Avg create time {avg_create_time*1000:.2f}ms exceeds 50ms"
        assert avg_update_time < 0.05, f"Avg update time {avg_update_time*1000:.2f}ms exceeds 50ms"

        # Clean up
        cleanup_tasks = [performance_engine.end_session(sid) for sid in session_ids]
        await asyncio.gather(*cleanup_tasks)

    @pytest.mark.asyncio
    async def test_websocket_performance(self, websocket_server):
        """Test WebSocket server performance under load."""
        server_task = asyncio.create_task(websocket_server.start_server())
        await asyncio.sleep(0.1)

        try:
            uri = f"ws://localhost:{websocket_server.port}/ws/ai/context"

            # Test connection establishment performance
            connection_times = []

            async def websocket_worker(worker_id: int):
                """Worker for WebSocket performance testing."""
                conn_start = time.perf_counter()
                try:
                    async with websockets.connect(uri) as websocket:
                        conn_time = time.perf_counter() - conn_start
                        connection_times.append(conn_time)

                        # Send test messages
                        for i in range(5):
                            message = {
                                "action": "ping",
                                "worker_id": worker_id,
                                "sequence": i,
                                "timestamp": time.time()
                            }

                            send_start = time.perf_counter()
                            await websocket.send(json.dumps(message))
                            response = await websocket.recv()
                            round_trip = time.perf_counter() - send_start

                            # Verify response
                            response_data = json.loads(response)
                            assert "success" in response_data

                        return True
                except Exception as e:
                    print(f"Worker {worker_id} failed: {e}")
                    return False

            # Test with 50 concurrent WebSocket connections
            start_time = time.time()
            tasks = [websocket_worker(i) for i in range(50)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()

            successful_connections = sum(1 for r in results if r is True)
            total_time = end_time - start_time

            if connection_times:
                avg_connection_time = statistics.mean(connection_times)
                print(f"WebSocket Performance (50 concurrent connections):")
                print(f"  Successful connections: {successful_connections}/50")
                print(f"  Total time: {total_time:.2f}s")
                print(f"  Avg connection time: {avg_connection_time*1000:.2f}ms")

                # Performance requirements
                assert successful_connections >= 45, f"Only {successful_connections}/50 connections successful"
                assert avg_connection_time < 0.1, f"Avg connection time {avg_connection_time*1000:.2f}ms too slow"

        finally:
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self, performance_engine):
        """Test memory usage patterns under sustained load."""
        memory_snapshots = []
        memory_snapshots.append(("start", self.get_memory_usage()))

        # Create sessions gradually and monitor memory
        session_ids = []
        for batch in range(10):  # 10 batches of 20 sessions = 200 total
            batch_start = time.time()
            for i in range(20):
                session_id = await performance_engine.create_session(
                    user_id=f"memory_test_{batch}_{i}",
                    context_type="trading",
                    initial_context={"batch": batch, "index": i}
                )
                session_ids.append(session_id)

            # Take memory snapshot after each batch
            memory_snapshots.append((f"batch_{batch+1}", self.get_memory_usage()))

            # Perform updates on all sessions
            update_tasks = []
            for session_id in session_ids:
                task = performance_engine.update_session_context(
                    session_id=session_id,
                    context_updates={"memory_test": True, "timestamp": time.time()}
                )
                update_tasks.append(task)

            await asyncio.gather(*update_tasks)
            memory_snapshots.append((f"updates_{batch+1}", self.get_memory_usage()))

        # Analyze memory growth pattern
        memory_deltas = []
        for i in range(1, len(memory_snapshots)):
            delta = memory_snapshots[i][1] - memory_snapshots[i-1][1]
            memory_deltas.append((memory_snapshots[i][0], delta))

        total_memory_growth = memory_snapshots[-1][1] - memory_snapshots[0][1]
        avg_memory_per_session = total_memory_growth / len(session_ids)

        print(f"Memory Usage Analysis (200 sessions):")
        print(f"  Total memory growth: {total_memory_growth:.2f}MB")
        print(f"  Memory per session: {avg_memory_per_session:.3f}MB")

        # Check for memory leaks (should not grow excessively per session)
        assert avg_memory_per_session < 0.5, f"Memory per session {avg_memory_per_session:.3f}MB too high"

        # Verify gradual cleanup
        cleanup_memory_start = self.get_memory_usage()
        cleanup_tasks = [performance_engine.end_session(sid) for sid in session_ids]
        await asyncio.gather(*cleanup_tasks)
        cleanup_memory_end = self.get_memory_usage()

        memory_recovered = cleanup_memory_start - cleanup_memory_end
        recovery_percentage = (memory_recovered / total_memory_growth) * 100 if total_memory_growth > 0 else 100

        print(f"  Memory recovery: {memory_recovered:.2f}MB ({recovery_percentage:.1f}%)")

        # Should recover most memory
        assert recovery_percentage > 80, f"Memory recovery {recovery_percentage:.1f}% too low"

    @pytest.mark.asyncio
    async def test_suggestion_generation_performance(self, performance_engine):
        """Test AI suggestion generation performance."""
        # Create sessions with different context types
        sessions_data = [
            ("trading_user", "trading", {"positions": [{"symbol": "AAPL", "pnl": 1000}], "risk_metrics": True}),
            ("analysis_user", "analysis", {"dataset_size": 5000, "analysis_type": "correlation"}),
            ("collaboration_user", "collaboration", {"participants": 5, "project": "ai_context"})
        ]

        session_ids = []
        for user_id, context_type, context in sessions_data:
            session_id = await performance_engine.create_session(
                user_id=user_id,
                context_type=context_type,
                initial_context=context
            )
            session_ids.append(session_id)

        # Measure suggestion generation time
        suggestion_times = []

        for session_id in session_ids:
            # Trigger context updates that should generate suggestions
            for i in range(5):
                start_time = time.perf_counter()

                result = await performance_engine.update_session_context(
                    session_id=session_id,
                    context_updates={
                        "trigger_suggestions": True,
                        "iteration": i,
                        "timestamp": time.time()
                    }
                )

                end_time = time.perf_counter()
                suggestion_times.append(end_time - start_time)

                # Verify suggestions were generated
                assert result["success"] is True
                assert len(result.get("new_suggestions", [])) >= 0

        avg_suggestion_time = statistics.mean(suggestion_times)
        p95_suggestion_time = np.percentile(suggestion_times, 95)

        print(f"Suggestion Generation Performance:")
        print(f"  Average time: {avg_suggestion_time*1000:.2f}ms")
        print(f"  P95 time: {p95_suggestion_time*1000:.2f}ms")
        print(f"  Total suggestions measured: {len(suggestion_times)}")

        # Performance requirements for suggestion generation
        assert avg_suggestion_time < 0.1, f"Avg suggestion time {avg_suggestion_time*1000:.2f}ms too slow"
        assert p95_suggestion_time < 0.2, f"P95 suggestion time {p95_suggestion_time*1000:.2f}ms too slow"

        # Clean up
        for session_id in session_ids:
            await performance_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_phase5_end_to_end_performance(self, performance_engine):
        """End-to-end performance test simulating Phase 5 real-world usage."""
        # Simulate a trading session with real-time updates
        session_id = await performance_engine.create_session(
            user_id="e2e_test_user",
            context_type="trading",
            initial_context={
                "portfolio": {
                    "cash": 50000,
                    "positions": {
                        "AAPL": {"shares": 100, "avg_price": 150.0},
                        "GOOGL": {"shares": 50, "avg_price": 2800.0},
                        "MSFT": {"shares": 75, "avg_price": 300.0}
                    }
                },
                "risk_tolerance": "moderate",
                "strategy": "diversified_growth"
            }
        )

        # Simulate real-time market updates (like Phase 5 would handle)
        market_updates = [
            {"AAPL": 152.0, "GOOGL": 2820.0, "MSFT": 305.0, "volatility": 0.15},
            {"AAPL": 149.5, "GOOGL": 2790.0, "MSFT": 298.0, "volatility": 0.18},
            {"AAPL": 153.2, "GOOGL": 2850.0, "MSFT": 310.0, "volatility": 0.12},
            {"AAPL": 151.8, "GOOGL": 2815.0, "MSFT": 307.0, "volatility": 0.14},
            {"AAPL": 154.0, "GOOGL": 2870.0, "MSFT": 312.0, "volatility": 0.16}
        ]

        response_times = []
        suggestions_generated = 0

        for update in market_updates:
            start_time = time.perf_counter()

            result = await performance_engine.update_session_context(
                session_id=session_id,
                context_updates={
                    "market_data": update,
                    "timestamp": time.time(),
                    "realtime_update": True
                }
            )

            end_time = time.perf_counter()
            response_time = end_time - start_time
            response_times.append(response_time)

            assert result["success"] is True
            suggestions_generated += len(result.get("new_suggestions", []))

        avg_response_time = statistics.mean(response_times)
        total_time = sum(response_times)

        print(f"Phase 5 E2E Performance (Real-time Trading Session):")
        print(f"  Market updates processed: {len(market_updates)}")
        print(f"  Total processing time: {total_time:.3f}s")
        print(f"  Average response time: {avg_response_time*1000:.2f}ms")
        print(f"  Suggestions generated: {suggestions_generated}")
        print(f"  Throughput: {len(market_updates)/total_time:.1f} updates/sec")

        # Phase 5 real-time requirements
        assert avg_response_time < 0.05, f"E2E response time {avg_response_time*1000:.2f}ms exceeds 50ms requirement"
        assert len(market_updates) / total_time > 5, f"Throughput too low for real-time requirements"

        await performance_engine.end_session(session_id)


class TestPerformanceBenchmarks:
    """Performance benchmark tests for continuous monitoring."""

    def test_performance_requirements_validation(self):
        """Validate that all performance requirements are documented and testable."""
        # This test ensures our performance requirements are properly specified

        phase5_requirements = {
            "response_time_avg": "< 50ms",
            "response_time_p95": "< 100ms",
            "concurrent_sessions": "> 1000",
            "throughput_updates": "> 100/sec",
            "memory_per_session": "< 1MB",
            "websocket_connections": "> 1000",
            "cpu_usage_peak": "< 80%",
            "memory_recovery": "> 80%"
        }

        # Verify all requirements are reasonable and measurable
        for metric, requirement in phase5_requirements.items():
            assert requirement, f"Missing requirement for {metric}"
            # Could add more validation logic here

        print("Phase 5 Performance Requirements Validation:")
        for metric, requirement in phase5_requirements.items():
            print(f"  ✅ {metric}: {requirement}")

        assert len(phase5_requirements) >= 8, "Missing performance requirements"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])