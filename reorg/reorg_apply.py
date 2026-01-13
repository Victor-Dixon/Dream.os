# reorg/reorg_apply.py
from __future__ import annotations

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List

try:
    import yaml
except Exception:
    yaml = None

def load_manifest(path: Path) -> Dict[str, Any]:
    if path.suffix in {".yml", ".yaml"}:
        if yaml is None:
            raise RuntimeError("pyyaml not installed: pip install pyyaml")
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    return json.loads(path.read_text(encoding="utf-8"))

def run(cmd: List[str]) -> None:
    subprocess.check_call(cmd)

def is_git_repo(repo: Path) -> bool:
    return (repo / ".git").exists()

def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Check if source is an empty directory
    if src.is_dir() and not any(src.iterdir()):
        # Use regular move for empty directories
        fs_mv(src, dst)
    else:
        run(["git", "mv", str(src), str(dst)])

def fs_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))

def make_symlink(old: Path, new: Path) -> None:
    # Only make link if old is absent and new exists
    if old.exists():
        return
    if not new.exists():
        return
    old.parent.mkdir(parents=True, exist_ok=True)
    old.symlink_to(new, target_is_directory=new.is_dir())

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', type=int, help='Phase number to execute')
    args = parser.parse_args()

    repo = Path.cwd()
    manifest = load_manifest(repo / "reorg" / "migration_manifest.yml")
    policy = manifest.get("policy", {})
    protect = set(policy.get("protect_paths", []))
    create_links = bool(policy.get("create_symlink_bridges", True))

    moves = manifest.get("moves", [])
    if not moves:
        print("No moves in manifest.")
        return 0

    # Check for phase filter
    phase_filter = args.phase or os.environ.get("REORG_PHASE")
    if phase_filter:
        try:
            phase_num = int(phase_filter)
            moves = [m for m in moves if m.get("phase", 1) == phase_num]
            print(f"Filtered to phase {phase_num}: {len(moves)} moves")
        except ValueError:
            print(f"Invalid phase: {phase_filter}")
            return 1

    # Backup tag (cheap safety)
    if is_git_repo(repo):
        try:
            run(["git", "rev-parse", "--verify", "HEAD"])
            run(["git", "tag", "-f", "pre-reorg-snapshot"])
            print("Tagged current HEAD as pre-reorg-snapshot")
        except Exception as e:
            print(f"Warning: could not tag snapshot: {e}")

    moved = 0
    for m in moves:
        src_rel = m["from"]
        dst_rel = m["to"]
        optional = bool(m.get("optional", False))

        if src_rel in protect:
            print(f"SKIP protected: {src_rel}")
            continue

        src = repo / src_rel

        # Handle EXTERNAL moves (skip actual moving)
        if dst_rel.startswith("EXTERNAL:"):
            if src.exists():
                print(f"SKIP externalized path: {src_rel} -> {dst_rel}")
                print("  Note: This path should be referenced via config.paths.WEBSITES_ROOT")
            continue

        dst = repo / dst_rel

        if optional and not src.exists():
            print(f"SKIP optional missing: {src_rel}")
            continue

        if not src.exists():
            raise FileNotFoundError(f"Missing required path: {src_rel}")

        if dst.exists():
            raise FileExistsError(f"Destination exists: {dst_rel}")

        print(f"MOVE {src_rel}  ->  {dst_rel}")
        try:
            if is_git_repo(repo):
                git_mv(src, dst)
            else:
                fs_mv(src, dst)

            if create_links:
                try:
                    make_symlink(repo / src_rel, repo / dst_rel)
                    print(f"  LINK {src_rel} -> {dst_rel}")
                except Exception as e:
                    print(f"  Warning: could not symlink {src_rel}: {e}")

            moved += 1
        except Exception as e:
            print(f"  ERROR: Failed to move {src_rel}: {e}")
            print("  Continuing with other moves...")

    print(f"\nDone. Moves applied: {moved}")
    print("Next: run validation ritual.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())