#!/usr/bin/env python3
"""
Discord Bot Quick Fix Script
============================

Diagnoses and fixes common Discord bot startup issues:
- Redis connection problems
- Log file permission issues
- Environment configuration

Usage: python scripts/fix_discord_bot.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class DiscordBotFixer:
    """Quick fix utility for Discord bot issues"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors = []
        self.fixes = []

    def check_redis_connection(self):
        """Check Redis connectivity"""
        print("🔍 Checking Redis connection...")

        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=5)
            r.ping()
            print("✅ Redis: Connected successfully")
            return True
        except redis.ConnectionError:
            print("❌ Redis: Connection failed")
            self.errors.append("redis_connection")
            return False
        except ImportError:
            print("⚠️ Redis library not installed")
            self.errors.append("redis_library")
            return False

    def fix_redis_connection(self):
        """Attempt to fix Redis connection issues"""
        if "redis_library" in self.errors:
            print("🔧 Installing redis library...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "redis"])
                print("✅ Redis library installed")
                self.fixes.append("redis_library")
            except subprocess.CalledProcessError:
                print("❌ Failed to install redis library")
                return False

        if "redis_connection" in self.errors:
            print("🔧 Attempting to start Redis server...")

            # Try Docker first
            try:
                result = subprocess.run(
                    ["docker", "run", "-d", "--name", "agent-redis", "-p", "6379:6379", "redis:7-alpine"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    print("✅ Redis started via Docker")
                    self.fixes.append("redis_docker")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print("⚠️ Docker not available, trying alternatives...")

            # Try local Redis installation
            if platform.system() == "Windows":
                # Try Redis in common locations
                redis_paths = [
                    r"C:\Program Files\Redis\redis-server.exe",
                    r"C:\Redis\redis-server.exe",
                    "redis-server.exe"
                ]

                for redis_path in redis_paths:
                    try:
                        result = subprocess.run([redis_path], capture_output=True, timeout=10)
                        if result.returncode == 0:
                            print("✅ Redis started locally")
                            self.fixes.append("redis_local")
                            return True
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        continue

            print("❌ Could not start Redis automatically")
            print("   Please install Redis manually:")
            print("   - Docker: docker run -d --name agent-redis -p 6379:6379 redis:7-alpine")
            print("   - Windows: Download from https://redis.io/download")
            return False

        return True

    def check_log_file_permissions(self):
        """Check log file permissions"""
        print("🔍 Checking log file permissions...")

        log_file = self.project_root / "src" / "logs" / "agent_cellphone.log"
        log_dir = log_file.parent

        # Ensure log directory exists
        if not log_dir.exists():
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
                print("✅ Log directory created")
            except Exception as e:
                print(f"❌ Failed to create log directory: {e}")
                return False

        # Check log file access
        try:
            with open(log_file, 'a') as f:
                f.write("")  # Test write access
            print("✅ Log file write access confirmed")
            return True
        except PermissionError:
            print("❌ Log file permission denied")
            self.errors.append("log_permissions")
            return False
        except Exception as e:
            print(f"⚠️ Log file access issue: {e}")
            return False

    def fix_log_file_permissions(self):
        """Fix log file permission issues"""
        if "log_permissions" not in self.errors:
            return True

        print("🔧 Fixing log file permissions...")

        log_file = self.project_root / "src" / "logs" / "agent_cellphone.log"

        try:
            # Try to clear the file
            with open(log_file, 'w') as f:
                f.write("")
            print("✅ Log file cleared and permissions verified")
            self.fixes.append("log_permissions")
            return True
        except Exception as e:
            print(f"❌ Could not fix log file permissions: {e}")
            return False

    def check_environment_variables(self):
        """Check required environment variables"""
        print("🔍 Checking environment variables...")

        required_vars = ['DISCORD_BOT_TOKEN']
        recommended_vars = ['REDIS_URL']

        missing_required = []
        missing_recommended = []

        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)

        for var in recommended_vars:
            if not os.getenv(var):
                missing_recommended.append(var)

        if missing_required:
            print(f"❌ Missing required environment variables: {missing_required}")
            self.errors.extend([f"missing_env_{var}" for var in missing_required])

        if missing_recommended:
            print(f"⚠️ Missing recommended environment variables: {missing_recommended}")

        if not missing_required and not missing_recommended:
            print("✅ Environment variables configured")

        return len(missing_required) == 0

    def generate_env_template(self):
        """Generate environment template"""
        if not any(error.startswith("missing_env_") for error in self.errors):
            return

        print("🔧 Generating environment template...")

        env_file = self.project_root / ".env"
        if env_file.exists():
            print("⚠️ .env file already exists, not overwriting")
            return

        template = """# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# Redis Configuration (Optional - bot works without it)
REDIS_URL=redis://localhost:6379

# Logging Configuration
LOG_LEVEL=INFO

# Database Configuration (if applicable)
DATABASE_URL=postgresql://user:password@localhost/dbname
"""

        try:
            with open(env_file, 'w') as f:
                f.write(template)
            print("✅ .env template created")
            print("   Please edit .env and add your DISCORD_BOT_TOKEN")
            self.fixes.append("env_template")
        except Exception as e:
            print(f"❌ Failed to create .env template: {e}")

    def run_diagnosis(self):
        """Run complete diagnosis"""
        print("🚀 Discord Bot Diagnostic Tool")
        print("=" * 40)

        # Run all checks
        redis_ok = self.check_redis_connection()
        logs_ok = self.check_log_file_permissions()
        env_ok = self.check_environment_variables()

        print("\n" + "=" * 40)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 40)

        if not self.errors:
            print("🎉 All checks passed! Bot should start successfully.")
            return True
        else:
            print(f"❌ Found {len(self.errors)} issues:")
            for error in self.errors:
                print(f"  • {error.replace('_', ' ').title()}")

            return False

    def apply_fixes(self):
        """Apply automatic fixes"""
        if not self.errors:
            return True

        print("\n🔧 APPLYING AUTOMATIC FIXES")
        print("=" * 40)

        success = True

        # Apply fixes in order
        if not self.fix_redis_connection():
            success = False

        if not self.fix_log_file_permissions():
            success = False

        self.generate_env_template()

        if success:
            print("✅ All automatic fixes applied")
        else:
            print("⚠️ Some fixes could not be applied automatically")

        return success

    def show_manual_steps(self):
        """Show manual steps for remaining issues"""
        if not self.errors:
            return

        print("\n📋 MANUAL STEPS REQUIRED")
        print("=" * 40)

        if any(error.startswith("missing_env_") for error in self.errors):
            print("1. Configure Environment Variables:")
            print("   - Copy .env.example to .env")
            print("   - Add your DISCORD_BOT_TOKEN")
            print("   - Optionally configure REDIS_URL")

        if "redis_connection" in self.errors and "redis_docker" not in self.fixes:
            print("2. Start Redis Server:")
            print("   Docker: docker run -d --name agent-redis -p 6379:6379 redis:7-alpine")
            print("   Local: Install Redis and run 'redis-server'")

        print("\n3. Test Bot Startup:")
        print("   python src/discord_commander/unified_discord_bot.py")

def main():
    """Main entry point"""
    fixer = DiscordBotFixer()

    # Run diagnosis
    diagnosis_ok = fixer.run_diagnosis()

    if not diagnosis_ok:
        # Apply automatic fixes
        fixer.apply_fixes()

        # Show manual steps
        fixer.show_manual_steps()

        print("\n" + "=" * 40)
        print("🔄 RUN THIS SCRIPT AGAIN after applying manual steps")
        print("=" * 40)
        return 1
    else:
        print("\n✅ Ready to start Discord bot!")
        print("   python src/discord_commander/unified_discord_bot.py")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)</content>
</xai:function_call<parameter name="path">D:\Agent_Cellphone_V2_Repository\scripts\fix_discord_bot.py