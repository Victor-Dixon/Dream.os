#!/usr/bin/env python3
"""
Phase -1: Signal vs Noise Classification Tool
Analyzes all tools in the repository and classifies them as SIGNAL (real infrastructure) or NOISE (thin wrappers).

Based on criteria from: agent_workspaces/Agent-1/TOOLBELT_SIGNAL_VS_NOISE_ANALYSIS.md
"""

import ast
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import re

# Classification criteria
SIGNAL_INDICATORS = [
    "business logic",
    "ast.parse",
    "ast.walk",
    "class ",
    "def ",
    "algorithm",
    "parsing",
    "analysis",
    "validation",
    "orchestration",
    "coordination",
    "infrastructure",
    "reusable",
    "utility",
    "helper",
    "validator",
    "analyzer",
    "orchestrator",
    "coordinator",
]

NOISE_INDICATORS = [
    "argparse",
    "sys.argv",
    "wrapper",
    "cli wrapper",
    "just calls",
    "convenience",
    "one-off",
    "sys.exit",
    "if __name__ == '__main__'",
]

MIN_LINES_FOR_SIGNAL = 50  # Very small files are more likely to be wrappers
MAX_IMPORT_RATIO = 0.3  # If >30% of file is imports, might be a wrapper


class ToolClassifier:
    """Classifies tools as SIGNAL (real infrastructure) or NOISE (thin wrappers)."""
    
    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.classifications: Dict[str, Dict] = {}
        self.stats = {
            'total': 0,
            'signal': 0,
            'noise': 0,
            'needs_review': 0,
        }
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single tool file and return classification data."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                total_lines = len([l for l in lines if l.strip()])
                
                if total_lines == 0:
                    return {'classification': 'NOISE', 'reason': 'Empty file'}
                
                # Parse AST to detect structure
                try:
                    tree = ast.parse(content)
                    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
                except SyntaxError:
                    return {
                        'classification': 'NEEDS_REVIEW',
                        'reason': 'Syntax error - cannot parse',
                        'total_lines': total_lines
                    }
                
                # Count imports vs code
                import_lines = sum(len(str(imp).split('\n')) for imp in imports)
                code_lines = total_lines - import_lines
                import_ratio = import_lines / total_lines if total_lines > 0 else 0
                
                # Detect patterns
                has_argparse = 'argparse' in content or 'ArgumentParser' in content
                has_main_guard = 'if __name__' in content
                has_wrapper_pattern = self._detect_wrapper_pattern(content, functions)
                has_business_logic = self._detect_business_logic(content, functions, classes)
                has_reusable_architecture = len(classes) > 0 or len(functions) > 5
                
                # Classification heuristics
                classification = 'NEEDS_REVIEW'
                reasons = []
                confidence = 'MEDIUM'
                
                # Strong NOISE indicators
                if has_wrapper_pattern and total_lines < MIN_LINES_FOR_SIGNAL:
                    classification = 'NOISE'
                    reasons.append(f'Wrapper pattern detected, small file ({total_lines} lines)')
                    confidence = 'HIGH'
                elif has_argparse and total_lines < MIN_LINES_FOR_SIGNAL and not has_business_logic:
                    classification = 'NOISE'
                    reasons.append(f'CLI wrapper pattern, small file ({total_lines} lines), no business logic')
                    confidence = 'HIGH'
                elif import_ratio > MAX_IMPORT_RATIO and total_lines < MIN_LINES_FOR_SIGNAL:
                    classification = 'NOISE'
                    reasons.append(f'High import ratio ({import_ratio:.1%}), small file ({total_lines} lines)')
                    confidence = 'MEDIUM'
                
                # Strong SIGNAL indicators
                elif has_business_logic and has_reusable_architecture:
                    classification = 'SIGNAL'
                    reasons.append(f'Business logic detected, reusable architecture ({len(classes)} classes, {len(functions)} functions)')
                    confidence = 'HIGH'
                elif total_lines > 200 and has_reusable_architecture:
                    classification = 'SIGNAL'
                    reasons.append(f'Large file ({total_lines} lines) with reusable architecture')
                    confidence = 'HIGH'
                elif len(functions) > 10 or len(classes) > 2:
                    classification = 'SIGNAL'
                    reasons.append(f'Complex structure ({len(functions)} functions, {len(classes)} classes)')
                    confidence = 'HIGH'
                
                # Medium confidence classifications
                elif has_business_logic and total_lines > MIN_LINES_FOR_SIGNAL:
                    classification = 'SIGNAL'
                    reasons.append(f'Business logic detected, reasonable size ({total_lines} lines)')
                    confidence = 'MEDIUM'
                elif has_reusable_architecture and total_lines > MIN_LINES_FOR_SIGNAL:
                    classification = 'SIGNAL'
                    reasons.append(f'Reusable architecture, reasonable size ({total_lines} lines)')
                    confidence = 'MEDIUM'
                
                # Needs manual review
                else:
                    classification = 'NEEDS_REVIEW'
                    reasons.append(f'Ambiguous - {total_lines} lines, {len(functions)} functions, {len(classes)} classes')
                    confidence = 'LOW'
                
                return {
                    'classification': classification,
                    'confidence': confidence,
                    'reason': '; '.join(reasons),
                    'total_lines': total_lines,
                    'code_lines': code_lines,
                    'import_lines': import_lines,
                    'import_ratio': import_ratio,
                    'num_functions': len(functions),
                    'num_classes': len(classes),
                    'has_argparse': has_argparse,
                    'has_main_guard': has_main_guard,
                    'has_wrapper_pattern': has_wrapper_pattern,
                    'has_business_logic': has_business_logic,
                    'has_reusable_architecture': has_reusable_architecture,
                }
                
        except Exception as e:
            return {
                'classification': 'NEEDS_REVIEW',
                'reason': f'Error analyzing file: {str(e)}',
                'error': str(e)
            }
    
    def _detect_wrapper_pattern(self, content: str, functions: List) -> bool:
        """Detect if file is a thin wrapper around another tool."""
        wrapper_patterns = [
            r'def main\(\):.*?if __name__',
            r'sys\.argv',
            r'ArgumentParser\(\)',
            r'just calls',
            r'wrapper around',
            r'convenience',
        ]
        
        # Check if main function just calls another function
        if len(functions) <= 2:
            for pattern in wrapper_patterns:
                if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                    return True
        
        return False
    
    def _detect_business_logic(self, content: str, functions: List, classes: List) -> bool:
        """Detect if file contains real business logic."""
        logic_indicators = [
            r'ast\.',
            r'parsing',
            r'analysis',
            r'validation',
            r'algorithm',
            r'calculat',
            r'process',
            r'transform',
            r'extract',
            r'generate',
            r'orchestrat',
            r'coordinat',
        ]
        
        # Check content for logic indicators
        content_lower = content.lower()
        for indicator in logic_indicators:
            if re.search(indicator, content_lower):
                return True
        
        # Check function/class names
        if len(functions) > 3 or len(classes) > 0:
            return True
        
        return False
    
    def classify_all(self) -> Dict:
        """Classify all Python files in tools directory."""
        tool_files = list(self.tools_dir.rglob('*.py'))
        
        # Exclude __init__.py and __pycache__
        tool_files = [
            f for f in tool_files 
            if not f.name.startswith('__') and '__pycache__' not in str(f)
        ]
        
        self.stats['total'] = len(tool_files)
        
        for file_path in sorted(tool_files):
            relative_path = file_path.relative_to(self.tools_dir)
            analysis = self.analyze_file(file_path)
            
            classification = analysis.get('classification', 'NEEDS_REVIEW')
            self.classifications[str(relative_path)] = {
                'file_path': str(relative_path),
                'absolute_path': str(file_path),
                **analysis
            }
            
            if classification == 'SIGNAL':
                self.stats['signal'] += 1
            elif classification == 'NOISE':
                self.stats['noise'] += 1
            else:
                self.stats['needs_review'] += 1
        
        return {
            'stats': self.stats,
            'classifications': self.classifications
        }
    
    def generate_report(self, output_file: Path):
        """Generate a classification report."""
        results = self.classify_all()
        
        # Group by classification
        signal_tools = []
        noise_tools = []
        needs_review_tools = []
        
        for file_path, data in results['classifications'].items():
            classification = data['classification']
            entry = {
                'file': file_path,
                'lines': data.get('total_lines', 0),
                'functions': data.get('num_functions', 0),
                'classes': data.get('num_classes', 0),
                'reason': data.get('reason', ''),
                'confidence': data.get('confidence', 'MEDIUM'),
            }
            
            if classification == 'SIGNAL':
                signal_tools.append(entry)
            elif classification == 'NOISE':
                noise_tools.append(entry)
            else:
                needs_review_tools.append(entry)
        
        # Generate markdown report
        report_lines = [
            "# Tool Classification Report - Signal vs Noise Analysis",
            "",
            f"**Date**: {Path(__file__).stat().st_mtime}",
            f"**Total Tools Analyzed**: {results['stats']['total']}",
            "",
            "## Summary Statistics",
            "",
            f"- **SIGNAL Tools** (Real Infrastructure): {results['stats']['signal']} ({results['stats']['signal']/results['stats']['total']*100:.1f}%)",
            f"- **NOISE Tools** (Thin Wrappers): {results['stats']['noise']} ({results['stats']['noise']/results['stats']['total']*100:.1f}%)",
            f"- **Needs Review**: {results['stats']['needs_review']} ({results['stats']['needs_review']/results['stats']['total']*100:.1f}%)",
            "",
            "## Classification Criteria",
            "",
            "### ✅ SIGNAL Tools (Real Infrastructure)",
            "- Contains real business logic",
            "- Reusable infrastructure",
            "- Modular architecture (classes, multiple functions)",
            "- Significant code (>50 lines typically)",
            "",
            "### ❌ NOISE Tools (Thin Wrappers)",
            "- CLI wrappers around existing functionality",
            "- No real business logic",
            "- Small files (<50 lines typically)",
            "- High import-to-code ratio",
            "",
            "## SIGNAL Tools",
            "",
            "| File | Lines | Functions | Classes | Confidence | Reason |",
            "|------|-------|-----------|---------|------------|--------|",
        ]
        
        for tool in sorted(signal_tools, key=lambda x: x['lines'], reverse=True):
            report_lines.append(
                f"| {tool['file']} | {tool['lines']} | {tool['functions']} | {tool['classes']} | {tool['confidence']} | {tool['reason'][:80]}... |"
            )
        
        report_lines.extend([
            "",
            "## NOISE Tools",
            "",
            "| File | Lines | Functions | Classes | Confidence | Reason |",
            "|------|-------|-----------|---------|------------|--------|",
        ])
        
        for tool in sorted(noise_tools, key=lambda x: x['lines']):
            report_lines.append(
                f"| {tool['file']} | {tool['lines']} | {tool['functions']} | {tool['classes']} | {tool['confidence']} | {tool['reason'][:80]}... |"
            )
        
        report_lines.extend([
            "",
            "## Needs Review",
            "",
            "| File | Lines | Functions | Classes | Confidence | Reason |",
            "|------|-------|-----------|---------|------------|--------|",
        ])
        
        for tool in sorted(needs_review_tools, key=lambda x: x['lines']):
            report_lines.append(
                f"| {tool['file']} | {tool['lines']} | {tool['functions']} | {tool['classes']} | {tool['confidence']} | {tool['reason'][:80]}... |"
            )
        
        report_lines.extend([
            "",
            "## Next Steps",
            "",
            "1. Review NEEDS_REVIEW tools manually",
            "2. Validate HIGH confidence classifications",
            "3. Move NOISE tools to scripts/ directory",
            "4. Update toolbelt registry (remove NOISE tools)",
            "5. Proceed with V2 refactoring on SIGNAL tools only",
            "",
        ])
        
        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        # Also write JSON for programmatic access
        json_file = output_file.with_suffix('.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Classification complete!")
        print(f"   - SIGNAL: {results['stats']['signal']} tools")
        print(f"   - NOISE: {results['stats']['noise']} tools")
        print(f"   - Needs Review: {results['stats']['needs_review']} tools")
        print(f"   - Report: {output_file}")
        print(f"   - JSON: {json_file}")
        
        return output_file


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent
    tools_dir = repo_root / 'tools'
    output_file = repo_root / 'docs' / 'toolbelt' / 'TOOL_CLASSIFICATION.md'
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    classifier = ToolClassifier(tools_dir)
    classifier.generate_report(output_file)


if __name__ == '__main__':
    main()

