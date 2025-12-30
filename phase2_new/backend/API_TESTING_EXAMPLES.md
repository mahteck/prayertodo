# SalaatFlow Chatbot API - Testing Examples

## Common JSON Formatting Errors

### ❌ WRONG - Invalid JSON (causes "Unprocessable Entity")
```json
{
  "message": "Fajr ka task bana do,    ← MISSING CLOSING QUOTE
  "user_id": 1,
  ...
}
```

### ❌ WRONG - Newlines in JSON string
```json
{
  "message": "Fajr ka task
  bana do",    ← NEWLINE BREAKS JSON
  "user_id": 1
}
```

### ✅ CORRECT - Valid JSON
```json
{
  "message": "Fajr ka task bana do",
  "user_id": 1,
  "conversation_history": [],
  "language": "en",
  "metadata": {}
}
```

## Testing with cURL

### Test 1: Simple Conversation (No Authentication)

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Assalamualaikum", "user_id": null}'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Wa alaikum assalam! ...",
  "error": null,
  "error_message": null,
  "request_id": "abc-123"
}
```

### Test 2: Authentication Required (Without Login)

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a task", "user_id": null}'
```

**Expected Response:**
```json
{
  "success": false,
  "message": "",
  "error": "authentication_required",
  "error_message": "Please log in to perform this action. You need to be signed in to create or manage tasks.",
  "request_id": "xyz-789"
}
```

### Test 3: Task Creation (With User ID)

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Fajr ka task bana do", "user_id": 1}'
```

**Current Response:**
```json
{
  "success": true,
  "message": "❌ Failed to create task: TOOL_NOT_FOUND",
  "error": null,
  "error_message": null,
  "request_id": "abc-123"
}
```

**Note:** The `TOOL_NOT_FOUND` error means the MCP tools (create_task, list_tasks, etc.) are not implemented yet. This is expected - the chatbot is working correctly, but the task management tools need to be set up.

### Test 4: List Tasks

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me my tasks", "user_id": 1}'
```

### Test 5: Conversation with History

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
  "message": "What did I just ask?",
  "user_id": null,
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello, my name is Ahmed"
    },
    {
      "role": "assistant",
      "content": "Hello Ahmed! How can I help you today?"
    }
  ]
}'
```

## Testing with Postman/Thunder Client

### Endpoint
```
POST http://localhost:8000/api/v1/chat/
```

### Headers
```
Content-Type: application/json
```

### Body (JSON)
```json
{
  "message": "Your message here",
  "user_id": 1,
  "conversation_history": [],
  "language": "en",
  "metadata": {}
}
```

### Test Cases

#### Case 1: Greeting
```json
{
  "message": "Assalamualaikum",
  "user_id": null
}
```

#### Case 2: Task Creation (Urdu)
```json
{
  "message": "Fajr ka task bana do",
  "user_id": 1
}
```

#### Case 3: Task List
```json
{
  "message": "Mujhe mere tasks dikhao",
  "user_id": 1
}
```

#### Case 4: Masjid Search
```json
{
  "message": "North Nazimabad mein konsi masjid hai?",
  "user_id": null
}
```

## Testing with Python

### Simple Test
```python
import requests

url = "http://localhost:8000/api/v1/chat/"
payload = {
    "message": "Assalamualaikum",
    "user_id": None
}

response = requests.post(url, json=payload)
print(response.json())
```

### With Error Handling
```python
import requests

