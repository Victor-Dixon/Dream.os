#!/usr/bin/env python3
"""
Phase 5 Infrastructure Documentation Generator
Automated generation of operational documentation and runbooks
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import argparse
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ServiceDocumentation:
    name: str
    description: str
    ports: List[int]
    dependencies: List[str]
    health_checks: List[str]
    configuration_files: List[str]
    troubleshooting: Dict[str, str]

@dataclass
class InfrastructureRunbook:
    service_name: str
    startup_procedure: List[str]
    shutdown_procedure: List[str]
    scaling_procedure: List[str]
    backup_procedure: List[str]
    recovery_procedure: List[str]
    monitoring_endpoints: List[str]
    common_issues: Dict[str, Dict]

class Phase5DocumentationGenerator:
    def __init__(self):
        self.docs_dir = Path("docs/phase5")
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.services_config = self._load_services_config()

    def _load_services_config(self) -> Dict:
        """Load services configuration from docker-compose.yml"""
        try:
            with open("docker-compose.yml", 'r') as f:
                compose_config = yaml.safe_load(f)
            return compose_config.get('services', {})
        except Exception as e:
            logger.warning(f"Could not load docker-compose.yml: {e}")
            return {}

    def generate_service_documentation(self) -> List[ServiceDocumentation]:
        """Generate comprehensive service documentation"""
        services = []

        service_configs = {
            "flask_app": {
                "description": "Flask web application providing REST API endpoints",
                "ports": [5000],
                "dependencies": ["postgres", "redis"],
                "health_checks": ["/health"],
                "configuration_files": ["src/app.py", "requirements.txt"],
                "troubleshooting": {
                    "connection_refused": "Check if service is running: docker-compose ps flask_app",
                    "port_already_in_use": "Check for conflicting services: netstat -tlnp | grep :5000",
                    "database_connection_error": "Verify PostgreSQL is running and credentials are correct"
                }
            },
            "fastapi_app": {
                "description": "FastAPI application providing high-performance REST API with async support",
                "ports": [8001],
                "dependencies": ["postgres", "redis"],
                "health_checks": ["/health", "/docs"],
                "configuration_files": ["src/main.py", "requirements.txt"],
                "troubleshooting": {
                    "uvicorn_not_starting": "Check Python dependencies: pip list | grep fastapi",
                    "port_conflict": "Check port availability: lsof -i :8001",
                    "async_task_failures": "Check Redis connection for background task processing"
                }
            },
            "kong": {
                "description": "Kong API Gateway providing rate limiting, authentication, and routing",
                "ports": [8000, 8443],
                "dependencies": ["postgres"],
                "health_checks": ["/status"],
                "configuration_files": ["kong.yml"],
                "troubleshooting": {
                    "gateway_unreachable": "Check Kong admin API: curl http://localhost:8001/status",
                    "plugin_loading_failed": "Check Kong logs: docker-compose logs kong",
                    "database_migration_error": "Verify PostgreSQL connectivity and run migrations"
                }
            },
            "nginx": {
                "description": "Nginx reverse proxy with SSL termination, load balancing, and CDN capabilities",
                "ports": [8080, 8443],
                "dependencies": ["flask_app", "fastapi_app", "kong"],
                "health_checks": ["/health"],
                "configuration_files": ["nginx/nginx.conf", "nginx/cdn.conf"],
                "troubleshooting": {
                    "502_bad_gateway": "Check upstream services: docker-compose ps",
                    "ssl_handshake_failed": "Verify SSL certificates: openssl x509 -in ssl/cert.pem -text",
                    "cdn_cache_issues": "Check cache directory permissions and size"
                }
            },
            "postgres": {
                "description": "PostgreSQL database with connection pooling and performance optimization",
                "ports": [5432],
                "dependencies": [],
                "health_checks": ["SELECT 1"],
                "configuration_files": ["config/database-optimization.conf"],
                "troubleshooting": {
                    "connection_timeout": "Check max_connections setting in postgresql.conf",
                    "disk_space_full": "Monitor disk usage: df -h /var/lib/postgresql",
                    "slow_queries": "Enable query logging and analyze with pg_stat_statements"
                }
            },
            "redis": {
                "description": "Redis cache and session store with persistence and clustering support",
                "ports": [6379],
                "dependencies": [],
                "health_checks": ["PING"],
                "configuration_files": ["config/database-optimization.conf"],
                "troubleshooting": {
                    "memory_full": "Check maxmemory setting and eviction policy",
                    "connection_refused": "Verify Redis is listening on correct port",
                    "persistence_failed": "Check disk space and file permissions for RDB/AOF files"
                }
            },
            "prometheus": {
                "description": "Prometheus monitoring system collecting metrics from all services",
                "ports": [9090],
                "dependencies": [],
                "health_checks": ["/-/healthy"],
                "configuration_files": ["config/prometheus.yml"],
                "troubleshooting": {
                    "metrics_not_collected": "Check service annotations and target endpoints",
                    "storage_full": "Monitor disk usage and adjust retention settings",
                    "query_timeout": "Optimize query range and reduce time series"
                }
            },
            "grafana": {
                "description": "Grafana dashboard platform with alerting and visualization",
                "ports": [3000],
                "dependencies": ["prometheus"],
                "health_checks": ["/api/health"],
                "configuration_files": ["config/grafana/provisioning/datasources/prometheus.yml"],
                "troubleshooting": {
                    "dashboard_not_loading": "Check datasource configuration and connectivity",
                    "alerts_not_working": "Verify SMTP settings and alert rules",
                    "performance_slow": "Check query optimization and dashboard refresh rates"
                }
            },
            "istio-proxy": {
                "description": "Istio service mesh proxy providing traffic management and observability",
                "ports": [15090, 15000, 15001],
                "dependencies": ["nginx"],
                "health_checks": ["/healthz/ready"],
                "configuration_files": ["config/istio/config/*"],
                "troubleshooting": {
                    "pilot_connection_failed": "Check Istio control plane connectivity",
                    "certificate_issues": "Verify Istio certificate provisioning",
                    "traffic_not_routing": "Check VirtualService and DestinationRule configurations"
                }
            }
        }

        for service_name, config in service_configs.items():
            # Get additional info from docker-compose if available
            compose_info = self.services_config.get(service_name, {})

            # Extract ports from compose config
            ports = config["ports"]
            if "ports" in compose_info:
                # Parse docker-compose port mappings
                for port_mapping in compose_info["ports"]:
                    if ":" in port_mapping:
                        host_port = port_mapping.split(":")[0]
                        try:
                            ports.append(int(host_port))
                        except ValueError:
                            pass

            service_doc = ServiceDocumentation(
                name=service_name,
                description=config["description"],
                ports=list(set(ports)),  # Remove duplicates
                dependencies=config["dependencies"],
                health_checks=config["health_checks"],
                configuration_files=config["configuration_files"],
                troubleshooting=config["troubleshooting"]
            )
            services.append(service_doc)

        return services

    def generate_infrastructure_runbook(self, service: ServiceDocumentation) -> InfrastructureRunbook:
        """Generate operational runbook for a service"""

        # Startup procedure
        startup_procedure = [
            f"Verify dependencies are running: {' '.join(service.dependencies)}" if service.dependencies else "No dependencies required",
            f"Start service: docker-compose up -d {service.name}",
            f"Wait for health checks to pass: {' '.join(service.health_checks)}",
            f"Verify service is responding on ports: {', '.join(map(str, service.ports))}",
            f"Check logs for startup errors: docker-compose logs {service.name}"
        ]

        # Shutdown procedure
        shutdown_procedure = [
            f"Graceful shutdown: docker-compose stop {service.name}",
            "Wait for connections to drain (30 seconds)",
            f"Force stop if needed: docker-compose kill {service.name}",
            "Verify service has stopped: docker-compose ps"
        ]

        # Scaling procedure
        if service.name in ["flask_app", "fastapi_app"]:
            scaling_procedure = [
                f"Scale service: docker-compose up -d --scale {service.name}=N",
                f"Verify load balancer distributes traffic across N instances",
                f"Monitor resource usage and adjust scaling as needed",
                f"Scale down: docker-compose up -d --scale {service.name}=1"
            ]
        else:
            scaling_procedure = [
                f"Service {service.name} does not support horizontal scaling",
                "Consider vertical scaling (increase CPU/memory limits)",
                "Review service architecture for scaling requirements"
            ]

        # Backup procedure
        if "postgres" in service.name:
            backup_procedure = [
                "Create database backup: docker exec postgres pg_dump -U postgres tradingrobotplug > backup.sql",
                "Compress backup: gzip backup.sql",
                "Store in secure location with encryption",
                "Test backup restoration regularly"
            ]
        elif "redis" in service.name:
            backup_procedure = [
                "Redis persistence is automatic (RDB/AOF)",
                "Copy dump.rdb file: docker cp redis:/data/dump.rdb ./backup/",
                "Archive AOF file if appendonly is enabled",
                "Store backups with encryption"
            ]
        else:
            backup_procedure = [
                "Service uses external data persistence",
                "Backup configuration files and logs",
                "Document service state and dependencies",
                "Test service recreation from backup"
            ]

        # Recovery procedure
        recovery_procedure = [
            "Identify root cause of failure",
            f"Check service logs: docker-compose logs {service.name}",
            "Restart service: docker-compose restart {service.name}",
            "If restart fails, recreate: docker-compose up --force-recreate {service.name}",
            "Verify service recovery and monitor for issues"
        ]

        # Monitoring endpoints
        monitoring_endpoints = []
        for port in service.ports:
            if port == 9090:  # Prometheus
                monitoring_endpoints.extend(["/-/healthy", "/-/ready", "/metrics"])
            elif port == 3000:  # Grafana
                monitoring_endpoints.extend(["/api/health", "/metrics"])
            elif port in [8001, 5000]:  # APIs
                monitoring_endpoints.extend(service.health_checks)

        # Common issues and solutions
        common_issues = service.troubleshooting.copy()

        # Add general issues
        common_issues.update({
            "out_of_memory": {
                "symptoms": "Service crashes with OOM errors",
                "solution": "Increase memory limits in docker-compose.yml",
                "prevention": "Monitor memory usage with Prometheus metrics"
            },
            "high_cpu_usage": {
                "symptoms": "Service consuming excessive CPU",
                "solution": "Profile application performance, optimize code",
                "prevention": "Set CPU limits and monitor usage trends"
            },
            "network_connectivity": {
                "symptoms": "Service cannot reach dependencies",
                "solution": "Check service discovery and network configuration",
                "prevention": "Monitor network latency and packet loss"
            }
        })

        return InfrastructureRunbook(
            service_name=service.name,
            startup_procedure=startup_procedure,
            shutdown_procedure=shutdown_procedure,
            scaling_procedure=scaling_procedure,
            backup_procedure=backup_procedure,
            recovery_procedure=recovery_procedure,
            monitoring_endpoints=monitoring_endpoints,
            common_issues=common_issues
        )

    def generate_troubleshooting_guide(self) -> str:
        """Generate comprehensive troubleshooting guide"""
        guide = f"""# Phase 5 Infrastructure Troubleshooting Guide

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Quick Health Check Commands

