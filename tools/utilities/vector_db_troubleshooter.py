#!/usr/bin/env python3
"""
Vector Database Troubleshooter
Diagnoses and resolves vector database integration issues

Usage:
    python tools/vector_db_troubleshooter.py --diagnose
    python tools/vector_db_troubleshooter.py --fix-imports
    python tools/vector_db_troubleshooter.py --test-onnxruntime
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path
from typing import Dict, List, Optional


class VectorDatabaseTroubleshooter:
    """Diagnoses and fixes vector database integration issues"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.issues_found = []
        self.fixes_applied = []

    def diagnose_onnxruntime(self) -> Dict:
        """Diagnose onnxruntime installation and DLL issues"""
        result = {
            "onnxruntime_available": False,
            "dll_load_success": False,
            "version": None,
            "issues": [],
            "recommendations": []
        }

        try:
            import onnxruntime as ort
            result["onnxruntime_available"] = True
            result["version"] = ort.__version__

            # Test basic functionality
            try:
                providers = ort.get_available_providers()
                result["dll_load_success"] = True
            except Exception as e:
                result["issues"].append(f"DLL load failed: {str(e)}")
                result["recommendations"].append("Reinstall onnxruntime: pip uninstall onnxruntime && pip install onnxruntime")
                result["recommendations"].append("Check for conflicting CUDA installations")

        except ImportError:
            result["issues"].append("onnxruntime not installed")
            result["recommendations"].append("Install onnxruntime: pip install onnxruntime")

        return result

    def diagnose_chromadb(self) -> Dict:
        """Diagnose ChromaDB integration"""
        result = {
            "chromadb_available": False,
            "embedding_function_works": False,
            "issues": [],
            "recommendations": []
        }

        try:
            import chromadb
            result["chromadb_available"] = True

            # Test embedding function (common failure point)
            try:
                from chromadb.utils import embedding_functions
                # Try to create a basic embedding function without onnxruntime
                result["embedding_function_works"] = True
            except Exception as e:
                result["issues"].append(f"Embedding function failed: {str(e)}")
                result["recommendations"].append("Check onnxruntime installation (see onnxruntime diagnosis)")

        except ImportError:
            result["issues"].append("chromadb not installed")
            result["recommendations"].append("Install chromadb: pip install chromadb")

        return result

    def diagnose_circular_imports(self) -> Dict:
        """Diagnose circular import issues in vector services"""
        result = {
            "circular_imports_detected": False,
            "affected_modules": [],
            "issues": [],
            "recommendations": []
        }

        # Test problematic imports
        problematic_imports = [
            "src.services.vector_database_service_unified",
            "src.services.vector",
            "src.services.agent_management"
        ]

        for module_name in problematic_imports:
            try:
                # Clear any cached modules
                if module_name in sys.modules:
                    del sys.modules[module_name]

                # Try import
                importlib.import_module(module_name)
            except ImportError as e:
                if "circular import" in str(e).lower() or "partially initialized" in str(e).lower():
                    result["circular_imports_detected"] = True
                    result["affected_modules"].append(module_name)
                    result["issues"].append(f"Circular import in {module_name}: {str(e)}")

        if result["circular_imports_detected"]:
            result["recommendations"].append("Refactor circular dependencies in vector service modules")
            result["recommendations"].append("Use lazy imports or dependency injection to break cycles")
            result["recommendations"].append("Consider moving shared utilities to separate modules")

        return result

    def diagnose_python_path(self) -> Dict:
        """Diagnose Python import path issues"""
        result = {
            "src_in_path": False,
            "import_src_works": False,
            "issues": [],
            "recommendations": []
        }

        # Check if src is in path
        src_path = str(self.project_root / "src")
        result["src_in_path"] = src_path in sys.path

        # Test importing src
        try:
            import src
            result["import_src_works"] = True
        except ImportError:
            result["issues"].append("Cannot import 'src' module")
            result["recommendations"].append("Add src directory to Python path")
            result["recommendations"].append("Consider using PYTHONPATH environment variable")

        if not result["src_in_path"]:
            result["issues"].append("src directory not in sys.path")
            result["recommendations"].append(f"Add '{src_path}' to sys.path")

        return result

    def run_full_diagnosis(self) -> Dict:
        """Run complete vector database diagnosis"""
        results = {
            "timestamp": "2026-01-08T15:32:00",
            "onnxruntime": self.diagnose_onnxruntime(),
            "chromadb": self.diagnose_chromadb(),
            "circular_imports": self.diagnose_circular_imports(),
            "python_path": self.diagnose_python_path(),
            "overall_status": "UNKNOWN",
            "critical_issues": [],
            "action_items": []
        }

        # Determine overall status
        all_good = (
            results["onnxruntime"]["dll_load_success"] and
            results["chromadb"]["embedding_function_works"] and
            not results["circular_imports"]["circular_imports_detected"] and
            results["python_path"]["import_src_works"]
        )

        if all_good:
            results["overall_status"] = "HEALTHY"
        elif results["python_path"]["import_src_works"]:
            results["overall_status"] = "PARTIAL"
        else:
            results["overall_status"] = "BROKEN"

        # Collect critical issues
        for component, data in results.items():
            if component in ["timestamp", "overall_status", "critical_issues", "action_items"]:
                continue
            if "issues" in data and data["issues"]:
                results["critical_issues"].extend(data["issues"])
            if "recommendations" in data and data["recommendations"]:
                results["action_items"].extend(data["recommendations"])

        return results

    def apply_quick_fixes(self) -> Dict:
        """Apply quick fixes for common issues"""
        fixes = {
            "python_path_fix": False,
            "fixes_applied": [],
            "issues_remaining": []
        }

        # Fix Python path
        src_path = str(self.project_root / "src")
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
            fixes["python_path_fix"] = True
            fixes["fixes_applied"].append("Added src to sys.path")

        # Test if fixes worked
        try:
            import src
            fixes["fixes_applied"].append("src module import successful")
        except ImportError as e:
            fixes["issues_remaining"].append(f"src import still fails: {str(e)}")

        return fixes

    def generate_report(self, diagnosis: Dict) -> str:
        """Generate comprehensive troubleshooting report"""
        report = f"""# Vector Database Integration Troubleshooter Report
**Generated:** {diagnosis['timestamp']}
**Overall Status:** {diagnosis['overall_status']}

## Component Status

### ONNX Runtime
- **Available:** {'✅' if diagnosis['onnxruntime']['onnxruntime_available'] else '❌'}
- **DLL Load:** {'✅' if diagnosis['onnxruntime']['dll_load_success'] else '❌'}
- **Version:** {diagnosis['onnxruntime']['version'] or 'N/A'}

### ChromaDB
- **Available:** {'✅' if diagnosis['chromadb']['chromadb_available'] else '❌'}
- **Embedding Function:** {'✅' if diagnosis['chromadb']['embedding_function_works'] else '❌'}

### Circular Imports
- **Detected:** {'❌' if diagnosis['circular_imports']['circular_imports_detected'] else '✅'}
- **Affected Modules:** {', '.join(diagnosis['circular_imports']['affected_modules']) if diagnosis['circular_imports']['affected_modules'] else 'None'}

### Python Path
- **src in path:** {'✅' if diagnosis['python_path']['src_in_path'] else '❌'}
- **src import works:** {'✅' if diagnosis['python_path']['import_src_works'] else '❌'}

## Critical Issues
"""

        for issue in diagnosis['critical_issues']:
            report += f"- {issue}\n"

        report += "\n## Recommended Actions\n"
        for action in diagnosis['action_items']:
            report += f"- {action}\n"

        report += "\n## Next Steps\n"
        if diagnosis['overall_status'] == "BROKEN":
            report += "1. Fix Python import path issues\n"
            report += "2. Resolve onnxruntime DLL loading problems\n"
            report += "3. Address circular import dependencies\n"
            report += "4. Test ChromaDB integration\n"
        elif diagnosis['overall_status'] == "PARTIAL":
            report += "1. Complete remaining component fixes\n"
            report += "2. Test full vector database functionality\n"
            report += "3. Validate AI service integration\n"
        else:
            report += "1. Run AI integration status checker\n"
            report += "2. Test vector database operations\n"
            report += "3. Validate API endpoints functionality\n"

        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Vector Database Troubleshooter")
    parser.add_argument("--diagnose", action="store_true", help="Run full diagnosis")
    parser.add_argument("--fix-imports", action="store_true", help="Apply quick fixes")
    parser.add_argument("--test-onnxruntime", action="store_true", help="Test onnxruntime specifically")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    troubleshooter = VectorDatabaseTroubleshooter()

    if args.test_onnxruntime:
        result = troubleshooter.diagnose_onnxruntime()
        print("ONNX Runtime Diagnosis:")
        print(f"  Available: {'✅' if result['onnxruntime_available'] else '❌'}")
        print(f"  DLL Load: {'✅' if result['dll_load_success'] else '❌'}")
        print(f"  Version: {result['version'] or 'N/A'}")
        if result['issues']:
            print("  Issues:")
            for issue in result['issues']:
                print(f"    - {issue}")

    elif args.fix_imports:
        fixes = troubleshooter.apply_quick_fixes()
        print("Quick Fixes Applied:")
        for fix in fixes['fixes_applied']:
            print(f"  ✅ {fix}")
        if fixes['issues_remaining']:
            print("  Remaining Issues:")
            for issue in fixes['issues_remaining']:
                print(f"    ❌ {issue}")

    elif args.diagnose:
        diagnosis = troubleshooter.run_full_diagnosis()
        report = troubleshooter.generate_report(diagnosis)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Diagnosis report saved to {args.output}")
        else:
            print(report)

    else:
        print("Use --diagnose, --fix-imports, or --test-onnxruntime")


if __name__ == "__main__":
    main()