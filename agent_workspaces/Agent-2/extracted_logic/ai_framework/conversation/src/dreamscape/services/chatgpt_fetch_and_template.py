"""
chatgpt_fetch_and_template.py

Service for fetching ChatGPT conversations and applying templates, callable from scripts and GUI.
Reuses ChatGPTScraper and TemplateResponder logic for login, fetching, templating, and saving.
"""
import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Import core scraping and template logic
from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
from jinja2 import Environment, FileSystemLoader

# --- TemplateSpec type for clarity ---
class TemplateSpec:
    def __init__(self, path: str, variables: Dict[str, Any]):
        self.path = path
        self.variables = variables

# --- Main service function ---
def fetch_and_apply_templates(
    username: str,
    password: str,
    templates: List[TemplateSpec],
    output_dir: str = "data/conversations/",
    headless: bool = True,
    use_undetected: bool = True,
    cookie_file: Optional[str] = None,
    totp_secret: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> List[Dict]:
    """
    Logs into ChatGPT, fetches all conversations, applies each template to each conversation,
    and saves the results as .json files in output_dir.
    """
    # --- Setup logging ---
    logger = logger or logging.getLogger("chatgpt_fetch_and_template")
    logger.info("Starting fetch_and_apply_templates service...")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # --- Step 1: Login and fetch conversations ---
    with ChatGPTScraper(
        headless=headless,
        username=username,
        password=password,
        cookie_file=cookie_file,
        totp_secret=totp_secret,
        use_undetected=use_undetected
    ) as scraper:
        logger.info("Logging into ChatGPT and fetching conversations...")
        # Run the scraper workflow to fetch conversations
        conversations_file = os.path.join(output_dir, "chatgpt_conversations.json")
        if not scraper.run_scraper(output_file=conversations_file):
            logger.error("Failed to fetch conversations from ChatGPT.")
            return []
        # Load conversations from file
        with open(conversations_file, "r", encoding="utf-8") as f:
            conversations = json.load(f)
        logger.info(f"Fetched {len(conversations)} conversations.")

        # --- Step 2: Apply templates to each conversation ---
        env = Environment(loader=FileSystemLoader("."))
        results = []
        for conv in conversations:
            conv_id = conv.get("id") or conv.get("conversation_id") or "unknown"
            conv_results = {"conversation": conv, "templates": []}
            for template_spec in templates:
                try:
                    template = env.get_template(template_spec.path)
                    prompt = template.render({**template_spec.variables, **conv})
                    # Optionally, send prompt to ChatGPT here if needed (not automated in headless mode)
                    # For now, just save the rendered prompt
                    conv_results["templates"].append({
                        "template_path": template_spec.path,
                        "prompt": prompt,
                        "applied_at": datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.error(f"Failed to apply template {template_spec.path} to conversation {conv_id}: {e}")
            results.append(conv_results)

        # --- Step 3: Save results as .json files ---
        for conv_result in results:
            conv_id = conv_result["conversation"].get("id") or "unknown"
            out_path = Path(output_dir) / f"conversation_{conv_id}_templated.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(conv_result, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved templated conversation to {out_path}")

        logger.info(f"Completed template application for {len(results)} conversations.")
        return results

# --- Example CLI usage ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch ChatGPT conversations and apply templates.")
    parser.add_argument("--username", required=True, help="ChatGPT username/email")
    parser.add_argument("--password", required=True, help="ChatGPT password")
    parser.add_argument("--output-dir", default="data/conversations/", help="Output directory")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--template", action="append", nargs=2, metavar=("PATH", "VARS_JSON"), help="Template path and variables as JSON string")
    args = parser.parse_args()

    # Parse templates
    templates = []
    if args.template:
        for path, vars_json in args.template:
            templates.append(TemplateSpec(path, json.loads(vars_json)))
    else:
        print("No templates specified. Exiting.")
        exit(1)

    fetch_and_apply_templates(
        username=args.username,
        password=args.password,
        templates=templates,
        output_dir=args.output_dir,
        headless=args.headless
    ) 