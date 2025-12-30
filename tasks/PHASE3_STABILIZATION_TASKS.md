# Phase III Stabilization - Detailed Task List

**Project**: SalaatFlow
**Goal**: Fix Gemini chatbot errors and ensure clean builds
**Date**: 2025-12-30
**Status**: Ready for Implementation

---

## Task Execution Guide

Each task is marked with:
- **Priority**: CRITICAL, HIGH, MEDIUM
- **Files**: Specific files to create/modify
- **Validation**: Commands to verify completion
- **Expected Behavior**: What should work after task completion

Execute tasks in order using `/sp.implement <task-id>`

---

## A) Logging & Diagnostics

### A1: Create Logging Configuration Module

**Priority**: CRITICAL
**Files**:
- `backend/chatbot/config/logging_config.py` (CREATE)
- `backend/main.py` (MODIFY)

**Requirements**:
1. Create `logging_config.py` with:
   - Structured logging with JSON format option
   - Console handler (INFO level)
   - File handler (DEBUG level) → `logs/chatbot.log`
   - Error file handler (ERROR level) → `logs/chatbot_errors.log`
   - Secret filter class to redact:
     - API keys (pattern: `AIza...`)
     - Bearer tokens
     - Passwords
     - Any field containing "api_key", "token", "password"
   - `setup_logging()` function that:
     - Creates `logs/` directory if not exists
     - Configures all handlers and filters
     - Logs initialization message
2. Modify `main.py` to:
   - Import and call `setup_logging()` before app creation
   - Add logger and log startup message

**Validation Commands**:
```bash
cd backend
source venv/bin/activate

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000

# Expected in console:
# INFO - Logging configured successfully
# INFO - Logs directory: /path/to/logs
# INFO - Initializing SalaatFlow API...

# Check log files created
ls -lh logs/
# Expected: chatbot.log, chatbot_errors.log

# Verify secret filtering
grep -i "api_key" logs/chatbot.log
# Expected: Should show [REDACTED] not actual keys
```

**Expected Behavior After Completion**:
- ✅ Logs directory auto-created on startup
- ✅ All log entries have timestamp, level, message, file location
- ✅ Secrets automatically redacted
- ✅ Error logs separate from main logs

---

### A2: Add Request ID Tracking Middleware

**Priority**: CRITICAL
**Files**:
- `backend/middleware/request_id.py` (CREATE)
- `backend/main.py` (MODIFY)

**Requirements**:
1. Create `middleware/request_id.py` with:
   - `RequestIDMiddleware` class extending `BaseHTTPMiddleware`
   - Generate UUID for each request (or use X-Request-ID header if present)
   - Store request_id in `request.state.request_id`
   - Log incoming request with:
     - request_id
     - method
     - path
     - client host
   - Add X-Request-ID to response headers
   - Log completed request with:
     - request_id
     - status_code
   - `add_request_id_middleware(app)` function
2. Modify `main.py` to:
   - Import and add middleware after app creation

**Validation Commands**:
```bash
# Send request with custom request ID
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: test-abc-123" \
  -d '{"message": "Hello", "user_id": null}' -v

# Check response headers
# Expected: X-Request-ID: test-abc-123

# Check logs
tail -f logs/chatbot.log | grep "test-abc-123"
# Expected: Multiple log lines with same request_id

# Send request without custom ID
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi", "user_id": null}' -v

# Check response headers for auto-generated UUID
# Expected: X-Request-ID: <uuid>
```

**Expected Behavior After Completion**:
- ✅ Every request gets unique request_id
- ✅ Request ID tracked through entire request lifecycle
- ✅ Request ID returned in response headers
- ✅ All logs for a request share same request_id
- ✅ Can grep logs by request_id to see full request flow

---

### A3: Add Chat Endpoint Request/Response Logging

**Priority**: CRITICAL
**Files**:
- `backend/routers/chatbot.py` (MODIFY)

**Requirements**:
1. At start of `/chat` endpoint, log:
   - request_id (from `request.state.request_id`)
   - user_id (if provided)
   - message length (not full message for privacy)
   - has_conversation_history (boolean)
   - language
2. At end of successful request, log:
   - request_id
   - success=True
   - response_length
   - tool_used (if any)
   - duration (time taken)
3. At end of failed request, log:
   - request_id
   - success=False
   - error_type
   - error_message
   - duration

**Validation Commands**:
```bash
# Make successful request
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Assalamualaikum",
    "user_id": null,
    "conversation_history": []
  }'

# Check logs
tail -20 logs/chatbot.log

# Expected to see:
# INFO - Chat request received: request_id=<uuid>
#   extra: {user_id: null, message_length: 16, has_history: false}
# INFO - Chat request completed: request_id=<uuid>
#   extra: {success: true, response_length: 45, duration: 1.23}

# Make failed request (auth required)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task",
    "user_id": null
  }'

# Check logs
# Expected:
# WARNING - Chat request failed: request_id=<uuid>
#   extra: {error: authentication_required, error_message: ...}
```

**Expected Behavior After Completion**:
- ✅ Every chat request logged at start
- ✅ Every chat response logged at end
- ✅ Success and failure paths both logged
- ✅ No sensitive data (full messages, tokens) in logs
- ✅ Can track request duration
- ✅ Can see which tool was used

---

### A4: Add Gemini Client Call Logging

**Priority**: CRITICAL
**Files**:
- `backend/chatbot/gemini/client.py` (CREATE or MODIFY)

**Requirements**:
1. Before calling Gemini API, log:
   - request_id (passed as context parameter)
   - prompt_length
   - model_name
   - has_system_instruction
2. After successful Gemini call, log:
   - request_id
   - response_length
   - duration
   - model_name