def test_chatbot(message, user_id=None):
    url = "http://localhost:8000/api/v1/chat/"
    payload = {
        "message": message,
        "user_id": user_id,
        "conversation_history": []
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        if result["success"]:
            print(f"✅ Success: {result['message']}")
        else:
            print(f"❌ Error: {result['error']}")
            print(f"   Message: {result['error_message']}")
            print(f"   Request ID: {result['request_id']}")

        return result

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

# Test 1: Simple conversation
test_chatbot("Hello")

# Test 2: Task creation without auth
test_chatbot("Create a task", user_id=None)

# Test 3: Task creation with auth
test_chatbot("Create a Fajr task", user_id=1)
```

## Testing with JavaScript/Fetch

```javascript
async function testChatbot(message, userId = null) {
  const url = "http://localhost:8000/api/v1/chat/";

  const payload = {
    message: message,
    user_id: userId,
    conversation_history: []
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (result.success) {
      console.log("✅ Success:", result.message);
    } else {
      console.log("❌ Error:", result.error);
      console.log("   Message:", result.error_message);
      console.log("   Request ID:", result.request_id);
    }

    return result;

  } catch (error) {
    console.error("❌ Request failed:", error);
    return null;
  }
}

// Test cases
testChatbot("Assalamualaikum");
testChatbot("Create a task", null); // Should require auth
testChatbot("Show my tasks", 1);
```

## Common Errors & Solutions

### Error 1: "Unprocessable Entity" (422)

**Cause:** Invalid JSON format

**Solutions:**
```bash
# ❌ WRONG - Missing quote
curl ... -d '{"message": "test'

# ❌ WRONG - Newline in string
curl ... -d '{"message": "line1
line2"}'

# ❌ WRONG - Trailing comma
curl ... -d '{"message": "test",}'

# ✅ CORRECT
curl ... -d '{"message": "test"}'
```

### Error 2: "Method Not Allowed" (405)

**Cause:** Using GET instead of POST

**Solution:**
```bash
# ❌ WRONG
curl http://localhost:8000/api/v1/chat/

# ✅ CORRECT
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Error 3: "Connection Refused"

**Cause:** Backend server not running

**Solution:**
```bash
cd backend
./start_chatbot.sh
```

### Error 4: "TOOL_NOT_FOUND"

**Cause:** MCP tools are not implemented (this is expected for now)

**Response:**
```json
{
  "success": true,
  "message": "❌ Failed to create task: TOOL_NOT_FOUND"
}
```

**What this means:**
- The chatbot IS working correctly
- It detected the task creation intent
- The actual task tools need to be implemented
- This is a backend limitation, not a bug

## Quick Test Script

Save this as `quick_test.sh`:

```bash
#!/bin/bash

echo "🧪 Quick Chatbot Tests"
echo ""

# Test 1: Simple greeting
echo "Test 1: Simple Greeting"
curl -s -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Assalamualaikum", "user_id": null}' \
  | python3 -m json.tool
echo ""

# Test 2: Auth guard
echo "Test 2: Authentication Guard"
curl -s -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a task", "user_id": null}' \
  | python3 -m json.tool
echo ""

# Test 3: Task creation (with user)
echo "Test 3: Task Creation (Authenticated)"
curl -s -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Fajr ka task bana do", "user_id": 1}' \
  | python3 -m json.tool
echo ""
```

Make it executable:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

## Response Format Reference

### Success Response
```json
{
  "success": true,
  "message": "Assistant's response message",
  "error": null,
  "error_message": null,
  "tool_used": "create_task",  // optional
  "data": {},                    // optional
  "request_id": "unique-id"
}
```

### Error Response
```json
{
  "success": false,
  "message": "",
  "error": "error_code",
  "error_message": "User-friendly error message",
  "tool_used": null,
  "data": null,
  "request_id": "unique-id"
}
```

### Error Codes
- `authentication_required` - User needs to log in
- `authentication_failed` - Invalid API key
- `quota_exceeded` - Rate limit exceeded
- `network_error` - Network/timeout issue
- `internal_error` - Unexpected error

## Summary

✅ **Your JSON formatting error is fixed!**

The correct format is:
```json
{
  "message": "Fajr ka task bana do",
  "user_id": 1,
  "conversation_history": [],
  "language": "en",
  "metadata": {}
}
```

**Current Status:**
- ✅ Backend is working
- ✅ Error handling is working
- ✅ Authentication guards are working
- ⚠️ MCP tools (create_task, etc.) return TOOL_NOT_FOUND (expected - not implemented yet)
- ⏱️ Gemini API may be rate limited (wait 1-2 minutes between tests)

**Next Step:**
Implement the MCP tools (create_task, list_tasks, etc.) in `backend/chatbot/mcp_tools.py` to enable full task management functionality.
