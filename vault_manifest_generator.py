import os, json, hashlib
from pathlib import Path

ROOT = Path(".")
out = []
for p in ROOT.rglob("*.md"):
    try:
        text = p.read_text(errors="ignore")
    except Exception:
        continue
    title = ""
    for line in text.splitlines():
        if line.strip().startswith("#"):
            title = line.strip().lstrip("#").strip()
            break
    out.append({
        "path": str(p),
        "bytes": p.stat().st_size,
        "title": title,
    })

out.sort(key=lambda x: x["bytes"], reverse=True)
Path("vault_manifest.json").write_text(json.dumps(out, indent=2))
print("md_files:", len(out))
print("top10_biggest:", [item["path"] for item in out[:10]])