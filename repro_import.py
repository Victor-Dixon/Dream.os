try:
    from src.services.messaging.discord_message_helpers import queue_message_for_agent_by_number
    print("Function found!")
except ImportError as e:
    print(f"Error: {e}")
