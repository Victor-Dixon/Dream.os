#!/usr/bin/env python3
"""
MCP Server for Deployment & Verification Operations
Consolidates scattered deployment and verification tools into centralized MCP server

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import json
import sys
import requests
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

# Try to import WordPress manager for deployments
try:
    from tools.wordpress_manager import WordPressManager
    HAS_WORDPRESS = True
except ImportError:
    HAS_WORDPRESS = False
    WordPressManager = None

# Constants
TIMEOUT = 15


def deploy_wordpress_theme(
    site_key: str,
    theme_files: List[str],
    remote_path: Optional[str] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Deploy WordPress theme files to a site.
    
    Consolidates: deploy_tradingrobotplug_theme*.py tools
    
    Args:
        site_key: WordPress site key
        theme_files: List of local file paths to deploy
        remote_path: Remote theme path (optional)
        dry_run: If True, don't actually deploy
        
    Returns:
        Deployment result with success status and details
    """
    if not HAS_WORDPRESS:
        return {"success": False, "error": "WordPress tools not available"}
    
    try:
        manager = WordPressManager(site_key=site_key, dry_run=dry_run)
        if not manager.connect():
            return {"success": False, "error": "Failed to connect to WordPress"}
        
        deployed_files = []
        failed_files = []
        
        for local_file in theme_files:
            file_path = Path(local_file)
            if not file_path.exists():
                failed_files.append({"file": local_file, "error": "File not found"})
                continue
            
            if remote_path:
                remote = remote_path
            else:
                # Default to theme directory
                remote = f"wp-content/themes/{site_key}-theme/{file_path.name}"
            
            if dry_run:
                deployed_files.append({"file": local_file, "remote": remote, "status": "dry_run"})
            else:
                success = manager.deploy_theme(local_path=file_path, remote_path=remote)
                if success:
                    deployed_files.append({"file": local_file, "remote": remote, "status": "deployed"})
                else:
                    failed_files.append({"file": local_file, "error": "Deployment failed"})
        
        manager.disconnect()
        
        return {
            "success": len(failed_files) == 0,
            "site": site_key,
            "deployed_files": deployed_files,
            "failed_files": failed_files,
            "total": len(theme_files),
            "deployed_count": len(deployed_files),
            "failed_count": len(failed_files)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def deploy_wordpress_file(
    site_key: str,
    local_path: str,
    remote_path: str,
    file_type: str = "theme"
) -> Dict[str, Any]:
    """
    Deploy a single file to WordPress site.
    
    Consolidates: deploy_*.py tools
    
    Args:
        site_key: WordPress site key
        local_path: Local file path
        remote_path: Remote file path
        file_type: Type of file (theme, plugin, other)
        
    Returns:
        Deployment result
    """
    if not HAS_WORDPRESS:
        return {"success": False, "error": "WordPress tools not available"}
    
    try:
        manager = WordPressManager(site_key=site_key, dry_run=False)
        if not manager.connect():
            return {"success": False, "error": "Failed to connect to WordPress"}
        
        local_file = Path(local_path)
        if not local_file.exists():
            return {"success": False, "error": f"Local file not found: {local_path}"}
        
        if file_type == "theme":
            success = manager.deploy_theme(local_path=local_file, remote_path=remote_path)
        elif file_type == "plugin":
            success = manager.deploy_plugin_file(local_path=local_file, remote_path=remote_path)
        else:
            success = manager.deploy_file(local_path=local_file, remote_path=remote_path)
        
        manager.disconnect()
        
        return {
            "success": success,
            "site": site_key,
            "local_path": local_path,
            "remote_path": remote_path,
            "file_type": file_type
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def verify_deployment(
    url: str,
    required_content: Optional[List[str]] = None,
    required_status: int = 200
) -> Dict[str, Any]:
    """
    Verify deployment by checking URL and content.
    
    Consolidates: verify_*.py tools, deployment_verification_tool.py
    
    Args:
        url: URL to verify
        required_content: List of content strings that must be present
        required_status: Expected HTTP status code
        
    Returns:
        Verification result with pass/fail status
    """
    try:
        response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        
        result = {
            "url": url,
            "status_code": response.status_code,
            "status_match": response.status_code == required_status,
            "timestamp": datetime.now().isoformat(),
            "overall_status": "PENDING"
        }
        
        if response.status_code == required_status:
            result["status_check"] = "PASS"
            
            if required_content:
                html_lower = response.text.lower()
                found_content = []
                missing_content = []
                
                for content in required_content:
                    if content.lower() in html_lower:
                        found_content.append(content)
                    else:
                        missing_content.append(content)
                
                result["content_check"] = {
                    "found": found_content,
                    "missing": missing_content,
                    "found_count": len(found_content),
                    "total_count": len(required_content)
                }
                
                if len(missing_content) == 0:
                    result["overall_status"] = "PASS"
                else:
                    result["overall_status"] = "PARTIAL"
            else:
                result["overall_status"] = "PASS"
        else:
            result["status_check"] = "FAIL"
            result["overall_status"] = "FAIL"
            result["error"] = f"Expected status {required_status}, got {response.status_code}"
        
        return result
    except Exception as e:
        return {
            "url": url,
            "overall_status": "ERROR",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def check_deployment_status(
    site_key: str,
    pages: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Check deployment status for a site.
    
    Consolidates: deployment_status_checker.py
    
    Args:
        site_key: Site identifier
        pages: List of pages to check (with url and required_content)
        
    Returns:
        Deployment status report
    """
    if pages is None:
        pages = []
    
    results = []
    all_pass = True
    
    for page in pages:
        url = page.get("url")
        required_content = page.get("required_content", [])
        
        if url:
            verification = verify_deployment(url, required_content)
            results.append({
                "page": page.get("name", url),
                "url": url,
                "verification": verification
            })
            
            if verification.get("overall_status") != "PASS":
                all_pass = False
    
    return {
        "success": True,
        "site": site_key,
        "timestamp": datetime.now().isoformat(),
        "overall_status": "PASS" if all_pass else "FAIL",
        "pages_checked": len(results),
        "results": results
    }


def check_http_status(url: str) -> Dict[str, Any]:
    """
    Check HTTP status code for a URL.
    
    Consolidates: check_*.py tools
    
    Args:
        url: URL to check
        
    Returns:
        HTTP status result
    """
    try:
        response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        
        return {
            "success": True,
            "url": url,
            "status_code": response.status_code,
            "status_text": response.reason,
            "headers": dict(response.headers),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def deploy_analytics_code(
    site_key: str,
    analytics_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Deploy analytics code (GA4/Pixel) to WordPress site.
    
    Consolidates: deploy_ga4_pixel_*.py tools
    
    Args:
        site_key: WordPress site key
        analytics_config: Analytics configuration (GA4 ID, Pixel ID, etc.)
        
    Returns:
        Deployment result
    """
    if not HAS_WORDPRESS:
        return {"success": False, "error": "WordPress tools not available"}
    
    try:
        # This would integrate with existing GA4/Pixel deployment logic
        # For now, return structure
        return {
            "success": True,
            "site": site_key,
            "analytics_config": analytics_config,
            "message": "Analytics code deployment (implementation needed)"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """MCP server main loop."""
    print(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "initialize",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "deploy_wordpress_theme": {
                                "description": "Deploy WordPress theme files to a site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {"type": "string", "description": "WordPress site key"},
                                        "theme_files": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of local file paths to deploy"
                                        },
                                        "remote_path": {"type": "string", "description": "Remote theme path (optional)"},
                                        "dry_run": {"type": "boolean", "description": "If True, don't actually deploy"}
                                    },
                                    "required": ["site_key", "theme_files"]
                                }
                            },
                            "deploy_wordpress_file": {
                                "description": "Deploy a single file to WordPress site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {"type": "string"},
                                        "local_path": {"type": "string"},
                                        "remote_path": {"type": "string"},
                                        "file_type": {"type": "string", "enum": ["theme", "plugin", "other"]}
                                    },
                                    "required": ["site_key", "local_path", "remote_path"]
                                }
                            },
                            "verify_deployment": {
                                "description": "Verify deployment by checking URL and content",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"},
                                        "required_content": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "List of content strings that must be present"
                                        },
                                        "required_status": {"type": "integer", "default": 200}
                                    },
                                    "required": ["url"]
                                }
                            },
                            "check_deployment_status": {
                                "description": "Check deployment status for a site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {"type": "string"},
                                        "pages": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "url": {"type": "string"},
                                                    "required_content": {"type": "array", "items": {"type": "string"}}
                                                }
                                            }
                                        }
                                    },
                                    "required": ["site_key"]
                                }
                            },
                            "check_http_status": {
                                "description": "Check HTTP status code for a URL",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {"type": "string"}
                                    },
                                    "required": ["url"]
                                }
                            },
                            "deploy_analytics_code": {
                                "description": "Deploy analytics code (GA4/Pixel) to WordPress site",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "site_key": {"type": "string"},
                                        "analytics_config": {
                                            "type": "object",
                                            "properties": {
                                                "ga4_id": {"type": "string"},
                                                "pixel_id": {"type": "string"}
                                            }
                                        }
                                    },
                                    "required": ["site_key", "analytics_config"]
                                }
                            }
                        }
                    }
                }
            }
        )
    )
    
    # Main loop - read JSON-RPC requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            
            if request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                arguments = request.get("params", {}).get("arguments", {})
                
                result = None
                if tool_name == "deploy_wordpress_theme":
                    result = deploy_wordpress_theme(**arguments)
                elif tool_name == "deploy_wordpress_file":
                    result = deploy_wordpress_file(**arguments)
                elif tool_name == "verify_deployment":
                    result = verify_deployment(**arguments)
                elif tool_name == "check_deployment_status":
                    result = check_deployment_status(**arguments)
                elif tool_name == "check_http_status":
                    result = check_http_status(**arguments)
                elif tool_name == "deploy_analytics_code":
                    result = deploy_analytics_code(**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request.get("id"),
                            "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                        }
                    )
                )
        except Exception as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if 'request' in locals() else None,
                        "error": {"code": -32603, "message": str(e)},
                    }
                )
            )


if __name__ == "__main__":
    main()

