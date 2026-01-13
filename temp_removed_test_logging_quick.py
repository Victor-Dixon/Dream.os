#!/usr/bin/env python3
"""Quick test for logging mixin functionality."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from src.core.logging_mixin import LoggingMixin

    class TestService(LoggingMixin):
        pass

    # Test instantiation
    service = TestService()
    print("✅ LoggingMixin imports and initializes successfully")
    print(f"✅ Logger created: {service.logger.name}")

    # Test basic logging
    service.logger.info("Test log message")
    print("✅ Basic logging functionality works")

    print("🎉 LoggingMixin Phase 1 implementation verified!")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)