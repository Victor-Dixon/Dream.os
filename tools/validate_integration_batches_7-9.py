#!/usr/bin/env python3
"""
Validate Agent-1's Integration Batches 7-9 (45 files)
Validates SSOT tag format, domain registry compliance, tag placement, and compilation.
"""

import sys
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Integration batches 7-9 files (45 files total, 3 batches × 15 files each)
INTEGRATION_BATCH_7_FILES = [
    "src/services/chat_presence/message_interpreter.py",
    "src/services/chat_presence/quote_generator.py",
    "src/services/chat_presence/status_reader.py",
    "src/services/chat_presence/twitch_bridge.py",
    "src/services/chat_presence/twitch_eventsub_handler.py",
    "src/services/chat_presence/twitch_eventsub_server.py",
    "src/services/swarm_website/__init__.py",
    "src/services/swarm_website/auto_updater.py",
    "src/services/swarm_website/website_updater.py",
    "src/services/onboarding/shared/__init__.py",
    "src/services/onboarding/shared/operations.py",
    "src/services/onboarding/shared/coordinates.py",
    "src/services/onboarding/hard/__init__.py",
    "src/services/onboarding/hard/service.py",
    "src/services/onboarding/hard/steps.py"
]

INTEGRATION_BATCH_8_FILES = [
    "src/services/onboarding/hard/default_message.py",
    "src/services/onboarding/soft/__init__.py",
    "src/services/onboarding/soft/messaging_fallback.py",
    "src/services/onboarding/soft/steps.py",
    "src/services/onboarding/soft/service.py",
    "src/services/onboarding/soft/default_message.py",
    "src/services/onboarding/soft/cleanup_defaults.py",
    "src/services/onboarding/soft/canonical_closure_prompt.py",
    "src/trading_robot/services/__init__.py",
    "src/trading_robot/services/trading_bi_analytics.py",
    "src/trading_robot/services/analytics/__init__.py",
    "src/trading_robot/services/analytics/market_trend_engine.py",
    "src/trading_robot/services/analytics/performance_metrics_engine.py",
    "src/trading_robot/services/analytics/risk_analysis_engine.py",
    "src/trading_robot/services/analytics/trading_bi_models.py"
]

INTEGRATION_BATCH_9_FILES = [
    "src/web/static/js/services-orchestrator.js",
    "src/web/static/js/services/agent-coordination-module.js",
    "src/web/static/js/services/business-insights-module.js",
    "src/web/static/js/services/business-validation-module.js",
    "src/web/static/js/services/component-validation-module.js",
    "src/web/static/js/services/coordination-reporting-module.js",
    "src/web/static/js/services/dashboard-data-service.js",
    "src/web/static/js/services/dashboard-init-service.js",
    "src/web/static/js/services/deployment-analysis-methods.js",
    "src/web/static/js/services/deployment-coordination-service.js",
    "src/web/static/js/services/deployment-metrics-service.js",
    "src/web/static/js/services/deployment-phase-service.js",
    "src/web/static/js/services/deployment-validation-service.js",
    "src/web/static/js/services/metrics-aggregation-module.js",
    "src/web/static/js/services/performance-analysis-module.js"
]

ALL_FILES = INTEGRATION_BATCH_7_FILES + INTEGRATION_BATCH_8_FILES + INTEGRATION_BATCH_9_FILES

# SSOT Domain Registry (from docs/SSOT_DOMAIN_MAPPING.md)
VALID_DOMAINS = [
    "integration", "core", "messaging", "analytics", "trading_robot",
    "architecture", "infrastructure", "deployment", "coordination",
    "gaming", "vision", "logging", "config", "monitoring", "performance",
    "error_handling", "discord", "swarm_brain", "git", "communication",
    "safety", "domain", "trading_robot", "performance", "error_handling",
    "swarm_brain", "analytics", "ai_training", "qa", "data"
]

