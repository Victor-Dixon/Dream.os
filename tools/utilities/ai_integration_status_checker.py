#!/usr/bin/env python3
"""
AI Integration Status Checker
Validates AI service availability and vector database integration

Usage:
    python tools/ai_integration_status_checker.py --check-all
    python tools/ai_integration_status_checker.py --check-service recommendation_engine
    python tools/ai_integration_status_checker.py --vector-db-status
"""

import argparse
import importlib
import sys
from typing import Dict, List, Optional


class AIIntegrationStatusChecker:
    """Checks AI integration status across swarm services"""

    def __init__(self):
        self.ai_services = [
            "performance_analyzer",
            "recommendation_engine",
            "work_indexer",
            "learning_recommender",
            "ai_service",
            "ai_context_engine"
        ]

        self.vector_db_services = [
            "vector_database_service",
            "dreamvault.database",
            "dreamvault.embedding_builder"
        ]

    def check_service_availability(self, service_name: str) -> Dict:
        """Check if an AI service can be imported and initialized"""
        result = {
            "service": service_name,
            "importable": False,
            "initializable": False,
            "vector_db_available": True,
            "errors": []
        }

        try:
            # Try to import the service
            module_path = f"src.services.{service_name}"
            module = importlib.import_module(module_path)
            result["importable"] = True

            # Try to initialize if it has an init function or class
            if hasattr(module, 'init') or hasattr(module, 'initialize'):
                try:
                    if hasattr(module, 'init'):
                        module.init()
                    elif hasattr(module, 'initialize'):
                        module.initialize()
                    result["initializable"] = True
                except Exception as e:
                    error_msg = str(e)
                    result["errors"].append(f"Initialization failed: {error_msg}")
                    if "vector database" in error_msg.lower() or "onnxruntime" in error_msg.lower():
                        result["vector_db_available"] = False

        except ImportError as e:
            result["errors"].append(f"Import failed: {str(e)}")
        except Exception as e:
            result["errors"].append(f"Unexpected error: {str(e)}")

        return result

    def check_vector_db_status(self) -> Dict:
        """Check vector database infrastructure status"""
        result = {
            "onnxruntime_available": False,
            "chromadb_available": False,
            "sentence_transformers_available": False,
            "vector_services_status": [],
            "overall_status": "UNKNOWN"
        }

        # Check core dependencies
        try:
            import onnxruntime
            result["onnxruntime_available"] = True
        except ImportError:
            pass

        try:
            import chromadb
            result["chromadb_available"] = True
        except ImportError:
            pass

        try:
            import sentence_transformers
            result["sentence_transformers_available"] = True
        except ImportError:
            pass

        # Check vector services
        for service in self.vector_db_services:
            service_result = self.check_service_availability(service)
            result["vector_services_status"].append(service_result)

        # Determine overall status
        if result["onnxruntime_available"] and result["chromadb_available"]:
            result["overall_status"] = "READY"
        elif result["chromadb_available"]:
            result["overall_status"] = "PARTIAL"
        else:
            result["overall_status"] = "BLOCKED"

        return result

    def run_comprehensive_check(self) -> Dict:
        """Run comprehensive AI integration status check"""
        results = {
            "timestamp": "2026-01-08T14:52:00",
            "ai_services_status": [],
            "vector_db_status": self.check_vector_db_status(),
            "summary": {
                "total_services": len(self.ai_services),
                "services_importable": 0,
                "services_initializable": 0,
                "services_blocked_by_vector_db": 0,
                "vector_db_status": "UNKNOWN"
            }
        }

        # Check all AI services
        for service in self.ai_services:
            service_result = self.check_service_availability(service)
            results["ai_services_status"].append(service_result)

            if service_result["importable"]:
                results["summary"]["services_importable"] += 1
            if service_result["initializable"]:
                results["summary"]["services_initializable"] += 1
            if not service_result["vector_db_available"]:
                results["summary"]["services_blocked_by_vector_db"] += 1

        results["summary"]["vector_db_status"] = results["vector_db_status"]["overall_status"]

        return results

    def generate_report(self, results: Dict) -> str:
        """Generate human-readable status report"""
        report = f"""# AI Integration Status Report
**Generated:** {results['timestamp']}

## Executive Summary
- **AI Services Checked:** {results['summary']['total_services']}
- **Services Importable:** {results['summary']['services_importable']}/{results['summary']['total_services']}
- **Services Initializable:** {results['summary']['services_initializable']}/{results['summary']['total_services']}
- **Services Blocked by Vector DB:** {results['summary']['services_blocked_by_vector_db']}/{results['summary']['total_services']}
- **Vector DB Status:** {results['summary']['vector_db_status']}

## Vector Database Status
- **ONNX Runtime:** {'✅' if results['vector_db_status']['onnxruntime_available'] else '❌'} Available
- **ChromaDB:** {'✅' if results['vector_db_status']['chromadb_available'] else '❌'} Available
- **Sentence Transformers:** {'✅' if results['vector_db_status']['sentence_transformers_available'] else '❌'} Available

## AI Services Status
"""

        for service in results["ai_services_status"]:
            status_icon = "✅" if service["initializable"] else "⚠️" if service["importable"] else "❌"
            vector_icon = "✅" if service["vector_db_available"] else "🔴"
            report += f"### {service['service']}\n"
            report += f"**Status:** {status_icon} {'Operational' if service['initializable'] else 'Importable' if service['importable'] else 'Failed'}\n"
            report += f"**Vector DB:** {vector_icon} {'Available' if service['vector_db_available'] else 'BLOCKED'}\n"
            if service["errors"]:
                report += "**Errors:**\n"
                for error in service["errors"]:
                    report += f"- {error}\n"
            report += "\n"

        report += "## Vector Services Status\n"

        for service in results["vector_db_status"]["vector_services_status"]:
            status_icon = "✅" if service["initializable"] else "⚠️" if service["importable"] else "❌"
            report += f"### {service['service']}\n"
            report += f"**Status:** {status_icon}\n"
            if service["errors"]:
                for error in service["errors"]:
                    report += f"- {error}\n"
            report += "\n"

        return report


def main():
    parser = argparse.ArgumentParser(description="AI Integration Status Checker")
    parser.add_argument("--check-all", action="store_true", help="Run comprehensive check")
    parser.add_argument("--check-service", help="Check specific service")
    parser.add_argument("--vector-db-status", action="store_true", help="Check vector database status only")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    checker = AIIntegrationStatusChecker()

    if args.check_service:
        result = checker.check_service_availability(args.check_service)
        print(f"Service: {result['service']}")
        print(f"Importable: {result['importable']}")
        print(f"Initializable: {result['initializable']}")
        print(f"Vector DB Available: {result['vector_db_available']}")
        if result['errors']:
            print("Errors:")
            for error in result['errors']:
                print(f"  - {error}")

    elif args.vector_db_status:
        result = checker.check_vector_db_status()
        print("Vector Database Status:")
        print(f"  ONNX Runtime: {'✅' if result['onnxruntime_available'] else '❌'}")
        print(f"  ChromaDB: {'✅' if result['chromadb_available'] else '❌'}")
        print(f"  Sentence Transformers: {'✅' if result['sentence_transformers_available'] else '❌'}")
        print(f"  Overall Status: {result['overall_status']}")

    elif args.check_all:
        results = checker.run_comprehensive_check()
        report = checker.generate_report(results)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    else:
        print("Use --check-all, --check-service SERVICE, or --vector-db-status")


if __name__ == "__main__":
    main()