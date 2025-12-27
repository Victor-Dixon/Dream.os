#!/usr/bin/env python3
"""
SEO Integration Validation Tool
==============================

Validates SEO elements (meta descriptions, title tags, H1 headings) across websites
for integration testing and grade card improvements.

V2 Compliance | Author: Agent-1 | Date: 2025-12-27
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Constants
TIMEOUT = 10
RESULTS_DIR = project_root / "agent_workspaces" / "Agent-1" / "seo_validation_tests"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Website list from audit
WEBSITES = [
    "https://ariajet.site",
    "https://crosbyultimateevents.com",
    "https://digitaldreamscape.site",
    "https://freerideinvestor.com",
    "https://prismblossom.online",
    "https://southwestsecret.com",
    "https://tradingrobotplug.com",
    "https://weareswarm.online",
    "https://weareswarm.site",
    "https://dadudekc.com"
]


class SEOValidator:
    """Validates SEO elements across websites."""
    
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse page content."""
        try:
            response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            return None
        except Exception as e:
            print(f"⚠️  Error fetching {url}: {e}")
            return None
    
    def validate_meta_description(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate meta description."""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc:
            return {
                "status": "FAIL",
                "issue": "Missing meta description",
                "recommendation": "Add <meta name='description' content='...'>"
            }
        
        content = meta_desc.get('content', '')
        if not content or len(content.strip()) == 0:
            return {
                "status": "FAIL",
                "issue": "Empty meta description",
                "recommendation": "Add content to meta description"
            }
        
        if len(content) < 120:
            return {
                "status": "WARN",
                "issue": f"Meta description too short ({len(content)} chars, recommended 120-160)",
                "content": content[:100] + "..." if len(content) > 100 else content
            }
        
        if len(content) > 160:
            return {
                "status": "WARN",
                "issue": f"Meta description too long ({len(content)} chars, recommended 120-160)",
                "content": content[:100] + "..."
            }
        
        return {
            "status": "PASS",
            "content": content[:100] + "..." if len(content) > 100 else content,
            "length": len(content)
        }
    
    def validate_title_tag(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate title tag."""
        title_tag = soup.find('title')
        
        if not title_tag:
            return {
                "status": "FAIL",
                "issue": "Missing title tag",
                "recommendation": "Add <title>...</title>"
            }
        
        title_text = title_tag.get_text(strip=True) if title_tag else ""
        
        if not title_text:
            return {
                "status": "FAIL",
                "issue": "Empty title tag",
                "recommendation": "Add text to title tag"
            }
        
        if len(title_text) < 30:
            return {
                "status": "WARN",
                "issue": f"Title too short ({len(title_text)} chars, recommended 30-60)",
                "title": title_text
            }
        
        if len(title_text) > 60:
            return {
                "status": "WARN",
                "issue": f"Title too long ({len(title_text)} chars, recommended 30-60)",
                "title": title_text[:60] + "..."
            }
        
        return {
            "status": "PASS",
            "title": title_text,
            "length": len(title_text)
        }
    
    def validate_h1_headings(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Validate H1 headings."""
        h1_tags = soup.find_all('h1')
        
        if len(h1_tags) == 0:
            return {
                "status": "FAIL",
                "issue": "No H1 heading found",
                "recommendation": "Add one H1 heading per page"
            }
        
        if len(h1_tags) > 1:
            return {
                "status": "WARN",
                "issue": f"Multiple H1 headings found ({len(h1_tags)}), recommended: 1 per page",
                "count": len(h1_tags),
                "headings": [h1.get_text(strip=True)[:50] for h1 in h1_tags[:3]]
            }
        
        h1_text = h1_tags[0].get_text(strip=True)
        if not h1_text:
            return {
                "status": "FAIL",
                "issue": "H1 heading is empty",
                "recommendation": "Add text to H1 heading"
            }
        
        return {
            "status": "PASS",
            "heading": h1_text[:100] + "..." if len(h1_text) > 100 else h1_text,
            "count": 1
        }
    
    def validate_website(self, url: str) -> Dict[str, Any]:
        """Validate SEO elements for a website."""
        print(f"🔍 Validating {url}...")
        
        soup = self.fetch_page(url)
        if not soup:
            return {
                "url": url,
                "status": "ERROR",
                "error": "Could not fetch page"
            }
        
        meta_desc = self.validate_meta_description(soup)
        title = self.validate_title_tag(soup)
        h1 = self.validate_h1_headings(soup)
        
        # Overall status
        statuses = [meta_desc["status"], title["status"], h1["status"]]
        if "FAIL" in statuses:
            overall_status = "FAIL"
        elif "WARN" in statuses:
            overall_status = "WARN"
        else:
            overall_status = "PASS"
        
        result = {
            "url": url,
            "status": overall_status,
            "meta_description": meta_desc,
            "title_tag": title,
            "h1_headings": h1,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results.append(result)
        return result
    
    def validate_all(self) -> List[Dict[str, Any]]:
        """Validate all websites."""
        print(f"🚀 Starting SEO validation for {len(WEBSITES)} websites...\n")
        
        for url in WEBSITES:
            result = self.validate_website(url)
            status_emoji = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARN" else "❌"
            print(f"{status_emoji} {url}: {result['status']}")
        
        return self.results
    
    def save_results(self):
        """Save validation results to JSON."""
        results_file = RESULTS_DIR / f"seo_validation_{self.timestamp}.json"
        summary_file = RESULTS_DIR / f"seo_validation_summary_{self.timestamp}.md"
        
        # Save JSON
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_websites": len(self.results),
                "results": self.results
            }, f, indent=2)
        
        # Generate summary
        summary = self.generate_summary()
        summary_file.write_text(summary, encoding='utf-8')
        
        print(f"\n✅ Results saved:")
        print(f"   JSON: {results_file}")
        print(f"   Summary: {summary_file}")
        
        return results_file, summary_file
    
    def generate_summary(self) -> str:
        """Generate markdown summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        warned = sum(1 for r in self.results if r["status"] == "WARN")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")
        
        summary = f"""# SEO Integration Validation Summary

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Validator**: Agent-1 (Integration & Core Systems Specialist)  
**Tool**: `tools/validate_seo_integration.py`

---

## Overall Results

- **Total Websites**: {total}
- **✅ Passed**: {passed}
- **⚠️ Warnings**: {warned}
- **❌ Failed**: {failed}
- **🔴 Errors**: {errors}

---

## Detailed Results

"""
        
        for result in self.results:
            status_emoji = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARN" else "❌" if result["status"] == "FAIL" else "🔴"
            summary += f"### {status_emoji} {result['url']}\n\n"
            summary += f"**Overall Status**: {result['status']}\n\n"
            
            # Meta description
            md = result["meta_description"]
            summary += f"**Meta Description**: {md['status']}\n"
            if md["status"] != "PASS":
                summary += f"- Issue: {md.get('issue', 'N/A')}\n"
                if "recommendation" in md:
                    summary += f"- Recommendation: {md['recommendation']}\n"
            summary += "\n"
            
            # Title tag
            title = result["title_tag"]
            summary += f"**Title Tag**: {title['status']}\n"
            if title["status"] != "PASS":
                summary += f"- Issue: {title.get('issue', 'N/A')}\n"
                if "recommendation" in title:
                    summary += f"- Recommendation: {title['recommendation']}\n"
            summary += "\n"
            
            # H1 headings
            h1 = result["h1_headings"]
            summary += f"**H1 Headings**: {h1['status']}\n"
            if h1["status"] != "PASS":
                summary += f"- Issue: {h1.get('issue', 'N/A')}\n"
                if "recommendation" in h1:
                    summary += f"- Recommendation: {h1['recommendation']}\n"
            summary += "\n---\n\n"
        
        return summary


def main():
    """Main execution."""
    validator = SEOValidator()
    results = validator.validate_all()
    validator.save_results()
    
    # Print summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    warned = sum(1 for r in results if r["status"] == "WARN")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Passed: {passed}/{len(results)}")
    print(f"   ⚠️  Warnings: {warned}/{len(results)}")
    print(f"   ❌ Failed: {failed}/{len(results)}")


if __name__ == "__main__":
    main()

