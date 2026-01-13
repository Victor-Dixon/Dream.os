#!/usr/bin/env python3
"""
FastAPI Configuration Verification Tool
Verifies required configuration for FastAPI service.

Usage:
    python tools/verify_fastapi_config.py [--config-file PATH]
    
Checks for required environment variables and configuration.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent

REQUIRED_ENV_VARS = [
    "DATABASE_URL",
    # Add other required variables as needed
]

OPTIONAL_ENV_VARS = [
    "API_KEY",
    "SECRET_KEY",
    # Add other optional variables as needed
]


def check_env_file(env_path: Path) -> Tuple[bool, Dict[str, any]]:
    """Check .env file for required variables."""
    results = {
        "file_exists": env_path.exists(),
        "required_vars": {},
        "optional_vars": {},
        "missing_required": []
    }
    
    if not env_path.exists():
        return False, results
    
    # Read .env file
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        env_vars = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
        
        # Check required variables
        for var in REQUIRED_ENV_VARS:
            if var in env_vars:
                results["required_vars"][var] = "✅ Present"
            else:
                results["required_vars"][var] = "❌ Missing"
                results["missing_required"].append(var)
        
        # Check optional variables
        for var in OPTIONAL_ENV_VARS:
            if var in env_vars:
                results["optional_vars"][var] = "✅ Present"
            else:
                results["optional_vars"][var] = "⚠️  Not set"
        
        results["all_required_present"] = len(results["missing_required"]) == 0
        
    except Exception as e:
        results["error"] = str(e)
        return False, results
    
    return results["all_required_present"], results


def verify_config(config_file: str = None):
    """Verify FastAPI configuration."""
    print("="*70)
    print("FASTAPI CONFIGURATION VERIFICATION")
    print("="*70)
    print()
    
    # Try to find .env file
    if config_file:
        env_path = Path(config_file)
    else:
        # Common locations
        possible_locations = [
            PROJECT_ROOT / ".env",
            PROJECT_ROOT / "backend" / ".env",
            Path("/tmp/tradingrobotplug-fastapi") / ".env",
        ]
        
        env_path = None
        for loc in possible_locations:
            if loc.exists():
                env_path = loc
                break
    
    if not env_path or not env_path.exists():
        print("❌ .env file not found")
        print()
        print("Expected locations:")
        for loc in possible_locations:
            print(f"  - {loc}")
        print()
        print("⚠️  Configuration verification cannot proceed without .env file")
        return False
    
    print(f"📄 Checking .env file: {env_path}")
    print()
    
    is_valid, results = check_env_file(env_path)
    
    # Required variables
    print("REQUIRED VARIABLES:")
    print("-" * 70)
    for var, status in results["required_vars"].items():
        print(f"  {status} - {var}")
    print()
    
    # Optional variables
    if results["optional_vars"]:
        print("OPTIONAL VARIABLES:")
        print("-" * 70)
        for var, status in results["optional_vars"].items():
            print(f"  {status} - {var}")
        print()
    
    # Summary
    print("="*70)
    if is_valid:
        print("✅ Configuration is VALID")
        print("   All required variables present")
    else:
        print("❌ Configuration is INVALID")
        print(f"   Missing required variables: {', '.join(results['missing_required'])}")
        print()
        print("Action Required:")
        print("1. Add missing variables to .env file")
        print("2. Restart service: sudo systemctl restart tradingrobotplug-fastapi")
    print("="*70)
    
    return is_valid


def main():
    parser = argparse.ArgumentParser(description="Verify FastAPI configuration")
    parser.add_argument("--config-file", help="Path to .env file")
    args = parser.parse_args()
    
    is_valid = verify_config(args.config_file)
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()

