#!/usr/bin/env python3
"""
Phase 6 Documentation Generator
Automated generation of operational runbooks and troubleshooting guides
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import argparse
import sys
from pathlib import Path
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ServiceDocumentation:
    """Service documentation structure"""
    service_name: str
    description: str
    ports: List[int]
    dependencies: List[str]
    health_checks: List[str]
    troubleshooting_steps: List[str]
    logs_location: str
    configuration_files: List[str]

@dataclass
class OperationalRunbook:
    """Operational runbook structure"""
    title: str
    description: str
    prerequisites: List[str]
    steps: List[str]
    verification: List[str]
    rollback_procedure: List[str]
    estimated_duration: str
    risk_level: str

class Phase6DocumentationGenerator:
    """Automated documentation generator for Phase 6 infrastructure"""

    def __init__(self):
        self.generated_docs = []

    def analyze_docker_compose(self) -> Dict[str, Any]:
        """Analyze docker-compose.yml for service information"""
        compose_file = Path('docker-compose.yml')
        services = {}

        if not compose_file.exists():
            logger.warning("docker-compose.yml not found")
            return services

        try:
            with open(compose_file, 'r') as f:
                # Simple parsing - in production, use yaml library
                content = f.read()

            # Extract service names and basic info
            service_blocks = re.findall(r'^(\w+):\s*$', content, re.MULTILINE)
            for service in service_blocks:
                services[service] = {
                    "name": service,
                    "ports": self._extract_ports(content, service),
                    "dependencies": self._extract_dependencies(content, service),
                    "healthcheck": "healthcheck" in content
                }

        except Exception as e:
            logger.error(f"Error analyzing docker-compose.yml: {e}")

        return services

    def _extract_ports(self, content: str, service: str) -> List[int]:
        """Extract ports for a service"""
        ports = []
        # Look for ports section for this service
        service_pattern = rf'{service}:\s*\n((?:\s+.*\n?)*?)(?=\n\w|\n\s*$)'
        service_match = re.search(service_pattern, content, re.MULTILINE)

        if service_match:
            service_content = service_match.group(1)
            port_matches = re.findall(r'ports:\s*\n((?:\s+- .*\n?)*)', service_content, re.MULTILINE)
            if port_matches:
                for port_line in port_matches[0].split('\n'):
                    port_match = re.search(r'"(\d+)"|(\d+):', port_line.strip())
                    if port_match:
                        port = port_match.group(1) or port_match.group(2)
                        ports.append(int(port))

        return ports

    def _extract_dependencies(self, content: str, service: str) -> List[str]:
        """Extract service dependencies"""
        dependencies = []
        service_pattern = rf'{service}:\s*\n((?:\s+.*\n?)*?)(?=\n\w|\n\s*$)'
        service_match = re.search(service_pattern, content, re.MULTILINE)

        if service_match:
            service_content = service_match.group(1)
            dep_matches = re.findall(r'depends_on:\s*\n((?:\s+- .*\n?)*)', service_content, re.MULTILINE)
            if dep_matches:
                for dep_line in dep_matches[0].split('\n'):
                    dep_match = re.search(r'- (\w+)', dep_line.strip())
                    if dep_match:
                        dependencies.append(dep_match.group(1))

        return dependencies

    def generate_service_documentation(self) -> List[ServiceDocumentation]:
        """Generate service documentation"""
        services = self.analyze_docker_compose()
        documentation = []

        service_templates = {
            "nginx": ServiceDocumentation(
                service_name="nginx",
                description="Reverse proxy and load balancer for the application stack",
                ports=[80, 443],
                dependencies=["fastapi_app", "kong"],
                health_checks=["curl -f http://localhost/health", "nginx -t"],
                troubleshooting_steps=[
                    "Check nginx error logs: docker logs nginx",
                    "Verify configuration: docker exec nginx nginx -t",
                    "Check upstream service health",
                    "Review SSL certificate validity"
                ],
                logs_location="/var/log/nginx/",
                configuration_files=["nginx/nginx.conf", "nginx/cdn.conf"]
            ),
            "fastapi_app": ServiceDocumentation(
                service_name="fastapi_app",
                description="Main API service built with FastAPI framework",
                ports=[8001],
                dependencies=["postgres", "redis"],
                health_checks=["curl -f http://localhost:8001/health", "curl -f http://localhost:8001/docs"],
                troubleshooting_steps=[
                    "Check application logs: docker logs fastapi_app",
                    "Verify database connectivity",
                    "Check Redis connection",
                    "Review API endpoints: /docs"
                ],
                logs_location="/app/logs/",
                configuration_files=["src/config/*.py", "docker-compose.yml"]
            ),
            "kong": ServiceDocumentation(
                service_name="kong",
                description="API Gateway for request routing and authentication",
                ports=[8000, 8443],
                dependencies=["fastapi_app"],
                health_checks=["curl -f http://localhost:8001/status"],
                troubleshooting_steps=[
                    "Check Kong admin API: curl http://localhost:8001",
                    "Verify service registration",
                    "Check plugin configurations",
                    "Review routing rules"
                ],
                logs_location="/usr/local/kong/logs/",
                configuration_files=["kong/kong.conf"]
            ),
            "postgres": ServiceDocumentation(
                service_name="postgres",
                description="Primary database for application data storage",
                ports=[5432],
                dependencies=[],
                health_checks=["pg_isready -h localhost -U postgres"],
                troubleshooting_steps=[
                    "Check database logs: docker logs postgres",
                    "Verify connection string",
                    "Check disk space",
                    "Review connection pool settings"
                ],
                logs_location="/var/log/postgresql/",
                configuration_files=["config/database-optimization.conf"]
            ),
            "redis": ServiceDocumentation(
                service_name="redis",
                description="In-memory data store for caching and sessions",
                ports=[6379],
                dependencies=[],
                health_checks=["redis-cli ping"],
                troubleshooting_steps=[
                    "Check Redis logs: docker logs redis",
                    "Verify memory usage: redis-cli info memory",
                    "Check connection pool",
                    "Review persistence settings"
                ],
                logs_location="/var/log/redis/",
                configuration_files=["config/database-optimization.conf"]
            )
        }

        for service_name, service_info in services.items():
            if service_name in service_templates:
                doc = service_templates[service_name]
                # Update with actual analyzed data
                doc.ports = service_info.get("ports", doc.ports)
                doc.dependencies = service_info.get("dependencies", doc.dependencies)
                documentation.append(doc)

        return documentation

    def generate_operational_runbooks(self) -> List[OperationalRunbook]:
        """Generate operational runbooks"""
        runbooks = []

        # Service restart runbook
        runbooks.append(OperationalRunbook(
            title="Service Restart Procedure",
            description="Standard procedure for restarting application services",
            prerequisites=[
                "Administrative access to Docker environment",
                "Backup of current configuration",
                "Notification to stakeholders if production"
            ],
            steps=[
                "docker-compose ps  # Check current service status",
                "docker-compose logs [service_name] --tail 50  # Review recent logs",
                "docker-compose restart [service_name]  # Restart the service",
                "docker-compose ps  # Verify service is running",
                "docker-compose logs [service_name] --tail 20  # Check startup logs",
                "curl [health_endpoint]  # Verify service health"
            ],
            verification=[
                "Service shows as 'Up' in docker-compose ps",
                "Health check endpoint returns 200 OK",
                "Application logs show successful startup",
                "No error messages in logs"
            ],
            rollback_procedure=[
                "docker-compose logs [service_name] --tail 100  # Review error logs",
                "docker-compose restart [service_name]  # Attempt restart",
                "If restart fails: docker-compose up -d [service_name]  # Force recreation",
                "Contact infrastructure team if issues persist"
            ],
            estimated_duration="5-15 minutes",
            risk_level="LOW"
        ))

        # SSL certificate renewal runbook
        runbooks.append(OperationalRunbook(
            title="SSL Certificate Renewal",
            description="Procedure for renewing and deploying SSL certificates",
            prerequisites=[
                "Access to certificate authority account",
                "Administrative access to server",
                "Backup of current certificates"
            ],
            steps=[
                "Check current certificate expiration: openssl x509 -in cert.pem -text | grep 'Not After'",
                "Generate CSR if needed: openssl req -new -key key.pem -out cert.csr",
                "Obtain new certificate from CA",
                "Backup current certificates: cp cert.pem cert.pem.backup",
                "Install new certificate: cp new-cert.pem cert.pem",
                "Test certificate: openssl x509 -in cert.pem -text -noout",
                "Reload nginx: docker-compose exec nginx nginx -s reload",
                "Verify SSL: curl -I https://[domain] | grep 'HTTP/2 200'"
            ],
            verification=[
                "Certificate shows correct expiration date",
                "SSL test passes: https://www.ssllabs.com/ssltest/",
                "No SSL errors in browser",
                "nginx reloads without errors"
            ],
            rollback_procedure=[
                "cp cert.pem.backup cert.pem  # Restore backup",
                "docker-compose exec nginx nginx -s reload  # Reload nginx",
                "Verify SSL connection works with old certificate",
                "Contact certificate authority for support"
            ],
            estimated_duration="30-60 minutes",
            risk_level="MEDIUM"
        ))

        # Database backup runbook
        runbooks.append(OperationalRunbook(
            title="Database Backup and Restore",
            description="Procedure for backing up and restoring PostgreSQL database",
            prerequisites=[
                "Administrative database access",
                "Sufficient disk space for backup",
                "Backup storage location available"
            ],
            steps=[
                "Check database size: docker exec postgres psql -U postgres -c 'SELECT pg_size_pretty(pg_database_size(current_database()));'",
                "Create backup: docker exec postgres pg_dump -U postgres -Fc [database_name] > backup_$(date +%Y%m%d_%H%M%S).dump",
                "Verify backup integrity: pg_restore -l backup_file.dump | head -20",
                "Compress backup: gzip backup_file.dump",
                "Copy to backup storage location",
                "Update backup inventory/log"
            ],
            verification=[
                "Backup file exists and is not empty",
                "pg_restore -l shows expected tables and schemas",
                "Backup size is reasonable for database size",
                "Backup storage location confirms receipt"
            ],
            rollback_procedure=[
                "Delete corrupted backup file",
                "Retry backup procedure",
                "If backup consistently fails, check database health",
                "Contact database administrator"
            ],
            estimated_duration="15-45 minutes",
            risk_level="LOW"
        ))

        return runbooks

    def generate_troubleshooting_guide(self) -> Dict[str, Any]:
        """Generate comprehensive troubleshooting guide"""
        guide = {
            "title": "Phase 6 Infrastructure Troubleshooting Guide",
            "last_updated": datetime.now().isoformat(),
            "sections": []
        }

        # Common issues section
        guide["sections"].append({
            "title": "Common Issues and Solutions",
            "issues": [
                {
                    "symptom": "Service fails to start",
                    "causes": ["Port conflicts", "Missing dependencies", "Configuration errors"],
                    "diagnosis": [
                        "docker-compose ps  # Check service status",
                        "docker-compose logs [service]  # Review startup logs",
                        "docker-compose config  # Validate configuration"
                    ],
                    "solutions": [
                        "Check port availability: netstat -tlnp | grep [port]",
                        "Verify dependencies are running",
                        "Review configuration syntax"
                    ]
                },
                {
                    "symptom": "Slow API responses",
                    "causes": ["Database connection issues", "Resource constraints", "Network latency"],
                    "diagnosis": [
                        "Check database connections: docker exec postgres pg_stat_activity;",
                        "Monitor resource usage: docker stats",
                        "Review application logs for bottlenecks"
                    ],
                    "solutions": [
                        "Optimize database queries",
                        "Scale resources or add caching",
                        "Review network configuration"
                    ]
                },
                {
                    "symptom": "SSL certificate errors",
                    "causes": ["Expired certificates", "Wrong certificate format", "Path issues"],
                    "diagnosis": [
                        "Check certificate validity: openssl x509 -in cert.pem -text",
                        "Verify certificate chain: openssl verify cert.pem",
                        "Check nginx SSL configuration"
                    ],
                    "solutions": [
                        "Renew expired certificates",
                        "Convert certificate format if needed",
                        "Update nginx configuration paths"
                    ]
                }
            ]
        })

        # Monitoring section
        guide["sections"].append({
            "title": "Monitoring and Alerting",
            "monitoring_points": [
                "Service health: docker-compose ps",
                "Application logs: docker-compose logs [service]",
                "Resource usage: docker stats",
                "Database health: pg_isready -h localhost",
                "SSL status: openssl s_client -connect localhost:443"
            ],
            "alert_triggers": [
                "Service down for >5 minutes",
                "CPU usage >90% for >10 minutes",
                "Memory usage >95%",
                "Disk space <10% available",
                "SSL certificate expires in <30 days"
            ]
        })

        return guide

    def generate_emergency_procedures(self) -> Dict[str, Any]:
        """Generate emergency procedures documentation"""
        procedures = {
            "title": "Phase 6 Emergency Procedures",
            "last_updated": datetime.now().isoformat(),
            "procedures": []
        }

        # Complete system failure
        procedures["procedures"].append({
            "scenario": "Complete System Failure",
            "priority": "CRITICAL",
            "response_time": "Immediate",
            "steps": [
                "Assess damage and isolate affected components",
                "Execute emergency backup restoration",
                "Bring up critical services first (database, then APIs)",
                "Verify data integrity",
                "Gradually restore full functionality",
                "Notify stakeholders and document incident"
            ],
            "contacts": [
                "Infrastructure Team Lead",
                "Database Administrator",
                "Security Officer"
            ]
        })

        # Security breach
        procedures["procedures"].append({
            "scenario": "Security Breach Detected",
            "priority": "CRITICAL",
            "response_time": "Immediate",
            "steps": [
                "Isolate affected systems",
                "Preserve evidence (logs, network traffic)",
                "Notify security team and legal",
                "Assess breach scope and impact",
                "Execute incident response plan",
                "Restore from clean backups",
                "Conduct post-mortem analysis"
            ],
            "contacts": [
                "Security Incident Response Team",
                "Legal Counsel",
                "Executive Leadership"
            ]
        })

        # Data loss
        procedures["procedures"].append({
            "scenario": "Data Loss Incident",
            "priority": "HIGH",
            "response_time": "Within 1 hour",
            "steps": [
                "Stop all write operations to prevent further damage",
                "Assess data loss scope and criticality",
                "Execute backup restoration procedures",
                "Verify data integrity after restoration",
                "Resume operations gradually",
                "Document lessons learned"
            ],
            "contacts": [
                "Database Administrator",
                "Data Protection Officer",
                "Business Continuity Team"
            ]
        })

        return procedures

    def run_documentation_generation(self) -> Dict[str, Any]:
        """Run complete documentation generation"""
        logger.info("📚 Starting Phase 6 documentation generation...")

        # Generate all documentation types
        service_docs = self.generate_service_documentation()
        runbooks = self.generate_operational_runbooks()
        troubleshooting = self.generate_troubleshooting_guide()
        emergency_procedures = self.generate_emergency_procedures()

        documentation = {
            "generated_timestamp": datetime.now().isoformat(),
            "service_documentation": [asdict(doc) for doc in service_docs],
            "operational_runbooks": [asdict(rb) for rb in runbooks],
            "troubleshooting_guide": troubleshooting,
            "emergency_procedures": emergency_procedures,
            "summary": {
                "services_documented": len(service_docs),
                "runbooks_generated": len(runbooks),
                "troubleshooting_sections": len(troubleshooting["sections"]),
                "emergency_procedures": len(emergency_procedures["procedures"])
            }
        }

        logger.info(f"✅ Documentation generation complete - {len(service_docs)} services, {len(runbooks)} runbooks")
        return documentation

    def print_documentation_summary(self, docs: Dict[str, Any]):
        """Print documentation generation summary"""
        print("\n" + "="*80)
        print("📚 PHASE 6 DOCUMENTATION GENERATION SUMMARY")
        print("="*80)

        summary = docs["summary"]
        print(f"🔧 SERVICES DOCUMENTED: {summary['services_documented']}")
        print(f"📋 OPERATIONAL RUNBOOKS: {summary['runbooks_generated']}")
        print(f"🔍 TROUBLESHOOTING SECTIONS: {summary['troubleshooting_sections']}")
        print(f"🚨 EMERGENCY PROCEDURES: {summary['emergency_procedures']}")

        print("\n" + "-"*80)
        print("📋 GENERATED CONTENT")
        print("-"*80)

        print("\n🔧 SERVICE DOCUMENTATION:")
        for service in docs["service_documentation"]:
            print(f"  • {service['service_name']}: {service['description'][:60]}...")

        print("\n📋 OPERATIONAL RUNBOOKS:")
        for runbook in docs["operational_runbooks"]:
            print(f"  • {runbook['title']} ({runbook['estimated_duration']})")

        print("\n🔍 TROUBLESHOOTING GUIDE:")
        for section in docs["troubleshooting_guide"]["sections"]:
            print(f"  • {section['title']}")

        print("\n🚨 EMERGENCY PROCEDURES:")
        for procedure in docs["emergency_procedures"]["procedures"]:
            print(f"  • {procedure['scenario']} ({procedure['priority']})")

        print("\n" + "="*80)

    def save_documentation(self, docs: Dict[str, Any], filename: str = None):
        """Save generated documentation to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase6_documentation_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(docs, f, indent=2, default=str)

        logger.info(f"💾 Documentation saved to: {filename}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 6 Documentation Generator')
    parser.add_argument('--output', type=str, help='Output filename for documentation')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--type', choices=['all', 'services', 'runbooks', 'troubleshooting'],
                       default='all', help='Type of documentation to generate')

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    generator = Phase6DocumentationGenerator()

    try:
        logger.info("📚 Starting Phase 6 documentation generation...")
        docs = generator.run_documentation_generation()
        generator.print_documentation_summary(docs)
        generator.save_documentation(docs, args.output)

        # Provide actionable summary
        summary = docs["summary"]
        total_items = sum(summary.values())
        logger.info(f"✅ Documentation generation complete - {total_items} total documentation items created")
        print(f"\n📚 Summary: Generated {total_items} documentation items across {len(summary)} categories")

        sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Documentation generation interrupted by user")
        print("\n👋 Documentation generation interrupted")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Documentation generation failed: {e}")
        print(f"\n❌ Documentation generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()