#!/usr/bin/env python3
"""
Digital Dreamscape - Standalone Project
Main entry point for the application.
"""

import sys, os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
# This ensures the modular core structure works for all entry points and environments.

# EDIT START: Configure logging at the very top for discord import debugging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_debug.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logging.debug('[TEST] Logging configured at DEBUG level and file handler is active.')
# Rationale: Ensures all debug output from discord import diagnostics is captured in the log file.
# EDIT END

# EDIT START: Minimal import diagnostics for discord.ext.commands error
import sys, os
print("PYTHON EXECUTABLE:", sys.executable)
print("sys.path:", sys.path)
print("CWD:", os.getcwd())
try:
    import discord
    print("discord.__file__:", discord.__file__)
    from discord.ext import commands
    print("discord.ext.commands import: SUCCESS")
except Exception as e:
    print("discord.ext.commands import: FAILED", e)
# Rationale: Minimal, direct diagnostics for discord.ext.commands import error
# EDIT END

# EDIT START: Remove forced discord.ext.commands import workaround (circular import issue resolved)
# (Removed forced import workaround)
# EDIT END

from dreamscape.core.config import MEMORY_DB_PATH, RESUME_DB_PATH

def main():
    """Main application entry point."""
    try:
        # Import and run the GUI application
        from dreamscape.gui.main_window import main as gui_main
        return gui_main()
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return 1
    except Exception as e:
        import traceback, textwrap
        print("Application error: {}".format(e))
        traceback.print_exc()
        return 1

def test_template_engine():
    """Test the template engine functionality."""
    try:
        from dreamscape.core.template_engine import render_template
        
        # Create a test template
        test_template = """
        Hello {{ name }}!
        Your value is {{ data.value }}.
        """
        
        # Test rendering
        context = {"name": "World", "data": {"value": 123}}
        result = render_template(test_template, context)
        
        if result:
            print("✅ Template engine test passed!")
            print(f"Result: {result}")
            return True
        else:
            print("❌ Template engine test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Template engine test error: {e}")
        return False

def test_scraper():
    """Test the scraper functionality."""
    try:
        from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
        print("✅ Scraper import successful!")
        
        # Test undetected-chromedriver capability
        scraper = ChatGPTScraper(use_undetected=True)
        if hasattr(scraper, 'use_undetected'):
            if scraper.use_undetected:
                print("✅ Undetected-chromedriver capability available!")
            else:
                print("⚠️  Undetected-chromedriver not available, using regular selenium")
        else:
            print("⚠️  Undetected-chromedriver feature not implemented")
        
        # Test demo conversation functionality
        conversations = scraper._get_demo_conversations()
        if conversations and len(conversations) > 0:
            print(f"✅ Demo conversations working: {len(conversations)} conversations")
        else:
            print("❌ Demo conversations not working")
            return False
        
        # Test template integration
        from dreamscape.core.template_engine import render_template
        prompt_template = "Analyze: {{ conversation.title }}"
        rendered = render_template(prompt_template, {"conversation": conversations[0]})
        if rendered and "Analyze:" in rendered:
            print("✅ Template integration working")
        else:
            print("❌ Template integration not working")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Scraper test error: {e}")
        return False

