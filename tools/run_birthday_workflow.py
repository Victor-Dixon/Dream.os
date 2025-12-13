#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Run Birthday Website Workflow
=============================

Demonstrates the unified tool using the birthday website workflow template.
Applies all 4 steps to prismblossom.online.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import sys
import json
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))

from website_manager import WebsiteManager


def run_birthday_workflow(site_key: str = "prismblossom"):
    """Run the complete birthday website workflow."""
    
    print("=" * 70)
    print("🎂 BIRTHDAY WEBSITE WORKFLOW - UNIFIED TOOL")
    print("=" * 70)
    print()
    
    try:
        manager = WebsiteManager(site_key)
        print(f"✅ Initialized for: {site_key}")
        print()
        
        # Step 1: Invitation Page
        print("📋 Step 1: Updating Invitation Page Colors...")
        print("-" * 70)
        color_scheme = {
            "#ff00ff": "#000000",  # Pink → Black
            "#ffffff": "#FFD700",  # White → Gold
            "rgba(255, 255, 255, 0.15)": "rgba(0, 0, 0, 0.8)",
            "rgba(255, 255, 255, 0.2)": "rgba(0, 0, 0, 0.6)",
            "rgba(255, 255, 255, 0.3)": "rgba(255, 215, 0, 0.5)"
        }
        result1 = manager.update_colors("page-invitation.php", color_scheme)
        print(f"   {'✅' if result1 else '⚠️'} Step 1 complete")
        print()
        
        # Step 2: Guestbook Placeholders
        print("📋 Step 2: Adding Guestbook Placeholder Entries...")
        print("-" * 70)
        entries = [
            {
                "name": "Sarah M.",
                "date": "Jan 25, 2025",
                "message": "Happy Birthday Carmyn! 🎉 Wishing you an amazing year ahead filled with music and joy!"
            },
            {
                "name": "Mike T.",
                "date": "Jan 24, 2025",
                "message": "Have a fantastic birthday! Your DJ skills are incredible! 🎵"
            },
            {
                "name": "Jessica L.",
                "date": "Jan 23, 2025",
                "message": "Happy Birthday! 🎂 Can't wait to hear your next mix!"
            }
        ]
        result2 = manager.add_placeholder_entries("page-guestbook.php", entries)
        print(f"   {'✅' if result2 else '⚠️'} Step 2 complete")
        print()
        
        # Step 3: Interactive Features
        print("📋 Step 3: Adding Interactive Features to Birthday Fun Page...")
        print("-" * 70)
        features = [
            {
                "type": "button_group",
                "class": "mini-games-container",
                "title": "🎮 Mini Games",
                "style": "margin: 40px 0; padding: 30px; background: rgba(0, 0, 0, 0.8); border: 2px solid #FFD700; border-radius: 15px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);",
                "title_style": "color: #FFD700; text-shadow: 0 0 10px #FFD700; margin-bottom: 20px;",
                "buttons": [
                    {
                        "id": "confetti-burst",
                        "text": "🎉 Confetti Burst",
                        "style": "background: rgba(0, 0, 0, 0.6); border: 2px solid #FFD700; color: #FFD700; padding: 15px 25px; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: bold; text-shadow: 0 0 5px #FFD700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.5); transition: all 0.3s ease;",
                        "action": "for (let i = 0; i < 100; i++) { setTimeout(() => createConfetti(), i * 10); }"
                    },
                    {
                        "id": "golden-sparkles",
                        "text": "✨ Golden Sparkles",
                        "style": "background: rgba(0, 0, 0, 0.6); border: 2px solid #FFD700; color: #FFD700; padding: 15px 25px; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: bold; text-shadow: 0 0 5px #FFD700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.5); transition: all 0.3s ease;",
                        "action": "createSparkles();"
                    },
                    {
                        "id": "birthday-song",
                        "text": "🎵 Birthday Song",
                        "style": "background: rgba(0, 0, 0, 0.6); border: 2px solid #FFD700; color: #FFD700; padding: 15px 25px; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: bold; text-shadow: 0 0 5px #FFD700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.5); transition: all 0.3s ease;",
                        "action": "playBirthdaySong();"
                    }
                ]
            },
            {
                "type": "gallery",
                "class": "birthday-gallery",
                "title": "📸 Birthday Memories",
                "style": "margin: 40px 0; padding: 30px; background: rgba(0, 0, 0, 0.8); border: 2px solid #FFD700; border-radius: 15px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);",
                "title_style": "color: #FFD700; text-shadow: 0 0 10px #FFD700; margin-bottom: 20px;",
                "items": [
                    {
                        "text": "[Birthday Image 1]<br><small style='opacity: 0.7;'>Click to add image</small>",
                        "style": "background: rgba(0, 0, 0, 0.6); border: 2px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center;",
                        "text_style": "color: #FFD700; text-shadow: 0 0 5px #FFD700;"
                    },
                    {
                        "text": "[Birthday Image 2]<br><small style='opacity: 0.7;'>Click to add image</small>",
                        "style": "background: rgba(0, 0, 0, 0.6); border: 2px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center;",
                        "text_style": "color: #FFD700; text-shadow: 0 0 5px #FFD700;"
                    },
                    {
                        "text": "[Birthday Image 3]<br><small style='opacity: 0.7;'>Click to add image</small>",
                        "style": "background: rgba(0, 0, 0, 0.6); border: 2px solid #FFD700; border-radius: 10px; padding: 20px; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center;",
                        "text_style": "color: #FFD700; text-shadow: 0 0 5px #FFD700;"
                    }
                ]
            }
        ]
        result3 = manager.add_interactive_features("page-birthday-fun.php", features)
        print(f"   {'✅' if result3 else '⚠️'} Step 3 complete")
        print()
        
        # Step 4: Blog Post (already created, just verify)
        print("📋 Step 4: Blog Post Template...")
        print("-" * 70)
        blog_exists = (manager.theme_path / "page-birthday-blog.php").exists()
        print(f"   {'✅' if blog_exists else '⚠️'} Blog post template: {'Exists' if blog_exists else 'Not found'}")
        print()
        
        # Summary
        print("=" * 70)
        print("📊 WORKFLOW SUMMARY")
        print("=" * 70)
        print(f"   Step 1 (Invitation Colors): {'✅' if result1 else '⚠️'}")
        print(f"   Step 2 (Guestbook Placeholders): {'✅' if result2 else '⚠️'}")
        print(f"   Step 3 (Interactive Features): {'✅' if result3 else '⚠️'}")
        print(f"   Step 4 (Blog Post): {'✅' if blog_exists else '⚠️'}")
        print()
        
        # Deployment instructions
        print("=" * 70)
        print("🚀 DEPLOYMENT INSTRUCTIONS")
        print("=" * 70)
        print("Use Hostinger File Manager (same method as dadudekc website):")
        print("   1. Log into hpanel.hostinger.com")
        print("   2. Open File Manager")
        print(f"   3. Navigate to: {manager.config['remote_base']}")
        print("   4. Upload updated files:")
        print("      - page-invitation.php")
        print("      - page-guestbook.php")
        print("      - page-birthday-fun.php")
        print("      - page-birthday-blog.php")
        print("   5. Files will be live immediately!")
        print()
        
        print("=" * 70)
        print("✅ BIRTHDAY WEBSITE WORKFLOW COMPLETE!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    site = sys.argv[1] if len(sys.argv) > 1 else "prismblossom"
    success = run_birthday_workflow(site)
    sys.exit(0 if success else 1)







