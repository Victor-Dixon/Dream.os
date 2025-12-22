#!/usr/bin/env python3
"""
Generate Digital Dreamscape Daily Episode

Extracts cycle accomplishments from agent work, uses Ollama to generate
narrative, and creates a blog post for Digital Dreamscape.

Usage:
    python tools/generate_daily_episode.py [--date YYYY-MM-DD]

Output:
    digitaldreamscape.site/blog/XXX-daily-episode-YYYY-MM-DD.md
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class CycleAccomplishmentsExtractor:
    """Extracts cycle accomplishments from agent status files."""

    def __init__(self, workspaces_dir: Path):
        """Initialize extractor with workspaces directory."""
        self.workspaces_dir = Path(workspaces_dir)
        self.accomplishments: List[Dict] = []

    def load_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Load agent status.json file."""
        status_file = self.workspaces_dir / agent_id / "status.json"
        if not status_file.exists():
            return None
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {status_file}: {e}")
            return None

    def extract_accomplishments(self, target_date: Optional[str] = None) -> List[Dict]:
        """Extract accomplishments from all agents for target date."""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")

        accomplishments = []
        agent_ids = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-5",
            "Agent-6", "Agent-7", "Agent-8"
        ]

        for agent_id in agent_ids:
            status = self.load_agent_status(agent_id)
            if not status:
                continue

            agent_name = status.get("agent_name", agent_id)
            last_updated = status.get("last_updated", "")

            # Extract completed tasks
            completed_tasks = status.get("completed_tasks", [])
            if completed_tasks:
                accomplishments.append({
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "type": "completed_tasks",
                    "content": completed_tasks,
                    "timestamp": last_updated
                })

            # Extract achievements
            achievements = status.get("achievements", [])
            if achievements:
                accomplishments.append({
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "type": "achievements",
                    "content": achievements,
                    "timestamp": last_updated
                })

            # Extract contract completions
            contract_status = status.get("contract_status", {})
            if contract_status.get("status") == "✅ COMPLETE":
                accomplishments.append({
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "type": "contract_completion",
                    "content": {
                        "contract": contract_status.get("current_contract", ""),
                        "deliverables": contract_status.get("deliverables", [])
                    },
                    "timestamp": last_updated
                })

        return accomplishments


class OllamaNarrativeGenerator:
    """Generates narrative from cycle accomplishments using Ollama."""

    def __init__(self, model: str = "mistral"):
        """Initialize with Ollama model name."""
        self.model = model

    def generate_narrative(self, accomplishments: List[Dict]) -> str:
        """Generate narrative from accomplishments."""
        # Format accomplishments for prompt
        accomplishments_text = self._format_accomplishments(accomplishments)

        prompt = f"""You are Thea, the Narrative + Coherence Authority of the Digital Dreamscape.

Generate a daily episode narrative from the following cycle accomplishments. Write in the style of the Digital Dreamscape blog posts - narrative, engaging, showing how the Swarm's work becomes story.

Format as a blog post with:
- Title
- Date
- Narrative introduction
- Main story (weave accomplishments into narrative)
- Conclusion (what this means for the Digital Dreamscape)

Tone: Reflective, meaningful, showing how execution becomes narrative. Make it feel like a living world where work has meaning.

Accomplishments:
{accomplishments_text}

Generate the full blog post now:"""

        try:
            import subprocess
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Ollama error: {result.stderr}")
                return self._fallback_narrative(accomplishments)
        except FileNotFoundError:
            logger.warning("Ollama not found, using fallback narrative")
            return self._fallback_narrative(accomplishments)
        except Exception as e:
            logger.error(f"Error generating narrative: {e}")
            return self._fallback_narrative(accomplishments)

    def _format_accomplishments(self, accomplishments: List[Dict]) -> str:
        """Format accomplishments for prompt."""
        formatted = []
        for acc in accomplishments:
            agent_name = acc.get("agent_name", acc.get("agent_id", ""))
            acc_type = acc.get("type", "")
            content = acc.get("content", [])

            if acc_type == "completed_tasks":
                formatted.append(f"{agent_name} completed tasks:")
                for task in content[:5]:  # Limit to 5 tasks
                    formatted.append(f"  - {task}")
            elif acc_type == "achievements":
                formatted.append(f"{agent_name} achievements:")
                for achievement in content[:3]:  # Limit to 3 achievements
                    formatted.append(f"  - {achievement}")
            elif acc_type == "contract_completion":
                contract = content.get("contract", "")
                formatted.append(f"{agent_name} completed contract: {contract}")

        return "\n".join(formatted)

    def _fallback_narrative(self, accomplishments: List[Dict]) -> str:
        """Generate fallback narrative if Ollama fails."""
        date = datetime.now().strftime("%Y-%m-%d")
        title = f"Daily Episode - {date}"

        narrative = f"""# {title}

**Date**: {date}

---

## The Swarm's Work Becomes Story

Today in the Digital Dreamscape, the Swarm continued building. Their work, their coordination, their achievements - all become part of the living narrative.

"""

        # Group by agent
        by_agent = {}
        for acc in accomplishments:
            agent_id = acc.get("agent_id", "Unknown")
            if agent_id not in by_agent:
                by_agent[agent_id] = []
            by_agent[agent_id].append(acc)

        for agent_id, agent_accs in by_agent.items():
            agent_name = agent_accs[0].get("agent_name", agent_id)
            narrative += f"\n### {agent_name}\n\n"
            for acc in agent_accs:
                if acc.get("type") == "contract_completion":
                    contract = acc.get("content", {}).get("contract", "")
                    narrative += f"Completed contract: {contract}\n\n"

        narrative += """
---

*This is how execution becomes narrative. This is how work becomes story. This is the Digital Dreamscape.*

*Generated by the canon automation system*
"""

        return narrative