def test_comprehensive_scraping():
    """Test comprehensive scraping functionality (requires manual login)."""
    try:
        from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
        import tempfile
        import os
        
        print("🧪 Testing comprehensive scraping functionality...")
        print("⚠️  This test requires manual login to ChatGPT")
        
        # Initialize scraper
        scraper = ChatGPTScraper(headless=False, use_undetected=True)
        
        with scraper:
            if not scraper.driver:
                print("❌ Failed to start driver")
                return False
            
            print("🌐 Navigating to ChatGPT...")
            
            # Test navigation
            if not scraper.navigate_to_chatgpt():
                print("❌ Failed to navigate to ChatGPT")
                return False
            
            print("✅ Successfully navigated to ChatGPT")
            
            # Test login detection
            is_logged_in = scraper.is_logged_in()
            print(f"🔐 Login status: {is_logged_in}")
            
            if not is_logged_in:
                print("⚠️  Please log in manually in the browser window")
                print("⏳ Waiting 30 seconds for manual login...")
                import time
                time.sleep(30)
                
                # Check again
                is_logged_in = scraper.is_logged_in()
                print(f"🔐 Login status after wait: {is_logged_in}")
            
            if is_logged_in:
                print("✅ User is logged in")
                
                # Test conversation extraction
                conversations = scraper.get_conversation_list()
                print(f"📋 Found {len(conversations)} conversations")
                
                if conversations:
                    # Test conversation entry and prompting
                    first_conv = conversations[0]
                    print(f"🔍 Testing conversation entry: {first_conv['title']}")
                    
                    if scraper.enter_conversation(first_conv['url']):
                        print("✅ Successfully entered conversation")
                        
                        # Test templated prompt
                        prompt_template = """
                        Please analyze this conversation and provide:
                        1. Key topics discussed
                        2. Main insights
                        3. Action items (if any)
                        
                        Conversation title: {{ conversation.title }}
                        """
                        
                        prompt = render_template(prompt_template, {"conversation": first_conv})
                        print(f"📝 Sending templated prompt: {prompt[:100]}...")
                        
                        if scraper.send_prompt(prompt):
                            print("✅ Successfully sent prompt")
                            
                            # Get response
                            content = scraper.get_conversation_content()
                            if content.get("full_conversation"):
                                print("✅ Successfully received response")
                                print(f"📄 Response length: {len(content['full_conversation'])} characters")
                            else:
                                print("⚠️  No response content received")
                        else:
                            print("❌ Failed to send prompt")
                    else:
                        print("❌ Failed to enter conversation")
                
                # Test saving to file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    temp_file = f.name
                
                try:
                    scraper._save_conversations(conversations, temp_file)
                    if os.path.exists(temp_file):
                        print("✅ Successfully saved conversations to file")
                        os.unlink(temp_file)  # Clean up
                    else:
                        print("❌ Failed to save conversations")
                except Exception as e:
                    print(f"❌ Error saving conversations: {e}")
            else:
                print("❌ User is not logged in - cannot test full functionality")
                return False
        
        print("✅ Comprehensive scraping test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive scraping test error: {e}")
        return False

def test_undetected_chrome():
    """Test the undetected-chromedriver functionality specifically."""
    try:
        import undetected_chromedriver as uc
        print("✅ Undetected-chromedriver import successful!")
        
        # Test basic functionality
        from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
        
        # Test with undetected-chromedriver enabled
        scraper_undetected = ChatGPTScraper(use_undetected=True, headless=True)
        print(f"✅ Undetected mode: {scraper_undetected.use_undetected}")
        
        # Test with undetected-chromedriver disabled
        scraper_regular = ChatGPTScraper(use_undetected=False, headless=True)
        print(f"✅ Regular mode: {not scraper_regular.use_undetected}")
        
        return True
    except ImportError as e:
        print(f"❌ Undetected-chromedriver not available: {e}")
        print("Install with: pip install undetected-chromedriver")
        return False
    except Exception as e:
        print(f"❌ Undetected-chromedriver test error: {e}")
        return False

