#!/usr/bin/env python3
"""
Validation Audit MCP Server
===========================

Provides validation and audit operations for:
- Closures validation and compliance checking
- SEO analysis and validation
- Website structure auditing
- WordPress health checks and diagnostics
- Content validation and SEO optimization

<!-- SSOT Domain: validation -->
"""

import os
import sys
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

# Add repository root to path for imports
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, PromptMessage

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None


class ValidationAuditServer:
    """MCP Server for validation and audit operations."""

    def __init__(self):
        self.server = Server("validation-audit")
        self.p0_sites = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]

    def _check_site_accessibility(self, site: str) -> ValidationResult:
        """Check if a WordPress site is accessible and healthy."""
        try:
            url = f"https://{site}"
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'WordPress-Health-Check/1.0'
            })

            if response.status_code == 200:
                # Check for WordPress-specific indicators
                is_wordpress = any(indicator in response.text.lower() for indicator in [
                    'wp-content', 'wp-includes', 'wordpress'
                ])

                return ValidationResult(
                    success=True,
                    message=f"Site accessible (HTTP {response.status_code})",
                    details={
                        "status_code": response.status_code,
                        "is_wordpress": is_wordpress,
                        "response_time": response.elapsed.total_seconds(),
                        "content_length": len(response.text)
                    }
                )
            else:
                return ValidationResult(
                    success=False,
                    message=f"Site returned HTTP {response.status_code}",
                    details={"status_code": response.status_code}
                )

        except requests.exceptions.RequestException as e:
            return ValidationResult(
                success=False,
                message=f"Connection failed: {str(e)}",
                recommendations=["Check DNS configuration", "Verify server is running", "Check firewall settings"]
            )

    def _wordpress_health_check(self, site: str) -> ValidationResult:
        """
        Perform comprehensive WordPress health check.
        This is the wordpress_health_check tool integrated into the MCP server.
        """
        result = self._check_site_accessibility(site)
        if not result.success:
            return result

        issues = []
        recommendations = []

        try:
            url = f"https://{site}"
            response = requests.get(url, timeout=10)

            # Check for common WordPress issues
            content = response.text

            # Check for WordPress version disclosure (security issue)
            if 'generator' in content.lower() and 'wordpress' in content.lower():
                issues.append("WordPress version is publicly disclosed")
                recommendations.append("Remove WordPress version from meta tags")

            # Check for common security issues
            if 'wp-admin' in content and 'wp-login.php' in content:
                # This is normal, but let's check if login page is accessible
                try:
                    login_response = requests.get(f"{url}/wp-login.php", timeout=5)
                    if login_response.status_code == 200:
                        issues.append("WordPress login page is publicly accessible")
                        recommendations.append("Consider restricting access to wp-admin and wp-login.php")
                except:
                    pass  # Login page check failed, not necessarily an issue

            # Check for database connection issues (look for common error patterns)
            error_patterns = [
                "error establishing database connection",
                "database connection error",
                "mysql_connect",
                "mysqli_connect"
            ]

            for pattern in error_patterns:
                if pattern.lower() in content.lower():
                    issues.append("Database connection error detected")
                    recommendations.append("Check database credentials and server status")
                    break

            # Check for PHP errors
            if any(php_error in content.lower() for php_error in [
                "php fatal error", "php warning", "parse error", "syntax error"
            ]):
                issues.append("PHP errors detected on frontend")
                recommendations.append("Check PHP error logs and fix syntax issues")

            # Check for maintenance mode
            if any(maintenance in content.lower() for maintenance in [
                "maintenance mode", "temporarily unavailable", "coming soon"
            ]):
                issues.append("Site appears to be in maintenance mode")
                recommendations.append("Complete maintenance tasks and disable maintenance mode")

            # Performance checks
            if response.elapsed.total_seconds() > 3.0:
                issues.append("Slow response time detected")
                recommendations.append("Optimize site performance, check hosting, enable caching")

            # Check for HTTPS
            if not url.startswith("https://"):
                issues.append("Site not using HTTPS")
                recommendations.append("Enable SSL certificate and force HTTPS")

            # Check for basic SEO elements
            if '<title>' not in content:
                issues.append("Missing page title")
                recommendations.append("Add proper page titles for SEO")

            if 'name="description"' not in content:
                issues.append("Missing meta description")
                recommendations.append("Add meta descriptions for better SEO")

            # Check for mobile responsiveness
            if 'viewport' not in content:
                issues.append("Missing viewport meta tag")
                recommendations.append("Add viewport meta tag for mobile responsiveness")

        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"Health check failed: {str(e)}",
                recommendations=["Review site configuration", "Check server logs"]
            )

        if issues:
            return ValidationResult(
                success=False,
                message=f"Health check found {len(issues)} issues",
                details={"issues": issues, "site": site},
                recommendations=recommendations
            )
        else:
            return ValidationResult(
                success=True,
                message="WordPress health check passed - no issues detected",
                details={"site": site, "checks_performed": 8},
                recommendations=["Consider enabling additional security measures", "Monitor performance regularly"]
            )

    def _validate_closure_format(self, closure_file: str) -> ValidationResult:
        """Validate that a session closure follows the required format."""
        try:
            with open(closure_file, 'r') as f:
                content = f.read()

            required_sections = [
                "- **Task:**",
                "- **Project:**",
                "- **Actions Taken:**",
                "- **Artifacts Created / Updated:**",
                "- **Verification:**",
                "- **Public Build Signal:**",
                "- **Git Commit:**",
                "- **Git Push:**",
                "- **Website Blogging:**",
                "- **Status:**"
            ]

            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)

            if missing_sections:
                return ValidationResult(
                    success=False,
                    message=f"Closure missing required sections: {', '.join(missing_sections)}",
                    recommendations=["Add missing sections to closure format"]
                )

            # Check for proper status format
            if "✅ Ready" not in content and "🟡 Blocked" not in content:
                return ValidationResult(
                    success=False,
                    message="Closure status must be either '✅ Ready' or '🟡 Blocked'",
                    recommendations=["Fix status format in closure"]
                )

            return ValidationResult(
                success=True,
                message="Closure format validation passed",
                details={"file": closure_file}
            )

        except FileNotFoundError:
            return ValidationResult(
                success=False,
                message=f"Closure file not found: {closure_file}",
                recommendations=["Ensure closure file exists and path is correct"]
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"Closure validation failed: {str(e)}",
                recommendations=["Check closure file format and content"]
            )

    def _audit_website_seo(self, site: str) -> ValidationResult:
        """Audit website for SEO optimization."""
        result = self._check_site_accessibility(site)
        if not result.success:
            return result

        try:
            url = f"https://{site}"
            response = requests.get(url, timeout=10)
            content = response.text

            seo_issues = []
            seo_recommendations = []

            # Title tag check
            if '<title>' not in content or '</title>' not in content:
                seo_issues.append("Missing or malformed title tag")
                seo_recommendations.append("Add a descriptive title tag (50-60 characters)")

            # Meta description check
            if 'name="description"' not in content:
                seo_issues.append("Missing meta description")
                seo_recommendations.append("Add meta description (150-160 characters)")

            # H1 tag check
            if '<h1>' not in content:
                seo_issues.append("Missing H1 heading")
                seo_recommendations.append("Add one H1 tag per page with target keyword")

            # Image alt attributes
            if '<img' in content and 'alt=' not in content:
                seo_issues.append("Images missing alt attributes")
                seo_recommendations.append("Add descriptive alt text to all images")

            # Open Graph tags
            og_tags = ['og:title', 'og:description', 'og:image', 'og:url']
            missing_og = [tag for tag in og_tags if f'property="{tag}"' not in content]
            if missing_og:
                seo_issues.append(f"Missing Open Graph tags: {', '.join(missing_og)}")
                seo_recommendations.append("Add Open Graph meta tags for better social sharing")

            # Structured data check
            if 'application/ld+json' not in content and '@context' not in content:
                seo_issues.append("Missing structured data markup")
                seo_recommendations.append("Add JSON-LD structured data for rich snippets")

            if seo_issues:
                return ValidationResult(
                    success=False,
                    message=f"SEO audit found {len(seo_issues)} issues",
                    details={"issues": seo_issues, "site": site},
                    recommendations=seo_recommendations
                )
            else:
                return ValidationResult(
                    success=True,
                    message="SEO audit passed - good optimization detected",
                    details={"site": site, "checks_performed": 6}
                )

        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"SEO audit failed: {str(e)}",
                recommendations=["Check site accessibility", "Review HTML structure"]
            )

    async def handle_wordpress_health_check(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle wordpress_health_check tool call."""
        site = arguments.get("site")

        if not site:
            return [TextContent(
                type="text",
                text="❌ ERROR: 'site' parameter is required for wordpress_health_check"
            )]

        result = self._wordpress_health_check(site)

        response = f"🔍 WordPress Health Check Results for {site}\n\n"
        response += f"**Status:** {'✅ PASSED' if result.success else '❌ FAILED'}\n"
        response += f"**Message:** {result.message}\n\n"

        if result.details:
            response += "**Details:**\n"
            for key, value in result.details.items():
                response += f"- {key}: {value}\n"
            response += "\n"

        if result.recommendations:
            response += "**Recommendations:**\n"
            for rec in result.recommendations:
                response += f"- {rec}\n"

        return [TextContent(type="text", text=response)]

    async def handle_validate_closure(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle validate_closure_format tool call."""
        closure_file = arguments.get("file")

        if not closure_file:
            return [TextContent(
                type="text",
                text="❌ ERROR: 'file' parameter is required for validate_closure_format"
            )]

        result = self._validate_closure_format(closure_file)

        response = f"📋 Closure Format Validation Results\n\n"
        response += f"**File:** {closure_file}\n"
        response += f"**Status:** {'✅ PASSED' if result.success else '❌ FAILED'}\n"
        response += f"**Message:** {result.message}\n\n"

        if result.recommendations:
            response += "**Fixes Needed:**\n"
            for rec in result.recommendations:
                response += f"- {rec}\n"

        return [TextContent(type="text", text=response)]

    async def handle_audit_website_seo(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle audit_website_seo tool call."""
        site = arguments.get("site")

        if not site:
            return [TextContent(
                type="text",
                text="❌ ERROR: 'site' parameter is required for audit_website_seo"
            )]

        result = self._audit_website_seo(site)

        response = f"🔍 SEO Audit Results for {site}\n\n"
        response += f"**Status:** {'✅ PASSED' if result.success else '❌ NEEDS IMPROVEMENT'}\n"
        response += f"**Message:** {result.message}\n\n"

        if result.details and "issues" in result.details:
            response += "**Issues Found:**\n"
            for issue in result.details["issues"]:
                response += f"- {issue}\n"
            response += "\n"

        if result.recommendations:
            response += "**Recommendations:**\n"
            for rec in result.recommendations:
                response += f"- {rec}\n"

        return [TextContent(type="text", text=response)]

    async def handle_validate_p0_sites(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle validate_p0_sites tool call - comprehensive validation of all P0 sites."""
        results = []

        for site in self.p0_sites:
            health_result = self._wordpress_health_check(site)
            seo_result = self._audit_website_seo(site)

            site_result = {
                "site": site,
                "health_check": {
                    "passed": health_result.success,
                    "message": health_result.message,
                    "issues": len(health_result.details.get("issues", [])) if health_result.details else 0
                },
                "seo_audit": {
                    "passed": seo_result.success,
                    "message": seo_result.message,
                    "issues": len(seo_result.details.get("issues", [])) if seo_result.details else 0
                }
            }
            results.append(site_result)

        # Generate summary report
        total_sites = len(results)
        health_passed = sum(1 for r in results if r["health_check"]["passed"])
        seo_passed = sum(1 for r in results if r["seo_audit"]["passed"])

        response = f"📊 P0 Sites Validation Summary Report\n"
        response += f"**Generated:** {os.environ.get('USER', 'Agent-5')}\n\n"

        response += f"## Executive Summary\n"
        response += f"- **Sites Tested:** {total_sites}\n"
        response += f"- **Health Checks Passed:** {health_passed}/{total_sites}\n"
        response += f"- **SEO Audits Passed:** {seo_passed}/{total_sites}\n\n"

        response += "## Site-by-Site Results\n\n"

        for result in results:
            site = result["site"]
            health = result["health_check"]
            seo = result["seo_audit"]

            response += f"### {site}\n"
            response += f"**Health Check:** {'✅' if health['passed'] else '❌'} {health['message']}\n"
            response += f"**SEO Audit:** {'✅' if seo['passed'] else '❌'} {seo['message']}\n\n"

        response += "## Next Steps\n\n"
        if health_passed < total_sites or seo_passed < total_sites:
            response += "⚠️ **Action Required:** Address issues identified above\n\n"
            response += "**Priority Order:**\n"
            response += "1. Fix accessibility/server issues\n"
            response += "2. Resolve security vulnerabilities\n"
            response += "3. Improve SEO optimization\n"
            response += "4. Enhance performance\n"
        else:
            response += "🎉 **All validations passed!** Continue monitoring site health.\n"

        return [TextContent(type="text", text=response)]

    async def wordpress_health_check(self, site: str) -> str:
        """Perform comprehensive WordPress health check for a site."""
        result = self._wordpress_health_check(site)

        response = f"🔍 WordPress Health Check Results for {site}\n\n"
        response += f"**Status:** {'✅ PASSED' if result.success else '❌ FAILED'}\n"
        response += f"**Message:** {result.message}\n\n"

        if result.details:
            response += "**Details:**\n"
            for key, value in result.details.items():
                response += f"- {key}: {value}\n"
            response += "\n"

        if result.recommendations:
            response += "**Recommendations:**\n"
            for rec in result.recommendations:
                response += f"- {rec}\n"

        return response

    async def validate_closure_format(self, file: str) -> str:
        """Validate that a session closure follows the required A+++ format."""
        result = self._validate_closure_format(file)

        response = f"📋 Closure Format Validation Results\n\n"
        response += f"**File:** {file}\n"
        response += f"**Status:** {'✅ PASSED' if result.success else '❌ FAILED'}\n"
        response += f"**Message:** {result.message}\n\n"

        if result.recommendations:
            response += "**Fixes Needed:**\n"
            for rec in result.recommendations:
                response += f"- {rec}\n"

        return response

    async def audit_website_seo(self, site: str) -> str:
        """Audit website for SEO optimization and best practices."""
        result = self._audit_website_seo(site)

        response = f"🔍 SEO Audit Results for {site}\n\n"
        response += f"**Status:** {'✅ PASSED' if result.success else '❌ NEEDS IMPROVEMENT'}\n"
        response += f"**Message:** {result.message}\n\n"

        if result.details and "issues" in result.details:
            response += "**Issues Found:**\n"
            for issue in result.details["issues"]:
                response += f"- {issue}\n"
            response += "\n"

        if result.recommendations:
            response += "**Recommendations:**\n"
            for rec in result.recommendations:
                response += f"- {rec}\n"

        return response

    async def validate_p0_sites(self) -> str:
        """Comprehensive validation of all P0 sites including health checks and SEO audits."""
        results = []

        for site in self.p0_sites:
            health_result = self._wordpress_health_check(site)
            seo_result = self._audit_website_seo(site)

            site_result = {
                "site": site,
                "health_check": {
                    "passed": health_result.success,
                    "message": health_result.message,
                    "issues": len(health_result.details.get("issues", [])) if health_result.details else 0
                },
                "seo_audit": {
                    "passed": seo_result.success,
                    "message": seo_result.message,
                    "issues": len(seo_result.details.get("issues", [])) if seo_result.details else 0
                }
            }
            results.append(site_result)

        # Generate summary report
        total_sites = len(results)
        health_passed = sum(1 for r in results if r["health_check"]["passed"])
        seo_passed = sum(1 for r in results if r["seo_audit"]["passed"])

        response = f"📊 P0 Sites Validation Summary Report\n"
        response += f"**Generated:** Agent-5 (Business Intelligence)\n\n"

        response += f"## Executive Summary\n"
        response += f"- **Sites Tested:** {total_sites}\n"
        response += f"- **Health Checks Passed:** {health_passed}/{total_sites}\n"
        response += f"- **SEO Audits Passed:** {seo_passed}/{total_sites}\n\n"

        response += "## Site-by-Site Results\n\n"

        for result in results:
            site = result["site"]
            health = result["health_check"]
            seo = result["seo_audit"]

            response += f"### {site}\n"
            response += f"**Health Check:** {'✅' if health['passed'] else '❌'} {health['message']}\n"
            response += f"**SEO Audit:** {'✅' if seo['passed'] else '❌'} {seo['message']}\n\n"

        response += "## Next Steps\n\n"
        if health_passed < total_sites or seo_passed < total_sites:
            response += "⚠️ **Action Required:** Address issues identified above\n\n"
            response += "**Priority Order:**\n"
            response += "1. Fix accessibility/server issues\n"
            response += "2. Resolve security vulnerabilities\n"
            response += "3. Improve SEO optimization\n"
            response += "4. Enhance performance\n"
        else:
            response += "🎉 **All validations passed!** Continue monitoring site health.\n"

        return response


def main():
    """Main entry point for MCP server."""
    server = ValidationAuditServer()

    @server.server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="wordpress_health_check",
                description="Perform comprehensive WordPress health check for a site",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site": {
                            "type": "string",
                            "description": "The WordPress site domain to check (e.g., 'freerideinvestor.com')"
                        }
                    },
                    "required": ["site"]
                }
            ),
            Tool(
                name="validate_closure_format",
                description="Validate that a session closure follows the required A+++ format",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file": {
                            "type": "string",
                            "description": "Path to the closure markdown file"
                        }
                    },
                    "required": ["file"]
                }
            ),
            Tool(
                name="audit_website_seo",
                description="Audit website for SEO optimization and best practices",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "site": {
                            "type": "string",
                            "description": "The website domain to audit"
                        }
                    },
                    "required": ["site"]
                }
            ),
            Tool(
                name="validate_p0_sites",
                description="Comprehensive validation of all P0 sites including health checks and SEO audits",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]

    @server.server.call_tool()
    async def call_tool(name: str, arguments: dict):
        try:
            if name == "wordpress_health_check":
                return await server.wordpress_health_check(arguments["site"])
            elif name == "validate_closure_format":
                return await server.validate_closure_format(arguments["file"])
            elif name == "audit_website_seo":
                return await server.audit_website_seo(arguments["site"])
            elif name == "validate_p0_sites":
                return await server.validate_p0_sites()
            else:
                return f"Error: Unknown tool '{name}'"
        except Exception as e:
            return f"Error executing tool '{name}': {str(e)}"

    import asyncio
    asyncio.run(server.server.run())


if __name__ == "__main__":
    main()