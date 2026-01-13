<<<<<<< HEAD
#!/usr/bin/env python
"""
Setup script for Agent Cellphone V2 - Swarm AI Coordination Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "PYPI_PACKAGE_README.md").read_text()

# Read version from package
def get_version():
    """Extract version from __init__.py"""
    init_file = this_directory / "src" / "__init__.py"
    if init_file.exists():
        content = init_file.read_text()
        for line in content.split('\n'):
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')

    # Fallback version
    return "2.0.0"

setup(
    name="agent-cellphone-v2",
    version=get_version(),
    author="Agent Cellphone Development Team",
    author_email="team@agent-cellphone-v2.com",
    description="Swarm AI Coordination Framework for Multi-Agent Collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/agent-cellphone-v2",
    project_urls={
        "Documentation": "https://docs.agent-cellphone-v2.com",
        "Source": "https://github.com/your-org/agent-cellphone-v2",
        "Tracker": "https://github.com/your-org/agent-cellphone-v2/issues",
        "Changelog": "https://github.com/your-org/agent-cellphone-v2/blob/main/CHANGELOG.md",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords=[
        "ai", "swarm", "agents", "coordination", "collaboration",
        "multi-agent", "artificial-intelligence", "distributed-systems",
        "machine-learning", "automation"
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (none required for basic functionality)
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "pre-commit>=3.0.0",
        ],
        "monitoring": [
            "prometheus-client>=0.16.0",
            "grafana-api>=1.0.3",
        ],
        "security": [
            "cryptography>=41.0.0",
            "pyjwt>=2.0.0",
        ],
        "web": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "websockets>=11.0.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "pre-commit>=3.0.0",
            "prometheus-client>=0.16.0",
            "grafana-api>=1.0.3",
            "cryptography>=41.0.0",
            "pyjwt>=2.0.0",
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "websockets>=11.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-cellphone=agent_cellphone.cli:main",
            "agent-cellphone-monitor=agent_cellphone.cli:monitor",
            "agent-cellphone-status=agent_cellphone.cli:status",
            "agent-cellphone-coordinate=agent_cellphone.cli:coordinate",
            "agent-cellphone-dashboard=agent_cellphone.cli:dashboard",
            "agent-cellphone-metrics=agent_cellphone.cli:metrics",
            "agent-cellphone-health=agent_cellphone.cli:health",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
=======
#!/usr/bin/env python3
"""
dream.os - One-Command Setup Script
===================================

The ultimate setup experience for dream.os. This script guides you through:
1. System validation
2. Interactive configuration
3. Installation (Docker or native)
4. Service startup and testing

Usage:
    python setup.py          # Interactive setup (recommended)
    python setup.py --docker # Force Docker installation
    python setup.py --native # Force native Python installation
    python setup.py --validate # Just run validation

V2 Compliance: <400 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import platform

