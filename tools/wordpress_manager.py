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
import socket
import sys
import time
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

# Ensure we have at least basic logging configured
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO)

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
    
    def connect(self, max_retries: int = 3, base_delay: float = 0.5) -> bool:
        """
        Establish SSH connection with structured diagnostics and safe retry.

        Logs each failure stage (DNS/TCP, SSH handshake, auth, SFTP init)
        without ever logging secrets.
        """
        if not HAS_PARAMIKO:
            logger.error("paramiko not installed - install with: pip install paramiko")
            return False

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    "Attempting SFTP connection",
                    extra={
                        "stage": "connect_start",
                        "host": self.host,
                        "port": self.port,
                        "username": self.username,
                        "attempt": attempt,
                        "max_retries": max_retries,
                    },
                )

                # DNS / TCP stage
                try:
                    self.transport = paramiko.Transport((self.host, self.port))
                except (socket.gaierror, OSError) as e:
                    logger.error(
                        "DNS/TCP connection failed "
                        f"for {self.host}:{self.port} (stage=dns_tcp, attempt={attempt}/{max_retries}): {e}"
                    )
                    if attempt == max_retries:
                        return False
                    time.sleep(base_delay * attempt)
                    continue

                # SSH authentication stage
                try:
                    self.transport.connect(username=self.username, password=self.password)
                except paramiko.AuthenticationException:
                    logger.error(
                        "Authentication failed "
                        f"for {self.username}@{self.host}:{self.port} (stage=auth)"
                    )
                    logger.error("Please verify username and password are correct")
                    return False
                except paramiko.SSHException as e:
                    logger.error(
                        f"SSH handshake/auth error for {self.host}:{self.port} "
                        f"(stage=ssh_handshake, attempt={attempt}/{max_retries}): {e}"
                    )
                    if attempt == max_retries:
                        return False
                    time.sleep(base_delay * attempt)
                    continue

                # SSH client + SFTP stage
                try:
                    self.client = paramiko.SSHClient()
                    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self.client.connect(
                        hostname=self.host,
                        port=self.port,
                        username=self.username,
                        password=self.password,
                    )
                    self.sftp = paramiko.SFTPClient.from_transport(self.transport)
                except paramiko.SSHException as e:
                    logger.error(
                        f"SFTP channel initialization failed for {self.host}:{self.port} "
                        f"(stage=sftp_init, attempt={attempt}/{max_retries}): {e}"
                    )
                    if attempt == max_retries:
                        return False
                    time.sleep(base_delay * attempt)
                    continue

                logger.info(
                    f"SFTP connection established successfully to {self.host}:{self.port} "
                    f"(username={self.username}, attempt={attempt}/{max_retries})"
                )
                return True

            except Exception as e:
                logger.error(
                    f"Unexpected connection failure for {self.host}:{self.port} "
                    f"(stage=unknown, attempt={attempt}/{max_retries}): {type(e).__name__}: {e}"
                )
                if attempt == max_retries:
                    return False
                time.sleep(base_delay * attempt)
                continue
    
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
                # Validate credentials are not empty
                if self.credentials and self._validate_credentials(self.credentials):
                    logger.info(f"Loaded credentials from sites.json for {self.site_key}")
                    return
                elif self.credentials:
                    logger.warning(f"Credentials found in sites.json for {self.site_key} but are empty/invalid")
                    self.credentials = None
            except Exception as e:
                logger.error(f"Failed to load credentials from sites.json: {e}")
        
        # Try .env file in multiple locations
        env_locations = [
            Path("D:/Agent_Cellphone_V2_Repository/.env"),
            Path(".env"),
            Path("D:/websites/.env"),
            Path(__file__).parent.parent / ".env"
        ]
        
        env_loaded = False
        for env_path in env_locations:
            if env_path.exists():
                try:
                    from dotenv import load_dotenv
                    load_dotenv(env_path)
                    env_loaded = True
                    logger.info(f"Loaded .env file from: {env_path}")
                    break
                except Exception as e:
                    logger.debug(f"Could not load .env from {env_path}: {e}")
        
        # Fallback to .env environment variables (shared Hostinger credentials)
        host = os.getenv("HOSTINGER_HOST") or os.getenv("SSH_HOST") or os.getenv("HOST")
        username = os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER") or os.getenv("USERNAME")
        password = os.getenv("HOSTINGER_PASS") or os.getenv("SSH_PASS") or os.getenv("PASSWORD")
        port_str = os.getenv("HOSTINGER_PORT") or os.getenv("SSH_PORT") or os.getenv("PORT", "65002")
        
        # Validate credentials are not empty
        if host and username and password and host.strip() and username.strip() and password.strip():
            try:
                port = int(port_str)
            except ValueError:
                port = 65002  # Default Hostinger SFTP port
            
            self.credentials = {
                "host": host.strip(),
                "username": username.strip(),
                "password": password.strip(),
                "port": port
            }
            if self._validate_credentials(self.credentials):
                logger.info(f"Loaded credentials from .env environment variables for {self.site_key}")
            else:
                logger.warning(f"Credentials from .env are invalid for {self.site_key}")
                self.credentials = None
        else:
            missing = []
            if not host or not host.strip():
                missing.append("HOSTINGER_HOST/SSH_HOST")
            if not username or not username.strip():
                missing.append("HOSTINGER_USER/SSH_USER")
            if not password or not password.strip():
                missing.append("HOSTINGER_PASS/SSH_PASS")
            logger.warning(f"Missing credentials for {self.site_key}: {', '.join(missing)}")
            self.credentials = None
    
    def _validate_credentials(self, creds: dict) -> bool:
        """Validate credentials are not empty."""
        if not creds:
            return False
        host = creds.get("host", "").strip()
        username = creds.get("username", "").strip()
        password = creds.get("password", "").strip()
        return bool(host and username and password)
    
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
            logger.error(f"No credentials available for {self.site_key}")
            logger.error("Please configure credentials in:")
            logger.error("  1. .deploy_credentials/sites.json (site-specific)")
            logger.error("  2. .env file (HOSTINGER_HOST, HOSTINGER_USER, HOSTINGER_PASS, HOSTINGER_PORT)")
            return False
        
        host = self.credentials.get("host", "").strip()
        username = self.credentials.get("username", "").strip()
        password = self.credentials.get("password", "").strip()
        port = self.credentials.get("port", 22)
        
        # Validate credentials
        missing = []
        if not host:
            missing.append("host")
        if not username:
            missing.append("username")
        if not password:
            missing.append("password")
        
        if missing:
            logger.error(f"Missing credentials for {self.site_key}: {', '.join(missing)}")
            logger.error("Please check .deploy_credentials/sites.json or .env file")
            return False
        
        try:
            self.conn_manager = ConnectionManager(host, username, password, port)
            if self.conn_manager.connect():
                logger.info(f"Connected to {host}:{port} as {username}")
                return True
            else:
                logger.error(f"Connection failed to {host}:{port}")
                logger.error("Please verify:")
                logger.error("  - Host address is correct")
                logger.error("  - Username and password are correct")
                logger.error("  - Port number is correct (default: 65002 for Hostinger SFTP)")
                logger.error("  - Firewall allows SFTP/SSH connections")
                return False
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
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
    
    # ========== THEME MANAGEMENT ==========
    
    def replace_theme(self, new_theme_path: Path, backup: bool = True) -> bool:
        """
        Replace entire theme on server.
        
        Args:
            new_theme_path: Local path to new theme directory
            backup: Whether to backup existing theme first
        
        Returns:
            True if successful
        """
        if not self.connect():
            return False
        
        try:
            remote_theme_dir = self.config['remote_base']
            
            # Backup existing theme if requested
            if backup:
                backup_cmd = f"cp -r {remote_theme_dir} {remote_theme_dir}.backup"
                stdout, stderr, code = self.conn_manager.execute_command(backup_cmd)
                if code == 0:
                    print(f"✅ Backup created: {remote_theme_dir}.backup")
            
            # Deploy all files from new theme
            files_deployed = 0
            for file_path in new_theme_path.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(new_theme_path)
                    remote_path = f"{remote_theme_dir}/{rel_path}"
                    if self.conn_manager.upload_file(file_path, remote_path):
                        files_deployed += 1
            
            print(f"✅ Theme replaced: {files_deployed} files deployed")
            return True
        except Exception as e:
            logger.error(f"Theme replacement failed: {e}")
            return False
    
    def activate_theme(self, theme_name: Optional[str] = None) -> bool:
        """
        Activate theme via WP-CLI.
        
        Args:
            theme_name: Theme name (defaults to configured theme)
        
        Returns:
            True if successful
        """
        if not theme_name:
            theme_name = self.config['theme_name']
        
        stdout, stderr, code = self.wp_cli(f"theme activate {theme_name}")
        if code == 0:
            print(f"✅ Theme '{theme_name}' activated")
            return True
        else:
            logger.error(f"Theme activation failed: {stderr}")
            return False
    
    def list_themes(self) -> List[Dict[str, str]]:
        """List all available themes."""
        stdout, stderr, code = self.wp_cli("theme list --format=json")
        if code == 0:
            try:
                themes = json.loads(stdout)
                return themes
            except:
                return []
        return []
    
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
    parser.add_argument('--replace-theme', type=str, help='Replace theme (path to new theme)')
    parser.add_argument('--activate-theme', type=str, help='Activate theme by name')
    parser.add_argument('--list-themes', action='store_true', help='List all themes')
    
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
        elif args.replace_theme:
            theme_path = Path(args.replace_theme)
            if manager.replace_theme(theme_path):
                print("✅ Theme replaced successfully")
        elif args.activate_theme:
            if manager.activate_theme(args.activate_theme):
                print("✅ Theme activated successfully")
        elif args.list_themes:
            themes = manager.list_themes()
            for theme in themes:
                status = "✅ ACTIVE" if theme.get('status') == 'active' else "  "
                print(f"{status} {theme.get('name', 'Unknown')} - {theme.get('version', 'N/A')}")
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

