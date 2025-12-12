================================================================================
COMMENT-CODE MISMATCH ANALYSIS REPORT
================================================================================

Total Mismatches Found: 92
  Critical: 0
  High: 22
  Medium: 70
  Low: 0


================================================================================
HIGH SEVERITY MISMATCHES (22)
================================================================================

File: src\ai_training\dreamvault\database.py:43
Type: parameter_missing
Description: Function '__init__' docstring mentions parameter 'Defaults to sqlite' but it's not in function signature
Code: def __init__(self, database_url)
Comment: Defaults to sqlite:///data/dreamvault.db

File: src\ai_training\dreamvault\database.py:26
Type: method_missing
Description: Class 'DatabaseConnection' docstring mentions method 'cursor()' but method doesn't exist
Code: class DatabaseConnection
Comment: Method: cursor()

File: src\architecture\design_patterns.py:74
Type: method_missing
Description: Class 'Factory' docstring mentions method 'Type1Class()' but method doesn't exist
Code: class Factory
Comment: Method: Type1Class()

File: src\architecture\design_patterns.py:122
Type: method_missing
Description: Class 'Subject' docstring mentions method 'MyObserver()' but method doesn't exist
Code: class Subject
Comment: Method: MyObserver()

File: src\core\error_handling\circuit_breaker\protocol.py:33
Type: parameter_missing
Description: Function 'call' docstring mentions parameter '*args' but it's not in function signature
Code: def call(self, func)
Comment: *args: Positional arguments for function

File: src\core\error_handling\circuit_breaker\protocol.py:33
Type: parameter_missing
Description: Function 'call' docstring mentions parameter '**kwargs' but it's not in function signature
Code: def call(self, func)
Comment: **kwargs: Keyword arguments for function

File: src\core\orchestration\base_orchestrator.py:26
Type: method_missing
Description: Class 'BaseOrchestrator' docstring mentions method 'super()' but method doesn't exist
Code: class BaseOrchestrator
Comment: Method: super()

File: src\core\session\base_session_manager.py:78
Type: parameter_missing
Description: Function 'create_session' docstring mentions parameter '**kwargs' but it's not in function signature
Code: def create_session(self, service_name)
Comment: **kwargs: Implementation-specific parameters

File: src\core\session\rate_limited_session_manager.py:69
Type: parameter_missing
Description: Function 'create_session' docstring mentions parameter '**kwargs' but it's not in function signature
Code: def create_session(self, service_name)
Comment: **kwargs: Additional session parameters

File: src\core\utils\coordination_utils.py:100
Type: parameter_missing
Description: Function 'store_coordination_history' docstring mentions parameter '**kwargs' but it's not in function signature
Code: def store_coordination_history(entry)
Comment: **kwargs: Additional history data (merged into entry)

File: src\core\utils\validation_utils.py:47
Type: method_missing
Description: Class 'ValidationReporter' docstring mentions method 'print_validation_report()' but method doesn't exist
Code: class ValidationReporter
Comment: Method: print_validation_report()

File: src\core\base\base_handler.py:26
Type: method_missing
Description: Class 'BaseHandler' docstring mentions method 'super()' but method doesn't exist
Code: class BaseHandler
Comment: Method: super()

File: src\core\base\base_manager.py:26
Type: method_missing
Description: Class 'BaseManager' docstring mentions method 'super()' but method doesn't exist
Code: class BaseManager
Comment: Method: super()

File: src\core\base\base_service.py:26
Type: method_missing
Description: Class 'BaseService' docstring mentions method 'super()' but method doesn't exist
Code: class BaseService
Comment: Method: super()

File: src\domain\ports\logger.py:31
Type: parameter_missing
Description: Function 'debug' docstring mentions parameter '**context' but it's not in function signature
Code: def debug(self, message)
Comment: **context: Additional context data

File: src\domain\ports\logger.py:41
Type: parameter_missing
Description: Function 'info' docstring mentions parameter '**context' but it's not in function signature
Code: def info(self, message)
Comment: **context: Additional context data

File: src\domain\ports\logger.py:51
Type: parameter_missing
Description: Function 'warning' docstring mentions parameter '**context' but it's not in function signature
Code: def warning(self, message)
Comment: **context: Additional context data

