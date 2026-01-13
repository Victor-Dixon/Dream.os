"""
Mode Selection Handler - V2 Compliant (<400 lines)
Handles interactive agent mode selection and configuration.
"""

import sys
from typing import Dict, Any, Optional


class ModeHandler:
    """Handles mode selection command with interactive configuration."""

    def __init__(self):
        self.available_modes = {
            'full': {
                'name': 'Full System',
                'description': 'All services (Message Queue, Twitch Bot, Discord Bot, FastAPI)',
                'services': ['message_queue', 'twitch_bot', 'discord_bot', 'fastapi_service']
            },
            'minimal': {
                'name': 'Minimal System',
                'description': 'Essential services only (Message Queue, FastAPI)',
                'services': ['message_queue', 'fastapi_service']
            },
            'bots': {
                'name': 'Bot Services',
                'description': 'Bot services only (Twitch Bot, Discord Bot)',
                'services': ['twitch_bot', 'discord_bot']
            },
            'api': {
                'name': 'API Only',
                'description': 'FastAPI service only',
                'services': ['fastapi_service']
            },
            'custom': {
                'name': 'Custom Configuration',
                'description': 'Select individual services',
                'services': []  # Will be populated interactively
            }
        }

    def execute(self) -> Optional[Dict[str, Any]]:
        """Execute mode selection command. Returns selected configuration."""
        print("🎭 dream.os - Agent Mode Selection")
        print("=" * 40)

        print("Available modes:")
        for mode_key, mode_info in self.available_modes.items():
            print(f"   {mode_key}: {mode_info['name']}")
            print(f"      {mode_info['description']}")

        print("\n   quit: Exit without selection")
        # Get user selection
        while True:
            try:
                selection = input("\nSelect mode: ").strip().lower()
            except KeyboardInterrupt:
                print("\n❌ Selection cancelled.")
                return None

            if selection == 'quit':
                print("❌ Selection cancelled.")
                return None

            if selection in self.available_modes:
                return self._handle_mode_selection(selection)
            else:
                print(f"❌ Invalid selection: {selection}")
                print("Please choose from:", ', '.join(self.available_modes.keys()))

    def _handle_mode_selection(self, mode_key: str) -> Dict[str, Any]:
        """Handle the selected mode and return configuration."""
        mode_info = self.available_modes[mode_key]

        if mode_key == 'custom':
            services = self._select_custom_services()
            if not services:
                return None
            mode_info['services'] = services

        print(f"\n✅ Selected: {mode_info['name']}")
        print(f"   Description: {mode_info['description']}")
        print(f"   Services: {', '.join(mode_info['services'])}")

        # Confirm selection
        try:
            confirm = input("\nConfirm selection? (Y/n): ").strip().lower()
            if confirm in ['n', 'no']:
                print("❌ Selection cancelled.")
                return None
        except KeyboardInterrupt:
            print("\n❌ Selection cancelled.")
            return None

        return {
            'mode': mode_key,
            'name': mode_info['name'],
            'services': mode_info['services'],
            'description': mode_info['description']
        }

    def _select_custom_services(self) -> list:
        """Allow user to select individual services for custom mode."""
        available_services = {
            'message_queue': 'Message Queue Processor (Redis-based)',
            'twitch_bot': 'Twitch Bot (chat interaction)',
            'discord_bot': 'Discord Bot (server management)',
            'fastapi_service': 'FastAPI Service (REST API)'
        }

        print("\n🎛️  Custom Service Selection")
        print("Available services:")
        for service_key, description in available_services.items():
            print(f"   {service_key}: {description}")

        selected_services = []

        for service_key, description in available_services.items():
            try:
                choice = input(f"Include {service_key}? (y/N): ").strip().lower()
                if choice in ['y', 'yes']:
                    selected_services.append(service_key)
                    print(f"   ✅ Added {service_key}")
                else:
                    print(f"   ⏭️  Skipped {service_key}")
            except KeyboardInterrupt:
                print("\n❌ Custom selection cancelled.")
                return []

        if not selected_services:
            print("❌ No services selected.")
            return []

        print(f"\n✅ Custom mode configured with {len(selected_services)} services:")
        for service in selected_services:
            print(f"   • {service}")

        return selected_services