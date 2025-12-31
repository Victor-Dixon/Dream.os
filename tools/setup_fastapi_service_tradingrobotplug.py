#!/usr/bin/env python3
"""
FastAPI Service Setup Script for TradingRobotPlug
==================================================

Automates virtual environment setup, .env configuration, and provides systemd service installation instructions.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
"""

import sys
import subprocess
from pathlib import Path

BACKEND_DIR = "backend"
VENV_DIR = "venv"
PYTHON_VERSION = "python3.11"


def run_command(cmd, check=True, shell=False):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd.split(),
            shell=shell,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)


def setup_fastapi_service():
    """Setup FastAPI service on the server."""
    print("🚀 TradingRobotPlug FastAPI Service Setup\n")
    
    # Check if backend directory exists
    backend_path = Path(BACKEND_DIR)
    if not backend_path.exists():
        print(f"❌ Backend directory not found: {BACKEND_DIR}")
        print(f"   Expected location: {Path.cwd() / BACKEND_DIR}")
        return False
    
    print(f"✅ Backend directory found: {backend_path.resolve()}\n")
    
    # Step 1: Create virtual environment
    venv_path = backend_path / VENV_DIR
    if not venv_path.exists():
        print(f"📦 Creating virtual environment...")
        success, stdout, stderr = run_command([PYTHON_VERSION, "-m", "venv", str(venv_path)])
        if success:
            print(f"✅ Virtual environment created: {venv_path}")
        else:
            print(f"❌ Failed to create virtual environment: {stderr}")
            return False
    else:
        print(f"✅ Virtual environment already exists: {venv_path}")
    
    # Step 2: Upgrade pip
    print(f"\n📦 Upgrading pip...")
    pip_cmd = f"{venv_path / 'bin' / 'pip'} install --upgrade pip"
    success, stdout, stderr = run_command(pip_cmd, shell=True)
    if success:
        print(f"✅ Pip upgraded")
    else:
        print(f"⚠️  Pip upgrade failed: {stderr}")
    
    # Step 3: Install dependencies
    requirements_file = backend_path / "requirements.txt"
    if requirements_file.exists():
        print(f"\n📦 Installing dependencies from requirements.txt...")
        pip_install_cmd = f"{venv_path / 'bin' / 'pip'} install -r {requirements_file}"
        success, stdout, stderr = run_command(pip_install_cmd, shell=True)
        if success:
            print(f"✅ Dependencies installed")
        else:
            print(f"❌ Failed to install dependencies: {stderr}")
            return False
    else:
        print(f"⚠️  requirements.txt not found, skipping dependency installation")
    
    # Step 4: Configure .env file
    print(f"\n📝 Configuring .env file...")
    env_example = backend_path / ".env.example"
    env_file = backend_path / ".env"
    
    if env_example.exists() and not env_file.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print(f"✅ .env file created from .env.example")
        print(f"⚠️  IMPORTANT: Edit .env file with actual values:")
        print(f"   - DATABASE_URL")
        print(f"   - ALPACA_API_KEY and ALPACA_SECRET_KEY")
        print(f"   - API_SECRET_KEY and JWT_SECRET_KEY")
        print(f"   - CORS_ORIGINS (for production)")
    elif env_file.exists():
        print(f"✅ .env file already exists")
    else:
        print(f"⚠️  .env.example not found, .env file not created")
    
    # Step 5: Systemd service installation instructions
    print(f"\n📋 Systemd Service Installation:")
    service_file = Path("/tmp/tradingrobotplug-fastapi.service")
    if service_file.exists():
        print(f"✅ Service file found at {service_file}")
        print(f"\n📋 Manual steps to install systemd service:")
        print(f"   1. sudo cp /tmp/tradingrobotplug-fastapi.service /etc/systemd/system/")
        print(f"   2. sudo systemctl daemon-reload")
        print(f"   3. sudo systemctl enable tradingrobotplug-fastapi")
        print(f"   4. sudo systemctl start tradingrobotplug-fastapi")
        print(f"   5. sudo systemctl status tradingrobotplug-fastapi")
    else:
        print(f"⚠️  Service file not found at /tmp/tradingrobotplug-fastapi.service")
        print(f"   Service file should have been deployed by deployment script")
    
    print(f"\n✅ FastAPI service setup complete!")
    print(f"\n📋 Next Steps:")
    print(f"   1. Edit .env file with actual configuration values")
    print(f"   2. Initialize database (if needed)")
    print(f"   3. Install and start systemd service (see instructions above)")
    print(f"   4. Verify health: curl http://localhost:8001/health")
    print(f"   5. Agent-7: Run endpoint verification script")
    
    return True


if __name__ == "__main__":
    success = setup_fastapi_service()
    sys.exit(0 if success else 1)

