# Phase III Fix & Stabilize - Implementation Plan

**Project**: SalaatFlow
**Goal**: Make Gemini chatbot functional and eliminate generic "unexpected error" responses
**Date**: 2025-12-30
**Status**: Ready for Execution

---

## Executive Summary

This plan addresses the critical issue where the Phase III chatbot returns generic "I encountered an unexpected error. Please try again." instead of:
- Proper responses when configured correctly
- Specific, actionable error messages when real problems occur

The plan is organized into 7 sequential milestones, each with specific files, validation steps, and success criteria.

---

## Overall Success Criteria

Before marking Phase III as "fixed and stable":

✅ **Functional Requirements**
1. Simple chat message returns valid assistant response (not an error)
2. Task creation via chat works for authenticated users
3. Health check endpoint returns "healthy" when Gemini is configured
4. Auth errors return 401 with clear message
5. Gemini errors are logged with details, user sees friendly message

✅ **Build Requirements**
1. `npm run lint` (frontend): No errors
2. `npm run build` (frontend): Success
3. `uvicorn main:app` (backend): Starts without errors
4. Integration tests pass

✅ **Observability Requirements**
1. All chat requests logged with request_id
2. All errors logged with stack trace
3. No secrets in logs
4. Diagnostic script works

---

## Milestone 1: Diagnostics & Logging Infrastructure

**Priority**: CRITICAL
**Duration**: ~1 hour
**Dependencies**: None

### Objective
Establish comprehensive logging so we can SEE what's failing when chatbot returns errors.

### Files to Create/Modify

#### 1.1 Create Logging Configuration

**File**: `backend/chatbot/config/logging_config.py`

**Content**:
```python
"""
Logging configuration for SalaatFlow chatbot
- Structured logging with JSON format
- Secret filtering
- Request ID tracking
- Separate error log file
"""

import logging
import logging.config
from pathlib import Path
import re
from typing import Any, Dict


class SecretFilter(logging.Filter):
    """Filter to remove secrets from logs"""

    SECRET_PATTERNS = [
        r'(api[_-]?key["\s:=]+)([a-zA-Z0-9-_]+)',
        r'(bearer\s+)([a-zA-Z0-9-_.]+)',
        r'(password["\s:=]+)([^\s"]+)',
        r'(AIza[a-zA-Z0-9_-]+)',  # Gemini API keys
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'msg'):
            msg = str(record.msg)
            for pattern in self.SECRET_PATTERNS:
                msg = re.sub(pattern, r'\1[REDACTED]', msg, flags=re.IGNORECASE)
            record.msg = msg
        return True


def setup_logging():
    """Setup logging configuration"""

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    logging_config = {
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
            "detailed": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - "
                    "%(message)s\n"
                    "  File: %(pathname)s:%(lineno)d\n"
                    "  Function: %(funcName)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "filters": {
            "secret_filter": {
                "()": SecretFilter
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "filters": ["secret_filter"],
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filters": ["secret_filter"],
                "filename": "logs/chatbot.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filters": ["secret_filter"],
                "filename": "logs/chatbot_errors.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 10,
                "encoding": "utf-8"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file", "error_file"]
        },
        "loggers": {
            "chatbot": {
                "level": "DEBUG",
                "propagate": True
            },
            "routers.chatbot": {
                "level": "DEBUG",
                "propagate": True
            }
        }
    }

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    logger.info(f"Logs directory: {Path('logs').absolute()}")
```

#### 1.2 Update Main Application to Use Logging

**File**: `backend/main.py`

**Modifications**:
- Add import: `from chatbot.config.logging_config import setup_logging`
- Call `setup_logging()` before app creation
- Add startup logging

**Expected additions**:
```python
# At the top, after imports
from chatbot.config.logging_config import setup_logging

# Before app creation
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Initializing SalaatFlow API...")
```

#### 1.3 Add Request ID Middleware

**File**: `backend/middleware/request_id.py` (NEW)

**Content**:
```python
"""
Request ID middleware for tracking requests through logs
"""

import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to every request"""

    async def dispatch(self, request: Request, call_next):
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store in request state
        request.state.request_id = request_id

        # Log incoming request
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host if request.client else None
            }
        )

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "status_code": response.status_code
            }
        )

        return response


def add_request_id_middleware(app: FastAPI):
    """Add middleware to app"""
    app.add_middleware(RequestIDMiddleware)
```

