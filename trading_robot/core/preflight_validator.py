"""
Pre-Flight Validation System for Trading Robot
Validates all systems before allowing trading operations
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger

from config.settings import config
from .broker_interface import BrokerInterface
from .broker_factory import create_broker_client


class PreFlightValidator:
    """Pre-flight validation system for trading readiness"""

    def __init__(self, broker_client: Optional[BrokerInterface] = None):
        self.broker_client = broker_client or create_broker_client()
        self.validation_results: Dict[str, Any] = {}
        self.validation_timestamp: Optional[datetime] = None

    async def validate_all(self) -> tuple[bool, Dict[str, Any]]:
        """Run all pre-flight validation checks."""
        broker_name = config.broker.upper()
        logger.info(f"🔍 Starting pre-flight validation checks for {broker_name}...")

        self.validation_timestamp = datetime.now()
        all_passed = True
        results = {
            "timestamp": self.validation_timestamp.isoformat(),
            "broker": broker_name,
            "checks": {},
            "overall_status": "PENDING",
            "errors": [],
            "warnings": [],
        }

        # Configuration validation
        config_valid, config_errors = self._validate_configuration()
        results["checks"]["configuration"] = {
            "status": "PASS" if config_valid else "FAIL",
            "errors": config_errors,
        }
        if not config_valid:
            all_passed = False
            results["errors"].extend(config_errors)

        # API connectivity validation
        api_valid, api_errors = await self._validate_api_connectivity()
        results["checks"]["api_connectivity"] = {
            "status": "PASS" if api_valid else "FAIL",
            "errors": api_errors,
        }
        if not api_valid:
            all_passed = False
            results["errors"].extend(api_errors)

        # Account validation
        account_valid, account_errors, account_warnings = await self._validate_account()
        results["checks"]["account"] = {
            "status": "PASS" if account_valid else "FAIL",
            "errors": account_errors,
            "warnings": account_warnings,
        }
        if not account_valid:
            all_passed = False
            results["errors"].extend(account_errors)
        results["warnings"].extend(account_warnings)

        # Risk limits validation
        risk_valid, risk_errors = self._validate_risk_limits()
        results["checks"]["risk_limits"] = {
            "status": "PASS" if risk_valid else "FAIL",
            "errors": risk_errors,
        }
        if not risk_valid:
            all_passed = False
            results["errors"].extend(risk_errors)

        # Emergency stop validation
        emergency_valid, emergency_errors = self._validate_emergency_stop()
        results["checks"]["emergency_stop"] = {
            "status": "PASS" if emergency_valid else "FAIL",
            "errors": emergency_errors,
        }
        if not emergency_valid:
            all_passed = False
            results["errors"].extend(emergency_errors)

        # Live trading specific checks
        if config.is_live_trading():
            live_valid, live_errors, live_warnings = await self._validate_live_trading()
            results["checks"]["live_trading"] = {
                "status": "PASS" if live_valid else "FAIL",
                "errors": live_errors,
                "warnings": live_warnings,
            }
            if not live_valid:
                all_passed = False
                results["errors"].extend(live_errors)
            results["warnings"].extend(live_warnings)

        # Set overall status
        if all_passed:
            results["overall_status"] = "PASS"
            logger.info("✅ All pre-flight validation checks PASSED")
        else:
            results["overall_status"] = "FAIL"
            logger.error(f"❌ Pre-flight validation FAILED: {len(results['errors'])} errors")

        self.validation_results = results
        return all_passed, results

    def _validate_configuration(self) -> tuple[bool, List[str]]:
        """Validate configuration settings."""
        errors = []
        try:
            is_valid, config_errors = config.validate_config()
            if not is_valid:
                errors.extend(config_errors)
            return len(errors) == 0, errors
        except Exception as e:
            errors.append(f"Configuration validation error: {str(e)}")
            return False, errors

    async def _validate_api_connectivity(self) -> tuple[bool, List[str]]:
        """Validate broker API connectivity."""
        errors = []
        broker_name = config.broker.upper()
        try:
            if not self.broker_client.is_connected():
                try:
                    if not self.broker_client.connect():
                        errors.append(f"Failed to connect to {broker_name} API")
                        return False, errors
                except Exception as e:
                    errors.append(f"Failed to connect to {broker_name} API: {str(e)}")
                    return False, errors

            # Test API call
            try:
                clock = self.broker_client.get_market_clock()
                if not clock:
                    errors.append(f"{broker_name} market clock API call failed")
            except Exception as e:
                errors.append(f"{broker_name} API connectivity test failed: {str(e)}")

            return len(errors) == 0, errors
        except Exception as e:
            errors.append(f"{broker_name} API connectivity validation error: {str(e)}")
            return False, errors

    async def _validate_account(self) -> tuple[bool, List[str], List[str]]:
        """Validate broker account status."""
        errors = []
        warnings = []
        broker_name = config.broker.upper()

        try:
            if not self.broker_client.is_connected():
                errors.append(f"{broker_name} client not connected")
                return False, errors, warnings

            account_info = self.broker_client.get_account_info()
            if not account_info:
                errors.append("Failed to retrieve account information")
                return False, errors, warnings

            # Check account status
            account_status = account_info.get("status", "").lower()
            if account_status not in ["active", "approved"]:
                errors.append(f"Account status is not active: {account_status}")

            # Check account balance
            cash = account_info.get("cash", 0.0)
            portfolio_value = account_info.get("portfolio_value", 0.0)

            if cash <= 0:
                warnings.append(f"Account cash balance is ${cash:.2f}")

            if portfolio_value <= 0:
                warnings.append(f"Portfolio value is ${portfolio_value:.2f}")

            # Check buying power
            buying_power = account_info.get("buying_power", 0.0)
            if buying_power <= 0:
                warnings.append(f"Buying power is ${buying_power:.2f}")

            return len(errors) == 0, errors, warnings
        except Exception as e:
            errors.append(f"Account validation error: {str(e)}")
            return False, errors, warnings

    def _validate_risk_limits(self) -> tuple[bool, List[str]]:
        """Validate risk management limits are properly configured."""
        errors = []

        # Check daily loss limit
        if config.daily_loss_limit_pct <= 0:
            errors.append("DAILY_LOSS_LIMIT_PCT must be greater than 0")

        # Check position size limits
        if config.max_position_size_pct <= 0 or config.max_position_size_pct > 1.0:
            errors.append("MAX_POSITION_SIZE_PCT must be between 0 and 1.0")

        # Check order value limits
        if config.min_order_value <= 0:
            errors.append("MIN_ORDER_VALUE must be greater than 0")
        if config.max_order_value <= config.min_order_value:
            errors.append("MAX_ORDER_VALUE must be greater than MIN_ORDER_VALUE")

        # Check daily trade limits
        if config.max_daily_trades <= 0:
            errors.append("MAX_DAILY_TRADES must be greater than 0")

        # Check emergency stop configuration
        if config.emergency_stop_enabled:
            if config.emergency_stop_loss_pct <= 0:
                errors.append("EMERGENCY_STOP_LOSS_PCT must be greater than 0")

        return len(errors) == 0, errors

    def _validate_emergency_stop(self) -> tuple[bool, List[str]]:
        """Validate emergency stop mechanism."""
        errors = []

        if not config.emergency_stop_enabled:
            errors.append("Emergency stop is not enabled. Enable for safety.")

        if config.emergency_stop_loss_pct <= 0:
            errors.append("Emergency stop loss percentage must be greater than 0")

        if config.emergency_stop_loss_pct > 0.5:
            errors.append(
                f"Emergency stop loss percentage ({config.emergency_stop_loss_pct}) "
                "is too high. Recommended: 0.1 (10%) or less."
            )

        return len(errors) == 0, errors

    async def _validate_live_trading(self) -> tuple[bool, List[str], List[str]]:
        """Validate live trading specific requirements."""
        errors = []
        warnings = []

        # Verify live trading is explicitly enabled
        if not config.live_trading_enabled:
            errors.append("LIVE_TRADING_ENABLED must be true for live trading")

        # Verify API URL is for live trading (Alpaca specific)
        if config.broker == "alpaca" and "paper-api" in config.alpaca_base_url:
            errors.append(
                "Live trading mode requires live API URL. "
                "Current URL points to paper trading API."
            )

        # Warnings for live trading
        warnings.append("⚠️ LIVE TRADING MODE: Real money at risk!")
        warnings.append("⚠️ Ensure all risk limits are properly configured")
        warnings.append("⚠️ Monitor closely during initial trading period")
        warnings.append("⚠️ Start with minimal position sizes")

        return len(errors) == 0, errors, warnings

    def get_validation_report(self) -> str:
        """Generate human-readable validation report."""
        if not self.validation_results:
            return "No validation results available. Run validate_all() first."

        results = self.validation_results
        report_lines = [
            "=" * 60,
            "PRE-FLIGHT VALIDATION REPORT",
            "=" * 60,
            f"Broker: {results.get('broker', 'UNKNOWN')}",
            f"Timestamp: {results['timestamp']}",
            f"Overall Status: {results['overall_status']}",
            "",
        ]

        # Check results
        for check_name, check_result in results["checks"].items():
            status = check_result["status"]
            status_icon = "✅" if status == "PASS" else "❌"
            report_lines.append(f"{status_icon} {check_name.upper()}: {status}")

            if check_result.get("errors"):
                for error in check_result["errors"]:
                    report_lines.append(f"   ❌ Error: {error}")

            if check_result.get("warnings"):
                for warning in check_result["warnings"]:
                    report_lines.append(f"   ⚠️  Warning: {warning}")

        # Summary
        report_lines.extend([
            "",
            "=" * 60,
            "SUMMARY",
            "=" * 60,
            f"Total Errors: {len(results['errors'])}",
            f"Total Warnings: {len(results['warnings'])}",
        ])

        if results["errors"]:
            report_lines.append("")
            report_lines.append("ERRORS:")
            for error in results["errors"]:
                report_lines.append(f"  - {error}")

        if results["warnings"]:
            report_lines.append("")
            report_lines.append("WARNINGS:")
            for warning in results["warnings"]:
                report_lines.append(f"  - {warning}")

        return "\n".join(report_lines)

    def can_proceed_with_trading(self) -> bool:
        """Check if trading can proceed based on validation results."""
        if not self.validation_results:
            return False
        return self.validation_results["overall_status"] == "PASS"


# Factory function
def create_preflight_validator(
    broker_client: Optional[BrokerInterface] = None,
) -> PreFlightValidator:
    """Factory function to create pre-flight validator."""
    return PreFlightValidator(broker_client)







