#!/usr/bin/env python3
"""
Phase 6 Performance Optimization Tool
Advanced performance analysis and optimization recommendations for enterprise infrastructure
"""

import asyncio
import aiohttp
import json
import time
import psycopg2
import redis
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import logging
import argparse
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PerformanceBottleneck:
    component: str
    issue_type: str
    severity: str
    current_value: Any
    threshold_value: Any
    impact: str
    recommendations: List[str]
    estimated_improvement: str

@dataclass
class OptimizationStrategy:
    strategy_name: str
    description: str
    components_affected: List[str]
    implementation_complexity: str
    estimated_effort_hours: int
    expected_performance_gain: str
    prerequisites: List[str]
    implementation_steps: List[str]
    rollback_plan: str

@dataclass
class PerformanceReport:
    timestamp: str
    analysis_period: str
    bottlenecks_identified: List[PerformanceBottleneck]
    optimization_strategies: List[OptimizationStrategy]
    quick_wins: List[str]
    architectural_recommendations: List[str]
    monitoring_recommendations: List[str]
    overall_performance_score: int

class Phase6PerformanceOptimizer:
    def __init__(self):
        self.bottlenecks = []
        self.optimizations = []

    async def analyze_application_performance(self) -> List[PerformanceBottleneck]:
        """Analyze application-level performance bottlenecks"""
        bottlenecks = []

        endpoints = [
            ("FastAPI Health", "http://localhost:8001/health"),
            ("FastAPI Docs", "http://localhost:8001/docs"),
            ("Flask Health", "http://localhost:5000/health"),
            ("Kong Status", "http://localhost:8000/status"),
            ("Prometheus Health", "http://localhost:9090/-/healthy"),
            ("Grafana Health", "http://localhost:3000/api/health")
        ]

        for name, url in endpoints:
            try:
                start_time = time.time()
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                    async with session.get(url) as response:
                        response_time = (time.time() - start_time) * 1000

                        # Check for slow responses
                        if response_time > 1000:  # 1 second threshold
                            severity = "HIGH" if response_time > 5000 else "MEDIUM"
                            bottleneck = PerformanceBottleneck(
                                component=name,
                                issue_type="slow_response",
                                severity=severity,
                                current_value=f"{response_time:.1f}ms",
                                threshold_value="1000ms",
                                impact=f"User experience degradation, potential timeouts",
                                recommendations=[
                                    "Enable response compression",
                                    "Implement caching headers",
                                    "Optimize database queries",
                                    "Consider CDN integration"
                                ],
                                estimated_improvement="50-80% reduction in response time"
                            )
                            bottlenecks.append(bottleneck)

                        # Check for non-200 responses during health checks
                        if response.status != 200:
                            bottleneck = PerformanceBottleneck(
                                component=name,
                                issue_type="unhealthy_service",
                                severity="HIGH",
                                current_value=f"HTTP {response.status}",
                                threshold_value="HTTP 200",
                                impact="Service availability issues",
                                recommendations=[
                                    "Check service logs",
                                    "Verify dependencies",
                                    "Restart service if needed",
                                    "Review health check configuration"
                                ],
                                estimated_improvement="Service restoration"
                            )
                            bottlenecks.append(bottleneck)

            except Exception as e:
                bottleneck = PerformanceBottleneck(
                    component=name,
                    issue_type="connection_failure",
                    severity="CRITICAL",
                    current_value="Connection failed",
                    threshold_value="Successful connection",
                    impact="Service unavailable",
                    recommendations=[
                        "Check service status: docker-compose ps",
                        "Review service logs: docker-compose logs",
                        "Verify network connectivity",
                        "Check resource constraints"
                    ],
                    estimated_improvement="Service availability restoration"
                )
                bottlenecks.append(bottleneck)

        return bottlenecks

    def analyze_database_performance(self) -> List[PerformanceBottleneck]:
        """Analyze database performance bottlenecks"""
        bottlenecks = []

        try:
            # PostgreSQL analysis
            conn = psycopg2.connect(
                host="localhost", port=5432, database="tradingrobotplug",
                user="postgres", password="postgres"
            )
            cursor = conn.cursor()

            # Check active connections
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
            active_connections = cursor.fetchone()[0]

            if active_connections > 50:  # Threshold
                bottleneck = PerformanceBottleneck(
                    component="PostgreSQL",
                    issue_type="high_connection_count",
                    severity="MEDIUM" if active_connections < 100 else "HIGH",
                    current_value=active_connections,
                    threshold_value="50",
                    impact="Connection pool exhaustion, slow queries",
                    recommendations=[
                        "Increase max_connections in postgresql.conf",
                        "Implement connection pooling (pgbouncer)",
                        "Optimize application connection usage",
                        "Monitor connection lifecycle"
                    ],
                    estimated_improvement="30-50% reduction in connection overhead"
                )
                bottlenecks.append(bottleneck)

            # Check cache hit ratio
            cursor.execute("""
                SELECT sum(blks_hit)*100/sum(blks_hit+blks_read) as cache_hit_ratio
                FROM pg_stat_database WHERE datname = 'tradingrobotplug'
            """)
            cache_hit_ratio = cursor.fetchone()[0] or 0

            if cache_hit_ratio < 95:  # Threshold
                bottleneck = PerformanceBottleneck(
                    component="PostgreSQL",
                    issue_type="low_cache_hit_ratio",
                    severity="MEDIUM",
                    current_value=f"{cache_hit_ratio:.1f}%",
                    threshold_value="95%",
                    impact="Increased disk I/O, slower queries",
                    recommendations=[
                        "Increase shared_buffers",
                        "Optimize working memory (work_mem)",
                        "Review query patterns for optimization",
                        "Consider query result caching"
                    ],
                    estimated_improvement="20-40% improvement in query performance"
                )
                bottlenecks.append(bottleneck)

            # Check slow queries
            cursor.execute("""
                SELECT count(*) FROM pg_stat_statements
                WHERE mean_time > 1000 AND calls > 10
            """)
            slow_queries = cursor.fetchone()[0]

            if slow_queries > 0:
                bottleneck = PerformanceBottleneck(
                    component="PostgreSQL",
                    issue_type="slow_queries",
                    severity="MEDIUM",
                    current_value=f"{slow_queries} slow queries",
                    threshold_value="0 slow queries",
                    impact="Degraded application performance",
                    recommendations=[
                        "Analyze slow query logs",
                        "Add appropriate indexes",
                        "Rewrite inefficient queries",
                        "Enable query plan analysis"
                    ],
                    estimated_improvement="Significant query performance improvement"
                )
                bottlenecks.append(bottleneck)

            cursor.close()
            conn.close()

        except Exception as e:
            logger.warning(f"PostgreSQL analysis failed: {e}")

        try:
            # Redis analysis
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            info = info = r.info()

            # Check memory usage
            used_memory = info.get('used_memory', 0) / (1024 * 1024)  # MB
            max_memory = info.get('maxmemory', 512 * 1024 * 1024) / (1024 * 1024)  # MB
            memory_usage_pct = (used_memory / max_memory) * 100 if max_memory > 0 else 0

            if memory_usage_pct > 80:
                bottleneck = PerformanceBottleneck(
                    component="Redis",
                    issue_type="high_memory_usage",
                    severity="HIGH" if memory_usage_pct > 90 else "MEDIUM",
                    current_value=f"{memory_usage_pct:.1f}%",
                    threshold_value="80%",
                    impact="Cache eviction, performance degradation",
                    recommendations=[
                        "Increase maxmemory setting",
                        "Implement memory optimization strategies",
                        "Configure appropriate eviction policy",
                        "Monitor memory usage trends"
                    ],
                    estimated_improvement="Improved cache hit ratios and response times"
                )
                bottlenecks.append(bottleneck)

            # Check connected clients
            connected_clients = info.get('connected_clients', 0)
            if connected_clients > 100:
                bottleneck = PerformanceBottleneck(
                    component="Redis",
                    issue_type="high_client_connections",
                    severity="MEDIUM",
                    current_value=connected_clients,
                    threshold_value="100",
                    impact="Connection overhead, resource contention",
                    recommendations=[
                        "Implement connection pooling",
                        "Review client connection patterns",
                        "Configure appropriate timeouts",
                        "Consider Redis clustering"
                    ],
                    estimated_improvement="Reduced connection overhead"
                )
                bottlenecks.append(bottleneck)

            r.close()

        except Exception as e:
            logger.warning(f"Redis analysis failed: {e}")

        return bottlenecks

    def analyze_system_performance(self) -> List[PerformanceBottleneck]:
        """Analyze system-level performance bottlenecks"""
        bottlenecks = []

        try:
            # CPU usage analysis
            result = subprocess.run(
                ['bash', '-c', 'top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\\1/" | awk \'{print 100 - $1}\''],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                cpu_usage = float(result.stdout.strip())
                if cpu_usage > 80:
                    severity = "CRITICAL" if cpu_usage > 95 else "HIGH" if cpu_usage > 90 else "MEDIUM"
                    bottleneck = PerformanceBottleneck(
                        component="System CPU",
                        issue_type="high_cpu_usage",
                        severity=severity,
                        current_value=f"{cpu_usage:.1f}%",
                        threshold_value="80%",
                        impact="Slow response times, service degradation",
                        recommendations=[
                            "Scale application horizontally",
                            "Optimize CPU-intensive operations",
                            "Profile application for bottlenecks",
                            "Consider CPU upgrade or optimization"
                        ],
                        estimated_improvement="30-60% improvement in response times"
                    )
                    bottlenecks.append(bottleneck)

            # Memory usage analysis
            result = subprocess.run(
                ['bash', '-c', 'free | grep Mem | awk \'{printf "%.1f", $3/$2 * 100.0}\''],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                memory_usage = float(result.stdout.strip())
                if memory_usage > 85:
                    severity = "CRITICAL" if memory_usage > 95 else "HIGH" if memory_usage > 90 else "MEDIUM"
                    bottleneck = PerformanceBottleneck(
                        component="System Memory",
                        issue_type="high_memory_usage",
                        severity=severity,
                        current_value=f"{memory_usage:.1f}%",
                        threshold_value="85%",
                        impact="Memory pressure, potential OOM kills",
                        recommendations=[
                            "Increase memory limits",
                            "Optimize memory usage in applications",
                            "Implement memory monitoring",
                            "Consider memory upgrade"
                        ],
                        estimated_improvement="Reduced memory pressure and OOM risks"
                    )
                    bottlenecks.append(bottleneck)

            # Disk I/O analysis
            result = subprocess.run(
                ['bash', '-c', 'iostat -x 1 1 | grep -A1 "Device" | tail -1 | awk \'{print $14}\''],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                try:
                    disk_utilization = float(result.stdout.strip())
                    if disk_utilization > 80:
                        bottleneck = PerformanceBottleneck(
                            component="Disk I/O",
                            issue_type="high_disk_utilization",
                            severity="MEDIUM" if disk_utilization < 95 else "HIGH",
                            current_value=f"{disk_utilization:.1f}%",
                            threshold_value="80%",
                            impact="Slow I/O operations, application stalls",
                            recommendations=[
                                "Implement I/O optimization strategies",
                                "Consider SSD upgrade",
                                "Optimize disk access patterns",
                                "Implement caching layers"
                            ],
                            estimated_improvement="50-70% improvement in I/O performance"
                        )
                        bottlenecks.append(bottleneck)
                except ValueError:
                    pass  # Could not parse disk utilization

        except Exception as e:
            logger.warning(f"System performance analysis failed: {e}")

        return bottlenecks

    def generate_optimization_strategies(self, bottlenecks: List[PerformanceBottleneck]) -> List[OptimizationStrategy]:
        """Generate comprehensive optimization strategies"""
        strategies = []

        # Database optimization strategy
        db_bottlenecks = [b for b in bottlenecks if "PostgreSQL" in b.component or "Redis" in b.component]
        if db_bottlenecks:
            strategy = OptimizationStrategy(
                strategy_name="database_performance_optimization",
                description="Comprehensive database performance optimization including query tuning, indexing, and connection pooling",
                components_affected=["PostgreSQL", "Redis", "Application Services"],
                implementation_complexity="MEDIUM",
                estimated_effort_hours=16,
                expected_performance_gain="40-60% improvement in database response times",
                prerequisites=[
                    "Database administrator access",
                    "Application downtime window (optional)",
                    "Backup of current database"
                ],
                implementation_steps=[
                    "Analyze slow query logs and execution plans",
                    "Add missing indexes based on query patterns",
                    "Optimize connection pooling configuration",
                    "Implement query result caching where appropriate",
                    "Tune database memory parameters",
                    "Monitor performance improvements"
                ],
                rollback_plan="Restore database from backup if performance degrades"
            )
            strategies.append(strategy)

        # Application scaling strategy
        app_bottlenecks = [b for b in bottlenecks if any(service in b.component for service in ["FastAPI", "Flask", "Kong"])]
        if app_bottlenecks:
            strategy = OptimizationStrategy(
                strategy_name="horizontal_application_scaling",
                description="Scale application services horizontally to distribute load and improve performance",
                components_affected=["FastAPI", "Flask", "Kong", "Load Balancer"],
                implementation_complexity="LOW",
                estimated_effort_hours=4,
                expected_performance_gain="50-80% improvement in throughput and response times",
                prerequisites=[
                    "Load balancer configuration",
                    "Sufficient server resources",
                    "Session management strategy"
                ],
                implementation_steps=[
                    "Update docker-compose.yml with replica counts",
                    "Configure load balancer for service discovery",
                    "Test load distribution across replicas",
                    "Monitor resource usage and adjust as needed",
                    "Update monitoring alerts for new replica counts"
                ],
                rollback_plan="Reduce replica count to original values"
            )
            strategies.append(strategy)

        # Caching optimization strategy
        cache_bottlenecks = [b for b in bottlenecks if "cache" in b.issue_type.lower() or "Redis" in b.component]
        if cache_bottlenecks or len([b for b in bottlenecks if b.issue_type == "slow_response"]) > 2:
            strategy = OptimizationStrategy(
                strategy_name="multi_layer_caching_strategy",
                description="Implement multi-layer caching strategy including application-level, database query, and CDN caching",
                components_affected=["Application Services", "Redis", "CDN", "Nginx"],
                implementation_complexity="MEDIUM",
                estimated_effort_hours=12,
                expected_performance_gain="60-80% reduction in response times for cached content",
                prerequisites=[
                    "Redis cluster availability",
                    "CDN service configuration",
                    "Cache invalidation strategy"
                ],
                implementation_steps=[
                    "Configure Redis for application caching",
                    "Implement database query result caching",
                    "Set up CDN for static asset caching",
                    "Configure cache headers and TTL values",
                    "Implement cache invalidation mechanisms",
                    "Monitor cache hit ratios and performance"
                ],
                rollback_plan="Disable caching layers if issues arise"
            )
            strategies.append(strategy)

        # System optimization strategy
        system_bottlenecks = [b for b in bottlenecks if "System" in b.component]
        if system_bottlenecks:
            strategy = OptimizationStrategy(
                strategy_name="system_resource_optimization",
                description="Optimize system resource allocation and configuration for better performance",
                components_affected=["System Resources", "Docker", "Kernel"],
                implementation_complexity="HIGH",
                estimated_effort_hours=20,
                expected_performance_gain="25-40% improvement in system-level performance",
                prerequisites=[
                    "Root system access",
                    "System maintenance window",
                    "Current system baseline metrics"
                ],
                implementation_steps=[
                    "Analyze current system configuration",
                    "Optimize kernel parameters for performance",
                    "Tune Docker daemon configuration",
                    "Implement system-level caching",
                    "Configure CPU and memory affinity",
                    "Monitor system performance improvements"
                ],
                rollback_plan="Restore previous system configuration from backup"
            )
            strategies.append(strategy)

        return strategies

    def generate_quick_wins(self, bottlenecks: List[PerformanceBottleneck]) -> List[str]:
        """Generate quick optimization wins (low effort, high impact)"""
        quick_wins = []

        # Configuration optimizations
        if any(b.issue_type == "slow_response" for b in bottlenecks):
            quick_wins.extend([
                "Enable gzip compression in nginx.conf",
                "Configure appropriate cache headers for static assets",
                "Optimize database connection pool settings"
            ])

        # Resource optimizations
        if any("memory" in b.issue_type.lower() for b in bottlenecks):
            quick_wins.extend([
                "Increase container memory limits in docker-compose.yml",
                "Implement memory usage monitoring alerts",
                "Review and optimize application memory usage"
            ])

        # Monitoring improvements
        quick_wins.extend([
            "Enable query logging in PostgreSQL for performance analysis",
            "Configure Redis slow log monitoring",
            "Set up application performance profiling"
        ])

        return quick_wins

    def generate_monitoring_recommendations(self, bottlenecks: List[PerformanceBottleneck]) -> List[str]:
        """Generate monitoring and alerting recommendations"""
        recommendations = []

        # Always include basic monitoring
        recommendations.extend([
            "Implement comprehensive application performance monitoring (APM)",
            "Set up real-time alerting for performance thresholds",
            "Configure detailed logging for performance troubleshooting"
        ])

        # Specific recommendations based on bottlenecks
        if any("database" in b.component.lower() for b in bottlenecks):
            recommendations.extend([
                "Monitor database connection pool utilization",
                "Track slow query performance and trends",
                "Set up database performance dashboards"
            ])

        if any("redis" in b.component.lower() for b in bottlenecks):
            recommendations.extend([
                "Monitor Redis memory usage and eviction rates",
                "Track cache hit ratios over time",
                "Set up Redis performance dashboards"
            ])

        if any("cpu" in b.issue_type.lower() or "memory" in b.issue_type.lower() for b in bottlenecks):
            recommendations.extend([
                "Implement system resource monitoring and alerting",
                "Configure auto-scaling based on resource utilization",
                "Set up capacity planning dashboards"
            ])

        return recommendations

    def calculate_performance_score(self, bottlenecks: List[PerformanceBottleneck]) -> int:
        """Calculate overall performance score (0-100)"""
        if not bottlenecks:
            return 100

        # Start with perfect score and deduct points for issues
        score = 100

        severity_weights = {
            "CRITICAL": 20,
            "HIGH": 10,
            "MEDIUM": 5,
            "LOW": 2
        }

        for bottleneck in bottlenecks:
            weight = severity_weights.get(bottleneck.severity, 0)
            score -= weight

        # Ensure score doesn't go below 0
        return max(0, score)

    def generate_performance_report(self) -> PerformanceReport:
        """Generate comprehensive performance optimization report"""
        logger.info("🔍 Analyzing system performance for optimization opportunities...")

        # Analyze all components
        app_bottlenecks = asyncio.run(self.analyze_application_performance())
        db_bottlenecks = self.analyze_database_performance()
        system_bottlenecks = self.analyze_system_performance()

        all_bottlenecks = app_bottlenecks + db_bottlenecks + system_bottlenecks
        self.bottlenecks = all_bottlenecks

        # Generate optimization strategies
        optimization_strategies = self.generate_optimization_strategies(all_bottlenecks)

        # Generate recommendations
        quick_wins = self.generate_quick_wins(all_bottlenecks)
        monitoring_recommendations = self.generate_monitoring_recommendations(all_bottlenecks)

        # Generate architectural recommendations
        architectural_recommendations = [
            "Consider implementing service mesh for better observability",
            "Evaluate microservices architecture for better scalability",
            "Implement circuit breakers for resilient service communication",
            "Consider read replicas for database scaling",
            "Implement CDN integration for global performance improvement"
        ]

        # Calculate performance score
        performance_score = self.calculate_performance_score(all_bottlenecks)

        report = PerformanceReport(
            timestamp=datetime.now().isoformat(),
            analysis_period="Current system state",
            bottlenecks_identified=all_bottlenecks,
            optimization_strategies=optimization_strategies,
            quick_wins=quick_wins,
            architectural_recommendations=architectural_recommendations,
            monitoring_recommendations=monitoring_recommendations,
            overall_performance_score=performance_score
        )

        return report

    def print_performance_report(self, report: PerformanceReport):
        """Print comprehensive performance optimization report"""
        print("\n" + "="*100)
        print("🚀 PHASE 6 PERFORMANCE OPTIMIZATION REPORT")
        print("="*100)

        print(f"📊 OVERALL PERFORMANCE SCORE: {report.overall_performance_score}/100")
        print(f"⏱️  ANALYSIS TIMESTAMP: {report.timestamp[:19]}")
        print(f"🔍 BOTTLENECKS IDENTIFIED: {len(report.bottlenecks_identified)}")

        # Performance score interpretation
        if report.overall_performance_score >= 90:
            print("✅ EXCELLENT: System performing optimally")
        elif report.overall_performance_score >= 75:
            print("⚠️  GOOD: Minor optimizations recommended")
        elif report.overall_performance_score >= 60:
            print("🟡 FAIR: Performance improvements needed")
        else:
            print("❌ POOR: Critical performance issues require immediate attention")

        print("\n" + "-"*100)
        print("🎯 CRITICAL BOTTLENECKS")
        print("-"*100)

        critical_bottlenecks = [b for b in report.bottlenecks_identified if b.severity == "CRITICAL"]
        if critical_bottlenecks:
            for i, bottleneck in enumerate(critical_bottlenecks, 1):
                print(f"\n{i}. {bottleneck.component} - {bottleneck.issue_type.upper()}")
                print(f"   Current: {bottleneck.current_value} | Threshold: {bottleneck.threshold_value}")
                print(f"   Impact: {bottleneck.impact}")
                print(f"   Estimated Improvement: {bottleneck.estimated_improvement}")
                print("   Recommendations:"                for rec in bottleneck.recommendations:
                    print(f"     • {rec}")
        else:
            print("   ✅ No critical bottlenecks identified")

        print("\n" + "-"*100)
        print("⚡ QUICK WINS (High Impact, Low Effort)")
        print("-"*100)

        for i, win in enumerate(report.quick_wins[:5], 1):  # Top 5
            print(f"{i}. {win}")

        print("\n" + "-"*100)
        print("🏗️  OPTIMIZATION STRATEGIES")
        print("-"*100)

        for i, strategy in enumerate(report.optimization_strategies, 1):
            print(f"\n{i}. {strategy.strategy_name.upper().replace('_', ' ')}")
            print(f"   Complexity: {strategy.implementation_complexity}")
            print(f"   Effort: {strategy.estimated_effort_hours} hours")
            print(f"   Expected Gain: {strategy.expected_performance_gain}")
            print("   Key Steps:"            for step in strategy.implementation_steps[:3]:  # First 3 steps
                print(f"     • {step}")

        print("\n" + "-"*100)
        print("📈 MONITORING RECOMMENDATIONS")
        print("-"*100)

        for i, rec in enumerate(report.monitoring_recommendations[:5], 1):  # Top 5
            print(f"{i}. {rec}")

        print("\n" + "="*100)

    def save_performance_report(self, report: PerformanceReport, filename: str = None):
        """Save performance report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase6_performance_report_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)

        logger.info(f"📄 Performance report saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 6 Performance Optimization Tool')
    parser.add_argument('--component', choices=['all', 'application', 'database', 'system'],
                       default='all', help='Component to analyze')
    parser.add_argument('--output', type=str, help='Output filename for performance report')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--threshold', type=int, default=75,
                       help='Performance score threshold for exit codes (default: 75)')

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    optimizer = Phase6PerformanceOptimizer()

    try:
        logger.info(f"🔍 Starting Phase 6 Performance Analysis for component: {args.component}")
        report = optimizer.generate_performance_report()

        if not report.bottlenecks_identified and not report.optimization_strategies:
            logger.warning("⚠️  No performance issues or optimization opportunities found")
            print("✅ No performance bottlenecks detected - system performing optimally")
            sys.exit(0)

        optimizer.print_performance_report(report)
        optimizer.save_performance_report(report, args.output)

        # Provide actionable summary
        bottleneck_count = len(report.bottlenecks_identified)
        strategy_count = len(report.optimization_strategies)

        logger.info(f"✅ Performance analysis complete - {bottleneck_count} bottlenecks, {strategy_count} strategies identified")
        print(f"\n📊 Summary: Performance Score {report.overall_performance_score}/100 - {bottleneck_count} bottlenecks, {strategy_count} optimization strategies")

        # Exit with code based on performance score and threshold
        if report.overall_performance_score >= args.threshold:
            logger.info(f"✅ Performance score {report.overall_performance_score} meets threshold {args.threshold}")
            sys.exit(0)  # Good performance
        elif report.overall_performance_score >= 50:
            logger.warning(f"⚠️  Performance score {report.overall_performance_score} below threshold {args.threshold}")
            sys.exit(1)  # Needs attention
        else:
            logger.error(f"❌ Critical performance issues detected (score: {report.overall_performance_score})")
            sys.exit(2)  # Critical issues

    except KeyboardInterrupt:
        logger.info("Performance optimization analysis interrupted by user")
        print("\n👋 Analysis interrupted")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Performance optimization analysis failed: {e}")
        print(f"\n❌ Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()