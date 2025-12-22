#!/usr/bin/env python3
"""
Audit Website Grade Cards
=========================

<!-- SSOT Domain: web -->

Validates and updates sales funnel grade cards for all websites.
Checks for grade card files, validates structure, and ensures consistency.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-22
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class GradeCardAuditor:
    """Audits website grade cards for sales funnel validation."""

    def __init__(self, websites_dir: Path):
        """Initialize auditor with websites directory."""
        self.websites_dir = Path(websites_dir)
        self.results: List[Dict[str, Any]] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def find_grade_cards(self) -> Dict[str, List[Path]]:
        """Find all grade card files across websites."""
        logger.info("🔍 Scanning for grade card files...")
        grade_cards = {}

        # Common grade card file patterns
        patterns = [
            "*grade*.json",
            "*grade*.md",
            "*funnel*.json",
            "*sales*.json",
            "GRADE_CARD*.json",
            "GRADE_CARD*.md"
        ]

        for website_dir in self.websites_dir.iterdir():
            if not website_dir.is_dir():
                continue

            website_name = website_dir.name
            grade_cards[website_name] = []

            for pattern in patterns:
                for grade_file in website_dir.rglob(pattern):
                    if grade_file.is_file():
                        grade_cards[website_name].append(grade_file)

        return grade_cards

    def validate_grade_card(self, file_path: Path) -> Dict[str, Any]:
        """Validate a single grade card file."""
        result = {
            "file": str(file_path),
            "valid": False,
            "issues": [],
            "warnings": [],
            "structure": {}
        }

        try:
            if file_path.suffix == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    result["structure"] = data
                    result["valid"] = self._validate_json_structure(data)
            elif file_path.suffix == ".md":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    result["structure"] = {"type": "markdown", "length": len(content)}
                    result["valid"] = self._validate_markdown_structure(content)
            else:
                result["issues"].append(f"Unknown file type: {file_path.suffix}")

        except json.JSONDecodeError as e:
            result["issues"].append(f"Invalid JSON: {e}")
        except Exception as e:
            result["issues"].append(f"Error reading file: {e}")

        return result

    def _validate_json_structure(self, data: Dict) -> bool:
        """Validate JSON grade card structure."""
        required_fields = ["website", "grade", "timestamp"]
        has_required = all(field in data for field in required_fields)
        return has_required

    def _validate_markdown_structure(self, content: str) -> bool:
        """Validate markdown grade card structure."""
        has_grade = "grade" in content.lower() or "score" in content.lower()
        has_website = any(
            keyword in content.lower()
            for keyword in ["website", "site", "domain"]
        )
        return has_grade and has_website

    def audit_all_websites(self) -> Dict[str, Any]:
        """Audit grade cards for all websites."""
        logger.info("📊 Starting grade card audit...")

        grade_cards = self.find_grade_cards()
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "websites_audited": len(grade_cards),
            "total_grade_cards": sum(len(cards) for cards in grade_cards.values()),
            "websites": {}
        }

        for website, card_files in grade_cards.items():
            logger.info(f"🔍 Auditing {website}...")
            website_result = {
                "website": website,
                "grade_cards_found": len(card_files),
                "cards": []
            }

            for card_file in card_files:
                card_result = self.validate_grade_card(card_file)
                website_result["cards"].append(card_result)

            valid_cards = sum(1 for c in website_result["cards"] if c["valid"])
            website_result["valid_cards"] = valid_cards
            website_result["invalid_cards"] = len(website_result["cards"]) - valid_cards

            audit_results["websites"][website] = website_result

        return audit_results

    def generate_report(self, results: Dict[str, Any]) -> Path:
        """Generate audit report."""
        reports_dir = project_root / "reports"
        reports_dir.mkdir(exist_ok=True)

        report_file = reports_dir / f"grade_cards_audit_{self.timestamp}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        logger.info(f"✅ Report generated: {report_file}")
        return report_file


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Audit website grade cards"
    )
    parser.add_argument(
        "--websites-dir",
        type=str,
        default=str(Path("D:/websites/websites")),
        help="Path to websites directory"
    )

    args = parser.parse_args()

    auditor = GradeCardAuditor(args.websites_dir)
    results = auditor.audit_all_websites()
    report_file = auditor.generate_report(results)

    print(f"\n✅ Grade card audit complete!")
    print(f"📊 Websites audited: {results['websites_audited']}")
    print(f"📄 Total grade cards: {results['total_grade_cards']}")
    print(f"📝 Report: {report_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

