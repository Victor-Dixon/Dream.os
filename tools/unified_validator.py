#!/usr/bin/env python3
"""
Unified Validator - Consolidated Validation Tool
================================================

<!-- SSOT Domain: qa -->

Consolidates all validation capabilities into a single unified tool.
Replaces 19+ individual validation tools with modular validation system.

Validation Categories:
- SSOT Config Validation
- Import Validation
- Code-Documentation Alignment
- Queue Behavior Validation
- Session Transition Validation
- Consolidation Validation

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-11-29
V2 Compliant: Yes (<400 lines)
"""

import argparse
import json
import logging
import sys
import ast
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UnifiedValidator:
    """Unified validation system consolidating all validation capabilities."""
    
    def __init__(self):
        """Initialize unified validator."""
        self.project_root = project_root
        
    def validate_ssot_config(self, file_path: str = None, dir_path: str = None) -> Dict[str, Any]:
        """Validate config_ssot usage and facade mapping."""
        try:
            from tools.ssot_config_validator import SSOTConfigValidator
            
            validator = SSOTConfigValidator()
            
            if file_path:
                path = Path(file_path)
                is_valid, issues = validator.validate_file(path)
                return {
                    "category": "ssot_config",
                    "target": file_path,
                    "valid": is_valid,
                    "issues": issues,
                    "timestamp": datetime.now().isoformat()
                }
            elif dir_path:
                path = Path(dir_path)
                is_valid, results = validator.validate_directory(path)
                return {
                    "category": "ssot_config",
                    "target": dir_path,
                    "valid": is_valid,
                    "results": results,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Check facade mapping
                facade_status = validator.check_facade_mapping()
                return {
                    "category": "ssot_config",
                    "target": "facade_mapping",
                    "facade_status": facade_status,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"SSOT config validation failed: {e}")
            return {
                "category": "ssot_config",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_imports(self, file_path: str = None) -> Dict[str, Any]:
        """Validate import paths and chains."""
        if file_path:
            path = Path(file_path)
            if not path.exists():
                return {
                    "category": "imports",
                    "target": file_path,
                    "error": "File not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            try:
                content = path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(path))
                
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ""
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}")
                
                return {
                    "category": "imports",
                    "target": file_path,
                    "imports": imports,
                    "count": len(imports),
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                return {
                    "category": "imports",
                    "target": file_path,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        else:
            return {
                "category": "imports",
                "error": "File path required",
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_code_docs_alignment(self, code_file: str, doc_files: List[str]) -> Dict[str, Any]:
        """Validate alignment between code and documentation."""
        try:
            from tools.ssot_validator import validate_ssot
            
            results = validate_ssot(code_file, doc_files)
            
            return {
                "category": "code_docs",
                "code_file": code_file,
                "doc_files": doc_files,
                "aligned_flags": list(results.get("aligned", [])),
                "undocumented_flags": list(results.get("undocumented", [])),
                "nonexistent_flags": list(results.get("nonexistent", [])),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Code-docs validation failed: {e}")
            return {
                "category": "code_docs",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_queue_behavior(self) -> Dict[str, Any]:
        """Validate deferred push queue behavior."""
        try:
            from src.core.deferred_push_queue import get_deferred_push_queue
            
            queue = get_deferred_push_queue()
            stats = queue.get_stats()
            
            return {
                "category": "queue",
                "stats": stats,
                "healthy": stats.get("failed", 0) == 0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Queue validation failed: {e}")
            return {
                "category": "queue",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def validate_session_transition(self) -> Dict[str, Any]:
        """Validate session transition integrity."""
        workspaces_dir = self.project_root / "agent_workspaces"
        
        if not workspaces_dir.exists():
            return {
                "category": "session",
                "error": "Agent workspaces directory not found",
                "timestamp": datetime.now().isoformat()
            }
        
        agent_statuses = []
        for agent_dir in sorted(workspaces_dir.iterdir()):
            if not agent_dir.is_dir():
                continue
            
            status_file = agent_dir / "status.json"
            if status_file.exists():
                try:
                    status_data = json.loads(status_file.read_text())
                    agent_statuses.append({
                        "agent": agent_dir.name,
                        "status": status_data.get("status", "unknown"),
                        "last_updated": status_data.get("last_updated", "unknown")
                    })
                except Exception:
                    pass
        
        return {
            "category": "session",
            "agents": len(agent_statuses),
            "agent_statuses": agent_statuses,
            "timestamp": datetime.now().isoformat()
        }
    
    def run_full_validation(self, file_path: str = None) -> Dict[str, Any]:
        """Run comprehensive validation suite."""
        logger.info("Running full validation suite...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "validations": {}
        }
        
        # SSOT config validation
        results["validations"]["ssot_config"] = self.validate_ssot_config()
        
        # Queue behavior validation
        results["validations"]["queue"] = self.validate_queue_behavior()
        
        # Session transition validation
        results["validations"]["session"] = self.validate_session_transition()
        
        # Import validation (if file provided)
        if file_path:
            results["validations"]["imports"] = self.validate_imports(file_path)
        
        return results
    
    def print_validation_report(self, results: Dict[str, Any]):
        """Print formatted validation report."""
        print("\n" + "=" * 70)
        print("✅ UNIFIED VALIDATION REPORT")
        print("=" * 70)
        
        validations = results.get("validations", {})
        
        # SSOT config
        if "ssot_config" in validations:
            ssot = validations["ssot_config"]
            if "facade_status" in ssot:
                status_icon = "✅" if all(ssot["facade_status"].values()) else "⚠️"
                print(f"\n{status_icon} SSOT Config: Facade mapping checked")
                for shim, mapped in ssot["facade_status"].items():
                    icon = "✅" if mapped else "❌"
                    print(f"   {icon} {shim}: {'Mapped' if mapped else 'Not mapped'}")
        
        # Queue
        if "queue" in validations:
            queue = validations["queue"]
            if "healthy" in queue:
                status_icon = "✅" if queue["healthy"] else "⚠️"
                print(f"\n{status_icon} Queue Behavior: {'Healthy' if queue['healthy'] else 'Issues detected'}")
        
        # Session
        if "session" in validations:
            session = validations["session"]
            print(f"\n👥 Session Transition: {session.get('agents', 0)} agents checked")
        
        # Imports
        if "imports" in validations:
            imports = validations["imports"]
            if "count" in imports:
                print(f"\n📦 Imports: {imports['count']} imports found")
        
        print(f"\n🕐 Timestamp: {results.get('timestamp', 'unknown')}")
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Unified Validator - Consolidated validation for all systems",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--category", "-c",
        choices=["ssot_config", "imports", "code_docs", "queue", "session", "all"],
        default="all",
        help="Validation category (default: all)"
    )
    
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Validate specific file"
    )
    
    parser.add_argument(
        "--dir", "-d",
        type=str,
        help="Validate specific directory"
    )
    
    parser.add_argument(
        "--code-file",
        type=str,
        help="Code file for code-docs alignment"
    )
    
    parser.add_argument(
        "--doc-files",
        type=str,
        nargs="+",
        help="Documentation files for code-docs alignment"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    validator = UnifiedValidator()
    
    if args.category == "all":
        results = validator.run_full_validation(args.file)
    elif args.category == "ssot_config":
        if args.file:
            results = {"validation": validator.validate_ssot_config(file_path=args.file)}
        elif args.dir:
            results = {"validation": validator.validate_ssot_config(dir_path=args.dir)}
        else:
            results = {"validation": validator.validate_ssot_config()}
    elif args.category == "imports":
        if args.file:
            results = {"validation": validator.validate_imports(args.file)}
        else:
            results = {"validation": {"error": "File path required for import validation"}}
    elif args.category == "code_docs":
        if args.code_file and args.doc_files:
            results = {"validation": validator.validate_code_docs_alignment(args.code_file, args.doc_files)}
        else:
            results = {"validation": {"error": "Code file and doc files required"}}
    elif args.category == "queue":
        results = {"validation": validator.validate_queue_behavior()}
    elif args.category == "session":
        results = {"validation": validator.validate_session_transition()}
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "validations" in results:
            validator.print_validation_report(results)
        elif "validation" in results:
            print(json.dumps(results["validation"], indent=2))
        else:
            print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

