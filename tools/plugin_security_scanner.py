#!/usr/bin/env python3
"""
Plugin Security Scanner - Agent-2 Closure Improvement Tool
Scans WordPress plugin directories for security vulnerabilities like missing index.html files.

Usage:
    python tools/plugin_security_scanner.py --scan-dir /path/to/plugins --fix
"""

import os
import argparse
from pathlib import Path

class PluginSecurityScanner:
    def __init__(self):
        self.issues_found = 0
        self.issues_fixed = 0

    def scan_directory(self, directory: str, fix: bool = False) -> dict:
        """Scan plugin directory for security issues."""
        results = {
            'scanned': 0,
            'issues': [],
            'fixed': []
        }

        plugin_dirs = [d for d in Path(directory).iterdir() if d.is_dir()]

        for plugin_dir in plugin_dirs:
            results['scanned'] += 1
            index_file = plugin_dir / 'index.html'

            if not index_file.exists():
                self.issues_found += 1
                results['issues'].append(str(plugin_dir))

                if fix:
                    self._create_secure_index(index_file)
                    results['fixed'].append(str(plugin_dir))
                    self.issues_fixed += 1

        return results

    def _create_secure_index(self, index_path: Path):
        """Create a secure index.html file."""
        content = """<!DOCTYPE html>
<html>
<head>
    <title>WordPress Plugin</title>
</head>
<body>
    <!-- WordPress Plugin Directory -->
    <!-- This file prevents directory browsing -->
</body>
</html>"""

        index_path.write_text(content)

    def get_summary(self) -> str:
        return f"Security scan completed — {self.issues_found} issues found, {self.issues_fixed} fixed"

def main():
    parser = argparse.ArgumentParser(description='WordPress Plugin Security Scanner')
    parser.add_argument('--scan-dir', required=True, help='Directory to scan for plugins')
    parser.add_argument('--fix', action='store_true', help='Automatically fix found issues')

    args = parser.parse_args()

    scanner = PluginSecurityScanner()
    results = scanner.scan_directory(args.scan_dir, args.fix)

    print(f"Scanned {results['scanned']} plugin directories")
    if results['issues']:
        print(f"Issues found in: {', '.join(results['issues'])}")
    if results['fixed']:
        print(f"Fixed: {', '.join(results['fixed'])}")

    print(scanner.get_summary())

if __name__ == '__main__':
    main()