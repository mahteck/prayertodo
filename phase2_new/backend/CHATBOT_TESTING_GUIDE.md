# SalaatFlow Chatbot Testing Guide

## Overview

The chatbot has been successfully integrated with Phase III stabilization features:
- ✅ Robust error handling with specific error types
- ✅ Request tracking with unique IDs
- ✅ Secret filtering in logs
- ✅ Bilingual error messages (English & Urdu)
- ✅ Health check endpoints

## Prerequisites

1. **Gemini API Key**: You need a valid Google Gemini API key
   - Get one FREE from: https://aistudio.google.com/app/apikey
   - Set in `.env` file: `GEMINI_API_KEY=your-key-here`

2. **Python Environment**: Python 3.12 with venv activated

3. **Database**: PostgreSQL (Neon) database configured in `.env`

## Starting the Chatbot Backend

### Method 1: Using the start script (Recommended)

```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend

# Activate virtual environment
source venv/bin/activate

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Method 2: Background mode

```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend
source venv/bin/activate
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
```

### Verify Server is Running

Check if the server started successfully:

```bash
curl http://localhost:8000/api/v1/chat/health
```

Expected output (if healthy):
```json
{
  "service": "gemini",
  "status": "healthy",
  "model": "gemini-2.0-flash",
  "timestamp": 1767083769.4124753,
  "response_length": 123
}
```

If quota exceeded (rate limit):
```json
{
  "service": "gemini",
  "status": "unhealthy",
  "error": "quota_exceeded",
  "message": "Gemini API quota exceeded...",
  "timestamp": 1767083769.4124753
}
```

## Testing the Chatbot

### 1. Health Check

```bash
curl http://localhost:8000/api/v1/chat/health
```

### 2. Simple Conversation (No Auth Required)

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Assalamualaikum, what can you do?",
    "user_id": null,
    "conversation_history": []
  }'
```

Expected response:
```json
{
  "success": true,
  "message": "Wa alaikum assalam! I can help you with...",
  "error": null,
  "error_message": null,
  "tool_used": null,
  "data": null,
  "request_id": "abc-123-def"
}
```

### 3. Test Authentication Guard (Task Creation Without Login)

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Fajr task for me",
    "user_id": null
  }'
```

Expected response:
```json
{
  "success": false,
  "message": "",
  "error": "authentication_required",
  "error_message": "Please log in to perform this action. You need to be signed in to create or manage tasks.",
  "request_id": "xyz-789"
}
```

### 4. Test with User ID (Authenticated)

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me my tasks",
    "user_id": 1,
    "conversation_history": []
  }'
```

### 5. Test Error Handling

The chatbot now returns specific errors:

**Quota Exceeded** (if you hit rate limits):
```json
{
  "success": false,
  "error": "quota_exceeded",
  "error_message": "The chatbot is experiencing high demand right now. Please try again in a few moments."
}
```

**Network Error**:
```json
{
  "success": false,
  "error": "network_error",
  "error_message": "Unable to connect to the chatbot service. Please check your internet connection and try again."
}
```

**Authentication Failed** (invalid API key):
```json
{
  "success": false,
  "error": "authentication_failed",
  "error_message": "The chatbot service is temporarily unavailable due to a configuration issue. Please contact support with reference ID: abc-123"
}
```

## Frontend Integration

### Start the Frontend

```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/frontend
npm run dev
```

The frontend should be available at: `http://localhost:3000`

### Chat Page

Navigate to: `http://localhost:3000/chat`

The chat interface will:
1. Connect to backend at `http://localhost:8000/api/v1/chat/`
2. Show loading states during requests
3. Display error messages from the backend
4. Track conversation history

## Checking Logs

The chatbot creates detailed logs with secret filtering:

### Main Log (All activity)
```bash
cat logs/chatbot.log
```

### Error Log (Errors only)
```bash
cat logs/chatbot_errors.log
```

### Live Monitoring
```bash
tail -f logs/chatbot.log
```

## Common Issues & Solutions

### Issue 1: "Quota Exceeded" Error

**Cause**: You've hit the Gemini API free tier rate limit (15 requests per minute, or 1500 per day)

**Solution**:
- Wait a few minutes and try again
- The free tier resets every minute for RPM limits
- Consider upgrading to Gemini API paid tier if needed

### Issue 2: "Backend is not running"

**Cause**: The FastAPI server is not running or crashed

**Solution**:
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Issue 3: "Authentication Failed"

**Cause**: Invalid or missing Gemini API key

**Solution**:
1. Check `.env` file has `GEMINI_API_KEY=AIza...`
2. Verify the key is valid at https://aistudio.google.com/app/apikey
3. Make sure the key starts with "AIza"
4. Restart the backend server after updating `.env`

### Issue 4: Server won't start - "Address already in use"

**Cause**: Another process is using port 8000

**Solution**:
```bash
# Find the process
lsof -i :8000

# Kill it (use PID from above)
kill -9 <PID>

# Or use a different port
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## API Endpoints Reference

### Chat Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat/` | POST | Send a message to the chatbot |
| `/api/v1/chat/health` | GET | Check chatbot service health |

### Request Format

```json
{
  "message": "string (required, 1-2000 chars)",
  "user_id": "int or null (required for task operations)",
  "conversation_history": [
    {
      "role": "user",
      "content": "previous message"
    },
    {
      "role": "assistant",
      "content": "previous response"
    }
  ],
  "language": "en or ur (optional, auto-detected)",
  "metadata": {}
}
```

### Response Format

```json
{
  "success": true/false,
  "message": "Assistant's response (if success)",
  "error": "error_code (if failed)",
  "error_message": "User-friendly error message (if failed)",
  "tool_used": "name of tool used (if any)",
  "data": {},
  "request_id": "unique-request-id"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `authentication_required` | 401 | User needs to log in for this action |
| `authentication_failed` | 500 | Gemini API key is invalid |
| `quota_exceeded` | 500 | Gemini API quota/rate limit exceeded |
| `network_error` | 500 | Network/timeout issue with Gemini |
| `internal_error` | 500 | Other unexpected errors |

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] Health check endpoint returns valid response
- [ ] Simple conversation works (non-authenticated)
- [ ] Authentication guard blocks task operations without user_id
- [ ] Error messages are user-friendly and specific
- [ ] Request IDs are generated for tracking
- [ ] Logs are created in `logs/` directory
- [ ] API keys are redacted from logs
- [ ] Frontend can connect to backend
- [ ] Chat UI displays messages correctly
- [ ] Error states show in UI

## Performance Notes

### Gemini API Free Tier Limits

- **RPM (Requests Per Minute)**: 15
- **RPD (Requests Per Day)**: 1500
- **TPM (Tokens Per Minute)**: 1,000,000

If you exceed these limits, you'll get a `quota_exceeded` error. The chatbot handles this gracefully and shows a user-friendly message.

### Rate Limit Recovery

- RPM limits reset after 1 minute
- RPD limits reset at midnight UTC
- No permanent blocking for free tier

## Next Steps

1. **Test with real users**: Have users interact with the chatbot
2. **Monitor logs**: Check `logs/chatbot.log` for any issues
3. **Track quota usage**: Monitor your Gemini API usage at https://aistudio.google.com
4. **Frontend integration**: Ensure the chat UI properly displays all error states

## Support

If you encounter issues:
1. Check the logs in `logs/chatbot.log` and `logs/chatbot_errors.log`
2. Verify your Gemini API key is valid
3. Ensure the backend server is running
4. Check the frontend is connecting to the correct backend URL
5. Use the `request_id` from error responses for debugging