class DigitalDreamscapeBlogger:
    """Creates blog posts for Digital Dreamscape."""

    def __init__(self, blog_dir: Path):
        """Initialize with blog directory."""
        self.blog_dir = Path(blog_dir)

    def create_episode(self, narrative: str, date: Optional[str] = None) -> Path:
        """Create blog post from narrative."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Find next episode number
        existing_posts = list(self.blog_dir.glob("*.md"))
        episode_num = len([p for p in existing_posts if p.name.startswith("0")]) + 1
        episode_num_str = f"{episode_num:03d}"

        filename = f"{episode_num_str}-daily-episode-{date}.md"
        filepath = self.blog_dir / filename

        # Ensure narrative has proper frontmatter
        if not narrative.startswith("---"):
            narrative = f"""---
title: Daily Episode - {date}
date: {date}
episode: {episode_num}
---

{narrative}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(narrative)

        logger.info(f"✅ Created episode: {filepath}")
        return filepath


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Digital Dreamscape daily episode")
    parser.add_argument(
        "--date",
        type=str,
        help="Target date (YYYY-MM-DD), defaults to today"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="mistral",
        help="Ollama model to use (default: mistral)"
    )
    parser.add_argument(
        "--workspaces",
        type=str,
        default=str(project_root / "agent_workspaces"),
        help="Path to agent workspaces directory"
    )
    parser.add_argument(
        "--blog-dir",
        type=str,
        default=str(Path("D:/websites/websites/digitaldreamscape.site/blog")),
        help="Path to Digital Dreamscape blog directory"
    )

    args = parser.parse_args()

    # Extract accomplishments
    logger.info("📊 Extracting cycle accomplishments...")
    extractor = CycleAccomplishmentsExtractor(args.workspaces)
    accomplishments = extractor.extract_accomplishments(args.date)
    logger.info(f"✅ Found {len(accomplishments)} accomplishments")

    if not accomplishments:
        logger.warning("⚠️  No accomplishments found, generating minimal episode")
        accomplishments = [{
            "agent_id": "System",
            "agent_name": "System",
            "type": "status",
            "content": ["System check - all agents operational"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]

    # Generate narrative
    logger.info("📝 Generating narrative with Ollama...")
    generator = OllamaNarrativeGenerator(model=args.model)
    narrative = generator.generate_narrative(accomplishments)
    logger.info("✅ Narrative generated")

    # Create blog post
    logger.info("📰 Creating blog post...")
    blogger = DigitalDreamscapeBlogger(args.blog_dir)
    episode_path = blogger.create_episode(narrative, args.date)
    logger.info(f"✅ Episode created: {episode_path}")

    print(f"\n✅ Daily episode generated: {episode_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

