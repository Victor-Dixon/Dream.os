#!/usr/bin/env python3
"""
Post-Deployment Verification Tool
=================================

Runs comprehensive verification after manual deployment.

Author: Agent-7 (Web Development Specialist)
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Import existing verification tool
sys.path.insert(0, str(Path(__file__).parent))
from verify_website_fixes import verify_prismblossom, verify_freerideinvestor

def create_deployment_report(results: dict) -> Path:
    """Create deployment completion report."""
    report_dir = Path("agent_workspaces/Agent-7")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / "DEPLOYMENT_COMPLETION_REPORT.md"
    
    report = f"""# Deployment Completion Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agent**: Agent-7 (Web Development Specialist)  
**Status**: ✅ **VERIFICATION COMPLETE**

---

## 📊 **EXECUTIVE SUMMARY**

**Deployment Method**: Manual WordPress Admin  
**Sites Deployed**: 2  
**Verification Status**: See details below

---

## 🔍 **VERIFICATION RESULTS**

### **1. FreeRideInvestor**

#### **Navigation Menu**:
- **Developer Tools Links Found**: {results.get('freerideinvestor', {}).get('developer_tools_links', 'N/A')}
- **Status**: {"✅ PASS" if results.get('freerideinvestor', {}).get('developer_tools_links', 999) == 0 else "❌ FAIL"}
- **Expected**: 0 links
- **Previous**: 18 links

#### **Text Rendering**:
- **Status**: {results.get('freerideinvestor', {}).get('text_rendering', 'N/A')}
- **Issues Found**: {len(results.get('freerideinvestor', {}).get('text_issues', []))}

#### **Site Functionality**:
- **Status**: {results.get('freerideinvestor', {}).get('functionality', 'N/A')}

---

### **2. prismblossom.online**

#### **Text Rendering**:
- **Status**: {results.get('prismblossom', {}).get('text_rendering', 'N/A')}
- **Issues Found**: {len(results.get('prismblossom', {}).get('text_issues', []))}

#### **Contact Form**:
- **Status**: {results.get('prismblossom', {}).get('contact_form', 'N/A')}
- **Forms Found**: {results.get('prismblossom', {}).get('forms_found', 'N/A')}

#### **Site Functionality**:
- **Status**: {results.get('prismblossom', {}).get('functionality', 'N/A')}

---

## ✅ **SUCCESS CRITERIA**

| Site | Criteria | Status |
|------|----------|--------|
| FreeRideInvestor | 0 Developer Tools links | {"✅ PASS" if results.get('freerideinvestor', {}).get('developer_tools_links', 999) == 0 else "❌ FAIL"} |
| FreeRideInvestor | Text rendering fixed | {results.get('freerideinvestor', {}).get('text_rendering', 'N/A')} |
| prismblossom.online | Text rendering fixed | {results.get('prismblossom', {}).get('text_rendering', 'N/A')} |
| prismblossom.online | Contact form working | {results.get('prismblossom', {}).get('contact_form', 'N/A')} |

---

## 📋 **DETAILED FINDINGS**

### **FreeRideInvestor**:
{format_findings(results.get('freerideinvestor', {}))}

### **prismblossom.online**:
{format_findings(results.get('prismblossom', {}))}

---

## 🎯 **OVERALL STATUS**

**Deployment**: ✅ **COMPLETE**  
**Verification**: {"✅ PASS" if all_checks_passed(results) else "⚠️ ISSUES FOUND"}  
**Next Steps**: {get_next_steps(results)}

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Agent**: Agent-7 (Web Development Specialist)