class DreamOSSetup:
    """Complete setup orchestrator for dream.os."""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.system = platform.system().lower()
        self.docker_available = self._check_docker()

    def _check_docker(self) -> bool:
        """Check if Docker is available."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f"🐝 {title}")
        print(f"{'='*60}")

    def print_success(self, message: str):
        """Print a success message."""
        print(f"✅ {message}")

    def print_error(self, message: str):
        """Print an error message."""
        print(f"❌ {message}")

    def print_warning(self, message: str):
        """Print a warning message."""
        print(f"⚠️  {message}")

    def print_info(self, message: str):
        """Print an info message."""
        print(f"ℹ️  {message}")

    def run_command(self, command: list, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a command with proper error handling."""
        try:
            working_dir = cwd or self.project_root
            result = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command failed: {' '.join(command)}")
            self.print_error(f"Error: {e.stderr}")
            raise

    def step_1_validation(self) -> bool:
        """Step 1: System validation."""
        self.print_header("STEP 1: System Validation")

        # Run post-clone validation
        self.print_info("Running system validation...")
        try:
            result = self.run_command([sys.executable, "scripts/post_clone_check.py"])
            if result.returncode == 0:
                self.print_success("System validation passed!")
                return True
            else:
                self.print_error("System validation failed. Please fix issues above.")
                return False
        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            return False

    def step_2_configuration(self) -> bool:
        """Step 2: Interactive configuration."""
        self.print_header("STEP 2: Configuration Setup")

        # Check if .env already exists
        env_file = self.project_root / ".env"
        if env_file.exists():
            self.print_info("Environment file (.env) already exists.")
            response = input("Do you want to reconfigure? (y/N): ").lower().strip()
            if response != 'y':
                self.print_success("Using existing configuration.")
                return True

        # Run setup wizard
        self.print_info("Starting interactive setup wizard...")
        try:
            result = self.run_command([sys.executable, "setup_wizard.py"])
            if result.returncode == 0:
                self.print_success("Configuration completed!")
                return True
            else:
                self.print_error("Configuration failed.")
                return False
        except Exception as e:
            self.print_error(f"Setup wizard failed: {e}")
            return False

    def step_3_installation(self, force_docker: bool = False, force_native: bool = False) -> bool:
        """Step 3: Installation."""
        self.print_header("STEP 3: Installation")

        # Determine installation method
        use_docker = False

        if force_docker and self.docker_available:
            use_docker = True
        elif force_native:
            use_docker = False
        else:
            # Interactive choice
            if self.docker_available:
                print("\n🐳 Installation Options:")
                print("1. Docker (recommended - isolated, easy)")
                print("2. Native Python (direct installation)")
                choice = input("Choose installation method (1/2) [1]: ").strip()

                if choice == "2":
                    use_docker = False
                else:
                    use_docker = True
            else:
                self.print_warning("Docker not available, using native Python installation.")
                use_docker = False

        # Perform installation
        if use_docker:
            return self._install_docker()
        else:
            return self._install_native()

    def _install_docker(self) -> bool:
        """Install using Docker."""
        self.print_info("Installing with Docker...")

        try:
            # Run Docker installation
            if self.system == "windows":
                script = "install.bat"
            else:
                script = "./install.sh"

            result = self.run_command([script, "--docker"])
            self.print_success("Docker installation completed!")

            # Start services
            self.print_info("Starting Docker services...")
            result = self.run_command(["docker-compose", "up", "-d"])
            self.print_success("Services started!")

            return True
        except Exception as e:
            self.print_error(f"Docker installation failed: {e}")
            return False

    def _install_native(self) -> bool:
        """Install using native Python."""
        self.print_info("Installing with native Python...")

        try:
            # Run native installation
            if self.system == "windows":
                script = "install.bat"
            else:
                script = "./install.sh"

            result = self.run_command([script])
            self.print_success("Native installation completed!")

            return True
        except Exception as e:
            self.print_error(f"Native installation failed: {e}")
            return False

    def step_4_verification(self) -> bool:
        """Step 4: Service verification."""
        self.print_header("STEP 4: Service Verification")

        self.print_info("Starting services and running health checks...")

        try:
            # Try to start services
            result = self.run_command([sys.executable, "main.py", "--background"])
            self.print_success("Services started!")

            # Wait a moment for services to initialize
            self.print_info("Waiting for services to initialize...")
            time.sleep(10)

            # Run health check
            self.print_info("Running health verification...")
            result = self.run_command([sys.executable, "main.py", "--status"])

            if "running" in result.stdout.lower():
                self.print_success("All services are running!")
                return True
            else:
                self.print_warning("Some services may not be running. Check logs.")
                return True  # Don't fail here, just warn

        except Exception as e:
            self.print_error(f"Service verification failed: {e}")
            return False

    def step_5_final_setup(self) -> bool:
        """Step 5: Final setup and next steps."""
        self.print_header("🎉 SETUP COMPLETE!")

        print("""
🐝 Welcome to dream.os!

Your multi-agent system is now ready. Here's what you can do:

📱 Access the Dashboard:
   • Web Dashboard: http://localhost:5000
   • API Documentation: http://localhost:8001/docs

🤖 Agent Commands:
   • Status: python main.py --status
   • Send message: python -m src.services.messaging_cli --bulk -m "Hello agents!"
   • Discord bot: python -m src.discord_commander.unified_discord_bot

📚 Getting Started:
   • Quick Start: QUICKSTART.md
   • Full Documentation: docs/
   • Discord Community: [Join our server]

🛠️  Troubleshooting:
   • Logs: tail -f logs/app.log
   • Health check: python scripts/health_check.py
   • Restart services: python main.py --restart

⚡ Next Steps:
   1. Configure your Discord bot token (if not done)
   2. Test agent communication
   3. Explore the web dashboard
   4. Join our Discord for support

Happy building with dream.os! 🚀
        """)

        return True

    def run_setup(self, force_docker: bool = False, force_native: bool = False, validate_only: bool = False):
        """Run the complete setup process."""
        print("🐝 dream.os - Complete Setup Experience")
        print("=" * 60)
        print("Welcome! This will guide you through setting up dream.os.")
        print("The process takes about 5-15 minutes depending on your system.")
        print()

        # Handle validation-only mode
        if validate_only:
            success = self.step_1_validation()
            return success

        # Run all steps
        steps = [
            ("System Validation", self.step_1_validation),
            ("Configuration", self.step_2_configuration),
            ("Installation", lambda: self.step_3_installation(force_docker, force_native)),
            ("Verification", self.step_4_verification),
            ("Final Setup", self.step_5_final_setup)
        ]

        for step_name, step_func in steps:
            try:
                success = step_func()
                if not success:
                    self.print_error(f"Setup failed at: {step_name}")
                    self.print_info("You can retry by running: python setup.py")
                    return False
            except KeyboardInterrupt:
                self.print_warning("Setup interrupted by user.")
                return False
            except Exception as e:
                self.print_error(f"Unexpected error in {step_name}: {e}")
                return False

        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="dream.os - Complete Setup Script")
    parser.add_argument("--docker", action="store_true", help="Force Docker installation")
    parser.add_argument("--native", action="store_true", help="Force native Python installation")
    parser.add_argument("--validate", action="store_true", help="Run validation only")

    args = parser.parse_args()

    # Validate arguments
    if args.docker and args.native:
        print("❌ Cannot specify both --docker and --native")
        sys.exit(1)

    # Run setup
    setup = DreamOSSetup()
    success = setup.run_setup(
        force_docker=args.docker,
        force_native=args.native,
        validate_only=args.validate
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
