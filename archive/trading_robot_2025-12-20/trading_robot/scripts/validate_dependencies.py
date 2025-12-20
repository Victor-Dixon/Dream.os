#!/usr/bin/env python3
"""
Trading Robot Dependency Validation Script
==========================================

Validates that all dependencies in requirements.txt are installable
and compatible. Creates virtual environment setup script.

Usage:
    python scripts/validate_dependencies.py

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def parse_requirements(requirements_file: Path) -> List[str]:
    """
    Parse requirements.txt file.
    
    Args:
        requirements_file: Path to requirements.txt
        
    Returns:
        List of requirement strings
    """
    if not requirements_file.exists():
        logger.error(f"❌ Requirements file not found: {requirements_file}")
        return []
    
    requirements = []
    with open(requirements_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith("#"):
                requirements.append(line)
    
    return requirements


def check_package_installable(package: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a package can be installed (dry run).
    
    Args:
        package: Package name with version specifier
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Use pip install --dry-run to check if package is installable
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--dry-run", package],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode == 0:
            return True, None
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        return False, "Timeout while checking package"
    except Exception as e:
        return False, str(e)


def validate_dependencies(requirements_file: Path) -> Tuple[bool, List[str]]:
    """
    Validate all dependencies in requirements.txt.
    
    Args:
        requirements_file: Path to requirements.txt
        
    Returns:
        Tuple of (all_valid, error_messages)
    """
    requirements = parse_requirements(requirements_file)
    
    if not requirements:
        return False, ["No requirements found"]
    
    logger.info(f"📦 Validating {len(requirements)} dependencies...")
    
    errors = []
    valid_count = 0
    
    for req in requirements:
        package_name = req.split(">=")[0].split("==")[0].split("<=")[0].strip()
        logger.info(f"  Checking {package_name}...")
        
        success, error = check_package_installable(req)
        
        if success:
            valid_count += 1
            logger.info(f"    ✅ {package_name}")
        else:
            errors.append(f"{package_name}: {error}")
            logger.warning(f"    ❌ {package_name}: {error}")
    
    all_valid = len(errors) == 0
    
    logger.info(f"\n📊 Validation Results:")
    logger.info(f"  ✅ Valid: {valid_count}/{len(requirements)}")
    logger.info(f"  ❌ Errors: {len(errors)}/{len(requirements)}")
    
    return all_valid, errors


def create_venv_setup_script(venv_dir: Path = Path("venv")) -> Path:
    """
    Create virtual environment setup script.
    
    Args:
        venv_dir: Virtual environment directory path
        
    Returns:
        Path to setup script
    """
    script_path = Path(__file__).parent.parent / "setup_venv.sh"
    
    script_content = f"""#!/bin/bash
# Trading Robot Virtual Environment Setup Script
# Generated: 2025-12-20
# Author: Agent-3 (Infrastructure & DevOps Specialist)

set -e

echo "🚀 Setting up Trading Robot virtual environment..."

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

echo "📍 Using Python: $($PYTHON_CMD --version)"

# Create virtual environment
echo "📦 Creating virtual environment in {venv_dir}..."
$PYTHON_CMD -m venv {venv_dir}

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source {venv_dir}/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source {venv_dir}/bin/activate"
"""
    
    script_path.write_text(script_content, encoding="utf-8")
    script_path.chmod(0o755)  # Make executable
    
    logger.info(f"✅ Created virtual environment setup script: {script_path}")
    
    return script_path


def create_venv_setup_script_windows(venv_dir: Path = Path("venv")) -> Path:
    """
    Create Windows virtual environment setup script.
    
    Args:
        venv_dir: Virtual environment directory path
        
    Returns:
        Path to setup script
    """
    script_path = Path(__file__).parent.parent / "setup_venv.bat"
    
    script_content = f"""@echo off
REM Trading Robot Virtual Environment Setup Script (Windows)
REM Generated: 2025-12-20
REM Author: Agent-3 (Infrastructure & DevOps Specialist)

echo 🚀 Setting up Trading Robot virtual environment...

REM Determine Python command
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

echo 📍 Using Python:
python --version

REM Create virtual environment
echo 📦 Creating virtual environment in {venv_dir}...
python -m venv {venv_dir}

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call {venv_dir}\\Scripts\\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo ✅ Virtual environment setup complete!
echo.
echo To activate the virtual environment, run:
echo   {venv_dir}\\Scripts\\activate.bat
"""
    
    script_path.write_text(script_content, encoding="utf-8")
    
    logger.info(f"✅ Created Windows virtual environment setup script: {script_path}")
    
    return script_path


def main():
    """Main function."""
    logger.info("🔍 Trading Robot Dependency Validation")
    
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        logger.error(f"❌ Requirements file not found: {requirements_file}")
        return 1
    
    # Validate dependencies
    all_valid, errors = validate_dependencies(requirements_file)
    
    if not all_valid:
        logger.warning("\n⚠️  Some dependencies failed validation:")
        for error in errors:
            logger.warning(f"  - {error}")
    
    # Create setup scripts
    logger.info("\n📝 Creating virtual environment setup scripts...")
    create_venv_setup_script()
    create_venv_setup_script_windows()
    
    if all_valid:
        logger.info("\n✅ All dependencies validated successfully")
        return 0
    else:
        logger.warning("\n⚠️  Dependency validation completed with errors")
        logger.warning("   Review errors above and fix requirements.txt if needed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
