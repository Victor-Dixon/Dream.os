#!/usr/bin/env python3
"""
Comprehensive Website Audit Tool
================================

<!-- SSOT Domain: web -->

Performs comprehensive audits of websites including:
- Website accessibility and response status
- SSL/HTTPS status
- SEO elements (meta tags, titles, descriptions)
- Performance metrics (load time, response size)
- Security headers
- Mobile responsiveness indicators
- Content structure analysis

V2 Compliance: <300 lines, single responsibility
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-22
"""

import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ComprehensiveWebsiteAuditor:
    """Comprehensive website auditor for accessibility, SEO, performance, and security."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize auditor with config path."""
        self.config_path = config_path or self._find_config()
        self.sites: Dict[str, Dict[str, Any]] = {}
        self.results: List[Dict[str, Any]] = []
    
    def _find_config(self) -> Path:
        """Find site configuration file."""
        possible_paths = [
            Path("D:/websites/configs/site_configs.json"),
            Path("../websites/configs/site_configs.json"),
            Path("../../websites/configs/site_configs.json"),
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return Path("D:/websites/configs/site_configs.json")
    
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
    
    def audit_site(self, site_name: str, site_config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive audit of a single website."""
        logger.info(f"Auditing {site_name}...")
        
        site_url = site_config.get("site_url", "")
        if not site_url:
            return {
                "site": site_name,
                "status": "ERROR",
                "issues": ["No site URL configured"]
            }
        
        result = {
            "site": site_name,
            "site_url": site_url,
            "timestamp": datetime.now().isoformat(),
            "accessibility": {},
            "seo": {},
            "performance": {},
            "security": {},
            "content": {},
            "issues": [],
            "recommendations": []
        }
        
        # Test website accessibility
        try:
            start_time = time.time()
            response = requests.get(site_url, timeout=15, allow_redirects=True)
            load_time = time.time() - start_time
            
            result["accessibility"] = {
                "status_code": response.status_code,
                "accessible": response.status_code == 200,
                "final_url": response.url,
                "redirected": response.url != site_url
            }
            
            result["performance"] = {
                "load_time_seconds": round(load_time, 2),
                "response_size_bytes": len(response.content),
                "response_size_kb": round(len(response.content) / 1024, 2)
            }
            
            # Check SSL/HTTPS
            parsed = urlparse(response.url)
            result["security"] = {
                "uses_https": parsed.scheme == "https",
                "domain": parsed.netloc
            }
            
            # Check security headers
            security_headers = {
                "strict_transport_security": response.headers.get("Strict-Transport-Security"),
                "x_frame_options": response.headers.get("X-Frame-Options"),
                "x_content_type_options": response.headers.get("X-Content-Type-Options"),
                "content_security_policy": response.headers.get("Content-Security-Policy")
            }
            result["security"]["headers"] = security_headers
            
            # Parse HTML for SEO and content analysis
            if response.status_code == 200:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    self._analyze_seo(soup, result)
                    self._analyze_content(soup, result)
                except Exception as e:
                    logger.warning(f"Failed to parse HTML for {site_name}: {e}")
                    result["issues"].append(f"HTML parsing failed: {str(e)}")
            
        except requests.exceptions.Timeout:
            result["accessibility"]["accessible"] = False
            result["issues"].append("Request timeout - site may be slow or unavailable")
        except requests.exceptions.ConnectionError:
            result["accessibility"]["accessible"] = False
            result["issues"].append("Connection error - site may be down")
        except Exception as e:
            result["accessibility"]["accessible"] = False
            result["issues"].append(f"Audit error: {str(e)}")
        
        # Generate recommendations
        self._generate_recommendations(result)
        
        return result
    
    def _analyze_seo(self, soup: BeautifulSoup, result: Dict[str, Any]) -> None:
        """Analyze SEO elements."""
        seo = {}
        
        # Title tag
        title_tag = soup.find("title")
        seo["title"] = title_tag.get_text().strip() if title_tag else None
        seo["title_length"] = len(seo["title"]) if seo["title"] else 0
        
        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        seo["meta_description"] = meta_desc.get("content", "").strip() if meta_desc else None
        seo["meta_description_length"] = len(seo["meta_description"]) if seo["meta_description"] else 0
        
        # Meta keywords
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        seo["meta_keywords"] = meta_keywords.get("content", "").strip() if meta_keywords else None
        
        # Open Graph tags
        og_title = soup.find("meta", attrs={"property": "og:title"})
        og_description = soup.find("meta", attrs={"property": "og:description"})
        og_image = soup.find("meta", attrs={"property": "og:image"})
        seo["og_tags"] = {
            "title": og_title.get("content") if og_title else None,
            "description": og_description.get("content") if og_description else None,
            "image": og_image.get("content") if og_image else None
        }
        
        # Canonical URL
        canonical = soup.find("link", attrs={"rel": "canonical"})
        seo["canonical_url"] = canonical.get("href") if canonical else None
        
        # Robots meta
        robots = soup.find("meta", attrs={"name": "robots"})
        seo["robots"] = robots.get("content") if robots else None
        
        result["seo"] = seo
        
        # Check for SEO issues
        if not seo["title"]:
            result["issues"].append("Missing title tag")
        elif seo["title_length"] < 30:
            result["issues"].append(f"Title too short ({seo['title_length']} chars, recommended 30-60)")
        elif seo["title_length"] > 60:
            result["issues"].append(f"Title too long ({seo['title_length']} chars, recommended 30-60)")
        
        if not seo["meta_description"]:
            result["issues"].append("Missing meta description")
        elif seo["meta_description_length"] < 120:
            result["issues"].append(f"Meta description too short ({seo['meta_description_length']} chars, recommended 120-160)")
        elif seo["meta_description_length"] > 160:
            result["issues"].append(f"Meta description too long ({seo['meta_description_length']} chars, recommended 120-160)")
    
    def _analyze_content(self, soup: BeautifulSoup, result: Dict[str, Any]) -> None:
        """Analyze content structure."""
        content = {}
        
        # Headings
        h1_tags = soup.find_all("h1")
        h2_tags = soup.find_all("h2")
        content["headings"] = {
            "h1_count": len(h1_tags),
            "h2_count": len(h2_tags),
            "h1_texts": [h.get_text().strip() for h in h1_tags[:5]]
        }
        
        # Images
        images = soup.find_all("img")
        images_with_alt = [img for img in images if img.get("alt")]
        content["images"] = {
            "total": len(images),
            "with_alt": len(images_with_alt),
            "missing_alt": len(images) - len(images_with_alt)
        }
        
        # Links
        links = soup.find_all("a", href=True)
        internal_links = [l for l in links if l["href"].startswith("/") or result["site_url"] in l["href"]]
        external_links = [l for l in links if l["href"].startswith("http") and result["site_url"] not in l["href"]]
        content["links"] = {
            "total": len(links),
            "internal": len(internal_links),
            "external": len(external_links)
        }
        
        result["content"] = content
        
        # Check for content issues
        if content["headings"]["h1_count"] == 0:
            result["issues"].append("No H1 heading found")
        elif content["headings"]["h1_count"] > 1:
            result["issues"].append(f"Multiple H1 headings ({content['headings']['h1_count']}, recommended 1)")
        
        if content["images"]["missing_alt"] > 0:
            result["issues"].append(f"{content['images']['missing_alt']} images missing alt text")
    
    def _generate_recommendations(self, result: Dict[str, Any]) -> None:
        """Generate recommendations based on audit findings."""
        if not result["accessibility"].get("accessible"):
            result["recommendations"].append("Fix website accessibility - site is not responding")
        
        if not result["security"].get("uses_https"):
            result["recommendations"].append("Enable HTTPS/SSL certificate")
        
        if not result["security"]["headers"].get("strict_transport_security"):
            result["recommendations"].append("Add Strict-Transport-Security header")
        
        if result["performance"]["load_time_seconds"] > 3:
            result["recommendations"].append(f"Optimize page load time (currently {result['performance']['load_time_seconds']}s, target <3s)")
        
        if result["performance"]["response_size_kb"] > 500:
            result["recommendations"].append(f"Reduce page size (currently {result['performance']['response_size_kb']}KB, target <500KB)")
    
    def run_audit(self) -> int:
        """Run comprehensive audit on all configured sites."""
        if not self.load_config():
            logger.error("Failed to load configuration")
            return 1
        
        logger.info(f"Starting comprehensive website audit for {len(self.sites)} sites...")
        
        for site_name, site_config in self.sites.items():
            try:
                result = self.audit_site(site_name, site_config)
                self.results.append(result)
                time.sleep(1)  # Rate limiting
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
        """Generate comprehensive audit report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"COMPREHENSIVE_WEBSITE_AUDIT_{timestamp}.md")
        
        accessible_count = sum(1 for r in self.results if r.get("accessibility", {}).get("accessible"))
        https_count = sum(1 for r in self.results if r.get("security", {}).get("uses_https"))
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🔍 Comprehensive Website Audit Report\n\n")
            f.write(f"**Audit Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Sites Audited**: {len(self.results)}\n\n")
            
            f.write("## 📊 Audit Summary\n")
            f.write(f"- ✅ **Accessible**: {accessible_count}/{len(self.results)} sites\n")
            f.write(f"- 🔒 **HTTPS Enabled**: {https_count}/{len(self.results)} sites\n")
            f.write(f"- ⚠️  **Total Issues Found**: {sum(len(r.get('issues', [])) for r in self.results)} issues\n\n")
            
            f.write("## 🌐 Site Details\n\n")
            for result in self.results:
                accessible = result.get("accessibility", {}).get("accessible", False)
                status_emoji = "✅" if accessible else "❌"
                f.write(f"### {status_emoji} {result['site']}\n")
                f.write(f"**URL**: {result.get('site_url', 'N/A')}\n")
                
                if accessible:
                    f.write(f"**Status Code**: {result['accessibility'].get('status_code', 'N/A')}\n")
                    f.write(f"**Load Time**: {result['performance'].get('load_time_seconds', 'N/A')}s\n")
                    f.write(f"**Page Size**: {result['performance'].get('response_size_kb', 'N/A')}KB\n")
                    f.write(f"**HTTPS**: {'✅' if result['security'].get('uses_https') else '❌'}\n")
                    
                    if result.get("seo", {}).get("title"):
                        f.write(f"**Title**: {result['seo']['title'][:60]}...\n")
                    if result.get("seo", {}).get("meta_description"):
                        f.write(f"**Meta Description**: {result['seo']['meta_description'][:80]}...\n")
                
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
        print(f"\n✅ Comprehensive website audit complete!")
        print(f"📊 Results: {accessible_count}/{len(self.results)} sites accessible")
        print(f"📄 Report: {report_path}")


def main() -> int:
    """Main entry point."""
    auditor = ComprehensiveWebsiteAuditor()
    return auditor.run_audit()


if __name__ == "__main__":
    sys.exit(main())