**File**: `backend/main.py` (UPDATE)

Add middleware:
```python
from middleware.request_id import add_request_id_middleware

# After app creation
add_request_id_middleware(app)
```

### Validation Steps

#### 1. Check Logging Setup
```bash
cd backend
source venv/bin/activate

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000

# Expected in console:
# 2025-12-30 12:00:00 - chatbot.config.logging_config - INFO - Logging configured successfully
# 2025-12-30 12:00:00 - chatbot.config.logging_config - INFO - Logs directory: /path/to/logs
# 2025-12-30 12:00:00 - __main__ - INFO - Initializing SalaatFlow API...
```

#### 2. Verify Log Files Created
```bash
ls -lh logs/

# Expected:
# chatbot.log
# chatbot_errors.log
```

#### 3. Test Request ID Tracking
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: test-request-123" \
  -d '{"message": "Hello", "user_id": null}'

# Check response headers for X-Request-ID
# Check logs:
tail -f logs/chatbot.log | grep test-request-123
```

#### 4. Verify Secret Filtering
```bash
# Check that API keys are redacted in logs
grep -i "api_key" logs/chatbot.log | grep -i "redacted"

# Should see [REDACTED] instead of actual keys
```

### Success Criteria

✅ Logging configuration loads without errors
✅ Log files created in `logs/` directory
✅ Request IDs tracked through entire request
✅ Secrets redacted in log output
✅ Console shows INFO level, files show DEBUG level
✅ Error log file created separately

---

## Milestone 2: Gemini Client with Robust Error Handling

**Priority**: CRITICAL
**Duration**: ~2 hours
**Dependencies**: Milestone 1 (logging)

### Objective
Create a robust Gemini API client that:
- Catches and classifies all error types
- Retries transient errors
- Logs everything with context
- Never returns generic errors

### Files to Create/Modify

#### 2.1 Create Gemini Client

**File**: `backend/chatbot/gemini/client.py` (NEW)

**Content**: Full implementation as specified in PHASE3_REFINED_SPECIFICATION.md Section 3.2

**Key features**:
- Custom exception classes: `GeminiAuthError`, `GeminiQuotaError`, `GeminiNetworkError`
- Retry logic with exponential backoff
- Detailed logging at every step
- Health check method
- No generic error messages

#### 2.2 Create Gemini Configuration

**File**: `backend/chatbot/gemini/config.py` (NEW)

**Content**:
```python
"""
Gemini API configuration with validation
"""

from pydantic import BaseModel, field_validator
import os
from dotenv import load_dotenv

load_dotenv()


class GeminiConfig(BaseModel):
    """Gemini API configuration"""

    api_key: str
    model: str = "gemini-pro"
    timeout: int = 30
    max_retries: int = 2
    retry_delay: float = 1.0

    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        if not v or v == "your-gemini-api-key":
            raise ValueError(
                "GEMINI_API_KEY not set. "
                "Get one from: https://aistudio.google.com/app/apikey"
            )
        if not v.startswith('AIza'):
            raise ValueError(
                f"Invalid Gemini API key format: {v[:10]}..."
            )
        return v

    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, v):
        if v < 5 or v > 300:
            raise ValueError("Timeout must be 5-300 seconds")
        return v

    @classmethod
    def from_env(cls) -> "GeminiConfig":
        """Load from environment variables"""
        return cls(
            api_key=os.getenv("GEMINI_API_KEY", ""),
            model=os.getenv("GEMINI_MODEL", "gemini-pro"),
            timeout=int(os.getenv("GEMINI_TIMEOUT", "30")),
            max_retries=int(os.getenv("GEMINI_MAX_RETRIES", "2")),
            retry_delay=float(os.getenv("GEMINI_RETRY_DELAY", "1.0"))
        )
```

#### 2.3 Update Settings to Use New Config

**File**: `backend/chatbot/config/settings.py`

**Update**:
```python
from chatbot.gemini.config import GeminiConfig

# Load Gemini config
try:
    GEMINI_CONFIG = GeminiConfig.from_env()
    print(f"✅ Gemini configured: model={GEMINI_CONFIG.model}")
except Exception as e:
    print(f"❌ Gemini configuration error: {e}")
    raise
