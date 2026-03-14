"""Ensure `tools` imports resolve to project package from unit/tools tests."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

sys.modules.pop("tools", None)
importlib.invalidate_caches()
importlib.import_module("tools")
