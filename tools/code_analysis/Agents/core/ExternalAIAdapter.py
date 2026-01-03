import json
import requests
import logging
from requests.exceptions import RequestException, HTTPError, Timeout
from Agents.core.AgentBase import AgentBase

# Configure logging
logging.basicConfig(
    filename='external_ai_adapter.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ExternalAIAdapter(AgentBase):
    """
    Adapter for a third-party AI model.
    
    Wraps API calls to the external AI model and conforms to the AgentBase interface.
    """

    def __init__(self, api_key: str, endpoint: str, timeout: int = 10, max_retries: int = 3):
        """
        Initializes the ExternalAIAdapter.

        Args:
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            timeout (int): Request timeout in seconds (default: 10).
            max_retries (int): Number of retries on request failure (default: 3).
        """
        super().__init__()
        self.api_key = api_key
        self.endpoint = endpoint
        self.timeout = timeout
        self.max_retries = max_retries

    def solve_task(self, action: str, **kwargs) -> dict:
        """
        Sends a request to the external AI model to perform a specified action.

        Args:
            action (str): The action to be performed.
            **kwargs: Additional parameters for the API request.

        Returns:
            dict: Dictionary containing success status and result or error message.
        """
        payload = {
            "action": action,
            "parameters": kwargs
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                logging.info(f"Attempt {attempt}: Sending request to {self.endpoint} with payload: {payload}")
                response = requests.post(self.endpoint, json=payload, headers=headers, timeout=self.timeout)
                response.raise_for_status()

                # Validate response structure
                result = response.json()
                if "result" not in result:
                    raise ValueError("Unexpected API response format: 'result' field missing.")

                logging.info(f"Response received: {result}")
                return {"status": "success", "result": result.get("result")}

            except (RequestException, HTTPError, Timeout) as e:
                logging.error(f"API call failed on attempt {attempt}: {str(e)}")
                if attempt == self.max_retries:
                    return {"error": f"External AI model call failed after {self.max_retries} attempts: {str(e)}"}
            except ValueError as e:
                logging.error(f"Response validation error: {str(e)}")
                return {"error": f"Invalid response from AI model: {str(e)}"}

        return {"error": "Unknown failure in ExternalAIAdapter."}
