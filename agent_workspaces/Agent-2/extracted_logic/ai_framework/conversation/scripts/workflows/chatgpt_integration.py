"""
ChatGPT Integration Workflow - Scraping & Setup
==============================================

This module handles all ChatGPT-related functionality including:
- Automated browser setup and login
- Cookie management and persistence  
- Conversation scraping with anti-detection
- Setup guidance for new users
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

from .base_workflow import BaseWorkflow, WorkflowResult
from .workflow_utils import WorkflowLogger, ErrorHandler, FileManager, SystemChecker

logger = logging.getLogger(__name__)


class ChatGPTIntegrationWorkflow(BaseWorkflow):
    """Handles ChatGPT integration, scraping, and setup."""
    
    def __init__(self):
        """Initialize ChatGPT integration workflow."""
        super().__init__()
        self.workflow_logger = WorkflowLogger("ChatGPT Integration")
        self.error_handler = ErrorHandler()
        self.cookies_dir = Path("data/cookies")
        self.cookie_file = self.cookies_dir / "chatgpt_cookies.json"
        
    async def execute(self) -> WorkflowResult:
        """Execute ChatGPT integration workflow."""
        try:
            self.start_workflow("ChatGPT Integration")
            await self.ensure_initialized()
            
            self.workflow_logger.phase("ChatGPT Integration Setup")
            
            # Check current setup status
            setup_status = await self.check_setup_status()
            
            if setup_status["needs_setup"]:
                # Guide user through setup
                await self.perform_initial_setup()
            else:
                # Verify existing setup
                await self.verify_existing_setup()
            
            # Test scraping capabilities
            scraping_result = await self.test_scraping_capabilities()
            
            self.finish_workflow("ChatGPT Integration")
            
            self.result.status = "completed"
            self.result.data = {
                "setup_status": setup_status,
                "scraping_result": scraping_result,
                "error_summary": self.error_handler.get_summary()
            }
            
            return self.result
            
        except Exception as e:
            logger.error(f"❌ ChatGPT integration workflow failed: {e}")
            self.result.status = "failed"
            self.result.add_error(str(e))
            return self.result
    
    async def check_setup_status(self) -> Dict[str, Any]:
        """Check ChatGPT setup status and requirements."""
        self.workflow_logger.step("Checking ChatGPT setup status")
        
        status = {
            "cookies_dir_exists": self.cookies_dir.exists(),
            "cookie_file_exists": self.cookie_file.exists(),
            "needs_setup": False,
            "setup_guidance": [],
            "chrome_available": False,
            "dependencies_available": False
        }
        
        try:
            # Check directory structure
            if not status["cookies_dir_exists"]:
                self.workflow_logger.info("Creating cookies directory...")
                FileManager.ensure_directory(str(self.cookies_dir))
                status["setup_guidance"].append("Created cookies directory")
            
            # Check cookie file
            if not status["cookie_file_exists"]:
                status["needs_setup"] = True
                status["setup_guidance"].extend([
                    "ChatGPT cookies not found",
                    "Browser will open for manual login on first run",
                    "Cookies will be saved automatically for future use"
                ])
            else:
                # Validate existing cookies
                cookie_data = FileManager.load_json(str(self.cookie_file))
                if cookie_data and cookie_data.get("setup_needed", True):
                    status["needs_setup"] = True
                    status["setup_guidance"].append("Cookie file exists but needs setup completion")
            
            # Check Chrome availability
            try:
                import undetected_chromedriver as uc
                status["chrome_available"] = True
                self.workflow_logger.success("Chrome driver available")
            except ImportError:
                status["chrome_available"] = False
                status["setup_guidance"].append("undetected-chromedriver not available")
                self.error_handler.add_warning("Chrome driver not available", "dependency_check")
            
            # Check scraping dependencies
            try:
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                status["dependencies_available"] = True
                self.workflow_logger.success("Selenium dependencies available")
            except ImportError:
                status["dependencies_available"] = False
                status["setup_guidance"].append("Selenium not available")
                self.error_handler.add_warning("Selenium not available", "dependency_check")
            
            self.workflow_logger.success("Setup status check completed")
            return status
            
        except Exception as e:
            self.error_handler.add_error(f"Failed to check setup status: {e}")
            status["needs_setup"] = True
            status["setup_guidance"].append(f"Setup check failed: {e}")
            return status
    
    async def perform_initial_setup(self):
        """Perform initial ChatGPT setup for new users."""
        self.workflow_logger.step("Performing initial ChatGPT setup")
        
        try:
            # Create placeholder cookie file with instructions
            cookie_instructions = {
                "instructions": "This file will be populated when you run ChatGPT scraping for the first time",
                "setup_needed": True,
                "how_to_setup": "Run any workflow that includes ChatGPT scraping - browser will open for login",
                "created_at": datetime.now().isoformat(),
                "auto_login_ready": False
            }
            
            FileManager.save_json(cookie_instructions, str(self.cookie_file))
            
            self.workflow_logger.success("Created placeholder cookie file with instructions")
            self.workflow_logger.info("Setup guidance provided - user can now run scraping workflows")
            
        except Exception as e:
            self.error_handler.add_error(f"Initial setup failed: {e}")
    
    async def verify_existing_setup(self):
        """Verify existing ChatGPT setup is functional."""
        self.workflow_logger.step("Verifying existing ChatGPT setup")
        
        try:
            cookie_data = FileManager.load_json(str(self.cookie_file))
            
            if cookie_data:
                setup_needed = cookie_data.get("setup_needed", True)
                auto_login_ready = cookie_data.get("auto_login_ready", False)
                
                if not setup_needed and auto_login_ready:
                    self.workflow_logger.success("ChatGPT setup verified - auto-login ready")
                else:
                    self.workflow_logger.info("ChatGPT setup exists but may need completion")
            else:
                self.workflow_logger.warning("Cookie file exists but contains no data")
                
        except Exception as e:
            self.error_handler.add_error(f"Setup verification failed: {e}")
    
    async def test_scraping_capabilities(self) -> Dict[str, Any]:
        """Test ChatGPT scraping capabilities without full execution."""
        self.workflow_logger.step("Testing scraping capabilities")
        
        try:
            # Test basic scraping setup without actually opening browser
            scraping_result = {
                "browser_setup_ready": False,
                "cookie_management_ready": False,
                "scraping_ready": False,
                "demo_mode_available": True
            }
            
            # Check if we can import scraping modules
            try:
                from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
                scraper = ChatGPTScraper()
                scraping_result["browser_setup_ready"] = True
                scraping_result["scraping_ready"] = True
                self.workflow_logger.success("ChatGPT scraper module available")
                
                # Check if cookies are ready for auto-login
                if self.cookie_file.exists():
                    cookie_data = FileManager.load_json(str(self.cookie_file))
                    if cookie_data and not cookie_data.get("setup_needed", True):
                        scraping_result["cookie_management_ready"] = True
                        self.workflow_logger.success("Cookie management ready")
                
            except ImportError as e:
                self.error_handler.add_warning(f"ChatGPT scraper not available: {e}")
                scraping_result["scraping_ready"] = False
            
            return scraping_result
            
        except Exception as e:
            self.error_handler.add_error(f"Scraping capability test failed: {e}")
            return {"error": str(e)}
    
    async def perform_scraping(self, max_conversations: int = -1, preview_mode: bool = False) -> Dict[str, Any]:
        """Perform actual ChatGPT conversation scraping."""
        self.workflow_logger.step("Performing ChatGPT conversation scraping")
        
        try:
            # Import scraper
            from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
            
            # Initialize scraper
            scraper = ChatGPTScraper()
            
            # Configure scraping parameters
            scraper_config = {
                "max_conversations": max_conversations if not preview_mode else 5,
                "save_cookies": True,
                "headless": False,  # Show browser for initial setup
                "timeout": 30
            }
            
            self.workflow_logger.info(f"Starting scraping with max_conversations: {scraper_config['max_conversations']}")
            
            # Perform scraping
            scraping_results = await scraper.scrape_conversations(**scraper_config)
            
            # Process results
            if scraping_results and scraping_results.get("success"):
                conversations = scraping_results.get("conversations", [])
                self.workflow_logger.success(f"Successfully scraped {len(conversations)} conversations")
                
                # Update cookie status
                if scraping_results.get("cookies_saved"):
                    await self._update_cookie_status()
                
                return {
                    "success": True,
                    "conversations_scraped": len(conversations),
                    "conversations": conversations,
                    "cookies_saved": scraping_results.get("cookies_saved", False)
                }
            else:
                error_msg = scraping_results.get("error", "Unknown scraping error")
                self.error_handler.add_error(f"Scraping failed: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            self.error_handler.add_error(f"Scraping execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _update_cookie_status(self):
        """Update cookie file to indicate successful setup."""
        try:
            cookie_data = FileManager.load_json(str(self.cookie_file))
            if cookie_data:
                cookie_data.update({
                    "setup_needed": False,
                    "auto_login_ready": True,
                    "last_updated": datetime.now().isoformat()
                })
                FileManager.save_json(cookie_data, str(self.cookie_file))
                self.workflow_logger.success("Updated cookie status - auto-login now ready")
        except Exception as e:
            self.error_handler.add_warning(f"Failed to update cookie status: {e}")
    
    async def get_demo_conversations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get demo conversations for testing without real scraping."""
        self.workflow_logger.step("Getting demo conversations")
        
        try:
            from dreamscape.scrapers.demo_conversations import DemoConversationGenerator
            demo_conversations = DemoConversationGenerator.get_demo_conversations(limit)
            
            self.workflow_logger.success(f"Retrieved {len(demo_conversations)} demo conversations")
            return demo_conversations
            
        except Exception as e:
            self.error_handler.add_warning(f"Demo conversations not available: {e}")
            
            # Fallback demo conversations
            return [
                {
                    "id": "demo_1",
                    "title": "Getting Started with AI Development",
                    "url": "https://chat.openai.com/c/demo_1",
                    "timestamp": datetime.now().isoformat(),
                    "captured_at": datetime.now().isoformat()
                },
                {
                    "id": "demo_2", 
                    "title": "Advanced Programming Techniques",
                    "url": "https://chat.openai.com/c/demo_2",
                    "timestamp": datetime.now().isoformat(),
                    "captured_at": datetime.now().isoformat()
                }
            ]
    
    def get_setup_guidance(self) -> List[str]:
        """Get setup guidance for users."""
        return [
            "🤖 ChatGPT Integration Setup:",
            "1. Install required dependencies: pip install selenium undetected-chromedriver",
            "2. Run any workflow that includes ChatGPT scraping",
            "3. Browser will open automatically for first-time login",
            "4. Log into ChatGPT manually when browser opens",
            "5. Cookies will be saved automatically for future use",
            "6. Subsequent runs will use auto-login",
            "",
            "💡 Tips:",
            "- Keep browser window visible during first setup",
            "- Don't close browser until scraping completes",
            "- Cookies are stored securely in data/cookies/",
            "- Setup only needs to be done once"
        ] 