#!/usr/bin/env python3
"""
WordPress Utilities
Shared utilities for WordPress operations and content management
"""

import logging
from typing import Dict, List, Any, Optional
try:
    from .ssh_utils import SSHManager
except ImportError:
    from ssh_utils import SSHManager

logger = logging.getLogger(__name__)

class WordPressManager:
    """High-level WordPress operations manager"""

    def __init__(self, site_key: str = "tradingrobotplug.com"):
        self.site_key = site_key
        self.ssh_manager = SSHManager(site_key)

    def create_pages_batch(self, pages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Create multiple WordPress pages in batch

        Args:
            pages: List of dicts with 'title', 'slug', and optional 'content' keys

        Returns:
            List of creation results
        """
        results = []

        with self.ssh_manager:
            for page in pages:
                title = page['title']
                slug = page['slug']
                content = page.get('content', f"<h1>{title}</h1><p>Content for {title} page.</p>")

                success, output, error = self.ssh_manager.execute_wp_cli(
                    f'post create --post_type=page --post_title="{title}" --post_name="{slug}" --post_content="{content}" --post_status=publish'
                )

                result = {
                    "title": title,
                    "slug": slug,
                    "success": success,
                    "output": output,
                    "error": error
                }

                results.append(result)
                status = "✅" if success else "❌"
                logger.info(f"{status} Created page: {title}")

        return results

    def update_homepage_content(self, content: str) -> bool:
        """
        Update homepage content

        Args:
            content: New homepage content

        Returns:
            Success status
        """
        with self.ssh_manager:
            success, output, error = self.ssh_manager.execute_wp_cli(
                f'post update 1 --post_content="{content}" --post_title="TradingRobotPlug - Advanced Trading Automation"'
            )

            if success:
                logger.info("✅ Homepage content updated")
                return True
            else:
                logger.error(f"❌ Failed to update homepage: {error}")
                return False

    def manage_menu_items(self, menu_slug: str, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Manage menu items (add/remove/update)

        Args:
            menu_slug: Menu slug (e.g., 'swarm-primary')
            operations: List of operations (add, remove, etc.)

        Returns:
            List of operation results
        """
        results = []

        with self.ssh_manager:
            for op in operations:
                op_type = op.get('type', 'add')

                if op_type == 'add':
                    page_id = op.get('page_id')
                    title = op.get('title', '')

                    if page_id:
                        success, output, error = self.ssh_manager.execute_wp_cli(
                            f'menu item add-post {menu_slug} {page_id} --title="{title}"'
                        )

                        result = {
                            "operation": "add",
                            "page_id": page_id,
                            "title": title,
                            "success": success,
                            "output": output,
                            "error": error
                        }
                    else:
                        result = {"operation": "add", "success": False, "error": "Missing page_id"}

                results.append(result)

        return results

    def search_replace_content(self, old_text: str, new_text: str, tables: str = "wp_posts") -> bool:
        """
        Search and replace content in WordPress database

        Args:
            old_text: Text to replace
            new_text: Replacement text
            tables: Tables to search (default: wp_posts)

        Returns:
            Success status
        """
        with self.ssh_manager:
            success, output, error = self.ssh_manager.execute_wp_cli(
                f'search-replace "{old_text}" "{new_text}" --{tables}'
            )

            if success:
                logger.info(f"✅ Search-replace completed: '{old_text}' → '{new_text}'")
                return True
            else:
                logger.error(f"❌ Search-replace failed: {error}")
                return False

    def get_site_info(self) -> Dict[str, Any]:
        """Get basic WordPress site information"""
        with self.ssh_manager:
            success, output, error = self.ssh_manager.execute_wp_cli('core version')

            return {
                "wp_version_available": success,
                "wp_version": output.strip() if success else None,
                "error": error if not success else None
            }

# Content templates for common pages
PAGE_TEMPLATES = {
    "about": """
<h1>About TradingRobotPlug</h1>

<p><strong>Our Mission:</strong> To democratize algorithmic trading by providing accessible, powerful, and reliable automated trading solutions.</p>

<h2>Our Story</h2>
<p>TradingRobotPlug was founded to bring advanced trading technology to everyone.</p>

<h2>Our Values</h2>
<p><strong>Transparency:</strong> Complete transparency in our strategies and performance.</p>
<p><strong>Reliability:</strong> Enterprise-grade reliability for 24/7 operation.</p>
<p><strong>Education:</strong> We educate traders about automated trading best practices.</p>

<h2>Company Information</h2>
<p><strong>Legal Entity:</strong> TradingRobotPlug LLC</p>
<p><strong>Jurisdiction:</strong> Delaware, United States</p>

<h2>Risk Disclosure</h2>
<p><strong>Important:</strong> Trading involves substantial risk. Past performance does not guarantee future results.</p>
""",

    "contact": """
<h1>Contact Us</h1>

<p>Get in touch with the TradingRobotPlug team.</p>

<h2>Business Inquiries</h2>
<p>Email: legal@tradingrobotplug.com</p>

<h2>Support</h2>
<p>For technical support, please use our support portal.</p>
""",

    "privacy": """
<h1>Privacy Policy</h1>

<p>Your privacy is important to us.</p>

<h2>Data Collection</h2>
<p>We collect minimal data necessary for service operation.</p>

<h2>Data Usage</h2>
<p>Your data is used solely for providing trading services.</p>

<h2>Contact Information</h2>
<p>For privacy concerns: legal@tradingrobotplug.com</p>
""",

    "terms": """
<h1>Terms of Service</h1>

<p>Terms and conditions for using TradingRobotPlug services.</p>

<h2>Acceptance of Terms</h2>
<p>By using our services, you agree to these terms.</p>

<h2>Service Limitations</h2>
<p>We provide automated trading tools but cannot guarantee profits.</p>

<h2>Risk Disclosure</h2>
<p>Trading involves substantial risk of loss.</p>
"""
}

def create_standard_pages(wp_manager: WordPressManager, pages_to_create: List[str]) -> List[Dict[str, Any]]:
    """
    Create standard WordPress pages using templates

    Args:
        wp_manager: WordPressManager instance
        pages_to_create: List of page types to create

    Returns:
        List of creation results
    """
    pages = []

    for page_type in pages_to_create:
        if page_type in PAGE_TEMPLATES:
            pages.append({
                "title": page_type.title(),
                "slug": page_type,
                "content": PAGE_TEMPLATES[page_type]
            })

    return wp_manager.create_pages_batch(pages)

def setup_menu_structure(wp_manager: WordPressManager, menu_config: Dict[str, List[int]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Setup complete menu structure

    Args:
        menu_config: Dict mapping menu slugs to lists of page IDs

    Returns:
        Dict of menu operation results
    """
    results = {}

    for menu_slug, page_ids in menu_config.items():
        operations = [{"type": "add", "page_id": page_id} for page_id in page_ids]
        results[menu_slug] = wp_manager.manage_menu_items(menu_slug, operations)

    return results