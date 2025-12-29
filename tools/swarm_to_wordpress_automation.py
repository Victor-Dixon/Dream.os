#!/usr/bin/env python3
"""
Swarm to WordPress Automation
=============================

Automatically creates WordPress content from swarm workflows:
- Session closures → Experiments/Projects
- Devlogs → Blog posts
- Status updates → Resume items

SSOT: "Dreamvault + ChatGPT conversation history = blogging for dadudekc"
      "plans + learnings from experiments = content"
      "demos of projects = content"
      "skills learned = added to resume"

Usage:
    python tools/swarm_to_wordpress_automation.py --watch
    python tools/swarm_to_wordpress_automation.py --once
    python tools/swarm_to_wordpress_automation.py --agent Agent-7
"""

import os
import re
import json
import argparse
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
from dataclasses import dataclass

# Add tools directory to path for multi_site_content_generator import
sys.path.insert(0, str(Path(__file__).parent))

try:
    from multi_site_content_generator import MultiSiteContentGenerator
    MULTI_SITE_GENERATOR_AVAILABLE = True
except ImportError:
    MULTI_SITE_GENERATOR_AVAILABLE = False
    print("⚠️  Multi-site content generator not available. Using basic formatting.")

# WordPress REST API configuration
WORDPRESS_SITES = {
    'dadudekc.com': {
        'url': 'https://dadudekc.com',
        'rest_base': '/wp-json/wp/v2',
        'username': os.getenv('DADUDEKC_WP_USERNAME'),
        'password': os.getenv('DADUDEKC_WP_PASSWORD'),  # Application password
    },
    'freerideinvestor.com': {
        'url': 'https://freerideinvestor.com',
        'rest_base': '/wp-json/wp/v2',
        'username': os.getenv('FREERIDEINVESTOR_WP_USERNAME'),
        'password': os.getenv('FREERIDEINVESTOR_WP_PASSWORD'),
    },
    'tradingrobotplug.com': {
        'url': 'https://tradingrobotplug.com',
        'rest_base': '/wp-json/wp/v2',
        'username': os.getenv('TRADINGROBOTPLUG_WP_USERNAME'),
        'password': os.getenv('TRADINGROBOTPLUG_WP_PASSWORD'),
    },
    'weareswarm.online': {
        'url': 'https://weareswarm.online',
        'rest_base': '/wp-json/wp/v2',
        'username': os.getenv('WEARESWARM_WP_USERNAME'),
        'password': os.getenv('WEARESWARM_WP_PASSWORD'),
    },
}

AGENT_WORKSPACES = Path(__file__).parent.parent / 'agent_workspaces'
SESSION_CLOSURES_DIR = 'session_closures'
DEVLOGS_DIR = 'devlogs'
STATE_FILE = Path(__file__).parent / '.swarm_wp_automation_state.json'


@dataclass
class SessionClosure:
    """Parsed session closure data."""
    agent_id: str
    task: str
    project: str
    actions: List[str]
    artifacts: List[str]
    verification: List[str]
    public_build_signal: str
    status: str
    file_path: Path
    timestamp: datetime


@dataclass
class Devlog:
    """Parsed devlog data."""
    agent_id: str
    title: str
    content: str
    file_path: Path
    timestamp: datetime


def load_state() -> Dict:
    """Load processed files state."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'processed_closures': [],
        'processed_devlogs': [],
        'last_check': None
    }


def save_state(state: Dict):
    """Save processed files state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)