3. On Gemini error, log with ERROR level:
   - request_id
   - error_type (auth, quota, network, unknown)
   - error_message
   - stack_trace (use `exc_info=True`)
   - attempt_number (if retrying)
   - will_retry (boolean)

**Validation Commands**:
```bash
# Make chat request that triggers Gemini
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Islam", "user_id": null}'

# Check logs
tail -30 logs/chatbot.log | grep -i gemini

# Expected:
# DEBUG - Gemini request started
#   extra: {request_id: ..., prompt_length: 45, model: gemini-pro}
# INFO - Gemini response received
#   extra: {request_id: ..., response_length: 234, duration: 1.5}

# Test error scenario (set invalid API key temporarily)
# Check error logs
tail -10 logs/chatbot_errors.log

# Expected:
# ERROR - Gemini API error: authentication_failed
#   extra: {request_id: ..., error_type: auth, will_retry: false}
#   Traceback (most recent call last):
#   ...
```

**Expected Behavior After Completion**:
- ✅ Every Gemini call logged before execution
- ✅ Every Gemini response logged
- ✅ All Gemini errors logged with full context
- ✅ Can track Gemini performance via logs
- ✅ Can debug Gemini issues from logs alone

---

### A5: Add MCP Tool Execution Logging

**Priority**: HIGH
**Files**:
- `backend/chatbot/mcp_tools/__init__.py` (MODIFY)

**Requirements**:
1. In `execute_tool()` function, before execution, log:
   - request_id (if available in context)
   - tool_name
   - user_id
   - sanitized_parameters (remove sensitive data)
2. After successful tool execution, log:
   - request_id
   - tool_name
   - success=True
   - result_type (e.g., "task_created", "tasks_listed")
   - duration
3. After failed tool execution, log with WARNING:
   - request_id
   - tool_name
   - success=False
   - error_type
   - error_message

**Validation Commands**:
```bash
# Make request that uses a tool (requires auth)
# First, create a test user and get auth token
# Then:
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <test-token>" \
  -d '{
    "message": "Create a task for Fajr prayer",
    "user_id": 1
  }'

# Check logs
tail -30 logs/chatbot.log | grep -i tool

# Expected:
# INFO - Executing tool: create_task
#   extra: {request_id: ..., tool_name: create_task, user_id: 1,
#           params: {title: Fajr prayer, priority: medium}}
# INFO - Tool execution successful
#   extra: {request_id: ..., tool_name: create_task, result: task_created}

# Test tool failure (invalid parameters)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <test-token>" \
  -d '{
    "message": "Delete task 99999",
    "user_id": 1
  }'

# Check logs
# Expected:
# WARNING - Tool execution failed
#   extra: {tool_name: delete_task, error: Task not found}
```

**Expected Behavior After Completion**:
- ✅ Every tool call logged before execution
- ✅ Tool success/failure logged
- ✅ Sensitive parameters sanitized in logs
- ✅ Can track which tools are being used
- ✅ Can debug tool failures from logs

---

### A6: Create Log Viewer Script

**Priority**: MEDIUM
**Files**:
- `backend/scripts/view_logs.py` (CREATE)

**Requirements**:
1. Create command-line script with arguments:
   - `--tail N`: Show last N lines
   - `--errors-only`: Show only ERROR level
   - `--request-id ID`: Filter by request ID
   - `--error-log`: View error log file instead of main
2. Script should:
   - Read from `logs/chatbot.log` by default
   - Support filtering by multiple criteria
   - Display lines with formatting
   - Show count of displayed lines at end

**Validation Commands**:
```bash
cd backend

# View last 20 lines
python scripts/view_logs.py --tail 20

# View errors only
python scripts/view_logs.py --errors-only

# View specific request
python scripts/view_logs.py --request-id "abc-123"

# View error log
python scripts/view_logs.py --error-log --tail 10

# Combine filters
python scripts/view_logs.py --errors-only --tail 50

# Check help
python scripts/view_logs.py --help
```

**Expected Behavior After Completion**:
- ✅ Can quickly view recent logs
- ✅ Can filter to errors only
- ✅ Can track specific requests
- ✅ Easy to use for debugging
- ✅ Helps during development

---

## B) Gemini Config & Health-Check

### B1: Create Gemini Configuration Module

**Priority**: CRITICAL
**Files**:
- `backend/chatbot/gemini/config.py` (CREATE)
- `backend/.env` (VERIFY)

**Requirements**:
1. Create `config.py` with `GeminiConfig` Pydantic model:
   - Fields:
     - `api_key: str` (required)
     - `model: str = "gemini-pro"`
     - `timeout: int = 30`
     - `max_retries: int = 2`
     - `retry_delay: float = 1.0`
   - Validators:
     - `api_key`: Must start with "AIza", not be empty or "your-gemini-api-key"
     - `timeout`: Must be 5-300 seconds
   - Class method `from_env()` to load from environment variables:
     - `GEMINI_API_KEY`
     - `GEMINI_MODEL`
     - `GEMINI_TIMEOUT`
     - `GEMINI_MAX_RETRIES`
     - `GEMINI_RETRY_DELAY`
2. Ensure `.env` has all required variables

**Validation Commands**:
```bash
cd backend

# Test configuration loading
python -c "
from chatbot.gemini.config import GeminiConfig
config = GeminiConfig.from_env()
print(f'Model: {config.model}')
print(f'Timeout: {config.timeout}s')
print(f'Max Retries: {config.max_retries}')
"

# Expected output:
# Model: gemini-pro
# Timeout: 30s
# Max Retries: 2

# Test validation (invalid key)
export GEMINI_API_KEY="invalid_key"
python -c "
from chatbot.gemini.config import GeminiConfig
try:
    config = GeminiConfig.from_env()
except ValueError as e:
    print(f'✅ Validation works: {e}')
"

# Expected:
# ✅ Validation works: Invalid Gemini API key format

# Test missing key
unset GEMINI_API_KEY
python -c "
from chatbot.gemini.config import GeminiConfig
try:
    config = GeminiConfig.from_env()
except ValueError as e:
    print(f'✅ Missing key caught: {e}')
"

# Expected:
# ✅ Missing key caught: GEMINI_API_KEY not set
```

