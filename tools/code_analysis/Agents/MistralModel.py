import logging
from Agents.SubprocessAIModel import SubprocessAIModel

class MistralModel(SubprocessAIModel):
    """
    AI model integration for Mistral.
    """

    def __init__(self):
        """
        Initializes the Mistral model.
        """
        super().__init__("ollama run mistral:latest", model_name="Mistral")
