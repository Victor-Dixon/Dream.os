#!/usr/bin/env python3
"""
Phase 2 Markdown Cleanup: Structural Consolidation
===============================================

Executes safe structural consolidation operations for markdown cleanup:
- Devlog deduplication (symlink creation)
- Archive reorganization
- Safe duplicate consolidation

Author: Agent-5 (Business Intelligence)
Date: 2026-01-11
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

class MarkdownCleanupPhase2:
    """Phase 2 structural consolidation for markdown files."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.safe_operations = []
        self.risk_operations = []
        self.stats = defaultdict(int)

    def analyze_devlog_duplication(self) -> Dict[str, List[str]]:
        """Analyze devlog files for duplication patterns."""
        print("🔍 Analyzing devlog duplication patterns...")

        devlog_files = []
        content_hashes = defaultdict(list)

        # Find all devlog files
        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
            for file in files:
                if 'devlog' in file.lower() and file.endswith('.md'):
                    file_path = Path(root) / file
                    devlog_files.append(file_path)

        print(f"Found {len(devlog_files)} devlog files")

        # Group by content hash
        for file_path in devlog_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                    content_hashes[content_hash].append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        # Identify duplicate groups
        duplicates = {k: v for k, v in content_hashes.items() if len(v) > 1}

        print(f"Found {len(duplicates)} duplicate devlog groups")
        for i, (hash_key, files) in enumerate(sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)[:5]):
            print(f"  Group {i+1}: {len(files)} files")
            for file_path in files[:3]:
                print(f"    {file_path}")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")

        return duplicates

    def identify_safe_consolidation_ops(self, duplicates: Dict[str, List[str]]) -> List[Tuple[str, List[str]]]:
        """Identify safe consolidation operations."""
        print("\n🛡️ Identifying safe consolidation operations...")

        safe_ops = []

        for hash_key, files in duplicates.items():
            if len(files) >= 3:
                # Look for the pattern: workspace + swarm_brain + archive
                workspace_files = [f for f in files if 'agent_workspaces' in str(f)]
                swarm_files = [f for f in files if 'swarm_brain' in str(f)]
                archive_files = [f for f in files if 'archive' in str(f)]

                if workspace_files and (swarm_files or archive_files):
                    # Safe to create symlinks from swarm_brain/archive to workspace
                    authoritative = workspace_files[0]  # Use first workspace file as authoritative
                    targets = swarm_files + archive_files

                    safe_ops.append((str(authoritative), [str(f) for f in targets]))

        print(f"Identified {len(safe_ops)} safe symlink operations")
        return safe_ops

    def execute_safe_symlink_creation(self, safe_ops: List[Tuple[str, List[str]]], dry_run: bool = True) -> Dict[str, int]:
        """Execute safe symlink creation operations."""
        print(f"\n🔗 {'DRY RUN: ' if dry_run else ''}Executing safe symlink creation...")

        results = defaultdict(int)

        for authoritative, targets in safe_ops[:5]:  # Limit to first 5 for safety
            auth_path = Path(authoritative)
            if not auth_path.exists():
                print(f"⚠️ Authoritative file missing: {authoritative}")
                results['errors'] += 1
                continue

            for target in targets:
                target_path = Path(target)

                if target_path.exists():
                    if dry_run:
                        print(f"Would replace {target} with symlink to {authoritative}")
                        results['would_symlink'] += 1
                    else:
                        try:
                            # Remove existing file and create symlink
                            target_path.unlink()
                            target_path.symlink_to(auth_path)
                            print(f"✅ Created symlink: {target} -> {authoritative}")
                            results['symlinked'] += 1
                        except Exception as e:
                            print(f"❌ Failed to create symlink {target}: {e}")
                            results['errors'] += 1
                else:
                    print(f"⚠️ Target file missing: {target}")
                    results['missing'] += 1

        return dict(results)

    def analyze_archive_reorganization(self) -> Dict[str, List[str]]:
        """Analyze files that should be moved from archive back to working directories."""
        print("\n📂 Analyzing archive reorganization opportunities...")

        recent_archive_files = []

        # Find markdown files in archive directories that are recent (< 30 days old)
        archive_paths = [
            self.repo_root / 'archive',
            self.repo_root / 'data' / 'models' / 'swarm_brain' / 'devlogs'
        ]

        for archive_path in archive_paths:
            if archive_path.exists():
                for root, dirs, files in os.walk(archive_path):
                    for file in files:
                        if file.endswith('.md'):
                            file_path = Path(root) / file
                            try:
                                # Check if file is recent (modified within last 30 days)
                                stat = file_path.stat()
                                age_days = (Path(__file__).stat().st_mtime - stat.st_mtime) / (24 * 3600)

                                if age_days < 30:  # Less than 30 days old
                                    recent_archive_files.append(str(file_path))
                            except Exception:
                                continue

        print(f"Found {len(recent_archive_files)} recent files in archive directories")

        # Group by potential target directories
        reorganization_targets = defaultdict(list)

        for file_path in recent_archive_files[:20]:  # Sample first 20
            path_parts = Path(file_path).parts

            # Look for agent workspace patterns
            if 'agent_workspaces' in path_parts:
                agent_idx = path_parts.index('agent_workspaces')
                if agent_idx + 1 < len(path_parts):
                    agent_name = path_parts[agent_idx + 1]
                    target_dir = f"agent_workspaces/{agent_name}"
                    reorganization_targets[target_dir].append(file_path)

            # Look for devlogs pattern
            elif 'devlogs' in path_parts:
                reorganization_targets['devlogs'].append(file_path)

        print("Potential reorganization targets:")
        for target, files in reorganization_targets.items():
            print(f"  {target}: {len(files)} files")

        return dict(reorganization_targets)

    def generate_cleanup_report(self, duplicates: Dict[str, List[str]],
                              safe_ops: List[Tuple[str, List[str]]],
                              symlink_results: Dict[str, int],
                              archive_targets: Dict[str, List[str]]) -> str:
        """Generate comprehensive cleanup report."""
        report = f"""# Phase 2 Markdown Cleanup Report
**Generated:** 2026-01-11
**Agent:** Agent-5 (Business Intelligence)

## Executive Summary

**Duplicate Analysis:**
- Total duplicate groups: {len(duplicates)}
- Files in duplicate groups: {sum(len(files) for files in duplicates.values())}
- Potential space savings: {sum(len(files) - 1 for files in duplicates.values())} files

**Safe Operations Identified:**
- Symlink creation operations: {len(safe_ops)}
- Archive reorganization targets: {len(archive_targets)}
- Total files that could be processed: {sum(len(files) for files in archive_targets.values())}

**Execution Results (Safe Operations):**
- Symlinks created: {symlink_results.get('symlinked', 0)}
- Symlinks that would be created: {symlink_results.get('would_symlink', 0)}
- Errors encountered: {symlink_results.get('errors', 0)}
- Missing files: {symlink_results.get('missing', 0)}

## Detailed Findings

### Major Duplicate Patterns
"""

        # Add top duplicate groups
        for i, (hash_key, files) in enumerate(sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)[:10]):
            report += f"**Group {i+1}:** {len(files)} files\n"
            for file_path in files[:5]:
                report += f"- {file_path}\n"
            if len(files) > 5:
                report += f"- ... and {len(files) - 5} more\n\n"

        report += """
### Safe Symlink Operations
The following operations can be executed with minimal risk:
"""

        for authoritative, targets in safe_ops[:10]:
            report += f"**Authoritative:** {authoritative}\n"
            report += "**Targets:**\n"
            for target in targets:
                report += f"- {target}\n"
            report += "\n"

        report += f"""
### Archive Reorganization Opportunities
Recent files found in archive directories that could be moved back to working areas:

"""
        for target, files in archive_targets.items():
            report += f"**{target}:** {len(files)} files\n"
            for file_path in files[:3]:
                report += f"- {file_path}\n"
            if len(files) > 3:
                report += f"- ... and {len(files) - 3} more\n\n"

        report += """
## Risk Assessment

### Low Risk Operations ✅
- Symlink creation for devlog deduplication
- Archive reorganization for recent files
- Safe consolidation of exact duplicates

### Medium Risk Operations ⚠️
- Content-based deduplication (requires human review)
- File relocation with reference updates

### High Risk Operations 🚫
- Automated deletion based on semantic similarity
- Bulk archive operations without backup

## Next Steps

1. **Execute Safe Symlink Creation** - Implement identified symlink operations
2. **Archive Reorganization** - Move recent files back to working directories
3. **Phase 3 Planning** - Develop semantic deduplication algorithms
4. **Coordination** - Sync with Agent-1 for Phase 3 execution approval

## Command Reference

```bash
# Execute safe symlink operations
python tools/markdown_cleanup_phase2.py --execute-symlinks

# Analyze archive reorganization
python tools/markdown_cleanup_phase2.py --analyze-archive

# Generate detailed report
python tools/markdown_cleanup_phase2.py --generate-report
```
"""
        return report