**Expected Behavior After Completion**:
- ✅ Configuration loads from environment
- ✅ Invalid API keys rejected at startup
- ✅ Missing configuration fails fast with clear error
- ✅ All Gemini settings centralized
- ✅ Easy to test with different configurations

---

### B2: Create Robust Gemini Client

**Priority**: CRITICAL
**Files**:
- `backend/chatbot/gemini/client.py` (CREATE)

**Requirements**:
1. Create custom exception classes:
   - `GeminiError(Exception)` - Base exception
   - `GeminiAuthError(GeminiError)` - Invalid API key
   - `GeminiQuotaError(GeminiError)` - Quota exceeded
   - `GeminiNetworkError(GeminiError)` - Network/timeout issues
2. Create `GeminiClient` class with:
   - `__init__(config: GeminiConfig)`: Initialize with config
   - `generate_response(prompt, system_instruction, context)`:
     - Call Gemini API
     - Handle all error types and convert to custom exceptions
     - Retry on network errors (up to max_retries)
     - Log all attempts
     - Return response text or raise specific exception
   - `health_check()`:
     - Send trivial prompt: "Hello from SalaatFlow health check. Respond with 'OK'."
     - Return dict: `{service, status, model, timestamp, error?}`
3. Error handling must catch and classify:
   - `google.api_core.exceptions.Unauthenticated` → `GeminiAuthError`
   - `google.api_core.exceptions.ResourceExhausted` → `GeminiQuotaError`
   - `google.api_core.exceptions.DeadlineExceeded` → `GeminiNetworkError` + retry
   - `google.api_core.exceptions.ServiceUnavailable` → `GeminiNetworkError` + retry
   - `google.api_core.exceptions.NotFound` → `GeminiError` (model not found)
   - `Exception` → `GeminiError` (catch-all)

**Validation Commands**:
```bash
cd backend

# Test initialization
python -c "
from chatbot.gemini.client import GeminiClient
from chatbot.gemini.config import GeminiConfig
config = GeminiConfig.from_env()
client = GeminiClient(config)
print('✅ Client initialized')
"

# Test health check (valid key)
python -c "
from chatbot.gemini.client import GeminiClient
from chatbot.gemini.config import GeminiConfig
config = GeminiConfig.from_env()
client = GeminiClient(config)
health = client.health_check()
print(f'Status: {health[\"status\"]}')
print(f'Model: {health[\"model\"]}')
"

# Expected:
# Status: healthy
# Model: gemini-pro

# Test invalid API key
export GEMINI_API_KEY="AIzaInvalidKey123"
python -c "
from chatbot.gemini.client import GeminiClient, GeminiAuthError
from chatbot.gemini.config import GeminiConfig
import os
os.environ['GEMINI_API_KEY'] = 'AIzaInvalidKey123'
config = GeminiConfig.from_env()
client = GeminiClient(config)
try:
    response = client.generate_response('Hello')
except GeminiAuthError as e:
    print(f'✅ Auth error caught correctly: {e}')
"

# Expected:
# ✅ Auth error caught correctly: Invalid Gemini API key...

# Test successful generation
python -c "
from chatbot.gemini.client import GeminiClient
from chatbot.gemini.config import GeminiConfig
config = GeminiConfig.from_env()
client = GeminiClient(config)
response = client.generate_response(
    'Say hello in one word',
    context={'test': True}
)
print(f'Response: {response}')
"

# Expected:
# Response: Hello (or similar)
```

**Expected Behavior After Completion**:
- ✅ Client initializes successfully with valid config
- ✅ Health check returns clear status
- ✅ Auth errors raise `GeminiAuthError` with helpful message
- ✅ Network errors retry automatically
- ✅ Quota errors raise `GeminiQuotaError`
- ✅ All errors logged with context
- ✅ Successful responses returned as strings
- ✅ No generic "unexpected error" exceptions

---

### B3: Create Health Check Endpoint

**Priority**: HIGH
**Files**:
- `backend/routers/chatbot.py` (MODIFY)

**Requirements**:
1. Add `GET /api/v1/chat/health` endpoint:
   - Call `gemini_client.health_check()`
   - Return JSON response:
     - Status 200 if healthy
     - Status 503 if unhealthy
   - Response body: health check dict from client
2. Add try/except to handle client not initialized
3. Log health check requests

**Validation Commands**:
```bash
# Test health check (healthy)
curl http://localhost:8000/api/v1/chat/health | jq

# Expected (200):
# {
#   "service": "gemini",
#   "status": "healthy",
#   "model": "gemini-pro",
#   "timestamp": 1735567890.123,
#   "response_length": 2
# }

# Test with invalid API key (unhealthy)
# Temporarily set invalid key in .env
# Restart server
curl http://localhost:8000/api/v1/chat/health | jq

# Expected (503):
# {
#   "service": "gemini",
#   "status": "unhealthy",
#   "error": "authentication_failed",
#   "message": "Invalid Gemini API key...",
#   "timestamp": 1735567890.123
# }

# Check health endpoint is documented
curl http://localhost:8000/docs
# Should see /api/v1/chat/health in Swagger UI
```

**Expected Behavior After Completion**:
- ✅ Health check endpoint accessible
- ✅ Returns 200 when Gemini is reachable
- ✅ Returns 503 when Gemini has issues
- ✅ Clear error messages when unhealthy
- ✅ Can be used for monitoring
- ✅ Documented in OpenAPI/Swagger

