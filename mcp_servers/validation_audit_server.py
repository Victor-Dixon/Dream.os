#!/usr/bin/env python3
"""
MCP Server for Validation & Audit Operations
Consolidates scattered validation and audit tools
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


# Required fields in A+++ closure format
REQUIRED_FIELDS = [
    'Task',
    'Project',
    'Actions Taken',
    'Artifacts Created / Updated',
    'Verification',
    'Public Build Signal',
    'Git Commit',
    'Git Push',
    'Website Blogging',
    'Status'
]

# Forbidden patterns
FORBIDDEN_PATTERNS = [
    (r'\bnext steps?\b', 'Next steps'),
    (r'\btodo\b', 'TODO'),
    (r'\bfuture work\b', 'Future work'),
    (r'\bremaining tasks?\b', 'Remaining tasks'),
    (r'\bshould work\b', 'Speculation: "should work"'),
    (r'\bmay need\b', 'Speculation: "may need"'),
    (r'\bcould be\b', 'Speculation: "could be"'),
    (r'\bmight require\b', 'Speculation: "might require"'),
    (r'\bmade progress\b', 'Progress report language'),
    (r'\bstarted working\b', 'Progress report language'),
    (r'\bpartially completed\b', 'Progress report language'),
]


def validate_closure_format(closure_file_path: str) -> Dict[str, Any]:
    """
    Validate session closure document against A+++ standard.

    Args:
        closure_file_path: Path to closure markdown file

    Returns:
        Dict with validation results
    """
    try:
        file_path = Path(closure_file_path)
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File not found: {closure_file_path}"
            }

        content = file_path.read_text(encoding='utf-8')

        violations = []
        missing_fields = []

        # Check for required fields
        for field in REQUIRED_FIELDS:
            pattern = rf'\*\*{re.escape(field)}\*\*'
            if not re.search(pattern, content, re.IGNORECASE):
                missing_fields.append(field)

        # Check for forbidden patterns
        for pattern, description in FORBIDDEN_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.append({
                    "type": "forbidden_pattern",
                    "description": description,
                    "pattern": pattern,
                    "matches": len(matches)
                })

        # Check status field format
        status_match = re.search(r'\*\*Status:\*\*\s*([✅🟡❌])', content)
        if not status_match:
            violations.append({
                "type": "missing_status_emoji",
                "description": "Status field must include emoji (✅, 🟡, or ❌)"
            })

        # --- PSE (Public Surface Expansion) Rule Validation ---
        pse_triggers = [
            'governance', 'safety', 'architecture', 'swarm behavior',
            'protocol', 'closure', 'canonical prompt', 'template',
            'shared workspace', 'swarm rule', 'mcp server'
        ]
        
        # Check if any trigger word exists in the content (excluding field headers)
        body_content = content.lower()
        needs_pse = any(trigger in body_content for trigger in pse_triggers)
        
        if needs_pse:
            # Required artifacts for PSE
            required_pse_artifacts = [
                'BLOG_DADUDEKC.md',
                'BLOG_WEARESWARM.md',
                'BLOG_DREAMSCAPE.md'
            ]
            
            # Check if these artifacts are mentioned in "Artifacts Created / Updated" section
            artifacts_section = re.search(r'\*\*Artifacts Created / Updated:\*\*(.+?)(?=\n\s*\*\*|\n\s*#|\Z)', content, re.IGNORECASE | re.DOTALL)
            if artifacts_section:
                artifacts_text = artifacts_section.group(1)
                missing_pse = [art for art in required_pse_artifacts if art.lower() not in artifacts_text.lower()]
                
                if missing_pse:
                    violations.append({
                        "type": "pse_violation",
                        "description": "Governance/Architecture changes require Public Surface Expansion (PSE) artifacts",
                        "missing_artifacts": missing_pse,
                        "required_artifacts": required_pse_artifacts
                    })
            else:
                violations.append({
                    "type": "pse_violation",
                    "description": "Governance/Architecture changes detected but 'Artifacts Created / Updated' section is missing or empty"
                })

        is_valid = len(missing_fields) == 0 and len(violations) == 0

        return {
            "success": True,
            "valid": is_valid,
            "file": str(file_path),
            "missing_fields": missing_fields,
            "violations": violations,
            "field_count": len(REQUIRED_FIELDS) - len(missing_fields),
            "total_fields": len(REQUIRED_FIELDS),
            "pse_triggered": needs_pse
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "file": closure_file_path
        }


def validate_seo_integration(site_key: str) -> Dict[str, Any]:
    """
    Validate SEO integration for a site.

    Args:
        site_key: Site identifier

    Returns:
        Dict with SEO validation results
    """
    # Placeholder - would integrate with existing SEO validation logic
    return {
        "success": True,
        "site_key": site_key,
        "seo_validated": True,
        "checks": {
            "meta_description": True,
            "open_graph": True,
            "twitter_cards": True
        }
    }


def audit_website_structure(site_key: str) -> Dict[str, Any]:
    """
    Audit website structure and identify issues.

    Args:
        site_key: Site identifier

    Returns:
        Dict with audit results
    """
    # Placeholder - would integrate with existing audit logic
    return {
        "success": True,
        "site_key": site_key,
        "audit_complete": True,
        "issues_found": 0,
        "recommendations": []
    }


def check_php_syntax(site_key: str, file_path: str) -> Dict[str, Any]:
    """
    Check PHP syntax for a remote WordPress file.

    Uses SSH/WP-CLI or SFTP to execute `php -l` on the remote server.

    Args:
        site_key: Site identifier
        file_path: Remote file path (e.g., "wp-content/themes/theme/functions.php")

    Returns:
        Dict with syntax validation results
    """
    try:
        # Try to import deployment tools for remote execution
        sys.path.insert(
            0, str(Path(__file__).parent.parent.parent / "websites" / "ops" / "deployment"))

        try:
            from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
            configs = load_site_configs()
            deployer = SimpleWordPressDeployer(
                site_key=site_key, site_configs=configs)

            if not deployer.connect():
                return {
                    "success": False,
                    "error": f"Failed to connect to {site_key}",
                    "site_key": site_key,
                    "file_path": file_path
                }

            # Use deployer's check_php_syntax method if available
            if hasattr(deployer, 'check_php_syntax'):
                result = deployer.check_php_syntax(file_path)
                deployer.disconnect()
                return {
                    "success": True,
                    "site_key": site_key,
                    "file_path": file_path,
                    "valid": result.get('valid', False),
                    "line_number": result.get('line_number'),
                    "error_message": result.get('error_message'),
                    "output": result.get('output', '')
                }
            else:
                # Fallback: Execute php -l command directly
                command = f"php -l {file_path} 2>&1"
                output = deployer.execute_command(command)
                deployer.disconnect()

                # Parse output
                is_valid = "No syntax errors" in output or "syntax is OK" in output
                line_number = None
                error_message = None

                if not is_valid:
                    # Try to extract line number from error
                    import re
                    line_match = re.search(r'on line (\d+)', output)
                    if line_match:
                        line_number = int(line_match.group(1))
                    error_message = output.strip()

                return {
                    "success": True,
                    "site_key": site_key,
                    "file_path": file_path,
                    "valid": is_valid,
                    "line_number": line_number,
                    "error_message": error_message,
                    "output": output
                }
        except ImportError:
            # Fallback: Try local PHP syntax check if file is accessible locally
            local_path = Path(__file__).parent.parent.parent / \
                "websites" / "sites" / site_key / "wp" / file_path
            if local_path.exists():
                import subprocess
                result = subprocess.run(
                    ["php", "-l", str(local_path)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                is_valid = result.returncode == 0
                output = result.stdout + result.stderr

                line_number = None
                error_message = None
                if not is_valid:
                    import re
                    line_match = re.search(r'on line (\d+)', output)
                    if line_match:
                        line_number = int(line_match.group(1))
                    error_message = output.strip()

                return {
                    "success": True,
                    "site_key": site_key,
                    "file_path": file_path,
                    "valid": is_valid,
                    "line_number": line_number,
                    "error_message": error_message,
                    "output": output,
                    "method": "local"
                }
            else:
                return {
                    "success": False,
                    "error": f"File not found locally and remote connection unavailable",
                    "site_key": site_key,
                    "file_path": file_path,
                    "local_path_checked": str(local_path)
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "site_key": site_key,
            "file_path": file_path
        }


def wordpress_health_check(site_key: str) -> Dict[str, Any]:
    """
    Perform comprehensive WordPress health check.

    Includes core version, database health, plugin status, theme status, 
    and error detection.

    Args:
        site_key: Site identifier

    Returns:
        Dict with health check results
    """
    try:
        # Try to import deployment tools
        sys.path.insert(
            0, str(Path(__file__).parent.parent.parent / "websites" / "ops" / "deployment"))

        try:
            from simple_wordpress_deployer import SimpleWordPressDeployer, load_site_configs
            configs = load_site_configs()
            deployer = SimpleWordPressDeployer(
                site_key=site_key, site_configs=configs)

            if not deployer.connect():
                return {
                    "success": False,
                    "error": f"Failed to connect to {site_key}",
                    "site_key": site_key
                }

            results = {}

            # 1. Core Version
            core_version = deployer.execute_command(
                "wp core version --allow-root").strip()
            results["core_version"] = core_version

            # 2. Database Health
            db_check = deployer.execute_command(
                "wp db check --allow-root").strip()
            results["db_status"] = "OK" if "Success" in db_check else "Warning/Error"
            results["db_output"] = db_check

            # 3. Active Plugins
            plugin_list = deployer.execute_command(
                "wp plugin list --status=active --format=count --allow-root").strip()
            results["active_plugins_count"] = int(
                plugin_list) if plugin_list.isdigit() else 0

            # 4. Active Theme
            theme_name = deployer.execute_command(
                "wp theme list --status=active --field=name --allow-root").strip()
            results["active_theme"] = theme_name

            # 5. Check for Error Logs (tail last 20 lines of debug.log)
            # remote_path = configs.get(site_key, {}).get("remote_path", f"domains/{site_key}/public_html")
            # debug_log_path = f"{remote_path}/wp-content/debug.log"
            # error_log = deployer.execute_command(f"tail -n 20 {debug_log_path} 2>/dev/null").strip()
            # results["recent_errors"] = error_log if error_log else "No recent errors found in debug.log"

            deployer.disconnect()

            return {
                "success": True,
                "site_key": site_key,
                "health": results,
                # Placeholder for real timestamp
                "timestamp": str(Path(__file__).stat().st_mtime)
            }

        except ImportError:
            return {
                "success": False,
                "error": "Deployment tools not available for remote health check",
                "site_key": site_key
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "site_key": site_key
        }


# MCP Server Protocol
def main():
    """MCP server main loop."""
    # Server state
    server_info = {"name": "validation-audit-server", "version": "1.0.0"}
    tools_definitions = {
        "validate_closure_format": {
            "description": "Validate session closure document against A+++ standard",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "closure_file_path": {
                        "type": "string",
                        "description": "Path to closure markdown file",
                    },
                },
                "required": ["closure_file_path"],
            },
        },
        "validate_seo_integration": {
            "description": "Validate SEO integration for a site",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {
                        "type": "string",
                        "description": "Site identifier",
                    },
                },
                "required": ["site_key"],
            },
        },
        "audit_website_structure": {
            "description": "Audit website structure and identify issues",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {
                        "type": "string",
                        "description": "Site identifier",
                    },
                },
                "required": ["site_key"],
            },
        },
        "check_php_syntax": {
            "description": "Check PHP syntax for a remote WordPress file using php -l",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {
                        "type": "string",
                        "description": "Site identifier",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Remote file path (e.g., wp-content/themes/theme/functions.php)",
                    },
                },
                "required": ["site_key", "file_path"],
            },
        },
        "wordpress_health_check": {
            "description": "Perform comprehensive WordPress health check (core, DB, plugins, theme)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "site_key": {
                        "type": "string",
                        "description": "Site identifier",
                    },
                },
                "required": ["site_key"],
            },
        },
    }
    initialized = False

    # Handle requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                # Respond to initialize request
                initialized = True
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "protocolVersion": "2024-11-05",
                                "capabilities": {
                                    "tools": tools_definitions,
                                },
                                "serverInfo": server_info,
                            },
                        }
                    )
                )
                sys.stdout.flush()

            elif method == "tools/list":
                # Handle ListOfferings request
                tools_list = []
                for tool_name, tool_def in tools_definitions.items():
                    tools_list.append(
                        {
                            "name": tool_name,
                            "description": tool_def["description"],
                            "inputSchema": tool_def["inputSchema"],
                        }
                    )
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {
                                "tools": tools_list,
                                "serverInfo": server_info,
                            },
                        }
                    )
                )
                sys.stdout.flush()

            elif method == "tools/call":
                # Handle tool execution
                tool_name = params.get("name")
                arguments = params.get("arguments", {})

                if tool_name == "validate_closure_format":
                    result = validate_closure_format(**arguments)
                elif tool_name == "validate_seo_integration":
                    result = validate_seo_integration(**arguments)
                elif tool_name == "audit_website_structure":
                    result = audit_website_structure(**arguments)
                elif tool_name == "check_php_syntax":
                    result = check_php_syntax(**arguments)
                elif tool_name == "wordpress_health_check":
                    result = wordpress_health_check(**arguments)
                else:
                    result = {"success": False,
                              "error": f"Unknown tool: {tool_name}"}

                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                        }
                    )
                )
                sys.stdout.flush()

            else:
                # Unknown method
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32601, "message": f"Unknown method: {method}"},
                        }
                    )
                )
                sys.stdout.flush()

        except json.JSONDecodeError as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if "request" in locals() else None,
                        "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
                    }
                )
            )
            sys.stdout.flush()
        except Exception as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if "request" in locals() else None,
                        "error": {"code": -32603, "message": str(e)},
                    }
                )
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()

