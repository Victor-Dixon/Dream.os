#!/usr/bin/env python3
"""
Test All Templates on Conversation
Send multiple templates to ChatGPT via scraper and show real AI responses.
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List
import logging
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dreamscape.core.memory.manager import MemoryManager
from dreamscape.core.scraping_system import ScraperOrchestrator
from dreamscape.core.templates.template_engine import render_template
from dreamscape.core.mmorpg.mmorpg_engine import MMORPGEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TemplateTester:
    """Test multiple templates by sending them to ChatGPT and showing responses."""
    
    def __init__(self):
        """Initialize the template tester."""
        self.memory_manager = MemoryManager("dreamos_memory.db")
        self.mmorpg_engine = MMORPGEngine("dreamos_memory.db")
        self.scraper_orchestrator = None
        
        # Available templates to test
        self.templates = {
            "dreamscape_saga": "templates/dreamscape.j2",
            "enhanced_conversation_analysis": "templates/prompts/enhanced_conversation_analyzer.j2",
            "enhanced_devlog": "templates/prompts/enhanced_devlog_generator.j2", 
            "enhanced_action_planning": "templates/prompts/enhanced_action_planner.j2",
            "code_review": "templates/prompts/code_review.j2",
            "project_summary": "templates/prompts/project_summary.j2",
            "work_analysis": "templates/work_analysis.j2",
            "workflow_suggestions": "templates/workflow_suggestions.j2"
        }
        
        logger.info("Template tester initialized")
    
    def initialize_scraper(self) -> bool:
        """Initialize the scraper orchestrator."""
        try:
            logger.info("Initializing scraper orchestrator...")
            self.scraper_orchestrator = ScraperOrchestrator()
            
            # Initialize the browser
            success = self.scraper_orchestrator.initialize_browser()
            if not success:
                logger.error("Failed to initialize browser")
                return False
            
            logger.info("✅ Scraper orchestrator initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize scraper: {e}")
            return False
    
    def get_conversation_for_testing(self) -> Dict[str, Any]:
        """Get a conversation with substantial content for testing."""
        try:
            # Get recent conversations
            conversations = self.memory_manager.get_recent_conversations(limit=10)
            
            # Find one with substantial content
            for conv in conversations:
                content_length = len(conv.get('content', ''))
                if content_length > 2000:  # At least 2000 characters
                    logger.info(f"Selected conversation: {conv.get('title', 'Untitled')} ({content_length} chars)")
                    return conv
            
            # If none found, use the first one
            if conversations:
                conv = conversations[0]
                logger.info(f"Using conversation: {conv.get('title', 'Untitled')} ({len(conv.get('content', ''))} chars)")
                return conv
            
            raise Exception("No conversations found")
            
        except Exception as e:
            logger.error(f"Failed to get conversation: {e}")
            return None
    
    def prepare_template_context(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for template rendering."""
        try:
            # Get work patterns from recent conversations
            recent_convs = self.memory_manager.get_recent_conversations(limit=20)
            work_patterns = self._analyze_work_patterns(recent_convs)
            
            # Get MMORPG state
            mmorpg_state = self._get_mmorpg_state()
            
            # Get current skills
            current_skills = self._get_current_skills()
            
            # Get relevant history
            relevant_history = self._get_relevant_history(conversation, recent_convs)
            
            context = {
                # Conversation data
                "conversation_content": conversation.get('content', '')[:3000],  # Limit for API
                "conversation_title": conversation.get('title', 'Untitled'),
                "conversation_id": conversation.get('id', ''),
                "conversation_length": f"{len(conversation.get('content', ''))} characters",
                "analysis_type": "Template Testing Session",
                "timestamp": datetime.now().isoformat(),
                
                # Context data
                "work_patterns": work_patterns,
                "mmorpg_state": mmorpg_state,
                "current_skills": current_skills,
                "relevant_history": relevant_history,
                
                # Additional context for specific templates
                "CURRENT_MEMORY_STATE": f"Testing templates on conversation: {conversation.get('title', 'Untitled')}",
                "content_to_review": conversation.get('content', '')[:2000],
                "review_scope": "Full Analysis",
                "code_language": "Python",
                "project_context": "Dream.OS Digital Dreamscape Platform"
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Failed to prepare context: {e}")
            return {}
    
    def _analyze_work_patterns(self, conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze work patterns from conversations."""
        try:
            patterns = {
                "technologies": {},
                "topics": {},
                "challenges": {},
                "total_conversations": len(conversations)
            }
            
            # Simple pattern analysis
            for conv in conversations:
                content = conv.get('content', '').lower()
                
                # Technology patterns
                tech_keywords = ['python', 'javascript', 'api', 'database', 'gui', 'web', 'ai', 'ml']
                for tech in tech_keywords:
                    if tech in content:
                        patterns["technologies"][tech] = patterns["technologies"].get(tech, 0) + 1
                
                # Topic patterns
                topic_keywords = ['development', 'testing', 'optimization', 'integration', 'architecture']
                for topic in topic_keywords:
                    if topic in content:
                        patterns["topics"][topic] = patterns["topics"].get(topic, 0) + 1
                
                # Challenge patterns
                challenge_keywords = ['error', 'bug', 'issue', 'problem', 'fix', 'debug']
                for challenge in challenge_keywords:
                    if challenge in content:
                        patterns["challenges"][challenge] = patterns["challenges"].get(challenge, 0) + 1
            
            return patterns
            
        except Exception as e:
            logger.error(f"Failed to analyze work patterns: {e}")
            return {"technologies": {}, "topics": {}, "challenges": {}, "total_conversations": 0}
    
    def _get_mmorpg_state(self) -> Dict[str, Any]:
        """Get current MMORPG state."""
        try:
            player = self.mmorpg_engine.get_player()
            skills = self.mmorpg_engine.get_skills()
            
            return {
                "level": getattr(player, 'level', 1),
                "xp": getattr(player, 'xp', 0),
                "active_skills": len(skills) if skills else 0,
                "recent_achievements": [],
                "active_quests": []
            }
            
        except Exception as e:
            logger.error(f"Failed to get MMORPG state: {e}")
            return {"level": 1, "xp": 0, "active_skills": 0, "recent_achievements": [], "active_quests": []}
    
    def _get_current_skills(self) -> Dict[str, Any]:
        """Get current skill levels."""
        try:
            skills = self.mmorpg_engine.get_skills()
            if isinstance(skills, dict):
                return {name: getattr(skill, 'current_level', 1) for name, skill in skills.items()}
            elif isinstance(skills, list):
                return {getattr(skill, 'name', f'Skill{i}'): getattr(skill, 'current_level', 1) 
                       for i, skill in enumerate(skills)}
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Failed to get current skills: {e}")
            return {}
    
    def _get_relevant_history(self, target_conv: Dict[str, Any], all_convs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get relevant conversation history."""
        try:
            relevant = []
            target_content = target_conv.get('content', '').lower()
            
            for conv in all_convs[:5]:  # Last 5 conversations
                if conv.get('id') == target_conv.get('id'):
                    continue
                
                content = conv.get('content', '').lower()
                
                # Simple relevance scoring
                relevance_score = 0
                common_words = set(target_content.split()) & set(content.split())
                relevance_score = len(common_words) / 10  # Normalize
                
                if relevance_score > 0.1:  # Only include somewhat relevant
                    relevant.append({
                        "title": conv.get('title', 'Untitled'),
                        "timestamp": conv.get('timestamp', ''),
                        "content": conv.get('content', '')[:200],
                        "relevance_score": relevance_score
                    })
            
            return relevant[:3]  # Top 3 most relevant
            
        except Exception as e:
            logger.error(f"Failed to get relevant history: {e}")
            return []
    
    def test_template(self, template_name: str, template_path: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single template by sending it to ChatGPT."""
        try:
            logger.info(f"🧪 Testing template: {template_name}")
            
            # Check if template exists
            if not os.path.exists(template_path):
                return {
                    "success": False,
                    "error": f"Template not found: {template_path}",
                    "template_name": template_name
                }
            
            # Read and render template
            logger.info(f"📝 Rendering template: {template_name}")
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            rendered_prompt = render_template(template_content, context)
            
            if not rendered_prompt:
                return {
                    "success": False,
                    "error": "Failed to render template",
                    "template_name": template_name
                }
            
            logger.info(f"📤 Sending template to ChatGPT ({len(rendered_prompt)} characters)")
            
            # Send to ChatGPT via scraper
            result = self.scraper_orchestrator.send_content_to_chat(
                content=rendered_prompt,
                wait_for_response=True,
                create_new_conversation=True
            )
            
            if result.success:
                logger.info(f"✅ Template {template_name} sent successfully")
                return {
                    "success": True,
                    "template_name": template_name,
                    "prompt": rendered_prompt,
                    "response": result.response,
                    "response_length": len(result.response) if result.response else 0
                }
            else:
                logger.error(f"❌ Template {template_name} failed: {result.error}")
                return {
                    "success": False,
                    "error": result.error,
                    "template_name": template_name,
                    "prompt": rendered_prompt
                }
                
        except Exception as e:
            logger.error(f"❌ Error testing template {template_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "template_name": template_name
            }
    
    def run_all_templates_test(self, conversation_id: str = None) -> Dict[str, Any]:
        """Run all templates on a conversation and show responses."""
        try:
            print("🚀 Testing All Templates on Conversation")
            print("=" * 80)
            
            # Initialize scraper
            if not self.initialize_scraper():
                return {"success": False, "error": "Failed to initialize scraper"}
            
            # Get conversation
            if conversation_id:
                conversation = self.memory_manager.get_conversation_by_id(conversation_id)
                if not conversation:
                    return {"success": False, "error": f"Conversation {conversation_id} not found"}
            else:
                conversation = self.get_conversation_for_testing()
                if not conversation:
                    return {"success": False, "error": "No suitable conversation found"}
            
            print(f"📝 Testing on conversation: {conversation.get('title', 'Untitled')}")
            print(f"📄 Content length: {len(conversation.get('content', ''))} characters")
            print()
            
            # Prepare context
            print("🔍 Preparing template context...")
            context = self.prepare_template_context(conversation)
            print(f"✅ Context prepared with {len(context.get('work_patterns', {}).get('technologies', {}))} technologies")
            print()
            
            # Test each template
            results = {}
            successful_tests = 0
            
            for template_name, template_path in self.templates.items():
                print(f"🧪 Testing: {template_name}")
                print("-" * 60)
                
                result = self.test_template(template_name, template_path, context)
                results[template_name] = result
                
                if result["success"]:
                    successful_tests += 1
                    print(f"✅ SUCCESS: {template_name}")
                    print(f"📤 Prompt length: {len(result.get('prompt', ''))} characters")
                    print(f"📥 Response length: {result.get('response_length', 0)} characters")
                    
                    # Show response preview
                    response = result.get('response', '')
                    if response:
                        preview = response[:300].replace('\n', ' ')
                        if len(response) > 300:
                            preview += "..."
                        print(f"📋 Response preview: {preview}")
                    
                    # Check for saga narrator JSON
                    if "```json" in response:
                        print("🎯 Contains structured JSON (saga narrator format)")
                    
                    print()
                else:
                    print(f"❌ FAILED: {template_name}")
                    print(f"   Error: {result.get('error', 'Unknown error')}")
                    print()
                
                # Small delay between requests
                import time
                time.sleep(2)
            
            # Summary
            print("=" * 80)
            print("📊 TEMPLATE TESTING SUMMARY")
            print(f"✅ Successful: {successful_tests}/{len(self.templates)}")
            print(f"❌ Failed: {len(self.templates) - successful_tests}/{len(self.templates)}")
            print()
            
            # Show successful results
            if successful_tests > 0:
                print("🎉 SUCCESSFUL TEMPLATE RESPONSES:")
                print("=" * 80)
                
                for template_name, result in results.items():
                    if result["success"]:
                        print(f"\n📋 {template_name.upper()}:")
                        print("-" * 40)
                        response = result.get('response', '')
                        if response:
                            # Show first 500 characters
                            preview = response[:500]
                            if len(response) > 500:
                                preview += "\n\n... (truncated)"
                            print(preview)
                        print()
            
            return {
                "success": True,
                "conversation": conversation,
                "results": results,
                "successful_tests": successful_tests,
                "total_tests": len(self.templates)
            }
            
        except Exception as e:
            logger.error(f"❌ Template testing failed: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            # Clean up
            if self.scraper_orchestrator:
                try:
                    self.scraper_orchestrator.close()
                except:
                    pass

def main():
    """Main function to run template testing."""
    try:
        tester = TemplateTester()
        
        # You can specify a conversation ID or let it pick one
        # conversation_id = "67d9ebb0-daa0-8009-876a-c5ccdc2b738f"  # Agent Architecture Overview
        conversation_id = None  # Let it pick the best one
        
        result = tester.run_all_templates_test(conversation_id)
        
        if result["success"]:
            print("🎉 Template testing completed successfully!")
        else:
            print(f"❌ Template testing failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 