---

## C) Chat Endpoint Behavior

### C1: Create Structured Response Models

**Priority**: CRITICAL
**Files**:
- `backend/routers/chatbot.py` (MODIFY)

**Requirements**:
1. Define Pydantic models at top of file:
   ```python
   class ChatMessage(BaseModel):
       role: str = Field(..., description="'user' or 'assistant'")
       content: str = Field(..., description="Message content")

   class ChatRequest(BaseModel):
       message: str = Field(..., min_length=1, max_length=2000)
       user_id: Optional[int] = None
       conversation_history: Optional[List[ChatMessage]] = []
       language: Optional[str] = "en"
       metadata: Optional[dict] = {}

   class ChatResponse(BaseModel):
       success: bool
       message: str = ""
       error: Optional[str] = None  # Error type code
       error_message: Optional[str] = None  # User-friendly message
       tool_used: Optional[str] = None
       data: Optional[dict] = None
       request_id: str
   ```

**Validation Commands**:
```bash
cd backend

# Test model validation
python -c "
from routers.chatbot import ChatRequest, ChatResponse

# Valid request
req = ChatRequest(message='Hello', user_id=1)
print(f'✅ Valid request: {req.message}')

# Invalid request (empty message)
try:
    req = ChatRequest(message='')
except Exception as e:
    print(f'✅ Validation works: {e}')

# Response model
resp = ChatResponse(
    success=True,
    message='Hello',
    request_id='abc-123'
)
print(f'✅ Valid response: {resp.dict()}')
"
```

**Expected Behavior After Completion**:
- ✅ Request/response models defined
- ✅ Input validation automatic
- ✅ Type safety enforced
- ✅ OpenAPI schema accurate

---

### C2: Rewrite Chat Endpoint with Error Handling

**Priority**: CRITICAL
**Files**:
- `backend/routers/chatbot.py` (MODIFY)

**Requirements**:
1. Update `POST /api/v1/chat` endpoint to:
   - Accept `ChatRequest` model
   - Return `ChatResponse` model
   - Get request_id from `request.state.request_id`
   - Check if operation requires auth (keywords: create, delete, update, task)
   - If requires auth and no user_id, return 401 with:
     - `error="authentication_required"`
     - `error_message="Please log in to perform this action..."`
   - Try to process message:
     - Detect intent
     - Execute tool or call Gemini
   - Catch specific exceptions:
     - `GeminiAuthError` → error="authentication_failed", 500
     - `GeminiQuotaError` → error="quota_exceeded", 500
     - `GeminiNetworkError` → error="network_error", 500
     - `Exception` → error="internal_error", 500
   - Always include request_id in response
   - Return 200 for success, appropriate code for errors
2. NEVER return generic "unexpected error" without logging details

**Validation Commands**:
```bash
# Test successful chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Assalamualaikum",
    "user_id": null
  }' | jq

# Expected (200):
# {
#   "success": true,
#   "message": "Wa alaikum assalam! How can I help you?",
#   "error": null,
#   "error_message": null,
#   "tool_used": null,
#   "data": null,
#   "request_id": "<uuid>"
# }

# Test auth required
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
#   "error_message": "Please log in to perform this action. You need to be signed in to create or manage tasks.",
#   "request_id": "<uuid>"
# }

# Test with task creation (authenticated)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a task for Fajr prayer",
    "user_id": 1
  }' | jq

# Expected (200):
# {
#   "success": true,
#   "message": "✅ Task created successfully!\n\nTitle: Fajr prayer\nPriority: medium\nLinked Prayer: Fajr",
#   "error": null,
#   "tool_used": "create_task",
#   "data": {"task": {...}},
#   "request_id": "<uuid>"
# }

# Verify error logging
# Cause an error (set invalid API key)
# Make request and check logs
tail -f logs/chatbot_errors.log

# Expected to see:
# - Full stack trace
# - Error type classification
# - Request ID
# - NOT "unexpected error"
```

**Expected Behavior After Completion**:
- ✅ Successful requests return assistant message
- ✅ Auth errors return 401 with clear message
- ✅ Gemini errors return 500 with specific error types
- ✅ All errors logged with full context
- ✅ Request ID in every response
- ✅ NO generic "unexpected error" messages
- ✅ User-friendly error messages

---

### C3: Update Agent to Propagate Exceptions

**Priority**: HIGH
**Files**:
- `backend/chatbot/agent/agent.py` (MODIFY)

