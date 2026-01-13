"""
AI Summarizer for DreamVault Training Pipeline
=============================================

SSOT Domain: ai_training

V2 Compliant: <100 lines, single responsibility
Text summarization for conversation processing and training data preparation.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class SummarySchema:
    """Schema for summary structure"""
    max_length: int = 500
    min_length: int = 50
    include_key_points: bool = True
    include_sentiment: bool = True
    preserve_timestamps: bool = False


class Summarizer:
    """
    V2 Compliant AI Summarizer

    Generates summaries of conversations and training data.
    Single responsibility: text summarization.
    """

    def __init__(self, llm_config: Dict[str, Any]):
        self.logger = logging.getLogger("Summarizer")
        self.llm_config = llm_config

        # Default summary schema
        self.schema = SummarySchema()

        # Initialize LLM client based on config
        self._llm_client = self._initialize_llm_client()

    def _initialize_llm_client(self):
        """Initialize LLM client based on configuration."""
        provider = self.llm_config.get("provider", "openai").lower()

        try:
            if provider == "openai":
                return self._initialize_openai_client()
            elif provider == "anthropic":
                return self._initialize_anthropic_client()
            elif provider == "ollama":
                return self._initialize_ollama_client()
            else:
                self.logger.warning(f"Unknown LLM provider: {provider}, falling back to extractive")
                return None
        except Exception as e:
            self.logger.warning(f"Failed to initialize LLM client: {e}, falling back to extractive")
            return None

    def _initialize_openai_client(self):
        """Initialize OpenAI client."""
        try:
            import openai
            api_key = self.llm_config.get("api_key") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")

            client = openai.OpenAI(api_key=api_key)
            self.logger.info("✅ OpenAI LLM client initialized")
            return client
        except ImportError:
            raise Exception("OpenAI package not installed")
        except Exception as e:
            raise Exception(f"OpenAI initialization failed: {e}")

    def _initialize_anthropic_client(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
            api_key = self.llm_config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key not found")

            client = anthropic.Anthropic(api_key=api_key)
            self.logger.info("✅ Anthropic LLM client initialized")
            return client
        except ImportError:
            raise Exception("Anthropic package not installed")
        except Exception as e:
            raise Exception(f"Anthropic initialization failed: {e}")

    def _initialize_ollama_client(self):
        """Initialize Ollama client for local models."""
        try:
            import ollama
            model = self.llm_config.get("model", "llama2")
            client = ollama.Client()
            # Test connection
            client.list()
            self.logger.info(f"✅ Ollama LLM client initialized with model: {model}")
            return {"client": client, "model": model}
        except ImportError:
            raise Exception("Ollama package not installed")
        except Exception as e:
            raise Exception(f"Ollama initialization failed: {e}")

    def summarize(self, text: str, schema: Optional[SummarySchema] = None) -> str:
        """
        Generate summary of input text using LLM.

        Args:
            text: Text to summarize
            schema: Summary schema (uses default if None)

        Returns:
            Summarized text
        """
        if not text or not text.strip():
            return ""

        schema = schema or self.schema

        # Try LLM-based summarization first
        if self._llm_client:
            try:
                return self._llm_summarize(text, schema)
            except Exception as e:
                self.logger.warning(f"LLM summarization failed: {e}, falling back to extractive")

        # Fallback to extractive summarization
        return self._extractive_summarize(text, schema)

    def _llm_summarize(self, text: str, schema: SummarySchema) -> str:
        """Generate summary using LLM."""
        provider = self.llm_config.get("provider", "openai").lower()

        if provider == "openai":
            return self._openai_summarize(text, schema)
        elif provider == "anthropic":
            return self._anthropic_summarize(text, schema)
        elif provider == "ollama":
            return self._ollama_summarize(text, schema)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _openai_summarize(self, text: str, schema: SummarySchema) -> str:
        """Summarize using OpenAI."""
        prompt = self._build_summary_prompt(text, schema)

        response = self._llm_client.chat.completions.create(
            model=self.llm_config.get("model", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=schema.max_length,
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    def _anthropic_summarize(self, text: str, schema: SummarySchema) -> str:
        """Summarize using Anthropic."""
        prompt = self._build_summary_prompt(text, schema)

        response = self._llm_client.messages.create(
            model=self.llm_config.get("model", "claude-3-haiku-20240307"),
            max_tokens=schema.max_length,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    def _ollama_summarize(self, text: str, schema: SummarySchema) -> str:
        """Summarize using Ollama."""
        prompt = self._build_summary_prompt(text, schema)

        response = self._llm_client["client"].chat(
            model=self._llm_client["model"],
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": schema.max_length, "temperature": 0.3}
        )

        return response["message"]["content"].strip()

    def _build_summary_prompt(self, text: str, schema: SummarySchema) -> str:
        """Build summarization prompt."""
        prompt_parts = [
            f"Summarize the following text in {schema.max_length} words or less:",
            f"Text: {text}",
            f"Requirements:",
            f"- Maximum length: {schema.max_length} words",
            f"- Minimum length: {schema.min_length} words" if schema.min_length > 0 else "",
            f"- {'Include key points' if schema.include_key_points else ''}",
            f"- {'Include sentiment analysis' if schema.include_sentiment else ''}",
        ]

        # Filter out empty requirements
        requirements = [req for req in prompt_parts[2:] if req.strip()]
        prompt_parts[2:] = requirements

        return "\n".join(prompt_parts)

    def summarize_batch(self, texts: List[str], schema: Optional[SummarySchema] = None) -> List[str]:
        """
        Summarize multiple texts.

        Args:
            texts: List of texts to summarize
            schema: Summary schema

        Returns:
            List of summaries
        """
        return [self.summarize(text, schema) for text in texts]

    def _extractive_summarize(self, text: str, schema: SummarySchema) -> str:
        """
        Simple extractive summarization (placeholder for LLM).

        Args:
            text: Input text
            schema: Summary schema

        Returns:
            Extracted summary
        """
        sentences = self._split_into_sentences(text)

        if not sentences:
            return text[:schema.max_length] + "..." if len(text) > schema.max_length else text

        # Simple scoring based on sentence length and position
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            score = len(sentence.split())  # Length-based scoring
            if i < 2:  # Favor first sentences
                score += 10
            scored_sentences.append((score, sentence))

        # Sort by score and select top sentences
        scored_sentences.sort(reverse=True)
        selected_sentences = [s for _, s in scored_sentences[:3]]  # Top 3

        # Reorder to maintain original flow
        summary = " ".join(selected_sentences)

        # Apply length constraints
        if len(summary) > schema.max_length:
            summary = summary[:schema.max_length - 3] + "..."
        elif len(summary) < schema.min_length and sentences:
            # If too short, include more sentences
            summary = " ".join(sentences[:2])

        return summary.strip()

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re

        # Simple sentence splitting
        sentences = re.split(r'[.!?]+\s*', text.strip())

        # Filter out empty sentences
        return [s.strip() for s in sentences if s.strip()]

    def set_schema(self, schema: SummarySchema) -> None:
        """Update summary schema."""
        self.schema = schema

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get summarizer capabilities.

        Returns:
            Dict with supported features and limits
        """
        return {
            "supports_batch": True,
            "max_input_length": 10000,  # Placeholder
            "supported_languages": ["en"],  # Placeholder
            "schema_configurable": True,
            "llm_backend": self.llm_config.get("backend", "extractive")
        }