File: src\infrastructure\logging\std_logger.py:43
Type: parameter_missing
Description: Function 'debug' docstring mentions parameter '**context' but it's not in function signature
Code: def debug(self, message)
Comment: **context: Additional context data

File: src\infrastructure\logging\std_logger.py:53
Type: parameter_missing
Description: Function 'info' docstring mentions parameter '**context' but it's not in function signature
Code: def info(self, message)
Comment: **context: Additional context data

File: src\infrastructure\logging\std_logger.py:63
Type: parameter_missing
Description: Function 'warning' docstring mentions parameter '**context' but it's not in function signature
Code: def warning(self, message)
Comment: **context: Additional context data

File: src\services\chatgpt\session.py:354
Type: parameter_missing
Description: Function 'create_session' docstring mentions parameter '**kwargs' but it's not in function signature
Code: def create_session(self, service_name)
Comment: **kwargs: Additional session parameters

File: src\services\utils\messaging_templates.py:36
Type: parameter_missing
Description: Function 'format_template' docstring mentions parameter '**kwargs' but it's not in function signature
Code: def format_template(template)
Comment: **kwargs: Template variables


================================================================================
MEDIUM SEVERITY MISMATCHES (70)
================================================================================

File: src\discord_commander\test_utils.py:124
Type: type_hint_missing
Description: Function 'get_mock_discord' docstring contains type information but function has no type hints
Code: def get_mock_discord(...)
Comment: Types mentioned: Tuple

File: src\discord_commander\test_utils.py:134
Type: type_hint_missing
Description: Function 'create_mock_discord_imports' docstring contains type information but function has no type hints
Code: def create_mock_discord_imports(...)
Comment: Types mentioned: Dict

File: src\discord_commander\unified_discord_bot.py:1454
Type: type_hint_missing
Description: Function '_perform_true_restart' docstring contains type information but function has no type hints
Code: def _perform_true_restart(...)
Comment: Types mentioned: spawn

File: src\ai_training\dreamvault\runner.py:26
Type: type_hint_missing
Description: Function '__init__' docstring contains type information but function has no type hints
Code: def __init__(...)
Comment: Types mentioned: config, Configuration

File: src\core\keyboard_control_lock.py:119
Type: type_hint_missing
Description: Function 'force_release_lock' docstring contains type information but function has no type hints
Code: def force_release_lock(...)
Comment: Types mentioned: Only

File: src\core\messaging_protocol_models.py:34
Type: return_mismatch
Description: Function 'send_message' docstring describes return value but function has no return statement
Code: def send_message(...)
Comment: bool: True if delivery successful, False otherwise

File: src\core\messaging_protocol_models.py:55
Type: return_mismatch
Description: Function 'generate_onboarding_message' docstring describes return value but function has no return statement
Code: def generate_onboarding_message(...)
Comment: str: Formatted onboarding message content

File: src\core\messaging_protocol_models.py:77
Type: return_mismatch
Description: Function 'format_message' docstring describes return value but function has no return statement
Code: def format_message(...)
Comment: str: Formatted message content

File: src\core\messaging_protocol_models.py:99
Type: return_mismatch
Description: Function 'check_and_rotate' docstring describes return value but function has no return statement
Code: def check_and_rotate(...)
Comment: bool: True if rotation performed, False otherwise

File: src\core\error_handling\circuit_breaker\protocol.py:33
Type: return_mismatch
Description: Function 'call' docstring describes return value but function has no return statement
Code: def call(...)
Comment: Function result

File: src\core\error_handling\circuit_breaker\protocol.py:51
Type: return_mismatch
Description: Function 'get_state' docstring describes return value but function has no return statement
Code: def get_state(...)
Comment: State string: "closed", "open", or "half_open"

File: src\core\error_handling\circuit_breaker\protocol.py:60
Type: return_mismatch
Description: Function 'get_status' docstring describes return value but function has no return statement
Code: def get_status(...)
Comment: Dictionary with status information:
    - name: Circuit breaker name
    - state: Current state
    

File: src\core\orchestration\base_orchestrator.py:100
Type: return_mismatch
Description: Function '_load_default_config' docstring describes return value but function has no return statement
Code: def _load_default_config(...)
Comment: Dictionary of default configuration values

File: src\core\session\base_session_manager.py:92
Type: return_mismatch
Description: Function 'validate_session' docstring describes return value but function has no return statement
Code: def validate_session(...)
Comment: True if valid, False otherwise

