#!/usr/bin/env python3
"""
Documentation Sprawl Audit Tool
Comprehensive audit of documentation files to identify:
- Unreferenced documentation files
- Duplicate documentation
- Outdated documentation
- Documentation not properly organized or linked
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import json

# Documentation directories to scan
DOC_DIRS = [
    "docs",
    "agent_workspaces",
    "prompts",
    "tools",
    "scripts",
    "mcp_servers",
]

# Exclude patterns
EXCLUDE_PATTERNS = [
    "**/node_modules/**",
    "**/__pycache__/**",
    "**/.git/**",
    "**/temp_repos/**",
    "**/archive/**",
    "**/venv/**",
    "**/env/**",
]

# Documentation file extensions
DOC_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".yaml", ".yml"}

def find_documentation_files():
    """Find all documentation files."""
    doc_files = []
    base_path = Path(".")
    
    for doc_dir in DOC_DIRS:
        dir_path = base_path / doc_dir
        if not dir_path.exists():
            continue
            
        for ext in DOC_EXTENSIONS:
            for file_path in dir_path.rglob(f"*{ext}"):
                # Check if file should be excluded
                if any(pattern.replace("**/", "") in str(file_path) for pattern in EXCLUDE_PATTERNS):
                    continue
                doc_files.append(file_path)
    
    return doc_files

def find_references_in_code():
    """Find all references to documentation files in code."""
    references = defaultdict(list)
    base_path = Path(".")
    
    # Search in Python files
    for py_file in base_path.rglob("*.py"):
        if any(pattern.replace("**/", "") in str(py_file) for pattern in EXCLUDE_PATTERNS):
            continue
            
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            # Find markdown file references
            md_refs = re.findall(r'\[([^\]]+)\]\(([^\)]+\.md[^\)]*)\)', content)
            for ref_text, ref_path in md_refs:
                ref_path_clean = ref_path.split("#")[0].split("?")[0]
                references[ref_path_clean].append(str(py_file))
        except Exception:
            pass
    
    # Search in markdown files for cross-references
    for md_file in base_path.rglob("*.md"):
        if any(pattern.replace("**/", "") in str(md_file) for pattern in EXCLUDE_PATTERNS):
            continue
            
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            md_refs = re.findall(r'\[([^\]]+)\]\(([^\)]+\.md[^\)]*)\)', content)
            for ref_text, ref_path in md_refs:
                ref_path_clean = ref_path.split("#")[0].split("?")[0]
                references[ref_path_clean].append(str(md_file))
        except Exception:
            pass
    
    return references

def check_file_content_similarity(file1_path, file2_path, threshold=0.8):
    """Check if two files have similar content."""
    try:
        content1 = file1_path.read_text(encoding="utf-8", errors="ignore")
        content2 = file2_path.read_text(encoding="utf-8", errors="ignore")
        
        # Simple similarity check (can be enhanced with difflib)
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return False
            
        intersection = words1 & words2
        union = words1 | words2
        
        similarity = len(intersection) / len(union) if union else 0
        return similarity >= threshold
    except Exception:
        return False

def audit_documentation():
    """Run comprehensive documentation audit."""
    print("🔍 Starting documentation sprawl audit...")
    
    # Find all documentation files
    print("📁 Scanning for documentation files...")
    doc_files = find_documentation_files()
    print(f"   Found {len(doc_files)} documentation files")
    
    # Find references
    print("🔗 Scanning for references...")
    references = find_references_in_code()
    print(f"   Found references to {len(references)} files")
    
    # Analyze files
    unreferenced = []
    duplicates = []
    file_info = []
    
    print("📊 Analyzing files...")
    for doc_file in doc_files:
        # Skip if file doesn't exist
        if not doc_file.exists():
            continue
        rel_path = str(doc_file.relative_to(Path(".")))
        
        # Check if referenced
        is_referenced = False
        ref_sources = []
        for ref_path, sources in references.items():
            if ref_path in rel_path or rel_path in ref_path:
                is_referenced = True
                ref_sources.extend(sources)
        
        # Check if file exists (handle deleted files)
        if not doc_file.exists():
            continue
            
        try:
            file_size = doc_file.stat().st_size
            file_content = doc_file.read_text(encoding="utf-8", errors="ignore")
            file_lines = len(file_content.splitlines())
        except Exception as e:
            print(f"⚠️  Skipping {rel_path}: {e}")
            continue
        
        if not is_referenced and doc_file.suffix == ".md":
            # Check if it's a README or important file
            if doc_file.name.lower() not in ["readme.md", "index.md", "main.md"]:
                unreferenced.append({
                    "file": rel_path,
                    "size": file_size,
                    "lines": file_lines,
                })
        
        file_info.append({
            "file": rel_path,
            "size": file_size,
            "lines": file_lines,
            "referenced": is_referenced,
            "reference_sources": list(set(ref_sources))[:5],  # Limit to 5 sources
        })
    
    # Check for duplicates (simplified - check similar filenames and content)
    print("🔄 Checking for duplicates...")
    seen_names = defaultdict(list)
    for doc_file in doc_files:
        seen_names[doc_file.name.lower()].append(doc_file)
    
    for name, files in seen_names.items():
        if len(files) > 1:
            # Check if content is similar
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    if check_file_content_similarity(file1, file2):
                        duplicates.append({
                            "file1": str(file1.relative_to(Path("."))),
                            "file2": str(file2.relative_to(Path("."))),
                        })
    
    # Generate report
    report = {
        "audit_date": datetime.now().isoformat(),
        "total_files": len(doc_files),
        "unreferenced_files": {
            "count": len(unreferenced),
            "files": sorted(unreferenced, key=lambda x: x["size"], reverse=True)[:50],  # Top 50
        },
        "duplicate_files": {
            "count": len(duplicates),
            "pairs": duplicates[:20],  # Top 20
        },
        "file_analysis": file_info[:100],  # Sample
    }
    
    # Save report
    report_path = Path("reports/documentation_sprawl_audit.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))
    
    # Generate markdown summary
    summary_path = Path("reports/documentation_sprawl_audit_summary.md")
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Documentation Sprawl Audit Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Documentation Files:** {len(doc_files)}\n\n")
        f.write(f"## Unreferenced Files: {len(unreferenced)}\n\n")
        f.write("Top unreferenced files (by size):\n\n")
        for item in sorted(unreferenced, key=lambda x: x["size"], reverse=True)[:20]:
            f.write(f"- `{item['file']}` ({item['size']} bytes, {item['lines']} lines)\n")
        f.write(f"\n## Duplicate Files: {len(duplicates)}\n\n")
        for pair in duplicates[:10]:
            f.write(f"- `{pair['file1']}` ↔ `{pair['file2']}`\n")
        f.write("\n## Recommendations\n\n")
        f.write("1. Review unreferenced files for deletion or linking\n")
        f.write("2. Consolidate duplicate files\n")
        f.write("3. Create documentation index/navigation\n")
        f.write("4. Establish documentation maintenance protocol\n")
    
    print(f"\n✅ Audit complete!")
    print(f"   📄 Report: {report_path}")
    print(f"   📋 Summary: {summary_path}")
    print(f"   📊 Unreferenced files: {len(unreferenced)}")
    print(f"   🔄 Duplicate pairs: {len(duplicates)}")
    
    return report

if __name__ == "__main__":
    audit_documentation()

