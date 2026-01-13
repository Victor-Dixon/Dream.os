"""
Validation Runner - Agent Cellphone V2
====================================

Runs comprehensive validation checks for the system including:
- SSOT compliance validation
- V2 compliance checks
- Integration status validation
- Service readiness validation
- Code quality checks

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ValidationRunner:
    """
    Runs comprehensive validation checks for the Agent Cellphone V2 system.
    """

    def __init__(self):
        self.results = {}
        self.validation_dir = Path('validation_results')
        self.validation_dir.mkdir(exist_ok=True)

    def run_comprehensive_validation(self, output_file: str = None) -> Dict[str, Any]:
        """
        Run all validation checks and return comprehensive results.

        Args:
            output_file: Optional file to save results to

        Returns:
            Dictionary containing all validation results
        """
        logger.info("Running comprehensive system validation...")

        self.results = {
            'timestamp': self._get_timestamp(),
            'validations': {}
        }

        # Run all validation checks
        self.results['validations']['ssot_compliance'] = self._run_ssot_compliance_check()
        self.results['validations']['v2_compliance'] = self._run_v2_compliance_check()
        self.results['validations']['integration_status'] = self._run_integration_check()
        self.results['validations']['service_readiness'] = self._run_service_readiness_check()
        self.results['validations']['code_quality'] = self._run_code_quality_check()

        # Calculate overall status
        self.results['overall_status'] = self._calculate_overall_status()

        # Save results if requested
        if output_file:
            self._save_results(output_file)

        logger.info(f"Comprehensive validation completed. Status: {self.results['overall_status']}")
        return self.results

    def run_ssot_validation(self, output_file: str = None) -> Dict[str, Any]:
        """Run SSOT compliance validation only."""
        result = self._run_ssot_compliance_check()
        if output_file:
            self._save_results(output_file, {'ssot_compliance': result})
        return result

    def run_v2_validation(self, output_file: str = None) -> Dict[str, Any]:
        """Run V2 compliance validation only."""
        result = self._run_v2_compliance_check()
        if output_file:
            self._save_results(output_file, {'v2_compliance': result})
        return result

    def run_integration_validation(self, output_file: str = None) -> Dict[str, Any]:
        """Run integration status validation only."""
        result = self._run_integration_check()
        if output_file:
            self._save_results(output_file, {'integration_status': result})
        return result

    def run_service_validation(self, output_file: str = None) -> Dict[str, Any]:
        """Run service readiness validation only."""
        result = self._run_service_readiness_check()
        if output_file:
            self._save_results(output_file, {'service_readiness': result})
        return result

    def _run_ssot_compliance_check(self) -> Dict[str, Any]:
        """Run SSOT compliance validation."""
        try:
            from tools.unified_validator import SSOTValidator
            validator = SSOTValidator()
            return validator.validate_all_files()
        except Exception as e:
            logger.error(f"SSOT validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_v2_compliance_check(self) -> Dict[str, Any]:
        """Run V2 compliance validation."""
        try:
            from tools.unified_validation_tools_manager import ValidationManager
            manager = ValidationManager()
            return manager.validate_v2_compliance()
        except Exception as e:
            logger.error(f"V2 compliance validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_integration_check(self) -> Dict[str, Any]:
        """Run integration status validation."""
        try:
            from tools.unified_validation_tools_manager import ValidationManager
            manager = ValidationManager()
            return manager.check_integration_status()
        except Exception as e:
            logger.error(f"Integration validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_service_readiness_check(self) -> Dict[str, Any]:
        """Run service readiness validation."""
        try:
            from tools.unified_validation_tools_manager import ValidationManager
            manager = ValidationManager()
            return manager.check_service_readiness()
        except Exception as e:
            logger.error(f"Service readiness validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_code_quality_check(self) -> Dict[str, Any]:
        """Run code quality validation."""
        try:
            # Run basic linting checks
            import subprocess
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', 'src/'],
                capture_output=True,
                text=True,
                cwd='.'
            )

            if result.returncode == 0:
                return {'status': 'PASS', 'message': 'No syntax errors found'}
            else:
                return {
                    'status': 'FAIL',
                    'message': 'Syntax errors detected',
                    'details': result.stderr
                }
        except Exception as e:
            logger.error(f"Code quality check failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _calculate_overall_status(self) -> str:
        """Calculate overall validation status."""
        validations = self.results.get('validations', {})

        # Check if any critical validations failed
        critical_failures = 0
        for validation_name, result in validations.items():
            status = result.get('status', 'UNKNOWN')
            if status in ['FAIL', 'ERROR']:
                if validation_name in ['ssot_compliance', 'v2_compliance', 'integration_status']:
                    critical_failures += 1

        if critical_failures > 0:
            return 'SYSTEM ISSUES DETECTED'
        elif all(result.get('status') == 'PASS' for result in validations.values()):
            return 'ALL SYSTEMS OPERATIONAL'
        else:
            return 'MINOR ISSUES DETECTED'

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()

    def _save_results(self, filename: str, results: Dict[str, Any] = None):
        """Save validation results to file."""
        if results is None:
            results = self.results

        output_path = self.validation_dir / filename
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Validation results saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save validation results: {e}")

def run_validation_command(args: List[str]) -> int:
    """
    Run validation from command line arguments.

    Args:
        args: Command line arguments

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    runner = ValidationRunner()

    if '--comprehensive' in args or len(args) == 0:
        # Run comprehensive validation
        output_file = 'comprehensive_validation.json'
        if '--output' in args:
            idx = args.index('--output')
            if idx + 1 < len(args):
                output_file = args[idx + 1]

        results = runner.run_comprehensive_validation(output_file)
        status = results.get('overall_status', 'UNKNOWN')

        print(f"📊 Comprehensive Validation Status: {status}")
        for validation_name, result in results.get('validations', {}).items():
            val_status = result.get('status', 'UNKNOWN')
            print(f"🔍 {validation_name}: {val_status}")

        return 0 if 'OPERATIONAL' in status else 1

    elif '--ssot' in args:
        output_file = args[args.index('--output')] if '--output' in args else 'ssot_validation.json'
        result = runner.run_ssot_validation(output_file)
        print(f"🔍 SSOT Compliance: {result.get('status', 'UNKNOWN')}")
        return 0 if result.get('status') == 'PASS' else 1

    elif '--v2' in args:
        output_file = args[args.index('--output')] if '--output' in args else 'v2_validation.json'
        result = runner.run_v2_validation(output_file)
        print(f"📋 V2 Compliance: {result.get('status', 'UNKNOWN')}")
        return 0 if result.get('status') == 'PASS' else 1

    elif '--integration' in args:
        output_file = args[args.index('--output')] if '--output' in args else 'integration_validation.json'
        result = runner.run_integration_validation(output_file)
        print(f"🔗 Integration Status: {result.get('status', 'UNKNOWN')}")
        return 0 if result.get('status') == 'PASS' else 1

    elif '--service' in args:
        output_file = args[args.index('--output')] if '--output' in args else 'service_validation.json'
        result = runner.run_service_validation(output_file)
        print(f"🚀 Service Readiness: {result.get('status', 'UNKNOWN')}")
        return 0 if result.get('status') == 'PASS' else 1

    else:
        print("Usage: python -m src.cli.validation_runner [--comprehensive|--ssot|--v2|--integration|--service] [--output filename]")
        return 1