<!-- SSOT Domain: architecture -->

# Cycle Snapshot System → Blog Integration Brainstorm

**Date:** 2025-12-31  
**Purpose:** Explore integration of cycle snapshot system with websites blog infrastructure  
**Approach:** AI Force Multiplication - Deep exploration of blog integration possibilities

---

## 🎯 Integration Vision

**Goal:**
Automatically publish cycle snapshot reports as blog posts to WordPress sites, enabling:
- Build-in-public transparency
- Historical cycle documentation
- Strategic decision-making visibility
- Automated content generation
- Multi-site publishing (dadudekc.com, weareswarm.online, etc.)

---

## 📊 Current Blog Infrastructure

### Existing Systems

**1. Cycle Accomplishments Blog Generator**
- Location: `tools/cycle_accomplishments/blog_generator.py`
- Generates: Victor-voiced narrative blog posts
- Output: `docs/blog/cycle_accomplishments_YYYY-MM-DD.md`
- Format: Markdown with frontmatter
- Voice: Victor's narrative voice (lowercase, no bullets, reflective)

**2. WordPress Publisher**
- Location: `websites/ops/deployment/publish_with_autoblogger.py`
- Function: Publishes blog posts via WP-CLI over SSH
- Features:
  - Voice pattern processing (Victor's voice)
  - HTML formatting
  - WP-CLI integration
  - SSH deployment
  - Post status (draft/publish)

**3. Voice Profile System**
- Location: `config/voice_profiles/victor_voice_profile.yaml`
- Features:
  - Narrative mode (blog posts)
  - Operational mode (devlogs)
  - Lexicon swaps
  - Formatting rules
  - Tone guidelines

**4. Blog Post Format**
```markdown
---
title: "cycle report: 2025-12-28"
date: 2025-12-28
author: victor
category: devlog
tags: [swarm, cycle-report, build-in-public]
excerpt: "swarm size: 8. shipped: 205. the signal."
---

[Victor-voiced narrative content]
```

---

## 🔄 Integration Architecture

### Option A: Extend Cycle Accomplishments (Recommended)

**Structure:**
```
tools/cycle_accomplishments/
  - data_collector.py (existing)
  - report_generator.py (existing)
  - blog_generator.py (existing - extend)
  - snapshot_generator.py (NEW)
  - status_resetter.py (NEW)
  - blog_publisher.py (NEW - WordPress integration)
  - main.py (extend)
```

**Flow:**
```
1. Generate Cycle Snapshot
   ├─ Collect agent data
   ├─ Collect project data (MASTER_TASK_LOG, git, etc.)
   ├─ Generate snapshot JSON
   ├─ Generate snapshot markdown report
   └─ Reset agent status.json files

2. Generate Blog Post
   ├─ Transform snapshot data to narrative format
   ├─ Apply Victor's voice (narrative mode)
   ├─ Generate markdown with frontmatter
   └─ Save to docs/blog/

3. Publish to WordPress (Optional)
   ├─ Process through voice pattern processor
   ├─ Convert markdown to HTML
   ├─ Publish via WP-CLI over SSH
   └─ Return post URL
```

**Benefits:**
- Reuses existing blog infrastructure
- Single command for snapshot + blog + publish
- Consistent voice and formatting
- Modular, V2 compliant

### Option B: Separate Snapshot Blog Module

**Structure:**
```
tools/cycle_snapshots/
  - snapshot_generator.py
  - blog_generator.py (NEW - snapshot-specific)
  - blog_publisher.py (NEW)
  - main.py
```

**Flow:**
```
1. Generate Snapshot (separate from cycle accomplishments)
2. Generate Snapshot Blog Post (different format)
3. Publish to WordPress
```

**Benefits:**
- Independent from cycle accomplishments
- Can have different blog format
- Separate concerns

**Drawbacks:**
- Duplicate blog infrastructure
- Two different blog post types (confusing?)

**Recommendation: Option A (Extend Existing)**

---

## 📝 Blog Post Formats

### Format 1: Narrative Cycle Snapshot (Victor Voice)

**Style:** Reflective, build-in-public, honest
**Voice:** Victor's narrative mode
**Structure:**
```
cycle snapshot: {date}

swarm reset complete.
cycle {number} closed.

here's what shipped this cycle:

[Agent accomplishments in narrative form]

project state:
- {metric 1}
- {metric 2}
- {metric 3}

what's next:
{strategic next steps in narrative}

closure.
victor.
```

**Example:**
```
cycle snapshot: 2025-12-31

swarm reset complete.
cycle 60 closed.

here's what shipped this cycle:

agent-3 (infrastructure & devops)
shipped:
phase 2a infrastructure refactoring integration complete
phase 2b infrastructure refactoring complete
fastapi deployment complete (28 files)

project state:
- 45 tasks completed this cycle
- 12 achievements unlocked
- 15 git commits, 42 files changed
- week 1 p0 execution: 2/19 complete (11%)

what's next:
complete tradingrobotplug theme deployment
execute remaining tier 1 quick wins
deploy build-in-public phase 0

closure.
victor.
```

### Format 2: Technical Cycle Snapshot (Structured)

**Style:** More structured, data-focused
**Voice:** Victor's operational mode (or hybrid)
**Structure:**
```
# Cycle Snapshot: {date} (Cycle {number})

## Executive Summary
- Agents Active: {count}
- Tasks Completed: {count}
- Achievements: {count}
- Git Activity: {commits} commits, {files} files changed

## Agent Accomplishments
[Structured list per agent]

## Project Metrics
[Data tables, metrics]

## Next Steps
[Priority-ordered actions]

## Closure
Cycle {number} complete. Status files reset. Next cycle begins.
```

**Use Case:** More technical audience, data-focused readers

### Format 3: Hybrid (Recommended)

**Style:** Narrative intro, structured data, narrative conclusion
**Voice:** Victor's narrative mode with structured sections
**Structure:**
```
cycle snapshot: {date}

swarm reset complete.
cycle {number} closed.

here's what shipped:

[Agent accomplishments - narrative]

project metrics:
- tasks: {completed}/{total}
- git: {commits} commits, +{lines} lines
- initiatives: {progress}

what's next:
{strategic narrative}

closure.
victor.
```

**Benefits:**
- Human-readable narrative
- Data for technical readers
- Victor's authentic voice
- Build-in-public transparency

---

## 🎨 Blog Post Content Strategy

### Content Sections

**1. Opening (Narrative)**
- Cycle closure announcement
- Swarm reset confirmation
- Cycle number
- Date

**2. Agent Accomplishments (Narrative + Data)**
- Per-agent shipped items
- Wins/achievements
- Focus/mission context
- Keep it tight (top 5 tasks, top 3 achievements)

**3. Project Metrics (Structured)**
- Task completion counts
- Git activity summary
- Initiative progress
- Health metrics

**4. Project State (Narrative)**
- Active initiatives status
- Blockers (if any)
- Strategic context

**5. Next Steps (Narrative)**
- Priority-ordered actions
- Strategic direction
- What to focus on next

**6. Closure (Narrative)**
- Cycle complete confirmation
- Reset status
- Next cycle begins
- Victor signature

### Content Transformation Rules

**From Snapshot Data → Blog Content:**

```python
def transform_snapshot_to_blog(snapshot_data: dict) -> str:
    """
    Transform cycle snapshot data into Victor-voiced blog post.
    
    Rules:
    1. Narrative mode (lowercase, no bullets, reflective)
    2. Keep accomplishments tight (top 5 tasks, top 3 achievements)
    3. Transform metrics to narrative
    4. Strategic next steps in narrative form
    5. Apply Victor's voice profile
    """
    # Extract data
    date = snapshot_data['snapshot_metadata']['date']
    cycle = snapshot_data['snapshot_metadata']['cycle_number']
    agents = snapshot_data['agent_accomplishments']
    metrics = snapshot_data['project_metrics']
    state = snapshot_data['project_state']
    
    # Build narrative
    content = f"cycle snapshot: {date}\n\n"
    content += f"swarm reset complete.\n"
    content += f"cycle {cycle} closed.\n\n"
    content += "here's what shipped:\n\n"
    
    # Agent accomplishments (narrative)
    for agent_id, agent_data in agents.items():
        agent_name = get_agent_name(agent_id)
        content += f"{agent_id.lower()} ({agent_name.lower()})\n"
        
        # Top 5 completed tasks
        tasks = agent_data.get('completed_tasks', [])[-5:]
        if tasks:
            content += "shipped:\n"
            for task in tasks:
                content += f"{format_task_narrative(task)}\n"
            content += "\n"
        
        # Top 3 achievements
        achievements = agent_data.get('achievements', [])[-3:]
        if achievements:
            content += "wins:\n"
            for ach in achievements:
                content += f"{format_achievement_narrative(ach)}\n"
            content += "\n"
    
    # Project metrics (narrative)
    content += "project metrics:\n"
    content += f"- tasks: {metrics['task_metrics']['completed_this_cycle']}/{metrics['task_metrics']['total_tasks']}\n"
    content += f"- git: {metrics['git_activity']['commits']} commits, +{metrics['git_activity']['net_change']} lines\n"
    content += f"- initiatives: {format_initiatives_narrative(state['active_initiatives'])}\n\n"
    
    # Next steps (narrative)
    content += "what's next:\n"
    for step in state['next_steps'][:5]:  # Top 5
        content += f"{format_next_step_narrative(step)}\n"
    content += "\n"
    
    # Closure
    content += "closure.\n"
    content += "victor.\n"
    
    # Apply Victor's voice
    return apply_victor_voice(content, mode='narrative')
```

---

## 🌐 Multi-Site Publishing Strategy

### Target Sites

**1. weareswarm.online (Build-In-Public)**
- Primary: Cycle snapshot blog posts
- Category: "swarm-cycles" or "build-in-public"
- Tags: [swarm, cycle-snapshot, build-in-public]
- Audience: Build-in-public community

**2. dadudekc.com (Personal/Authority)**
- Secondary: Selected cycle snapshots
- Category: "devlog" or "swarm"
- Tags: [swarm, development, automation]
- Audience: Personal brand, authority building

**3. tradingrobotplug.com (Product/Business)**
- Optional: Technical cycle snapshots
- Category: "development" or "updates"
- Tags: [development, updates, infrastructure]
- Audience: Product users, technical audience

### Publishing Logic

```python
def determine_publish_sites(snapshot_data: dict, config: dict) -> List[str]:
    """
    Determine which sites to publish to based on snapshot content.
    
    Rules:
    - weareswarm.online: Always publish (build-in-public)
    - dadudekc.com: Publish if significant accomplishments
    - tradingrobotplug.com: Publish if infrastructure/product-related
    """
    sites = []
    
    # Always publish to build-in-public site
    sites.append('weareswarm.online')
    
    # Publish to personal site if significant
    if is_significant_snapshot(snapshot_data):
        sites.append('dadudekc.com')
    
    # Publish to product site if relevant
    if has_infrastructure_or_product_content(snapshot_data):
        sites.append('tradingrobotplug.com')
    
    return sites

def is_significant_snapshot(snapshot_data: dict) -> bool:
    """Check if snapshot has significant accomplishments."""
    metrics = snapshot_data['project_metrics']
    return (
        metrics['task_metrics']['completed_this_cycle'] >= 10 or
        metrics['git_activity']['commits'] >= 10 or
        len(snapshot_data['agent_accomplishments']) >= 6
    )

def has_infrastructure_or_product_content(snapshot_data: dict) -> bool:
    """Check if snapshot has infrastructure/product content."""
    # Check agent accomplishments for infrastructure/product keywords
    keywords = ['infrastructure', 'deployment', 'api', 'product', 'feature']
    for agent_data in snapshot_data['agent_accomplishments'].values():
        tasks = ' '.join(agent_data.get('completed_tasks', []))
        if any(keyword in tasks.lower() for keyword in keywords):
            return True
    return False
```

### Site-Specific Customization

**weareswarm.online:**
- Full narrative format
- Build-in-public focus
- All cycle snapshots
- Category: "swarm-cycles"
- Tags: [swarm, cycle-snapshot, build-in-public]

**dadudekc.com:**
- Selected snapshots (significant only)
- Personal/authority angle
- Category: "devlog"
- Tags: [swarm, development, automation]

**tradingrobotplug.com:**
- Technical focus
- Infrastructure/product updates
- Category: "development"
- Tags: [development, updates, infrastructure]

---

## 🔧 Implementation Details

### Blog Generator Module

**File:** `tools/cycle_accomplishments/snapshot_blog_generator.py`

```python
"""
Snapshot Blog Generator Module
===============================

Generates Victor-voiced blog posts from cycle snapshot data.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0 (extended)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from .blog_generator import (
    load_voice_profile,
    apply_victor_voice,
    save_blog_post
)


def transform_snapshot_to_blog_content(
    snapshot_data: Dict[str, Any],
    workspace_root: Optional[Path] = None
) -> str:
    """
    Transform cycle snapshot data into Victor-voiced blog post content.
    
    Args:
        snapshot_data: Complete snapshot JSON data
        workspace_root: Root workspace path for voice profile
    
    Returns:
        Blog post content as string (Victor's narrative voice)
    """
    profile = load_voice_profile(workspace_root)
    
    # Extract metadata
    metadata = snapshot_data['snapshot_metadata']
    date_str = metadata['date']
    cycle_num = metadata['cycle_number']
    
    # Extract accomplishments
    agents = snapshot_data['agent_accomplishments']
    metrics = snapshot_data['project_metrics']
    state = snapshot_data['project_state']
    
    # Build narrative content
    content = f"cycle snapshot: {date_str}\n\n"
    content += f"swarm reset complete.\n"
    content += f"cycle {cycle_num} closed.\n\n"
    content += "here's what shipped:\n\n"
    
    # Agent accomplishments
    for agent_id, agent_data in sorted(agents.items()):
        agent_name = get_agent_name_from_data(agent_data)
        content += f"{agent_id.lower()} ({agent_name.lower()})\n"
        
        # Top 5 completed tasks
        tasks = agent_data.get('completed_tasks', [])[-5:]
        if tasks:
            content += "shipped:\n"
            for task in tasks:
                task_text = format_task_narrative(task)
                if task_text:
                    content += f"{task_text}\n"
            content += "\n"
        
        # Top 3 achievements
        achievements = agent_data.get('achievements', [])[-3:]
        if achievements:
            content += "wins:\n"
            for ach in achievements:
                ach_text = format_achievement_narrative(ach)
                if ach_text:
                    content += f"{ach_text}\n"
            content += "\n"
    
    # Project metrics (narrative)
    content += "project metrics:\n"
    task_metrics = metrics.get('task_metrics', {})
    git_metrics = metrics.get('git_activity', {})
    
    content += f"- tasks: {task_metrics.get('completed_this_cycle', 0)}/{task_metrics.get('total_tasks', 0)}\n"
    content += f"- git: {git_metrics.get('commits', 0)} commits, +{git_metrics.get('net_change', 0)} lines\n"
    
    # Initiatives
    initiatives = state.get('active_initiatives', [])
    if initiatives:
        content += f"- initiatives: {format_initiatives_narrative(initiatives)}\n"
    content += "\n"
    
    # Next steps
    next_steps = state.get('next_steps', [])[:5]
    if next_steps:
        content += "what's next:\n"
        for step in next_steps:
            content += f"{format_next_step_narrative(step)}\n"
        content += "\n"
    
    # Closure
    content += "closure.\n"
    content += "victor.\n"
    
    # Apply Victor's voice
    return apply_victor_voice(content, profile, mode='narrative')


def save_snapshot_blog_post(
    blog_content: str,
    snapshot_data: Dict[str, Any],
    workspace_root: Optional[Path] = None
) -> Path:
    """
    Save cycle snapshot blog post with frontmatter.
    
    Args:
        blog_content: Blog post body content
        snapshot_data: Snapshot data for metadata
        workspace_root: Root workspace path
    
    Returns:
        Path to saved blog post file
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    
    blog_dir = workspace_root / "docs" / "blog"
    blog_dir.mkdir(parents=True, exist_ok=True)
    
    metadata = snapshot_data['snapshot_metadata']
    date_str = metadata['date']
    cycle_num = metadata['cycle_number']
    
    blog_filename = f"cycle_snapshot_{date_str}.md"
    blog_path = blog_dir / blog_filename
    
    # Calculate metrics for excerpt
    metrics = snapshot_data['project_metrics']
    task_metrics = metrics.get('task_metrics', {})
    completed = task_metrics.get('completed_this_cycle', 0)
    achievements = sum(len(a.get('achievements', [])) for a in snapshot_data['agent_accomplishments'].values())
    
    # Create frontmatter
    blog_final_content = f"""---
title: "cycle snapshot: {date_str} (cycle {cycle_num})"
date: {date_str}
author: victor
category: devlog
tags: [swarm, cycle-snapshot, build-in-public]
excerpt: "cycle {cycle_num} closed. {completed} tasks shipped. swarm reset complete."
---

{blog_content}
"""
    
    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(blog_final_content)
    
    return blog_path
```

### Blog Publisher Module

**File:** `tools/cycle_accomplishments/blog_publisher.py`

```python
"""
Blog Publisher Module
=====================

Publishes cycle snapshot blog posts to WordPress sites.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0 (extended)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-31
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import subprocess
import sys


def publish_snapshot_blog_post(
    blog_file: Path,
    sites: List[str],
    workspace_root: Optional[Path] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Publish cycle snapshot blog post to WordPress sites.
    
    Args:
        blog_file: Path to blog post markdown file
        sites: List of site domains to publish to
        workspace_root: Root workspace path
    
    Returns:
        Dict mapping site -> publish result
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    
    # Read blog post
    with open(blog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    frontmatter, body = parse_frontmatter(content)
    title = frontmatter.get('title', 'Cycle Snapshot')
    
    # Publish to each site
    results = {}
    publisher_script = workspace_root / "websites" / "ops" / "deployment" / "publish_with_autoblogger.py"
    
    for site in sites:
        try:
            # Call publish script
            result = subprocess.run(
                [
                    sys.executable,
                    str(publisher_script),
                    '--site', site,
                    '--title', title,
                    '--file', str(blog_file),
                    '--status', 'publish'
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            results[site] = {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'url': extract_post_url(result.stdout) if result.returncode == 0 else None
            }
            
        except Exception as e:
            results[site] = {
                'success': False,
                'error': str(e)
            }
    
    return results


def determine_publish_sites(snapshot_data: Dict[str, Any]) -> List[str]:
    """
    Determine which sites to publish to based on snapshot content.
    
    Args:
        snapshot_data: Snapshot data
    
    Returns:
        List of site domains
    """
    sites = ['weareswarm.online']  # Always publish to build-in-public
    
    # Add other sites based on content
    if is_significant_snapshot(snapshot_data):
        sites.append('dadudekc.com')
    
    if has_infrastructure_content(snapshot_data):
        sites.append('tradingrobotplug.com')
    
    return sites
```

### Main Integration

**File:** `tools/cycle_accomplishments/main.py` (extend)

```python
# Add to main() function:

# Generate snapshot blog post (if requested)
blog_path = None
if not args.no_blog:
    print("✍️  Generating snapshot blog post (Victor voice)...")
    
    blog_content = transform_snapshot_to_blog_content(
        snapshot_data,  # From snapshot generation
        workspace_root=workspace_root
    )
    
    blog_path = save_snapshot_blog_post(
        blog_content,
        snapshot_data,
        workspace_root=workspace_root
    )
    print(f"📝 Blog post saved to: {blog_path}")

# Publish to WordPress (if requested)
if not args.no_publish and blog_path:
    print("🌐 Publishing to WordPress sites...")
    
    sites = determine_publish_sites(snapshot_data)
    publish_results = publish_snapshot_blog_post(
        blog_path,
        sites,
        workspace_root=workspace_root
    )
    
    for site, result in publish_results.items():
        if result['success']:
            print(f"✅ Published to {site}: {result.get('url', 'N/A')}")
        else:
            print(f"⚠️  Failed to publish to {site}: {result.get('error', 'Unknown error')}")
```

---

## 🎯 Publishing Workflow

### Automated Publishing Flow

```
1. SNAPSHOT GENERATION
   ├─ Collect all data
   ├─ Generate snapshot JSON
   ├─ Generate snapshot markdown report
   └─ Reset agent status.json files

2. BLOG POST GENERATION
   ├─ Transform snapshot to narrative format
   ├─ Apply Victor's voice
   ├─ Generate markdown with frontmatter
   └─ Save to docs/blog/

3. PUBLISHING DECISION
   ├─ Determine target sites (weareswarm.online always)
   ├─ Check if significant (for dadudekc.com)
   ├─ Check if infrastructure-related (for tradingrobotplug.com)
   └─ Generate site list

4. WORDPRESS PUBLISHING
   ├─ For each site:
   │   ├─ Process through voice pattern processor
   │   ├─ Convert markdown to HTML
   │   ├─ Publish via WP-CLI over SSH
   │   └─ Capture post URL
   └─ Log results

5. POST-PUBLISH
   ├─ Update snapshot with published URLs
   ├─ Log publishing results
   └─ Report completion
```

### Manual Publishing Option

```bash
# Generate snapshot and blog, but don't publish
python -m tools.cycle_accomplishments.main --no-publish

# Publish existing blog post manually
python websites/ops/deployment/publish_with_autoblogger.py \
  --site weareswarm.online \
  --title "cycle snapshot: 2025-12-31" \
  --file docs/blog/cycle_snapshot_2025-12-31.md
```

---

## 📊 Blog Post Analytics

### Track Publishing Success

**Add to Snapshot JSON:**
```json
{
  "snapshot_metadata": {
    ...
    "blog_published": true,
    "blog_publish_timestamp": "2025-12-31T10:15:00.000000+00:00",
    "blog_publish_sites": ["weareswarm.online", "dadudekc.com"],
    "blog_post_urls": {
      "weareswarm.online": "https://weareswarm.online/cycle-snapshot-2025-12-31/",
      "dadudekc.com": "https://dadudekc.com/devlog/cycle-snapshot-2025-12-31/"
    }
  }
}
```

### Blog Post Performance

**Track:**
- Views per post
- Engagement (comments, shares)
- Traffic from blog posts
- Conversion from blog to product

**Integration:**
- GA4 event tracking
- WordPress analytics
- Custom tracking

---

## 🚀 Benefits

### For Build-In-Public

- **Transparency:** Complete cycle visibility
- **Authenticity:** Victor's honest voice
- **Consistency:** Regular cycle updates
- **Community:** Engages build-in-public audience

### For Strategic Planning

- **Documentation:** Historical cycle records
- **Decision Support:** Data-driven next cycle planning
- **Accountability:** Public commitment to next steps
- **Learning:** Patterns visible over time

### For SEO/Content

- **Regular Content:** Consistent blog posting
- **Long-tail Keywords:** Cycle, swarm, build-in-public
- **Internal Linking:** Link between cycle posts
- **Authority Building:** Demonstrates consistent execution

### For Automation

- **Zero Manual Work:** Fully automated
- **Consistent Format:** Same structure every time
- **Multi-Site:** Publish to multiple sites automatically
- **Voice Consistency:** Victor's voice applied automatically

---

## 🎨 Content Customization Options

### Site-Specific Variations

**weareswarm.online (Build-In-Public):**
- Full narrative
- All cycles
- Community-focused
- Build-in-public tags

**dadudekc.com (Personal):**
- Selected cycles (significant only)
- Personal angle
- Authority building
- Development tags

**tradingrobotplug.com (Product):**
- Technical focus
- Infrastructure/product updates
- User-facing
- Product tags

### Format Variations

**Option 1: Full Narrative (Default)**
- Victor's narrative voice
- All sections
- Build-in-public style

**Option 2: Technical Summary**
- More structured
- Data-focused
- Technical audience

**Option 3: Executive Summary**
- High-level only
- Strategic focus
- Leadership audience

---

## 🔧 CLI Options

### Extended CLI

```bash
# Generate snapshot + blog + publish (default)
python -m tools.cycle_accomplishments.main

# Generate snapshot + blog, but don't publish
python -m tools.cycle_accomplishments.main --no-publish

# Generate snapshot only (no blog)
python -m tools.cycle_accomplishments.main --no-blog

# Publish to specific sites only
python -m tools.cycle_accomplishments.main --sites weareswarm.online,dadudekc.com

# Publish as draft (review before publishing)
python -m tools.cycle_accomplishments.main --draft

# Skip voice processing (use raw content)
python -m tools.cycle_accomplishments.main --skip-voice
```

---

## 📝 Next Steps

1. **Review Integration Approach** - Confirm Option A (extend existing)
2. **Design Blog Format** - Finalize narrative structure
3. **Implement Blog Generator** - Create snapshot_blog_generator.py
4. **Implement Publisher** - Create blog_publisher.py
5. **Test Publishing** - Test with one site first
6. **Multi-Site Testing** - Test with all target sites
7. **Documentation** - Update protocol docs
8. **Deploy** - Integrate into workflow

---

**Status:** 🧠 BRAINSTORMING COMPLETE  
**Ready for:** Review, prioritization, implementation planning  
**Next:** Implementation design

