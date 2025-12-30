# SalaatFlow Chatbot - Requirements Document

## Overview
Yeh document SalaatFlow application ke AI Chatbot ke complete requirements aur specifications define karta hai.

## Current Status
- Backend server running on port 8000
- Google Gemini API integrated (FREE)
- Database seeded with sample data
- Frontend on port 3000

## Chatbot Ki Zarooriyaat

### 1. Task Management Operations

#### A. Task Creation
Chatbot ko ye operations perform karne chahiye:
- **Natural language se task banana**
  - Example: "Fajr ki namaz ka task bana do"
  - Example: "Reminder set karo Quran padhne ke liye"
  - Example: "Kal subah 6 baje Tahajjud ki reminder"

- **Task parameters extract karna**:
  - Task title
  - Linked prayer (Fajr, Dhuhr, Asr, Maghrib, Isha)
  - Priority (high, medium, low)
  - Time (agar specify kiya ho)
  - Description

#### B. Task Listing
- **User ke tasks dikhana**
  - Example: "Mujhe aaj ke tasks dikhao"
  - Example: "Mere pending tasks kya hain"
  - Example: "Show my Fajr tasks"

#### C. Task Update
- **Task ko update karna**
  - Example: "Quran task ko urgent mark karo"
  - Example: "Fajr task complete kar do"
  - Example: "Task #1 ka time change karo"

#### D. Task Deletion
- **Task ko delete karna**
  - Example: "Quran task delete kar do"
  - Example: "Task #2 remove karo"

### 2. Masjid Information

#### Masjid Search
- **Area se masjid dhundna**
  - Example: "North Nazimabad mein konsi masjid hai"
  - Example: "DHA mein namaz kahan padh sakte hain"

#### Prayer Times
- **Masjid ki namaz times batana**
  - Example: "Masjid Al-Huda ki Fajr time kya hai"
  - Example: "Nearest masjid ka Jummah time"

### 3. Hadith & Islamic Content

- **Daily Hadith share karna**
  - Example: "Aaj ki hadith sunao"
  - Example: "Koi motivational hadith batao"

- **Islamic guidance**
  - Example: "Tahajjud ka tareeqa batao"
  - Example: "Wudu kaise karte hain"

### 4. General Conversation

- **Greetings & small talk**
  - Example: "Assalam o Alaikum"
  - Example: "Kaise ho"

- **Help & guidance**
  - Example: "Tum kya kar sakte ho"
  - Example: "Meri madad karo"

## Technical Specifications

### Language Support
- **Urdu (primary)**
- **English (secondary)**
- **Urdu-English mix (Romanized Urdu)**

### Response Format
- Clear and concise
- Formatted with emojis for better UX
- Numbered lists for multiple items
- Status indicators (✅, ⏳, ❌)

### Error Handling
- User-friendly error messages
- Graceful degradation
- Retry suggestions

## Integration Points

### Backend APIs
- `POST /api/v1/chat/` - Main chat endpoint
- Uses existing task/masjid/hadith APIs

### Database
- PostgreSQL (Neon)
- Tables: spiritual_tasks, masjids, daily_hadith

### AI Model
- Google Gemini Pro (FREE)
- Intent detection + Tool calling
- Context-aware responses

## Success Criteria

1. ✅ Task creation via natural language
2. ✅ Task listing with proper formatting
3. ✅ Masjid search by area
4. ✅ Prayer times display
5. ✅ Urdu language support
6. ✅ Error handling
7. ⏳ Task updates
8. ⏳ Task deletion
9. ⏳ Hadith sharing
10. ⏳ Islamic Q&A

## Next Steps

### Phase 1: Core Functionality (COMPLETED)
- [x] Setup Gemini API
- [x] Intent detection system
- [x] Task creation
- [x] Task listing
- [x] Masjid search

### Phase 2: Enhanced Features (IN PROGRESS)
- [ ] Task update/delete
- [ ] Better intent patterns
- [ ] Hadith integration
- [ ] Context memory

### Phase 3: Polish (PENDING)
- [ ] Natural language understanding
- [ ] Multi-turn conversations
- [ ] Personalization
- [ ] Analytics

## Notes
- FREE tier Gemini API use kar rahe hain
- Rate limits: Generous (60 requests per minute)
- No OpenAI dependency
- Fully functional chatbot

---

**Last Updated**: 2025-12-30
**Version**: 1.0.0
**Status**: Active Development
