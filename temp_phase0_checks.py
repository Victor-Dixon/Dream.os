import re
import sys
from typing import List, Tuple

import requests

URLS = {
    "weareswarm.home": "https://weareswarm.online/",
    "weareswarm.how": "https://weareswarm.online/how-the-swarm-works/",
    "weareswarm.manifesto": "https://weareswarm.online/swarm-manifesto/",
    "dadudekc.home": "https://dadudekc.com/",
    "freerideinvestor.home": "https://freerideinvestor.com/",
    "crosby.home": "https://crosbyultimateevents.com/",
}

TIMEOUT = 15
UA = {"User-Agent": "Mozilla/5.0 (SwarmVerifier/1.0)"}


def title_from_html(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def markers_for(key: str) -> List[Tuple[str, str]]:
    if key.startswith("weareswarm"):
        return [
            ("build in public", "build in public"),
            ("how the swarm works", "how the swarm works"),
            ("manifesto", "manifesto"),
            ("agents", "meet the agents"),
        ]
    if key == "dadudekc.home":
        return [
            ("what i do", "what i do"),
            ("live experiments", "live experiments"),
            ("build", "build"),
        ]
    return []


def main() -> int:
    print("Phase0 page-level checks")
    print("=========================")

    for key, url in URLS.items():
        try:
            r = requests.get(url, timeout=TIMEOUT, allow_redirects=True, headers=UA)
            html = r.text or ""
            print(f"\n[{key}] {url} -> {r.status_code} len={len(html)}")

            if r.status_code != 200:
                snippet = re.sub(r"\s+", " ", html)[:400]
                print(f"  snippet: {snippet}")
                continue

            t = title_from_html(html)
            if t:
                print(f"  title: {t[:120]}")

            low = html.lower()
            markers = markers_for(key)
            for name, needle in markers:
                ok = needle in low
                print(f"  marker:{name}: {'PASS' if ok else 'FAIL'}")

        except Exception as e:
            print(f"\n[{key}] {url} -> ERROR {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