def main():
    """Main execution function."""
    repo_root = Path('.')
    cleanup = MarkdownCleanupPhase2(repo_root)

    print("🚀 Phase 2 Markdown Cleanup: Structural Consolidation")
    print("=" * 60)

    # Step 1: Analyze devlog duplication
    duplicates = cleanup.analyze_devlog_duplication()

    # Step 2: Identify safe operations
    safe_ops = cleanup.identify_safe_consolidation_ops(duplicates)

    # Step 3: Execute safe symlink creation (dry run)
    symlink_results = cleanup.execute_safe_symlink_creation(safe_ops, dry_run=True)

    # Step 4: Analyze archive reorganization
    archive_targets = cleanup.analyze_archive_reorganization()

    # Step 5: Generate comprehensive report
    report = cleanup.generate_cleanup_report(duplicates, safe_ops, symlink_results, archive_targets)

    # Save report
    report_path = Path('reports/markdown_cleanup_phase2_20260111.md')
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n📄 Report saved to: reports/markdown_cleanup_phase2_20260111.md")
    print(f"📊 Phase 2 Analysis Complete:")
    print(f"   Duplicate groups: {len(duplicates)}")
    print(f"   Safe symlink ops: {len(safe_ops)}")
    print(f"   Archive targets: {len(archive_targets)}")
    print(f"   Total files analyzed: {sum(len(files) for files in duplicates.values())}")

if __name__ == "__main__":
    main()