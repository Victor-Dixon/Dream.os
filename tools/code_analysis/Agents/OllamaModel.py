import logging
from Agents.SubprocessAIModel import SubprocessAIModel

class OllamaModel(SubprocessAIModel):
    """
    AI model integration for Ollama.

    Based on the output of:
      (base) PS D:\AgentProject> ollama list
      NAME                     ID              SIZE      MODIFIED    
      deepseek-coder:latest    3ddd2d3fc8d2    776 MB    8 days ago
      deepseek-r1:latest       0a8c26691023    4.7 GB    11 days ago
      mistral:latest           f974a74358d6    4.1 GB    11 days ago

    You can select the appropriate model. For instance, to use the 'mistral:latest' model,
    initialize the class as follows:

        ollama = OllamaModel("ollama run mistral:latest")
    """

    def __init__(self):
        """
        Initializes the Ollama model with the default model command.
        Change 'mistral:latest' to another model if needed.
        """
        super().__init__("ollama run mistral:latest", model_name="Ollama")
