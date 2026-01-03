#!/usr/bin/env python3
"""
Test Shortcode Directly
=======================

Tests the shortcode execution directly via WP-CLI.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root / "tools"))

from wordpress_manager import WordPressManager

manager = WordPressManager("crosbyultimateevents.com")

# Test shortcode execution
print("Testing shortcode execution...")
stdout, stderr, code = manager.wp_cli(
    'eval \'$output = do_shortcode("[crosby_business_plan]"); '
    'if (empty($output)) { echo "EMPTY_OUTPUT"; } else { echo "SUCCESS: " . strlen($output) . " characters"; echo "\\n\\nFirst 500 chars:\\n" . substr($output, 0, 500); }\''
)

print(f"Exit code: {code}")
print(f"Stdout: {stdout}")
if stderr:
    print(f"Stderr: {stderr}")

# Check for PHP errors
print("\nChecking PHP errors...")
error_stdout, error_stderr, error_code = manager.wp_cli(
    'eval \'$errors = error_get_last(); if ($errors) { print_r($errors); } else { echo "NO_ERRORS"; }\''
)
print(f"Errors: {error_stdout}")

# Check template file path
print("\nChecking template file...")
template_check = manager.wp_cli(
    'eval \'$template = ABSPATH . "wp-content/plugins/crosby-business-plan/templates/business-plan-display.php"; '
    'echo file_exists($template) ? "EXISTS: " . $template : "NOT_FOUND: " . $template;\''
)
print(f"Template check: {template_check[0]}")