```

### Validation Steps

#### 1. Test Configuration Loading
```bash
cd backend
source venv/bin/activate
python -c "from chatbot.gemini.config import GeminiConfig; c = GeminiConfig.from_env(); print(f'Model: {c.model}')"

# Expected:
# Model: gemini-pro
```

#### 2. Test Invalid API Key Detection
```bash
# Temporarily set invalid key
export GEMINI_API_KEY="invalid_key"

python -c "from chatbot.gemini.config import GeminiConfig; GeminiConfig.from_env()"

# Expected:
# ValueError: Invalid Gemini API key format: invalid_key...
```

#### 3. Test Gemini Client Health Check
```bash
# With valid API key
export GEMINI_API_KEY="your-actual-key"

python -c "
from chatbot.gemini.client import GeminiClient
from chatbot.gemini.config import GeminiConfig
client = GeminiClient(GeminiConfig.from_env())
health = client.health_check()
print(health)
"

# Expected:
# {'service': 'gemini', 'status': 'healthy', 'model': 'gemini-pro', ...}
```

#### 4. Test Error Classification
```bash
# Test with invalid key
python -c "
from chatbot.gemini.client import GeminiClient, GeminiAuthError
from chatbot.gemini.config import GeminiConfig
import os
os.environ['GEMINI_API_KEY'] = 'AIzaInvalidKey'
config = GeminiConfig.from_env()
client = GeminiClient(config)
try:
    client.generate_response('Hello')
except GeminiAuthError as e:
    print(f'✅ Auth error caught: {e}')
"

# Expected:
# ✅ Auth error caught: Invalid Gemini API key. Please check your configuration.
```

### Success Criteria

✅ `GeminiConfig` loads from environment
✅ `GeminiConfig` validates API key format
✅ `GeminiClient` initializes successfully
✅ Health check works with valid API key
✅ Auth errors caught and classified as `GeminiAuthError`
✅ Network errors caught and classified as `GeminiNetworkError`
✅ All errors logged with full context
✅ No generic "unexpected error" messages

---

## Milestone 3: Chat Endpoint with Structured Error Handling

**Priority**: CRITICAL
**Duration**: ~1.5 hours
**Dependencies**: Milestones 1, 2

### Objective
Rewrite the `/chat` endpoint to:
- Use the new Gemini client
- Return structured responses (never generic errors)
- Log all errors with context
- Handle auth properly

### Files to Modify

#### 3.1 Update Chat Router

**File**: `backend/routers/chatbot.py`

**Complete rewrite** based on specification Section 4.1.

**Key changes**:
- Import new `GeminiClient` and exceptions
- Add request ID to all responses
- Structured error responses with types
- Auth checking for protected operations
- Comprehensive logging

**Response structure**:
```python
class ChatResponse(BaseModel):
    success: bool
    message: str = ""
    error: Optional[str] = None  # Error type code
    error_message: Optional[str] = None  # User-friendly message
    tool_used: Optional[str] = None
    data: Optional[dict] = None
    request_id: str
```

**Error types to handle**:
- `authentication_required` → 401
- `authentication_failed` → 500
- `quota_exceeded` → 500
- `network_error` → 500
- `tool_execution_failed` → 500
- `internal_error` → 500

#### 3.2 Add Health Check Endpoint

**File**: `backend/routers/chatbot.py`

**Add endpoint**:
```python
@router.get("/chat/health")
async def chat_health_check():
    """Health check for chat service"""
    try:
        health = gemini_client.health_check()
        status_code = (
            200 if health["status"] == "healthy"
            else 503
        )
        return JSONResponse(
            status_code=status_code,
            content=health
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={
                "service": "gemini",
                "status": "unhealthy",
                "error": str(e)
            }
        )
```

#### 3.3 Update Agent to Use New Client

**File**: `backend/chatbot/agent/agent.py`

**Key changes**:
- Import `GeminiClient` and exceptions
- Remove old Gemini integration code
- Update `run_agent` to use new client
- Propagate exceptions to router for handling

### Validation Steps

#### 1. Test Simple Chat Success
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Assalamualaikum",
    "user_id": null
  }' | jq

# Expected:
# {
#   "success": true,
#   "message": "Wa alaikum assalam! How can I help you?...",
#   "error": null,
#   "error_message": null,
#   "tool_used": null,
#   "data": null,
#   "request_id": "uuid-here"
# }
```

