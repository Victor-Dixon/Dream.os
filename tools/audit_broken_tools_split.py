#!/usr/bin/env python3
"""
Broken Tools Audit - Split for 8 Agents
========================================

Splits tool auditing into 8 equal parts for parallel execution across agents.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-20
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

PROJECT_ROOT = Path(__file__).parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"
ASSIGNMENTS_DIR = PROJECT_ROOT / "agent_workspaces" / "Agent-5" / "tool_audit_assignments"


def get_all_tools() -> List[Path]:
    """Get all Python tool files to audit."""
    python_files = []
    
    for file_path in TOOLS_DIR.rglob("*.py"):
        if _should_skip(file_path):
            continue
        python_files.append(file_path)
    
    return sorted(python_files)


def _should_skip(path: Path) -> bool:
    """Check if file should be skipped."""
    skip_patterns = [
        '__pycache__',
        '.pyc',
        'test_',
        '_test.py',
        'conftest.py',
        '__init__.py',
        'temp_',
        '.git',
        'deprecated'
    ]
    
    path_str = str(path)
    return any(pattern in path_str for pattern in skip_patterns)


def split_into_chunks(tools: List[Path], num_chunks: int = 8) -> List[List[Path]]:
    """Split tools into N equal chunks."""
    chunk_size = len(tools) // num_chunks
    remainder = len(tools) % num_chunks
    
    chunks = []
    start = 0
    
    for i in range(num_chunks):
        # Add 1 extra item to first 'remainder' chunks
        size = chunk_size + (1 if i < remainder else 0)
        end = start + size
        chunks.append(tools[start:end])
        start = end
    
    return chunks


def create_agent_assignments(chunks: List[List[Path]]):
    """Create assignment files for each agent."""
    ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    agents = [f"Agent-{i}" for i in range(1, 9)]
    
    for agent, chunk in zip(agents, chunks):
        assignment_file = ASSIGNMENTS_DIR / f"{agent}_tool_audit_assignment.json"
        
        assignment = {
            "agent": agent,
            "chunk_number": agents.index(agent) + 1,
            "total_chunks": 8,
            "tools_assigned": len(chunk),
            "tools": [str(t.relative_to(PROJECT_ROOT)) for t in chunk],
            "created_at": datetime.now().isoformat()
        }
        
        with open(assignment_file, 'w', encoding='utf-8') as f:
            json.dump(assignment, f, indent=2)
        
        print(f"✅ Created assignment for {agent}: {len(chunk)} tools")
    
    # Create summary
    summary_file = ASSIGNMENTS_DIR / "AUDIT_ASSIGNMENT_SUMMARY.json"
    summary = {
        "total_tools": sum(len(chunk) for chunk in chunks),
        "chunks": len(chunks),
        "assignments": [
            {
                "agent": agent,
                "chunk": i + 1,
                "tools_count": len(chunk),
                "assignment_file": f"{agent}_tool_audit_assignment.json"
            }
            for i, (agent, chunk) in enumerate(zip(agents, chunks))
        ],
        "created_at": datetime.now().isoformat()
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Summary saved: {summary_file}")


def run_agent_audit(agent: str, chunk_number: int) -> Dict:
    """Run audit for a specific agent's chunk."""
    assignment_file = ASSIGNMENTS_DIR / f"{agent}_tool_audit_assignment.json"
    
    if not assignment_file.exists():
        print(f"❌ Assignment file not found: {assignment_file}")
        return {"success": False, "error": "Assignment file not found"}
    
    with open(assignment_file, 'r', encoding='utf-8') as f:
        assignment = json.load(f)
    
    tools = assignment.get("tools", [])
    
    print(f"🔍 {agent} - Auditing {len(tools)} tools (Chunk {chunk_number}/8)")
    print("=" * 70)
    
    # Import and use ToolAuditor from audit_broken_tools.py
    sys.path.insert(0, str(PROJECT_ROOT))
    from tools.audit_broken_tools import ToolAuditor
    
    auditor = ToolAuditor(verbose=False)
    
    # Create a temp directory with symlinks or run on subset
    # For now, we'll filter the audit to only these tools
    results = {
        'working': [],
        'broken': [],
        'syntax_errors': [],
        'import_errors': [],
        'runtime_errors': []
    }
    
    for idx, tool_path_str in enumerate(tools, 1):
        tool_path = PROJECT_ROOT / tool_path_str
        if not tool_path.exists():
            continue
        
        print(f"[{idx}/{len(tools)}] Testing {Path(tool_path_str).name}...", end=" ")
        result = auditor._test_file(tool_path)
        print(result['status'])
        
        # Collect results
        tool_rel = tool_path_str
        if 'WORKING' in result['status']:
            results['working'].append(tool_rel)
        else:
            results['broken'].append(tool_rel)
            if 'SYNTAX' in result['status']:
                results['syntax_errors'].append(tool_rel)
            elif 'IMPORT' in result['status']:
                results['import_errors'].append(tool_rel)
            elif 'RUNTIME' in result['status']:
                results['runtime_errors'].append(tool_rel)
    
    # Save results
    results_file = ASSIGNMENTS_DIR / f"{agent}_audit_results.json"
    audit_results = {
        "agent": agent,
        "chunk_number": chunk_number,
        "audit_date": datetime.now().isoformat(),
        "tools_audited": len(tools),
        "results": results,
        "summary": {
            "working": len(results['working']),
            "broken": len(results['broken']),
            "syntax_errors": len(results['syntax_errors']),
            "import_errors": len(results['import_errors']),
            "runtime_errors": len(results['runtime_errors'])
        }
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(audit_results, f, indent=2)
    
    print(f"\n✅ Results saved: {results_file}")
    
    return {
        "success": True,
        "results_file": str(results_file),
        "summary": audit_results["summary"]
    }


def combine_results() -> Dict:
    """Combine results from all agents."""
    agents = [f"Agent-{i}" for i in range(1, 9)]
    
    combined = {
        'working': [],
        'broken': [],
        'syntax_errors': [],
        'import_errors': [],
        'runtime_errors': []
    }
    
    agent_summaries = {}
    
    for agent in agents:
        results_file = ASSIGNMENTS_DIR / f"{agent}_audit_results.json"
        if not results_file.exists():
            print(f"⚠️  Results not found for {agent}")
            continue
        
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = data.get("results", {})
        for key in combined:
            combined[key].extend(results.get(key, []))
        
        agent_summaries[agent] = data.get("summary", {})
    
    # Save combined results
    combined_file = ASSIGNMENTS_DIR / "COMBINED_AUDIT_RESULTS.json"
    combined_data = {
        "combined_at": datetime.now().isoformat(),
        "total_tools": sum(len(v) for v in combined.values()),
        "summary": {
            "working": len(combined['working']),
            "broken": len(combined['broken']),
            "syntax_errors": len(combined['syntax_errors']),
            "import_errors": len(combined['import_errors']),
            "runtime_errors": len(combined['runtime_errors'])
        },
        "agent_summaries": agent_summaries,
        "results": combined
    }
    
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"✅ Combined results saved: {combined_file}")
    
    return combined_data


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Split tool audit into 8 agent assignments")
    parser.add_argument('--split', action='store_true', help='Split tools into 8 assignments')
    parser.add_argument('--agent', type=str, help='Run audit for specific agent (e.g., Agent-1)')
    parser.add_argument('--chunk', type=int, help='Run audit for specific chunk (1-8)')
    parser.add_argument('--combine', action='store_true', help='Combine all agent results')
    
    args = parser.parse_args()
    
    if args.split:
        print("🔍 Finding all tools...")
        tools = get_all_tools()
        print(f"✅ Found {len(tools)} tools to audit")
        
        print("\n📦 Splitting into 8 equal chunks...")
        chunks = split_into_chunks(tools, 8)
        
        for i, chunk in enumerate(chunks, 1):
            print(f"   Chunk {i}: {len(chunk)} tools")
        
        print("\n📋 Creating agent assignments...")
        create_agent_assignments(chunks)
        
        print("\n✅ Assignments created! Agents can now run:")
        print("   python tools/audit_broken_tools_split.py --agent Agent-X --chunk X")
        
    elif args.agent and args.chunk:
        result = run_agent_audit(args.agent, args.chunk)
        if result.get("success"):
            summary = result.get("summary", {})
            print(f"\n📊 {args.agent} Summary:")
            print(f"   Working: {summary.get('working', 0)}")
            print(f"   Broken: {summary.get('broken', 0)}")
    
    elif args.combine:
        print("🔗 Combining results from all agents...")
        combined = combine_results()
        summary = combined.get("summary", {})
        print(f"\n📊 COMBINED SUMMARY:")
        print(f"   Total Tools: {combined.get('total_tools', 0)}")
        print(f"   ✅ Working: {summary.get('working', 0)}")
        print(f"   ❌ Broken: {summary.get('broken', 0)}")
        print(f"      - Syntax Errors: {summary.get('syntax_errors', 0)}")
        print(f"      - Import Errors: {summary.get('import_errors', 0)}")
        print(f"      - Runtime Errors: {summary.get('runtime_errors', 0)}")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


