#!/usr/bin/env python3
"""
Analyze Merged Repo Patterns - Agent-2
======================================

Analyzes merged repos in DreamVault to extract integration patterns:
1. DreamBank - Portfolio management patterns
2. DigitalDreamscape - AI framework patterns
3. Thea - Advanced AI framework patterns
"""

import os
import sys
import subprocess
import tempfile
import shutil
import time
import stat
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or .env file."""
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    env_path = Path(".env")
    if env_path.exists():
        try:
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None


def get_github_username() -> Optional[str]:
    """Get GitHub username from environment or .env file."""
    username = os.getenv("GITHUB_USERNAME")
    if username:
        return username
    
    env_path = Path(".env")
    if env_path.exists():
        try:
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("GITHUB_USERNAME="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None


def ensure_dir_removed(dir_path: Path, name: str):
    """Ensure directory is completely removed."""
    if dir_path.exists():
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
            time.sleep(0.5)
            if dir_path.exists():
                def remove_readonly(func, path, exc):
                    os.chmod(path, stat.S_IWRITE)
                    func(path)
                shutil.rmtree(dir_path, onerror=remove_readonly)
                time.sleep(0.5)
        except Exception:
            pass


def clone_dreamvault(temp_base: Path, token: str, username: str) -> Optional[Path]:
    """Clone DreamVault repository."""
    owner = "Dadudekc"
    repo = "DreamVault"
    repo_dir = temp_base / repo
    
    try:
        repo_url = f"https://{username}:{token}@github.com/{owner}/{repo}.git"
        subprocess.run(
            ["git", "clone", repo_url, str(repo_dir)],
            check=True, timeout=300, capture_output=True, text=True
        )
        return repo_dir
    except Exception:
        return None


def analyze_portfolio_patterns(repo_dir: Path) -> Dict:
    """Analyze DreamBank portfolio management patterns."""
    patterns = {
        "files": [],
        "modules": [],
        "functions": [],
        "classes": [],
        "dependencies": []
    }
    
    # Look for portfolio-related files
    portfolio_files = list(repo_dir.rglob("*portfolio*.py"))
    portfolio_files.extend(repo_dir.rglob("*stock*.py"))
    portfolio_files.extend(repo_dir.rglob("*financial*.py"))
    
    for file_path in portfolio_files:
        if ".git" in file_path.parts or "site-packages" in str(file_path):
            continue
        
        rel_path = file_path.relative_to(repo_dir)
        patterns["files"].append(str(rel_path))
        
        # Try to extract classes and functions
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")
            
            for line in lines:
                if line.strip().startswith("class "):
                    class_name = line.strip().split("class ")[1].split("(")[0].strip()
                    patterns["classes"].append(f"{rel_path}:{class_name}")
                elif line.strip().startswith("def ") and not line.strip().startswith("def _"):
                    func_name = line.strip().split("def ")[1].split("(")[0].strip()
                    patterns["functions"].append(f"{rel_path}:{func_name}")
        except Exception:
            pass
    
    return patterns


def analyze_ai_framework_patterns(repo_dir: Path) -> Dict:
    """Analyze DigitalDreamscape and Thea AI framework patterns."""
    patterns = {
        "files": [],
        "modules": [],
        "functions": [],
        "classes": [],
        "ai_models": [],
        "nlp_components": [],
        "conversation_handlers": []
    }
    
    # Look for AI-related files
    ai_files = list(repo_dir.rglob("*ai*.py"))
    ai_files.extend(repo_dir.rglob("*assistant*.py"))
    ai_files.extend(repo_dir.rglob("*conversation*.py"))
    ai_files.extend(repo_dir.rglob("*nlp*.py"))
    ai_files.extend(repo_dir.rglob("*model*.py"))
    
    for file_path in ai_files:
        if ".git" in file_path.parts or "site-packages" in str(file_path):
            continue
        
        rel_path = file_path.relative_to(repo_dir)
        patterns["files"].append(str(rel_path))
        
        # Categorize by type
        path_str = str(rel_path).lower()
        if "model" in path_str:
            patterns["ai_models"].append(str(rel_path))
        if "nlp" in path_str or "language" in path_str:
            patterns["nlp_components"].append(str(rel_path))
        if "conversation" in path_str or "chat" in path_str:
            patterns["conversation_handlers"].append(str(rel_path))
        
        # Extract classes and functions
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            lines = content.split("\n")
            
            for line in lines:
                if line.strip().startswith("class "):
                    class_name = line.strip().split("class ")[1].split("(")[0].strip()
                    patterns["classes"].append(f"{rel_path}:{class_name}")
                elif line.strip().startswith("def ") and not line.strip().startswith("def _"):
                    func_name = line.strip().split("def ")[1].split("(")[0].strip()
                    patterns["functions"].append(f"{rel_path}:{func_name}")
        except Exception:
            pass
    
    return patterns


def generate_integration_patterns_report(repo_dir: Path, portfolio_patterns: Dict, ai_patterns: Dict) -> str:
    """Generate integration patterns report."""
    report = []
    report.append("="*60)
    report.append("📋 DREAMVAULT INTEGRATION PATTERNS ANALYSIS")
    report.append("="*60)
    
    report.append("\n📊 PORTFOLIO MANAGEMENT PATTERNS (DreamBank):")
    report.append(f"   Files: {len(portfolio_patterns['files'])}")
    report.append(f"   Classes: {len(portfolio_patterns['classes'])}")
    report.append(f"   Functions: {len(portfolio_patterns['functions'])}")
    
    if portfolio_patterns['files']:
        report.append("\n   Key Files:")
        for file in portfolio_patterns['files'][:10]:
            report.append(f"      - {file}")
        if len(portfolio_patterns['files']) > 10:
            report.append(f"      ... and {len(portfolio_patterns['files']) - 10} more")
    
    if portfolio_patterns['classes']:
        report.append("\n   Key Classes:")
        for cls in portfolio_patterns['classes'][:10]:
            report.append(f"      - {cls}")
        if len(portfolio_patterns['classes']) > 10:
            report.append(f"      ... and {len(portfolio_patterns['classes']) - 10} more")
    
    report.append("\n🤖 AI FRAMEWORK PATTERNS (DigitalDreamscape + Thea):")
    report.append(f"   Files: {len(ai_patterns['files'])}")
    report.append(f"   AI Models: {len(ai_patterns['ai_models'])}")
    report.append(f"   NLP Components: {len(ai_patterns['nlp_components'])}")
    report.append(f"   Conversation Handlers: {len(ai_patterns['conversation_handlers'])}")
    report.append(f"   Classes: {len(ai_patterns['classes'])}")
    report.append(f"   Functions: {len(ai_patterns['functions'])}")
    
    if ai_patterns['ai_models']:
        report.append("\n   AI Model Files:")
        for file in ai_patterns['ai_models'][:10]:
            report.append(f"      - {file}")
    
    if ai_patterns['conversation_handlers']:
        report.append("\n   Conversation Handler Files:")
        for file in ai_patterns['conversation_handlers'][:10]:
            report.append(f"      - {file}")
    
    report.append("\n🔧 INTEGRATION TASKS:")
    report.append("   1. Extract portfolio management modules from DreamBank")
    report.append("   2. Extract AI framework components from DigitalDreamscape")
    report.append("   3. Extract advanced AI components from Thea")
    report.append("   4. Unify into SSOT service architecture")
    report.append("   5. Integrate data models")
    report.append("   6. Test unified functionality")
    
    return "\n".join(report)


def main():
    """Main entry point."""
    token = get_github_token()
    username = get_github_username()
    
    if not token or not username:
        print("❌ GITHUB_TOKEN or GITHUB_USERNAME not found.")
        return 1
    
    timestamp = int(time.time() * 1000000)
    temp_base = Path(tempfile.mkdtemp(prefix=f"pattern_analysis_{timestamp}_"))
    
    try:
        repo_dir = clone_dreamvault(temp_base, token, username)
        if not repo_dir:
            return 1
        
        print("🔍 Analyzing portfolio patterns (DreamBank)...")
        portfolio_patterns = analyze_portfolio_patterns(repo_dir)
        
        print("🔍 Analyzing AI framework patterns (DigitalDreamscape + Thea)...")
        ai_patterns = analyze_ai_framework_patterns(repo_dir)
        
        print("📋 Generating integration patterns report...")
        report = generate_integration_patterns_report(repo_dir, portfolio_patterns, ai_patterns)
        print(report)
        
        # Save report
        report_file = project_root / "agent_workspaces" / "Agent-2" / "INTEGRATION_PATTERNS_ANALYSIS.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✅ Report saved to: {report_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        ensure_dir_removed(temp_base, "temp_repo_clone")


if __name__ == "__main__":
    sys.exit(main())

