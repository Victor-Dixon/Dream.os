#!/usr/bin/env python3
"""
Phase 6 Capacity Planning Tool
Advanced capacity planning and scaling recommendations for enterprise infrastructure
"""

import json
import statistics
import math
from datetime import datetime, timedelta
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
class CapacityMetrics:
    timestamp: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_rx: float
    network_tx: float
    active_connections: int
    request_rate: float
    error_rate: float
    response_time: float

@dataclass
class ScalingRecommendation:
    service: str
    current_replicas: int
    recommended_replicas: int
    confidence_level: str
    reasoning: str
    projected_improvement: str
    implementation_steps: List[str]

@dataclass
class CapacityPlan:
    service_name: str
    current_capacity: Dict[str, Any]
    projected_growth: Dict[str, Any]
    scaling_recommendations: List[ScalingRecommendation]
    infrastructure_upgrades: List[str]
    timeline: str
    risk_assessment: str

class Phase6CapacityPlanner:
    def __init__(self):
        self.metrics_history = []
        self.baseline_period_days = 30
        self.growth_projection_months = 6

    def load_metrics_data(self, metrics_file: Optional[str] = None) -> List[CapacityMetrics]:
        """Load metrics data from monitoring snapshots"""
        metrics = []

        if metrics_file and Path(metrics_file).exists():
            with open(metrics_file, 'r') as f:
                data = json.load(f)
                # Parse metrics from monitoring snapshot
                # This would integrate with actual monitoring data
                pass
        else:
            # Generate sample metrics for demonstration
            metrics = self._generate_sample_metrics()

        return metrics

    def _generate_sample_metrics(self) -> List[CapacityMetrics]:
        """Generate sample metrics for capacity planning analysis"""
        import random
        metrics = []

        base_time = datetime.now() - timedelta(days=self.baseline_period_days)

        for i in range(self.baseline_period_days * 24):  # Hourly data for 30 days
            timestamp = base_time + timedelta(hours=i)

            # Simulate realistic usage patterns with daily/weekly cycles
            hour_of_day = timestamp.hour
            day_of_week = timestamp.weekday()

            # Base load with daily patterns
            base_cpu = 15 + (hour_of_day - 12) ** 2 * 0.5  # Higher during business hours
            base_memory = 60 + random.uniform(-5, 5)

            # Weekly patterns (higher on weekdays)
            weekday_multiplier = 1.2 if day_of_week < 5 else 0.8

            # Add some random variation and trends
            cpu_usage = min(95, base_cpu * weekday_multiplier + random.uniform(-3, 3))
            memory_usage = min(95, base_memory * weekday_multiplier + random.uniform(-2, 2))
            disk_usage = 34 + random.uniform(-1, 1)  # Relatively stable
            network_rx = random.uniform(10, 50)  # Mbps
            network_tx = random.uniform(5, 25)  # Mbps
            active_connections = int(random.uniform(50, 200))
            request_rate = random.uniform(100, 500)  # requests/second
            error_rate = random.uniform(0.1, 2.0)  # percentage
            response_time = random.uniform(50, 200)  # milliseconds

            # Add occasional spikes
            if random.random() < 0.05:  # 5% chance of spike
                cpu_usage *= 1.5
                memory_usage *= 1.3
                request_rate *= 2
                response_time *= 1.5

            metrics.append(CapacityMetrics(
                timestamp=timestamp.isoformat(),
                cpu_usage=round(cpu_usage, 1),
                memory_usage=round(memory_usage, 1),
                disk_usage=round(disk_usage, 1),
                network_rx=round(network_rx, 2),
                network_tx=round(network_tx, 2),
                active_connections=active_connections,
                request_rate=round(request_rate, 1),
                error_rate=round(error_rate, 2),
                response_time=round(response_time, 1)
            ))

        return metrics

    def analyze_capacity_trends(self, metrics: List[CapacityMetrics]) -> Dict[str, Any]:
        """Analyze capacity trends and predict future requirements"""
        if not metrics:
            return {}

        # Extract metric values
        cpu_values = [m.cpu_usage for m in metrics]
        memory_values = [m.memory_usage for m in metrics]
        disk_values = [m.disk_usage for m in metrics]
        network_rx_values = [m.network_rx for m in metrics]
        network_tx_values = [m.network_tx for m in metrics]
        connection_values = [m.active_connections for m in metrics]
        request_values = [m.request_rate for m in metrics]
        error_values = [m.error_rate for m in metrics]
        response_values = [m.response_time for m in metrics]

        # Calculate statistical measures
        analysis = {
            "cpu": {
                "current_avg": round(statistics.mean(cpu_values), 1),
                "peak": max(cpu_values),
                "p95": round(statistics.quantiles(cpu_values, n=20)[18], 1),
                "p99": round(statistics.quantiles(cpu_values, n=100)[98], 1),
                "trend": self._calculate_trend(cpu_values),
                "volatility": round(statistics.stdev(cpu_values), 1)
            },
            "memory": {
                "current_avg": round(statistics.mean(memory_values), 1),
                "peak": max(memory_values),
                "p95": round(statistics.quantiles(memory_values, n=20)[18], 1),
                "p99": round(statistics.quantiles(memory_values, n=100)[98], 1),
                "trend": self._calculate_trend(memory_values),
                "volatility": round(statistics.stdev(memory_values), 1)
            },
            "disk": {
                "current_avg": round(statistics.mean(disk_values), 1),
                "peak": max(disk_values),
                "trend": self._calculate_trend(disk_values),
                "volatility": round(statistics.stdev(disk_values), 1)
            },
            "network": {
                "rx_avg": round(statistics.mean(network_rx_values), 2),
                "tx_avg": round(statistics.mean(network_tx_values), 2),
                "rx_peak": max(network_rx_values),
                "tx_peak": max(network_tx_values),
                "trend": self._calculate_trend(network_rx_values + network_tx_values)
            },
            "connections": {
                "current_avg": round(statistics.mean(connection_values), 0),
                "peak": max(connection_values),
                "p95": round(statistics.quantiles(connection_values, n=20)[18], 0),
                "trend": self._calculate_trend(connection_values)
            },
            "performance": {
                "request_rate_avg": round(statistics.mean(request_values), 1),
                "request_rate_peak": max(request_values),
                "error_rate_avg": round(statistics.mean(error_values), 2),
                "response_time_avg": round(statistics.mean(response_values), 1),
                "response_time_p95": round(statistics.quantiles(response_values, n=20)[18], 1),
                "trend": self._calculate_trend(request_values)
            }
        }

        return analysis

    def _calculate_trend(self, values: List[float], window_size: int = 24) -> str:
        """Calculate trend direction using linear regression on recent window"""
        if len(values) < window_size * 2:
            return "insufficient_data"

        # Use recent window for trend analysis
        recent = values[-window_size:]
        x = list(range(len(recent)))
        y = recent

        # Simple linear regression
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi * xi for xi in x)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)

        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"

    def generate_scaling_recommendations(self, analysis: Dict[str, Any]) -> List[ScalingRecommendation]:
        """Generate scaling recommendations based on capacity analysis"""
        recommendations = []

        # CPU-based scaling recommendations
        cpu_analysis = analysis.get("cpu", {})
        if cpu_analysis.get("p95", 0) > 75:
            confidence = "high" if cpu_analysis.get("p95", 0) > 85 else "medium"

            rec = ScalingRecommendation(
                service="application_services",
                current_replicas=1,
                recommended_replicas=math.ceil(cpu_analysis.get("p95", 0) / 60),  # Target 60% per replica
                confidence_level=confidence,
                reasoning=f"CPU usage at 95th percentile ({cpu_analysis.get('p95')}%) exceeds threshold. {cpu_analysis.get('trend', 'stable').title()} trend indicates {'growing' if cpu_analysis.get('trend') == 'increasing' else 'stable'} demand.",
                projected_improvement=f"Expected {cpu_analysis.get('p95') // 2}% reduction in CPU usage per request",
                implementation_steps=[
                    "Update docker-compose.yml with new replica count",
                    "Test load balancer distribution",
                    "Monitor resource usage post-scaling",
                    "Update monitoring alerts for new replica count"
                ]
            )
            recommendations.append(rec)

        # Memory-based recommendations
        memory_analysis = analysis.get("memory", {})
        if memory_analysis.get("p95", 0) > 80:
            rec = ScalingRecommendation(
                service="application_services",
                current_replicas=1,
                recommended_replicas=math.ceil(memory_analysis.get("p95", 0) / 65),  # Target 65% per replica
                confidence_level="medium",
                reasoning=f"Memory usage at 95th percentile ({memory_analysis.get('p95')}%) indicates memory pressure.",
                projected_improvement="Distributed memory load across replicas",
                implementation_steps=[
                    "Increase memory limits in docker-compose.yml",
                    "Consider horizontal scaling for memory-intensive workloads",
                    "Implement memory monitoring alerts",
                    "Review application memory usage patterns"
                ]
            )
            recommendations.append(rec)

        # Connection-based recommendations
        conn_analysis = analysis.get("connections", {})
        if conn_analysis.get("p95", 0) > 150:
            rec = ScalingRecommendation(
                service="api_gateway",
                current_replicas=1,
                recommended_replicas=min(3, math.ceil(conn_analysis.get("p95", 0) / 100)),  # Target 100 connections per replica
                confidence_level="high",
                reasoning=f"Active connections at 95th percentile ({conn_analysis.get('p95')}) exceed recommended limits.",
                projected_improvement="Better connection distribution and reduced latency",
                implementation_steps=[
                    "Scale Kong API Gateway replicas",
                    "Configure load balancer for session affinity if needed",
                    "Monitor connection pooling efficiency",
                    "Update rate limiting configuration"
                ]
            )
            recommendations.append(rec)

        # Performance-based recommendations
        perf_analysis = analysis.get("performance", {})
        if perf_analysis.get("response_time_p95", 0) > 1000:  # 1 second
            rec = ScalingRecommendation(
                service="fastapi_app",
                current_replicas=1,
                recommended_replicas=2,
                confidence_level="medium",
                reasoning=f"Response time at 95th percentile ({perf_analysis.get('response_time_p95')}ms) indicates performance bottleneck.",
                projected_improvement="Parallel request processing and reduced queueing",
                implementation_steps=[
                    "Scale FastAPI application replicas",
                    "Ensure database connection pooling scales",
                    "Monitor async task performance",
                    "Consider CDN integration for static content"
                ]
            )
            recommendations.append(rec)

        return recommendations

    def project_future_requirements(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Project future capacity requirements based on trends"""
        projections = {}

        for metric_name, metric_data in analysis.items():
            trend = metric_data.get("trend", "stable")
            current_avg = metric_data.get("current_avg", 0)

            # Growth rate assumptions based on trend
            if trend == "increasing":
                monthly_growth_rate = 0.15  # 15% monthly growth
            elif trend == "decreasing":
                monthly_growth_rate = -0.05  # 5% monthly decline
            else:
                monthly_growth_rate = 0.05   # 5% monthly growth (conservative)

            # Project for 6 months
            projections[metric_name] = {}
            for month in range(1, self.growth_projection_months + 1):
                projected_value = current_avg * (1 + monthly_growth_rate) ** month
                projections[metric_name][f"month_{month}"] = round(projected_value, 1)

        return projections

    def generate_infrastructure_upgrades(self, analysis: Dict[str, Any], projections: Dict[str, Any]) -> List[str]:
        """Generate infrastructure upgrade recommendations"""
        upgrades = []

        # CPU upgrade recommendations
        cpu_projection = projections.get("cpu", {})
        max_projected_cpu = max(cpu_projection.values()) if cpu_projection else 0
        if max_projected_cpu > 80:
            upgrades.append("Consider upgrading to higher CPU instances or increasing replica count for CPU-intensive workloads")

        # Memory upgrade recommendations
        memory_projection = projections.get("memory", {})
        max_projected_memory = max(memory_projection.values()) if memory_projection else 0
        if max_projected_memory > 85:
            upgrades.append("Plan memory capacity upgrade - consider instances with more RAM or implement memory optimization strategies")

        # Network upgrade recommendations
        network_analysis = analysis.get("network", {})
        if network_analysis.get("rx_peak", 0) > 100 or network_analysis.get("tx_peak", 0) > 50:
            upgrades.append("Network bandwidth upgrade recommended for high-throughput workloads")

        # Storage upgrade recommendations
        disk_analysis = analysis.get("disk", {})
        if disk_analysis.get("current_avg", 0) > 70:
            upgrades.append("Storage capacity planning required - implement automated cleanup and consider SSD upgrades")

        # Database scaling recommendations
        conn_analysis = analysis.get("connections", {})
        if conn_analysis.get("peak", 0) > 500:
            upgrades.append("Database connection pooling and read replica implementation for high connection workloads")

        # Performance optimization recommendations
        perf_analysis = analysis.get("performance", {})
        if perf_analysis.get("request_rate_peak", 0) > 1000:
            upgrades.append("Implement caching layer (Redis/Varnish) and consider CDN integration for high-traffic scenarios")

        return upgrades

    def generate_capacity_plan(self, service_name: str = "infrastructure") -> CapacityPlan:
        """Generate comprehensive capacity plan"""
        logger.info("🔍 Generating Phase 6 Capacity Plan...")

        # Load and analyze metrics
        metrics = self.load_metrics_data()
        analysis = self.analyze_capacity_trends(metrics)
        projections = self.project_future_requirements(analysis)
        recommendations = self.generate_scaling_recommendations(analysis)
        upgrades = self.generate_infrastructure_upgrades(analysis, projections)

        # Assess risks
        risk_assessment = self._assess_capacity_risks(analysis, projections, recommendations)

        # Determine timeline
        timeline = "immediate" if any(r.confidence_level == "high" for r in recommendations) else "3-6_months"

        plan = CapacityPlan(
            service_name=service_name,
            current_capacity={
                "cpu_utilization": f"{analysis.get('cpu', {}).get('current_avg', 0)}%",
                "memory_utilization": f"{analysis.get('memory', {}).get('current_avg', 0)}%",
                "peak_connections": analysis.get('connections', {}).get('peak', 0),
                "avg_request_rate": f"{analysis.get('performance', {}).get('request_rate_avg', 0)} req/s",
                "avg_response_time": f"{analysis.get('performance', {}).get('response_time_avg', 0)}ms"
            },
            projected_growth={
                "cpu_growth_6months": f"{projections.get('cpu', {}).get('month_6', 0)}%",
                "memory_growth_6months": f"{projections.get('memory', {}).get('month_6', 0)}%",
                "connection_growth_6months": projections.get('connections', {}).get('month_6', 0),
                "request_growth_6months": f"{projections.get('performance', {}).get('month_6', 0)} req/s"
            },
            scaling_recommendations=recommendations,
            infrastructure_upgrades=upgrades,
            timeline=timeline,
            risk_assessment=risk_assessment
        )

        return plan

    def _assess_capacity_risks(self, analysis: Dict[str, Any], projections: Dict[str, Any], recommendations: List[ScalingRecommendation]) -> str:
        """Assess capacity-related risks"""
        risk_factors = []

        # High utilization risks
        cpu_analysis = analysis.get("cpu", {})
        if cpu_analysis.get("p95", 0) > 85:
            risk_factors.append("high_cpu_utilization")

        memory_analysis = analysis.get("memory", {})
        if memory_analysis.get("p95", 0) > 90:
            risk_factors.append("high_memory_utilization")

        # Trend risks
        if cpu_analysis.get("trend") == "increasing":
            risk_factors.append("increasing_cpu_trend")

        if memory_analysis.get("trend") == "increasing":
            risk_factors.append("increasing_memory_trend")

        # Performance risks
        perf_analysis = analysis.get("performance", {})
        if perf_analysis.get("error_rate_avg", 0) > 1.0:
            risk_factors.append("high_error_rate")

        if perf_analysis.get("response_time_p95", 0) > 2000:
            risk_factors.append("high_response_time")

        # Scaling risks
        if len(recommendations) > 2:
            risk_factors.append("multiple_scaling_needed")

        # Determine overall risk level
        if "high_cpu_utilization" in risk_factors or "high_memory_utilization" in risk_factors:
            risk_level = "CRITICAL"
        elif len(risk_factors) >= 3:
            risk_level = "HIGH"
        elif len(risk_factors) >= 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        risk_description = f"{risk_level} risk: {', '.join(risk_factors) if risk_factors else 'No significant risks identified'}"

        return risk_description

    def print_capacity_report(self, plan: CapacityPlan):
        """Print comprehensive capacity planning report"""
        print("\n" + "="*100)
        print("📊 PHASE 6 CAPACITY PLANNING REPORT")
        print("="*100)

        print(f"🎯 SERVICE: {plan.service_name}")
        print(f"⚠️  RISK ASSESSMENT: {plan.risk_assessment}")
        print(f"⏰ TIMELINE: {plan.timeline.replace('_', ' ').title()}")

        print("\n" + "-"*100)
        print("📈 CURRENT CAPACITY")
        print("-"*100)

        for metric, value in plan.current_capacity.items():
            print(f"  {metric.replace('_', ' ').title()}: {value}")

        print("\n" + "-"*100)
        print("🔮 PROJECTED GROWTH (6 Months)")
        print("-"*100)

        for metric, value in plan.projected_growth.items():
            print(f"  {metric.replace('_', ' ').replace('6months', '6 Months').title()}: {value}")

        print("\n" + "-"*100)
        print("⚖️  SCALING RECOMMENDATIONS")
        print("-"*100)

        if plan.scaling_recommendations:
            for i, rec in enumerate(plan.scaling_recommendations, 1):
                print(f"\n{i}. {rec.service.upper()} SCALING")
                print(f"   Current: {rec.current_replicas} replicas")
                print(f"   Recommended: {rec.recommended_replicas} replicas")
                print(f"   Confidence: {rec.confidence_level.upper()}")
                print(f"   Reasoning: {rec.reasoning}")
                print(f"   Improvement: {rec.projected_improvement}")
                print("   Implementation Steps:"                for step in rec.implementation_steps:
                    print(f"     • {step}")
        else:
            print("   ✅ No scaling recommendations needed at this time")

        print("\n" + "-"*100)
        print("🏗️  INFRASTRUCTURE UPGRADES")
        print("-"*100)

        if plan.infrastructure_upgrades:
            for i, upgrade in enumerate(plan.infrastructure_upgrades, 1):
                print(f"{i}. {upgrade}")
        else:
            print("   ✅ No infrastructure upgrades recommended")

        print("\n" + "="*100)

    def save_capacity_plan(self, plan: CapacityPlan, filename: str = None):
        """Save capacity plan to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase6_capacity_plan_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(asdict(plan), f, indent=2, default=str)

        logger.info(f"📄 Capacity plan saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 6 Capacity Planning Tool')
    parser.add_argument('--metrics-file', help='JSON file containing metrics data')
    parser.add_argument('--service', default='infrastructure', help='Service name for planning')
    parser.add_argument('--baseline-days', type=int, default=30, help='Baseline period in days')
    parser.add_argument('--projection-months', type=int, default=6, help='Projection period in months')
    parser.add_argument('--output', type=str, help='Output filename for capacity plan')

    args = parser.parse_args()

    planner = Phase6CapacityPlanner()
    planner.baseline_period_days = args.baseline_days
    planner.growth_projection_months = args.projection_months

    try:
        plan = planner.generate_capacity_plan(args.service)
        planner.print_capacity_report(plan)
        planner.save_capacity_plan(plan, args.output)

    except Exception as e:
        logger.error(f"Capacity planning failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()