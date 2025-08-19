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
