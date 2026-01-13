#!/usr/bin/env python3
"""Deployment Integration Verification (legacy CLI)

This script is kept for backward compatibility with existing automation and
unit tests. The canonical MCP implementation lives in `mcp_servers/`.

Unit test dependency:
  - `DeploymentVerifier._build_api_url()` must preserve `rest_api_base` even if
    endpoint is provided with a leading slash.

<!-- SSOT Domain: integration -->
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests

TIMEOUT = 15

DEFAULT_SITES: dict[str, dict[str, Any]] = {
    "tradingrobotplug.com": {
        "url": "https://tradingrobotplug.com",
        "wordpress_api": "/wp-json/",
        "rest_api_base": "/wp-json/tradingrobotplug/v1",
        "endpoints": ["/stock-data", "/stock-data/TSLA", "/strategies"],
    },
    "dadudekc.com": {"url": "https://dadudekc.com", "wordpress_api": "/wp-json/"},
    "crosbyultimateevents.com": {"url": "https://crosbyultimateevents.com", "wordpress_api": "/wp-json/"},
    "freerideinvestor.com": {"url": "https://freerideinvestor.com", "wordpress_api": "/wp-json/"},
}


@dataclass
class DeploymentVerifier:
    results: List[Dict[str, Any]]
    timestamp: str

    def __init__(self) -> None:
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def _build_api_url(base_url: str, api_base: str, endpoint: str) -> str:
        """Build a REST URL safely.

        `urljoin` treats a leading '/' as an absolute path (dropping prior path),
        so we normalize segments before joining.
        """

        root = base_url.rstrip("/") + "/"
        api = (api_base or "").strip("/")
        ep = (endpoint or "").strip("/")

        if api and ep:
            return urljoin(root, f"{api}/{ep}")
        if api:
            return urljoin(root, api)
        return urljoin(root, ep)

    def _get(self, url: str) -> requests.Response:
        return requests.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": "SwarmVerifier/1.0"},
        )

    def check_accessibility(self, url: str) -> Dict[str, Any]:
        try:
            r = self._get(url)
            return {
                "status": "PASS" if r.status_code == 200 else "FAIL",
                "status_code": r.status_code,
                "size": len(r.content or b""),
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def check_wp_api(self, base_url: str, wp_api_path: str = "/wp-json/") -> Dict[str, Any]:
        api_url = self._build_api_url(base_url, "", wp_api_path)
        try:
            r = self._get(api_url)
            ok = r.status_code == 200
            return {
                "status": "PASS" if ok else "FAIL",
                "status_code": r.status_code,
                "wp_api_available": ok,
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e), "wp_api_available": False}

    def check_rest_endpoint(self, url: str) -> Dict[str, Any]:
        try:
            r = self._get(url)
            return {
                "status": "PASS" if r.status_code == 200 else "FAIL",
                "status_code": r.status_code,
                "url": url,
                "response_size": len(r.content or b""),
            }
        except Exception as e:
            return {"status": "ERROR", "error": str(e), "url": url}

    def verify_site(self, site_name: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
        base_url = cfg["url"]
        result: Dict[str, Any] = {
            "site": site_name,
            "url": base_url,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
        }

        result["checks"]["accessibility"] = self.check_accessibility(base_url)
        result["checks"]["wordpress_api"] = self.check_wp_api(base_url, cfg.get("wordpress_api", "/wp-json/"))

        if cfg.get("endpoints"):
            endpoint_results = []
            for endpoint in cfg["endpoints"]:
                full_url = self._build_api_url(base_url, cfg.get("rest_api_base", ""), endpoint)
                endpoint_results.append({"endpoint": endpoint, **self.check_rest_endpoint(full_url)})
            result["checks"]["custom_endpoints"] = endpoint_results

        overall = "PASS"
        for check in result["checks"].values():
            if isinstance(check, list):
                if any(c.get("status") != "PASS" for c in check):
                    overall = "FAIL"
            else:
                if check.get("status") != "PASS":
                    overall = "FAIL"
        result["overall_status"] = overall
        return result

    def run(self, sites: Optional[dict[str, dict[str, Any]]] = None) -> Dict[str, Any]:
        sites = sites or DEFAULT_SITES
        for name, cfg in sites.items():
            self.results.append(self.verify_site(name, cfg))

        passed = sum(1 for r in self.results if r.get("overall_status") == "PASS")
        failed = sum(1 for r in self.results if r.get("overall_status") == "FAIL")
        return {
            "timestamp": datetime.now().isoformat(),
            "total_sites": len(self.results),
            "passed": passed,
            "failed": failed,
            "results": self.results,
        }


def _write_outputs(payload: Dict[str, Any]) -> tuple[Path, Path]:
    out_dir = Path("agent_workspaces") / "Agent-1" / "deployment_verification_tests"
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_dir / f"deployment_verification_{ts}.json"
    md_path = out_dir / f"deployment_verification_summary_{ts}.md"

    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Deployment Integration Verification Summary",
        "",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"- **Total Websites**: {payload.get('total_sites')}",
        f"- **✅ Passed**: {payload.get('passed')}",
        f"- **⚠️ Failed**: {payload.get('failed')}",
        "",
    ]

    for r in payload.get("results", []):
        lines.append(f"## {'✅' if r.get('overall_status') == 'PASS' else '⚠️'} {r.get('site')}")
        lines.append(f"**URL**: {r.get('url')}")
        lines.append(f"**Overall Status**: {r.get('overall_status')}")
        lines.append("")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    verifier = DeploymentVerifier()
    payload = verifier.run()
    _write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
