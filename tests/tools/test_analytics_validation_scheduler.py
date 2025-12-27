import sys
from pathlib import Path

import pytest

# Ensure repo root is importable in pytest collection environments.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.analytics_validation_scheduler import diff


@pytest.mark.unit
def test_diff_detects_status_change():
    old = {
        "freerideinvestor.com": {"status": "PENDING_IDS"},
        "tradingrobotplug.com": {"status": "PENDING_DEPLOYMENT"},
        "dadudekc.com": {"status": "PENDING_DEPLOYMENT"},
        "crosbyultimateevents.com": {"status": "PENDING_DEPLOYMENT"},
    }
    new = {
        "freerideinvestor.com": {"status": "READY"},
        "tradingrobotplug.com": {"status": "PENDING_DEPLOYMENT"},
        "dadudekc.com": {"status": "PENDING_DEPLOYMENT"},
        "crosbyultimateevents.com": {"status": "PENDING_DEPLOYMENT"},
    }

    changes = diff(old, new)
    assert ("freerideinvestor.com", "PENDING_IDS", "READY") in changes