File: src\core\stress_testing\messaging_core_protocol.py:24
Type: return_mismatch
Description: Function 'send_message' docstring describes return value but function has no return statement
Code: def send_message(...)
Comment: True if delivery successful, False otherwise

File: src\domain\ports\clock.py:21
Type: return_mismatch
Description: Function 'now' docstring describes return value but function has no return statement
Code: def now(...)
Comment: Current datetime in UTC

File: src\domain\ports\clock.py:30
Type: return_mismatch
Description: Function 'utcnow' docstring describes return value but function has no return statement
Code: def utcnow(...)
Comment: Current UTC datetime

File: src\domain\ports\clock.py:39
Type: return_mismatch
Description: Function 'from_timestamp' docstring describes return value but function has no return statement
Code: def from_timestamp(...)
Comment: Datetime object

File: src\domain\ports\clock.py:51
Type: return_mismatch
Description: Function 'to_timestamp' docstring describes return value but function has no return statement
Code: def to_timestamp(...)
Comment: Unix timestamp (seconds since epoch)

File: src\domain\ports\agent_repository.py:38
Type: return_mismatch
Description: Function 'get_by_capability' docstring describes return value but function has no return statement
Code: def get_by_capability(...)
Comment: Iterable of agents with the specified capability

File: src\domain\ports\agent_repository.py:50
Type: return_mismatch
Description: Function 'get_active' docstring describes return value but function has no return statement
Code: def get_active(...)
Comment: Iterable of active agents

File: src\domain\ports\agent_repository.py:59
Type: return_mismatch
Description: Function 'get_available' docstring describes return value but function has no return statement
Code: def get_available(...)
Comment: Iterable of available agents

File: src\domain\ports\agent_repository.py:89
Type: return_mismatch
Description: Function 'delete' docstring describes return value but function has no return statement
Code: def delete(...)
Comment: True if agent was deleted, False if not found

File: src\domain\ports\agent_repository.py:101
Type: return_mismatch
Description: Function 'list_all' docstring describes return value but function has no return statement
Code: def list_all(...)
Comment: Iterable of all agents

File: src\domain\ports\browser.py:77
Type: return_mismatch
Description: Function 'send_and_wait' docstring describes return value but function has no return statement
Code: def send_and_wait(...)
Comment: PageReply with response data

File: src\domain\ports\browser.py:110
Type: return_mismatch
Description: Function 'is_ready' docstring describes return value but function has no return statement
Code: def is_ready(...)
Comment: True if browser is ready, False otherwise

File: src\domain\ports\browser.py:130
Type: return_mismatch
Description: Function 'wait_for_element' docstring describes return value but function has no return statement
Code: def wait_for_element(...)
Comment: True if element appeared, False if timeout

File: src\domain\ports\message_bus.py:33
Type: return_mismatch
Description: Function 'publish' docstring describes return value but function has no return statement
Code: def publish(...)
Comment: True if published successfully, False otherwise

File: src\domain\ports\message_bus.py:57
Type: return_mismatch
Description: Function 'subscribe' docstring describes return value but function has no return statement
Code: def subscribe(...)
Comment: Handler ID (generated if not provided)

File: src\domain\ports\message_bus.py:80
Type: return_mismatch
Description: Function 'unsubscribe' docstring describes return value but function has no return statement
Code: def unsubscribe(...)
Comment: True if handler was removed, False if not found

File: src\domain\ports\message_bus.py:96
Type: return_mismatch
Description: Function 'get_subscribers' docstring describes return value but function has no return statement
Code: def get_subscribers(...)
Comment: Dictionary mapping event types to list of handler IDs

File: src\domain\ports\message_bus.py:109
Type: return_mismatch
Description: Function 'is_available' docstring describes return value but function has no return statement
Code: def is_available(...)
Comment: True if message bus is available, False otherwise

File: src\domain\ports\message_bus.py:119
Type: return_mismatch
Description: Function 'get_stats' docstring describes return value but function has no return statement
Code: def get_stats(...)
Comment: Dictionary with stats (total_events, subscribers_count, etc.)

File: src\domain\ports\task_repository.py:39
Type: return_mismatch
Description: Function 'get_by_agent' docstring describes return value but function has no return statement
Code: def get_by_agent(...)
Comment: Iterable of tasks assigned to the agent

