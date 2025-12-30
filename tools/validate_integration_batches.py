#!/usr/bin/env python3
"""
Validate Agent-1's Integration Batches 1-6 (90 files)
Validates SSOT tag format, domain registry compliance, tag placement, and compilation.
"""

import sys
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Integration batches 1-6 files (90 files total, 6 batches × 15 files each)
INTEGRATION_BATCH_FILES = [
    # Batch 1 (15 files)
    "src/domain/services/__init__.py",
    "src/domain/services/assignment_service.py",
    "src/services/__init__.py",
    "src/services/agent_management.py",
    "src/services/agent_vector_utils.py",
    "src/services/ai_service.py",
    "src/services/architectural_models.py",
    "src/services/architectural_principles.py",
    "src/services/architectural_principles_data.py",
    "src/services/chatgpt/__init__.py",
    "src/services/chatgpt/cli.py",
    "src/services/chatgpt/extractor.py",
    "src/services/chatgpt/extractor_message_parser.py",
    "src/services/chatgpt/extractor_storage.py",
    "src/services/chatgpt/navigator.py",
    # Batch 2 (15 files)
    "src/services/chatgpt/navigator_messaging.py",
    "src/services/chatgpt/session.py",
    "src/services/chatgpt/session_persistence.py",
    "src/services/config.py",
    "src/services/constants.py",
    "src/services/contract_service.py",
    "src/services/contract_system/__init__.py",
    "src/services/contract_system/contract_notifications_integration.py",
    "src/services/contract_system/cycle_planner_integration.py",
    "src/services/contract_system/manager.py",
    "src/services/contract_system/models.py",
    "src/services/contract_system/storage.py",
    "src/services/coordination/__init__.py",
    "src/services/coordinator.py",
    "src/services/handlers/__init__.py",
    # Batch 3 (15 files)
    "src/services/handlers/batch_message_handler.py",
    "src/services/handlers/command_handler.py",
    "src/services/hard_onboarding_service.py",
    "src/services/learning_recommender.py",
    "src/services/message_identity_clarification.py",
    "src/services/onboarding_template_loader.py",
    "src/services/overnight_command_handler.py",
    "src/services/performance_analyzer.py",
    "src/services/portfolio_service.py",
    "src/services/recommendation_engine.py",
    "src/services/role_command_handler.py",
    "src/services/soft_onboarding_service.py",
    "src/services/status_embedding_indexer.py",
    "src/services/swarm_intelligence_manager.py",
    "src/services/work_indexer.py",
    # Batch 4 (15 files)
    "src/services/chat_presence/__init__.py",
    "src/services/chat_presence/agent_personality.py",
    "src/services/chat_presence/channel_points_rewards.py",
    "src/services/chat_presence/chat_presence_orchestrator.py",
    "src/services/chat_presence/chat_scheduler.py",
    "src/services/chat_presence/message_interpreter.py",
    "src/services/chat_presence/quote_generator.py",
    "src/services/chat_presence/status_reader.py",
    "src/services/chat_presence/twitch_bridge.py",
    "src/services/chat_presence/twitch_eventsub_handler.py",
    "src/services/chat_presence/twitch_eventsub_server.py",
    "src/services/messaging_cli_coordinate_management/utilities.py",
    "src/services/models/__init__.py",
    "src/services/onboarding/hard/__init__.py",
    "src/services/onboarding/hard/default_message.py",
    # Batch 5 (15 files)
    "src/services/onboarding/hard/service.py",
    "src/services/onboarding/hard/steps.py",
    "src/services/onboarding/shared/__init__.py",
    "src/services/onboarding/shared/coordinates.py",
    "src/services/onboarding/shared/operations.py",
    "src/services/onboarding/soft/__init__.py",
    "src/services/onboarding/soft/canonical_closure_prompt.py",
    "src/services/onboarding/soft/cleanup_defaults.py",
    "src/services/onboarding/soft/default_message.py",
    "src/services/onboarding/soft/messaging_fallback.py",
    "src/services/onboarding/soft/service.py",
    "src/services/onboarding/soft/steps.py",
    "src/services/protocol/__init__.py",
    "src/services/protocol/message_router.py",
    "src/services/protocol/messaging_protocol_models.py",
    # Batch 6 (15 files)
    "src/services/protocol/policy_enforcer.py",
    "src/services/protocol/protocol_validator.py",
    "src/services/protocol/route_manager.py",
    "src/services/protocol/routers/__init__.py",
    "src/services/publishers/__init__.py",
    "src/services/swarm_website/__init__.py",
    "src/services/swarm_website/auto_updater.py",
    "src/services/swarm_website/website_updater.py",
    "src/services/thea/__init__.py",
    "src/services/thea/thea_service.py",
    "src/services/utils/__init__.py",
    "src/services/utils/agent_utils_registry.py",
    "src/services/utils/onboarding_constants.py",
    "src/services/utils/vector_config_utils.py",
    "src/services/utils/vector_integration_helpers.py",
]

