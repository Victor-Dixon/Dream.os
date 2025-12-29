#!/usr/bin/env python3
"""
Generate Blog Preview
=====================

Generates a standalone HTML preview of the styled blog post.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.post_cycle_report_to_blog import convert_to_html_with_styling

def generate_preview(markdown_file):
    path = Path(markdown_file)
    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strip frontmatter for the body content if present
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    # Get the styled HTML fragment
    styled_html = convert_to_html_with_styling(content)

    # Wrap in a full HTML page structure for browser viewing
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Preview - Victor Style</title>
    <style>
        body {{
            background-color: #121212; /* Slightly darker outer background for contrast */
            margin: 0;
            padding: 40px;
            font-family: sans-serif;
        }}
    </style>
</head>
<body>
    {styled_html}
</body>
</html>
"""

    output_path = project_root / "reports" / "blog_preview.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✅ Preview generated at: {output_path}")
    print("👉 Open this file in your browser to check the style.")

if __name__ == "__main__":
    # Default to the latest generated blog post
    blog_file = project_root / "docs" / "blog" / "cycle_accomplishments_2025-12-28.md"
    generate_preview(blog_file)