File: src\domain\ports\task_repository.py:52
Type: return_mismatch
Description: Function 'get_pending' docstring describes return value but function has no return statement
Code: def get_pending(...)
Comment: Iterable of pending tasks

File: src\domain\ports\task_repository.py:85
Type: return_mismatch
Description: Function 'delete' docstring describes return value but function has no return statement
Code: def delete(...)
Comment: True if task was deleted, False if not found

File: src\domain\ports\task_repository.py:97
Type: return_mismatch
Description: Function 'list_all' docstring describes return value but function has no return statement
Code: def list_all(...)
Comment: Iterable of all tasks

File: src\gaming\dreamos\ui_integration.py:470
Type: type_hint_missing
Description: Function 'register_gamification_blueprint' docstring contains type information but function has no type hints
Code: def register_gamification_blueprint(...)
Comment: Types mentioned: app, Flask

File: src\infrastructure\browser\unified\driver_manager.py:95
Type: type_hint_missing
Description: Function '_setup_chrome_options' docstring contains type information but function has no type hints
Code: def _setup_chrome_options(...)
Comment: Types mentioned: ChromeOptions, Configured

File: src\infrastructure\browser\unified\driver_manager.py:123
Type: type_hint_missing
Description: Function 'get_driver' docstring contains type information but function has no type hints
Code: def get_driver(...)
Comment: Types mentioned: Chrome, Undetected, Exception

File: src\infrastructure\browser\unified\driver_manager.py:150
Type: type_hint_missing
Description: Function 'close_driver' docstring contains type information but function has no type hints
Code: def close_driver(...)
Comment: Types mentioned: Exception, If

File: src\infrastructure\browser\unified\driver_manager.py:165
Type: type_hint_missing
Description: Function '__enter__' docstring contains type information but function has no type hints
Code: def __enter__(...)
Comment: Types mentioned: Chrome, WebDriver

File: src\infrastructure\browser\unified\driver_manager.py:174
Type: type_hint_missing
Description: Function '__exit__' docstring contains type information but function has no type hints
Code: def __exit__(...)
Comment: Types mentioned: exc_type, Exception, Exception

File: src\infrastructure\persistence\base_file_repository.py:55
Type: return_mismatch
Description: Function '_get_default_data' docstring describes return value but function has no return statement
Code: def _get_default_data(...)
Comment: Dictionary with default structure including metadata

File: src\infrastructure\persistence\base_file_repository.py:65
Type: return_mismatch
Description: Function '_get_data_key' docstring describes return value but function has no return statement
Code: def _get_data_key(...)
Comment: Key name (e.g., "contracts", "messages", "activity_logs")

File: src\infrastructure\persistence\sqlite_agent_repo.py:90
Type: return_mismatch
Description: Function 'get_by_capability' docstring describes return value but function has no return statement
Code: def get_by_capability(...)
Comment: Iterable of agents with the specified capability

File: src\infrastructure\persistence\sqlite_agent_repo.py:114
Type: return_mismatch
Description: Function 'get_active' docstring describes return value but function has no return statement
Code: def get_active(...)
Comment: Iterable of active agents

File: src\infrastructure\persistence\sqlite_agent_repo.py:135
Type: return_mismatch
Description: Function 'get_available' docstring describes return value but function has no return statement
Code: def get_available(...)
Comment: Iterable of available agents

File: src\infrastructure\persistence\sqlite_agent_repo.py:223
Type: return_mismatch
Description: Function 'list_all' docstring describes return value but function has no return statement
Code: def list_all(...)
Comment: Iterable of all agents

File: src\infrastructure\persistence\sqlite_task_repo.py:91
Type: return_mismatch
Description: Function 'get_by_agent' docstring describes return value but function has no return statement
Code: def get_by_agent(...)
Comment: Iterable of tasks assigned to the agent

File: src\infrastructure\persistence\sqlite_task_repo.py:118
Type: return_mismatch
Description: Function 'get_pending' docstring describes return value but function has no return statement
Code: def get_pending(...)
Comment: Iterable of pending tasks

File: src\infrastructure\persistence\sqlite_task_repo.py:203
Type: return_mismatch
Description: Function 'list_all' docstring describes return value but function has no return statement
Code: def list_all(...)
Comment: Iterable of all tasks