def parse_session_closure(file_path: Path) -> Optional[SessionClosure]:
    """Parse a session closure markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Extract agent ID from path
        agent_match = re.search(r'Agent-(\d+)', str(file_path))
        agent_id = f"Agent-{agent_match.group(1)}" if agent_match else "Unknown"
        
        # Parse structured fields
        task_match = re.search(r'- \*\*Task:\*\* (.+)', content)
        project_match = re.search(r'- \*\*Project:\*\* (.+)', content)
        status_match = re.search(r'- \*\*Status:\*\* (.+)', content)
        build_signal_match = re.search(r'- \*\*Public Build Signal:\*\* (.+)', content, re.DOTALL)
        
        # Extract actions (bullet list)
        actions_section = re.search(r'- \*\*Actions Taken:\*\*(.*?)(?=- \*\*|$)', content, re.DOTALL)
        actions = []
        if actions_section:
            action_lines = re.findall(r'^\s+- (.+)$', actions_section.group(1), re.MULTILINE)
            actions = [line.strip() for line in action_lines]
        
        # Extract artifacts
        artifacts_section = re.search(r'- \*\*Artifacts Created / Updated:\*\*(.*?)(?=- \*\*|$)', content, re.DOTALL)
        artifacts = []
        if artifacts_section:
            artifact_lines = re.findall(r'^\s+- (.+)$', artifacts_section.group(1), re.MULTILINE)
            artifacts = [line.strip() for line in artifact_lines]
        
        # Extract verification
        verification_section = re.search(r'- \*\*Verification:\*\*(.*?)(?=- \*\*|$)', content, re.DOTALL)
        verification = []
        if verification_section:
            verification_lines = re.findall(r'^\s+- (.+)$', verification_section.group(1), re.MULTILINE)
            verification = [line.strip() for line in verification_lines]
        
        # Get file timestamp
        timestamp = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        return SessionClosure(
            agent_id=agent_id,
            task=task_match.group(1).strip() if task_match else '',
            project=project_match.group(1).strip() if project_match else '',
            actions=actions,
            artifacts=artifacts,
            verification=verification,
            public_build_signal=build_signal_match.group(1).strip() if build_signal_match else '',
            status=status_match.group(1).strip() if status_match else '',
            file_path=file_path,
            timestamp=timestamp
        )
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None


def parse_devlog(file_path: Path) -> Optional[Devlog]:
    """Parse a devlog markdown file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Extract agent ID from path
        agent_match = re.search(r'Agent-(\d+)', str(file_path))
        agent_id = f"Agent-{agent_match.group(1)}" if agent_match else "Unknown"
        
        # Extract title (first H1 or filename)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else file_path.stem
        
        # Get file timestamp
        timestamp = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        return Devlog(
            agent_id=agent_id,
            title=title,
            content=content,
            file_path=file_path,
            timestamp=timestamp
        )
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None


def create_wordpress_post(
    site_key: str,
    post_type: str,
    title: str,
    content: str,
    meta: Dict = None,
    status: str = 'publish'
) -> Optional[int]:
    """Create a WordPress post via REST API."""
    site_config = WORDPRESS_SITES.get(site_key)
    if not site_config:
        print(f"❌ Unknown site: {site_key}")
        return None
    
    if not site_config['username'] or not site_config['password']:
        print(f"❌ Missing WordPress credentials for {site_key}")
        return None
    
    url = f"{site_config['url']}{site_config['rest_base']}/{post_type}"
    auth = (site_config['username'], site_config['password'])
    
    data = {
        'title': title,
        'content': content,
        'status': status,
    }
    
    # Add meta fields if provided
    if meta:
        data['meta'] = meta
    
    try:
        response = requests.post(url, json=data, auth=auth, timeout=30)
        response.raise_for_status()
        post_data = response.json()
        post_id = post_data.get('id')
        print(f"✅ Created {post_type} post: {title} (ID: {post_id})")
        return post_id
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating WordPress post: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text}")
        return None


