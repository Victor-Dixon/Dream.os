#!/usr/bin/env python3
"""
dream.os Setup Wizard
=====================

Interactive setup wizard for configuring dream.os.
Helps users configure environment variables, services, and settings.

Usage:
    python setup_wizard.py          # Interactive setup
    python setup_wizard.py --validate  # Validate existing config
    python setup_wizard.py --reset     # Reset configuration

V2 Compliance: <400 lines
Author: Agent-2 (Architecture & Design Specialist)
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import argparse

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv, set_key

# Load existing environment
load_dotenv()

@dataclass
class ServiceConfig:
    """Service configuration settings."""
    enabled: bool = False
    auto_start: bool = False
    config_valid: bool = False
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class SetupConfig:
    """Complete setup configuration."""
    # Environment settings
    environment: str = "development"
    debug_mode: bool = False
    log_level: str = "INFO"

    # API Keys and Tokens
    discord_token: Optional[str] = None
    twitch_token: Optional[str] = None
    twitch_channel: Optional[str] = None
    twitch_username: Optional[str] = None
    openai_api_key: Optional[str] = None

    # Database settings
    database_url: Optional[str] = None
    redis_url: Optional[str] = None

    # Web settings
    fastapi_port: int = 8001
    flask_port: int = 5000
    web_host: str = "localhost"
    cors_origins: List[str] = None

    # Service configurations
    services: Dict[str, ServiceConfig] = None

    # Advanced settings
    max_workers: int = 4
    request_timeout: int = 30
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:3000", "http://localhost:5000"]

        if self.services is None:
            self.services = {
                "message_queue": ServiceConfig(enabled=True, auto_start=True),
                "discord_bot": ServiceConfig(enabled=False, auto_start=False, dependencies=["discord_token"]),
                "twitch_bot": ServiceConfig(enabled=False, auto_start=False, dependencies=["twitch_token", "twitch_channel"]),
                "fastapi_service": ServiceConfig(enabled=True, auto_start=True),
                "web_server": ServiceConfig(enabled=True, auto_start=True),
                "auto_gas_pipeline": ServiceConfig(enabled=False, auto_start=False),
            }

class SetupWizard:
    """Interactive setup wizard for dream.os."""

    def __init__(self):
        self.config = SetupConfig()
        self.env_file = project_root / ".env"
        self.config_file = project_root / "setup_config.json"

        # Load existing configuration
        self.load_existing_config()

    def load_existing_config(self):
        """Load existing configuration from files."""
        # Load from .env file
        if self.env_file.exists():
            load_dotenv(self.env_file)

            # Update config with existing env values
            self.config.discord_token = os.getenv("DISCORD_TOKEN")
            self.config.twitch_token = os.getenv("TWITCH_ACCESS_TOKEN")
            self.config.twitch_channel = os.getenv("TWITCH_CHANNEL")
            self.config.twitch_username = os.getenv("TWITCH_BOT_USERNAME")
            self.config.openai_api_key = os.getenv("OPENAI_API_KEY")
            self.config.database_url = os.getenv("DATABASE_URL")
            self.config.redis_url = os.getenv("REDIS_URL")
            self.config.fastapi_port = int(os.getenv("FASTAPI_PORT", "8001"))
            self.config.flask_port = int(os.getenv("FLASK_PORT", "5000"))
            self.config.web_host = os.getenv("WEB_HOST", "localhost")

        # Load from config file
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    # Update config with saved settings
                    for key, value in data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
            except Exception as e:
                print(f"⚠️  Warning: Could not load existing config: {e}")

    def save_config(self):
        """Save configuration to files."""
        # Save to .env file
        self.save_env_file()

        # Save to config file
        config_dict = asdict(self.config)
        # Remove sensitive data from JSON config
        config_dict.pop('discord_token', None)
        config_dict.pop('twitch_token', None)
        config_dict.pop('openai_api_key', None)

        with open(self.config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)

        print("✅ Configuration saved successfully!")

    def save_env_file(self):
        """Save environment variables to .env file."""
        env_vars = {
            "ENV": self.config.environment,
            "DEBUG": str(self.config.debug_mode).lower(),
            "LOG_LEVEL": self.config.log_level,
            "DISCORD_TOKEN": self.config.discord_token or "",
            "TWITCH_ACCESS_TOKEN": self.config.twitch_token or "",
            "TWITCH_CHANNEL": self.config.twitch_channel or "",
            "TWITCH_BOT_USERNAME": self.config.twitch_username or "",
            "OPENAI_API_KEY": self.config.openai_api_key or "",
            "DATABASE_URL": self.config.database_url or "",
            "REDIS_URL": self.config.redis_url or "",
            "FASTAPI_PORT": str(self.config.fastapi_port),
            "FLASK_PORT": str(self.config.flask_port),
            "WEB_HOST": self.config.web_host,
            "CORS_ORIGINS": ",".join(self.config.cors_origins),
            "MAX_WORKERS": str(self.config.max_workers),
            "REQUEST_TIMEOUT": str(self.config.request_timeout),
            "RATE_LIMIT_REQUESTS": str(self.config.rate_limit_requests),
            "RATE_LIMIT_WINDOW": str(self.config.rate_limit_window),
        }

        # Create or update .env file
        if not self.env_file.exists():
            self.env_file.touch()

        for key, value in env_vars.items():
            set_key(str(self.env_file), key, value)

    def validate_config(self) -> Tuple[bool, List[str]]:
        """Validate current configuration."""
        issues = []

        # Check required API keys for enabled services
        if self.config.services["discord_bot"].enabled and not self.config.discord_token:
            issues.append("❌ Discord bot enabled but DISCORD_TOKEN not set")

        if self.config.services["twitch_bot"].enabled:
            if not self.config.twitch_token:
                issues.append("❌ Twitch bot enabled but TWITCH_ACCESS_TOKEN not set")
            if not self.config.twitch_channel:
                issues.append("❌ Twitch bot enabled but TWITCH_CHANNEL not set")

        # Check port conflicts
        if self.config.fastapi_port == self.config.flask_port:
            issues.append(f"❌ Port conflict: FastAPI ({self.config.fastapi_port}) and Flask ({self.config.flask_port}) use same port")

        # Check URL formats
        if self.config.database_url and not self.config.database_url.startswith(('sqlite://', 'postgresql://', 'mysql://')):
            issues.append("⚠️  DATABASE_URL format may be invalid")

        if self.config.redis_url and not self.config.redis_url.startswith(('redis://', 'rediss://')):
            issues.append("⚠️  REDIS_URL format may be invalid")

        return len(issues) == 0, issues

    def run_interactive_setup(self):
        """Run interactive setup wizard."""
        print("🤖 dream.os Setup Wizard")
        print("=" * 50)
        print()

        # Environment settings
        self.configure_environment()

        # API Keys
        self.configure_api_keys()

        # Services
        self.configure_services()

        # Network settings
        self.configure_network()

        # Advanced settings
        self.configure_advanced()

        # Validate and save
        self.finalize_setup()

    def configure_environment(self):
        """Configure environment settings."""
        print("🌍 Environment Configuration")
        print("-" * 30)

        environments = ["development", "staging", "production"]
        for i, env in enumerate(environments, 1):
            print(f"{i}. {env.capitalize()}")

        while True:
            try:
                choice = input(f"Select environment (1-{len(environments)}) [{environments.index(self.config.environment) + 1}]: ").strip()
                if not choice:
                    break
                choice = int(choice) - 1
                if 0 <= choice < len(environments):
                    self.config.environment = environments[choice]
                    break
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a number")

        # Debug mode
        debug_choice = input(f"Enable debug mode? (y/n) [{'y' if self.config.debug_mode else 'n'}]: ").strip().lower()
        self.config.debug_mode = debug_choice in ('y', 'yes', 'true', '1')

        print()

    def configure_api_keys(self):
        """Configure API keys and tokens."""
        print("🔑 API Keys & Tokens Configuration")
        print("-" * 35)

        # Discord
        if not self.config.discord_token:
            self.config.discord_token = input("Discord Bot Token (leave empty to skip): ").strip()
        else:
            update = input("Update Discord Bot Token? (y/n) [n]: ").strip().lower()
            if update in ('y', 'yes'):
                self.config.discord_token = input("Discord Bot Token: ").strip()

        # Twitch
        if not self.config.twitch_token:
            self.config.twitch_token = input("Twitch Access Token (leave empty to skip): ").strip()
        else:
            update = input("Update Twitch Access Token? (y/n) [n]: ").strip().lower()
            if update in ('y', 'yes'):
                self.config.twitch_token = input("Twitch Access Token: ").strip()

        if not self.config.twitch_channel:
            self.config.twitch_channel = input("Twitch Channel Name (leave empty to skip): ").strip()
        else:
            update = input("Update Twitch Channel? (y/n) [n]: ").strip().lower()
            if update in ('y', 'yes'):
                self.config.twitch_channel = input("Twitch Channel Name: ").strip()

        if not self.config.twitch_username:
            self.config.twitch_username = input("Twitch Bot Username (leave empty to use channel name): ").strip()
        else:
            update = input("Update Twitch Bot Username? (y/n) [n]: ").strip().lower()
            if update in ('y', 'yes'):
                self.config.twitch_username = input("Twitch Bot Username: ").strip()

        # OpenAI (optional)
        if not self.config.openai_api_key:
            self.config.openai_api_key = input("OpenAI API Key (leave empty to skip): ").strip()
        else:
            update = input("Update OpenAI API Key? (y/n) [n]: ").strip().lower()
            if update in ('y', 'yes'):
                self.config.openai_api_key = input("OpenAI API Key: ").strip()

        print()

    def configure_services(self):
        """Configure which services to enable."""
        print("⚙️  Service Configuration")
        print("-" * 25)

        services = [
            ("message_queue", "Message Queue Service"),
            ("discord_bot", "Discord Bot"),
            ("twitch_bot", "Twitch Bot"),
            ("fastapi_service", "FastAPI Service"),
            ("web_server", "Web Server (Flask)"),
            ("auto_gas_pipeline", "Auto Gas Pipeline"),
        ]

        for service_key, service_name in services:
            service_config = self.config.services[service_key]

            # Check dependencies
            can_enable = True
            missing_deps = []
            for dep in service_config.dependencies:
                if not getattr(self.config, dep, None):
                    can_enable = False
                    missing_deps.append(dep)

            if not can_enable and missing_deps:
                print(f"⚠️  {service_name}: Disabled (missing: {', '.join(missing_deps)})")
                service_config.enabled = False
            else:
                enabled = input(f"Enable {service_name}? (y/n) [{'y' if service_config.enabled else 'n'}]: ").strip().lower()
                service_config.enabled = enabled in ('y', 'yes', 'true', '1')

                if service_config.enabled:
                    auto_start = input(f"Auto-start {service_name}? (y/n) [{'y' if service_config.auto_start else 'n'}]: ").strip().lower()
                    service_config.auto_start = auto_start in ('y', 'yes', 'true', '1')

        print()

    def configure_network(self):
        """Configure network settings."""
        print("🌐 Network Configuration")
        print("-" * 25)

        # Ports
        try:
            fastapi_port = input(f"FastAPI Port [{self.config.fastapi_port}]: ").strip()
            if fastapi_port:
                self.config.fastapi_port = int(fastapi_port)
        except ValueError:
            print("❌ Invalid port number")

        try:
            flask_port = input(f"Flask Port [{self.config.flask_port}]: ").strip()
            if flask_port:
                self.config.flask_port = int(flask_port)
        except ValueError:
            print("❌ Invalid port number")

        # Check for conflicts
        if self.config.fastapi_port == self.config.flask_port:
            print("⚠️  Warning: FastAPI and Flask ports are the same!")

        web_host = input(f"Web Host [{self.config.web_host}]: ").strip()
        if web_host:
            self.config.web_host = web_host

        print()

    def configure_advanced(self):
        """Configure advanced settings."""
        print("⚡ Advanced Configuration")
        print("-" * 25)

        # Performance settings
        try:
            max_workers = input(f"Max Workers [{self.config.max_workers}]: ").strip()
            if max_workers:
                self.config.max_workers = int(max_workers)
        except ValueError:
            print("❌ Invalid number")

        try:
            timeout = input(f"Request Timeout (seconds) [{self.config.request_timeout}]: ").strip()
            if timeout:
                self.config.request_timeout = int(timeout)
        except ValueError:
            print("❌ Invalid number")

        print()

    def finalize_setup(self):
        """Finalize setup with validation and saving."""
        print("🔍 Configuration Validation")
        print("-" * 30)

        is_valid, issues = self.validate_config()

        if issues:
            print("❌ Configuration Issues Found:")
            for issue in issues:
                print(f"  {issue}")
            print()

            fix = input("Attempt to fix issues? (y/n) [y]: ").strip().lower()
            if fix in ('', 'y', 'yes'):
                # Basic auto-fix for common issues
                self.auto_fix_issues(issues)
                is_valid, issues = self.validate_config()

        if is_valid:
            print("✅ Configuration is valid!")
        else:
            print("⚠️  Configuration has issues but proceeding...")

        # Save configuration
        save = input("Save configuration? (y/n) [y]: ").strip().lower()
        if save in ('', 'y', 'yes'):
            self.save_config()
            print("✅ Setup complete! Run 'python main.py' to start services.")
        else:
            print("⚠️  Configuration not saved.")

    def auto_fix_issues(self, issues: List[str]):
        """Attempt to auto-fix common configuration issues."""
        for issue in issues:
            if "Port conflict" in issue:
                print("🔧 Auto-fixing port conflict...")
                if self.config.fastapi_port == 8001:
                    self.config.flask_port = 5001
                else:
                    self.config.flask_port = 5000
                print(f"  Set Flask port to {self.config.flask_port}")

    def run_validation_only(self):
        """Run configuration validation only."""
        print("🔍 Configuration Validation")
        print("=" * 30)

        is_valid, issues = self.validate_config()

        if is_valid:
            print("✅ Configuration is valid!")
            print("\n📋 Enabled Services:")
            for service_key, service_config in self.config.services.items():
                if service_config.enabled:
                    status = "✅ Auto-start" if service_config.auto_start else "✅ Enabled"
                    print(f"  {service_key}: {status}")
        else:
            print("❌ Configuration Issues Found:")
            for issue in issues:
                print(f"  {issue}")

            print("\n💡 Run 'python setup_wizard.py' to fix configuration issues.")

    def reset_configuration(self):
        """Reset configuration to defaults."""
        confirm = input("Reset all configuration to defaults? (y/n) [n]: ").strip().lower()
        if confirm in ('y', 'yes'):
            # Remove config files
            if self.env_file.exists():
                self.env_file.unlink()
            if self.config_file.exists():
                self.config_file.unlink()

            # Reset config
            self.config = SetupConfig()
            print("✅ Configuration reset to defaults.")
        else:
            print("❌ Reset cancelled.")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="dream.os Setup Wizard")
    parser.add_argument("--validate", action="store_true", help="Validate existing configuration only")
    parser.add_argument("--reset", action="store_true", help="Reset configuration to defaults")

    args = parser.parse_args()

    wizard = SetupWizard()

    if args.reset:
        wizard.reset_configuration()
    elif args.validate:
        wizard.run_validation_only()
    else:
        wizard.run_interactive_setup()

if __name__ == "__main__":
    main()