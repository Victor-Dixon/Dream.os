# <!-- SSOT Domain: discord -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import approval_commands
from . import contract_notifications
# from . import debate_discord_integration  # DELETED - File does not exist
from . import discord_agent_communication
from . import discord_embeds
from . import discord_gui_controller
from . import discord_gui_modals
from . import discord_models
from . import discord_service
from . import github_book_viewer
from . import messaging_commands
from . import messaging_controller
from . import messaging_controller_modals
# messaging_controller_views removed - merged into canonical controllers
from . import status_reader
from . import swarm_showcase_commands
from . import unified_discord_bot
from . import webhook_commands

__all__ = [
    'approval_commands',
    'contract_notifications',
    # 'debate_discord_integration',  # DELETED - File does not exist
    'discord_agent_communication',
    'discord_embeds',
    'discord_gui_controller',
    'discord_gui_modals',
    'discord_models',
    'discord_service',
    'github_book_viewer',
    'messaging_commands',
    'messaging_controller',
    'messaging_controller_modals',
    # 'messaging_controller_views',  # Removed - merged into canonical controllers
    'status_reader',
    'swarm_showcase_commands',
    'unified_discord_bot',
    'webhook_commands',
]
