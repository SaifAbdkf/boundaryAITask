"""
FastAPI application factory and configuration.
"""

from fastapi import FastAPI

from app.routes import health_router, surveys_router

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Survey Generator API",
        description="AI-powered survey generation API",
        version="1.0.0"
    )
    
    # Include routers
    app.include_router(health_router)
    app.include_router(surveys_router)
    
    return app

# Create the app instance
app = create_app()
