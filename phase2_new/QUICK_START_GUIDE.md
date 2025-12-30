# 🚀 SalaatFlow - Quick Start Guide

## ✅ Everything is Fixed and Running!

Both backend and frontend are currently running and fully functional.

## 🌐 Access Your Application

### Frontend (Main App)
**URL**: http://localhost:3001

### Backend API
**URL**: http://localhost:8000
**Documentation**: http://localhost:8000/docs

---

## 🎯 How to Use the Chatbot

### Option 1: Navigation Bar
Look at the top of the page → Click **"AI Assistant 🤖"**

### Option 2: Home Page
On the dashboard → Click the **"AI Assistant"** card (it has a green "NEW" badge)

### Option 3: Direct URL
Navigate to: http://localhost:3001/chat

---

## 💬 Try These Chat Commands

### Create Tasks
```
Add a task to pray Fajr tomorrow at 5:30 AM
Create a reminder for Asr prayer
Remind me to read Quran daily
```

### Query Masjids
```
Show me masjids in North Nazimabad
What time is Jummah at Masjid Al-Huda?
Find prayer times for my area
```

### Daily Hadith
```
Show me today's hadith
Aaj ka hadith sunao (Urdu)
```

### In Urdu
```
Kal se daily Fajr se 20 minutes pehle mujhe remind karna
North Nazimabad main masjid dikhao
Aaj ka hadith batao
```

---

## 📱 Navigate the App

### 🏠 Dashboard
- View statistics
- See upcoming tasks
- Quick actions
- Today's hadith preview

### ✓ Tasks
- Create new tasks
- View all tasks
- Filter by category/priority
- Mark complete/incomplete

### 🕌 Masjids
- Browse by area
- View prayer times
- Add new masjids
- Link tasks to masjids

### 📖 Daily Hadith
- Today's hadith
- English + Arabic
- Narrator & source info

### 🤖 AI Assistant
- **NEW!** Natural conversation
- Task management via chat
- Bilingual support
- Smart suggestions

---

## 🛠️ Current Status

✅ Backend: Running on port 8000
✅ Frontend: Running on port 3001
✅ Database: Connected
✅ AI Agent: Active (gpt-4o-mini)
✅ Chatbot: Visible and functional
✅ Tasks: Working
✅ Masjids: Working
✅ Hadith: Working

---

## 🔄 Restart Services (if needed)

### Backend
```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend
```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/frontend
npm run dev
```

---

## 🐛 Troubleshooting

### Chatbot not responding?
1. Check backend is running (http://localhost:8000/docs)
2. Verify your OpenAI API key has credits
3. Check browser console for errors

### Tasks/Masjids not loading?
1. Ensure backend is running
2. Check database connection
3. Refresh the page

### Port conflicts?
- Backend uses port 8000
- Frontend uses port 3000 or 3001
- Kill conflicting processes or change ports

---

## 🎉 You're All Set!

Open http://localhost:3001 in your browser and start using SalaatFlow!

**Try the AI Assistant first** - it's the coolest new feature! 🤖✨
