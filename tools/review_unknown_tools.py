#!/usr/bin/env python3
"""
Review and Classify UNKNOWN Tools
==================================

Reviews tools classified as UNKNOWN and reclassifies them as SIGNAL or NOISE
based on manual analysis of their purpose and usage.

<!-- SSOT Domain: tools -->
"""

import json
from pathlib import Path
from typing import Dict, List

def load_classification_report() -> Dict:
    """Load the tool classification report."""
    report_path = Path("reports/tool_classification_signal_noise.json")
    if not report_path.exists():
        print("❌ Classification report not found")
        return {}
    
    with open(report_path) as f:
        return json.load(f)

def analyze_unknown_tool(file_path: Path) -> str:
    """Analyze a single UNKNOWN tool to determine classification."""
    if not file_path.exists():
        return "UNKNOWN"
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        path_str = str(file_path).lower()
        name_lower = file_path.name.lower()
        
        # Test files - likely NOISE unless part of test infrastructure
        if "test_" in name_lower or "_test.py" in name_lower:
            # Infrastructure tests (deployment, staging, integration) are SIGNAL
            if any(keyword in path_str for keyword in ["deployment", "staging", "integration", "infrastructure"]):
                return "SIGNAL"
            return "NOISE"
        
        # Standalone scripts - check if they're entry points or utilities
        if "start_" in name_lower or "run_" in name_lower:
            # Entry point scripts are usually SIGNAL
            return "SIGNAL"
        
        # Monitoring/health tools - usually SIGNAL
        if any(keyword in name_lower for keyword in ["monitor", "health", "dashboard", "status"]):
            return "SIGNAL"
        
        # Configuration/setup tools - usually SIGNAL
        if any(keyword in name_lower for keyword in ["setup", "config", "add_", "install"]):
            return "SIGNAL"
        
        # CLI tools - usually SIGNAL
        if "_cli" in name_lower or "cli_" in name_lower:
            return "SIGNAL"
        
        # Planner/coordination tools - usually SIGNAL
        if any(keyword in name_lower for keyword in ["planner", "coordinate", "assign"]):
            return "SIGNAL"
        
        # Deployment tools - usually SIGNAL
        if "deploy" in name_lower:
            return "SIGNAL"
        
        # Generator tools - usually SIGNAL
        if "generate" in name_lower:
            return "SIGNAL"
        
        # Update/sync tools - usually SIGNAL
        if any(keyword in name_lower for keyword in ["update", "sync", "calibrate"]):
            return "SIGNAL"
        
        # Check if it's imported or used
        if "import" in content.lower() or "from" in content.lower():
            # Has imports - likely SIGNAL
            return "SIGNAL"
        
        # If it's a core infrastructure file (tool_spec, base classes), likely SIGNAL
        if "tool_spec" in name_lower or "base" in name_lower or "spec" in name_lower:
            return "SIGNAL"
        
        # If it has a main function or entry point, likely SIGNAL
        if "if __name__" in content or "def main" in content.lower():
            return "SIGNAL"
        
        return "UNKNOWN"  # Still unclear
        
    except Exception as e:
        print(f"⚠️  Error analyzing {file_path}: {e}")
        return "UNKNOWN"

def main():
    """Review and reclassify UNKNOWN tools."""
    print("="*60)
    print("UNKNOWN TOOL CLASSIFICATION REVIEW")
    print("="*60)
    print()
    
    # Load classification report
    data = load_classification_report()
    if not data:
        return 1
    
    unknown_tools = data['classifications']['UNKNOWN']
    print(f"📊 Found {len(unknown_tools)} UNKNOWN tools to review")
    print()
    
    # Analyze each tool
    reclassifications = {
        "SIGNAL": [],
        "NOISE": [],
        "UNKNOWN": []
    }
    
    tools_dir = Path("tools")
    
    print("🔍 Analyzing UNKNOWN tools...")
    print()
    
    for tool_info in unknown_tools:
        tool_path = tools_dir / tool_info['path']
        new_classification = analyze_unknown_tool(tool_path)
        
        tool_info['reviewed_classification'] = new_classification
        reclassifications[new_classification].append(tool_info)
        
        status = "✅" if new_classification != "UNKNOWN" else "❓"
        print(f"{status} {tool_info['path']} → {new_classification}")
    
    print()
    print("="*60)
    print("RECLASSIFICATION SUMMARY")
    print("="*60)
    print()
    print(f"✅ SIGNAL: {len(reclassifications['SIGNAL'])} tools")
    print(f"❌ NOISE: {len(reclassifications['NOISE'])} tools")
    print(f"❓ UNKNOWN: {len(reclassifications['UNKNOWN'])} tools (still need manual review)")
    print()
    
    # Save reclassification report
    report_path = Path("reports/tool_classification_review.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    review_report = {
        "review_date": "2025-12-30",
        "original_unknown_count": len(unknown_tools),
        "reclassifications": reclassifications,
        "summary": {
            "SIGNAL": len(reclassifications['SIGNAL']),
            "NOISE": len(reclassifications['NOISE']),
            "UNKNOWN": len(reclassifications['UNKNOWN'])
        }
    }
    
    with open(report_path, 'w') as f:
        json.dump(review_report, f, indent=2)
    
    print(f"📄 Review report saved to: {report_path}")
    print()
    
    # Show tools that still need manual review
    if reclassifications['UNKNOWN']:
        print("="*60)
        print("TOOLS STILL NEEDING MANUAL REVIEW")
        print("="*60)
        print()
        for tool in reclassifications['UNKNOWN']:
            print(f"  ❓ {tool['path']}")
        print()
    
    return 0

if __name__ == "__main__":
    exit(main())

