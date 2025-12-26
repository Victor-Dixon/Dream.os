#!/usr/bin/env python3
"""
GA4/Pixel Analytics Deployment Automation
=========================================

<!-- SSOT Domain: infrastructure -->

Automated deployment script for GA4 and Facebook Pixel analytics code
across all 4 revenue engine websites.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps)
Date: 2025-12-25
Coordination: Agent-5 (Analytics validation)
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Revenue engine websites
REVENUE_SITES = [
    "freerideinvestor.com",
    "dadudekc.com",
    "crosbyultimateevents.com",
    "tradingrobotplug.com"
]

# Website directories (adjust paths as needed)
WEBSITES_DIR = Path("D:/websites/websites")
TEMPLATES_DIR = project_root / "agent_workspaces" / "Agent-5"


class AnalyticsDeployer:
    """Deploy GA4/Pixel analytics code to WordPress sites."""

    def __init__(self, websites_dir: Path = None):
        """Initialize deployer."""
        self.websites_dir = websites_dir or WEBSITES_DIR
        self.templates_dir = TEMPLATES_DIR
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results: List[Dict] = []

    def load_template(self) -> str:
        """Load combined GA4/Pixel template."""
        template_file = self.templates_dir / "GA4_PIXEL_CODE_TEMPLATES.md"
        
        if not template_file.exists():
            logger.error(f"Template file not found: {template_file}")
            return ""
        
        # Extract the combined template from markdown
        content = template_file.read_text(encoding="utf-8")
        
        # Find the combined template section
        start_marker = "## Combined Template (GA4 + Pixel)"
        end_marker = "---"
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            logger.error("Combined template section not found")
            return ""
        
        # Find the code block
        code_start = content.find("```php", start_idx)
        if code_start == -1:
            logger.error("PHP code block not found")
            return ""
        
        code_start += len("```php\n")
        code_end = content.find("```", code_start)
        if code_end == -1:
            logger.error("Code block not closed")
            return ""
        
        template_code = content[code_start:code_end].strip()
        return template_code

    def find_functions_php(self, site_dir: Path) -> Optional[Path]:
        """Find functions.php file for WordPress site."""
        possible_locations = [
            site_dir / "functions.php",
            site_dir / "wp-content" / "themes" / "functions.php",
            site_dir / "wp" / "wp-content" / "themes" / "functions.php",
        ]
        
        # Try to find active theme
        themes_dirs = [
            site_dir / "wp-content" / "themes",
            site_dir / "wp" / "wp-content" / "themes",
        ]
        
        for themes_dir in themes_dirs:
            if themes_dir.exists():
                # Find active theme (heuristic: look for theme with site name)
                site_name = site_dir.name.split('.')[0]
                for theme_dir in themes_dir.iterdir():
                    if theme_dir.is_dir():
                        theme_functions = theme_dir / "functions.php"
                        if theme_functions.exists():
                            return theme_functions
        
        # Fallback to root functions.php
        for location in possible_locations:
            if location.exists():
                return location
        
        return None

    def deploy_to_site(
        self, site_name: str, template_code: str, ga4_id: str = "", pixel_id: str = ""
    ) -> Dict:
        """Deploy analytics code to a single site."""
        logger.info(f"🔧 Deploying analytics to {site_name}...")
        
        result = {
            "site": site_name,
            "status": "pending",
            "timestamp": datetime.now().isoformat(),
            "errors": [],
            "warnings": []
        }
        
        site_dir = self.websites_dir / site_name
        if not site_dir.exists():
            result["status"] = "error"
            result["errors"].append(f"Site directory not found: {site_dir}")
            return result
        
        functions_php = self.find_functions_php(site_dir)
        if not functions_php:
            result["status"] = "error"
            result["errors"].append("functions.php not found")
            return result
        
        try:
            # Read existing functions.php
            existing_content = functions_php.read_text(encoding="utf-8")
            
            # Check if analytics already deployed
            if "add_analytics_tracking" in existing_content:
                result["warnings"].append("Analytics function already exists")
                result["status"] = "skipped"
                return result
            
            # Customize template with site name
            customized_code = template_code.replace("{SITE_NAME}", site_name)
            
            # Add analytics function to functions.php
            new_content = existing_content.rstrip() + "\n\n" + customized_code + "\n"
            
            # Create backup
            backup_file = functions_php.parent / f"functions.php.backup_{self.timestamp}"
            backup_file.write_text(existing_content, encoding="utf-8")
            logger.info(f"   📦 Backup created: {backup_file.name}")
            
            # Write updated functions.php
            functions_php.write_text(new_content, encoding="utf-8")
            
            # Update wp-config.php with IDs if provided
            if ga4_id or pixel_id:
                self.update_wp_config(site_dir, ga4_id, pixel_id, result)
            
            result["status"] = "success"
            result["functions_php"] = str(functions_php)
            result["backup"] = str(backup_file)
            logger.info(f"   ✅ Analytics code deployed to {site_name}")
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            logger.error(f"   ❌ Error deploying to {site_name}: {e}")
        
        return result

    def update_wp_config(
        self, site_dir: Path, ga4_id: str, pixel_id: str, result: Dict
    ) -> None:
        """Update wp-config.php with analytics IDs."""
        wp_config_paths = [
            site_dir / "wp-config.php",
            site_dir / "wp" / "wp-config.php",
        ]
        
        wp_config = None
        for path in wp_config_paths:
            if path.exists():
                wp_config = path
                break
        
        if not wp_config:
            result["warnings"].append("wp-config.php not found, IDs must be configured manually")
            return
        
        try:
            content = wp_config.read_text(encoding="utf-8")
            
            # Check if constants already exist
            if "GA4_MEASUREMENT_ID" in content:
                result["warnings"].append("GA4_MEASUREMENT_ID already in wp-config.php")
            else:
                # Add GA4 constant before "That's all, stop editing!"
                marker = "/* That's all, stop editing!"
                if marker in content:
                    ga4_line = f"define('GA4_MEASUREMENT_ID', '{ga4_id}');\n"
                    content = content.replace(marker, ga4_line + marker)
                else:
                    content += f"\ndefine('GA4_MEASUREMENT_ID', '{ga4_id}');\n"
            
            if "FACEBOOK_PIXEL_ID" in content:
                result["warnings"].append("FACEBOOK_PIXEL_ID already in wp-config.php")
            else:
                marker = "/* That's all, stop editing!"
                if marker in content:
                    pixel_line = f"define('FACEBOOK_PIXEL_ID', '{pixel_id}');\n"
                    content = content.replace(marker, pixel_line + marker)
                else:
                    content += f"\ndefine('FACEBOOK_PIXEL_ID', '{pixel_id}');\n"
            
            # Create backup
            backup = wp_config.parent / f"wp-config.php.backup_{self.timestamp}"
            backup.write_bytes(wp_config.read_bytes())
            
            # Write updated config
            wp_config.write_text(content, encoding="utf-8")
            logger.info(f"   ✅ wp-config.php updated with analytics IDs")
            
        except Exception as e:
            result["warnings"].append(f"Could not update wp-config.php: {e}")

    def deploy_all(self, ga4_ids: Dict[str, str] = None, pixel_ids: Dict[str, str] = None) -> Dict:
        """Deploy analytics to all revenue engine sites."""
        logger.info("🚀 Starting GA4/Pixel analytics deployment...")
        
        template_code = self.load_template()
        if not template_code:
            return {
                "status": "error",
                "error": "Failed to load template",
                "sites": []
            }
        
        ga4_ids = ga4_ids or {}
        pixel_ids = pixel_ids or {}
        
        for site in REVENUE_SITES:
            ga4_id = ga4_ids.get(site, "")
            pixel_id = pixel_ids.get(site, "")
            
            result = self.deploy_to_site(site, template_code, ga4_id, pixel_id)
            self.results.append(result)
        
        # Generate report
        success_count = sum(1 for r in self.results if r["status"] == "success")
        error_count = sum(1 for r in self.results if r["status"] == "error")
        skipped_count = sum(1 for r in self.results if r["status"] == "skipped")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": "complete",
            "total_sites": len(REVENUE_SITES),
            "success": success_count,
            "errors": error_count,
            "skipped": skipped_count,
            "sites": self.results
        }
        
        return report

    def generate_report(self, report: Dict) -> Path:
        """Generate deployment report."""
        reports_dir = project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"ga4_pixel_deployment_{self.timestamp}.json"
        report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
        
        logger.info(f"📊 Report generated: {report_file}")
        return report_file


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Deploy GA4/Pixel analytics to revenue engine websites"
    )
    parser.add_argument(
        "--websites-dir",
        type=str,
        default=str(WEBSITES_DIR),
        help="Path to websites directory"
    )
    parser.add_argument(
        "--ga4-ids",
        type=str,
        help="JSON file with GA4 Measurement IDs per site"
    )
    parser.add_argument(
        "--pixel-ids",
        type=str,
        help="JSON file with Facebook Pixel IDs per site"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run (don't actually deploy)"
    )
    
    args = parser.parse_args()
    
    # Load IDs if provided
    ga4_ids = {}
    pixel_ids = {}
    
    if args.ga4_ids:
        with open(args.ga4_ids, 'r') as f:
            ga4_ids = json.load(f)
    
    if args.pixel_ids:
        with open(args.pixel_ids, 'r') as f:
            pixel_ids = json.load(f)
    
    deployer = AnalyticsDeployer(Path(args.websites_dir))
    
    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - No changes will be made")
        template = deployer.load_template()
        if template:
            logger.info("✅ Template loaded successfully")
            for site in REVENUE_SITES:
                functions_php = deployer.find_functions_php(Path(args.websites_dir) / site)
                if functions_php:
                    logger.info(f"   ✅ {site}: functions.php found at {functions_php}")
                else:
                    logger.warning(f"   ⚠️  {site}: functions.php not found")
        return 0
    
    report = deployer.deploy_all(ga4_ids, pixel_ids)
    report_file = deployer.generate_report(report)
    
    print(f"\n✅ Deployment complete!")
    print(f"📊 Success: {report['success']}/{report['total_sites']}")
    print(f"❌ Errors: {report['errors']}")
    print(f"⏭️  Skipped: {report['skipped']}")
    print(f"📝 Report: {report_file}")
    
    return 0 if report['errors'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

