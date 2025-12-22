"""
Mindrian Settings

Configuration management using environment variables.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application settings loaded from environment."""

    # API Keys
    anthropic_api_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # Pinecone Configuration
    pinecone_index_name: str = "pws-world"
    pinecone_namespace: str = ""  # Default namespace

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 7777

    # Environment
    environment: str = "development"
    debug: bool = True

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        return cls(
            # API Keys
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            pinecone_api_key=os.getenv("PINECONE_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),

            # Pinecone
            pinecone_index_name=os.getenv("PINECONE_INDEX_NAME", "mindrian-pws-brain"),
            pinecone_namespace=os.getenv("PINECONE_NAMESPACE", "pws-content"),

            # Server
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "7777")),

            # Environment
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "true").lower() == "true",
        )

    def validate(self) -> list[str]:
        """Validate settings and return list of errors."""
        errors = []

        if not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required")

        if not self.pinecone_api_key:
            errors.append("PINECONE_API_KEY is required for PWS Brain")

        return errors


# Global settings instance
settings = Settings.from_env()
