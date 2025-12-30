#!/usr/bin/env python3
"""
Tool Classification: Signal vs Noise
====================================

Classifies tools in the tools/ directory as SIGNAL (active/important) or NOISE (unused/deprecated).

Classification Criteria:
- SIGNAL: Tools registered in tool_registry.lock.json, actively imported, or part of core infrastructure
- NOISE: Deprecated, legacy, unused, or test-only tools
- UNKNOWN: Tools that can't be clearly classified

<!-- SSOT Domain: tools -->
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# Classification criteria
SIGNAL_INDICATORS = [
    "tool_registry.lock.json",  # Registered tools
    "import",  # Actively imported
    "from tools",  # Referenced by other tools
    "core",  # Core infrastructure
    "toolbelt",  # Toolbelt system
    "registry",  # Registry system
]

NOISE_INDICATORS = [
    "deprecated",
    "DEPRECATED",
    "legacy",
    "LEGACY",
    "unused",
    "old",
    "archive",
    "test_",  # Test-only files
    "_test.py",
    "example",
    "demo",
    "standalone",  # Standalone scripts (may be noise)
]

def load_tool_registry() -> Set[str]:
    """Load registered tools from tool_registry.lock.json."""
    registry_path = Path("tools/tool_registry.lock.json")
    if not registry_path.exists():
        return set()
    
    try:
        with open(registry_path, "r") as f:
            data = json.load(f)
            tools = data.get("tools", {})
            # Extract module paths from registry
            registered_modules = set()
            for tool_name, (module_path, _) in tools.items():
                # Convert module path to file path
                # e.g., "tools.categories.vector_tools" -> "tools/categories/vector_tools.py"
                file_path = module_path.replace(".", "/") + ".py"
                registered_modules.add(file_path)
            return registered_modules
    except Exception as e:
        print(f"⚠️  Error loading registry: {e}")
        return set()

def check_file_imports(file_path: Path, all_tools: List[Path]) -> Set[str]:
    """Check if file is imported by other tools."""
    imported_by = set()
    file_module = str(file_path.relative_to(Path("tools"))).replace("\\", "/").replace(".py", "").replace("/", ".")
    
    for tool in all_tools:
        if tool == file_path:
            continue
        try:
            content = tool.read_text(encoding="utf-8", errors="ignore")
            # Check for imports
            patterns = [
                rf"from\s+{re.escape(file_module)}",
                rf"import\s+{re.escape(file_module)}",
                rf"from\s+tools\.{re.escape(file_module.split('.', 1)[-1] if '.' in file_module else file_module)}",
            ]
            for pattern in patterns:
                if re.search(pattern, content):
                    imported_by.add(str(tool.relative_to(Path("tools"))))
                    break
        except Exception:
            pass
    
    return imported_by

def classify_tool(file_path: Path, registered_modules: Set[str], all_tools: List[Path]) -> Tuple[str, Dict]:
    """Classify a single tool as SIGNAL, NOISE, or UNKNOWN."""
    rel_path = str(file_path.relative_to(Path("tools"))).replace("\\", "/")
    classification = "UNKNOWN"
    reasons = []
    metadata = {
        "path": rel_path,
        "is_registered": False,
        "is_imported": False,
        "has_deprecated": False,
        "is_test": False,
        "imported_by": [],
    }
    
    # Check if registered
    if rel_path in registered_modules:
        classification = "SIGNAL"
        reasons.append("Registered in tool_registry.lock.json")
        metadata["is_registered"] = True
    
    # Read file content
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return "UNKNOWN", metadata
    
    # Check for NOISE indicators
    file_lower = content.lower()
    path_lower = str(file_path).lower()
    
    # Check for deprecated markers (but not in comments about other tools)
    if "deprecated" in file_lower or "DEPRECATED" in file_lower:
        # Only mark as deprecated if it's clearly about THIS file
        deprecated_patterns = [
            r"⚠️\s*deprecated",
            r"deprecated.*this tool",
            r"this.*deprecated",
            r"deprecated.*replaced",
            r"⚠️\s*DEPRECATED",
            r"DEPRECATED.*This tool",
        ]
        # Skip if this is the classification script itself
        if file_path.name == "classify_tools_signal_noise.py":
            pass  # Don't classify the classifier as deprecated
        elif any(re.search(pattern, content, re.IGNORECASE) for pattern in deprecated_patterns):
            classification = "NOISE"
            reasons.append("Marked as deprecated")
            metadata["has_deprecated"] = True
    
    # Check for test files
    if "test_" in path_lower or "_test.py" in path_lower or path_lower.endswith("tests/"):
        # Test files in tests/ directory are usually NOISE (test infrastructure)
        # But test files that are part of core testing might be SIGNAL
        if "tests/" in path_lower or path_lower.startswith("test_"):
            classification = "NOISE"
            reasons.append("Test-only file")
            metadata["is_test"] = True
    
    # Check if imported by other tools
    imported_by = check_file_imports(file_path, all_tools)
    if imported_by:
        if classification == "UNKNOWN":
            classification = "SIGNAL"
        reasons.append(f"Imported by {len(imported_by)} tool(s)")
        metadata["is_imported"] = True
        metadata["imported_by"] = list(imported_by)[:5]  # Limit to first 5
    
    # Check for core infrastructure indicators
    if any(indicator in content for indicator in ["tool_registry", "toolbelt_core", "IToolAdapter"]):
        if classification == "UNKNOWN":
            classification = "SIGNAL"
        reasons.append("Core infrastructure component")
    
    # Check for utility/helper tools that are actively used
    utility_indicators = ["tag_analyzer", "ssot_tagging", "validate", "verify", "check", "audit", "classify"]
    if any(indicator in rel_path.lower() for indicator in utility_indicators):
        if classification == "UNKNOWN" and "test" not in path_lower:
            # Utility tools are likely SIGNAL if not tests
            classification = "SIGNAL"
            reasons.append("Utility/helper tool")
    
    # Classification and analysis tools are SIGNAL
    if any(indicator in rel_path.lower() for indicator in ["classify", "analyzer", "validator", "checker"]):
        if classification == "UNKNOWN":
            classification = "SIGNAL"
            reasons.append("Analysis/classification tool")
    
    # Special cases
    if file_path.name == "__init__.py":
        # __init__.py files are usually SIGNAL if they're in registered modules
        if any(rel_path.startswith(reg.replace(".py", "")) for reg in registered_modules):
            classification = "SIGNAL"
            reasons.append("Package init for registered module")
    
    metadata["classification"] = classification
    metadata["reasons"] = reasons
    
    return classification, metadata

def main():
    """Main classification function."""
    tools_dir = Path("tools")
    if not tools_dir.exists():
        print("❌ tools/ directory not found")
        return 1
    
    # Load registered tools
    print("📊 Loading tool registry...")
    registered_modules = load_tool_registry()
    print(f"   Found {len(registered_modules)} registered tool modules")
    
    # Find all Python files
    print("🔍 Scanning tools/ directory...")
    all_tools = list(tools_dir.rglob("*.py"))
    print(f"   Found {len(all_tools)} Python files")
    
    # Classify each tool
    print("🏷️  Classifying tools...")
    classifications = defaultdict(list)
    results = []
    
    for tool_path in all_tools:
        classification, metadata = classify_tool(tool_path, registered_modules, all_tools)
        classifications[classification].append(metadata)
        results.append(metadata)
    
    # Generate report
    print("\n" + "="*60)
    print("📊 TOOL CLASSIFICATION RESULTS")
    print("="*60)
    
    signal_count = len(classifications["SIGNAL"])
    noise_count = len(classifications["NOISE"])
    unknown_count = len(classifications["UNKNOWN"])
    total = len(results)
    
    print(f"\n✅ SIGNAL: {signal_count} tools ({signal_count/total*100:.1f}%)")
    print(f"❌ NOISE: {noise_count} tools ({noise_count/total*100:.1f}%)")
    print(f"❓ UNKNOWN: {unknown_count} tools ({unknown_count/total*100:.1f}%)")
    print(f"📦 TOTAL: {total} tools")
    
    # Save detailed report
    report_path = Path("reports/tool_classification_signal_noise.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = {
        "classification_date": "2025-12-30",
        "total_tools": total,
        "summary": {
            "SIGNAL": signal_count,
            "NOISE": noise_count,
            "UNKNOWN": unknown_count,
        },
        "classifications": {
            "SIGNAL": classifications["SIGNAL"],
            "NOISE": classifications["NOISE"],
            "UNKNOWN": classifications["UNKNOWN"],
        },
    }
    
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    
    # Print sample classifications
    print("\n" + "="*60)
    print("📋 SAMPLE CLASSIFICATIONS")
    print("="*60)
    
    print("\n✅ SIGNAL Examples (first 5):")
    for tool in classifications["SIGNAL"][:5]:
        print(f"   - {tool['path']}")
        print(f"     Reasons: {', '.join(tool['reasons'])}")
    
    print("\n❌ NOISE Examples (first 5):")
    for tool in classifications["NOISE"][:5]:
        print(f"   - {tool['path']}")
        print(f"     Reasons: {', '.join(tool['reasons'])}")
    
    if classifications["UNKNOWN"]:
        print("\n❓ UNKNOWN Examples (first 5):")
        for tool in classifications["UNKNOWN"][:5]:
            print(f"   - {tool['path']}")
    
    return 0

if __name__ == "__main__":
    exit(main())

