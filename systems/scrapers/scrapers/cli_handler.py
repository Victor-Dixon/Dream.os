"""
CLI Handler for ChatGPT Scraper
Handles command-line interface and main function operations.
"""

import argparse
import logging

logger = logging.getLogger(__name__)

class CLIHandler:
    """Handles command-line interface operations for the ChatGPT scraper."""
    
    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """
        Create argument parser for command-line usage.
        
        Returns:
            Configured argument parser
        """
        parser = argparse.ArgumentParser(description="ChatGPT Scraper")
        parser.add_argument("--headless", action="store_true", help="Run in headless mode")
        parser.add_argument("--model", default="", help="Specific model to scrape")
        parser.add_argument("--output", default="chatgpt_chats.json", help="Output file")
        parser.add_argument("--timeout", type=int, default=30, help="Timeout for operations")
        parser.add_argument("--username", help="ChatGPT username/email")
        parser.add_argument("--password", help="ChatGPT password")
        parser.add_argument("--cookie-file", help="Path to cookie file for session persistence")
        parser.add_argument("--totp-secret", help="TOTP secret for 2FA")
        
        return parser
    
    @staticmethod
    def run_scraper_from_args(args, scraper_class):
        """
        Run scraper with arguments from command line.
        
        Args:
            args: Parsed command line arguments
            scraper_class: Scraper class to instantiate
            
        Returns:
            True if scraping successful, False otherwise
        """
        try:
            # Run scraper with credentials if provided
            with scraper_class(
                headless=args.headless, 
                timeout=args.timeout,
                username=args.username,
                password=args.password,
                cookie_file=args.cookie_file,
                totp_secret=args.totp_secret
            ) as scraper:
                success = scraper.run_scraper(model=args.model, output_file=args.output)
                
                if success:
                    print(f"✅ Scraping completed successfully. Results saved to {args.output}")
                    return True
                else:
                    print("❌ Scraping failed")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to run scraper: {e}")
            print(f"❌ Scraping failed with error: {e}")
            return False 