```bash
# Overall system health
python tools/phase5_health_check.py

# Load testing
python tools/phase5_load_test_orchestrator.py --scenario baseline_validation

# Real-time monitoring
python tools/phase5_monitoring_dashboard.py

# Deployment validation
python tools/phase5_deployment_validator.py
```

## Service Status Commands

```bash
# Check all services
docker-compose ps

# View service logs
docker-compose logs [service_name]

# Restart service
docker-compose restart [service_name]

# View resource usage
docker stats
```

## Common Issues and Solutions

### SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Regenerate certificates
python tools/phase5_infrastructure_automation.py ssl-update

# Reload nginx
docker-compose exec nginx nginx -s reload
```

### Database Connection Issues
```bash
# Check PostgreSQL
docker-compose exec postgres psql -U postgres -d tradingrobotplug -c "SELECT version();"

# Check Redis
docker-compose exec redis redis-cli ping

# Reset database connections
python tools/phase5_infrastructure_automation.py db-optimize
```

### Performance Issues
```bash
# Run performance benchmark
python tools/phase5_performance_benchmark.py --duration 30

# Check system resources
top -p $(pgrep -d',' -f "python|node|nginx")

# Monitor network
iftop -i eth0
```

### Service Mesh Issues
```bash
# Check Istio proxy status
docker-compose exec istio-proxy curl http://localhost:15000/healthz/ready