🐝 **WE. ARE. SWARM. ⚡🔥**
"""
    
    report_file.write_text(report)
    return report_file

def format_findings(site_results: dict) -> str:
    """Format findings for report."""
    findings = []
    if site_results.get('developer_tools_links', 0) > 0:
        findings.append(f"- ⚠️  {site_results['developer_tools_links']} Developer Tools links still present")
    if site_results.get('text_issues'):
        for issue in site_results['text_issues']:
            findings.append(f"- ⚠️  {issue}")
    if not findings:
        findings.append("- ✅ No issues found")
    return "\n".join(findings)

def all_checks_passed(results: dict) -> bool:
    """Check if all verification checks passed."""
    freeride = results.get('freerideinvestor', {})
    prism = results.get('prismblossom', {})
    
    return (
        freeride.get('developer_tools_links', 999) == 0 and
        freeride.get('text_rendering') == 'success' and
        prism.get('text_rendering') == 'success' and
        prism.get('contact_form') == 'success'
    )

def get_next_steps(results: dict) -> str:
    """Get next steps based on results."""
    if all_checks_passed(results):
        return "✅ All checks passed - Deployment successful!"
    
    steps = []
    if results.get('freerideinvestor', {}).get('developer_tools_links', 0) > 0:
        steps.append("1. FreeRideInvestor: Remove remaining Developer Tools links manually")
    if results.get('freerideinvestor', {}).get('text_rendering') != 'success':
        steps.append("2. FreeRideInvestor: Check text rendering fixes")
    if results.get('prismblossom', {}).get('text_rendering') != 'success':
        steps.append("3. prismblossom.online: Check text rendering fixes")
    
    return "\n".join(steps) if steps else "✅ All checks passed!"

def main():
    """Main verification function."""
    print("=" * 60)
    print("🔍 Post-Deployment Verification")
    print("=" * 60)
    print()
    
    # Run verification
    print("Running website verification...")
    print()
    
    # Verify both sites
    freeride_results = verify_freerideinvestor()
    prism_results = verify_prismblossom()
    
    # Extract key metrics
    results = {
        "freerideinvestor": {
            "developer_tools_links": 0,
            "text_rendering": "unknown",
            "text_issues": [],
            "functionality": "unknown"
        },
        "prismblossom": {
            "text_rendering": "unknown",
            "text_issues": [],
            "contact_form": "unknown",
            "forms_found": 0,
            "functionality": "unknown"
        }
    }
    
    # Parse FreeRideInvestor results
    for check in freeride_results.get('checks', []):
        if check.get('type') == 'navigation_menu':
            results['freerideinvestor']['developer_tools_links'] = check.get('developer_tools_links_found', 0)
        elif check.get('type') == 'text_rendering_home':
            results['freerideinvestor']['text_rendering'] = check.get('status', 'unknown')
            if check.get('issues'):
                results['freerideinvestor']['text_issues'].extend(check['issues'])
    
    # Parse prismblossom results
    for check in prism_results.get('checks', []):
        if check.get('type') == 'text_rendering_home':
            results['prismblossom']['text_rendering'] = check.get('status', 'unknown')
            if check.get('issues'):
                results['prismblossom']['text_issues'].extend(check['issues'])
        elif check.get('type') == 'contact_form':
            results['prismblossom']['contact_form'] = check.get('status', 'unknown')
            results['prismblossom']['forms_found'] = check.get('forms_found', 0)
    
    # Create report
    report_file = create_deployment_report(results)
    
    print("=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    print()
    print(f"FreeRideInvestor:")
    print(f"  Developer Tools Links: {results['freerideinvestor']['developer_tools_links']} (expected: 0)")
    print(f"  Text Rendering: {results['freerideinvestor']['text_rendering']}")
    print()
    print(f"prismblossom.online:")
    print(f"  Text Rendering: {results['prismblossom']['text_rendering']}")
    print(f"  Contact Form: {results['prismblossom']['contact_form']}")
    print()
    print(f"✅ Report created: {report_file}")
    print()
    
    # Determine overall status
    if all_checks_passed(results):
        print("✅ All verification checks PASSED!")
        return 0
    else:
        print("⚠️  Some verification checks FAILED - see report for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())