def validate_ssot_tag_format(content: str) -> Tuple[bool, str]:
    """Validate SSOT tag format."""
    pattern = r'<!--\s*SSOT\s+Domain:\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*-->'
    match = re.search(pattern, content, re.IGNORECASE)
    if not match:
        return False, "SSOT tag not found or invalid format"
    domain = match.group(1)
    return True, domain

def validate_domain_registry(domain: str) -> bool:
    """Validate domain is in SSOT registry."""
    return domain.lower() in [d.lower() for d in VALID_DOMAINS]

def validate_tag_placement(content: str) -> Tuple[bool, str]:
    """Validate tag is in docstring or header (first 50 lines)."""
    lines = content.split('\n')[:50]
    header_content = '\n'.join(lines)
    pattern = r'<!--\s*SSOT\s+Domain:\s*[a-zA-Z_][a-zA-Z0-9_]*\s*-->'
    if re.search(pattern, header_content, re.IGNORECASE):
        return True, "Tag found in header/docstring"
    return False, "Tag not found in first 50 lines"

def validate_compilation(file_path: Path) -> Tuple[bool, str]:
    """Validate Python file compiles."""
    if not file_path.suffix == '.py':
        return True, "Not a Python file (skipping compilation)"
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Compilation successful"
        else:
            error = result.stderr[:200] if result.stderr else "Unknown compilation error"
            return False, f"Compilation failed: {error}"
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, f"Compilation error: {str(e)[:200]}"

def validate_file(file_path: Path) -> Dict:
    """Validate a single file."""
    repo_root = Path(__file__).parent.parent
    full_path = repo_root / file_path
    
    if not full_path.exists():
        return {
            "file": str(file_path),
            "valid": False,
            "errors": [f"File not found: {full_path}"]
        }
    
    try:
        content = full_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {
            "file": str(file_path),
            "valid": False,
            "errors": [f"Could not read file: {e}"]
        }
    
    errors = []
    
    # Validate tag format
    tag_valid, tag_result = validate_ssot_tag_format(content)
    if not tag_valid:
        errors.append(f"Tag Format: {tag_result}")
    else:
        domain = tag_result
        # Validate domain registry
        if not validate_domain_registry(domain):
            errors.append(f"Domain Registry: Domain '{domain}' not in SSOT registry")
        # Validate domain matches expected
        if domain.lower() != "integration":
            errors.append(f"Domain Mismatch: Expected 'integration', found '{domain}'")
    
    # Validate tag placement
    placement_valid, placement_msg = validate_tag_placement(content)
    if not placement_valid:
        errors.append(f"Tag Placement: {placement_msg}")
    
    # Validate compilation (Python files only)
    if full_path.suffix == '.py':
        compile_valid, compile_msg = validate_compilation(full_path)
        if not compile_valid:
            errors.append(f"Compilation: {compile_msg}")
    
    return {
        "file": str(file_path),
        "valid": len(errors) == 0,
        "errors": errors
    }

def main():
    """Main validation function."""
    print("🔍 Validating Integration Batches 7-9 (45 files)...\n")
    
    results = []
    valid_count = 0
    invalid_count = 0
    
    for file_path_str in ALL_FILES:
        file_path = Path(file_path_str.replace('\\', '/'))
        result = validate_file(file_path)
        results.append(result)
        
        if result["valid"]:
            valid_count += 1
            print(f"✅ {file_path}")
        else:
            invalid_count += 1
            print(f"❌ {file_path}")
            for error in result["errors"]:
                print(f"   - {error}")
    
    print(f"\n📊 Summary:")
    print(f"   Total files: {len(ALL_FILES)}")
    print(f"   Valid: {valid_count}")
    print(f"   Invalid: {invalid_count}")
    print(f"   Pass rate: {(valid_count/len(ALL_FILES)*100):.1f}%")
    
    if invalid_count > 0:
        print(f"\n❌ Validation failed: {invalid_count} files have errors")
        sys.exit(1)
    else:
        print(f"\n✅ All files validated successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()