# View Envoy configuration
docker-compose exec istio-proxy curl http://localhost:15000/config_dump
```

## Emergency Procedures

### Complete System Restart
```bash
# Graceful shutdown
docker-compose down

# Start all services
docker-compose up -d

# Verify health
python tools/phase5_health_check.py
```

### Database Recovery
```bash
# Stop database
docker-compose stop postgres

# Start in recovery mode
docker-compose up -d postgres

# Check logs
docker-compose logs postgres
```

### Monitoring Stack Issues
```bash
# Reset Grafana admin password
docker-compose exec grafana grafana-cli admin reset-admin-password admin123

# Clear Prometheus data
docker-compose stop prometheus
sudo rm -rf prometheus_data/*
docker-compose up -d prometheus
```

## Monitoring and Alerting

### Key Metrics to Monitor
- Service response times (< 2s for APIs)
- Error rates (< 1% for healthy services)
- Resource usage (CPU < 80%, Memory < 85%)
- Database connections (< 100 active)
- Cache hit ratios (> 95% for Redis)

### Alert Thresholds
- Service down: Immediate alert
- High error rate: > 5% for 5 minutes
- Resource exhaustion: > 90% for 10 minutes
- Database slow queries: > 1000ms average

## Contact and Support

For urgent issues:
1. Check this troubleshooting guide
2. Run automated diagnostics
3. Review service logs
4. Contact infrastructure team with diagnostic output

## Log Locations

- Application logs: `docker-compose logs [service]`
- Nginx access logs: `docker-compose exec nginx tail -f /var/log/nginx/access.log`
- System logs: `/var/log/syslog`
- Audit logs: `logs/audit.log`

---
*This guide is automatically generated and updated with infrastructure changes.*
"""
        return guide

    def generate_monitoring_guide(self) -> str:
        """Generate monitoring and alerting guide"""
        guide = f"""# Phase 5 Infrastructure Monitoring Guide

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Monitoring Stack Overview

The Phase 5 infrastructure uses a comprehensive monitoring stack:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and alerting dashboards
- **Custom Tools**: Specialized monitoring and health checks

## Access Points

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin123)
- Real-time Dashboard: `python tools/phase5_monitoring_dashboard.py`
- Health Checks: `python tools/phase5_health_check.py`

## Key Metrics

### System Metrics
- CPU Usage: Target < 75%
- Memory Usage: Target < 80%
- Disk Usage: Target < 85%
- Network I/O: Monitor for bottlenecks

### Service Metrics
- Response Time: Target < 2000ms for APIs
- Error Rate: Target < 1%
- Uptime: Target > 99.9%
- Throughput: Monitor RPS trends

### Database Metrics
- Active Connections: Target < 100
- Cache Hit Ratio: Target > 95%
- Slow Queries: Target < 1%
- Lock Waits: Target = 0

### CDN Metrics
- Cache Hit Ratio: Target > 90%
- Response Time: Target < 500ms
- Error Rate: Target < 1%
- Bandwidth Usage: Monitor trends

## Alert Rules

### Critical Alerts (Immediate Response)
- Service Down
- Database Connection Lost
- SSL Certificate Expiring (< 30 days)
- Disk Space Critical (> 95%)
- Memory Exhaustion (> 90%)

### Warning Alerts (Review Within 1 Hour)
- High CPU Usage (> 80%)
- High Memory Usage (> 85%)
- Increased Error Rates (> 5%)
- Slow Response Times (> 3000ms)

### Info Alerts (Monitor Trends)
- Certificate Expiring (< 90 days)
- Resource Usage Trends
- Performance Degradation

## Dashboard Panels

### Infrastructure Overview
- System resource usage (CPU, Memory, Disk, Network)
- Service health status
- Database performance metrics
- CDN performance indicators

### Service Details
- Individual service metrics
- Error rates and response times
- Resource consumption
- Dependency health

### Performance Trends
- Historical performance data
- Capacity planning metrics
- Seasonal usage patterns
- Growth projections

## Monitoring Commands

```bash
# Real-time dashboard
python tools/phase5_monitoring_dashboard.py

# Health snapshot
python tools/phase5_monitoring_dashboard.py --snapshot

# Load testing
python tools/phase5_load_test_orchestrator.py --scenario baseline_validation

# Performance benchmark
python tools/phase5_performance_benchmark.py --duration 60
```

## Custom Metrics

### Application Metrics
- Request count by endpoint
- Response time percentiles
- Error count by type
- User session metrics

### Business Metrics
- API usage by client
- Feature adoption rates
- Performance by user segment
- Revenue-impacting metrics

## Alert Configuration

### Email Alerts
```yaml
# SMTP configuration in docker-compose.yml
environment:
  GF_SMTP_ENABLED: true
  GF_SMTP_HOST: smtp.example.com
  GF_SMTP_USER: alerts@example.com
```

### Webhook Alerts
- Slack integration
- PagerDuty escalation
- Custom webhook endpoints

## Maintenance Windows

### Scheduled Maintenance
- Weekly: Log rotation and cleanup
- Monthly: Certificate renewal checks
- Quarterly: Performance audits
- Annually: Security assessments

### Emergency Maintenance
- Critical security patches: Immediate
- Performance degradation: Within 4 hours
- Service outages: Immediate response

## Reporting

### Daily Reports
- System health summary
- Performance metrics
- Error rate trends
- Capacity utilization

### Weekly Reports
- Trend analysis
- Capacity planning
- Incident summary
- Improvement recommendations

### Monthly Reports
- SLA compliance
- Cost optimization
- Security posture
- Future planning

## Integration Points

### External Systems
- Cloud monitoring (AWS CloudWatch, GCP Monitoring)
- APM tools (New Relic, Datadog)
- Log aggregation (ELK Stack, Splunk)

### Internal Systems
- CI/CD pipelines
- Configuration management
- Incident response
- Change management

---
*This monitoring guide is automatically maintained with infrastructure updates.*
"""
        return guide

    def generate_maintenance_runbook(self) -> str:
        """Generate maintenance and operations runbook"""
        runbook = f"""# Phase 5 Infrastructure Maintenance Runbook

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Daily Operations

### Morning Health Check
```bash
# Run comprehensive health check
python tools/phase5_health_check.py

# Check system resources
docker stats --no-stream

# Review overnight logs
docker-compose logs --since 6h | grep -i error
```

### Log Management
```bash
# Rotate application logs
docker-compose exec nginx nginx -s reopen

# Archive old logs
find logs/ -name "*.log" -mtime +7 -exec gzip {{}} \;

# Clean temporary files
docker system prune -f
```

### Backup Verification
```bash
# Check backup integrity
ls -la backups/
find backups/ -name "*.sql.gz" -mtime -1  # Recent DB backups

# Test backup restoration (monthly)
# [See individual service runbooks for restoration procedures]
```

## Weekly Maintenance

### Security Updates
```bash
# Update Docker images
docker-compose pull

# Check for security vulnerabilities
docker scan [image_name]

# Update SSL certificates if needed
python tools/phase5_infrastructure_automation.py ssl-update
```

### Database Maintenance
```bash
# Run database optimization
python tools/phase5_infrastructure_automation.py db-optimize

# Vacuum and analyze
docker-compose exec postgres psql -U postgres -d tradingrobotplug -c "VACUUM ANALYZE;"

# Check for unused indexes
docker-compose exec postgres psql -U postgres -d tradingrobotplug -c "SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;"
```

### Performance Tuning
```bash
# Run performance benchmark
python tools/phase5_performance_benchmark.py --duration 300

# Analyze results and adjust configurations
# Update docker-compose.yml resource limits if needed
```

## Monthly Maintenance

### Comprehensive Testing
```bash
# Full load test suite
python tools/phase5_load_test_orchestrator.py

# Deployment validation
python tools/phase5_deployment_validator.py

# Security assessment
# [Run external security scanning tools]
```

### Capacity Planning
```bash
# Analyze resource usage trends
# Review Prometheus metrics for the past month
# Plan for scaling requirements
```

### Documentation Updates
```bash
# Regenerate documentation
python tools/phase5_documentation_generator.py

# Update runbooks with new procedures
# Review and update emergency contacts
```

## Quarterly Maintenance

### Major Updates
```bash
# Update to latest stable versions
# Test compatibility with new versions
# Plan and execute rolling updates
```

### Disaster Recovery Testing
```bash
# Test backup restoration procedures
# Simulate service failures
# Validate failover mechanisms
```

### Compliance Audits
```bash
# Security compliance review
# Performance benchmark against SLAs
# Cost optimization analysis
```

## Emergency Procedures

### Service Outage Response
1. **Immediate Assessment**
   ```bash
   # Check service status
   docker-compose ps

   # Review recent logs
   docker-compose logs --tail 100 [failed_service]

   # Run health check
   python tools/phase5_health_check.py
   ```

2. **Initial Recovery**
   ```bash
   # Attempt service restart
   docker-compose restart [failed_service]

   # If restart fails, check dependencies
   docker-compose ps [dependencies]

   # Check resource constraints
   docker stats [failed_service]
   ```

3. **Escalation**
   - Notify team leads
   - Document incident details
   - Begin root cause analysis

### Data Loss Recovery
1. **Assess Impact**
   ```bash
   # Check available backups
   ls -la backups/

   # Determine data loss scope
   # Review backup timestamps
   ```

2. **Recovery Execution**
   ```bash
   # Stop affected services
   docker-compose stop [affected_services]

   # Restore from backup
   # [See specific service runbook for restoration commands]

   # Verify data integrity
   # Run validation tests
   ```

3. **Post-Recovery**
   - Validate system functionality
   - Update monitoring baselines
   - Document lessons learned

### Security Incident Response
1. **Containment**
   ```bash
   # Isolate affected systems
   docker-compose stop [compromised_services]

   # Block suspicious traffic
   # Update firewall rules
   ```

2. **Investigation**
   ```bash
   # Preserve evidence
   docker logs [compromised_services] > incident_logs.txt

   # Analyze attack vectors
   # Review access logs
   ```

3. **Recovery**
   ```bash
   # Clean compromised systems
   # Restore from known-good backups
   # Update security configurations
   ```

## Automation Commands

### Routine Maintenance
```bash
# Daily cleanup
python tools/phase5_infrastructure_automation.py cleanup --days 7

# Weekly optimization
python tools/phase5_infrastructure_automation.py db-optimize

# Monthly backup
python tools/phase5_infrastructure_automation.py backup --database all
```

### Emergency Automation
```bash
# Quick health check
python tools/phase5_infrastructure_automation.py health-check

# Service restart
python tools/phase5_infrastructure_automation.py restart --service [service_name]

# Scale service
python tools/phase5_infrastructure_automation.py scale --service [service_name] --replicas 2
```

## Contact Information

### Emergency Contacts
- Infrastructure Lead: [Name] - [Phone] - [Email]
- Security Officer: [Name] - [Phone] - [Email]
- Business Owner: [Name] - [Phone] - [Email]

### Support Hours
- Business Hours: 9:00 AM - 6:00 PM EST
- Emergency Support: 24/7 for critical incidents
- Maintenance Windows: Saturday 10:00 PM - Sunday 6:00 AM EST

## Change Management

### Change Approval Process
1. Submit change request with impact assessment
2. Technical review by infrastructure team
3. Business approval for production changes
4. Schedule implementation during maintenance windows

### Rollback Procedures
- Document rollback steps for each change
- Test rollback procedures regularly
- Maintain known-good configurations
- Automate rollback where possible

## Performance Benchmarks

### Target Performance Metrics
- API Response Time: < 2 seconds (95th percentile)
- Error Rate: < 1% (monthly average)
- Uptime: > 99.9% (monthly)
- Recovery Time: < 15 minutes (from failure detection)

### Monitoring Thresholds
- Warning: 80% of target metrics
- Critical: 95% of target metrics
- Immediate Action: Any target exceeded

---
*This maintenance runbook is automatically updated with infrastructure changes.*
"""
        return runbook

    def generate_documentation(self) -> Dict[str, str]:
        """Generate all documentation files"""
        logger.info("🎯 Generating Phase 5 Infrastructure Documentation...")

        # Generate service documentation
        services = self.generate_service_documentation()

        # Generate runbooks for each service
        runbooks = {}
        for service in services:
            runbook = self.generate_infrastructure_runbook(service)
            runbooks[service.name] = runbook

        # Generate comprehensive documentation
        docs = {
            "services_overview.md": self._generate_services_overview(services),
            "troubleshooting_guide.md": self.generate_troubleshooting_guide(),
            "monitoring_guide.md": self.generate_monitoring_guide(),
            "maintenance_runbook.md": self.generate_maintenance_runbook(),
            "emergency_procedures.md": self._generate_emergency_procedures(services, runbooks)
        }

        # Generate individual service runbooks
        for service_name, runbook in runbooks.items():
            docs[f"runbooks/{service_name}_runbook.md"] = self._generate_service_runbook(runbook)

        # Save all documentation
        for filename, content in docs.items():
            filepath = self.docs_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w') as f:
                f.write(content)

            logger.info(f"📄 Generated: {filepath}")

        # Generate JSON metadata
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "services_count": len(services),
            "runbooks_count": len(runbooks),
            "documentation_files": list(docs.keys()),
            "services": [asdict(service) for service in services],
            "runbooks": {name: asdict(runbook) for name, runbook in runbooks.items()}
        }

        metadata_file = self.docs_dir / "documentation_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)

        logger.info(f"📊 Generated documentation for {len(services)} services with {len(runbooks)} runbooks")

        return docs

    def _generate_services_overview(self, services: List[ServiceDocumentation]) -> str:
        """Generate services overview documentation"""
        overview = f"""# Phase 5 Infrastructure Services Overview

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Architecture Overview

The Phase 5 infrastructure consists of {len(services)} core services running in a containerized environment with enterprise-grade features including SSL termination, service mesh orchestration, comprehensive monitoring, and automated scaling.

## Service Inventory

"""

        for service in services:
            overview += f"""### {service.name.replace('_', ' ').title()}

**Description:** {service.description}

**Ports:** {', '.join(map(str, service.ports))}

**Dependencies:** {', '.join(service.dependencies) if service.dependencies else 'None'}

**Health Checks:**
"""
            for check in service.health_checks:
                overview += f"- `{check}`\n"

            overview += f"""
**Configuration Files:**
"""
            for config in service.configuration_files:
                overview += f"- `{config}`\n"

            overview += "\n---\n\n"

        overview += """## Infrastructure Capabilities

### Security & Compliance
- SSL/TLS termination with modern cipher suites
- JWT authentication and RBAC authorization
- Enterprise-grade security headers
- Automated certificate management

### Performance & Scalability
- Service mesh with intelligent routing
- Load balancing and auto-scaling
- CDN capabilities with edge caching
- Database connection pooling

### Monitoring & Observability
- Comprehensive metrics collection
- Real-time alerting and dashboards
- Distributed tracing and logging
- Performance benchmarking tools

### Operations & Automation
- Automated deployment and scaling
- Infrastructure as Code principles
- Comprehensive health checking
- Automated backup and recovery

## Quick Start Commands

```bash
# Start all services
docker-compose up -d

# Check system health
python tools/phase5_health_check.py

# View real-time monitoring
python tools/phase5_monitoring_dashboard.py

# Run performance tests
python tools/phase5_load_test_orchestrator.py --scenario baseline_validation
```

## Service Dependencies Graph

```
Internet
    ↓
  [Nginx Reverse Proxy]
    ↓
  [Kong API Gateway]
    ↓
  [Flask App] [FastAPI App]
    ↓         ↓
  [PostgreSQL] [Redis]
    ↓         ↓
  [Prometheus] [Grafana]
    ↓         ↓
[Istio Service Mesh]
```

## Configuration Management

All services are configured using:
- Docker Compose for container orchestration
- Environment variables for runtime configuration
- YAML configuration files for service-specific settings
- Automated configuration validation tools

## Monitoring Integration

Each service exposes metrics for:
- Health status and availability
- Performance metrics (response times, throughput)
- Resource utilization (CPU, memory, disk)
- Error rates and exception tracking

See the monitoring guide for detailed metric definitions and alerting rules.

---
*This overview is automatically generated and updated with infrastructure changes.*
"""
        return overview

    def _generate_service_runbook(self, runbook: InfrastructureRunbook) -> str:
        """Generate individual service runbook"""
        runbook_md = f"""# {runbook.service_name.upper()} Operations Runbook

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Startup Procedure

"""
        for i, step in enumerate(runbook.startup_procedure, 1):
            runbook_md += f"{i}. {step}\n"

        runbook_md += "\n## Shutdown Procedure\n\n"
        for i, step in enumerate(runbook.shutdown_procedure, 1):
            runbook_md += f"{i}. {step}\n"

        runbook_md += "\n## Scaling Procedure\n\n"
        for i, step in enumerate(runbook.scaling_procedure, 1):
            runbook_md += f"{i}. {step}\n"

        runbook_md += "\n## Backup Procedure\n\n"
        for i, step in enumerate(runbook.backup_procedure, 1):
            runbook_md += f"{i}. {step}\n"

        runbook_md += "\n## Recovery Procedure\n\n"
        for i, step in enumerate(runbook.recovery_procedure, 1):
            runbook_md += f"{i}. {step}\n"

        runbook_md += "\n## Monitoring Endpoints\n\n"
        for endpoint in runbook.monitoring_endpoints:
            runbook_md += f"- `{endpoint}`\n"

        runbook_md += "\n## Common Issues & Solutions\n\n"
        for issue, details in runbook.common_issues.items():
            runbook_md += f"### {issue.replace('_', ' ').title()}\n\n"
            if isinstance(details, dict):
                for key, value in details.items():
                    runbook_md += f"**{key.title()}:** {value}\n\n"
            else:
                runbook_md += f"{details}\n\n"

        runbook_md += "---\n*This runbook is automatically generated and maintained.*\n"
        return runbook_md

    def _generate_emergency_procedures(self, services: List[ServiceDocumentation], runbooks: Dict[str, InfrastructureRunbook]) -> str:
        """Generate emergency procedures documentation"""
        procedures = f"""# Phase 5 Infrastructure Emergency Procedures

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Emergency Contact Information

### Primary Contacts
- **Infrastructure Lead**: [Name] - [Phone] - [Email]
- **Security Officer**: [Name] - [Phone] - [Email]
- **DevOps Engineer**: [Name] - [Phone] - [Email]

### Support Hours
- **Business Hours**: 9:00 AM - 6:00 PM EST
- **Emergency Support**: 24/7 for critical incidents
- **Maintenance Windows**: Saturday 10:00 PM - Sunday 6:00 AM EST

## Incident Severity Levels

### SEV 1 - Critical (Immediate Response Required)
- Complete system outage
- Data loss or corruption
- Security breach
- Production impacting issues

### SEV 2 - High (Response within 1 hour)
- Partial system degradation
- Significant performance issues
- Single service failures
- Database connectivity issues

### SEV 3 - Medium (Response within 4 hours)
- Minor performance degradation
- Non-critical service issues
- Monitoring alert investigations

### SEV 4 - Low (Next business day)
- Cosmetic issues
- Documentation updates
- Minor configuration changes

## Emergency Response Procedures

### 1. Initial Assessment (First 5 minutes)

```bash
# Quick system status check
python tools/phase5_health_check.py

# Check service status
docker-compose ps

# Review recent logs for errors
docker-compose logs --since 10m | grep -i error
```

**Questions to answer:**
- Which services are affected?
- When did the issue start?
- What symptoms are users experiencing?
- Is this affecting production traffic?

### 2. Communication (First 10 minutes)

- Notify incident response team
- Update status page if applicable
- Inform stakeholders for SEV 1 incidents
- Assign incident commander

### 3. Containment (First 30 minutes)

**For Service Outages:**
```bash
# Attempt service restart
docker-compose restart [affected_service]

# Check resource usage
docker stats [affected_service]

# Review service dependencies
docker-compose ps [dependency_services]
```

**For Security Incidents:**
```bash
# Isolate affected systems
docker-compose stop [compromised_services]

# Preserve evidence
docker logs [compromised_services] > incident_evidence_$(date +%Y%m%d_%H%M%S).log

# Block suspicious traffic (if applicable)
# Update firewall rules
```

### 4. Investigation (First 1-2 hours)

**Diagnostic Commands:**
```bash
# Detailed service logs
docker-compose logs --tail 500 [service_name]

# System resource analysis
top -b -n1 | head -20

# Network connectivity
docker-compose exec [service] ping -c 4 [dependency]

# Configuration validation
python tools/phase5_deployment_validator.py
```

**Common Investigation Steps:**
- Review monitoring dashboards
- Check recent configuration changes
- Analyze traffic patterns
- Review system logs

### 5. Resolution (Within SLA timeframes)

**Service Recovery:**
```bash
# Graceful service restart
docker-compose up -d [service_name]

# Verify service health
python tools/phase5_health_check.py

# Monitor for stability
python tools/phase5_monitoring_dashboard.py
```

**Configuration Fixes:**
```bash
# Update configuration
# Test configuration changes
python tools/phase5_deployment_validator.py

# Apply changes
docker-compose up -d
```

### 6. Post-Incident Activities

**Immediate (Within 1 hour of resolution):**
- Verify full system recovery
- Update incident status
- Notify stakeholders of resolution

**Short-term (Within 24 hours):**
- Document root cause analysis
- Update monitoring/alerting if needed
- Review and update runbooks

**Long-term (Within 1 week):**
- Implement preventive measures
- Update incident response procedures
- Conduct post-mortem meeting

## Service-Specific Emergency Procedures

"""

        for service in services:
            runbook = runbooks.get(service.name)
            if runbook:
                procedures += f"""### {service.name.replace('_', ' ').title()} Failure

**Recovery Steps:**
"""
                for i, step in enumerate(runbook.recovery_procedure, 1):
                    procedures += f"{i}. {step}\n"

                procedures += "\n**Common Issues:**\n"
                for issue, details in list(runbook.common_issues.items())[:3]:  # First 3 issues
                    procedures += f"- **{issue.replace('_', ' ').title()}:** {details.get('solution', 'See runbook')}\n"

                procedures += "\n**Monitoring Endpoints:**\n"
                for endpoint in runbook.monitoring_endpoints[:3]:  # First 3 endpoints
                    procedures += f"- `{endpoint}`\n"

                procedures += "\n---\n\n"

        procedures += """## Communication Templates

### Initial Incident Notification
```
INCIDENT ALERT - [SEV Level]

Time: [Timestamp]
Service: [Affected Service]
Impact: [Brief description]
Status: Investigating
Next Update: [Time]

Current Actions:
- [Action 1]
- [Action 2]
```

### Status Updates
```
INCIDENT UPDATE - [SEV Level]

Current Status: [Investigating/Resolving/Resolved]
Timeline: [Started at X, ETA Y]

Latest Actions:
- [Recent action 1]
- [Recent action 2]

Next Steps:
- [Planned action 1]
- [Planned action 2]
```

### Resolution Notification
```
INCIDENT RESOLVED - [SEV Level]

Resolution Time: [Duration]
Root Cause: [Brief summary]
Impact: [Description]

Actions Taken:
- [Action 1]
- [Action 2]

Preventive Measures:
- [Measure 1]
- [Measure 2]

Post-mortem scheduled for: [Date/Time]
```

## Escalation Matrix

### Response Times by Severity
- **SEV 1**: Immediate (0 minutes)
- **SEV 2**: Within 15 minutes
- **SEV 3**: Within 1 hour
- **SEV 4**: Next business day

### Escalation Contacts
- **Level 1**: On-call engineer
- **Level 2**: Infrastructure lead (+15 min for SEV 2)
- **Level 3**: Senior management (+1 hour for SEV 1/2)

## Tools and Resources

### Diagnostic Tools
```bash
# Comprehensive health check
python tools/phase5_health_check.py

# Real-time monitoring
python tools/phase5_monitoring_dashboard.py

# Load testing
python tools/phase5_load_test_orchestrator.py

# Deployment validation
python tools/phase5_deployment_validator.py
```

### Log Locations
- Application logs: `docker-compose logs [service]`
- System logs: `/var/log/syslog`
- Audit logs: `logs/audit.log`
- Monitoring logs: `docker-compose logs prometheus grafana`

### Backup Locations
- Database backups: `backups/postgres/`
- Redis backups: `backups/redis/`
- Configuration backups: `backups/config/`

## Training and Preparedness

### Required Training
- Incident response procedures review (quarterly)
- Tool familiarization sessions (monthly)
- Disaster recovery testing (quarterly)

### Emergency Drills
- Tabletop exercises (monthly)
- Technical drills (quarterly)
- Full disaster recovery testing (annually)

---
*Emergency procedures are regularly reviewed and updated based on incident learnings.*
"""
        return procedures

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Phase 5 Infrastructure Documentation Generator')
    parser.add_argument('--output-dir', help='Output directory for documentation')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format')

    args = parser.parse_args()

    generator = Phase5DocumentationGenerator()

    if args.output_dir:
        generator.docs_dir = Path(args.output_dir)

    try:
        docs = generator.generate_documentation()

        if args.format == 'json':
            # Output JSON metadata
            metadata_file = generator.docs_dir / "documentation_metadata.json"
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            print(json.dumps(metadata, indent=2))
        else:
            print("📚 Phase 5 Infrastructure Documentation Generated Successfully!"            print(f"📁 Documentation saved to: {generator.docs_dir}")
            print("\n📋 Generated Files:"            for filename in docs.keys():
                print(f"  • {filename}")
            print(f"\n📊 Total Services Documented: {len(generator.services_config)}")

    except Exception as e:
        logger.error(f"Documentation generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()