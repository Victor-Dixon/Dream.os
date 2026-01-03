import asyncio
import logging
from Agents.AIModel import AIModel

class SubprocessAIModel(AIModel):
    """
    Base class for AI models that use subprocesses to generate fixes.
    """

    def __init__(self, command: str, model_name: str):
        """
        Args:
            command (str): The command to run the model (e.g., "ollama run mistral:latest").
            model_name (str): A human-readable name for logging.
        """
        self.command = command
        self.model_name = model_name
        self.logger = logging.getLogger(self.__class__.__name__)

    async def generate_fix(self, error_type: str, error_message: str) -> str:
        """
        Asynchronously generates a fix suggestion by invoking an AI model via subprocess.

        Args:
            error_type (str): The type of error detected.
            error_message (str): The error message.

        Returns:
            str: The fix suggestion, or an empty string if generation fails.
        """
        prompt = (
            f"Provide a fix suggestion for the following error:\n"
            f"Error Type: {error_type}\n"
            f"Error Message: {error_message}\n"
            "Fix:"
        )
        try:
            process = await asyncio.create_subprocess_exec(
                *self.command.split(),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate(input=prompt.encode("utf-8"))

            if process.returncode == 0:
                fix = stdout.decode().strip()
                self.logger.info(f"{self.model_name}-generated fix for {error_type}: {fix}")
                return fix
            else:
                self.logger.error(f"{self.model_name} failed: {stderr.decode().strip()}")
                return ""
        except FileNotFoundError:
            self.logger.error(f"{self.model_name} is not installed or not accessible in the PATH.")
            return ""
        except Exception as e:
            self.logger.error(f"Error using {self.model_name} for {error_type}: {str(e)}")
            return ""
