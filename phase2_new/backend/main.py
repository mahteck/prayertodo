"""
SalaatFlow API - Phase II/III
FastAPI backend for Islamic task management

Author: Claude Code
Date: 2025-12-27
Phase III Added: 2025-12-29
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Configure logging FIRST before any other imports
from chatbot.config.logging_config import setup_logging, get_logger
setup_logging(log_level="INFO")

from config import settings
from database import create_db_and_tables

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - runs on startup and shutdown"""
    logger.info("🚀 Starting SalaatFlow API...")
    logger.info(f"📍 Environment: {settings.environment}")
    logger.info(f"🔌 Database: {settings.database_url[:20]}...")

    # Create database tables on startup
    create_db_and_tables()
    logger.info("✅ Database tables ready")

    # CRITICAL: Validate MCP tools on startup (Phase III)
    logger.info("🔧 Validating MCP tools registry...")
    from chatbot.mcp_tools import validate_all_tools, get_tool_registry

    try:
        validate_all_tools()
        registry = get_tool_registry()
        tool_names = registry.get_all_tool_names()
        logger.info(f"✅ All {len(tool_names)} MCP tools validated and registered")
        logger.debug(f"Registered tools: {', '.join(tool_names)}")
    except RuntimeError as e:
        logger.error(f"❌ MCP Tools validation FAILED: {e}")
        logger.error("Application cannot start without all required tools")
        raise  # Re-raise to prevent application startup

    yield

    logger.info("👋 Shutting down SalaatFlow API...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Islamic Task Management API for tracking spiritual activities",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "As-salamu alaykum! Welcome to SalaatFlow API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SalaatFlow API",
        "version": settings.app_version,
    }


# Include routers
from routers import tasks, masjids, hadith, chatbot

app.include_router(
    tasks.router,
    prefix=f"{settings.api_v1_prefix}/tasks",
    tags=["Tasks"],
)

app.include_router(
    masjids.router,
    prefix=f"{settings.api_v1_prefix}/masjids",
    tags=["Masjids"],
)

app.include_router(
    hadith.router,
    prefix=f"{settings.api_v1_prefix}/hadith",
    tags=["Daily Hadith"],
)

# Phase III: AI Chatbot
app.include_router(
    chatbot.router,
    prefix=f"{settings.api_v1_prefix}/chat",
    tags=["Chatbot"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