#### 2. Test Auth Required Error
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task for Fajr",
    "user_id": null
  }' | jq

# Expected (401):
# {
#   "success": false,
#   "message": "",
#   "error": "authentication_required",
#   "error_message": "Please log in to perform this action...",
#   "request_id": "uuid-here"
# }
```

#### 3. Test Health Check
```bash
curl http://localhost:8000/api/v1/chat/health | jq

# Expected:
# {
#   "service": "gemini",
#   "status": "healthy",
#   "model": "gemini-pro",
#   "timestamp": 1234567890.123
# }
```

#### 4. Verify Error Logging
```bash
# Make a request that will fail (invalid API key)
# Check logs:
tail -f logs/chatbot_errors.log

# Expected to see:
# - Full stack trace
# - Request ID
# - Error type classification
# - NOT "unexpected error"
```

### Success Criteria

✅ Simple chat returns valid response
✅ Auth-required operations return 401 with clear message
✅ Health check endpoint works
✅ All responses include request_id
✅ Errors are classified (not generic)
✅ Error messages are user-friendly
✅ All errors logged with stack trace
✅ No unhandled exceptions

---

## Milestone 4: Frontend Error Handling & UI Polish

**Priority**: HIGH
**Duration**: ~1.5 hours
**Dependencies**: Milestone 3

### Objective
Update chat UI to:
- Display errors clearly and distinctly
- Show loading states
- Handle all error types gracefully
- No unhandled promise rejections

### Files to Modify

#### 4.1 Update Chat Page Component

**File**: `frontend/app/chat/page.tsx`

**Key changes**:
- Add error state with type and message
- Distinct error rendering for each type
- Loading state during requests
- Error styling different from normal messages

**Error types to handle**:
```typescript
type ErrorType =
  | 'authentication_required'
  | 'authentication_failed'
  | 'quota_exceeded'
  | 'network_error'
  | 'tool_execution_failed'
  | 'internal_error'
  | 'unknown';

interface ErrorState {
  type: ErrorType;
  message: string;
  requestId?: string;
}
```

**Error display components**:
```tsx
{error?.type === 'authentication_required' && (
  <Alert variant="warning" className="mb-4">
    <Lock className="h-4 w-4" />
    <AlertTitle>Sign In Required</AlertTitle>
    <AlertDescription>
      {error.message}
      <Button variant="link" className="pl-1" onClick={() => router.push('/signin')}>
        Sign in now
      </Button>
    </AlertDescription>
  </Alert>
)}

{error?.type === 'network_error' && (
  <Alert variant="destructive" className="mb-4">
    <AlertCircle className="h-4 w-4" />
    <AlertTitle>Connection Issue</AlertTitle>
    <AlertDescription>
      {error.message || 'Unable to reach the server. Please check your connection.'}
    </AlertDescription>
  </Alert>
)}

// ... other error types
```

#### 4.2 Update API Call Logic

**File**: `frontend/lib/chatApi.ts` (NEW if doesn't exist)

**Create abstraction**:
```typescript
export interface ChatRequest {
  message: string;
  userId?: number;
  conversationHistory?: ChatMessage[];
}

export interface ChatResponse {
  success: boolean;
  message: string;
  error?: string;
  errorMessage?: string;
  requestId: string;
  toolUsed?: string;
  data?: any;
}

