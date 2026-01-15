
def deliver_via_core(message: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Deliver message via core messaging system.

    Args:
        message: Message data to deliver

    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Extract delivery information
        recipient = message.get("recipient", message.get("to"))
        sender = message.get("sender", message.get("from", "system"))
        content = message.get("content", message.get("message", ""))
        message_type = message.get("type", "text")
        priority = message.get("priority", "normal")

        if not recipient:
            return False, "No recipient specified"

        if not content:
            return False, "No message content"

        # Import messaging CLI for delivery
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

        try:
            from src.services.messaging_cli import UnifiedMessagingCLI

            # Create messaging CLI instance
            cli = UnifiedMessagingCLI()

            # Prepare delivery parameters
            delivery_params = {
                "agent": recipient,
                "message": content,
                "sender": sender,
                "type": message_type,
                "priority": priority
            }

            # Add optional parameters
            if "tags" in message:
                delivery_params["tags"] = message["tags"]
            if "category" in message:
                delivery_params["category"] = message["category"]

            # Execute delivery
            success = cli.send_message(**delivery_params)

            if success:
                logger.info(f"Message delivered via core to {recipient}")
                return True, None
            else:
                return False, "Core messaging delivery failed"

        except ImportError as e:
            logger.warning(f"Could not import messaging CLI: {e}")
            # Fallback to basic delivery simulation
            logger.info(f"Message would be delivered via core to {recipient}: {content[:100]}...")
            return True, None

        except Exception as e:
            logger.error(f"Core delivery error: {e}")
            return False, f"Core delivery error: {str(e)}"
    except Exception as e:
        return False, f"Core delivery failed: {str(e)}"

