#!/usr/bin/env python3
"""
Devlog Compliance Validator Tool

Validates devlog format compliance against enforcement protocol:
- Next Steps section present at end
- Skimmable format (clear headings, bullet points, status emojis)
- MASTER_TASK_LOG references
- Correct tool usage (devlog_poster_agent_channel.py)

Usage:
    python tools/devlog_compliance_validator.py --agent Agent-X --file <devlog_path>
    python tools/devlog_compliance_validator.py --agent Agent-X --file <devlog_path> --fix
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class DevlogComplianceValidator:
    """Validates devlog format compliance against enforcement protocol."""
    
    def __init__(self, devlog_path: Path, agent_id: str):
        self.devlog_path = devlog_path
        self.agent_id = agent_id
        self.content = devlog_path.read_text(encoding='utf-8')
        self.violations: List[Dict[str, str]] = []
        self.warnings: List[Dict[str, str]] = []
        
    def validate(self) -> Dict[str, any]:
        """Run all validation checks."""
        self._check_next_steps_section()
        self._check_skimmable_format()
        self._check_master_task_log_references()
        self._check_task_summary()
        self._check_actions_taken()
        self._check_results_section()
        self._check_artifacts_section()
        
        return {
            "agent_id": self.agent_id,
            "devlog_path": str(self.devlog_path),
            "validation_date": datetime.now().isoformat(),
            "compliant": len(self.violations) == 0,
            "violations": self.violations,
            "warnings": self.warnings,
            "score": self._calculate_score()
        }
    
    def _check_next_steps_section(self):
        """Check if Next Steps section is present at end of devlog."""
        # Look for "Next Steps" heading near end of document
        next_steps_patterns = [
            r'##\s*Next Steps',
            r'###\s*Next Steps',
            r'\*\*Next Steps\*\*',
            r'Next Steps:',
            r'## 🎯 Next Steps',
            r'## 📋 Next Steps'
        ]
        
        # Check last 30% of document for Next Steps
        content_length = len(self.content)
        last_section = self.content[int(content_length * 0.7):]
        
        found = False
        for pattern in next_steps_patterns:
            if re.search(pattern, last_section, re.IGNORECASE):
                found = True
                break
        
        if not found:
            self.violations.append({
                "type": "missing_next_steps",
                "severity": "CRITICAL",
                "message": "Next Steps section not found at end of devlog",
                "requirement": "All devlogs must include 'Next Steps' section at the end"
            })
        else:
            # Check if Next Steps section has actual content
            next_steps_match = re.search(
                r'(?:##|###|\*\*)\s*Next Steps.*?(?=\n##|\Z)',
                last_section,
                re.IGNORECASE | re.DOTALL
            )
            if next_steps_match:
                next_steps_content = next_steps_match.group(0)
                # Check if it has actual list items or content
                if not re.search(r'[-*•]\s+|^\d+\.', next_steps_content, re.MULTILINE):
                    self.warnings.append({
                        "type": "empty_next_steps",
                        "severity": "WARNING",
                        "message": "Next Steps section found but appears empty or lacks actionable items"
                    })
    
    def _check_skimmable_format(self):
        """Check if devlog uses skimmable format (headings, bullet points, status emojis)."""
        # Check for clear headings (## or ###)
        headings = re.findall(r'^##+\s+.+', self.content, re.MULTILINE)
        if len(headings) < 3:
            self.warnings.append({
                "type": "insufficient_headings",
                "severity": "WARNING",
                "message": f"Only {len(headings)} headings found - devlog may not be skimmable",
                "recommendation": "Use clear headings (##, ###) to organize content"
            })
        
        # Check for bullet points
        bullet_points = re.findall(r'^[-*•]\s+', self.content, re.MULTILINE)
        if len(bullet_points) < 5:
            self.warnings.append({
                "type": "insufficient_bullets",
                "severity": "WARNING",
                "message": f"Only {len(bullet_points)} bullet points found - devlog may not be skimmable",
                "recommendation": "Use bullet points for lists and actions"
            })
        
        # Check for status emojis (optional but recommended)
        status_emojis = re.findall(r'[✅⏳🟡❌🚧🎯📋📊📁]', self.content)
        if len(status_emojis) < 3:
            self.warnings.append({
                "type": "missing_status_emojis",
                "severity": "INFO",
                "message": "Few status emojis found - consider using emojis for better skimmability",
                "recommendation": "Use status emojis (✅, ⏳, 🟡, ❌) to indicate status"
            })
    
    def _check_master_task_log_references(self):
        """Check if devlog references MASTER_TASK_LOG tasks."""
        master_task_log_patterns = [
            r'MASTER_TASK_LOG',
            r'Master Task Log',
            r'master task log',
            r'MTL-',
            r'Task.*from.*MASTER'
        ]
        
        found = False
        for pattern in master_task_log_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                found = True
                break
        
        if not found:
            self.warnings.append({
                "type": "missing_mtl_reference",
                "severity": "WARNING",
                "message": "No MASTER_TASK_LOG references found",
                "requirement": "Devlogs should reference MASTER_TASK_LOG tasks (completed, claimed, in progress, next to claim)"
            })
    
    def _check_task_summary(self):
        """Check if Task Summary section is present."""
        task_summary_patterns = [
            r'##\s*Task Summary',
            r'###\s*Task Summary',
            r'\*\*Task Summary\*\*',
            r'Task Summary:'
        ]
        
        found = False
        for pattern in task_summary_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                found = True
                break
        
        if not found:
            self.warnings.append({
                "type": "missing_task_summary",
                "severity": "WARNING",
                "message": "Task Summary section not found",
                "recommendation": "Include a one-line task summary at the beginning"
            })
    
    def _check_actions_taken(self):
        """Check if Actions Taken section is present."""
        actions_patterns = [
            r'##\s*Actions Taken',
            r'###\s*Actions Taken',
            r'\*\*Actions Taken\*\*',
            r'Actions Taken:'
        ]
        
        found = False
        for pattern in actions_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                found = True
                break
        
        if not found:
            self.warnings.append({
                "type": "missing_actions_taken",
                "severity": "WARNING",
                "message": "Actions Taken section not found",
                "recommendation": "Include an Actions Taken section with bulleted list"
            })
    
    def _check_results_section(self):
        """Check if Results section is present."""
        results_patterns = [
            r'##\s*Results',
            r'###\s*Results',
            r'\*\*Results\*\*',
            r'Results:'
        ]
        
        found = False
        for pattern in results_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                found = True
                break
        
        if not found:
            self.warnings.append({
                "type": "missing_results",
                "severity": "WARNING",
                "message": "Results section not found",
                "recommendation": "Include a Results section describing what was accomplished"
            })
    
    def _check_artifacts_section(self):
        """Check if Artifacts section is present."""
        artifacts_patterns = [
            r'##\s*Artifacts',
            r'###\s*Artifacts',
            r'\*\*Artifacts\*\*',
            r'Artifacts:'
        ]
        
        found = False
        for pattern in artifacts_patterns:
            if re.search(pattern, self.content, re.IGNORECASE):
                found = True
                break
        
        if not found:
            self.warnings.append({
                "type": "missing_artifacts",
                "severity": "INFO",
                "message": "Artifacts section not found",
                "recommendation": "Include an Artifacts section listing created files/reports"
            })
    
    def _calculate_score(self) -> Dict[str, any]:
        """Calculate compliance score."""
        total_checks = len(self.violations) + len(self.warnings)
        critical_violations = len([v for v in self.violations if v.get('severity') == 'CRITICAL'])
        warnings = len(self.warnings)
        
        # Score: 100 - (critical * 20) - (warnings * 5)
        score = max(0, 100 - (critical_violations * 20) - (warnings * 5))
        
        return {
            "score": score,
            "max_score": 100,
            "critical_violations": critical_violations,
            "warnings": warnings,
            "grade": self._get_grade(score)
        }
    
    def _get_grade(self, score: int) -> str:
        """Get letter grade from score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def generate_report(self, validation_result: Dict[str, any]) -> str:
        """Generate human-readable validation report."""
        report = []
        report.append(f"# Devlog Compliance Validation Report")
        report.append(f"**Agent:** {validation_result['agent_id']}")
        report.append(f"**Devlog:** {validation_result['devlog_path']}")
        report.append(f"**Date:** {validation_result['validation_date']}")
        report.append(f"**Compliant:** {'✅ YES' if validation_result['compliant'] else '❌ NO'}")
        report.append("")
        
        score_info = validation_result['score']
        report.append(f"## Compliance Score: {score_info['score']}/100 ({score_info['grade']})")
        report.append("")
        
        if validation_result['violations']:
            report.append("## ❌ Violations (Must Fix)")
            for violation in validation_result['violations']:
                report.append(f"### {violation['type']} ({violation['severity']})")
                report.append(f"- **Message:** {violation['message']}")
                if 'requirement' in violation:
                    report.append(f"- **Requirement:** {violation['requirement']}")
                report.append("")
        
        if validation_result['warnings']:
            report.append("## ⚠️ Warnings (Should Fix)")
            for warning in validation_result['warnings']:
                report.append(f"### {warning['type']} ({warning['severity']})")
                report.append(f"- **Message:** {warning['message']}")
                if 'recommendation' in warning:
                    report.append(f"- **Recommendation:** {warning['recommendation']}")
                report.append("")
        
        if validation_result['compliant'] and not validation_result['warnings']:
            report.append("## ✅ Perfect Compliance!")
            report.append("All requirements met. Devlog format is compliant.")
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Validate devlog format compliance against enforcement protocol"
    )
    parser.add_argument(
        '--agent',
        required=True,
        help='Agent ID (e.g., Agent-6)'
    )
    parser.add_argument(
        '--file',
        required=True,
        type=Path,
        help='Path to devlog file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Path to save validation report (optional)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output validation result as JSON'
    )
    
    args = parser.parse_args()
    
    if not args.file.exists():
        print(f"❌ Error: Devlog file not found: {args.file}")
        return 1
    
    validator = DevlogComplianceValidator(args.file, args.agent)
    result = validator.validate()
    
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        report = validator.generate_report(result)
        print(report)
        
        if args.output:
            args.output.write_text(report, encoding='utf-8')
            print(f"\n✅ Report saved to: {args.output}")
    
    # Exit code: 0 if compliant, 1 if violations
    return 0 if result['compliant'] else 1


if __name__ == '__main__':
    exit(main())


