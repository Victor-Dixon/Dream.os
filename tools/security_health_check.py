#!/usr/bin/env python3
"""
Security Health Check Utility - ≤150 lines
==========================================

Quick security health assessment for swarm operations.
Provides rapid security status checking and alerting.

Usage:
    python tools/security_health_check.py
"""

import os
import json
from pathlib import Path
from datetime import datetime

def check_security_files():
    """Check for presence of critical security files."""
    critical_files = [
        'docs/security/VIBE_CODE_SECURITY_CLEANUP_KIT.md',
        'docs/security/SECURITY_IMPLEMENTATION_SUMMARY.md',
        'tools/security_audit_runner.py',
        'websites/scripts/security_test_suite.php'
    ]

    status = {}
    for file_path in critical_files:
        exists = Path(file_path).exists()
        status[file_path] = '✅ PRESENT' if exists else '❌ MISSING'

    return status

def check_recent_audits():
    """Check for recent security audit results."""
    audit_dir = Path('reports/security_audits')

    if not audit_dir.exists():
        return {'status': '❌ NO AUDIT DIRECTORY'}

    audits = list(audit_dir.glob('*.json'))
    if not audits:
        return {'status': '❌ NO AUDIT RESULTS'}

    # Check most recent audit
    most_recent = max(audits, key=lambda x: x.stat().st_mtime)
    age_hours = (datetime.now().timestamp() - most_recent.stat().st_mtime) / 3600

    if age_hours < 24:
        return {'status': '✅ RECENT AUDIT', 'file': str(most_recent), 'age_hours': round(age_hours, 1)}
    else:
        return {'status': '⚠️ STALE AUDIT', 'file': str(most_recent), 'age_hours': round(age_hours, 1)}

def check_qa_framework():
    """Check QA framework completeness."""
    qa_file = Path('docs/qa/QUALITY_ASSURANCE_FRAMEWORK.md')

    if not qa_file.exists():
        return {'status': '❌ QA FRAMEWORK MISSING'}

    content = qa_file.read_text()
    checks = {
        '4-phase roadmap': 'Phase 1:' in content and 'Phase 2:' in content,
        'Agent responsibilities': 'Agent-6' in content and 'Agent-1' in content,
        'Testing protocols': 'checklist' in content.lower(),
        'Coordination workflows': 'coordination' in content.lower()
    }

    passed = sum(1 for check in checks.values() if check)
    return {
        'status': f'✅ QA FRAMEWORK ({passed}/4 complete)',
        'checks': checks
    }

def generate_health_report():
    """Generate comprehensive security health report."""
    print("🔒 SECURITY HEALTH CHECK")
    print("=" * 40)

    # Check security files
    print("\n1. Security Infrastructure Files:")
    file_status = check_security_files()
    for file_path, status in file_status.items():
        print(f"   {status}: {file_path}")

    # Check audit status
    print("\n2. Security Audit Status:")
    audit_status = check_recent_audits()
    if 'file' in audit_status:
        print(f"   {audit_status['status']}: {audit_status['file']} ({audit_status['age_hours']}h old)")
    else:
        print(f"   {audit_status['status']}")

    # Check QA framework
    print("\n3. QA Framework Status:")
    qa_status = check_qa_framework()
    print(f"   {qa_status['status']}")
    if 'checks' in qa_status:
        for check_name, passed in qa_status['checks'].items():
            status_icon = '✅' if passed else '❌'
            print(f"      {status_icon} {check_name}")

    # Overall assessment
    print("\n4. Overall Security Health:")
    scores = {
        'files': sum(1 for s in file_status.values() if '✅' in s) / len(file_status),
        'audits': 1.0 if '✅' in audit_status.get('status', '') else 0.5,
        'qa': 1.0 if '4/4' in qa_status.get('status', '') else 0.7
    }

    overall_score = sum(scores.values()) / len(scores)
    if overall_score >= 0.9:
        health_status = "🟢 EXCELLENT"
    elif overall_score >= 0.7:
        health_status = "🟡 GOOD"
    else:
        health_status = "🔴 NEEDS ATTENTION"

    print(f"   {health_status} ({overall_score:.1%} security readiness)")
    print(f"   Files: {scores['files']:.1%} | Audits: {scores['audits']:.1%} | QA: {scores['qa']:.1%}")

    print("
✅ Security health check completed"
if __name__ == "__main__":
    generate_health_report()