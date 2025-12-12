"""
<!-- SSOT Domain: infrastructure -->
SFTP Credential Troubleshooter - V2 Compliant
=============================================

Comprehensive SFTP authentication troubleshooting tool.
Tests credentials, provides diagnostics, and suggests fixes.

V2 Compliance: ≤400 lines, comprehensive error handling, type hints.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SFTPCredentialTroubleshooter:
    """Comprehensive SFTP credential troubleshooting."""

    def __init__(self):
        """Initialize troubleshooter."""
        self.results = []

    def load_credentials(self) -> Dict[str, Optional[str]]:
        """Load credentials from .env."""
        return {
            "host": os.getenv("HOSTINGER_HOST") or os.getenv("SSH_HOST"),
            "username": os.getenv("HOSTINGER_USER") or os.getenv("SSH_USER"),
            "password": os.getenv("HOSTINGER_PASS") or os.getenv("SSH_PASS"),
            "port": os.getenv("HOSTINGER_PORT") or os.getenv("SSH_PORT", "65002"),
        }

    def test_connection(
        self, host: str, username: str, password: str, port: int
    ) -> Tuple[bool, str, Optional[Exception]]:
        """
        Test SFTP connection with detailed diagnostics.
        
        Returns:
            (success, message, exception)
        """
        if not HAS_PARAMIKO:
            return False, "paramiko not installed", None

        try:
            logger.info(f"Testing connection to {host}:{port} as {username}")
            
            # Create transport
            transport = paramiko.Transport((host, int(port)))
            
            # Try connection with timeout
            transport.start_client(timeout=TimeoutConstants.HTTP_SHORT)
            transport.auth_password(username=username, password=password)
            
            # Create SFTP client
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            # Test by listing directory
            sftp.listdir(".")
            
            # Success
            sftp.close()
            transport.close()
            
            return True, "Connection successful!", None

        except paramiko.AuthenticationException as e:
            return False, "Authentication failed - username or password incorrect", e
        except paramiko.SSHException as e:
            return False, f"SSH error: {str(e)}", e
        except paramiko.socket.timeout:
            return False, "Connection timeout - server may be unreachable", None
        except Exception as e:
            return False, f"Connection error: {type(e).__name__}: {str(e)}", e

    def test_password_variations(
        self, host: str, username: str, base_password: str, port: int
    ) -> List[Tuple[str, bool, str]]:
        """
        Test password with common variations (escaping, encoding).
        
        Returns:
            List of (password_variant, success, message) tuples
        """
        variations = [
            (base_password, "Original password"),
            (base_password.replace("#", "\\#"), "Escaped # character"),
            (base_password.replace("!", "\\!"), "Escaped ! character"),
            (base_password.replace("@", "\\@"), "Escaped @ character"),
            (base_password.encode('utf-8').decode('utf-8'), "UTF-8 encoded"),
        ]
        
        results = []
        for password_var, description in variations:
            success, message, _ = self.test_connection(host, username, password_var, port)
            results.append((description, success, message))
            if success:
                logger.info(f"✅ Success with: {description}")
                break
        
        return results

    def test_username_variations(
        self, host: str, base_username: str, password: str, port: int, domain: str = None
    ) -> List[Tuple[str, bool, str]]:
        """
        Test username with common variations.
        
        Returns:
            List of (username_variant, success, message) tuples
        """
        variations = [
            (base_username, "Original username"),
        ]
        
        # Add variations if domain provided
        if domain:
            variations.extend([
                (f"{base_username}@{domain}", "Email format"),
                (f"{base_username}@hostinger.com", "Hostinger email format"),
                (f"u{base_username}", "Prefixed with 'u'"),
            ])
        
        # Extract username from email if email format
        if "@" in base_username:
            username_part = base_username.split("@")[0]
            variations.append((username_part, "Extracted from email"))
        
        results = []
        for username_var, description in variations:
            success, message, _ = self.test_connection(host, username_var, password, port)
            results.append((description, success, message))
            if success:
                logger.info(f"✅ Success with: {description}")
                break
        
        return results

    def diagnose_authentication_failure(
        self, host: str, username: str, password: str, port: int
    ) -> Dict[str, any]:
        """
        Comprehensive authentication diagnosis.
        
        Returns:
            Dictionary with diagnosis results and recommendations
        """
        diagnosis = {
            "host": host,
            "port": port,
            "username": username,
            "password_length": len(password) if password else 0,
            "tests": [],
            "recommendations": [],
        }
        
        # Test 1: Basic connection
        logger.info("Test 1: Basic connection test...")
        success, message, exception = self.test_connection(host, username, password, port)
        diagnosis["tests"].append({
            "test": "Basic Connection",
            "success": success,
            "message": message,
            "exception_type": type(exception).__name__ if exception else None,
        })
        
        if success:
            diagnosis["recommendations"].append("✅ Credentials are correct!")
            return diagnosis
        
        # Test 2: Username variations
        logger.info("Test 2: Testing username variations...")
        username_results = self.test_username_variations(
            host, username, password, port, "freerideinvestor.com"
        )
        diagnosis["tests"].extend([
            {"test": f"Username: {desc}", "success": succ, "message": msg}
            for desc, succ, msg in username_results
        ])
        
        # Test 3: Password variations
        logger.info("Test 3: Testing password variations...")
        password_results = self.test_password_variations(host, username, password, port)
        diagnosis["tests"].extend([
            {"test": f"Password: {desc}", "success": succ, "message": msg}
            for desc, succ, msg in password_results
        ])
        
        # Generate recommendations
        if not any(t["success"] for t in diagnosis["tests"]):
            diagnosis["recommendations"].extend([
                "❌ All credential variations failed",
                "💡 Verify credentials in Hostinger control panel",
                "💡 Check if SFTP is enabled on your Hostinger account",
                "💡 Verify username format (may need cPanel username, not email)",
                "💡 Reset SFTP password in Hostinger if needed",
                "💡 Try manual connection with FileZilla to verify credentials work",
            ])
        
        return diagnosis

    def generate_report(self, diagnosis: Dict[str, any]) -> str:
        """Generate human-readable diagnosis report."""
        report = []
        report.append("=" * 70)
        report.append("🔍 SFTP Credential Troubleshooting Report")
        report.append("=" * 70)
        report.append("")
        report.append(f"Host: {diagnosis['host']}")
        report.append(f"Port: {diagnosis['port']}")
        report.append(f"Username: {diagnosis['username']}")
        report.append(f"Password Length: {diagnosis['password_length']} characters")
        report.append("")
        report.append("Test Results:")
        report.append("-" * 70)
        
        for test in diagnosis["tests"]:
            status = "✅" if test["success"] else "❌"
            report.append(f"{status} {test['test']}: {test['message']}")
        
        report.append("")
        report.append("Recommendations:")
        report.append("-" * 70)
        for rec in diagnosis["recommendations"]:
            report.append(rec)
        
        return "\n".join(report)


def main():
    """CLI entry point."""
    import argparse
from src.core.config.timeout_constants import TimeoutConstants
    
    parser = argparse.ArgumentParser(
        description="SFTP Credential Troubleshooter"
    )
    parser.add_argument(
        "--host",
        help="SFTP host (or use HOSTINGER_HOST from .env)"
    )
    parser.add_argument(
        "--username",
        help="SFTP username (or use HOSTINGER_USER from .env)"
    )
    parser.add_argument(
        "--password",
        help="SFTP password (or use HOSTINGER_PASS from .env)"
    )
    parser.add_argument(
        "--port",
        type=int,
        help="SFTP port (or use HOSTINGER_PORT from .env, default: 65002)"
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save diagnosis report to file"
    )
    
    args = parser.parse_args()
    
    troubleshooter = SFTPCredentialTroubleshooter()
    
    # Load credentials
    creds = troubleshooter.load_credentials()
    
    # Override with CLI args if provided
    host = args.host or creds["host"]
    username = args.username or creds["username"]
    password = args.password or creds["password"]
    port = args.port or int(creds["port"] or 65002)
    
    if not all([host, username, password]):
        print("❌ Missing credentials:")
        if not host:
            print("   - Host (set HOSTINGER_HOST in .env or use --host)")
        if not username:
            print("   - Username (set HOSTINGER_USER in .env or use --username)")
        if not password:
            print("   - Password (set HOSTINGER_PASS in .env or use --password)")
        return 1
    
    print("🔍 Starting SFTP credential troubleshooting...")
    print()
    
    # Run diagnosis
    diagnosis = troubleshooter.diagnose_authentication_failure(
        host, username, password, port
    )
    
    # Generate and print report
    report = troubleshooter.generate_report(diagnosis)
    print(report)
    
    # Save report if requested
    if args.save_report:
        report_file = Path("agent_workspaces/Agent-3/sftp_troubleshooting_report.txt")
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report)
        print(f"\n✅ Report saved: {report_file}")
    
    # Return exit code
    if any(t["success"] for t in diagnosis["tests"]):
        print("\n✅ Credentials verified!")
        return 0
    else:
        print("\n❌ All credential tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

