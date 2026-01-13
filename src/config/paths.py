# config/paths.py
from pathlib import Path
import os
import platform

def _websites_root() -> Path:
    if platform.system().lower().startswith("win"):
        return Path(os.environ.get("WEBSITES_ROOT", "D:/websites"))
    return Path(os.environ.get("WEBSITES_ROOT", "/mnt/websites"))

WEBSITES_ROOT = _websites_root()

# canonical subpaths (example)
FREERIDEINVESTOR_SITE = WEBSITES_ROOT / "freerideinvestor.com"
WEARESWARM_SITE = WEBSITES_ROOT / "weareswarm.site"