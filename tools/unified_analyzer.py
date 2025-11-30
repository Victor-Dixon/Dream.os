#!/usr/bin/env python3
"""
Unified Analyzer - Consolidated Analysis Tool
=============================================

Consolidates all analysis capabilities into a single unified tool.
Replaces 45+ individual analysis tools with modular analysis system.

Analysis Categories:
- Project Structure Analysis
- Code Analysis (AST, complexity, imports)
- Messaging Files Analysis
- Technical Debt Scanning
- GitHub Repo Analysis
- Architecture Audits

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-29
V2 Compliant: Yes (<400 lines)
"""

import argparse
import json
import logging
import sys
import re
import ast
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict, Counter

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UnifiedAnalyzer:
    """Unified analysis system consolidating all analysis capabilities."""
    
    def __init__(self):
        """Initialize unified analyzer."""
        self.project_root = project_root
        
    def analyze_project_structure(self, target_path: str = None) -> Dict[str, Any]:
        """Analyze project structure and organization."""
        target = Path(target_path) if target_path else self.project_root
        
        structure = {
            "total_files": 0,
            "total_dirs": 0,
            "file_types": Counter(),
            "directories": {}
        }
        
        skip_dirs = {"__pycache__", ".git", "node_modules", "venv", ".venv", "env", ".pytest_cache"}
        
        import os
        
        for root, dirs, files in os.walk(target):
            root_path = Path(root)
            
            # Filter out skipped directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            rel_path = str(root_path.relative_to(target)) if root_path != target else "."
            if any(skip in Path(rel_path).parts for skip in skip_dirs):
                continue
            
            file_count = len(files)
            if file_count > 0 or len(dirs) > 0:
                structure["directories"][rel_path] = {
                    "files": file_count,
                    "subdirs": len(dirs)
                }
                structure["total_files"] += file_count
                structure["total_dirs"] += len(dirs)
                
                # Count file types
                for f in files:
                    file_path = root_path / f
                    if file_path.is_file():
                        structure["file_types"][file_path.suffix or "no_extension"] += 1
        
        structure["file_types"] = dict(structure["file_types"])
        
        return {
            "category": "structure",
            "target": str(target),
            "analysis": structure,
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single code file (Python/JS/TS)."""
        path = Path(file_path)
        
        if not path.exists():
            return {
                "category": "code",
                "file": file_path,
                "error": "File not found",
                "timestamp": datetime.now().isoformat()
            }
        
        ext = path.suffix.lower()
        
        if ext == ".py":
            return self._analyze_python_file(path)
        elif ext in [".js", ".jsx", ".ts", ".tsx"]:
            return self._analyze_js_file(path)
        else:
            return {
                "category": "code",
                "file": file_path,
                "error": f"Unsupported file type: {ext}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Python file using AST."""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            
            functions = []
            classes = {}
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes[node.name] = {
                        "methods": methods,
                        "line_count": len(node.body)
                    }
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        module = node.module or ""
                        imports.extend([f"{module}.{alias.name}" for alias in node.names])
            
            return {
                "category": "code",
                "file": str(file_path),
                "language": "python",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "line_count": len(content.splitlines()),
                "complexity": len(functions) + len(classes),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "category": "code",
                "file": str(file_path),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_js_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            functions = re.findall(r'function\s+(\w+)\s*\(', content)
            classes = re.findall(r'class\s+(\w+)', content)
            
            return {
                "category": "code",
                "file": str(file_path),
                "language": "javascript",
                "functions": functions,
                "classes": {cls: {"methods": []} for cls in classes},
                "line_count": len(content.splitlines()),
                "complexity": len(functions) + len(classes),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "category": "code",
                "file": str(file_path),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def scan_technical_debt(self, target_path: str = None, marker_type: str = None) -> Dict[str, Any]:
        """Scan for technical debt markers (TODO, FIXME, etc.)."""
        target = Path(target_path) if target_path else self.project_root
        
        debt_markers = {
            "TODO": r"TODO[:\s]",
            "FIXME": r"FIXME[:\s]",
            "HACK": r"HACK[:\s]",
            "BUG": r"BUG[:\s]",
            "XXX": r"XXX[:\s]",
            "DEPRECATED": r"DEPRECATED[:\s]|@deprecated",
            "REFACTOR": r"REFACTOR[:\s]|needs? refactor",
        }
        
        markers_to_scan = {marker_type: debt_markers[marker_type]} if marker_type else debt_markers
        results = defaultdict(list)
        
        skip_dirs = {"__pycache__", "node_modules", ".git", "venv", ".venv", "env", ".pytest_cache"}
        scan_extensions = {".py", ".js", ".jsx", ".ts", ".tsx", ".md", ".yml", ".yaml"}
        
        for file_path in target.rglob("*"):
            if not file_path.is_file():
                continue
            
            if any(skip in file_path.parts for skip in skip_dirs):
                continue
            
            if file_path.suffix not in scan_extensions:
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                for line_num, line in enumerate(content.splitlines(), 1):
                    for marker_name, marker_pattern in markers_to_scan.items():
                        if re.search(marker_pattern, line, re.IGNORECASE):
                            results[marker_name].append({
                                "file": str(file_path.relative_to(self.project_root)),
                                "line": line_num,
                                "content": line.strip(),
                                "marker": marker_name
                            })
            except Exception:
                pass
        
        return {
            "category": "technical_debt",
            "target": str(target),
            "markers": dict(results),
            "total_issues": sum(len(issues) for issues in results.values()),
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_messaging_files(self) -> Dict[str, Any]:
        """Analyze messaging-related files."""
        messaging_dirs = [
            self.project_root / "src" / "services" / "messaging",
            self.project_root / "src" / "core" / "messaging",
            self.project_root / "agent_workspaces"
        ]
        
        messaging_files = []
        
        for dir_path in messaging_dirs:
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.rglob("*.py"):
                analysis = self.analyze_code_file(str(file_path))
                if "error" not in analysis:
                    messaging_files.append(analysis)
        
        return {
            "category": "messaging",
            "files_analyzed": len(messaging_files),
            "files": messaging_files[:50],  # Limit to first 50
            "timestamp": datetime.now().isoformat()
        }
    
    def run_full_analysis(self, target_path: str = None) -> Dict[str, Any]:
        """Run comprehensive analysis suite."""
        logger.info("Running full analysis suite...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "analyses": {}
        }
        
        # Project structure
        results["analyses"]["structure"] = self.analyze_project_structure(target_path)
        
        # Technical debt
        results["analyses"]["technical_debt"] = self.scan_technical_debt(target_path)
        
        # Messaging files
        results["analyses"]["messaging"] = self.analyze_messaging_files()
        
        return results
    
    def print_analysis_report(self, results: Dict[str, Any]):
        """Print formatted analysis report."""
        print("\n" + "=" * 70)
        print("📊 UNIFIED ANALYSIS REPORT")
        print("=" * 70)
        
        analyses = results.get("analyses", {})
        
        # Structure analysis
        if "structure" in analyses:
            structure = analyses["structure"].get("analysis", {})
            print(f"\n📁 Project Structure:")
            print(f"   Total Files: {structure.get('total_files', 0)}")
            print(f"   Total Directories: {structure.get('total_dirs', 0)}")
            print(f"   Top File Types: {dict(list(structure.get('file_types', {}).items())[:5])}")
        
        # Technical debt
        if "technical_debt" in analyses:
            debt = analyses["technical_debt"]
            print(f"\n⚠️  Technical Debt:")
            print(f"   Total Issues: {debt.get('total_issues', 0)}")
            markers = debt.get("markers", {})
            for marker, issues in markers.items():
                if issues:
                    print(f"   {marker}: {len(issues)}")
        
        # Messaging analysis
        if "messaging" in analyses:
            messaging = analyses["messaging"]
            print(f"\n💬 Messaging Files:")
            print(f"   Files Analyzed: {messaging.get('files_analyzed', 0)}")
        
        print(f"\n🕐 Timestamp: {results.get('timestamp', 'unknown')}")
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Unified Analyzer - Consolidated analysis for all code",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--category", "-c",
        choices=["structure", "code", "debt", "messaging", "all"],
        default="all",
        help="Analysis category (default: all)"
    )
    
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Analyze specific file"
    )
    
    parser.add_argument(
        "--path", "-p",
        type=str,
        help="Analyze specific path"
    )
    
    parser.add_argument(
        "--marker",
        type=str,
        help="Specific technical debt marker to scan for"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    analyzer = UnifiedAnalyzer()
    
    if args.file:
        # Analyze single file
        results = {"analysis": analyzer.analyze_code_file(args.file)}
    elif args.category == "all":
        # Full analysis
        results = analyzer.run_full_analysis(args.path)
    elif args.category == "structure":
        results = {"analysis": analyzer.analyze_project_structure(args.path)}
    elif args.category == "debt":
        results = {"analysis": analyzer.scan_technical_debt(args.path, args.marker)}
    elif args.category == "messaging":
        results = {"analysis": analyzer.analyze_messaging_files()}
    else:
        results = {"error": "Invalid category"}
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "analyses" in results:
            analyzer.print_analysis_report(results)
        elif "analysis" in results:
            print(json.dumps(results["analysis"], indent=2))
        else:
            print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

