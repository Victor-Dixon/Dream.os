"""
<!-- SSOT Domain: swarm_brain -->

Hostinger Site Adapter - WeAreSwarm
===================================

Provides a narrow, allowlisted interface to interact with the WeAreSwarm
WordPress instance. Operations are scoped to low-risk actions and must be
invoked via the control plane with policy checks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from src.control_plane.adapters.base import SiteAdapter


class WeAreSwarmHostingerAdapter:
    """
    Hostinger adapter for WeAreSwarm.

    Allowlisted ops (suggested):
    - cache_flush
    - permalinks_refresh
    - post_daily_plan (via WP REST + app password)
    """

    def __init__(
        self,
        base_url: str,
        wp_user: Optional[str] = None,
        wp_app_password: Optional[str] = None,
        health_path: str = "/",
        timeout: float = 10.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.wp_user = wp_user
        self.wp_app_password = wp_app_password
        self.health_path = health_path
        self.timeout = timeout

        self.allowed_ops = {
            "cache_flush": self._op_cache_flush,
            "permalinks_refresh": self._op_permalinks_refresh,
            "post_daily_plan": self._op_post_daily_plan,
        }

    # --------- Public API ---------

    def health(self) -> Dict[str, Any]:
        url = f"{self.base_url}{self.health_path}"
        try:
            resp = requests.get(url, timeout=self.timeout)
            return {
                "ok": resp.ok,
                "status_code": resp.status_code,
                "content_length": len(resp.text),
                "url": url,
            }
        except Exception as exc:  # pragma: no cover
            return {"ok": False, "error": str(exc), "url": url}

    def last_deploy(self) -> Dict[str, Any]:
        meta_path = Path("runtime/deploy_logs/weareswarm_last.json")
        if not meta_path.exists():
            return {"ok": False, "error": "no deploy metadata found"}
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            return {"ok": True, "data": data}
        except Exception as exc:  # pragma: no cover
            return {"ok": False, "error": str(exc)}

    def run_allowed(self, op: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        handler = self.allowed_ops.get(op)
        if not handler:
            return {"ok": False, "error": f"op '{op}' not allowed"}
        return handler(payload or {})

    # --------- Allowlisted ops ---------

    def _op_cache_flush(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": False, "error": "cache_flush not wired yet"}

    def _op_permalinks_refresh(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": False, "error": "permalinks_refresh not wired yet"}

    def _op_post_daily_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not (self.wp_user and self.wp_app_password):
            return {"ok": False, "error": "wp credentials not configured"}

        title = payload.get("title")
        content = payload.get("content")
        categories = payload.get("categories")
        if not title or not content:
            return {"ok": False, "error": "title and content required"}

        endpoint = f"{self.base_url}/wp-json/wp/v2/posts"
        body = {"title": title, "content": content, "status": "publish"}
        if categories:
            body["categories"] = categories

        try:
            resp = requests.post(
                endpoint,
                auth=(self.wp_user, self.wp_app_password),
                json=body,
                timeout=self.timeout,
            )
            if not resp.ok:
                return {"ok": False, "status_code": resp.status_code, "error": resp.text}
            data = resp.json()
            return {"ok": True, "id": data.get("id"), "link": data.get("link")}
        except Exception as exc:  # pragma: no cover
            return {"ok": False, "error": str(exc)}


def get_weareswarm_adapter() -> SiteAdapter:
    base_url = "https://weareswarm.online"
    wp_user = None
    wp_app_password = None
    return WeAreSwarmHostingerAdapter(base_url=base_url, wp_user=wp_user, wp_app_password=wp_app_password)


def get_weareswarm_site_adapter() -> SiteAdapter:
    base_url = "https://weareswarm.site"
    wp_user = None
    wp_app_password = None
    return WeAreSwarmHostingerAdapter(base_url=base_url, wp_user=wp_user, wp_app_password=wp_app_password)

