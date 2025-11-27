================================================================================
COMPREHENSIVE DISCORD COMMANDS & CONTROLLERS LIST
================================================================================

📦 UNIFIED DISCORD BOT COMMANDS (unified_discord_bot.py)
--------------------------------------------------------------------------------
  !control (or !panel, !menu)
    - Open main control panel with interactive buttons

  !gui
    - Open messaging GUI interface

  !status
    - View detailed swarm status

  !message <agent-id> <message>
    - Send message to specific agent

  !broadcast <message>
    - Broadcast message to all agents

  !help
    - Show interactive help menu

  !shutdown (Admin only)
    - Gracefully shutdown the bot (with confirmation)

  !restart (Admin only)
    - Restart the Discord bot (with confirmation)

  [C2A] Agent-X format
    - Send regular message using C2A format

  [D2A] Agent-X format
    - Send urgent message using D2A format


📨 MESSAGING COMMANDS (messaging_commands.py)
--------------------------------------------------------------------------------
  !message_agent <agent-id> <message> [priority]
    - Send message to specific agent with optional priority

  !agent_interact
    - Interactive agent messaging interface

  !swarm_status
    - View current swarm status

  !broadcast <message> [priority]
    - Broadcast message to all agents with optional priority

  !agent_list
    - List all available agents

  !agent <agent-name> <message>
    - Send message to agent (C-057 format)

  !help_messaging
    - Get help with messaging commands


🐝 SWARM SHOWCASE COMMANDS (swarm_showcase_commands.py)
--------------------------------------------------------------------------------
  !swarm_tasks (or !tasks, !directives)
    - Display all active tasks and directives dashboard

  !swarm_roadmap (or !roadmap, !plan)
    - Show integration roadmap

  !swarm_excellence (or !excellence, !achievements)
    - Showcase agent achievements

  !swarm_overview (or !overview, !dashboard)
    - Complete swarm status and missions


📚 GITHUB BOOK VIEWER COMMANDS (github_book_viewer.py)
--------------------------------------------------------------------------------
  !github_book [repo_num] (or !book, !repos)
    - Interactive GitHub book viewer with navigation
    - Start from beginning or jump to specific repo

  !goldmines (or !jackpots, !discoveries)
    - Showcase all goldmine and jackpot discoveries

  !book_stats (or !book_progress, !repo_stats)
    - Show GitHub book statistics and progress

  !book_search <keyword> (or !search_repos, !find_repo)
    - Search repositories by keyword

  !book_filter [agent_id] (or !filter_repos, !repos_by_agent)
    - Filter repositories by agent


🔗 WEBHOOK COMMANDS (webhook_commands.py) - Admin Only
--------------------------------------------------------------------------------
  !create_webhook <channel> <webhook_name>
    - Create webhook for specific channel

  !list_webhooks [channel]
    - List all webhooks in server or specific channel

  !delete_webhook <webhook_id>
    - Delete webhook by ID (with confirmation)

  !test_webhook <webhook_id>
    - Test webhook by sending test message

  !webhook_info <webhook_id>
    - Get detailed information about webhook


🎛️ CONTROLLERS (Interactive Views)
--------------------------------------------------------------------------------

📨 MessagingControllerView (controllers/messaging_controller_view.py)
    Features:
    - Agent selector dropdown with live status
    - Custom message entry modal
    - Priority selection
    - Broadcast quick access
    - Jet Fuel message button
    - Live status button
    - Refresh agents button

📊 StatusControllerView (controllers/status_controller_view.py)
    Features:
    - Real-time agent status
    - Points and mission tracking
    - Live refresh capability
    - Status filters (Active/Idle)
    - Message idle agents button

📢 BroadcastControllerView (controllers/broadcast_controller_view.py)
    Features:
    - Broadcast to all agents
    - Select specific agents
    - Jet Fuel broadcast
    - Broadcast templates

📋 BroadcastTemplatesView (controllers/broadcast_templates_view.py)
    Features:
    - Pre-defined broadcast templates
    - Quick template selection


🖼️ GUI COMPONENTS (discord_gui_*.py)
--------------------------------------------------------------------------------

DiscordGUIController (discord_gui_controller.py)
    - Main GUI controller facade
    - Creates all GUI views and modals

AgentMessagingGUIView (discord_gui_views.py)
    - Main messaging GUI view
    - Agent selection dropdown
    - Message composition

SwarmStatusGUIView (discord_gui_views.py)
    - Swarm status monitoring view

HelpGUIView (discord_gui_views.py)
    - Interactive help menu

MainControlPanelView (discord_gui_views.py)
    - Main control panel with all features

AgentMessageModal (discord_gui_modals.py)
    - Modal for messaging specific agent

BroadcastMessageModal (discord_gui_modals.py)
    - Modal for broadcasting to all agents


🔌 INTEGRATIONS & SERVICES
--------------------------------------------------------------------------------

DebateDiscordPoster (debate_discord_integration.py)
    - Posts agent debates to Discord
    - Shows agent votes with attribution
    - Posts debate status/results

ContractNotifier (contract_notifications.py)
    - Real-time contract event notifications
    - Contract assigned notifications
    - Contract started notifications
    - Contract completed notifications

DiscordAgentCommunication (discord_agent_communication.py)
    - send_to_agent_inbox()
    - broadcast_to_all_agents()
    - send_human_prompt_to_captain()
    - execute_agent_command()


================================================================================
SUMMARY
================================================================================

Total Commands: ~30+
  - Unified Bot: 8 commands
  - Messaging: 7 commands
  - Swarm Showcase: 4 commands
  - GitHub Book: 5 commands
  - Webhooks: 5 commands (admin)

Total Controllers/Views: 8+
  - MessagingControllerView
  - StatusControllerView
  - BroadcastControllerView
  - BroadcastTemplatesView
  - AgentMessagingGUIView
  - SwarmStatusGUIView
  - HelpGUIView
  - MainControlPanelView

Total Modals: 2
  - AgentMessageModal
  - BroadcastMessageModal

Total Integrations: 3
  - DebateDiscordPoster
  - ContractNotifier
  - DiscordAgentCommunication

================================================================================
All commands are case-insensitive
GUI commands (!control, !gui) are preferred for ease of use
================================================================================
