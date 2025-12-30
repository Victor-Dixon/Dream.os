"""
Phase 3 Component Validation Utility
====================================

Quick validation utility for Phase 3 TradingRobotPlug components.
Validates file existence, basic structure, and integration points.

Usage:
    python tools/validate_phase3_components.py

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-30
"""

import sys
from pathlib import Path

# Component files to validate
COMPONENTS = {
    "FastAPI REST API": "backend/api/fastapi_app.py",
    "WebSocketEventServer": "backend/core/websocket_event_server.py",
    "MarketDataStreamer": "backend/core/market_data_streamer.py",
    "StrategyAnalytics": "backend/core/strategy_analytics.py",
    "BacktestingEngine": "backend/core/backtesting_engine.py",
    "EventPublisherV2": "backend/core/event_publisher_v2.py",
}

# Integration points to check
INTEGRATION_POINTS = {
    "FastAPI → WebSocketEventServer": ("backend/api/fastapi_app.py", "WebSocketEventServer"),
    "FastAPI → EventPublisherV2": ("backend/api/fastapi_app.py", "EventPublisherV2"),
    "StrategyAnalytics → EventPublisherV2": ("backend/core/strategy_analytics.py", "EventPublisherV2"),
    "BacktestingEngine → MarketDataStreamer": ("backend/core/backtesting_engine.py", "MarketDataStreamer"),
    "BacktestingEngine → EventPublisherV2": ("backend/core/backtesting_engine.py", "EventPublisherV2"),
}


def validate_component(component_name: str, file_path: str, repo_root: Path) -> tuple[bool, str]:
    """Validate a component file exists and has basic structure."""
    full_path = repo_root / file_path
    
    if not full_path.exists():
        return False, f"File not found: {file_path}"
    
    try:
        content = full_path.read_text(encoding="utf-8")
        
        # Basic structure checks
        if len(content.strip()) == 0:
            return False, "File is empty"
        
        # Check for class definition (basic structure)
        if "class " not in content and "def " not in content:
            return False, "No class or function definitions found"
        
        return True, "Valid"
    
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_integration(integration_name: str, file_path: str, import_name: str, repo_root: Path) -> tuple[bool, str]:
    """Validate integration point (import exists)."""
    full_path = repo_root / file_path
    
    if not full_path.exists():
        return False, f"File not found: {file_path}"
    
    try:
        content = full_path.read_text(encoding="utf-8")
        
        # Check for import
        if import_name in content or import_name.lower() in content.lower():
            return True, "Integration found"
        else:
            return False, f"Import '{import_name}' not found"
    
    except Exception as e:
        return False, f"Error reading file: {e}"


def main():
    """Main validation function."""
    # Find repository root (TradingRobotPlugWeb)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    
    # Try to find TradingRobotPlugWeb repository
    if (repo_root / "websites" / "TradingRobotPlugWeb").exists():
        repo_root = repo_root / "websites" / "TradingRobotPlugWeb"
    elif (Path("D:/websites/TradingRobotPlugWeb")).exists():
        repo_root = Path("D:/websites/TradingRobotPlugWeb")
    else:
        print("❌ ERROR: TradingRobotPlugWeb repository not found")
        sys.exit(1)
    
    print(f"📁 Repository root: {repo_root}")
    print(f"\n🔍 Validating Phase 3 Components...\n")
    
    # Validate components
    component_results = []
    for component_name, file_path in COMPONENTS.items():
        is_valid, message = validate_component(component_name, file_path, repo_root)
        status = "✅" if is_valid else "❌"
        component_results.append((component_name, is_valid))
        print(f"{status} {component_name}: {message}")
    
    # Validate integration points
    print(f"\n🔗 Validating Integration Points...\n")
    integration_results = []
    for integration_name, (file_path, import_name) in INTEGRATION_POINTS.items():
        is_valid, message = validate_integration(integration_name, file_path, import_name, repo_root)
        status = "✅" if is_valid else "❌"
        integration_results.append((integration_name, is_valid))
        print(f"{status} {integration_name}: {message}")
    
    # Summary
    print(f"\n📊 Summary:\n")
    component_pass = sum(1 for _, is_valid in component_results if is_valid)
    integration_pass = sum(1 for _, is_valid in integration_results if is_valid)
    
    print(f"Components: {component_pass}/{len(component_results)} valid")
    print(f"Integrations: {integration_pass}/{len(integration_results)} valid")
    
    if component_pass == len(component_results) and integration_pass == len(integration_results):
        print(f"\n✅ All Phase 3 components validated successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Validation failed - some components or integrations missing")
        sys.exit(1)


if __name__ == "__main__":
    main()

