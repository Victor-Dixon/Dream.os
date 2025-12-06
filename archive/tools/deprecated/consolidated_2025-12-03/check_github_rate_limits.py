#!/usr/bin/env python3
"""
Check GitHub Rate Limits - All Methods
======================================

Checks rate limits for all GitHub API access methods:
- GitHub CLI (gh)
- GitHub REST API
- GitHub GraphQL API

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-26
License: MIT
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, Optional
import requests


def check_gh_cli_rate_limit() -> Optional[Dict]:
    """Check GitHub CLI rate limit."""
    try:
        result = subprocess.run(
            ['gh', 'api', 'rate_limit'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                "method": "GitHub CLI (gh)",
                "limit": data.get("resources", {}).get("core", {}).get("limit", 0),
                "remaining": data.get("resources", {}).get("core", {}).get("remaining", 0),
                "reset": data.get("resources", {}).get("core", {}).get("reset", 0),
                "used": data.get("resources", {}).get("core", {}).get("used", 0),
                "status": "✅ Available"
            }
        else:
            return {
                "method": "GitHub CLI (gh)",
                "status": "❌ Not available",
                "error": result.stderr.strip()[:100]
            }
    except FileNotFoundError:
        return {
            "method": "GitHub CLI (gh)",
            "status": "❌ Not installed",
            "error": "gh command not found"
        }
    except Exception as e:
        return {
            "method": "GitHub CLI (gh)",
            "status": "❌ Error",
            "error": str(e)[:100]
        }


def check_rest_api_rate_limit(token: Optional[str] = None) -> Dict:
    """Check GitHub REST API rate limit."""
    try:
        # Try to get token from environment or gh config
        if not token:
            try:
                result = subprocess.run(
                    ['gh', 'auth', 'token'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    token = result.stdout.strip()
            except:
                pass
        
        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'
        
        response = requests.get('https://api.github.com/rate_limit', headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            core = data.get("resources", {}).get("core", {})
            search = data.get("resources", {}).get("search", {})
            
            return {
                "method": "GitHub REST API",
                "core": {
                    "limit": core.get("limit", 0),
                    "remaining": core.get("remaining", 0),
                    "reset": core.get("reset", 0),
                    "used": core.get("used", 0)
                },
                "search": {
                    "limit": search.get("limit", 0),
                    "remaining": search.get("remaining", 0),
                    "reset": search.get("reset", 0),
                    "used": search.get("used", 0)
                },
                "status": "✅ Available"
            }
        else:
            return {
                "method": "GitHub REST API",
                "status": "❌ Error",
                "error": f"HTTP {response.status_code}: {response.text[:100]}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "method": "GitHub REST API",
            "status": "❌ Error",
            "error": str(e)[:100]
        }
    except Exception as e:
        return {
            "method": "GitHub REST API",
            "status": "❌ Error",
            "error": str(e)[:100]
        }


def check_graphql_api_rate_limit(token: Optional[str] = None) -> Dict:
    """Check GitHub GraphQL API rate limit."""
    try:
        # Try to get token from environment or gh config
        if not token:
            try:
                result = subprocess.run(
                    ['gh', 'auth', 'token'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    token = result.stdout.strip()
            except:
                pass
        
        if not token:
            return {
                "method": "GitHub GraphQL API",
                "status": "❌ No token",
                "error": "GitHub token required"
            }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        query = """
        query {
            rateLimit {
                limit
                remaining
                resetAt
                used
            }
        }
        """
        
        response = requests.post(
            'https://api.github.com/graphql',
            headers=headers,
            json={'query': query},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                return {
                    "method": "GitHub GraphQL API",
                    "status": "❌ Error",
                    "error": str(data.get("errors", []))[:100]
                }
            
            rate_limit = data.get("data", {}).get("rateLimit", {})
            return {
                "method": "GitHub GraphQL API",
                "limit": rate_limit.get("limit", 0),
                "remaining": rate_limit.get("remaining", 0),
                "reset": rate_limit.get("resetAt", ""),
                "used": rate_limit.get("used", 0),
                "status": "✅ Available"
            }
        else:
            return {
                "method": "GitHub GraphQL API",
                "status": "❌ Error",
                "error": f"HTTP {response.status_code}: {response.text[:100]}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "method": "GitHub GraphQL API",
            "status": "❌ Error",
            "error": str(e)[:100]
        }
    except Exception as e:
        return {
            "method": "GitHub GraphQL API",
            "status": "❌ Error",
            "error": str(e)[:100]
        }


def format_rate_limit_report(results: list) -> str:
    """Format rate limit results as a report."""
    report = "# GitHub Rate Limits Report\n\n"
    report += "**Date**: 2025-11-26\n"
    report += "**Generated By**: Agent-2 (Architecture & Design Specialist)\n\n"
    report += "---\n\n"
    
    for result in results:
        method = result.get("method", "Unknown")
        status = result.get("status", "❓ Unknown")
        
        report += f"## {method}\n\n"
        report += f"**Status**: {status}\n\n"
        
        if status == "✅ Available":
            if "limit" in result:
                # Simple rate limit (CLI, GraphQL)
                limit = result.get("limit", 0)
                remaining = result.get("remaining", 0)
                used = result.get("used", 0)
                reset = result.get("reset", 0)
                
                percentage = (remaining / limit * 100) if limit > 0 else 0
                
                report += f"- **Limit**: {limit:,}\n"
                report += f"- **Remaining**: {remaining:,} ({percentage:.1f}%)\n"
                report += f"- **Used**: {used:,}\n"
                if reset:
                    from datetime import datetime
                    if isinstance(reset, (int, float)):
                        reset_time = datetime.fromtimestamp(reset)
                    else:
                        reset_time = reset
                    report += f"- **Reset**: {reset_time}\n"
                
                # Visual indicator
                if percentage > 75:
                    report += f"- **Status**: 🟢 **Excellent** ({percentage:.1f}% remaining)\n"
                elif percentage > 50:
                    report += f"- **Status**: 🟡 **Good** ({percentage:.1f}% remaining)\n"
                elif percentage > 25:
                    report += f"- **Status**: 🟠 **Low** ({percentage:.1f}% remaining)\n"
                else:
                    report += f"- **Status**: 🔴 **Critical** ({percentage:.1f}% remaining)\n"
            
            elif "core" in result:
                # REST API (has core and search)
                core = result.get("core", {})
                search = result.get("search", {})
                
                core_limit = core.get("limit", 0)
                core_remaining = core.get("remaining", 0)
                core_percentage = (core_remaining / core_limit * 100) if core_limit > 0 else 0
                
                search_limit = search.get("limit", 0)
                search_remaining = search.get("remaining", 0)
                search_percentage = (search_remaining / search_limit * 100) if search_limit > 0 else 0
                
                report += "### Core API\n"
                report += f"- **Limit**: {core_limit:,}\n"
                report += f"- **Remaining**: {core_remaining:,} ({core_percentage:.1f}%)\n"
                report += f"- **Used**: {core.get('used', 0):,}\n"
                
                if core_percentage > 75:
                    report += f"- **Status**: 🟢 **Excellent** ({core_percentage:.1f}% remaining)\n"
                elif core_percentage > 50:
                    report += f"- **Status**: 🟡 **Good** ({core_percentage:.1f}% remaining)\n"
                elif core_percentage > 25:
                    report += f"- **Status**: 🟠 **Low** ({core_percentage:.1f}% remaining)\n"
                else:
                    report += f"- **Status**: 🔴 **Critical** ({core_percentage:.1f}% remaining)\n"
                
                report += "\n### Search API\n"
                report += f"- **Limit**: {search_limit:,}\n"
                report += f"- **Remaining**: {search_remaining:,} ({search_percentage:.1f}%)\n"
                report += f"- **Used**: {search.get('used', 0):,}\n"
                
                if search_percentage > 75:
                    report += f"- **Status**: 🟢 **Excellent** ({search_percentage:.1f}% remaining)\n"
                elif search_percentage > 50:
                    report += f"- **Status**: 🟡 **Good** ({search_percentage:.1f}% remaining)\n"
                elif search_percentage > 25:
                    report += f"- **Status**: 🟠 **Low** ({search_percentage:.1f}% remaining)\n"
                else:
                    report += f"- **Status**: 🔴 **Critical** ({search_percentage:.1f}% remaining)\n"
        else:
            error = result.get("error", "Unknown error")
            report += f"**Error**: {error}\n"
        
        report += "\n---\n\n"
    
    return report


def main():
    """Main execution."""
    print("=" * 60)
    print("🔍 GITHUB RATE LIMITS CHECKER")
    print("=" * 60)
    print()
    
    results = []
    
    # Check GitHub CLI
    print("📊 Checking GitHub CLI (gh)...")
    gh_result = check_gh_cli_rate_limit()
    results.append(gh_result)
    if gh_result.get("status") == "✅ Available":
        remaining = gh_result.get("remaining", 0)
        limit = gh_result.get("limit", 0)
        percentage = (remaining / limit * 100) if limit > 0 else 0
        print(f"   ✅ {remaining:,}/{limit:,} remaining ({percentage:.1f}%)")
    else:
        print(f"   {gh_result.get('status', '❓')}")
    print()
    
    # Check REST API
    print("📊 Checking GitHub REST API...")
    rest_result = check_rest_api_rate_limit()
    results.append(rest_result)
    if rest_result.get("status") == "✅ Available":
        core_remaining = rest_result.get("core", {}).get("remaining", 0)
        core_limit = rest_result.get("core", {}).get("limit", 0)
        core_percentage = (core_remaining / core_limit * 100) if core_limit > 0 else 0
        print(f"   ✅ Core: {core_remaining:,}/{core_limit:,} remaining ({core_percentage:.1f}%)")
        
        search_remaining = rest_result.get("search", {}).get("remaining", 0)
        search_limit = rest_result.get("search", {}).get("limit", 0)
        search_percentage = (search_remaining / search_limit * 100) if search_limit > 0 else 0
        print(f"   ✅ Search: {search_remaining:,}/{search_limit:,} remaining ({search_percentage:.1f}%)")
    else:
        print(f"   {rest_result.get('status', '❓')}")
    print()
    
    # Check GraphQL API
    print("📊 Checking GitHub GraphQL API...")
    graphql_result = check_graphql_api_rate_limit()
    results.append(graphql_result)
    if graphql_result.get("status") == "✅ Available":
        remaining = graphql_result.get("remaining", 0)
        limit = graphql_result.get("limit", 0)
        percentage = (remaining / limit * 100) if limit > 0 else 0
        print(f"   ✅ {remaining:,}/{limit:,} remaining ({percentage:.1f}%)")
    else:
        print(f"   {graphql_result.get('status', '❓')}")
    print()
    
    # Generate report
    report_file = Path("github_rate_limits_report.md")
    report = format_rate_limit_report(results)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Report saved to: {report_file}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("❌ Error: requests library not installed")
        print("   Install with: pip install requests")
        sys.exit(1)
    
    main()

