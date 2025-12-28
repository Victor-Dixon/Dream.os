#!/usr/bin/env python3
"""
Analytics & SEO MCP Server
==========================

Google Analytics, SEO optimization, meta tags, structured data,
and analytics tracking across all websites.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-28
V2 Compliant: Yes (<300 lines per function)
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


@dataclass
class AnalyticsConfig:
    """Analytics configuration for a site."""
    site_name: str
    ga4_measurement_id: Optional[str] = None
    gtm_container_id: Optional[str] = None
    facebook_pixel_id: Optional[str] = None
    site_url: Optional[str] = None


@dataclass
class SEOData:
    """SEO data for a page/post."""
    title: str
    meta_description: str
    canonical_url: str
    og_title: str
    og_description: str
    og_image: str
    twitter_card: str
    focus_keyword: str
    readability_score: int
    seo_score: int


class AnalyticsSEOEngine:
    """Analytics and SEO operations engine."""

    def __init__(self, sites_config: Dict[str, Any]):
        self.sites = {}
        for name, config in sites_config.items():
            self.sites[name] = AnalyticsConfig(
                site_name=name,
                ga4_measurement_id=config.get('ga4_measurement_id'),
                gtm_container_id=config.get('gtm_container_id'),
                facebook_pixel_id=config.get('facebook_pixel_id'),
                site_url=config.get('site_url')
            )

    def generate_ga4_code(self, measurement_id: str) -> str:
        """Generate Google Analytics 4 tracking code."""
        return f"""<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{measurement_id}');
