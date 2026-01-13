#!/usr/bin/env python3
"""
Deploy FastAPI TradingRobotPlug Backend
=========================================

Deploys FastAPI application files to production server and configures service.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
"""

import sys
from pathlib import Path
import json

# Add ops/deployment to path for SimpleWordPressDeployer
sys.path.insert(0, str(Path(__file__).parent.parent / "ops" / "deployment"))
from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs

# FastAPI application paths
FASTAPI_BACKEND_PATH = Path("D:/websites/TradingRobotPlugWeb/backend")
# Deploy to user's home directory (accessible via SFTP)
# On Hostinger: /home/username/domains/tradingrobotplug.com/public_html/backend
# We'll use a relative path that the deployer will resolve
REMOTE_BACKEND_BASE = "backend"

# Site configuration
SITE_KEY = "tradingrobotplug.com"


def deploy_fastapi_backend():
    """Deploy FastAPI backend files to production server."""
    print("🚀 TradingRobotPlug FastAPI Backend Deployment\n")
    
    if not FASTAPI_BACKEND_PATH.exists():
        print(f"❌ FastAPI backend not found: {FASTAPI_BACKEND_PATH}")
        return False
    
    print(f"✅ FastAPI backend found: {FASTAPI_BACKEND_PATH}")
    print(f"📦 Deploying to: {REMOTE_BACKEND_BASE}\n")
    
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
    
    # Files to deploy (core FastAPI application)
    files_to_deploy = [
        # Main application
        ("api/fastapi_app.py", "api/fastapi_app.py"),
        ("api/__init__.py", "api/__init__.py"),
        ("api/dependencies.py", "api/dependencies.py"),
        ("api/auth.py", "api/auth.py"),
        
        # Routes
        ("api/routes/__init__.py", "api/routes/__init__.py"),
        ("api/routes/account.py", "api/routes/account.py"),
        ("api/routes/trades.py", "api/routes/trades.py"),
        ("api/routes/strategies.py", "api/routes/strategies.py"),
        ("api/routes/analytics.py", "api/routes/analytics.py"),
        
        # Models
        ("api/models/__init__.py", "api/models/__init__.py"),
        ("api/models/account.py", "api/models/account.py"),
        ("api/models/trade.py", "api/models/trade.py"),
        ("api/models/strategy.py", "api/models/strategy.py"),
        
        # Middleware
        ("api/middleware/__init__.py", "api/middleware/__init__.py"),
        ("api/middleware/rate_limit.py", "api/middleware/rate_limit.py"),
        
        # Core modules (if needed)
        ("core/__init__.py", "core/__init__.py"),
        ("core/trading_engine_v2.py", "core/trading_engine_v2.py"),
        ("core/strategy_manager_v2.py", "core/strategy_manager_v2.py"),
        ("core/event_publisher_v2.py", "core/event_publisher_v2.py"),
        ("core/market_data_streamer.py", "core/market_data_streamer.py"),
        ("core/websocket_event_server.py", "core/websocket_event_server.py"),
        
        # Database
        ("database/__init__.py", "database/__init__.py"),
        ("database/connection.py", "database/connection.py"),
        ("database/models.py", "database/models.py"),
        ("database/repositories.py", "database/repositories.py"),
        
        # Configuration
        ("config/__init__.py", "config/__init__.py"),
        ("config/settings.py", "config/settings.py"),
        
        # Requirements
        ("requirements.txt", "requirements.txt"),
        
        # Environment template
        ("deployment/env.example", ".env.example"),
    ]
    
    deployed_count = 0
    failed_count = 0
    
    for local_rel_path, remote_rel_path in files_to_deploy:
        local_file = FASTAPI_BACKEND_PATH / local_rel_path
        remote_path = f"{REMOTE_BACKEND_BASE}/{remote_rel_path}"
        
        if not local_file.exists():
            print(f"⚠️  Local file not found: {local_file} (skipping)")
            continue
        
        print(f"📤 Deploying: {local_rel_path} -> {remote_path}")
        try:
            # Ensure remote directory exists using SSH
            remote_dir = '/'.join(remote_path.split('/')[:-1])
            if remote_dir:
                # Try to create directory via SSH command
                mkdir_output = deployer.execute_command(f"mkdir -p {remote_dir} 2>&1 || true")
                if mkdir_output:
                    print(f"   📁 Directory creation: {mkdir_output.strip()}")
            
            # Use absolute path for local file
            local_file_abs = local_file.resolve()
            if not local_file_abs.exists():
                print(f"   ❌ Local file does not exist: {local_file_abs}")
                failed_count += 1
                continue
                
            # Deploy file - use full remote path
            # The deployer will handle path resolution relative to remote_path
            full_remote = f"{REMOTE_BACKEND_BASE}/{remote_rel_path}"
            success = deployer.deploy_file(local_file_abs, full_remote)
            if success:
                deployed_count += 1
                print(f"   ✅ Deployed successfully")
            else:
                failed_count += 1
                print(f"   ❌ Deployment failed (check SFTP permissions/path)")
        except Exception as e:
            print(f"   ❌ Error deploying {local_rel_path}: {e}")
            import traceback
            traceback.print_exc()
            failed_count += 1
    
    # Deploy systemd service file
    systemd_service_local = FASTAPI_BACKEND_PATH / "deployment" / "systemd" / "tradingrobotplug-fastapi.service"
    if systemd_service_local.exists():
        print(f"\n📤 Deploying systemd service file")
        try:
            remote_service_path = "/tmp/tradingrobotplug-fastapi.service"
            if deployer.deploy_file(systemd_service_local, remote_service_path):
                print(f"   ✅ Service file deployed to {remote_service_path}")
                print(f"   📋 Manual step: sudo mv {remote_service_path} /etc/systemd/system/")
                print(f"   📋 Manual step: sudo systemctl daemon-reload")
                print(f"   📋 Manual step: sudo systemctl enable tradingrobotplug-fastapi")
                print(f"   📋 Manual step: sudo systemctl start tradingrobotplug-fastapi")
        except Exception as e:
            print(f"   ⚠️  Error deploying service file: {e}")
    
    print(f"\n📊 Deployment Summary:")
    print(f"   ✅ Deployed: {deployed_count} files")
    print(f"   ❌ Failed: {failed_count} files\n")
    
    if deployed_count > 0 and failed_count == 0:
        print("✅ FastAPI backend deployment complete!")
        print(f"\n📋 Next Steps:")
        print(f"   1. SSH to server and create virtual environment:")
        print(f"      cd {REMOTE_BACKEND_BASE}")
        print(f"      python3.11 -m venv venv")
        print(f"      source venv/bin/activate")
        print(f"      pip install -r requirements.txt")
        print(f"   2. Configure .env file from .env.example")
        print(f"   3. Initialize database (if needed)")
        print(f"   4. Configure and start systemd service")
        print(f"   5. Verify health endpoint: curl http://localhost:8001/health")
        return True
    else:
        print("❌ FastAPI backend deployment had errors.")
        return False


if __name__ == "__main__":
    success = deploy_fastapi_backend()
    sys.exit(0 if success else 1)

