# reorg/reorg_dry_run.py
from __future__ import annotations

import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

try:
    import yaml
except Exception:
    yaml = None

TEXT_EXTS = {".py", ".md", ".yml", ".yaml", ".json", ".toml", ".ini", ".txt", ".sh", ".ps1"}

def load_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix in {".yml", ".yaml"}:
        if yaml is None:
            raise RuntimeError("pyyaml not installed: pip install pyyaml")
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    return json.loads(path.read_text(encoding="utf-8"))

def iter_text_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            # avoid giant dirs
            if any(part in {".git", ".venv", "node_modules"} for part in p.parts):
                continue
            files.append(p)
    return files

def scan_references(root: Path, from_path: str) -> List[Tuple[str, int, str]]:
    hits: List[Tuple[str, int, str]] = []
    pattern = re.compile(re.escape(from_path))
    for fp in iter_text_files(root):
        try:
            lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            if pattern.search(line):
                hits.append((str(fp), i, line.strip()[:240]))
    return hits

def main() -> int:
    repo = Path.cwd()
    manifest = load_manifest(repo / "reorg" / "migration_manifest.yml")

    moves = manifest.get("moves", [])
    protect = set(manifest.get("policy", {}).get("protect_paths", []))

    print("=== REORG DRY RUN ===")
    print(f"Repo: {repo}")
    print(f"Moves: {len(moves)}")
    print()

    missing = []
    conflicts = []
    for m in moves:
        src = repo / m["from"]
        dst = repo / m["to"]
        if m.get("optional") and not src.exists():
            continue
        if m["from"] in protect:
            conflicts.append((m["from"], "protected path"))
            continue
        if not src.exists():
            missing.append(m["from"])
            continue
        if dst.exists() and not m["to"].startswith("EXTERNAL:"):
            conflicts.append((m["from"], f"destination exists: {m['to']}"))

    if missing:
        print("Missing sources (non-optional):")
        for p in missing:
            print(f"  - {p}")
        print()

    if conflicts:
        print("Conflicts:")
        for src, why in conflicts:
            print(f"  - {src}: {why}")
        print()

    # Reference scan
    print("Reference scan (top 10 hits per move):")
    for m in moves:
        src = m["from"]
        if m.get("optional") and not (repo / src).exists():
            continue
        hits = scan_references(repo, src + "/") + scan_references(repo, src)
        if hits:
            print(f"\n- {src}  ->  {m['to']}  (hits={len(hits)})")
            for h in hits[:10]:
                print(f"    {h[0]}:{h[1]}  {h[2]}")
    print("\nDone.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())