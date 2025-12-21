# Comment-Code Mismatch Report

**Date**: 1765575800.0
**Total Mismatches**: 1738

## Summary

- High severity: 1636
- Medium severity: 102
- Low severity: 0

## Detailed Results

### agent_workspaces\Agent-1\extracted_patterns\patterns\error_handler_pattern.py

**Line 17** (high): docstring_param_mismatch
- Comment: `
        Initialize error handler.
        
        Args:
            show_stack_trace: If None, aut`
- Code: `def __init__(self, show_stack_trace)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'show_stack_trace'}

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Handle error and return formatted error response.
        
        Args:
            error:`
- Code: `def handle_error(self, error, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Format error for API response.
        
        Args:
            error: Exception to forma`
- Code: `def format_error_response(self, error, status_code)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

### agent_workspaces\Agent-1\extracted_patterns\utilities\project_scanner.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
        :param project_root: The root directory of the project to scan.
        `
- Code: `def __init__(self, project_root)`
- Issue: Docstring params don't match: missing=set(), extra={'self'}

**Line 100** (high): docstring_param_mismatch
- Comment: `
        Calculates an MD5 hash of a file's content.

        :param file_path: Path to the file to `
- Code: `def hash_file(self, file_path)`
- Issue: Docstring params don't match: missing={'return'}, extra={'self'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\chatgpt_api_client.py

**Line 71** (high): comment_return_mismatch
- Comment: `Return mock data for now`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\conversation_storage.py

**Line 90** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation storage.

        Args:
            connection: SQLite connecti`
- Code: `def __init__(self, connection)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'connection'}

**Line 244** (high): docstring_param_mismatch
- Comment: `
        Store a conversation in the database.

        Args:
            conversation_data: Diction`
- Code: `def store_conversation(self, conversation_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'conversation_data', 'self'}

**Line 291** (high): docstring_param_mismatch
- Comment: `
        Retrieve a conversation by ID.

        Args:
            conversation_id: ID of the conver`
- Code: `def get_conversation_by_id(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 406** (high): docstring_param_mismatch
- Comment: `
        Get the total number of conversations in the database.

        Returns:
            Total `
- Code: `def get_conversations_count(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 421** (high): docstring_param_mismatch
- Comment: `
        Get conversations from the database.

        Args:
            limit: Maximum number of co`
- Code: `def get_conversations(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 459** (high): docstring_param_mismatch
- Comment: `Insert many conversations in one executemany call.

        Parameters
        ----------
        ro`
- Code: `def store_conversations_bulk(self, rows)`
- Issue: Docstring params don't match: missing={'py'}, extra={'self', 'rows'}

**Line 492** (high): docstring_param_mismatch
- Comment: `
        Update conversation content, message count, and word count.

        Args:
            conv`
- Code: `def update_conversation_content(self, conversation_id, content, message_count, word_count)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\intelligence\analysis\conversation_analyzer.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Analyze the quality of a response.
        
        Args:
            conversation_id: ID o`
- Code: `def analyze_response_quality(self, conversation_id, response_content, conversation_content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\legacy\chatgpt_dreamscape_agent.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Process a conversation using ChatGPT for narrative generation and memory updates.
        
`
- Code: `def process_conversation_with_ai(self, conversation_id, conversation_content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 107** (high): docstring_param_mismatch
- Comment: `
        Send a direct query to the Dreamscape AI.
        
        Args:
            query: The que`
- Code: `def query_dreamscape_ai(self, query, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\memory\storage\conversation_operations.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
        Initialize conversation operations.
        
        Args:
            conn: SQLite databas`
- Code: `def __init__(self, conn)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'conn'}

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Store a conversation in the database.
        
        Args:
            conversation_data:`
- Code: `def store_conversation(self, conversation_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'conversation_data', 'self'}

**Line 68** (high): docstring_param_mismatch
- Comment: `
        Retrieve a conversation by ID.
        
        Args:
            conversation_id: Conversa`
- Code: `def get_conversation_by_id(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Get recent conversations ordered by creation date.
        
        Args:
            limit`
- Code: `def get_recent_conversations(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Get conversations ordered chronologically by timestamp.
        
        Args:
            `
- Code: `def get_conversations_chronological(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 183** (high): docstring_param_mismatch
- Comment: `
        Get statistics about stored conversations.
        
        Returns:
            Dictionary`
- Code: `def get_conversation_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 225** (high): docstring_param_mismatch
- Comment: `
        Delete a conversation and its associated data.
        
        Args:
            conversat`
- Code: `def delete_conversation(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\utils\chat_navigation.py

**Line 19** (high): docstring_param_mismatch
- Comment: `
    Ensures the conversation is accessible and chat input is interactable.
    Handles redirect iss`
- Code: `def robust_navigate_to_convo(driver, convo_id, model, timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'driver'}

**Line 116** (high): docstring_param_mismatch
- Comment: `
    Wait for the chat interface to be ready for input.
    
    Args:
        driver: Selenium WebD`
- Code: `def wait_for_chat_ready(driver, timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'driver'}

**Line 144** (high): docstring_param_mismatch
- Comment: `
    Send a prompt to the current chat and wait for response.
    
    Args:
        driver: Seleniu`
- Code: `def send_prompt_to_chat(driver, prompt_text, timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'driver'}

**Line 194** (high): docstring_param_mismatch
- Comment: `
    Wait for ChatGPT to finish responding and capture the response.
    
    Args:
        driver: `
- Code: `def wait_for_chatgpt_response(driver, timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'driver'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\core\workflow\pipelines\conversation_pipeline.py

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Initialize the unified conversation workflow.
        
        Args:
            memory_man`
- Code: `def __init__(self, memory_manager, template_engine, discord_manager, mmorpg_engine, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'memory_manager'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\chatgpt_scraper.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Initialize the ChatGPT scraper.
        
        Args:
            headless: Run browser in`
- Code: `def __init__(self, headless, timeout, use_undetected, username, password, cookie_file, totp_secret)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'headless'}

**Line 90** (high): docstring_param_mismatch
- Comment: `
        Navigate to ChatGPT with optional model selection.
        
        Args:
            model`
- Code: `def navigate_to_chatgpt(self, model)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'model', 'self'}

**Line 120** (high): docstring_param_mismatch
- Comment: `
        Check if user is logged in using the login handler.
        
        Returns:
            T`
- Code: `def is_logged_in(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 137** (high): docstring_param_mismatch
- Comment: `
        Run the complete scraping workflow.
        
        Args:
            model: Specific mode`
- Code: `def run_scraper(self, model, output_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'model', 'self'}

**Line 192** (high): docstring_param_mismatch
- Comment: `
        Enter a specific conversation using the conversation extractor.
        
        Args:
    `
- Code: `def enter_conversation(self, conversation_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_url'}

**Line 204** (high): docstring_param_mismatch
- Comment: `
        Get content from the current conversation using the conversation extractor.
        
      `
- Code: `def get_conversation_content(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 213** (high): docstring_param_mismatch
- Comment: `
        Send a prompt to the current conversation using the conversation extractor.
        
      `
- Code: `def send_prompt(self, prompt, wait_for_response)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'prompt'}

**Line 226** (high): docstring_param_mismatch
- Comment: `
        Run templated prompts on a list of conversations.
        
        Args:
            conver`
- Code: `def run_templated_prompts(self, conversations, prompt_template)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversations'}

**Line 245** (high): docstring_param_mismatch
- Comment: `
        Ensure user is logged in with comprehensive fallback strategy.
        
        This is the`
- Code: `def ensure_login(self, allow_manual, manual_timeout)`
- Issue: Docstring params don't match: missing={'Strategy', 'Returns', 'Args'}, extra={'self', 'allow_manual'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\conversation\conversation_scraper.py

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation scraper.
        
        Args:
            **kwargs: Arguments`
- Code: `def __init__(self)`
- Issue: Docstring params don't match: missing={'kwargs'}, extra={'self'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Main scraping method for conversations.
        
        Args:
            max_conversation`
- Code: `def scrape(self, max_conversations, include_content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'max_conversations', 'self'}

**Line 117** (high): docstring_param_mismatch
- Comment: `
        Scrape the list of conversations from the sidebar.
        
        Args:
            max_c`
- Code: `def _scrape_conversation_list(self, max_conversations)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'max_conversations', 'self'}

**Line 170** (high): docstring_param_mismatch
- Comment: `
        Extract metadata from a conversation link element.
        
        Args:
            link_`
- Code: `def _extract_conversation_metadata(self, link_element, index)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'link_element'}

**Line 206** (high): docstring_param_mismatch
- Comment: `
        Scrape full content for each conversation.
        
        Args:
            conversations`
- Code: `def _scrape_conversation_content(self, conversations)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversations'}

**Line 247** (high): docstring_param_mismatch
- Comment: `
        Scrape all messages from the current conversation.
        
        Returns:
            Li`
- Code: `def _scrape_messages(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 292** (high): docstring_param_mismatch
- Comment: `
        Extract a single message from its container.
        
        Args:
            container: `
- Code: `def _extract_message(self, container, index)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'container'}

**Line 346** (high): docstring_param_mismatch
- Comment: `
        Calculate statistics for a conversation.
        
        Args:
            messages: List `
- Code: `def _calculate_conversation_stats(self, messages)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'messages', 'self'}

**Line 376** (high): docstring_param_mismatch
- Comment: `
        Validate the scraping result.
        
        Args:
            result: Scraped data to va`
- Code: `def validate_scrape_result(self, result)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'result'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\conversation\unified_conversation_scraper.py

**Line 47** (high): docstring_param_mismatch
- Comment: `
        Initialize the unified conversation scraper.
        
        Args:
            timeout: Ti`
- Code: `def __init__(self, timeout, scrolling_strategy, max_conversations, scroll_delay)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'timeout', 'self'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Get all conversations using the configured scrolling strategy.
        
        Args:
     `
- Code: `def get_conversation_list(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 462** (high): docstring_param_mismatch
- Comment: `
        Run the complete scraping process.
        
        Args:
            driver: Selenium WebD`
- Code: `def run_scraper(self, driver, output_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\conversation_extractor.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation extractor.
        
        Args:
            timeout: Timeout `
- Code: `def __init__(self, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'timeout', 'self'}

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Navigate to a specific conversation.
        
        Args:
            driver: Selenium we`
- Code: `def enter_conversation(self, driver, conversation_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\conversation_extractor_legacy.py

**Line 18** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation extractor.
        
        Args:
            timeout: Timeout `
- Code: `def __init__(self, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'timeout', 'self'}

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Find the scrollport container for conversation list.
        
        Args:
            dri`
- Code: `def find_scrollport_container(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
        Get list of conversations using scrollport scrolling.
        
        Args:
            dr`
- Code: `def get_conversation_list(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 93** (high): docstring_param_mismatch
- Comment: `
        Perform scrollport scrolling to load all conversations.
        
        Args:
            `
- Code: `def _scrollport_scroll(self, driver, scroll_container)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'driver'}

**Line 134** (high): docstring_param_mismatch
- Comment: `
        Extract conversation data from the page.
        
        Args:
            driver: Seleniu`
- Code: `def _extract_conversations(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\conversation_list_manager.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation list manager.
        
        Args:
            timeout: Timeo`
- Code: `def __init__(self, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'timeout', 'self'}

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Get list of available conversations with improved scrolling.
        Args:
            driv`
- Code: `def get_conversation_list(self, driver, max_conversations, use_cache, cache_file, skip_before, skip_titles, progress_callback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'use_cache', 'cache_file', 'skip_titles', 'self', 'driver', 'skip_before'}

**Line 186** (high): docstring_param_mismatch
- Comment: `
        Perform burst scrolling to try to load more content.
        
        Args:
            dri`
- Code: `def _burst_scroll(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamscape\scrapers\demo_conversations.py

**Line 16** (high): docstring_param_mismatch
- Comment: `
        Return a small set of demo conversations for offline/testing flows.

        Priority:
    `
- Code: `def get_demo_conversations(limit)`
- Issue: Docstring params don't match: missing={'Priority', 'Returns', 'Args'}, extra={'limit'}

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Generate static demo conversations for fallback scenarios.
        
        Args:
         `
- Code: `def _get_static_demo_conversations(limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'limit'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamvault\agents\conversation_agent.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation agent trainer.
        
        Args:
            training_data`
- Code: `def __init__(self, training_data_dir, model_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'training_data_dir', 'self'}

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Load conversation pairs from training data.
        
        Returns:
            List of c`
- Code: `def load_training_data(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Prepare training data in the format expected by training frameworks.
        
        Args:`
- Code: `def prepare_training_data(self, pairs)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'pairs', 'self'}

**Line 116** (high): docstring_param_mismatch
- Comment: `
        Train using OpenAI's fine-tuning API.
        
        Args:
            training_data: Pre`
- Code: `def train_with_openai(self, training_data, api_key)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'training_data'}

**Line 183** (high): docstring_param_mismatch
- Comment: `
        Train using Hugging Face transformers.
        
        Args:
            training_data: Pr`
- Code: `def train_with_huggingface(self, training_data, model_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'training_data'}

**Line 273** (high): docstring_param_mismatch
- Comment: `
        Train using local LLM (e.g., Llama, Mistral).
        
        Args:
            training_d`
- Code: `def train_with_local_llm(self, training_data, model_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'training_data'}

**Line 297** (high): docstring_param_mismatch
- Comment: `
        Generate response using trained model.
        
        Args:
            input_text: User `
- Code: `def generate_response(self, input_text, model_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'input_text'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamvault\scrapers\chatgpt_scraper.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Initialize the ChatGPT scraper.
        
        Args:
            headless: Run browser in`
- Code: `def __init__(self, headless, use_undetected, username, password, totp_secret, cookie_file, rate_limit_delay, progress_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'headless'}

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Ensure user is logged into ChatGPT.
        
        Args:
            allow_manual: Allow `
- Code: `def ensure_login(self, allow_manual, manual_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'allow_manual'}

**Line 159** (high): docstring_param_mismatch
- Comment: `
        Select a specific ChatGPT model.
        
        Args:
            model: Model to select `
- Code: `def select_model(self, model)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'model', 'self'}

**Line 205** (high): docstring_param_mismatch
- Comment: `
        Get list of available conversations with self-healing.
        
        Args:
            p`
- Code: `def get_conversation_list(self, progress_callback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'progress_callback'}

**Line 234** (high): docstring_param_mismatch
- Comment: `
        Extract a single conversation.
        
        Args:
            conversation_url: URL of `
- Code: `def extract_conversation(self, conversation_url, output_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_url'}

**Line 275** (high): docstring_param_mismatch
- Comment: `
        Extract all available conversations with resume functionality.
        
        Args:
     `
- Code: `def extract_all_conversations(self, limit, output_dir, progress_callback, skip_processed)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\conversation\src\dreamvault\scrapers\conversation_extractor.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
        Initialize the conversation extractor.
        
        Args:
            timeout: Timeout `
- Code: `def __init__(self, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'timeout', 'self'}

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Get list of available conversations with infinite scrolling.
        
        Args:
       `
- Code: `def get_conversation_list(self, driver, progress_callback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 168** (high): docstring_param_mismatch
- Comment: `
        Navigate to a specific conversation.
        
        Args:
            driver: Selenium we`
- Code: `def enter_conversation(self, driver, conversation_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 219** (high): docstring_param_mismatch
- Comment: `
        Extract content from the current conversation.
        
        Args:
            driver: S`
- Code: `def get_conversation_content(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 304** (high): docstring_param_mismatch
- Comment: `
        Save conversation data to file.
        
        Args:
            conversation_data: Conve`
- Code: `def save_conversation(self, conversation_data, output_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'conversation_data', 'self'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\agent_devlog_trainer.py

**Line 26** (high): comment_return_mismatch
- Comment: `return ContextUtils`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\legacy\model_config_manager.py

**Line 103** (high): docstring_param_mismatch
- Comment: `
        Generate a model-specific ChatGPT URL.
        
        Args:
            conversation_id: `
- Code: `def get_model_url(self, conversation_id, model)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\training_data_orchestrator.py

**Line 17** (high): docstring_param_mismatch
- Comment: `
    Run structured training data extraction with comprehensive configuration.
    
    Args:
      `
- Code: `def run_structured_training_data_extraction(memory_manager, template_engine, output_dir, categories, max_samples_per_category, include_conversations, include_templates)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'memory_manager'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\core\workflow\pipelines\daily_pipeline.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Initialize the daily conversation pipeline.
        
        Args:
            memory_manag`
- Code: `def __init__(self, memory_manager, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'memory_manager'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\main_window_original_backup.py

**Line 1436** (high): docstring_param_mismatch
- Comment: `Handle actions coming from TemplatesPanel (edit or send).

        Enhanced: If OpenAI API key is no`
- Code: `def _handle_template_action(self, payload)`
- Issue: Docstring params don't match: missing={'Enhanced'}, extra={'self', 'payload'}

**Line 617** (high): comment_return_mismatch
- Comment: `returns list[dict]`
- Code: `templates = self.memory_manager.get_templates()`
- Issue: Comment says 'returns' but code doesn't return

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamscape\gui\panels\training_data_panel.py

**Line 608** (high): comment_return_mismatch
- Comment: `Override the data getter to return our training data`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\src\dreamvault\deployment\model_manager.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Initialize the model manager.
        
        Args:
            models_dir: Directory cont`
- Code: `def __init__(self, models_dir)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'models_dir'}

**Line 48** (high): docstring_param_mismatch
- Comment: `
        Discover available trained models.
        
        Returns:
            Dictionary of mode`
- Code: `def discover_models(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 122** (high): docstring_param_mismatch
- Comment: `
        Load a trained model into memory.
        
        Args:
            model_name: Name of th`
- Code: `def load_model(self, model_name, force_reload)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'model_name'}

**Line 261** (high): docstring_param_mismatch
- Comment: `
        Unload a model from memory.
        
        Args:
            model_name: Name of the mode`
- Code: `def unload_model(self, model_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'model_name'}

**Line 301** (high): docstring_param_mismatch
- Comment: `
        Get a loaded model.
        
        Args:
            model_name: Name of the model to get`
- Code: `def get_model(self, model_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'model_name'}

**Line 318** (high): docstring_param_mismatch
- Comment: `
        List all available and loaded models.
        
        Returns:
            Dictionary with`
- Code: `def list_models(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 336** (high): docstring_param_mismatch
- Comment: `
        Get statistics for a specific model.
        
        Args:
            model_name: Name of`
- Code: `def get_model_stats(self, model_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'model_name'}

**Line 348** (high): docstring_param_mismatch
- Comment: `
        Update model statistics.
        
        Args:
            model_name: Name of the model
 `
- Code: `def update_model_stats(self, model_name, response_time, success)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'model_name'}

**Line 372** (high): docstring_param_mismatch
- Comment: `
        Start health check thread.
        
        Args:
            interval: Health check interv`
- Code: `def start_health_check(self, interval)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'interval'}

### agent_workspaces\Agent-2\extracted_logic\ai_framework\models\tests\integration\test_agent_training_system.py

**Line 814** (high): comment_raise_mismatch
- Comment: `Should not raise exceptions`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### agent_workspaces\Agent-3\infrastructure_audit_scanner.py

**Line 200** (high): docstring_param_mismatch
- Comment: `Classify repo: KEEP, NEEDS WORK, or ARCHIVE.`
- Code: `def classify_repo(self, repo, infra_score, burden)`
- Issue: Docstring params don't match: missing=set(), extra={'self', 'burden', 'infra_score'}

### agent_workspaces\Agent-5\registry_plugin_discovery_proof_of_concept.py

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Auto-discover engines implementing Engine protocol.
        
        This method:
        1`
- Code: `def _discover_engines(self)`
- Issue: Docstring params don't match: missing={'method', 'Raises'}, extra={'self'}

**Line 112** (high): docstring_param_mismatch
- Comment: `
        Find Engine implementation in module.
        
        Looks for classes that:
        1. A`
- Code: `def _find_engine_class(self, module)`
- Issue: Docstring params don't match: missing={'Returns', 'Args', 'that'}, extra={'module', 'self'}

### agent_workspaces\Agent-7\C-024_PRIORITY2_UNIFIED_CONFIGS.py

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Calculate delay for given attempt with exponential backoff and jitter.
        
        Arg`
- Code: `def calculate_delay(self, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'attempt'}

**Line 104** (high): docstring_param_mismatch
- Comment: `
        Determine if operation should be retried.
        
        Args:
            error: Excepti`
- Code: `def should_retry(self, error, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

### docs\examples\gaming_integration_core_examples.py

**Line 26** (high): docstring_param_mismatch
- Comment: `Example 1: Create and manage a basic game session.`
- Code: `def example_basic_session()`
- Issue: Docstring params don't match: missing={'1'}, extra=set()

**Line 59** (high): docstring_param_mismatch
- Comment: `Example 2: Multi-player game session management.`
- Code: `def example_multi_player()`
- Issue: Docstring params don't match: missing={'2'}, extra=set()

**Line 99** (high): docstring_param_mismatch
- Comment: `Example 3: Managing multiple entertainment systems.`
- Code: `def example_entertainment_systems()`
- Issue: Docstring params don't match: missing={'3'}, extra=set()

**Line 142** (high): docstring_param_mismatch
- Comment: `Example 4: Event-driven game management.`
- Code: `def example_event_driven()`
- Issue: Docstring params don't match: missing={'4'}, extra=set()

**Line 184** (high): docstring_param_mismatch
- Comment: `Example 5: Register and use custom event handler.`
- Code: `def example_custom_handler()`
- Issue: Docstring params don't match: missing={'5'}, extra=set()

**Line 235** (high): docstring_param_mismatch
- Comment: `Example 6: Monitor gaming core health.`
- Code: `def example_health_monitoring()`
- Issue: Docstring params don't match: missing={'6'}, extra=set()

**Line 276** (high): docstring_param_mismatch
- Comment: `Example 7: Advanced dependency injection.`
- Code: `def example_dependency_injection()`
- Issue: Docstring params don't match: missing={'7'}, extra=set()

### dream\repos\master\dadudekc\test_q_learning.py

**Line 100** (high): comment_raise_mismatch
- Comment: `This should not raise an error`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 120** (high): comment_return_mismatch
- Comment: `This should not raise an error, just return early`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 120** (high): comment_raise_mismatch
- Comment: `This should not raise an error, just return early`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### dream\repos\master\dadudekc\train_cartpole.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
    Train CartPole with Q-learning
    
    Args:
        episodes: Number of training episodes
   `
- Code: `def train_cartpole(episodes, gamma, epsilon_start, epsilon_min, epsilon_decay, batch_size, memory_size, learning_rate, save_interval)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'episodes'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
    Evaluate a trained model
    
    Args:
        model_path: Path to the trained model
        e`
- Code: `def evaluate_model(model_path, episodes)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'model_path'}

### examples\webhook_management_demo.py

**Line 20** (high): docstring_param_mismatch
- Comment: `Demo: List existing webhooks from config.`
- Code: `def demo_list_webhooks()`
- Issue: Docstring params don't match: missing={'Demo'}, extra=set()

**Line 43** (high): docstring_param_mismatch
- Comment: `Demo: Save a webhook URL to config.`
- Code: `def demo_save_webhook()`
- Issue: Docstring params don't match: missing={'Demo'}, extra=set()

**Line 75** (high): docstring_param_mismatch
- Comment: `Demo: Test a webhook (will fail if not configured).`
- Code: `def demo_test_webhook()`
- Issue: Docstring params don't match: missing={'Demo'}, extra=set()

**Line 103** (high): docstring_param_mismatch
- Comment: `Demo: Use all-in-one webhook manager.`
- Code: `def demo_webhook_manager()`
- Issue: Docstring params don't match: missing={'Demo'}, extra=set()

**Line 139** (high): docstring_param_mismatch
- Comment: `Demo: Complete agent workflow for webhook usage.`
- Code: `def demo_agent_workflow()`
- Issue: Docstring params don't match: missing={'Demo'}, extra=set()

### scripts\enforce_python_standards.py

**Line 50** (high): docstring_param_mismatch
- Comment: `Enforce Python coding standards on all Python files.

        Args:
            root_path: Root path`
- Code: `def enforce_standards(self, root_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'root_path', 'self'}

### scripts\index_v2_refactoring.py

**Line 203** (high): docstring_param_mismatch
- Comment: `Index all V2 compliance refactoring work into vector database.

        Returns:
            int: Nu`
- Code: `def index_refactoring_work(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 240** (high): docstring_param_mismatch
- Comment: `Index a single file into the vector database.

        Args:
            file_path: Path to the file`
- Code: `def _index_single_file(self, file_path, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'file_path'}

### scripts\test_queue_processing_delivery_logging.py

**Line 197** (high): docstring_param_mismatch
- Comment: `Test complete end-to-end flow: queue → process → deliver → log.`
- Code: `def test_end_to_end_flow()`
- Issue: Docstring params don't match: missing={'flow'}, extra=set()

### scripts\v2_refactoring_tracker.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
    Scan for V2 compliance violations.
    
    Args:
        src_dir: Source directory to scan
   `
- Code: `def scan_violations(src_dir, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'src_dir'}

**Line 56** (high): docstring_param_mismatch
- Comment: `
    Categorize violations by severity.
    
    Args:
        violations: List of (file_path, line_`
- Code: `def categorize_violations(violations)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'violations'}

**Line 83** (high): docstring_param_mismatch
- Comment: `
    Generate progress report comparing to baseline.
    
    Args:
        violations: Current viol`
- Code: `def generate_progress_report(violations, baseline_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'violations'}

### scripts\validate_refactored_files.py

**Line 83** (high): docstring_param_mismatch
- Comment: `
    Validate multiple refactored files.
    
    Args:
        file_paths: List of file paths to va`
- Code: `def validate_refactored_files(file_paths, loc_limit, output_format)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_paths'}

### scripts\validate_v2_compliance.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
    Validate V2 compliance.
    
    Args:
        rules_file: Path to V2 rules YAML file (optional`
- Code: `def validate_v2_compliance(rules_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'rules_file'}

### src\ai_automation\utils\filesystem.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
    Make a file executable by adding execute permissions.

    Args:
        path: Path to the file`
- Code: `def make_executable(path)`
- Issue: Docstring params don't match: missing={'Note', 'Raises', 'Args'}, extra={'path'}

### src\ai_training\dreamvault\database.py

**Line 43** (high): docstring_param_mismatch
- Comment: `
        Initialize database connection.

        Args:
            database_url: Database URL (sqli`
- Code: `def __init__(self, database_url)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'database_url'}

**Line 87** (high): docstring_param_mismatch
- Comment: `
        Get a database connection.

        Returns:
            Database connection (sqlite3.Conne`
- Code: `def get_connection(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 125** (high): docstring_param_mismatch
- Comment: `
        Execute a query and return results.

        Args:
            query: SQL query
           `
- Code: `def execute(self, query, params)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

**Line 151** (high): docstring_param_mismatch
- Comment: `
        Execute a query multiple times with different parameters.

        Args:
            query:`
- Code: `def executemany(self, query, params_list)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

**Line 168** (high): docstring_param_mismatch
- Comment: `
        Get the parameter placeholder for this database type.

        SQLite uses ?, PostgreSQL us`
- Code: `def get_placeholder(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 184** (high): docstring_param_mismatch
- Comment: `
        Adapt a query for the current database type.

        Converts placeholders and database-sp`
- Code: `def adapt_query(self, query)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

**Line 210** (high): docstring_param_mismatch
- Comment: `
        Test the database connection.

        Returns:
            True if connection successful, `
- Code: `def test_connection(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 232** (high): docstring_param_mismatch
- Comment: `
    Get or create the global database connection.

    Args:
        database_url: Optional databas`
- Code: `def get_database_connection(database_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'database_url'}

### src\ai_training\dreamvault\runner.py

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Initialize batch runner.

        Args:
            config: Configuration object
        `
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 69** (high): docstring_param_mismatch
- Comment: `
        Add conversations to processing queue.

        Args:
            conversation_ids: List of`
- Code: `def add_conversations_to_queue(self, conversation_ids)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'conversation_ids', 'self'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Fetch conversation data (mock implementation).

        Args:
            conversation_id: `
- Code: `def _fetch_conversation(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Process a single conversation through the pipeline.

        Args:
            conversation`
- Code: `def _process_conversation(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 191** (high): docstring_param_mismatch
- Comment: `
        Run batch processing of conversations.

        Args:
            max_conversations: Maximu`
- Code: `def run_batch(self, max_conversations, batch_size)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'max_conversations', 'self'}

**Line 290** (high): docstring_param_mismatch
- Comment: `
        Clean up old data files.

        Args:
            days_old: Remove data older than this m`
- Code: `def cleanup_old_data(self, days_old)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'days_old'}

**Line 313** (high): docstring_param_mismatch
- Comment: `
        Rebuild all indexes from summary files.

        Returns:
            Dictionary with rebui`
- Code: `def rebuild_indexes(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\ai_training\dreamvault\scrapers\browser_manager.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
        Initialize the browser manager.

        Args:
            headless: Run browser in headles`
- Code: `def __init__(self, headless, use_undetected)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'headless'}

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Create and configure Chrome driver.

        Returns:
            Configured Chrome driver `
- Code: `def create_driver(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\ai_training\dreamvault\scrapers\login_handler.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
        Initialize the login handler.

        Args:
            username: ChatGPT username/email
 `
- Code: `def __init__(self, username, password, totp_secret)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'username'}

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Ensure user is logged into ChatGPT.

        Args:
            driver: Selenium webdriver i`
- Code: `def ensure_login(self, driver, allow_manual, manual_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

### src\application\use_cases\assign_task_uc.py

**Line 62** (high): docstring_param_mismatch
- Comment: `
        Execute the task assignment use case.

        Args:
            request: The assignment re`
- Code: `def execute(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\application\use_cases\complete_task_uc.py

**Line 59** (high): docstring_param_mismatch
- Comment: `
        Execute the task completion use case.

        Args:
            request: The completion re`
- Code: `def execute(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\architecture\system_integration.py

**Line 282** (high): docstring_param_mismatch
- Comment: `Integrate all registered systems (Phase 2: Auto-register existing systems).`
- Code: `def integrate_systems(self)`
- Issue: Docstring params don't match: missing={'2'}, extra={'self'}

### src\automation\ui_onboarding.py

**Line 45** (high): docstring_param_mismatch
- Comment: `Perform UI onboarding sequence for an agent.

        Args:
            agent_id: The agent identifi`
- Code: `def perform(self, agent_id, coords, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 104** (high): docstring_param_mismatch
- Comment: `Validate that coordinates are reasonable for screen interaction.

        Args:
            x: X coo`
- Code: `def _validate_coordinates(self, x, y)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'x', 'self'}

**Line 124** (high): docstring_param_mismatch
- Comment: `Validate that the message has the correct format.

        Args:
            agent_id: The agent ide`
- Code: `def _validate_message_format(self, agent_id, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\control_plane\adapters\base.py

**Line 24** (medium): docstring_return_mismatch
- Comment: `
        Execute an allowlisted operation.

        Args:
            op: Operation key (must be on `
- Code: `def run_allowed(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Execute an allowlisted operation.

        Args:
            op: Operation key (must be on `
- Code: `def run_allowed(self, op, payload)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'op', 'self'}

### src\control_plane\adapters\hostinger\freeride_adapter.py

**Line 95** (high): docstring_param_mismatch
- Comment: `
        Placeholder for cache flush via a secured endpoint or worker.
        Recommend: invoke a s`
- Code: `def _op_cache_flush(self, payload)`
- Issue: Docstring params don't match: missing={'Recommend'}, extra={'self', 'payload'}

**Line 109** (high): docstring_param_mismatch
- Comment: `
        Posts a daily plan via WP REST using application password auth.
        Requires: wp_user/w`
- Code: `def _op_post_daily_plan(self, payload)`
- Issue: Docstring params don't match: missing={'Requires'}, extra={'self', 'payload'}

### src\core\activity_emitter.py

**Line 127** (high): docstring_param_mismatch
- Comment: `
    Convenience wrapper so tools can emit without boilerplate.

    Args:
        event_type: Activ`
- Code: `def emit_activity_event(event_type, source, agent_id, summary, artifact, meta)`
- Issue: Docstring params don't match: missing={'force_discord', 'log_path', 'Args'}, extra={'event_type'}

### src\core\agent_activity_tracker.py

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Mark agent as actively working.
        
        Args:
            agent_id: Agent identifi`
- Code: `def mark_active(self, agent_id, operation)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 90** (high): docstring_param_mismatch
- Comment: `
        Mark agent as delivering a message.
        
        Args:
            agent_id: Agent iden`
- Code: `def mark_delivering(self, agent_id, queue_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 115** (high): docstring_param_mismatch
- Comment: `
        Mark agent as inactive (operation complete).
        
        Args:
            agent_id: A`
- Code: `def mark_inactive(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 135** (high): docstring_param_mismatch
- Comment: `
        Check if agent is currently active.
        
        Args:
            agent_id: Agent iden`
- Code: `def is_agent_active(self, agent_id, timeout_minutes)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 170** (high): docstring_param_mismatch
- Comment: `
        Get activity information for specific agent.
        
        Args:
            agent_id: A`
- Code: `def get_agent_activity(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 188** (high): docstring_param_mismatch
- Comment: `
        Get activity information for all agents.
        
        Returns:
            Dictionary m`
- Code: `def get_all_agent_activity(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 198** (high): docstring_param_mismatch
- Comment: `
        Get list of currently active agents.
        
        Args:
            timeout_minutes: Mi`
- Code: `def get_active_agents(self, timeout_minutes)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'timeout_minutes'}

### src\core\agent_context_manager.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Set context for an agent.

        Args:
            agent_id: The agent identifier
       `
- Code: `def set_agent_context(self, agent_id, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 60** (high): docstring_param_mismatch
- Comment: `
        Get context for an agent.

        Args:
            agent_id: The agent identifier

      `
- Code: `def get_agent_context(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Update context for an agent.

        Args:
            agent_id: The agent identifier
    `
- Code: `def update_agent_context(self, agent_id, updates)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 96** (high): docstring_param_mismatch
- Comment: `
        Remove context for an agent.

        Args:
            agent_id: The agent identifier

   `
- Code: `def remove_agent_context(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
        List all agents with contexts.

        Returns:
            list[str]: List of agent IDs
 `
- Code: `def list_agents(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 132** (high): docstring_param_mismatch
- Comment: `
        Get summary of all agent contexts.

        Returns:
            Dict[str, Any]: Context su`
- Code: `def get_context_summary(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\agent_documentation_service.py

**Line 24** (high): docstring_param_mismatch
- Comment: `Initialize documentation service.
        
        Args:
            agent_id: Optional agent ID for`
- Code: `def __init__(self, agent_id, vector_db, db_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 53** (high): docstring_param_mismatch
- Comment: `Search documentation using vector database service.
        
        Args:
            agent_id: Opt`
- Code: `def search_documentation(self, agent_id, query, n_results)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 148** (high): docstring_param_mismatch
- Comment: `Search documentation (alias for backward compatibility).
        
        Args:
            query: S`
- Code: `def search_docs(self, query, n_results)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

**Line 160** (high): docstring_param_mismatch
- Comment: `Get specific document by ID using vector database service.
        
        Args:
            doc_id`
- Code: `def get_doc(self, doc_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'doc_id'}

**Line 251** (high): docstring_param_mismatch
- Comment: `Get documentation summary.
        
        Args:
            agent_id: Optional agent ID (uses self`
- Code: `def get_documentation_summary(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 263** (high): docstring_param_mismatch
- Comment: `Get agent context.
        
        Returns:
            Agent context dictionary
        `
- Code: `def get_agent_context(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 275** (high): docstring_param_mismatch
- Comment: `Get service status.
        
        Returns:
            Service status dictionary
        `
- Code: `def get_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\agent_lifecycle.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
        Initialize AgentLifecycle for an agent.
        
        Args:
            agent_id: Agent `
- Code: `def __init__(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Commit status.json to git.
        
        Args:
            message: Optional custom comm`
- Code: `def _commit_to_git(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 120** (high): docstring_param_mismatch
- Comment: `
        AUTOMATIC status update on cycle start.
        
        Updates:
            - status: "AC`
- Code: `def start_cycle(self)`
- Issue: Docstring params don't match: missing={'last_cycle'}, extra={'self'}

**Line 141** (high): docstring_param_mismatch
- Comment: `
        AUTOMATIC status update when mission starts.
        
        Args:
            mission_nam`
- Code: `def start_mission(self, mission_name, priority)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'mission_name'}

**Line 162** (high): docstring_param_mismatch
- Comment: `
        AUTOMATIC status update for phase changes.
        
        Args:
            phase_descrip`
- Code: `def update_phase(self, phase_description)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'phase_description'}

**Line 174** (high): docstring_param_mismatch
- Comment: `
        Add task to current_tasks list.
        
        Args:
            task_name: Task descript`
- Code: `def add_task(self, task_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_name'}

**Line 189** (high): docstring_param_mismatch
- Comment: `
        AUTOMATIC status update when task completes.
        
        Args:
            task_name: `
- Code: `def complete_task(self, task_name, points)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_name'}

**Line 214** (high): docstring_param_mismatch
- Comment: `
        Add blocker and set status to BLOCKED.
        
        Args:
            blocker_descripti`
- Code: `def add_blocker(self, blocker_description)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'blocker_description'}

**Line 240** (high): docstring_param_mismatch
- Comment: `
        Add achievement to agent's record.
        
        Args:
            achievement: Achievem`
- Code: `def add_achievement(self, achievement)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'achievement'}

**Line 255** (high): docstring_param_mismatch
- Comment: `
        Set planned next actions.
        
        Args:
            actions: List of next action d`
- Code: `def set_next_actions(self, actions)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'actions'}

**Line 282** (high): docstring_param_mismatch
- Comment: `
        AUTOMATIC status update on cycle end.
        
        Args:
            commit: If True, a`
- Code: `def end_cycle(self, commit)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'commit'}

**Line 327** (high): docstring_param_mismatch
- Comment: `
    Quick helper to start a cycle.
    
    Args:
        agent_id: Agent identifier
        
    R`
- Code: `def quick_cycle_start(agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 342** (high): docstring_param_mismatch
- Comment: `
    Quick helper to mark task complete.
    
    Args:
        agent_id: Agent identifier
        t`
- Code: `def quick_task_complete(agent_id, task_name, points)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'agent_id'}

**Line 355** (high): docstring_param_mismatch
- Comment: `
    Quick helper to end cycle.
    
    Args:
        agent_id: Agent identifier
        commit: Wh`
- Code: `def quick_cycle_end(agent_id, commit)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'agent_id'}

### src\core\agent_self_healing_system.py

**Line 82** (high): docstring_param_mismatch
- Comment: `Initialize self-healing system.
        
        Args:
            config: Configuration (uses defau`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 171** (high): docstring_param_mismatch
- Comment: `Record terminal cancellation and return count for today.
        
        Args:
            agent_id`
- Code: `def _record_terminal_cancellation(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 189** (high): docstring_param_mismatch
- Comment: `Get terminal cancellation count for agent today.
        
        Args:
            agent_id: Agent `
- Code: `def get_cancellation_count_today(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 626** (high): docstring_param_mismatch
- Comment: `Record healing action in history.
        
        Args:
            agent_id: Agent identifier
    `
- Code: `def _record_healing(self, agent_id, action_type, reason, success, error)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 658** (high): docstring_param_mismatch
- Comment: `Get healing statistics.
        
        Returns:
            Dictionary with healing statistics
   `
- Code: `def get_healing_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 708** (high): docstring_param_mismatch
- Comment: `Get or create global self-healing system instance.
    
    Args:
        config: Configuration (onl`
- Code: `def get_self_healing_system(config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

### src\core\analytics\engines\caching_engine_fixed.py

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Initialize caching engine with memory limits.

        Args:
            config: Configurat`
- Code: `def __init__(self, config, max_size)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'config'}

**Line 44** (high): docstring_param_mismatch
- Comment: `Get value from cache (LRU: moves to end).`
- Code: `def get(self, key)`
- Issue: Docstring params don't match: missing={'LRU'}, extra={'self', 'key'}

### src\core\analytics\engines\metrics_engine.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
        Initialize metrics engine.
        
        Args:
            config: Optional configuratio`
- Code: `def __init__(self, config, metrics_repository)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 177** (high): docstring_param_mismatch
- Comment: `
        Save current metrics snapshot to repository.
        
        Args:
            source: Sou`
- Code: `def save_snapshot(self, source)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'source'}

**Line 201** (high): docstring_param_mismatch
- Comment: `
        Get metrics history from repository.
        
        Args:
            source: Optional so`
- Code: `def get_metrics_history(self, source, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'source'}

**Line 221** (high): docstring_param_mismatch
- Comment: `
        Get trend data for a specific metric over time.
        
        Args:
            metric_n`
- Code: `def get_metrics_trend(self, metric_name, source, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'metric_name'}

### src\core\auto_gas_pipeline_system.py

**Line 124** (high): docstring_param_mismatch
- Comment: `
        Calculate agent's progress percentage.
        
        Looks for:
        1. Completed rep`
- Code: `def _calculate_progress(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'for'}, extra={'self', 'agent_id'}

**Line 202** (high): docstring_param_mismatch
- Comment: `
        Determine if gas should be sent and to whom.
        
        Returns: List of reasons to s`
- Code: `def _should_send_gas(self, agent_id, progress)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'progress', 'agent_id'}

**Line 319** (high): docstring_param_mismatch
- Comment: `
        🔥 PERPETUAL MOTION ENGINE
        
        Monitors all agents every X seconds:
        1. `
- Code: `def monitor_pipeline(self, check_interval)`
- Issue: Docstring params don't match: missing={'seconds', 'Result'}, extra={'self', 'check_interval'}

**Line 439** (high): docstring_param_mismatch
- Comment: `
        Calculate agent's execution velocity (repos per cycle).
        
        Fast agents: Get g`
- Code: `def analyze_agent_velocity(self, agent_id)`
- Issue: Docstring params don't match: missing={'agents'}, extra={'self', 'agent_id'}

**Line 478** (high): docstring_param_mismatch
- Comment: `
        💎 JET FUEL vs Regular Gas
        
        Jet fuel includes:
        - Context from previo`
- Code: `def create_jet_fuel_message(self, agent_id, next_agent, progress)`
- Issue: Docstring params don't match: missing={'Result'}, extra={'self', 'progress', 'agent_id', 'next_agent'}

### src\core\base\availability_mixin.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
        Check if a service/module is available.
        
        Args:
            available: Wheth`
- Code: `def check_availability(self, available, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'available'}

### src\core\base\base_handler.py

**Line 47** (high): docstring_param_mismatch
- Comment: `
        Initialize base handler.
        
        Uses InitializationMixin for consolidated initial`
- Code: `def __init__(self, handler_name, config_section)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'handler_name'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Validate request (override for custom validation).
        
        Args:
            reque`
- Code: `def validate_request(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 87** (high): docstring_param_mismatch
- Comment: `
        Format handler response.
        
        Args:
            result: Result data
           `
- Code: `def format_response(self, result, success, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'result'}

**Line 111** (high): docstring_param_mismatch
- Comment: `
        Format error response as Flask tuple (response, status_code).
        
        Args:
      `
- Code: `def format_error(self, error_message, status_code)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'error_message'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Handle error and format error response.
        
        Uses ErrorHandlingMixin for consol`
- Code: `def handle_error(self, error, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 158** (high): docstring_param_mismatch
- Comment: `
        Log request (override for custom logging).
        
        Args:
            request: Requ`
- Code: `def log_request(self, request, level)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'request'}

### src\core\base\base_manager.py

**Line 43** (high): docstring_param_mismatch
- Comment: `
        Initialize base manager.
        
        Uses InitializationMixin for consolidated initial`
- Code: `def __init__(self, manager_name, config_section)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'manager_name'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Initialize manager (called after __init__ if needed).
        
        Returns:
           `
- Code: `def initialize(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Activate manager (start operations).
        
        Returns:
            True if activati`
- Code: `def activate(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 138** (high): docstring_param_mismatch
- Comment: `
        Deactivate manager (stop operations).
        
        Returns:
            True if deactiv`
- Code: `def deactivate(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 166** (high): docstring_param_mismatch
- Comment: `
        Get manager status.
        
        Returns:
            Dict with status information
    `
- Code: `def get_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\base\base_service.py

**Line 43** (high): docstring_param_mismatch
- Comment: `
        Initialize base service.
        
        Uses InitializationMixin for consolidated initial`
- Code: `def __init__(self, service_name, config_section)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'service_name', 'self'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Initialize service (called after __init__ if needed).
        
        Returns:
           `
- Code: `def initialize(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Start service (begin operations).
        
        Returns:
            True if start succe`
- Code: `def start(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 138** (high): docstring_param_mismatch
- Comment: `
        Stop service (end operations).
        
        Returns:
            True if stop successfu`
- Code: `def stop(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 166** (high): docstring_param_mismatch
- Comment: `
        Get service status.
        
        Returns:
            Dict with status information
    `
- Code: `def get_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\base\error_handling_mixin.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Handle error and format error response (consolidated pattern).
        
        This method`
- Code: `def handle_error(self, error, context, logger, component_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 93** (high): docstring_param_mismatch
- Comment: `
        Format standardized error response.
        
        Args:
            error_message: Error`
- Code: `def format_error_response(self, error_message, component_name, additional_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error_message'}

**Line 123** (high): docstring_param_mismatch
- Comment: `
        Format standardized success response.
        
        Args:
            data: Result data
`
- Code: `def format_success_response(self, data, component_name, additional_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 153** (high): docstring_param_mismatch
- Comment: `
        Safely execute an operation with error handling (consolidated pattern).
        
        Th`
- Code: `def safe_execute(self, operation, operation_name, default_return, logger, component_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'operation', 'self'}

### src\core\base\initialization_mixin.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Setup logging for class.
        
        Args:
            name: Logger name
            l`
- Code: `def setup_logging(self, name, level)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'name'}

**Line 56** (high): docstring_param_mismatch
- Comment: `
        Load configuration section.
        
        Args:
            section: Config section name`
- Code: `def load_config(self, section)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'section'}

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Get config value.
        
        Args:
            key: Config key
            default: D`
- Code: `def get_config_value(self, key, default, section)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'key'}

**Line 86** (high): docstring_param_mismatch
- Comment: `
        Ensure class is initialized (check for _initialized attribute).
        
        Args:
    `
- Code: `def ensure_initialized(self, attribute)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'attribute', 'self'}

**Line 100** (high): docstring_param_mismatch
- Comment: `
        Initialize logging and config together (convenience method).
        
        Args:
       `
- Code: `def initialize_with_config(self, name, section)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'name'}

### src\core\command_execution_wrapper.py

**Line 53** (high): docstring_param_mismatch
- Comment: `
    Execute command with automatic completion detection.
    
    Args:
        command: Command to`
- Code: `def execute_command_with_completion(command, shell, timeout, check_completion, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'command'}

**Line 192** (high): docstring_param_mismatch
- Comment: `
    Wait for task to complete.
    
    Args:
        task_id: Task identifier
        timeout: Max`
- Code: `def wait_for_completion(task_id, timeout, check_interval)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'task_id'}

### src\core\config\config_dataclasses.py

**Line 318** (high): docstring_param_mismatch
- Comment: `
        Calculate delay for given attempt with exponential backoff and jitter.
        
        Arg`
- Code: `def calculate_delay(self, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'attempt'}

**Line 351** (high): docstring_param_mismatch
- Comment: `
        Determine if operation should be retried.
        
        Args:
            error: Excepti`
- Code: `def should_retry(self, error, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

### src\core\consolidation\base.py

**Line 19** (high): docstring_param_mismatch
- Comment: `Consolidate Python files from ``directories`` into the target layout.

        Parameters
        --`
- Code: `def consolidate_directories(self, directories)`
- Issue: Docstring params don't match: missing=set(), extra={'self'}

### src\core\coordinate_loader.py

**Line 15** (high): docstring_param_mismatch
- Comment: `Load agent coordinates from the cursor_agent_coords.json SSOT.
    
    CRITICAL: chat_input_coordin`
- Code: `def _load_coordinates()`
- Issue: Docstring params don't match: missing={'CRITICAL'}, extra=set()

**Line 86** (high): docstring_param_mismatch
- Comment: `Get chat coordinates for agent.
        
        CRITICAL: Always returns chat_input_coordinates, NE`
- Code: `def get_chat_coordinates(self, agent_id)`
- Issue: Docstring params don't match: missing={'CRITICAL'}, extra={'self', 'agent_id'}

### src\core\coordination\agent_strategies.py

**Line 144** (high): docstring_param_mismatch
- Comment: `Create appropriate strategy for agent type.

        Args:
            agent_type: Type of agent to `
- Code: `def create_strategy(agent_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_type'}

**Line 167** (high): docstring_param_mismatch
- Comment: `Get all available strategies.

        Returns:
            Dictionary mapping agent types to their `
- Code: `def get_all_strategies()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### src\core\daily_cycle_tracker.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
        Initialize daily cycle tracker.
        
        Args:
            agent_id: Agent identifi`
- Code: `def __init__(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Start a new day cycle.
        
        Returns:
            Dictionary with day cycle info`
- Code: `def start_new_day(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 127** (high): docstring_param_mismatch
- Comment: `
        Record a completed task.
        
        Args:
            task_name: Name of completed ta`
- Code: `def record_task_completed(self, task_name, points)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_name'}

**Line 184** (high): docstring_param_mismatch
- Comment: `
        Add a blocker for the day.
        
        Args:
            blocker: Description of block`
- Code: `def add_blocker(self, blocker)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'blocker'}

**Line 201** (high): docstring_param_mismatch
- Comment: `
        Add an achievement for the day.
        
        Args:
            achievement: Description`
- Code: `def add_achievement(self, achievement)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'achievement'}

**Line 236** (high): docstring_param_mismatch
- Comment: `
        Get summary of today's cycle.
        
        Returns:
            Dictionary with today's`
- Code: `def get_today_summary(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 264** (high): docstring_param_mismatch
- Comment: `
        Get summary of all days.
        
        Returns:
            List of day summaries
      `
- Code: `def get_all_days_summary(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\debate_to_gas_integration.py

**Line 343** (high): docstring_param_mismatch
- Comment: `
        Process debate decision and activate agents

        Args:
            topic: Debate topic `
- Code: `def process_debate_decision(self, topic, decision, execution_plan, agent_assignments)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'topic', 'self'}

**Line 567** (high): docstring_param_mismatch
- Comment: `
    Quick function to activate a debate decision

    Example:
        activate_debate_decision(
  `
- Code: `def activate_debate_decision(topic, decision, execution_plan, agent_assignments)`
- Issue: Docstring params don't match: missing={'Example'}, extra={'topic', 'decision', 'execution_plan', 'agent_assignments'}

### src\core\deferred_push_queue.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Initialize deferred push queue.
        
        Args:
            queue_file: Path to queu`
- Code: `def __init__(self, queue_file)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'queue_file'}

**Line 95** (high): docstring_param_mismatch
- Comment: `
        Add push operation to deferred queue.
        
        Args:
            repo: Repository n`
- Code: `def enqueue_push(self, repo, branch, patch_file, reason, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo'}

### src\core\end_of_cycle_push.py

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Initialize end-of-cycle push handler.
        
        Args:
            agent_id: Agent id`
- Code: `def __init__(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Prepare for end-of-cycle push.
        
        Returns:
            Dictionary with push p`
- Code: `def prepare_for_push(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 68** (high): docstring_param_mismatch
- Comment: `
        Execute end-of-cycle push.
        
        Args:
            commit_message: Optional cust`
- Code: `def execute_push(self, commit_message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'commit_message'}

### src\core\engines\engine_base_helpers.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Standard initialization pattern - SSOT for all engines.
        
        Args:
            `
- Code: `def _standard_initialize(self, context, engine_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'context'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Standard cleanup pattern - SSOT for all engines.
        
        Args:
            context`
- Code: `def _standard_cleanup(self, context, engine_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'context'}

**Line 88** (high): docstring_param_mismatch
- Comment: `
        Standard error handling - SSOT for all engines.
        
        Args:
            error: E`
- Code: `def _handle_operation_error(self, error, operation)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Standard operation routing - SSOT for all engines.
        
        Args:
            conte`
- Code: `def _route_operation(self, context, payload, operation_map, default_error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'context'}

**Line 146** (high): docstring_param_mismatch
- Comment: `
    Create standard error result - SSOT utility function.
    
    Args:
        error: Error messa`
- Code: `def create_error_result(error, operation)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

### src\core\engines\registry.py

**Line 126** (high): docstring_param_mismatch
- Comment: `
        Find Engine implementation in module.
        
        For Protocol-based classes, we check`
- Code: `def _find_engine_class(self, module, protocol)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'module', 'self'}

### src\core\enhanced_activity_status_checker.py

**Line 33** (high): docstring_param_mismatch
- Comment: `Initialize enhanced status checker.
        
        Args:
            workspace_root: Root workspac`
- Code: `def __init__(self, workspace_root, use_activity_detection, stale_threshold_hours, activity_lookback_minutes)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'workspace_root'}

**Line 63** (high): docstring_param_mismatch
- Comment: `Check if agent is actually stalled (not just status.json stale).
        
        Args:
            `
- Code: `def is_agent_stalled(self, agent_id, status_timestamp)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 146** (high): docstring_param_mismatch
- Comment: `Get list of actually stalled agents.
        
        Args:
            agent_ids: List of agent IDs`
- Code: `def get_stalled_agents(self, agent_ids)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'agent_ids', 'self'}

**Line 203** (high): docstring_param_mismatch
- Comment: `Convenience function to check if agent is stalled.
    
    Args:
        agent_id: Agent identifier`
- Code: `def is_agent_stalled(agent_id, workspace_root, use_activity_detection)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### src\core\error_handling\circuit_breaker\protocol.py

**Line 33** (medium): docstring_return_mismatch
- Comment: `
        Execute function with circuit breaker protection.
        
        Args:
            func: `
- Code: `def call(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Execute function with circuit breaker protection.
        
        Args:
            func: `
- Code: `def call(self, func)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'args', 'Exception', 'Args', 'kwargs'}, extra={'self', 'func'}

**Line 51** (medium): docstring_return_mismatch
- Comment: `
        Get current circuit breaker state.
        
        Returns:
            State string: "clo`
- Code: `def get_state(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 51** (high): docstring_param_mismatch
- Comment: `
        Get current circuit breaker state.
        
        Returns:
            State string: "clo`
- Code: `def get_state(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 60** (medium): docstring_return_mismatch
- Comment: `
        Get current circuit breaker status.
        
        Returns:
            Dictionary with s`
- Code: `def get_status(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 60** (high): docstring_param_mismatch
- Comment: `
        Get current circuit breaker status.
        
        Returns:
            Dictionary with s`
- Code: `def get_status(self)`
- Issue: Docstring params don't match: missing={'failure_count', 'name', 'last_failure_time', 'timeout_seconds', 'next_attempt_time', 'failure_threshold', 'state', 'Returns'}, extra={'self'}

### src\core\error_handling\circuit_breaker\provider.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Create a Circuit Breaker instance.
        
        Args:
            config: Circuit Break`
- Code: `def create(config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

**Line 48** (high): docstring_param_mismatch
- Comment: `
        Get default Circuit Breaker instance.
        
        Returns:
            Default Circuit`
- Code: `def get_default()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Create Circuit Breaker with inline configuration.
        
        Args:
            name: `
- Code: `def create_with_config(name, failure_threshold, recovery_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'name'}

### src\core\error_handling\component_management.py

**Line 43** (high): docstring_param_mismatch
- Comment: `Register a circuit breaker for a component.

        Args:
            component: Component identifi`
- Code: `def register_circuit_breaker(self, component, failure_threshold, recovery_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 69** (high): docstring_param_mismatch
- Comment: `Register a retry mechanism for a component.

        Args:
            component: Component identifi`
- Code: `def register_retry_mechanism(self, component, max_attempts, base_delay, max_delay)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 97** (high): docstring_param_mismatch
- Comment: `Add a custom recovery strategy.

        Args:
            strategy: Recovery strategy to add
      `
- Code: `def add_recovery_strategy(self, strategy)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'strategy', 'self'}

**Line 106** (high): docstring_param_mismatch
- Comment: `Get detailed status for a specific component.

        Args:
            component: Component to ana`
- Code: `def get_component_status(self, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 132** (high): docstring_param_mismatch
- Comment: `Generate comprehensive error report with intelligence insights.

        Returns:
            Compre`
- Code: `def get_error_report(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 164** (high): docstring_param_mismatch
- Comment: `Reset error handling state for a specific component.

        Args:
            component: Component`
- Code: `def reset_component(self, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 181** (high): docstring_param_mismatch
- Comment: `Get list of all registered components.

        Returns:
            List of component identifiers
 `
- Code: `def get_all_components(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 192** (high): docstring_param_mismatch
- Comment: `Get metrics for a specific component.

        Args:
            component: Component to analyze

  `
- Code: `def get_component_metrics(self, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 298** (high): docstring_param_mismatch
- Comment: `Execute operation with comprehensive error handling.

        Args:
            operation: Operation`
- Code: `def execute_with_error_handling(self, operation, operation_name, component, use_retry, use_circuit_breaker, use_recovery, use_intelligence)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'operation', 'self'}

**Line 335** (high): docstring_param_mismatch
- Comment: `Register a circuit breaker for a component.

        Args:
            component: Component identifi`
- Code: `def register_circuit_breaker(self, component, failure_threshold, recovery_timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'component'}

**Line 349** (high): docstring_param_mismatch
- Comment: `Register a retry mechanism for a component.

        Args:
            component: Component identifi`
- Code: `def register_retry_mechanism(self, component, max_attempts, base_delay, max_delay)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'component'}

**Line 368** (high): docstring_param_mismatch
- Comment: `Add a custom recovery strategy.

        Args:
            strategy: Recovery strategy to add
      `
- Code: `def add_recovery_strategy(self, strategy)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'strategy', 'self'}

**Line 376** (high): docstring_param_mismatch
- Comment: `Generate comprehensive error report with intelligence insights.

        Returns:
            Compre`
- Code: `def get_error_report(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 384** (high): docstring_param_mismatch
- Comment: `Get detailed status for a specific component.

        Args:
            component: Component to ana`
- Code: `def get_component_status(self, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 395** (high): docstring_param_mismatch
- Comment: `Reset error handling state for a specific component.

        Args:
            component: Component`
- Code: `def reset_component(self, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 263** (high): comment_return_mismatch
- Comment: `Type variable for generic return types`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\core\error_handling\coordination_decorator.py

**Line 52** (high): docstring_param_mismatch
- Comment: `Decorator for coordination-specific error handling.

    Args:
        component: Component identifi`
- Code: `def handle_coordination_errors(component, use_retry, use_circuit_breaker, use_recovery, use_intelligence)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'component'}

### src\core\error_handling\coordination_strategies.py

**Line 24** (high): docstring_param_mismatch
- Comment: `Create a service restart recovery strategy for coordination systems.

    Returns:
        ServiceRe`
- Code: `def create_service_restart_strategy()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 31** (high): docstring_param_mismatch
- Comment: `Restart coordination service.

        Returns:
            True if restart successful
        `
- Code: `def restart_service()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 44** (high): docstring_param_mismatch
- Comment: `Create a configuration reset recovery strategy for coordination systems.

    Returns:
        Confi`
- Code: `def create_config_reset_strategy()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 51** (high): docstring_param_mismatch
- Comment: `Reset coordination configuration.

        Returns:
            True if reset successful
        `
- Code: `def reset_config()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 64** (high): docstring_param_mismatch
- Comment: `Register default coordination recovery strategies.

    Args:
        component_manager: Component m`
- Code: `def register_default_coordination_strategies(component_manager)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'component_manager'}

### src\core\error_handling\error_classification.py

**Line 63** (high): docstring_param_mismatch
- Comment: `Classify error by severity and category.

        Args:
            error: Exception to classify

  `
- Code: `def classify_error(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 87** (high): docstring_param_mismatch
- Comment: `Determine error severity based on error type.

        Args:
            error: Exception to analyze`
- Code: `def determine_severity(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 107** (high): docstring_param_mismatch
- Comment: `Determine error category for targeted handling.

        Args:
            error: Exception to analy`
- Code: `def determine_category(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 127** (high): docstring_param_mismatch
- Comment: `Determine if error is potentially recoverable.

        Args:
            error: Exception to analyz`
- Code: `def is_recoverable(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 153** (high): docstring_param_mismatch
- Comment: `Suggest recovery approach based on error classification.

        Args:
            error: Exception`
- Code: `def suggest_recovery_approach(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 175** (high): docstring_param_mismatch
- Comment: `Get classification statistics.

        Returns:
            Statistics about classified errors
    `
- Code: `def get_classification_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\error_handling\error_config.py

**Line 34** (high): docstring_param_mismatch
- Comment: `Backward compatibility: alias for recovery_timeout.`
- Code: `def timeout(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

### src\core\error_handling\error_decision_models.py

**Line 48** (high): docstring_param_mismatch
- Comment: `Classify error by severity, category, and recoverability.

        Args:
            error: Exceptio`
- Code: `def classify(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 122** (high): docstring_param_mismatch
- Comment: `Determine if operation should be retried.

        Args:
            error: Exception that occurred
`
- Code: `def should_retry(self, error, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

**Line 137** (high): docstring_param_mismatch
- Comment: `Calculate delay for given attempt.

        Args:
            attempt: Current attempt number

     `
- Code: `def get_delay(self, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'attempt'}

**Line 165** (high): docstring_param_mismatch
- Comment: `Decide action for error handling.

        Args:
            error: Exception that occurred
        `
- Code: `def decide_action(self, error, attempt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

### src\core\error_handling\error_execution.py

**Line 42** (high): docstring_param_mismatch
- Comment: `Initialize execution orchestrator.

        Args:
            circuit_breakers: Dict of circuit brea`
- Code: `def __init__(self, circuit_breakers, retry_mechanisms, recovery_strategies, classifier)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'circuit_breakers'}

**Line 85** (high): docstring_param_mismatch
- Comment: `Execute operation with comprehensive error handling.

        Args:
            operation: Operation`
- Code: `def execute_with_error_handling(self, operation, operation_name, component, use_retry, use_circuit_breaker, use_recovery, use_intelligence)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'operation', 'self'}

**Line 160** (high): docstring_param_mismatch
- Comment: `Execute operation with retry mechanism if available.

        Args:
            operation: Operation`
- Code: `def _execute_with_retry(self, operation, retry_mechanism, operation_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'operation', 'self'}

**Line 217** (high): docstring_param_mismatch
- Comment: `Attempt error recovery using registered strategies.

        Args:
            component: Component `
- Code: `def _attempt_recovery(self, component, error_type, use_intelligence)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 241** (high): docstring_param_mismatch
- Comment: `Execute a single recovery strategy.

        Args:
            strategy: Strategy to execute
       `
- Code: `def _execute_recovery_strategy(self, strategy, component, error_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'strategy', 'self'}

**Line 262** (high): docstring_param_mismatch
- Comment: `Check predictive failure risk for component.

        Args:
            component: Component to chec`
- Code: `def _check_failure_risk(self, component)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'component'}

**Line 277** (high): docstring_param_mismatch
- Comment: `Record error for intelligence analysis.

        Args:
            error: Exception that occurred
  `
- Code: `def _record_error_intelligence(self, error, component, operation_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'error'}

**Line 33** (high): comment_return_mismatch
- Comment: `Type variable for generic return types`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\core\error_handling\error_intelligence.py

**Line 65** (high): docstring_param_mismatch
- Comment: `Initialize error intelligence engine.

        Args:
            history_window: Number of error rec`
- Code: `def __init__(self, history_window, analysis_interval)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'history_window', 'self'}

**Line 90** (high): docstring_param_mismatch
- Comment: `Record an error occurrence for analysis.

        Args:
            error_type: Type of error
      `
- Code: `def record_error(self, error_type, component, severity, context)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'error_type'}

**Line 146** (high): docstring_param_mismatch
- Comment: `Record recovery attempt outcome for learning.

        Args:
            component: Component being `
- Code: `def record_recovery(self, component, success, recovery_time)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'component'}

**Line 176** (high): docstring_param_mismatch
- Comment: `Predict failure risk for a component.

        Args:
            component: Component to analyze

  `
- Code: `def predict_failure_risk(self, component)`
- Issue: Docstring params don't match: missing={'risk_score', 'Returns', 'Args'}, extra={'self', 'component'}

**Line 229** (high): docstring_param_mismatch
- Comment: `Suggest optimal recovery strategy based on historical success.

        Args:
            error_type`
- Code: `def suggest_recovery_strategy(self, error_type, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error_type'}

**Line 249** (high): docstring_param_mismatch
- Comment: `Get comprehensive health report for a component.

        Args:
            component: Component to `
- Code: `def get_component_health(self, component)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'component'}

**Line 274** (high): docstring_param_mismatch
- Comment: `Generate comprehensive intelligence report for entire system.

        Returns:
            System-w`
- Code: `def get_system_intelligence_report(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\error_handling\error_utilities_core.py

**Line 40** (high): docstring_param_mismatch
- Comment: `Map ErrorSeverity to LogLevel for coordinated error/logging.

    DUP-006/007 Coordination: Integrat`
- Code: `def get_log_level_for_severity(severity)`
- Issue: Docstring params don't match: missing={'Coordination', 'Returns', 'Args'}, extra={'severity'}

**Line 72** (high): docstring_param_mismatch
- Comment: `Log exception with appropriate severity level.

    DUP-006/007 Coordination: Unified exception logg`
- Code: `def log_exception_with_severity(logger, severity, exception, context)`
- Issue: Docstring params don't match: missing={'Coordination', 'Args'}, extra={'logger'}

### src\core\error_handling\retry_safety_engine.py

**Line 37** (high): docstring_param_mismatch
- Comment: `Retry operation with exponential backoff.

        Args:
            operation_func: Function to ret`
- Code: `def retry_operation(self, operation_func, config, logger)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'operation_func'}

**Line 111** (high): docstring_param_mismatch
- Comment: `Safely execute operation with fallback return value.

        Args:
            operation_func: Func`
- Code: `def safe_execute(self, operation_func, default_return, logger, operation_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'operation_func'}

**Line 137** (high): docstring_param_mismatch
- Comment: `Validate input and execute operation.

        Args:
            operation_func: Function to execute`
- Code: `def validate_and_execute(self, operation_func, validation_func, error_message, logger)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'operation_func'}

**Line 176** (high): docstring_param_mismatch
- Comment: `Execute operation with timeout.

        Args:
            operation_func: Function to execute
     `
- Code: `def execute_with_timeout(self, operation_func, timeout, default_return, logger)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'operation_func'}

**Line 244** (high): docstring_param_mismatch
- Comment: `Execute operation with circuit breaker pattern.

        Args:
            operation_func: Function `
- Code: `def circuit_breaker_execute(self, operation_func, failure_threshold, recovery_timeout, logger)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'operation_func'}

### src\core\gamification\achievements.py

**Line 68** (high): docstring_param_mismatch
- Comment: `
        Calculate bonus for proactive initiatives.

        Proactive work (self-directed without o`
- Code: `def calculate_proactive_bonus(base_points)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'base_points'}

**Line 83** (high): docstring_param_mismatch
- Comment: `
        Calculate quality multiplier based on metrics.

        Args:
            quality_metrics: `
- Code: `def calculate_quality_multiplier(quality_metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'quality_metrics'}

### src\core\gamification\competition_storage.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
    Load scores from storage.

    Args:
        storage_path: Path to storage directory

    Retur`
- Code: `def load_scores(storage_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'storage_path'}

**Line 48** (high): docstring_param_mismatch
- Comment: `
    Save scores to storage.

    Args:
        storage_path: Path to storage directory
        scor`
- Code: `def save_scores(storage_path, scores, mode_value)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'storage_path'}

**Line 81** (high): docstring_param_mismatch
- Comment: `
    Update agent ranks based on total points (in-place).

    Args:
        scores: Dictionary of a`
- Code: `def update_ranks(scores)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'scores'}

### src\core\gamification\leaderboard.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
        Get leaderboard rankings.

        Args:
            scores: Dictionary of agent scores
   `
- Code: `def get_leaderboard(scores, top_n)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'scores'}

**Line 44** (high): docstring_param_mismatch
- Comment: `
        Generate leaderboard message for broadcast.

        Args:
            scores: Dictionary o`
- Code: `def generate_leaderboard_message(scores, show_top)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'scores'}

### src\core\gamification\system_core.py

**Line 58** (high): docstring_param_mismatch
- Comment: `
        Award achievement to agent.

        Args:
            agent_id: Agent identifier
         `
- Code: `def award_achievement(self, agent_id, agent_name, achievement_type, title, description, points, mission_ref, evidence, is_proactive, quality_metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\core\gasline_integrations.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        When debate concludes → Store in brain → Activate agents
        
        Flow:
        Deb`
- Code: `def hook_debate_decision(self, topic, decision, agent_assignments)`
- Issue: Docstring params don't match: missing={'Flow'}, extra={'topic', 'self', 'decision', 'agent_assignments'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        When violations found → Create tasks → Activate agents
        
        Flow:
        Scann`
- Code: `def hook_violations_found(self, violations, auto_assign)`
- Issue: Docstring params don't match: missing={'Flow'}, extra={'auto_assign', 'self', 'violations'}

**Line 218** (high): docstring_param_mismatch
- Comment: `
        When agent needs knowledge → Brain searches → Gas delivers results
        
        Flow:
 `
- Code: `def hook_knowledge_request(self, agent_id, query)`
- Issue: Docstring params don't match: missing={'Flow'}, extra={'query', 'self', 'agent_id'}

**Line 295** (high): docstring_param_mismatch
- Comment: `
        When documentation needs migration → Assign → Activate
        
        Flow:
        Docs `
- Code: `def hook_documentation_migration(self, completed_items, remaining_items)`
- Issue: Docstring params don't match: missing={'Flow'}, extra={'remaining_items', 'self', 'completed_items'}

### src\core\hardened_activity_detector.py

**Line 116** (high): docstring_param_mismatch
- Comment: `
        Assess agent activity with multi-source validation.
        
        Args:
            agen`
- Code: `def assess_agent_activity(self, agent_id, lookback_minutes)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 404** (high): docstring_param_mismatch
- Comment: `
        Parse git log output with --name-only format.
        
        Format:
        commit_hash|`
- Code: `def _parse_git_log_with_files(self, output)`
- Issue: Docstring params don't match: missing={'Format'}, extra={'self', 'output'}

**Line 816** (high): docstring_param_mismatch
- Comment: `
        Cross-validate signals for consistency.
        
        Returns:
            True if signa`
- Code: `def _validate_signals(self, signals, lookback_time)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'signals', 'lookback_time'}

### src\core\in_memory_message_queue.py

**Line 83** (high): docstring_param_mismatch
- Comment: `Initialize in-memory queue.
        
        Args:
            max_size: Maximum queue size (default`
- Code: `def __init__(self, max_size)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'max_size', 'self'}

**Line 99** (high): docstring_param_mismatch
- Comment: `Enqueue message to in-memory queue.
        
        Args:
            message: Message dictionary
 `
- Code: `def enqueue(self, message, priority, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 142** (high): docstring_param_mismatch
- Comment: `Dequeue messages from in-memory queue.
        
        Args:
            batch_size: Number of mess`
- Code: `def dequeue(self, batch_size)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'batch_size'}

**Line 166** (high): docstring_param_mismatch
- Comment: `Mark message as delivered.
        
        Args:
            queue_id: Queue entry ID
            
`
- Code: `def mark_delivered(self, queue_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'queue_id'}

**Line 184** (high): docstring_param_mismatch
- Comment: `Mark message as failed.
        
        Args:
            queue_id: Queue entry ID
            reas`
- Code: `def mark_failed(self, queue_id, error)`
- Issue: Docstring params don't match: missing={'Returns', 'reason', 'Args'}, extra={'self', 'error', 'queue_id'}

**Line 205** (high): docstring_param_mismatch
- Comment: `Get queue statistics.
        
        Returns:
            Dictionary with queue statistics
       `
- Code: `def get_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 213** (high): docstring_param_mismatch
- Comment: `Get queue statistics (interface method).
        
        Returns:
            Dictionary with queue`
- Code: `def get_statistics(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 237** (high): docstring_param_mismatch
- Comment: `Remove expired entries (interface method).
        
        In-memory queue doesn't expire entries, `
- Code: `def cleanup_expired(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 262** (high): docstring_param_mismatch
- Comment: `Remove expired entries (interface method).
        
        In-memory queue doesn't expire entries, `
- Code: `def cleanup_expired(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\keyboard_control_lock.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
    Context manager for exclusive keyboard control.
    
    Ensures only ONE source can control ke`
- Code: `def keyboard_control(source)`
- Issue: Docstring params don't match: missing={'Example', 'Args'}, extra={'source'}

**Line 87** (high): docstring_param_mismatch
- Comment: `
    Manually acquire keyboard lock (alternative to context manager).
    
    Returns:
        True`
- Code: `def acquire_lock(source, timeout)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'timeout', 'source'}

**Line 119** (high): docstring_param_mismatch
- Comment: `
    Force release keyboard lock (emergency recovery).
    
    WARNING: Only use when lock is stuck`
- Code: `def force_release_lock()`
- Issue: Docstring params don't match: missing={'WARNING'}, extra=set()

**Line 149** (high): docstring_param_mismatch
- Comment: `
    Get detailed lock status for debugging.
    
    Returns:
        Dictionary with lock status i`
- Code: `def get_lock_status()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 139** (high): comment_raise_mismatch
- Comment: `Force release - may raise RuntimeError if lock not held by this thread`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### src\core\local_repo_layer.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Initialize local repo manager with self-healing capabilities.
        
        Args:
      `
- Code: `def __init__(self, base_path)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'base_path'}

**Line 173** (high): docstring_param_mismatch
- Comment: `
        Clone repository from GitHub to local storage.
        
        Args:
            repo_name`
- Code: `def clone_from_github(self, repo_name, github_url, github_user, branch)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 238** (high): docstring_param_mismatch
- Comment: `
        Clone from another local repository.
        
        Args:
            repo_name: Name for`
- Code: `def clone_locally(self, repo_name, source_path, branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 334** (high): docstring_param_mismatch
- Comment: `
        Merge branches locally.
        
        Args:
            repo_name: Name of repository
  `
- Code: `def merge_branch(self, repo_name, source_branch, target_branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 390** (high): docstring_param_mismatch
- Comment: `
        Generate patch file for branch.
        
        Args:
            repo_name: Name of repos`
- Code: `def generate_patch(self, repo_name, branch, output_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

### src\core\managers\domains\resource_domain_manager.py

**Line 94** (high): docstring_param_mismatch
- Comment: `
        Execute resource operation by routing to appropriate module.

        Supports operations a`
- Code: `def execute(self, context, operation, payload)`
- Issue: Docstring params don't match: missing={'operations'}, extra={'operation', 'self', 'context', 'payload'}

### src\core\managers\manager_metrics.py

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Get manager metrics.

        Returns:
            Dict containing performance metrics
    `
- Code: `def get_metrics(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Reset manager metrics.

        Returns:
            bool: True if reset successful
       `
- Code: `def reset(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\managers\manager_operations.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Execute operation with validation and error handling.

        Args:
            context: M`
- Code: `def execute_with_validation(self, context, operation, payload, execute_callback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'context'}

### src\core\merge_conflict_resolver.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Detect merge conflicts before attempting merge.
        
        Args:
            repo_pat`
- Code: `def detect_conflicts(self, repo_path, source_branch, target_branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_path'}

**Line 93** (high): docstring_param_mismatch
- Comment: `
        Automatically resolve conflicts using strategy.
        
        Args:
            repo_pat`
- Code: `def resolve_conflicts_auto(self, repo_path, conflict_files, strategy)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_path'}

**Line 171** (high): docstring_param_mismatch
- Comment: `
        Generate detailed conflict report.
        
        Args:
            repo_path: Path to re`
- Code: `def generate_conflict_report(self, repo_path, conflict_files)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_path'}

**Line 212** (high): docstring_param_mismatch
- Comment: `
        Perform merge with automatic conflict resolution.
        
        Args:
            repo_p`
- Code: `def merge_with_conflict_resolution(self, repo_path, source_branch, target_branch, resolution_strategy)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_path'}

### src\core\message_formatters.py

**Line 22** (high): docstring_param_mismatch
- Comment: `Format message with full details (Captain communications, onboarding).

    Includes:
    - Full hea`
- Code: `def format_message_full(message)`
- Issue: Docstring params don't match: missing={'15', 'Returns', 'Args'}, extra={'message'}

**Line 160** (high): docstring_param_mismatch
- Comment: `Format message with compact details (standard agent-to-agent).

    Includes:
    - Simple header wi`
- Code: `def format_message_compact(message)`
- Issue: Docstring params don't match: missing={'15', 'Returns', 'Args'}, extra={'message'}

**Line 241** (high): docstring_param_mismatch
- Comment: `Format message with minimal details (quick updates, passdown).

    Includes:
    - Bare minimum: fr`
- Code: `def format_message_minimal(message)`
- Issue: Docstring params don't match: missing={'minimum', 'Example', 'To', 'Args', 'Returns'}, extra={'message'}

**Line 276** (high): docstring_param_mismatch
- Comment: `Format message using specified template type.

    Routes to appropriate formatter based on template`
- Code: `def format_message(message, template)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message'}

### src\core\message_queue.py

**Line 129** (high): docstring_param_mismatch
- Comment: `Add message to queue with priority-based ordering.

        Args:
            message: Message to qu`
- Code: `def enqueue(self, message, delivery_callback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 160** (high): docstring_param_mismatch
- Comment: `Create new queue entry.
        
        FIXED: Normalize message format to dict to ensure consisten`
- Code: `def _create_queue_entry(self, queue_id, message, priority_score, delivery_callback)`
- Issue: Docstring params don't match: missing={'FIXED'}, extra={'priority_score', 'message', 'delivery_callback', 'self', 'queue_id'}

**Line 226** (high): docstring_param_mismatch
- Comment: `Calculate priority score for message.
        
        FIXED: Handles both UnifiedMessage objects an`
- Code: `def _calculate_priority_score(self, message, now)`
- Issue: Docstring params don't match: missing={'FIXED'}, extra={'message', 'self', 'now'}

**Line 255** (high): docstring_param_mismatch
- Comment: `Get next messages for processing based on priority.

        Args:
            batch_size: Number of`
- Code: `def dequeue(self, batch_size)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'batch_size'}

### src\core\message_queue_helpers.py

**Line 25** (high): docstring_param_mismatch
- Comment: `Log queued message to repository (SSOT enforcement).
    
    Args:
        message_repository: Mess`
- Code: `def log_message_to_repository(message_repository, message, queue_id, now, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message_repository'}

**Line 65** (high): docstring_param_mismatch
- Comment: `Track queue metrics via metrics engine.
    
    Args:
        metrics_engine: MetricsEngine instanc`
- Code: `def track_queue_metrics(metrics_engine, message, queue_size, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'metrics_engine'}

**Line 96** (high): docstring_param_mismatch
- Comment: `Track agent activity when message queued.
    
    Args:
        message: Message data
        logge`
- Code: `def track_agent_activity(message, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message'}

**Line 118** (high): docstring_param_mismatch
- Comment: `Wait for message delivery to complete (DELIVERED or FAILED).
    
    CRITICAL: Blocks until message`
- Code: `def wait_for_queue_delivery(queue, queue_id, timeout, poll_interval, logger)`
- Issue: Docstring params don't match: missing={'default', 'CRITICAL', 'Returns', 'Args'}, extra={'queue'}

### src\core\message_queue_persistence.py

**Line 93** (high): docstring_param_mismatch
- Comment: `Attempt to recover from corrupted JSON.
        
        Strategies:
        1. Try to find valid JS`
- Code: `def _recover_corrupted_json(self, raw_content, json_error)`
- Issue: Docstring params don't match: missing={'Strategies'}, extra={'raw_content', 'self', 'json_error'}

**Line 197** (high): docstring_param_mismatch
- Comment: `Save queue entries to JSON file with atomic write and retry logic.
        
        Args:
          `
- Code: `def save_entries(self, entries, max_retries, base_delay)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'entries'}

### src\core\message_queue_processor.py

**Line 47** (high): docstring_param_mismatch
- Comment: `Initialize message queue processor.

        Args:
            queue: MessageQueue instance (creates`
- Code: `def __init__(self, queue, message_repository, config, messaging_core)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'queue'}

**Line 69** (high): docstring_param_mismatch
- Comment: `
        Process queued messages in controlled batches.

        Args:
            max_messages: Max`
- Code: `def process_queue(self, max_messages, batch_size, interval)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'max_messages'}

**Line 127** (high): docstring_param_mismatch
- Comment: `Safely dequeue messages with error isolation.

        Args:
            batch_size: Number of messa`
- Code: `def _safe_dequeue(self, batch_size)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'batch_size'}

**Line 142** (high): docstring_param_mismatch
- Comment: `
        Deliver queue entry → log → mark state.

        Error isolation: Each step wrapped in try/`
- Code: `def _deliver_entry(self, entry)`
- Issue: Docstring params don't match: missing={'isolation', 'Returns', 'Args'}, extra={'self', 'entry'}

**Line 272** (high): docstring_param_mismatch
- Comment: `
        Route message delivery with fallback logic.

        Primary: PyAutoGUI delivery via messag`
- Code: `def _route_delivery(self, recipient, content, metadata, message_type_str, sender, priority_str, tags_list)`
- Issue: Docstring params don't match: missing={'Backup', 'Primary', 'Returns', 'Args'}, extra={'sender', 'self', 'recipient', 'priority_str', 'tags_list', 'message_type_str'}

**Line 347** (high): docstring_param_mismatch
- Comment: `
        Primary path: Unified messaging core (PyAutoGUI delivery or injected mock).

        Uses i`
- Code: `def _deliver_via_core(self, recipient, content, metadata, message_type_str, sender, priority_str, tags_list)`
- Issue: Docstring params don't match: missing={'path', 'control', 'Args', 'Imports', 'Returns'}, extra={'sender', 'self', 'recipient', 'priority_str', 'tags_list', 'message_type_str'}

**Line 504** (high): docstring_param_mismatch
- Comment: `
        Backup path: Inbox file-based delivery.

        Used when PyAutoGUI delivery fails (e.g., `
- Code: `def _deliver_fallback_inbox(self, recipient, content, metadata, sender, priority_str)`
- Issue: Docstring params don't match: missing={'Returns', 'Args', 'path'}, extra={'self', 'recipient'}

### src\core\messaging_core.py

**Line 114** (high): docstring_param_mismatch
- Comment: `
        Send a message using the unified messaging system.
        
        VALIDATION: Checks if r`
- Code: `def send_message(self, content, sender, recipient, message_type, priority, tags, metadata)`
- Issue: Docstring params don't match: missing={'VALIDATION'}, extra={'message_type', 'sender', 'priority', 'self', 'recipient', 'content', 'metadata', 'tags'}

**Line 353** (high): docstring_param_mismatch
- Comment: `Broadcast message to all agents.
        
        CRITICAL FIX: Expands "ALL_AGENTS" into individual`
- Code: `def broadcast_message(self, content, sender, priority)`
- Issue: Docstring params don't match: missing={'FIX'}, extra={'self', 'sender', 'content', 'priority'}

**Line 526** (high): comment_raise_mismatch
- Comment: `Don't raise exception during import - allow system to continue`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### src\core\messaging_process_lock.py

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Initialize cross-process lock.

        Args:
            lock_dir: Directory for lock file`
- Code: `def __init__(self, lock_dir, timeout)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'lock_dir'}

**Line 77** (high): docstring_param_mismatch
- Comment: `
        Acquire cross-process lock with exponential backoff retry logic.

        Args:
           `
- Code: `def acquire(self, retry_delay, use_exponential_backoff)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'retry_delay'}

### src\core\messaging_protocol_models.py

**Line 34** (medium): docstring_return_mismatch
- Comment: `
        Send a message using the delivery mechanism.

        Args:
            message: UnifiedMes`
- Code: `def send_message(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 34** (high): docstring_param_mismatch
- Comment: `
        Send a message using the delivery mechanism.

        Args:
            message: UnifiedMes`
- Code: `def send_message(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 55** (medium): docstring_return_mismatch
- Comment: `
        Generate onboarding message for an agent.

        Args:
            agent_id: Target agent`
- Code: `def generate_onboarding_message(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Generate onboarding message for an agent.

        Args:
            agent_id: Target agent`
- Code: `def generate_onboarding_message(self, agent_id, style)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 77** (medium): docstring_return_mismatch
- Comment: `
        Format a message using the specified template.

        Args:
            message: UnifiedM`
- Code: `def format_message(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 77** (high): docstring_param_mismatch
- Comment: `
        Format a message using the specified template.

        Args:
            message: UnifiedM`
- Code: `def format_message(self, message, template)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 99** (medium): docstring_return_mismatch
- Comment: `
        Check if inbox rotation is needed and perform it.

        Args:
            filepath: Path`
- Code: `def check_and_rotate(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Check if inbox rotation is needed and perform it.

        Args:
            filepath: Path`
- Code: `def check_and_rotate(self, filepath)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'filepath', 'self'}

### src\core\messaging_pyautogui.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
    Determine correct message tag based on sender and recipient.
    
    Args:
        sender: Mes`
- Code: `def get_message_tag(sender, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'sender'}

**Line 86** (high): docstring_param_mismatch
- Comment: `
    Format message with correct tag based on sender (UPDATED - Agent-1 2025-10-15).

    Per STANDA`
- Code: `def format_c2a_message(recipient, content, priority, sender)`
- Issue: Docstring params don't match: missing={'md', 'Returns', 'Args'}, extra={'recipient'}

**Line 126** (high): docstring_param_mismatch
- Comment: `
        Validate coordinates before sending with comprehensive checks.

        Args:
            a`
- Code: `def validate_coordinates(self, agent_id, coords)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 187** (high): docstring_param_mismatch
- Comment: `
        Send message to agent chat input coordinates.
        
        RACE CONDITION FIXES:
      `
- Code: `def send_message(self, message)`
- Issue: Docstring params don't match: missing={'FIX'}, extra={'message', 'self'}

### src\core\messaging_templates.py

**Line 85** (high): docstring_param_mismatch
- Comment: `Public S2A formatter: always injects operating cycle.`
- Code: `def format_s2a_message(template_key)`
- Issue: Docstring params don't match: missing={'formatter'}, extra={'template_key'}

### src\core\mock_unified_messaging_core.py

**Line 62** (high): docstring_param_mismatch
- Comment: `Initialize mock messaging core.
        
        Args:
            config: Mock delivery configurati`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Simulate sending a message.
        
        Args:
            content: Message content
   `
- Code: `def send_message(self, content, sender, recipient, message_type, priority, tags, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

**Line 167** (high): docstring_param_mismatch
- Comment: `Send a UnifiedMessage object (compatibility method).
        
        Args:
            message: Uni`
- Code: `def send_message_object(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 191** (high): docstring_param_mismatch
- Comment: `Record delivery statistics.
        
        Args:
            success: Whether delivery was success`
- Code: `def _record_delivery(self, success, latency_ms, error, chaos_event)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'success'}

**Line 222** (high): docstring_param_mismatch
- Comment: `Get delivery statistics.
        
        Returns:
            Dictionary with delivery statistics
 `
- Code: `def get_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 262** (high): docstring_param_mismatch
- Comment: `Update configuration.
        
        Args:
            min_latency_ms: Minimum latency in millisec`
- Code: `def configure(self, min_latency_ms, max_latency_ms, success_rate, chaos_mode, chaos_crash_rate, chaos_latency_spike_rate)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'min_latency_ms'}

**Line 299** (high): docstring_param_mismatch
- Comment: `Get or create global mock messaging core instance.
    
    Args:
        config: Configuration (onl`
- Code: `def get_mock_messaging_core(config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

### src\core\multi_agent_request_validator.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Check if agent has pending multi-agent request.
        
        Args:
            agent_id`
- Code: `def check_pending_request(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Validate agent can send message (no pending multi-agent requests).
        
        Args:
 `
- Code: `def validate_agent_can_send_message(self, agent_id, target_recipient, message_content)`
- Issue: Docstring params don't match: missing={'pending_info', 'can_send', 'error_message', 'Args', 'Returns'}, extra={'self', 'agent_id'}

**Line 153** (high): docstring_param_mismatch
- Comment: `
        Get the pending request message for an agent.
        
        Useful for showing in type h`
- Code: `def get_pending_request_message(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\core\multi_agent_responder.py

**Line 160** (high): docstring_param_mismatch
- Comment: `
        Create multi-agent request and return collector ID.
        
        Args:
            requ`
- Code: `def create_request(self, request_id, sender, recipients, content, timeout_seconds, wait_for_all)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'request_id', 'self'}

**Line 205** (high): docstring_param_mismatch
- Comment: `
        Submit agent's response to collector.
        
        Args:
            collector_id: Coll`
- Code: `def submit_response(self, collector_id, agent_id, response)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'collector_id', 'self'}

### src\core\onboarding_service.py

**Line 49** (high): docstring_param_mismatch
- Comment: `
        Generate onboarding message for an agent.

        Args:
            agent_id: Target agent`
- Code: `def generate_onboarding_message(self, agent_id, style)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\core\optimized_stall_resume_prompt.py

**Line 109** (high): docstring_param_mismatch
- Comment: `Initialize prompt generator.

        Args:
            workspace_root: Root directory for agent wor`
- Code: `def __init__(self, workspace_root, scheduler, auto_claim_tasks)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'workspace_root'}

**Line 131** (high): docstring_param_mismatch
- Comment: `
        Generate optimized resume prompt based on FSM state and Cycle Planner.

        Args:
     `
- Code: `def generate_resume_prompt(self, agent_id, fsm_state, last_mission, stall_duration_minutes, validate_activity)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 490** (high): docstring_param_mismatch
- Comment: `
    Convenience function to generate optimized resume prompt.

    Args:
        agent_id: Agent id`
- Code: `def generate_optimized_resume_prompt(agent_id, fsm_state, last_mission, stall_duration_minutes, scheduler)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### src\core\orchestration\base_orchestrator.py

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Initialize base orchestrator.

        Args:
            name: Orchestrator identifier name`
- Code: `def __init__(self, name, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'name'}

**Line 81** (high): docstring_param_mismatch
- Comment: `
        Register components with orchestrator.

        Subclasses must implement this method to:
 `
- Code: `def _register_components(self)`
- Issue: Docstring params don't match: missing={'to', 'Example'}, extra={'self'}

**Line 100** (medium): docstring_return_mismatch
- Comment: `
        Load default configuration for orchestrator.

        Returns:
            Dictionary of de`
- Code: `def _load_default_config(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 100** (high): docstring_param_mismatch
- Comment: `
        Load default configuration for orchestrator.

        Returns:
            Dictionary of de`
- Code: `def _load_default_config(self)`
- Issue: Docstring params don't match: missing={'Example', 'Returns'}, extra={'self'}

**Line 117** (high): docstring_param_mismatch
- Comment: `
        Initialize orchestrator and all components.

        Returns:
            True if initializ`
- Code: `def initialize(self)`
- Issue: Docstring params don't match: missing={'Note', 'Returns'}, extra={'self'}

**Line 151** (high): docstring_param_mismatch
- Comment: `
        Cleanup orchestrator and all components.

        Performs cleanup in reverse order of init`
- Code: `def cleanup(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 194** (high): docstring_param_mismatch
- Comment: `
        Get orchestrator status and health information.

        Returns:
            Dictionary co`
- Code: `def get_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 219** (high): docstring_param_mismatch
- Comment: `
        Get health check information.

        Returns:
            Dictionary with health status a`
- Code: `def get_health(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\repository_merge_improvements.py

**Line 145** (high): docstring_param_mismatch
- Comment: `
        Classify error as permanent, transient, or unknown.
        
        Permanent errors: Don'`
- Code: `def classify_error(self, error_message)`
- Issue: Docstring params don't match: missing={'errors'}, extra={'self', 'error_message'}

### src\core\resume_cycle_planner_integration.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Get and automatically claim next available task from cycle planner.
        
        This m`
- Code: `def get_and_claim_next_task(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'method', 'Args'}, extra={'self', 'agent_id'}

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Preview next available task without claiming it.
        
        Useful for displaying in `
- Code: `def get_next_task_preview(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\core\session\base_session_manager.py

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Initialize base session manager.

        Args:
            config: Configuration dictionar`
- Code: `def __init__(self, config, logger_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 78** (medium): docstring_return_mismatch
- Comment: `
        Create a new session.

        Args:
            service_name: Name of service session is f`
- Code: `def create_session(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 78** (high): docstring_param_mismatch
- Comment: `
        Create a new session.

        Args:
            service_name: Name of service session is f`
- Code: `def create_session(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'kwargs', 'Args'}, extra={'service_name', 'self'}

**Line 92** (medium): docstring_return_mismatch
- Comment: `
        Validate that a session is still active and valid.

        Args:
            session_id: S`
- Code: `def validate_session(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 92** (high): docstring_param_mismatch
- Comment: `
        Validate that a session is still active and valid.

        Args:
            session_id: S`
- Code: `def validate_session(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 104** (high): docstring_param_mismatch
- Comment: `
        Get information about a session.

        Args:
            session_id: Session ID to retri`
- Code: `def get_session_info(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Check if a session exists.

        Args:
            session_id: Session ID to check

    `
- Code: `def session_exists(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 142** (high): docstring_param_mismatch
- Comment: `
        Update last activity timestamp for a session.

        Args:
            session_id: Sessio`
- Code: `def update_session_activity(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 160** (high): docstring_param_mismatch
- Comment: `
        Close a session and clean up resources.

        Args:
            session_id: Session ID t`
- Code: `def close_session(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 178** (high): docstring_param_mismatch
- Comment: `
        Clean up expired sessions based on timeout.

        Returns:
            Number of session`
- Code: `def cleanup_expired_sessions(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 204** (high): docstring_param_mismatch
- Comment: `
        Get information about all sessions.

        Returns:
            Dictionary mapping sessio`
- Code: `def get_all_sessions(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 215** (high): docstring_param_mismatch
- Comment: `
        Get count of active sessions.

        Returns:
            Number of active sessions
     `
- Code: `def get_active_session_count(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 224** (high): docstring_param_mismatch
- Comment: `
        Get statistics about session manager.

        Returns:
            Dictionary with session`
- Code: `def get_session_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 244** (high): docstring_param_mismatch
- Comment: `
        Generate a unique session ID.

        Args:
            service_name: Service name to incl`
- Code: `def _generate_session_id(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_name', 'self'}

### src\core\session\rate_limited_session_manager.py

**Line 48** (high): docstring_param_mismatch
- Comment: `
        Initialize rate-limited session manager.

        Args:
            config: Configuration d`
- Code: `def __init__(self, config, logger_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 69** (high): docstring_param_mismatch
- Comment: `
        Create a new rate-limited session.

        Args:
            service_name: Name of service`
- Code: `def create_session(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'kwargs', 'Args'}, extra={'service_name', 'self'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
        Validate that a session exists and is active.

        Args:
            session_id: Sessio`
- Code: `def validate_session(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 148** (high): docstring_param_mismatch
- Comment: `
        Check if a request can be made for this session.

        Args:
            service_name: S`
- Code: `def can_make_request(self, service_name, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_name', 'self'}

**Line 187** (high): docstring_param_mismatch
- Comment: `
        Record a request for rate limiting.

        Args:
            service_name: Service name
 `
- Code: `def record_request(self, service_name, session_id, success)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'service_name', 'self'}

**Line 210** (high): docstring_param_mismatch
- Comment: `
        Wait for rate limit to reset.

        Args:
            service_name: Service name
       `
- Code: `def wait_for_rate_limit_reset(self, service_name, session_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'service_name', 'self'}

**Line 238** (high): docstring_param_mismatch
- Comment: `
        Handle a rate limit error from the service.

        Immediately triggers rate limiting reg`
- Code: `def handle_rate_limit_error(self, service_name, session_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'service_name', 'self'}

**Line 257** (high): docstring_param_mismatch
- Comment: `
        Get rate limit status for a service.

        Args:
            service_name: Service name
`
- Code: `def get_rate_limit_status(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_name', 'self'}

**Line 281** (high): docstring_param_mismatch
- Comment: `
        Manually reset rate limit for a service.

        Args:
            service_name: Service n`
- Code: `def reset_rate_limit(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_name', 'self'}

### src\core\smart_assignment_optimizer.py

**Line 120** (high): comment_return_mismatch
- Comment: `Return agent with highest score`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\core\stall_resumer_guard.py

**Line 72** (high): docstring_param_mismatch
- Comment: `
    Validate if resume prompt should be sent to agent.
    
    Uses hardened activity detection to`
- Code: `def should_send_resume(agent_id, lookback_minutes)`
- Issue: Docstring params don't match: missing={'Args', 'reason', 'should_send'}, extra={'agent_id'}

### src\core\stress_test_metrics_integration.py

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Initialize metrics collection for stress test run.
        
        Args:
            test_`
- Code: `def integrate_with_stress_test_runner(self, test_config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'test_config'}

**Line 85** (high): docstring_param_mismatch
- Comment: `
        Finalize stress test and generate dashboard.
        
        Args:
            output_dir:`
- Code: `def finalize_stress_test(self, output_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'output_dir'}

### src\core\stress_test_runner.py

**Line 120** (high): docstring_param_mismatch
- Comment: `Initialize stress test runner.
        
        Args:
            delivery_callback: Function to cal`
- Code: `def __init__(self, delivery_callback, duration_seconds, messages_per_second, message_types)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'delivery_callback', 'self'}

**Line 200** (high): docstring_param_mismatch
- Comment: `Worker thread for a single agent.
        
        Args:
            agent_id: Agent identifier
    `
- Code: `def _agent_worker(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 251** (high): docstring_param_mismatch
- Comment: `Generate message content.
        
        Args:
            sender: Sender agent ID
            rec`
- Code: `def _generate_message_content(self, sender, recipient, message_type, count)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'sender'}

**Line 278** (high): docstring_param_mismatch
- Comment: `Send a message via delivery callback.
        
        Args:
            sender: Sender agent ID
   `
- Code: `def _send_message(self, sender, recipient, content, message_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'sender'}

**Line 316** (high): docstring_param_mismatch
- Comment: `Get stress test statistics.
        
        Returns:
            Dictionary with test statistics
  `
- Code: `def get_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\stress_testing\message_generator.py

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Initialize message generator.

        Args:
            num_agents: Number of concurrent a`
- Code: `def __init__(self, num_agents, message_types)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'num_agents'}

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Generate batch of test messages.

        Args:
            count: Number of messages to ge`
- Code: `def generate_batch(self, count)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'count'}

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Map message type string to UnifiedMessageType value.

        Args:
            msg_type: M`
- Code: `def _map_message_type(self, msg_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'msg_type', 'self'}

### src\core\stress_testing\messaging_core_protocol.py

**Line 24** (medium): docstring_return_mismatch
- Comment: `
        Send message - matches real messaging_core.send_message signature.

        Args:
         `
- Code: `def send_message(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Send message - matches real messaging_core.send_message signature.

        Args:
         `
- Code: `def send_message(self, content, sender, recipient, message_type, priority, tags, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

### src\core\stress_testing\metrics_collector.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
        Record a message delivery attempt.

        Args:
            message_record: Dictionary wi`
- Code: `def record_message(self, message_record)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message_record', 'self'}

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Calculate and return metrics.

        Returns:
            Dictionary with comprehensive m`
- Code: `def get_metrics(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\core\stress_testing\mock_messaging_core.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Initialize mock messaging core.

        Args:
            metrics_collector: Optional metr`
- Code: `def __init__(self, metrics_collector, delivery_success_rate, simulated_delay)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'metrics_collector', 'self'}

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Simulate message delivery - NO REAL AGENT INTERACTION.

        Args:
            content: `
- Code: `def send_message(self, content, sender, recipient, message_type, priority, tags, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

### src\core\stress_testing\real_messaging_core_adapter.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Initialize adapter with real send_message function.

        Args:
            send_message`
- Code: `def __init__(self, send_message_func)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'send_message_func', 'self'}

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Delegate to real messaging core.

        Args:
            content: Message content
      `
- Code: `def send_message(self, content, sender, recipient, message_type, priority, tags, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

### src\core\stress_testing\stress_runner.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Initialize stress test runner.

        Args:
            num_agents: Number of concurrent `
- Code: `def __init__(self, num_agents, messages_per_agent, message_types)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'num_agents'}

**Line 52** (high): docstring_param_mismatch
- Comment: `
        Run complete stress test.

        Args:
            batch_size: Number of messages to proc`
- Code: `def run_stress_test(self, batch_size, interval)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'batch_size'}

### src\core\synthetic_github.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Initialize sandbox mode manager.
        
        Args:
            config_file: Path to sa`
- Code: `def __init__(self, config_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config_file'}

**Line 143** (high): docstring_param_mismatch
- Comment: `
        Get repository (local-first, GitHub fallback).
        
        Args:
            repo_name`
- Code: `def get_repo(self, repo_name, github_user, branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 190** (high): docstring_param_mismatch
- Comment: `
        Create branch (local-only, GitHub sync deferred).
        
        Args:
            repo_n`
- Code: `def create_branch(self, repo_name, branch_name, source_branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 231** (high): docstring_param_mismatch
- Comment: `
        Push branch to GitHub (with deferred queue fallback).
        
        Args:
            re`
- Code: `def push_branch(self, repo_name, branch, force)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 328** (high): docstring_param_mismatch
- Comment: `
        Create pull request (with deferred queue fallback).
        
        Args:
            repo`
- Code: `def create_pr(self, repo_name, branch, base_branch, title, body)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 451** (high): docstring_param_mismatch
- Comment: `
        Get file content (local-first).
        
        Args:
            repo_name: Name of repos`
- Code: `def get_file(self, repo_name, file_path, branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 486** (high): docstring_param_mismatch
- Comment: `
        Merge branches locally.
        
        Args:
            repo_name: Name of repository
  `
- Code: `def merge_branches(self, repo_name, source_branch, target_branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 554** (high): docstring_param_mismatch
- Comment: `
        Initialize sandbox mode manager.
        
        Args:
            config_file: Path to sa`
- Code: `def __init__(self, config_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config_file'}

**Line 664** (high): docstring_param_mismatch
- Comment: `
        Get repository (local-first, GitHub fallback).
        
        Args:
            repo_name`
- Code: `def get_repo(self, repo_name, github_user, branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 711** (high): docstring_param_mismatch
- Comment: `
        Create branch (local-only, GitHub sync deferred).
        
        Args:
            repo_n`
- Code: `def create_branch(self, repo_name, branch_name, source_branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 752** (high): docstring_param_mismatch
- Comment: `
        Push branch to GitHub (with deferred queue fallback).
        
        Args:
            re`
- Code: `def push_branch(self, repo_name, branch, force)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 849** (high): docstring_param_mismatch
- Comment: `
        Create pull request (with deferred queue fallback).
        
        Args:
            repo`
- Code: `def create_pr(self, repo_name, branch, base_branch, title, body)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 972** (high): docstring_param_mismatch
- Comment: `
        Get file content (local-first).
        
        Args:
            repo_name: Name of repos`
- Code: `def get_file(self, repo_name, file_path, branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 1007** (high): docstring_param_mismatch
- Comment: `
        Merge branches locally.
        
        Args:
            repo_name: Name of repository
  `
- Code: `def merge_branches(self, repo_name, source_branch, target_branch)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

### src\core\task_completion_detector.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Register a task for completion monitoring.
        
        Args:
            task_id: Uniq`
- Code: `def register_task(self, task_id, task_type, expected_output_file, success_patterns, failure_patterns, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_id'}

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Update task with output and check for completion.
        
        Args:
            task_i`
- Code: `def update_task_output(self, task_id, output, exit_code)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

**Line 166** (high): docstring_param_mismatch
- Comment: `
        Check if task is complete.
        
        Returns:
            Tuple of (is_complete, sta`
- Code: `def is_task_complete(self, task_id)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'task_id'}

**Line 196** (high): docstring_param_mismatch
- Comment: `
        Remove completed tasks older than max_age_hours.
        
        Returns:
            Numb`
- Code: `def cleanup_completed_tasks(self, max_age_hours)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'max_age_hours'}

**Line 226** (high): docstring_param_mismatch
- Comment: `
        Detect if output indicates completion.
        
        Common completion indicators:
     `
- Code: `def detect_output_completion(self, output, success_indicators)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'success_indicators', 'output'}

**Line 316** (high): docstring_param_mismatch
- Comment: `
    Quick helper to detect if command output indicates completion.
    
    Returns:
        Tuple `
- Code: `def detect_command_completion(output)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'output'}

### src\core\unified_config.py

**Line 75** (medium): deprecated_code_active
- Comment: `Deprecated alias`
- Code: `"UnifiedConfig",`
- Issue: Code marked as deprecated but still active

### src\core\unified_data_processing_system.py

**Line 19** (high): docstring_param_mismatch
- Comment: `Read JSON file with error handling.

    Args:
        file_path: Path to JSON file

    Returns:
  `
- Code: `def read_json(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 40** (high): docstring_param_mismatch
- Comment: `Write data to JSON file with error handling.

    Args:
        file_path: Path to JSON file
       `
- Code: `def write_json(file_path, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 63** (high): docstring_param_mismatch
- Comment: `Ensure directory exists.

    Args:
        dir_path: Directory path

    Returns:
        True if s`
- Code: `def ensure_directory(dir_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'dir_path'}

**Line 79** (high): docstring_param_mismatch
- Comment: `Resolve path to absolute path.

    Args:
        path: Path to resolve

    Returns:
        Resolv`
- Code: `def resolve_path(path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'path'}

**Line 91** (high): docstring_param_mismatch
- Comment: `Write content to file with error handling.

    Args:
        file_path: Path to file
        conten`
- Code: `def write_file(file_path, content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

### src\core\utilities\handler_utilities.py

**Line 17** (high): docstring_param_mismatch
- Comment: `
    Handle error with context and optional traceback logging.

    Consolidates 3 duplicate impleme`
- Code: `def handle_error(error, context, log_traceback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

**Line 51** (high): docstring_param_mismatch
- Comment: `
    Handle file operation errors.

    From specialized_handlers.py and error_handling_orchestrator`
- Code: `def handle_file_error(error, file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

**Line 73** (high): docstring_param_mismatch
- Comment: `
    Handle network operation errors.

    From specialized_handlers.py and error_handling_orchestra`
- Code: `def handle_network_error(error, endpoint)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

**Line 95** (high): docstring_param_mismatch
- Comment: `
    Handle database operation errors.

    From specialized_handlers.py and error_handling_orchestr`
- Code: `def handle_database_error(error, operation)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

**Line 117** (high): docstring_param_mismatch
- Comment: `
    Handle validation errors.

    From specialized_handlers.py and error_handling_orchestrator.py
`
- Code: `def handle_validation_error(error, field)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

**Line 139** (high): docstring_param_mismatch
- Comment: `
    Handle agent operation errors.

    From specialized_handlers.py and error_handling_orchestrato`
- Code: `def handle_agent_error(error, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

**Line 161** (high): docstring_param_mismatch
- Comment: `
    Handle generic operation with context and payload.

    Consolidates 3 duplicate implementation`
- Code: `def handle_operation(context, payload)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'context'}

**Line 193** (high): docstring_param_mismatch
- Comment: `
    Handle generic event.

    Consolidates 3 duplicate implementations from:
    - gaming_integrat`
- Code: `def handle_event(event)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'event'}

**Line 216** (high): docstring_param_mismatch
- Comment: `
    Handle rate limit errors for services.

    Consolidates 3 duplicate implementations from:
    `
- Code: `def handle_rate_limit_error(service_name, session_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'service_name'}

**Line 234** (high): docstring_param_mismatch
- Comment: `
    Handle coordination message.

    Consolidates 2 duplicate implementations from:
    - osrs_age`
- Code: `def handle_coordination_message(message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message'}

**Line 254** (high): docstring_param_mismatch
- Comment: `
    Handle resource request message.

    Consolidates 2 duplicate implementations from:
    - osrs`
- Code: `def handle_resource_request(message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message'}

**Line 274** (high): docstring_param_mismatch
- Comment: `
    Handle activity coordination message.

    Consolidates 2 duplicate implementations from:
    -`
- Code: `def handle_activity_coordination(message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message'}

**Line 294** (high): docstring_param_mismatch
- Comment: `
    Handle emergency alert message.

    Consolidates 2 duplicate implementations from:
    - osrs_`
- Code: `def handle_emergency_alert(message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message'}

**Line 377** (high): docstring_param_mismatch
- Comment: `
    Handle performance alerts.

    From gaming_alert_handlers.py

    Args:
        manager: Alert`
- Code: `def handle_performance_alerts(manager, performance_metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'manager'}

**Line 403** (high): docstring_param_mismatch
- Comment: `
    Handle system health alerts.

    From gaming_alert_handlers.py

    Args:
        manager: Ale`
- Code: `def handle_system_health_alerts(manager, health_metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'manager'}

**Line 429** (high): docstring_param_mismatch
- Comment: `
    Handle alert acknowledgment.

    From gaming_alert_handlers.py

    Args:
        manager: Ale`
- Code: `def handle_alert_acknowledgment(manager, alert_id, acknowledged_by)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'manager'}

**Line 450** (high): docstring_param_mismatch
- Comment: `
    Handle alert resolution.

    From gaming_alert_handlers.py

    Args:
        manager: Alert m`
- Code: `def handle_alert_resolution(manager, alert_id, resolved_by, resolution_notes)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'manager'}

### src\core\utilities\processing_utilities.py

**Line 95** (high): docstring_param_mismatch
- Comment: `
    Process results with type-specific handling.

    Consolidates 4 duplicate implementations from`
- Code: `def process_results(results, result_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'results'}

**Line 135** (high): docstring_param_mismatch
- Comment: `
    Process event with type-specific handling.

    Consolidates 2 duplicate implementations from:
`
- Code: `def process_event(event_type, event_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'event_type'}

**Line 201** (high): docstring_param_mismatch
- Comment: `
    Process analytics data.

    From coordination_analytics_orchestrator.py

    Args:
        dat`
- Code: `def process_analytics(data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'data'}

**Line 226** (high): docstring_param_mismatch
- Comment: `
    Process insight data.

    From insight_processor.py

    Args:
        insight_data: Insight d`
- Code: `def process_insight(insight_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'insight_data'}

**Line 251** (high): docstring_param_mismatch
- Comment: `
    Process prediction data.

    From prediction_processor.py

    Args:
        data: Prediction `
- Code: `def process_prediction(data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'data'}

**Line 276** (high): docstring_param_mismatch
- Comment: `
    Process workflow data.

    From base_orchestrator.py

    Args:
        data: Workflow data (a`
- Code: `def process_workflow(data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'data'}

**Line 324** (high): docstring_param_mismatch
- Comment: `
    Process message for task integration.

    From messaging_integration.py

    Args:
        mes`
- Code: `def process_message_for_task(message, task_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message'}

### src\core\utilities\standardized_logging.py

**Line 52** (high): docstring_param_mismatch
- Comment: `Initialize formatter.

        Args:
            use_colors: Enable colored output (for console only`
- Code: `def __init__(self, use_colors)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'use_colors', 'self'}

**Line 85** (high): docstring_param_mismatch
- Comment: `Initialize logger factory.

        Args:
            level: Default log level
            enable_co`
- Code: `def __init__(self, level, enable_console, enable_file, log_dir, max_file_size, backup_count, use_colors)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'level'}

**Line 118** (high): docstring_param_mismatch
- Comment: `Create standardized logger instance.

        Args:
            name: Logger name (typically __name_`
- Code: `def create_logger(self, name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'name'}

**Line 160** (high): docstring_param_mismatch
- Comment: `Get standardized logger instance (simple usage).

    This is the recommended way to get a logger in`
- Code: `def get_logger(name)`
- Issue: Docstring params don't match: missing={'Example', 'Returns', 'Args'}, extra={'name'}

**Line 178** (high): docstring_param_mismatch
- Comment: `Configure global logging settings.

    Call this once at application startup to configure logging f`
- Code: `def configure_logging(level, enable_console, enable_file, log_dir, use_colors)`
- Issue: Docstring params don't match: missing={'Example', 'Args'}, extra={'level'}

### src\core\utilities\validation_utilities.py

**Line 19** (high): docstring_param_mismatch
- Comment: `
    Validate Python import statement syntax.

    Consolidates 4 duplicate implementations from:
  `
- Code: `def validate_import_syntax(import_statement)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'import_statement'}

**Line 48** (high): docstring_param_mismatch
- Comment: `
    Validate import pattern string.

    Consolidates 3 duplicate implementations from:
    - unifi`
- Code: `def validate_import_pattern(pattern)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'pattern'}

**Line 70** (high): docstring_param_mismatch
- Comment: `
    Validate file path and return validation result.

    Consolidates 3 duplicate implementations `
- Code: `def validate_file_path(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 122** (high): docstring_param_mismatch
- Comment: `
    Validate configuration dictionary.

    Consolidates 3 duplicate implementations from:
    - co`
- Code: `def validate_config(config, required_fields)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

**Line 150** (high): docstring_param_mismatch
- Comment: `
    Validate session ID and optionally check if it exists.

    Consolidates 3 duplicate implementa`
- Code: `def validate_session(session_id, sessions)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'session_id'}

**Line 176** (high): docstring_param_mismatch
- Comment: `
    Validate screen coordinates.

    Consolidates 2 duplicate implementations from:
    - messagin`
- Code: `def validate_coordinates(coordinates, screen_width, screen_height)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'coordinates'}

**Line 208** (high): docstring_param_mismatch
- Comment: `
    Validate forecast accuracy against actual results.

    Consolidates 2 duplicate implementation`
- Code: `def validate_forecast_accuracy(forecast, actual)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'forecast'}

**Line 241** (high): docstring_param_mismatch
- Comment: `
    Safely validate if object has attribute.

    From unified_validation_orchestrator.py

    Args`
- Code: `def validate_hasattr(obj, attr)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj'}

**Line 257** (high): docstring_param_mismatch
- Comment: `
    Validate object type.

    From unified_validation_orchestrator.py

    Args:
        obj: Obje`
- Code: `def validate_type(obj, expected_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj'}

**Line 273** (high): docstring_param_mismatch
- Comment: `
    Validate object is not None.

    From unified_validation_orchestrator.py

    Args:
        ob`
- Code: `def validate_not_none(obj)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj'}

**Line 288** (high): docstring_param_mismatch
- Comment: `
    Validate object is not empty.

    From unified_validation_orchestrator.py

    Args:
        o`
- Code: `def validate_not_empty(obj)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj'}

**Line 307** (high): docstring_param_mismatch
- Comment: `
    Validate value is within range.

    From unified_validation_orchestrator.py

    Args:
       `
- Code: `def validate_range(value, min_val, max_val)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'value'}

**Line 327** (high): docstring_param_mismatch
- Comment: `
    Validate string against regex pattern.

    From unified_validation_orchestrator.py

    Args:
`
- Code: `def validate_regex(value, pattern)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'value'}

**Line 348** (high): docstring_param_mismatch
- Comment: `
    Validate object using custom validator function.

    From unified_validation_orchestrator.py

`
- Code: `def validate_custom(obj, validator_func)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj'}

### src\core\utils\agent_matching.py

**Line 46** (high): docstring_param_mismatch
- Comment: `Calculate agent match score for task requirements.

        Args:
            task_requirements: Tas`
- Code: `def calculate_agent_match_score(task_requirements, agent_capabilities)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'task_requirements'}

**Line 80** (high): docstring_param_mismatch
- Comment: `Calculate agent type match score for task requirements.

        Args:
            task_requirements`
- Code: `def get_agent_type_match_score(task_requirements, agent_type, metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'task_requirements'}

**Line 112** (high): docstring_param_mismatch
- Comment: `Rank available agents by their capability to handle the task.

        Args:
            task_requir`
- Code: `def rank_agents_by_capability(task_requirements, available_agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'task_requirements'}

**Line 144** (high): docstring_param_mismatch
- Comment: `Get the best agent for a specific task.

        Args:
            task_requirements: Task requireme`
- Code: `def get_best_agent_for_task(task_requirements, available_agents, min_score)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'task_requirements'}

### src\core\utils\coordination_utils.py

**Line 28** (high): docstring_param_mismatch
- Comment: `Update coordination metrics.
        
        Args:
            success: Whether coordination was su`
- Code: `def update_coordination_metrics(success, coordination_time)`
- Issue: Docstring params don't match: missing={'kwargs', 'Args'}, extra={'success'}

**Line 62** (high): docstring_param_mismatch
- Comment: `Update performance metrics.
        
        Args:
            task_id: Task identifier
            `
- Code: `def update_performance_metrics(task_id, execution_time, success)`
- Issue: Docstring params don't match: missing={'kwargs', 'Args'}, extra={'task_id'}

**Line 100** (high): docstring_param_mismatch
- Comment: `Store coordination history entry.
        
        Args:
            entry: History entry dictionary`
- Code: `def store_coordination_history(entry)`
- Issue: Docstring params don't match: missing={'kwargs', 'Args'}, extra={'entry'}

**Line 131** (high): docstring_param_mismatch
- Comment: `Get performance summary.
        
        Args:
            metrics: Optional metrics dictionary (us`
- Code: `def get_performance_summary(metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'metrics'}

**Line 220** (high): docstring_param_mismatch
- Comment: `Get comprehensive coordination summary.

        Args:
            metrics: Performance metrics dict`
- Code: `def get_coordination_summary(metrics, coordination_history)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'metrics'}

**Line 243** (high): docstring_param_mismatch
- Comment: `Validate coordination data structure.

        Args:
            data: Coordination data to validate`
- Code: `def validate_coordination_data(data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'data'}

### src\core\utils\file_utils.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
    Ensure directory is completely removed, handling readonly files.
    
    SSOT for directory re`
- Code: `def ensure_directory_removed(dir_path, name, retry_delay, max_retries)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'dir_path'}

### src\core\utils\github_utils.py

**Line 89** (high): docstring_param_mismatch
- Comment: `
    Get GitHub token from environment or .env file.

    SSOT for GitHub token extraction - consoli`
- Code: `def get_github_token(project_root)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'project_root'}

**Line 131** (high): docstring_param_mismatch
- Comment: `
    Create standard GitHub API headers for PR operations.

    SSOT for GitHub API headers - consol`
- Code: `def create_github_pr_headers(token)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'token'}

**Line 153** (high): docstring_param_mismatch
- Comment: `
    Create GitHub PR API URL.

    Args:
        owner: Repository owner
        repo: Repository n`
- Code: `def create_github_pr_url(owner, repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'owner'}

**Line 167** (high): docstring_param_mismatch
- Comment: `
    Create PR data payload.

    Args:
        title: PR title
        body: PR body
        head: `
- Code: `def create_pr_data(title, body, head, base)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'title'}

**Line 188** (high): docstring_param_mismatch
- Comment: `
    Check if PR already exists for given head branch.

    SSOT for PR existence checking - consoli`
- Code: `def check_existing_pr(owner, repo, head, token, head_owner, timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'owner'}

### src\core\utils\serialization_utils.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Convert object to dictionary.
    
    SSOT for to_dict() conversion - consolidates duplicate s`
- Code: `def to_dict(obj, include_none)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj'}

**Line 104** (high): docstring_param_mismatch
- Comment: `
        Convert object to dictionary using SSOT utility.
        
        Args:
            include`
- Code: `def to_dict(self, include_none)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'include_none'}

### src\core\utils\validation_utils.py

**Line 19** (high): docstring_param_mismatch
- Comment: `
    Print formatted validation report.
    
    SSOT for validation output formatting - consolidate`
- Code: `def print_validation_report(errors, warnings, success_message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'errors'}

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Print validation report using errors and warnings attributes.
        
        Expects vali`
- Code: `def print_report(self)`
- Issue: Docstring params don't match: missing={'warnings', 'errors'}, extra={'self'}

**Line 69** (high): docstring_param_mismatch
- Comment: `
    Validate value is within specified range.
    
    SSOT for range validation - consolidates dup`
- Code: `def validate_range(value, min_val, max_val, field_name)`
- Issue: Docstring params don't match: missing={'Raises', 'Args'}, extra={'value'}

**Line 95** (high): docstring_param_mismatch
- Comment: `
    Validate value is positive (>= min_val).
    
    SSOT for positive value validation - consolid`
- Code: `def validate_positive(value, field_name, min_val)`
- Issue: Docstring params don't match: missing={'default', 'Raises', 'Args'}, extra={'value'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
    Validate configuration using list of field validators.
    
    SSOT for list-based configurati`
- Code: `def validate_config_list(config, validators)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

### src\core\validation\unified_validation_orchestrator.py

**Line 27** (high): docstring_param_mismatch
- Comment: `Validate that object has attribute.
        
        Args:
            obj: Object to validate
     `
- Code: `def validate_hasattr(self, obj, attr)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj', 'self'}

**Line 39** (high): docstring_param_mismatch
- Comment: `Validate that object is of expected type.
        
        Args:
            obj: Object to validate`
- Code: `def validate_type(self, obj, expected_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj', 'self'}

**Line 51** (high): docstring_param_mismatch
- Comment: `Validate that object is not None.
        
        Args:
            obj: Object to validate
       `
- Code: `def validate_not_none(self, obj)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj', 'self'}

**Line 62** (high): docstring_param_mismatch
- Comment: `Validate that object is not empty.
        
        Args:
            obj: Object to validate
      `
- Code: `def validate_not_empty(self, obj)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj', 'self'}

**Line 77** (high): docstring_param_mismatch
- Comment: `Validate that value is within range.
        
        Args:
            value: Value to validate
   `
- Code: `def validate_range(self, value, min_val, max_val)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'value'}

**Line 90** (high): docstring_param_mismatch
- Comment: `Validate that value matches regex pattern.
        
        Args:
            value: Value to valida`
- Code: `def validate_regex(self, value, pattern)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'value'}

**Line 103** (high): docstring_param_mismatch
- Comment: `Validate using custom validator function.
        
        Args:
            obj: Object to validate`
- Code: `def validate_custom(self, obj, validator_func)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj', 'self'}

### src\core\vector_strategic_oversight\unified_strategic_oversight\analyzers\swarm_analyzer.py

**Line 298** (high): docstring_param_mismatch
- Comment: `Fallback: Analyze mission data directly without task repository.`
- Code: `def _analyze_mission_data_directly(self, mission_data)`
- Issue: Docstring params don't match: missing={'Fallback'}, extra={'self', 'mission_data'}

**Line 453** (high): docstring_param_mismatch
- Comment: `Fallback: Analyze agent performance directly from agent data.`
- Code: `def _analyze_agent_performance_directly(self, agent_data, time_window_hours)`
- Issue: Docstring params don't match: missing={'Fallback'}, extra={'self', 'agent_data', 'time_window_hours'}

**Line 79** (high): comment_return_mismatch
- Comment: `No message data - return minimal insight`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\core\workspace_agent_registry.py

**Line 84** (high): docstring_param_mismatch
- Comment: `Get onboarding coordinates for an agent.

        Uses SSOT coordinate loader for consistency across`
- Code: `def get_onboarding_coords(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\discord_commander\messaging_controller.py

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Initialize the Discord messaging controller.

        Args:
            messaging_service: `
- Code: `def __init__(self, messaging_service)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'messaging_service', 'self'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Create agent messaging view using canonical WOW FACTOR controller.

        Returns:
      `
- Code: `def create_agent_messaging_view(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Create swarm status view using canonical WOW FACTOR controller.

        Returns:
         `
- Code: `def create_swarm_status_view(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 133** (high): docstring_param_mismatch
- Comment: `
        Get current agent status.

        Returns:
            Dictionary of agent IDs to status i`
- Code: `def get_agent_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\discord_commander\music_commands.py

**Line 63** (high): docstring_param_mismatch
- Comment: `
            Extract song title from !music(song title) command.
            
            Args:
    `
- Code: `def _extract_song_title(self, content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

### src\discord_commander\status_change_monitor.py

**Line 50** (high): docstring_param_mismatch
- Comment: `
        Initialize status change monitor.

        Args:
            bot: Discord bot instance
    `
- Code: `def __init__(self, bot, channel_id, scheduler)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'bot'}

**Line 779** (high): docstring_param_mismatch
- Comment: `
        Manually trigger status update notification.

        Can be called by AgentLifecycle when `
- Code: `def notify_status_change(self, agent_id, status)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 797** (high): docstring_param_mismatch
- Comment: `
    Setup and start status change monitoring.

    Args:
        bot: Discord bot instance
        `
- Code: `def setup_status_monitor(bot, channel_id, scheduler)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'bot'}

### src\discord_commander\status_reader.py

**Line 30** (high): docstring_param_mismatch
- Comment: `Initialize status reader with memory leak prevention.

        Args:
            workspace_dir: Dire`
- Code: `def __init__(self, workspace_dir, cache_ttl)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'workspace_dir'}

**Line 43** (high): docstring_param_mismatch
- Comment: `Read status for a specific agent.

        Args:
            agent_id: Agent identifier (e.g., "Agen`
- Code: `def read_agent_status(self, agent_id, force_refresh)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 103** (high): docstring_param_mismatch
- Comment: `Read status for all agents (only main 8 agents, not role workspaces).

        Returns:
            `
- Code: `def read_all_statuses(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 129** (high): docstring_param_mismatch
- Comment: `Normalize status data to standard format.

        Args:
            data: Raw status.json data

   `
- Code: `def _normalize_status(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 188** (high): docstring_param_mismatch
- Comment: `Get cache statistics.

        Returns:
            Cache statistics
        `
- Code: `def get_cache_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\discord_commander\test_utils.py

**Line 124** (high): docstring_param_mismatch
- Comment: `
    Get mock Discord module when discord.py is not available.
    
    Returns:
        Tuple of (d`
- Code: `def get_mock_discord()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 134** (high): docstring_param_mismatch
- Comment: `
    Create mock Discord imports for use when discord.py is unavailable.
    
    Returns:
        D`
- Code: `def create_mock_discord_imports()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### src\discord_commander\tools_commands.py

**Line 252** (high): comment_return_mismatch
- Comment: `Return None if Discord not available (cog won't load)`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\discord_commander\unified_discord_bot.py

**Line 1454** (high): docstring_param_mismatch
- Comment: `Perform true restart: spawn fresh process for bot + queue processor, then exit current.`
- Code: `def _perform_true_restart(self)`
- Issue: Docstring params don't match: missing={'restart'}, extra={'self'}

### src\discord_commander\utils\message_chunking.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
    Split a long message into chunks that fit within Discord's limits.
    
    Args:
        conte`
- Code: `def chunk_message(content, max_size)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'content'}

**Line 68** (high): docstring_param_mismatch
- Comment: `
    Split a long field value into multiple parts.
    
    Args:
        value: Field value to chun`
- Code: `def chunk_field_value(value, max_size)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'value'}

**Line 102** (high): docstring_param_mismatch
- Comment: `
    Split a long embed description into multiple parts.
    
    Args:
        description: Embed d`
- Code: `def chunk_embed_description(description, max_size)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'description'}

### src\discord_commander\views\swarm_snapshot_view.py

**Line 32** (high): docstring_param_mismatch
- Comment: `Initialize swarm snapshot view.
        
        Args:
            snapshot: Swarm snapshot data fro`
- Code: `def __init__(self, snapshot)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'snapshot'}

### src\domain\ports\agent_repository.py

**Line 26** (medium): docstring_return_mismatch
- Comment: `
        Retrieve an agent by its identifier.

        Args:
            agent_id: The unique identi`
- Code: `def get(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Retrieve an agent by its identifier.

        Args:
            agent_id: The unique identi`
- Code: `def get(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 38** (medium): docstring_return_mismatch
- Comment: `
        Retrieve agents that have a specific capability.

        Args:
            capability: The`
- Code: `def get_by_capability(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Retrieve agents that have a specific capability.

        Args:
            capability: The`
- Code: `def get_by_capability(self, capability)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'capability'}

**Line 50** (medium): docstring_return_mismatch
- Comment: `
        Retrieve all active agents.

        Returns:
            Iterable of active agents
       `
- Code: `def get_active(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 50** (high): docstring_param_mismatch
- Comment: `
        Retrieve all active agents.

        Returns:
            Iterable of active agents
       `
- Code: `def get_active(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 59** (medium): docstring_return_mismatch
- Comment: `
        Retrieve agents that can accept more tasks.

        Returns:
            Iterable of avail`
- Code: `def get_available(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 59** (high): docstring_param_mismatch
- Comment: `
        Retrieve agents that can accept more tasks.

        Returns:
            Iterable of avail`
- Code: `def get_available(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 68** (high): docstring_param_mismatch
- Comment: `
        Add a new agent to the repository.

        Args:
            agent: The agent to add

    `
- Code: `def add(self, agent)`
- Issue: Docstring params don't match: missing={'Raises', 'Args'}, extra={'self', 'agent'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Save an existing agent (create or update).

        Args:
            agent: The agent to s`
- Code: `def save(self, agent)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent'}

**Line 89** (medium): docstring_return_mismatch
- Comment: `
        Delete an agent from the repository.

        Args:
            agent_id: The identifier of`
- Code: `def delete(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Delete an agent from the repository.

        Args:
            agent_id: The identifier of`
- Code: `def delete(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 101** (medium): docstring_return_mismatch
- Comment: `
        List all agents in the repository.

        Returns:
            Iterable of all agents
   `
- Code: `def list_all(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 101** (high): docstring_param_mismatch
- Comment: `
        List all agents in the repository.

        Returns:
            Iterable of all agents
   `
- Code: `def list_all(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\domain\ports\browser.py

**Line 49** (high): docstring_param_mismatch
- Comment: `
        Open browser with optional profile.
        
        Args:
            profile: Optional br`
- Code: `def open(self, profile)`
- Issue: Docstring params don't match: missing={'Args', 'Raises', 'ValueError'}, extra={'self', 'profile'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        
      `
- Code: `def goto(self, url)`
- Issue: Docstring params don't match: missing={'Raises', 'RuntimeError', 'Args'}, extra={'url', 'self'}

**Line 77** (medium): docstring_return_mismatch
- Comment: `
        Send prompt and wait for response.
        
        Args:
            prompt: Text prompt t`
- Code: `def send_and_wait(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 77** (high): docstring_param_mismatch
- Comment: `
        Send prompt and wait for response.
        
        Args:
            prompt: Text prompt t`
- Code: `def send_and_wait(self, prompt, timeout_s)`
- Issue: Docstring params don't match: missing={'default', 'Raises', 'Args', 'TimeoutError', 'Returns', 'RuntimeError'}, extra={'self', 'prompt'}

**Line 100** (high): docstring_param_mismatch
- Comment: `
        Close the browser.
        
        Raises:
            RuntimeError: If browser cannot be `
- Code: `def close(self)`
- Issue: Docstring params don't match: missing={'Raises'}, extra={'self'}

**Line 110** (medium): docstring_return_mismatch
- Comment: `
        Check if browser is ready for interactions.
        
        Returns:
            True if b`
- Code: `def is_ready(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Check if browser is ready for interactions.
        
        Returns:
            True if b`
- Code: `def is_ready(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 120** (medium): docstring_return_mismatch
- Comment: `
        Get current browser URL.
        
        Returns:
            Current URL or None if not a`
- Code: `def get_current_url(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 120** (high): docstring_param_mismatch
- Comment: `
        Get current browser URL.
        
        Returns:
            Current URL or None if not a`
- Code: `def get_current_url(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 130** (medium): docstring_return_mismatch
- Comment: `
        Wait for element to appear on page.
        
        Args:
            selector: CSS select`
- Code: `def wait_for_element(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Wait for element to appear on page.
        
        Args:
            selector: CSS select`
- Code: `def wait_for_element(self, selector, timeout_s)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'selector'}

### src\domain\ports\clock.py

**Line 21** (medium): docstring_return_mismatch
- Comment: `
        Get the current time.

        Returns:
            Current datetime in UTC
        `
- Code: `def now(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 21** (high): docstring_param_mismatch
- Comment: `
        Get the current time.

        Returns:
            Current datetime in UTC
        `
- Code: `def now(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 30** (medium): docstring_return_mismatch
- Comment: `
        Get the current UTC time.

        Returns:
            Current UTC datetime
        `
- Code: `def utcnow(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Get the current UTC time.

        Returns:
            Current UTC datetime
        `
- Code: `def utcnow(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 39** (medium): docstring_return_mismatch
- Comment: `
        Create datetime from Unix timestamp.

        Args:
            timestamp: Unix timestamp (`
- Code: `def from_timestamp(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Create datetime from Unix timestamp.

        Args:
            timestamp: Unix timestamp (`
- Code: `def from_timestamp(self, timestamp)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'timestamp', 'self'}

**Line 51** (medium): docstring_return_mismatch
- Comment: `
        Convert datetime to Unix timestamp.

        Args:
            dt: Datetime object

       `
- Code: `def to_timestamp(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 51** (high): docstring_param_mismatch
- Comment: `
        Convert datetime to Unix timestamp.

        Args:
            dt: Datetime object

       `
- Code: `def to_timestamp(self, dt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'dt'}

### src\domain\ports\logger.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Log debug message.

        Args:
            message: Log message
            **context: A`
- Code: `def debug(self, message)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Log info message.

        Args:
            message: Log message
            **context: Ad`
- Code: `def info(self, message)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 51** (high): docstring_param_mismatch
- Comment: `
        Log warning message.

        Args:
            message: Log message
            **context:`
- Code: `def warning(self, message)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Log error message.

        Args:
            message: Log message
            exception: O`
- Code: `def error(self, message, exception)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Log critical message.

        Args:
            message: Log message
            exception`
- Code: `def critical(self, message, exception)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 83** (high): docstring_param_mismatch
- Comment: `
        Log message with specific level.

        Args:
            level: Log level
            me`
- Code: `def log(self, level, message, exception)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'self', 'level'}

### src\domain\ports\message_bus.py

**Line 33** (medium): docstring_return_mismatch
- Comment: `
        Publish a domain event to all subscribers.
        
        Args:
            event_type: T`
- Code: `def publish(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Publish a domain event to all subscribers.
        
        Args:
            event_type: T`
- Code: `def publish(self, event_type, event_data, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'RuntimeError', 'Args'}, extra={'event_type', 'self'}

**Line 57** (medium): docstring_return_mismatch
- Comment: `
        Subscribe to events of a specific type.
        
        Args:
            event_type: Type`
- Code: `def subscribe(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Subscribe to events of a specific type.
        
        Args:
            event_type: Type`
- Code: `def subscribe(self, event_type, handler, handler_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'event_type', 'self'}

**Line 80** (medium): docstring_return_mismatch
- Comment: `
        Unsubscribe a handler from events.
        
        Args:
            handler_id: Unique id`
- Code: `def unsubscribe(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Unsubscribe a handler from events.
        
        Args:
            handler_id: Unique id`
- Code: `def unsubscribe(self, handler_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'handler_id'}

**Line 96** (medium): docstring_return_mismatch
- Comment: `
        Get list of subscribers for event types.
        
        Args:
            event_type: Opt`
- Code: `def get_subscribers(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 96** (high): docstring_param_mismatch
- Comment: `
        Get list of subscribers for event types.
        
        Args:
            event_type: Opt`
- Code: `def get_subscribers(self, event_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'event_type', 'self'}

**Line 109** (medium): docstring_return_mismatch
- Comment: `
        Check if message bus is available and ready.
        
        Returns:
            True if `
- Code: `def is_available(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 109** (high): docstring_param_mismatch
- Comment: `
        Check if message bus is available and ready.
        
        Returns:
            True if `
- Code: `def is_available(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 119** (medium): docstring_return_mismatch
- Comment: `
        Get message bus statistics.
        
        Returns:
            Dictionary with stats (to`
- Code: `def get_stats(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 119** (high): docstring_param_mismatch
- Comment: `
        Get message bus statistics.
        
        Returns:
            Dictionary with stats (to`
- Code: `def get_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\domain\ports\task_repository.py

**Line 27** (medium): docstring_return_mismatch
- Comment: `
        Retrieve a task by its identifier.

        Args:
            task_id: The unique identifie`
- Code: `def get(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Retrieve a task by its identifier.

        Args:
            task_id: The unique identifie`
- Code: `def get(self, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

**Line 39** (medium): docstring_return_mismatch
- Comment: `
        Retrieve tasks assigned to a specific agent.

        Args:
            agent_id: The agent`
- Code: `def get_by_agent(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Retrieve tasks assigned to a specific agent.

        Args:
            agent_id: The agent`
- Code: `def get_by_agent(self, agent_id, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 52** (medium): docstring_return_mismatch
- Comment: `
        Retrieve pending (unassigned) tasks.

        Args:
            limit: Maximum number of ta`
- Code: `def get_pending(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 52** (high): docstring_param_mismatch
- Comment: `
        Retrieve pending (unassigned) tasks.

        Args:
            limit: Maximum number of ta`
- Code: `def get_pending(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 64** (high): docstring_param_mismatch
- Comment: `
        Add a new task to the repository.

        Args:
            task: The task to add

       `
- Code: `def add(self, task)`
- Issue: Docstring params don't match: missing={'Raises', 'Args'}, extra={'self', 'task'}

**Line 76** (high): docstring_param_mismatch
- Comment: `
        Save an existing task (create or update).

        Args:
            task: The task to save`
- Code: `def save(self, task)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task'}

**Line 85** (medium): docstring_return_mismatch
- Comment: `
        Delete a task from the repository.

        Args:
            task_id: The identifier of th`
- Code: `def delete(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 85** (high): docstring_param_mismatch
- Comment: `
        Delete a task from the repository.

        Args:
            task_id: The identifier of th`
- Code: `def delete(self, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

**Line 97** (medium): docstring_return_mismatch
- Comment: `
        List all tasks in the repository.

        Args:
            limit: Maximum number of tasks`
- Code: `def list_all(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 97** (high): docstring_param_mismatch
- Comment: `
        List all tasks in the repository.

        Args:
            limit: Maximum number of tasks`
- Code: `def list_all(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

### src\domain\services\assignment_service.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
        Find the best agent for a given task based on business rules.

        Business Rules:
    `
- Code: `def find_best_agent_for_task(self, task, available_agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 73** (high): docstring_param_mismatch
- Comment: `
        Validate if a task can be assigned to an agent.

        Args:
            task: The task t`
- Code: `def validate_assignment(self, task, agent)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 106** (high): docstring_param_mismatch
- Comment: `
        Calculate how suitable an agent is for a task.

        Scoring factors:
        - Current `
- Code: `def _calculate_agent_score(self, agent, task)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'agent', 'task'}

### src\features\flags.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Check if feature is enabled.

    Args:
        feature: Feature name (msg_task, oss_cli, etc.)`
- Code: `def is_enabled(feature)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'feature'}

### src\gaming\dreamos\fsm_file_operations.py

**Line 34** (high): docstring_param_mismatch
- Comment: `Initialize file operations handler.

        Args:
            fsm_root: Root directory for FSM data`
- Code: `def __init__(self, fsm_root, inbox_root, outbox_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'fsm_root'}

**Line 54** (high): docstring_param_mismatch
- Comment: `Save task to disk.

        Args:
            task: Task to save

        Returns:
            True `
- Code: `def save_task(self, task)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 72** (high): docstring_param_mismatch
- Comment: `Load task from disk.

        Args:
            task_id: Task identifier

        Returns:
         `
- Code: `def load_task(self, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

**Line 93** (high): docstring_param_mismatch
- Comment: `Emit verification message for task completion.

        Args:
            task: Task to verify
     `
- Code: `def emit_verification_message(self, task, status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 132** (high): docstring_param_mismatch
- Comment: `Get list of all task files.

        Returns:
            List of task file paths
        `
- Code: `def get_all_task_files(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 144** (high): docstring_param_mismatch
- Comment: `Check for new agent reports in inboxes.

        Returns:
            List of report file paths
    `
- Code: `def check_agent_reports(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 168** (high): docstring_param_mismatch
- Comment: `Move report file to processed folder.

        Args:
            report_file: Report file path

    `
- Code: `def move_to_processed(self, report_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'report_file'}

### src\gaming\dreamos\fsm_orchestrator.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Initialize FSM Orchestrator

        Args:
            fsm_root: Root directory for FSM dat`
- Code: `def __init__(self, fsm_root, inbox_root, outbox_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'fsm_root'}

### src\gaming\dreamos\resumer_v2\atomic_file_manager.py

**Line 14** (high): docstring_param_mismatch
- Comment: `Initialize atomic file manager.

        Args:
            file_path: Path to the file to manage
   `
- Code: `def __init__(self, file_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'file_path'}

**Line 23** (high): docstring_param_mismatch
- Comment: `Write content to file atomically.

        Args:
            content: Content to write
            m`
- Code: `def atomic_write(self, content, mode)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

**Line 53** (high): docstring_param_mismatch
- Comment: `Read content from file atomically.

        Args:
            mode: File mode ('r' for text, 'rb' fo`
- Code: `def atomic_read(self, mode)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'mode', 'self'}

**Line 71** (high): docstring_param_mismatch
- Comment: `Context manager for atomic file updates.

        Args:
            mode: File mode for the update

`
- Code: `def atomic_update(self, mode)`
- Issue: Docstring params don't match: missing={'Yields', 'Args'}, extra={'mode', 'self'}

**Line 96** (high): docstring_param_mismatch
- Comment: `Create a backup of the current file.

        Args:
            backup_suffix: Suffix for backup fil`
- Code: `def backup(self, backup_suffix)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'backup_suffix'}

**Line 114** (high): docstring_param_mismatch
- Comment: `Restore file from backup.

        Args:
            backup_suffix: Suffix of backup file

        R`
- Code: `def restore(self, backup_suffix)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'backup_suffix'}

### src\gaming\dreamos\ui_integration.py

**Line 57** (high): docstring_param_mismatch
- Comment: `Calculate level from XP (simple formula: level = sqrt(xp / 100)).`
- Code: `def calculate_level_from_xp(xp)`
- Issue: Docstring params don't match: missing={'formula'}, extra={'xp'}

**Line 68** (high): docstring_param_mismatch
- Comment: `
    Get player gamification status from FSMOrchestrator and agent data.

    Returns:
        Dict:`
- Code: `def get_player_status()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 303** (high): docstring_param_mismatch
- Comment: `
    Get detailed quest information from FSMOrchestrator.

    Args:
        quest_id: Quest identif`
- Code: `def get_quest_details(quest_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'quest_id'}

**Line 397** (high): docstring_param_mismatch
- Comment: `
    Get agent leaderboard with real agent data.

    Returns:
        List: Leaderboard rankings so`
- Code: `def get_leaderboard()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 470** (high): docstring_param_mismatch
- Comment: `
    Register gamification blueprint with Flask app.

    Args:
        app: Flask application insta`
- Code: `def register_gamification_blueprint(app)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'app'}

### src\gui\components\agent_card.py

**Line 50** (high): docstring_param_mismatch
- Comment: `
            Initialize agent card.

            Args:
                agent_id: Agent identifier (e`
- Code: `def __init__(self, agent_id, parent)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 161** (high): docstring_param_mismatch
- Comment: `
            Update agent status display.

            Args:
                status: Status string (`
- Code: `def update_status(self, status)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'status'}

**Line 193** (high): docstring_param_mismatch
- Comment: `
            Update activity display.

            Args:
                activity: Activity descript`
- Code: `def update_activity(self, activity)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'activity'}

### src\gui\components\status_panel.py

**Line 52** (high): docstring_param_mismatch
- Comment: `
            Initialize status panel.

            Args:
                parent: Parent widget
     `
- Code: `def __init__(self, parent)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'parent'}

**Line 157** (high): docstring_param_mismatch
- Comment: `
            Add a log message with timestamp.

            Args:
                sender: Message se`
- Code: `def add_log_message(self, sender, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'sender'}

### src\gui\controllers\base.py

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Execute action on selected agents.

        Args:
            action_type: Type of action (`
- Code: `def execute_selected_agents_action(self, action_type, action_name, action_func)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'action_type'}

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Broadcast action to all agents.

        Args:
            action_type: Type of action
    `
- Code: `def broadcast_action(self, action_type, action_name, default_command, action_func)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'action_type'}

**Line 178** (high): docstring_param_mismatch
- Comment: `
        Add a message to the log display.

        Args:
            sender: Message sender
       `
- Code: `def log_message(self, sender, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'sender'}

**Line 198** (high): docstring_param_mismatch
- Comment: `
        Setup periodic status updates.

        Args:
            update_interval: Update interval `
- Code: `def setup_status_updates(self, update_interval)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'update_interval'}

### src\gui\ui_builders.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
    Create header section for GUI.

    Args:
        layout: Parent layout to add header to
      `
- Code: `def create_header(layout, theme, system_status_label_ref)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'layout'}

**Line 91** (high): docstring_param_mismatch
- Comment: `
    Create left panel with agent grid and controls.

    Args:
        theme: Theme manager for sty`
- Code: `def create_left_panel(theme, agent_widgets, callbacks)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'theme'}

**Line 171** (high): docstring_param_mismatch
- Comment: `
    Create right panel with status and logs.

    Args:
        status_panel_widget: StatusPanel wi`
- Code: `def create_right_panel(status_panel_widget)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'status_panel_widget'}

### src\infrastructure\browser\thea_browser_service.py

**Line 490** (high): comment_return_mismatch
- Comment: `Return highest scoring candidate`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\infrastructure\browser\unified\driver_manager.py

**Line 54** (high): docstring_param_mismatch
- Comment: `
        Initialize the driver manager with options.

        Args:
            driver_options: Opti`
- Code: `def __init__(self, driver_options)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'driver_options'}

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Download Chrome driver if not present.

        Returns:
            str: Path to Chrome dr`
- Code: `def _download_driver_if_needed(self)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises'}, extra={'self'}

**Line 95** (high): docstring_param_mismatch
- Comment: `
        Setup Chrome options based on configuration.

        Returns:
            ChromeOptions: C`
- Code: `def _setup_chrome_options(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 123** (high): docstring_param_mismatch
- Comment: `
        Get the Chrome WebDriver instance.

        Returns:
            Chrome: Undetected Chrome `
- Code: `def get_driver(self)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises'}, extra={'self'}

**Line 150** (high): docstring_param_mismatch
- Comment: `
        Close the Chrome WebDriver instance.

        Raises:
            Exception: If driver clea`
- Code: `def close_driver(self)`
- Issue: Docstring params don't match: missing={'Raises'}, extra={'self'}

**Line 165** (high): docstring_param_mismatch
- Comment: `
        Context manager entry.

        Returns:
            Chrome: WebDriver instance
        `
- Code: `def __enter__(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 174** (high): docstring_param_mismatch
- Comment: `
        Context manager exit - cleanup driver.

        Args:
            exc_type: Exception type `
- Code: `def __exit__(self, exc_type, exc_val, exc_tb)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'exc_type', 'self'}

### src\infrastructure\browser\unified_cookie_manager.py

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Initialize unified cookie manager.

        Args:
            cookie_file: Path to cookie f`
- Code: `def __init__(self, cookie_file, auto_save, enable_encryption, encryption_key)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'cookie_file'}

**Line 94** (high): docstring_param_mismatch
- Comment: `
        Save cookies for a specific service using BrowserAdapter.

        Args:
            browse`
- Code: `def save_cookies_for_service(self, browser_adapter, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'browser_adapter'}

**Line 124** (high): docstring_param_mismatch
- Comment: `
        Load cookies for a specific service using BrowserAdapter.

        Args:
            browse`
- Code: `def load_cookies_for_service(self, browser_adapter, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'browser_adapter'}

**Line 152** (high): docstring_param_mismatch
- Comment: `
        Check if there's a valid session for the service.

        Args:
            service_name: `
- Code: `def has_valid_session(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_name', 'self'}

**Line 168** (high): docstring_param_mismatch
- Comment: `
        Save cookies from Selenium WebDriver session.

        Args:
            driver: Selenium W`
- Code: `def save_cookies(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 196** (high): docstring_param_mismatch
- Comment: `
        Load cookies into Selenium WebDriver session.

        Auto-decrypts encrypted cookies if a`
- Code: `def load_cookies(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 236** (high): docstring_param_mismatch
- Comment: `
        Check if valid cookies exist (for WebDriver interface).

        Returns:
            True `
- Code: `def has_valid_cookies(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 256** (high): docstring_param_mismatch
- Comment: `
        Clear saved cookies.

        Args:
            service_name: Service identifier (None = cl`
- Code: `def clear_cookies(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_name', 'self'}

**Line 391** (high): docstring_param_mismatch
- Comment: `
        Generate a new Fernet encryption key.

        Returns:
            Base64-encoded encrypti`
- Code: `def generate_encryption_key()`
- Issue: Docstring params don't match: missing={'Returns', 'Raises'}, extra=set()

### src\infrastructure\dependency_injection.py

**Line 248** (high): docstring_param_mismatch
- Comment: `
    Get dependency injection container.

    Returns:
        Dictionary of dependencies
    `
- Code: `def get_dependencies()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 79** (high): comment_return_mismatch
- Comment: `Infrastructure repository returns persistence model objects`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\infrastructure\infrastructure_health_monitor.py

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Initialize health monitor.

        Args:
            warning_threshold: Percentage thresho`
- Code: `def __init__(self, warning_threshold, critical_threshold)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'warning_threshold'}

**Line 64** (high): docstring_param_mismatch
- Comment: `
        Check disk space for a given path.

        Args:
            path: Path to check (defaults`
- Code: `def check_disk_space(self, path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'path'}

**Line 165** (high): docstring_param_mismatch
- Comment: `
        Check if browser automation is ready.

        Returns:
            Dictionary with browser`
- Code: `def check_browser_automation_readiness(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 225** (high): docstring_param_mismatch
- Comment: `
        Perform a comprehensive health check.

        Returns:
            HealthCheckResult with `
- Code: `def perform_full_health_check(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\infrastructure\logging\std_logger.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
        Initialize the logger.

        Args:
            name: Logger name for identification
    `
- Code: `def __init__(self, name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'name'}

**Line 43** (high): docstring_param_mismatch
- Comment: `
        Log debug message.

        Args:
            message: Log message
            **context: A`
- Code: `def debug(self, message)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Log info message.

        Args:
            message: Log message
            **context: Ad`
- Code: `def info(self, message)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
        Log warning message.

        Args:
            message: Log message
            **context:`
- Code: `def warning(self, message)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 73** (high): docstring_param_mismatch
- Comment: `
        Log error message.

        Args:
            message: Log message
            exception: O`
- Code: `def error(self, message, exception)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 86** (high): docstring_param_mismatch
- Comment: `
        Log critical message.

        Args:
            message: Log message
            exception`
- Code: `def critical(self, message, exception)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'message', 'self'}

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Log message with specific level.

        Args:
            level: Log level
            me`
- Code: `def log(self, level, message, exception)`
- Issue: Docstring params don't match: missing={'context', 'Args'}, extra={'self', 'level'}

### src\infrastructure\persistence\base_file_repository.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Initialize file repository.
        
        Args:
            file_path: Path to JSON file`
- Code: `def __init__(self, file_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'file_path'}

**Line 55** (medium): docstring_return_mismatch
- Comment: `
        Get default data structure for new file.
        
        Returns:
            Dictionary w`
- Code: `def _get_default_data(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Get default data structure for new file.
        
        Returns:
            Dictionary w`
- Code: `def _get_default_data(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 65** (medium): docstring_return_mismatch
- Comment: `
        Get key for data array in JSON structure.
        
        Returns:
            Key name (e`
- Code: `def _get_data_key(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Get key for data array in JSON structure.
        
        Returns:
            Key name (e`
- Code: `def _get_data_key(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Load data from file.
        
        Returns:
            Data dictionary from file, or de`
- Code: `def _load_data(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 88** (high): docstring_param_mismatch
- Comment: `
        Save data to file.
        
        Args:
            data: Data dictionary to save
       `
- Code: `def _save_data(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Update metadata in data structure.
        
        Args:
            data: Data dictionary`
- Code: `def _update_metadata(self, data)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'data'}

**Line 121** (high): docstring_param_mismatch
- Comment: `
        Get items array from data structure.
        
        Args:
            data: Data dictiona`
- Code: `def _get_items(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 134** (high): docstring_param_mismatch
- Comment: `
        Set items array in data structure.
        
        Args:
            data: Data dictionary`
- Code: `def _set_items(self, data, items)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'data'}

**Line 145** (high): docstring_param_mismatch
- Comment: `
        Add item to repository.
        
        Args:
            item: Item dictionary to add
   `
- Code: `def _add_item(self, item)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'item'}

**Line 168** (high): docstring_param_mismatch
- Comment: `
        Find item matching predicate.
        
        Args:
            predicate: Function that t`
- Code: `def _find_item(self, predicate)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'predicate'}

**Line 184** (high): docstring_param_mismatch
- Comment: `
        Update item matching predicate.
        
        Args:
            predicate: Function that`
- Code: `def _update_item(self, predicate, updates)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'predicate'}

**Line 213** (high): docstring_param_mismatch
- Comment: `
        Delete item matching predicate.
        
        Args:
            predicate: Function that`
- Code: `def _delete_item(self, predicate)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'predicate'}

**Line 236** (high): docstring_param_mismatch
- Comment: `
        Filter items matching predicate.
        
        Args:
            predicate: Function tha`
- Code: `def _filter_items(self, predicate)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'predicate'}

**Line 249** (high): docstring_param_mismatch
- Comment: `
        Sort items by key.
        
        Args:
            items: List of items to sort
        `
- Code: `def _sort_items(self, items, key, reverse)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'items', 'self'}

**Line 263** (high): docstring_param_mismatch
- Comment: `
        Limit number of items.
        
        Args:
            items: List of items
            `
- Code: `def _limit_items(self, items, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'items', 'self'}

### src\infrastructure\persistence\sqlite_agent_repo.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Initialize the SQLite repository.

        Args:
            db_path: Path to the SQLite da`
- Code: `def __init__(self, db_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'db_path'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Retrieve an agent by its identifier.

        Args:
            agent_id: The unique identi`
- Code: `def get(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 90** (medium): docstring_return_mismatch
- Comment: `
        Retrieve agents that have a specific capability.

        Args:
            capability: The`
- Code: `def get_by_capability(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 90** (high): docstring_param_mismatch
- Comment: `
        Retrieve agents that have a specific capability.

        Args:
            capability: The`
- Code: `def get_by_capability(self, capability)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'capability'}

**Line 114** (medium): docstring_return_mismatch
- Comment: `
        Retrieve all active agents.

        Returns:
            Iterable of active agents
       `
- Code: `def get_active(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 114** (high): docstring_param_mismatch
- Comment: `
        Retrieve all active agents.

        Returns:
            Iterable of active agents
       `
- Code: `def get_active(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 135** (medium): docstring_return_mismatch
- Comment: `
        Retrieve agents that can accept more tasks.

        Returns:
            Iterable of avail`
- Code: `def get_available(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 135** (high): docstring_param_mismatch
- Comment: `
        Retrieve agents that can accept more tasks.

        Returns:
            Iterable of avail`
- Code: `def get_available(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 164** (high): docstring_param_mismatch
- Comment: `
        Add a new agent to the repository.

        Args:
            agent: The agent to add

    `
- Code: `def add(self, agent)`
- Issue: Docstring params don't match: missing={'Raises', 'Args'}, extra={'self', 'agent'}

**Line 189** (high): docstring_param_mismatch
- Comment: `
        Save an existing agent (create or update).

        Args:
            agent: The agent to s`
- Code: `def save(self, agent)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent'}

**Line 208** (high): docstring_param_mismatch
- Comment: `
        Delete an agent from the repository.

        Args:
            agent_id: The identifier of`
- Code: `def delete(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 223** (medium): docstring_return_mismatch
- Comment: `
        List all agents in the repository.

        Returns:
            Iterable of all agents
   `
- Code: `def list_all(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 223** (high): docstring_param_mismatch
- Comment: `
        List all agents in the repository.

        Returns:
            Iterable of all agents
   `
- Code: `def list_all(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\infrastructure\persistence\sqlite_task_repo.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Initialize the SQLite repository.

        Args:
            db_path: Path to the SQLite da`
- Code: `def __init__(self, db_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'db_path'}

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Retrieve a task by its identifier.

        Args:
            task_id: The unique identifie`
- Code: `def get(self, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

**Line 91** (medium): docstring_return_mismatch
- Comment: `
        Retrieve tasks assigned to a specific agent.

        Args:
            agent_id: The agent`
- Code: `def get_by_agent(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 91** (high): docstring_param_mismatch
- Comment: `
        Retrieve tasks assigned to a specific agent.

        Args:
            agent_id: The agent`
- Code: `def get_by_agent(self, agent_id, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 118** (medium): docstring_return_mismatch
- Comment: `
        Retrieve pending (unassigned) tasks.

        Args:
            limit: Maximum number of ta`
- Code: `def get_pending(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 118** (high): docstring_param_mismatch
- Comment: `
        Retrieve pending (unassigned) tasks.

        Args:
            limit: Maximum number of ta`
- Code: `def get_pending(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 144** (high): docstring_param_mismatch
- Comment: `
        Add a new task to the repository.

        Args:
            task: The task to add

       `
- Code: `def add(self, task)`
- Issue: Docstring params don't match: missing={'Raises', 'Args'}, extra={'self', 'task'}

**Line 169** (high): docstring_param_mismatch
- Comment: `
        Save an existing task (create or update).

        Args:
            task: The task to save`
- Code: `def save(self, task)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task'}

**Line 188** (high): docstring_param_mismatch
- Comment: `
        Delete a task from the repository.

        Args:
            task_id: The identifier of th`
- Code: `def delete(self, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

**Line 203** (medium): docstring_return_mismatch
- Comment: `
        List all tasks in the repository.

        Args:
            limit: Maximum number of tasks`
- Code: `def list_all(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 203** (high): docstring_param_mismatch
- Comment: `
        List all tasks in the repository.

        Args:
            limit: Maximum number of tasks`
- Code: `def list_all(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

### src\integrations\osrs\osrs_coordination_handlers.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Handle coordination message from another agent.

        Args:
            message: Coordin`
- Code: `def handle_coordination_message(self, message)`
- Issue: Docstring params don't match: missing={'Raises', 'Args'}, extra={'message', 'self'}

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Handle resource request from another agent.

        Args:
            message: Resource re`
- Code: `def handle_resource_request(self, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Handle activity coordination message.

        Args:
            message: Activity coordina`
- Code: `def handle_activity_coordination(self, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 139** (high): docstring_param_mismatch
- Comment: `
        Handle emergency alert from another agent.

        Args:
            message: Emergency al`
- Code: `def handle_emergency_alert(self, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 172** (high): docstring_param_mismatch
- Comment: `
        Handle status update from another agent.

        Args:
            message: Status update `
- Code: `def handle_status_update(self, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 199** (high): docstring_param_mismatch
- Comment: `
        Determine if this agent should participate in a coordinated activity.

        Args:
      `
- Code: `def should_participate_in_activity(self, activity)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'activity'}

**Line 259** (high): docstring_param_mismatch
- Comment: `
        Initiate emergency response procedure.

        Args:
            emergency_type: Type of e`
- Code: `def initiate_emergency_response(self, emergency_type, alerting_agent)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'emergency_type'}

### src\message_task\dedupe.py

**Line 17** (high): docstring_param_mismatch
- Comment: `
    Generate unique fingerprint for task deduplication.

    Uses SHA-1 hash of normalized task fie`
- Code: `def task_fingerprint(parsed_task_dict)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'parsed_task_dict'}

**Line 47** (high): docstring_param_mismatch
- Comment: `
    Normalize priority string to P0-P3 format.

    Args:
        priority: Raw priority string

  `
- Code: `def normalize_priority(priority)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'priority'}

**Line 76** (high): docstring_param_mismatch
- Comment: `
    Extract tags from text.

    Looks for #hashtags in text.

    Args:
        text: Text to extr`
- Code: `def extract_tags(text)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'text'}

### src\message_task\emitters.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
        Initialize emitter.

        Args:
            messaging_bus: Messaging system instance
   `
- Code: `def __init__(self, messaging_bus)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'messaging_bus'}

**Line 32** (high): docstring_param_mismatch
- Comment: `
        Emit message via messaging bus.

        Args:
            content: Message content
       `
- Code: `def emit(self, content, recipient, priority)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'content'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
    Notify on task state change.

    Args:
        task: Task object
        transition: State tra`
- Code: `def on_task_state_change(task, transition, bus)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'task'}

**Line 113** (high): docstring_param_mismatch
- Comment: `
    Send task completion report.

    Args:
        task: Task object
        result: Completion re`
- Code: `def send_completion_report(task, result, agent_id, bus)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'task'}

**Line 154** (high): docstring_param_mismatch
- Comment: `
    Send acknowledgment that task was created from message.

    Args:
        task_id: Created tas`
- Code: `def send_task_created_ack(task_id, title, msg_id, bus)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'task_id'}

### src\message_task\fsm_bridge.py

**Line 75** (high): docstring_param_mismatch
- Comment: `
    Check if transition is valid.

    Args:
        from_state: Current state
        to_state: Ta`
- Code: `def can_transition(from_state, to_state)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'from_state'}

**Line 100** (high): docstring_param_mismatch
- Comment: `
    Get event for state transition.

    Args:
        from_state: Current state
        to_state: `
- Code: `def get_transition_event(from_state, to_state)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'from_state'}

### src\message_task\ingestion_pipeline.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Initialize pipeline.

        Args:
            task_repository: SqliteTaskRepository insta`
- Code: `def __init__(self, task_repository, messaging_bus)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'task_repository', 'self'}

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Process inbound message.

        Args:
            msg: Inbound message

        Returns:
`
- Code: `def process(self, msg)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'msg'}

**Line 69** (high): docstring_param_mismatch
- Comment: `
    Handle inbound message (convenience function).

    Args:
        msg: Inbound message
        `
- Code: `def handle_inbound(msg, repo, bus)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'msg'}

### src\message_task\messaging_integration.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
    Process message and potentially create task.

    Args:
        message_id: Message ID
        `
- Code: `def process_message_for_task(message_id, content, author, channel)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message_id'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
    Determine if message should create a task.

    Args:
        content: Message content

    Ret`
- Code: `def should_create_task_from_message(content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'content'}

### src\message_task\parsers\ai_parser.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
        Parse message using AI/heuristics.

        This is a lightweight implementation. Can be en`
- Code: `def parse(content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'content'}

### src\message_task\parsers\fallback_regex.py

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Parse using fallback regex patterns.

        This is the safety net - should almost always`
- Code: `def parse(content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'content'}

### src\message_task\parsers\structured_parser.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Parse structured message format.

        Args:
            content: Message content

     `
- Code: `def parse(content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'content'}

### src\message_task\router.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Initialize router.

        Args:
            task_repository: SqliteTaskRepository instanc`
- Code: `def __init__(self, task_repository)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'task_repository', 'self'}

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Parse message using 3-tier cascade.

        Args:
            msg: Inbound message

      `
- Code: `def parse(self, msg)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'msg'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Ingest message and create task.

        Args:
            msg: Inbound message

        Re`
- Code: `def ingest(self, msg)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'msg'}

### src\obs\caption_listener.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Initialize OBS caption listener.

        Args:
            host: OBS WebSocket host (defau`
- Code: `def __init__(self, host, port, password, on_caption)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'host'}

**Line 160** (high): docstring_param_mismatch
- Comment: `
        Check if message is a caption event.

        Args:
            data: Parsed JSON data

   `
- Code: `def _is_caption_event(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 178** (high): docstring_param_mismatch
- Comment: `
        Extract caption data from event.

        Args:
            data: Event data

        Retur`
- Code: `def _extract_caption(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 273** (high): docstring_param_mismatch
- Comment: `
        Initialize file-based caption listener.

        Args:
            caption_file_path: Path `
- Code: `def __init__(self, caption_file_path, on_caption, poll_interval)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'caption_file_path'}

### src\obs\metrics.py

**Line 18** (high): docstring_param_mismatch
- Comment: `
    Increment metric counter.

    Args:
        key: Metric key (e.g., "ingest.ok", "msg.sent")
  `
- Code: `def incr(key, n)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'key'}

**Line 54** (high): docstring_param_mismatch
- Comment: `
    Dump metrics as formatted string.

    Returns:
        Formatted metrics output
    `
- Code: `def dump_metrics()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### src\obs\speech_log_manager.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Initialize speech log manager.

        Args:
            devlogs_path: Path to devlogs dir`
- Code: `def __init__(self, devlogs_path, memory_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'devlogs_path'}

**Line 51** (high): docstring_param_mismatch
- Comment: `
        Log caption to specified destination.

        Args:
            caption_text: Caption text`
- Code: `def log_caption(self, caption_text, interpreted, destination)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'caption_text', 'self'}

**Line 78** (high): docstring_param_mismatch
- Comment: `
        Log caption to devlog file.

        Args:
            caption_text: Caption text
         `
- Code: `def _log_to_devlog(self, caption_text, interpreted)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'caption_text', 'self'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Format devlog entry for caption.

        Args:
            caption_text: Caption text
    `
- Code: `def _format_devlog(self, caption_text, interpreted)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'caption_text', 'self'}

**Line 143** (high): docstring_param_mismatch
- Comment: `
        Log caption to memory/knowledge base.

        Args:
            caption_text: Caption text`
- Code: `def _log_to_memory(self, caption_text, interpreted)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'caption_text', 'self'}

**Line 191** (high): docstring_param_mismatch
- Comment: `
        Get recent caption entries from memory.

        Args:
            limit: Number of entries`
- Code: `def get_recent_captions(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

### src\opensource\contribution_tracker.py

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Initialize contribution tracker.

        Args:
            portfolio_file: Path to portfol`
- Code: `def __init__(self, portfolio_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'portfolio_file'}

**Line 87** (high): docstring_param_mismatch
- Comment: `
        Log a contribution.

        Args:
            project_name: Project name
            contr`
- Code: `def log_contribution(self, project_name, contribution_type, description, agents, pr_url, status)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'project_name', 'self'}

### src\opensource\github_integration.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
        Initialize GitHub integration.

        Args:
            token: GitHub personal access tok`
- Code: `def __init__(self, token)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'token', 'self'}

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Fetch issues from GitHub repository.

        Args:
            repo_url: Repository URL
  `
- Code: `def fetch_issues(self, repo_url, labels, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_url'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Create new branch for contribution.

        Args:
            project_path: Path to projec`
- Code: `def create_branch(self, project_path, branch_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'project_path'}

**Line 104** (high): docstring_param_mismatch
- Comment: `
        Commit changes with swarm signature.

        Args:
            project_path: Path to proje`
- Code: `def commit_changes(self, project_path, message, agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'project_path'}

**Line 142** (high): docstring_param_mismatch
- Comment: `
        Push branch to origin.

        Args:
            project_path: Path to project
           `
- Code: `def push_branch(self, project_path, branch_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'project_path'}

**Line 172** (high): docstring_param_mismatch
- Comment: `
        Create pull request via GitHub CLI.

        Args:
            project_path: Path to projec`
- Code: `def create_pr(self, project_path, title, description, agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'project_path'}

### src\opensource\portfolio_builder.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
        Initialize portfolio builder.

        Args:
            contribution_tracker: Contribution`
- Code: `def __init__(self, contribution_tracker)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'contribution_tracker', 'self'}

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Generate portfolio README.

        Args:
            output_path: Output file path
       `
- Code: `def generate_readme(self, output_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'output_path', 'self'}

**Line 127** (high): docstring_param_mismatch
- Comment: `
        Generate HTML portfolio dashboard.

        Args:
            output_path: Output file path`
- Code: `def generate_dashboard_html(self, output_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'output_path', 'self'}

**Line 229** (high): docstring_param_mismatch
- Comment: `
        Export portfolio as JSON.

        Args:
            output_path: Output file path
        `
- Code: `def export_portfolio_json(self, output_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'output_path', 'self'}

### src\opensource\project_manager.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
        Initialize project manager.

        Args:
            projects_root: Root directory for ex`
- Code: `def __init__(self, projects_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'projects_root'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Clone external open source project.

        Args:
            github_url: GitHub repositor`
- Code: `def clone_project(self, github_url, project_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'github_url'}

**Line 198** (high): docstring_param_mismatch
- Comment: `
        Add contribution record.

        Args:
            project_id: Project ID
            cont`
- Code: `def add_contribution(self, project_id, contribution_type, description, agents)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'project_id'}

### src\opensource\task_integration.py

**Line 20** (high): docstring_param_mismatch
- Comment: `
        Initialize task integration.

        Args:
            project_manager: OpenSourceProjectM`
- Code: `def __init__(self, project_manager, task_repository)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'project_manager'}

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Create task from GitHub issue.

        Args:
            project_id: OSS project ID
      `
- Code: `def create_task_from_issue(self, project_id, issue_number, issue_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'project_id'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Import multiple issues as tasks.

        Args:
            project_id: OSS project ID
    `
- Code: `def bulk_import_issues(self, project_id, issues, max_tasks)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'project_id'}

### src\orchestrators\overnight\enhanced_agent_activity_detector.py

**Line 44** (high): docstring_param_mismatch
- Comment: `
        Detect all activity indicators for an agent.

        Returns dict with:
        - latest_a`
- Code: `def detect_agent_activity(self, agent_id)`
- Issue: Docstring params don't match: missing={'latest_activity', 'activity_details', 'activity_sources'}, extra={'self', 'agent_id'}

### src\orchestrators\overnight\fsm_updates_processor.py

**Line 43** (high): docstring_param_mismatch
- Comment: `
    Process a single FSM update JSON file.
    
    Args:
        filepath: Path to FSM update JSON`
- Code: `def process_fsm_update_file(filepath)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'filepath'}

**Line 97** (high): docstring_param_mismatch
- Comment: `
    Process all FSM update files in a directory.
    
    Args:
        updates_dir: Directory cont`
- Code: `def process_fsm_updates_directory(updates_dir, target_agent)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'updates_dir'}

**Line 134** (high): docstring_param_mismatch
- Comment: `
    Migrate FSM updates from V1 to V2 format.
    
    Args:
        v1_updates_dir: V1 FSM_UPDATES`
- Code: `def migrate_v1_fsm_updates(v1_updates_dir, v2_fsm_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'v1_updates_dir'}

### src\orchestrators\overnight\inbox_consumer.py

**Line 87** (high): docstring_param_mismatch
- Comment: `
    Process all files in the inbox directory.
    
    Args:
        agent_id: Agent ID to process `
- Code: `def process_inbox(agent_id, outbox_root)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 132** (high): docstring_param_mismatch
- Comment: `
    Continuously process inbox files.
    
    Args:
        agent_id: Agent ID to process inbox fo`
- Code: `def process_inbox_continuous(agent_id, poll_interval, max_iterations)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'agent_id'}

### src\orchestrators\overnight\integration_example.py

**Line 39** (high): docstring_param_mismatch
- Comment: `Example: Using message plans.`
- Code: `def example_message_plans()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

**Line 61** (high): docstring_param_mismatch
- Comment: `Example: Using FSM bridge.`
- Code: `def example_fsm_bridge()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

**Line 90** (high): docstring_param_mismatch
- Comment: `Example: Using inbox consumer.`
- Code: `def example_inbox_consumer()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

**Line 116** (high): docstring_param_mismatch
- Comment: `Example: Using listener.`
- Code: `def example_listener()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

**Line 140** (high): docstring_param_mismatch
- Comment: `Example: Processing V1 FSM updates.`
- Code: `def example_fsm_updates_processor()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

**Line 154** (high): docstring_param_mismatch
- Comment: `Example: Integrated workflow using all components.`
- Code: `def example_integrated_workflow()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

### src\orchestrators\overnight\message_plans.py

**Line 56** (high): docstring_param_mismatch
- Comment: `
    Build message plan based on strategy.
    
    Args:
        plan: Plan name (contracts, autono`
- Code: `def build_message_plan(plan, repos_root)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'plan'}

**Line 289** (high): docstring_param_mismatch
- Comment: `
    Format a planned message with agent name and optional variables.
    
    Args:
        planned`
- Code: `def format_message(planned, agent)`
- Issue: Docstring params don't match: missing={'Returns', 'kwargs', 'Args'}, extra={'planned'}

### src\orchestrators\overnight\monitor.py

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Initialize progress monitor.

        Args:
            config: Configuration dictionary (u`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 187** (high): docstring_param_mismatch
- Comment: `Update agent activity timestamp when meaningful progress is detected.

        This method should be`
- Code: `def update_agent_activity_on_progress(self, agent_id, event)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 355** (high): docstring_param_mismatch
- Comment: `Determine if agent is stalled with progressive timeout system.

        Returns dict with:
        -`
- Code: `def _determine_stall_status(self, agent_id, latest_activity, confidence, activity_sources, current_time)`
- Issue: Docstring params don't match: missing={'is_stalled', 'severity', 'reason'}, extra={'confidence', 'activity_sources', 'self', 'latest_activity', 'agent_id', 'current_time'}

### src\orchestrators\overnight\monitor_discord_alerts.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
    Get Discord webhook URL for an agent.
    
    Args:
        agent_id: Agent identifier (e.g., `
- Code: `def get_agent_webhook(agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 54** (high): docstring_param_mismatch
- Comment: `
    Send Discord alert for stalled agent.
    
    Args:
        agent_id: Agent identifier
       `
- Code: `def send_stall_alert(agent_id, stall_duration_seconds, activity_details)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
    Send Discord alert for recovery action.
    
    Args:
        agent_id: Agent identifier
     `
- Code: `def send_recovery_alert(agent_id, recovery_status, details)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 164** (high): docstring_param_mismatch
- Comment: `
    Send Discord alert for system health issues.
    
    Args:
        issues: List of health issu`
- Code: `def send_health_alert(issues, health_status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'issues'}

### src\orchestrators\overnight\orchestrator.py

**Line 84** (high): docstring_param_mismatch
- Comment: `
        Initialize overnight orchestrator.
        
        Args:
            config: Configuration`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

### src\orchestrators\overnight\recovery.py

**Line 49** (high): docstring_param_mismatch
- Comment: `
        Initialize recovery system.

        Args:
            config: Configuration dictionary (us`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

### src\orchestrators\overnight\scheduler.py

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Initialize task scheduler.

        Args:
            config: Configuration dictionary (use`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 116** (high): docstring_param_mismatch
- Comment: `
        Add a task to the scheduler.

        Args:
            task_id: Unique task identifier
   `
- Code: `def add_task(self, task_id, task_type, agent_id, data, priority, scheduled_cycle, dependencies, estimated_duration)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

### src\orchestrators\overnight\scheduler_integration.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Initialize integration.
        
        Args:
            scheduler: TaskScheduler instanc`
- Code: `def __init__(self, scheduler, status_monitor)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'scheduler', 'self'}

**Line 62** (high): docstring_param_mismatch
- Comment: `
        Notify status monitor about pending scheduled task.
        
        Args:
            agen`
- Code: `def notify_pending_task(self, agent_id, task_id, task_type, priority, scheduled_cycle)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 96** (high): docstring_param_mismatch
- Comment: `
        Get all pending tasks for an agent from scheduler.
        
        Args:
            agent`
- Code: `def get_pending_tasks_for_agent(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 137** (high): docstring_param_mismatch
- Comment: `
        Mark agent as inactive in scheduler.
        
        Args:
            agent_id: Agent ide`
- Code: `def mark_agent_inactive(self, agent_id, inactivity_duration_minutes)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 168** (high): docstring_param_mismatch
- Comment: `
        Format scheduled tasks for inclusion in resume prompt.
        
        Args:
            a`
- Code: `def format_scheduled_tasks_for_prompt(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 200** (high): docstring_param_mismatch
- Comment: `
        Get integration status.
        
        Returns:
            Status dictionary
        `
- Code: `def get_integration_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\orchestrators\overnight\scheduler_queue.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
        Initialize scheduler queue.

        Args:
            completed_tasks: Set of completed ta`
- Code: `def __init__(self, completed_tasks, failed_tasks, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'completed_tasks'}

**Line 45** (high): docstring_param_mismatch
- Comment: `
        Get tasks available for execution in this cycle.

        Args:
            cycle_number: C`
- Code: `def get_available_tasks(self, cycle_number)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'cycle_number'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Check if a task is ready for execution.

        Args:
            task: Task to check
    `
- Code: `def is_task_ready(self, task, cycle_number)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 101** (high): docstring_param_mismatch
- Comment: `
        Remove task from priority queue.

        Args:
            task_id: ID of task to remove
 `
- Code: `def remove_task(self, task_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_id'}

**Line 119** (high): docstring_param_mismatch
- Comment: `
        Balance task load across agents.

        Args:
            tasks: Tasks to balance
       `
- Code: `def balance_agent_load(self, tasks, agent_load)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'tasks'}

### src\orchestrators\overnight\scheduler_refactored.py

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Initialize task scheduler.

        Args:
            config: Configuration dictionary (use`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 116** (high): docstring_param_mismatch
- Comment: `
        Add a task to the scheduler.

        Args:
            task_id: Unique task identifier
   `
- Code: `def add_task(self, task_id, task_type, agent_id, data, priority, scheduled_cycle, dependencies, estimated_duration)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task_id'}

### src\orchestrators\overnight\scheduler_tracking.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
        Initialize scheduler tracking.

        Args:
            task_registry: Dictionary of task`
- Code: `def __init__(self, task_registry, completed_tasks, failed_tasks, agent_load, current_cycle, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'task_registry', 'self'}

**Line 48** (high): docstring_param_mismatch
- Comment: `
        Mark a task as completed.

        Args:
            task_id: ID of completed task
        `
- Code: `def mark_task_completed(self, task_id, remove_from_queue_fn)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_id'}

**Line 70** (high): docstring_param_mismatch
- Comment: `
        Mark a task as failed and optionally retry.

        Args:
            task_id: ID of faile`
- Code: `def mark_task_failed(self, task_id, retry, add_to_queue_fn, remove_from_queue_fn)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'task_id'}

**Line 109** (high): docstring_param_mismatch
- Comment: `
        Update agent load.

        Args:
            agent_id: Agent ID
            duration: Dura`
- Code: `def update_agent_load(self, agent_id, duration)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

### src\repositories\activity_repository.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Initialize activity repository.

        Args:
            activity_history_file: Path to a`
- Code: `def __init__(self, activity_history_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'activity_history_file'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Save activity state change to history.

        Args:
            agent_id: Agent identifie`
- Code: `def save_activity_change(self, agent_id, state, message_id, queue_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        Get activity history, optionally filtered by agent.

        Args:
            agent_id: Op`
- Code: `def get_activity_history(self, agent_id, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 134** (high): docstring_param_mismatch
- Comment: `
        Get activity summary for agent.

        Args:
            agent_id: Agent identifier
     `
- Code: `def get_agent_activity_summary(self, agent_id, hours)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\repositories\agent_repository.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Initialize agent repository.

        Args:
            workspace_root: Root directory for `
- Code: `def __init__(self, workspace_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'workspace_root'}

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Get agent data by ID.

        Args:
            agent_id: Agent identifier (e.g., "Agent-7`
- Code: `def get_agent(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
        Get all agents from workspace.

        Returns:
            List of agent data dictionarie`
- Code: `def get_all_agents(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 83** (high): docstring_param_mismatch
- Comment: `
        Update agent status file.

        Args:
            agent_id: Agent identifier (e.g., "Age`
- Code: `def update_agent_status(self, agent_id, status_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 107** (high): docstring_param_mismatch
- Comment: `
        Get agent inbox messages.

        Args:
            agent_id: Agent identifier (e.g., "Age`
- Code: `def get_agent_inbox(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 137** (high): docstring_param_mismatch
- Comment: `
        Get agent workspace directory path.

        Args:
            agent_id: Agent identifier (`
- Code: `def get_agent_workspace_path(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 149** (high): docstring_param_mismatch
- Comment: `
        Check if agent workspace exists.

        Args:
            agent_id: Agent identifier (e.g`
- Code: `def agent_exists(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 161** (high): docstring_param_mismatch
- Comment: `
        Get agent notes from workspace.

        Args:
            agent_id: Agent identifier (e.g.`
- Code: `def get_agent_notes(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\repositories\contract_repository.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
        Initialize contract repository.

        Args:
            contracts_file: Path to contract`
- Code: `def __init__(self, contracts_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'contracts_file'}

**Line 50** (high): docstring_param_mismatch
- Comment: `
        Load contracts from file.

        Returns:
            Contracts data dictionary
        `
- Code: `def _load_contracts(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
        Save contracts to file.

        Args:
            data: Contracts data dictionary

       `
- Code: `def _save_contracts(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Get contract by ID.

        Args:
            contract_id: Contract identifier

        Re`
- Code: `def get_contract(self, contract_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'contract_id', 'self'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Get all contracts.

        Returns:
            List of all contract data dictionaries
   `
- Code: `def get_all_contracts(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        Get available contracts (unclaimed or for specific agent).

        Args:
            agent`
- Code: `def get_available_contracts(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 132** (high): docstring_param_mismatch
- Comment: `
        Claim contract for agent.

        Args:
            contract_id: Contract identifier
     `
- Code: `def claim_contract(self, contract_id, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'contract_id', 'self'}

**Line 155** (high): docstring_param_mismatch
- Comment: `
        Mark contract as completed.

        Args:
            contract_id: Contract identifier

  `
- Code: `def complete_contract(self, contract_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'contract_id', 'self'}

**Line 176** (high): docstring_param_mismatch
- Comment: `
        Add new contract to storage.

        Args:
            contract_data: Contract data dictio`
- Code: `def add_contract(self, contract_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'contract_data', 'self'}

**Line 198** (high): docstring_param_mismatch
- Comment: `
        Get all contracts assigned to specific agent.

        Args:
            agent_id: Agent id`
- Code: `def get_contracts_by_agent(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 215** (high): docstring_param_mismatch
- Comment: `
        Update contract status.

        Args:
            contract_id: Contract identifier
       `
- Code: `def update_contract_status(self, contract_id, status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'contract_id', 'self'}

### src\repositories\message_repository.py

**Line 44** (high): docstring_param_mismatch
- Comment: `
        Initialize message repository.

        Args:
            message_history_file: Path to mes`
- Code: `def __init__(self, message_history_file, inbox_root, metrics_engine)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'message_history_file'}

**Line 76** (high): docstring_param_mismatch
- Comment: `
        Load message history from file.

        Returns:
            Message history data dictiona`
- Code: `def _load_history(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Save message history to file.

        Args:
            data: Message history data diction`
- Code: `def _save_history(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 106** (high): docstring_param_mismatch
- Comment: `
        Save message to storage.

        Args:
            message: Message data dictionary

     `
- Code: `def save_message(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 163** (high): docstring_param_mismatch
- Comment: `
        Get message history, optionally filtered by agent.

        Args:
            agent_id: Opt`
- Code: `def get_message_history(self, agent_id, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 192** (high): docstring_param_mismatch
- Comment: `
        Get recent messages across all agents.

        Args:
            limit: Maximum number of `
- Code: `def get_recent_messages(self, limit)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'limit'}

**Line 204** (high): docstring_param_mismatch
- Comment: `
        Get all messages from specific sender.

        Args:
            sender_id: Sender identif`
- Code: `def get_messages_by_sender(self, sender_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'sender_id'}

**Line 223** (high): docstring_param_mismatch
- Comment: `
        Get all messages to specific recipient.

        Args:
            recipient_id: Recipient `
- Code: `def get_messages_by_recipient(self, recipient_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'recipient_id'}

**Line 242** (high): docstring_param_mismatch
- Comment: `
        Get inbox messages for specific agent from file system.

        Args:
            agent_id`
- Code: `def get_inbox_messages(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 272** (high): docstring_param_mismatch
- Comment: `
        Get message count, optionally filtered by agent.

        Args:
            agent_id: Optio`
- Code: `def get_message_count(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 285** (high): docstring_param_mismatch
- Comment: `
        Clear messages older than specified days.

        Args:
            days: Number of days t`
- Code: `def clear_old_messages(self, days)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'days'}

**Line 318** (high): docstring_param_mismatch
- Comment: `
        Compress messages older than specified days using Agent-3's compression tools.

        Arg`
- Code: `def compress_old_messages(self, days, compression_level)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'days'}

**Line 376** (high): docstring_param_mismatch
- Comment: `
        Get compression statistics using Agent-3's health check tool.

        Returns:
           `
- Code: `def get_compression_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\repositories\metrics_repository.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Initialize metrics repository.

        Args:
            metrics_history_file: Path to met`
- Code: `def __init__(self, metrics_history_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'metrics_history_file'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Save metrics snapshot to history.

        Args:
            metrics: Metrics dictionary fr`
- Code: `def save_metrics_snapshot(self, metrics, source)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'metrics'}

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Get metrics history, optionally filtered by source.

        Args:
            source: Opti`
- Code: `def get_metrics_history(self, source, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'source'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Get trend data for specific metric.

        Args:
            metric_name: Name of metric `
- Code: `def get_metrics_trend(self, metric_name, source, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'metric_name'}

### src\services\agent_vector_utils.py

**Line 11** (high): docstring_param_mismatch
- Comment: `
    Format a vector search result for display.

    Args:
        result: Search result object

   `
- Code: `def format_search_result(result)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'result'}

**Line 34** (high): docstring_param_mismatch
- Comment: `
    Generate recommendations based on search results.

    Args:
        results: List of search re`
- Code: `def generate_recommendations(results)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'results'}

### src\services\ai_service.py

**Line 69** (high): docstring_param_mismatch
- Comment: `
        Process a message and generate AI response.
        
        Args:
            message: Use`
- Code: `def process_message(self, message, user_id, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 120** (high): docstring_param_mismatch
- Comment: `
        Start a new conversation.
        
        Args:
            user_id: User identifier
     `
- Code: `def start_conversation(self, user_id, initial_message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'user_id'}

**Line 155** (high): docstring_param_mismatch
- Comment: `
        Continue an existing conversation.
        
        Args:
            conversation_id: Conv`
- Code: `def continue_conversation(self, conversation_id, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 172** (high): docstring_param_mismatch
- Comment: `
        Process multimodal content (text + media).
        
        Args:
            text: Text co`
- Code: `def process_multimodal(self, text, media)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'text'}

**Line 194** (high): docstring_param_mismatch
- Comment: `
        Get conversation history.
        
        Args:
            conversation_id: Conversation `
- Code: `def get_conversation_history(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 221** (high): docstring_param_mismatch
- Comment: `
        Get conversation context.
        
        Args:
            conversation_id: Conversation `
- Code: `def get_context(self, conversation_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conversation_id'}

**Line 247** (high): docstring_param_mismatch
- Comment: `
        Generate AI response.
        
        Args:
            message: User message
            `
- Code: `def _generate_response(self, message, conversation)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 278** (high): docstring_param_mismatch
- Comment: `
        Get relevant context for message processing.
        
        Args:
            message: Us`
- Code: `def _get_relevant_context(self, message, conversation)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

### src\services\chat_presence\agent_personality.py

**Line 156** (high): docstring_param_mismatch
- Comment: `
    Get personality profile for an agent.

    Args:
        agent_id: Agent identifier (e.g., "Age`
- Code: `def get_personality(agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 169** (high): docstring_param_mismatch
- Comment: `
    Format a message with agent personality applied.

    Args:
        agent_id: Agent identifier
`
- Code: `def format_chat_message(agent_id, base_message, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 223** (high): docstring_param_mismatch
- Comment: `
    Determine if an agent should respond to a message based on personality.

    Args:
        agen`
- Code: `def should_agent_respond(agent_id, message_content)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### src\services\chat_presence\chat_presence_orchestrator.py

**Line 81** (high): docstring_param_mismatch
- Comment: `
        Initialize chat presence orchestrator.

        Args:
            twitch_config: Twitch con`
- Code: `def __init__(self, twitch_config, obs_config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'twitch_config'}

**Line 635** (high): docstring_param_mismatch
- Comment: `
        Check if user is an admin.

        Args:
            username: Twitch username (lowercase)`
- Code: `def _is_admin_user(self, username, tags)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'username'}

### src\services\chat_presence\chat_scheduler.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Initialize chat scheduler.

        Args:
            cooldown_seconds: Minimum seconds bet`
- Code: `def __init__(self, cooldown_seconds)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'cooldown_seconds'}

**Line 44** (high): docstring_param_mismatch
- Comment: `
        Check if agent can speak (cooldown check).

        Args:
            agent_id: Agent ident`
- Code: `def can_agent_speak(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Record that an agent has responded.

        Args:
            agent_id: Agent identifier
 `
- Code: `def record_agent_response(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 84** (high): docstring_param_mismatch
- Comment: `
        Get least active agent from candidates.

        Args:
            candidate_agents: List o`
- Code: `def get_least_active_agent(self, candidate_agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'candidate_agents'}

**Line 109** (high): docstring_param_mismatch
- Comment: `
        Get activity statistics for all agents.

        Returns:
            Dictionary of agent a`
- Code: `def get_agent_activity_stats(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 139** (high): docstring_param_mismatch
- Comment: `
        Select agent with rotation fairness applied.

        Args:
            suggested_agent: In`
- Code: `def select_agent_with_rotation(self, suggested_agent, all_candidates)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'suggested_agent'}

**Line 168** (high): docstring_param_mismatch
- Comment: `
        Reset activity tracking.

        Args:
            agent_id: Specific agent to reset, or N`
- Code: `def reset_activity(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

### src\services\chat_presence\message_interpreter.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Determine which agent should respond.

        Args:
            message: Chat message cont`
- Code: `def determine_responder(self, message, username, channel)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 70** (high): docstring_param_mismatch
- Comment: `
        Check for explicit agent commands.

        Args:
            message: Message content

   `
- Code: `def _check_explicit_command(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 122** (high): docstring_param_mismatch
- Comment: `
        Check if message is a status command.

        Args:
            message: Message content

`
- Code: `def is_status_command(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 136** (high): docstring_param_mismatch
- Comment: `
        Parse status command to determine what status to show.

        Args:
            message: `
- Code: `def parse_status_command(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'agent_id', 'Args'}, extra={'message', 'self'}

**Line 193** (high): docstring_param_mismatch
- Comment: `
        Check if message is a broadcast command.

        Args:
            message: Message conten`
- Code: `def _is_broadcast_command(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 208** (high): docstring_param_mismatch
- Comment: `
        Find best matching agent by content analysis.

        Args:
            message: Message c`
- Code: `def _find_best_agent_match(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 246** (high): docstring_param_mismatch
- Comment: `
        Calculate match score for agent and message.

        Args:
            agent_id: Agent ide`
- Code: `def _calculate_match_score(self, agent_id, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 284** (high): docstring_param_mismatch
- Comment: `
        Apply activity rotation for fair speaking time.

        Args:
            suggested_agent:`
- Code: `def _apply_activity_rotation(self, suggested_agent, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'suggested_agent'}

**Line 307** (high): docstring_param_mismatch
- Comment: `
        Determine if system should respond at all.

        Args:
            message: Message cont`
- Code: `def should_respond(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 333** (high): docstring_param_mismatch
- Comment: `
        Determine how many messages to send.

        Args:
            message: Message content

 `
- Code: `def get_response_count(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

### src\services\chat_presence\status_reader.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Initialize status reader.
        
        Args:
            workspace_root: Root path to a`
- Code: `def __init__(self, workspace_root)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'workspace_root'}

**Line 44** (high): docstring_param_mismatch
- Comment: `
        Get status for a specific agent.
        
        Args:
            agent_id: Agent identif`
- Code: `def get_agent_status(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Get status for all agents.
        
        Returns:
            Dictionary mapping agent_i`
- Code: `def get_all_agents_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 84** (high): docstring_param_mismatch
- Comment: `
        Format agent status for chat display.
        
        Args:
            agent_id: Agent id`
- Code: `def format_agent_status(self, agent_id, status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 133** (high): docstring_param_mismatch
- Comment: `
        Format summary of all agents for chat display.
        
        Returns:
            Format`
- Code: `def format_all_agents_summary(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 167** (high): docstring_param_mismatch
- Comment: `
        Format compact single-line status for chat.
        
        Args:
            agent_id: Ag`
- Code: `def format_agent_status_compact(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\services\chat_presence\twitch_bridge.py

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Initialize Twitch chat bridge.

        Args:
            username: Twitch bot username
   `
- Code: `def __init__(self, username, oauth_token, channel, on_message)`
- Issue: Docstring params don't match: missing={'oauth', 'Args'}, extra={'self', 'username'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Mask OAuth token for safe logging.
        
        Args:
            tok: OAuth token stri`
- Code: `def _mask_token(tok)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'tok'}

**Line 301** (high): docstring_param_mismatch
- Comment: `
        Handle incoming chat message.

        Args:
            message_data: Message data diction`
- Code: `def _handle_message(self, message_data)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message_data', 'self'}

**Line 466** (high): docstring_param_mismatch
- Comment: `
        Initialize Twitch IRC bot.

        Args:
            server_list: List of (host, port) tup`
- Code: `def __init__(self, server_list, nickname, realname, channel, on_message, bridge_instance, oauth_token)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'server_list'}

**Line 510** (high): docstring_param_mismatch
- Comment: `
        Mask OAuth token for safe logging.
        
        Args:
            tok: OAuth token stri`
- Code: `def _mask_token(tok)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'tok'}

**Line 526** (high): docstring_param_mismatch
- Comment: `
        Override connection method to ensure password is set BEFORE connecting.
        
        CR`
- Code: `def _connect(self)`
- Issue: Docstring params don't match: missing={'CRITICAL'}, extra={'self'}

**Line 579** (high): docstring_param_mismatch
- Comment: `
        Handle PING messages from Twitch IRC server.
        
        CRITICAL: Twitch sends PING e`
- Code: `def on_ping(self, connection, event)`
- Issue: Docstring params don't match: missing={'CRITICAL'}, extra={'self', 'connection', 'event'}

**Line 817** (high): docstring_param_mismatch
- Comment: `
        Called when public message received.

        Args:
            connection: IRC connection
`
- Code: `def on_pubmsg(self, connection, event)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'connection'}

**Line 872** (high): docstring_param_mismatch
- Comment: `
        Called when private message received.

        Args:
            connection: IRC connection`
- Code: `def on_privmsg(self, connection, event)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'connection'}

**Line 911** (high): docstring_param_mismatch
- Comment: `
        Initialize WebSocket bridge.

        Args:
            client_id: Twitch API client ID
   `
- Code: `def __init__(self, client_id, access_token, channel_id, on_message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'client_id', 'self'}

**Line 666** (high): comment_return_mismatch
- Comment: `This ensures bot.start() returns so the reconnect loop can create a new bot`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\services\chatgpt\extractor.py

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Initialize conversation extractor.

        Args:
            config: Configuration diction`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 133** (high): docstring_param_mismatch
- Comment: `
        Save conversation to file.

        Args:
            conversation: Conversation data to sa`
- Code: `def save_conversation(self, conversation, filename)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'conversation', 'self'}

**Line 148** (high): docstring_param_mismatch
- Comment: `
        Load conversation from file.

        Args:
            filename: Filename to load

       `
- Code: `def load_conversation(self, filename)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'filename', 'self'}

**Line 160** (high): docstring_param_mismatch
- Comment: `
        List all saved conversations.

        Returns:
            List of conversation metadata
 `
- Code: `def list_conversations(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 169** (high): docstring_param_mismatch
- Comment: `
        Clean up old conversation files.

        Args:
            max_age_days: Maximum age of fi`
- Code: `def cleanup_old_conversations(self, max_age_days)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'max_age_days'}

### src\services\chatgpt\extractor_message_parser.py

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Initialize message parser.

        Args:
            message_selector: CSS selector for me`
- Code: `def __init__(self, message_selector, text_selector, timestamp_selector, max_messages, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'message_selector'}

### src\services\chatgpt\extractor_storage.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
        Initialize conversation storage.

        Args:
            storage_dir: Directory for stor`
- Code: `def __init__(self, storage_dir, save_format, logger)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'storage_dir'}

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Save conversation to file.

        Args:
            conversation: Conversation data to sa`
- Code: `def save_conversation(self, conversation, filename)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'conversation', 'self'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Load conversation from file.

        Args:
            filename: Filename to load

       `
- Code: `def load_conversation(self, filename)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'filename', 'self'}

**Line 107** (high): docstring_param_mismatch
- Comment: `
        List all saved conversations.

        Returns:
            List of conversation metadata
 `
- Code: `def list_conversations(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 149** (high): docstring_param_mismatch
- Comment: `
        Clean up old conversation files.

        Args:
            max_age_days: Maximum age of fi`
- Code: `def cleanup_old_conversations(self, max_age_days)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'max_age_days'}

### src\services\chatgpt\navigator.py

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Initialize ChatGPT navigator.
        
        Args:
            config: Configuration dict`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 198** (high): docstring_param_mismatch
- Comment: `
        Get the active page created by navigate_to_chat.
        
        Returns:
            Acti`
- Code: `def get_active_page(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\services\chatgpt\session.py

**Line 70** (high): docstring_param_mismatch
- Comment: `
        Initialize browser session manager.

        Args:
            config: Configuration dictio`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 300** (high): docstring_param_mismatch
- Comment: `
        Clear all session data.

        Returns:
            True if successful, False otherwise
 `
- Code: `def clear_session(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 354** (high): docstring_param_mismatch
- Comment: `
        Create a new browser session.

        Implementation of BaseSessionManager abstract method`
- Code: `def create_session(self, service_name)`
- Issue: Docstring params don't match: missing={'Returns', 'kwargs', 'Args'}, extra={'service_name', 'self'}

**Line 386** (high): docstring_param_mismatch
- Comment: `
        Validate that a browser session exists and is active.

        Implementation of BaseSessio`
- Code: `def validate_session(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

### src\services\contract_system\contract_notifications_integration.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Hook: Called when contract is assigned to agent.
        
        Args:
            contrac`
- Code: `def on_contract_assigned(self, contract_id, agent_id, contract_data)`
- Issue: Docstring params don't match: missing={'Hook', 'Returns', 'Args'}, extra={'contract_id', 'self'}

**Line 77** (high): docstring_param_mismatch
- Comment: `
        Hook: Called when agent starts working on contract.
        
        Args:
            cont`
- Code: `def on_contract_started(self, contract_id, agent_id, contract_name)`
- Issue: Docstring params don't match: missing={'Hook', 'Returns', 'Args'}, extra={'contract_id', 'self'}

**Line 112** (high): docstring_param_mismatch
- Comment: `
        Hook: Called when agent completes contract.
        
        Args:
            contract_id:`
- Code: `def on_contract_completed(self, contract_id, agent_id, contract_data, metrics)`
- Issue: Docstring params don't match: missing={'Hook', 'Returns', 'Args'}, extra={'contract_id', 'self'}

**Line 151** (high): docstring_param_mismatch
- Comment: `
        Hook: Called when agent is blocked on contract.
        
        Args:
            contract`
- Code: `def on_contract_blocked(self, contract_id, agent_id, contract_name, blocker)`
- Issue: Docstring params don't match: missing={'Hook', 'Returns', 'Args'}, extra={'contract_id', 'self'}

### src\services\contract_system\cycle_planner_integration.py

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Initialize cycle planner integration.

        Args:
            project_root: Project root`
- Code: `def __init__(self, project_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'project_root'}

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Load pending tasks from cycle planner JSON file for agent.

        Args:
            agent`
- Code: `def load_cycle_planner_tasks(self, agent_id, target_date)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 115** (high): docstring_param_mismatch
- Comment: `
        Convert cycle planner task to contract format.

        Args:
            task: Cycle plann`
- Code: `def convert_task_to_contract(self, task, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 163** (high): docstring_param_mismatch
- Comment: `
        Get next available task from cycle planner for agent.

        Args:
            agent_id: `
- Code: `def get_next_cycle_task(self, agent_id, target_date)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 189** (high): docstring_param_mismatch
- Comment: `
        Mark cycle planner task as complete.

        Args:
            agent_id: Agent ID
        `
- Code: `def mark_task_complete(self, agent_id, task_id, target_date)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\services\contract_system\manager.py

**Line 79** (high): docstring_param_mismatch
- Comment: `
        Get next available task for agent.
        
        Checks cycle planner first, then falls `
- Code: `def get_next_task(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 182** (high): docstring_param_mismatch
- Comment: `
        Mark cycle planner task as active/assigned.
        
        Args:
            agent_id: Ag`
- Code: `def _mark_cycle_task_active(self, agent_id, task_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\services\coordination\bulk_coordinator.py

**Line 36** (high): docstring_param_mismatch
- Comment: `Coordinate multiple messages for efficient delivery.

        Args:
            messages: List of me`
- Code: `def coordinate_bulk_messages(self, messages)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'messages', 'self'}

### src\services\handlers\utility_handler.py

**Line 43** (high): docstring_param_mismatch
- Comment: `Check status of agents or specific agent using onboarding handler.

        Args:
            agent_`
- Code: `def check_status(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 99** (high): docstring_param_mismatch
- Comment: `List all available agents from onboarding handler.

        Returns:
            List of agent infor`
- Code: `def list_agents(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 129** (high): docstring_param_mismatch
- Comment: `Get coordinates for a specific agent from coordinate file.

        Args:
            agent_id: Agen`
- Code: `def get_coordinates(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 168** (high): docstring_param_mismatch
- Comment: `Get message history for agents from vector database.

        Args:
            agent_id: Optional s`
- Code: `def get_history(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\services\hard_onboarding_service.py

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Step 1: Go to chat input area and press Ctrl+Shift+Backspace.

        Args:
            ag`
- Code: `def step_1_clear_chat(self, agent_id)`
- Issue: Docstring params don't match: missing={'1', 'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
        Step 2: Press Ctrl+Enter to send/execute.

        Returns:
            True if successful
`
- Code: `def step_2_send_execute(self)`
- Issue: Docstring params don't match: missing={'Returns', '2'}, extra={'self'}

**Line 136** (high): docstring_param_mismatch
- Comment: `
        Step 3: Press Ctrl+N to create new window/session.

        Returns:
            True if su`
- Code: `def step_3_new_window(self)`
- Issue: Docstring params don't match: missing={'Returns', '3'}, extra={'self'}

**Line 155** (high): docstring_param_mismatch
- Comment: `
        Step 4: Navigate to onboarding input coordinates.

        Args:
            agent_id: Targ`
- Code: `def step_4_navigate_to_onboarding(self, agent_id)`
- Issue: Docstring params don't match: missing={'4', 'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 198** (high): docstring_param_mismatch
- Comment: `
        Get agent-specific optimized instructions based on role.

        Args:
            agent_i`
- Code: `def _get_agent_specific_instructions(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 591** (high): docstring_param_mismatch
- Comment: `
        Step 5: Send onboarding message via Enter.

        Args:
            agent_id: Target agen`
- Code: `def step_5_send_onboarding_message(self, agent_id, onboarding_message, role)`
- Issue: Docstring params don't match: missing={'Returns', '5', 'Args'}, extra={'self', 'agent_id'}

**Line 772** (high): docstring_param_mismatch
- Comment: `
        Execute complete hard onboarding protocol (5 steps).

        Args:
            agent_id: T`
- Code: `def execute_hard_onboarding(self, agent_id, onboarding_message, role)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 820** (high): docstring_param_mismatch
- Comment: `
    Convenience function for hard onboarding single agent.

    Args:
        agent_id: Target agen`
- Code: `def hard_onboard_agent(agent_id, onboarding_message, role)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 840** (high): docstring_param_mismatch
- Comment: `
    Hard onboard multiple agents sequentially.

    Args:
        agents: List of (agent_id, onboar`
- Code: `def hard_onboard_multiple_agents(agents, role)`
- Issue: Docstring params don't match: missing={'Returns', 'agent_id', 'Args'}, extra={'agents'}

### src\services\message_batching_service.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Initialize message batch.

        Args:
            agent_id: Agent creating the batch
   `
- Code: `def __init__(self, agent_id, recipient)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        Start a new message batch.

        Args:
            agent_id: Agent creating the batch
  `
- Code: `def start_batch(self, agent_id, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Add message to existing batch.

        Args:
            agent_id: Agent adding the messag`
- Code: `def add_to_batch(self, agent_id, recipient, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 153** (high): docstring_param_mismatch
- Comment: `
        Send consolidated batch message.

        Args:
            agent_id: Agent sending the bat`
- Code: `def send_batch(self, agent_id, recipient, priority)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 194** (high): docstring_param_mismatch
- Comment: `
        Get status of current batch.

        Args:
            agent_id: Agent ID
            reci`
- Code: `def get_batch_status(self, agent_id, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 224** (high): docstring_param_mismatch
- Comment: `
        Cancel and clear batch without sending.

        Args:
            agent_id: Agent ID
     `
- Code: `def cancel_batch(self, agent_id, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\services\message_identity_clarification.py

**Line 23** (high): docstring_param_mismatch
- Comment: `Format message with agent identity clarification.

        Args:
            message: The message to`
- Code: `def format_message_with_identity_clarification(self, message, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

### src\services\messaging_cli_coordinate_management\utilities.py

**Line 15** (high): docstring_param_mismatch
- Comment: `
    Load agent coordinates using SSOT coordinate loader.

    Returns:
        Dictionary of agent `
- Code: `def load_coords_file()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### src\services\messaging_infrastructure.py

**Line 265** (high): docstring_param_mismatch
- Comment: `
    Format multi-agent request message with response instructions.

    Args:
        message: Orig`
- Code: `def _format_multi_agent_request_message(message, collector_id, request_id, recipient_count, timeout_seconds)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message'}

**Line 310** (high): docstring_param_mismatch
- Comment: `
    Format normal message with response instructions.

    Args:
        message: Original message `
- Code: `def _format_normal_message_with_instructions(message, message_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message'}

**Line 709** (high): docstring_param_mismatch
- Comment: `
        Send message to agent via message queue (prevents race conditions).

        CRITICAL: All `
- Code: `def send_to_agent(agent, message, priority, use_pyautogui, stalled, send_mode, sender, message_category, message_metadata)`
- Issue: Docstring params don't match: missing={'VALIDATION', 'CRITICAL', 'Args'}, extra={'message_category', 'agent', 'message_metadata'}

**Line 867** (high): docstring_param_mismatch
- Comment: `
        Send multi-agent request that collects responses and combines them.

        Creates a resp`
- Code: `def send_multi_agent_request(recipients, message, sender, priority, timeout_seconds, wait_for_all, stalled)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'recipients'}

**Line 961** (high): docstring_param_mismatch
- Comment: `
        Broadcast message to all agents via message queue.

        CRITICAL: All messages route th`
- Code: `def broadcast_to_all(message, priority, stalled)`
- Issue: Docstring params don't match: missing={'VALIDATION', 'CRITICAL'}, extra={'message', 'stalled', 'priority'}

**Line 1110** (high): docstring_param_mismatch
- Comment: `
        Detect actual sender from environment and context.

        Checks:
        1. AGENT_CONTEX`
- Code: `def _detect_sender()`
- Issue: Docstring params don't match: missing={'Checks', 'Returns'}, extra=set()

**Line 1152** (high): docstring_param_mismatch
- Comment: `
        Determine message type and normalize sender based on sender/recipient.

        Args:
     `
- Code: `def _determine_message_type(sender, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'sender'}

**Line 1503** (high): docstring_param_mismatch
- Comment: `
        Send message to agent via message queue (synchronized delivery).

        VALIDATION: Check`
- Code: `def send_message(self, agent, message, priority, use_pyautogui, wait_for_delivery, timeout, discord_user_id, stalled, apply_template, message_category, sender)`
- Issue: Docstring params don't match: missing={'VALIDATION', 'default', 'Args', 'CRITICAL', 'Returns'}, extra={'self', 'agent'}

**Line 1758** (high): docstring_param_mismatch
- Comment: `
        Broadcast message to all agents.

        CRITICAL: Wraps entire operation in keyboard lock`
- Code: `def broadcast_message(self, message, priority)`
- Issue: Docstring params don't match: missing={'CRITICAL', 'Returns', 'Args'}, extra={'message', 'self'}

**Line 1856** (high): docstring_param_mismatch
- Comment: `
        Determine message type and normalize sender based on sender/recipient.

        Args:
     `
- Code: `def _determine_message_type(sender, recipient)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'sender'}

**Line 1893** (high): docstring_param_mismatch
- Comment: `
        Get Discord username from user ID.

        Args:
            discord_user_id: Discord user`
- Code: `def _get_discord_username(self, discord_user_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'discord_user_id'}

### src\services\models\vector_models.py

**Line 130** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return query_text as 'query'.`
- Code: `def query_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 135** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return similarity_threshold as 'threshold'.`
- Code: `def threshold_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 140** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return filters as 'metadata_filter'.`
- Code: `def metadata_filter_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 213** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return document_id as 'id'.`
- Code: `def id_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 218** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return document_id as 'result_id'.`
- Code: `def result_id_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 223** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return similarity_score as 'score'.`
- Code: `def score_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 228** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return similarity_score as 'relevance'.`
- Code: `def relevance_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

**Line 233** (high): docstring_param_mismatch
- Comment: `Backward compatibility: return similarity_score as 'relevance_score'.`
- Code: `def relevance_score_alias(self)`
- Issue: Docstring params don't match: missing={'compatibility'}, extra={'self'}

### src\services\onboarding_template_loader.py

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Create complete onboarding message by merging template + custom content.

        Args:
   `
- Code: `def create_onboarding_message(self, agent_id, role, custom_message, contract_info)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 91** (high): docstring_param_mismatch
- Comment: `Fallback: Format custom message if template missing.`
- Code: `def _format_custom_message(self, agent_id, role, custom_message)`
- Issue: Docstring params don't match: missing={'Fallback'}, extra={'role', 'self', 'custom_message', 'agent_id'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
    Convenience function to load complete onboarding message.

    Usage:
        message = load_on`
- Code: `def load_onboarding_template(agent_id, role, custom_message, contract_info)`
- Issue: Docstring params don't match: missing={'Usage'}, extra={'custom_message', 'role', 'contract_info', 'agent_id'}

### src\services\portfolio_service.py

**Line 76** (high): docstring_param_mismatch
- Comment: `
        Create a new portfolio.
        
        Args:
            user_id: User identifier
       `
- Code: `def create_portfolio(self, user_id, portfolio_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'user_id'}

**Line 102** (high): docstring_param_mismatch
- Comment: `
        Add stock to portfolio.
        
        Args:
            portfolio_id: Portfolio identifi`
- Code: `def add_stock(self, portfolio_id, stock)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'portfolio_id', 'self'}

**Line 140** (high): docstring_param_mismatch
- Comment: `
        Remove stock from portfolio.
        
        Args:
            portfolio_id: Portfolio ide`
- Code: `def remove_stock(self, portfolio_id, symbol)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'portfolio_id', 'self'}

**Line 166** (high): docstring_param_mismatch
- Comment: `
        Analyze portfolio performance.
        
        Args:
            portfolio_id: Portfolio i`
- Code: `def analyze_portfolio(self, portfolio_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'portfolio_id', 'self'}

**Line 202** (high): docstring_param_mismatch
- Comment: `
        Get stock recommendations for portfolio.
        
        Args:
            portfolio_id: P`
- Code: `def get_recommendations(self, portfolio_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'portfolio_id', 'self'}

**Line 224** (high): docstring_param_mismatch
- Comment: `
        Calculate total portfolio value.
        
        Args:
            portfolio_id: Portfolio`
- Code: `def calculate_total_value(self, portfolio_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'portfolio_id', 'self'}

**Line 245** (high): docstring_param_mismatch
- Comment: `
        Get portfolio performance metrics.
        
        Args:
            portfolio_id: Portfol`
- Code: `def get_performance_metrics(self, portfolio_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'portfolio_id', 'self'}

**Line 265** (high): docstring_param_mismatch
- Comment: `
        Fetch current stock price from Alpha Vantage API.
        
        Args:
            symbol`
- Code: `def _fetch_stock_price(self, symbol)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'symbol', 'self'}

**Line 305** (high): docstring_param_mismatch
- Comment: `
        Calculate percentage change.
        
        Args:
            current_price: Current pric`
- Code: `def _calculate_change(self, current_price, previous_price)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'current_price'}

### src\services\protocol\message_router.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Route a message based on priority and strategies.

        Args:
            message: Messa`
- Code: `def route_message(self, message, strategies)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Route message with priority override.

        Args:
            message: Message to route
`
- Code: `def route_with_priority(self, message, priority_override)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 93** (high): docstring_param_mismatch
- Comment: `
        Route message with specific strategy.

        Args:
            message: Message to route
`
- Code: `def route_with_strategy(self, message, strategy)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

### src\services\protocol\policy_enforcer.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Enforce policy on a message.

        Args:
            message: Message to enforce policy `
- Code: `def enforce_policy(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Validate policy data structure.

        Args:
            policy_data: Policy data to vali`
- Code: `def validate_policy(self, policy_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'policy_data', 'self'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Check if sender has permission to send to recipient.

        Args:
            sender: Sen`
- Code: `def check_permissions(self, sender, recipient, message_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'sender'}

### src\services\protocol\protocol_validator.py

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Validate protocol data structure.

        Args:
            protocol_data: Protocol data t`
- Code: `def validate_protocol(self, protocol_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'protocol_data'}

**Line 58** (high): docstring_param_mismatch
- Comment: `
        Validate message protocol compliance.

        Args:
            message: Message to valida`
- Code: `def validate_message(self, message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Validate route protocol compliance.

        Args:
            route: Route to validate

  `
- Code: `def validate_route(self, route)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'route'}

**Line 121** (high): docstring_param_mismatch
- Comment: `
        Format validation errors.

        Args:
            errors: List of error messages

      `
- Code: `def validation_errors(self, errors)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'errors'}

### src\services\protocol\route_manager.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Add a new route.

        Args:
            route_name: Name of the route
            route`
- Code: `def add_route(self, route_name, route_type, optimization, config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'route_name'}

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Remove a route.

        Args:
            route_name: Name of the route to remove

       `
- Code: `def remove_route(self, route_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'route_name'}

**Line 82** (high): docstring_param_mismatch
- Comment: `
        Get route information.

        Args:
            route_name: Name of the route

        Re`
- Code: `def get_route(self, route_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'route_name'}

**Line 102** (high): docstring_param_mismatch
- Comment: `
        List all registered routes.

        Returns:
            List of route names
        `
- Code: `def list_routes(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\services\recommendation_engine.py

**Line 43** (high): docstring_param_mismatch
- Comment: `
        Get personalized recommendations for an agent based on context.

        Args:
            `
- Code: `def get_agent_recommendations(self, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'context'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Optimize workflow based on historical data and patterns.

        Args:
            workflo`
- Code: `def optimize_workflow(self, workflow_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'workflow_data'}

### src\services\soft_onboarding_service.py

**Line 62** (high): docstring_param_mismatch
- Comment: `Step 1: Click chat input to get agent's attention.`
- Code: `def step_1_click_chat_input(self, agent_id)`
- Issue: Docstring params don't match: missing={'1'}, extra={'self', 'agent_id'}

**Line 89** (high): docstring_param_mismatch
- Comment: `Step 2: Save session (Ctrl+Enter).`
- Code: `def step_2_save_session(self)`
- Issue: Docstring params don't match: missing={'2'}, extra={'self'}

**Line 105** (high): docstring_param_mismatch
- Comment: `Step 3: Send cleanup prompt (passdown message).`
- Code: `def step_3_send_cleanup_prompt(self, agent_id, custom_cleanup_message)`
- Issue: Docstring params don't match: missing={'3'}, extra={'self', 'custom_cleanup_message', 'agent_id'}

**Line 135** (high): docstring_param_mismatch
- Comment: `Step 4: Open new tab (Ctrl+T).`
- Code: `def step_4_open_new_tab(self)`
- Issue: Docstring params don't match: missing={'4'}, extra={'self'}

**Line 151** (high): docstring_param_mismatch
- Comment: `Step 5: Navigate to onboarding coordinates.`
- Code: `def step_5_navigate_to_onboarding(self, agent_id)`
- Issue: Docstring params don't match: missing={'5'}, extra={'self', 'agent_id'}

**Line 178** (high): docstring_param_mismatch
- Comment: `Step 6: Paste and send onboarding message.`
- Code: `def step_6_paste_onboarding_message(self, agent_id, message)`
- Issue: Docstring params don't match: missing={'6'}, extra={'message', 'self', 'agent_id'}

**Line 224** (high): docstring_param_mismatch
- Comment: `Fallback: Send cleanup via messaging system (S2A template, no-ack).`
- Code: `def _send_cleanup_via_messaging(self, agent_id, custom_message)`
- Issue: Docstring params don't match: missing={'Fallback'}, extra={'custom_message', 'self', 'agent_id'}

**Line 263** (high): docstring_param_mismatch
- Comment: `Fallback: Send onboarding via messaging system (S2A template, no-ack).`
- Code: `def _send_onboarding_via_messaging(self, agent_id, message)`
- Issue: Docstring params don't match: missing={'Fallback'}, extra={'message', 'self', 'agent_id'}

**Line 322** (high): docstring_param_mismatch
- Comment: `
        Execute full soft onboarding protocol (6 steps with animations).

        NOTE: Lock handli`
- Code: `def execute_soft_onboarding(self, agent_id, onboarding_message, role, custom_cleanup_message)`
- Issue: Docstring params don't match: missing={'NOTE'}, extra={'onboarding_message', 'role', 'self', 'custom_cleanup_message', 'agent_id'}

**Line 372** (high): docstring_param_mismatch
- Comment: `
    Convenience function for soft onboarding.

    CRITICAL: Wrapped in keyboard_control to block o`
- Code: `def soft_onboard_agent(agent_id, message)`
- Issue: Docstring params don't match: missing={'kwargs', 'FIX', 'Args', 'CRITICAL', 'Returns'}, extra={'agent_id'}

**Line 410** (high): docstring_param_mismatch
- Comment: `
    Soft onboard multiple agents sequentially.

    CRITICAL: Wrapped in keyboard_control to block `
- Code: `def soft_onboard_multiple_agents(agents, role, generate_cycle_report)`
- Issue: Docstring params don't match: missing={'CRITICAL', 'Returns', 'agent_id', 'Args'}, extra={'agents'}

**Line 484** (high): docstring_param_mismatch
- Comment: `
    Generate cycle accomplishments report from all agent status.json files.

    Convenience functi`
- Code: `def generate_cycle_accomplishments_report(cycle_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'cycle_id'}

### src\services\thea\thea_service.py

**Line 334** (high): docstring_param_mismatch
- Comment: `
        Send message to Thea and optionally wait for response.

        Args:
            message: `
- Code: `def send_message(self, message, wait_for_response)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 419** (high): docstring_param_mismatch
- Comment: `
        Complete communication cycle: send message and get response.

        Args:
            mes`
- Code: `def communicate(self, message, save)`
- Issue: Docstring params don't match: missing={'cycle', 'Returns', 'Args'}, extra={'message', 'self'}

### src\services\trader_replay\behavioral_scoring.py

**Line 262** (high): docstring_param_mismatch
- Comment: `
        Calculate all behavioral scores for a session.

        Args:
            session_id: Sessi`
- Code: `def calculate_all_scores(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

### src\services\trader_replay\replay_engine.py

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Initialize replay engine.

        Args:
            db_path: Path to SQLite database
     `
- Code: `def __init__(self, db_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'db_path'}

**Line 88** (high): docstring_param_mismatch
- Comment: `
        Create a new replay session.

        Args:
            symbol: Trading symbol (e.g., 'AAPL`
- Code: `def create_session(self, symbol, session_date, timeframe, candles)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'symbol', 'self'}

**Line 189** (high): docstring_param_mismatch
- Comment: `
        Get session information.

        Args:
            session_id: Session ID

        Returns`
- Code: `def get_session_info(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 228** (high): docstring_param_mismatch
- Comment: `
        Get current replay state for a session.

        Args:
            session_id: Session ID

`
- Code: `def get_replay_state(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 245** (high): docstring_param_mismatch
- Comment: `
        Step replay forward or backward.

        Args:
            session_id: Session ID
        `
- Code: `def step_replay(self, session_id, direction)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'direction', 'session_id'}

### src\services\trader_replay\trader_replay_orchestrator.py

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Initialize trader replay orchestrator.

        Args:
            db_path: Path to SQLite d`
- Code: `def __init__(self, db_path, agent_workspace_path)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'db_path'}

**Line 96** (high): docstring_param_mismatch
- Comment: `
        Create a new replay session.

        Args:
            symbol: Trading symbol (e.g., 'AAPL`
- Code: `def create_session(self, symbol, session_date, timeframe, candles, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'symbol', 'self'}

**Line 152** (high): docstring_param_mismatch
- Comment: `
        Start a replay session.

        Args:
            session_id: Session ID

        Returns:`
- Code: `def start_replay(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 189** (high): docstring_param_mismatch
- Comment: `
        Step replay forward or backward.

        Args:
            session_id: Session ID
        `
- Code: `def step_replay(self, session_id, direction)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'direction', 'session_id'}

**Line 232** (high): docstring_param_mismatch
- Comment: `
        Complete a replay session and generate summary.

        Args:
            session_id: Sess`
- Code: `def complete_session(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 275** (high): docstring_param_mismatch
- Comment: `
        Notify agent via messaging system.

        Args:
            agent_id: Agent ID
          `
- Code: `def _notify_agent(self, agent_id, message)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 298** (high): docstring_param_mismatch
- Comment: `
        Get current session status.

        Args:
            session_id: Session ID

        Retu`
- Code: `def get_session_status(self, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

### src\services\unified_messaging_service.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Send message to agent.

        Args:
            agent: Target agent ID
            messag`
- Code: `def send_message(self, agent, message, priority, use_pyautogui, wait_for_delivery, timeout, discord_user_id, stalled, apply_template, message_category, sender)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'agent'}

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Broadcast message to all agents.

        Args:
            message: Message content
      `
- Code: `def broadcast_message(self, message, priority)`
- Issue: Docstring params don't match: missing={'Returns', 'agent_id', 'Args'}, extra={'message', 'self'}

### src\services\utils\messaging_templates.py

**Line 15** (high): docstring_param_mismatch
- Comment: `
    Validate that all template variables are provided.
    
    Args:
        template: Template st`
- Code: `def validate_template_vars(template, vars_dict)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'template'}

**Line 36** (high): docstring_param_mismatch
- Comment: `
    Format template with validation.
    
    Args:
        template: Template string
        **kwa`
- Code: `def format_template(template)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'kwargs', 'Args'}, extra={'template'}

### src\services\utils\vector_integration_helpers.py

**Line 18** (high): docstring_param_mismatch
- Comment: `Format search result for agent consumption.

    Args:
        result: Search result object

    Ret`
- Code: `def format_search_result(result)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'result'}

**Line 44** (high): docstring_param_mismatch
- Comment: `Generate recommendations based on similar tasks.

    Args:
        similar_tasks: List of similar t`
- Code: `def generate_recommendations(similar_tasks)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'similar_tasks'}

**Line 73** (high): docstring_param_mismatch
- Comment: `Generate agent-specific recommendations.

    Args:
        work_history: List of work history items`
- Code: `def generate_agent_recommendations(work_history)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'work_history'}

### src\services\vector_database_service_unified.py

**Line 442** (high): comment_return_mismatch
- Comment: `Chroma returns lists nested by query.`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\services\work_indexer.py

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Index agent's completed work to vector database.

        Args:
            file_path: Path`
- Code: `def index_agent_work(self, file_path, work_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'file_path'}

**Line 120** (high): docstring_param_mismatch
- Comment: `
        Index agent's inbox messages for intelligent search.

        Returns:
            Number o`
- Code: `def index_inbox_messages(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\shared_utils\config.py

**Line 27** (high): docstring_param_mismatch
- Comment: `Retrieve a setting from the environment.

    Args:
        key: Name of the environment variable to`
- Code: `def get_setting(key, default)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'key'}

### src\shared_utils\logger.py

**Line 20** (high): docstring_param_mismatch
- Comment: `
    Set up and return a logger with console and file handlers.
    
    **CONSOLIDATED**: Now uses `
- Code: `def setup_logger(name, level)`
- Issue: Docstring params don't match: missing={'Idempotent'}, extra={'level', 'name'}

### src\swarm_brain\agent_notes.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Initialize agent notes.

        Args:
            agent_id: Agent ID (e.g., "Agent-7")
   `
- Code: `def __init__(self, agent_id, workspace_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 80** (high): docstring_param_mismatch
- Comment: `
        Add a note.

        Args:
            content: Note content
            note_type: Type of`
- Code: `def add_note(self, content, note_type, tags)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

**Line 139** (high): docstring_param_mismatch
- Comment: `
        Get notes with optional filtering.

        Args:
            note_type: Filter by type
   `
- Code: `def get_notes(self, note_type, tags)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'note_type'}

**Line 160** (high): docstring_param_mismatch
- Comment: `
        Search notes by content.

        Args:
            query: Search query

        Returns:
 `
- Code: `def search_notes(self, query)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

**Line 177** (high): docstring_param_mismatch
- Comment: `
        Log work session.

        Args:
            session_summary: Summary of work completed
   `
- Code: `def log_work(self, session_summary)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'session_summary'}

**Line 186** (high): docstring_param_mismatch
- Comment: `
        Record something learned.

        Args:
            learning: What was learned
        `
- Code: `def record_learning(self, learning)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'learning'}

**Line 195** (high): docstring_param_mismatch
- Comment: `
        Mark information as important.

        Args:
            info: Important information
     `
- Code: `def mark_important(self, info)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'info'}

### src\swarm_brain\knowledge_base.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Initialize knowledge base.

        Args:
            brain_root: Root directory for swarm `
- Code: `def __init__(self, brain_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'brain_root', 'self'}

**Line 87** (high): docstring_param_mismatch
- Comment: `
        Add knowledge entry.

        Args:
            entry: Knowledge entry

        Returns:
  `
- Code: `def add_entry(self, entry)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'entry'}

**Line 150** (high): docstring_param_mismatch
- Comment: `
        Search knowledge base.

        Args:
            query: Search query

        Returns:
   `
- Code: `def search(self, query)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

### src\swarm_brain\swarm_memory.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Initialize swarm memory.

        Args:
            agent_id: Agent ID
            workspac`
- Code: `def __init__(self, agent_id, workspace_root, brain_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Take personal note.

        Args:
            content: Note content
            note_type:`
- Code: `def take_note(self, content, note_type)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'content'}

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Share learning with entire swarm.

        Args:
            title: Learning title
        `
- Code: `def share_learning(self, title, content, tags)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'title'}

**Line 82** (high): docstring_param_mismatch
- Comment: `
        Record important decision for swarm.

        Args:
            title: Decision title
     `
- Code: `def record_decision(self, title, decision, rationale)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'title'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        Log work session.

        Args:
            summary: Session summary
        `
- Code: `def log_session(self, summary)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'summary'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
        Search swarm's shared knowledge.

        Args:
            query: Search query

        Re`
- Code: `def search_swarm_knowledge(self, query)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'query', 'self'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Get my personal notes.

        Args:
            note_type: Optional filter by type

     `
- Code: `def get_my_notes(self, note_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'note_type'}

**Line 146** (high): docstring_param_mismatch
- Comment: `
        Update status.json with notes section.

        Args:
            status_file: Path to stat`
- Code: `def update_status_with_notes(self, status_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'status_file', 'self'}

### src\swarm_pulse\intelligence.py

**Line 73** (high): docstring_param_mismatch
- Comment: `Hybrid routing: combine semantic similarity with tag-based rules.`
- Code: `def route_with_intelligence(event)`
- Issue: Docstring params don't match: missing={'routing'}, extra={'event'}

**Line 118** (high): docstring_param_mismatch
- Comment: `Analyze coordination efficiency metrics (Phase 2C).

    Calculates real metrics from:
    - PulseBu`
- Code: `def analyze_coordination_efficiency(agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### src\templates\onboarding_roles.py

**Line 18** (high): docstring_param_mismatch
- Comment: `
    Build role-based onboarding message.

    Args:
        agent_id: Agent ID
        role: Role k`
- Code: `def build_role_message(agent_id, role)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### src\tools\github_scanner.py

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Initialize GitHub scanner.

        Args:
            token: GitHub personal access token (`
- Code: `def __init__(self, token)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'token', 'self'}

**Line 90** (high): docstring_param_mismatch
- Comment: `
        List all repositories for authenticated user or specific username.

        Args:
         `
- Code: `def list_user_repositories(self, username, include_private)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'username'}

**Line 135** (high): docstring_param_mismatch
- Comment: `
        Get detailed information about a specific repository.

        Args:
            owner: Rep`
- Code: `def get_repository(self, owner, repo_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'owner'}

**Line 157** (high): docstring_param_mismatch
- Comment: `
        Get language breakdown for a repository.

        Args:
            owner: Repository owner`
- Code: `def get_repository_languages(self, owner, repo_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'owner'}

**Line 179** (high): docstring_param_mismatch
- Comment: `
        Parse GitHub API repository response into RepositoryInfo.

        Args:
            data: `
- Code: `def _parse_repository(self, data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'data'}

**Line 220** (high): docstring_param_mismatch
- Comment: `
    Filter repositories to identify integration candidates.

    Args:
        repos: List of repos`
- Code: `def filter_integration_candidates(repos, min_size_kb, max_size_kb, exclude_names, primary_language)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'repos'}

**Line 261** (high): docstring_param_mismatch
- Comment: `
    Print formatted summary of repositories.

    Args:
        repos: List of repository informati`
- Code: `def print_repository_summary(repos)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'repos'}

### src\trading_robot\services\analytics\performance_metrics_engine.py

**Line 62** (high): comment_return_mismatch
- Comment: `Simplified total return calculation`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\utils\agent_queue_status.py

**Line 78** (high): docstring_param_mismatch
- Comment: `
        Mark agent's Cursor queue as full.
        
        Args:
            agent_id: Agent ident`
- Code: `def mark_full(cls, agent_id, reason)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'cls', 'agent_id'}

**Line 132** (high): docstring_param_mismatch
- Comment: `
        Mark agent's Cursor queue as available (not full).
        
        Args:
            agent`
- Code: `def mark_available(cls, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'cls', 'agent_id'}

**Line 185** (high): docstring_param_mismatch
- Comment: `
        Check if agent's Cursor queue is marked as full.
        
        Args:
            agent_i`
- Code: `def is_full(cls, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'cls', 'agent_id'}

**Line 228** (high): docstring_param_mismatch
- Comment: `
        Get full queue status for an agent.
        
        Args:
            agent_id: Agent iden`
- Code: `def get_status(cls, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'cls', 'agent_id'}

### src\utils\backup.py

**Line 22** (high): docstring_param_mismatch
- Comment: `Initialize backup manager.

        Args:
            root: Root directory to backup
            des`
- Code: `def __init__(self, root, dest)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'root'}

**Line 33** (high): docstring_param_mismatch
- Comment: `Create backup of agent state.

        Args:
            agents: List of specific agents to backup (`
- Code: `def create_backup(self, agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agents'}

**Line 66** (high): docstring_param_mismatch
- Comment: `List all available backups.

        Returns:
            List of backup directory paths
        `
- Code: `def list_backups(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 77** (high): docstring_param_mismatch
- Comment: `Restore from backup.

        Args:
            backup_path: Path to backup directory

        Retur`
- Code: `def restore_backup(self, backup_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'backup_path'}

**Line 102** (high): docstring_param_mismatch
- Comment: `Clean up old backups, keeping only the most recent ones.

        Args:
            keep_count: Numb`
- Code: `def cleanup_old_backups(self, keep_count)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'keep_count'}

### src\utils\config_file_scanner.py

**Line 26** (high): docstring_param_mismatch
- Comment: `Initialize file scanner with available scanners.

        Args:
            scanners: List of config`
- Code: `def __init__(self, scanners)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'scanners', 'self'}

**Line 47** (high): docstring_param_mismatch
- Comment: `Check if file should be skipped during scanning.

        Args:
            file_path: Path to file `
- Code: `def should_skip_file(self, file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'file_path'}

**Line 59** (high): docstring_param_mismatch
- Comment: `Scan a single file for configuration patterns.

        Args:
            file_path: Path to file to`
- Code: `def scan_file(self, file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'file_path'}

**Line 87** (high): docstring_param_mismatch
- Comment: `Scan all Python files in a directory.

        Args:
            root_dir: Root directory to scan

 `
- Code: `def scan_directory(self, root_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'root_dir', 'self'}

### src\utils\config_scanners.py

**Line 181** (high): docstring_param_mismatch
- Comment: `Create default set of configuration scanners.
    
    Returns:
        List of default configuratio`
- Code: `def create_default_scanners()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### src\utils\confirm.py

**Line 10** (high): docstring_param_mismatch
- Comment: `
    Get user confirmation.

    Args:
        message: Confirmation message to display
        defa`
- Code: `def confirm(message, default)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message'}

### src\utils\file_operations\backup_operations.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
        Create a backup of a file.

        Args:
            file_path: Path to the file to backup`
- Code: `def create_backup(file_path, backup_suffix)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 50** (high): docstring_param_mismatch
- Comment: `
        Restore a file from backup.

        Args:
            backup_path: Path to the backup file`
- Code: `def restore_from_backup(backup_path, target_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'backup_path'}

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Copy file from source to destination.

        Args:
            source: Source file path
 `
- Code: `def copy_file(source, destination)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'source'}

**Line 92** (high): docstring_param_mismatch
- Comment: `
        Safely delete a file with automatic backup.

        Args:
            file_path: Path to t`
- Code: `def safe_delete_file(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 122** (high): docstring_param_mismatch
- Comment: `
        Initialize backup manager.

        Args:
            root: Root directory to backup
      `
- Code: `def __init__(self, root, dest)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'root'}

**Line 134** (high): docstring_param_mismatch
- Comment: `
        Create backup of agent state.

        Args:
            agents: List of specific agents to`
- Code: `def create_backup(self, agents)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'agents'}

**Line 167** (high): docstring_param_mismatch
- Comment: `
        List all available backups.

        Returns:
            list[str]: List of backup directo`
- Code: `def list_backups(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 178** (high): docstring_param_mismatch
- Comment: `
        Restore from backup.

        Args:
            backup_path: Path to backup directory to re`
- Code: `def restore_backup(self, backup_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'backup_path'}

**Line 203** (high): docstring_param_mismatch
- Comment: `
        Clean up old backups, keeping only the most recent ones.

        Args:
            keep_co`
- Code: `def cleanup_old_backups(self, keep_count)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'self', 'keep_count'}

**Line 233** (high): docstring_param_mismatch
- Comment: `
    Factory function to create backup manager.

    Args:
        root: Root directory to backup
  `
- Code: `def create_backup_manager(root, dest)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'root'}

### src\utils\file_operations\scanner_operations.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Initialize file scanner.

        Args:
            root_directory: Root directory to scan `
- Code: `def __init__(self, root_directory)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'root_directory'}

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Scan directory for files matching criteria.

        Args:
            extensions: List of `
- Code: `def scan_directory(self, extensions, exclude_patterns)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'extensions'}

**Line 73** (high): docstring_param_mismatch
- Comment: `
        Scan directory using glob pattern.

        Args:
            pattern: Glob pattern (e.g., `
- Code: `def scan_by_pattern(self, pattern)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'pattern', 'self'}

**Line 95** (high): docstring_param_mismatch
- Comment: `
        Get set of all scanned files.

        Returns:
            set[str]: Set of file paths tha`
- Code: `def get_scanned_files(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        Count scanned files by extension.

        Returns:
            dict[str, int]: Dictionary `
- Code: `def count_files_by_extension(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\utils\file_operations\validation_operations.py

**Line 52** (high): docstring_param_mismatch
- Comment: `
        Validate file path and return detailed information.

        Args:
            file_path: P`
- Code: `def validate_file_path(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 82** (high): docstring_param_mismatch
- Comment: `
        Check if a path is safe (not trying to escape allowed directories).

        Args:
        `
- Code: `def is_path_safe(file_path, allowed_dirs)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 100** (high): docstring_param_mismatch
- Comment: `
        Validate that file has an allowed extension.

        Args:
            file_path: Path to `
- Code: `def validate_file_extension(file_path, allowed_extensions)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

### src\utils\inbox_utility.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
    Create an inbox message file directly in agent's inbox directory.
    
    This is a simple fil`
- Code: `def create_inbox_message(recipient, sender, content, priority, message_type, tags)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'recipient'}

### src\utils\logger.py

**Line 37** (high): docstring_param_mismatch
- Comment: `Initialize V2 logger (redirects to unified system).

        Args:
            name: Logger name
   `
- Code: `def __init__(self, name, log_level, log_to_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'name'}

**Line 133** (high): docstring_param_mismatch
- Comment: `Get a configured V2 logger with the given name.

    Args:
        name: Logger name
        log_lev`
- Code: `def get_logger(name, log_level)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'name'}

### src\utils\logger_utils.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
    Set up logger with specified configuration.

    Args:
        name: Logger name
        level:`
- Code: `def setup_logger(name, level, log_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'name'}

**Line 62** (high): docstring_param_mismatch
- Comment: `
    Get logger instance by name.

    Args:
        name: Logger name

    Returns:
        Logger `
- Code: `def get_logger(name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'name'}

### src\utils\swarm_time.py

**Line 18** (high): docstring_param_mismatch
- Comment: `
    Get current local time for swarm operations.
    
    All agents should use this function to en`
- Code: `def get_swarm_time()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 31** (high): docstring_param_mismatch
- Comment: `
    Format datetime as ISO 8601 timestamp.
    
    Args:
        dt: Datetime to format (defaults `
- Code: `def format_swarm_timestamp(dt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'dt'}

**Line 47** (high): docstring_param_mismatch
- Comment: `
    Format datetime as human-readable timestamp.
    
    Args:
        dt: Datetime to format (def`
- Code: `def format_swarm_timestamp_readable(dt)`
- Issue: Docstring params don't match: missing={'HH', 'Returns', 'Args'}, extra={'dt'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
    Format datetime for use in filenames.
    
    Args:
        dt: Datetime to format (defaults t`
- Code: `def format_swarm_timestamp_filename(dt)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'dt'}

**Line 79** (high): docstring_param_mismatch
- Comment: `
    Get current local time formatted for display in messages.
    
    Returns:
        Formatted t`
- Code: `def get_swarm_time_display()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### src\utils\unified_utilities.py

**Line 61** (high): docstring_param_mismatch
- Comment: `Get a configured logger with the given name.
    
    Args:
        name: Logger name
        log_le`
- Code: `def get_logger(name, log_level)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'name'}

### src\vision\analysis.py

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Initialize visual analyzer orchestrator.

        Args:
            config: Configuration d`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 111** (high): docstring_param_mismatch
- Comment: `
        Detect UI elements like buttons, text fields, etc.

        Args:
            image: Input `
- Code: `def detect_ui_elements(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

**Line 123** (high): docstring_param_mismatch
- Comment: `
        Comprehensive screen content analysis.

        Args:
            image: Input image array
`
- Code: `def analyze_screen_content(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

**Line 163** (high): docstring_param_mismatch
- Comment: `
        Detect changes between two images.

        Args:
            image1: First image
         `
- Code: `def detect_changes(self, image1, image2, threshold)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'image1', 'self'}

### src\vision\analyzers\color_analyzer.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
        Initialize color analyzer.

        Args:
            config: Configuration dictionary (res`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Analyze color distribution in the image.

        Args:
            image: Input image arra`
- Code: `def analyze_colors(self, image)`
- Issue: Docstring params don't match: missing={'mean_colors', 'color_channels', 'mean_intensity', 'results', 'Args', 'Returns'}, extra={'self', 'image'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Analyze RGB color image.

        Args:
            image: RGB image array

        Returns`
- Code: `def _analyze_rgb_image(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

**Line 82** (high): docstring_param_mismatch
- Comment: `
        Analyze grayscale image.

        Args:
            image: Grayscale image array

        R`
- Code: `def _analyze_grayscale_image(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

**Line 96** (high): docstring_param_mismatch
- Comment: `
        Get analyzer configuration and capabilities.

        Returns:
            Dictionary with `
- Code: `def get_analyzer_info(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\vision\analyzers\edge_analyzer.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Initialize edge analyzer.

        Args:
            config: Configuration dictionary with `
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 54** (high): docstring_param_mismatch
- Comment: `
        Analyze edge content in the image.

        Args:
            image: Input image array (RGB`
- Code: `def analyze_edges(self, image)`
- Issue: Docstring params don't match: missing={'edge_density', 'edge_pixels', 'Args', 'Returns', 'total_pixels'}, extra={'self', 'image'}

**Line 97** (high): docstring_param_mismatch
- Comment: `
        Get analyzer configuration and capabilities.

        Returns:
            Dictionary with `
- Code: `def get_analyzer_info(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\vision\analyzers\ui_detector.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Initialize UI detector.

        Args:
            config: Configuration dictionary with de`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 60** (high): docstring_param_mismatch
- Comment: `
        Detect UI elements in an image.

        Args:
            image: Input image array (RGB or`
- Code: `def detect_ui_elements(self, image)`
- Issue: Docstring params don't match: missing={'area', 'confidence', 'type', 'Args', 'Returns'}, extra={'self', 'image'}

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Process a single contour and extract UI element information.

        Args:
            con`
- Code: `def _process_contour(self, contour)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'contour'}

**Line 148** (high): docstring_param_mismatch
- Comment: `
        Classify UI element type based on shape characteristics.

        Args:
            approx:`
- Code: `def _classify_element(self, approx, area, width, height)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'approx'}

**Line 179** (high): docstring_param_mismatch
- Comment: `
        Get detector configuration and capabilities.

        Returns:
            Dictionary with `
- Code: `def get_detector_info(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\vision\capture.py

**Line 64** (high): docstring_param_mismatch
- Comment: `
        Capture screenshot of specified region or full screen.

        Args:
            region: (`
- Code: `def capture_screen(self, region)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'region'}

**Line 100** (high): docstring_param_mismatch
- Comment: `
        Capture screen region for specific agent using coordinates.

        Args:
            agen`
- Code: `def capture_agent_region(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 136** (high): docstring_param_mismatch
- Comment: `
        Continuously capture screen and call callback with image.

        Args:
            callba`
- Code: `def continuous_capture(self, callback_func, duration, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'callback_func'}

**Line 184** (high): docstring_param_mismatch
- Comment: `
        Save image to file.

        Args:
            image: Image array to save
            filen`
- Code: `def save_image(self, image, filename, format)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

### src\vision\integration.py

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Initialize vision system orchestrator.

        Args:
            config: Configuration dic`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Capture screen and perform comprehensive analysis.

        Args:
            region: (x, y`
- Code: `def capture_and_analyze(self, region, agent_id, include_ocr, include_ui_detection)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'region'}

**Line 156** (high): docstring_param_mismatch
- Comment: `
        Start continuous monitoring with callback.

        Args:
            callback: Function to`
- Code: `def start_monitoring(self, callback, duration, agent_id, frequency)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'callback', 'self'}

**Line 193** (high): docstring_param_mismatch
- Comment: `
        Detect changes in screen content.

        Args:
            agent_id: Agent ID for coordin`
- Code: `def detect_changes(self, agent_id, region, threshold)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### src\vision\monitoring.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Initialize vision monitoring manager.

        Args:
            config: Configuration dict`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 48** (high): docstring_param_mismatch
- Comment: `
        Start continuous monitoring with callback.

        Args:
            capture_func: Functio`
- Code: `def start_monitoring(self, capture_func, analysis_func, callback, duration, frequency)`
- Issue: Docstring params don't match: missing={'capture_kwargs', 'Args'}, extra={'self', 'capture_func'}

**Line 125** (high): docstring_param_mismatch
- Comment: `
        Get current monitoring status.

        Returns:
            Dictionary with monitoring inf`
- Code: `def get_monitoring_status(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\vision\ocr.py

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Extract text from image using OCR.

        Args:
            image: Input image array

   `
- Code: `def extract_text(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Extract text with bounding box regions.

        Args:
            image: Input image array`
- Code: `def extract_text_with_regions(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

**Line 129** (high): docstring_param_mismatch
- Comment: `
        Preprocess image for better OCR accuracy.

        Args:
            image: Input image arr`
- Code: `def preprocess_image(self, image)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'image'}

### src\vision\persistence.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
        Initialize vision persistence manager.

        Args:
            config: Configuration dic`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Store analysis results in history.

        Args:
            analysis: Analysis results di`
- Code: `def store_analysis(self, analysis)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'analysis', 'self'}

**Line 75** (high): docstring_param_mismatch
- Comment: `
        Get previously captured image for change detection.

        Args:
            agent_id: Ag`
- Code: `def get_previous_image(self, agent_id, region)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Store image for future change detection.

        Args:
            image: Image array to s`
- Code: `def store_previous_image(self, image, agent_id, region)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'image'}

**Line 102** (high): docstring_param_mismatch
- Comment: `
        Save vision analysis data to JSON file.

        Args:
            analysis: Analysis resul`
- Code: `def save_vision_data(self, analysis, filename)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'analysis', 'self'}

**Line 133** (high): docstring_param_mismatch
- Comment: `
        Clean up old vision data files.

        Args:
            max_age_days: Maximum age of fil`
- Code: `def cleanup_old_data(self, max_age_days)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'max_age_days'}

**Line 175** (high): docstring_param_mismatch
- Comment: `
        Convert object to JSON-serializable format.

        Args:
            obj: Object to conve`
- Code: `def _make_serializable(self, obj)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'obj', 'self'}

**Line 196** (high): docstring_param_mismatch
- Comment: `
        Get analysis history.

        Args:
            limit: Maximum number of entries to return`
- Code: `def get_history(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 215** (high): docstring_param_mismatch
- Comment: `
        Get information about persistence state.

        Returns:
            Dictionary with pers`
- Code: `def get_persistence_info(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### src\web\__init__.py

**Line 46** (high): docstring_param_mismatch
- Comment: `
    Create and configure Flask application.

    Returns:
        Configured Flask application inst`
- Code: `def create_app()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 90** (high): docstring_param_mismatch
- Comment: `
    Register all blueprints with Flask app.

    Args:
        app: Flask application instance
    `
- Code: `def register_all_blueprints(app)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'app'}

### src\web\ai_handlers.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
        Handle request to list all AI conversations.
        
        Args:
            request: Fl`
- Code: `def handle_list_conversations(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Handle request to process an AI message.
        
        Args:
            request: Flask `
- Code: `def handle_process_message(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\ai_training_handlers.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Handle request to get DreamVault training status.

        Args:
            request: Flask`
- Code: `def handle_get_dreamvault_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 63** (high): docstring_param_mismatch
- Comment: `
        Handle request to run DreamVault batch processing.

        Args:
            request: Flas`
- Code: `def handle_run_dreamvault_batch(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\architecture_handlers.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Handle request to get all architectural principles.

        Args:
            request: Fla`
- Code: `def handle_get_all_principles(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 76** (high): docstring_param_mismatch
- Comment: `
        Handle request to get specific architectural principle.

        Args:
            request:`
- Code: `def handle_get_principle(self, request, principle_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\assignment_handlers.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Handle request to assign task to best agent.

        Args:
            request: Flask requ`
- Code: `def handle_assign(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Handle request to list all assignments.

        Args:
            request: Flask request o`
- Code: `def handle_list(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 149** (high): docstring_param_mismatch
- Comment: `
        Handle request to get assignment service status.

        Args:
            request: Flask `
- Code: `def handle_get_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\chat_presence_handlers.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Handle request to update chat presence.

        Args:
            request: Flask request o`
- Code: `def handle_update(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 95** (high): docstring_param_mismatch
- Comment: `
        Handle request to get chat presence status.

        Args:
            request: Flask reque`
- Code: `def handle_get_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 128** (high): docstring_param_mismatch
- Comment: `
        Handle request to list all chat presences.

        Args:
            request: Flask reques`
- Code: `def handle_list(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 77** (high): comment_return_mismatch
- Comment: `For now, return success - full implementation would update config`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\web\contract_handlers.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Handle request to get system contract status.

        Args:
            request: Flask req`
- Code: `def handle_get_system_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 52** (high): docstring_param_mismatch
- Comment: `
        Handle request to get agent contract status.

        Args:
            request: Flask requ`
- Code: `def handle_get_agent_status(self, request, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 78** (high): docstring_param_mismatch
- Comment: `
        Handle request to get next available task.

        Args:
            request: Flask reques`
- Code: `def handle_get_next_task(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\coordination_handlers.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Handle request to get task coordination status.

        Args:
            request: Flask r`
- Code: `def handle_get_task_coordination_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 58** (high): docstring_param_mismatch
- Comment: `
        Handle request to execute task coordination.

        Args:
            request: Flask requ`
- Code: `def handle_execute_task_coordination(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 90** (high): docstring_param_mismatch
- Comment: `
        Handle request to coordinate a specific task.
        
        Args:
            request: F`
- Code: `def handle_coordinate_task(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 123** (high): docstring_param_mismatch
- Comment: `
        Handle request to resolve coordination conflicts.
        
        Args:
            reques`
- Code: `def handle_resolve_coordination(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\core_handlers.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Handle request to get agent lifecycle status.

        Args:
            request: Flask req`
- Code: `def handle_get_agent_lifecycle_status(self, request, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 62** (high): docstring_param_mismatch
- Comment: `
        Handle request to start agent lifecycle cycle.

        Args:
            request: Flask re`
- Code: `def handle_start_cycle(self, request, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 86** (high): docstring_param_mismatch
- Comment: `
        Handle request to get message queue status.

        Args:
            request: Flask reque`
- Code: `def handle_get_message_queue_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\discord_handlers.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Handle request to get swarm tasks information.

        Args:
            request: Flask re`
- Code: `def handle_get_swarm_tasks(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Handle request to get broadcast templates.

        Args:
            request: Flask reques`
- Code: `def handle_get_broadcast_templates(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Handle request to get control panel status.

        Args:
            request: Flask reque`
- Code: `def handle_get_control_panel_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\engines_routes.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
    Get engine discovery status.
    
    Returns:
        JSON with engines list, summary, and dis`
- Code: `def get_engine_discovery()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 106** (high): docstring_param_mismatch
- Comment: `
    Get details for a specific engine.
    
    Args:
        engine_type: Type of engine (e.g., "a`
- Code: `def get_engine_details(engine_type)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'engine_type'}

**Line 149** (high): docstring_param_mismatch
- Comment: `
    Initialize a specific engine.
    
    Args:
        engine_type: Type of engine to initialize
`
- Code: `def initialize_engine(engine_type)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'engine_type'}

**Line 266** (high): docstring_param_mismatch
- Comment: `
    Cleanup a specific engine.
    
    Args:
        engine_type: Type of engine to cleanup
    `
- Code: `def cleanup_engine(engine_type)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'engine_type'}

### src\web\integrations_handlers.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Handle Jarvis conversation request.

        Args:
            request: Flask request objec`
- Code: `def handle_jarvis_conversation(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Handle Jarvis vision request.

        Args:
            request: Flask request object

   `
- Code: `def handle_jarvis_vision(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\messaging_handlers.py

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Handle request to parse messaging CLI command.
        
        Args:
            request: `
- Code: `def handle_parse_cli(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 90** (high): docstring_param_mismatch
- Comment: `
        Handle request to get CLI help documentation.
        
        Args:
            request: F`
- Code: `def handle_get_cli_help(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 125** (high): docstring_param_mismatch
- Comment: `
        Handle request to execute messaging CLI command.
        
        Args:
            request`
- Code: `def handle_execute_cli(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 169** (high): docstring_param_mismatch
- Comment: `
        Handle request to list available messaging templates.
        
        Args:
            re`
- Code: `def handle_list_templates(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 210** (high): docstring_param_mismatch
- Comment: `
        Handle request to render messaging template with variables.
        
        Args:
        `
- Code: `def handle_render_template(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 277** (high): docstring_param_mismatch
- Comment: `
        Handle request to get specific template by name.
        
        Args:
            request`
- Code: `def handle_get_template(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\monitoring_handlers.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Handle request to get monitoring status.

        Args:
            request: Flask request `
- Code: `def handle_get_monitoring_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 62** (high): docstring_param_mismatch
- Comment: `
        Handle request to initialize monitoring.

        Args:
            request: Flask request `
- Code: `def handle_initialize_monitoring(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 82** (high): comment_return_mismatch
- Comment: `For web integration, return success message`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\web\pipeline_handlers.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Handle request to get gas pipeline system status.
        
        Args:
            reques`
- Code: `def handle_get_gas_pipeline_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 70** (high): docstring_param_mismatch
- Comment: `
        Handle request to monitor and send gas to agents.
        
        Args:
            reques`
- Code: `def handle_monitor_gas_pipeline(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 98** (high): docstring_param_mismatch
- Comment: `
        Handle request to get gas status for specific agent.
        
        Args:
            req`
- Code: `def handle_get_agent_gas_status(self, request, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\portfolio_handlers.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
        Handle request to list all portfolios.
        
        Args:
            request: Flask re`
- Code: `def handle_list_portfolios(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
        Handle request to create a new portfolio.
        
        Args:
            request: Flask`
- Code: `def handle_create_portfolio(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\repository_merge_routes.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
    Get repository merge status overview.
    
    Returns:
        JSON with status summary, repo `
- Code: `def get_merge_status()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 117** (high): docstring_param_mismatch
- Comment: `
    Get status for a specific repository.
    
    Args:
        repo_name: Repository name (normal`
- Code: `def get_repo_status(repo_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'repo_name'}

**Line 310** (high): docstring_param_mismatch
- Comment: `
    Get merge attempt history.
    
    Query params:
        - source_repo: Filter by source repos`
- Code: `def get_merge_attempts()`
- Issue: Docstring params don't match: missing={'source_repo', 'error_type', 'success', 'target_repo'}, extra=set()

### src\web\scheduler_handlers.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Handle request to get scheduler status.

        Args:
            request: Flask request o`
- Code: `def handle_get_scheduler_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Handle request to schedule a task.

        Args:
            request: Flask request object`
- Code: `def handle_schedule_task(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\services_handlers.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Handle request to get chat presence status.

        Args:
            request: Flask reque`
- Code: `def handle_get_chat_presence_status(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Handle request to start chat presence.

        Args:
            request: Flask request ob`
- Code: `def handle_start_chat_presence(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Handle request to stop chat presence.

        Args:
            request: Flask request obj`
- Code: `def handle_stop_chat_presence(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\task_handlers.py

**Line 49** (high): docstring_param_mismatch
- Comment: `
        Handle task assignment request.

        Args:
            request: Flask request object

 `
- Code: `def handle_assign_task(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 106** (high): docstring_param_mismatch
- Comment: `
        Handle task completion request.

        Args:
            request: Flask request object

 `
- Code: `def handle_complete_task(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 90** (high): comment_return_mismatch
- Comment: `Return response`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 149** (high): comment_return_mismatch
- Comment: `Return response`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\web\vector_database\unified_middleware.py

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Rate limiting decorator.

        Note: Simplified implementation. In production, use Redis`
- Code: `def rate_limit(self, max_requests, window_seconds)`
- Issue: Docstring params don't match: missing={'Note'}, extra={'window_seconds', 'self', 'max_requests'}

**Line 153** (high): docstring_param_mismatch
- Comment: `
        Response caching decorator.

        Note: Simplified implementation. In production, use Re`
- Code: `def cache_response(self, ttl_seconds)`
- Issue: Docstring params don't match: missing={'Note'}, extra={'ttl_seconds', 'self'}

### src\web\vision_handlers.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Handle request to analyze color in image.

        Args:
            request: Flask request`
- Code: `def handle_analyze_color(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\web\workflow_handlers.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Handle request to execute a workflow.

        Args:
            request: Flask request obj`
- Code: `def handle_execute_workflow(self, request)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

**Line 68** (high): docstring_param_mismatch
- Comment: `
        Handle request to get workflow status.

        Args:
            request: Flask request ob`
- Code: `def handle_get_workflow_status(self, request, workflow_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'request'}

### src\workflows\engine.py

**Line 64** (high): docstring_param_mismatch
- Comment: `
        Initialize workflow engine.

        Args:
            workflow_name: Unique identifier for`
- Code: `def __init__(self, workflow_name, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'workflow_name', 'self'}

**Line 332** (high): docstring_param_mismatch
- Comment: `
        Restore workflow state from saved data.
        
        Args:
            state_data: Dict`
- Code: `def restore_state(self, state_data)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'state_data', 'self'}

**Line 200** (high): comment_return_mismatch
- Comment: `Execute GPT step (returns AIResponse directly)`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### src\workflows\gpt_integration.py

**Line 46** (high): docstring_param_mismatch
- Comment: `
        Initialize GPT workflow integration.
        
        Args:
            config: Configurati`
- Code: `def __init__(self, config)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'config'}

**Line 81** (high): docstring_param_mismatch
- Comment: `
        Execute a workflow step using GPT API.
        
        Args:
            step: Workflow st`
- Code: `def execute_gpt_step(self, step, workflow_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'self', 'step'}

**Line 155** (high): docstring_param_mismatch
- Comment: `
        Create a builder for GPT-powered workflow steps.
        
        Returns:
            GPTS`
- Code: `def create_gpt_step_builder(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 173** (high): docstring_param_mismatch
- Comment: `
        Initialize GPT step builder.
        
        Args:
            integration: GPTWorkflowInt`
- Code: `def __init__(self, integration)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'integration', 'self'}

**Line 184** (high): docstring_param_mismatch
- Comment: `
        Create a GPT-powered workflow step.
        
        Args:
            name: Step name
    `
- Code: `def create_gpt_step(self, name, description, prompt, response_type, timeout_seconds, dependencies, metadata)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'name'}

**Line 240** (high): docstring_param_mismatch
- Comment: `
    Get or create global GPT workflow integration instance.
    
    Args:
        config: Optional`
- Code: `def get_gpt_integration(config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

### src\workflows\steps.py

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Create a conversation loop between two agents.

        Args:
            agent_a: First ag`
- Code: `def create_conversation_loop(self, agent_a, agent_b, topic, iterations, timeout_per_round)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_a', 'self'}

**Line 145** (high): docstring_param_mismatch
- Comment: `
        Create multi-agent orchestration workflow.

        Args:
            task: Task descriptio`
- Code: `def create_multi_agent_orchestration(self, task, agents, strategy, timeout_per_agent)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 218** (high): docstring_param_mismatch
- Comment: `
        Create decision tree workflow.

        Args:
            decision_point: Description of th`
- Code: `def create_decision_tree(self, decision_point, branches, decision_agent, analysis_timeout, branch_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'decision_point'}

**Line 285** (high): docstring_param_mismatch
- Comment: `
        Create autonomous workflow loop.

        Args:
            goal: Goal to work towards
    `
- Code: `def create_autonomous_loop(self, goal, max_iterations, assessment_agent, action_agent, assessment_timeout, action_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'goal'}

### src\workflows\strategies.py

**Line 53** (medium): docstring_return_mismatch
- Comment: `
        Check if a step can be executed with this strategy.

        Args:
            step: Step t`
- Code: `def can_execute_step(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Check if a step can be executed with this strategy.

        Args:
            step: Step t`
- Code: `def can_execute_step(self, step, completed_steps, failed_steps)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'step'}

### swarm_brain\agent_field_manual\automation\cycle_health_check.py

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Initialize cycle health checker
        
        Args:
            max_age_minutes: Maximum`
- Code: `def __init__(self, max_age_minutes)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'max_age_minutes'}

**Line 67** (high): docstring_param_mismatch
- Comment: `
        Validate agent ready for cycle start
        
        Checks:
        - status.json exists `
- Code: `def pre_cycle_check(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 118** (high): docstring_param_mismatch
- Comment: `
        Validate cycle completion
        
        Checks:
        - status.json updated with new t`
- Code: `def post_cycle_check(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

### swarm_brain\agent_field_manual\automation\database_sync_lifecycle.py

**Line 60** (high): docstring_param_mismatch
- Comment: `
        Initialize database sync lifecycle manager
        
        Args:
            agent_id: Age`
- Code: `def __init__(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 78** (high): docstring_param_mismatch
- Comment: `
        Pull latest status from database → status.json
        
        Called at the beginning of `
- Code: `def sync_on_cycle_start(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 115** (high): docstring_param_mismatch
- Comment: `
        Push status.json → database
        
        Called at the end of each agent cycle to persi`
- Code: `def sync_on_cycle_end(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 155** (high): docstring_param_mismatch
- Comment: `
        Check consistency between status.json and database
        
        Returns:
            Di`
- Code: `def validate_consistency(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 260** (high): docstring_param_mismatch
- Comment: `
        Pull agent status from database.
        
        Returns:
            Agent status diction`
- Code: `def _pull_from_database(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 288** (high): docstring_param_mismatch
- Comment: `
        Push agent status to database.
        
        Args:
            status: Agent status dict`
- Code: `def _push_to_database(self, status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'status'}

### systems\output_flywheel\dashboard_loader.py

**Line 220** (high): comment_return_mismatch
- Comment: `888', callback: function(value) {{ return value + '%'; }} }},`
- Code: `ticks: {{ color: '`
- Issue: Comment says 'returns' but code doesn't return

### systems\output_flywheel\integration\agent_session_hooks.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Initialize session hook.
        
        Args:
            agent_id: Agent identifier (e.g`
- Code: `def __init__(self, agent_id, workspace_root)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'agent_id'}

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Assemble work_session.json from agent session data.
        
        Args:
            sess`
- Code: `def assemble_work_session(self, session_type, metadata, source_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'session_type', 'self'}

**Line 101** (high): docstring_param_mismatch
- Comment: `
        Save work_session.json to disk.
        
        Args:
            session: Work session da`
- Code: `def save_session(self, session)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session'}

**Line 120** (high): docstring_param_mismatch
- Comment: `
        Trigger Output Flywheel pipeline for session.
        
        Args:
            session_fi`
- Code: `def trigger_pipeline(self, session_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'session_file', 'self'}

**Line 158** (high): docstring_param_mismatch
- Comment: `
        Complete end-of-session workflow: assemble, save, and trigger pipeline.
        
        Ar`
- Code: `def end_of_session(self, session_type, metadata, source_data, auto_trigger)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'workflow', 'Args'}, extra={'session_type', 'self'}

**Line 207** (high): docstring_param_mismatch
- Comment: `
        Auto-collect session metadata from status.json.
        
        Args:
            status_d`
- Code: `def _collect_session_metadata(self, status_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'status_data'}

**Line 237** (high): docstring_param_mismatch
- Comment: `
        Auto-collect git data from repository.
        
        Returns:
            Source data di`
- Code: `def _collect_git_data(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 322** (high): docstring_param_mismatch
- Comment: `
    Convenience function for end-of-session integration.
    
    Usage:
        from systems.outpu`
- Code: `def end_of_session_hook(agent_id, session_type, metadata, source_data, auto_trigger)`
- Issue: Docstring params don't match: missing={'Usage', 'Returns', 'Args'}, extra={'session_type', 'agent_id'}

### systems\output_flywheel\integration\status_json_integration.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
        Initialize status.json integration.
        
        Args:
            agent_id: Agent iden`
- Code: `def __init__(self, agent_id, workspace_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 47** (high): docstring_param_mismatch
- Comment: `
        Check status.json for significant changes and trigger Output Flywheel if needed.
        
 `
- Code: `def check_and_trigger(self, force)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'force', 'self'}

**Line 87** (high): docstring_param_mismatch
- Comment: `
        Infer session type from status.json.
        
        Args:
            status_data: Agent `
- Code: `def _infer_session_type(self, status_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'status_data'}

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Determine if Output Flywheel should be triggered.
        
        Args:
            status`
- Code: `def _should_trigger(self, status_data, session_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'status_data'}

**Line 138** (high): docstring_param_mismatch
- Comment: `
        Generate hash of status.json for change detection.
        
        Args:
            statu`
- Code: `def _hash_status(self, status_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'status_data'}

**Line 161** (high): docstring_param_mismatch
- Comment: `
        Update status.json with generated artifact paths.
        
        Args:
            artifa`
- Code: `def update_status_with_artifacts(self, artifacts, session_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'artifacts'}

**Line 207** (high): docstring_param_mismatch
- Comment: `
    Convenience function to check status.json and auto-trigger Output Flywheel.
    
    Usage:
   `
- Code: `def auto_trigger_on_status_update(agent_id)`
- Issue: Docstring params don't match: missing={'Usage', 'Returns', 'Args'}, extra={'agent_id'}

### systems\output_flywheel\manifest_system.py

**Line 26** (high): docstring_param_mismatch
- Comment: `
        Initialize manifest system.
        
        Args:
            manifest_path: Path to manif`
- Code: `def __init__(self, manifest_path)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'manifest_path'}

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Register a work session in the manifest.
        
        Args:
            session_id: Uni`
- Code: `def register_session(self, session_id, session_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 99** (high): docstring_param_mismatch
- Comment: `
        Register an artifact in the manifest.
        
        Args:
            session_id: Sessio`
- Code: `def register_artifact(self, session_id, artifact_type, artifact_path, artifact_hash)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'session_id'}

**Line 219** (high): docstring_param_mismatch
- Comment: `
        Verify SSOT compliance of the manifest system.
        
        Returns:
            Compli`
- Code: `def verify_ssot_compliance(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 261** (high): docstring_param_mismatch
- Comment: `
    Calculate SHA256 hash of artifact file for duplicate detection.
    
    Args:
        artifact`
- Code: `def calculate_artifact_hash(artifact_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'artifact_path'}

### systems\output_flywheel\processors\build_log_generator.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
    Generate a build-log markdown file for the given session.

    Args:
        session: work_sess`
- Code: `def generate_build_log(session, repo_stats, output_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'session'}

### systems\output_flywheel\processors\readme_generator.py

**Line 50** (high): docstring_param_mismatch
- Comment: `
    Generate README.md using the configured template and data.

    Args:
        config: ReadmeCon`
- Code: `def generate_readme(config, story, repo_stats, extra)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'config'}

### systems\output_flywheel\processors\repo_scanner.py

**Line 154** (high): docstring_param_mismatch
- Comment: `
    Public entry point for S1: Repo Scan.

    - If GitPython is available and `use_git` is True, u`
- Code: `def scan_repo(repo_path, use_git, max_commits)`
- Issue: Docstring params don't match: missing={'S1'}, extra={'use_git', 'repo_path', 'max_commits'}

### systems\output_flywheel\processors\story_extractor.py

**Line 108** (high): docstring_param_mismatch
- Comment: `
    Main S2 entry point: extract a StorySummary from a work_session dict.
    `
- Code: `def extract_story_from_session(session)`
- Issue: Docstring params don't match: missing={'point'}, extra={'session'}

### systems\output_flywheel\publication\github_publisher.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Run git command with enhanced error messages.
        
        Args:
            command: G`
- Code: `def _run_git_command(self, command, cwd)`
- Issue: Docstring params don't match: missing={'default', 'output', 'success', 'Args', 'Returns'}, extra={'self', 'command'}

**Line 86** (high): docstring_param_mismatch
- Comment: `
        Update README.md in repository with enhanced error messages.
        
        Args:
       `
- Code: `def update_readme(self, readme_path, commit_message)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'readme_path', 'self'}

### systems\output_flywheel\ssot_verifier.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Initialize SSOT verifier.
        
        Args:
            base_path: Base path to output`
- Code: `def __init__(self, base_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'base_path'}

**Line 204** (high): docstring_param_mismatch
- Comment: `
        Run all SSOT verification checks.
        
        Returns:
            Comprehensive SSOT `
- Code: `def verify_all(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### systems\output_flywheel\unified_metrics_reader.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
        Initialize unified metrics reader.
        
        Args:
            metrics_export_path: `
- Code: `def __init__(self, metrics_export_path)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'metrics_export_path'}

**Line 50** (high): docstring_param_mismatch
- Comment: `
        Read unified metrics from JSON file.
        
        Returns:
            Unified metrics `
- Code: `def read_metrics_from_file(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Get unified metrics (from file or fresh export).
        
        Args:
            force_e`
- Code: `def get_metrics(self, force_export)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'force_export'}

**Line 107** (high): docstring_param_mismatch
- Comment: `
        Export fresh unified metrics.
        
        Args:
            output_path: Output file p`
- Code: `def export_fresh_metrics(self, output_path)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'output_path', 'self'}

### systems\output_flywheel\unified_tools_dashboard.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Initialize dashboard generator.
        
        Args:
            output_path: Path to out`
- Code: `def __init__(self, output_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'output_path', 'self'}

### systems\output_flywheel\unified_tools_metrics.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
        Initialize metrics tracker.
        
        Args:
            data_dir: Directory for stor`
- Code: `def __init__(self, data_dir)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'data_dir'}

**Line 74** (high): docstring_param_mismatch
- Comment: `
        Track tool usage.
        
        Args:
            tool_name: Name of the tool (e.g., "un`
- Code: `def track_tool_usage(self, tool_name, category, success, execution_time)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'tool_name', 'self'}

### systems\technical_debt\daily_report_generator.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Generate daily progress report.
        
        Args:
            report_time: "morning" o`
- Code: `def generate_daily_report(self, report_time)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'report_time'}

### tests\discord\test_agent_name_validation.py

**Line 94** (medium): docstring_return_mismatch
- Comment: `Test that get_all_agent_names returns only valid agents.`
- Code: `def test_get_all_agent_names(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 78** (high): comment_raise_mismatch
- Comment: `Skip None for is_valid_agent (it will raise TypeError)`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\discord\test_discord_service.py

**Line 336** (medium): docstring_return_mismatch
- Comment: `Test get_discord_service returns singleton instance.`
- Code: `def test_get_discord_service_singleton(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\fixtures\trader_replay\session_fixtures.py

**Line 13** (high): docstring_param_mismatch
- Comment: `
    Create deterministic test candles.

    Args:
        count: Number of candles to create
      `
- Code: `def create_test_candles(count, base_price)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'count'}

**Line 52** (high): docstring_param_mismatch
- Comment: `
    Create a "disciplined" session fixture.

    Characteristics:
    - Proper stop loss usage
    `
- Code: `def create_disciplined_session_fixture()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 115** (high): docstring_param_mismatch
- Comment: `
    Create a "chaotic" session fixture.

    Characteristics:
    - No stop losses
    - Overtradin`
- Code: `def create_chaotic_session_fixture()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 194** (high): docstring_param_mismatch
- Comment: `
    Create minimal test session data.

    Args:
        symbol: Trading symbol
        session_dat`
- Code: `def create_test_session_data(symbol, session_date, candle_count)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'symbol'}

### tests\integration\test_ci_workflow_tdd.py

**Line 21** (high): docstring_param_mismatch
- Comment: `TDD: All workflows should handle missing requirements gracefully.`
- Code: `def test_all_workflows_have_conditional_requirements()`
- Issue: Docstring params don't match: missing={'TDD'}, extra=set()

**Line 55** (high): docstring_param_mismatch
- Comment: `TDD: All test steps should have continue-on-error or conditional checks.`
- Code: `def test_all_test_steps_have_continue_on_error()`
- Issue: Docstring params don't match: missing={'TDD'}, extra=set()

**Line 95** (high): docstring_param_mismatch
- Comment: `TDD: All install steps should check for file existence.`
- Code: `def test_all_install_steps_handle_missing_files()`
- Issue: Docstring params don't match: missing={'TDD'}, extra=set()

**Line 121** (high): docstring_param_mismatch
- Comment: `TDD: Coverage threshold should be achievable (50% or lower for initial setup).`
- Code: `def test_coverage_threshold_is_realistic()`
- Issue: Docstring params don't match: missing={'TDD'}, extra=set()

### tests\integration\test_messaging_templates_integration.py

**Line 411** (high): comment_raise_mismatch
- Comment: `Should not raise KeyError from template formatting`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 574** (high): comment_raise_mismatch
- Comment: `Should not raise KeyError or formatting errors`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\integration\trader_replay\test_cli_smoke.py

**Line 331** (high): docstring_param_mismatch
- Comment: `Test complete workflow: create → start → step → pause → status.`
- Code: `def test_end_to_end_workflow(self, cli_command, temp_db)`
- Issue: Docstring params don't match: missing={'workflow'}, extra={'cli_command', 'self', 'temp_db'}

### tests\services\chat_presence\test_twitch_bridge_errors.py

**Line 135** (medium): docstring_return_mismatch
- Comment: `Test sending empty message returns False.`
- Code: `def test_send_message_with_empty_string(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 143** (medium): docstring_return_mismatch
- Comment: `Test sending None message returns False.`
- Code: `def test_send_message_with_none(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 162** (medium): docstring_return_mismatch
- Comment: `Test sending message when not connected returns False.`
- Code: `def test_send_message_when_not_connected(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 172** (medium): docstring_return_mismatch
- Comment: `Test sending message when not running returns False.`
- Code: `def test_send_message_when_not_running(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 182** (medium): docstring_return_mismatch
- Comment: `Test sending message without bot instance returns False.`
- Code: `def test_send_message_without_bot(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\test_engine_registry_plugin_discovery.py

**Line 94** (medium): docstring_return_mismatch
- Comment: `Test that same engine type returns same instance.`
- Code: `def test_engine_singleton_behavior(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 103** (medium): docstring_return_mismatch
- Comment: `Test that get_engine_types returns a list.`
- Code: `def test_get_engine_types_returns_list(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 138** (high): comment_return_mismatch
- Comment: `Should accept EngineContext and return bool`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 151** (high): comment_return_mismatch
- Comment: `Should accept EngineContext and payload, return EngineResult`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 166** (high): comment_return_mismatch
- Comment: `Should accept EngineContext and return bool`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 175** (high): comment_return_mismatch
- Comment: `Should return dict`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\unit\core\engines\test_registry_discovery.py

**Line 71** (medium): docstring_return_mismatch
- Comment: `Test that get_engine creates and returns engine instance.`
- Code: `def test_get_engine_creates_instance(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 214** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\core\file_locking\test_chain3_redirect_shim.py

**Line 107** (high): docstring_param_mismatch
- Comment: `Test old import: from file_locking_engine_base import file_locking_engine_base.`
- Code: `def test_old_import_pattern_1(self)`
- Issue: Docstring params don't match: missing={'import'}, extra={'self'}

**Line 116** (high): docstring_param_mismatch
- Comment: `Test old import: from file_locking import file_locking_engine_base.`
- Code: `def test_old_import_pattern_2(self)`
- Issue: Docstring params don't match: missing={'import'}, extra={'self'}

**Line 125** (high): docstring_param_mismatch
- Comment: `Test old import: from file_locking_engine_base import FileLockEngineBase.`
- Code: `def test_old_import_pattern_3(self)`
- Issue: Docstring params don't match: missing={'import'}, extra={'self'}

### tests\unit\core\managers\test_core_service_manager.py

**Line 49** (medium): docstring_return_mismatch
- Comment: `Test is_initialized returns False before initialization.`
- Code: `def test_is_initialized_false(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 54** (medium): docstring_return_mismatch
- Comment: `Test is_initialized returns True after initialization.`
- Code: `def test_is_initialized_true(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\core\test_config_ssot.py

**Line 59** (medium): docstring_return_mismatch
- Comment: `Test get_config returns default when env var not set.`
- Code: `def test_get_config_with_default(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 111** (high): comment_return_mismatch
- Comment: `validate_config returns list of errors (empty if valid)`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 444** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\domain\test_browser_port.py

**Line 148** (medium): docstring_return_mismatch
- Comment: `Test is_ready returns correct state.`
- Code: `def test_is_ready_returns_correct_state(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\domain\test_message_bus_port.py

**Line 200** (medium): docstring_return_mismatch
- Comment: `Test unsubscribing non-existent handler returns False.`
- Code: `def test_unsubscribe_not_found_returns_false(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 237** (medium): docstring_return_mismatch
- Comment: `Test is_available returns True when available.`
- Code: `def test_is_available_returns_true(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 242** (medium): docstring_return_mismatch
- Comment: `Test is_available returns False when not available.`
- Code: `def test_is_available_returns_false(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 255** (medium): docstring_return_mismatch
- Comment: `Test get_stats returns correct statistics.`
- Code: `def test_get_stats_returns_correct_data(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\browser\test_thea_browser_service.py

**Line 25** (medium): docstring_return_mismatch
- Comment: `Test get_driver returns driver instance.`
- Code: `def test_thea_browser_service_get_driver(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\browser\test_unified_cookie_manager.py

**Line 62** (high): comment_return_mismatch
- Comment: `_load_persisted_cookies returns False on error, cookies dict otherwise`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\unit\infrastructure\logging\test_std_logger.py

**Line 29** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 35** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 41** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 47** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 53** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 59** (high): comment_raise_mismatch
- Comment: `Should not raise exception - use non-conflicting context keys`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\infrastructure\logging\test_unified_logger.py

**Line 37** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 44** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 51** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 58** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 65** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 72** (high): comment_raise_mismatch
- Comment: `Should not raise exception - use non-conflicting context keys`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\infrastructure\persistence\test_agent_repository.py

**Line 70** (medium): docstring_return_mismatch
- Comment: `Test get nonexistent agent returns None.`
- Code: `def test_agent_repository_get_nonexistent_agent(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 87** (medium): docstring_return_mismatch
- Comment: `Test list_all returns all agents.`
- Code: `def test_agent_repository_list_all_agents(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 111** (medium): docstring_return_mismatch
- Comment: `Test get_active returns only active agents.`
- Code: `def test_agent_repository_get_active_agents(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\persistence\test_persistence_statistics.py

**Line 29** (medium): docstring_return_mismatch
- Comment: `Test get_database_stats returns comprehensive stats.`
- Code: `def test_persistence_statistics_get_database_stats(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\persistence\test_task_repository.py

**Line 78** (medium): docstring_return_mismatch
- Comment: `Test get nonexistent task returns None.`
- Code: `def test_task_repository_get_nonexistent_task(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 97** (medium): docstring_return_mismatch
- Comment: `Test list_all returns all tasks.`
- Code: `def test_task_repository_list_all_tasks(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 122** (medium): docstring_return_mismatch
- Comment: `Test get_pending returns only pending tasks.`
- Code: `def test_task_repository_get_pending_tasks(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 74** (high): comment_return_mismatch
- Comment: `This is a repository implementation detail - just verify it returns something`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 99** (high): comment_return_mismatch
- Comment: `Mock _row_to_task to return TaskPersistenceModel instances`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 124** (high): comment_return_mismatch
- Comment: `Mock _row_to_task to return TaskPersistenceModel instance`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\unit\infrastructure\test_dependency_injection.py

**Line 20** (medium): docstring_return_mismatch
- Comment: `Test get_dependencies returns dictionary of dependencies.`
- Code: `def test_get_dependencies_returns_dict(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 33** (medium): docstring_return_mismatch
- Comment: `Test get_dependencies returns same instances on multiple calls.`
- Code: `def test_get_dependencies_returns_singleton_instances(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\test_unified_browser_service.py

**Line 47** (high): comment_return_mismatch
- Comment: `Browser adapter stub returns False by default`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 54** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\infrastructure\test_unified_logging_time.py

**Line 40** (medium): docstring_return_mismatch
- Comment: `Test get_logger returns logger instance.`
- Code: `def test_unified_logging_time_service_get_logger(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 71** (medium): docstring_return_mismatch
- Comment: `Test now() returns current time.`
- Code: `def test_unified_logging_time_service_now(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\test_unified_persistence.py

**Line 62** (medium): docstring_return_mismatch
- Comment: `Test list_agents returns list of agents.`
- Code: `def test_unified_persistence_service_list_agents(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 71** (medium): docstring_return_mismatch
- Comment: `Test list_tasks returns list of tasks.`
- Code: `def test_unified_persistence_service_list_tasks(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 79** (medium): docstring_return_mismatch
- Comment: `Test get_database_stats returns statistics.`
- Code: `def test_unified_persistence_service_get_database_stats(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\time\test_system_clock.py

**Line 26** (medium): docstring_return_mismatch
- Comment: `Test now() returns current time.`
- Code: `def test_system_clock_now(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 33** (medium): docstring_return_mismatch
- Comment: `Test utcnow() returns UTC time.`
- Code: `def test_system_clock_utc_now(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\infrastructure\time\test_system_clock_extended.py

**Line 24** (medium): docstring_return_mismatch
- Comment: `Test utcnow returns UTC datetime.`
- Code: `def test_system_clock_utcnow(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\quality\test_proof_ledger.py

**Line 26** (medium): docstring_return_mismatch
- Comment: `Test _git_head returns commit hash when git is available.`
- Code: `def test_git_head_success(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 34** (medium): docstring_return_mismatch
- Comment: `Test _git_head returns 'unknown' when git fails.`
- Code: `def test_git_head_failure(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\services\test_extractor_message_parser.py

**Line 228** (high): comment_raise_mismatch
- Comment: `Make extract_messages raise an exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\services\test_extractor_storage.py

**Line 167** (high): comment_return_mismatch
- Comment: `Mock time.time() to return current time`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\unit\services\test_session.py

**Line 89** (high): comment_return_mismatch
- Comment: `Should return None since we can't actually create a context without Playwright`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 171** (high): comment_return_mismatch
- Comment: `When disabled, is_session_valid returns True`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 182** (high): comment_return_mismatch
- Comment: `Returns False if session doesn't exist`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\unit\services\trader_replay\test_behavioral_scoring.py

**Line 176** (medium): docstring_return_mismatch
- Comment: `Test calculate_all_scores returns all score types.`
- Code: `def test_calculate_all_scores(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\services\trader_replay\test_repositories.py

**Line 76** (medium): docstring_return_mismatch
- Comment: `Test getting a non-existent session returns None.`
- Code: `def test_get_nonexistent_session(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 96** (medium): docstring_return_mismatch
- Comment: `Test listing sessions with non-existent symbol returns empty list.`
- Code: `def test_list_sessions_filtered_by_nonexistent_symbol(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 112** (medium): docstring_return_mismatch
- Comment: `Test updating non-existent session returns False.`
- Code: `def test_update_nonexistent_session_status(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 190** (medium): docstring_return_mismatch
- Comment: `Test getting non-existent trade returns None.`
- Code: `def test_get_nonexistent_trade(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 215** (medium): docstring_return_mismatch
- Comment: `Test listing trades for session with no trades returns empty list.`
- Code: `def test_list_trades_empty_session(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 249** (medium): docstring_return_mismatch
- Comment: `Test updating trade without ID returns False.`
- Code: `def test_update_trade_without_id(...)`
- Issue: Docstring mentions return but function has no return statement

### tests\unit\swarm_brain\test_agent_notes.py

**Line 230** (medium): docstring_return_mismatch
- Comment: `Test get_notes returns all notes.`
- Code: `def test_get_notes_returns_all(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 378** (high): comment_raise_mismatch
- Comment: `Should not raise exception (error handling in real implementation)`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

**Line 393** (high): comment_raise_mismatch
- Comment: `Should not raise exception`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\swarm_brain\test_swarm_memory.py

**Line 261** (high): comment_raise_mismatch
- Comment: `Should not raise error`
- Code: ``
- Issue: Comment says 'raises' but code doesn't raise

### tests\unit\systems\test_output_flywheel_integration.py

**Line 105** (high): comment_return_mismatch
- Comment: `Configure mock to return different results for different calls`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\unit\systems\test_output_flywheel_pipelines.py

**Line 222** (high): comment_return_mismatch
- Comment: `Returns StorySummary object, not dict`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tests\utils\discord_test_utils.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
    Setup Discord module mocks before importing Discord-related code.
    
    This must be called `
- Code: `def setup_discord_mocks()`
- Issue: Docstring params don't match: missing={'Usage'}, extra=set()

**Line 65** (high): docstring_param_mismatch
- Comment: `
    Create a mock Discord bot instance.
    
    Args:
        display_name: Bot display name
     `
- Code: `def create_mock_discord_bot(display_name, user_id, guilds)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'display_name'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
    Create a mock Discord context (commands.Context).
    
    Args:
        user_display_name: Use`
- Code: `def create_mock_discord_context(user_display_name, user_id, channel_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'user_display_name'}

**Line 117** (high): docstring_param_mismatch
- Comment: `
    Create a mock Discord interaction.
    
    Args:
        user_display_name: User display name
`
- Code: `def create_mock_discord_interaction(user_display_name, user_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'user_display_name'}

**Line 143** (high): docstring_param_mismatch
- Comment: `
    Create a mock messaging service.
    
    Args:
        service_class: Service class to spec (o`
- Code: `def create_mock_messaging_service(service_class, send_message_return, broadcast_message_return, agent_data)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'service_class'}

**Line 187** (high): docstring_param_mismatch
- Comment: `
    Create a mock messaging controller.
    
    Args:
        send_agent_message_return: Return va`
- Code: `def create_mock_messaging_controller(send_agent_message_return, broadcast_to_swarm_return, get_agent_status_return)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'send_agent_message_return'}

**Line 219** (high): docstring_param_mismatch
- Comment: `
    Create a mock Discord embed.
    
    Args:
        title: Embed title
        description: Emb`
- Code: `def create_mock_discord_embed(title, description, color)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'title'}

**Line 246** (high): docstring_param_mismatch
- Comment: `
    Create a mock Discord view.
    
    Returns:
        Mock Discord view
    `
- Code: `def create_mock_discord_view()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 259** (high): docstring_param_mismatch
- Comment: `
    Create a mock Discord modal.
    
    Returns:
        Mock Discord modal
    `
- Code: `def create_mock_discord_modal()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### tools\activate_wordpress_theme.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
    Activate WordPress theme via browser automation.
    
    Args:
        site_url: Base site URL`
- Code: `def activate_theme(site_url, theme_name, auto_login, wait_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site_url'}

### tools\add_type_annotations.py

**Line 69** (high): comment_return_mismatch
- Comment: `Match function definitions without return type`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 76** (high): comment_return_mismatch
- Comment: `Skip if already has return type`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tools\agent_activity_detector.py

**Line 129** (high): docstring_param_mismatch
- Comment: `Initialize activity detector.
        
        Args:
            workspace_root: Root directory for `
- Code: `def __init__(self, workspace_root)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'workspace_root'}

**Line 140** (high): docstring_param_mismatch
- Comment: `
        Detect agent activity from all sources.
        
        Args:
            agent_id: Agent `
- Code: `def detect_agent_activity(self, agent_id, lookback_minutes, use_events, activity_threshold)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 260** (high): docstring_param_mismatch
- Comment: `
        Return True if agent is considered active within the window using telemetry first.

       `
- Code: `def is_active(self, agent_id, window_s, activity_threshold)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 1612** (high): docstring_param_mismatch
- Comment: `
        Find agents that are inactive.
        
        Args:
            inactivity_threshold_minu`
- Code: `def find_inactive_agents(self, inactivity_threshold_minutes, lookback_minutes)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'inactivity_threshold_minutes', 'self'}

### tools\agent_bump_script.py

**Line 53** (high): docstring_param_mismatch
- Comment: `
    Bump agent by clicking chat input and pressing shift+backspace.
    
    Args:
        agent_id`
- Code: `def bump_agent(agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

**Line 97** (high): docstring_param_mismatch
- Comment: `
    Bump multiple agents.
    
    Args:
        agent_ids: List of agent identifiers
        
    `
- Code: `def bump_agents(agent_ids)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_ids'}

**Line 115** (high): docstring_param_mismatch
- Comment: `
    Bump agents by number (1-8).
    
    Args:
        agent_numbers: List of agent numbers (1-8)
`
- Code: `def bump_agents_by_number(agent_numbers)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_numbers'}

### tools\agent_cycle_v2_report_validator.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Validate status.json against v2 cycle schema.
        
        Args:
            status_pat`
- Code: `def validate_status_json(self, status_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'status_path'}

### tools\agent_lifecycle_automator.py

**Line 203** (high): docstring_param_mismatch
- Comment: `Example: Multi-repo mission with full automation.`
- Code: `def main()`
- Issue: Docstring params don't match: missing={'Example'}, extra=set()

### tools\analysis\scan_technical_debt.py

**Line 44** (high): docstring_param_mismatch
- Comment: `
        Scan for technical debt.

        Args:
            marker_type: Specific marker to scan fo`
- Code: `def scan(self, marker_type, target_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'marker_type', 'self'}

### tools\architecture_review.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Request an architecture review.

    Args:
        files: List of files to review
        scope`
- Code: `def request_review(files, scope, agent)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'files'}

**Line 60** (high): docstring_param_mismatch
- Comment: `
    Provide an architecture review.

    Args:
        request_file: Path to review request
       `
- Code: `def provide_review(request_file, approval, comments)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'request_file'}

### tools\audit_imports.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Test if a module can be imported.
    
    Returns:
        (success: bool, error_message: str)`
- Code: `def test_import(module_path)`
- Issue: Docstring params don't match: missing={'success', 'error_message'}, extra={'module_path'}

### tools\auto_inbox_processor.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Extract metadata from message file.

        Returns:
            Message metadata dict
   `
- Code: `def parse_message_metadata(self, message_path)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'message_path', 'self'}

**Line 147** (high): docstring_param_mismatch
- Comment: `
        Process a single agent's inbox.

        Returns:
            Processing statistics
       `
- Code: `def process_inbox(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'agent_id'}

### tools\auto_learn_preferences.py

**Line 57** (high): docstring_param_mismatch
- Comment: `
        Learn from an interaction and update preferences automatically.
        
        Args:
    `
- Code: `def learn_from_interaction(self, message, response, response_quality, feedback, response_time_seconds)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self', 'response_quality'}

### tools\auto_status_updater.py

**Line 49** (high): docstring_param_mismatch
- Comment: `
        Update agent status with various activity types.

        Args:
            agent_id: Agent`
- Code: `def update_status(self, agent_id, activity, milestone, points, mission, task_complete, custom_fields)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 193** (high): docstring_param_mismatch
- Comment: `
        Automatically detect recent agent activity by scanning workspace.

        Returns:
       `
- Code: `def auto_detect_activity(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'agent_id'}

### tools\auto_validate_cycle_v2.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
    Auto-validate agent's cycle v2 and optionally attach to status.json.
    
    Args:
        age`
- Code: `def auto_validate_cycle_v2(agent_id, attach_to_status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### tools\auto_workspace_cleanup.py

**Line 93** (high): docstring_param_mismatch
- Comment: `
        Clean up a single agent's workspace.

        Returns:
            Cleanup statistics
     `
- Code: `def cleanup_agent_workspace(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'agent_id'}

### tools\browser_pool_manager.py

**Line 69** (high): docstring_param_mismatch
- Comment: `
        Initialize browser pool.

        Args:
            pool_size: Number of browser instances `
- Code: `def __init__(self, pool_size, max_lifetime_minutes, max_usage_per_instance, headless)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'pool_size', 'self'}

**Line 132** (high): docstring_param_mismatch
- Comment: `
        Acquire a browser instance from the pool.

        Returns:
            Browser driver inst`
- Code: `def acquire(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 167** (high): docstring_param_mismatch
- Comment: `
        Release a browser instance back to the pool.

        Args:
            driver: Browser dri`
- Code: `def release(self, driver)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'driver'}

**Line 181** (high): comment_return_mismatch
- Comment: `Return to pool if space available`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tools\captain_inbox_manager.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
    Categorize a message file.
    
    Args:
        file_path: Path to message file
        
    `
- Code: `def categorize_message(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 97** (high): docstring_param_mismatch
- Comment: `
    Analyze Captain's inbox.
    
    Args:
        inbox_path: Path to Agent-4 inbox
        
    `
- Code: `def analyze_inbox(inbox_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'inbox_path'}

### tools\check_wordpress_debug_log.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
    Check WordPress debug.log for errors.
    
    Args:
        site: Site key
        lines: Numb`
- Code: `def check_debug_log(site, lines)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\circular_import_detector.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Detect circular imports in codebase.

        Returns:
            List of cycles, each cyc`
- Code: `def detect(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools\cleanup\cleanup_obsolete_files.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
    Clean up obsolete files.

    Args:
        dry_run: If True, only show what would be deleted
 `
- Code: `def cleanup(dry_run, remove_replaced)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'dry_run'}

### tools\cleanup_old_merge_directories.py

**Line 16** (high): docstring_param_mismatch
- Comment: `
    Clean up old merge and conflict resolution directories.
    
    Args:
        base_path: Base `
- Code: `def cleanup_old_directories(base_path, days_old, dry_run)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'base_path'}

### tools\clear_wordpress_transients.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
    Clear WordPress transients via SQL command.
    
    Args:
        site: Site key
        
    `
- Code: `def clear_transients_via_sql(site)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

**Line 85** (high): docstring_param_mismatch
- Comment: `
    Clear WordPress transients via WP-CLI.
    
    Args:
        site: Site key
        
    Retur`
- Code: `def clear_transients_via_wpcli(site)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\cli\command_discovery.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Discover all CLI commands in tools directory.
        
        Returns:
            List of`
- Code: `def discover_commands(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 64** (high): docstring_param_mismatch
- Comment: `
        Analyze a Python file for CLI command patterns.
        
        Args:
            file_pat`
- Code: `def _analyze_file(self, file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'file_path'}

**Line 200** (high): docstring_param_mismatch
- Comment: `
        Generate Python code for command registry.
        
        Returns:
            Python cod`
- Code: `def generate_registry_code(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools\communication\agent_status_validator.py

**Line 42** (high): docstring_param_mismatch
- Comment: `Initialize validator.

        Args:
            workspace_root: Root workspace directory
          `
- Code: `def __init__(self, workspace_root, use_activity_detection)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'self', 'workspace_root'}

**Line 157** (high): docstring_param_mismatch
- Comment: `Verify agent has recent activity from multiple sources.

        Returns:
            Tuple of (is_a`
- Code: `def _verify_agent_activity(self, agent_id, status_timestamp)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'status_timestamp', 'agent_id'}

### tools\consolidation_executor.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Initialize consolidation executor.

        Args:
            consolidation_plan_path: Path`
- Code: `def __init__(self, consolidation_plan_path)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'consolidation_plan_path', 'self'}

**Line 81** (high): comment_return_mismatch
- Comment: `For now, return a structured plan based on Phase 1 execution approval`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tools\consolidation_strategy_reviewer.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
        Initialize strategy reviewer.
        
        Args:
            status_tracker: Optional R`
- Code: `def __init__(self, status_tracker)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'status_tracker'}

**Line 55** (high): docstring_param_mismatch
- Comment: `
        Validate consolidation direction makes sense.
        
        Args:
            source_rep`
- Code: `def validate_consolidation_direction(self, source_repo, target_repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'source_repo', 'self'}

**Line 105** (high): docstring_param_mismatch
- Comment: `
        Review a consolidation plan for issues.
        
        Args:
            plan: Consolidat`
- Code: `def review_consolidation_plan(self, plan)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'plan'}

**Line 141** (high): docstring_param_mismatch
- Comment: `
        Verify consolidation strategy consistency.
        
        Args:
            merges: List `
- Code: `def verify_strategy_consistency(self, merges)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'merges', 'self'}

**Line 202** (high): docstring_param_mismatch
- Comment: `
        Generate comprehensive strategy review report.
        
        Args:
            merges: L`
- Code: `def generate_strategy_report(self, merges)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'merges', 'self'}

### tools\coordination\discord_commands_tester.py

**Line 202** (high): docstring_param_mismatch
- Comment: `
    Test Discord commands directly in Discord using PyAutoGUI.
    
    Args:
        commands: Lis`
- Code: `def test_commands_in_discord(commands)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'commands'}

### tools\coordination\discord_simple_test.py

**Line 30** (high): docstring_param_mismatch
- Comment: `
    Send a Discord command using PyAutoGUI.
    
    Args:
        command: The command to send (e.`
- Code: `def send_discord_command(command, delay)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'command'}

### tools\coordination_health_check.py

**Line 162** (high): docstring_param_mismatch
- Comment: `
    Collect basic coordination metrics.
    
    Returns:
        Dictionary with coordination metr`
- Code: `def collect_coordination_metrics()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### tools\create_trading_repo_branch.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
    Create a merge branch for repository consolidation.
    
    Args:
        owner: Repository ow`
- Code: `def create_merge_branch(owner, target_repo, source_repo, branch_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'owner'}

### tools\cycle_v2_to_spreadsheet_integration.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
    Convert Cycle V2 cycles from agent status files to spreadsheet tasks.
    
    Args:
        ou`
- Code: `def cycle_v2_to_spreadsheet_tasks(output_file, include_completed, min_score_threshold)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'output_file'}

**Line 166** (high): docstring_param_mismatch
- Comment: `
    Update Cycle V2 tracker when agent completes cycle.
    
    Args:
        agent_id: Agent ID
 `
- Code: `def update_cycle_v2_tracker(agent_id, status, validation_score, artifacts, commit_hash, pr_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### tools\debate_execution_tracker_hook.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
    Update debate execution tracker when agent completes task.
    
    Args:
        topic: Debate`
- Code: `def update_execution_tracker(topic, agent_id, status, artifact_paths, commit_hash, pr_url, evidence)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'topic'}

**Line 158** (high): docstring_param_mismatch
- Comment: `
    Convert debate execution trackers to spreadsheet tasks.
    
    Args:
        output_file: Out`
- Code: `def debate_trackers_to_spreadsheet_tasks(output_file, include_completed)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'output_file'}

### tools\deploy_via_sftp.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
    Deploy a file to WordPress site via SFTP/SSH.
    
    Args:
        site: Site key (e.g., "fre`
- Code: `def deploy_file(site, file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\deprecated\consolidated_2025-12-05\test_scheduler_integration.py

**Line 67** (high): comment_return_mismatch
- Comment: `Test 4: Test pending tasks query (without scheduler, should return empty)`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

**Line 75** (high): comment_return_mismatch
- Comment: `Test 5: Test task formatting (without tasks, should return empty)`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tools\detect_duplicate_files.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
    Detect duplicate files by content hash.
    
    Args:
        root_path: Root directory to sca`
- Code: `def detect_duplicate_files(root_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'root_path'}

**Line 65** (high): docstring_param_mismatch
- Comment: `
    Detect files with duplicate names (different locations).
    
    Args:
        root_path: Root`
- Code: `def detect_duplicate_names(root_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'root_path'}

### tools\devlog_compressor.py

**Line 279** (high): docstring_param_mismatch
- Comment: `
    Convenience function to compress and archive a devlog.
    
    Args:
        file_path: Path t`
- Code: `def compress_and_archive(file_path, agent, delete_original)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

### tools\disable_wordpress_plugins.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
    Disable or enable WordPress plugins.
    
    Args:
        site: Site key
        disable: Tru`
- Code: `def disable_plugins(site, disable)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\discord_mermaid_renderer.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Extract Mermaid diagrams from markdown content.
        
        Returns:
            List `
- Code: `def extract_mermaid_diagrams(self, content)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'content'}

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Render Mermaid diagram to image URL.
        
        Args:
            diagram_code: Merma`
- Code: `def render_mermaid_to_image_url(self, diagram_code)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'diagram_code', 'self'}

**Line 92** (high): docstring_param_mismatch
- Comment: `
        Render Mermaid diagram to PNG file.
        
        Args:
            diagram_code: Mermai`
- Code: `def render_mermaid_to_file(self, diagram_code, output_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'diagram_code', 'self'}

**Line 127** (high): docstring_param_mismatch
- Comment: `
        Replace Mermaid diagrams in content with image references.
        
        Args:
         `
- Code: `def replace_mermaid_with_images(self, content, output_dir)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'content'}

**Line 171** (high): docstring_param_mismatch
- Comment: `
        Post content to Discord, converting Mermaid diagrams to images.
        
        Args:
    `
- Code: `def post_to_discord_with_mermaid(self, content, webhook_url, username, temp_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

### tools\enable_wordpress_debug.py

**Line 28** (high): docstring_param_mismatch
- Comment: `
    Enable or disable WordPress debug mode.
    
    Args:
        site: Site key
        enable: T`
- Code: `def enable_debug_mode(site, enable)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\enhanced_unified_github.py

**Line 104** (high): docstring_param_mismatch
- Comment: `
        Check rate limits for all APIs.
        
        Returns:
            Dictionary mapping AP`
- Code: `def check_rate_limits(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 210** (high): docstring_param_mismatch
- Comment: `
        Select best API for operation based on rate limits.
        
        Args:
            oper`
- Code: `def select_best_api(self, operation_type)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'operation_type'}

**Line 257** (high): docstring_param_mismatch
- Comment: `
        Create PR with auto-switching and queuing.
        
        Args:
            repo: Target `
- Code: `def create_pr(self, repo, title, body, head, base, queue_on_failure)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo'}

**Line 348** (high): docstring_param_mismatch
- Comment: `
        Merge PR with auto-switching and queuing.
        
        Args:
            repo: Reposito`
- Code: `def merge_pr(self, repo, pr_number, merge_method, queue_on_failure)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo'}

**Line 608** (high): docstring_param_mismatch
- Comment: `
        Queue operation for later retry.
        
        Args:
            operation_type: Type of`
- Code: `def _queue_operation(self, operation_type, params, reason)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'operation_type'}

### tools\extension_test_runner.py

**Line 48** (high): docstring_param_mismatch
- Comment: `
        Run tests for extension.

        Args:
            extension_name: Name of extension
     `
- Code: `def run_tests(self, extension_name, test_type, coverage)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'extension_name', 'self'}

### tools\fix_invalid_agent_workspaces.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
    Find invalid workspace directories and their messages.
    
    Returns:
        List of tuples`
- Code: `def find_invalid_workspaces(workspace_root)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'workspace_root'}

### tools\generate_cycle_accomplishments_report.py

**Line 70** (high): docstring_param_mismatch
- Comment: `
    Generate comprehensive cycle accomplishments report.
    
    Args:
        cycle_id: Optional `
- Code: `def generate_cycle_report(cycle_id, output_dir)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'cycle_id'}

### tools\generate_tools_consolidation_prs.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
    Identify tools that need consolidation PRs.
    
    Returns:
        List of consolidation tas`
- Code: `def identify_consolidation_candidates()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 79** (high): docstring_param_mismatch
- Comment: `
    Generate CSV spreadsheet from tasks.
    
    Args:
        tasks: List of task dictionaries
  `
- Code: `def generate_spreadsheet(tasks, output_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'tasks'}

**Line 115** (high): docstring_param_mismatch
- Comment: `
    Load consolidation tasks from analysis file.
    
    Args:
        analysis_file: Path to anal`
- Code: `def load_from_analysis_file(analysis_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'analysis_file'}

### tools\generate_weekly_progression_report.py

**Line 43** (high): docstring_param_mismatch
- Comment: `
        Generate weekly progression report.

        Args:
            week_start_date: Week start `
- Code: `def generate_report(self, week_start_date)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'week_start_date'}

### tools\git_based_merge_primary.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
    Merge repositories using pure git operations - NO API RATE LIMITS!
    
    Process:
    1. Clo`
- Code: `def git_based_merge(owner, target_repo, source_repo, title, description)`
- Issue: Docstring params don't match: missing={'Process', 'Returns', 'Args'}, extra={'owner'}

### tools\git_work_verifier.py

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Verify if an agent actually did claimed work
        
        Args:
            agent: Agen`
- Code: `def verify_claim(self, agent, file_path, claimed_changes, time_window_hours)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent'}

### tools\github_create_and_push_repo.py

**Line 48** (high): docstring_param_mismatch
- Comment: `
    Create a new GitHub repository using GitHub API.
    
    Args:
        repo_name: Name of the `
- Code: `def create_github_repo(repo_name, description, private, token)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'repo_name'}

**Line 138** (high): docstring_param_mismatch
- Comment: `
    Push local code to GitHub repository.
    
    Args:
        repo_url: GitHub repository URL (H`
- Code: `def push_to_github(repo_url, branch, force, remote_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'repo_url'}

### tools\github_pusher_agent.py

**Line 49** (high): docstring_param_mismatch
- Comment: `
        Process deferred push queue.
        
        Args:
            max_items: Maximum items to`
- Code: `def process_queue(self, max_items)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'max_items', 'self'}

**Line 175** (high): docstring_param_mismatch
- Comment: `
        Run agent continuously.
        
        Args:
            interval_seconds: Seconds betwee`
- Code: `def run_continuous(self, interval_seconds, max_iterations)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'interval_seconds', 'self'}

**Line 314** (high): docstring_param_mismatch
- Comment: `
        Process deferred push queue.
        
        Args:
            max_items: Maximum items to`
- Code: `def process_queue(self, max_items)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'max_items', 'self'}

**Line 440** (high): docstring_param_mismatch
- Comment: `
        Run agent continuously.
        
        Args:
            interval_seconds: Seconds betwee`
- Code: `def run_continuous(self, interval_seconds, max_iterations)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'interval_seconds', 'self'}

### tools\github_queue_processor.py

**Line 54** (high): docstring_param_mismatch
- Comment: `
        Process queued operations.
        
        Args:
            max_items: Maximum items to p`
- Code: `def process_queue(self, max_items, wait_for_reset)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'max_items', 'self'}

**Line 218** (high): docstring_param_mismatch
- Comment: `
        Run continuous queue processing.
        
        Args:
            check_interval: Seconds`
- Code: `def run_continuous(self, check_interval, max_cycles)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'check_interval'}

### tools\identify_problematic_plugin.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
    Identify which plugin is causing the error.
    
    Args:
        site: Site key
        site_`
- Code: `def identify_problematic_plugin(site, site_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\identify_unnecessary_files.py

**Line 175** (medium): deprecated_code_active
- Comment: `In deprecated/temp directories`
- Code: `"deprecated_directory": [],`
- Issue: Code marked as deprecated but still active

### tools\import_chain_validator.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Test if a module can be imported.
    
    Returns dict with:
    - success: bool
    - error: `
- Code: `def test_import(module_path)`
- Issue: Docstring params don't match: missing={'missing_modules', 'success', 'error'}, extra={'module_path'}

### tools\integrate_auto_learning.py

**Line 24** (high): docstring_param_mismatch
- Comment: `
    Automatically learn from a message response interaction.
    
    Args:
        message_file: P`
- Code: `def learn_from_message_response(message_file, response, response_quality, feedback)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message_file', 'response_quality'}

### tools\integration_workflow_automation.py

**Line 30** (high): docstring_param_mismatch
- Comment: `Phase 0: Pre-Integration Cleanup.`
- Code: `def phase_0_cleanup(self)`
- Issue: Docstring params don't match: missing={'0'}, extra={'self'}

**Line 82** (high): docstring_param_mismatch
- Comment: `Phase 1: Pattern Extraction.`
- Code: `def phase_1_pattern_extraction(self)`
- Issue: Docstring params don't match: missing={'1'}, extra={'self'}

### tools\manual_theme_activation.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
    Manually activate theme via database.
    
    Args:
        site: Site key
        theme_name:`
- Code: `def activate_theme_via_database(site, theme_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'site'}

### tools\markov_swarm_integration.py

**Line 304** (high): docstring_param_mismatch
- Comment: `
        Get optimal next task using Markov optimizer.
        
        Args:
            agent_id: `
- Code: `def get_optimal_next_task(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 342** (high): docstring_param_mismatch
- Comment: `
        Get optimal task for agent and assign via CaptainSwarmCoordinator.
        
        Returns`
- Code: `def assign_optimal_task_to_agent(self, agent_id)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'agent_id'}

### tools\markov_task_optimizer.py

**Line 59** (high): docstring_param_mismatch
- Comment: `
        Initialize Markov task optimizer.

        Args:
            tasks: List of all tasks
     `
- Code: `def __init__(self, tasks, agents, weights)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'weights', 'tasks'}

**Line 83** (high): docstring_param_mismatch
- Comment: `
        Select optimal next task using Markov analysis.

        Args:
            state: Current p`
- Code: `def select_next_task(self, state, return_scores)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'state', 'self'}

**Line 297** (high): docstring_param_mismatch
- Comment: `
        Find optimal task sequence using Markov analysis.

        Args:
            start_state: S`
- Code: `def find_optimal_sequence(self, start_state, max_steps)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'start_state'}

### tools\message_compression_automation.py

**Line 41** (high): docstring_param_mismatch
- Comment: `
        Compress message based on age.
        
        Args:
            message: Message dictiona`
- Code: `def compress_message(self, message, age_days)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 76** (high): docstring_param_mismatch
- Comment: `
        Aggregate messages into statistics.
        
        Args:
            messages: List of me`
- Code: `def aggregate_messages(self, messages)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'messages', 'self'}

**Line 132** (high): docstring_param_mismatch
- Comment: `
        Compress message history.
        
        Args:
            dry_run: If True, don't save c`
- Code: `def compress_history(self, dry_run)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'dry_run', 'self'}

### tools\pipeline_gas_scheduler.py

**Line 39** (high): docstring_param_mismatch
- Comment: `
        Initialize pipeline gas scheduler.
        
        Args:
            agent_id: Current age`
- Code: `def __init__(self, agent_id, mission_name, total_items, send_message_func)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Check progress and send gas if checkpoint reached.
        
        Args:
            curre`
- Code: `def check_progress(self, current_item)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'current_item'}

### tools\project_metrics_to_spreadsheet.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
    Collect comprehensive project metrics.

    Returns:
        Dictionary with project metrics
  `
- Code: `def collect_project_metrics()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 182** (medium): docstring_return_mismatch
- Comment: `
    Convert metrics to spreadsheet rows (actionable format).

    Args:
        metrics: Project me`
- Code: `def metrics_to_spreadsheet_rows(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 182** (high): docstring_param_mismatch
- Comment: `
    Convert metrics to spreadsheet rows (actionable format).

    Args:
        metrics: Project me`
- Code: `def metrics_to_spreadsheet_rows(metrics)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'metrics'}

**Line 284** (high): docstring_param_mismatch
- Comment: `
    Collect Cycle V2 metrics from all agent status files.

    Returns:
        Dictionary with cyc`
- Code: `def collect_cycle_v2_metrics()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 466** (high): docstring_param_mismatch
- Comment: `
    Generate comprehensive dashboard spreadsheet.

    Args:
        metrics: Project metrics
     `
- Code: `def generate_dashboard_spreadsheet(metrics, output_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'metrics'}

### tools\projectscanner_modular_reports.py

**Line 417** (high): docstring_param_mismatch
- Comment: `
        Chunk a JSON report into 15k character pieces for agent consumption.
        Returns list o`
- Code: `def chunk_report(report_path, chunk_size)`
- Issue: Docstring params don't match: missing={'DEPRECATED'}, extra={'chunk_size', 'report_path'}

### tools\quick_linecount.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Count lines in a file.

    Args:
        filepath: Path to file

    Returns:
        Tuple of`
- Code: `def count_lines(filepath)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'filepath'}

**Line 39** (high): docstring_param_mismatch
- Comment: `
    Format line count result.

    Args:
        filepath: Path to file
        lines: Line count
 `
- Code: `def format_result(filepath, lines, show_status)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'filepath'}

### tools\real_violation_scanner.py

**Line 19** (high): docstring_param_mismatch
- Comment: `
    Scan a file for actual line count.

    Args:
        file_path: Path to file

    Returns:
   `
- Code: `def scan_file(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 37** (high): docstring_param_mismatch
- Comment: `
    Find files that are ACTUALLY over the threshold.

    Args:
        threshold: Line count thres`
- Code: `def find_real_violations(threshold)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'threshold'}

**Line 62** (high): docstring_param_mismatch
- Comment: `
    Verify if claimed files are actually violations.

    Args:
        files: List of file paths t`
- Code: `def verify_claimed_files(files, threshold)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'files'}

### tools\repo_safe_merge.py

**Line 84** (high): docstring_param_mismatch
- Comment: `
        Initialize safe merge operation.

        Args:
            target_repo: Name of target rep`
- Code: `def __init__(self, target_repo, source_repo, repo_numbers)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'target_repo'}

**Line 266** (high): docstring_param_mismatch
- Comment: `
        Execute the merge operation.

        Args:
            dry_run: If True, only simulate the`
- Code: `def execute_merge(self, dry_run)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'dry_run', 'self'}

**Line 357** (high): docstring_param_mismatch
- Comment: `
        Execute merge using Local-First Architecture (zero blocking).

        Enhanced with merge `
- Code: `def _execute_merge_local_first(self, conflicts)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'conflicts'}

**Line 1232** (high): docstring_param_mismatch
- Comment: `
        Create merge from local repositories using Local-First Architecture.

        Args:
       `
- Code: `def _create_merge_from_local_repos(self, target_path, source_path, username, title, description)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'target_path', 'self'}

**Line 887** (high): comment_raise_mismatch
- Comment: `Don't raise on error, capture output`
- Code: `check=False,`
- Issue: Comment says 'raises' but code doesn't raise

**Line 933** (high): comment_raise_mismatch
- Comment: `Don't raise on error, capture output`
- Code: `check=False,`
- Issue: Comment says 'raises' but code doesn't raise

### tools\repo_status_tracker.py

**Line 34** (high): docstring_param_mismatch
- Comment: `
        Initialize repository status tracker.
        
        Args:
            status_file: Path `
- Code: `def __init__(self, status_file)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'status_file', 'self'}

**Line 82** (high): docstring_param_mismatch
- Comment: `
        Normalize repository name for consistent tracking.
        
        Args:
            repo_`
- Code: `def normalize_repo_name(self, repo_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        Get current status of repository.
        
        Args:
            repo_name: Repository `
- Code: `def get_repo_status(self, repo_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'repo_name'}

**Line 127** (high): docstring_param_mismatch
- Comment: `
        Set repository status.
        
        Args:
            repo_name: Repository name
      `
- Code: `def set_repo_status(self, repo_name, status, reason)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'repo_name'}

**Line 149** (high): docstring_param_mismatch
- Comment: `
        Record merge attempt to prevent duplicates.
        
        Args:
            source_repo:`
- Code: `def record_attempt(self, source_repo, target_repo, success, error)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'source_repo', 'self'}

**Line 182** (high): docstring_param_mismatch
- Comment: `
        Check if merge has been attempted before.
        
        Args:
            source_repo: S`
- Code: `def has_attempted(self, source_repo, target_repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'source_repo', 'self'}

**Line 199** (high): docstring_param_mismatch
- Comment: `
        Get last attempt details.
        
        Args:
            source_repo: Source repository`
- Code: `def get_last_attempt(self, source_repo, target_repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'source_repo', 'self'}

**Line 219** (high): docstring_param_mismatch
- Comment: `
        Record consolidation direction (source → target).
        
        Args:
            source`
- Code: `def set_consolidation_direction(self, source_repo, target_repo)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'source_repo', 'self'}

**Line 233** (high): docstring_param_mismatch
- Comment: `
        Get consolidation target for source repository.
        
        Args:
            source_r`
- Code: `def get_consolidation_target(self, source_repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'source_repo', 'self'}

**Line 246** (high): docstring_param_mismatch
- Comment: `
        Classify error as permanent (no retries).
        
        Args:
            error: Error m`
- Code: `def is_permanent_error(self, error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'error'}

### tools\repository_cleanup_for_migration.py

**Line 122** (high): docstring_param_mismatch
- Comment: `
    Remove internal directories from git tracking (keep files locally).
    
    Returns:
        T`
- Code: `def remove_from_tracking(dry_run)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'dry_run'}

### tools\run_weekly_dashboard_and_report.py

**Line 32** (high): docstring_param_mismatch
- Comment: `Return Monday 00:00 of the requested or current week.`
- Code: `def compute_week_start(week_start_str)`
- Issue: Docstring params don't match: missing={'00'}, extra={'week_start_str'}

### tools\schedule_daily_reports.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
    Schedule reports using Windows Task Scheduler (Windows).
    
    Creates two scheduled tasks:
`
- Code: `def schedule_with_task_scheduler()`
- Issue: Docstring params don't match: missing={'report'}, extra=set()

### tools\schedule_dashboard_updates.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
    Schedule dashboard updates using Windows Task Scheduler (Windows).
    
    Creates a scheduled`
- Code: `def schedule_with_task_scheduler()`
- Issue: Docstring params don't match: missing={'update'}, extra=set()

### tools\spreadsheet_github_adapter.py

**Line 71** (high): docstring_param_mismatch
- Comment: `
    Process GitHub task using swarm's unified GitHub tools.
    
    Args:
        task: GitHub tas`
- Code: `def handle_task(task)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'task'}

**Line 107** (high): docstring_param_mismatch
- Comment: `
    Handle create_issue task type using GitHub API.
    
    TODO: Implement issue creation via Git`
- Code: `def _handle_create_issue(task)`
- Issue: Docstring params don't match: missing={'TODO'}, extra={'task'}

**Line 205** (high): docstring_param_mismatch
- Comment: `
    Parse spreadsheet row into GithubTask.
    
    Args:
        row: Dictionary with column names`
- Code: `def parse_spreadsheet_row(row, default_repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'row'}

**Line 242** (high): docstring_param_mismatch
- Comment: `
    Format GithubResult for spreadsheet update.
    
    Returns:
        Dictionary with columns m`
- Code: `def format_result_for_spreadsheet(result)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'result'}

**Line 257** (high): docstring_param_mismatch
- Comment: `
    Process spreadsheet file (CSV or JSON) and execute tasks.
    
    Args:
        file_path: Pat`
- Code: `def process_spreadsheet_file(file_path, default_repo)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

### tools\START_CHAT_BOT_NOW.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
    Mask OAuth token for safe logging.
    
    Args:
        tok: OAuth token string
        
    `
- Code: `def _mask_token(tok)`
- Issue: Docstring params don't match: missing={'Returns', 'oauth', 'Args'}, extra={'tok'}

### tools\stress_test_messaging_queue.py

**Line 110** (high): docstring_param_mismatch
- Comment: `Run stress test.
    
    Args:
        duration: Test duration in seconds
        messages_per_seco`
- Code: `def run_stress_test(duration, messages_per_second, use_mock, chaos_mode, success_rate, min_latency_ms, max_latency_ms, output_file, batch_size, interval, use_in_memory_queue)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'duration'}

**Line 250** (high): docstring_param_mismatch
- Comment: `Run comparison mode (real vs mock delivery).
    
    Args:
        duration: Test duration in secon`
- Code: `def run_comparison_mode(duration, messages_per_second, output_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'duration'}

### tools\swarm_orchestrator.py

**Line 260** (high): docstring_param_mismatch
- Comment: `
    Run the orchestrator for N cycles.

    Args:
        cycles: Number of cycles to run (0 = infi`
- Code: `def run_orchestrator(cycles, interval)`
- Issue: Docstring params don't match: missing={'default', 'Args'}, extra={'cycles'}

### tools\test_repo_status_tracker.py

**Line 75** (high): docstring_param_mismatch
- Comment: `Test 1: Name Resolution - Normalize and verify exact repo names.`
- Code: `def test_name_resolution(self)`
- Issue: Docstring params don't match: missing={'1'}, extra={'self'}

**Line 107** (high): docstring_param_mismatch
- Comment: `Test 2: Status Tracking - Track repo status (exists/merged/deleted).`
- Code: `def test_status_tracking(self)`
- Issue: Docstring params don't match: missing={'2'}, extra={'self'}

**Line 154** (high): docstring_param_mismatch
- Comment: `Test 3: Error Classification - Permanent vs retryable errors.`
- Code: `def test_error_classification(self)`
- Issue: Docstring params don't match: missing={'3'}, extra={'self'}

**Line 206** (high): docstring_param_mismatch
- Comment: `Test 4: Duplicate Prevention - Track attempts and skip duplicates.`
- Code: `def test_duplicate_prevention(self)`
- Issue: Docstring params don't match: missing={'4'}, extra={'self'}

**Line 261** (high): docstring_param_mismatch
- Comment: `Test 5: Strategy Review - Verify consolidation direction.`
- Code: `def test_consolidation_direction(self)`
- Issue: Docstring params don't match: missing={'5'}, extra={'self'}

**Line 299** (high): docstring_param_mismatch
- Comment: `Test 6: Persistence - Status tracking persists correctly.`
- Code: `def test_persistence(self)`
- Issue: Docstring params don't match: missing={'6'}, extra={'self'}

### tools\test_twitch_bot_connection.py

**Line 40** (high): docstring_param_mismatch
- Comment: `Test 1: Configuration is valid.`
- Code: `def test_configuration(self)`
- Issue: Docstring params don't match: missing={'1'}, extra={'self'}

**Line 72** (high): docstring_param_mismatch
- Comment: `Test 2: Bridge can be created.`
- Code: `def test_bridge_creation(self)`
- Issue: Docstring params don't match: missing={'2'}, extra={'self'}

### tools\test_twitch_connection_tdd.py

**Line 25** (high): docstring_param_mismatch
- Comment: `Test 1: Channel name extraction.`
- Code: `def test_channel_name_extraction()`
- Issue: Docstring params don't match: missing={'1'}, extra=set()

**Line 51** (high): docstring_param_mismatch
- Comment: `Test 2: OAuth token format.`
- Code: `def test_oauth_token_format()`
- Issue: Docstring params don't match: missing={'2'}, extra=set()

**Line 71** (high): docstring_param_mismatch
- Comment: `Test 3: Bot username.`
- Code: `def test_bot_username()`
- Issue: Docstring params don't match: missing={'3'}, extra=set()

**Line 85** (high): docstring_param_mismatch
- Comment: `Test 4: Complete configuration check.`
- Code: `def test_configuration_complete()`
- Issue: Docstring params don't match: missing={'4'}, extra=set()

**Line 109** (high): docstring_param_mismatch
- Comment: `Test 5: Check if required libraries are available.`
- Code: `def test_import_availability()`
- Issue: Docstring params don't match: missing={'5'}, extra=set()

**Line 126** (high): docstring_param_mismatch
- Comment: `Test 6: Test bridge initialization.`
- Code: `def test_bridge_initialization()`
- Issue: Docstring params don't match: missing={'6'}, extra=set()

### tools\thea\simple_thea_communication.py

**Line 260** (high): docstring_param_mismatch
- Comment: `
        Complete communication cycle: send message and get response.

        Returns:
            `
- Code: `def communicate(self, message)`
- Issue: Docstring params don't match: missing={'cycle', 'Returns'}, extra={'message', 'self'}

### tools\thea\thea_automation.py

**Line 298** (high): docstring_param_mismatch
- Comment: `
        Send message to Thea and optionally wait for response.

        Args:
            message: `
- Code: `def send_message(self, message, wait_for_response)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 398** (high): docstring_param_mismatch
- Comment: `
        Complete communication cycle: send message and get response.

        Args:
            mes`
- Code: `def communicate(self, message, save)`
- Issue: Docstring params don't match: missing={'cycle', 'Returns', 'Args'}, extra={'message', 'self'}

### tools\thea\thea_automation_browser.py

**Line 29** (high): docstring_param_mismatch
- Comment: `
        Initialize browser manager.

        Args:
            headless: Whether to run browser in `
- Code: `def __init__(self, headless)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'headless'}

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Initialize and start Chrome browser.

        Returns:
            bool: True if browser st`
- Code: `def start_browser(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 69** (high): docstring_param_mismatch
- Comment: `
        Check if logged in to ChatGPT.

        Returns:
            bool: True if logged in
      `
- Code: `def is_logged_in(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 102** (high): docstring_param_mismatch
- Comment: `
        Ensure we're logged in to Thea, with automatic cookie loading.

        Args:
            t`
- Code: `def ensure_login(self, thea_url, cookie_manager, login_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'thea_url'}

**Line 144** (high): docstring_param_mismatch
- Comment: `
        Handle manual login process.

        Args:
            thea_url: URL to Thea ChatGPT insta`
- Code: `def _handle_manual_login(self, thea_url, cookie_manager, login_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'thea_url'}

**Line 189** (high): docstring_param_mismatch
- Comment: `
        Get the WebDriver instance.

        Returns:
            WebDriver: The browser driver ins`
- Code: `def get_driver(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools\thea\thea_automation_cookie_manager.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
        Initialize cookie manager.

        Args:
            driver: Selenium WebDriver instance
 `
- Code: `def __init__(self, driver, cookie_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'driver'}

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Save cookies from current session to file.

        Returns:
            bool: True if cook`
- Code: `def save_cookies(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Load cookies from file into current session.

        Returns:
            bool: True if co`
- Code: `def load_cookies(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 85** (high): docstring_param_mismatch
- Comment: `
        Check if valid (non-expired) cookies exist in file.

        Returns:
            bool: Tru`
- Code: `def has_valid_cookies(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 106** (high): docstring_param_mismatch
- Comment: `
        Filter cookies to keep only authentication-related ones.

        Args:
            cookies`
- Code: `def _filter_auth_cookies(self, cookies)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'cookies'}

**Line 129** (high): docstring_param_mismatch
- Comment: `
        Load cookies into WebDriver.

        Args:
            cookies: List of cookie dictionarie`
- Code: `def _load_cookies_into_driver(self, cookies)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'cookies'}

**Line 150** (high): docstring_param_mismatch
- Comment: `
        Filter cookies to keep only non-expired ones.

        Args:
            cookies: List of c`
- Code: `def _filter_valid_cookies(self, cookies)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'cookies'}

### tools\thea\thea_automation_messaging.py

**Line 38** (high): docstring_param_mismatch
- Comment: `
        Initialize messaging manager.

        Args:
            driver: Selenium WebDriver instanc`
- Code: `def __init__(self, driver, responses_dir, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'driver'}

**Line 59** (high): docstring_param_mismatch
- Comment: `
        Send message to Thea and optionally wait for response.

        Args:
            message: `
- Code: `def send_message(self, message, wait_for_response)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

**Line 92** (high): docstring_param_mismatch
- Comment: `
        Wait for and capture Thea's response.

        Returns:
            str: Response text, or `
- Code: `def wait_for_response(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 121** (high): docstring_param_mismatch
- Comment: `
        Process response wait result.

        Args:
            result: ResponseWaitResult from de`
- Code: `def _process_response_result(self, result)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'result'}

**Line 140** (high): docstring_param_mismatch
- Comment: `
        Save conversation to JSON file.

        Args:
            message: Message that was sent
 `
- Code: `def save_conversation(self, message, response, thea_url)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'message', 'self'}

### tools\thea\thea_login_handler.py

**Line 61** (high): docstring_param_mismatch
- Comment: `
        Initialize the cookie manager.

        Args:
            cookie_file: Path to cookie file `
- Code: `def __init__(self, cookie_file)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'cookie_file'}

**Line 71** (high): docstring_param_mismatch
- Comment: `
        Save cookies from the current driver session.

        Args:
            driver: Selenium w`
- Code: `def save_cookies(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 130** (high): docstring_param_mismatch
- Comment: `
        Load cookies into the current driver session.

        Args:
            driver: Selenium w`
- Code: `def load_cookies(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 170** (high): docstring_param_mismatch
- Comment: `
        Check if valid cookies exist.

        Returns:
            True if cookie file exists and `
- Code: `def has_valid_cookies(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 207** (high): docstring_param_mismatch
- Comment: `
        Clear saved cookies.

        Returns:
            True if cookies cleared successfully, Fa`
- Code: `def clear_cookies(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 231** (high): docstring_param_mismatch
- Comment: `
        Initialize the Thea login handler.

        Args:
            username: ChatGPT username/em`
- Code: `def __init__(self, username, password, cookie_file, timeout)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'username'}

**Line 256** (high): docstring_param_mismatch
- Comment: `
        Ensure user is logged into Thea/ChatGPT.

        Args:
            driver: Selenium webdri`
- Code: `def ensure_login(self, driver, allow_manual, manual_timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 610** (high): docstring_param_mismatch
- Comment: `
        Perform automated login with credentials.

        Args:
            driver: Selenium webdr`
- Code: `def _automated_login(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 670** (high): docstring_param_mismatch
- Comment: `
        Allow manual login with timeout.

        Args:
            driver: Selenium webdriver inst`
- Code: `def _manual_login(self, driver, timeout)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 748** (high): docstring_param_mismatch
- Comment: `
        Force logout from ChatGPT.

        Args:
            driver: Selenium webdriver instance

`
- Code: `def force_logout(self, driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'driver'}

**Line 777** (high): docstring_param_mismatch
- Comment: `
    Create a Thea login handler with default settings.

    Args:
        username: ChatGPT usernam`
- Code: `def create_thea_login_handler(username, password, cookie_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'username'}

**Line 792** (high): docstring_param_mismatch
- Comment: `
    Quick check of Thea login status.

    Args:
        driver: Selenium webdriver instance

    R`
- Code: `def check_thea_login_status(driver)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'driver'}

### tools\thea\thea_undetected_helper.py

**Line 37** (high): docstring_param_mismatch
- Comment: `
    Create an undetected Chrome driver for Thea communication.

    This function automatically han`
- Code: `def create_undetected_driver(headless, user_data_dir, profile, version_main)`
- Issue: Docstring params don't match: missing={'Returns', 'kwargs', 'Args'}, extra={'headless'}

**Line 113** (high): docstring_param_mismatch
- Comment: `
    Create a standard Chrome driver using Selenium Manager.

    Args:
        headless: Run in hea`
- Code: `def create_standard_driver(headless, user_data_dir, profile)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'headless'}

**Line 155** (high): docstring_param_mismatch
- Comment: `
    Check if undetected-chromedriver is available.

    Returns:
        True if available, False o`
- Code: `def check_undetected_available()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

**Line 165** (high): docstring_param_mismatch
- Comment: `
    Get installation instructions for undetected-chromedriver.

    Returns:
        Installation i`
- Code: `def get_installation_instructions()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### tools\timeout_constant_replacer.py

**Line 72** (high): docstring_param_mismatch
- Comment: `
        Find all timeout occurrences in content.
        
        Returns:
            List of (lin`
- Code: `def find_timeout_occurrences(self, content)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'content'}

### tools\toolbelt\executors\compliance_tracking_executor.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Execute compliance tracking command.

        Args:
            args: Parsed arguments with`
- Code: `def execute(self, args)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'args'}

### tools\toolbelt\executors\leaderboard_executor.py

**Line 32** (high): docstring_param_mismatch
- Comment: `
        Execute leaderboard command.

        Args:
            args: Parsed arguments with lb_acti`
- Code: `def execute(self, args)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'args'}

### tools\toolbelt\executors\onboarding_executor.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Execute onboarding command.

        Args:
            args: Parsed arguments with onboard_`
- Code: `def execute(self, args)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'args'}

### tools\toolbelt\executors\swarm_executor.py

**Line 33** (high): docstring_param_mismatch
- Comment: `
        Execute swarm command.

        Args:
            args: Parsed arguments with swarm_action
`
- Code: `def execute(self, args)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'args'}

### tools\toolbelt_help.py

**Line 22** (high): docstring_param_mismatch
- Comment: `
        Initialize help generator.

        Args:
            registry: ToolRegistry instance
     `
- Code: `def __init__(self, registry)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'registry', 'self'}

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Generate formatted help text.

        Returns:
            Formatted help text
        `
- Code: `def generate_help(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Show help for specific tool.

        Args:
            tool_config: Tool configuration

  `
- Code: `def show_tool_help(self, tool_config)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'tool_config', 'self'}

### tools\toolbelt_registry.py

**Line 758** (high): docstring_param_mismatch
- Comment: `
        Get tool configuration by flag.

        Args:
            flag: Tool flag (e.g., "--scan",`
- Code: `def get_tool_for_flag(self, flag)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'flag'}

**Line 773** (high): docstring_param_mismatch
- Comment: `
        Get tool configuration by tool ID.

        Args:
            name: Tool ID (e.g., "scan", `
- Code: `def get_tool_by_name(self, name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'name'}

**Line 785** (high): docstring_param_mismatch
- Comment: `
        List all available tools.

        Returns:
            List of tool configurations
       `
- Code: `def list_tools(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools\toolbelt_runner.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Execute tool with given arguments.

        Args:
            tool_config: Tool configurati`
- Code: `def execute_tool(self, tool_config, args)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'tool_config', 'self'}

**Line 70** (high): comment_return_mismatch
- Comment: `Handle None return as success`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tools\tools_consolidation_quick.py

**Line 68** (high): comment_return_mismatch
- Comment: `Return groups with multiple tools`
- Code: ``
- Issue: Comment says 'returns' but code doesn't return

### tools\unified_github_pr_creator.py

**Line 283** (high): docstring_param_mismatch
- Comment: `
        Create PR using best available method with automatic fallback.
        
        Args:
     `
- Code: `def create_pr_unified(self, repo, title, body, head, base, prefer_method)`
- Issue: Docstring params don't match: missing={'owner', 'Returns', 'Args'}, extra={'self'}

### tools\validate_stress_test_integration.py

**Line 31** (high): docstring_param_mismatch
- Comment: `Initialize validator.
        
        Args:
            stress_test_dir: Path to stress_testing dir`
- Code: `def __init__(self, stress_test_dir)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'stress_test_dir', 'self'}

**Line 42** (high): docstring_param_mismatch
- Comment: `Run all validation checks.
        
        Returns:
            Tuple of (all_passed, results_dict)`
- Code: `def validate_all(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools\verify_failed_merge_repos.py

**Line 50** (high): docstring_param_mismatch
- Comment: `
    Verify repository existence using GitHub API.
    
    Returns:
        Dict with exists (bool)`
- Code: `def verify_repo_exists(owner, repo, token)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'token', 'owner', 'repo'}

### tools\verify_file_usage_enhanced_v2.py

**Line 197** (high): docstring_param_mismatch
- Comment: `
        Check if file is referenced in config files.
        
        Checks: YAML, JSON, TOML, INI`
- Code: `def check_config_references(self, file_path)`
- Issue: Docstring params don't match: missing={'Checks'}, extra={'self', 'file_path'}

### tools\verify_github_repo_cicd.py

**Line 23** (high): docstring_param_mismatch
- Comment: `
    Verify CI/CD for a GitHub repository.
    
    Args:
        repo_owner: GitHub repository owne`
- Code: `def verify_repo_cicd(repo_owner, repo_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'repo_owner'}

### tools\violation_domain_analyzer.py

**Line 218** (high): docstring_param_mismatch
- Comment: `Parse location string like 'file.py:16' into Path and line number.`
- Code: `def parse_location(location_str)`
- Issue: Docstring params don't match: missing={'py'}, extra={'location_str'}

### tools\website_manager.py

**Line 95** (high): docstring_param_mismatch
- Comment: `
        Update a page template with content changes.
        
        Args:
            template_na`
- Code: `def update_page_template(self, template_name, updates)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'template_name'}

**Line 179** (high): docstring_param_mismatch
- Comment: `
        Update color scheme in a template.
        
        Args:
            template_name: Templa`
- Code: `def update_colors(self, template_name, color_scheme)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'template_name'}

**Line 328** (high): docstring_param_mismatch
- Comment: `
        Deploy a file to the live server.
        
        Args:
            template_name: Templat`
- Code: `def deploy_file(self, template_name, use_hostinger_file_manager)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'template_name'}

**Line 394** (high): docstring_param_mismatch
- Comment: `
        Create WordPress page (compatible with wordpress_page_setup.py).
        Consolidates: word`
- Code: `def create_page(self, page_name, page_slug, template_content)`
- Issue: Docstring params don't match: missing={'Consolidates'}, extra={'self', 'template_content', 'page_name', 'page_slug'}

**Line 465** (high): docstring_param_mismatch
- Comment: `
        Deploy all theme files (compatible with wordpress_manager.deploy_theme()).
        Consolid`
- Code: `def deploy_theme_files(self, pattern)`
- Issue: Docstring params don't match: missing={'Consolidates'}, extra={'pattern', 'self'}

**Line 483** (high): docstring_param_mismatch
- Comment: `
        Auto-deploy changed files (compatible with auto_deploy_hook.py).
        Consolidates: auto`
- Code: `def auto_deploy_changed_files(self, changed_files)`
- Issue: Docstring params don't match: missing={'Consolidates'}, extra={'changed_files', 'self'}

### tools\wordpress_manager.py

**Line 577** (high): docstring_param_mismatch
- Comment: `
        Deploy single file to server.

        Args:
            local_path: Local file path to dep`
- Code: `def deploy_file(self, local_path, remote_path, auto_flush_cache)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'local_path'}

**Line 627** (high): docstring_param_mismatch
- Comment: `
        Deploy all theme files matching pattern.

        Args:
            pattern: File pattern t`
- Code: `def deploy_theme(self, pattern, auto_flush_cache)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'pattern', 'self'}

**Line 741** (high): docstring_param_mismatch
- Comment: `
        Replace entire theme on server.

        Args:
            new_theme_path: Local path to ne`
- Code: `def replace_theme(self, new_theme_path, backup, auto_flush_cache)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'new_theme_path'}

**Line 793** (high): docstring_param_mismatch
- Comment: `
        Activate theme using multiple methods.

        Tries methods in order:
        1. WP-CLI (`
- Code: `def activate_theme(self, theme_name, use_browser_fallback, auto_login)`
- Issue: Docstring params don't match: missing={'order', 'Returns', 'Args'}, extra={'self', 'theme_name'}

**Line 839** (high): docstring_param_mismatch
- Comment: `
        Activate theme via browser automation (fallback method).

        Args:
            theme_n`
- Code: `def _activate_theme_via_browser(self, theme_name, auto_login)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'theme_name'}

**Line 976** (high): docstring_param_mismatch
- Comment: `
        Purge WordPress cache using multiple methods.

        Tries methods in order:
        1. W`
- Code: `def purge_caches(self, use_comprehensive_flush)`
- Issue: Docstring params don't match: missing={'order', 'Returns', 'Args'}, extra={'use_comprehensive_flush', 'self'}

### tools\wordpress_page_setup.py

**Line 132** (high): docstring_param_mismatch
- Comment: `Complete page setup: create template and add to functions.php.`
- Code: `def setup_page(self, page_name, page_slug, template_content, template_name)`
- Issue: Docstring params don't match: missing={'setup'}, extra={'template_content', 'page_slug', 'self', 'template_name', 'page_name'}

### tools\work_attribution_tool.py

**Line 40** (high): docstring_param_mismatch
- Comment: `
        Get all work done by a specific agent
        
        Args:
            agent: Agent ID
  `
- Code: `def get_agent_work(self, agent, hours, file_pattern)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent'}

### tools\work_completion_verifier.py

**Line 35** (high): docstring_param_mismatch
- Comment: `
        Verify VSCode extension completion.

        Checks:
        - Files exist
        - Tests `
- Code: `def verify_extension(self, extension_name)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'extension_name', 'self'}

**Line 149** (high): docstring_param_mismatch
- Comment: `
        Verify Python module completion.

        Checks:
        - Files exist
        - No syntax`
- Code: `def verify_python_module(self, module_path)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'module_path', 'self'}

### tools\workspace_health_checker.py

**Line 25** (high): docstring_param_mismatch
- Comment: `
    Check workspace structure health.
    
    Returns:
        Health report dictionary
    `
- Code: `def check_workspace_structure(workspace_root)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'workspace_root'}

### tools_v2\adapters\base_adapter.py

**Line 27** (high): docstring_param_mismatch
- Comment: `
        Validate tool parameters.

        Args:
            params: Parameters to validate

      `
- Code: `def validate_params(self, params)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'params'}

**Line 66** (medium): docstring_return_mismatch
- Comment: `
        Get tool specification.

        Returns:
            Tool specification with metadata
    `
- Code: `def get_spec(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 66** (high): docstring_param_mismatch
- Comment: `
        Get tool specification.

        Returns:
            Tool specification with metadata
    `
- Code: `def get_spec(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 76** (medium): docstring_return_mismatch
- Comment: `
        Validate tool parameters.

        Args:
            params: Parameters to validate

      `
- Code: `def validate(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 76** (high): docstring_param_mismatch
- Comment: `
        Validate tool parameters.

        Args:
            params: Parameters to validate

      `
- Code: `def validate(self, params)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'params'}

**Line 89** (medium): docstring_return_mismatch
- Comment: `
        Execute the tool with given parameters.

        Args:
            params: Tool parameters
`
- Code: `def execute(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 89** (high): docstring_param_mismatch
- Comment: `
        Execute the tool with given parameters.

        Args:
            params: Tool parameters
`
- Code: `def execute(self, params, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'params'}

**Line 102** (high): docstring_param_mismatch
- Comment: `
        Get help text for the tool.

        Returns:
            Help text describing tool usage
 `
- Code: `def get_help(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools_v2\adapters\error_types.py

**Line 15** (high): docstring_param_mismatch
- Comment: `
        Initialize toolbelt error.

        Args:
            message: Error description
          `
- Code: `def __init__(self, message, tool_name)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Initialize validation error.

        Args:
            message: Error description
        `
- Code: `def __init__(self, message, tool_name, invalid_params)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 54** (high): docstring_param_mismatch
- Comment: `
        Initialize execution error.

        Args:
            message: Error description
         `
- Code: `def __init__(self, message, tool_name, exit_code)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 70** (high): docstring_param_mismatch
- Comment: `
        Initialize dependency error.

        Args:
            message: Error description
        `
- Code: `def __init__(self, message, tool_name, missing_deps)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'message', 'self'}

**Line 94** (high): docstring_param_mismatch
- Comment: `
    Format toolbelt error for user display.

    Args:
        error: Toolbelt error instance

    `
- Code: `def format_toolbelt_error(error)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'error'}

### tools_v2\categories\autonomous_workflow_tools.py

**Line 101** (high): docstring_param_mismatch
- Comment: `
        Assign task to best-fit agent
        
        Args:
            task: WorkflowAssignmentTa`
- Code: `def assign_task(self, task, dry_run)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'task'}

**Line 323** (high): docstring_param_mismatch
- Comment: `
        Get complete dashboard state
        
        Returns:
            Dictionary with agents, `
- Code: `def get_dashboard_view(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools_v2\categories\communication_tools.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Post update to Discord via router.
        
        Args:
            agent_id: Agent ident`
- Code: `def post_update(self, agent_id, message, title, priority)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'agent_id'}

**Line 110** (high): docstring_param_mismatch
- Comment: `
        Execute Discord post.
        
        Args:
            params: {
                "agent_i`
- Code: `def execute(self, params, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'context', 'params'}

### tools_v2\categories\discord_webhook_tools.py

**Line 42** (high): docstring_param_mismatch
- Comment: `
        Create Discord webhook.
        
        Args:
            channel_id: Discord channel ID (`
- Code: `def execute(self)`
- Issue: Docstring params don't match: missing={'default', 'save_to_config', 'avatar_url', 'webhook_name', 'Args', 'Returns', 'config_key'}, extra={'self'}

**Line 109** (high): docstring_param_mismatch
- Comment: `
        List Discord webhooks.
        
        Args:
            channel_id: Optional - filter by `
- Code: `def execute(self)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'show_urls', 'Args'}, extra={'self'}

**Line 190** (high): docstring_param_mismatch
- Comment: `
        Save webhook URL to config.
        
        Args:
            webhook_url: Discord webhook`
- Code: `def execute(self)`
- Issue: Docstring params don't match: missing={'default', 'config_file', 'Args', 'Returns', 'config_key', 'target'}, extra={'self'}

**Line 297** (high): docstring_param_mismatch
- Comment: `
        Test webhook.
        
        Args:
            webhook_url: Discord webhook URL (or confi`
- Code: `def execute(self)`
- Issue: Docstring params don't match: missing={'default', 'test_message', 'Args', 'Returns', 'config_key'}, extra={'self'}

**Line 369** (high): docstring_param_mismatch
- Comment: `
        Manage webhooks.
        
        Args:
            action: "create", "list", "save", "test`
- Code: `def execute(self)`
- Issue: Docstring params don't match: missing={'Returns', 'kwargs', 'Args'}, extra={'self'}

### tools_v2\categories\github_consolidation_tools.py

**Line 513** (high): docstring_param_mismatch
- Comment: `
        Execute repository merge by calling repo_safe_merge.py via subprocess.
        
        SSO`
- Code: `def execute(self, params, context)`
- Issue: Docstring params don't match: missing={'SSOT'}, extra={'self', 'context', 'params'}

### tools_v2\categories\intelligent_mission_advisor.py

**Line 45** (high): docstring_param_mismatch
- Comment: `
        Initialize intelligent mission advisor for specific agent.

        Args:
            agent`
- Code: `def __init__(self, agent_id)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 152** (high): docstring_param_mismatch
- Comment: `
        Get intelligent mission recommendation for agent.

        This is the CORE masterpiece fun`
- Code: `def get_mission_recommendation(self, context, prefer_high_roi, avoid_duplication)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'recommended_task', 'estimated_points', 'roi_score', 'conflicts', 'Args', 'verification_status', 'intelligent_briefing', 'specialty_match', 'risk_factors', 'execution_guidance', 'success_patterns'}, extra={'self', 'context'}

**Line 556** (high): docstring_param_mismatch
- Comment: `
        Validate a Captain's order before executing.

        Applies Swarm Brain Pattern #1 - veri`
- Code: `def validate_captain_order(self, order_file)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'order_file', 'self'}

**Line 694** (high): docstring_param_mismatch
- Comment: `
        Get real-time guidance during task execution.

        Provides intelligent suggestions bas`
- Code: `def get_realtime_guidance(self, current_step, task_context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'current_step'}

**Line 730** (high): docstring_param_mismatch
- Comment: `
        Analyze overall swarm state and provide strategic insights.

        Returns:
            C`
- Code: `def analyze_swarm_state(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 769** (high): docstring_param_mismatch
- Comment: `
    Get intelligent mission advisor for an agent.

    Args:
        agent_id: Agent identifier

  `
- Code: `def get_mission_advisor(agent_id)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'agent_id'}

### tools_v2\categories\intelligent_mission_advisor_analysis.py

**Line 30** (high): docstring_param_mismatch
- Comment: `
        Initialize analysis module.

        Args:
            agent_id: Agent identifier
         `
- Code: `def __init__(self, agent_id, agent_specialty, project_root, other_agents_work)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

### tools_v2\categories\intelligent_mission_advisor_guidance.py

**Line 31** (high): docstring_param_mismatch
- Comment: `
        Initialize guidance module.

        Args:
            agent_id: Agent identifier
         `
- Code: `def __init__(self, agent_id, agent_specialty, agent_status, swarm_brain, other_agents_work, leaderboard)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'agent_id'}

**Line 194** (high): docstring_param_mismatch
- Comment: `
        Get real-time guidance during task execution.

        Provides intelligent suggestions bas`
- Code: `def get_realtime_guidance(self, current_step, task_context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'current_step'}

**Line 228** (high): docstring_param_mismatch
- Comment: `
        Analyze overall swarm state and provide strategic insights.

        Returns:
            C`
- Code: `def analyze_swarm_state(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

### tools_v2\categories\memory_safety_tools.py

**Line 21** (high): docstring_param_mismatch
- Comment: `
    Detect potential memory leaks in Python codebase.

    Scans for:
    - Unbounded list.append()`
- Code: `def detect_memory_leaks(target_path)`
- Issue: Docstring params don't match: missing={'default', 'Returns', 'Args'}, extra={'target_path'}

**Line 111** (high): docstring_param_mismatch
- Comment: `
    Verify that files exist before task assignment.

    Prevents "phantom task" issues where tasks`
- Code: `def verify_files_exist(file_list)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_list'}

**Line 143** (high): docstring_param_mismatch
- Comment: `
    Scan for unbounded data structures that could cause memory leaks.

    Identifies:
    - Lists `
- Code: `def scan_unbounded_structures(target_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'target_path'}

**Line 235** (high): docstring_param_mismatch
- Comment: `
    Validate that a Python file's imports work correctly.

    Tests imports without executing the `
- Code: `def validate_imports(file_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'file_path'}

**Line 304** (high): docstring_param_mismatch
- Comment: `
    Check for unclosed file handles (potential resource leaks).

    Scans for:
    - open() withou`
- Code: `def check_file_handles(target_path)`
- Issue: Docstring params don't match: missing={'Warning', 'Returns', 'Args'}, extra={'target_path'}

### tools_v2\tests\test_adapters.py

**Line 105** (medium): docstring_return_mismatch
- Comment: `Test adapter returns valid spec.`
- Code: `def test_adapter_get_spec(...)`
- Issue: Docstring mentions return but function has no return statement

**Line 127** (medium): docstring_return_mismatch
- Comment: `Test adapter returns help text.`
- Code: `def test_adapter_get_help(...)`
- Issue: Docstring mentions return but function has no return statement

### tools_v2\tests\test_registry.py

**Line 33** (medium): docstring_return_mismatch
- Comment: `Test registry singleton returns same instance.`
- Code: `def test_singleton_pattern(...)`
- Issue: Docstring mentions return but function has no return statement

### tools_v2\toolbelt_core.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Run a tool with given parameters (resolve→validate→execute→record).

        Args:
        `
- Code: `def run(self, tool_name, params, context)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'tool_name', 'self'}

**Line 108** (high): docstring_param_mismatch
- Comment: `
        List all available tools.

        Returns:
            Sorted list of tool names
        `
- Code: `def list_tools(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 117** (high): docstring_param_mismatch
- Comment: `
        List tools grouped by category.

        Returns:
            Dictionary mapping category t`
- Code: `def list_categories(self)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self'}

**Line 126** (high): docstring_param_mismatch
- Comment: `
        Get help text for a specific tool.

        Args:
            tool_name: Name of tool

    `
- Code: `def get_tool_help(self, tool_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'tool_name', 'self'}

**Line 143** (high): docstring_param_mismatch
- Comment: `
        Get recent tool execution history.

        Args:
            limit: Maximum number of entr`
- Code: `def get_execution_history(self, limit)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'limit'}

**Line 160** (high): docstring_param_mismatch
- Comment: `
        Record tool execution for metrics and debugging.

        Args:
            tool_name: Name`
- Code: `def _record_execution(self, tool_name, params, result)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'tool_name', 'self'}

**Line 190** (high): docstring_param_mismatch
- Comment: `
    Get singleton toolbelt core instance.

    Returns:
        Toolbelt core instance
    `
- Code: `def get_toolbelt_core()`
- Issue: Docstring params don't match: missing={'Returns'}, extra=set()

### tools_v2\utils\discord_mermaid_renderer.py

**Line 36** (high): docstring_param_mismatch
- Comment: `
        Extract Mermaid diagrams from markdown content.
        
        Returns:
            List `
- Code: `def extract_mermaid_diagrams(self, content)`
- Issue: Docstring params don't match: missing={'Returns'}, extra={'self', 'content'}

**Line 53** (high): docstring_param_mismatch
- Comment: `
        Render Mermaid diagram to image URL.
        
        Args:
            diagram_code: Merma`
- Code: `def render_mermaid_to_image_url(self, diagram_code)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'diagram_code', 'self'}

**Line 92** (high): docstring_param_mismatch
- Comment: `
        Render Mermaid diagram to PNG file.
        
        Args:
            diagram_code: Mermai`
- Code: `def render_mermaid_to_file(self, diagram_code, output_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'diagram_code', 'self'}

**Line 127** (high): docstring_param_mismatch
- Comment: `
        Alias for render_mermaid_to_file (for backward compatibility).
        
        Args:
     `
- Code: `def render_to_file(self, diagram_code, output_path)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'diagram_code', 'self'}

**Line 140** (high): docstring_param_mismatch
- Comment: `
        Replace Mermaid diagrams in content with image references.
        
        Args:
         `
- Code: `def replace_mermaid_with_images(self, content, output_dir)`
- Issue: Docstring params don't match: missing={'Args'}, extra={'self', 'content'}

**Line 184** (high): docstring_param_mismatch
- Comment: `
        Post content to Discord, converting Mermaid diagrams to images.
        
        Args:
    `
- Code: `def post_to_discord_with_mermaid(self, content, webhook_url, username, temp_dir)`
- Issue: Docstring params don't match: missing={'Returns', 'Args'}, extra={'self', 'content'}

### trading_robot\core\broker_factory.py

**Line 13** (high): docstring_param_mismatch
- Comment: `
    Factory function to create broker client based on configuration.
    
    Args:
        broker_`
- Code: `def create_broker_client(broker_name)`
- Issue: Docstring params don't match: missing={'Returns', 'Raises', 'Args'}, extra={'broker_name'}

