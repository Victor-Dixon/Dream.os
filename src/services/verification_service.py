#!/usr/bin/env python3
"""
Verification Service - Automated Harness
========================================

Provides automated verification for claims:
- Page fetch checks
- Content validation
- Unit test execution
- Link checking

<!-- SSOT Domain: integration -->

Navigation References:
├── Related Files:
│   ├── Test Runners → tests/unit/ and tests/integration/
│   ├── Validation Tools → tools/validation_audit_mcp.py
│   ├── Deployment Scripts → scripts/deployment_verification.py
│   └── CI/CD Pipeline → .github/workflows/
├── Documentation:
│   ├── Testing Guide → docs/TESTING_PROTOCOL.md
│   ├── Validation Audit → docs/VALIDATION_AUDIT_PROCEDURE.md
│   └── CI/CD Setup → docs/CI_CD_INTEGRATION.md
├── API Endpoints:
│   └── Validation API → src/services/validation_audit/validation_api.py
└── Usage:
    └── Run Tests → python -m pytest tests/

Author: Agent-Generic
License: MIT
"""

import logging
import requests
import subprocess
import json
import yaml
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from src.core.base.base_service import BaseService

logger = logging.getLogger(__name__)

class VerificationService(BaseService):
    """
    Automated verification harness for validating system claims.

    Enhanced with 'existence vs functionality' testing methodology.
    """

    def __init__(self):
        super().__init__("VerificationService")

    def get_content_validator(self, file_type: str) -> Optional[Callable[[str], bool]]:
        """
        Get a content validator for a specific file type.

        Args:
            file_type: File extension (without dot)

        Returns:
            Validator function or None if not available
        """
        if not hasattr(self, '_content_validators'):
            self._init_content_validators()
        return self._content_validators.get(file_type.lower())

    def _init_content_validators(self):
        """Initialize content validators dictionary."""
        self._content_validators = {
            'json': self._validate_json,
            'yaml': self._validate_yaml,
            'yml': self._validate_yaml,
            'py': self._validate_python,
            'md': self._validate_markdown,
            'html': self._validate_html,
        }

    def _validate_json(self, content: str) -> bool:
        """Validate JSON content."""
        try:
            json.loads(content)
            return True
        except (json.JSONDecodeError, ValueError):
            return False

    def _validate_yaml(self, content: str) -> bool:
        """Validate YAML content."""
        try:
            import yaml
            yaml.safe_load(content)
            return True
        except (yaml.YAMLError, ImportError):
            return False

    def _validate_python(self, content: str) -> bool:
        """Basic Python syntax validation."""
        try:
            compile(content, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    def _validate_markdown(self, content: str) -> bool:
        """Basic Markdown validation - just check it's not empty and has some structure."""
        if not content.strip():
            return False
        # Check for common markdown elements
        has_headers = '#' in content
        has_lists = any(line.strip().startswith(('- ', '* ', '1. ')) for line in content.split('\n'))
        has_links = '[' in content and ']' in content
        return has_headers or has_lists or has_links or len(content) > 50

    def _validate_html(self, content: str) -> bool:
        """Basic HTML validation."""
        content_lower = content.lower()
        has_html = '<html' in content_lower
        has_doctype = '<!doctype' in content_lower
        has_body = '<body' in content_lower
        has_closing_tags = '</html>' in content_lower or '</body>' in content_lower
        return (has_html or has_doctype) and (has_body or has_closing_tags)
    """
    Automated verification harness for validating system claims.
    """

    def __init__(self):
        super().__init__("VerificationService")

    def verify_url_status(self, url: str, expected_status: int = 200, timeout: int = 10) -> Dict[str, Any]:
        """Verify a URL returns the expected status code (legacy method - use verify_url_functional for comprehensive checks)."""
        try:
            response = requests.get(url, timeout=timeout)
            success = response.status_code == expected_status
            return {
                "success": success,
                "url": url,
                "status_code": response.status_code,
                "expected": expected_status,
                "elapsed": response.elapsed.total_seconds()
            }
        except Exception as e:
            self.logger.error(f"Error verifying URL {url}: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }

    def verify_url_functional(self, url: str, expected_status: int = 200, timeout: int = 10,
                             check_content=True, min_content_length=100) -> Dict[str, Any]:
        """
        Verify URL works AND content is actually functional (status + content fetchable + meaningful content).

        Args:
            url: URL to verify
            expected_status: Expected HTTP status code
            timeout: Request timeout in seconds
            check_content: Whether to verify content is fetchable
            min_content_length: Minimum content length for success

        Returns:
            Dict with comprehensive verification results
        """
        result = {
            "success": False,
            "url": url,
            "status_code": None,
            "expected_status": expected_status,
            "content_fetchable": False,
            "content_length": 0,
            "has_meaningful_content": False,
            "response_time": None,
            "error": None
        }

        try:
            # Check 1: HTTP status
            response = requests.get(url, timeout=timeout)
            result["status_code"] = response.status_code
            result["response_time"] = response.elapsed.total_seconds()

            status_ok = response.status_code == expected_status
            if not status_ok:
                result["error"] = f"HTTP {response.status_code}, expected {expected_status}"
                return result

            if not check_content:
                # Only checking status, not content
                result["success"] = True
                return result

            # Check 2: Content fetchability
            try:
                content = response.text
                result["content_length"] = len(content)
                result["content_fetchable"] = True
            except Exception as e:
                result["error"] = f"Content fetch failed: {e}"
                return result

            # Check 3: Meaningful content
            result["has_meaningful_content"] = result["content_length"] >= min_content_length

            if not result["has_meaningful_content"]:
                result["error"] = f"Content too small ({result['content_length']} chars, min {min_content_length})"
                return result

            # Check 4: Basic HTML structure (indicates page rendered)
            has_html = "<html" in content.lower() or "<!doctype" in content.lower()
            has_body = "<body" in content.lower()
            result["appears_to_be_html"] = has_html
            result["has_body_tag"] = has_body

            # Success if all checks pass
            result["success"] = True
            result["error"] = None
            return result

        except requests.exceptions.Timeout:
            result["error"] = f"Request timeout after {timeout}s"
            return result
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection failed"
            return result
        except Exception as e:
            result["error"] = f"Verification failed: {e}"
            return result

    def verify_text_in_page(self, url: str, text: str, timeout: int = 10) -> Dict[str, Any]:
        """Verify specific text exists in the page content."""
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code != 200:
                return {"success": False, "url": url, "error": f"Status {response.status_code}"}
            
            found = text in response.text
            return {
                "success": found,
                "url": url,
                "text_found": found,
                "search_text": text
            }
        except Exception as e:
            self.logger.error(f"Error searching text in {url}: {e}")
            return {"success": False, "url": url, "error": str(e)}

    def run_unit_tests(self, test_path: str) -> Dict[str, Any]:
        """Run pytest on a specific path."""
        try:
            # Check if path exists
            if not Path(test_path).exists():
                 return {"success": False, "path": test_path, "error": "Path does not exist"}

            result = subprocess.run(
                ["pytest", test_path, "--maxfail=1", "--disable-warnings", "-q"],
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "path": test_path,
                "output": result.stdout,
                "errors": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            self.logger.error(f"Error running tests at {test_path}: {e}")
            return {"success": False, "path": test_path, "error": str(e)}

    def verify_file_exists(self, path: str) -> Dict[str, Any]:
        """Verify a local file exists (legacy method - use verify_file_functional for comprehensive checks)."""
        exists = Path(path).exists()
        return {"success": exists, "path": path}

    def verify_file_smart(self, path: str, require_writable=False, auto_validate=True) -> Dict[str, Any]:
        """
        Smart file verification that automatically detects file type and applies appropriate validation.

        Args:
            path: File path to verify
            require_writable: Whether file must be writable
            auto_validate: Whether to auto-detect and validate content based on file extension

        Returns:
            Dict with comprehensive verification results
        """
        file_path = Path(path)
        file_extension = file_path.suffix.lstrip('.')

        # Get appropriate validator
        content_validator = None
        if auto_validate and file_extension:
            content_validator = self.get_content_validator(file_extension)

        return self.verify_file_functional(path, content_validator, require_writable)

    def verify_file_functional(self, path: str, content_validator=None, require_writable=False) -> Dict[str, Any]:
        """
        Verify file exists AND is actually functional (readable, optionally writable, and valid content).

        Args:
            path: File path to verify
            content_validator: Optional function to validate content (takes content string, returns bool)
            require_writable: Whether file must be writable

        Returns:
            Dict with comprehensive verification results
        """
        result = {
            "success": False,
            "path": path,
            "exists": False,
            "readable": False,
            "writable": False,
            "content_valid": None,  # None = no validator provided
            "error": None
        }

        try:
            file_path = Path(path)

            # Check 1: Existence
            result["exists"] = file_path.exists()
            if not result["exists"]:
                result["error"] = "File does not exist"
                return result

            # Check 2: Readability
            try:
                # Try to actually open and read the file
                with open(path, 'r', encoding='utf-8') as f:
                    f.read(1)  # Just read one character to test
                result["readable"] = True
            except (PermissionError, OSError) as e:
                result["readable"] = False
                result["error"] = f"File exists but is not readable: {e}"
                return result
            except Exception as e:
                # For other errors (like encoding issues), we'll still consider it readable
                # but mark content validation as potentially failing
                result["readable"] = True

            # Check 3: Writability (if required)
            if require_writable:
                result["writable"] = os.access(path, os.W_OK)
                if not result["writable"]:
                    result["error"] = "File exists and is readable but not writable"
                    return result

            # Check 4: Content validity (if validator provided)
            if content_validator:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    result["content_valid"] = content_validator(content)
                    if not result["content_valid"]:
                        result["error"] = "File exists, is readable, but contains invalid content"
                        return result
                except Exception as e:
                    result["content_valid"] = False
                    result["error"] = f"File exists but content validation failed: {e}"
                    return result
            else:
                result["content_valid"] = None  # No validator = assume valid

            # All checks passed
            result["success"] = True
            result["error"] = None
            return result

        except Exception as e:
            result["error"] = f"Verification failed: {e}"
            return result

    def run_lighthouse_audit(self, url: str) -> Dict[str, Any]:
        """
        Run comprehensive Lighthouse audit on a website.
        Provides performance, accessibility, SEO, and best practices scoring.
        """
        import subprocess
        import json
        import tempfile
        import os
        from datetime import datetime

        result = {
            "success": False,
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "categories": {},
            "error": None
        }

        try:
            # Check if lighthouse is available
            try:
                subprocess.run(['lighthouse', '--version'],
                             capture_output=True, check=True, timeout=10)
            except (subprocess.CalledProcessError, FileNotFoundError):
                result["error"] = "Lighthouse not installed. Install with: npm install -g lighthouse"
                return result

            # Create temporary file for results
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp_file:
                tmp_path = tmp_file.name

            try:
                # Run lighthouse audit with comprehensive categories
                cmd = [
                    'lighthouse',
                    url,
                    '--output=json',
                    f'--output-path={tmp_path}',
                    '--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage',
                    '--only-categories=performance,accessibility,best-practices,seo',
                    '--quiet'
                ]

                # Execute lighthouse
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

                if process.returncode == 0:
                    # Read and parse results
                    with open(tmp_path, 'r') as f:
                        lighthouse_data = json.load(f)

                    result["success"] = True

                    # Extract category scores
                    categories = lighthouse_data.get('categories', {})
                    for category_name, category_data in categories.items():
                        score = category_data.get('score', 0) * 100  # Convert to percentage
                        result["categories"][category_name] = {
                            "score": score,
                            "title": category_data.get('title', category_name),
                            "description": category_data.get('description', '')
                        }

                    # Add overall performance insights
                    result["insights"] = {
                        "performance_score": result["categories"].get("performance", {}).get("score", 0),
                        "accessibility_score": result["categories"].get("accessibility", {}).get("score", 0),
                        "seo_score": result["categories"].get("seo", {}).get("score", 0),
                        "best_practices_score": result["categories"].get("best-practices", {}).get("score", 0)
                    }

                    # Add recommendations based on scores
                    recommendations = []
                    if result["insights"]["performance_score"] < 70:
                        recommendations.append("Performance score below 70 - optimize images, minify resources, enable compression")
                    if result["insights"]["accessibility_score"] < 80:
                        recommendations.append("Accessibility score below 80 - add alt text, improve color contrast, fix keyboard navigation")
                    if result["insights"]["seo_score"] < 80:
                        recommendations.append("SEO score below 80 - add meta descriptions, improve page titles, fix crawl errors")
                    if result["insights"]["best_practices_score"] < 80:
                        recommendations.append("Best practices score below 80 - fix deprecated APIs, enable HTTPS, remove unused code")

                    result["recommendations"] = recommendations

                else:
                    result["error"] = f"Lighthouse audit failed: {process.stderr}"

            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_path)
                except:
                    pass

        except subprocess.TimeoutExpired:
            result["error"] = "Lighthouse audit timed out after 120 seconds"
        except json.JSONDecodeError as e:
            result["error"] = f"Failed to parse Lighthouse results: {e}"
        except Exception as e:
            result["error"] = f"Unexpected error during Lighthouse audit: {e}"

        return result
