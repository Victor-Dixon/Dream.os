#!/usr/bin/env python3
"""
WordPress Blog Auditor
======================

<!-- SSOT Domain: web -->

Comprehensive WordPress blog audit tool that:
- Validates blog functionality via WordPress REST API
- Checks content integrity (posts exist, are accessible, have content)
- Verifies REST API availability and authentication
- Generates detailed audit reports

V2 Compliance: < 300 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests
from requests.auth import HTTPBasicAuth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WordPressBlogAuditor:
    """Audits WordPress blog functionality and content integrity."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize auditor with config path."""
        self.config_path = config_path or self._find_config()
        self.sites: Dict[str, Dict[str, Any]] = {}
        self.results: List[Dict[str, Any]] = []

    def _find_config(self) -> Path:
        """Find site configuration file."""
        # Try multiple possible locations
        possible_paths = [
            Path("configs/site_configs.json"),
            Path("../websites/configs/site_configs.json"),
            Path("../../websites/configs/site_configs.json"),
            Path(__file__).parent.parent.parent / "websites" / "configs" / "site_configs.json"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # Default fallback
        return Path("configs/site_configs.json")

    def load_config(self) -> bool:
        """Load site configurations."""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config not found: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.sites = json.load(f)
            
            logger.info(f"Loaded {len(self.sites)} site configurations")
            return True
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return False

    def has_valid_credentials(self, site_config: Dict[str, Any]) -> bool:
        """Check if site has valid REST API credentials."""
        rest_api = site_config.get("rest_api", {})
        username = rest_api.get("username", "").strip()
        app_password = rest_api.get("app_password", "").strip()
        
        if not username or not app_password:
            return False
        
        # Check for placeholder values
        if "REPLACE" in app_password.upper() or app_password == "":
            return False
        
        return True

    def test_rest_api_availability(self, site_url: str) -> bool:
        """Test if WordPress REST API is accessible."""
        try:
            api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2"
            response = requests.get(api_url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"REST API test failed for {site_url}: {e}")
            return False

    def get_blog_posts(self, site_url: str, auth: HTTPBasicAuth) -> Optional[List[Dict]]:
        """Retrieve blog posts from WordPress REST API."""
        try:
            api_url = f"{site_url.rstrip('/')}/wp-json/wp/v2/posts?per_page=10"
            response = requests.get(api_url, auth=auth, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.warning(f"Authentication failed for {site_url}")
                return None
            else:
                logger.warning(f"Unexpected status {response.status_code} for {site_url}")
                return None
        except Exception as e:
            logger.error(f"Failed to get posts from {site_url}: {e}")
            return None

    def validate_post_content(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Validate individual post content integrity."""
        issues = []
        
        # Check required fields
        if not post.get("id"):
            issues.append("Missing post ID")
        if not post.get("title", {}).get("rendered"):
            issues.append("Missing or empty title")
        if not post.get("content", {}).get("rendered"):
            issues.append("Missing or empty content")
        if not post.get("link"):
            issues.append("Missing post URL")
        
        # Check content length
        content = post.get("content", {}).get("rendered", "")
        if len(content) < 50:
            issues.append("Content too short (may be empty or placeholder)")
        
        # Check status
        status = post.get("status", "")
        if status not in ["publish", "draft", "private"]:
            issues.append(f"Unusual status: {status}")
        
        return {
            "post_id": post.get("id"),
            "title": post.get("title", {}).get("rendered", "Untitled"),
            "status": status,
            "has_issues": len(issues) > 0,
            "issues": issues
        }

    def audit_site(self, site_name: str, site_config: Dict[str, Any]) -> Dict[str, Any]:
        """Audit a single WordPress site."""
        logger.info(f"Auditing {site_name}...")
        
        site_url = site_config.get("site_url", "")
        rest_api = site_config.get("rest_api", {})
        
        result = {
            "site": site_name,
            "site_url": site_url,
            "status": "UNKNOWN",
            "rest_api_available": False,
            "has_credentials": False,
            "authenticated": False,
            "posts_count": 0,
            "posts_validated": 0,
            "posts_with_issues": 0,
            "issues": [],
            "recommendations": []
        }
        
        # Test REST API availability
        result["rest_api_available"] = self.test_rest_api_availability(site_url)
        if not result["rest_api_available"]:
            result["status"] = "REST_API_UNAVAILABLE"
            result["issues"].append("WordPress REST API not accessible")
            result["recommendations"].append("Verify WordPress installation and REST API is enabled")
            return result
        
        # Check credentials
        result["has_credentials"] = self.has_valid_credentials(site_config)
        if not result["has_credentials"]:
            result["status"] = "NO_CREDENTIALS"
            result["issues"].append("Missing or invalid REST API credentials")
            result["recommendations"].append("Add valid WordPress application password to site config")
            return result
        
        # Attempt authentication and retrieve posts
        username = rest_api.get("username", "")
        app_password = rest_api.get("app_password", "")
        auth = HTTPBasicAuth(username, app_password)
        
        posts = self.get_blog_posts(site_url, auth)
        if posts is None:
            result["status"] = "AUTH_FAILED"
            result["issues"].append("Failed to authenticate or retrieve posts")
            result["recommendations"].append("Verify WordPress credentials are correct")
            return result
        
        result["authenticated"] = True
        result["posts_count"] = len(posts)
        
        # Validate posts
        validated_posts = []
        for post in posts:
            validation = self.validate_post_content(post)
            validated_posts.append(validation)
            if validation["has_issues"]:
                result["posts_with_issues"] += 1
            else:
                result["posts_validated"] += 1
        
        # Determine overall status
        if result["posts_count"] == 0:
            result["status"] = "NO_POSTS"
            result["issues"].append("No blog posts found")
            result["recommendations"].append("Create blog posts or verify post visibility settings")
        elif result["posts_with_issues"] > 0:
            result["status"] = "CONTENT_ISSUES"
            result["issues"].append(f"{result['posts_with_issues']} posts have content issues")
        else:
            result["status"] = "HEALTHY"
        
        result["post_details"] = validated_posts[:5]  # Include first 5 for report
        
        return result

    def run_audit(self) -> int:
        """Run audit on all configured sites."""
        if not self.load_config():
            logger.error("Failed to load configuration")
            return 1
        
        logger.info(f"Starting WordPress blog audit for {len(self.sites)} sites...")
        
        for site_name, site_config in self.sites.items():
            try:
                result = self.audit_site(site_name, site_config)
                self.results.append(result)
            except Exception as e:
                logger.error(f"Error auditing {site_name}: {e}")
                self.results.append({
                    "site": site_name,
                    "status": "ERROR",
                    "issues": [f"Audit failed: {str(e)}"]
                })
        
        self.generate_report()
        return 0

    def generate_report(self) -> None:
        """Generate audit report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"WORDPRESS_BLOG_AUDIT_{timestamp}.md")
        
        healthy_count = sum(1 for r in self.results if r.get("status") == "HEALTHY")
        total_posts = sum(r.get("posts_count", 0) for r in self.results)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🔍 WordPress Blog Audit Report\n\n")
            f.write(f"**Audit Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Sites Audited**: {len(self.results)}\n\n")
            
            f.write("## 📊 Audit Summary\n")
            f.write(f"- ✅ **Healthy**: {healthy_count} sites\n")
            f.write(f"- 📝 **Total Posts**: {total_posts} posts\n")
            f.write(f"- ⚠️  **Issues Found**: {len(self.results) - healthy_count} sites\n\n")
            
            f.write("## 🌐 Site Details\n\n")
            for result in self.results:
                status_emoji = "✅" if result.get("status") == "HEALTHY" else "⚠️"
                f.write(f"### {status_emoji} {result['site']}\n")
                f.write(f"**Status**: {result.get('status', 'UNKNOWN')}\n")
                f.write(f"**URL**: {result.get('site_url', 'N/A')}\n")
                
                if result.get("posts_count") is not None:
                    f.write(f"**Posts**: {result['posts_count']} total, "
                           f"{result['posts_validated']} validated, "
                           f"{result['posts_with_issues']} with issues\n")
                
                if result.get("issues"):
                    f.write(f"**Issues**:\n")
                    for issue in result["issues"]:
                        f.write(f"  - {issue}\n")
                
                if result.get("recommendations"):
                    f.write(f"**Recommendations**:\n")
                    for rec in result["recommendations"]:
                        f.write(f"  - {rec}\n")
                
                f.write("\n")
        
        logger.info(f"Report generated: {report_path}")
        print(f"\n✅ WordPress blog audit complete!")
        print(f"📊 Results: {healthy_count}/{len(self.results)} sites healthy")
        print(f"📄 Report: {report_path}")


def main() -> int:
    """Main entry point."""
    auditor = WordPressBlogAuditor()
    return auditor.run_audit()


if __name__ == "__main__":
    sys.exit(main())

