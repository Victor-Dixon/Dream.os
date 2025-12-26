#!/usr/bin/env python3
"""
Unified Website Audit Tool
==========================

Comprehensive website audit tool combining:
- Grade card YAML-based scoring (from comprehensive_grade_card_audit.py)
- Real-time website analysis (from enhanced_grade_card_audit.py)
- Technical metrics (performance, SEO, accessibility, conversion, mobile)

This unified tool replaces:
- comprehensive_grade_card_audit.py (DEPRECATED)
- enhanced_grade_card_audit.py (DEPRECATED)
- improved_grade_card_audit.py (DEPRECATED)

V2 Compliance: Modular design, single responsibility per method
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-25
"""

import json
import logging
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class UnifiedWebsiteAuditor:
    """Unified website auditor combining grade card and real-time analysis."""

    def __init__(self, websites_dir: Path = None, output_dir: Path = None):
        """Initialize auditor with directories."""
        self.websites_dir = websites_dir or project_root / "websites" / "websites"
        self.websites_dir = Path(self.websites_dir)
        self.output_dir = output_dir or project_root / "reports"
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def find_grade_card(self, website_dir: Path) -> Optional[Path]:
        """Find grade card file for a website."""
        patterns = [
            "GRADE_CARD_SALES_FUNNEL.yaml",
            "GRADE_CARD*.yaml",
            "GRADE_CARD*.yml",
            "*gradecard*.yaml",
            "*gradecard*.yml"
        ]

        for pattern in patterns:
            for grade_file in website_dir.rglob(pattern):
                if grade_file.is_file():
                    return grade_file
        return None

    def load_grade_card(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse grade card YAML file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data.get("gradecard", data)
        except Exception as e:
            logger.error(f"Error loading grade card {file_path}: {e}")
            return {}

    def analyze_website_real_time(self, url: str) -> Dict[str, Any]:
        """Analyze website in real-time for technical metrics."""
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            
            analysis = {
                "url": url,
                "status_code": response.status_code,
                "load_time": response.elapsed.total_seconds(),
                "page_size_kb": len(html) / 1024,
                "has_meta_description": bool(soup.find('meta', attrs={'name': 'description'})),
                "has_open_graph": bool(soup.find('meta', attrs={'property': 'og:title'})),
                "has_twitter_card": bool(soup.find('meta', attrs={'name': 'twitter:card'})),
                "has_canonical": bool(soup.find('link', attrs={'rel': 'canonical'})),
                "h1_count": len(soup.find_all('h1')),
                "h1_text": soup.find('h1').get_text(strip=True) if soup.find('h1') else None,
                "has_schema_org": bool(soup.find('script', attrs={'type': 'application/ld+json'})),
                "form_count": len(soup.find_all('form')),
                "image_count": len(soup.find_all('img')),
                "images_with_alt": len([img for img in soup.find_all('img') if img.get('alt')]),
                "has_analytics": self._check_analytics(html),
                "has_ga4": 'gtag' in html.lower() or 'gtm' in html.lower(),
                "has_pixel": 'fbevents' in html.lower() or 'pixel' in html.lower(),
                "has_chat_widget": self._check_chat_widget(html),
                "mobile_friendly_check": self._check_mobile_viewport(soup),
            }
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing {url}: {e}")
            return {"url": url, "error": str(e)}

    def _check_analytics(self, html: str) -> Dict[str, bool]:
        """Check for various analytics implementations."""
        html_lower = html.lower()
        return {
            "google_analytics": 'ga(' in html_lower or 'google-analytics' in html_lower,
            "google_tag_manager": 'gtm' in html_lower or 'googletagmanager' in html_lower,
            "facebook_pixel": 'fbevents' in html_lower,
            "pinterest_pixel": 'pinimg.com' in html_lower and 'pinit.js' in html_lower,
        }

    def _check_chat_widget(self, html: str) -> bool:
        """Check for chat widgets."""
        html_lower = html.lower()
        chat_indicators = ['intercom', 'crisp', 'tawk.to', 'drift', 'zendesk', 'livechat']
        return any(indicator in html_lower for indicator in chat_indicators)

    def _check_mobile_viewport(self, soup: BeautifulSoup) -> bool:
        """Check if mobile viewport meta tag exists."""
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return viewport is not None

    def calculate_grade_card_score(self, category: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate score for a grade card category."""
        criteria = category.get("criteria", [])
        weight = category.get("weight_points", 0)
        
        total_score = 0
        max_score = len(criteria) * 5  # 0-5 scale per criterion
        
        scored_criteria = []
        for criterion in criteria:
            score = criterion.get("score_0_to_5", 0)
            total_score += score
            scored_criteria.append({
                "id": criterion.get("id", ""),
                "name": criterion.get("name", ""),
                "score": score,
                "max_score": 5,
                "evidence": criterion.get("evidence", ""),
                "gap": criterion.get("gap", ""),
                "fix": criterion.get("fix", ""),
                "priority": criterion.get("priority", "P2")
            })

        category_score = (total_score / max_score * 100) if max_score > 0 else 0
        weighted_score = (category_score / 100) * weight

        return {
            "category_name": category.get("name", ""),
            "weight_points": weight,
            "criteria_count": len(criteria),
            "total_score": total_score,
            "max_score": max_score,
            "category_score_percent": round(category_score, 2),
            "weighted_score": round(weighted_score, 2),
            "criteria": scored_criteria
        }

    def calculate_technical_metrics(self, real_time_analysis: Dict) -> Dict[str, Any]:
        """Calculate technical metrics from real-time analysis."""
        return {
            "performance": {
                "load_time_seconds": real_time_analysis.get("load_time", 0),
                "page_size_kb": real_time_analysis.get("page_size_kb", 0),
                "score": self._score_performance(real_time_analysis)
            },
            "seo": {
                "meta_description": real_time_analysis.get("has_meta_description", False),
                "open_graph": real_time_analysis.get("has_open_graph", False),
                "twitter_card": real_time_analysis.get("has_twitter_card", False),
                "canonical": real_time_analysis.get("has_canonical", False),
                "h1_count": real_time_analysis.get("h1_count", 0),
                "h1_proper": real_time_analysis.get("h1_count", 0) == 1,
                "schema_org": real_time_analysis.get("has_schema_org", False),
                "score": self._score_seo(real_time_analysis)
            },
            "accessibility": {
                "images_with_alt": real_time_analysis.get("images_with_alt", 0),
                "total_images": real_time_analysis.get("image_count", 0),
                "alt_text_coverage": (real_time_analysis.get("images_with_alt", 0) / 
                                    max(real_time_analysis.get("image_count", 1), 1) * 100),
                "score": self._score_accessibility(real_time_analysis)
            },
            "conversion": {
                "form_count": real_time_analysis.get("form_count", 0),
                "has_chat": real_time_analysis.get("has_chat_widget", False),
                "has_analytics_tracking": bool(real_time_analysis.get("has_analytics", {})),
                "has_ga4": real_time_analysis.get("has_ga4", False),
                "has_pixel": real_time_analysis.get("has_pixel", False),
                "score": self._score_conversion(real_time_analysis)
            },
            "mobile": {
                "viewport_meta": real_time_analysis.get("mobile_friendly_check", False),
                "score": self._score_mobile(real_time_analysis)
            }
        }

    def _score_performance(self, analysis: Dict) -> float:
        """Score performance metrics (0-100)."""
        load_time = analysis.get("load_time", 10)
        page_size = analysis.get("page_size_kb", 5000)
        
        if load_time < 2:
            time_score = 100
        elif load_time < 3:
            time_score = 80
        elif load_time < 5:
            time_score = 60
        elif load_time < 10:
            time_score = 40
        else:
            time_score = 20
        
        if page_size < 500:
            size_score = 100
        elif page_size < 1000:
            size_score = 80
        elif page_size < 2000:
            size_score = 60
        else:
            size_score = 40
        
        return (time_score + size_score) / 2

    def _score_seo(self, analysis: Dict) -> float:
        """Score SEO metrics (0-100)."""
        checks = [
            analysis.get("has_meta_description", False),
            analysis.get("has_open_graph", False),
            analysis.get("has_twitter_card", False),
            analysis.get("has_canonical", False),
            analysis.get("h1_count", 0) == 1,
            analysis.get("has_schema_org", False),
        ]
        return (sum(checks) / len(checks)) * 100

    def _score_accessibility(self, analysis: Dict) -> float:
        """Score accessibility metrics (0-100)."""
        images_with_alt = analysis.get("images_with_alt", 0)
        total_images = max(analysis.get("image_count", 1), 1)
        coverage = (images_with_alt / total_images) * 100
        return min(coverage, 100)

    def _score_conversion(self, analysis: Dict) -> float:
        """Score conversion optimization metrics (0-100)."""
        checks = [
            analysis.get("form_count", 0) > 0,
            analysis.get("has_chat_widget", False),
            analysis.get("has_ga4", False),
            analysis.get("has_pixel", False),
        ]
        return (sum(checks) / len(checks)) * 100

    def _score_mobile(self, analysis: Dict) -> float:
        """Score mobile optimization (0-100)."""
        return 100 if analysis.get("mobile_friendly_check", False) else 0

    def _calculate_letter_grade(self, score: float) -> str:
        """Calculate letter grade from score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def _generate_recommendations(self, real_time: Dict, tech_metrics: Dict, 
                                  grade_card_result: Dict = None) -> List[Dict[str, Any]]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Performance recommendations
        if tech_metrics["performance"]["score"] < 70:
            recommendations.append({
                "category": "Performance",
                "priority": "HIGH",
                "issue": f"Load time: {real_time.get('load_time', 0):.2f}s, Page size: {real_time.get('page_size_kb', 0):.1f}KB",
                "recommendation": "Optimize images, enable caching, minimize CSS/JS, use CDN"
            })
        
        # SEO recommendations
        if not real_time.get("has_meta_description"):
            recommendations.append({
                "category": "SEO",
                "priority": "HIGH",
                "issue": "Missing meta description",
                "recommendation": "Add compelling meta description (150-160 chars)"
            })
        
        if real_time.get("h1_count", 0) != 1:
            recommendations.append({
                "category": "SEO",
                "priority": "MEDIUM",
                "issue": f"H1 count: {real_time.get('h1_count', 0)} (should be 1)",
                "recommendation": "Ensure single H1 heading on homepage"
            })
        
        # Accessibility recommendations
        if tech_metrics["accessibility"]["score"] < 80:
            recommendations.append({
                "category": "Accessibility",
                "priority": "MEDIUM",
                "issue": f"Alt text coverage: {tech_metrics['accessibility']['alt_text_coverage']:.1f}%",
                "recommendation": "Add alt text to all images (use empty alt='' for decorative images)"
            })
        
        # Conversion recommendations
        if not real_time.get("has_chat_widget"):
            recommendations.append({
                "category": "Conversion",
                "priority": "MEDIUM",
                "issue": "No chat widget detected",
                "recommendation": "Add chat widget (Intercom, Crisp, Tawk.to) to reduce friction"
            })
        
        if not real_time.get("has_ga4"):
            recommendations.append({
                "category": "Analytics",
                "priority": "HIGH",
                "issue": "GA4 not detected",
                "recommendation": "Install Google Analytics 4 for conversion tracking"
            })
        
        # Add grade card recommendations if available
        if grade_card_result:
            for cat_result in grade_card_result.get("categories", []):
                for criterion in cat_result.get("criteria", []):
                    if criterion.get("score", 5) < 3:
                        recommendations.append({
                            "category": cat_result.get("category_name", "Unknown"),
                            "priority": criterion.get("priority", "P2"),
                            "issue": criterion.get("gap", ""),
                            "recommendation": criterion.get("fix", "")
                        })
        
        return recommendations

    def audit_website(self, website_name: str, url: str = None) -> Dict[str, Any]:
        """Perform unified audit on a single website."""
        logger.info(f"🔍 Auditing {website_name}...")
        
        # Get URL
        if not url:
            url = f"https://{website_name}"
        
        result = {
            "website": website_name,
            "url": url,
            "audit_date": datetime.now().isoformat(),
            "status": "complete"
        }
        
        # Real-time analysis
        real_time = self.analyze_website_real_time(url)
        result["real_time_analysis"] = real_time
        
        # Technical metrics
        tech_metrics = self.calculate_technical_metrics(real_time)
        result["technical_metrics"] = tech_metrics
        
        # Grade card analysis (if available)
        website_dir = self.websites_dir / website_name
        grade_card_result = None
        
        if website_dir.exists():
            grade_card_path = self.find_grade_card(website_dir)
            if grade_card_path:
                grade_card = self.load_grade_card(grade_card_path)
                if grade_card:
                    categories = grade_card.get("categories", [])
                    category_results = []
                    total_weighted_score = 0
                    total_weight = 0
                    
                    for category in categories:
                        cat_result = self.calculate_grade_card_score(category)
                        category_results.append(cat_result)
                        total_weighted_score += cat_result["weighted_score"]
                        total_weight += cat_result["weight_points"]
                    
                    grade_card_score = (total_weighted_score / total_weight * 100) if total_weight > 0 else 0
                    
                    grade_card_result = {
                        "grade_card_path": str(grade_card_path),
                        "categories": category_results,
                        "grade_card_score": round(grade_card_score, 2),
                        "letter_grade": self._calculate_letter_grade(grade_card_score),
                        "total_weight": total_weight
                    }
                    result["grade_card"] = grade_card_result
        
        # Calculate overall score (combine grade card and technical metrics)
        scores = [tech_metrics["performance"]["score"],
                  tech_metrics["seo"]["score"],
                  tech_metrics["accessibility"]["score"],
                  tech_metrics["conversion"]["score"],
                  tech_metrics["mobile"]["score"]]
        
        if grade_card_result:
            scores.append(grade_card_result["grade_card_score"])
        
        overall_score = sum(scores) / len(scores)
        result["overall_score"] = round(overall_score, 2)
        result["letter_grade"] = self._calculate_letter_grade(overall_score)
        
        # Generate recommendations
        result["recommendations"] = self._generate_recommendations(
            real_time, tech_metrics, grade_card_result
        )
        
        return result

    def audit_all_websites(self, website_configs: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Audit all specified websites or discover them."""
        if website_configs is None:
            # Discover websites
            website_configs = []
            if self.websites_dir.exists():
                for website_dir in self.websites_dir.iterdir():
                    if website_dir.is_dir():
                        website_configs.append({
                            "name": website_dir.name,
                            "url": f"https://{website_dir.name}"
                        })
        
        logger.info(f"📊 Starting unified audit for {len(website_configs)} websites...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "audit_type": "unified_website_audit",
            "websites_audited": len(website_configs),
            "websites": {}
        }
        
        for config in website_configs:
            website_name = config.get("name", "")
            url = config.get("url", f"https://{website_name}")
            result = self.audit_website(website_name, url)
            results["websites"][website_name] = result
        
        # Calculate summary statistics
        scores = [
            w.get("overall_score", 0) 
            for w in results["websites"].values()
            if w.get("status") == "complete"
        ]
        results["average_score"] = round(sum(scores) / len(scores), 2) if scores else 0
        
        return results

    def generate_report(self, results: Dict[str, Any]) -> Path:
        """Generate unified audit report."""
        report_file = self.output_dir / f"unified_website_audit_{self.timestamp}.json"
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"✅ Unified report generated: {report_file}")
        return report_file


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Website Audit Tool")
    parser.add_argument("--websites-dir", type=str,
                       help="Directory containing website folders")
    parser.add_argument("--output-dir", type=str,
                       help="Output directory for reports")
    parser.add_argument("--websites", nargs="+",
                       help="Specific websites to audit (format: name:url or just name)")
    
    args = parser.parse_args()
    
    auditor = UnifiedWebsiteAuditor(
        Path(args.websites_dir) if args.websites_dir else None,
        Path(args.output_dir) if args.output_dir else None
    )
    
    # Parse website configs
    website_configs = None
    if args.websites:
        website_configs = []
        for website_arg in args.websites:
            if ":" in website_arg:
                name, url = website_arg.split(":", 1)
                website_configs.append({"name": name, "url": url})
            else:
                website_configs.append({"name": website_arg, "url": f"https://{website_arg}"})
    
    # Default to revenue engine websites if none specified
    if not website_configs:
        website_configs = [
            {"name": "freerideinvestor.com", "url": "https://freerideinvestor.com"},
            {"name": "dadudekc.com", "url": "https://dadudekc.com"},
            {"name": "tradingrobotplug.com", "url": "https://tradingrobotplug.com"},
            {"name": "crosbyultimateevents.com", "url": "https://crosbyultimateevents.com"},
        ]
    
    results = auditor.audit_all_websites(website_configs)
    report_path = auditor.generate_report(results)
    
    print(f"\n📊 Unified Audit Complete!")
    print(f"   Websites: {results['websites_audited']}")
    print(f"   Average Score: {results['average_score']}/100")
    print(f"   Report: {report_path}")
    
    # Print summary per website
    for website, result in results["websites"].items():
        if result.get("status") == "complete":
            print(f"\n{website}:")
            print(f"  Overall Score: {result.get('overall_score', 0)}/100 (Grade {result.get('letter_grade', 'N/A')})")
            if "grade_card" in result:
                print(f"  Grade Card Score: {result['grade_card']['grade_card_score']}/100")
            print(f"  Technical Score: {sum([result['technical_metrics'][k]['score'] for k in result['technical_metrics']]) / len(result['technical_metrics']):.1f}/100")
            print(f"  Recommendations: {len(result.get('recommendations', []))}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

