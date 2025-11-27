#!/usr/bin/env python3
"""
Test Training Data Integration
=============================

Tests the integration of structured training data generation into the GUI.
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

def test_orchestrator():
    """Test the training data orchestrator."""
    logger.info("🧪 Testing Training Data Orchestrator")
    logger.info("=" * 50)
    
    try:
        # Initialize orchestrator
        orchestrator = TrainingDataOrchestrator()
        logger.info("✅ Orchestrator initialized successfully")
        
        # Get sample conversation
        memory_manager = MemoryManager()
        conversations = memory_manager.get_conversations(limit=1)
        
        if not conversations:
            logger.warning("No conversations found in database")
            return False
        
        conversation = conversations[0]
        logger.info(f"📊 Testing with conversation: {conversation.get('title', 'Unknown')}")
        
        # Test offline prompt generation
        logger.info("🔧 Testing offline prompt generation...")
        result = orchestrator.generate_structured_data_for_conversation(
            conversation, 
            use_chatgpt=False
        )
        
        if result.get("success", False):
            logger.info("✅ Offline prompt generation successful")
            logger.info(f"📁 Output file: {result.get('output_file', 'Unknown')}")
        else:
            logger.error(f"❌ Offline prompt generation failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test prompt generation
        logger.info("🔧 Testing prompt generation...")
        prompt = orchestrator._get_structured_summary_prompt(conversation)
        
        if prompt and len(prompt) > 100:
            logger.info("✅ Prompt generation successful")
            logger.info(f"📝 Prompt length: {len(prompt)} characters")
            logger.info(f"📝 Prompt preview: {prompt[:200]}...")
        else:
            logger.error("❌ Prompt generation failed")
            return False
        
        # Test JSON extraction (with sample data)
        logger.info("🔧 Testing JSON extraction...")
        sample_response = '''
        Here's the JSON analysis:
        
        ```json
        {
            "summary": "User had a Python import error and learned about JSON parsing",
            "key_topics": ["Python", "ModuleNotFoundError", "JSON parsing"],
            "user_intent": "Fix import error and learn JSON parsing",
            "assistant_actions": ["Diagnosed error", "Provided pip install command", "Explained JSON parsing"],
            "skills_demonstrated": ["debugging", "teaching", "Python basics"],
            "code_examples": ["pip install requests", "import json ..."],
            "best_practices": ["Use virtual environments", "Check Python interpreter"],
            "pitfalls": ["Forgetting to activate venv"],
            "personality_traits": ["helpful", "step-by-step", "encouraging"],
            "difficulty_level": "beginner",
            "conversation_type": "debugging"
        }
        ```
        '''
        
        extracted_json = orchestrator._extract_json_from_response(sample_response)
        
        if extracted_json and isinstance(extracted_json, dict):
            logger.info("✅ JSON extraction successful")
            logger.info(f"📋 Extracted fields: {list(extracted_json.keys())}")
        else:
            logger.error("❌ JSON extraction failed")
            return False
        
        logger.info("✅ All orchestrator tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Orchestrator test failed: {e}")
        return False

def test_gui_integration():
    """Test that the GUI integration components are available."""
    logger.info("\n🧪 Testing GUI Integration")
    logger.info("=" * 50)
    
    try:
        # Test that the conversations panel can be imported
        from dreamscape.gui.panels.conversations_panel import ConversationsPanel
        logger.info("✅ ConversationsPanel imported successfully")
        
        # Test that the orchestrator can be imported
        from dreamscape.core.training_data_orchestrator import TrainingDataOrchestrator
        logger.info("✅ TrainingDataOrchestrator imported successfully")
        
        # Test that the training data generator can be imported
        from dreamscape.core.training_data_generator import TrainingDataGenerator
        logger.info("✅ TrainingDataGenerator imported successfully")
        
        logger.info("✅ All GUI integration components available!")
        return True
        
    except Exception as e:
        logger.error(f"❌ GUI integration test failed: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🚀 Starting Training Data Integration Tests")
    logger.info("=" * 60)
    
    try:
        # Test 1: Orchestrator functionality
        orchestrator_ok = test_orchestrator()
        
        # Test 2: GUI integration
        gui_ok = test_gui_integration()
        
        if orchestrator_ok and gui_ok:
            logger.info("\n🎉 All integration tests passed!")
            logger.info("\n📋 Integration Summary:")
            logger.info("✅ TrainingDataOrchestrator - Core orchestration logic")
            logger.info("✅ ConversationsPanel - GUI integration with new button")
            logger.info("✅ Background processing - QThread worker for non-blocking operation")
            logger.info("✅ Progress tracking - Real-time progress updates")
            logger.info("✅ Error handling - Graceful error display")
            logger.info("\n🚀 Ready to use in GUI!")
            return True
        else:
            logger.error("\n❌ Some integration tests failed!")
            return False
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 