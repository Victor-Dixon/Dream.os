#!/usr/bin/env python3
"""
Deploy Build-In-Public Sites and Fix UTF-8 Encoding Issues
=========================================================

This script handles deployment of dadudekc.com and freerideinvestor.com
and addresses UTF-8 encoding issues across all sites.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-08
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
import shutil

# Setup logging - will be configured in class init
pass
logger = logging.getLogger(__name__)

class BuildInPublicDeployer:
    """Handles deployment of Build-In-Public sites and encoding fixes."""

    def __init__(self, repo_root=None):
        self.repo_root = Path(repo_root or Path(__file__).parent.parent)
        # Ensure logs directory exists
        self.logs_dir = self.repo_root / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        # Setup logging
        log_file = self.logs_dir / f'build_in_public_deployment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        self.sites = ["dadudekc.com", "freerideinvestor.com"]

    def deploy_all_sites(self):
        """Deploy all Build-In-Public sites."""
        logger.info("Starting Build-In-Public deployment")
        logger.info(f"Sites to deploy: {', '.join(self.sites)}")

        results = {}
        for site in self.sites:
            try:
                logger.info(f"Deploying {site}...")
                result = self.deploy_site(site)
                results[site] = result
                logger.info(f"✅ {site} deployment preparation complete")
            except Exception as e:
                logger.error(f"❌ {site} deployment failed: {e}")
                results[site] = {"error": str(e)}

        self.print_summary(results)
        return results

    def deploy_site(self, site_name):
        """Deploy a single site and fix encoding issues."""
        site_dir = self.repo_root / "sites" / site_name

        if not site_dir.exists():
            raise FileNotFoundError(f"Site directory not found: {site_dir}")

        logger.info(f"Processing {site_name}...")

        results = {
            "wp_config_updated": False,
            "encoding_issues_fixed": 0,
            "critical_files_checked": {},
            "theme_files_count": 0
        }

        # Fix wp-config.php charset
        results["wp_config_updated"] = self.fix_wp_config_charset(site_dir / "wp" / "wp-config.php")

        # Fix encoding issues in PHP files
        results["encoding_issues_fixed"] = self.fix_php_encoding_issues(site_dir)

        # Check theme files
        theme_results = self.check_theme_files(site_dir / "wp" / "wp-content" / "themes")
        results.update(theme_results)

        return results

    def fix_wp_config_charset(self, wp_config_path):
        """Ensure wp-config.php has correct UTF-8 charset settings."""
        if not wp_config_path.exists():
            logger.warning(f"wp-config.php not found: {wp_config_path}")
            return False

        logger.info("Checking wp-config.php charset configuration...")

        try:
            with open(wp_config_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check for DB_CHARSET
            charset_updated = False
            collate_updated = False

            if "define('DB_CHARSET', 'utf8mb4')" not in content:
                if "define('DB_CHARSET'" in content:
                    # Update existing charset
                    content = content.replace(
                        content[content.find("define('DB_CHARSET'"):content.find("');", content.find("define('DB_CHARSET'")) + 3],
                        "define('DB_CHARSET', 'utf8mb4');"
                    )
                else:
                    # Add charset after DB_NAME
                    db_name_pos = content.find("define('DB_NAME'")
                    if db_name_pos != -1:
                        end_pos = content.find("');", db_name_pos) + 3
                        content = content[:end_pos] + "\ndefine('DB_CHARSET', 'utf8mb4');" + content[end_pos:]

                charset_updated = True
                logger.info("✅ Updated DB_CHARSET to utf8mb4")

            # Check for DB_COLLATE
            if "define('DB_COLLATE'" in content and "utf8mb4_unicode_ci" not in content:
                # Update collation to empty string for better compatibility
                content = content.replace(
                    content[content.find("define('DB_COLLATE'"):content.find("');", content.find("define('DB_COLLATE'")) + 3],
                    "define('DB_COLLATE', '');"
                )
                collate_updated = True
                logger.info("✅ Updated DB_COLLATE for UTF-8 compatibility")

            # Write back if changes were made
            if charset_updated or collate_updated:
                with open(wp_config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info("✅ wp-config.php charset configuration updated")
                return True
            else:
                logger.info("✅ wp-config.php charset already correctly configured")
                return False

        except Exception as e:
            logger.error(f"Error updating wp-config.php: {e}")
            return False

    def fix_php_encoding_issues(self, site_dir):
        """Check and fix encoding issues in PHP files."""
        logger.info("Checking PHP files for encoding issues...")

        php_files = list(site_dir.rglob("*.php"))
        fixed_count = 0

        for php_file in php_files:
            try:
                # Try to read as UTF-8
                with open(php_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # If successful, file is already UTF-8
                continue

            except UnicodeDecodeError:
                # File has encoding issues
                logger.warning(f"Encoding issue detected in: {php_file}")

                try:
                    # Try to read as latin-1 and convert to UTF-8
                    with open(php_file, 'r', encoding='latin-1') as f:
                        content = f.read()

                    # Write back as UTF-8
                    with open(php_file, 'w', encoding='utf-8') as f:
                        f.write(content)

                    fixed_count += 1
                    logger.info(f"✅ Fixed encoding for: {php_file}")

                except Exception as e:
                    logger.error(f"Could not fix encoding for {php_file}: {e}")

        if fixed_count == 0:
            logger.info("✅ No encoding issues found in PHP files")
        else:
            logger.info(f"✅ Fixed encoding issues in {fixed_count} PHP files")

        return fixed_count

    def check_theme_files(self, theme_dir):
        """Check theme files for deployment readiness."""
        results = {
            "critical_files_checked": {},
            "theme_files_count": 0
        }

        if not theme_dir.exists():
            logger.warning(f"Theme directory not found: {theme_dir}")
            return results

        logger.info("Checking theme files...")

        # Count theme files
        theme_files = list(theme_dir.rglob("*.php")) + list(theme_dir.rglob("*.css")) + list(theme_dir.rglob("*.js"))
        results["theme_files_count"] = len(theme_files)

        # Check critical files
        critical_files = [
            "front-page.php",
            "page-contact.php",
            "functions.php",
            "index.php"
        ]

        for filename in critical_files:
            file_path = theme_dir / filename
            if file_path.exists():
                results["critical_files_checked"][filename] = True
                logger.info(f"✅ Critical file present: {filename}")
            else:
                results["critical_files_checked"][filename] = False
                logger.warning(f"❌ Critical file missing: {filename}")

        return results

    def print_summary(self, results):
        """Print deployment summary."""
        print("\n" + "="*60)
        print("BUILD-IN-PUBLIC DEPLOYMENT SUMMARY")
        print("="*60)

        total_sites = len(results)
        successful_sites = sum(1 for result in results.values() if "error" not in result)

        print(f"Sites Processed: {total_sites}")
        print(f"Successful: {successful_sites}")
        print(f"Failed: {total_sites - successful_sites}")

        for site, result in results.items():
            print(f"\n{site}:")
            if "error" in result:
                print(f"  ❌ Error: {result['error']}")
            else:
                print(f"  ✅ wp-config updated: {result['wp_config_updated']}")
                print(f"  ✅ Encoding issues fixed: {result['encoding_issues_fixed']}")
                print(f"  ✅ Theme files checked: {result['theme_files_count']}")

                critical_files = result['critical_files_checked']
                present_count = sum(critical_files.values())
                total_count = len(critical_files)
                print(f"  ✅ Critical files: {present_count}/{total_count} present")

        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("1. Deploy files to live servers")
        print("2. Test contact forms and functionality")
        print("3. Monitor for remaining encoding issues")
        print("4. Verify UTF-8 charset in database")
        print("="*60)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Deploy Build-In-Public sites and fix encoding issues")
    parser.add_argument("--site", help="Specific site to deploy (default: all sites)")
    parser.add_argument("--repo-root", help="Repository root directory")

    args = parser.parse_args()

    try:
        deployer = BuildInPublicDeployer(args.repo_root)

        if args.site:
            if args.site not in deployer.sites:
                print(f"Error: Invalid site '{args.site}'. Valid sites: {', '.join(deployer.sites)}")
                sys.exit(1)
            deployer.sites = [args.site]

        results = deployer.deploy_all_sites()

        # Check for errors
        has_errors = any("error" in result for result in results.values())
        if has_errors:
            logger.error("Some deployments had errors")
            sys.exit(1)
        else:
            logger.info("All deployments completed successfully")

    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()