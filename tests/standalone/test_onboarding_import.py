#!/usr/bin/env python3
"""Test script to reproduce onboarding template loader import issue."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# This should trigger the import in steps.py
try:
    from services.onboarding.hard.steps import HardOnboardingSteps
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()

