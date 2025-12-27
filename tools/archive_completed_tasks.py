#!/usr/bin/env python3
"""
Archive Completed Tasks from Master Task Logs
=============================================

Automatically archives all completed tasks from master task logs to archive sections.
Also generates cycle accomplishments report and posts to weareswarm.online.

Usage:
    python tools/archive_completed_tasks.py [--dry-run] [--log-file <path>] [--no-report] [--no-swarm-post]

Options:
    --dry-run          Preview changes without modifying files
    --log-file <path>  Path to master task log (default: MASTER_TASK_LOG.md)
    --all              Process all master task logs found in workspace
    --no-report        Skip generating cycle accomplishments report
    --no-swarm-post    Skip posting to weareswarm.online

Integration:
    - Connects to cycle accomplishments report generator
    - Posts archived tasks to weareswarm.online via REST API
    - Requires WEARESWARM_API_URL and WEARESWARM_API_KEY in .env
"""

import sys
import re
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Any

# Optional imports
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def find_completed_tasks(content: str) -> List[Tuple[int, str, str]]:
    """
    Find all completed tasks in content.
    
    Returns:
        List of (line_number, task_line, section_name) tuples
    """
    completed_tasks = []
    lines = content.split('\n')
    current_section = "INBOX"
    
    for i, line in enumerate(lines):
        # Track section headers
        if line.startswith('## ') or line.startswith('### '):
            # Extract section name
            section_match = re.match(r'^#+\s+(.+)$', line)
            if section_match:
                current_section = section_match.group(1).strip()
        
        # Check for completed task markers
        # Matches: - [x], - [X], -[x], etc.
        if re.match(r'^\s*-\s*\[[xX]\]', line):
            completed_tasks.append((i, line, current_section))
    
    return completed_tasks


def extract_archive_section(content: str) -> Tuple[str, int]:
    """
    Find or create archive section.
    
    Returns:
        (archive_content, insertion_line)
    """
    lines = content.split('\n')
    
    # Look for existing archive section
    archive_start = None
    archive_end = None
    
    for i, line in enumerate(lines):
        if 'COMPLETED TASKS ARCHIVE' in line.upper() or 'ARCHIVE' in line.upper():
            if archive_start is None:
                archive_start = i
        elif archive_start is not None and line.startswith('## ') and i > archive_start:
            archive_end = i
            break
    
    if archive_start is not None:
        # Extract existing archive
        if archive_end:
            archive_lines = lines[archive_start:archive_end]
        else:
            archive_lines = lines[archive_start:]
        return '\n'.join(archive_lines), archive_start
    
    # Create new archive section at end
    return None, len(lines)


