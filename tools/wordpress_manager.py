#!/usr/bin/env python3
"""
Unified WordPress Management Tool
==================================

Single comprehensive tool for all WordPress operations:
- Page creation and setup
- File deployment (SFTP/SSH)
- Database table creation
- Menu management
- Content updates
- WP-CLI commands

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <400 lines
"""

import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Load .env file if available
try:
    from dotenv import load_dotenv, dotenv_values
    env_vars = dotenv_values(".env")
    # Merge into os.environ
    for key, value in env_vars.items():
        if value and key not in os.environ:
            os.environ[key] = value
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages SSH/SFTP connections."""
    
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = None
        self.sftp = None
        self.transport = None
    
    def connect(self) -> bool:
        """Establish SSH connection."""
        if not HAS_PARAMIKO:
            logger.error("paramiko not installed")
            return False
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.host, port=self.port, 
                              username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close connections."""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        if self.transport:
            self.transport.close()
        self.client = None
        self.sftp = None
        self.transport = None
    
    def upload_file(self, local_path: Path, remote_path: str) -> bool:
        """Upload file via SFTP."""
        if not self.sftp:
            return False
        try:
            remote_dir = '/'.join(remote_path.split('/')[:-1])
            try:
                self.sftp.mkdir(remote_dir)
            except:
                pass
            self.sftp.put(str(local_path), remote_path)
            return True
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return False
    
    def execute_command(self, command: str) -> Tuple[str, str, int]:
        """Execute SSH command."""
        if not self.client:
            return "", "Not connected", 1
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            return stdout.read().decode(), stderr.read().decode(), exit_code
        except Exception as e:
            return "", str(e), 1


