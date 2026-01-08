#!/usr/bin/env python3
"""
Import Path Fix Utility
Resolves Python import path issues for src module access

Usage:
    python tools/import_path_fix.py --fix
    python tools/import_path_fix.py --test
"""

import sys
import os
from pathlib import Path


def fix_import_path():
    """Fix Python import path for src module access"""
    project_root = Path(__file__).parent.parent

    # Add src directory to Python path
    src_path = str(project_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
        print(f"✅ Added {src_path} to sys.path")

    # Test import
    try:
        import src
        print("✅ Successfully imported 'src' module")
        return True
    except ImportError as e:
        print(f"❌ Failed to import 'src' module: {e}")
        return False


def test_ai_services():
    """Test if AI services can now be imported"""
    services_to_test = [
        "performance_analyzer",
        "recommendation_engine",
        "work_indexer",
        "learning_recommender"
    ]

    results = {}

    for service in services_to_test:
        try:
            module_path = f"src.services.{service}"
            __import__(module_path)
            results[service] = "✅ SUCCESS"
            print(f"✅ {service}: Import successful")
        except ImportError as e:
            results[service] = f"❌ FAILED: {e}"
            print(f"❌ {service}: Import failed - {e}")
        except Exception as e:
            results[service] = f"⚠️ PARTIAL: {e}"
            print(f"⚠️ {service}: Import succeeded but initialization failed - {e}")

    return results


def create_startup_script():
    """Create a startup script that fixes import paths"""
    script_content = '''#!/usr/bin/env python3
"""
Swarm Startup Script with Import Path Fix
Ensures proper Python path configuration for AI services
"""

import sys
from pathlib import Path

# Fix import path
project_root = Path(__file__).parent
src_path = str(project_root / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"Import path fixed: {src_path}")

# Now you can import AI services
try:
    import src.services.performance_analyzer as pa
    print("✅ AI services ready")
except ImportError as e:
    print(f"❌ AI services still unavailable: {e}")
'''

    script_path = Path(__file__).parent.parent / "swarm_startup.py"
    with open(script_path, 'w') as f:
        f.write(script_content)

    print(f"✅ Created startup script: {script_path}")
    return script_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Import Path Fix Utility")
    parser.add_argument("--fix", action="store_true", help="Apply import path fix")
    parser.add_argument("--test", action="store_true", help="Test AI service imports")
    parser.add_argument("--create-startup", action="store_true", help="Create startup script")

    args = parser.parse_args()

    if args.fix:
        success = fix_import_path()
        if success:
            print("\nTesting AI services...")
            test_ai_services()

    elif args.test:
        print("Testing AI service imports...")
        test_ai_services()

    elif args.create_startup:
        create_startup_script()

    else:
        print("Use --fix, --test, or --create-startup")


if __name__ == "__main__":
    main()