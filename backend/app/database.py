"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from app.models.generated_survey import Base

# Database engine
engine = None
SessionLocal = None

def init_database():
    """Initialize database connection."""
    global engine, SessionLocal
    
    if not settings.DATABASE_URL:
        raise Exception("DATABASE_URL must be configured for PostgreSQL")
    
    # Use PostgreSQL
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
    )
    print("✅ Database: PostgreSQL connected")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Get database session."""
    if not SessionLocal:
        init_database()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_sync() -> Session:
    """Get database session synchronously."""
    if not SessionLocal:
        init_database()
    
    return SessionLocal()