def session_closure_to_experiment(closure: SessionClosure) -> Tuple[str, str, Dict]:
    """Convert session closure to experiment post data using multi-site generator if available."""
    
    # Use multi-site content generator if available
    if MULTI_SITE_GENERATOR_AVAILABLE:
        # Build source payload from closure
        source_payload = f"""
# {closure.task}

**Project:** {closure.project}
**Agent:** {closure.agent_id}

## Actions Taken
{chr(10).join('- ' + action for action in closure.actions)}

## Artifacts
{chr(10).join('- ' + artifact for artifact in closure.artifacts)}

## Verification
{chr(10).join('- ' + verify for verify in closure.verification)}

## Public Build Signal
{closure.public_build_signal}
"""
        
        # Generate multi-site content
        generator = MultiSiteContentGenerator(source_payload=source_payload)
        multi_site_content = generator.generate_all()
        
        # Extract dadudekc.com format
        dadudekc_content = multi_site_content.get('dadudekc', {})
        
        title = dadudekc_content.get('title', f"{closure.task} - {closure.agent_id}")
        hook = dadudekc_content.get('hook', '')
        bullets = dadudekc_content.get('bullets', {})
        resume_delta = dadudekc_content.get('resume_delta', {})
        
        # Build HTML content from structured data
        content_parts = []
        if hook:
            content_parts.append(f"<p class='hook'>{hook}</p>")
        
        if bullets:
            content_parts.append("<div class='bullets'>")
            for key, value in bullets.items():
                if value and value != f"NEEDED_INPUT: {key} from source_payload":
                    content_parts.append(f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value}</p>")
            content_parts.append("</div>")
        
        if resume_delta:
            content_parts.append("<div class='resume-delta'>")
            if resume_delta.get('skills_learned'):
                content_parts.append(f"<p><strong>Skills:</strong> {', '.join(resume_delta['skills_learned'])}</p>")
            if resume_delta.get('artifact_shipped'):
                content_parts.append(f"<p><strong>Shipped:</strong> {resume_delta['artifact_shipped']}</p>")
            content_parts.append("</div>")
        
        content = "\n".join(content_parts) if content_parts else closure.public_build_signal
        
        # Determine experiment status
        if 'complete' in closure.status.lower() or 'ready' in closure.status.lower():
            exp_status = 'shipped'
        elif 'in progress' in closure.status.lower():
            exp_status = 'in-progress'
        else:
            exp_status = 'live'
        
        # Build meta fields
        meta = {
            'experiment_status': exp_status,
            'experiment_learnings': bullets.get('what_i_learned', '') or '\n'.join(closure.verification[:3]) if closure.verification else '',
            'experiment_stats': json.dumps([
                f"Agent: {closure.agent_id}",
                f"Status: {closure.status}",
                f"Artifacts: {len(closure.artifacts)}"
            ]),
        }
        
        return title, content, meta
    
    # Fallback to basic formatting if multi-site generator not available
    title = f"{closure.task} - {closure.agent_id}"
    
    # Build content from closure data
    content_parts = [
        f"<h2>Task</h2><p>{closure.task}</p>",
        f"<h2>Project</h2><p>{closure.project}</p>",
    ]
    
    if closure.actions:
        content_parts.append("<h2>Actions Taken</h2><ul>")
        for action in closure.actions:
            content_parts.append(f"<li>{action}</li>")
        content_parts.append("</ul>")
    
    if closure.artifacts:
        content_parts.append("<h2>Artifacts</h2><ul>")
        for artifact in closure.artifacts:
            content_parts.append(f"<li>{artifact}</li>")
        content_parts.append("</ul>")
    
    if closure.public_build_signal:
        content_parts.append(f"<h2>Public Build Signal</h2><p>{closure.public_build_signal}</p>")
    
    content = "\n".join(content_parts)
    
    # Determine experiment status
    if 'complete' in closure.status.lower() or 'ready' in closure.status.lower():
        exp_status = 'shipped'
    elif 'in progress' in closure.status.lower():
        exp_status = 'in-progress'
    else:
        exp_status = 'live'
    
    # Build meta fields
    meta = {
        'experiment_status': exp_status,
        'experiment_learnings': '\n'.join(closure.verification[:3]) if closure.verification else '',
        'experiment_stats': json.dumps([
            f"Agent: {closure.agent_id}",
            f"Status: {closure.status}",
            f"Artifacts: {len(closure.artifacts)}"
        ]),
    }
    
    return title, content, meta


def session_closure_to_project(closure: SessionClosure) -> Optional[Tuple[str, str, Dict]]:
    """Convert session closure to project post data (if it's a shipped project)."""
    # Only convert if status indicates completion
    if 'ready' not in closure.status.lower() and 'complete' not in closure.status.lower():
        return None
    
    title = closure.project or closure.task
    
    content_parts = [
        f"<h2>Project: {title}</h2>",
        f"<p>{closure.public_build_signal or closure.task}</p>",
    ]
    
    if closure.artifacts:
        content_parts.append("<h2>What Shipped</h2><ul>")
        for artifact in closure.artifacts:
            content_parts.append(f"<li>{artifact}</li>")
        content_parts.append("</ul>")
    
    if closure.verification:
        content_parts.append("<h2>Proof</h2><ul>")
        for verify in closure.verification:
            content_parts.append(f"<li>{verify}</li>")
        content_parts.append("</ul>")
    
    content = "\n".join(content_parts)
    
    # Extract skills from actions/artifacts
    skills = []
    all_text = ' '.join(closure.actions + closure.artifacts).lower()
    tech_keywords = ['wordpress', 'php', 'python', 'javascript', 'react', 'api', 'rest', 'mcp', 'git']
    for keyword in tech_keywords:
        if keyword in all_text:
            skills.append(keyword.title())
    
    meta = {
        'project_status': 'shipped',
        'project_skills': ', '.join(skills) if skills else '',
        'project_proof': '\n'.join(closure.verification[:2]) if closure.verification else '',
    }
    
    return title, content, meta