export async function sendChatMessage(
  request: ChatRequest,
  authToken?: string
): Promise<ChatResponse> {
  const response = await fetch('/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(authToken && { 'Authorization': `Bearer ${authToken}` })
    },
    body: JSON.stringify({
      message: request.message,
      user_id: request.userId,
      conversation_history: request.conversationHistory || []
    })
  });

  if (!response.ok && response.status !== 401) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return await response.json();
}
```

#### 4.3 Update Chat Component to Use API

**File**: `frontend/app/chat/page.tsx`

**Update sendMessage function**:
```typescript
async function handleSendMessage(message: string) {
  setIsLoading(true);
  setError(null);

  // Add user message
  const userMsg: ChatMessage = {
    role: 'user',
    content: message,
    timestamp: new Date()
  };
  setMessages(prev => [...prev, userMsg]);

  try {
    const response = await sendChatMessage(
      {
        message,
        userId: session?.user?.id,
        conversationHistory: messages.slice(-10)
      },
      session?.accessToken
    );

    if (response.success) {
      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.message,
        timestamp: new Date()
      }]);
    } else {
      // Handle error response
      setError({
        type: (response.error as ErrorType) || 'unknown',
        message: response.errorMessage || 'An error occurred',
        requestId: response.requestId
      });

      // Optionally show error as message too
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.errorMessage || 'Sorry, I encountered an error.',
        timestamp: new Date(),
        isError: true
      }]);
    }
  } catch (err) {
    console.error('Chat request failed:', err);
    setError({
      type: 'network_error',
      message: 'Unable to connect to the server. Please try again.'
    });

    setMessages(prev => [...prev, {
      role: 'assistant',
      content: 'Connection failed. Please check your internet and try again.',
      timestamp: new Date(),
      isError: true
    }]);
  } finally {
    setIsLoading(false);
  }
}
```

### Validation Steps

#### 1. Test Normal Chat Flow
```
1. Open http://localhost:3000/chat
2. Type: "Assalamualaikum"
3. Send
Expected:
- Loading indicator appears
- Response appears (not an error)
- No error alerts shown
```

#### 2. Test Auth Error Display
```
1. Ensure not signed in
2. Type: "Create a task for Fajr"
3. Send
Expected:
- Warning alert appears
- Message says "Sign In Required"
- Link to sign in page provided
- Error styled differently (yellow/warning color)
```

#### 3. Test Network Error Display
```
1. Stop backend server
2. Type any message
3. Send
Expected:
- Error alert appears (red)
- Message says "Connection Issue"
- Helpful troubleshooting text
```

#### 4. Test Console for Errors
```
1. Open browser DevTools
2. Go through various scenarios
Expected:
- No unhandled promise rejections
- No undefined/null errors in console
- Network errors show in Network tab with details
```

### Success Criteria

✅ Loading state displays during request
✅ Auth errors show warning alert with sign-in link
✅ Network errors show error alert with helpful message
✅ Service errors show error alert with support info
✅ Error messages styled distinctly from normal messages
✅ No unhandled promise rejections in console
✅ All error types handled gracefully
✅ User never sees raw API responses

---

## Milestone 5: Integration Tests & Validation Scripts

**Priority**: HIGH
**Duration**: ~1 hour
**Dependencies**: Milestones 1-4

### Objective
Create automated tests that verify:
- Chatbot responds correctly
- Errors are handled properly
- Health checks work
- Build succeeds

### Files to Create

#### 5.1 Chat Integration Test

**File**: `backend/tests/test_chat_integration.py`

**Content**: Full implementation as specified in PHASE3_REFINED_SPECIFICATION.md Section 7.3

**Tests to include**:
1. `test_health_check()` - Gemini health check works
2. `test_simple_chat()` - Simple message gets valid response
3. `test_authenticated_operation()` - Auth errors handled correctly

#### 5.2 Diagnostic Script

**File**: `backend/scripts/diagnose.py`

**Content**: Full implementation as specified in PHASE3_REFINED_SPECIFICATION.md Section 8.2

**Checks to include**:
- Environment variables set
- Dependencies installed
- Server running
- Gemini API reachable
- Database connected
- Log files exist

#### 5.3 Log Viewer Script

**File**: `backend/scripts/view_logs.py`

**Content**:
```python
#!/usr/bin/env python3
"""
Simple log viewer for debugging
Usage: python scripts/view_logs.py [--tail N] [--errors-only] [--request-id ID]
"""

import argparse
from pathlib import Path
import sys


def view_logs(
    log_file: str = "logs/chatbot.log",
    tail: int = None,
    errors_only: bool = False,
    request_id: str = None
):
    """View logs with filtering"""

    log_path = Path(log_file)
    if not log_path.exists():
        print(f"❌ Log file not found: {log_file}")
        print(f"   Looking in: {log_path.absolute()}")
        sys.exit(1)

    with open(log_path, 'r') as f:
        lines = f.readlines()

    # Apply tail
    if tail:
        lines = lines[-tail:]

    # Filter and display
    displayed = 0
    for line in lines:
        # Filter by error level
        if errors_only and " - ERROR - " not in line:
            continue

        # Filter by request ID
        if request_id and request_id not in line:
            continue

        print(line.rstrip())
        displayed += 1

    print(f"\n{'='*60}")
    print(f"Displayed {displayed} log lines")
    if tail:
        print(f"(Last {tail} lines)")
    if errors_only:
        print("(Errors only)")
    if request_id:
        print(f"(Request ID: {request_id})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View SalaatFlow logs")
    parser.add_argument(
        "--tail",
        type=int,
        help="Show last N lines"
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Show only ERROR level logs"
    )
    parser.add_argument(
        "--request-id",
        help="Filter by request ID"
    )
    parser.add_argument(
        "--error-log",
        action="store_true",
        help="View error log file instead"
    )

    args = parser.parse_args()

    log_file = (
        "logs/chatbot_errors.log" if args.error_log
        else "logs/chatbot.log"
    )

    view_logs(
        log_file=log_file,
        tail=args.tail,
        errors_only=args.errors_only,
        request_id=args.request_id
    )
