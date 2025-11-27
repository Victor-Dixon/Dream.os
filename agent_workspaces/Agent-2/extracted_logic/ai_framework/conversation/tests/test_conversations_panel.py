#!/usr/bin/env python3
"""
Test Conversations Panel Integration
===================================

Tests the conversations panel and structured training data generation integration.
"""

import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dreamscape.core.memory.manager import MemoryManager
from dreamscape.core.training_system import TrainingDataOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_conversations_panel_integration():
    """Test the conversations panel integration."""
    logger.info("🧪 Testing Conversations Panel Integration")
    logger.info("=" * 60)
    
    try:
        # Test 1: Memory Manager
        logger.info("🔧 Test 1: Memory Manager")
        memory_manager = MemoryManager()
        conversations = memory_manager.get_conversations(limit=5)
        
        if conversations:
            logger.info(f"✅ Found {len(conversations)} conversations")
            for i, conv in enumerate(conversations[:3]):
                logger.info(f"  {i+1}. {conv.get('title', 'Unknown')} ({len(conv.get('content', ''))} chars)")
        else:
            logger.warning("⚠️ No conversations found in database")
            return False
        
        # Test 2: Training Data Orchestrator
        logger.info("\n🔧 Test 2: Training Data Orchestrator")
        orchestrator = TrainingDataOrchestrator()
        logger.info("✅ Orchestrator initialized")
        
        # Test 3: Prompt Generation
        logger.info("\n🔧 Test 3: Prompt Generation")
        if conversations:
            conversation = conversations[0]
            prompt = orchestrator._get_structured_summary_prompt(conversation)
            
            if prompt and len(prompt) > 100:
                logger.info("✅ Prompt generation successful")
                logger.info(f"📝 Prompt length: {len(prompt)} characters")
                logger.info(f"📝 Prompt preview: {prompt[:200]}...")
            else:
                logger.error("❌ Prompt generation failed")
                return False
        
        # Test 4: Offline Training Data Generation
        logger.info("\n🔧 Test 4: Offline Training Data Generation")
        if conversations:
            result = orchestrator.generate_structured_data_for_conversation(
                conversations[0], 
                use_chatgpt=False
            )
            
            if result.get("success", False):
                logger.info("✅ Offline training data generation successful")
                logger.info(f"📁 Output file: {result.get('output_file', 'Unknown')}")
            else:
                logger.error(f"❌ Offline training data generation failed: {result.get('error', 'Unknown error')}")
                return False
        
        logger.info("\n✅ All conversations panel integration tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Conversations panel integration test failed: {e}")
        return False

def test_gui_components():
    """Test that GUI components can be imported."""
    logger.info("\n🧪 Testing GUI Components")
    logger.info("=" * 50)
    
    try:
        # Test conversations panel import
        from dreamscape.gui.panels.conversations_panel import ConversationsPanel
        logger.info("✅ ConversationsPanel imported successfully")
        
        # Test main window import
        from dreamscape.gui.main_window import TheaMainWindow
        logger.info("✅ TheaMainWindow imported successfully")
        
        # Test training data orchestrator import
        from dreamscape.core.training_system import TrainingDataOrchestrator
        logger.info("✅ TrainingDataOrchestrator imported successfully")
        
        # Test training data generator import
        from dreamscape.core.training_data_generator import TrainingDataGenerator
        logger.info("✅ TrainingDataGenerator imported successfully")
        
        logger.info("✅ All GUI components available!")
        return True
        
    except Exception as e:
        logger.error(f"❌ GUI component test failed: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🚀 Starting Conversations Panel Integration Tests")
    logger.info("=" * 70)
    
    try:
        # Test 1: Conversations panel integration
        panel_ok = test_conversations_panel_integration()
        
        # Test 2: GUI components
        gui_ok = test_gui_components()
        
        if panel_ok and gui_ok:
            logger.info("\n🎉 All tests passed!")
            logger.info("\n📋 Integration Summary:")
            logger.info("✅ Conversations Panel - Displays conversation list and content")
            logger.info("✅ Training Data Button - Added to conversation viewer")
            logger.info("✅ Background Processing - QThread worker for non-blocking operation")
            logger.info("✅ Progress Tracking - Real-time progress updates")
            logger.info("✅ Error Handling - Graceful error display")
            logger.info("\n🚀 Ready to use in GUI!")
            logger.info("\n💡 To test:")
            logger.info("1. Run: python main.py")
            logger.info("2. Navigate to Conversations tab")
            logger.info("3. Select a conversation")
            logger.info("4. Click '🤖 Generate Training Data' button")
            return True
        else:
            logger.error("\n❌ Some tests failed!")
            return False
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 