#!/usr/bin/env python3
"""
Create System Health Coordination Dashboard
===========================================

Creates a coordination dashboard showing system health metrics:
- Toolbelt health (100%)
- Import health (0 issues)
- V2 compliance (87.7%, 204 violations)
- Website audits (complete)

Agent-6: Coordination & Communication Specialist
Task: Create system health coordination dashboard (MEDIUM priority)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict

def load_health_metrics() -> Dict:
    """Load health metrics from various sources."""
    project_root = Path(__file__).parent.parent
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "toolbelt_health": {},
        "import_health": {},
        "v2_compliance": {},
        "website_audits": {},
        "overall_health": {}
    }
    
    # Toolbelt health
    toolbelt_audit = project_root / "toolbelt_health_audit.json"
    if toolbelt_audit.exists():
        try:
            with open(toolbelt_audit, 'r', encoding='utf-8') as f:
                toolbelt_data = json.load(f)
                metrics["toolbelt_health"] = {
                    "status": toolbelt_data.get("health_status", "UNKNOWN"),
                    "tools_audited": toolbelt_data.get("total_tools", 0),
                    "working_tools": toolbelt_data.get("working_tools", 0),
                    "broken_tools": toolbelt_data.get("broken_tools", 0),
                    "success_rate": toolbelt_data.get("success_rate", 0)
                }
        except Exception:
            metrics["toolbelt_health"] = {"status": "UNKNOWN", "note": "Could not load toolbelt audit"}
    else:
        metrics["toolbelt_health"] = {"status": "UNKNOWN", "note": "toolbelt_health_audit.json not found"}
    
    # Import health
    import_audit = project_root / "reports" / "import_audit_report.json"
    if import_audit.exists():
        try:
            with open(import_audit, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                circular_deps = import_data.get("circular_dependencies", [])
                if isinstance(circular_deps, list):
                    circular_deps_count = len(circular_deps)
                else:
                    circular_deps_count = circular_deps if isinstance(circular_deps, int) else 0
                
                metrics["import_health"] = {
                    "status": "HEALTHY" if circular_deps_count == 0 else "ISSUES",
                    "files_analyzed": import_data.get("total_files", 0),
                    "circular_dependencies": circular_deps_count,
                    "ssot_violations": import_data.get("ssot_violations", 0)
                }
        except Exception:
            metrics["import_health"] = {"status": "UNKNOWN", "note": "Could not load import audit"}
    else:
        metrics["import_health"] = {"status": "UNKNOWN", "note": "import_audit_report.json not found"}
    
    # V2 compliance
    v2_violations = project_root / "agent_workspaces" / "Agent-6" / "v2_violations_count.json"
    if v2_violations.exists():
        try:
            with open(v2_violations, 'r', encoding='utf-8') as f:
                v2_data = json.load(f)
                metrics["v2_compliance"] = {
                    "status": "NEEDS_IMPROVEMENT" if v2_data.get("violation_count", 0) > 0 else "COMPLIANT",
                    "total_files": v2_data.get("total_files", 0),
                    "compliant_files": v2_data.get("compliant_files", 0),
                    "violations": v2_data.get("violation_count", 0),
                    "compliance_percent": v2_data.get("compliance_percent", 0)
                }
        except Exception:
            metrics["v2_compliance"] = {"status": "UNKNOWN", "note": "Could not load V2 violations"}
    else:
        metrics["v2_compliance"] = {"status": "UNKNOWN", "note": "v2_violations_count.json not found"}
    
    # Website audits
    website_audit_summary = project_root / "docs" / "website_audits" / "COMPREHENSIVE_AUDIT_SUMMARY_2025-12-22.md"
    if website_audit_summary.exists():
        metrics["website_audits"] = {
            "status": "COMPLETE",
            "summary_file": str(website_audit_summary.relative_to(project_root)),
            "note": "Comprehensive audit completed 2025-12-22"
        }
    else:
        metrics["website_audits"] = {"status": "UNKNOWN", "note": "Audit summary not found"}
    
    # Calculate overall health
    health_scores = []
    if metrics["toolbelt_health"].get("status") == "EXCELLENT":
        health_scores.append(100)
    elif metrics["toolbelt_health"].get("status") == "UNKNOWN":
        health_scores.append(50)
    else:
        health_scores.append(metrics["toolbelt_health"].get("success_rate", 0))
    
    if metrics["import_health"].get("status") == "HEALTHY":
        health_scores.append(100)
    elif metrics["import_health"].get("status") == "UNKNOWN":
        health_scores.append(50)
    else:
        health_scores.append(0)
    
    if metrics["v2_compliance"].get("status") == "COMPLIANT":
        health_scores.append(100)
    elif metrics["v2_compliance"].get("status") == "UNKNOWN":
        health_scores.append(50)
    else:
        health_scores.append(metrics["v2_compliance"].get("compliance_percent", 0))
    
    if metrics["website_audits"].get("status") == "COMPLETE":
        health_scores.append(100)
    else:
        health_scores.append(50)
    
    overall_score = sum(health_scores) / len(health_scores) if health_scores else 0
    
    metrics["overall_health"] = {
        "score": round(overall_score, 1),
        "status": "EXCELLENT" if overall_score >= 90 else "GOOD" if overall_score >= 75 else "NEEDS_IMPROVEMENT",
        "components": len(health_scores),
        "timestamp": datetime.now().isoformat()
    }
    
    return metrics

def generate_dashboard_markdown(metrics: Dict) -> str:
    """Generate markdown dashboard."""
    md = f"""# System Health Coordination Dashboard

