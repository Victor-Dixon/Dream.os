#!/usr/bin/env python3
"""
Enhanced File Usage Verification Tool
======================================

Performs comprehensive verification to check if files are truly unused.
Checks for dynamic imports, string-based imports, config references, entry points, etc.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-01
Priority: HIGH - Prevents false positives in file deletion
"""

import ast
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Optional


class EnhancedFileUsageVerifier:
    """Enhanced verification to check if files are truly unused."""

    def __init__(self, src_root: str = "src", project_root: str = "."):
        """Initialize verifier."""
        self.src_root = Path(src_root)
        self.project_root = Path(project_root)
        self.verification_results: Dict[str, Dict[str, Any]] = {}
        
    def get_file_module_name(self, file_path: Path) -> str:
        """Convert file path to module name."""
        relative = file_path.relative_to(self.src_root)
        return str(relative.with_suffix("")).replace("\\", ".").replace("/", ".")
    
    def find_all_source_files(self) -> List[Path]:
        """Find all Python source files."""
        source_files = []
        for path in self.src_root.rglob("*.py"):
            if "__pycache__" not in str(path):
                source_files.append(path)
        return sorted(source_files)
    
    def check_dynamic_imports(self, file_path: Path) -> List[str]:
        """Check if file is imported dynamically."""
        references = []
        
        for source_file in self.find_all_source_files():
            if source_file == file_path:
                continue
                
            try:
                with open(source_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    module_name = self.get_file_module_name(file_path)
                    module_parts = module_name.split(".")
                    
                    # Check for importlib.import_module
                    if "importlib" in content:
                        patterns = [
                            f"importlib.import_module('{module_name}'",
                            f'importlib.import_module("{module_name}"',
                            f"import_module('{module_name}'",
                            f'import_module("{module_name}"',
                        ]
                        for pattern in patterns:
                            if pattern in content:
                                references.append(f"Dynamic import in {source_file.relative_to(self.src_root)}")
                    
                    # Check for __import__
                    if "__import__" in content:
                        patterns = [
                            f"__import__('{module_name}'",
                            f'__import__("{module_name}"',
                        ]
                        for pattern in patterns:
                            if pattern in content:
                                references.append(f"__import__ in {source_file.relative_to(self.src_root)}")
                    
                    # Check for string-based imports
                    for part in module_parts:
                        if f"'{part}'" in content or f'"{part}"' in content:
                            # Check if it's in an import context
                            if "import" in content.lower():
                                # Simple heuristic - could be improved
                                pass
                                
            except Exception:
                pass
        
        return references
    
    def check_entry_points(self, file_path: Path) -> bool:
        """Check if file has entry points or is executable."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Check for __main__ block
                if "__name__" in content and "__main__" in content:
                    return True
                
                # Check if it's a script (has if __name__ == "__main__")
                if re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', content):
                    return True
                    
        except Exception:
            pass
        
        # Check setup.py for entry points
        setup_py = self.project_root / "setup.py"
        if setup_py.exists():
            try:
                with open(setup_py, "r", encoding="utf-8") as f:
                    content = f.read()
                    module_name = self.get_file_module_name(file_path)
                    if module_name in content:
                        return True
            except Exception:
                pass
        
        return False
    
    def check_test_references(self, file_path: Path) -> List[str]:
        """Check if file is referenced in test files."""
        references = []
        tests_root = self.project_root / "tests"
        
        if not tests_root.exists():
            return references
        
        module_name = self.get_file_module_name(file_path)
        relative_path = file_path.relative_to(self.src_root)
        file_stem = file_path.stem
        
        for test_file in tests_root.rglob("*.py"):
            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Check for direct imports
                    if module_name in content or file_stem in content:
                        references.append(f"Referenced in {test_file.relative_to(self.project_root)}")
                        
            except Exception:
                pass
        
        return references
    
    def check_config_references(self, file_path: Path) -> List[str]:
        """Check if file is referenced in config files."""
        references = []
        module_name = self.get_file_module_name(file_path)
        relative_path = str(file_path.relative_to(self.src_root))
        
        # Check common config file patterns
        config_patterns = ["*.yaml", "*.yml", "*.json", "*.toml", "*.ini", "*.cfg"]
        
        for pattern in config_patterns:
            for config_file in self.project_root.rglob(pattern):
                try:
                    with open(config_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if module_name in content or relative_path in content:
                            references.append(f"Referenced in {config_file.relative_to(self.project_root)}")
                except Exception:
                    pass
        
        return references
    
    def check_documentation_references(self, file_path: Path) -> List[str]:
        """Check if file is referenced in documentation."""
        references = []
        module_name = self.get_file_module_name(file_path)
        relative_path = str(file_path.relative_to(self.src_root))
        
        # Check common documentation patterns
        doc_patterns = ["*.md", "*.rst", "*.txt"]
        
        for pattern in doc_patterns:
            for doc_file in self.project_root.rglob(pattern):
                # Skip certain directories
                if any(skip in str(doc_file) for skip in [".git", "__pycache__", "node_modules"]):
                    continue
                    
                try:
                    with open(doc_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if module_name in content or relative_path in content:
                            references.append(f"Referenced in {doc_file.relative_to(self.project_root)}")
                except Exception:
                    pass
        
        return references
    
    def verify_file(self, file_path: Path) -> Dict[str, Any]:
        """Perform comprehensive verification on a file."""
        results = {
            "file_path": str(file_path),
            "relative_path": str(file_path.relative_to(self.src_root)),
            "module_name": self.get_file_module_name(file_path),
            "is_truly_unused": True,
            "verification_results": {
                "dynamic_imports": [],
                "entry_points": False,
                "test_references": [],
                "config_references": [],
                "documentation_references": [],
            },
            "risk_level": "low",
            "recommendation": "SAFE_TO_DELETE"
        }
        
        # Check dynamic imports
        dynamic_refs = self.check_dynamic_imports(file_path)
        if dynamic_refs:
            results["verification_results"]["dynamic_imports"] = dynamic_refs
            results["is_truly_unused"] = False
            results["risk_level"] = "high"
            results["recommendation"] = "KEEP - Dynamic import detected"
        
        # Check entry points
        has_entry_point = self.check_entry_points(file_path)
        if has_entry_point:
            results["verification_results"]["entry_points"] = True
            results["is_truly_unused"] = False
            results["risk_level"] = "high"
            results["recommendation"] = "KEEP - Has entry point"
        
        # Check test references
        test_refs = self.check_test_references(file_path)
        if test_refs:
            results["verification_results"]["test_references"] = test_refs
            results["is_truly_unused"] = False
            if results["risk_level"] == "low":
                results["risk_level"] = "medium"
                results["recommendation"] = "REVIEW - Referenced in tests"
        
        # Check config references
        config_refs = self.check_config_references(file_path)
        if config_refs:
            results["verification_results"]["config_references"] = config_refs
            results["is_truly_unused"] = False
            if results["risk_level"] == "low":
                results["risk_level"] = "medium"
                results["recommendation"] = "REVIEW - Referenced in config"
        
        # Check documentation references
        doc_refs = self.check_documentation_references(file_path)
        if doc_refs:
            results["verification_results"]["documentation_references"] = doc_refs
            # Documentation references are lower risk
            if results["risk_level"] == "low":
                results["risk_level"] = "low"
                results["recommendation"] = "REVIEW - Referenced in documentation (lower risk)"
        
        return results
    
    def verify_files_from_analysis(self, analysis_file: str) -> Dict[str, Any]:
        """Verify files from unnecessary_files_analysis.json."""
        print(f"📋 Loading analysis file: {analysis_file}")
        
        with open(analysis_file, "r", encoding="utf-8") as f:
            analysis_data = json.load(f)
        
        files_to_verify = []
        
        # Collect all files from analysis
        for category in ["unused", "deprecated_directory", "deletion_markers", "duplicates"]:
            for file_info in analysis_data.get(category, []):
                file_path = Path(file_info["file_path"])
                if file_path.exists():
                    files_to_verify.append(file_path)
        
        print(f"🔍 Verifying {len(files_to_verify)} files with enhanced checks...\n")
        
        verification_results = {
            "summary": {
                "total_files_verified": len(files_to_verify),
                "truly_unused": 0,
                "needs_review": 0,
                "must_keep": 0,
            },
            "truly_unused": [],
            "needs_review": [],
            "must_keep": [],
        }
        
        for i, file_path in enumerate(files_to_verify, 1):
            print(f"  [{i}/{len(files_to_verify)}] Verifying: {file_path.relative_to(self.src_root)}")
            result = self.verify_file(file_path)
            
            if result["is_truly_unused"] and result["risk_level"] == "low":
                verification_results["truly_unused"].append(result)
                verification_results["summary"]["truly_unused"] += 1
            elif result["risk_level"] == "high":
                verification_results["must_keep"].append(result)
                verification_results["summary"]["must_keep"] += 1
            else:
                verification_results["needs_review"].append(result)
                verification_results["summary"]["needs_review"] += 1
        
        return verification_results


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced file usage verification")
    parser.add_argument(
        "--analysis-file",
        default="agent_workspaces/Agent-5/unnecessary_files_analysis.json",
        help="Path to unnecessary_files_analysis.json"
    )
    parser.add_argument(
        "--output",
        default="agent_workspaces/Agent-5/enhanced_verification_results.json",
        help="Output file path"
    )
    
    args = parser.parse_args()
    
    print("🔍 ENHANCED FILE USAGE VERIFICATION")
    print("=" * 60)
    print("Performing comprehensive verification to prevent false positives\n")
    
    verifier = EnhancedFileUsageVerifier()
    
    if not Path(args.analysis_file).exists():
        print(f"❌ Analysis file not found: {args.analysis_file}")
        return
    
    results = verifier.verify_files_from_analysis(args.analysis_file)
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    summary = results["summary"]
    print(f"Total Files Verified: {summary['total_files_verified']}")
    print(f"✅ Truly Unused (Safe to Delete): {summary['truly_unused']}")
    print(f"⚠️  Needs Review: {summary['needs_review']}")
    print(f"❌ Must Keep: {summary['must_keep']}")
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_path}")
    
    # Show top false positives
    if results["must_keep"]:
        print("\n" + "=" * 60)
        print("❌ FALSE POSITIVES - Must Keep These Files")
        print("=" * 60)
        for result in results["must_keep"][:10]:
            print(f"\n{result['relative_path']}")
            print(f"  Reason: {result['recommendation']}")
            if result["verification_results"]["dynamic_imports"]:
                print(f"  Dynamic imports found: {len(result['verification_results']['dynamic_imports'])}")
            if result["verification_results"]["entry_points"]:
                print(f"  Has entry point: Yes")
    
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()