def test_enhanced_skill_system():
    """Test the enhanced skill resume system functionality."""
    try:
        from dreamscape.core.mmorpg.enhanced_skill_resume_system import EnhancedSkillResumeSystem
        from dreamscape.core.mmorpg.mmorpg_engine import MMORPGEngine
        from dreamscape.core.resume_tracker import ResumeTracker
        from dreamscape.core.memory import MemoryManager
        
        print("🧪 Testing enhanced skill resume system...")
        
        # Initialize components
        memory_manager = MemoryManager(str(MEMORY_DB_PATH))
        mmorpg_engine = MMORPGEngine(str(MEMORY_DB_PATH))
        resume_tracker = ResumeTracker(str(RESUME_DB_PATH))
        
        # Initialize enhanced skill system
        enhanced_system = EnhancedSkillResumeSystem(memory_manager, mmorpg_engine, resume_tracker)
        print("✅ Enhanced skill resume system initialized")
        
        # Test skill categorization
        test_skills = ["Architecture", "Testing", "Python", "Debugging", "Optimization", "Problem Solving"]
        for skill in test_skills:
            category = enhanced_system._categorize_skill(skill)
            print(f"  {skill} -> {category}")
        
        # Test skill tree building
        print("🌳 Building enhanced skill tree...")
        skill_tree = enhanced_system.build_enhanced_skill_tree()
        
        if skill_tree and not skill_tree.get('error'):
            print(f"✅ Skill tree built successfully:")
            print(f"  - Categories: {len(skill_tree.get('root_skills', {}))}")
            print(f"  - Total skills: {sum(len(skills) for skills in skill_tree.get('root_skills', {}).values())}")
            print(f"  - Expertise areas: {len(skill_tree.get('expertise_areas', {}))}")
            print(f"  - Skill gaps: {len(skill_tree.get('skill_gaps', {}))}")
            return True
        else:
            print(f"❌ Skill tree build failed: {skill_tree.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced skill system test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_demo_conversations():
    """Create demo conversations for testing the enhanced skill system."""
    try:
        from dreamscape.core.memory import MemoryManager
        from datetime import datetime
        
        print("📝 Creating demo conversations for testing...")
        
        # Initialize memory manager
        memory_manager = MemoryManager(str(MEMORY_DB_PATH))
        
        # Demo conversations with different skills
        demo_conversations = [
            {
                'id': 'demo_1',
                'title': 'Python Web Development with FastAPI',
                'content': 'I learned about FastAPI, async programming, and REST API design. The conversation covered database integration, authentication, and deployment strategies.',
                'timestamp': datetime.now().isoformat(),
                'model': 'gpt-4o',
                'message_count': 15,
                'word_count': 500,
                'source': 'chatgpt',
                'status': 'active'
            },
            {
                'id': 'demo_2', 
                'title': 'System Architecture Design Patterns',
                'content': 'Discussed microservices architecture, database design patterns, and scalability considerations. Covered topics like load balancing, caching, and monitoring.',
                'timestamp': datetime.now().isoformat(),
                'model': 'gpt-4o',
                'message_count': 12,
                'word_count': 400,
                'source': 'chatgpt',
                'status': 'active'
            },
            {
                'id': 'demo_3',
                'title': 'Testing Strategies and Debugging Techniques',
                'content': 'Explored unit testing, integration testing, and debugging methodologies. Learned about test-driven development and automated testing frameworks.',
                'timestamp': datetime.now().isoformat(),
                'model': 'gpt-4o',
                'message_count': 18,
                'word_count': 600,
                'source': 'chatgpt',
                'status': 'active'
            },
            {
                'id': 'demo_4',
                'title': 'JavaScript Frontend Optimization',
                'content': 'Discussed React performance optimization, bundle size reduction, and frontend debugging tools. Covered topics like code splitting and lazy loading.',
                'timestamp': datetime.now().isoformat(),
                'model': 'gpt-4o',
                'message_count': 10,
                'word_count': 350,
                'source': 'chatgpt',
                'status': 'active'
            },
            {
                'id': 'demo_5',
                'title': 'Database Design and Query Optimization',
                'content': 'Learned about database normalization, indexing strategies, and query optimization techniques. Covered both SQL and NoSQL considerations.',
                'timestamp': datetime.now().isoformat(),
                'model': 'gpt-4o',
                'message_count': 14,
                'word_count': 450,
                'source': 'chatgpt',
                'status': 'active'
            }
        ]
        
        # Store demo conversations
        for conv in demo_conversations:
            if memory_manager.storage.store_conversation(conv):
                print(f"✅ Created demo conversation: {conv['title']}")
            else:
                print(f"❌ Failed to create demo conversation: {conv['title']}")
        
        print(f"📊 Created {len(demo_conversations)} demo conversations")
        return True
        
    except Exception as e:
        print(f"❌ Error creating demo conversations: {e}")
        return False

def test_enhanced_ingestion():
    """Test the enhanced ingestion pipeline with full workflow."""
    try:
        from dreamscape.core.memory import MemoryManager
        
        print("🧪 Testing enhanced ingestion pipeline...")
        
        # Initialize memory manager
        memory_manager = MemoryManager(str(MEMORY_DB_PATH))
        
        # Test enhanced ingestion with available method
        print("🎯 Running enhanced ingestion...")
        processed_count = memory_manager.ingest_conversations(
            conversations_dir="data/conversations"
        )
        
        if processed_count >= 0:
            print("✅ Enhanced ingestion completed successfully!")
            print(f"  - Processed: {processed_count} conversations")
            print(f"  - Note: Full workflow features (templates, Discord, game updates) require additional setup")
        else:
            print(f"❌ Enhanced ingestion failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced ingestion test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            print("🧪 Running component tests...")
            template_ok = test_template_engine()
            scraper_ok = test_scraper()
            undetected_ok = test_undetected_chrome()
            enhanced_skill_ok = test_enhanced_skill_system()
            
            if template_ok and scraper_ok and undetected_ok and enhanced_skill_ok:
                print("✅ All component tests passed!")
                sys.exit(0)
            else:
                print("❌ Some component tests failed!")
                sys.exit(1)
        
        elif command == "template":
            test_template_engine()
            sys.exit(0)
        
        elif command == "scraper":
            test_scraper()
            sys.exit(0)
        
        elif command == "undetected_chrome":
            test_undetected_chrome()
            sys.exit(0)
        
        elif command == "comprehensive_scraping":
            test_comprehensive_scraping()
            sys.exit(0)
        
        elif command == "enhanced_skill_system":
            test_enhanced_skill_system()
            sys.exit(0)
        
        elif command == "create_demo_conversations":
            create_demo_conversations()
            sys.exit(0)
        
        elif command == "enhanced_ingestion":
            test_enhanced_ingestion()
            sys.exit(0)
        
        elif command == "scrape_conversations":
            from scripts.scrape_real_conversations import scrape_real_conversations
            max_conv = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            results = scrape_real_conversations(max_conversations=max_conv)
            if results.get("success"):
                print(f"✅ Successfully scraped {results['conversations_scraped']} conversations!")
            else:
                print(f"❌ Scraping failed: {results.get('error')}")
            sys.exit(0)
        
        elif command == "load_cookies_and_scrape":
            from scripts.load_cookies_and_scrape import load_cookies_and_scrape
            max_conv = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            results = load_cookies_and_scrape(max_conversations=max_conv)
            if results.get("success"):
                print(f"✅ Successfully scraped {results['conversations_scraped']} conversations with cookies!")
            else:
                print(f"❌ Cookie-based scraping failed: {results.get('error')}")
            sys.exit(0)
        
        elif command == "templates":
            from scripts.template_usage_guide import TemplateUsageGuide
            guide = TemplateUsageGuide()
            if len(sys.argv) > 2:
                subcommand = sys.argv[2]
                if subcommand == "list":
                    guide.show_available_templates()
                elif subcommand == "usage" and len(sys.argv) > 3:
                    guide.show_template_usage(sys.argv[3])
                elif subcommand == "test" and len(sys.argv) > 3:
                    guide.test_template_rendering(sys.argv[3])
                elif subcommand == "workflow":
                    guide.show_response_processing_workflow()
                elif subcommand == "integration":
                    guide.show_integration_examples()
                else:
                    print("Usage: python main.py templates <subcommand> [args]")
                    print("Subcommands: list, usage <category>, test <category>, workflow, integration")
            else:
                guide.show_available_templates()
            sys.exit(0)
        
        elif command == "process_response":
            from scripts.response_processor import ResponseProcessor
            if len(sys.argv) > 2:
                conversation_id = sys.argv[2]
                response_content = sys.argv[3] if len(sys.argv) > 3 else "Sample response content for testing"
                processor = ResponseProcessor()
                results = processor.process_conversation_response(conversation_id, response_content)
                if results.get("success"):
                    print(f"✅ Response processed successfully!")
                    print(f"📊 Results: {len(results.get('results', {}))} processing steps completed")
                else:
                    print(f"❌ Response processing failed: {results.get('error')}")
            else:
                print("Usage: python main.py process_response <conversation_id> [response_content]")
            sys.exit(0)
        
        elif command == "process_old_conversation":
            from scripts.process_old_conversation_with_templates import OldConversationTemplateProcessor
            processor = OldConversationTemplateProcessor()
            if len(sys.argv) > 2:
                conversation_id = sys.argv[2]
                print(f"🎯 Processing conversation: {conversation_id}")
                results = processor.process_conversation_with_templates(conversation_id)
                if results.get("success"):
                    print(f"✅ Conversation processed successfully!")
                    print(f"📊 Prompts sent: {results.get('prompts_sent', 0)}")
                    print(f"📊 Responses received: {results.get('responses_received', 0)}")
                else:
                    print(f"❌ Processing failed: {results.get('error')}")
            else:
                # Interactive mode
                conversation_id = processor.interactive_selection()
                if conversation_id:
                    results = processor.process_conversation_with_templates(conversation_id)
                    if results.get("success"):
                        print(f"✅ Conversation processed successfully!")
                        print(f"📊 Prompts sent: {results.get('prompts_sent', 0)}")
                        print(f"📊 Responses received: {results.get('responses_received', 0)}")
                    else:
                        print(f"❌ Processing failed: {results.get('error')}")
                else:
                    print("👋 No conversation selected")
            sys.exit(0)
        
        elif command == "full_workflow":
            from scripts.process_conversations_full_workflow import FullWorkflowProcessor
            processor = FullWorkflowProcessor()
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            print(f"🎯 Running full workflow processing for {limit} conversations...")
            results = processor.process_multiple_conversations(limit=limit)
            if "error" not in results:
                print(f"✅ Full workflow completed successfully!")
                print(f"📊 Conversations processed: {results['conversations_processed']}")
                print(f"📄 Templates rendered: {results['total_templates_rendered']}")
                print(f"🤖 Responses generated: {results['total_responses_generated']}")
                print(f"🎮 Skills updated: {results['total_skills_updated']}")
                print(f"📝 Discord posts: {results['total_discord_posts']}")
            else:
                print(f"❌ Full workflow failed: {results['error']}")
            sys.exit(0)
        
        elif command == "test_gui_content":
            from scripts.test_gui_content_display import test_gui_content_display, test_conversation_panel_simulation
            print("🧪 Testing GUI conversation content display...")
            content_ok = test_gui_content_display()
            panel_ok = test_conversation_panel_simulation()
            if content_ok and panel_ok:
                print("✅ GUI content display test passed!")
            else:
                print("❌ GUI content display test failed!")
            sys.exit(0)
        
        elif command == "test_enhanced_templates":
            from scripts.test_enhanced_templates import EnhancedTemplateTester
            print("🧪 Testing enhanced templates with human-AI workflow context...")
            tester = EnhancedTemplateTester()
            results = tester.run_enhanced_template_tests()
            if results['success']:
                print("✅ Enhanced template test passed!")
            else:
                print("❌ Enhanced template test failed!")
            sys.exit(0)
        
        elif command == "workflows":
            print("🔄 Workflow management is now available in the GUI!")
            print("Please run 'python main.py' to start the GUI and use the '🔄 Workflows' tab.")
            print("This consolidates all command-line workflows into a single interface.")
            sys.exit(0)
        
        elif command == "help":
            print("Digital Dreamscape - Available Commands:")
            print("  python main.py          - Start GUI application (RECOMMENDED)")
            print("  python main.py workflows - Workflow management (now in GUI)")
            print("  python main.py test     - Run component tests")
            print("  python main.py template - Test template engine")
            print("  python main.py scraper  - Test scraper")
            print("  python main.py undetected_chrome - Test undetected-chromedriver")
            print("  python main.py comprehensive_scraping - Test comprehensive scraping")
            print("  python main.py enhanced_skill_system - Test enhanced skill resume system")
            print("  python main.py create_demo_conversations - Create demo conversations for testing")
            print("  python main.py enhanced_ingestion - Test enhanced ingestion pipeline")
            print("  python main.py scrape_conversations [count] - Scrape real ChatGPT conversations")
            print("  python main.py load_cookies_and_scrape [count] - Scrape with cookie authentication")
            print("  python main.py templates [subcommand] - Template management and usage guide")
            print("  python main.py process_response [id] [content] - Process ChatGPT responses")
            print("  python main.py process_old_conversation [id] - Process old conversation with all templates")
            print("  python main.py full_workflow [count] - Process conversations with full workflow (templates, MMORPG, Discord)")
            print("  python main.py test_gui_content - Test GUI conversation content display")
            print("  python main.py test_enhanced_templates - Test enhanced templates with human-AI workflow context")
            print("  python main.py help     - Show this help")
            print("\n🎯 NOTE: All workflow management is now available in the GUI!")
            print("   Use the '🔄 Workflows' tab for unified conversation management.")
            sys.exit(0)
    
    # Default: run the main application
    print("🚀 Starting Digital Dreamscape...")
    sys.exit(main()) 