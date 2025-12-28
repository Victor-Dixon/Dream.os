#!/usr/bin/env python3
"""
Simple WordPress Deployer
==========================

A lightweight WordPress deployment tool that uses site_configs.json
for SFTP credentials. Works without WordPressManager dependency.

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-21
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Dict, Optional, List

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False


REPO_ROOT = Path(__file__).resolve().parents[2]


def _normalize_site_key(site_key: str) -> str:
    """Normalize a domain/site key into an ENV-safe token (e.g. ariajet.site -> ARIAJET_SITE)."""
    token = re.sub(r"[^A-Za-z0-9]+", "_", site_key).upper().strip("_")
    return token or "SITE"


def _load_dotenv_if_available(*candidate_paths: Path) -> None:
    """
    Best-effort .env loading.
    """
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return

    for p in candidate_paths:
        try:
            if p and p.exists():
                load_dotenv(p, override=False)
        except Exception:
            continue


def _get_env_credential(site_key: str, name: str) -> Optional[str]:
    """
    Credential lookup with site-specific override.
    """
    norm = _normalize_site_key(site_key)
    return (
        os.getenv(f"{norm}_{name}")
        or os.getenv(f"HOSTINGER_{name.replace('SFTP_', '')}")
        or os.getenv(name)
    )


def load_hostinger_env_credentials():
    """Load Hostinger credentials from environment variables."""
    _load_dotenv_if_available(REPO_ROOT / ".env")

    host = os.getenv("HOSTINGER_HOST")
    username = os.getenv("HOSTINGER_USER")
    password = os.getenv("HOSTINGER_PASS")
    port = int(os.getenv("HOSTINGER_PORT", "65002"))
    
    if all([host, username, password]):
        return {
            "host": host,
            "username": username,
            "password": password,
            "port": port
        }
    return None


def load_site_configs():
    """Load site configurations from multiple sources."""
    hostinger_creds = load_hostinger_env_credentials()
    default_config = {}
    if hostinger_creds:
        default_config = {
            "default": {
                "host": hostinger_creds["host"],
                "username": hostinger_creds["username"],
                "password": hostinger_creds["password"],
                "port": hostinger_creds["port"]
            }
        }
    
    # Priority 2: .deploy_credentials/sites.json
    sites_json_path = REPO_ROOT / ".deploy_credentials" / "sites.json"
    if sites_json_path.exists():
        try:
            with open(sites_json_path, 'r') as f:
                configs = json.load(f)
                if hostinger_creds:
                    for site_key, site_config in configs.items():
                        if not site_config.get('host'):
                            for k in ["host", "username", "password", "port"]:
                                site_config[k] = hostinger_creds[k]
                return configs
        except Exception as e:
            print(f"⚠️  Could not load sites.json: {e}")
    
    # Priority 3: site_configs.json (check websites repo if not in root)
    config_path = Path(os.getenv("SITE_CONFIGS_PATH", str(REPO_ROOT / "configs" / "site_configs.json")))
    if not config_path.exists():
        # Fallback to websites repo
        fallback_path = Path("D:/websites/configs/site_configs.json")
        if fallback_path.exists():
            config_path = fallback_path

    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                configs = json.load(f)
                if hostinger_creds:
                    for site_key, site_config in configs.items():
                        sftp_config = site_config.get('sftp', {})
                        if not sftp_config.get('host'):
                            for k in ["host", "username", "password", "port"]:
                                sftp_config[k] = hostinger_creds[k]
                return configs
        except Exception as e:
            print(f"❌ Could not load site_configs.json: {e}")
    
    if hostinger_creds:
        return default_config
    
    return {}


class SimpleWordPressDeployer:
    """Simple WordPress deployer using SFTP."""
    
    def __init__(self, site_key: str, site_configs: dict):
        self.site_key = site_key
        self.site_config = None
        self.sftp = None
        self.transport = None
        
        if site_key in site_configs:
            self.site_config = site_configs[site_key]
        else:
            for domain, config in site_configs.items():
                if site_key in domain or domain.endswith(site_key):
                    self.site_config = config
                    break
        
        if not self.site_config:
            raise ValueError(f"Site '{site_key}' not found in configuration")
    
    def connect(self) -> bool:
        if not PARAMIKO_AVAILABLE:
            print("❌ paramiko not installed")
            return False
        
        _load_dotenv_if_available(REPO_ROOT / ".env")

        host = _get_env_credential(self.site_key, "SFTP_HOST") or os.getenv("HOSTINGER_HOST")
        username = _get_env_credential(self.site_key, "SFTP_USER") or os.getenv("HOSTINGER_USER")
        password = _get_env_credential(self.site_key, "SFTP_PASS") or os.getenv("HOSTINGER_PASS")
        port = int(_get_env_credential(self.site_key, "SFTP_PORT") or os.getenv("HOSTINGER_PORT") or "65002")
        
        if not all([host, username, password]):
            if 'sftp' in self.site_config:
                sftp_config = self.site_config.get('sftp', {})
                host = sftp_config.get('host') or host
                username = sftp_config.get('username') or username
                password = sftp_config.get('password') or password
                port = sftp_config.get('port', port)
                remote_path = sftp_config.get('remote_path', '')
            else:
                host = self.site_config.get('host') or host
                username = self.site_config.get('username') or username
                password = self.site_config.get('password') or password
                port = self.site_config.get('port', port)
                remote_path = self.site_config.get('remote_path', '')
        else:
            if 'sftp' in self.site_config:
                remote_path = self.site_config.get('sftp', {}).get('remote_path', '')
            else:
                remote_path = self.site_config.get('remote_path', '')
        
        if not all([host, username, password]):
            return False
        
        self.remote_path = remote_path
        
        try:
            self.transport = paramiko.Transport((host, port))
            self.transport.connect(username=username, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            return True
        except Exception:
            return False
    
    def deploy_file(self, local_path: Path, remote_path: str = None) -> bool:
        if not self.sftp: return False
        try:
            if remote_path:
                full_remote_path = remote_path
            else:
                base_path = getattr(self, 'remote_path', '')
                full_remote_path = f"{base_path}/{local_path.name}" if base_path else local_path.name
            
            full_remote_path = full_remote_path.replace('\\', '/')
            if not full_remote_path.startswith('/'):
                username = self.site_config.get('username') or self.site_config.get('sftp', {}).get('username', '')
                if username and not full_remote_path.startswith(f'/home/{username}'):
                    full_remote_path = f"/home/{username}/{full_remote_path}"
            
            remote_dir = str(Path(full_remote_path).parent)
            parts = remote_dir.strip('/').split('/')
            current = ''
            for part in parts:
                if part:
                    current = f"{current}/{part}" if current else f"/{part}"
                    try:
                        self.sftp.stat(current)
                    except FileNotFoundError:
                        try:
                            self.sftp.mkdir(current)
                        except Exception: pass
            
            self.sftp.put(str(local_path.resolve()), full_remote_path)
            return True
        except Exception:
            return False
    
    def execute_command(self, command: str) -> str:
        if not PARAMIKO_AVAILABLE: return ""
        try:
            _load_dotenv_if_available(REPO_ROOT / ".env")
            host = _get_env_credential(self.site_key, "SFTP_HOST") or os.getenv("HOSTINGER_HOST")
            username = _get_env_credential(self.site_key, "SFTP_USER") or os.getenv("HOSTINGER_USER")
            password = _get_env_credential(self.site_key, "SFTP_PASS") or os.getenv("HOSTINGER_PASS")
            port = int(_get_env_credential(self.site_key, "SFTP_PORT") or os.getenv("HOSTINGER_PORT") or "65002")
            
            if not all([host, username, password]):
                if 'sftp' in self.site_config:
                    sftp_config = self.site_config.get('sftp', {})
                    host = sftp_config.get('host') or host
                    username = sftp_config.get('username') or username
                    password = sftp_config.get('password') or password
                    port = sftp_config.get('port', port)
                else:
                    host = self.site_config.get('host') or host
                    username = self.site_config.get('username') or username
                    password = self.site_config.get('password') or password
                    port = self.site_config.get('port', port)
            
            if not all([host, username, password]): return ""
            
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password, timeout=10)
            stdin, stdout, stderr = ssh.exec_command(command, timeout=30)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            ssh.close()
            return output if output else error
        except Exception:
            return ""

    def check_php_syntax(self, remote_file_path: str) -> Dict[str, any]:
        """
        Check PHP file syntax and return detailed error information with line numbers.
        
        Args:
            remote_file_path: Path to PHP file on remote server
            
        Returns:
            Dictionary with syntax check results including line numbers
        """
        if not self.sftp:
            return {
                "valid": False,
                "error": "Not connected. Call connect() first.",
                "line_number": None,
                "error_message": None
            }
        
        try:
            command = f"php -l {remote_file_path} 2>&1"
            result = self.execute_command(command)
            
            # Parse PHP syntax error output
            if "No syntax errors" in result or "syntax is OK" in result:
                return {
                    "valid": True,
                    "error": None,
                    "line_number": None,
                    "error_message": None,
                    "output": result.strip()
                }
            
            # Extract line number from error message
            # PHP error format: "Parse error: ... in /path/to/file.php on line N"
            import re
            line_match = re.search(r'on line (\d+)', result, re.IGNORECASE)
            line_number = int(line_match.group(1)) if line_match else None
            
            # Extract error type and message
            error_type_match = re.search(r'(Parse error|Fatal error|Warning|Notice):\s*(.+?)(?:\s+in\s|$)', result, re.IGNORECASE | re.DOTALL)
            error_type = error_type_match.group(1) if error_type_match else "Unknown error"
            error_message = error_type_match.group(2).strip() if error_type_match else result.strip()
            
            # Get context around error line if line number found
            context = None
            if line_number:
                try:
                    # Read lines around the error (5 lines before and after)
                    start_line = max(1, line_number - 5)
                    end_line = line_number + 5
                    context_command = f"sed -n '{start_line},{end_line}p' {remote_file_path}"
                    context = self.execute_command(context_command)
                except Exception:
                    context = None
            
            return {
                "valid": False,
                "error": error_type,
                "line_number": line_number,
                "error_message": error_message,
                "output": result.strip(),
                "context": context,
                "file_path": remote_file_path
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Syntax check failed: {str(e)}",
                "line_number": None,
                "error_message": str(e),
                "output": None
            }

    def list_files(self, remote_path: str) -> List[str]:
        """List files in a remote directory."""
        if not self.sftp:
            return []
        
        try:
            return self.sftp.listdir(remote_path)
        except Exception:
            return []

    def file_exists(self, remote_path: str) -> bool:
        """Check if a file exists on the remote server."""
        if not self.sftp:
            return False
        try:
            self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def disconnect(self):
        if self.sftp: self.sftp.close()
        if self.transport: self.transport.close()

