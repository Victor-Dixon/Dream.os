#!/usr/bin/env python3
"""
Twitch OAuth Integration
========================

Proper OAuth 2.0 flow for Twitch authentication.
Creates OAuth application and handles token generation.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Optional

logger = logging.getLogger(__name__)


class TwitchOAuthHandler:
    """
    Handles Twitch OAuth 2.0 authentication flow.

    Flow:
    1. Redirect user to Twitch authorization
    2. User authorizes application
    3. Twitch redirects back with code
    4. Exchange code for access token
    5. Return token to application
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:3000/callback",
        scopes: list[str] | None = None,
    ):
        """
        Initialize Twitch OAuth handler.

        Args:
            client_id: Twitch application client ID
            client_secret: Twitch application client secret
            redirect_uri: OAuth redirect URI (must match Twitch app settings)
            scopes: OAuth scopes to request
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes or ["chat:read", "chat:edit", "channel:moderate"]
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    def get_authorization_url(self) -> str:
        """
        Generate Twitch authorization URL.

        Returns:
            Authorization URL for user to visit
        """
        scope_string = "+".join(self.scopes)
        url = (
            f"https://id.twitch.tv/oauth2/authorize?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"response_type=code&"
            f"scope={scope_string}"
        )
        return url

    def exchange_code_for_token(self, code: str) -> dict:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from callback

        Returns:
            Token response dictionary
        """
        import requests

        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data.get("access_token")
        self.refresh_token = token_data.get("refresh_token")

        return token_data

    def get_oauth_token(self) -> Optional[str]:
        """
        Get current access token.

        Returns:
            Access token or None
        """
        return self.access_token

    def refresh_access_token(self) -> Optional[str]:
        """
        Refresh access token using refresh token.

        Returns:
            New access token or None
        """
        if not self.refresh_token:
            logger.error("No refresh token available")
            return None

        import requests

        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            return self.access_token
        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            return None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""

    def do_GET(self):
        """Handle GET request (OAuth callback)."""
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if "code" in query:
            code = query["code"][0]
            self.server.oauth_code = code
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authorization successful!</h1>"
                b"<p>You can close this window and return to the application.</p></body></html>"
            )
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authorization failed</h1>"
                b"<p>No authorization code received.</p></body></html>"
            )

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def get_oauth_token_interactive(
    client_id: str,
    client_secret: str,
    redirect_uri: str = "http://localhost:3000/callback",
    scopes: list[str] | None = None,
) -> Optional[str]:
    """
    Interactive OAuth flow to get access token.

    Args:
        client_id: Twitch application client ID
        client_secret: Twitch application client secret
        redirect_uri: OAuth redirect URI
        scopes: OAuth scopes

    Returns:
        Access token or None
    """
    oauth = TwitchOAuthHandler(client_id, client_secret, redirect_uri, scopes)

    # Start local server for callback
    from urllib.parse import urlparse

    parsed = urlparse(redirect_uri)
    port = parsed.port or 3000

    server = HTTPServer(("localhost", port), OAuthCallbackHandler)
    server.oauth_code = None

    # Open browser to authorization URL
    auth_url = oauth.get_authorization_url()
    print(f"\n🔐 Opening browser for Twitch authorization...")
    print(f"URL: {auth_url}\n")
    webbrowser.open(auth_url)

    # Wait for callback
    print(f"⏳ Waiting for authorization...")
    print(f"Listening on http://localhost:{port}/callback")
    print(f"After authorizing, return here...\n")

    server.timeout = 300  # 5 minute timeout
    server.handle_request()

    if server.oauth_code:
        print(f"✅ Authorization code received!")
        print(f"🔄 Exchanging for access token...")

        token_data = oauth.exchange_code_for_token(server.oauth_code)
        access_token = oauth.get_oauth_token()

        if access_token:
            print(f"✅ Access token obtained!")
            print(f"Token: {access_token[:20]}...\n")
            return access_token

    print(f"❌ Failed to obtain access token")
    return None


__all__ = [
    "TwitchOAuthHandler",
    "get_oauth_token_interactive",
    "OAuthCallbackHandler",
]