# SSOT Domain Registry - integration domain is valid
VALID_DOMAINS = ["integration", "core", "architecture", "messaging", "onboarding", "services"]

def validate_tag_format(content: str) -> Tuple[bool, str]:
    """Validate SSOT tag format: <!-- SSOT Domain: integration -->"""
    pattern = r'<!--\s*SSOT\s+Domain:\s*integration\s*-->'
    if re.search(pattern, content, re.IGNORECASE):
        return True, "Tag format correct"
    return False, "Tag format incorrect or missing"

def validate_domain_registry(domain: str) -> Tuple[bool, str]:
    """Validate domain matches SSOT registry"""
    if domain.lower() == "integration":
        return True, "Domain matches SSOT registry"
    return False, f"Domain '{domain}' not in SSOT registry"

def validate_tag_placement(content: str) -> Tuple[bool, str]:
    """Validate tag placement in docstrings/headers"""
    # Check if tag is in module docstring (first 50 lines)
    lines = content.split('\n')[:50]
    header_content = '\n'.join(lines)
    
    if '<!-- SSOT Domain: integration -->' in header_content or '<!-- SSOT Domain:integration -->' in header_content:
        return True, "Tag placed in module docstring/header"
    return False, "Tag not found in module docstring/header (first 50 lines)"

def validate_compilation(file_path: Path) -> Tuple[bool, str]:
    """Validate Python file compiles without syntax errors"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(file_path)],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, "Compilation successful"
        else:
            return False, f"Compilation error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, "Compilation timeout"
    except Exception as e:
        return False, f"Compilation error: {str(e)}"

def validate_file(file_path: Path) -> Dict:
    """Validate a single file for SSOT compliance"""
    if not file_path.exists():
        return {
            "file": str(file_path),
            "valid": False,
            "error": "File not found"
        }
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "file": str(file_path),
            "valid": False,
            "error": f"Could not read file: {str(e)}"
        }
    
    results = {
        "file": str(file_path),
        "tag_format": validate_tag_format(content),
        "domain_registry": validate_domain_registry("integration"),
        "tag_placement": validate_tag_placement(content),
        "compilation": validate_compilation(file_path)
    }
    
    # Overall validation
    results["valid"] = all([
        results["tag_format"][0],
        results["domain_registry"][0],
        results["tag_placement"][0],
        results["compilation"][0]
    ])
    
    return results

def main():
    """Validate all integration batch files"""
    repo_root = Path(__file__).parent.parent
    results = []
    
    print("=" * 70)
    print("Integration Batches 1-6 Validation (90 files)")
    print("=" * 70)
    print()
    
    for file_path_str in INTEGRATION_BATCH_FILES:
        file_path = repo_root / file_path_str
        result = validate_file(file_path)
        results.append(result)
        
        status = "✅" if result["valid"] else "❌"
        print(f"{status} {file_path_str}")
        
        if not result["valid"]:
            if "error" in result:
                print(f"   Error: {result['error']}")
            else:
                if not result["tag_format"][0]:
                    print(f"   Tag Format: {result['tag_format'][1]}")
                if not result["domain_registry"][0]:
                    print(f"   Domain Registry: {result['domain_registry'][1]}")
                if not result["tag_placement"][0]:
                    print(f"   Tag Placement: {result['tag_placement'][1]}")
                if not result["compilation"][0]:
                    print(f"   Compilation: {result['compilation'][1]}")
    
    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    valid_count = sum(1 for r in results if r["valid"])
    total_count = len(results)
    
    print(f"Total Files: {total_count}")
    print(f"Valid: {valid_count} ✅")
    print(f"Invalid: {total_count - valid_count} ❌")
    print(f"Success Rate: {(valid_count/total_count)*100:.1f}%")
    
    if valid_count == total_count:
        print("\n🎉 All files validated successfully!")
        return 0
    else:
        print(f"\n⚠️  {total_count - valid_count} files need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())

