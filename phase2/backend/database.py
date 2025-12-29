"""
SalaatFlow Phase II - Database Configuration

Database connection, session management, and dependency injection for FastAPI.
Uses SQLModel with PostgreSQL (Neon).
"""

from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ============================================================================
# Database Configuration
# ============================================================================

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please create a .env file with your Neon PostgreSQL connection string."
    )

# Create engine with connection pooling
# For serverless (Neon), use NullPool to avoid connection pooling issues
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (set to False in production)
    poolclass=NullPool,  # Disable connection pooling for serverless
)


# ============================================================================
# Database Initialization
# ============================================================================

def create_db_and_tables() -> None:
    """
    Create all database tables based on SQLModel models.

    This function should be called once at application startup.
    In production, use Alembic migrations instead.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get database session.

    Yields:
        Session: SQLModel database session

    Usage:
        @app.get("/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            tasks = session.exec(select(SpiritualTask)).all()
            return tasks
    """
    with Session(engine) as session:
        yield session


# ============================================================================
# Session Context Manager (for manual usage)
# ============================================================================

def get_db_session() -> Session:
    """
    Get a database session for manual usage (non-FastAPI contexts).

    Returns:
        Session: SQLModel database session

    Usage:
        with get_db_session() as session:
            task = session.get(SpiritualTask, task_id)
    """
    return Session(engine)
