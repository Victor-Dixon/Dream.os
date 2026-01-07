#!/usr/bin/env python3
"""
Phase 5 Infrastructure Deployment Validator
Comprehensive validation of Phase 5 enterprise infrastructure deployment
"""

import os
import json
import yaml
import subprocess
import sys
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    component: str
    status: str
    details: Dict
    recommendations: List[str]
    timestamp: str

class Phase5DeploymentValidator:
    def __init__(self):
        self.results = []
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def validate_file_exists(self, file_path: str, component: str) -> ValidationResult:
        """Validate that a required file exists"""
        full_path = os.path.join(self.base_dir, file_path)

        if os.path.exists(full_path):
            status = "PASS"
            details = {"file_path": full_path, "size_bytes": os.path.getsize(full_path)}
            recommendations = []
        else:
            status = "FAIL"
            details = {"file_path": full_path, "error": "File not found"}
            recommendations = [f"Create {file_path} or check file path"]

        return ValidationResult(
            component=component,
            status=status,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def validate_docker_compose_config(self) -> ValidationResult:
        """Validate Docker Compose configuration"""
        compose_file = "docker-compose.yml"

        try:
            with open(os.path.join(self.base_dir, compose_file), 'r') as f:
                compose_config = yaml.safe_load(f)

            services = compose_config.get('services', {})
            expected_services = ['flask_app', 'fastapi_app', 'kong', 'nginx', 'postgres', 'redis', 'prometheus', 'grafana', 'istio-proxy']

            found_services = list(services.keys())
            missing_services = [s for s in expected_services if s not in found_services]
            extra_services = [s for s in found_services if s not in expected_services]

            # Check service configurations
            issues = []
            for service_name, service_config in services.items():
                if 'image' not in service_config and 'build' not in service_config:
                    issues.append(f"{service_name}: Missing image or build configuration")
                if 'ports' not in service_config:
                    issues.append(f"{service_name}: No ports exposed")
                if 'depends_on' not in service_config and service_name != 'postgres':
                    issues.append(f"{service_name}: Missing dependency declarations")

            if missing_services or extra_services or issues:
                status = "WARNING"
                details = {
                    "total_services": len(found_services),
                    "expected_services": expected_services,
                    "found_services": found_services,
                    "missing_services": missing_services,
                    "extra_services": extra_services,
                    "configuration_issues": issues
                }
                recommendations = []
                if missing_services:
                    recommendations.append(f"Add missing services: {', '.join(missing_services)}")
                if issues:
                    recommendations.extend([f"Fix: {issue}" for issue in issues])
            else:
                status = "PASS"
                details = {
                    "total_services": len(found_services),
                    "services_configured": found_services
                }
                recommendations = []

        except Exception as e:
            status = "FAIL"
            details = {"error": str(e)}
            recommendations = ["Check Docker Compose YAML syntax"]

        return ValidationResult(
            component="Docker Compose Configuration",
            status=status,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def validate_nginx_config(self) -> ValidationResult:
        """Validate Nginx configuration"""
        nginx_config = "nginx/nginx.conf"

        try:
            # Check if nginx config file exists
            config_path = os.path.join(self.base_dir, nginx_config)
            if not os.path.exists(config_path):
                return ValidationResult(
                    component="Nginx Configuration",
                    status="FAIL",
                    details={"error": "nginx.conf not found"},
                    recommendations=["Create nginx/nginx.conf configuration file"],
                    timestamp=datetime.now().isoformat()
                )

            # Read configuration content
            with open(config_path, 'r') as f:
                config_content = f.read()

            # Check for required Phase 5 features
            required_features = {
                'upstream fastapi_backend': 'FastAPI upstream configuration',
                'upstream kong_gateway': 'Kong gateway upstream configuration',
                'location /api/v1/': 'FastAPI API routing',
                'location /gateway/': 'Kong gateway routing',
                'ssl_certificate': 'SSL certificate configuration',
                'ssl_protocols': 'SSL protocol configuration',
                'limit_req_zone': 'Rate limiting configuration',
                'proxy_cache cdn_cache': 'CDN cache configuration'
            }

            found_features = {}
            missing_features = {}

            for feature, description in required_features.items():
                if feature in config_content:
                    found_features[feature] = description
                else:
                    missing_features[feature] = description

            if missing_features:
                status = "WARNING"
                details = {
                    "config_file": config_path,
                    "features_found": found_features,
                    "features_missing": missing_features
                }
                recommendations = [f"Add {desc}: {feature}" for feature, desc in missing_features.items()]
            else:
                status = "PASS"
                details = {
                    "config_file": config_path,
                    "features_validated": list(found_features.keys())
                }
                recommendations = []

        except Exception as e:
            status = "FAIL"
            details = {"error": str(e)}
            recommendations = ["Check nginx configuration syntax"]

        return ValidationResult(
            component="Nginx Configuration",
            status=status,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def validate_ssl_configuration(self) -> ValidationResult:
        """Validate SSL certificate configuration"""
        ssl_dir = "ssl"
        cert_files = ["cert.pem", "key.pem", "ssl-config.sh"]

        issues = []
        found_files = []

        for cert_file in cert_files:
            file_path = os.path.join(self.base_dir, ssl_dir, cert_file)
            if os.path.exists(file_path):
                found_files.append(cert_file)
                # Check if ssl-config.sh is executable
                if cert_file == "ssl-config.sh" and not os.access(file_path, os.X_OK):
                    issues.append("ssl-config.sh is not executable")
            else:
                issues.append(f"Missing SSL file: {cert_file}")

        # Check certificate validity if files exist
        cert_path = os.path.join(self.base_dir, ssl_dir, "cert.pem")
        key_path = os.path.join(self.base_dir, ssl_dir, "key.pem")

        if os.path.exists(cert_path) and os.path.exists(key_path):
            try:
                # Use openssl to check certificate
                result = subprocess.run(
                    ['openssl', 'x509', '-in', cert_path, '-text', '-noout'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    # Extract certificate info
                    cert_info = result.stdout
                    if "Issuer:" in cert_info and "Subject:" in cert_info:
                        cert_status = "Certificate appears valid"
                    else:
                        cert_status = "Certificate format unclear"
                        issues.append("Certificate may not be properly formatted")
                else:
                    cert_status = "Certificate validation failed"
                    issues.append("Certificate validation failed with openssl")
            except Exception as e:
                cert_status = f"Certificate check failed: {e}"
                issues.append("Unable to validate certificate")
        else:
            cert_status = "Certificate files not found"
            issues.append("Certificate files missing for validation")

        if issues:
            status = "WARNING" if found_files else "FAIL"
            details = {
                "ssl_directory": ssl_dir,
                "files_found": found_files,
                "certificate_status": cert_status,
                "issues": issues
            }
            recommendations = issues + (["Run ssl/ssl-config.sh to generate certificates"] if not found_files else [])
        else:
            status = "PASS"
            details = {
                "ssl_directory": ssl_dir,
                "files_found": found_files,
                "certificate_status": cert_status
            }
            recommendations = []

        return ValidationResult(
            component="SSL Configuration",
            status=status,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def validate_monitoring_config(self) -> ValidationResult:
        """Validate monitoring configuration"""
        monitoring_files = [
            "config/prometheus.yml",
            "config/alert_rules.yml",
            "config/grafana/provisioning/datasources/prometheus.yml",
            "config/grafana/provisioning/dashboards/dashboard.yml"
        ]

        issues = []
        found_files = []

        for config_file in monitoring_files:
            file_path = os.path.join(self.base_dir, config_file)
            if os.path.exists(file_path):
                found_files.append(config_file)

                # Basic validation of YAML files
                try:
                    with open(file_path, 'r') as f:
                        yaml.safe_load(f)
                except Exception as e:
                    issues.append(f"{config_file}: Invalid YAML syntax - {e}")
            else:
                issues.append(f"Missing monitoring file: {config_file}")

        # Check for dashboard files
        dashboard_dir = "config/grafana/provisioning/dashboards"
        dashboard_path = os.path.join(self.base_dir, dashboard_dir)
        if os.path.exists(dashboard_path):
            dashboard_files = [f for f in os.listdir(dashboard_path) if f.endswith('.json')]
            if dashboard_files:
                found_files.extend([f"{dashboard_dir}/{f}" for f in dashboard_files])
            else:
                issues.append("No Grafana dashboard files found")
        else:
            issues.append("Grafana dashboards directory missing")

        if issues:
            status = "WARNING"
            details = {
                "monitoring_files_found": found_files,
                "issues": issues
            }
            recommendations = issues
        else:
            status = "PASS"
            details = {
                "monitoring_files_configured": found_files,
                "monitoring_stack": ["Prometheus", "Grafana", "Alert Rules"]
            }
            recommendations = []

        return ValidationResult(
            component="Monitoring Configuration",
            status=status,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def validate_database_config(self) -> ValidationResult:
        """Validate database configuration"""
        db_config_file = "config/database-optimization.conf"

        try:
            config_path = os.path.join(self.base_dir, db_config_file)
            if not os.path.exists(config_path):
                return ValidationResult(
                    component="Database Configuration",
                    status="FAIL",
                    details={"error": "Database optimization config not found"},
                    recommendations=["Create config/database-optimization.conf with PostgreSQL and Redis optimization settings"],
                    timestamp=datetime.now().isoformat()
                )

            with open(config_path, 'r') as f:
                db_config = yaml.safe_load(f)

            # Check for required sections
            required_sections = ['postgresql', 'redis', 'monitoring']
            found_sections = []
            missing_sections = []

            for section in required_sections:
                if section in db_config:
                    found_sections.append(section)
                else:
                    missing_sections.append(section)

            # Validate PostgreSQL settings
            pg_issues = []
            if 'postgresql' in db_config:
                pg_config = db_config['postgresql']
                required_pg_settings = ['max_connections', 'shared_buffers', 'work_mem', 'wal_level']
                for setting in required_pg_settings:
                    if setting not in pg_config:
                        pg_issues.append(f"Missing PostgreSQL setting: {setting}")

            # Validate Redis settings
            redis_issues = []
            if 'redis' in db_config:
                redis_config = db_config['redis']
                required_redis_settings = ['maxmemory', 'maxmemory-policy', 'appendonly']
                for setting in required_redis_settings:
                    if setting not in redis_config:
                        redis_issues.append(f"Missing Redis setting: {setting}")

            all_issues = pg_issues + redis_issues

            if missing_sections or all_issues:
                status = "WARNING"
                details = {
                    "config_file": db_config_file,
                    "sections_found": found_sections,
                    "sections_missing": missing_sections,
                    "configuration_issues": all_issues
                }
                recommendations = []
                if missing_sections:
                    recommendations.extend([f"Add missing section: {section}" for section in missing_sections])
                recommendations.extend(all_issues)
            else:
                status = "PASS"
                details = {
                    "config_file": db_config_file,
                    "sections_configured": found_sections,
                    "databases_supported": ["PostgreSQL", "Redis"]
                }
                recommendations = []

        except Exception as e:
            status = "FAIL"
            details = {"error": str(e)}
            recommendations = ["Check database configuration YAML syntax"]

        return ValidationResult(
            component="Database Configuration",
            status=status,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def run_comprehensive_validation(self) -> Dict:
        """Run comprehensive deployment validation"""
        logger.info("🚀 Starting Phase 5 Infrastructure Deployment Validation...")

        # Define validation checks
        validations = [
            lambda: self.validate_file_exists("docker-compose.yml", "Docker Compose File"),
            lambda: self.validate_file_exists("nginx/nginx.conf", "Nginx Configuration"),
            lambda: self.validate_file_exists("ssl/cert.pem", "SSL Certificate"),
            lambda: self.validate_file_exists("ssl/key.pem", "SSL Private Key"),
            lambda: self.validate_file_exists("config/prometheus.yml", "Prometheus Configuration"),
            self.validate_docker_compose_config,
            self.validate_nginx_config,
            self.validate_ssl_configuration,
            self.validate_monitoring_config,
            self.validate_database_config,
        ]

        # Run all validations
        results = []
        for validation_func in validations:
            try:
                result = validation_func()
                results.append(result)
            except Exception as e:
                # Handle validation errors
                error_result = ValidationResult(
                    component="Validation Error",
                    status="ERROR",
                    details={"error": str(e)},
                    recommendations=["Check validation function implementation"],
                    timestamp=datetime.now().isoformat()
                )
                results.append(error_result)

        self.results = results

        # Calculate summary statistics
        total_checks = len(results)
        passed_checks = len([r for r in results if r.status == "PASS"])
        warning_checks = len([r for r in results if r.status == "WARNING"])
        failed_checks = len([r for r in results if r.status in ["FAIL", "ERROR"]])

        all_recommendations = []
        for result in results:
            all_recommendations.extend(result.recommendations)

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_validations": total_checks,
            "passed_validations": passed_checks,
            "warning_validations": warning_checks,
            "failed_validations": failed_checks,
            "success_rate": round((passed_checks / total_checks) * 100, 1) if total_checks > 0 else 0,
            "deployment_readiness": self._calculate_deployment_readiness(results),
            "total_recommendations": len(all_recommendations)
        }

        return {
            "summary": summary,
            "results": [asdict(result) for result in results],
            "recommendations": list(set(all_recommendations))  # Remove duplicates
        }

    def _calculate_deployment_readiness(self, results: List[ValidationResult]) -> str:
        """Calculate overall deployment readiness"""
        if not results:
            return "UNKNOWN"

        passed_count = len([r for r in results if r.status == "PASS"])
        total_count = len(results)
        success_rate = passed_count / total_count

        if success_rate >= 0.95:
            return "PRODUCTION_READY"
        elif success_rate >= 0.80:
            return "STAGING_READY"
        elif success_rate >= 0.60:
            return "DEVELOPMENT_READY"
        else:
            return "NEEDS_ATTENTION"

    def print_report(self, data: Dict):
        """Print comprehensive validation report"""
        print("\n" + "="*100)
        print("🔍 PHASE 5 INFRASTRUCTURE DEPLOYMENT VALIDATION REPORT")
        print("="*100)

        summary = data["summary"]
        print(f"🎯 DEPLOYMENT READINESS: {summary['deployment_readiness']}")
        print(f"📊 VALIDATIONS RUN: {summary['total_validations']}")
        print(f"✅ PASSED: {summary['passed_validations']}")
        print(f"⚠️  WARNINGS: {summary['warning_validations']}")
        print(f"❌ FAILED: {summary['failed_validations']}")
        print(".1f"        print(f"📋 RECOMMENDATIONS: {summary['total_recommendations']}")

        print("\n" + "-"*100)
        print("📋 VALIDATION DETAILS")
        print("-"*100)

        for result in data["results"]:
            status_emoji = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARNING" else "❌"
            print(f"{status_emoji} {result['component']:<30} | {result['status']}")
            if result["recommendations"]:
                for rec in result["recommendations"][:2]:  # Show first 2 recommendations
                    print(f"   → {rec}")
                if len(result["recommendations"]) > 2:
                    print(f"   → ... and {len(result['recommendations']) - 2} more")

        if data["recommendations"]:
            print("\n" + "-"*100)
            print("💡 ACTION ITEMS")
            print("-"*100)
            for i, rec in enumerate(data["recommendations"][:10], 1):  # Show first 10
                print(f"{i:2d}. {rec}")
            if len(data["recommendations"]) > 10:
                print(f"   ... and {len(data['recommendations']) - 10} more recommendations")

        print("\n" + "="*100)

    def save_report(self, data: Dict, filename: str = None):
        """Save validation report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phase5_deployment_validation_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"📄 Report saved to: {filename}")

def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Phase 5 Infrastructure Deployment Validator')
    parser.add_argument('--output', type=str, help='Output filename for JSON report')
    parser.add_argument('--quiet', action='store_true', help='Suppress console output')

    args = parser.parse_args()

    validator = Phase5DeploymentValidator()

    try:
        results = validator.run_comprehensive_validation()

        if not args.quiet:
            validator.print_report(results)

        validator.save_report(results, args.output)

        # Exit with appropriate code based on validation results
        summary = results["summary"]
        if summary["failed_validations"] > 0:
            sys.exit(1)  # Critical validation failures
        elif summary["warning_validations"] > 0:
            sys.exit(2)  # Warnings present
        else:
            sys.exit(0)  # All validations passed

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()