def devlog_to_blog_post(devlog: Devlog) -> Tuple[str, str]:
    """Convert devlog to blog post data."""
    title = f"{devlog.title} - {devlog.agent_id}"
    content = devlog.content
    return title, content


def process_session_closures(agent_filter: Optional[str] = None, once: bool = False, use_multi_site: bool = True):
    """Process new session closures and create WordPress content for all sites."""
    state = load_state()
    processed = set(state.get('processed_closures', []))
    
    # Find all session closure files
    for agent_dir in AGENT_WORKSPACES.iterdir():
        if not agent_dir.is_dir() or not agent_dir.name.startswith('Agent-'):
            continue
        
        agent_id = agent_dir.name
        if agent_filter and agent_id != agent_filter:
            continue
        
        closures_dir = agent_dir / SESSION_CLOSURES_DIR
        if not closures_dir.exists():
            continue
        
        for closure_file in closures_dir.glob('*.md'):
            file_id = str(closure_file.relative_to(AGENT_WORKSPACES))
            
            if file_id in processed:
                continue
            
            print(f"📄 Processing: {file_id}")
            closure = parse_session_closure(closure_file)
            
            if not closure:
                continue
            
            # Use multi-site content generator if available and enabled
            if use_multi_site and MULTI_SITE_GENERATOR_AVAILABLE:
                # Build source payload from closure
                source_payload = f"""
# {closure.task}

**Project:** {closure.project}
**Agent:** {closure.agent_id}

## Actions Taken
{chr(10).join('- ' + action for action in closure.actions)}

## Artifacts
{chr(10).join('- ' + artifact for artifact in closure.artifacts)}

## Verification
{chr(10).join('- ' + verify for verify in closure.verification)}

## Public Build Signal
{closure.public_build_signal}
"""
                
                # Generate multi-site content
                generator = MultiSiteContentGenerator(source_payload=source_payload)
                multi_site_content = generator.generate_all()
                
                # Post to dadudekc.com (experiment)
                dadudekc_content = multi_site_content.get('dadudekc', {})
                if dadudekc_content:
                    title = dadudekc_content.get('title', f"{closure.task} - {closure.agent_id}")
                    bullets = dadudekc_content.get('bullets', {})
                    content = f"<p>{dadudekc_content.get('hook', '')}</p>"
                    for key, value in bullets.items():
                        if value and not value.startswith('NEEDED_INPUT'):
                            content += f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value}</p>"
                    
                    # Determine experiment status
                    if 'complete' in closure.status.lower() or 'ready' in closure.status.lower():
                        exp_status = 'shipped'
                    else:
                        exp_status = 'live'
                    
                    meta = {
                        'experiment_status': exp_status,
                        'experiment_learnings': bullets.get('what_i_learned', ''),
                    }
                    
                    create_wordpress_post('dadudekc.com', 'experiments', title, content, meta)
                
                # Post to freerideinvestor.com (if trading-related)
                freeride_content = multi_site_content.get('freerideinvestor', {})
                if freeride_content and freeride_content.get('status') != 'blocked':
                    title = freeride_content.get('title', f"{closure.task}")
                    # Format as trading journal post
                    content = f"<h2>Setup</h2><p>{freeride_content.get('setup', {}).get('plan', '')}</p>"
                    content += f"<h2>Execution</h2><p>{freeride_content.get('execution', {}).get('entry', '')}</p>"
                    content += f"<h2>Results</h2><p>{freeride_content.get('results', {}).get('p_l', '')}</p>"
                    create_wordpress_post('freerideinvestor.com', 'posts', title, content)
                
                # Post to tradingrobotplug.com (if trading/backtest-related)
                trp_content = multi_site_content.get('tradingrobotplug', {})
                if trp_content:
                    title = trp_content.get('title', f"{closure.task}")
                    content = f"<h2>Thesis</h2><p>{trp_content.get('thesis', '')}</p>"
                    content += f"<h2>Backtest Summary</h2><p>{trp_content.get('backtest_or_test_summary', '')}</p>"
                    create_wordpress_post('tradingrobotplug.com', 'posts', title, content)
                
                # Post to weareswarm.online (docs + implementation)
                swarm_content = multi_site_content.get('weareswarm_online', {})
                if swarm_content:
                    title = swarm_content.get('title', f"{closure.task}")
                    content = f"<h2>What We Built</h2><p>{swarm_content.get('what_we_built', '')}</p>"
                    content += f"<h2>How It Works</h2><p>{swarm_content.get('how_it_works', '')}</p>"
                    create_wordpress_post('weareswarm.online', 'posts', title, content)
                
            else:
                # Fallback: Basic single-site posting
                title, content, meta = session_closure_to_experiment(closure)
                post_id = create_wordpress_post(
                    'dadudekc.com',
                    'experiments',
                    title,
                    content,
                    meta
                )
                
                if post_id:
                    # Also create project if it's a completed project
                    project_data = session_closure_to_project(closure)
                    if project_data:
                        p_title, p_content, p_meta = project_data
                        create_wordpress_post(
                            'dadudekc.com',
                            'projects',
                            p_title,
                            p_content,
                            p_meta
                        )
            
            processed.add(file_id)
            state['processed_closures'] = list(processed)
            save_state(state)
    
    if once:
        print("✅ One-time check complete")
    else:
        state['last_check'] = datetime.now().isoformat()
        save_state(state)


