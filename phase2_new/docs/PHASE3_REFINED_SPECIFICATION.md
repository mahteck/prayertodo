# Phase III Refined Specification: Authenticated AI-Powered Prayer & Masjid Chatbot

**Project**: SalaatFlow
**Version**: 2.0 (Refined)
**Date**: 2025-12-30
**Status**: Active Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Scope & Objectives](#scope--objectives)
3. [Gemini Integration Requirements](#gemini-integration-requirements)
4. [Chat Endpoint Specification](#chat-endpoint-specification)
5. [Frontend Chat UI Specification](#frontend-chat-ui-specification)
6. [Error Handling & Logging](#error-handling--logging)
7. [Build & Test Requirements](#build--test-requirements)
8. [Health Check & Diagnostics](#health-check--diagnostics)
9. [Acceptance Criteria](#acceptance-criteria)
10. [Documentation Requirements](#documentation-requirements)
11. [Implementation Checklist](#implementation-checklist)

---

## 1. Executive Summary

### Current Issues
- ❌ Chatbot returns generic "I encountered an unexpected error. Please try again."
- ❌ No clear logging or diagnostics for Gemini API failures
- ❌ No health check mechanism
- ❌ Inadequate error differentiation (API key invalid vs. network error vs. tool failure)
- ❌ No documented build/test procedures

### Refinement Goals
- ✅ Make Gemini chatbot ACTUALLY functional with proper error handling
- ✅ Add comprehensive logging and diagnostics
- ✅ Implement health checks
- ✅ Ensure full project builds and runs without errors
- ✅ Create clear test/validation procedures
- ✅ Maintain all Phase III functional goals (auth, tasks, masjids, hadith)

---

## 2. Scope & Objectives

### In Scope
- ✅ Gemini API integration with robust error handling
- ✅ Authenticated chatbot operations
- ✅ Task management via natural language
- ✅ Masjid search capabilities
- ✅ Hadith retrieval
- ✅ Comprehensive logging
- ✅ Health check endpoints
- ✅ Build/test automation

### Out of Scope
- ❌ Changing core Phase III functionality
- ❌ Adding new major features beyond chatbot reliability
- ❌ Manual code writing (all AI-generated)

---

## 3. Gemini Integration Requirements

### 3.1 Configuration

#### Environment Variables (Required)

**File**: `backend/.env`

```env
# Gemini API Configuration
GEMINI_API_KEY=<your-api-key-here>
GEMINI_MODEL=gemini-pro
GEMINI_BASE_URL=https://generativelanguage.googleapis.com
GEMINI_TIMEOUT=30
GEMINI_MAX_RETRIES=2
GEMINI_RETRY_DELAY=1.0
```

#### Configuration Validation

**File**: `backend/chatbot/config/settings.py`

```python
import os
from typing import Optional
from pydantic import BaseModel, validator

class GeminiConfig(BaseModel):
    """Gemini API Configuration with validation"""

    api_key: str
    model: str = "gemini-pro"
    base_url: str = "https://generativelanguage.googleapis.com"
    timeout: int = 30
    max_retries: int = 2
    retry_delay: float = 1.0

    @validator('api_key')
    def validate_api_key(cls, v):
        if not v or v == "your-api-key-here":
            raise ValueError(
                "GEMINI_API_KEY must be set. Get one from: "
                "https://aistudio.google.com/app/apikey"
            )
        if not v.startswith('AIza'):
            raise ValueError("Invalid Gemini API key format")
        return v

    @validator('timeout')
    def validate_timeout(cls, v):
        if v < 5 or v > 300:
            raise ValueError("Timeout must be between 5-300 seconds")
        return v

    class Config:
        env_prefix = 'GEMINI_'
```

### 3.2 Gemini Client Implementation

**File**: `backend/chatbot/agent/gemini_client.py`

```python
"""
Robust Gemini API Client with comprehensive error handling
"""

import logging
import time
from typing import Optional, Dict, Any
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from chatbot.config.settings import GeminiConfig

logger = logging.getLogger(__name__)


class GeminiError(Exception):
    """Base exception for Gemini-related errors"""
    pass


class GeminiAuthError(GeminiError):
    """Authentication/API key error"""
    pass


class GeminiQuotaError(GeminiError):
    """Quota exceeded error"""
    pass


class GeminiNetworkError(GeminiError):
    """Network/connectivity error"""
    pass


class GeminiClient:
    """
    Production-ready Gemini API client with:
    - Proper error handling
    - Retry logic
    - Detailed logging
    - Health checks
    """

    def __init__(self, config: GeminiConfig):
        self.config = config
        self._model = None

        try:
            genai.configure(api_key=config.api_key)
            logger.info(
                f"Gemini client initialized with model: {config.model}"
            )
        except Exception as e:
            logger.error(f"Failed to configure Gemini: {e}", exc_info=True)
            raise GeminiAuthError(
                f"Failed to initialize Gemini client: {str(e)}"
            )

    def _get_model(self):
        """Lazy load model"""
        if self._model is None:
            try:
                self._model = genai.GenerativeModel(
                    model_name=self.config.model
                )
                logger.debug(f"Gemini model {self.config.model} loaded")
            except Exception as e:
                logger.error(
                    f"Failed to load model {self.config.model}: {e}",
                    exc_info=True
                )
                raise GeminiError(f"Model loading failed: {str(e)}")
        return self._model

    def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate response from Gemini with comprehensive error handling

        Args:
            prompt: User message
            system_instruction: Optional system prompt
            context: Optional context dict for logging

        Returns:
            Generated response text

        Raises:
            GeminiAuthError: Invalid API key
            GeminiQuotaError: Quota exceeded
            GeminiNetworkError: Network issues
            GeminiError: Other errors
        """

        # Log request (without sensitive data)
        log_context = {
            "prompt_length": len(prompt),
            "has_system_instruction": system_instruction is not None,
            **(context or {})
        }
        logger.info(f"Gemini request started: {log_context}")

        attempt = 0
        last_error = None

        while attempt < self.config.max_retries:
            try:
                model = self._get_model()

                # Generate content
                start_time = time.time()
                response = model.generate_content(prompt)
                duration = time.time() - start_time

                # Validate response
                if not response or not response.text:
                    raise GeminiError("Empty response from Gemini")

                # Log success
                logger.info(
                    f"Gemini response received: "
                    f"duration={duration:.2f}s, "
                    f"length={len(response.text)}"
                )

                return response.text

            except google_exceptions.Unauthenticated as e:
                logger.error(
                    f"Gemini authentication error: {e}",
                    exc_info=True,
                    extra=log_context
                )
                raise GeminiAuthError(
                    "Invalid Gemini API key. Please check your configuration."
                ) from e

            except google_exceptions.ResourceExhausted as e:
                logger.error(
                    f"Gemini quota exceeded: {e}",
                    exc_info=True,
                    extra=log_context
                )
                raise GeminiQuotaError(
                    "Gemini API quota exceeded. Please try again later."
                ) from e

            except (
                google_exceptions.DeadlineExceeded,
                google_exceptions.ServiceUnavailable,
                google_exceptions.InternalServerError
            ) as e:
                attempt += 1
                last_error = e

                if attempt < self.config.max_retries:
                    wait_time = self.config.retry_delay * attempt
                    logger.warning(
                        f"Gemini request failed (attempt {attempt}), "
                        f"retrying in {wait_time}s: {e}",
                        extra=log_context
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"Gemini request failed after {attempt} attempts: {e}",
                        exc_info=True,
                        extra=log_context
                    )
                    raise GeminiNetworkError(
                        "The assistant is having trouble connecting. "
                        "Please try again in a moment."
                    ) from e

            except google_exceptions.NotFound as e:
                logger.error(
                    f"Gemini model not found: {e}",
                    exc_info=True,
                    extra=log_context
                )
                raise GeminiError(
                    f"Model '{self.config.model}' not found. "
                    "Please check configuration."
                ) from e

            except Exception as e:
                logger.error(
                    f"Unexpected Gemini error: {type(e).__name__}: {e}",
                    exc_info=True,
                    extra=log_context
                )
                raise GeminiError(
                    "The assistant encountered an unexpected issue. "
                    "Our team has been notified."
                ) from e

        # Should not reach here, but just in case
        raise GeminiNetworkError(
            f"Failed after {self.config.max_retries} retries"
        ) from last_error

    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on Gemini API

        Returns:
            Dict with health status
        """
        health = {
            "service": "gemini",
            "status": "unknown",
            "model": self.config.model,
            "timestamp": time.time()
        }

        try:
            # Simple health check prompt
            response = self.generate_response(
                "Hello from SalaatFlow health check. Respond with 'OK'.",
                context={"health_check": True}
            )

            if response and len(response) > 0:
                health["status"] = "healthy"
                health["response_length"] = len(response)
                logger.info("Gemini health check: PASSED")
            else:
                health["status"] = "unhealthy"
                health["error"] = "Empty response"
                logger.warning("Gemini health check: FAILED (empty response)")

        except GeminiAuthError as e:
            health["status"] = "unhealthy"
            health["error"] = "authentication_failed"
            health["message"] = str(e)
            logger.error(f"Gemini health check: FAILED (auth error)")

        except GeminiQuotaError as e:
            health["status"] = "unhealthy"
            health["error"] = "quota_exceeded"
            health["message"] = str(e)
            logger.error(f"Gemini health check: FAILED (quota)")

        except Exception as e:
            health["status"] = "unhealthy"
            health["error"] = type(e).__name__
            health["message"] = str(e)
            logger.error(
                f"Gemini health check: FAILED ({type(e).__name__})",
                exc_info=True
            )

        return health
```

### 3.3 Agent Orchestrator

**File**: `backend/chatbot/agent/orchestrator.py`

```python
"""
Chatbot orchestrator that coordinates Gemini and tools
"""

import logging
from typing import Dict, Any, Optional

from chatbot.agent.gemini_client import (
    GeminiClient,
    GeminiError,
    GeminiAuthError,
    GeminiQuotaError,
    GeminiNetworkError
)
from chatbot.agent.intent_detector import IntentDetector
from chatbot.mcp_tools import execute_tool

logger = logging.getLogger(__name__)


class ChatbotOrchestrator:
    """
    Coordinates:
    - Intent detection
    - Tool execution
    - Gemini interaction
    - Error handling
    """

    def __init__(self, gemini_client: GeminiClient):
        self.gemini = gemini_client
        self.intent_detector = IntentDetector()

    def process_message(
        self,
        user_id: int,
        message: str,
        conversation_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Process user message and return structured response

        Returns:
            {
                "success": bool,
                "message": str,  # Assistant's response
                "error": Optional[str],  # Error type if failed
                "error_message": Optional[str],  # User-friendly error
                "tool_used": Optional[str],  # Tool name if used
                "data": Optional[dict]  # Structured data (e.g., created task)
            }
        """

        context = {
            "user_id": user_id,
            "message_length": len(message),
            "has_history": bool(conversation_history)
        }

        logger.info(f"Processing message for user {user_id}", extra=context)

        try:
            # Detect intent
            intent_result = self.intent_detector.detect(message)
            intent = intent_result["intent"]

            logger.debug(f"Detected intent: {intent}", extra=context)

            # Handle different intents
            if intent in ["create_task", "list_tasks", "update_task",
                          "delete_task", "search_masjids"]:
                return self._handle_tool_intent(
                    user_id, message, intent, context
                )
            else:
                # General conversation via Gemini
                return self._handle_conversation(
                    user_id, message, conversation_history, context
                )

        except GeminiAuthError as e:
            logger.error(
                "Authentication error",
                exc_info=True,
                extra=context
            )
            return {
                "success": False,
                "message": "",
                "error": "authentication_failed",
                "error_message": (
                    "The chatbot service is not properly configured. "
                    "Please contact support."
                )
            }

        except GeminiQuotaError as e:
            logger.error(
                "Quota exceeded",
                exc_info=True,
                extra=context
            )
            return {
                "success": False,
                "message": "",
                "error": "quota_exceeded",
                "error_message": (
                    "The assistant is currently at capacity. "
                    "Please try again in a few moments."
                )
            }

        except GeminiNetworkError as e:
            logger.error(
                "Network error",
                exc_info=True,
                extra=context
            )
            return {
                "success": False,
                "message": "",
                "error": "network_error",
                "error_message": (
                    "Unable to reach the assistant right now. "
                    "Please check your connection or try again later."
                )
            }

        except Exception as e:
            logger.error(
                f"Unexpected error: {type(e).__name__}: {e}",
                exc_info=True,
                extra=context
            )
            return {
                "success": False,
                "message": "",
                "error": "internal_error",
                "error_message": (
                    "Something went wrong. Our team has been notified and "
                    "will fix this shortly."
                )
            }

    def _handle_tool_intent(
        self,
        user_id: int,
        message: str,
        intent: str,
        context: dict
    ) -> Dict[str, Any]:
        """Handle tool-based intents"""

        try:
            # Extract parameters
            params = self.intent_detector.extract_parameters(message, intent)

            # Execute tool
            logger.info(
                f"Executing tool: {intent}",
                extra={**context, "params": params}
            )

            result = execute_tool(intent, user_id, **params)

            if result.get("success"):
                return {
                    "success": True,
                    "message": self._format_tool_response(intent, result),
                    "tool_used": intent,
                    "data": result
                }
            else:
                logger.warning(
                    f"Tool execution failed: {result.get('error')}",
                    extra=context
                )
                return {
                    "success": False,
                    "message": "",
                    "error": "tool_execution_failed",
                    "error_message": (
                        f"Unable to complete that action: "
                        f"{result.get('error', 'Unknown error')}"
                    )
                }

        except Exception as e:
            logger.error(
                f"Tool execution error: {e}",
                exc_info=True,
                extra=context
            )
            return {
                "success": False,
                "message": "",
                "error": "tool_error",
                "error_message": "Failed to perform that action. Please try again."
            }

    def _handle_conversation(
        self,
        user_id: int,
        message: str,
        history: Optional[list],
        context: dict
    ) -> Dict[str, Any]:
        """Handle general conversation via Gemini"""

        try:
            # Build prompt with history
            prompt = self._build_prompt(message, history)

            # Call Gemini
            response = self.gemini.generate_response(
                prompt,
                context={**context, "conversation": True}
            )

            return {
                "success": True,
                "message": response,
                "tool_used": None,
                "data": None
            }

        except (GeminiError, Exception) as e:
            # Re-raise to be caught by process_message
            raise

    def _build_prompt(
        self,
        message: str,
        history: Optional[list]
    ) -> str:
        """Build prompt with context"""

        system = (
            "You are SalaatFlow Assistant, helping Muslims with "
            "prayer times, tasks, and Islamic guidance."
        )

        if history:
            # Include recent history
            history_text = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in history[-5:]  # Last 5 messages
            ])
            return f"{system}\n\n{history_text}\nuser: {message}\nassistant:"
        else:
            return f"{system}\n\nuser: {message}\nassistant:"

    def _format_tool_response(self, intent: str, result: dict) -> str:
        """Format tool result into user-friendly message"""

        if intent == "create_task":
            task = result.get("task", {})
            return (
                f"✅ Task created successfully!\n\n"
                f"Title: {task.get('title')}\n"
                f"Priority: {task.get('priority')}\n"
                f"Linked Prayer: {task.get('linked_prayer', 'None')}"
            )

        elif intent == "list_tasks":
            tasks = result.get("tasks", [])
            if not tasks:
                return "You don't have any tasks yet. Would you like to create one?"

            response = f"📋 Your Tasks ({len(tasks)} total):\n\n"
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get("completed") else "⏳"
                prayer = f" ({task.get('linked_prayer')})" if task.get('linked_prayer') else ""
                response += (
                    f"{i}. {status} {task.get('title')}{prayer}\n"
                    f"   Priority: {task.get('priority')}\n\n"
                )
            return response

        # ... other intents

        return str(result)
```

---

## 4. Chat Endpoint Specification

### 4.1 HTTP Endpoint Definition

**Endpoint**: `POST /api/v1/chat`

**File**: `backend/routers/chatbot.py`

#### Request Schema

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User message"
    )
    user_id: Optional[int] = Field(
        None,
        description="User ID (required for authenticated operations)"
    )
    conversation_history: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        max_items=20,
        description="Recent conversation history"
    )
    language: Optional[str] = Field(
        "en",
        description="Preferred language: 'en' or 'ur'"
    )
    metadata: Optional[dict] = Field(
        default_factory=dict,
        description="Additional client metadata"
    )

class ChatResponse(BaseModel):
    success: bool = Field(..., description="Operation success flag")
    message: str = Field("", description="Assistant's response message")
    error: Optional[str] = Field(None, description="Error type if failed")
    error_message: Optional[str] = Field(
        None,
        description="User-friendly error message"
    )
    tool_used: Optional[str] = Field(None, description="Tool that was used")
    data: Optional[dict] = Field(None, description="Structured response data")
    request_id: str = Field(..., description="Unique request ID for tracking")
```

#### Endpoint Implementation

```python
import logging
import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from chatbot.agent.orchestrator import ChatbotOrchestrator
from chatbot.agent.gemini_client import GeminiClient
from chatbot.config.settings import GeminiConfig

router = APIRouter(prefix="/api/v1", tags=["chat"])
logger = logging.getLogger(__name__)

# Initialize orchestrator
config = GeminiConfig()
gemini_client = GeminiClient(config)
orchestrator = ChatbotOrchestrator(gemini_client)


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process chat message with comprehensive error handling

    Behavior:
    - Returns 200 with success=true for valid responses
    - Returns 401 if auth required but not provided
    - Returns 500 for server errors with detailed logging
    - NEVER returns generic errors without context
    """

    request_id = str(uuid.uuid4())

    # Log incoming request
    logger.info(
        f"Chat request received: request_id={request_id}",
        extra={
            "request_id": request_id,
            "user_id": request.user_id,
            "message_length": len(request.message),
            "has_history": bool(request.conversation_history),
            "language": request.language
        }
    )

    try:
        # Validate user_id for authenticated operations
        if not request.user_id:
            # Check if message requires auth
            if _requires_authentication(request.message):
                logger.warning(
                    f"Unauthenticated request for protected operation: "
                    f"request_id={request_id}"
                )
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "success": False,
                        "message": "",
                        "error": "authentication_required",
                        "error_message": (
                            "Please log in to perform this action. "
                            "You need to be signed in to create or manage tasks."
                        ),
                        "request_id": request_id
                    }
                )

        # Process message
        result = orchestrator.process_message(
            user_id=request.user_id or 0,  # 0 for anonymous
            message=request.message,
            conversation_history=[
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ] if request.conversation_history else None
        )

        # Add request_id to result
        result["request_id"] = request_id

        # Log result
        if result["success"]:
            logger.info(
                f"Chat request successful: request_id={request_id}",
                extra={
                    "request_id": request_id,
                    "tool_used": result.get("tool_used"),
                    "response_length": len(result.get("message", ""))
                }
            )
        else:
            logger.warning(
                f"Chat request failed: request_id={request_id}",
                extra={
                    "request_id": request_id,
                    "error": result.get("error"),
                    "error_message": result.get("error_message")
                }
            )

        # Return response
        status_code = status.HTTP_200_OK if result["success"] else status.HTTP_500_INTERNAL_SERVER_ERROR

        return JSONResponse(
            status_code=status_code,
            content=result
        )

    except Exception as e:
        # Log unexpected errors with full context
        logger.error(
            f"Unexpected error in chat endpoint: request_id={request_id}",
            exc_info=True,
            extra={
                "request_id": request_id,
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "",
                "error": "internal_server_error",
                "error_message": (
                    "An unexpected error occurred. "
                    "Our team has been notified. "
                    f"Reference ID: {request_id}"
                ),
                "request_id": request_id
            }
        )


def _requires_authentication(message: str) -> bool:
    """Check if message requires authentication"""
    auth_keywords = [
        "create", "bana", "add", "delete", "remove",
        "update", "change", "complete", "task"
    ]
    return any(kw in message.lower() for kw in auth_keywords)


@router.get("/chat/health")
async def chat_health_check():
    """
    Health check endpoint for chat service
    """
    try:
        health = orchestrator.gemini.health_check()

        status_code = (
            status.HTTP_200_OK if health["status"] == "healthy"
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )

        return JSONResponse(
            status_code=status_code,
            content=health
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "service": "gemini",
                "status": "unhealthy",
                "error": str(e)
            }
        )
```

### 4.2 Error Response Standards

All error responses MUST follow this standard:

```json
{
  "success": false,
  "message": "",
  "error": "error_type_code",
  "error_message": "User-friendly explanation of what went wrong and what to do",
  "request_id": "uuid-for-tracking"
}
```

#### Error Types

| Error Code | HTTP Status | User Message | When to Use |
|------------|-------------|--------------|-------------|
| `authentication_required` | 401 | "Please log in to perform this action..." | User not authenticated for mutating operation |
| `authentication_failed` | 500 | "The chatbot service is not properly configured..." | Invalid Gemini API key |
| `quota_exceeded` | 500 | "The assistant is currently at capacity..." | Gemini quota exceeded |
| `network_error` | 500 | "Unable to reach the assistant right now..." | Network/connectivity issues |
| `tool_execution_failed` | 500 | "Unable to complete that action: [specific reason]" | Tool execution failed |
| `internal_error` | 500 | "Something went wrong. Our team has been notified..." | Unexpected errors |

**CRITICAL**: The endpoint MUST NEVER return:
- ❌ "I encountered an unexpected error. Please try again."
- ❌ Generic messages without differentiation
- ❌ Errors without logging the full stack trace server-side

---

## 5. Frontend Chat UI Specification

### 5.1 Chat Page Component

**File**: `frontend/app/chat/page.tsx`

#### State Management

```typescript
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isError?: boolean;
}

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: {
    type: string;
    message: string;
  } | null;
  connected: boolean;
}
```

#### Error Display Requirements

The chat UI MUST implement distinct error displays:

1. **Loading State**
   ```tsx
   {isLoading && (
     <div className="flex items-center gap-2 text-gray-600">
       <Loader2 className="h-4 w-4 animate-spin" />
       <span>Assistant is thinking...</span>
     </div>
   )}
   ```

2. **Network Error State**
   ```tsx
   {error?.type === 'network_error' && (
     <Alert variant="destructive">
       <AlertCircle className="h-4 w-4" />
       <AlertTitle>Connection Issue</AlertTitle>
       <AlertDescription>
         Unable to reach the assistant. Please check your internet
         connection and try again.
       </AlertDescription>
     </Alert>
   )}
   ```

3. **Authentication Error State**
   ```tsx
   {error?.type === 'authentication_required' && (
     <Alert variant="warning">
       <Lock className="h-4 w-4" />
       <AlertTitle>Sign In Required</AlertTitle>
       <AlertDescription>
         Please <Link href="/signin">sign in</Link> to create or
         manage tasks.
       </AlertDescription>
     </Alert>
   )}
   ```

4. **Service Error State**
   ```tsx
   {error?.type === 'authentication_failed' && (
     <Alert variant="destructive">
       <AlertCircle className="h-4 w-4" />
       <AlertTitle>Service Configuration Issue</AlertTitle>
       <AlertDescription>
         The chatbot service is not available right now. Our team
         has been notified and is working to fix this.
       </AlertDescription>
     </Alert>
   )}
   ```

5. **Generic Error State** (last resort only)
   ```tsx
   {error && !['network_error', 'authentication_required',
               'authentication_failed'].includes(error.type) && (
     <Alert variant="destructive">
       <AlertCircle className="h-4 w-4" />
       <AlertTitle>Something Went Wrong</AlertTitle>
       <AlertDescription>
         {error.message || 'Please try your request again.'}
       </AlertDescription>
     </Alert>
   )}
   ```

#### API Call Implementation

```typescript
async function sendMessage(message: string): Promise<void> {
  setIsLoading(true);
  setError(null);

  // Add user message immediately
  const userMessage: ChatMessage = {
    role: 'user',
    content: message,
    timestamp: new Date()
  };
  setMessages(prev => [...prev, userMessage]);

  try {
    const response = await fetch('/api/v1/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(session?.accessToken && {
          'Authorization': `Bearer ${session.accessToken}`
        })
      },
      body: JSON.stringify({
        message,
        user_id: session?.user?.id,
        conversation_history: messages.slice(-10).map(m => ({
          role: m.role,
          content: m.content
        })),
        language: 'en'
      })
    });

    const data = await response.json();

    if (data.success) {
      // Add assistant message
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.message,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } else {
      // Handle error response
      setError({
        type: data.error || 'unknown_error',
        message: data.error_message || 'Failed to get response'
      });

      // Optionally add error as a message
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: data.error_message || 'Sorry, I encountered an error.',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    }

  } catch (err) {
    console.error('Chat request failed:', err);

    setError({
      type: 'network_error',
      message: 'Unable to reach the server. Please check your connection.'
    });

    const errorMessage: ChatMessage = {
      role: 'assistant',
      content: 'Unable to connect to the assistant. Please try again.',
      timestamp: new Date(),
      isError: true
    };
    setMessages(prev => [...prev, errorMessage]);

  } finally {
    setIsLoading(false);
  }
}
```

### 5.2 Error Styling Requirements

Error messages in chat MUST be visually distinct:

```typescript
<div className={cn(
  "flex gap-3 p-4 rounded-lg",
  message.role === 'user'
    ? "bg-blue-50 ml-auto max-w-[80%]"
    : message.isError
      ? "bg-red-50 border border-red-200 mr-auto max-w-[80%]"
      : "bg-gray-50 mr-auto max-w-[80%]"
)}>
  {message.isError && (
    <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0" />
  )}
  <div className="flex-1">
    <p className={message.isError ? "text-red-700" : ""}>
      {message.content}
    </p>
  </div>
</div>
```

---

## 6. Error Handling & Logging

### 6.1 Logging Policy

#### Log Levels

| Level | When to Use | Examples |
|-------|-------------|----------|
| `DEBUG` | Development diagnostics | Model loading, parameter extraction |
| `INFO` | Normal operations | Request received, response sent, tool executed |
| `WARNING` | Recoverable issues | Retry attempt, quota near limit, invalid input |
| `ERROR` | Failures requiring attention | API errors, tool failures, exceptions |

#### Required Log Fields

Every log entry MUST include:
```python
logger.info(
    "Human-readable message",
    extra={
        "request_id": "uuid",
        "user_id": 123,
        "operation": "chat_request",
        "duration": 1.23,  # seconds
        # ... operation-specific fields
    }
)
```

#### Logging Configuration

**File**: `backend/logging_config.py`

```python
import logging
import logging.config
from pathlib import Path

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(message)s [%(filename)s:%(lineno)d]"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": (
                "%(asctime)s %(name)s %(levelname)s %(message)s "
                "%(filename)s %(lineno)d"
            )
        }
    },
    "filters": {
        "remove_secrets": {
            "()": "logging_config.RemoveSecretsFilter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "filters": ["remove_secrets"],
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filters": ["remove_secrets"],
            "filename": "logs/salaatflow.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "json",
            "filters": ["remove_secrets"],
            "filename": "logs/salaatflow_errors.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file", "error_file"]
    },
    "loggers": {
        "chatbot": {
            "level": "DEBUG",
            "propagate": True
        },
        "uvicorn": {
            "level": "INFO",
            "propagate": True
        }
    }
}


class RemoveSecretsFilter(logging.Filter):
    """Remove sensitive data from logs"""

    REDACT_PATTERNS = [
        "api_key", "password", "token", "secret",
        "authorization", "bearer"
    ]

    def filter(self, record):
        # Redact sensitive fields
        if hasattr(record, 'extra'):
            for key in list(record.extra.keys()):
                if any(pattern in key.lower()
                       for pattern in self.REDACT_PATTERNS):
                    record.extra[key] = "[REDACTED]"

        # Redact in message
        message = str(record.getMessage())
        for pattern in self.REDACT_PATTERNS:
            if pattern in message.lower():
                # Simple redaction - could be more sophisticated
                parts = message.split('=')
                if len(parts) > 1:
                    record.msg = parts[0] + "=[REDACTED]"

        return True


def setup_logging():
    """Setup logging configuration"""
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # Apply config
    logging.config.dictConfig(LOGGING_CONFIG)

    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")
```

### 6.2 Required Logging Points

#### 1. Request/Response Logging

```python
# At start of request
logger.info(
    f"Chat request received: request_id={request_id}",
    extra={
        "request_id": request_id,
        "user_id": user_id,
        "message_length": len(message),
        "endpoint": "/api/v1/chat"
    }
)

# At end of request
logger.info(
    f"Chat request completed: request_id={request_id}",
    extra={
        "request_id": request_id,
        "success": True,
        "duration": duration,
        "response_length": len(response)
    }
)
```

#### 2. Tool Execution Logging

```python
logger.info(
    f"Executing tool: {tool_name}",
    extra={
        "request_id": request_id,
        "tool_name": tool_name,
        "user_id": user_id,
        "parameters": sanitized_params  # Remove sensitive data
    }
)
```

#### 3. Error Logging

```python
logger.error(
    f"Gemini API error: {error_type}",
    exc_info=True,  # Include stack trace
    extra={
        "request_id": request_id,
        "error_type": error_type,
        "user_id": user_id,
        "retry_attempt": attempt,
        "will_retry": attempt < max_retries
    }
)
```

### 6.3 Log Viewing

Create a simple log viewer script:

**File**: `backend/scripts/view_logs.py`

```python
#!/usr/bin/env python3
"""
Simple log viewer for SalaatFlow
Usage: python scripts/view_logs.py [--tail] [--errors-only] [--request-id=xxx]
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

def view_logs(
    log_file: str = "logs/salaatflow.log",
    tail: int = None,
    errors_only: bool = False,
    request_id: str = None
):
    """View logs with filtering"""

    log_path = Path(log_file)
    if not log_path.exists():
        print(f"Log file not found: {log_file}")
        return

    with open(log_path) as f:
        lines = f.readlines()

    # Apply tail
    if tail:
        lines = lines[-tail:]

    # Filter and display
    for line in lines:
        try:
            log = json.loads(line)

            # Filter by error level
            if errors_only and log.get("levelname") != "ERROR":
                continue

            # Filter by request_id
            if request_id and log.get("request_id") != request_id:
                continue

            # Format output
            timestamp = log.get("asctime", "")
            level = log.get("levelname", "INFO")
            message = log.get("message", "")

            print(f"[{timestamp}] {level:8s} {message}")

            # Show extra context for errors
            if level == "ERROR" and "exc_info" in log:
                print(f"  Error: {log.get('exc_info')}")

        except json.JSONDecodeError:
            # Plain text log line
            print(line.strip())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View SalaatFlow logs")
    parser.add_argument("--tail", type=int, help="Show last N lines")
    parser.add_argument("--errors-only", action="store_true")
    parser.add_argument("--request-id", help="Filter by request ID")

    args = parser.parse_args()
    view_logs(
        tail=args.tail,
        errors_only=args.errors_only,
        request_id=args.request_id
    )
```

---

## 7. Build & Test Requirements

### 7.1 Frontend Build Requirements

#### Prerequisites
- Node.js 18+
- npm 9+

#### Build Commands

**File**: `frontend/package.json` scripts section:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint --fix",
    "lint:check": "next lint",
    "type-check": "tsc --noEmit",
    "test": "npm run lint:check && npm run type-check && npm run build"
  }
}
```

#### Build Success Criteria

All of these MUST pass without errors:

```bash
cd frontend

# 1. Lint check
npm run lint:check
# Expected: ✓ No ESLint warnings or errors

# 2. Type check
npm run type-check
# Expected: ✓ No TypeScript errors

# 3. Production build
npm run build
# Expected:
# ✓ Compiled successfully
# ✓ Route (pages/chat): Finished
# ✓ No build errors
```

#### Common Build Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `Module not found` | Missing dependency | `npm install` |
| `Type error: ...` | TypeScript mismatch | Check types, update interfaces |
| `ESLint: ... is not defined` | Missing import | Add import statement |
| `Build failed` | Syntax error | Check logs, fix syntax |

### 7.2 Backend Build Requirements

#### Prerequisites
- Python 3.12+
- pip
- Virtual environment

#### Build Commands

```bash
cd backend

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run type checking (if using mypy)
mypy chatbot/ routers/ --ignore-missing-imports

# 3. Start server
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Server Startup Success Criteria

```bash
uvicorn main:app --host 0.0.0.0 --port 8000

# Expected output:
# ✅ Chatbot settings loaded (Google Gemini):
#    Model: gemini-pro
#    Backend: http://localhost:8000
#    API Key: Set ✅
# 🚀 Starting SalaatFlow API...
# 📍 Environment: development
# 🔌 Database: postgresql://...
# ✅ Database tables ready
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [xxxxx] using WatchFiles
# INFO:     Started server process [xxxxx]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

### 7.3 Integration Testing

#### Minimal Chat Test Script

**File**: `backend/tests/test_chat_integration.py`

```python
#!/usr/bin/env python3
"""
Minimal integration test for chat endpoint
"""

import requests
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def test_health_check() -> bool:
    """Test health check endpoint"""
    print("Testing health check...")

    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/chat/health",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Health check passed")
                return True
            else:
                print(f"❌ Health check failed: {data}")
                return False
        else:
            print(f"❌ Health check returned {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_simple_chat() -> bool:
    """Test simple chat message"""
    print("\nTesting simple chat...")

    payload = {
        "message": "Assalamualaikum",
        "user_id": None,  # Anonymous
        "conversation_history": [],
        "language": "en"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json=payload,
            timeout=30
        )

        data = response.json()

        # Check response structure
        if not isinstance(data, dict):
            print(f"❌ Invalid response type: {type(data)}")
            return False

        if "success" not in data:
            print("❌ Missing 'success' field in response")
            return False

        if data["success"]:
            if data.get("message"):
                print(f"✅ Chat response received: {data['message'][:50]}...")
                return True
            else:
                print("❌ Success but empty message")
                return False
        else:
            error_type = data.get("error", "unknown")
            error_msg = data.get("error_message", "No error message")
            print(f"❌ Chat failed: {error_type} - {error_msg}")
            return False

    except requests.Timeout:
        print("❌ Chat request timed out")
        return False
    except Exception as e:
        print(f"❌ Chat request error: {e}")
        return False


def test_authenticated_operation() -> bool:
    """Test operation requiring authentication"""
    print("\nTesting authenticated operation (should fail gracefully)...")

    payload = {
        "message": "Create a task for Fajr prayer",
        "user_id": None,  # No auth
        "conversation_history": [],
        "language": "en"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json=payload,
            timeout=30
        )

        data = response.json()

        # Should get auth error
        if response.status_code == 401:
            if data.get("error") == "authentication_required":
                print("✅ Auth error handled correctly")
                return True
            else:
                print(f"❌ Wrong error type: {data.get('error')}")
                return False
        else:
            print(f"❌ Expected 401, got {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("SalaatFlow Chat Integration Tests")
    print("=" * 60)

    results = {
        "Health Check": test_health_check(),
        "Simple Chat": test_simple_chat(),
        "Auth Handling": test_authenticated_operation()
    }

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())

    print("=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

#### Running Integration Tests

```bash
cd backend

# 1. Ensure server is running
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 2. Wait for startup
sleep 5

# 3. Run tests
python tests/test_chat_integration.py

# Expected output:
# ============================================================
# SalaatFlow Chat Integration Tests
# ============================================================
# Testing health check...
# ✅ Health check passed
#
# Testing simple chat...
# ✅ Chat response received: Wa alaikum assalam! How can I help you...
#
# Testing authenticated operation (should fail gracefully)...
# ✅ Auth error handled correctly
#
# ============================================================
# Test Results:
# ============================================================
# ✅ PASS - Health Check
# ✅ PASS - Simple Chat
# ✅ PASS - Auth Handling
# ============================================================
# ✅ All tests passed!
```

---

## 8. Health Check & Diagnostics

### 8.1 Health Check Endpoint

Already defined in section 4.1: `GET /api/v1/chat/health`

### 8.2 Diagnostic Script

**File**: `backend/scripts/diagnose.py`

```python
#!/usr/bin/env python3
"""
SalaatFlow Diagnostic Script
Checks system health and configuration
"""

import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_check(name: str, passed: bool, message: str = ""):
    """Print check result"""
    status = f"{GREEN}✅{RESET}" if passed else f"{RED}❌{RESET}"
    print(f"{status} {name}")
    if message:
        print(f"   {message}")


def check_environment():
    """Check environment configuration"""
    print("\n📋 Environment Configuration")
    print("=" * 60)

    # Load .env
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)

    # Check GEMINI_API_KEY
    api_key = os.getenv("GEMINI_API_KEY")
    print_check(
        "GEMINI_API_KEY set",
        bool(api_key and api_key != "your-api-key-here"),
        f"Value: {api_key[:20]}..." if api_key else "Not set"
    )

    # Check DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    print_check(
        "DATABASE_URL set",
        bool(db_url),
        "Connected to Neon PostgreSQL" if db_url else "Not set"
    )

    # Check other vars
    for var in ["GEMINI_MODEL", "BACKEND_BASE_URL"]:
        value = os.getenv(var)
        print_check(
            f"{var} set",
            bool(value),
            f"Value: {value}" if value else "Using default"
        )


def check_dependencies():
    """Check Python dependencies"""
    print("\n📦 Dependencies")
    print("=" * 60)

    required_packages = [
        "fastapi",
        "google-generativeai",
        "sqlmodel",
        "pydantic",
        "uvicorn"
    ]

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_check(f"{package} installed", True)
        except ImportError:
            print_check(f"{package} installed", False, "Run: pip install -r requirements.txt")


def check_server():
    """Check if server is running"""
    print("\n🌐 Server Status")
    print("=" * 60)

    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        print_check(
            "Server running on port 8000",
            response.status_code == 200
        )
    except requests.ConnectionError:
        print_check(
            "Server running on port 8000",
            False,
            "Server not reachable. Start with: uvicorn main:app --host 0.0.0.0 --port 8000"
        )
    except Exception as e:
        print_check(
            "Server running on port 8000",
            False,
            f"Error: {e}"
        )


def check_gemini_health():
    """Check Gemini API health"""
    print("\n🤖 Gemini API Status")
    print("=" * 60)

    try:
        response = requests.get(
            "http://localhost:8000/api/v1/chat/health",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            healthy = data.get("status") == "healthy"
            print_check(
                "Gemini API reachable",
                healthy,
                f"Model: {data.get('model')}" if healthy else data.get('error')
            )
        else:
            print_check(
                "Gemini API reachable",
                False,
                f"Health check returned {response.status_code}"
            )

    except requests.ConnectionError:
        print_check(
            "Gemini API reachable",
            False,
            "Server not running"
        )
    except Exception as e:
        print_check(
            "Gemini API reachable",
            False,
            f"Error: {e}"
        )


def check_database():
    """Check database connection"""
    print("\n🗄️  Database Status")
    print("=" * 60)

    try:
        # Try to import and connect
        from sqlmodel import create_engine, Session, select
        from models import SpiritualTask

        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            print_check("Database connection", False, "DATABASE_URL not set")
            return

        engine = create_engine(db_url)
        with Session(engine) as session:
            # Try simple query
            result = session.exec(select(SpiritualTask).limit(1)).first()
            print_check("Database connection", True, "Connected and query successful")

    except Exception as e:
        print_check("Database connection", False, f"Error: {e}")


def check_logs():
    """Check log files"""
    print("\n📝 Log Files")
    print("=" * 60)

    log_dir = Path(__file__).parent.parent / "logs"

    if not log_dir.exists():
        print_check("Log directory exists", False, "Create with: mkdir logs")
        return

    print_check("Log directory exists", True)

    for log_file in ["salaatflow.log", "salaatflow_errors.log"]:
        log_path = log_dir / log_file
        if log_path.exists():
            size = log_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print_check(
                f"{log_file} exists",
                True,
                f"Size: {size_mb:.2f} MB"
            )
        else:
            print_check(
                f"{log_file} exists",
                False,
                "Will be created on first run"
            )


def main():
    """Run all diagnostics"""
    print("=" * 60)
    print("🔍 SalaatFlow System Diagnostics")
    print("=" * 60)

    check_environment()
    check_dependencies()
    check_logs()
    check_server()
    check_gemini_health()
    check_database()

    print("\n" + "=" * 60)
    print("Diagnostic scan complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

#### Running Diagnostics

```bash
cd backend
python scripts/diagnose.py

# Example output:
# ============================================================
# 🔍 SalaatFlow System Diagnostics
# ============================================================
#
# 📋 Environment Configuration
# ============================================================
# ✅ GEMINI_API_KEY set
#    Value: AIzaSyBa-hcy0emMTYAwu...
# ✅ DATABASE_URL set
#    Connected to Neon PostgreSQL
# ✅ GEMINI_MODEL set
#    Value: gemini-pro
# ...
```

---

## 9. Acceptance Criteria

### 9.1 Functional Acceptance Criteria

All Phase III functionality MUST meet these criteria:

#### 1. Simple Chat Success
✅ **PASS Criteria**:
- User sends: "Assalamualaikum" or "Hello, what can you do?"
- Backend returns: Valid, helpful assistant reply (not an error)
- Response time: < 5 seconds
- No errors in logs

✅ **Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Assalamualaikum",
    "user_id": null,
    "conversation_history": [],
    "language": "en"
  }'

# Expected response:
# {
#   "success": true,
#   "message": "Wa alaikum assalam! How can I help you today?...",
#   "error": null,
#   "tool_used": null,
#   "request_id": "..."
# }
```

#### 2. Gemini Health Check Passes
✅ **PASS Criteria**:
- Health check endpoint returns 200
- Status is "healthy"
- Response time < 10 seconds

✅ **Test Command**:
```bash
curl http://localhost:8000/api/v1/chat/health

# Expected response:
# {
#   "service": "gemini",
#   "status": "healthy",
#   "model": "gemini-pro",
#   "timestamp": 1735567890.123
# }
```

#### 3. Task Creation Works
✅ **PASS Criteria**:
- Authenticated user sends: "Create a task for Fajr prayer"
- Backend creates task successfully
- Returns structured response with task data
- No errors in logs

✅ **Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task for Fajr prayer",
    "user_id": 1,
    "conversation_history": [],
    "language": "en"
  }'

# Expected response:
# {
#   "success": true,
#   "message": "✅ Task created successfully!\n\nTitle: Fajr prayer\n...",
#   "tool_used": "create_task",
#   "data": {"task": {...}},
#   "request_id": "..."
# }
```

#### 4. Authentication Handling
✅ **PASS Criteria**:
- Unauthenticated user sends: "Create a task for Fajr"
- Backend returns 401 with clear message
- Error message guides user to sign in
- No server errors

✅ **Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task for Fajr prayer",
    "user_id": null,
    "conversation_history": [],
    "language": "en"
  }'

# Expected response (401):
# {
#   "success": false,
#   "message": "",
#   "error": "authentication_required",
#   "error_message": "Please log in to perform this action...",
#   "request_id": "..."
# }
```

#### 5. Error Transparency
✅ **PASS Criteria**:
- Intentionally invalid API key triggers clear error
- Backend logs full error with stack trace
- Chat UI shows user-friendly message (not cryptic)
- Error differentiated from other types

✅ **Test Procedure**:
```bash
# 1. Set invalid API key in .env
GEMINI_API_KEY=invalid_key

# 2. Restart server

# 3. Send chat request
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": null}'

# Expected:
# - Response has error="authentication_failed"
# - error_message is user-friendly
# - Server logs show full error with stack trace
# - Log entry includes request_id for tracking
```

#### 6. Clean Build/Test
✅ **PASS Criteria**:
- `npm run build` (frontend): Completes with exit code 0
- `npm run lint:check` (frontend): No errors
- `uvicorn main:app` (backend): Starts without errors
- `python tests/test_chat_integration.py`: All tests pass

### 9.2 Non-Functional Acceptance Criteria

#### Performance
- Chat response time: < 5 seconds (95th percentile)
- Health check response: < 2 seconds
- Server startup time: < 30 seconds

#### Reliability
- Chat success rate: > 95% (excluding quota/network errors)
- Error handling coverage: 100% (no unhandled exceptions)
- Graceful degradation: Service works with basic conversation even if tools fail

#### Observability
- All requests logged with unique request_id
- All errors logged with stack trace
- Log rotation configured (max 10MB per file)
- Diagnostic script available

#### Security
- API keys never logged
- No secrets in error messages returned to client
- Input validation on all endpoints
- Authentication enforced for mutating operations

---

## 10. Documentation Requirements

### 10.1 Required Documentation Files

#### File: `docs/phase3_spec.md`
**Content**: This refined specification document

#### File: `docs/phase3_build_and_test.md`
**Content**:

```markdown
# Phase III Build and Test Guide

## Prerequisites

### Frontend
- Node.js 18+
- npm 9+

### Backend
- Python 3.12+
- pip
- PostgreSQL (Neon)
- Google Gemini API key

## Environment Setup

### 1. Clone and Install

```bash
# Frontend
cd frontend
npm install

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create `backend/.env`:
```env
GEMINI_API_KEY=your-actual-api-key-here
DATABASE_URL=your-neon-postgres-url-here
GEMINI_MODEL=gemini-pro
```

Get Gemini API key: https://aistudio.google.com/app/apikey

## Build Commands

### Frontend

```bash
cd frontend

# Lint check
npm run lint:check
# Expected: ✓ No ESLint warnings or errors

# Type check
npm run type-check
# Expected: ✓ No TypeScript errors

# Production build
npm run build
# Expected: ✓ Compiled successfully

# Run all checks
npm test
```

### Backend

```bash
cd backend
source venv/bin/activate

# Type check (optional)
mypy chatbot/ routers/ --ignore-missing-imports

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Expected output:
# ✅ Chatbot settings loaded (Google Gemini)
# 🚀 Starting SalaatFlow API...
# INFO: Uvicorn running on http://0.0.0.0:8000
```

## Testing

### 1. Run Diagnostics

```bash
cd backend
python scripts/diagnose.py
```

This checks:
- ✅ Environment configuration
- ✅ Dependencies installed
- ✅ Server running
- ✅ Gemini API reachable
- ✅ Database connected
- ✅ Log files present

### 2. Run Integration Tests

```bash
cd backend

# Start server first
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Run tests
python tests/test_chat_integration.py

# Expected:
# ✅ PASS - Health Check
# ✅ PASS - Simple Chat
# ✅ PASS - Auth Handling
```

### 3. Manual Testing

#### Test Chat UI
1. Start both servers:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. Open http://localhost:3000/chat

3. Test scenarios:
   - ✅ Simple greeting: "Assalamualaikum"
   - ✅ Task creation (signed in): "Create Fajr task"
   - ✅ Task creation (not signed in): Should show auth error
   - ✅ Masjid search: "Find masjids in DHA"

## Troubleshooting

### Build Fails

**Frontend**:
- Run `npm install` to ensure dependencies
- Check `package.json` for syntax errors
- Clear `.next` folder: `rm -rf .next`

**Backend**:
- Check Python version: `python --version` (must be 3.12+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check `.env` file exists and has all required variables

### Server Won't Start

**Port already in use**:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection fails**:
- Check DATABASE_URL is correct
- Verify network connection to Neon
- Check Neon dashboard for database status

**Gemini API errors**:
- Verify API key is valid: Check https://aistudio.google.com/app/apikey
- Check internet connection
- Check Gemini service status

### Tests Fail

1. Check server is running: `curl http://localhost:8000/docs`
2. Check health endpoint: `curl http://localhost:8000/api/v1/chat/health`
3. Check logs: `tail -f backend/logs/salaatflow.log`
4. Run diagnostics: `python scripts/diagnose.py`

## Success Indicators

✅ **All these should be true**:
- Frontend builds without errors
- Backend starts without errors
- Health check returns "healthy"
- Simple chat returns valid response
- Auth errors handled gracefully
- All tests pass

If any of these fail, check the troubleshooting section above.
```

#### File: `README.md` (update)
Add section:

```markdown
## Phase III: AI Chatbot

### Features
- 🤖 Google Gemini-powered assistant
- ✅ Task management via natural language
- 🕌 Masjid information queries
- 📖 Hadith retrieval
- 🔒 Authenticated operations
- 🌐 Urdu & English support

### Quick Start

#### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm run dev
```

Visit: http://localhost:3000/chat

### Build & Test

See [Phase III Build Guide](docs/phase3_build_and_test.md) for detailed instructions.

#### Quick Test
```bash
# Run diagnostics
python backend/scripts/diagnose.py

# Run integration tests
python backend/tests/test_chat_integration.py
```

### Troubleshooting

**Chatbot returns errors?**
1. Check Gemini API key: `cat backend/.env | grep GEMINI`
2. Check health: `curl http://localhost:8000/api/v1/chat/health`
3. View logs: `python backend/scripts/view_logs.py --errors-only --tail 20`

**Server won't start?**
1. Check port: `lsof -i:8000`
2. Kill if needed: `lsof -ti:8000 | xargs kill -9`
3. Check logs: `tail -f backend/logs/salaatflow.log`

For more help, see docs/phase3_build_and_test.md
```

---

## 11. Implementation Checklist

### Backend Implementation

- [ ] **Configuration**
  - [ ] `backend/chatbot/config/settings.py` - Gemini configuration with validation
  - [ ] `backend/.env` - All required variables set
  - [ ] Validation on startup

- [ ] **Gemini Client**
  - [ ] `backend/chatbot/agent/gemini_client.py` - Robust client implementation
  - [ ] Error handling (auth, quota, network, generic)
  - [ ] Retry logic
  - [ ] Health check method
  - [ ] Comprehensive logging

- [ ] **Orchestrator**
  - [ ] `backend/chatbot/agent/orchestrator.py` - Message processing
  - [ ] Intent detection
  - [ ] Tool execution
  - [ ] Error transformation
  - [ ] Response formatting

- [ ] **Chat Endpoint**
  - [ ] `backend/routers/chatbot.py` - HTTP endpoint
  - [ ] Request validation
  - [ ] Authentication checks
  - [ ] Structured error responses
  - [ ] Health check endpoint
  - [ ] Request ID tracking

- [ ] **Logging**
  - [ ] `backend/logging_config.py` - Configuration
  - [ ] Secret filtering
  - [ ] Log rotation
  - [ ] Request/response logging
  - [ ] Error logging with stack traces

- [ ] **Testing**
  - [ ] `backend/tests/test_chat_integration.py` - Integration tests
  - [ ] Health check test
  - [ ] Simple chat test
  - [ ] Auth handling test
  - [ ] All tests pass

- [ ] **Diagnostics**
  - [ ] `backend/scripts/diagnose.py` - Diagnostic script
  - [ ] `backend/scripts/view_logs.py` - Log viewer
  - [ ] Documentation for both

### Frontend Implementation

- [ ] **Chat UI**
  - [ ] `frontend/app/chat/page.tsx` - Main chat page
  - [ ] Message display
  - [ ] Loading states
  - [ ] Error displays (network, auth, service)
  - [ ] Error styling distinct from normal messages

- [ ] **API Integration**
  - [ ] Fetch to `/api/v1/chat`
  - [ ] Error handling
  - [ ] Auth token passing
  - [ ] Conversation history management

- [ ] **Build**
  - [ ] `npm run build` succeeds
  - [ ] `npm run lint:check` succeeds
  - [ ] `npm run type-check` succeeds
  - [ ] No build warnings

### Documentation

- [ ] **Specification**
  - [ ] This file (`docs/PHASE3_REFINED_SPECIFICATION.md`)
  - [ ] All sections complete
  - [ ] Examples provided

- [ ] **Build Guide**
  - [ ] `docs/phase3_build_and_test.md`
  - [ ] Prerequisites listed
  - [ ] Build commands documented
  - [ ] Test procedures documented
  - [ ] Troubleshooting guide

- [ ] **README**
  - [ ] Phase III section added
  - [ ] Quick start instructions
  - [ ] Troubleshooting basics
  - [ ] Links to detailed docs

### Acceptance Testing

- [ ] **Simple Chat Success**
  - [ ] "Assalamualaikum" returns valid response
  - [ ] No errors in logs
  - [ ] Response time < 5s

- [ ] **Health Check**
  - [ ] Endpoint returns 200
  - [ ] Status is "healthy"
  - [ ] Documented command works

- [ ] **Error Transparency**
  - [ ] Invalid API key logged clearly
  - [ ] User-friendly error shown
  - [ ] Request ID for tracking
  - [ ] Stack trace in logs

- [ ] **Authentication**
  - [ ] Unauthenticated task creation returns 401
  - [ ] Clear message shown
  - [ ] No server errors

- [ ] **Clean Build/Test**
  - [ ] All build commands succeed
  - [ ] All tests pass
  - [ ] Documentation accurate

---

## Summary

This refined specification addresses all critical issues with the Phase III chatbot:

1. **Generic Errors Fixed**: Comprehensive error handling with specific, actionable messages
2. **Logging Added**: Full observability with request tracking and detailed logs
3. **Health Checks**: Gemini health check endpoint and diagnostic tools
4. **Build/Test**: Clear procedures and automated testing
5. **Documentation**: Complete guides for building, testing, and troubleshooting

**Key Improvements**:
- ✅ NO MORE "I encountered an unexpected error"
- ✅ Clear error differentiation (auth, quota, network, etc.)
- ✅ Request ID tracking through entire flow
- ✅ Comprehensive logging without secrets
- ✅ Diagnostic tools for troubleshooting
- ✅ Integration tests with clear pass/fail criteria
- ✅ User-friendly error messages in UI
- ✅ Full documentation

**Next Steps**:
1. Implement backend changes per specification
2. Implement frontend error handling
3. Add logging configuration
4. Create test and diagnostic scripts
5. Update documentation
6. Run acceptance tests
7. Verify all criteria met

---

**Version**: 2.0 (Refined)
**Status**: Ready for Implementation
**Approval**: Pending Review