```

### Validation Steps

#### 1. Run Diagnostic Script
```bash
cd backend
python scripts/diagnose.py

# Expected output:
# ============================================================
# 🔍 SalaatFlow System Diagnostics
# ============================================================
#
# 📋 Environment Configuration
# ============================================================
# ✅ GEMINI_API_KEY set
# ✅ DATABASE_URL set
# ...
# ============================================================
# Diagnostic scan complete!
# ============================================================
```

#### 2. Run Integration Tests
```bash
cd backend
source venv/bin/activate

# Ensure server is running first
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for startup
sleep 5

# Run tests
python tests/test_chat_integration.py

# Expected:
# ============================================================
# SalaatFlow Chat Integration Tests
# ============================================================
# Testing health check...
# ✅ Health check passed
#
# Testing simple chat...
# ✅ Chat response received: Wa alaikum assalam...
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

#### 3. Test Log Viewer
```bash
# View last 20 lines
python scripts/view_logs.py --tail 20

# View errors only
python scripts/view_logs.py --errors-only --tail 50

# View specific request
python scripts/view_logs.py --request-id "uuid-from-response"

# View error log file
python scripts/view_logs.py --error-log --tail 10
```

### Success Criteria

✅ Diagnostic script runs without errors
✅ All environment checks pass
✅ Integration test suite passes (3/3 tests)
✅ Health check test passes
✅ Simple chat test passes
✅ Auth handling test passes
✅ Log viewer displays logs correctly
✅ Filtering options work

---

## Milestone 6: Build & Lint Stabilization

**Priority**: HIGH
**Duration**: ~1 hour
**Dependencies**: All previous milestones

### Objective
Ensure the entire project builds and lints cleanly:
- Frontend builds without errors
- Backend starts without errors
- No TypeScript/linting issues

### Build Commands to Fix

#### 6.1 Frontend Build

**Commands to run and fix**:
```bash
cd frontend

# 1. Install/update dependencies
npm install

# 2. Lint check (fix auto-fixable issues)
npm run lint

# If errors remain, review and fix:
# - Unused imports
# - Missing dependencies
# - TypeScript errors

# 3. Type check
npm run build

# Fix any TypeScript errors that appear
```

**Common issues and fixes**:

| Issue | Fix |
|-------|-----|
| `'X' is defined but never used` | Remove unused imports/variables |
| `Cannot find module 'X'` | `npm install X` or check import path |
| `Type 'X' is not assignable to type 'Y'` | Fix type definitions in components |
| `Property 'X' does not exist on type 'Y'` | Add to interface or handle undefined |

#### 6.2 Backend Dependencies

**File**: `backend/requirements.txt`

**Verify all required packages**:
```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.14
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
psycopg2-binary>=2.9.9
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
```

**Install**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### 6.3 Backend Startup

**Test startup**:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Expected:
# ✅ Logging configured successfully
# ✅ Gemini configured: model=gemini-pro
# 🚀 Starting SalaatFlow API...
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

**Fix import errors**:
- Check all imports resolve
- Check file paths are correct
- Check __init__.py files exist

### Validation Steps

#### 1. Frontend Build Test
```bash
cd frontend

# Clean build
rm -rf .next
npm run build

# Expected output (end):
# ✓ Compiled successfully
# ✓ Linting and checking validity of types
# ✓ Collecting page data
# ✓ Generating static pages (X/X)
# ✓ Finalizing page optimization
#
# Route (app)                              Size     First Load JS
# ┌ ○ /                                    XXX kB        XXX kB
# ├ ○ /chat                                XXX kB        XXX kB
# ...
```

