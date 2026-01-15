# <!-- SSOT Domain: discord -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import approval_commands
from . import contract_notifications
# from . import debate_discord_integration  # DELETED - File does not exist
from . import discord_agent_communication
from . import discord_embeds
from . import discord_gui_controller
from . import discord_gui_modals_v2
from . import discord_models
from . import discord_service
from . import github_book_viewer
from . import messaging_controller
from . import messaging_controller_modals
# messaging_controller_views removed - merged into canonical controllers
from . import unified_discord_bot

__all__ = [
    'approval_commands',
    'contract_notifications',
    # 'debate_discord_integration',  # DELETED - File does not exist
    'discord_agent_communication',
    'discord_embeds',
    'discord_gui_controller',
    'discord_gui_modals_v2',
    'discord_models',
    'discord_service',
    'github_book_viewer',
    'messaging_controller',
    'messaging_controller_modals',
    # 'messaging_controller_views',  # Removed - merged into canonical controllers
    'unified_discord_bot',
]
