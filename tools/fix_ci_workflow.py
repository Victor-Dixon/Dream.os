#!/usr/bin/env python3
"""
Fix CI/CD Workflow Issues
=========================
Updates CI workflows to ignore gitignored directories and handle common failures.
"""

import re
from pathlib import Path

def fix_ci_workflow(workflow_file: str):
    """Fix common CI workflow issues."""
    print(f"Fixing {workflow_file}...")
    
    with open(workflow_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add exclusions for gitignored directories in ruff/black/isort
    original_lint = r'ruff check \.'
    if original_lint in content and '--exclude' not in content:
        new_lint = (
            'ruff check . --exclude "agent_workspaces,temp_repos,archive,'
            '.git,__pycache__,*.pyc,venv,.venv"'
        )
        content = content.replace('ruff check .', new_lint)
    
    original_black = r'black --check \.'
    if original_black in content and '--exclude' not in content:
        new_black = (
            'black --check . --exclude "/(agent_workspaces|temp_repos|archive|'
            '.git|__pycache__|venv|.venv)/"'
        )
        content = content.replace('black --check .', new_black)
    
    original_isort = r'isort --check-only \.'
    if original_isort in content and '--skip' not in content:
        new_isort = (
            'isort --check-only . --skip "agent_workspaces,temp_repos,archive"'
        )
        content = content.replace('isort --check-only .', new_isort)
    
    # Add pytest exclusions
    original_pytest = r'pytest.*tests/'
    if '--ignore' not in content and 'pytest' in content:
        # Find pytest commands and add ignore patterns
        pytest_pattern = r'(pytest[^\n]*)'
        def add_ignore(match):
            cmd = match.group(1)
            if '--ignore' not in cmd:
                return cmd + ' --ignore=agent_workspaces --ignore=temp_repos --ignore=archive'
            return cmd
        content = re.sub(pytest_pattern, add_ignore, content)
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {workflow_file}")

def main():
    """Fix all CI workflow files."""
    workflow_dir = Path(".github/workflows")
    
    workflows = [
        "ci-cd.yml",
        "ci.yml",
        "ci-optimized.yml",
        "ci-minimal.yml",
    ]
    
    for workflow in workflows:
        workflow_path = workflow_dir / workflow
        if workflow_path.exists():
            fix_ci_workflow(str(workflow_path))
        else:
            print(f"⚠️  {workflow} not found, skipping")

if __name__ == "__main__":
    main()