#### 2. Backend Import Test
```bash
cd backend
python -c "
from main import app
from routers.chatbot import router
from chatbot.gemini.client import GeminiClient
from chatbot.config.logging_config import setup_logging
print('✅ All imports successful')
"

# Expected:
# ✅ All imports successful
```

#### 3. Full Stack Test
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - Test
curl http://localhost:3000/chat
# Should return HTML

curl http://localhost:8000/api/v1/chat/health
# Should return JSON health status
```

### Success Criteria

✅ `npm run lint` passes with no errors
✅ `npm run build` succeeds
✅ Backend starts without import errors
✅ Backend starts without configuration errors
✅ Health check endpoint accessible
✅ Frontend pages render without errors
✅ No console errors in browser
✅ All routes accessible

---

## Milestone 7: Documentation & Final Validation

**Priority**: MEDIUM
**Duration**: ~30 minutes
**Dependencies**: All previous milestones

### Objective
Update all documentation to reflect:
- New error handling behavior
- Build and test procedures
- Troubleshooting guide

### Files to Create/Update

#### 7.1 Phase 3 Build & Test Guide

**File**: `docs/phase3_build_and_test.md`

**Content**: Complete guide based on PHASE3_REFINED_SPECIFICATION.md Section 10.1

**Sections**:
1. Prerequisites
2. Environment Setup
3. Build Commands (Frontend & Backend)
4. Testing Procedures
5. Troubleshooting Guide
6. Success Indicators

#### 7.2 Update Main README

**File**: `README.md`

**Add section**:
```markdown
## Phase III: AI-Powered Chatbot

### Quick Start

