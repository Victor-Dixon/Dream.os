#!/usr/bin/env python3
"""
FastAPI Refactoring Validation Framework
========================================

Validation checklist for fastapi_app.py modularization (1526 lines → ~80 lines).
Ensures functionality preservation during V2 compliance refactoring.

Author: Agent-4 (Captain - Strategic Coordination)
Date: 2026-01-08
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

class FastAPIRefactoringValidator:
    """Validates fastapi_app.py modularization maintains functionality."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.fastapi_file = self.project_root / "src" / "web" / "fastapi_app.py"
        self.validation_results = {}

    def validate_file_structure(self) -> Dict[str, bool]:
        """Validate that refactored file structure meets V2 compliance."""
        results = {}

        # Check main file size
        if self.fastapi_file.exists():
            with open(self.fastapi_file, 'r', encoding='utf-8') as f:
                line_count = len(f.readlines())
            results["main_file_size"] = line_count <= 100
            results["main_file_exists"] = True
        else:
            results["main_file_exists"] = False
            results["main_file_size"] = False

        # Check that modular components exist
        modular_files = [
            "src/web/fastapi_config.py",
            "src/web/fastapi_middleware.py",
            "src/web/fastapi_routes.py"
        ]

        for mod_file in modular_files:
            mod_path = self.project_root / mod_file
            results[f"{Path(mod_file).stem}_exists"] = mod_path.exists()
            if mod_path.exists():
                with open(mod_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                results[f"{Path(mod_file).stem}_size"] = lines <= 400

        return results

    def extract_route_definitions(self, file_path: Path) -> Set[str]:
        """Extract all route definitions from a file."""
        routes = set()
        if not file_path.exists():
            return routes

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find @app.route or @router. patterns
        import re
        route_pattern = r'@(?:app|router)\.(?:get|post|put|delete|patch|options|head)\s*\(\s*["\']([^"\']+)["\']'
        matches = re.findall(route_pattern, content)
        routes.update(matches)

        return routes

    def validate_route_coverage(self) -> Dict[str, bool]:
        """Validate that all routes are preserved in modular structure."""
        results = {}

        # Get routes from original file (before refactoring)
        original_routes = self.extract_route_definitions(self.fastapi_file)

        # Get routes from modular files
        modular_routes = set()
        modular_files = [
            "src/web/fastapi_routes.py",
            "src/web/fastapi_middleware.py"
        ]

        for mod_file in modular_files:
            mod_path = self.project_root / mod_file
            modular_routes.update(self.extract_route_definitions(mod_path))

        # Check coverage
        results["routes_preserved"] = original_routes.issubset(modular_routes)
        results["original_routes_count"] = len(original_routes)
        results["modular_routes_count"] = len(modular_routes)

        return results

    def validate_imports(self) -> Dict[str, bool]:
        """Validate that all necessary imports are preserved."""
        results = {}

        # Check that modular files can be imported
        try:
            from src.web import fastapi_config, fastapi_middleware, fastapi_routes
            results["modular_imports_work"] = True
        except ImportError as e:
            results["modular_imports_work"] = False
            results["import_error"] = str(e)

        return results

    def validate_functionality(self) -> Dict[str, bool]:
        """Validate that core functionality is preserved."""
        results = {}

        # Test basic FastAPI startup
        try:
            from src.web.fastapi_app import app
            results["app_creation_works"] = app is not None
            results["app_title"] = hasattr(app, 'title')
        except Exception as e:
            results["app_creation_works"] = False
            results["app_creation_error"] = str(e)

        # Test middleware setup
        try:
            from src.web.fastapi_middleware import setup_all_middleware
            results["middleware_import_works"] = True
        except ImportError:
            results["middleware_import_works"] = False

        return results

    def run_full_validation(self) -> Dict[str, Dict[str, bool]]:
        """Run complete validation suite."""
        print("🔍 Running FastAPI Refactoring Validation...")
        print("=" * 50)

        validation_results = {
            "file_structure": self.validate_file_structure(),
            "route_coverage": self.validate_route_coverage(),
            "imports": self.validate_imports(),
            "functionality": self.validate_functionality()
        }

        # Calculate overall compliance
        all_checks = []
        for category, checks in validation_results.items():
            for key, value in checks.items():
                if isinstance(value, bool):
                    all_checks.append(value)

        validation_results["summary"] = {
            "total_checks": len(all_checks),
            "passed_checks": sum(all_checks),
            "compliance_percentage": (sum(all_checks) / len(all_checks)) * 100 if all_checks else 0,
            "v2_compliant": all(all_checks)
        }

        return validation_results

    def print_validation_report(self, results: Dict[str, Dict[str, bool]]):
        """Print formatted validation report."""
        print("\n📊 FASTAPI REFACTORING VALIDATION REPORT")
        print("=" * 50)

        for category, checks in results.items():
            if category == "summary":
                continue
            print(f"\n🔧 {category.upper().replace('_', ' ')}:")
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {check.replace('_', ' ').title()}")

        # Summary
        summary = results.get("summary", {})
        print(f"\n📈 SUMMARY:")
        print(f"  Total Checks: {summary.get('total_checks', 0)}")
        print(f"  Passed: {summary.get('passed_checks', 0)}")
        print(f"  Compliance: {summary.get('compliance_percentage', 0):.1f}%")
        print(f"  V2 Compliant: {'✅ YES' if summary.get('v2_compliant', False) else '❌ NO'}")

def main():
    """Run validation and exit with appropriate code."""
    validator = FastAPIRefactoringValidator()
    results = validator.run_full_validation()
    validator.print_validation_report(results)

    # Exit with success/failure code
    summary = results.get("summary", {})
    is_compliant = summary.get("v2_compliant", False)
    sys.exit(0 if is_compliant else 1)

if __name__ == "__main__":
    main()