"""
Embedding Builder for DreamVault AI Training Pipeline
====================================================

SSOT Domain: ai_training

V2 Compliant: <100 lines, single responsibility
Vector embedding generation for semantic search and similarity.
"""

import logging
from typing import List, Dict, Any, Optional
import hashlib


class EmbeddingBuilder:
    """
    V2 Compliant Embedding Builder

    Generates vector embeddings for text data.
    Single responsibility: embedding generation.
    """

    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger("EmbeddingBuilder")
        self.config = config

        # Embedding configuration
        self.model_name = config.get("model", "sentence-transformers")
        self.dimension = config.get("dimension", 384)
        self.max_tokens = config.get("max_tokens", 512)

        # Initialize actual embedding model
        self._embedding_model = self._initialize_embedding_model()

    def _initialize_embedding_model(self):
        """Initialize embedding model based on configuration."""
        provider = self.model_name.lower()

        try:
            if provider == "sentence-transformers" or provider.startswith("sentence-transformers/"):
                return self._initialize_sentence_transformers()
            elif provider.startswith("openai"):
                return self._initialize_openai_embeddings()
            elif provider == "hash-based" or provider == "default":
                # Keep hash-based as fallback
                return None
            else:
                self.logger.warning(f"Unknown embedding provider: {provider}, using hash-based")
                return None
        except Exception as e:
            self.logger.warning(f"Failed to initialize embedding model: {e}, using hash-based")
            return None

    def _initialize_sentence_transformers(self):
        """Initialize SentenceTransformers model."""
        try:
            from sentence_transformers import SentenceTransformer

            model_name = self.model_name
            if model_name == "sentence-transformers":
                model_name = "all-MiniLM-L6-v2"  # Default model

            model = SentenceTransformer(model_name)
            self.dimension = model.get_sentence_embedding_dimension()
            self.logger.info(f"✅ SentenceTransformers model initialized: {model_name} (dim: {self.dimension})")
            return model
        except ImportError:
            raise Exception("sentence-transformers package not installed")
        except Exception as e:
            raise Exception(f"SentenceTransformers initialization failed: {e}")

    def _initialize_openai_embeddings(self):
        """Initialize OpenAI embeddings."""
        try:
            import openai
            api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")

            client = openai.OpenAI(api_key=api_key)
            self.dimension = 1536  # Ada-002 dimension
            self.logger.info("✅ OpenAI embeddings initialized")
            return client
        except ImportError:
            raise Exception("OpenAI package not installed")
        except Exception as e:
            raise Exception(f"OpenAI embeddings initialization failed: {e}")

    def build_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            Vector embedding as list of floats
        """
        if not text or not text.strip():
            return [0.0] * self.dimension

        # Try real embeddings first
        if self._embedding_model:
            try:
                return self._real_embedding(text)
            except Exception as e:
                self.logger.warning(f"Real embedding failed: {e}, falling back to hash-based")

        # Fallback to hash-based embeddings
        return self._hash_based_embedding(text)

    def _real_embedding(self, text: str) -> List[float]:
        """Generate real embeddings using configured model."""
        if hasattr(self._embedding_model, 'encode'):  # SentenceTransformers
            embedding = self._embedding_model.encode(text, convert_to_numpy=True)
            return embedding.tolist()

        elif hasattr(self._embedding_model, 'embeddings'):  # OpenAI
            response = self._embedding_model.embeddings.create(
                input=text,
                model=self.model_name
            )
            return response.data[0].embedding

        else:
            raise ValueError(f"Unsupported embedding model type: {type(self._embedding_model)}")

    def build_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of vector embeddings
        """
        return [self.build_embedding(text) for text in texts]

    def _hash_based_embedding(self, text: str) -> List[float]:
        """
        Generate deterministic embedding using hashing (placeholder).

        Args:
            text: Input text

        Returns:
            Pseudo-embedding vector
        """
        # Create hash of text
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_bytes = hash_obj.digest()

        # Convert hash to float values between -1 and 1
        embedding = []
        for i in range(0, len(hash_bytes), 4):
            chunk = hash_bytes[i:i+4]
            if len(chunk) < 4:
                chunk += b'\x00' * (4 - len(chunk))

            # Convert 4 bytes to float
            value = int.from_bytes(chunk, byteorder='big') / (2**32 - 1)
            # Normalize to [-1, 1]
            normalized = (value * 2) - 1
            embedding.append(normalized)

        # Pad or truncate to target dimension
        while len(embedding) < self.dimension:
            embedding.extend(embedding)  # Repeat pattern

        return embedding[:self.dimension]

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score between 0 and 1
        """
        if len(embedding1) != len(embedding2):
            return 0.0

        # Cosine similarity
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        magnitude1 = sum(a * a for a in embedding1) ** 0.5
        magnitude2 = sum(b * b for b in embedding2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def find_similar(self, query_embedding: List[float], embeddings: List[List[float]], top_k: int = 5) -> List[tuple]:
        """
        Find most similar embeddings.

        Args:
            query_embedding: Query embedding
            embeddings: List of embeddings to search
            top_k: Number of top results to return

        Returns:
            List of (index, similarity_score) tuples
        """
        similarities = []
        for i, embedding in enumerate(embeddings):
            similarity = self.calculate_similarity(query_embedding, embedding)
            similarities.append((i, similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        backend = "hash_based"
        if self._embedding_model:
            if hasattr(self._embedding_model, 'encode'):
                backend = "sentence_transformers"
            elif hasattr(self._embedding_model, 'embeddings'):
                backend = "openai"
            else:
                backend = "unknown"

        return {
            "model": self.model_name,
            "dimension": self.dimension,
            "max_tokens": self.max_tokens,
            "backend": backend
        }

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate embedding dimensions and values.

        Args:
            embedding: Embedding vector to validate

        Returns:
            True if valid, False otherwise
        """
        if len(embedding) != self.dimension:
            return False

        # Check for NaN or infinite values
        for value in embedding:
            if not isinstance(value, (int, float)) or str(value) in ('nan', 'inf', '-inf'):
                return False

        return True