</script>"""

    def generate_gtm_code(self, container_id: str) -> str:
        """Generate Google Tag Manager code."""
        return f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{container_id}');</script>
<!-- End Google Tag Manager -->"""

    def generate_facebook_pixel_code(self, pixel_id: str) -> str:
        """Generate Facebook Pixel tracking code."""
        return f"""<!-- Facebook Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{pixel_id}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"
/></noscript>
<!-- End Facebook Pixel Code -->"""

    def generate_tracking_code(self, site_name: str, include_ga4: bool = True,
                             include_gtm: bool = True, include_fbp: bool = True) -> str:
        """Generate complete tracking code for a site."""
        if site_name not in self.sites:
            return f"<!-- Error: Site '{site_name}' not configured -->"

        site = self.sites[site_name]
        code_parts = []

        if include_ga4 and site.ga4_measurement_id:
            code_parts.append(self.generate_ga4_code(site.ga4_measurement_id))

        if include_gtm and site.gtm_container_id:
            code_parts.append(self.generate_gtm_code(site.gtm_container_id))

        if include_fbp and site.facebook_pixel_id:
            code_parts.append(self.generate_facebook_pixel_code(site.facebook_pixel_id))

        if not code_parts:
            return f"<!-- No tracking codes configured for {site_name} -->"

        return "\n\n".join(code_parts)

    def analyze_seo_score(self, content: str, title: str = "", meta_description: str = "",
                         focus_keyword: str = "") -> SEOData:
        """Analyze SEO score for content."""
        # Basic SEO analysis
        seo_score = 100
        issues = []

        # Title analysis
        if len(title) < 30:
            seo_score -= 10
            issues.append("Title too short (< 30 characters)")
        elif len(title) > 60:
            seo_score -= 5
            issues.append("Title too long (> 60 characters)")

        # Meta description analysis
        if not meta_description:
            seo_score -= 15
            issues.append("Missing meta description")
        elif len(meta_description) < 120:
            seo_score -= 10
            issues.append("Meta description too short (< 120 characters)")
        elif len(meta_description) > 160:
            seo_score -= 5
            issues.append("Meta description too long (> 160 characters)")

        # Focus keyword analysis
        if focus_keyword:
            keyword_density = content.lower().count(focus_keyword.lower()) / len(content.split()) * 100
            if keyword_density < 0.5:
                seo_score -= 5
                issues.append("Low keyword density")
            elif keyword_density > 2.5:
                seo_score -= 10
                issues.append("Keyword stuffing detected")

        # Content analysis
        word_count = len(content.split())
        if word_count < 300:
            seo_score -= 15
            issues.append("Content too short (< 300 words)")
        elif word_count > 2500:
            seo_score -= 5
            issues.append("Content very long (> 2500 words)")

        # Readability score (simplified)
        readability_score = max(0, min(100, 100 - (len(content) // 1000)))

        # Generate Open Graph data
        og_title = title[:60] if title else ""
        og_description = meta_description[:160] if meta_description else content[:160]
        og_image = ""  # Would need to extract from content

        return SEOData(
            title=title,
            meta_description=meta_description,
            canonical_url="",
            og_title=og_title,
            og_description=og_description,
            og_image=og_image,
            twitter_card="summary_large_image",
            focus_keyword=focus_keyword,
            readability_score=readability_score,
            seo_score=max(0, seo_score)
        )

    def generate_meta_tags(self, seo_data: SEOData) -> str:
        """Generate HTML meta tags for SEO."""
        tags = []

        # Basic meta tags
        if seo_data.meta_description:
            tags.append(f'<meta name="description" content="{seo_data.meta_description}">')

        if seo_data.focus_keyword:
            tags.append(f'<meta name="keywords" content="{seo_data.focus_keyword}">')

        # Open Graph tags
        tags.append(f'<meta property="og:title" content="{seo_data.og_title}">')
        tags.append(f'<meta property="og:description" content="{seo_data.og_description}">')
        tags.append('<meta property="og:type" content="article">')
        if seo_data.canonical_url:
            tags.append(f'<meta property="og:url" content="{seo_data.canonical_url}">')
        if seo_data.og_image:
            tags.append(f'<meta property="og:image" content="{seo_data.og_image}">')

        # Twitter Card tags
        tags.append('<meta name="twitter:card" content="summary_large_image">')
        tags.append(f'<meta name="twitter:title" content="{seo_data.og_title}">')
        tags.append(f'<meta name="twitter:description" content="{seo_data.og_description}">')
        if seo_data.og_image:
            tags.append(f'<meta name="twitter:image" content="{seo_data.og_image}">')

        # Canonical URL
        if seo_data.canonical_url:
            tags.append(f'<link rel="canonical" href="{seo_data.canonical_url}">')

        return "\n    ".join(tags)

    def generate_structured_data(self, content_type: str, data: Dict[str, Any]) -> str:
        """Generate JSON-LD structured data."""
        structured_data = {
            "@context": "https://schema.org",
            "@type": content_type
        }

        # Add content-specific data
        if content_type == "Article":
            structured_data.update({
                "headline": data.get("title", ""),
                "description": data.get("description", ""),
                "author": {
                    "@type": "Person",
                    "name": data.get("author", "")
                },
                "datePublished": data.get("date_published", ""),
                "dateModified": data.get("date_modified", ""),
                "image": data.get("image", "")
            })
        elif content_type == "WebSite":
            structured_data.update({
                "name": data.get("site_name", ""),
                "url": data.get("site_url", ""),
                "description": data.get("description", "")
            })
        elif content_type == "Organization":
            structured_data.update({
                "name": data.get("org_name", ""),
                "url": data.get("org_url", ""),
                "logo": data.get("logo", "")
            })

        return f'<script type="application/ld+json">\n{json.dumps(structured_data, indent=2)}\n</script>'

    def analyze_page_performance(self, url: str) -> Dict[str, Any]:
        """Analyze page performance metrics."""
        if not REQUESTS_AVAILABLE:
            return {"error": "Requests library not available"}

        try:
            import time
            start_time = time.time()

            response = requests.get(url, timeout=10)
            load_time = time.time() - start_time

            # Basic performance metrics
            performance = {
                "url": url,
                "status_code": response.status_code,
                "load_time_seconds": round(load_time, 2),
                "content_length": len(response.content),
                "content_type": response.headers.get('content-type', ''),
                "server": response.headers.get('server', ''),
                "last_modified": response.headers.get('last-modified', '')
            }

            # Performance scoring
            score = 100
            if load_time > 3:
                score -= 20
                performance["slow_loading"] = True
            if len(response.content) > 5000000:  # 5MB
                score -= 10
                performance["large_content"] = True

            performance["performance_score"] = score

            return {"success": True, "performance": performance}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_tracking_implementation(self, site_name: str, page_content: str) -> Dict[str, Any]:
        """Check if tracking codes are properly implemented."""
        if site_name not in self.sites:
            return {"error": f"Site '{site_name}' not configured"}

        site = self.sites[site_name]
        results = {
            "site": site_name,
            "checks": {},
            "overall_status": "unknown"
        }

        # Check GA4
        if site.ga4_measurement_id:
            has_ga4 = site.ga4_measurement_id in page_content
            results["checks"]["ga4"] = {
                "expected_id": site.ga4_measurement_id,
                "implemented": has_ga4,
                "status": "✅" if has_ga4 else "❌"
            }

        # Check GTM
        if site.gtm_container_id:
            has_gtm = site.gtm_container_id in page_content
            results["checks"]["gtm"] = {
                "expected_id": site.gtm_container_id,
                "implemented": has_gtm,
                "status": "✅" if has_gtm else "❌"
            }

        # Check Facebook Pixel
        if site.facebook_pixel_id:
            has_fbp = site.facebook_pixel_id in page_content
            results["checks"]["facebook_pixel"] = {
                "expected_id": site.facebook_pixel_id,
                "implemented": has_fbp,
                "status": "✅" if has_fbp else "❌"
            }

        # Overall status
        implemented_count = sum(1 for check in results["checks"].values() if check["implemented"])
        total_checks = len(results["checks"])

        if implemented_count == total_checks:
            results["overall_status"] = "✅ All tracking codes implemented"
        elif implemented_count == 0:
            results["overall_status"] = "❌ No tracking codes implemented"
        else:
            results["overall_status"] = f"⚠️ {implemented_count}/{total_checks} tracking codes implemented"

        return results

    def bulk_seo_analysis(self, pages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Perform SEO analysis on multiple pages."""
        results = []

        for page in pages:
            content = page.get("content", "")
            title = page.get("title", "")
            meta_description = page.get("meta_description", "")
            focus_keyword = page.get("focus_keyword", "")

            seo_data = self.analyze_seo_score(content, title, meta_description, focus_keyword)

            results.append({
                "page_title": title,
                "seo_score": seo_data.seo_score,
                "readability_score": seo_data.readability_score,
                "issues": [],  # Would need to be populated based on analysis
                "recommendations": self._generate_seo_recommendations(seo_data)
            })

        return results

    def _generate_seo_recommendations(self, seo_data: SEOData) -> List[str]:
        """Generate SEO improvement recommendations."""
        recommendations = []

        if seo_data.seo_score < 80:
            if len(seo_data.title) < 30:
                recommendations.append("Increase title length to 30-60 characters")
            if not seo_data.meta_description:
                recommendations.append("Add meta description (120-160 characters)")
            if seo_data.focus_keyword and seo_data.seo_score < 70:
                recommendations.append("Improve keyword optimization")

        return recommendations


def load_sites_config() -> Dict[str, Any]:
    """Load analytics configuration for sites."""
    # This would typically load from a config file
    return {
        "example_site": {
            "ga4_measurement_id": "G-XXXXXXXXXX",
            "gtm_container_id": "GTM-XXXXXXX",
            "facebook_pixel_id": "123456789012345",
            "site_url": "https://example.com"
        }
    }


def generate_tracking_code(site_name: str) -> Dict[str, Any]:
    """Generate tracking code for a site."""
    try:
        sites_config = load_sites_config()
        engine = AnalyticsSEOEngine(sites_config)

        code = engine.generate_tracking_code(site_name)
        return {"success": True, "tracking_code": code}
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_seo(content: str, title: str = "", meta_description: str = "",
               focus_keyword: str = "") -> Dict[str, Any]:
    """Analyze SEO for content."""
    try:
        sites_config = load_sites_config()
        engine = AnalyticsSEOEngine(sites_config)

        seo_data = engine.analyze_seo_score(content, title, meta_description, focus_keyword)

        return {
            "success": True,
            "seo_data": {
                "seo_score": seo_data.seo_score,
                "readability_score": seo_data.readability_score,
                "title": seo_data.title,
                "meta_description": seo_data.meta_description,
                "focus_keyword": seo_data.focus_keyword
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_meta_tags(seo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate meta tags for SEO data."""
    try:
        sites_config = load_sites_config()
        engine = AnalyticsSEOEngine(sites_config)

        # Convert dict to SEOData object
        seo_obj = SEOData(
            title=seo_data.get("title", ""),
            meta_description=seo_data.get("meta_description", ""),
            canonical_url=seo_data.get("canonical_url", ""),
            og_title=seo_data.get("og_title", ""),
            og_description=seo_data.get("og_description", ""),
            og_image=seo_data.get("og_image", ""),
            twitter_card=seo_data.get("twitter_card", "summary_large_image"),
            focus_keyword=seo_data.get("focus_keyword", ""),
            readability_score=seo_data.get("readability_score", 0),
            seo_score=seo_data.get("seo_score", 0)
        )

        meta_tags = engine.generate_meta_tags(seo_obj)
        return {"success": True, "meta_tags": meta_tags}
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_performance(url: str) -> Dict[str, Any]:
    """Analyze page performance."""
    try:
        sites_config = load_sites_config()
        engine = AnalyticsSEOEngine(sites_config)

        result = engine.analyze_page_performance(url)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_tracking(site_name: str, page_content: str) -> Dict[str, Any]:
    """Check tracking implementation."""
    try:
        sites_config = load_sites_config()
        engine = AnalyticsSEOEngine(sites_config)

        result = engine.check_tracking_implementation(site_name, page_content)
        return {"success": True, "tracking_check": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def bulk_seo_analysis(pages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Bulk SEO analysis."""
    try:
        sites_config = load_sites_config()
        engine = AnalyticsSEOEngine(sites_config)

        results = engine.bulk_seo_analysis(pages)
        return {"success": True, "analysis_results": results}
    except Exception as e:
        return {"success": False, "error": str(e)}


# MCP Server Protocol
def main():
    """MCP server main loop."""
    server_info = {"name": "analytics-seo-server", "version": "1.0.0"}

    tools_definitions = {
        "generate_tracking_code": {
            "description": "Generate Google Analytics, GTM, and Facebook Pixel tracking code for a site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "Site name"}
                },
                "required": ["site_name"]
            }
        },
        "analyze_seo": {
            "description": "Analyze SEO score for content",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to analyze"},
                    "title": {"type": "string", "description": "Page title"},
                    "meta_description": {"type": "string", "description": "Meta description"},
                    "focus_keyword": {"type": "string", "description": "Focus keyword"}
                },
                "required": ["content"]
            }
        },
        "generate_meta_tags": {
            "description": "Generate SEO meta tags and Open Graph tags",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "seo_data": {"type": "object", "description": "SEO data object"}
                },
                "required": ["seo_data"]
            }
        },
        "analyze_performance": {
            "description": "Analyze page performance metrics",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Page URL to analyze"}
                },
                "required": ["url"]
            }
        },
        "check_tracking": {
            "description": "Check if tracking codes are properly implemented",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_name": {"type": "string", "description": "Site name"},
                    "page_content": {"type": "string", "description": "Page HTML content"}
                },
                "required": ["site_name", "page_content"]
            }
        },
        "bulk_seo_analysis": {
            "description": "Perform SEO analysis on multiple pages",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "pages": {"type": "array", "items": {"type": "object"}, "description": "List of pages with content"}
                },
                "required": ["pages"]
            }
        }
    }

    initialized = False

    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                initialized = True
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": tools_definitions},
                        "serverInfo": server_info
                    }
                }))
                sys.stdout.flush()

            elif method == "tools/list":
                tools_list = []
                for tool_name, tool_def in tools_definitions.items():
                    tools_list.append({
                        "name": tool_name,
                        "description": tool_def["description"],
                        "inputSchema": tool_def["inputSchema"]
                    })
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list, "serverInfo": server_info}
                }))
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name == "generate_tracking_code":
                    result = generate_tracking_code(**arguments)
                elif tool_name == "analyze_seo":
                    result = analyze_seo(**arguments)
                elif tool_name == "generate_meta_tags":
                    result = generate_meta_tags(**arguments)
                elif tool_name == "analyze_performance":
                    result = analyze_performance(**arguments)
                elif tool_name == "check_tracking":
                    result = check_tracking(**arguments)
                elif tool_name == "bulk_seo_analysis":
                    result = bulk_seo_analysis(**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}

                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
                }))
                sys.stdout.flush()

            else:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"}
                }))
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": request.get("id") if "request" in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