#### Prerequisites
- Google Gemini API key (get from: https://aistudio.google.com/app/apikey)
- Environment configured (see `.env.example`)

#### Start Services

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (separate terminal)
cd frontend
npm run dev
```

#### Test Chatbot

Visit: http://localhost:3000/chat

Try:
- "Assalamualaikum" (greeting)
- "Create a task for Fajr prayer" (requires sign in)
- "Find masjids in DHA" (search)

### Build & Test

```bash
# Frontend
cd frontend
npm run lint && npm run build

# Backend tests
cd backend
python tests/test_chat_integration.py
```

See [Phase III Build Guide](docs/phase3_build_and_test.md) for details.

### Troubleshooting

**Chatbot returns errors?**
```bash
# 1. Check configuration
python backend/scripts/diagnose.py

# 2. Check health
curl http://localhost:8000/api/v1/chat/health

# 3. View logs
python backend/scripts/view_logs.py --errors-only --tail 20
```

**Build fails?**
- Frontend: `rm -rf .next && npm install && npm run build`
- Backend: Check `logs/chatbot_errors.log`

For more help: [docs/phase3_build_and_test.md](docs/phase3_build_and_test.md)
```

#### 7.3 Create .env.example

**File**: `backend/.env.example`

**Content**:
```env
# SalaatFlow Backend Configuration

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro
GEMINI_TIMEOUT=30
GEMINI_MAX_RETRIES=2

# Server
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Get Gemini API key from:
# https://aistudio.google.com/app/apikey
```

### Validation Steps

#### 1. Verify Documentation Accuracy

```bash
# Follow build guide exactly
cd docs
cat phase3_build_and_test.md

# Try each command listed
# Verify outputs match what's documented
```

#### 2. Test from Fresh Clone

```bash
# Simulate new developer experience
cd /tmp
git clone <your-repo>
cd salaatflow

# Follow README instructions
# Verify everything works
```

#### 3. Verify Troubleshooting Steps

```bash
# Try each troubleshooting command
python backend/scripts/diagnose.py
curl http://localhost:8000/api/v1/chat/health
python backend/scripts/view_logs.py --tail 10

# Verify they all work
```

### Success Criteria

✅ Build guide is accurate and complete
✅ README has Phase III section
✅ .env.example exists with all variables
✅ Troubleshooting commands work
✅ Fresh clone can build and run
✅ All documentation links work

---

## Final Acceptance Testing

After completing all 7 milestones, run this complete test suite:

### 1. Clean Build Test

```bash
# Frontend
cd frontend
rm -rf .next node_modules
npm install
npm run lint
npm run build

# Backend
cd backend
rm -rf logs
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected**: All succeed

### 2. Integration Test Suite

```bash
cd backend
python tests/test_chat_integration.py
```

**Expected**: 3/3 tests pass

### 3. Manual Chat Flow Test

```
1. Open http://localhost:3000/chat
2. Test scenarios:
   ✅ "Assalamualaikum" → Valid response
   ✅ "Create Fajr task" (not signed in) → Auth error with sign-in link
   ✅ Sign in → Create task → Success message
   ✅ "Find masjids in DHA" → List of masjids
```

### 4. Error Scenario Tests

```
1. Stop backend
   → Frontend shows connection error

2. Set invalid Gemini key
   → Health check fails
   → Chat returns clear error
   → Error logged with details

3. Exceed quota (if possible)
   → User sees "at capacity" message
   → Specific error type logged
```

### 5. Logging Verification

```bash
# Make a chat request
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": null}'

# Check logs contain:
python scripts/view_logs.py --tail 20

# Verify present:
✅ Request received with request_id
✅ Gemini request started
✅ Gemini response received
✅ Request completed
✅ No secrets in logs
```

### 6. Diagnostic Check

```bash
python scripts/diagnose.py

# Verify all green:
✅ Environment configured
✅ Dependencies installed
✅ Server running
✅ Gemini reachable
✅ Database connected
✅ Logs present
```

---

## Rollback Plan

If any milestone fails critically:

1. **Identify failure point**
   ```bash
   # Check logs
   python scripts/view_logs.py --errors-only

   # Run diagnostics
   python scripts/diagnose.py
   ```

2. **Revert to last working state**
   ```bash
   git checkout <last-working-commit>
   ```

3. **Document issue**
   - Create issue with:
     - Milestone that failed
     - Error logs
     - Steps to reproduce

4. **Fix and retry**
   - Address root cause
   - Re-run milestone validation
   - Continue from that point

---

## Success Metrics

Phase III is considered "Fixed and Stable" when:

### Functional Metrics
- ✅ Health check returns "healthy"
- ✅ Simple chat works without errors (95%+ success rate)
- ✅ Auth errors are clear and actionable
- ✅ Task creation works for authenticated users
- ✅ No "unexpected error" messages

### Build Metrics
- ✅ Frontend builds in < 2 minutes
- ✅ Backend starts in < 30 seconds
- ✅ All linting passes
- ✅ All tests pass

### Observability Metrics
- ✅ 100% of requests logged
- ✅ 100% of errors logged with stack trace
- ✅ 0 secrets in logs
- ✅ Request tracking works

### Documentation Metrics
- ✅ Build guide accurate
- ✅ Troubleshooting guide complete
- ✅ All commands work as documented

---

## Timeline

**Estimated Total Time**: 8-10 hours

| Milestone | Duration | Priority |
|-----------|----------|----------|
| 1. Logging | 1 hour | CRITICAL |
| 2. Gemini Client | 2 hours | CRITICAL |
| 3. Chat Endpoint | 1.5 hours | CRITICAL |
| 4. Frontend Errors | 1.5 hours | HIGH |
| 5. Tests | 1 hour | HIGH |
| 6. Build | 1 hour | HIGH |
| 7. Docs | 0.5 hours | MEDIUM |
| **Testing** | 1 hour | - |

**Recommended approach**: Complete in order, validating each milestone before proceeding.

---

## Next Steps

1. Review this plan
2. Execute `/sp.tasks` to create task list
3. Execute `/sp.implement` for each milestone
4. Run validation steps after each
5. Complete final acceptance testing
6. Deploy to production

**Plan Status**: ✅ Ready for Execution
**Version**: 1.0
**Date**: 2025-12-30

---

## Appendix: Quick Reference Commands

### Diagnostic Commands
```bash
# Health check
curl http://localhost:8000/api/v1/chat/health

# System diagnostics
python backend/scripts/diagnose.py

# View logs
python backend/scripts/view_logs.py --tail 20 --errors-only
```

### Test Commands
```bash
# Integration tests
python backend/tests/test_chat_integration.py

# Frontend build
cd frontend && npm run build

# Backend start
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
```

### Quick Chat Test
```bash
# Simple chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": null}' | jq

# Auth test
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create task", "user_id": null}' | jq
```

---

**END OF PLAN**
