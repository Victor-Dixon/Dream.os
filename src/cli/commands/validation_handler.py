"""
Validation Command Handler - V2 Compliant (<400 lines)
Handles comprehensive system validation and health checks.
"""

import sys
from typing import Dict, Any, List, Tuple
from src.cli.validation_runner import ValidationRunner


class ValidationHandler:
    """Handles validation command with comprehensive system checks."""

    def __init__(self):
        self.validation_runner = ValidationRunner()

    def execute(self) -> int:
        """Execute validation command. Returns exit code."""
        print("🔍 dream.os - System Validation")
        print("=" * 40)

        try:
            results = self.validation_runner.run_comprehensive_validation()
            return self._display_results(results)
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            return 1

    def _display_results(self, results: Dict[str, Any]) -> int:
        """Display validation results and return appropriate exit code."""
        if not results:
            print("❌ No validation results returned.")
            return 1

        # Handle nested results structure from ValidationRunner
        validations = results.get('validations', results)

        # Display overall status
        overall_status = results.get('overall_status', 'UNKNOWN')
        print(f"\n📊 Overall Status: {overall_status}")

        # Categorize results
        passed = []
        failed = []
        warnings = []
        errors = []

        for check_name, check_result in validations.items():
            if isinstance(check_result, dict):
                status = check_result.get('status', 'UNKNOWN')
                if status == 'PASS':
                    passed.append((check_name, check_result))
                elif status == 'FAIL':
                    failed.append((check_name, check_result))
                elif status == 'WARN':
                    warnings.append((check_name, check_result))
                elif status == 'ERROR':
                    errors.append((check_name, check_result))
                else:
                    warnings.append((check_name, check_result))
            else:
                # Handle string results
                if 'PASS' in str(check_result).upper():
                    passed.append((check_name, {'message': str(check_result)}))
                elif 'FAIL' in str(check_result).upper():
                    failed.append((check_name, {'message': str(check_result)}))
                else:
                    warnings.append((check_name, {'message': str(check_result)}))

        # Display passed checks
        if passed:
            print(f"\n✅ PASSED ({len(passed)}):")
            for check_name, result in passed:
                message = result.get('message', 'OK')
                print(f"   🟢 {check_name}: {message}")

        # Display warnings
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for check_name, result in warnings:
                message = result.get('message', 'Warning')
                print(f"   🟡 {check_name}: {message}")

        # Display failed checks with details
        if failed:
            print(f"\n❌ FAILED ({len(failed)}):")
            for check_name, result in failed:
                message = result.get('message', 'Failed')
                print(f"   🔴 {check_name}: {message}")

                # Show additional details if available
                if 'details' in result:
                    details = result['details']
                    if isinstance(details, list):
                        for detail in details[:3]:  # Show first 3 details
                            print(f"      • {detail}")
                        if len(details) > 3:
                            print(f"      • ... and {len(details) - 3} more")
                    elif isinstance(details, str):
                        print(f"      • {details}")

                # Show recommendations if available
                if 'recommendations' in result:
                    recommendations = result['recommendations']
                    if isinstance(recommendations, list) and recommendations:
                        print("      💡 Recommendations:")
                        for rec in recommendations[:2]:  # Show first 2 recommendations
                            print(f"         • {rec}")
                        if len(recommendations) > 2:
                            print(f"         • ... and {len(recommendations) - 2} more")

        # Overall summary
        total_checks = len(results)
        passed_count = len(passed)
        failed_count = len(failed)
        warning_count = len(warnings)

        print(f"\n📊 VALIDATION SUMMARY: {passed_count}/{total_checks} checks passed")

        # Determine exit code and overall status
        if failed_count > 0:
            print("🚨 Critical validation failures detected!")
            print("   System may not function correctly.")
            print("\n💡 Fix validation errors before proceeding.")
            return 1
        elif warning_count > 0:
            print("⚠️  Validation passed with warnings.")
            print("   System should function but review warnings.")
            return 0
        else:
            print("🎉 All validations passed!")
            print("   System ready for operation.")
            return 0