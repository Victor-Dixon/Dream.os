#!/usr/bin/env python3
"""
Phase 6 Cost Optimization Tool
Infrastructure cost analysis and optimization recommendations for enterprise deployments
"""

import json
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
class CostComponent:
    service: str
    resource_type: str
    current_cost_monthly: float
    optimized_cost_monthly: float
    savings_percentage: float
    savings_monthly: float
    implementation_effort: str
    risk_level: str

@dataclass
class CostOptimizationStrategy:
    strategy_name: str
    description: str
    total_savings_monthly: float
    total_savings_percentage: float
    implementation_complexity: str
    estimated_effort_days: int
    prerequisites: List[str]
    implementation_steps: List[str]
    rollback_plan: str

@dataclass
class CostAnalysisReport:
    timestamp: str
    analysis_period_months: int
    total_current_cost: float
    total_optimized_cost: float
    total_savings_monthly: float
    total_savings_percentage: float
    cost_components: List[CostComponent]
    optimization_strategies: List[CostOptimizationStrategy]
    quick_savings: List[str]
    architectural_changes: List[str]
    monitoring_recommendations: List[str]
    cost_score: int

class Phase6CostOptimizer:
    def __init__(self):
        self.cost_components = []

        # Cost assumptions (adjustable based on actual cloud provider rates)
        self.cost_rates = {
            "cpu_hour": 0.096,      # vCPU per hour (c6i.large equivalent)
            "memory_gb_hour": 0.012, # GB RAM per hour
            "storage_gb_month": 0.12,  # EBS gp3 per GB/month
            "data_transfer_gb": 0.09,  # Outbound data transfer
            "redis_gb_hour": 0.034,   # ElastiCache Redis per GB/hour
            "postgres_gb_hour": 0.034, # RDS PostgreSQL per GB/hour
            "load_balancer_hour": 0.0225, # ALB per hour
            "nat_gateway_hour": 0.045,     # NAT Gateway per hour
        }

    def analyze_infrastructure_costs(self) -> List[CostComponent]:
        """Analyze current infrastructure costs and identify optimization opportunities"""
        components = []

        # Application servers cost analysis
        app_servers_cost = self._calculate_application_servers_cost()
        if app_servers_cost:
            components.extend(app_servers_cost)

        # Database costs
        db_costs = self._calculate_database_costs()
        components.extend(db_costs)

        # Storage costs
        storage_costs = self._calculate_storage_costs()
        components.extend(storage_costs)

        # Network costs
        network_costs = self._calculate_network_costs()
        components.extend(network_costs)

        # Monitoring and logging costs
        monitoring_costs = self._calculate_monitoring_costs()
        components.extend(monitoring_costs)

        return components

    def _calculate_application_servers_cost(self) -> List[CostComponent]:
        """Calculate application server costs with optimization opportunities"""
        components = []

        # Assume current setup: 2 application servers
        current_servers = 2
        cpu_per_server = 2      # vCPUs
        memory_per_server = 4   # GB RAM
        hours_per_month = 730    # ~30.4 days

        # Current costs
        current_cpu_cost = current_servers * cpu_per_server * self.cost_rates["cpu_hour"] * hours_per_month
        current_memory_cost = current_servers * memory_per_server * self.cost_rates["memory_gb_hour"] * hours_per_month
        current_total = current_cpu_cost + current_memory_cost

        # Optimization 1: Rightsize instances
        optimized_servers = 2  # Keep same count but rightsize
        optimized_cpu_per_server = 1.5  # Reduce CPU allocation
        optimized_memory_per_server = 3  # Reduce memory allocation

        optimized_cpu_cost = optimized_servers * optimized_cpu_per_server * self.cost_rates["cpu_hour"] * hours_per_month
        optimized_memory_cost = optimized_servers * optimized_memory_per_server * self.cost_rates["memory_gb_hour"] * hours_per_month
        optimized_total = optimized_cpu_cost + optimized_memory_cost

        savings = current_total - optimized_total
        savings_pct = (savings / current_total) * 100

        component = CostComponent(
            service="Application Servers",
            resource_type="Compute Resources",
            current_cost_monthly=round(current_total, 2),
            optimized_cost_monthly=round(optimized_total, 2),
            savings_percentage=round(savings_pct, 1),
            savings_monthly=round(savings, 2),
            implementation_effort="LOW",
            risk_level="LOW"
        )
        components.append(component)

        # Optimization 2: Reserved instances
        ri_discount = 0.6  # 40% savings with 3-year reserved instances
        ri_cost = current_total * (1 - ri_discount)
        ri_savings = current_total - ri_cost
        ri_savings_pct = ri_discount * 100

        ri_component = CostComponent(
            service="Application Servers",
            resource_type="Reserved Instances",
            current_cost_monthly=round(current_total, 2),
            optimized_cost_monthly=round(ri_cost, 2),
            savings_percentage=round(ri_savings_pct, 1),
            savings_monthly=round(ri_savings, 2),
            implementation_effort="MEDIUM",
            risk_level="LOW"
        )
        components.append(ri_component)

        return components

    def _calculate_database_costs(self) -> List[CostComponent]:
        """Calculate database costs with optimization opportunities"""
        components = []

        # PostgreSQL costs
        storage_gb = 100
        backup_storage_gb = 200
        hours_per_month = 730

        # Current costs
        compute_cost = 2 * self.cost_rates["cpu_hour"] * hours_per_month  # 2 vCPUs
        storage_cost = storage_gb * self.cost_rates["postgres_gb_hour"] * hours_per_month
        backup_cost = backup_storage_gb * self.cost_rates["storage_gb_month"]
        current_total = compute_cost + storage_cost + backup_cost

        # Optimization: Use Aurora Serverless v2
        aurora_cost = current_total * 0.7  # ~30% savings with Aurora
        aurora_savings = current_total - aurora_cost
        aurora_savings_pct = (aurora_savings / current_total) * 100

        component = CostComponent(
            service="PostgreSQL Database",
            resource_type="Managed Database Service",
            current_cost_monthly=round(current_total, 2),
            optimized_cost_monthly=round(aurora_cost, 2),
            savings_percentage=round(aurora_savings_pct, 1),
            savings_monthly=round(aurora_savings, 2),
            implementation_effort="HIGH",
            risk_level="MEDIUM"
        )
        components.append(component)

        # Redis costs
        redis_memory_gb = 4
        redis_compute_cost = 1 * self.cost_rates["cpu_hour"] * hours_per_month  # 1 vCPU
        redis_storage_cost = redis_memory_gb * self.cost_rates["redis_gb_hour"] * hours_per_month
        redis_current_total = redis_compute_cost + redis_storage_cost

        # Optimization: Use ElastiCache instead of EC2-based Redis
        elasticache_cost = redis_current_total * 0.8  # ~20% savings
        elasticache_savings = redis_current_total - elasticache_cost
        elasticache_savings_pct = (elasticache_savings / redis_current_total) * 100

        redis_component = CostComponent(
            service="Redis Cache",
            resource_type="Managed Cache Service",
            current_cost_monthly=round(redis_current_total, 2),
            optimized_cost_monthly=round(elasticache_cost, 2),
            savings_percentage=round(elasticache_savings_pct, 1),
            savings_monthly=round(elasticache_savings, 2),
            implementation_effort="MEDIUM",
            risk_level="LOW"
        )
        components.append(redis_component)

        return components

    def _calculate_storage_costs(self) -> List[CostComponent]:
        """Calculate storage costs with optimization opportunities"""
        components = []

        # Current storage costs
        ebs_storage_gb = 500
        snapshot_storage_gb = 1000
        current_total = (ebs_storage_gb + snapshot_storage_gb) * self.cost_rates["storage_gb_month"]

        # Optimization: Use cheaper storage tiers
        optimized_ebs_gb = 300  # Reduce allocated storage
        optimized_snapshot_gb = 500  # Reduce snapshot retention
        optimized_total = (optimized_ebs_gb + optimized_snapshot_gb) * self.cost_rates["storage_gb_month"] * 0.9  # Cheaper tier

        savings = current_total - optimized_total
        savings_pct = (savings / current_total) * 100

        component = CostComponent(
            service="Storage (EBS + Snapshots)",
            resource_type="Block Storage",
            current_cost_monthly=round(current_total, 2),
            optimized_cost_monthly=round(optimized_total, 2),
            savings_percentage=round(savings_pct, 1),
            savings_monthly=round(savings, 2),
            implementation_effort="LOW",
            risk_level="LOW"
        )
        components.append(component)

        return components

    def _calculate_network_costs(self) -> List[CostComponent]:
        """Calculate network costs with optimization opportunities"""
        components = []

        # Current network costs (NAT Gateway + Data Transfer)
        nat_gateway_cost = 1 * self.cost_rates["nat_gateway_hour"] * 730  # 1 NAT Gateway
        data_transfer_gb = 1000  # Outbound data transfer
        data_transfer_cost = data_transfer_gb * self.cost_rates["data_transfer_gb"]
        current_total = nat_gateway_cost + data_transfer_cost

        # Optimization: Use VPC endpoints and reduce data transfer
        optimized_nat_cost = nat_gateway_cost * 0.5  # Reduce NAT Gateway usage with VPC endpoints
        optimized_data_transfer = data_transfer_gb * 0.7  # Compress and optimize data transfer
        optimized_data_cost = optimized_data_transfer * self.cost_rates["data_transfer_gb"]
        optimized_total = optimized_nat_cost + optimized_data_cost

        savings = current_total - optimized_total
        savings_pct = (savings / current_total) * 100

        component = CostComponent(
            service="Network (NAT Gateway + Data Transfer)",
            resource_type="Network Infrastructure",
            current_cost_monthly=round(current_total, 2),
            optimized_cost_monthly=round(optimized_total, 2),
            savings_percentage=round(savings_pct, 1),
            savings_monthly=round(savings, 2),
            implementation_effort="MEDIUM",
            risk_level="LOW"
        )
        components.append(component)

        return components

    def _calculate_monitoring_costs(self) -> List[CostComponent]:
        """Calculate monitoring and logging costs"""
        components = []

        # CloudWatch costs (estimated)
        logs_gb = 50  # GB of logs per month
        metrics = 100  # Custom metrics
        dashboards = 5

        # Rough cost estimates
        logs_cost = logs_gb * 0.50  # $0.50 per GB
        metrics_cost = metrics * 0.30  # $0.30 per metric
        dashboard_cost = dashboards * 3.00  # $3 per dashboard
        current_total = logs_cost + metrics_cost + dashboard_cost

        # Optimization: Reduce log retention and optimize metrics
        optimized_logs_gb = 20  # Reduce retention
        optimized_metrics = 50  # Reduce custom metrics
        optimized_logs_cost = optimized_logs_gb * 0.50
        optimized_metrics_cost = optimized_metrics * 0.30
        optimized_total = optimized_logs_cost + optimized_metrics_cost + dashboard_cost

        savings = current_total - optimized_total
        savings_pct = (savings / current_total) * 100

        component = CostComponent(
            service="Monitoring (CloudWatch)",
            resource_type="Observability Services",
            current_cost_monthly=round(current_total, 2),
            optimized_cost_monthly=round(optimized_total, 2),
            savings_percentage=round(savings_pct, 1),
            savings_monthly=round(savings, 2),
            implementation_effort="LOW",
            risk_level="LOW"
        )
        components.append(component)

        return components

    def generate_optimization_strategies(self, components: List[CostComponent]) -> List[CostOptimizationStrategy]:
        """Generate comprehensive cost optimization strategies"""
        strategies = []

        # Strategy 1: Reserved Instances
        ri_components = [c for c in components if "Reserved Instances" in c.resource_type]
        if ri_components:
            total_current = sum(c.current_cost_monthly for c in ri_components)
            total_optimized = sum(c.optimized_cost_monthly for c in ri_components)
            total_savings = total_current - total_optimized
            total_savings_pct = (total_savings / total_current) * 100 if total_current > 0 else 0

            strategy = CostOptimizationStrategy(
                strategy_name="reserved_instances_program",
                description="Commit to reserved instances for stable workloads to reduce compute costs by 40%",
                total_savings_monthly=round(total_savings, 2),
                total_savings_percentage=round(total_savings_pct, 1),
                implementation_complexity="MEDIUM",
                estimated_effort_days=5,
                prerequisites=[
                    "3-year commitment planning",
                    "Workload stability analysis",
                    "Budget approval for upfront costs"
                ],
                implementation_steps=[
                    "Analyze workload patterns for reservation candidates",
                    "Calculate reserved instance purchase amounts",
                    "Purchase reserved instances through AWS console",
                    "Tag resources for cost allocation",
                    "Monitor utilization and coverage metrics"
                ],
                rollback_plan="Reserved instances can be sold on the reserved instance marketplace"
            )
            strategies.append(strategy)

        # Strategy 2: Managed Services Migration
        managed_components = [c for c in components if "Managed" in c.resource_type]
        if managed_components:
            total_current = sum(c.current_cost_monthly for c in managed_components)
            total_optimized = sum(c.optimized_cost_monthly for c in managed_components)
            total_savings = total_current - total_optimized
            total_savings_pct = (total_savings / total_current) * 100 if total_current > 0 else 0

            strategy = CostOptimizationStrategy(
                strategy_name="managed_services_migration",
                description="Migrate self-managed databases to fully managed services for better performance and cost efficiency",
                total_savings_monthly=round(total_savings, 2),
                total_savings_percentage=round(total_savings_pct, 1),
                implementation_complexity="HIGH",
                estimated_effort_days=14,
                prerequisites=[
                    "Database schema compatibility verification",
                    "Application connection string updates",
                    "Backup and recovery strategy validation",
                    "Performance testing environment"
                ],
                implementation_steps=[
                    "Create managed database instances",
                    "Migrate data using AWS DMS or similar tools",
                    "Update application configurations",
                    "Test application functionality",
                    "Switch traffic to managed databases",
                    "Monitor performance and costs"
                ],
                rollback_plan="Switch back to self-managed databases with data restoration from backups"
            )
            strategies.append(strategy)

        # Strategy 3: Storage Optimization
        storage_components = [c for c in components if "Storage" in c.resource_type]
        if storage_components:
            total_current = sum(c.current_cost_monthly for c in storage_components)
            total_optimized = sum(c.optimized_cost_monthly for c in storage_components)
            total_savings = total_current - total_optimized
            total_savings_pct = (total_savings / total_current) * 100 if total_current > 0 else 0

            strategy = CostOptimizationStrategy(
                strategy_name="storage_optimization",
                description="Optimize storage usage through rightsizing, tiering, and lifecycle policies",
                total_savings_monthly=round(total_savings, 2),
                total_savings_percentage=round(total_savings_pct, 1),
                implementation_complexity="LOW",
                estimated_effort_days=3,
                prerequisites=[
                    "Storage usage analysis",
                    "Data classification and retention policies",
                    "Backup strategy review"
                ],
                implementation_steps=[
                    "Analyze current storage usage and growth patterns",
                    "Implement storage lifecycle policies",
                    "Rightsize EBS volumes and snapshots",
                    "Configure automated cleanup jobs",
                    "Monitor storage costs and utilization"
                ],
                rollback_plan="Remove lifecycle policies and restore previous storage allocations"
            )
            strategies.append(strategy)

        return strategies

    def generate_quick_savings(self) -> List[str]:
        """Generate quick cost-saving opportunities"""
        quick_savings = [
            "Stop unused development environments after hours",
            "Delete unattached EBS volumes and old snapshots",
            "Use spot instances for non-critical workloads",
            "Implement auto-scaling to reduce over-provisioning",
            "Configure CloudWatch billing alerts",
            "Use compression for CloudWatch logs",
            "Delete unused load balancers and NAT gateways",
            "Optimize data transfer by using CloudFront",
            "Use VPC endpoints to reduce NAT Gateway costs",
            "Implement instance scheduling for non-production environments"
        ]
        return quick_savings

    def calculate_cost_score(self, components: List[CostComponent]) -> int:
        """Calculate cost optimization score (0-100)"""
        if not components:
            return 100

        total_current = sum(c.current_cost_monthly for c in components)
        total_optimized = sum(c.optimized_cost_monthly for c in components)

        if total_current == 0:
            return 100

        optimization_ratio = (total_current - total_optimized) / total_current
        score = min(100, optimization_ratio * 100)

        return round(score)

    def generate_cost_report(self) -> CostAnalysisReport:
        """Generate comprehensive cost analysis report"""
        logger.info("💰 Analyzing infrastructure costs for optimization opportunities...")

        # Analyze all cost components
        cost_components = self.analyze_infrastructure_costs()

        # Generate optimization strategies
        optimization_strategies = self.generate_optimization_strategies(cost_components)

        # Calculate totals
        total_current = sum(c.current_cost_monthly for c in cost_components)
        total_optimized = sum(c.optimized_cost_monthly for c in cost_components)
        total_savings_monthly = total_current - total_optimized
        total_savings_percentage = (total_savings_monthly / total_current) * 100 if total_current > 0 else 0

        # Generate recommendations
        quick_savings = self.generate_quick_savings()

        architectural_changes = [
            "Implement multi-region deployment for disaster recovery",
            "Consider serverless architecture for variable workloads",
            "Implement container orchestration for better resource utilization",
            "Use spot instances with auto-scaling for cost optimization",
            "Implement cost-aware auto-scaling policies"
        ]

        monitoring_recommendations = [
            "Set up cost anomaly detection alerts",
            "Implement cost allocation tags for all resources",
            "Configure monthly cost budget alerts",
            "Create cost dashboards for team visibility",
            "Implement automated cost optimization workflows"
        ]

        # Calculate cost score
        cost_score = self.calculate_cost_score(cost_components)

        report = CostAnalysisReport(
            timestamp=datetime.now().isoformat(),
            analysis_period_months=1,
            total_current_cost=round(total_current, 2),
            total_optimized_cost=round(total_optimized, 2),
            total_savings_monthly=round(total_savings_monthly, 2),
            total_savings_percentage=round(total_savings_percentage, 1),
            cost_components=cost_components,
            optimization_strategies=optimization_strategies,
            quick_savings=quick_savings,
            architectural_changes=architectural_changes,
            monitoring_recommendations=monitoring_recommendations,
            cost_score=cost_score
        )

        return report

    def print_cost_report(self, report: CostAnalysisReport):
        """Print comprehensive cost analysis report"""
        print("\n" + "="*100)
        print("💰 PHASE 6 COST OPTIMIZATION REPORT")
        print("="*100)

        print(f"📊 COST OPTIMIZATION SCORE: {report.cost_score}/100")
        print(f"💵 CURRENT MONTHLY COST: ${report.total_current_cost:,.2f}")
        print(f"💰 OPTIMIZED MONTHLY COST: ${report.total_optimized_cost:,.2f}")
        print(f"💸 MONTHLY SAVINGS: ${report.total_savings_monthly:,.2f}")
        print(".1f"
        print(f"📈 POTENTIAL ANNUAL SAVINGS: ${report.total_savings_monthly * 12:,.2f}")

        # Cost score interpretation
        if report.cost_score >= 80:
            print("✅ EXCELLENT: Costs are well optimized")
        elif report.cost_score >= 60:
            print("⚠️  GOOD: Moderate optimization opportunities available")
        elif report.cost_score >= 40:
            print("🟡 FAIR: Significant cost optimization potential")
        else:
            print("❌ POOR: Major cost optimization required")

        print("\n" + "-"*100)
        print("💵 COST BREAKDOWN BY COMPONENT")
        print("-"*100)

        for component in sorted(report.cost_components, key=lambda x: x.savings_monthly, reverse=True):
            print(f"{component.service:<30} | ${component.current_cost_monthly:>8.2f} → ${component.optimized_cost_monthly:>8.2f} | ${component.savings_monthly:>7.2f} ({component.savings_percentage:>4.1f}%)")

        print("\n" + "-"*100)
        print("🎯 OPTIMIZATION STRATEGIES")
        print("-"*100)

        for i, strategy in enumerate(report.optimization_strategies, 1):
            print(f"\n{i}. {strategy.strategy_name.upper().replace('_', ' ')}")
            print(f"   Potential Savings: ${strategy.total_savings_monthly:.2f}/month ({strategy.total_savings_percentage:.1f}%)")
            print(f"   Complexity: {strategy.implementation_complexity}")
            print(f"   Effort: {strategy.estimated_effort_days} days")
            print("   Key Prerequisites:"            for prereq in strategy.prerequisites[:2]:  # First 2
                print(f"     • {prereq}")

        print("\n" + "-"*100)
        print("⚡ QUICK SAVINGS OPPORTUNITIES")
        print("-"*100)

        for i, saving in enumerate(report.quick_savings[:8], 1):  # Top 8
            print(f"{i}. {saving}")

        print("\n" + "-"*100)
        print("🏗️  ARCHITECTURAL RECOMMENDATIONS")
        print("-"*100)

        for i, rec in enumerate(report.architectural_changes[:5], 1):  # Top 5
            print(f"{i}. {rec}")

        print("\n" + "="*100)

    def save_cost_report(self, report: CostAnalysisReport, filename: str = None):
        """Save cost report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase6_cost_report_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)

        logger.info(f"📄 Cost report saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 6 Cost Optimization Tool')
    parser.add_argument('--output', type=str, help='Output filename for cost report')
    parser.add_argument('--analysis-months', type=int, default=1, help='Analysis period in months')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    optimizer = Phase6CostOptimizer()

    try:
        logger.info("🚀 Starting Phase 6 Cost Optimization Analysis...")
        report = optimizer.generate_cost_report()

        if not report.cost_components:
            logger.warning("⚠️  No cost components found for analysis")
            print("⚠️  No cost components found for analysis")
            sys.exit(2)

        optimizer.print_cost_report(report)
        optimizer.save_cost_report(report, args.output)

        # Provide actionable summary
        logger.info("✅ Cost optimization analysis complete")
        print(f"\n💡 Summary: ${report.total_savings_monthly:.2f}/month savings potential ({report.total_savings_percentage:.1f}%)")

        # Exit with success
        sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Cost optimization analysis interrupted by user")
        print("\n👋 Analysis interrupted")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Cost optimization analysis failed: {e}")
        print(f"\n❌ Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()