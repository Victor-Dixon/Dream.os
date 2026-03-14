"""Interpreter bootstrap to prioritize project-root package imports."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_tools = ROOT / "tools" / "__init__.py"
if _tools.exists() and "tools" not in sys.modules:
    spec = importlib.util.spec_from_file_location("tools", _tools)
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)
        mod.__path__ = [str(ROOT / "tools")]
        sys.modules["tools"] = mod
        spec.loader.exec_module(mod)