**Requirements**:
1. Update `run_agent()` function to:
   - Use `GeminiClient` instead of direct API calls
   - Let exceptions propagate (don't catch and return generic error)
   - Remove any code that catches all exceptions with generic message
   - Only catch specific, expected exceptions for business logic
2. Update intent detection to return structured result
3. Update parameter extraction to use intent result

**Validation Commands**:
```bash
# Test that agent lets exceptions propagate
python -c "
from chatbot.agent.agent import run_agent, initialize_agent
from chatbot.gemini.client import GeminiAuthError
import os

# Set invalid key
os.environ['GEMINI_API_KEY'] = 'AIzaInvalid'

try:
    agent = initialize_agent()
    result = run_agent(agent, user_id=1, user_message='Hello')
except GeminiAuthError as e:
    print(f'✅ Exception propagated: {type(e).__name__}')
except Exception as e:
    print(f'❌ Wrong exception type: {type(e).__name__}')
"

# Test successful flow
python -c "
from chatbot.agent.agent import run_agent, initialize_agent

agent = initialize_agent()
result = run_agent(
    agent,
    user_id=1,
    user_message='Hello',
    conversation_history=None
)
print(f'Result type: {type(result)}')
print(f'Has message: {\"message\" in result if isinstance(result, dict) else hasattr(result, \"message\")}')
"
```

**Expected Behavior After Completion**:
- ✅ Agent uses new GeminiClient
- ✅ Exceptions propagate to endpoint
- ✅ No generic error catching in agent
- ✅ Business logic still handles expected cases
- ✅ Endpoint handles all errors appropriately

---

## D) Frontend Error Handling

### D1: Create Chat API Client Module

**Priority**: HIGH
**Files**:
- `frontend/lib/chatApi.ts` (CREATE)

**Requirements**:
1. Create TypeScript interfaces:
   ```typescript
   export interface ChatMessage {
     role: 'user' | 'assistant';
     content: string;
     timestamp: Date;
     isError?: boolean;
   }

   export interface ChatRequest {
     message: string;
     userId?: number;
     conversationHistory?: ChatMessage[];
     language?: string;
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

   export type ErrorType =
     | 'authentication_required'
     | 'authentication_failed'
     | 'quota_exceeded'
     | 'network_error'
     | 'tool_execution_failed'
     | 'internal_error'
     | 'unknown';
   ```
2. Create `sendChatMessage()` async function:
   - Accept ChatRequest and optional auth token
   - Call `/api/v1/chat` endpoint
   - Handle HTTP errors
   - Return ChatResponse
   - Throw on network errors

**Validation Commands**:
```bash
cd frontend

# Type check
npm run type-check

# Expected: No errors in chatApi.ts

# Build check
npm run build

# Expected: Builds successfully
```

**Expected Behavior After Completion**:
- ✅ Type-safe API client
- ✅ Reusable across components
- ✅ Proper error handling
- ✅ TypeScript compilation passes

---

### D2: Update Chat Page with Error States

**Priority**: HIGH
**Files**:
- `frontend/app/chat/page.tsx` (MODIFY)

**Requirements**:
1. Add error state:
   ```typescript
   interface ErrorState {
     type: ErrorType;
     message: string;
     requestId?: string;
   }
   const [error, setError] = useState<ErrorState | null>(null);
   ```
2. Add loading state:
   ```typescript
   const [isLoading, setIsLoading] = useState(false);
   ```
3. Update message sending logic to:
   - Set loading=true before request
   - Clear error before request
   - Add user message to UI immediately
   - Call `sendChatMessage()` from API client
   - On success: Add assistant message to UI
   - On error: Set error state with type and message
   - Always: Set loading=false
4. Handle all error types with try/catch
5. Display errors using Alert components (import from shadcn/ui)

**Validation Commands**:
```bash
cd frontend

# Type check
npm run type-check

# Build
npm run build

# Start dev server
npm run dev

# Manual testing:
# 1. Open http://localhost:3000/chat
# 2. Type "Hello" and send
#    Expected: Loading indicator → Response appears
#
# 3. Sign out, type "Create task", send
#    Expected: Warning alert about sign in required
#
# 4. Stop backend, type anything, send
#    Expected: Error alert about connection issue
```

**Expected Behavior After Completion**:
- ✅ Loading state shows during request
- ✅ Errors display in Alert component
- ✅ Different error types styled differently
- ✅ No unhandled promise rejections
- ✅ User-friendly error messages

---

### D3: Add Error Display Components

**Priority**: HIGH
**Files**:
- `frontend/app/chat/page.tsx` (MODIFY)

**Requirements**:
1. Create error display sections for each error type:
   - `authentication_required`: Warning alert with sign-in link
   - `network_error`: Error alert with connectivity message
   - `authentication_failed`: Error alert with support message
   - `quota_exceeded`: Warning alert with retry message
   - `internal_error`: Error alert with apology and reference ID
2. Use appropriate icons (Lock, AlertCircle, WifiOff, etc.)
3. Add retry/dismiss buttons where appropriate
4. Show error messages in chat history as error bubbles

**Validation Commands**:
```bash
# Start dev server
cd frontend
npm run dev

# Test each error type manually:

# 1. Auth required
#    - Sign out
#    - Type "Create task"
#    - Expected: Yellow warning box with "Sign In Required" + link

# 2. Network error
#    - Stop backend
#    - Type "Hello"
#    - Expected: Red error box with "Connection Issue"

# 3. Service error
#    - Set invalid Gemini key in backend
#    - Restart backend
#    - Type "Hello"
#    - Expected: Red error box with "Service Configuration Issue"

# Check console
# - No unhandled errors
# - No undefined/null errors
```

**Expected Behavior After Completion**:
- ✅ Each error type has distinct display
- ✅ Errors visually different from normal messages
- ✅ Auth errors include sign-in link
- ✅ Network errors include helpful guidance
- ✅ All errors show request ID for support
- ✅ No console errors

---

### D4: Add Input Validation and Disable States

**Priority**: MEDIUM
**Files**:
- `frontend/app/chat/page.tsx` (MODIFY)

**Requirements**:
1. Disable send button and input when:
   - Loading is true
   - Message is empty
   - Previous request failed with network error (until retry)
2. Re-enable after request completes
3. Add visual feedback:
   - Loading spinner on button
   - Disabled styling on input
4. Validate message:
   - Min length: 1 character
   - Max length: 2000 characters
   - Show character count near max

**Validation Commands**:
```bash
# Manual testing:
# 1. Type message and send
#    - Button shows spinner
#    - Input disabled during request
#    - Button re-enabled after response
#
# 2. Clear input
#    - Button disabled (no spinner)
#
# 3. Type 1950+ characters
#    - Character count appears
#    - Turns red near 2000
#    - Blocks sending at 2000
```

**Expected Behavior After Completion**:
- ✅ Can't send empty messages
- ✅ Can't send during loading
- ✅ Clear visual feedback
- ✅ Character limit enforced
- ✅ Better UX

---

## E) Integration Tests

### E1: Create Chat Integration Test Script

**Priority**: HIGH
**Files**:
- `backend/tests/test_chat_integration.py` (CREATE)

**Requirements**:
1. Create Python test script with three test functions:
   - `test_health_check()`:
     - GET /api/v1/chat/health
     - Assert status 200
     - Assert status="healthy"
     - Print success message
   - `test_simple_chat()`:
     - POST /api/v1/chat with "Assalamualaikum"
     - Assert status 200
     - Assert success=true
     - Assert message is non-empty
     - Assert no error field
     - Print response preview
   - `test_authenticated_operation()`:
     - POST /api/v1/chat with "Create a task" (no user_id)
     - Assert status 401
     - Assert error="authentication_required"
     - Assert error_message is helpful
     - Print success message
2. Create `main()` function that:
   - Runs all tests
   - Prints summary
   - Exits with code 0 if all pass, 1 if any fail
3. Add to file docstring:
   - How to run: `python tests/test_chat_integration.py`
   - Prerequisites: Backend server must be running

**Validation Commands**:
```bash
cd backend

# Ensure server is running
uvicorn main:app --host 0.0.0.0 --port 8000 &
sleep 5

# Run tests
python tests/test_chat_integration.py

# Expected output:
# ============================================================
# SalaatFlow Chat Integration Tests
# ============================================================
# Testing health check...
# ✅ Health check passed
#
# Testing simple chat...
# ✅ Chat response received: Wa alaikum assalam! How can...
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

# Check exit code
echo $?
# Expected: 0

# Test failure scenario (stop server)
pkill -f uvicorn
python tests/test_chat_integration.py

# Expected:
# ❌ Some tests failed
# Exit code: 1
```

**Expected Behavior After Completion**:
- ✅ Test script runs independently
- ✅ All three tests pass with running backend
- ✅ Clear pass/fail output
- ✅ Exit code indicates success/failure
- ✅ Can be run in CI/CD

---

### E2: Create Diagnostic Script

**Priority**: MEDIUM
**Files**:
- `backend/scripts/diagnose.py` (CREATE)

**Requirements**:
1. Create script that checks:
   - Environment variables:
     - GEMINI_API_KEY set and valid format
     - DATABASE_URL set
     - GEMINI_MODEL set
   - Python dependencies:
     - fastapi, google-generativeai, sqlmodel, etc.
     - Print installed/missing
   - Server status:
     - Check if port 8000 is listening
     - Check if /docs endpoint accessible
   - Gemini API:
     - Call /api/v1/chat/health
     - Print healthy/unhealthy
   - Database:
     - Try connection
     - Run simple query
   - Log files:
     - Check if logs/ directory exists
     - Check if log files present
2. Use colored output:
   - Green ✅ for passed checks
   - Red ❌ for failed checks
   - Yellow ⚠️ for warnings
3. Print summary at end

**Validation Commands**:
```bash
cd backend

# Run diagnostics
python scripts/diagnose.py

# Expected output:
# ============================================================
# 🔍 SalaatFlow System Diagnostics
# ============================================================
#
# 📋 Environment Configuration
# ============================================================
# ✅ GEMINI_API_KEY set
#    Value: AIzaSyBa-hcy0emMTYAwu...
# ✅ DATABASE_URL set
# ✅ GEMINI_MODEL set
#    Value: gemini-pro
#
# 📦 Dependencies
# ============================================================
# ✅ fastapi installed
# ✅ google-generativeai installed
# ✅ sqlmodel installed
# ...
#
# 🌐 Server Status
# ============================================================
# ✅ Server running on port 8000
#
# 🤖 Gemini API Status
# ============================================================
# ✅ Gemini API reachable
#    Model: gemini-pro
#
# 🗄️  Database Status
# ============================================================
# ✅ Database connection
#
# 📝 Log Files
# ============================================================
# ✅ Log directory exists
# ✅ chatbot.log exists
#    Size: 1.23 MB
# ✅ chatbot_errors.log exists
#
# ============================================================
# Diagnostic scan complete!
# All checks passed!
# ============================================================

# Test with issues (stop server)
pkill -f uvicorn
python scripts/diagnose.py

# Expected:
# ❌ Server running on port 8000
#    Server not reachable...
```

**Expected Behavior After Completion**:
- ✅ Quick health check of entire system
- ✅ Clear visual output
- ✅ Identifies configuration issues
- ✅ Helps debug problems
- ✅ Useful during development

---

## F) Build & Lint Tasks

### F1: Fix Frontend Linting Issues

**Priority**: HIGH
**Files**:
- Various frontend files (as identified by linter)

**Requirements**:
1. Run `npm run lint` to identify issues
2. Fix issues via AI-generated changes:
   - Remove unused imports
   - Fix missing dependencies in useEffect
   - Fix TypeScript type errors
   - Fix ESLint rule violations
3. Run `npm run lint` again until it passes
4. Document any intentional rule exceptions

**Validation Commands**:
```bash
cd frontend

# Check current state
npm run lint 2>&1 | tee lint_before.txt

# After fixes
npm run lint

# Expected:
# ✓ No ESLint warnings or errors
# Exit code: 0

# Count issues fixed
wc -l lint_before.txt
# Should see reduction to 0
```

**Expected Behavior After Completion**:
- ✅ `npm run lint` exits with code 0
- ✅ No ESLint errors
- ✅ No ESLint warnings
- ✅ Code follows project style guide

---

### F2: Fix Frontend TypeScript Errors

**Priority**: HIGH
**Files**:
- Various frontend files (as identified by type checker)

**Requirements**:
1. Run `npm run type-check` to identify errors
2. Fix type errors via AI-generated changes:
   - Add missing type annotations
   - Fix type mismatches
   - Add proper interfaces
   - Handle undefined/null properly
3. Run `npm run type-check` again until it passes

**Validation Commands**:
```bash
cd frontend

# Check current state
npm run type-check 2>&1 | tee typecheck_before.txt

# After fixes
npm run type-check

# Expected:
# ✓ No TypeScript errors
# Exit code: 0

# Count errors fixed
grep "error TS" typecheck_before.txt | wc -l
# Should be 0 after fixes
```

**Expected Behavior After Completion**:
- ✅ `npm run type-check` exits with code 0
- ✅ No TypeScript errors
- ✅ All types properly defined
- ✅ Type safety enforced

---

### F3: Fix Frontend Build Issues

**Priority**: CRITICAL
**Files**:
- Various frontend files (as identified by build)

**Requirements**:
1. Run `npm run build` to identify issues
2. Fix build errors via AI-generated changes:
   - Missing dependencies
   - Import path errors
   - Environment variable issues
   - Next.js configuration issues
3. Run `npm run build` again until it succeeds
4. Verify build output is production-ready

**Validation Commands**:
```bash
cd frontend

# Clean build
rm -rf .next

# Build
npm run build

# Expected output (end):
# ✓ Compiled successfully
# ✓ Linting and checking validity of types
# ✓ Collecting page data
# ✓ Generating static pages
# ✓ Finalizing page optimization
#
# Route (app)                              Size     First Load JS
# ┌ ○ /                                    ...
# ├ ○ /chat                                ...
# ...
# ○  (Static)  prerendered as static content
#
# Exit code: 0

# Verify build directory
ls -la .next/
# Should contain: server, static, BUILD_ID, etc.

# Test production build
npm run start &
sleep 5
curl http://localhost:3000
# Should return HTML
```

**Expected Behavior After Completion**:
- ✅ `npm run build` succeeds
- ✅ All pages compile
- ✅ No build errors or warnings
- ✅ Production build works
- ✅ All routes accessible

---

### F4: Fix Backend Import and Startup Issues

**Priority**: CRITICAL
**Files**:
- Various backend files (as identified by startup)

**Requirements**:
1. Attempt to start backend: `uvicorn main:app`
2. Fix startup errors via AI-generated changes:
   - Missing imports
   - Module not found errors
   - Configuration errors
   - Missing __init__.py files
   - Circular import issues
3. Start backend again until it runs without errors
4. Verify all endpoints accessible

**Validation Commands**:
```bash
cd backend
source venv/bin/activate

# Try starting
uvicorn main:app --host 0.0.0.0 --port 8000

# Expected output:
# ✅ Logging configured successfully
# ✅ Gemini configured: model=gemini-pro
# 🚀 Starting SalaatFlow API...
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.

# Verify imports work
python -c "
from main import app
from routers.chatbot import router
from chatbot.gemini.client import GeminiClient
from chatbot.config.logging_config import setup_logging
print('✅ All imports successful')
"

# Check endpoints
curl http://localhost:8000/docs
# Should return OpenAPI documentation

curl http://localhost:8000/api/v1/chat/health
# Should return health status

# Check no errors in logs
tail -20 logs/chatbot.log
# Should not see any ERROR level logs from startup
```

**Expected Behavior After Completion**:
- ✅ Backend starts without errors
- ✅ All imports resolve correctly
- ✅ All modules load successfully
- ✅ Configuration validates on startup
- ✅ All endpoints accessible
- ✅ OpenAPI docs work

---

## G) Documentation Updates

### G1: Update Phase 3 Specification

**Priority**: MEDIUM
**Files**:
- `docs/phase3_spec.md` (MODIFY)

**Requirements**:
1. Add sections:
   - Error Handling Strategy (reference error types)
   - Health Check Endpoint documentation
   - Logging Requirements
   - Request ID Tracking
2. Update endpoint specifications with:
   - New response formats
   - Error codes and meanings
   - Example requests/responses
3. Add troubleshooting section

**Validation Commands**:
```bash
# Check file exists and is readable
cat docs/phase3_spec.md | head -50

# Verify sections present
grep -i "error handling" docs/phase3_spec.md
grep -i "health check" docs/phase3_spec.md
grep -i "logging" docs/phase3_spec.md

# Check for broken links
# (manual review)
```

**Expected Behavior After Completion**:
- ✅ Specification reflects current implementation
- ✅ Error handling documented
- ✅ Health check documented
- ✅ Examples provided
- ✅ Clear and accurate

---

### G2: Create Build & Test Guide

**Priority**: HIGH
**Files**:
- `docs/phase3_build_and_test.md` (CREATE)

**Requirements**:
1. Create comprehensive guide with sections:
   - Prerequisites (Node.js, Python, API keys)
   - Environment Setup (step-by-step)
   - Build Commands (frontend & backend)
   - Testing Procedures (integration tests, manual testing)
   - Troubleshooting (common issues and fixes)
   - Success Indicators (what "working" looks like)
2. Include exact commands to copy/paste
3. Include expected output for each command
4. Include troubleshooting for common failures

**Validation Commands**:
```bash
# Verify file exists
ls -lh docs/phase3_build_and_test.md

# Check completeness
grep -c "```bash" docs/phase3_build_and_test.md
# Should have multiple code blocks

# Verify sections present
grep "## " docs/phase3_build_and_test.md

# Expected:
# ## Prerequisites
# ## Environment Setup
# ## Build Commands
# ## Testing Procedures
# ## Troubleshooting
# ## Success Indicators

# Test commands work by following guide
# (manual verification)
```

**Expected Behavior After Completion**:
- ✅ Complete step-by-step guide
- ✅ All commands included
- ✅ Expected outputs documented
- ✅ Troubleshooting covered
- ✅ Easy to follow
- ✅ Accurate and tested

---

### G3: Update Main README

**Priority**: HIGH
**Files**:
- `README.md` (MODIFY)

**Requirements**:
1. Add "Phase III: AI Chatbot" section with:
   - Feature overview
   - Quick start commands
   - Basic usage examples
   - Build & test commands
   - Troubleshooting quick reference
   - Links to detailed docs
2. Update table of contents
3. Add troubleshooting commands:
   - Health check
   - View logs
   - Run diagnostics

**Validation Commands**:
```bash
# Verify section added
grep -A 20 "Phase III" README.md

# Check commands are valid
# Extract commands and test them
grep "```bash" README.md -A 5 | grep -E "^(cd|npm|python|curl)"

# Verify links work
grep "\[.*\](.*\.md)" README.md
# (manually verify each link)

# Check formatting
# (open in Markdown viewer)
```

**Expected Behavior After Completion**:
- ✅ README has Phase III section
- ✅ Quick start works
- ✅ All commands tested
- ✅ Links work
- ✅ Helpful for new users

---

### G4: Create .env.example File

**Priority**: MEDIUM
**Files**:
- `backend/.env.example` (CREATE)

**Requirements**:
1. Create template with all required variables:
   - DATABASE_URL (with example format)
   - GEMINI_API_KEY (with placeholder and link to get key)
   - GEMINI_MODEL (with default)
   - GEMINI_TIMEOUT, GEMINI_MAX_RETRIES
   - Server settings (HOST, PORT, ENVIRONMENT)
   - CORS_ORIGINS
2. Add comments explaining:
   - What each variable is for
   - Where to get API keys
   - Example values
   - Which are optional vs required

**Validation Commands**:
```bash
# Verify file exists
ls -lh backend/.env.example

# Check has all required variables
grep "GEMINI_API_KEY" backend/.env.example
grep "DATABASE_URL" backend/.env.example

# Verify has helpful comments
grep "#" backend/.env.example | wc -l
# Should have multiple comment lines

# Test that .env can be created from example
cd backend
cp .env.example .env
# Edit .env with real values
# Try loading config
python -c "
from chatbot.gemini.config import GeminiConfig
config = GeminiConfig.from_env()
print('✅ Config loads from .env')
"
```

**Expected Behavior After Completion**:
- ✅ Template exists
- ✅ All variables documented
- ✅ Helpful comments included
- ✅ Links to get credentials
- ✅ Easy for new users to set up

---

## Summary and Success Criteria

### Task Completion Checklist

After ALL tasks complete, verify:

**A) Logging & Diagnostics**
- [ ] A1: Logging configuration created and working
- [ ] A2: Request ID tracking in all requests
- [ ] A3: Chat endpoint logs all requests/responses
- [ ] A4: Gemini calls logged with errors
- [ ] A5: Tool executions logged
- [ ] A6: Log viewer script works

**B) Gemini Config & Health-Check**
- [ ] B1: Gemini configuration validates properly
- [ ] B2: Gemini client handles all error types
- [ ] B3: Health check endpoint returns status

**C) Chat Endpoint Behavior**
- [ ] C1: Response models defined and validated
- [ ] C2: Chat endpoint returns structured responses
- [ ] C3: Agent propagates exceptions properly

**D) Frontend Error Handling**
- [ ] D1: Chat API client created
- [ ] D2: Error states added to chat page
- [ ] D3: Error displays for all error types
- [ ] D4: Input validation and disable states

**E) Integration Tests**
- [ ] E1: Integration test script passes
- [ ] E2: Diagnostic script shows all green

**F) Build & Lint**
- [ ] F1: `npm run lint` passes
- [ ] F2: `npm run type-check` passes
- [ ] F3: `npm run build` succeeds
- [ ] F4: Backend starts without errors

**G) Documentation**
- [ ] G1: Phase 3 spec updated
- [ ] G2: Build & test guide created
- [ ] G3: README updated
- [ ] G4: .env.example created

### Final Acceptance Tests

Run these to confirm Phase III is fixed:

```bash
# 1. Clean build test
cd frontend && rm -rf .next && npm run build
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000

# 2. Integration tests pass
cd backend && python tests/test_chat_integration.py
# Expected: ✅ All tests passed!

# 3. Health check works
curl http://localhost:8000/api/v1/chat/health
# Expected: {"status": "healthy", ...}

# 4. Simple chat works
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Assalamualaikum", "user_id": null}'
# Expected: {"success": true, "message": "Wa alaikum assalam...", ...}

# 5. Auth errors clear
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Create task", "user_id": null}'
# Expected: {"success": false, "error": "authentication_required", ...}

# 6. Logs contain details
python backend/scripts/view_logs.py --tail 20
# Expected: See request IDs, no secrets, detailed errors

# 7. Diagnostics pass
python backend/scripts/diagnose.py
# Expected: All checks green
```

### Success Metrics

Phase III is considered **FIXED AND STABLE** when:

✅ **Functional**
- Simple chat returns valid response (not error) 95%+ of the time
- Auth errors return 401 with clear, actionable message
- All error types have specific messages (no "unexpected error")
- Health check returns accurate status

✅ **Build**
- `npm run lint` exits 0
- `npm run build` completes successfully
- Backend starts without import/config errors
- All integration tests pass

✅ **Observability**
- All requests logged with request_id
- All errors logged with stack trace
- No secrets in log files
- Can debug issues from logs alone

✅ **Documentation**
- Build guide accurate and complete
- All commands work as documented
- Troubleshooting guide helpful

---

**Total Tasks**: 28
**Estimated Time**: 8-10 hours
**Ready for**: `/sp.implement <task-id>` execution

---

**END OF TASK LIST**
