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
from typing import Dict, Any, List, Optional
from pathlib import Path
from src.core.base.base_service import BaseService

logger = logging.getLogger(__name__)

class VerificationService(BaseService):
    """
    Automated verification harness for validating system claims.
    """

    def __init__(self):
        super().__init__("VerificationService")

    def verify_url_status(self, url: str, expected_status: int = 200, timeout: int = 10) -> Dict[str, Any]:
        """Verify a URL returns the expected status code."""
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
        """Verify a local file exists."""
        exists = Path(path).exists()
        return {"success": exists, "path": path}

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
