#!/usr/bin/env python3
"""
SFTP Path Structure Validation Tool
===================================

Tests SFTP connection and verifies actual path structure for Hostinger deployments.

Usage:
    python tools/test_sftp_path_structure.py --site freerideinvestor
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False
    print("❌ paramiko not installed. Install with: pip install paramiko")

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def load_credentials(site_key: str) -> dict:
    """Load credentials from sites.json or .env."""
    import json
    import os
    
    # Try sites.json first
    creds_file = Path(".deploy_credentials/sites.json")
    if creds_file.exists():
        try:
            with open(creds_file) as f:
                all_creds = json.load(f)
            creds = (
                all_creds.get(site_key) or 
                all_creds.get(f"{site_key}.online") or
                all_creds.get(site_key.replace(".online", ""))
            )
            if creds:
                logger.info(f"✅ Loaded credentials from sites.json for {site_key}")
                return creds
        except Exception as e:
            logger.warning(f"Failed to load from sites.json: {e}")
    
    # Try .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        host = os.getenv("HOSTINGER_HOST") or os.getenv("SSH_HOST")
        user = os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER")
        password = os.getenv("HOSTINGER_PASS") or os.getenv("SSH_PASS")
        port = int(os.getenv("HOSTINGER_PORT") or os.getenv("SSH_PORT", "65002"))
        
        if host and user and password:
            logger.info(f"✅ Loaded credentials from .env for {site_key}")
            return {
                "host": host,
                "username": user,
                "password": password,
                "port": port
            }
    except Exception as e:
        logger.warning(f"Failed to load from .env: {e}")
    
    return None


def test_sftp_connection(creds: dict) -> tuple[bool, paramiko.SFTPClient, paramiko.SSHClient]:
    """Test SFTP connection and return client objects."""
    if not HAS_PARAMIKO:
        return False, None, None
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        logger.info(f"🔌 Connecting to {creds['host']}:{creds['port']}...")
        client.connect(
            hostname=creds['host'],
            port=creds['port'],
            username=creds['username'],
            password=creds['password'],
            timeout=10
        )
        
        logger.info("✅ SSH connection established")
        
        sftp = client.open_sftp()
        logger.info("✅ SFTP connection established")
        
        return True, sftp, client
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False, None, None


def check_path_structure(sftp: paramiko.SFTPClient) -> dict:
    """Check SFTP path structure and return findings."""
    results = {
        "current_dir": None,
        "home_dir": None,
        "public_html_exists": False,
        "domains_exists": False,
        "test_paths": {}
    }
    
    try:
        # Get current working directory
        results["current_dir"] = sftp.getcwd()
        logger.info(f"📁 Current directory: {results['current_dir']}")
        
        # Try to get home directory (usually ~ or /home/username)
        try:
            results["home_dir"] = sftp.normalize(".")
            logger.info(f"📁 Home directory: {results['home_dir']}")
        except:
            pass
        
        # Test common paths
        test_paths = [
            "/public_html",
            "/domains",
            "/domains/freerideinvestor.com",
            "/domains/freerideinvestor.com/public_html",
            "public_html",
            "domains",
        ]
        
        for path in test_paths:
            try:
                sftp.stat(path)
                results["test_paths"][path] = "EXISTS"
                logger.info(f"✅ Path exists: {path}")
            except FileNotFoundError:
                results["test_paths"][path] = "NOT_FOUND"
                logger.info(f"❌ Path not found: {path}")
            except Exception as e:
                results["test_paths"][path] = f"ERROR: {e}"
                logger.warning(f"⚠️ Path error: {path} - {e}")
        
        # Check if we can list current directory
        try:
            files = sftp.listdir(".")
            logger.info(f"📋 Current directory contents ({len(files)} items): {', '.join(files[:10])}")
            results["current_dir_contents"] = files[:20]  # First 20 items
        except Exception as e:
            logger.warning(f"⚠️ Cannot list directory: {e}")
        
    except Exception as e:
        logger.error(f"❌ Path check failed: {e}")
        results["error"] = str(e)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Test SFTP path structure")
    parser.add_argument("--site", type=str, required=True, help="Site key (e.g., freerideinvestor)")
    args = parser.parse_args()
    
    logger.info(f"🔍 Testing SFTP path structure for {args.site}")
    
    # Load credentials
    creds = load_credentials(args.site)
    if not creds:
        logger.error("❌ Failed to load credentials")
        return 1
    
    # Test connection
    success, sftp, client = test_sftp_connection(creds)
    if not success:
        return 1
    
    try:
        # Check path structure
        results = check_path_structure(sftp)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 SFTP PATH STRUCTURE VALIDATION RESULTS")
        print("="*60)
        print(f"Current Directory: {results.get('current_dir', 'Unknown')}")
        print(f"Home Directory: {results.get('home_dir', 'Unknown')}")
        print("\nPath Test Results:")
        for path, status in results.get("test_paths", {}).items():
            print(f"  {path}: {status}")
        
        if "current_dir_contents" in results:
            print(f"\nCurrent Directory Contents ({len(results['current_dir_contents'])} items):")
            for item in results["current_dir_contents"][:10]:
                print(f"  - {item}")
        
        print("\n" + "="*60)
        print("✅ Validation complete")
        print("="*60)
        
    finally:
        if sftp:
            sftp.close()
        if client:
            client.close()
        logger.info("🔌 Connection closed")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