File: src\message_task\emitters.py:23
Type: type_hint_missing
Description: Function '__init__' docstring contains type information but function has no type hints
Code: def __init__(...)
Comment: Types mentioned: messaging_bus, Messaging

File: src\message_task\ingestion_pipeline.py:24
Type: type_hint_missing
Description: Function '__init__' docstring contains type information but function has no type hints
Code: def __init__(...)
Comment: Types mentioned: task_repository, SqliteTaskRepository, Messaging

File: src\message_task\router.py:27
Type: type_hint_missing
Description: Function '__init__' docstring contains type information but function has no type hints
Code: def __init__(...)
Comment: Types mentioned: task_repository, SqliteTaskRepository

File: src\opensource\task_integration.py:20
Type: type_hint_missing
Description: Function '__init__' docstring contains type information but function has no type hints
Code: def __init__(...)
Comment: Types mentioned: project_manager, OpenSourceProjectManager, SqliteTaskRepository

File: src\orchestrators\overnight\integration_example.py:39
Type: type_hint_missing
Description: Function 'example_message_plans' docstring contains type information but function has no type hints
Code: def example_message_plans(...)
Comment: Types mentioned: Using

File: src\orchestrators\overnight\integration_example.py:61
Type: type_hint_missing
Description: Function 'example_fsm_bridge' docstring contains type information but function has no type hints
Code: def example_fsm_bridge(...)
Comment: Types mentioned: Using

File: src\orchestrators\overnight\integration_example.py:90
Type: type_hint_missing
Description: Function 'example_inbox_consumer' docstring contains type information but function has no type hints
Code: def example_inbox_consumer(...)
Comment: Types mentioned: Using

File: src\orchestrators\overnight\integration_example.py:116
Type: type_hint_missing
Description: Function 'example_listener' docstring contains type information but function has no type hints
Code: def example_listener(...)
Comment: Types mentioned: Using

File: src\orchestrators\overnight\integration_example.py:140
Type: type_hint_missing
Description: Function 'example_fsm_updates_processor' docstring contains type information but function has no type hints
Code: def example_fsm_updates_processor(...)
Comment: Types mentioned: Processing

File: src\orchestrators\overnight\integration_example.py:154
Type: type_hint_missing
Description: Function 'example_integrated_workflow' docstring contains type information but function has no type hints
Code: def example_integrated_workflow(...)
Comment: Types mentioned: Integrated

File: src\orchestrators\overnight\scheduler_integration.py:42
Type: type_hint_missing
Description: Function '__init__' docstring contains type information but function has no type hints
Code: def __init__(...)
Comment: Types mentioned: scheduler, TaskScheduler, StatusChangeMonitor

File: src\services\chat_presence\twitch_bridge.py:526
Type: type_hint_missing
Description: Function '_connect' docstring contains type information but function has no type hints
Code: def _connect(...)
Comment: Types mentioned: Password

File: src\web\engines_routes.py:33
Type: type_hint_missing
Description: Function 'get_engine_discovery' docstring contains type information but function has no type hints
Code: def get_engine_discovery(...)
Comment: Types mentioned: JSON

File: src\web\repository_merge_routes.py:32
Type: type_hint_missing
Description: Function 'get_merge_status' docstring contains type information but function has no type hints
Code: def get_merge_status(...)
Comment: Types mentioned: JSON

File: src\web\repository_merge_routes.py:310
Type: type_hint_missing
Description: Function 'get_merge_attempts' docstring contains type information but function has no type hints
Code: def get_merge_attempts(...)
Comment: Types mentioned: Filter, Filter, Filter

File: src\workflows\strategies.py:53
Type: return_mismatch
Description: Function 'can_execute_step' docstring describes return value but function has no return statement
Code: def can_execute_step(...)
Comment: True if step can be executed

File: src\workflows\gpt_integration.py:155
Type: type_hint_missing
Description: Function 'create_gpt_step_builder' docstring contains type information but function has no type hints
Code: def create_gpt_step_builder(...)
Comment: Types mentioned: GPTStepBuilder

File: src\control_plane\adapters\base.py:24
Type: return_mismatch
Description: Function 'run_allowed' docstring describes return value but function has no return statement
Code: def run_allowed(...)
Comment: Result dict with status and message/details.
