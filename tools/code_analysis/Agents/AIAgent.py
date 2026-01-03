"""
AIAgent.py

This module defines a simple AI Agent that manages a collection of plugins.
Each plugin implements a common interface (e.g., having an `execute` method).
The agent can register plugins by name and execute commands via those plugins.
"""

from utils.plugins.LoggerManager import LoggerManager

# Use LoggerManager for logging
logger = LoggerManager(log_file="ai_agent.log").get_logger()
logger.setLevel("DEBUG")


class PluginInterface:
    """
    Example plugin interface.
    Concrete plugins should subclass this interface and implement `execute(command)`.
    """
    def execute(self, command: str) -> str:
        """
        Execute a command or action, returning a response.

        Args:
            command (str): The command or action to perform.

        Returns:
            str: The result or output of the command.
        """
        raise NotImplementedError("Plugins must implement `execute()`.")


class AIAgent:
    """
    AIAgent manages a collection of plugins. Each plugin provides certain
    capabilities (e.g., debugging, quick fixes, memory management).
    The agent acts as a central dispatcher for plugin commands.
    """

    def __init__(self):
        """
        Initializes an AIAgent with an empty plugin registry.
        """
        self.plugins = {}
        logger.info("AIAgent initialized with no plugins.")

    def register_plugin(self, name: str, plugin: PluginInterface):
        """
        Registers a plugin with the agent.

        Args:
            name (str): Unique identifier for the plugin.
            plugin (PluginInterface): A plugin instance implementing `execute()`.
        """
        if not hasattr(plugin, 'execute') or not callable(plugin.execute):
            raise ValueError(f"Plugin '{name}' must implement an `execute` method.")
        self.plugins[name] = plugin
        logger.info(f"Plugin '{name}' registered.")

    def execute(self, plugin_name: str, command: str) -> str:
        """
        Executes a command using the specified plugin.

        Args:
            plugin_name (str): The name of the plugin to use.
            command (str): The command or action to execute.

        Returns:
            str: The result or response from the plugin.

        Raises:
            ValueError: If the specified plugin isn't registered.
        """
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' not found in agent's registry.")
        logger.debug(f"Executing command '{command}' using plugin '{plugin_name}'.")
        return self.plugins[plugin_name].execute(command)


# ==============================
# Example usage (test scenario)
# ==============================
if __name__ == "__main__":
    # Set up a console handler for demonstration (optional)
    from sys import stdout
    from logging import StreamHandler

    console_handler = StreamHandler(stdout)
    console_handler.setLevel("DEBUG")
    logger.addHandler(console_handler)

    # Example plugin implementing PluginInterface
    class EchoPlugin(PluginInterface):
        def execute(self, command: str) -> str:
            return f"EchoPlugin responding to '{command}'"

    # Create an agent
    agent = AIAgent()

    # Create and register a plugin
    echo_plugin = EchoPlugin()
    agent.register_plugin("echo", echo_plugin)

    # Execute a command against the plugin
    result = agent.execute("echo", "Hello, plugin!")
    print(f"Plugin result: {result}")