**Generated**: {metrics['timestamp']}  
**Overall Health**: {metrics['overall_health']['status']} ({metrics['overall_health']['score']}%)

---

## Toolbelt Health

**Status**: {metrics['toolbelt_health'].get('status', 'UNKNOWN')}  
**Tools Audited**: {metrics['toolbelt_health'].get('tools_audited', 'N/A')}  
**Working Tools**: {metrics['toolbelt_health'].get('working_tools', 'N/A')}  
**Broken Tools**: {metrics['toolbelt_health'].get('broken_tools', 'N/A')}  
**Success Rate**: {metrics['toolbelt_health'].get('success_rate', 'N/A')}%

---

## Import Health

**Status**: {metrics['import_health'].get('status', 'UNKNOWN')}  
**Files Analyzed**: {metrics['import_health'].get('files_analyzed', 'N/A')}  
**Circular Dependencies**: {metrics['import_health'].get('circular_dependencies', 'N/A')}  
**SSOT Violations**: {metrics['import_health'].get('ssot_violations', 'N/A')}

---

## V2 Compliance

**Status**: {metrics['v2_compliance'].get('status', 'UNKNOWN')}  
**Total Files**: {metrics['v2_compliance'].get('total_files', 'N/A')}  
**Compliant Files**: {metrics['v2_compliance'].get('compliant_files', 'N/A')}  
**Violations**: {metrics['v2_compliance'].get('violations', 'N/A')}  
**Compliance**: {metrics['v2_compliance'].get('compliance_percent', 'N/A')}%

---

## Website Audits

**Status**: {metrics['website_audits'].get('status', 'UNKNOWN')}  
**Summary**: {metrics['website_audits'].get('note', 'N/A')}

---

## Coordination Recommendations

"""
    
    recommendations = []
    
    if metrics['v2_compliance'].get('violations', 0) > 0:
        recommendations.append(f"- **V2 Compliance**: {metrics['v2_compliance'].get('violations', 0)} violations need refactoring (current: {metrics['v2_compliance'].get('compliance_percent', 0)}% compliance)")
    
    broken_tools = metrics['toolbelt_health'].get('broken_tools', 0)
    if isinstance(broken_tools, (int, float)) and broken_tools > 0:
        recommendations.append(f"- **Toolbelt**: {broken_tools} broken tools need fixing")
    
    if metrics['import_health'].get('circular_dependencies', 0) > 0:
        recommendations.append(f"- **Imports**: {metrics['import_health'].get('circular_dependencies', 0)} circular dependencies need resolution")
    
    if not recommendations:
        recommendations.append("- ✅ All systems healthy - no immediate coordination actions needed")
    
    md += "\n".join(recommendations)
    md += "\n\n---\n\n*Dashboard generated by Agent-6 (Coordination & Communication Specialist)*"
    
    return md

def main():
    """Main execution."""
    print("=" * 70)
    print("SYSTEM HEALTH COORDINATION DASHBOARD")
    print("=" * 70)
    print()
    
    metrics = load_health_metrics()
    
    print("TOOLBELT HEALTH:")
    print(f"  Status: {metrics['toolbelt_health'].get('status', 'UNKNOWN')}")
    print(f"  Success Rate: {metrics['toolbelt_health'].get('success_rate', 'N/A')}%")
    
    print()
    print("IMPORT HEALTH:")
    print(f"  Status: {metrics['import_health'].get('status', 'UNKNOWN')}")
    print(f"  Circular Dependencies: {metrics['import_health'].get('circular_dependencies', 'N/A')}")
    
    print()
    print("V2 COMPLIANCE:")
    print(f"  Status: {metrics['v2_compliance'].get('status', 'UNKNOWN')}")
    print(f"  Compliance: {metrics['v2_compliance'].get('compliance_percent', 'N/A')}%")
    print(f"  Violations: {metrics['v2_compliance'].get('violations', 'N/A')}")
    
    print()
    print("WEBSITE AUDITS:")
    print(f"  Status: {metrics['website_audits'].get('status', 'UNKNOWN')}")
    
    print()
    print("=" * 70)
    print("OVERALL HEALTH:")
    print(f"  Score: {metrics['overall_health']['score']}%")
    print(f"  Status: {metrics['overall_health']['status']}")
    
    # Save JSON
    output_json = Path("agent_workspaces/Agent-6/system_health_dashboard.json")
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
    
    # Save Markdown
    dashboard_md = generate_dashboard_markdown(metrics)
    output_md = Path("agent_workspaces/Agent-6/system_health_dashboard.md")
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(dashboard_md)
    
    print()
    print(f"✅ Dashboard saved to:")
    print(f"   JSON: {output_json}")
    print(f"   Markdown: {output_md}")

if __name__ == "__main__":
    main()

