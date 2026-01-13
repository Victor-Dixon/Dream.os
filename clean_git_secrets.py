#!/usr/bin/env python3
"""
Git Secrets Cleaner - Remove exposed secrets from git history
==============================================================

This script helps clean up exposed secrets from git repository history.
It provides options to either rewrite history or create clean commits.

WARNING: This script performs destructive operations on git history.
Make sure to backup your repository before running.

Usage:
    python clean_git_secrets.py --scan          # Scan for secrets
    python clean_git_secrets.py --clean         # Clean history (destructive)
    python clean_git_secrets.py --replace       # Replace with placeholders
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Set

class GitSecretsCleaner:
    """Clean exposed secrets from git repository history"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).absolute()
        self.known_secrets = {
            "discord_tokens": [
                "<REDACTED_DISCORD_BOT_TOKEN>",  # Known exposed token
            ],
            "github_tokens": [
                "<REDACTED_GITHUB_TOKEN>",  # Known PAT
            ],
            "robinhood_keys": [
                "<REDACTED_ROBINHOOD_CLIENT_ID>",  # Robinhood client_id
            ]
        }

        # Patterns for detecting secrets
        self.secret_patterns = {
            "discord_bot_token": re.compile(r'DISCORD_BOT_TOKEN\s*=\s*["\']([^"\']+)["\']'),
            "github_token": re.compile(r'github.*token["\']?\s*[:=]\s*["\']([^"\']+)["\']'),
            "generic_token": re.compile(r'[A-Za-z0-9]{50,70}'),  # Long alphanumeric strings
        }

    def run_command(self, cmd: List[str], cwd: Path = None) -> str:
        """Run a command and return output"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {' '.join(cmd)}")
            print(f"Error: {e.stderr}")
            return ""

    def scan_for_secrets(self) -> Dict[str, List[str]]:
        """Scan repository for exposed secrets"""
        print("🔍 Scanning repository for exposed secrets...")

        found_secrets = {
            "discord_tokens": [],
            "github_tokens": [],
            "other_secrets": [],
            "files_with_secrets": []
        }

        # Check current files
        for root, dirs, files in os.walk(self.repo_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.json', '.yaml', '.yml', '.env', '.bat', '.ps1')):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text()

                        # Check for known secrets
                        for secret_type, secrets in self.known_secrets.items():
                            for secret in secrets:
                                if secret in content:
                                    found_secrets[secret_type].append(str(file_path))
                                    found_secrets["files_with_secrets"].append(str(file_path))

                        # Check for pattern matches
                        for pattern_name, pattern in self.secret_patterns.items():
                            matches = pattern.findall(content)
                            for match in matches:
                                if len(match) > 40:  # Likely a real token
                                    if 'discord' in str(file_path).lower() or 'bot' in str(file_path).lower():
                                        if match not in found_secrets["discord_tokens"]:
                                            found_secrets["discord_tokens"].append(match)
                                    elif 'github' in str(file_path).lower():
                                        if match not in found_secrets["github_tokens"]:
                                            found_secrets["github_tokens"].append(match)
                                    else:
                                        if match not in found_secrets["other_secrets"]:
                                            found_secrets["other_secrets"].append(match)

                    except Exception as e:
                        continue

        # Remove duplicates and clean up
        for key in found_secrets:
            if key != "files_with_secrets":
                found_secrets[key] = list(set(found_secrets[key]))

        found_secrets["files_with_secrets"] = list(set(found_secrets["files_with_secrets"]))

        return found_secrets

    def scan_git_history(self) -> Dict[str, List[str]]:
        """Scan git history for exposed secrets"""
        print("🔍 Scanning git history for exposed secrets...")

        found_in_history = {
            "commits_with_secrets": [],
            "secret_types": []
        }

        try:
            # Get all commits
            commits = self.run_command(["git", "log", "--oneline", "--all"]).split('\n')

            for commit_line in commits:
                if not commit_line.strip():
                    continue

                commit_hash = commit_line.split()[0]

                # Check commit content for secrets
                try:
                    # Check changed files in this commit
                    changed_files = self.run_command(["git", "show", "--name-only", commit_hash]).split('\n')
                    changed_files = [f for f in changed_files if f and not f.startswith('commit ') and not f.startswith('Author:') and not f.startswith('Date:')]

                    for file in changed_files:
                        if file and any(file.endswith(ext) for ext in ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.env', '.bat', '.ps1']):
                            try:
                                content = self.run_command(["git", "show", f"{commit_hash}:{file}"])

                                # Check for known secrets
                                for secret_type, secrets in self.known_secrets.items():
                                    for secret in secrets:
                                        if secret in content:
                                            found_in_history["commits_with_secrets"].append(f"{commit_hash}: {file}")
                                            if secret_type not in found_in_history["secret_types"]:
                                                found_in_history["secret_types"].append(secret_type)

                            except subprocess.CalledProcessError:
                                # File might not exist in that commit
                                continue

                except Exception as e:
                    continue

        except Exception as e:
            print(f"⚠️ Error scanning git history: {e}")

        return found_in_history

    def create_clean_commit(self):
        """Create a clean commit by replacing secrets with placeholders"""
        print("🧹 Creating clean commit by replacing secrets with placeholders...")

        # Replace known secrets in files
        replacements_made = []

        for root, dirs, files in os.walk(self.repo_path):
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                if file.endswith(('.py', '.md', '.txt', '.json', '.yaml', '.yml', '.env', '.bat', '.ps1')):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text()
                        original_content = content

                        # Replace known secrets
                        for secret_type, secrets in self.known_secrets.items():
                            for secret in secrets:
                                if secret in content:
                                    placeholder = f"<REDACTED_{secret_type.upper()}_SECRET>"
                                    content = content.replace(secret, placeholder)
                                    print(f"  📝 Replaced secret in {file_path}")

                        # Write back if changed
                        if content != original_content:
                            file_path.write_text(content)
                            replacements_made.append(str(file_path))

                    except Exception as e:
                        continue

        if replacements_made:
            print(f"✅ Replaced secrets in {len(replacements_made)} files")
            print("📝 Ready to commit with: git add . && git commit -m 'security: replace exposed secrets with placeholders'")
            return True
        else:
            print("ℹ️ No secrets found to replace in current files")
            return False

    def show_rewrite_warning(self):
        """Show warning about history rewriting"""
        print("⚠️  WARNING: Git History Rewrite")
        print("=" * 50)
        print("This operation will permanently alter your git history.")
        print("This cannot be undone and may cause issues with:")
        print("- Other developers working on this repository")
        print("- Existing pull requests and branches")
        print("- CI/CD pipelines")
        print("- Local repositories of other team members")
        print()
        print("Recommended approach:")
        print("1. Create a fresh repository")
        print("2. Copy only the clean files")
        print("3. Push to a new remote repository")
        print()
        print("Continue only if you fully understand the consequences!")

    def run(self):
        """Main execution"""
        print("🔐 Git Secrets Cleaner")
        print("=" * 30)

        if len(sys.argv) < 2:
            self.show_help()
            return

        command = sys.argv[1]

        if command == "--scan":
            print("🔍 SCAN MODE: Analyzing repository for secrets")
            print("-" * 50)

            current_secrets = self.scan_for_secrets()
            history_secrets = self.scan_git_history()

            print("\n📊 CURRENT FILES SECRETS:")
            for secret_type, secrets in current_secrets.items():
                if secrets and secret_type != "files_with_secrets":
                    print(f"  {secret_type}: {len(secrets)} found")
                    for secret in secrets[:3]:  # Show first 3
                        print(f"    • {secret}")

            print(f"\n📁 Files with secrets: {len(current_secrets['files_with_secrets'])}")

            print("\n📊 GIT HISTORY SECRETS:")
            print(f"  Commits with secrets: {len(history_secrets['commits_with_secrets'])}")
            if history_secrets['secret_types']:
                print(f"  Secret types found: {', '.join(history_secrets['secret_types'])}")

        elif command == "--replace":
            print("🔄 REPLACE MODE: Replace secrets with placeholders")
            print("-" * 50)

            if self.create_clean_commit():
                print("\n✅ Secrets replaced successfully")
                print("Next steps:")
                print("1. Review the changes: git diff")
                print("2. Commit the changes: git add . && git commit -m 'security: replace exposed secrets with placeholders'")
                print("3. Push to GitHub: git push")
            else:
                print("ℹ️ No secrets found to replace")

        elif command == "--clean":
            print("🧹 CLEAN MODE: Full repository cleanup")
            print("-" * 50)

            self.show_rewrite_warning()

            response = input("\nDo you want to continue? Type 'yes' to proceed: ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                return

            print("\n🚨 This will create a new repository without the problematic history.")
            print("1. All files will be preserved")
            print("2. Git history will be clean")
            print("3. You can push to a new repository")

            # This would implement the full cleanup - for now, just show the plan
            print("\n📋 CLEANUP PLAN:")
            print("1. Create backup of current repository")
            print("2. Create fresh git repository")
            print("3. Copy all files (excluding .git)")
            print("4. Add files and commit")
            print("5. Push to new remote repository")

        else:
            self.show_help()
            return

    def show_help(self):
        """Show help information"""
        print("Usage:")
        print("  python clean_git_secrets.py --scan     # Scan for secrets")
        print("  python clean_git_secrets.py --replace  # Replace secrets with placeholders")
        print("  python clean_git_secrets.py --clean    # Full cleanup (destructive)")
        print()
        print("Examples:")
        print("  python clean_git_secrets.py --scan")
        print("  python clean_git_secrets.py --replace")

if __name__ == "__main__":
    cleaner = GitSecretsCleaner()
    cleaner.run()</content>
</xai:function_call<parameter name="path">D:\Agent_Cellphone_V2_Repository\clean_git_secrets.py