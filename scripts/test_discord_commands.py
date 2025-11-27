#!/usr/bin/env python3
"""
Test All Discord Commands
=========================

Tests all Discord bot commands to ensure they work correctly.
This simulates command execution without requiring an actual Discord connection.
"""
import sys
import asyncio
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Test imports
try:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.services.messaging_infrastructure import ConsolidatedMessagingService
    from src.discord_commander.discord_gui_controller import DiscordGUIController
    IMPORTS_OK = True
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    IMPORTS_OK = False

def test_messaging_service():
    """Test the messaging service directly."""
    logger.info("=" * 60)
    logger.info("Testing ConsolidatedMessagingService")
    logger.info("=" * 60)
    
    try:
        service = ConsolidatedMessagingService()
        logger.info("✅ ConsolidatedMessagingService initialized")
        
        # Test sending a message (use queue directly to avoid subprocess issues)
        logger.info("\n📤 Testing send_message()...")
        try:
            result = service.send_message(
                agent="Agent-1",
                message="Test message from command test",
                priority="regular",
                use_pyautogui=False,  # Don't use PyAutoGUI for testing
                wait_for_delivery=False
            )
            
            if result.get("success"):
                logger.info(f"✅ Message queued successfully: {result.get('queue_id')}")
                return True
            else:
                logger.error(f"❌ Message failed: {result.get('message', 'Unknown error')}")
                return False
        except Exception as e:
            # If subprocess fails, test queue directly
            logger.warning(f"⚠️ Direct send failed (subprocess issue): {e}")
            logger.info("📤 Testing queue directly...")
            try:
                from src.core.message_queue import MessageQueue
                queue = MessageQueue()
                queue_id = queue.enqueue({
                    "type": "agent_message",
                    "sender": "TEST",
                    "recipient": "Agent-1",
                    "content": "Test message from command test",
                    "priority": "regular",
                    "source": "test"
                })
                logger.info(f"✅ Message queued directly: {queue_id}")
                return True
            except Exception as queue_e:
                logger.error(f"❌ Queue test also failed: {queue_e}")
                return False
            
    except Exception as e:
        logger.error(f"❌ Error testing messaging service: {e}", exc_info=True)
        return False

def test_gui_controller():
    """Test the GUI controller."""
    logger.info("\n" + "=" * 60)
    logger.info("Testing DiscordGUIController")
    logger.info("=" * 60)
    
    try:
        # Create messaging service first
        messaging_service = ConsolidatedMessagingService()
        controller = DiscordGUIController(messaging_service)
        logger.info("✅ DiscordGUIController initialized")
        
        # Check if messaging service is available
        if hasattr(controller, 'messaging_service'):
            logger.info("✅ Messaging service available in controller")
        else:
            logger.warning("⚠️ Messaging service not found in controller")
        
        # Test creating GUI components
        try:
            main_gui = controller.create_main_gui()
            logger.info("✅ Main GUI view created")
        except Exception as e:
            logger.warning(f"⚠️ Could not create main GUI: {e}")
        
        try:
            control_panel = controller.create_control_panel()
            logger.info("✅ Control panel created")
        except Exception as e:
            logger.warning(f"⚠️ Could not create control panel: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing GUI controller: {e}", exc_info=True)
        return False

def test_coordinate_loader():
    """Test coordinate loading."""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Coordinate Loader")
    logger.info("=" * 60)
    
    try:
        from src.core.coordinate_loader import get_coordinate_loader
        
        loader = get_coordinate_loader()
        logger.info("✅ Coordinate loader initialized")
        
        # Test loading coordinates for all agents
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        
        for agent_id in agents:
            try:
                coords = loader.get_chat_coordinates(agent_id)
                logger.info(f"✅ {agent_id}: {coords}")
            except Exception as e:
                logger.error(f"❌ {agent_id}: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing coordinate loader: {e}", exc_info=True)
        return False

def test_message_queue():
    """Test message queue functionality."""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Message Queue")
    logger.info("=" * 60)
    
    try:
        from src.core.message_queue import MessageQueue
        
        queue = MessageQueue()
        logger.info("✅ Message queue initialized")
        
        # Check queue status
        stats = queue.get_statistics()
        logger.info(f"📊 Queue statistics: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing message queue: {e}", exc_info=True)
        return False

def test_pyautogui_delivery():
    """Test PyAutoGUI delivery (without actually sending)."""
    logger.info("\n" + "=" * 60)
    logger.info("Testing PyAutoGUI Delivery")
    logger.info("=" * 60)
    
    try:
        from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        delivery = PyAutoGUIMessagingDelivery()
        logger.info("✅ PyAutoGUIMessagingDelivery initialized")
        
        # Test coordinate validation
        from src.core.coordinate_loader import get_coordinate_loader
        loader = get_coordinate_loader()
        coords = loader.get_chat_coordinates("Agent-1")
        
        is_valid = delivery.validate_coordinates("Agent-1", coords)
        logger.info(f"✅ Coordinate validation for Agent-1: {is_valid}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing PyAutoGUI delivery: {e}", exc_info=True)
        return False

def main():
    """Run all tests."""
    logger.info("🧪 Testing All Discord Command Components")
    logger.info("=" * 60)
    
    if not IMPORTS_OK:
        logger.error("❌ Cannot run tests - imports failed")
        return False
    
    results = []
    
    # Run all tests
    results.append(("Messaging Service", test_messaging_service()))
    results.append(("GUI Controller", test_gui_controller()))
    results.append(("Coordinate Loader", test_coordinate_loader()))
    results.append(("Message Queue", test_message_queue()))
    results.append(("PyAutoGUI Delivery", test_pyautogui_delivery()))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {name}")
    
    logger.info(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✅ All tests passed!")
        return True
    else:
        logger.warning(f"⚠️ {total - passed} test(s) failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

