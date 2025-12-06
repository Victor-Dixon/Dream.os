#!/usr/bin/env python3
"""
Duplication Analyzer - Consolidated Analysis Tool
================================================

Consolidates duplicate file and code detection with consolidation recommendations.

Replaces:
- comprehensive_duplicate_analyzer.py
- duplication_analyzer.py (wrapper)
- duplication_analysis.py (code-level analysis)
- analyze_duplicate_code_consolidation.py (consolidation aspects)

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
SSOT Domain: analytics

<!-- SSOT Domain: analytics -->
"""

import ast
import difflib
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# SSOT Domain: analytics


class DuplicationAnalyzer:
    """Unified duplication analyzer for files and code."""

    def __init__(self, repo_root: Path = None):
        """Initialize analyzer."""
        self.repo_root = repo_root or Path.cwd()
        self.excluded_patterns = {
            '.git', 'node_modules', '__pycache__', '.venv', 'venv', 'env',
            '.env', 'data', 'archive', 'agent_workspaces', '.pytest_cache',
            'dist', 'build', '.mypy_cache', '.ruff_cache'
        }

    def is_excluded(self, file_path: Path) -> bool:
        """Check if file should be excluded."""
        return any(pattern in str(file_path) for pattern in self.excluded_patterns)

    def calculate_hash(self, file_path: Path) -> Optional[str]:
        """Calculate SHA256 hash of file."""
        try:
            return hashlib.sha256(file_path.read_bytes()).hexdigest()
        except Exception:
            return None

    def scan_file_duplicates(self) -> Tuple[Dict[str, List[Path]], Dict[str, List[Path]]]:
        """Scan repository for duplicate files."""
        files_by_hash: Dict[str, List[Path]] = defaultdict(list)
        files_by_name: Dict[str, List[Path]] = defaultdict(list)
        
        count = 0
        for file_path in self.repo_root.rglob("*"):
            if not file_path.is_file() or self.is_excluded(file_path):
                continue
            
            count += 1
            if count % 1000 == 0:
                print(f"   Scanned {count} files...")
            
            file_hash = self.calculate_hash(file_path)
            if file_hash:
                files_by_hash[file_hash].append(file_path)
            
            if file_path.suffix in ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md']:
                files_by_name[file_path.name].append(file_path)
        
        exact_duplicates = {h: paths for h, paths in files_by_hash.items() if len(paths) > 1}
        name_duplicates = {n: paths for n, paths in files_by_name.items() if len(paths) > 1}
        
        return exact_duplicates, name_duplicates

    def scan_code_duplicates(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Scan for duplicate code (functions/classes)."""
        functions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        classes: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        for file_path in self.repo_root.rglob("*.py"):
            if self.is_excluded(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                tree = ast.parse(content, filename=str(file_path))
                rel_path = str(file_path.relative_to(self.repo_root))
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        code = ast.get_source_segment(content, node)
                        if code:
                            code_hash = hashlib.sha256(code.encode()).hexdigest()
                            entry = {"name": node.name, "file": rel_path, "content": code[:300]}
                            (functions if isinstance(node, ast.FunctionDef) else classes)[code_hash].append(entry)
            except Exception:
                pass
        
        return {"functions": dict(functions), "classes": dict(classes)}

    def determine_ssot(self, paths: List[Path]) -> Path:
        """Determine single source of truth file."""
        for path in paths:
            rel = path.relative_to(self.repo_root)
            if str(rel).startswith('src/core/') or str(rel).startswith('src/services/'):
                return path
        return min(paths, key=lambda p: len(p.relative_to(self.repo_root).parts))

    def calculate_similarity(self, contents: List[str]) -> float:
        """Calculate average similarity between contents."""
        if len(contents) < 2:
            return 1.0
        
        similarities = []
        for i in range(len(contents)):
            for j in range(i + 1, len(contents)):
                similarity = difflib.SequenceMatcher(None, contents[i], contents[j]).ratio()
                similarities.append(similarity)
        
        return sum(similarities) / len(similarities) if similarities else 1.0

    def categorize_duplicates(
        self, exact_duplicates: Dict[str, List[Path]], name_duplicates: Dict[str, List[Path]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize duplicates for resolution."""
        cats = {'identical_safe_delete': [], 'same_name_different': [], 'needs_analysis': []}
        
        for hash_val, paths in exact_duplicates.items():
            ssot = self.determine_ssot(paths)
            cats['identical_safe_delete'].append({
                'ssot': str(ssot.relative_to(self.repo_root)),
                'duplicates': [str(p.relative_to(self.repo_root)) for p in paths if p != ssot],
                'count': len(paths)
            })
        
        for name, paths in name_duplicates.items():
            if name == '__init__.py':
                continue
            hashes = {self.calculate_hash(p): p for p in paths if self.calculate_hash(p)}
            cat_key = 'same_name_different' if len(hashes) == len(paths) else 'needs_analysis'
            cats[cat_key].append({
                'filename': name,
                'paths': [str(p.relative_to(self.repo_root)) for p in paths],
                'count': len(paths)
            })
        
        return cats

    def generate_consolidation_plan(
        self, categories: Dict[str, List[Dict[str, Any]]], code_duplicates: Dict[str, Dict[str, List[Dict[str, Any]]]]
    ) -> Dict[str, Any]:
        """Generate consolidation recommendations."""
        plan = {'safe_consolidations': [], 'code_consolidations': []}
        
        for g in categories['identical_safe_delete']:
            plan['safe_consolidations'].append({'ssot': g['ssot'], 'duplicates': g['duplicates'], 'action': 'DELETE', 'risk': 'LOW'})
        
        for func_hash, instances in code_duplicates.get('functions', {}).items():
            if len(instances) > 1:
                sim = self.calculate_similarity([inst['content'] for inst in instances])
                if sim > 0.9:
                    plan['code_consolidations'].append({'type': 'function', 'instances': instances, 'similarity': sim, 'action': 'EXTRACT_TO_UTILITY', 'risk': 'MEDIUM'})
        
        return plan

    def analyze(self) -> Dict[str, Any]:
        """Run comprehensive duplication analysis."""
        print("🔍 Scanning repository for duplicates...")
        
        exact_duplicates, name_duplicates = self.scan_file_duplicates()
        print(f"✅ Found {len(exact_duplicates)} identical file groups")
        print(f"✅ Found {len(name_duplicates)} same-name file groups")
        
        print("\n🔍 Scanning for code-level duplicates...")
        code_duplicates = self.scan_code_duplicates()
        func_dups = sum(1 for v in code_duplicates['functions'].values() if len(v) > 1)
        class_dups = sum(1 for v in code_duplicates['classes'].values() if len(v) > 1)
        print(f"✅ Found {func_dups} duplicate function groups")
        print(f"✅ Found {class_dups} duplicate class groups")
        
        print("\n🔍 Categorizing duplicates...")
        categories = self.categorize_duplicates(exact_duplicates, name_duplicates)
        
        print("\n🔍 Generating consolidation plan...")
        consolidation_plan = self.generate_consolidation_plan(categories, code_duplicates)
        
        return {
            "summary": {
                "exact_duplicate_groups": len(exact_duplicates),
                "same_name_groups": len(name_duplicates),
                "function_duplicate_groups": func_dups,
                "class_duplicate_groups": class_dups,
                "safe_consolidations": len(consolidation_plan['safe_consolidations']),
                "analysis_date": datetime.now().isoformat(),
            },
            "file_duplicates": {
                "exact": {h: [str(p.relative_to(self.repo_root)) for p in paths]
                         for h, paths in exact_duplicates.items()},
                "same_name": {n: [str(p.relative_to(self.repo_root)) for p in paths]
                            for n, paths in name_duplicates.items()},
            },
            "code_duplicates": code_duplicates,
            "categories": categories,
            "consolidation_plan": consolidation_plan,
        }

    def save_results(self, results: Dict[str, Any], output_path: Path):
        """Save analysis results to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to: {output_path}")

    def generate_report(self, results: Dict[str, Any], report_path: Path):
        """Generate markdown report."""
        report_path.parent.mkdir(parents=True, exist_ok=True)
        s = results["summary"]
        report = f"""# Duplication Analysis Report

**Generated**: {s['analysis_date']}  
**Exact Duplicate Groups**: {s['exact_duplicate_groups']}  
**Same-Name Groups**: {s['same_name_groups']}  
**Function Duplicates**: {s['function_duplicate_groups']}  
**Class Duplicates**: {s['class_duplicate_groups']}  
**Safe Consolidations**: {s['safe_consolidations']}

---

## 📊 File Duplicates - Identical Files (Safe Delete)
"""
        for i, g in enumerate(results["categories"]["identical_safe_delete"][:15], 1):
            report += f"\n### {i}. {g['count']} files - Keep: `{g['ssot']}` - Delete: {len(g['duplicates'])} files\n"
        
        if results["consolidation_plan"]["code_consolidations"]:
            report += "\n---\n\n## 🔄 Code Consolidation Opportunities\n"
            for i, c in enumerate(results["consolidation_plan"]["code_consolidations"][:5], 1):
                report += f"\n{i}. {c['type'].title()}: {c['similarity']:.1%} similarity - {c['action']} ({c['risk']} risk)\n"
        
        report += "\n---\n\n🐝 **WE. ARE. SWARM. ⚡🔥**\n"
        report_path.write_text(report, encoding="utf-8")
        print(f"✅ Report saved to: {report_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Duplication Analyzer")
    parser.add_argument("--output", type=Path,
                       default=Path("docs/technical_debt/DUPLICATION_ANALYSIS.json"),
                       help="Output JSON file path")
    parser.add_argument("--report", type=Path,
                       default=Path("docs/technical_debt/DUPLICATION_ANALYSIS_REPORT.md"),
                       help="Output markdown report path")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root")
    
    args = parser.parse_args()
    
    print("🔍 DUPLICATION ANALYZER")
    print("=" * 60)
    print()
    
    analyzer = DuplicationAnalyzer(repo_root=args.repo_root)
    results = analyzer.analyze()
    analyzer.save_results(results, args.output)
    analyzer.generate_report(results, args.report)
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Exact Duplicate Groups: {results['summary']['exact_duplicate_groups']}")
    print(f"Safe Consolidations: {results['summary']['safe_consolidations']}")
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()
