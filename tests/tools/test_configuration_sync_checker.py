import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.configuration_sync_checker import parse_wp_config, compare_configs


@pytest.mark.unit
def test_parse_wp_config_extracts_define_values(tmp_path: Path):
    config_content = """<?php
define('DB_NAME', 'testdb');
define('DB_USER', 'admin');
define('DB_PASSWORD', 'secret123');
define('WP_DEBUG', true);
define('GA4_MEASUREMENT_ID', 'G-ABC12345');
define('FACEBOOK_PIXEL_ID', '1234567890');
"""
    config_file = tmp_path / "wp-config.php"
    config_file.write_text(config_content, encoding="utf-8")

    result = parse_wp_config(config_file)

    assert result["DB_NAME"] == "testdb"
    assert result["DB_USER"] == "admin"
    assert result["DB_PASSWORD"] == "secret123"
    assert result["GA4_MEASUREMENT_ID"] == "G-ABC12345"
    assert result["FACEBOOK_PIXEL_ID"] == "1234567890"


@pytest.mark.unit
def test_compare_configs_detects_differences():
    a = {"DB_NAME": "prod_db", "GA4_MEASUREMENT_ID": "G-ABC12345"}
    b = {"DB_NAME": "prod_db", "GA4_MEASUREMENT_ID": "G-XYZ98765"}

    diffs = compare_configs(a, b)

    assert any(d[0] == "GA4_MEASUREMENT_ID" for d in diffs)
    assert not any(d[0] == "DB_NAME" for d in diffs)