def post_to_weareswarm(archived_tasks: List[Dict[str, Any]], api_url: str = None, api_key: str = None) -> bool:
    """
    Post archived tasks to weareswarm.online via REST API.
    
    Args:
        archived_tasks: List of archived task dictionaries
        api_url: Base URL for weareswarm.online API (default: from env or default)
        api_key: API key for authentication (default: from env)
    
    Returns:
        True if successful, False otherwise
    """
    if not REQUESTS_AVAILABLE:
        print("⚠️  requests library not available, skipping weareswarm.online post")
        print("   Install with: pip install requests")
        return False
    
    try:
        import os
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass  # dotenv not required if env vars are set directly
        
        # Get API URL and key from environment
        if not api_url:
            api_url = os.getenv('WEARESWARM_API_URL', 'https://weareswarm.online/wp-json/swarm/v2')
        if not api_key:
            api_key = os.getenv('WEARESWARM_API_KEY', '')
        
        if not api_key:
            print("⚠️  WEARESWARM_API_KEY not set, skipping weareswarm.online post")
            print("   Set WEARESWARM_API_KEY in .env file")
            return False
        
        # Format mission log entry
        total_tasks = len(archived_tasks)
        task_summary = "\n".join([f"- {task['section']}: {task['count']} tasks" 
                                  for task in archived_tasks])
        
        mission_log_entry = {
            'agent_id': 'System',
            'agent_name': 'Task Archiver',
            'mission': f'Archived {total_tasks} completed tasks',
            'status': 'complete',
            'details': f'Completed tasks archived from master task log:\n{task_summary}',
            'timestamp': datetime.now().isoformat(),
            'priority': 'normal'
        }
        
        # Post to mission log endpoint
        url = f"{api_url}/mission-log"
        headers = {
            'Content-Type': 'application/json',
            'X-Swarm-API-Key': api_key
        }
        
        response = requests.post(url, json=mission_log_entry, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"✅ Posted archived tasks to weareswarm.online")
            return True
        else:
            print(f"⚠️  Failed to post to weareswarm.online: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"⚠️  Error posting to weareswarm.online: {e}")
        return False


def generate_cycle_report() -> bool:
    """
    Generate cycle accomplishments report.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from tools.generate_cycle_accomplishments_report import generate_cycle_accomplishments_report
        
        print("📊 Generating cycle accomplishments report...")
        report_file = generate_cycle_accomplishments_report()
        
        if report_file:
            print(f"✅ Cycle accomplishments report generated: {report_file}")
            return True
        else:
            print("⚠️  Failed to generate cycle accomplishments report")
            return False
            
    except ImportError as e:
        print(f"⚠️  Cycle accomplishments report generator not available: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Error generating cycle accomplishments report: {e}")
        return False


def archive_tasks(log_file: Path, dry_run: bool = False, generate_report: bool = True, post_to_swarm: bool = True) -> dict:
    """
    Archive completed tasks from master task log.
    
    Returns:
        dict with stats about archived tasks
    """
    if not log_file.exists():
        return {
            'error': f'Log file not found: {log_file}',
            'archived': 0,
            'sections_updated': []
        }
    
    content = log_file.read_text(encoding='utf-8')
    original_content = content
    
    # Find completed tasks
    completed_tasks = find_completed_tasks(content)
    
    if not completed_tasks:
        return {
            'archived': 0,
            'sections_updated': [],
            'message': 'No completed tasks found'
        }
    
    # Group tasks by section
    tasks_by_section = {}
    for line_num, task_line, section in completed_tasks:
        if section not in tasks_by_section:
            tasks_by_section[section] = []
        tasks_by_section[section].append((line_num, task_line))
    
    # Get or create archive section
    archive_content, archive_insert_line = extract_archive_section(content)
    
    # Build archive entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    archive_entry = f"\n## COMPLETED TASKS ARCHIVE\n\n**Last Updated:** {timestamp}\n**Total Archived:** {len(completed_tasks)} tasks\n\n"
    
    for section, tasks in tasks_by_section.items():
        archive_entry += f"### {section}\n\n"
        for line_num, task_line in tasks:
            # Remove checkbox, keep rest of task
            cleaned_task = re.sub(r'^\s*-\s*\[[xX]\]\s*', '- [x] ', task_line)
            archive_entry += f"{cleaned_task}\n"
        archive_entry += "\n"
    
    # Remove completed tasks from active sections
    lines = content.split('\n')
    # Sort by line number descending to avoid index shifting
    lines_to_remove = sorted([line_num for line_num, _, _ in completed_tasks], reverse=True)
    
    for line_num in lines_to_remove:
        # Remove the line and any trailing empty lines
        del lines[line_num]
        # Remove following empty lines
        while line_num < len(lines) and lines[line_num].strip() == '':
            del lines[line_num]
    
    # Insert or update archive section
    if archive_content is None:
        # New archive section
        lines.insert(archive_insert_line, archive_entry)
    else:
        # Update existing archive
        archive_end = archive_insert_line + len(archive_content.split('\n'))
        # Replace existing archive
        lines[archive_insert_line:archive_end] = archive_entry.split('\n')
    
    new_content = '\n'.join(lines)
    
    # Prepare archived tasks summary for posting
    archived_tasks_summary = []
    for section, tasks in tasks_by_section.items():
        archived_tasks_summary.append({
            'section': section,
            'count': len(tasks),
            'tasks': [task_line for _, task_line in tasks]
        })
    
    if not dry_run:
        log_file.write_text(new_content, encoding='utf-8')
        
        # Generate cycle accomplishments report
        if generate_report and archived_tasks_summary:
            generate_cycle_report()
        
        # Post to weareswarm.online
        if post_to_swarm and archived_tasks_summary:
            post_to_weareswarm(archived_tasks_summary)
    
    return {
        'archived': len(completed_tasks),
        'sections_updated': list(tasks_by_section.keys()),
        'dry_run': dry_run,
        'changes': new_content != original_content,
        'archived_tasks_summary': archived_tasks_summary
    }


def find_all_master_logs() -> List[Path]:
    """Find all MASTER_TASK_LOG.md files in workspace."""
    master_logs = []
    
    # Check project root
    root_log = project_root / 'MASTER_TASK_LOG.md'
    if root_log.exists():
        master_logs.append(root_log)
    
    # Check websites workspace
    websites_root = Path('D:/websites')
    if websites_root.exists():
        websites_log = websites_root / 'MASTER_TASK_LOG.md'
        if websites_log.exists():
            master_logs.append(websites_log)
    
    # Search for other master logs
    for log_file in project_root.rglob('MASTER_TASK_LOG*.md'):
        if log_file not in master_logs:
            master_logs.append(log_file)
    
    return master_logs


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Archive completed tasks from master task logs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/archive_completed_tasks.py
  python tools/archive_completed_tasks.py --dry-run
  python tools/archive_completed_tasks.py --all
  python tools/archive_completed_tasks.py --log-file D:\\websites\\MASTER_TASK_LOG.md
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Process all master task logs found in workspace'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        help='Path to master task log file (default: MASTER_TASK_LOG.md in project root)'
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='Skip generating cycle accomplishments report'
    )
    
    parser.add_argument(
        '--no-swarm-post',
        action='store_true',
        help='Skip posting to weareswarm.online'
    )
    
    args = parser.parse_args()
    
    # Determine which files to process
    if args.all:
        log_files = find_all_master_logs()
        if not log_files:
            print("❌ No master task logs found")
            sys.exit(1)
        print(f"📋 Found {len(log_files)} master task log(s)")
    elif args.log_file:
        log_file = Path(args.log_file)
        if not log_file.is_absolute():
            log_file = project_root / log_file
        log_files = [log_file]
    else:
        # Default: project root
        log_file = project_root / 'MASTER_TASK_LOG.md'
        log_files = [log_file]
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
    
    total_archived = 0
    total_files = 0
    
    for log_file in log_files:
        print(f"\n📋 Processing: {log_file}")
        
        if not log_file.exists():
            print(f"   ⚠️  File not found, skipping")
            continue
        
        result = archive_tasks(
            log_file, 
            dry_run=args.dry_run,
            generate_report=not args.no_report,
            post_to_swarm=not args.no_swarm_post
        )
        
        if 'error' in result:
            print(f"   ❌ Error: {result['error']}")
            continue
        
        if result['archived'] == 0:
            print(f"   ✅ {result.get('message', 'No completed tasks to archive')}")
            continue
        
        total_archived += result['archived']
        total_files += 1
        
        print(f"   ✅ Archived {result['archived']} completed tasks")
        print(f"   📁 Sections updated: {', '.join(result['sections_updated'])}")
        
        if not args.dry_run:
            print(f"   💾 Changes saved")
    
    print(f"\n📊 Summary:")
    print(f"   Files processed: {total_files}")
    print(f"   Total tasks archived: {total_archived}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN - Run without --dry-run to apply changes")
    
    sys.exit(0)


if __name__ == '__main__':
    main()

