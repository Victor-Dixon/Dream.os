#!/usr/bin/env python3
"""
JWT Manager - Phase 5 Advanced Security
========================================

Enterprise-grade JWT authentication and authorization system.
Provides secure token generation, validation, and user management.

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import jwt
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class JWTManager:
    """
    Enterprise JWT Authentication Manager

    Provides secure token generation, validation, and user session management.
    Supports RSA/ECDSA signing for production-grade security.
    """

    def __init__(self):
        """Initialize JWT Manager with security configuration."""
        self.secret_key = os.getenv("JWT_SECRET_KEY", "changeme-in-production")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))

        # Load RSA keys if using RS256
        if self.algorithm.startswith("RS"):
            self._load_rsa_keys()

        logger.info(f"✅ JWT Manager initialized with {self.algorithm} algorithm")

    def _load_rsa_keys(self):
        """Load RSA private and public keys for RS256 signing."""
        try:
            key_dir = Path("config/security/keys")
            key_dir.mkdir(parents=True, exist_ok=True)

            private_key_path = key_dir / "jwt_private.pem"
            public_key_path = key_dir / "jwt_public.pem"

            if private_key_path.exists():
                with open(private_key_path, "rb") as f:
                    self.private_key = f.read()
                with open(public_key_path, "rb") as f:
                    self.public_key = f.read()
            else:
                logger.warning("RSA keys not found, generating temporary keys...")
                self._generate_temp_rsa_keys()

        except Exception as e:
            logger.error(f"Failed to load RSA keys: {e}")
            raise

    def _generate_temp_rsa_keys(self):
        """Generate temporary RSA keys for development."""
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Serialize private key
        self.private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Serialize public key
        public_key = private_key.public_key()
        self.public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """
        Create JWT access token.

        Args:
            data: Token payload data

        Returns:
            JWT access token string
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})

        if self.algorithm.startswith("RS"):
            encoded_jwt = jwt.encode(to_encode, self.private_key, algorithm=self.algorithm)
        else:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create JWT refresh token.

        Args:
            data: Token payload data

        Returns:
            JWT refresh token string
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})

        if self.algorithm.startswith("RS"):
            encoded_jwt = jwt.encode(to_encode, self.private_key, algorithm=self.algorithm)
        else:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token string
            token_type: Expected token type ("access" or "refresh")

        Returns:
            Decoded token payload or None if invalid
        """
        try:
            if self.algorithm.startswith("RS"):
                payload = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            else:
                payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Verify token type
            if payload.get("type") != token_type:
                logger.warning(f"Token type mismatch: expected {token_type}, got {payload.get('type')}")
                return None

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.JWTError as e:
            logger.warning(f"Token validation failed: {e}")
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Refresh access token using valid refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New access token or None if refresh failed
        """
        payload = self.verify_token(refresh_token, "refresh")
        if not payload:
            return None

        # Create new access token with same user data
        user_data = {k: v for k, v in payload.items() if k not in ["exp", "type"]}
        return self.create_access_token(user_data)

    def get_token_expiry(self, token: str) -> Optional[datetime]:
        """
        Get token expiration time without full verification.

        Args:
            token: JWT token string

        Returns:
            Expiration datetime or None if invalid
        """
        try:
            # Decode without verification to check expiry
            header = jwt.get_unverified_header(token)
            payload = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})

            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                return datetime.fromtimestamp(exp_timestamp)
            return None

        except jwt.JWTError:
            return None

    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired.

        Args:
            token: JWT token string

        Returns:
            True if token is expired
        """
        expiry = self.get_token_expiry(token)
        if expiry:
            return datetime.utcnow() > expiry
        return True  # Consider invalid tokens as expired

# Global JWT manager instance
jwt_manager = JWTManager()