class WordPressManager:
    """Unified WordPress management tool."""
    
    SITE_CONFIGS = {
        "southwestsecret": {
            "local_path": "D:/websites/southwestsecret.com",
            "theme_name": "southwestsecret",
            "remote_base": "/public_html/wp-content/themes/southwestsecret",
            "function_prefix": "southwestsecret"
        },
        "prismblossom": {
            "local_path": "D:/websites/prismblossom.online",
            "theme_name": "prismblossom",
            "remote_base": "/public_html/wp-content/themes/prismblossom",
            "function_prefix": "prismblossom"
        },
        "prismblossom.online": {
            "local_path": "D:/websites/prismblossom.online",
            "theme_name": "prismblossom",
            "remote_base": "/public_html/wp-content/themes/prismblossom",
            "function_prefix": "prismblossom"
        },
        "freerideinvestor": {
            "local_path": "D:/websites/FreeRideInvestor",
            "theme_name": "freerideinvestor",
            "remote_base": "/public_html/wp-content/themes/freerideinvestor",
            "function_prefix": "freerideinvestor"
        },
        "FreeRideInvestor": {
            "local_path": "D:/websites/FreeRideInvestor",
            "theme_name": "freerideinvestor",
            "remote_base": "/public_html/wp-content/themes/freerideinvestor",
            "function_prefix": "freerideinvestor"
        }
    }
    
    def __init__(self, site_key: str = "prismblossom"):
        """Initialize WordPress manager."""
        self.site_key = site_key
        self.config = self.SITE_CONFIGS.get(site_key)
        if not self.config:
            raise ValueError(f"Unknown site: {site_key}")
        
        self.conn_manager: Optional[ConnectionManager] = None
        self.credentials: Optional[dict] = None
        self._load_credentials()
    
    def _load_credentials(self):
        """Load deployment credentials from sites.json or .env environment variables."""
        # First try sites.json
        creds_file = Path("D:/Agent_Cellphone_V2_Repository/.deploy_credentials/sites.json")
        if creds_file.exists():
            try:
                with open(creds_file) as f:
                    all_creds = json.load(f)
                self.credentials = (
                    all_creds.get(self.site_key) or 
                    all_creds.get(f"{self.site_key}.online") or
                    all_creds.get(self.site_key.replace(".online", ""))
                )
                if self.credentials:
                    return
            except Exception as e:
                logger.error(f"Failed to load credentials from sites.json: {e}")
        
        # Fallback to .env environment variables (shared Hostinger credentials)
        host = os.getenv("HOSTINGER_HOST") or os.getenv("SSH_HOST")
        username = os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER")
        password = os.getenv("HOSTINGER_PASS") or os.getenv("SSH_PASS")
        port_str = os.getenv("HOSTINGER_PORT") or os.getenv("SSH_PORT", "65002")
        
        if host and username and password:
            try:
                port = int(port_str)
            except ValueError:
                port = 65002  # Default Hostinger SFTP port
            
            self.credentials = {
                "host": host,
                "username": username,
                "password": password,
                "port": port
            }
            logger.info(f"Loaded credentials from .env environment variables")
    
    def get_theme_path(self) -> Path:
        """Get local theme directory path."""
        theme_paths = [
            Path(self.config["local_path"]) / "wordpress-theme" / self.config["theme_name"],
            Path(self.config["local_path"]) / "wp-content" / "themes" / self.config["theme_name"],
            Path(self.config["local_path"]),  # For FreeRideInvestor where theme is in root
        ]
        for path in theme_paths:
            if path.exists():
                return path
        raise FileNotFoundError(f"Theme directory not found for {self.site_key}")
    
    # ========== PAGE MANAGEMENT ==========
    
    def create_page(self, page_name: str, page_slug: Optional[str] = None,
                   template_content: Optional[str] = None) -> bool:
        """Create WordPress page with template."""
        page_slug = page_slug or page_name.lower().replace(' ', '-')
        template_name = f"page-{page_slug}.php"
        theme_path = self.get_theme_path()
        
        if not template_content:
            template_content = f"""<?php
/**
 * Template Name: {page_name}
 * @package {self.config['theme_name'].title()}
 */
get_header();
?>
<section class="{page_slug}-section">
    <div class="container">
        <h1>{page_name}</h1>
        <p>Content goes here...</p>
    </div>
</section>
<?php get_footer(); ?>"""
        
        # Create template file
        template_file = theme_path / template_name
        template_file.write_text(template_content, encoding='utf-8')
        
        # Add to functions.php
        function_code = self._generate_page_function(page_name, page_slug, template_name)
        self._add_to_functions_php(function_code)
        
        print(f"✅ Page '{page_name}' created!")
        return True
    
    def _generate_page_function(self, page_name: str, page_slug: str, template_name: str) -> str:
        """Generate page creation function."""
        prefix = self.config["function_prefix"]
        function_name = f"{prefix}_create_{page_slug.replace('-', '_')}_page"
        return f"""// Create {page_name} page
function {function_name}() {{
    if (get_page_by_path('{page_slug}')) return;
    ${page_slug}_page = array(
        'post_title' => '{page_name}',
        'post_name' => '{page_slug}',
        'post_status' => 'publish',
        'post_type' => 'page',
        'page_template' => '{template_name}'
    );
    wp_insert_post(${page_slug}_page);
}}
add_action('after_switch_theme', '{function_name}');"""
    
    def _add_to_functions_php(self, code: str):
        """Add code to functions.php."""
        theme_path = self.get_theme_path()
        functions_file = theme_path / "functions.php"
        content = functions_file.read_text(encoding='utf-8')
        if code not in content:
            content += f"\n\n{code}\n"
            functions_file.write_text(content, encoding='utf-8')
    
    # ========== DEPLOYMENT ==========
    
    def connect(self) -> bool:
        """Connect to deployment server."""
        if not self.credentials:
            logger.error("No credentials available")
            return False
        host = self.credentials.get("host")
        username = self.credentials.get("username")
        password = self.credentials.get("password")
        port = self.credentials.get("port", 22)
        if not all([host, username, password]):
            return False
        self.conn_manager = ConnectionManager(host, username, password, port)
        return self.conn_manager.connect()
    
    def disconnect(self):
        """Disconnect from server."""
        if self.conn_manager:
            self.conn_manager.disconnect()
    
    def deploy_file(self, local_path: Path, remote_path: Optional[str] = None) -> bool:
        """Deploy single file to server."""
        if not self.conn_manager:
            if not self.connect():
                return False
        if not remote_path:
            theme_path = self.get_theme_path()
            if theme_path in local_path.parents:
                rel_path = local_path.relative_to(theme_path)
                remote_path = f"{self.config['remote_base']}/{rel_path}"
            else:
                remote_path = f"{self.config['remote_base']}/{local_path.name}"
        return self.conn_manager.upload_file(local_path, remote_path)
    
    def deploy_theme(self, pattern: str = "*.php") -> int:
        """Deploy all theme files matching pattern."""
        if not self.connect():
            return 0
        theme_path = self.get_theme_path()
        files_deployed = 0
        for file_path in theme_path.glob(pattern):
            if self.deploy_file(file_path):
                files_deployed += 1
                print(f"✅ Deployed: {file_path.name}")
        return files_deployed
    
    # ========== DATABASE ==========
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """Create database table code."""
        prefix = self.config["function_prefix"]
        function_name = f"{prefix}_create_{table_name}_table"
        column_defs = [f"        {k} {v}" for k, v in columns.items()]
        code = f"""// Create {table_name} table
function {function_name}() {{
    global $wpdb;
    $table_name = $wpdb->prefix . '{table_name}';
    $charset_collate = $wpdb->get_charset_collate();
    $sql = "CREATE TABLE IF NOT EXISTS $table_name (
{chr(10).join(column_defs)}
    ) $charset_collate;";
    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}}
add_action('after_switch_theme', '{function_name}');"""
        self._add_to_functions_php(code)
        return True
    
    # ========== MENU ==========
    
    def add_to_menu(self, page_slug: str, menu_text: Optional[str] = None) -> bool:
        """Add page to navigation menu."""
        menu_text = menu_text or page_slug.replace('-', ' ').title()
        prefix = self.config["function_prefix"]
        code = f"""// Add {menu_text} to menu
function {prefix}_add_{page_slug}_menu($items, $args) {{
    if ($args->theme_location == 'primary') {{
        ${page_slug}_page = get_page_by_path('{page_slug}');
        ${page_slug}_url = ${page_slug}_page ? get_permalink(${page_slug}_page->ID) : home_url('/{page_slug}');
        $items .= '<li><a href="' . esc_url(${page_slug}_url) . '">{menu_text}</a></li>';
    }}
    return $items;
}}
add_filter('wp_nav_menu_items', '{prefix}_add_{page_slug}_menu', 10, 2);"""
        self._add_to_functions_php(code)
        return True
    
    # ========== WP-CLI ==========
    
    def wp_cli(self, command: str) -> Tuple[str, str, int]:
        """Execute WP-CLI command."""
        if not self.conn_manager:
            if not self.connect():
                return "", "Not connected", 1
        wp_path = self.credentials.get("wp_cli_path", "wp")
        remote_path = self.credentials.get("remote_path", "/public_html")
        full_cmd = f"cd {remote_path} && {wp_path} {command}"
        return self.conn_manager.execute_command(full_cmd)
    
    # ========== UTILITIES ==========
    
    def list_pages(self) -> List[Dict[str, str]]:
        """List all page templates."""
        theme_path = self.get_theme_path()
        pages = []
        for template_file in theme_path.glob("page-*.php"):
            try:
                content = template_file.read_text(encoding='utf-8')
                template_name = None
                for line in content.split('\n'):
                    if 'Template Name:' in line:
                        template_name = line.split('Template Name:')[-1].strip()
                        break
                pages.append({
                    'file': template_file.name,
                    'template_name': template_name or 'Unknown',
                    'path': str(template_file)
                })
            except Exception as e:
                logger.error(f"Error reading {template_file}: {e}")
        return pages
    
    def verify(self) -> Dict[str, any]:
        """Verify WordPress setup."""
        results = {'theme_exists': False, 'functions_exists': False, 'pages': 0}
        try:
            theme_path = self.get_theme_path()
            results['theme_exists'] = theme_path.exists()
            results['functions_exists'] = (theme_path / "functions.php").exists()
            results['pages'] = len(list(theme_path.glob("page-*.php")))
        except Exception as e:
            logger.error(f"Verification error: {e}")
        return results


def main():
    """CLI interface."""
    import argparse
    parser = argparse.ArgumentParser(description="Unified WordPress Management Tool")
    parser.add_argument('--site', default='prismblossom', help='Site key')
    parser.add_argument('--create-page', type=str, help='Create page')
    parser.add_argument('--deploy', action='store_true', help='Deploy theme files')
    parser.add_argument('--list', action='store_true', help='List pages')
    parser.add_argument('--verify', action='store_true', help='Verify setup')
    parser.add_argument('--add-menu', type=str, help='Add page to menu (slug)')
    
    args = parser.parse_args()
    
    try:
        manager = WordPressManager(args.site)
        
        if args.create_page:
            manager.create_page(args.create_page)
        elif args.deploy:
            count = manager.deploy_theme()
            print(f"✅ Deployed {count} files")
        elif args.list:
            pages = manager.list_pages()
            for p in pages:
                print(f"  • {p['file']} - {p['template_name']}")
        elif args.verify:
            results = manager.verify()
            print(f"Theme exists: {results['theme_exists']}")
            print(f"Functions.php: {results['functions_exists']}")
            print(f"Pages: {results['pages']}")
        elif args.add_menu:
            manager.add_to_menu(args.add_menu)
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

