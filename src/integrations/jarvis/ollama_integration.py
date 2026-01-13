from ..core.unified_entry_point_system import main
from src.core.config.timeout_constants import TimeoutConstants

"""
<!-- SSOT Domain: core -->

Ollama Integration for Local Agents
Provides local LLM capabilities for our custom agents
"""

<<<<<<< HEAD
import os
import platform
import subprocess
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

logger = logging.getLogger(__name__)


@dataclass
<<<<<<< HEAD
class OllamaDiscoveryResult:
    """Result of Ollama discovery attempt"""

    available: bool
    api_url: Optional[str] = None
    cli_path: Optional[str] = None
    models: List[str] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.models is None:
            self.models = []


class OllamaDiscovery:
    """Dynamic discovery of Ollama installations across platforms"""

    @staticmethod
    def get_platform_paths() -> List[str]:
        """Get platform-specific paths where Ollama might be installed"""
        system = platform.system().lower()

        if system == "windows":
            return [
                "C:\\Program Files\\Ollama\\ollama.exe",
                "C:\\Program Files (x86)\\Ollama\\ollama.exe",
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Ollama\\ollama.exe",
                "ollama.exe"  # In PATH
            ]
        elif system == "linux":
            return [
                "/usr/bin/ollama",
                "/usr/local/bin/ollama",
                "/snap/bin/ollama",
                "/opt/ollama/bin/ollama",
                "~/.local/bin/ollama",
                str(Path.home() / ".ollama" / "ollama"),
                "ollama"  # In PATH
            ]
        elif system == "darwin":  # macOS
            return [
                "/usr/local/bin/ollama",
                "/opt/homebrew/bin/ollama",
                "/usr/bin/ollama",
                str(Path.home() / ".ollama" / "ollama"),
                "ollama"  # In PATH
            ]
        else:
            return ["ollama"]  # Fallback to PATH

    @staticmethod
    def find_cli_path() -> Optional[str]:
        """Find the Ollama CLI executable"""
        paths = OllamaDiscovery.get_platform_paths()

        for path in paths:
            expanded_path = Path(path).expanduser()
            if expanded_path.exists() and expanded_path.is_file():
                return str(expanded_path)

            # Try running as command
            try:
                result = subprocess.run(
                    [path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and "ollama" in result.stdout.lower():
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                continue

        return None

    @staticmethod
    def discover_api_endpoints() -> List[str]:
        """Discover possible Ollama API endpoints"""
        endpoints = [
            "http://localhost:11434",
            "http://127.0.0.1:11434",
            "http://localhost:8080",  # Alternative port
            "http://127.0.0.1:8080",
        ]

        # Check environment variables
        env_url = os.environ.get("OLLAMA_HOST")
        if env_url:
            endpoints.insert(0, env_url)

        # Check for remote Ollama instances
        # Could be extended to scan network, but for now just common locations

        return endpoints

    @staticmethod
    def test_api_endpoint(url: str, timeout: int = 2) -> Tuple[bool, List[str]]:
        """Test if an Ollama API endpoint is accessible"""
        try:
            response = requests.get(f"{url}/api/tags", timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                models = [model.get("name", "") for model in data.get("models", [])]
                return True, models
        except Exception:
            pass
        return False, []

    @classmethod
    def discover(cls) -> OllamaDiscoveryResult:
        """Discover Ollama installation and API endpoint"""
        result = OllamaDiscoveryResult(available=False)

        # First, find CLI path
        result.cli_path = cls.find_cli_path()

        # Then, find working API endpoint
        endpoints = cls.discover_api_endpoints()

        for endpoint in endpoints:
            available, models = cls.test_api_endpoint(endpoint)
            if available:
                result.available = True
                result.api_url = endpoint
                result.models = models
                break

        if not result.available:
            result.error = "No accessible Ollama API endpoint found. Make sure Ollama is running."

        return result

    @classmethod
    def get_recommended_config(cls) -> Dict[str, Any]:
        """Get recommended Ollama configuration for current system"""
        discovery = cls.discover()

        config = {
            "available": discovery.available,
            "api_url": discovery.api_url,
            "cli_path": discovery.cli_path,
            "models": discovery.models,
            "error": discovery.error
        }

        return config


@dataclass
=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
class OllamaResponse:
    """Response from Ollama API"""

    model: str
    response: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class OllamaClient:
    """Client for interacting with Ollama API"""

<<<<<<< HEAD
    def __init__(self, base_url: Optional[str] = None, auto_discover: bool = True):
        """
        Initialize Ollama client with dynamic discovery

        Args:
            base_url: Explicit base URL to use, or None to auto-discover
            auto_discover: Whether to auto-discover Ollama if base_url not provided
        """
        if base_url:
            self.base_url = base_url.rstrip("/")
            self.discovery_result = None
        elif auto_discover:
            discovery = OllamaDiscovery.discover()
            if discovery.available and discovery.api_url:
                self.base_url = discovery.api_url.rstrip("/")
                self.discovery_result = discovery
                logger.info(f"Auto-discovered Ollama at: {self.base_url}")
                if discovery.models:
                    logger.info(f"Available models: {', '.join(discovery.models)}")
            else:
                # Fallback to default
                self.base_url = "http://localhost:11434"
                self.discovery_result = discovery
                logger.warning(f"Could not auto-discover Ollama, using fallback: {self.base_url}")
                if discovery.error:
                    logger.warning(f"Discovery error: {discovery.error}")
        else:
            self.base_url = "http://localhost:11434"
            self.discovery_result = None

=======
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
        self.session = requests.Session()
        self.logger = logging.getLogger("OllamaClient")

    def is_available(self) -> bool:
        """Check if Ollama is running and available"""
        try:
<<<<<<< HEAD
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available at {self.base_url}: {e}")
=======
            response = self.session.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            self.get_logger(__name__).warning(f"Ollama not available: {e}")
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
            return False

    def get_models(self) -> List[Dict[str, Any]]:
        """Get list of available models"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception as e:
            self.get_logger(__name__).error(f"Error getting models: {e}")
            return []

    def generate(self, model: str, prompt: str, **kwargs) -> OllamaResponse:
        """Generate text using Ollama"""
        try:
            payload = {"model": model, "prompt": prompt, "stream": False, **kwargs}

            response = self.session.post(f"{self.base_url}/api/generate", json=payload, timeout=TimeoutConstants.HTTP_MEDIUM)

            if response.status_code == 200:
                data = response.json()
                return OllamaResponse(**data)
            else:
                raise Exception(f"Ollama API error: {response.status_code}")

        except Exception as e:
            self.get_logger(__name__).error(f"Error generating text: {e}")
            raise

    async def generate_async(self, model: str, prompt: str, **kwargs) -> OllamaResponse:
        """Generate text asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.generate(model, prompt, **kwargs))


class OllamaAgent:
    """Agent powered by Ollama LLM"""

    def __init__(self, model: str = "llama3.2", client: Optional[OllamaClient] = None):
        self.model = model
        self.client = client or OllamaClient()
        self.logger = logging.getLogger(f"OllamaAgent_{model}")

    def is_ready(self) -> bool:
        """Check if agent is ready to use"""
        return self.client.is_available()

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        models = self.client.get_models()
        for model_info in models:
            if model_info.get("name") == self.model:
                return model_info
        return {}

    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate a response using Ollama"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt

            response = self.client.generate(
                model=self.model, prompt=full_prompt, temperature=0.7, max_tokens=1000
            )

            return response.response

        except Exception as e:
            self.get_logger(__name__).error(f"Error generating response: {e}")
            return f"Error: {str(e)}"

    async def generate_response_async(self, prompt: str, context: str = "") -> str:
        """Generate response asynchronously"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt

            response = await self.client.generate_async(
                model=self.model, prompt=full_prompt, temperature=0.7, max_tokens=1000
            )

            return response.response

        except Exception as e:
            self.get_logger(__name__).error(f"Error generating response: {e}")
            return f"Error: {str(e)}"


class OllamaCodeAgent(OllamaAgent):
    """Specialized agent for code-related tasks"""

    def __init__(self, model: str = "codellama", client: Optional[OllamaClient] = None):
        super().__init__(model, client)
        self.code_context = ""

    def set_code_context(self, code: str):
        """Set the current code context"""
        self.code_context = code

    def analyze_code(self, prompt: str) -> str:
        """Analyze code with context"""
        context = f"Code to analyze:\n{self.code_context}\n\nAnalysis request:"
        return self.generate_response(prompt, context)

    def generate_code(self, description: str) -> str:
        """Generate code based on description"""
        prompt = (
            f"Generate Python code for: {description}\n\nProvide only the code, no explanations:"
        )
        return self.generate_response(prompt)

    def review_code(self, code: str) -> str:
        """Review and suggest improvements for code"""
        prompt = f"Review this code and suggest improvements:\n\n{code}\n\nReview:"
        return self.generate_response(prompt)

    def debug_code(self, code: str, error: str) -> str:
        """Debug code with error information"""
        prompt = f"Debug this code with error:\n\nCode:\n{code}\n\nError:\n{error}\n\nFix:"
        return self.generate_response(prompt)


class OllamaVoiceAgent(OllamaAgent):
    """Agent for voice interaction and natural language processing"""

    def __init__(self, model: str = "llama3.2", client: Optional[OllamaClient] = None):
        super().__init__(model, client)

    def process_voice_command(self, command: str) -> str:
        """Process voice command and return response"""
        prompt = f"Process this voice command and provide a helpful response: {command}"
        return self.generate_response(prompt)

    def extract_intent(self, command: str) -> Dict[str, Any]:
        """Extract intent from voice command"""
        prompt = f"""
        Extract the intent from this voice command and return as JSON:
        Command: {command}
        
        Return format:
        {{
            "intent": "action_type",
            "parameters": {{}},
            "confidence": 0.0
        }}
        """

        response = self.generate_response(prompt)
        try:
            return json.loads(response)
        except:
            return {"intent": "unknown", "parameters": {}, "confidence": 0.0}


class OllamaManager:
    """Manager for multiple Ollama agents"""

    def __init__(self):
        self.agents: Dict[str, OllamaAgent] = {}
        self.client = OllamaClient()
        self.logger = logging.getLogger("OllamaManager")

    def register_agent(self, name: str, agent: OllamaAgent):
        """Register an agent"""
        self.agents[name] = agent
        self.get_logger(__name__).info(f"Registered agent: {name}")

    def get_agent(self, name: str) -> Optional[OllamaAgent]:
        """Get agent by name"""
        return self.agents.get(name)

    def is_available(self) -> bool:
        """Check if Ollama is available"""
        return self.client.is_available()

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return [model.get("name") for model in self.client.get_models()]

    def create_code_agent(self, name: str, model: str = "codellama") -> OllamaCodeAgent:
        """Create and register a code agent"""
        agent = OllamaCodeAgent(model, self.client)
        self.register_agent(name, agent)
        return agent

    def create_voice_agent(self, name: str, model: str = "llama3.2") -> OllamaVoiceAgent:
        """Create and register a voice agent"""
        agent = OllamaVoiceAgent(model, self.client)
        self.register_agent(name, agent)
        return agent


# Example usage

if __name__ == "__main__":
    main()
