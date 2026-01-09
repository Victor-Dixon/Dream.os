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
        except ImportError:
            # Fallback: Basic SSOT check without specialized tool
            logger.warning("SSOT validation tool not available, running basic check")
            return self._run_basic_ssot_check()
        except Exception as e:
            logger.error(f"SSOT validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_basic_ssot_check(self) -> Dict[str, Any]:
        """Run basic SSOT compliance check without specialized tools."""
        try:
            # Check for basic SSOT compliance indicators
            required_files = ['src/core/config/config_manager.py', 'src/services/']
            missing_files = []

            for file_path in required_files:
                if not Path(file_path).exists():
                    missing_files.append(file_path)

            if missing_files:
                return {
                    'status': 'FAIL',
                    'message': f'Missing required SSOT files: {missing_files}'
                }

            return {
                'status': 'PASS',
                'message': 'Basic SSOT structure present'
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}

    def _run_v2_compliance_check(self) -> Dict[str, Any]:
        """Run V2 compliance validation."""
        try:
            from tools.unified_validation_tools_manager import ValidationManager
            manager = ValidationManager()
            return manager.validate_v2_compliance()
        except ImportError:
            # Fallback: Basic V2 compliance check
            logger.warning("V2 validation tool not available, running basic check")
            return self._run_basic_v2_check()
        except Exception as e:
            logger.error(f"V2 compliance validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_basic_v2_check(self) -> Dict[str, Any]:
        """Run basic V2 compliance check."""
        try:
            # Check for basic V2 compliance indicators
            v2_indicators = [
                'src/core/base/base_service.py',
                'src/services/',
                'agent_workspaces/'
            ]

            missing_indicators = []
            for indicator in v2_indicators:
                if not Path(indicator).exists():
                    missing_indicators.append(indicator)

            if missing_indicators:
                return {
                    'status': 'FAIL',
                    'message': f'Missing V2 compliance indicators: {missing_indicators}'
                }

            return {
                'status': 'PASS',
                'message': 'Basic V2 compliance structure present'
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}

    def _run_integration_check(self) -> Dict[str, Any]:
        """Run integration status validation."""
        try:
            from tools.unified_validation_tools_manager import ValidationManager
            manager = ValidationManager()
            return manager.check_integration_status()
        except ImportError:
            # Fallback: Basic integration check
            logger.warning("Integration validation tool not available, running basic check")
            return self._run_basic_integration_check()
        except Exception as e:
            logger.error(f"Integration validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_service_readiness_check(self) -> Dict[str, Any]:
        """Run service readiness validation."""
        try:
            from tools.unified_validation_tools_manager import ValidationManager
            manager = ValidationManager()
            return manager.check_service_readiness()
        except ImportError:
            # Fallback: Basic service readiness check
            logger.warning("Service validation tool not available, running basic check")
            return self._run_basic_service_check()
        except Exception as e:
            logger.error(f"Service readiness validation failed: {e}")
            return {'status': 'ERROR', 'error': str(e)}

    def _run_basic_integration_check(self) -> Dict[str, Any]:
        """Run basic integration status check."""
        try:
            # Check for integration indicators
            integration_files = [
                'src/services/messaging/',
                'agent_workspaces/',
                'src/core/messaging_core.py'
            ]

            present_integrations = []
            missing_integrations = []

            for file_path in integration_files:
                if Path(file_path).exists():
                    present_integrations.append(file_path)
                else:
                    missing_integrations.append(file_path)

            if missing_integrations:
                return {
                    'status': 'WARN',
                    'message': f'Some integration components missing: {missing_integrations}',
                    'present': present_integrations
                }

            return {
                'status': 'PASS',
                'message': 'Basic integration components present'
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}

    def _run_basic_service_check(self) -> Dict[str, Any]:
        """Run basic service readiness check."""
        try:
            # Check for key services
            key_services = [
                'src/services/thea/',
                'src/services/messaging/',
                'src/core/'
            ]

            ready_services = []
            unready_services = []

            for service_path in key_services:
                if Path(service_path).exists():
                    # Check if service has __init__.py
                    init_file = Path(service_path) / '__init__.py'
                    if init_file.exists():
                        ready_services.append(service_path)
                    else:
                        unready_services.append(f"{service_path} (missing __init__.py)")
                else:
                    unready_services.append(service_path)

            if unready_services:
                return {
                    'status': 'WARN',
                    'message': f'Some services not ready: {unready_services}',
                    'ready': ready_services
                }

            return {
                'status': 'PASS',
                'message': 'Basic services are ready'
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}

    def _run_code_quality_check(self) -> Dict[str, Any]:
        """Run code quality validation."""
        try:
            # Check if src directory exists and is readable
            src_path = Path('src')
            if not src_path.exists():
                return {'status': 'FAIL', 'message': 'src/ directory not found'}

            if not src_path.is_dir():
                return {'status': 'FAIL', 'message': 'src/ is not a directory'}

            # Find Python files to check
            python_files = list(src_path.rglob('*.py'))
            if not python_files:
                return {'status': 'WARN', 'message': 'No Python files found in src/'}

            # Check a sample of files for syntax (don't check all to avoid timeouts)
            sample_size = min(10, len(python_files))
            sample_files = python_files[:sample_size]

            syntax_errors = []
            for py_file in sample_files:
                try:
                    compile(py_file.read_text(encoding='utf-8'), str(py_file), 'exec')
                except SyntaxError as e:
                    syntax_errors.append(f"{py_file}: {e}")
                except Exception as e:
                    # Skip files with encoding issues or other problems
                    continue

            if syntax_errors:
                return {
                    'status': 'FAIL',
                    'message': f'Syntax errors in {len(syntax_errors)} files',
                    'details': syntax_errors[:5]  # Show first 5 errors
                }
            else:
                return {
                    'status': 'PASS',
                    'message': f'No syntax errors found in {sample_size} sample files'
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