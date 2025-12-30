# Phase III Configuration Guide

## Overview

Phase III adds AI-powered conversational capabilities to SalaatFlow. This guide explains how to configure the chatbot environment variables and troubleshoot common issues.

## Required Environment Variables

### OpenAI Configuration

#### `OPENAI_API_KEY` (Required)
- **Purpose**: API key for OpenAI services (GPT-4 model)
- **Type**: String
- **Example**: `sk-proj-...`
- **How to obtain**:
  1. Visit https://platform.openai.com/api-keys
  2. Sign in or create an account
  3. Click "Create new secret key"
  4. Copy the key and add to `.env`

#### `CHATBOT_MODEL` (Optional)
- **Purpose**: OpenAI model to use for the chatbot
- **Type**: String
- **Default**: `gpt-4`
- **Options**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Example**: `CHATBOT_MODEL=gpt-4`

#### `CHATBOT_TEMPERATURE` (Optional)
- **Purpose**: Controls randomness in responses (0.0-1.0)
- **Type**: Float
- **Default**: `0.7`
- **Example**: `CHATBOT_TEMPERATURE=0.7`
- **Note**: Lower values (0.2-0.4) = more focused/deterministic, Higher values (0.8-1.0) = more creative

#### `CHATBOT_MAX_TOKENS` (Optional)
- **Purpose**: Maximum tokens in agent response
- **Type**: Integer
- **Default**: `1000`
- **Example**: `CHATBOT_MAX_TOKENS=1000`

#### `CHATBOT_TIMEOUT` (Optional)
- **Purpose**: Timeout for agent requests (seconds)
- **Type**: Integer
- **Default**: `30`
- **Example**: `CHATBOT_TIMEOUT=30`

### Backend Integration

#### `BACKEND_BASE_URL` (Optional)
- **Purpose**: Base URL for Phase II backend API
- **Type**: String
- **Default**: `http://localhost:8000`
- **Example**: `BACKEND_BASE_URL=http://localhost:8000`
- **Production**: Set to your deployed backend URL

### User Preferences

#### `DEFAULT_AREA` (Optional)
- **Purpose**: Default area for masjid queries
- **Type**: String
- **Default**: None
- **Example**: `DEFAULT_AREA=North Nazimabad`

#### `DEFAULT_MASJID_ID` (Optional)
- **Purpose**: Default masjid ID for prayer time queries
- **Type**: Integer
- **Default**: None
- **Example**: `DEFAULT_MASJID_ID=1`

## Setup Instructions

### 1. Backend Setup

```bash
cd phase2_new/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # If you don't have .env yet
nano .env  # Or use your preferred editor
```

### 2. Set Your OpenAI API Key

**IMPORTANT**: Replace the placeholder with your real key:

```bash
# In .env file:
OPENAI_API_KEY=sk-your-real-api-key-here
```

### 3. Verify Configuration

```bash
python -c "from chatbot.config.settings import OPENAI_API_KEY; print('✅ API Key loaded' if OPENAI_API_KEY else '❌ API Key missing')"
```

## Troubleshooting

### Issue: "OPENAI_API_KEY environment variable is required"

**Cause**: The API key is not set in your environment.

**Solution**:
1. Ensure `.env` file exists in `backend/` directory
2. Verify `OPENAI_API_KEY=sk-...` line is present
3. Restart your backend server to reload environment

### Issue: "API rate limit exceeded"

**Cause**: You've exceeded OpenAI's free tier limits.

**Solution**:
1. Check your usage at https://platform.openai.com/usage
2. Add payment method if needed
3. Consider using `gpt-3.5-turbo` model to reduce costs

### Issue: "Backend connection refused"

**Cause**: Phase II backend is not running or wrong URL.

**Solution**:
1. Ensure Phase II backend is running: `python main.py`
2. Verify `BACKEND_BASE_URL` matches backend port
3. Check backend health: `curl http://localhost:8000/health`

### Issue: "Agent timeout"

**Cause**: Request took longer than `CHATBOT_TIMEOUT` seconds.

**Solution**:
1. Increase timeout: `CHATBOT_TIMEOUT=60`
2. Check OpenAI API status
3. Simplify complex queries

## Security Best Practices

1. **Never commit `.env` to version control**
   - Ensure `.env` is in `.gitignore`
   - Use `.env.example` for documentation

2. **Protect your API key**
   - Don't share your `OPENAI_API_KEY`
   - Rotate keys periodically
   - Use environment variables in production

3. **Monitor API usage**
   - Set spending limits in OpenAI dashboard
   - Monitor monthly usage
   - Alert on unusual activity

## Testing Configuration

Test your configuration with this simple script:

```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend
source venv/bin/activate

python << 'EOF'
import os
from chatbot.config import settings

print("Configuration Test:")
print(f"✅ OpenAI API Key: {'Set' if settings.OPENAI_API_KEY else 'Missing'}")
print(f"✅ Model: {settings.CHATBOT_MODEL}")
print(f"✅ Backend URL: {settings.BACKEND_BASE_URL}")
print(f"✅ Temperature: {settings.CHATBOT_TEMPERATURE}")
print(f"✅ Max Tokens: {settings.CHATBOT_MAX_TOKENS}")
print(f"✅ Timeout: {settings.CHATBOT_TIMEOUT}s")
print("\nAll settings loaded successfully!")
EOF
```

## Next Steps

Once configuration is complete:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run backend**: `python main.py`
3. **Access chat**: Visit `http://localhost:3000/chat` (after frontend setup)
4. **Test conversation**: Try "Add a task to pray Fajr tomorrow"

## Additional Resources

- OpenAI API Documentation: https://platform.openai.com/docs
- OpenAI Pricing: https://openai.com/api/pricing/
- SalaatFlow Phase III Specification: See `specs/` directory
- Task List: See `tasks/PHASE3_TASKS.md`
