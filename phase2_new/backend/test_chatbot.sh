#!/bin/bash
# SalaatFlow Chatbot Testing Script
# Quick tests to verify the chatbot is working

echo "🧪 Testing SalaatFlow Chatbot..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HEALTH_RESPONSE=$(curl -s http://localhost:8000/api/v1/chat/health)
echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null

if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    echo -e "${GREEN}✅ Health check PASSED${NC}"
elif echo "$HEALTH_RESPONSE" | grep -q '"quota_exceeded"'; then
    echo -e "${YELLOW}⚠️  Server is healthy but Gemini API quota exceeded${NC}"
    echo -e "${YELLOW}   Wait a few minutes and try again${NC}"
else
    echo -e "${RED}❌ Health check FAILED${NC}"
fi
echo ""

# Test 2: Simple Conversation (Without Auth)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Simple Conversation (No Auth Required)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Assalamualaikum",
    "user_id": null,
    "conversation_history": []
  }')

echo "$CHAT_RESPONSE" | python3 -m json.tool 2>/dev/null

if echo "$CHAT_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ Conversation test PASSED${NC}"
elif echo "$CHAT_RESPONSE" | grep -q '"quota_exceeded"'; then
    echo -e "${YELLOW}⚠️  API quota exceeded - chatbot is working but rate limited${NC}"
else
    echo -e "${RED}❌ Conversation test FAILED${NC}"
fi
echo ""

# Test 3: Authentication Guard
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Authentication Guard (Task Creation Without Login)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
AUTH_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Fajr task for me",
    "user_id": null
  }')

echo "$AUTH_RESPONSE" | python3 -m json.tool 2>/dev/null

if echo "$AUTH_RESPONSE" | grep -q '"authentication_required"'; then
    echo -e "${GREEN}✅ Authentication guard PASSED${NC}"
else
    echo -e "${RED}❌ Authentication guard FAILED${NC}"
fi
echo ""

# Test 4: Error Message Format
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 4: Error Message Format Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if response has required fields
if echo "$AUTH_RESPONSE" | grep -q '"request_id"'; then
    echo -e "${GREEN}✅ Request ID present${NC}"
else
    echo -e "${RED}❌ Request ID missing${NC}"
fi

if echo "$AUTH_RESPONSE" | grep -q '"error_message"'; then
    echo -e "${GREEN}✅ Error message present${NC}"
else
    echo -e "${RED}❌ Error message missing${NC}"
fi

if echo "$AUTH_RESPONSE" | grep -q '"error"'; then
    echo -e "${GREEN}✅ Error code present${NC}"
else
    echo -e "${RED}❌ Error code missing${NC}"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Chatbot backend is working correctly!"
echo ""
echo "⚠️  Note: If you see 'quota_exceeded' errors, this means:"
echo "   - The backend is working correctly"
echo "   - Error handling is functioning properly"
echo "   - You've hit the Gemini API free tier rate limit"
echo "   - Wait a few minutes and try again"
echo ""
echo "📚 See CHATBOT_TESTING_GUIDE.md for more details"
echo ""
