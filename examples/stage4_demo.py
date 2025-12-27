#!/usr/bin/env python3
"""
Stage 4 Unlocks Demo
====================

Demonstrates the three new Stage 4 capabilities:
1. Impact Scoring + Task Selection (ROI)
2. Automated Verification Harness
3. Autonomous Recovery

Author: Agent-Generic
"""

import sys
import logging
from unittest.mock import MagicMock

# Mock GUI dependencies to run in headless environment
sys.modules['pyautogui'] = MagicMock()
sys.modules['pyperclip'] = MagicMock()
sys.modules['mouseinfo'] = MagicMock()
sys.modules['Xlib'] = MagicMock()
sys.modules['Xlib.display'] = MagicMock()
sys.modules['Xlib.protocol'] = MagicMock()

# Add workspace root to path
sys.path.append("/workspace")

from src.services.contract_system.models import Contract
from src.services.verification_service import VerificationService
from src.services.recovery_service import RecoveryService

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Stage4Demo")

def demo_roi_selection():
    logger.info("--- Demo 1: Impact Scoring + Task Selection ---")
    
    tasks_data = [
        {
            "contract_id": "TASK-001",
            "title": "Low Value, High Effort",
            "user_value": 10.0,
            "effort": 10.0,
            "risk": 1.0,
            "dependency_count": 0,
            "status": "pending"
        },
        {
            "contract_id": "TASK-002",
            "title": "High Value, Low Effort",
            "user_value": 100.0,
            "effort": 2.0,
            "risk": 1.0,
            "dependency_count": 0,
            "status": "pending"
        },
        {
            "contract_id": "TASK-003",
            "title": "High Value, High Risk",
            "user_value": 100.0,
            "effort": 2.0,
            "risk": 10.0, # High risk penalty
            "dependency_count": 0,
            "status": "pending"
        }
    ]
    
    contracts = []
    for data in tasks_data:
        c = Contract.from_dict(data)
        roi = c.calculate_roi()
        contracts.append(c)
        logger.info(f"Task '{c.title}' ROI: {roi:.2f} (Value={c.user_value}, Effort={c.effort}, Risk={c.risk})")
    
    # Sort
    contracts.sort(key=lambda x: x.roi_score, reverse=True)
    winner = contracts[0]
    logger.info(f"🏆 Winner: {winner.title} with ROI {winner.roi_score:.2f}")

def demo_verification():
    logger.info("\n--- Demo 2: Automated Verification Harness ---")
    verifier = VerificationService()
    
    # 1. Verify URL (Example)
    url = "https://example.com"
    logger.info(f"Verifying {url}...")
    result = verifier.verify_url_status(url)
    logger.info(f"Result: {result}")
    
    # 2. Verify Text
    text = "Example Domain"
    logger.info(f"Checking for '{text}' in {url}...")
    result = verifier.verify_text_in_page(url, text)
    logger.info(f"Result: {result}")
    
    # 3. Verify File
    path = "README.md" # Assuming this exists or similar
    logger.info(f"Verifying file {path} exists...")
    result = verifier.verify_file_exists(path)
    logger.info(f"Result: {result}")

def demo_recovery():
    logger.info("\n--- Demo 3: Autonomous Recovery ---")
    recovery = RecoveryService()
    
    # Create a dummy broken file
    broken_file = "broken_script.py"
    with open(broken_file, "w") as f:
        f.write("print('Hello World'") # Syntax error
    
    context = {
        "error": "SyntaxError: unexpected EOF while parsing",
        "file_path": broken_file,
        # In a real scenario, we'd have a test that fails
    }
    
    logger.info(f"Simulating failure in {broken_file}...")
    
    # We mock the validation to pass after 'patching' for this demo
    # In reality, the patch would fix it and validation would pass
    
    # Mocking propose_patch output for the demo script since we don't have a real AI
    # This just proves the flow works
    
    result = recovery.handle_failure(context)
    logger.info(f"Recovery Result: {result}")
    
    # Clean up
    if result["success"]:
        with open(broken_file, "r") as f:
            logger.info(f"Patched content: {f.read().strip()}")
    
    import os
    if os.path.exists(broken_file):
        os.remove(broken_file)
    if os.path.exists(broken_file + ".bak"):
        os.remove(broken_file + ".bak")

if __name__ == "__main__":
    demo_roi_selection()
    demo_verification()
    demo_recovery()
