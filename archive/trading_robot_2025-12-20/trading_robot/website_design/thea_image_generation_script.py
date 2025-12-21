#!/usr/bin/env python3
"""
Thea Image Generation Helper
============================

Script to help generate images for Trading Robot Plug website using Thea.
This script prepares prompts and can interface with Thea if image generation is available.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-15
"""

from pathlib import Path
import json
from typing import List, Dict


class TheaImageGenerator:
    """Helper for generating website images via Thea."""

    def __init__(self, output_dir: str = "website_design/generated_images"):
        """Initialize image generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_image_prompts(self) -> List[Dict[str, str]]:
        """Generate prompts for all needed images."""
        prompts = [
            {
                "name": "hero_background",
                "description": "Hero section background",
                "prompt": "Abstract gradient background with purple and blue tones, modern tech aesthetic, suitable for trading/finance website, 1920x1080, high quality, professional",
                "usage": "Hero section background image"
            },
            {
                "name": "robot_icon",
                "description": "Trading robot icon",
                "prompt": "Modern minimalist robot icon, purple gradient, clean design, suitable for logo/icon, square format, professional",
                "usage": "Logo, favicon, app icon"
            },
            {
                "name": "funnel_step_1",
                "description": "Discovery step graphic",
                "prompt": "Abstract graphic representing discovery/search, concentric circles, purple gradient, modern, clean",
                "usage": "Funnel step 1 visual"
            },
            {
                "name": "funnel_step_2",
                "description": "Choose step graphic",
                "prompt": "Abstract graphic representing selection/choice, stacked elements, green gradient, modern, clean",
                "usage": "Funnel step 2 visual"
            },
            {
                "name": "funnel_step_3",
                "description": "Deploy step graphic",
                "prompt": "Abstract graphic representing deployment/automation, geometric shapes, pink gradient, modern, clean",
                "usage": "Funnel step 3 visual"
            },
            {
                "name": "funnel_step_4",
                "description": "Profit step graphic",
                "prompt": "Abstract graphic representing success/profit, star or upward arrow, gold/yellow gradient, modern, clean",
                "usage": "Funnel step 4 visual"
            },
            {
                "name": "plugin_card_bg",
                "description": "Plugin card background",
                "prompt": "Subtle pattern background for product cards, light texture, professional, suitable for overlay text",
                "usage": "Plugin showcase cards"
            },
            {
                "name": "testimonial_avatar_1",
                "description": "Testimonial avatar placeholder",
                "prompt": "Professional headshot, business person, neutral background, friendly, trustworthy",
                "usage": "Testimonial section"
            },
            {
                "name": "testimonial_avatar_2",
                "description": "Testimonial avatar placeholder",
                "prompt": "Professional headshot, business person, neutral background, friendly, trustworthy",
                "usage": "Testimonial section"
            },
            {
                "name": "testimonial_avatar_3",
                "description": "Testimonial avatar placeholder",
                "prompt": "Professional headshot, business person, neutral background, friendly, trustworthy",
                "usage": "Testimonial section"
            }
        ]

        return prompts

    def save_prompts(self):
        """Save prompts to JSON file for Thea or other image generators."""
        prompts = self.generate_image_prompts()
        output_file = self.output_dir / "image_prompts.json"

        with open(output_file, "w") as f:
            json.dump(prompts, f, indent=2)

        print(f"✅ Saved {len(prompts)} image prompts to {output_file}")
        return output_file

    def create_thea_prompt_file(self):
        """Create a formatted prompt file for Thea image generation."""
        prompts = self.generate_image_prompts()
        output_file = self.output_dir / "thea_image_generation_prompt.md"

        content = "# Image Generation Prompts for Trading Robot Plug\n\n"
        content += "Use these prompts with Thea or your preferred image generation tool.\n\n"

        for i, prompt_data in enumerate(prompts, 1):
            content += f"## {i}. {prompt_data['name']}\n\n"
            content += f"**Description**: {prompt_data['description']}\n\n"
            content += f"**Prompt**: {prompt_data['prompt']}\n\n"
            content += f"**Usage**: {prompt_data['usage']}\n\n"
            content += "---\n\n"

        with open(output_file, "w") as f:
            f.write(content)

        print(f"✅ Created Thea prompt file: {output_file}")
        return output_file


if __name__ == "__main__":
    generator = TheaImageGenerator()
    generator.save_prompts()
    generator.create_thea_prompt_file()
    print("\n✅ Image generation prompts ready!")
    print("📝 Use these prompts with Thea or any image generation tool")
    print("🎨 All prompts are optimized for Trading Robot Plug branding")

