"""
Chatbot Router - Phase III
HTTP endpoint for AI-powered chat interface with structured error handling
"""

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
import time
import uuid

from chatbot.gemini.client import GeminiClient, GeminiAuthError, GeminiQuotaError, GeminiNetworkError, GeminiError
from chatbot.gemini.config import get_gemini_config
from chatbot.agent.agent import initialize_agent, run_agent
from chatbot.utils.language import detect_language

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Gemini client once at module level
gemini_client: Optional[GeminiClient] = None


@router.on_event("startup")
async def startup_event():
    """Initialize Gemini client when router starts"""
    global gemini_client
    try:
        logger.info("Initializing Gemini client...")
        config = get_gemini_config()
        gemini_client = GeminiClient(config)
        logger.info(f"✅ Gemini client ready (model: {config.model})")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Gemini client: {e}", exc_info=True)
        # Don't raise - let the application start, errors will be caught per-request


# Pydantic models for request/response
class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat request from frontend"""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    user_id: Optional[int] = Field(None, description="User ID (required for task operations)")
    conversation_history: Optional[List[ChatMessage]] = Field(default=[], description="Previous messages")
    language: Optional[str] = Field(default="en", description="Preferred language")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")


class ChatResponse(BaseModel):
    """Structured chat response"""
    success: bool = Field(..., description="Whether the request succeeded")
    message: str = Field(default="", description="Assistant's response message")
    error: Optional[str] = Field(None, description="Error type code (if failed)")
    error_message: Optional[str] = Field(None, description="User-friendly error message (if failed)")
    tool_used: Optional[str] = Field(None, description="Name of tool/function used")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")
    request_id: str = Field(..., description="Unique request ID for tracking")


@router.post("/", response_model=ChatResponse)
async def chat(chat_request: ChatRequest, request: Request):
    """
    Chat endpoint - processes user message and returns agent response.

    Handles:
    - Language detection
    - Authentication requirements for task operations
    - Gemini API errors with specific error codes
    - Request tracking via request_id

    Error codes:
    - authentication_required (401): User needs to log in for this action
    - authentication_failed (500): Gemini API key is invalid
    - quota_exceeded (500): Gemini API quota/rate limit exceeded
    - network_error (500): Network/timeout issue with Gemini
    - tool_execution_failed (500): MCP tool execution failed
    - internal_error (500): Other unexpected errors

    Example request:
    ```json
    {
        "message": "Assalamualaikum, what can you do?",
        "user_id": null,
        "conversation_history": []
    }
    ```

    Example success response:
    ```json
    {
        "success": true,
        "message": "Wa alaikum assalam! I can help you...",
        "error": null,
        "error_message": null,
        "tool_used": null,
        "data": null,
        "request_id": "abc-123-def"
    }
    ```

    Example error response:
    ```json
    {
        "success": false,
        "message": "",
        "error": "authentication_required",
        "error_message": "Please log in to perform this action...",
        "request_id": "abc-123-def"
    }
    ```
    """
    global gemini_client

    # Get or generate request ID
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))

    start_time = time.time()

    # Detect language
    language = detect_language(chat_request.message)

    # Log request
    logger.info(
        f"Chat request received",
        extra={
            "request_id": request_id,
            "user_id": chat_request.user_id,
            "message_length": len(chat_request.message),
            "has_history": len(chat_request.conversation_history) > 0,
            "language": language,
        }
    )

    try:
        # Ensure Gemini client is initialized
        if gemini_client is None:
            logger.warning(f"Gemini client not initialized, initializing now... (request_id={request_id})")
            config = get_gemini_config()
            gemini_client = GeminiClient(config)

        # Check if message requires authentication
        # Keywords that require user to be logged in
        auth_required_keywords = [
            "create", "add", "bana", "banao",
            "delete", "remove", "hata",
            "update", "edit", "change", "badal",
            "task", "reminder"
        ]

        message_lower = chat_request.message.lower()
        requires_auth = any(keyword in message_lower for keyword in auth_required_keywords)

        if requires_auth and chat_request.user_id is None:
            # Authentication required but no user_id provided
            logger.warning(
                f"Authentication required but no user_id provided",
                extra={"request_id": request_id, "user_message": chat_request.message[:50]}
            )

            error_msg_en = (
                "Please log in to perform this action. "
                "You need to be signed in to create or manage tasks."
            )
            error_msg_ur = (
                "Yeh action karne ke liye login karein. "
                "Tasks banane ya manage karne ke liye sign in hona zaroori hai."
            )

            duration = time.time() - start_time
            logger.info(
                f"Chat request failed: authentication required",
                extra={
                    "request_id": request_id,
                    "duration": f"{duration:.2f}s",
                    "error": "authentication_required"
                }
            )

            return ChatResponse(
                success=False,
                message="",
                error="authentication_required",
                error_message=error_msg_ur if language == "ur" else error_msg_en,
                request_id=request_id
            )

        # Process message with agent (which uses Gemini client)
        # The agent will use our gemini_client for AI responses
        response_text = run_agent(
            agent=None,  # Agent will initialize itself
            user_id=chat_request.user_id or 0,
            user_message=chat_request.message,
            conversation_history=[
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.conversation_history
            ] if chat_request.conversation_history else None,
            gemini_client=gemini_client,
            request_id=request_id
        )

        # Log successful response
        duration = time.time() - start_time
        logger.info(
            f"Chat request completed successfully",
            extra={
                "request_id": request_id,
                "success": True,
                "response_length": len(response_text),
                "duration": f"{duration:.2f}s",
            }
        )

        return ChatResponse(
            success=True,
            message=response_text,
            error=None,
            error_message=None,
            request_id=request_id
        )

    except GeminiAuthError as e:
        # Authentication error with Gemini API
        duration = time.time() - start_time
        logger.error(
            f"Gemini authentication error",
            extra={
                "request_id": request_id,
                "error_type": "authentication_failed",
                "duration": f"{duration:.2f}s",
            },
            exc_info=True
        )

        error_msg_en = (
            "The chatbot service is temporarily unavailable due to a configuration issue. "
            "Please contact support with reference ID: " + request_id
        )
        error_msg_ur = (
            "Chatbot service abhi available nahi hai (configuration issue). "
            "Support se contact karein. Reference ID: " + request_id
        )

        return ChatResponse(
            success=False,
            message="",
            error="authentication_failed",
            error_message=error_msg_ur if language == "ur" else error_msg_en,
            request_id=request_id
        )

    except GeminiQuotaError as e:
        # Quota exceeded
        duration = time.time() - start_time
        logger.error(
            f"Gemini quota exceeded",
            extra={
                "request_id": request_id,
                "error_type": "quota_exceeded",
                "duration": f"{duration:.2f}s",
            },
            exc_info=True
        )

        error_msg_en = (
            "The chatbot is experiencing high demand right now. "
            "Please try again in a few moments."
        )
        error_msg_ur = (
            "Chatbot abhi bohat busy hai. "
            "Kuch der baad dobara try karein."
        )

        return ChatResponse(
            success=False,
            message="",
            error="quota_exceeded",
            error_message=error_msg_ur if language == "ur" else error_msg_en,
            request_id=request_id
        )

    except GeminiNetworkError as e:
        # Network error
        duration = time.time() - start_time
        logger.error(
            f"Gemini network error",
            extra={
                "request_id": request_id,
                "error_type": "network_error",
                "duration": f"{duration:.2f}s",
            },
            exc_info=True
        )

        error_msg_en = (
            "Unable to connect to the chatbot service. "
            "Please check your internet connection and try again."
        )
        error_msg_ur = (
            "Chatbot service se connection nahi ho raha. "
            "Apna internet check karein aur dobara try karein."
        )

        return ChatResponse(
            success=False,
            message="",
            error="network_error",
            error_message=error_msg_ur if language == "ur" else error_msg_en,
            request_id=request_id
        )

    except GeminiError as e:
        # General Gemini error
        duration = time.time() - start_time
        logger.error(
            f"Gemini error",
            extra={
                "request_id": request_id,
                "error_type": "gemini_error",
                "error_message": str(e),
                "duration": f"{duration:.2f}s",
            },
            exc_info=True
        )

        error_msg_en = (
            "The chatbot encountered an issue. "
            "Please try again. If the problem persists, contact support with ID: " + request_id
        )
        error_msg_ur = (
            "Chatbot mein koi issue aaya. "
            "Dobara try karein. Agar problem rahe toh support se contact karein. ID: " + request_id
        )

        return ChatResponse(
            success=False,
            message="",
            error="internal_error",
            error_message=error_msg_ur if language == "ur" else error_msg_en,
            request_id=request_id
        )

    except Exception as e:
        # Unexpected error
        duration = time.time() - start_time
        logger.error(
            f"Unexpected error in chat endpoint",
            extra={
                "request_id": request_id,
                "error_type": "unknown",
                "error_class": type(e).__name__,
                "error_message": str(e),
                "duration": f"{duration:.2f}s",
            },
            exc_info=True
        )

        error_msg_en = (
            "An unexpected error occurred. "
            "Please try again. Reference ID: " + request_id
        )
        error_msg_ur = (
            "Ek unexpected error aaya. "
            "Dobara try karein. Reference ID: " + request_id
        )

        return ChatResponse(
            success=False,
            message="",
            error="internal_error",
            error_message=error_msg_ur if language == "ur" else error_msg_en,
            request_id=request_id
        )


@router.get("/health")
async def health_check():
    """
    Health check for chatbot service.

    Verifies Gemini API connectivity.

    Returns:
        200: Service is healthy
        503: Service is unhealthy
    """
    global gemini_client

    try:
        if gemini_client is None:
            logger.warning("Health check: Gemini client not initialized")
            return {
                "service": "chatbot",
                "status": "unhealthy",
                "error": "not_initialized",
                "message": "Gemini client not initialized",
            }

        # Run health check
        health = gemini_client.health_check()

        if health["status"] == "healthy":
            return health
        else:
            # Return 503 for unhealthy
            from fastapi import Response
            response = Response(
                content=str(health),
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                media_type="application/json"
            )
            return health

    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return {
            "service": "chatbot",
            "status": "unhealthy",
            "error": "health_check_failed",
            "message": str(e),
        }