def process_devlogs(agent_filter: Optional[str] = None, once: bool = False):
    """Process new devlogs and create blog posts."""
    state = load_state()
    processed = set(state.get('processed_devlogs', []))
    
    # Find all devlog files
    for agent_dir in AGENT_WORKSPACES.iterdir():
        if not agent_dir.is_dir() or not agent_dir.name.startswith('Agent-'):
            continue
        
        agent_id = agent_dir.name
        if agent_filter and agent_id != agent_filter:
            continue
        
        devlogs_dir = agent_dir / DEVLOGS_DIR
        if not devlogs_dir.exists():
            continue
        
        for devlog_file in devlogs_dir.glob('*.md'):
            file_id = str(devlog_file.relative_to(AGENT_WORKSPACES))
            
            if file_id in processed:
                continue
            
            print(f"📝 Processing devlog: {file_id}")
            devlog = parse_devlog(devlog_file)
            
            if not devlog:
                continue
            
            # Create blog post (using standard 'post' type)
            title, content = devlog_to_blog_post(devlog)
            post_id = create_wordpress_post(
                'dadudekc.com',
                'posts',  # Standard WordPress post type
                title,
                content
            )
            
            if post_id:
                processed.add(file_id)
                state['processed_devlogs'] = list(processed)
                save_state(state)
    
    if once:
        print("✅ One-time devlog check complete")


def main():
    parser = argparse.ArgumentParser(description='Automate WordPress content from swarm workflows')
    parser.add_argument('--watch', action='store_true', help='Watch mode (continuous)')
    parser.add_argument('--once', action='store_true', help='One-time check')
    parser.add_argument('--agent', help='Filter by agent ID (e.g., Agent-7)')
    parser.add_argument('--devlogs', action='store_true', help='Process devlogs (default: session closures)')
    parser.add_argument('--interval', type=int, default=300, help='Watch interval in seconds (default: 300)')
    parser.add_argument('--no-multi-site', action='store_true', help='Disable multi-site content generation (use basic formatting)')
    
    args = parser.parse_args()
    
    if not args.once and not args.watch:
        args.once = True  # Default to one-time if neither specified
    
    use_multi_site = not args.no_multi_site
    
    if args.devlogs:
        process_func = process_devlogs
        if args.watch:
            print(f"👀 Watching for new devlogs (interval: {args.interval}s)...")
            while True:
                try:
                    process_func(args.agent, once=False)
                    time.sleep(args.interval)
                except KeyboardInterrupt:
                    print("\n👋 Stopping watch mode")
                    break
        else:
            process_func(args.agent, once=True)
    else:
        if args.watch:
            print(f"👀 Watching for new session closures (interval: {args.interval}s)...")
            if use_multi_site and MULTI_SITE_GENERATOR_AVAILABLE:
                print("✅ Multi-site content generation enabled - will post to all 4 sites")
            while True:
                try:
                    process_session_closures(args.agent, once=False, use_multi_site=use_multi_site)
                    time.sleep(args.interval)
                except KeyboardInterrupt:
                    print("\n👋 Stopping watch mode")
                    break
        else:
            process_session_closures(args.agent, once=True, use_multi_site=use_multi_site)


if __name__ == '__main__':
    main()

