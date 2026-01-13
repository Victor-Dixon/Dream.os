#!/usr/bin/env python3
"""
Ollama Website Audit Agent Report Generator
===========================================

Generates comprehensive website audit reports using available tools.
Creates actionable reports that agents can follow for website improvements.

Author: Agent-1
Date: 2026-01-12
"""

import asyncio
import json
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path

logger = logging.getLogger(__name__)


class WebsiteAuditorAgent:
    """Website auditor that generates reports agents can follow."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def audit_website(self, url: str) -> Dict[str, Any]:
        """
        Perform comprehensive website audit and generate agent-actionable report.

        Args:
            url: Website URL to audit

        Returns:
            Comprehensive audit report with agent action items
        """
        logger.info(f"🔍 Starting comprehensive audit for: {url}")

        audit_report = {
            "audit_timestamp": datetime.now().isoformat(),
            "website_url": url,
            "domain": urlparse(url).netloc,
            "audit_status": "in_progress",
            "sections": {}
        }

        try:
            # 1. Basic Connectivity & Performance
            audit_report["sections"]["connectivity"] = self._audit_connectivity(url)

            # 2. SEO Analysis
            audit_report["sections"]["seo"] = self._audit_seo(url)

            # 3. Technical Analysis
            audit_report["sections"]["technical"] = self._audit_technical(url)

            # 4. Content Analysis
            audit_report["sections"]["content"] = self._audit_content(url)

            # 5. Security Analysis
            audit_report["sections"]["security"] = self._audit_security(url)

            # 6. Mobile & Accessibility
            audit_report["sections"]["accessibility"] = self._audit_accessibility(url)

            # 7. Generate Agent Action Items
            audit_report["agent_action_items"] = self._generate_agent_actions(audit_report)

            # 8. Overall Assessment
            audit_report["overall_assessment"] = self._generate_overall_assessment(audit_report)

            audit_report["audit_status"] = "completed"
            logger.info(f"✅ Audit completed for: {url}")

        except Exception as e:
            logger.error(f"❌ Audit failed for {url}: {e}")
            audit_report["audit_status"] = "failed"
            audit_report["error"] = str(e)

        return audit_report

    def _audit_connectivity(self, url: str) -> Dict[str, Any]:
        """Audit basic connectivity and performance."""
        result = {
            "status": "unknown",
            "response_time_ms": None,
            "status_code": None,
            "redirects": [],
            "is_https": False,
            "issues": [],
            "recommendations": []
        }

        try:
            start_time = datetime.now()
            response = self.session.get(url, timeout=10, allow_redirects=True)
            end_time = datetime.now()

            result["status_code"] = response.status_code
            result["response_time_ms"] = (end_time - start_time).total_seconds() * 1000
            result["is_https"] = url.startswith("https://")
            result["redirects"] = [r.url for r in response.history] if response.history else []

            # Analyze results
            if response.status_code == 200:
                result["status"] = "healthy"
            elif response.status_code >= 400:
                result["status"] = "error"
                result["issues"].append(f"HTTP {response.status_code} error")
            else:
                result["status"] = "warning"
                result["issues"].append(f"HTTP {response.status_code} status")

            if result["response_time_ms"] > 3000:
                result["issues"].append("Slow response time (>3s)")
                result["recommendations"].append("Optimize server response time")

            if not result["is_https"]:
                result["issues"].append("Not using HTTPS")
                result["recommendations"].append("Implement SSL certificate and redirect to HTTPS")

            if len(result["redirects"]) > 2:
                result["issues"].append("Too many redirects")
                result["recommendations"].append("Reduce redirect chain")

        except requests.exceptions.RequestException as e:
            result["status"] = "error"
            result["issues"].append(f"Connection failed: {str(e)}")
            result["recommendations"].append("Check DNS configuration and server availability")

        return result

    def _audit_seo(self, url: str) -> Dict[str, Any]:
        """Audit SEO elements."""
        result = {
            "title_tag": {"present": False, "length": 0, "content": ""},
            "meta_description": {"present": False, "length": 0, "content": ""},
            "h1_tags": {"count": 0, "content": []},
            "canonical_url": {"present": False, "url": ""},
            "robots_txt": {"present": False, "accessible": False},
            "sitemap": {"present": False, "accessible": False},
            "issues": [],
            "recommendations": []
        }

        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                result["issues"].append(f"Cannot analyze SEO - HTTP {response.status_code}")
                return result

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Title tag
            title_tag = soup.find('title')
            if title_tag:
                result["title_tag"]["present"] = True
                result["title_tag"]["content"] = title_tag.get_text().strip()
                result["title_tag"]["length"] = len(result["title_tag"]["content"])

                if result["title_tag"]["length"] == 0:
                    result["issues"].append("Empty title tag")
                    result["recommendations"].append("Add descriptive title tag (30-60 characters)")
                elif result["title_tag"]["length"] > 60:
                    result["issues"].append("Title tag too long")
                    result["recommendations"].append("Shorten title tag to 30-60 characters")

            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                result["meta_description"]["present"] = True
                result["meta_description"]["content"] = meta_desc['content'].strip()
                result["meta_description"]["length"] = len(result["meta_description"]["content"])

                if result["meta_description"]["length"] > 160:
                    result["issues"].append("Meta description too long")
                    result["recommendations"].append("Shorten meta description to 120-160 characters")

            # H1 tags
            h1_tags = soup.find_all('h1')
            result["h1_tags"]["count"] = len(h1_tags)
            result["h1_tags"]["content"] = [h1.get_text().strip() for h1 in h1_tags]

            if result["h1_tags"]["count"] == 0:
                result["issues"].append("No H1 tags found")
                result["recommendations"].append("Add exactly one H1 tag with main page title")
            elif result["h1_tags"]["count"] > 1:
                result["issues"].append("Multiple H1 tags found")
                result["recommendations"].append("Use only one H1 tag per page")

            # Canonical URL
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if canonical and canonical.get('href'):
                result["canonical_url"]["present"] = True
                result["canonical_url"]["url"] = canonical['href']

            # Check robots.txt
            robots_url = urljoin(url, '/robots.txt')
            try:
                robots_response = self.session.get(robots_url, timeout=5)
                result["robots_txt"]["present"] = robots_response.status_code == 200
                result["robots_txt"]["accessible"] = True
            except:
                pass

            if not result["robots_txt"]["present"]:
                result["issues"].append("Missing robots.txt")
                result["recommendations"].append("Create robots.txt file for search engine crawling")

        except Exception as e:
            result["issues"].append(f"SEO analysis failed: {str(e)}")

        return result

    def _audit_technical(self, url: str) -> Dict[str, Any]:
        """Audit technical aspects."""
        result = {
            "page_size_kb": 0,
            "has_compression": False,
            "response_headers": {},
            "issues": [],
            "recommendations": []
        }

        try:
            response = self.session.get(url, timeout=10)

            # Page size
            result["page_size_kb"] = len(response.content) / 1024

            if result["page_size_kb"] > 500:
                result["issues"].append("Page size too large")
                result["recommendations"].append("Optimize images and minify resources")

            # Compression check
            encoding = response.headers.get('content-encoding', '')
            result["has_compression"] = 'gzip' in encoding.lower() or 'br' in encoding.lower()

            if not result["has_compression"]:
                result["issues"].append("No compression enabled")
                result["recommendations"].append("Enable gzip or brotli compression")

            # Cache headers
            cache_control = response.headers.get('cache-control', '')
            if not cache_control:
                result["issues"].append("Missing cache headers")
                result["recommendations"].append("Add appropriate cache headers")

            result["response_headers"] = dict(response.headers)

        except Exception as e:
            result["issues"].append(f"Technical analysis failed: {str(e)}")

        return result

    def _audit_content(self, url: str) -> Dict[str, Any]:
        """Audit content quality."""
        result = {
            "word_count": 0,
            "image_count": 0,
            "images_with_alt": 0,
            "link_count": 0,
            "internal_links": 0,
            "external_links": 0,
            "issues": [],
            "recommendations": []
        }

        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                result["issues"].append(f"Cannot analyze content - HTTP {response.status_code}")
                return result

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Word count (rough estimate)
            text_content = soup.get_text()
            words = text_content.split()
            result["word_count"] = len(words)

            if result["word_count"] < 300:
                result["issues"].append("Low word count")
                result["recommendations"].append("Add more comprehensive content")

            # Images
            images = soup.find_all('img')
            result["image_count"] = len(images)

            for img in images:
                if img.get('alt'):
                    result["images_with_alt"] += 1

            if result["image_count"] > 0:
                alt_ratio = result["images_with_alt"] / result["image_count"]
                if alt_ratio < 0.8:
                    result["issues"].append("Missing alt text on images")
                    result["recommendations"].append("Add descriptive alt text to all images")

            # Links
            links = soup.find_all('a', href=True)
            result["link_count"] = len(links)

            domain = urlparse(url).netloc
            for link in links:
                href = link['href']
                if href.startswith(('http://', 'https://')):
                    link_domain = urlparse(href).netloc
                    if link_domain == domain:
                        result["internal_links"] += 1
                    else:
                        result["external_links"] += 1
                else:
                    result["internal_links"] += 1

        except Exception as e:
            result["issues"].append(f"Content analysis failed: {str(e)}")

        return result

    def _audit_security(self, url: str) -> Dict[str, Any]:
        """Audit security aspects."""
        result = {
            "has_ssl": False,
            "ssl_expiry_days": None,
            "has_security_headers": False,
            "security_headers": {},
            "issues": [],
            "recommendations": []
        }

        try:
            response = self.session.get(url, timeout=10)

            # SSL check
            result["has_ssl"] = url.startswith("https://")

            if not result["has_ssl"]:
                result["issues"].append("Not using HTTPS")
                result["recommendations"].append("Implement SSL certificate")

            # Security headers
            security_headers = [
                'strict-transport-security',
                'x-content-type-options',
                'x-frame-options',
                'x-xss-protection',
                'content-security-policy'
            ]

            found_headers = []
            for header in security_headers:
                if header in response.headers:
                    found_headers.append(header)
                    result["security_headers"][header] = response.headers[header]

            result["has_security_headers"] = len(found_headers) > 0

            missing_headers = [h for h in security_headers if h not in response.headers]
            if missing_headers:
                result["issues"].append(f"Missing security headers: {', '.join(missing_headers[:3])}")
                result["recommendations"].append("Add essential security headers (HSTS, CSP, X-Frame-Options)")

        except Exception as e:
            result["issues"].append(f"Security analysis failed: {str(e)}")

        return result

    def _audit_accessibility(self, url: str) -> Dict[str, Any]:
        """Audit accessibility and mobile-friendliness."""
        result = {
            "has_viewport_meta": False,
            "has_lang_attribute": False,
            "form_labels_present": 0,
            "forms_without_labels": 0,
            "issues": [],
            "recommendations": []
        }

        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                result["issues"].append(f"Cannot analyze accessibility - HTTP {response.status_code}")
                return result

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Viewport meta tag
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            result["has_viewport_meta"] = viewport is not None

            if not result["has_viewport_meta"]:
                result["issues"].append("Missing viewport meta tag")
                result["recommendations"].append("Add viewport meta tag for mobile responsiveness")

            # Language attribute
            html_tag = soup.find('html')
            result["has_lang_attribute"] = html_tag and html_tag.get('lang')

            if not result["has_lang_attribute"]:
                result["issues"].append("Missing lang attribute")
                result["recommendations"].append("Add lang attribute to html tag")

            # Form accessibility
            forms = soup.find_all('form')
            for form in forms:
                inputs = form.find_all('input', attrs={'type': ['text', 'email', 'password', 'tel', 'search']})
                for input_field in inputs:
                    input_id = input_field.get('id')
                    if input_id:
                        label = soup.find('label', attrs={'for': input_id})
                        if label:
                            result["form_labels_present"] += 1
                        else:
                            result["forms_without_labels"] += 1

            if result["forms_without_labels"] > 0:
                result["issues"].append("Forms missing labels")
                result["recommendations"].append("Add proper labels to all form inputs")

        except Exception as e:
            result["issues"].append(f"Accessibility analysis failed: {str(e)}")

        return result

    def _generate_agent_actions(self, audit_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable items for agents to follow."""
        actions = []

        # Process each section for action items
        for section_name, section_data in audit_report.get("sections", {}).items():
            issues = section_data.get("issues", [])
            recommendations = section_data.get("recommendations", [])

            for issue in issues:
                actions.append({
                    "priority": "high",
                    "category": section_name,
                    "issue": issue,
                    "action_required": True,
                    "estimated_effort": "medium",
                    "assignee": "web_development_agent"
                })

            for recommendation in recommendations:
                actions.append({
                    "priority": "medium",
                    "category": section_name,
                    "recommendation": recommendation,
                    "action_required": True,
                    "estimated_effort": "low",
                    "assignee": "web_development_agent"
                })

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        actions.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 2))

        return actions

    def _generate_overall_assessment(self, audit_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall assessment of the website."""
        assessment = {
            "overall_score": 0,
            "grade": "F",
            "strengths": [],
            "critical_issues": [],
            "summary": ""
        }

        sections = audit_report.get("sections", {})
        total_score = 0
        section_count = 0

        # Score each section
        for section_name, section_data in sections.items():
            section_count += 1

            if section_name == "connectivity":
                if section_data.get("status") == "healthy":
                    total_score += 100
                    assessment["strengths"].append("Good connectivity and performance")
                else:
                    critical_issues = section_data.get("issues", [])
                    assessment["critical_issues"].extend(critical_issues[:2])  # Top 2 issues

            elif section_name == "seo":
                score = 0
                if section_data.get("title_tag", {}).get("present"):
                    score += 25
                    assessment["strengths"].append("Has title tag")
                if section_data.get("meta_description", {}).get("present"):
                    score += 25
                    assessment["strengths"].append("Has meta description")
                if section_data.get("h1_tags", {}).get("count") == 1:
                    score += 25
                    assessment["strengths"].append("Proper H1 structure")
                if section_data.get("canonical_url", {}).get("present"):
                    score += 25
                    assessment["strengths"].append("Has canonical URL")

                total_score += score

            elif section_name == "technical":
                if not section_data.get("issues"):
                    total_score += 100
                    assessment["strengths"].append("Good technical performance")
                else:
                    total_score += 50

            elif section_name == "content":
                if section_data.get("word_count", 0) > 300:
                    total_score += 100
                    assessment["strengths"].append("Good content depth")
                else:
                    total_score += 30

            elif section_name == "security":
                if section_data.get("has_ssl"):
                    total_score += 100
                    assessment["strengths"].append("Uses HTTPS")
                else:
                    total_score += 20
                    assessment["critical_issues"].append("Not using HTTPS")

            elif section_name == "accessibility":
                score = 0
                if section_data.get("has_viewport_meta"):
                    score += 50
                if section_data.get("has_lang_attribute"):
                    score += 50
                total_score += score

        # Calculate overall score
        if section_count > 0:
            assessment["overall_score"] = total_score / section_count

            # Assign grade
            score = assessment["overall_score"]
            if score >= 90:
                assessment["grade"] = "A"
            elif score >= 80:
                assessment["grade"] = "B"
            elif score >= 70:
                assessment["grade"] = "C"
            elif score >= 60:
                assessment["grade"] = "D"
            else:
                assessment["grade"] = "F"

        # Generate summary
        grade = assessment["grade"]
        score = assessment["overall_score"]

        if grade == "A":
            assessment["summary"] = f"Excellent website (Grade {grade}, {score:.1f}%). Well-optimized with good performance."
        elif grade == "B":
            assessment["summary"] = f"Good website (Grade {grade}, {score:.1f}%). Generally well-structured with minor improvements needed."
        elif grade == "C":
            assessment["summary"] = f"Average website (Grade {grade}, {score:.1f}%). Functional but needs several improvements."
        elif grade == "D":
            assessment["summary"] = f"Poor website (Grade {grade}, {score:.1f}%). Significant issues requiring attention."
        else:
            assessment["summary"] = f"Critical issues (Grade {grade}, {score:.1f}%). Major improvements urgently needed."

        return assessment


async def main():
    """Main function to run website audit and generate agent report."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate website audit report for agents")
    parser.add_argument("urls", nargs="+", help="Website URLs to audit")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    auditor = WebsiteAuditorAgent()

    print("🚀 Starting Ollama Website Audit Agent Report Generation")
    print(f"📋 Auditing {len(args.urls)} websites...")

    all_results = {
        "audit_run_timestamp": datetime.now().isoformat(),
        "websites_audited": len(args.urls),
        "tool_used": "ollama_website_audit_agent_report",
        "results": {}
    }

    for url in args.urls:
        print(f"🔍 Auditing: {url}")
        try:
            result = auditor.audit_website(url)
            all_results["results"][url] = result
            print(f"✅ Completed audit for: {url}")
        except Exception as e:
            print(f"❌ Failed to audit {url}: {e}")
            all_results["results"][url] = {
                "audit_status": "failed",
                "error": str(e),
                "audit_timestamp": datetime.now().isoformat()
            }

    # Generate summary
    successful_audits = sum(1 for r in all_results["results"].values() if r.get("audit_status") == "completed")
    failed_audits = len(args.urls) - successful_audits

    all_results["summary"] = {
        "total_websites": len(args.urls),
        "successful_audits": successful_audits,
        "failed_audits": failed_audits,
        "success_rate": successful_audits / len(args.urls) if args.urls else 0,
        "generated_at": datetime.now().isoformat()
    }

    # Output results
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        print(f"💾 Report saved to: {args.output}")
    else:
        # Print to console
        print("\n" + "="*80)
        print("📊 WEBSITE AUDIT AGENT REPORT")
        print("="*80)

        for url, result in all_results["results"].items():
            print(f"\n🔗 Website: {url}")
            print(f"📅 Audited: {result.get('audit_timestamp', 'Unknown')}")

            if result.get("audit_status") == "completed":
                assessment = result.get("overall_assessment", {})
                print(f"📊 Score: {assessment.get('overall_score', 0):.1f}% (Grade: {assessment.get('grade', 'N/A')})")
                print(f"💡 Summary: {assessment.get('summary', 'No summary available')}")

                # Show top action items
                actions = result.get("agent_action_items", [])[:3]  # Top 3
                if actions:
                    print("🎯 Top Agent Actions:")
                    for i, action in enumerate(actions, 1):
                        issue = action.get("issue") or action.get("recommendation", "Unknown")
                        priority = action.get("priority", "unknown")
                        print(f"  {i}. [{priority.upper()}] {issue}")
            else:
                print(f"❌ Status: {result.get('audit_status', 'Unknown')}")
                if "error" in result:
                    print(f"   Error: {result['error']}")

        print(f"\n📈 Summary: {successful_audits}/{len(args.urls)} websites successfully audited")
        print("="*80)


if __name__ == "__main__":
    asyncio.run(main())