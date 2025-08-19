"""
Application configuration management.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Database Configuration (for future use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # LLM Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1500"))
    
    @property
    def is_openai_configured(self) -> bool:
        """Check if OpenAI API key is properly configured."""
        return bool(self.OPENAI_API_KEY)

# Global settings instance
settings = Settings()

# Print configuration status on import
print(f"Configuration loaded:")
print(f"  - OpenAI API key configured: {settings.is_openai_configured}")
print(f"  - API Host: {settings.API_HOST}")
print(f"  - API Port: {settings.API_PORT}")
print(f"  - LLM Model: {settings.LLM_MODEL}")
print(f"  - LLM Temperature: {settings.LLM_TEMPERATURE}")
print(f"  - LLM Max Tokens: {settings.LLM_MAX_TOKENS}")
