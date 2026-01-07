"""
Setup Wizard V2 - Agent Cellphone V2
====================================

SSOT Domain: core

Refactored interactive setup wizard using service architecture.

Features:
- Interactive configuration
- Environment validation
- Service setup
- Configuration management

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

from src.setup.setup_service import (
    setup_service,
    SetupConfig,
    ServiceConfig
)

class SetupWizard:
    """
    Interactive setup wizard for configuring dream.os.
    """

    def __init__(self):
        self.setup_service = setup_service
        self.config = self.setup_service.load_config()

    def run_interactive_setup(self) -> None:
        """Run interactive setup wizard."""
        print("🐝 dream.os Setup Wizard")
        print("=" * 50)

        # Environment setup
        print("\n1. Environment Configuration")
        self.config.environment = self._prompt_choice(
            "Select environment",
            ["development", "staging", "production"],
            default="development"
        )

        # Discord setup
        print("\n2. Discord Configuration")
        self.config.discord_bot_token = self._prompt_secret("Discord Bot Token")
        self.config.discord_guild_id = self._prompt_input("Discord Guild/Server ID")
        self.config.discord_channel_id = self._prompt_input("Discord Channel ID (optional)")

        # Service configuration
        print("\n3. Service Configuration")
        services = ["discord_bot", "fastapi", "message_queue", "database"]

        for service_name in services:
            if self._prompt_yes_no(f"Enable {service_name} service?", default=True):
                self.config.services[service_name].enabled = True
                self.config.services[service_name].auto_start = self._prompt_yes_no(
                    f"Auto-start {service_name} on boot?", default=True
                )

        # Database setup (if enabled)
        if self.config.services["database"].enabled:
            print("\n4. Database Configuration")
            self.config.database_url = self._prompt_input("Database URL")
            self.config.database_enabled = bool(self.config.database_url)

        # API configuration
        print("\n5. API Configuration")
        self.config.api_host = self._prompt_input("API Host", default="localhost")
        self.config.api_port = int(self._prompt_input("API Port", default="8001"))

        # Logging configuration
        print("\n6. Logging Configuration")
        self.config.log_level = self._prompt_choice(
            "Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO"
        )

        # Save configuration
        self._save_configuration()

        print("\n✅ Setup complete! Run validation to verify configuration.")

    def run_validation(self) -> bool:
        """
        Validate current configuration.

        Returns:
            True if configuration is valid
        """
        print("🔍 Validating configuration...")

        # Environment validation
        env_valid, env_issues = self.setup_service.validate_environment()
        if not env_valid:
            print("❌ Environment issues:")
            for issue in env_issues:
                print(f"  • {issue}")
            return False

        # Service dependency validation
        service_issues = self.setup_service.validate_service_dependencies(self.config)
        if service_issues:
            print("❌ Service dependency issues:")
            for service, issues in service_issues.items():
                print(f"  • {service}: {', '.join(issues)}")
            return False

        print("✅ Configuration validation passed!")
        return True

    def run_reset(self) -> None:
        """Reset configuration to defaults."""
        print("⚠️  This will reset all configuration to defaults.")
        if self._prompt_yes_no("Are you sure you want to continue?", default=False):
            if self.setup_service.reset_configuration():
                print("✅ Configuration reset successfully!")
                self.config = SetupConfig()
            else:
                print("❌ Failed to reset configuration.")
        else:
            print("❌ Reset cancelled.")

    def _save_configuration(self) -> None:
        """Save current configuration."""
        try:
            self.setup_service.save_config(self.config)
            self.setup_service.setup_environment_variables(self.config)
            print("💾 Configuration saved successfully!")
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")

    def _prompt_input(self, prompt: str, default: str = "", password: bool = False) -> str:
        """Prompt user for input."""
        suffix = f" (default: {default})" if default else ""
        if password:
            import getpass
            try:
                value = getpass.getpass(f"{prompt}{suffix}: ")
            except:
                # Fallback for environments without getpass
                value = input(f"{prompt}{suffix}: ")
        else:
            value = input(f"{prompt}{suffix}: ")

        return value.strip() or default

    def _prompt_secret(self, prompt: str) -> Optional[str]:
        """Prompt for secret input."""
        return self._prompt_input(prompt, password=True)

    def _prompt_choice(self, prompt: str, choices: list, default: str = None) -> str:
        """Prompt user to choose from options."""
        print(f"\n{prompt}:")
        for i, choice in enumerate(choices, 1):
            marker = "→" if choice == default else " "
            print(f"  {marker} {i}. {choice}")

        while True:
            try:
                choice_input = input("Enter choice (number): ").strip()
                if not choice_input and default:
                    return default

                choice_idx = int(choice_input) - 1
                if 0 <= choice_idx < len(choices):
                    return choices[choice_idx]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def _prompt_yes_no(self, prompt: str, default: bool = None) -> bool:
        """Prompt for yes/no answer."""
        default_text = "(y/N)" if default is False else "(Y/n)" if default is True else "(y/n)"

        while True:
            response = input(f"{prompt} {default_text}: ").strip().lower()

            if not response:
                if default is not None:
                    return default
                continue

            if response in ['y', 'yes', 'true', '1']:
                return True
            elif response in ['n', 'no', 'false', '0']:
                return False
            else:
                print("Please answer yes (y) or no (n).")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="dream.os Setup Wizard")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate existing configuration"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset configuration to defaults"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run non-interactive setup with defaults"
    )

    args = parser.parse_args()

    try:
        wizard = SetupWizard()

        if args.validate:
            success = wizard.run_validation()
            sys.exit(0 if success else 1)

        elif args.reset:
            wizard.run_reset()

        elif args.non_interactive:
            # Non-interactive setup with defaults
            wizard.config = SetupConfig()
            wizard._save_configuration()
            print("✅ Non-interactive setup complete with defaults!")

        else:
            # Interactive setup
            wizard.run_interactive_setup()

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()