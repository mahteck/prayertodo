"""
Database connection and session management
Uses SQLModel with PostgreSQL (Neon serverless)
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from typing import Generator

from config import settings


# Create engine with NullPool for serverless PostgreSQL (Neon)
engine = create_engine(
    settings.database_url,
    echo=True,  # Log SQL queries in development
    poolclass=NullPool,  # Disable connection pooling for serverless
)


def create_db_and_tables():
    """Create all database tables defined in models"""
    # Import models to register them with SQLModel
    from models import SpiritualTask, Masjid, DailyHadith

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get database session
    Usage: session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session
