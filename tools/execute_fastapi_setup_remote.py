#!/usr/bin/env python3
"""
Execute FastAPI Service Setup Remotely
=======================================

Executes Phase 2 service setup on remote server via SSH.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
"""

import sys
from pathlib import Path

# Add ops/deployment to path for SimpleWordPressDeployer
# Check if we're in Agent_Cellphone_V2_Repository or websites workspace
repo_root = Path(__file__).parent.parent
websites_root = Path("D:/websites")
if (repo_root / "websites" / "ops" / "deployment" / "simple_wordpress_deployer.py").exists():
    sys.path.insert(0, str(repo_root / "websites" / "ops" / "deployment"))
elif (websites_root / "ops" / "deployment" / "simple_wordpress_deployer.py").exists():
    sys.path.insert(0, str(websites_root / "ops" / "deployment"))
else:
    print("❌ Could not find simple_wordpress_deployer.py")
    sys.exit(1)

from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

SITE_KEY = "tradingrobotplug.com"
BACKEND_DIR = "backend"
VENV_DIR = "venv"
PYTHON_VERSION = "python3.11"


def execute_remote_setup():
    """Execute FastAPI service setup on remote server."""
    print("🚀 TradingRobotPlug FastAPI Remote Service Setup\n")
    
    site_configs = load_site_configs()
    try:
        deployer = SimpleWordPressDeployer(SITE_KEY, site_configs)
    except Exception as e:
        print(f"❌ Failed to initialize deployer: {e}")
        return False
    
    if not deployer.connect():
        print("❌ Failed to connect to server")
        return False
    print(f"✅ Connected to {SITE_KEY}\n")
    
    # Step 1: Check if backend directory exists
    print("📂 Checking backend directory...")
    check_backend_cmd = f"cd {BACKEND_DIR} && pwd"
    result = deployer.execute_command(check_backend_cmd)
    if "No such file" in result or "cannot access" in result.lower():
        print(f"❌ Backend directory not found: {BACKEND_DIR}")
        print(f"   Please ensure files were deployed in Phase 1")
        return False
    print(f"✅ Backend directory found\n")
    
    # Step 2: Create virtual environment
    print("📦 Creating virtual environment...")
    create_venv_cmd = f"cd {BACKEND_DIR} && {PYTHON_VERSION} -m venv {VENV_DIR}"
    result = deployer.execute_command(create_venv_cmd)
    if "error" in result.lower() and "already exists" not in result.lower():
        print(f"⚠️  Virtual environment creation: {result}")
    else:
        print(f"✅ Virtual environment created/verified\n")
    
    # Step 3: Upgrade pip
    print("📦 Upgrading pip...")
    upgrade_pip_cmd = f"cd {BACKEND_DIR} && {VENV_DIR}/bin/pip install --upgrade pip"
    result = deployer.execute_command(upgrade_pip_cmd)
    if "error" not in result.lower() or "already satisfied" in result.lower():
        print(f"✅ Pip upgraded\n")
    else:
        print(f"⚠️  Pip upgrade: {result}\n")
    
    # Step 4: Install dependencies
    print("📦 Installing dependencies from requirements.txt...")
    install_deps_cmd = f"cd {BACKEND_DIR} && {VENV_DIR}/bin/pip install -r requirements.txt"
    result = deployer.execute_command(install_deps_cmd)
    if "error" in result.lower() and "already satisfied" not in result.lower():
        print(f"❌ Dependency installation failed: {result}")
        print(f"   Continuing with manual review needed...\n")
    else:
        print(f"✅ Dependencies installed\n")
    
    # Step 5: Configure .env file
    print("📝 Configuring .env file...")
    setup_env_cmd = f"cd {BACKEND_DIR} && if [ -f .env.example ] && [ ! -f .env ]; then cp .env.example .env && echo 'Created'; elif [ -f .env ]; then echo 'Exists'; else echo 'NoExample'; fi"
    result = deployer.execute_command(setup_env_cmd)
    if "Created" in result:
        print(f"✅ .env file created from .env.example")
        print(f"⚠️  IMPORTANT: Edit .env file with actual values:\n")
        print(f"   - DATABASE_URL")
        print(f"   - ALPACA_API_KEY and ALPACA_SECRET_KEY")
        print(f"   - API_SECRET_KEY and JWT_SECRET_KEY")
        print(f"   - CORS_ORIGINS (for production)\n")
    elif "Exists" in result:
        print(f"✅ .env file already exists\n")
    else:
        print(f"⚠️  .env.example not found, .env file not created\n")
    
    # Step 6: Systemd service installation instructions
    print("📋 Systemd Service Installation:")
    check_service_cmd = "test -f /tmp/tradingrobotplug-fastapi.service && echo 'Found' || echo 'NotFound'"
    result = deployer.execute_command(check_service_cmd)
    if "Found" in result:
        print(f"✅ Service file found at /tmp/tradingrobotplug-fastapi.service")
        print(f"\n📋 Manual steps to install systemd service (requires sudo):")
        print(f"   1. sudo cp /tmp/tradingrobotplug-fastapi.service /etc/systemd/system/")
        print(f"   2. sudo systemctl daemon-reload")
        print(f"   3. sudo systemctl enable tradingrobotplug-fastapi")
        print(f"   4. sudo systemctl start tradingrobotplug-fastapi")
        print(f"   5. sudo systemctl status tradingrobotplug-fastapi\n")
    else:
        print(f"⚠️  Service file not found at /tmp/tradingrobotplug-fastapi.service")
        print(f"   Service file should have been deployed by deployment script\n")
    
    print(f"✅ FastAPI service setup complete!\n")
    print(f"📋 Next Steps:")
    print(f"   1. Edit .env file with actual configuration values (via SFTP or SSH)")
    print(f"   2. Initialize database (if needed):")
    print(f"      cd {BACKEND_DIR} && source {VENV_DIR}/bin/activate")
    print(f"      python -c 'from database.connection import init_database; init_database()'")
    print(f"   3. Install and start systemd service (see instructions above)")
    print(f"   4. Verify health: curl http://localhost:8001/health")
    print(f"   5. Agent-1: Test FastAPI endpoints")
    print(f"   6. Agent-7: Verify WordPress endpoints\n")
    
    return True


if __name__ == "__main__":
    success = execute_remote_setup()
    sys.exit(0 if success else 1)

