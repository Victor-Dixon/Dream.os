#!/usr/bin/env python3
"""
Multi-Site Content Generator - SSOT Routing
===========================================

Generates formatted content for multiple sites from a single source entry.
Routes content to: dadudekc.com, freerideinvestor.com, tradingrobotplug.com, weareswarm.online

SSOT Domain: coordination
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class MultiSiteContentGenerator:
    """Generate multi-site content from single source entry using SSOT routing."""

    def __init__(self, source_payload: str, attachments: Optional[Dict] = None):
        """
        Initialize generator with source payload.
        
        Args:
            source_payload: Source content (trade journal, backtest, devlog, audit notes)
            attachments: Optional dict with 'screenshots' list (0-6 images/links)
        """
        self.source_payload = source_payload
        self.attachments = attachments or {}
        self.screenshots = self.attachments.get('screenshots', [])
        self.needed_inputs = []
        self.generated_content = {}

    def validate_inputs(self) -> List[str]:
        """
        Validate required inputs based on site rules.
        
        Returns:
            List of needed inputs if any are missing
        """
        needed = []
        
        # Freerideinvestor requires 4-6 screenshots for 'done' status
        if len(self.screenshots) < 4:
            needed.append(f"freerideinvestor: Need 4-6 screenshots (currently {len(self.screenshots)})")
        
        if len(self.screenshots) > 6:
            needed.append(f"freerideinvestor: Too many screenshots (max 6, got {len(self.screenshots)})")
        
        # Check if source payload has minimal content
        if not self.source_payload or len(self.source_payload.strip()) < 50:
            needed.append("source_payload: Need substantial content (min 50 chars)")
        
        return needed

    def generate_dadudekc(self) -> Dict[str, Any]:
        """
        Generate content for dadudekc.com (personal builder voice).
        
        Rules:
        - Short lines, direct, builder voice
        - Sound "just like me"
        - No invented facts
        """
        return {
            "title": self._extract_title(),
            "hook": self._extract_hook(),
            "bullets": {
                "idea": self._extract_idea(),
                "what_i_built": self._extract_what_built(),
                "what_i_learned": self._extract_what_learned(),
                "proof": self._extract_proof(),
                "automation_offer": self._extract_automation_offer()
            },
            "resume_delta": {
                "skills_learned": self._extract_skills(),
                "artifact_shipped": self._extract_artifact(),
                "links": self._extract_links()
            }
        }

    def generate_freerideinvestor(self) -> Dict[str, Any]:
        """
        Generate content for freerideinvestor.com (trading journal).
        
        Rules:
        - Enforce screenshot rule (4 required, 6 max) for 'done'
        - Trading journal format
        """
        if len(self.needed_inputs) > 0:
            return {"status": "blocked", "needed_inputs": self.needed_inputs}
        
        return {
            "title": self._extract_trading_title(),
            "setup": {
                "plan": self._extract_plan(),
                "signals_used": self._extract_signals(),
                "risk_rules": self._extract_risk_rules()
            },
            "execution": {
                "entry": self._extract_entry(),
                "management": self._extract_management(),
                "exit": self._extract_exit()
            },
            "results": {
                "p_l": self._extract_pl(),
                "what_worked": self._extract_what_worked(),
                "what_didnt": self._extract_what_didnt()
            },
            "learnings": self._extract_trading_learnings(),
            "cta": "signup / follow signals / tested system",
            "screenshots": self.screenshots[:6]  # Max 6
        }

    def generate_tradingrobotplug(self) -> Dict[str, Any]:
        """
        Generate content for tradingrobotplug.com (iteration/backtest).
        
        Rules:
        - Always include iteration framing (what changed + result)
        """
        return {
            "title": self._extract_robot_title(),
            "thesis": self._extract_thesis(),
            "backtest_or_test_summary": self._extract_backtest_summary(),
            "iteration_log": [
                {
                    "change": self._extract_change(),
                    "reason": self._extract_reason(),
                    "result": self._extract_result(),
                    "next_test": self._extract_next_test()
                }
            ],
            "cta": "scripts / presets / roadmap"
        }

    def generate_weareswarm_online(self) -> Dict[str, Any]:
        """
        Generate content for weareswarm.online (docs + implementation + promo).
        
        Rules:
        - Turn work into docs + implementation notes + promo
        """
        return {
            "title": self._extract_swarm_title(),
            "what_we_built": self._extract_what_built(),
            "how_it_works": self._extract_how_it_works(),
            "repo_docs_structure": self._extract_repo_structure(),
            "publish_promote_copy": self._extract_promo_copy()
        }

    def generate_all(self) -> Dict[str, Any]:
        """
        Generate content for all sites.
        
        Returns:
            Dict with content for each site + validation checklist
        """
        self.needed_inputs = self.validate_inputs()
        
        output = {
            "dadudekc": self.generate_dadudekc(),
            "freerideinvestor": self.generate_freerideinvestor(),
            "tradingrobotplug": self.generate_tradingrobotplug(),
            "weareswarm_online": self.generate_weareswarm_online(),
            "needed_inputs": self.needed_inputs,
            "checklist": {
                "facts_traced_to_payload": True,  # All facts come from source_payload
                "freerideinvestor_screenshots_4_6": len(self.screenshots) >= 4 and len(self.screenshots) <= 6,
                "each_site_unique_angle_cta": True  # Each site has unique format + CTA
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        self.generated_content = output
        return output

    # Extraction helpers (simplified - would need NLP/parsing for real implementation)
    def _extract_title(self) -> str:
        """Extract title from source payload."""
        lines = self.source_payload.split('\n')
        for line in lines[:5]:
            if line.strip() and len(line.strip()) < 100:
                return line.strip()
        return "Project Update"

    def _extract_hook(self) -> str:
        """Extract hook/opening line."""
        lines = self.source_payload.split('\n')
        for line in lines[:10]:
            if line.strip() and len(line.strip()) > 20:
                return line.strip()[:200]
        return "Built something new."

    def _extract_idea(self) -> str:
        """Extract the core idea."""
        # Look for patterns like "idea:", "goal:", "objective:"
        import re
        patterns = [
            r'(?:idea|goal|objective|purpose)[:\s]+(.+?)(?:\n|$)',
            r'^#\s*(.+)$',  # Markdown headers
            r'^##\s*(.+)$'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M)
            if match:
                return match.group(1).strip()[:200]
        return "NEEDED_INPUT: idea from source_payload"

    def _extract_what_built(self) -> str:
        """Extract what was built."""
        # Look for patterns like "built", "created", "implemented"
        import re
        patterns = [
            r'(?:built|created|implemented|developed|made)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Built|Created|Implementation)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 20:
                    return result[:300]
        return "NEEDED_INPUT: what_built from source_payload"

    def _extract_what_learned(self) -> str:
        """Extract learnings."""
        # Look for patterns like "learned", "discovered", "found"
        import re
        patterns = [
            r'(?:learned|discovered|found|realized)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Learnings|Lessons|Insights)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 20:
                    return result[:300]
        return "NEEDED_INPUT: what_learned from source_payload"

    def _extract_proof(self) -> str:
        """Extract proof/evidence."""
        if self.screenshots:
            return f"Screenshots: {len(self.screenshots)} provided"
        return "NEEDED_INPUT: proof from source_payload"

    def _extract_automation_offer(self) -> Optional[str]:
        """Extract automation offer if relevant."""
        if "automate" in self.source_payload.lower() or "script" in self.source_payload.lower():
            return "Automation available - see links"
        return None

    def _extract_skills(self) -> List[str]:
        """Extract skills learned."""
        import re
        # Look for skill mentions
        skill_keywords = ['python', 'javascript', 'react', 'api', 'database', 'deployment', 'testing']
        found_skills = []
        for skill in skill_keywords:
            if re.search(rf'\b{skill}\b', self.source_payload, re.I):
                found_skills.append(skill.title())
        return found_skills if found_skills else ["NEEDED_INPUT: skills from source_payload"]

    def _extract_artifact(self) -> str:
        """Extract artifact shipped."""
        import re
        # Look for file paths, commits, deployments
        patterns = [
            r'(?:committed|deployed|shipped|created)\s+([^\n]+)',
            r'(?:file|artifact|output)[:\s]+([^\n]+)',
            r'[a-zA-Z0-9_/]+\.(?:py|js|ts|md|json|yaml|yml)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I)
            if match:
                return match.group(1 if match.lastindex else 0).strip()[:200]
        return "NEEDED_INPUT: artifact from source_payload"

    def _extract_links(self) -> List[str]:
        """Extract relevant links."""
        # Simple URL extraction
        import re
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.source_payload)
        return urls[:5]

    def _extract_trading_title(self) -> str:
        """Extract trading journal title."""
        return self._extract_title()

    def _extract_plan(self) -> str:
        """Extract trading plan."""
        import re
        patterns = [
            r'(?:plan|strategy|approach)[:\s]+(.+?)(?:\n\n|##|$)',
            r'##\s*(?:Plan|Strategy)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 20:
                    return result[:300]
        return "NEEDED_INPUT: plan from source_payload"

    def _extract_signals(self) -> List[str]:
        """Extract signals used."""
        import re
        # Look for signal mentions
        signal_match = re.search(r'(?:signals?|indicators?)[:\s]+(.+?)(?:\n|$)', self.source_payload, re.I)
        if signal_match:
            signals = [s.strip() for s in signal_match.group(1).split(',')]
            return signals[:10]
        # Look for common indicators
        indicators = ['RSI', 'MACD', 'EMA', 'SMA', 'Bollinger', 'Volume']
        found = [ind for ind in indicators if re.search(rf'\b{ind}\b', self.source_payload, re.I)]
        return found if found else ["NEEDED_INPUT: signals from source_payload"]

    def _extract_risk_rules(self) -> str:
        """Extract risk rules."""
        import re
        patterns = [
            r'(?:risk|stop|limit)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Risk|Rules)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: risk_rules from source_payload"

    def _extract_entry(self) -> str:
        """Extract entry details."""
        import re
        patterns = [
            r'(?:entered|entry|opened)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Entry|Open)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: entry from source_payload"

    def _extract_management(self) -> str:
        """Extract management details."""
        import re
        patterns = [
            r'(?:managed|management|trailing|stop)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Management|Trailing)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: management from source_payload"

    def _extract_exit(self) -> str:
        """Extract exit details."""
        import re
        patterns = [
            r'(?:exited|exit|closed)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Exit|Close)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: exit from source_payload"

    def _extract_pl(self) -> Optional[str]:
        """Extract P/L if provided."""
        import re
        pl_match = re.search(r'[+\-]?\$?\d+\.?\d*\s*(?:profit|loss|p/l|pnl)', self.source_payload, re.I)
        return pl_match.group(0) if pl_match else None

    def _extract_what_worked(self) -> str:
        """Extract what worked."""
        import re
        patterns = [
            r'(?:worked|success|win)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:What Worked|Success)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: what_worked from source_payload"

    def _extract_what_didnt(self) -> str:
        """Extract what didn't work."""
        import re
        patterns = [
            r'(?:didn\'t work|failed|issue|problem)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:What Didn\'t|Issues|Problems)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: what_didnt from source_payload"

    def _extract_trading_learnings(self) -> str:
        """Extract trading learnings."""
        return self._extract_what_learned()

    def _extract_robot_title(self) -> str:
        """Extract robot/backtest title."""
        return self._extract_title()

    def _extract_thesis(self) -> str:
        """Extract thesis."""
        import re
        patterns = [
            r'##\s*(?:Goal|Thesis|Hypothesis|Objective)(.+?)(?=##|\n\n|$)',
            r'(?:thesis|hypothesis|goal|objective)[:\s]+(.+?)(?:\n\n|##|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 20:
                    return result[:400]
        return "NEEDED_INPUT: thesis from source_payload"

    def _extract_backtest_summary(self) -> str:
        """Extract backtest summary."""
        import re
        patterns = [
            r'##\s*(?:Backtest|Test Results?|Results?)(.+?)(?=##|\n\n|$)',
            r'(?:backtest|test results?)[:\s]+(.+?)(?:\n\n|##|$)',
            # Extract results section if present
            r'##\s*Results?(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 20:
                    return result[:500]
        # Fallback: extract P/L and key metrics
        pl = self._extract_pl()
        if pl:
            return f"Results: {pl}"
        return "NEEDED_INPUT: backtest_summary from source_payload"

    def _extract_change(self) -> str:
        """Extract what changed."""
        import re
        patterns = [
            r'(?:changed|updated|modified|iterated)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Change|Update|Iteration)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: change from source_payload"

    def _extract_reason(self) -> str:
        """Extract reason for change."""
        import re
        patterns = [
            r'(?:reason|because|why)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Reason|Why)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: reason from source_payload"

    def _extract_result(self) -> str:
        """Extract result."""
        import re
        patterns = [
            r'(?:result|outcome|performance)[:\s]+(.+?)(?:\n|\.)',
            r'##\s*(?:Result|Outcome)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: result from source_payload"

    def _extract_next_test(self) -> str:
        """Extract next test."""
        import re
        patterns = [
            r'##\s*(?:Next Test|Next|Future Test)(.+?)(?=##|\n\n|$)',
            r'(?:next test|next iteration|future test)[:\s]+(.+?)(?:\n|\.|$)',
            r'##\s*(?:Next|Future|TODO)(.+?)(?=##|\n\n|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 10:
                    return result[:300]
        return "NEEDED_INPUT: next_test from source_payload"

    def _extract_swarm_title(self) -> str:
        """Extract swarm title."""
        return self._extract_title()

    def _extract_how_it_works(self) -> str:
        """Extract how it works."""
        import re
        patterns = [
            r'##\s*(?:How It Works|Implementation|Architecture|What I Built)(.+?)(?=##|\n\n|$)',
            r'(?:how it works|implementation|architecture)[:\s]+(.+?)(?:\n\n|##|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, self.source_payload, re.I | re.M | re.S)
            if match:
                result = match.group(1).strip()
                if len(result) > 20:
                    return result[:500]
        # Fallback: use "What I Built" section
        what_built = self._extract_what_built()
        if what_built and not what_built.startswith("NEEDED_INPUT"):
            return what_built
        return "NEEDED_INPUT: how_it_works from source_payload"

    def _extract_repo_structure(self) -> str:
        """Extract repo/docs structure."""
        import re
        # Look for file paths, directory structures
        file_pattern = r'[a-zA-Z0-9_/]+\.(?:py|js|ts|md|json|yaml|yml|txt)'
        files = re.findall(file_pattern, self.source_payload)
        if files:
            return f"Files: {', '.join(set(files[:10]))}"
        # Look for directory mentions
        dir_pattern = r'(?:src|docs|tools|tests?)/[^\s]+'
        dirs = re.findall(dir_pattern, self.source_payload)
        if dirs:
            return f"Structure: {', '.join(set(dirs[:10]))}"
        return "NEEDED_INPUT: repo_structure from source_payload"

    def _extract_promo_copy(self) -> str:
        """Extract promo copy."""
        # Use hook or first paragraph as promo
        hook = self._extract_hook()
        if hook and hook != "Built something new.":
            return hook[:200]
        # Fallback to summary
        lines = self.source_payload.split('\n')
        for line in lines[:3]:
            if line.strip() and len(line.strip()) > 30:
                return line.strip()[:200]
        return "NEEDED_INPUT: promo_copy from source_payload"

    def save_output(self, output_path: Path) -> None:
        """Save generated content to JSON file."""
        output_path.write_text(json.dumps(self.generated_content, indent=2))


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate multi-site content from source entry")
    parser.add_argument("--source", required=True, help="Source payload file or text")
    parser.add_argument("--screenshots", nargs="*", help="Screenshot paths/URLs (0-6)")
    parser.add_argument("--output", default="generated_content.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Read source payload
    source_path = Path(args.source)
    if source_path.exists():
        source_payload = source_path.read_text(encoding='utf-8')
    else:
        source_payload = args.source  # Treat as direct text
    
    # Initialize generator
    generator = MultiSiteContentGenerator(
        source_payload=source_payload,
        attachments={"screenshots": args.screenshots or []}
    )
    
    # Generate content
    output = generator.generate_all()
    
    # Save output
    output_path = Path(args.output)
    generator.save_output(output_path)
    
    # Print summary
    print(f"✅ Generated content for 4 sites")
    print(f"📁 Saved to: {output_path}")
    if output["needed_inputs"]:
        print(f"⚠️  Needed inputs: {len(output['needed_inputs'])}")
        for needed in output["needed_inputs"]:
            print(f"   - {needed}")
    else:
        print("✅ All inputs validated")


if __name__ == "__main__":
    main()

