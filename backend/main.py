"""
Entry point that uses the modular structure.

This imports from the organized app/ directory structure.
"""

from app.main import app
from app.config import settings

# Re-export the app for backwards compatibility
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)