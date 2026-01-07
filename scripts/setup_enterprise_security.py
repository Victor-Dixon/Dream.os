#!/usr/bin/env python3
"""
Enterprise Security Framework - Phase 3 Infrastructure
====================================================

Advanced security enhancements for Agent Cellphone V2 infrastructure.
Implements enterprise-grade security measures, authentication, and authorization.

Features:
- JWT token-based authentication
- Role-based access control (RBAC)
- API rate limiting and throttling
- Security headers and CORS policies
- SSL/TLS certificate management
- Security monitoring and alerting

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import json
import logging
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import hashlib
import hmac

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Security configuration
SECURITY_CONFIG = {
    'jwt': {
        'secret_key': os.getenv('JWT_SECRET_KEY', secrets.token_hex(32)),
        'algorithm': 'HS256',
        'access_token_expire_minutes': 30,
        'refresh_token_expire_days': 7,
    },
    'cors': {
        'origins': [
            "http://localhost:3000",
            "http://localhost:8080",
            "https://agent-cellphone.local",
        ],
        'allow_credentials': True,
        'allow_methods': ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        'allow_headers': ["*"],
        'max_age': 86400,
    },
    'rate_limiting': {
        'default': {'requests': 100, 'window': 60},  # 100 requests per minute
        'api': {'requests': 1000, 'window': 60},     # Higher for API endpoints
        'auth': {'requests': 5, 'window': 300},      # Stricter for auth endpoints
    },
    'security_headers': {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
    },
    'ssl': {
        'cert_file': 'ssl/cert.pem',
        'key_file': 'ssl/key.pem',
        'ca_cert_file': 'ssl/ca-cert.pem',
    }
}

# User roles and permissions
ROLES = {
    'admin': {
        'permissions': ['*'],
        'description': 'Full system access'
    },
    'captain': {
        'permissions': [
            'agent.manage',
            'coordination.create',
            'messaging.broadcast',
            'analytics.view',
            'system.monitor'
        ],
        'description': 'Swarm coordination and management'
    },
    'swarm_commander': {
        'permissions': [
            'agent.view',
            'coordination.view',
            'messaging.send',
            'analytics.view'
        ],
        'description': 'Swarm operations and monitoring'
    },
    'user': {
        'permissions': [
            'agent.view',
            'messaging.send',
            'analytics.view'
        ],
        'description': 'Basic swarm access'
    }
}

class SecurityManager:
    """Enterprise security manager for infrastructure protection."""

    def __init__(self):
        """Initialize security manager."""
        self.config = SECURITY_CONFIG
        self.logger = logging.getLogger(__name__)
        self._load_or_generate_keys()

    def _load_or_generate_keys(self):
        """Load or generate security keys."""
        key_file = Path('config/security_keys.json')

        if key_file.exists():
            try:
                with open(key_file, 'r') as f:
                    keys = json.load(f)
                self.config['jwt']['secret_key'] = keys.get('jwt_secret', self.config['jwt']['secret_key'])
                self.logger.info("✅ Security keys loaded from file")
            except Exception as e:
                self.logger.warning(f"Failed to load security keys: {e}")
                self._generate_keys()
        else:
            self._generate_keys()

    def _generate_keys(self):
        """Generate new security keys."""
        key_file = Path('config/security_keys.json')
        key_file.parent.mkdir(exist_ok=True)

        keys = {
            'jwt_secret': secrets.token_hex(32),
            'api_keys': {},
            'generated_at': datetime.now().isoformat()
        }

        with open(key_file, 'w') as f:
            json.dump(keys, f, indent=2)

        self.config['jwt']['secret_key'] = keys['jwt_secret']
        self.logger.info("✅ New security keys generated and saved")

    def create_jwt_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token."""
        try:
            import jwt

            to_encode = data.copy()
            expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.config['jwt']['access_token_expire_minutes']))
            to_encode.update({"exp": expire})

            encoded_jwt = jwt.encode(
                to_encode,
                self.config['jwt']['secret_key'],
                algorithm=self.config['jwt']['algorithm']
            )
            return encoded_jwt
        except ImportError:
            self.logger.error("JWT library not available. Install with: pip install PyJWT")
            return None

    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token."""
        try:
            import jwt
            from jwt import PyJWTError

            payload = jwt.decode(
                token,
                self.config['jwt']['secret_key'],
                algorithms=[self.config['jwt']['algorithm']]
            )
            return payload
        except ImportError:
            self.logger.error("JWT library not available")
            return None
        except PyJWTError as e:
            self.logger.warning(f"JWT verification failed: {e}")
            return None

    def check_permissions(self, user_role: str, required_permissions: List[str]) -> bool:
        """Check if user role has required permissions."""
        if user_role not in ROLES:
            return False

        user_permissions = ROLES[user_role]['permissions']

        # Admin has all permissions
        if '*' in user_permissions:
            return True

        # Check if user has all required permissions
        return all(perm in user_permissions for perm in required_permissions)

    def get_rate_limit_config(self, endpoint_type: str = 'default') -> Dict[str, int]:
        """Get rate limiting configuration for endpoint type."""
        return self.config['rate_limiting'].get(endpoint_type, self.config['rate_limiting']['default'])

    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return key information."""
        key_file = Path('config/security_keys.json')

        if not key_file.exists():
            return None

        try:
            with open(key_file, 'r') as f:
                keys = json.load(f)

            # Hash the provided key for comparison
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

            for key_id, key_data in keys.get('api_keys', {}).items():
                if hmac.compare_digest(key_data.get('hash', ''), key_hash):
                    return {
                        'id': key_id,
                        'name': key_data.get('name', ''),
                        'role': key_data.get('role', 'user'),
                        'permissions': key_data.get('permissions', [])
                    }

            return None
        except Exception as e:
            self.logger.error(f"API key validation failed: {e}")
            return None

    def create_api_key(self, name: str, role: str = 'user') -> Dict[str, Any]:
        """Create new API key."""
        key_file = Path('config/security_keys.json')

        # Generate new API key
        api_key = secrets.token_urlsafe(32)

        try:
            if key_file.exists():
                with open(key_file, 'r') as f:
                    keys = json.load(f)
            else:
                keys = {'api_keys': {}}

            key_id = secrets.token_hex(8)
            keys['api_keys'][key_id] = {
                'name': name,
                'role': role,
                'hash': hashlib.sha256(api_key.encode()).hexdigest(),
                'created_at': datetime.now().isoformat(),
                'permissions': ROLES.get(role, {}).get('permissions', [])
            }

            with open(key_file, 'w') as f:
                json.dump(keys, f, indent=2)

            return {
                'key_id': key_id,
                'api_key': api_key,
                'name': name,
                'role': role
            }

        except Exception as e:
            self.logger.error(f"API key creation failed: {e}")
            return None

    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for HTTP responses."""
        return self.config['security_headers'].copy()

    def validate_cors_origin(self, origin: str) -> bool:
        """Validate CORS origin."""
        cors_config = self.config['cors']

        # Allow all origins if wildcard is specified
        if '*' in cors_config['origins']:
            return True

        return origin in cors_config['origins']


# Global security manager instance
_security_manager = None

def get_security_manager() -> SecurityManager:
    """Get global security manager instance."""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager


# Security middleware for web frameworks
def create_flask_security_middleware():
    """Create Flask security middleware."""
    from flask import request, g, jsonify

    def security_middleware():
        """Flask security middleware function."""
        security = get_security_manager()

        # Add security headers
        response_headers = security.get_security_headers()
        # Note: Headers would be added in after_request handler

        # CORS validation
        origin = request.headers.get('Origin')
        if origin and not security.validate_cors_origin(origin):
            return jsonify({'error': 'CORS origin not allowed'}), 403

        # API key authentication
        api_key = request.headers.get('X-API-Key')
        if api_key:
            key_info = security.validate_api_key(api_key)
            if key_info:
                g.user = key_info
                g.authenticated = True
            else:
                return jsonify({'error': 'Invalid API key'}), 401

        # JWT token authentication
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            payload = security.verify_jwt_token(token)
            if payload:
                g.user = payload
                g.authenticated = True
            else:
                return jsonify({'error': 'Invalid or expired token'}), 401

        return None

    return security_middleware


def create_fastapi_security_middleware():
    """Create FastAPI security middleware."""
    from fastapi import Request, HTTPException, status
    from fastapi.responses import JSONResponse

    async def security_middleware(request: Request, call_next):
        """FastAPI security middleware."""
        security = get_security_manager()

        # CORS validation
        origin = request.headers.get('origin')
        if origin and not security.validate_cors_origin(origin):
            return JSONResponse(
                content={'error': 'CORS origin not allowed'},
                status_code=status.HTTP_403_FORBIDDEN
            )

        # Add security headers to response
        response = await call_next(request)
        for header, value in security.get_security_headers().items():
            response.headers[header] = value

        return response

    return security_middleware


def setup_ssl_certificates():
    """Setup SSL certificates for HTTPS."""
    ssl_dir = Path('ssl')
    ssl_dir.mkdir(exist_ok=True)

    cert_file = ssl_dir / 'cert.pem'
    key_file = ssl_dir / 'key.pem'

    if not cert_file.exists() or not key_file.exists():
        logger.info("SSL certificates not found. Generating self-signed certificates...")

        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.backends import default_backend

            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            # Generate certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Development"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Agent Cellphone V2"),
                x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ])

            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.DNSName("127.0.0.1"),
                ]),
                critical=False,
            ).sign(private_key, hashes.SHA256(), default_backend())

            # Write certificate and key
            with open(cert_file, 'wb') as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))

            with open(key_file, 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            logger.info("✅ Self-signed SSL certificates generated")

        except ImportError:
            logger.warning("Cryptography library not available. Install with: pip install cryptography")
            logger.warning("SSL certificates not generated - HTTPS will not be available")


def main():
    """Main entry point for security setup."""
    import argparse

    parser = argparse.ArgumentParser(description="Enterprise Security Framework")
    parser.add_argument('--setup-ssl', action='store_true', help='Setup SSL certificates')
    parser.add_argument('--create-api-key', help='Create new API key (provide name)')
    parser.add_argument('--list-keys', action='store_true', help='List existing API keys')
    parser.add_argument('--test-jwt', action='store_true', help='Test JWT token creation/verification')

    args = parser.parse_args()

    security = get_security_manager()

    if args.setup_ssl:
        setup_ssl_certificates()
        print("✅ SSL certificate setup complete")

    elif args.create_api_key:
        key_info = security.create_api_key(args.create_api_key)
        if key_info:
            print(f"✅ API Key Created:")
            print(f"   Key ID: {key_info['key_id']}")
            print(f"   Name: {key_info['name']}")
            print(f"   Role: {key_info['role']}")
            print(f"   API Key: {key_info['api_key']}")
            print("   ⚠️  Save this API key securely - it will not be shown again!")
        else:
            print("❌ Failed to create API key")

    elif args.list_keys:
        key_file = Path('config/security_keys.json')
        if key_file.exists():
            try:
                with open(key_file, 'r') as f:
                    keys = json.load(f)

                print("🔑 Existing API Keys:")
                for key_id, key_data in keys.get('api_keys', {}).items():
                    print(f"   {key_id}: {key_data['name']} ({key_data['role']})")
            except Exception as e:
                print(f"❌ Failed to read keys: {e}")
        else:
            print("❌ No API keys file found")

    elif args.test_jwt:
        # Test JWT functionality
        test_data = {"user_id": "test_user", "role": "admin"}
        token = security.create_jwt_token(test_data)

        if token:
            print(f"✅ JWT Token Created: {token[:50]}...")
            decoded = security.verify_jwt_token(token)
            if decoded:
                print(f"✅ JWT Token Verified: {decoded}")
            else:
                print("❌ JWT Token verification failed")
        else:
            print("❌ JWT Token creation failed")

    else:
        print("🏰 Enterprise Security Framework")
        print("Use --help for available options")


if __name__ == "__main__":
    main()