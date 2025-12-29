# SalaatFlow Phase II - Complete Setup Guide

**Date**: 2025-12-27
**Important**: Follow these steps to set up the project correctly

---

## ✅ UPDATE: Phase II Files Created

Phase II backend and frontend have been created in `phase2_new/` directory due to WSL permission issues with the old `phase2/` folder.

**IMPORTANT: Use `phase2_new/` for all setup steps below.**

---

## Step 1: Verify Project Structure

The correct structure is now:

```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo

# Verify the new structure
ls -la phase2_new/
```

Expected structure:
```
hackathon2_prayertodo/
├── phase1/               # Console app (Phase I)
├── phase2_new/           # Web app (Phase II) ← USE THIS
│   ├── backend/          # FastAPI backend (CREATED ✅)
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── tasks.py
│   │   │   ├── masjids.py
│   │   │   └── hadith.py
│   │   ├── requirements.txt
│   │   ├── seed_data.py
│   │   └── .env.example
│   └── frontend/         # Next.js frontend (PARTIAL ✅)
│       ├── package.json
│       ├── tsconfig.json
│       ├── lib/
│       │   ├── types.ts
│       │   └── api.ts
│       ├── components/
│       │   ├── Navbar.tsx
│       │   └── TaskCard.tsx
│       └── .env.local.example
├── plans/
├── specs/
├── tasks/
└── README.md
```

---

## Step 2: Backend Setup (Python Virtual Environment)

### A. Navigate to Backend Directory

```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend
```

### B. Install Python Requirements (if needed)

```bash
# Only if you get errors about missing python3-venv
sudo apt update
sudo apt install python3-full python3-venv python3-pip -y
```

### C. Create Virtual Environment

```bash
# Create virtual environment named 'venv'
python3 -m venv venv
```

If you get an error, try:
```bash
python3.11 -m venv venv
# or
python3.12 -m venv venv
```

### D. Activate Virtual Environment

```bash
# On Linux/WSL
source venv/bin/activate

# You should see (venv) in your prompt now
# (venv) user@machine:~/path$
```

### E. Install Python Dependencies

```bash
# Now install requirements (pip is inside venv, not system)
pip install -r requirements.txt
```

This should work without the "externally-managed-environment" error!

### F. Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env
# or
vim .env
# or use any text editor
```

**Required settings in .env**:
```
# Get this from https://neon.tech (free tier available)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Frontend URL for CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Server settings (these are fine as defaults)
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

### G. Set Up Database (Neon PostgreSQL)

1. Go to https://neon.tech
2. Sign up for free account
3. Create new project: "salaatflow"
4. Copy connection string
5. Paste into .env as DATABASE_URL

### H. Run Database Migrations

```bash
# Make sure venv is activated (you should see (venv) in prompt)
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> xxxxx, Initial schema
```

### I. Seed Database with Sample Data

```bash
python3 seed_data.py
```

Expected output:
```
🗑️  Clearing existing data...
✅ Existing data cleared
🕌 Seeding masjids...
  ✓ Created: Masjid Al-Huda
  ✓ Created: Masjid Al-Noor
  ...
✅ 5 masjids seeded
📋 Seeding spiritual tasks...
  ✓ Created: Attend Fajr at Masjid Al-Huda...
  ...
✅ 14 spiritual tasks seeded
📖 Seeding daily hadith...
  ✓ Created hadith for: 2025-12-27
  ...
✅ 5 hadith entries seeded

✅ Database seeding completed successfully!
```

### J. Start Backend Server

```bash
# Make sure venv is activated
uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### K. Test Backend

Open another terminal and test:

```bash
# Health check
curl http://localhost:8000/health

# API root
curl http://localhost:8000/

# View Swagger docs in browser
xdg-open http://localhost:8000/docs
# or just open: http://localhost:8000/docs
```

---

## Step 3: Frontend Setup (Node.js)

### A. Navigate to Frontend Directory

```bash
# Open a NEW terminal (keep backend running)
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/frontend
```

### B. Install Node.js (if needed)

```bash
# Check if Node.js is installed
node --version
npm --version

# If not installed or version < 20, install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### C. Install Frontend Dependencies

```bash
npm install
```

This will install all packages from package.json.

### D. Configure Environment Variables

```bash
# Copy example file
cp .env.local.example .env.local

# Edit .env.local
nano .env.local
```

**Required settings in .env.local**:
```
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### E. Start Frontend Dev Server

```bash
npm run dev
```

Expected output:
```
   ▲ Next.js 14.2.0
   - Local:        http://localhost:3000
   - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.1s
```

### F. Open Application in Browser

```bash
# Open browser to:
http://localhost:3000

# Or use command:
xdg-open http://localhost:3000
```

---

## Step 4: Verify Everything Works

### Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Swagger docs accessible at http://localhost:8000/docs
- [ ] Dashboard loads at http://localhost:3000
- [ ] Daily hadith displays on dashboard
- [ ] Task list shows seeded tasks at http://localhost:3000/tasks
- [ ] Can create new task
- [ ] Can edit task
- [ ] Can delete task
- [ ] Can toggle task completion
- [ ] Masjid list shows seeded masjids at http://localhost:3000/masjids

---

## Troubleshooting

### Problem: "externally-managed-environment" error

**Solution**: You forgot to activate the virtual environment.
```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend
source venv/bin/activate
# Now you can use pip
```

### Problem: "alembic: command not found"

**Solution**: Virtual environment not activated or alembic not installed.
```bash
source venv/bin/activate
pip install alembic
```

### Problem: "Cannot connect to database" or "invalid channel_binding value"

**Solution 1**: Remove extra quotes and `channel_binding` parameter from DATABASE_URL.

Your DATABASE_URL should look like this:
```bash
# CORRECT - No extra quotes, no channel_binding
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# WRONG - Has extra quote at end
DATABASE_URL=postgresql://user:password@host/database?sslmode=require'

# WRONG - Has channel_binding (not needed for Neon)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require&channel_binding=require
```

**Solution 2**: Verify your .env file has correct DATABASE_URL from Neon.
```bash
# Check your DATABASE_URL (should have no extra quotes)
cat .env | grep DATABASE_URL

# Test connection
python3 -c "from database import engine; print(engine)"
```

### Problem: "CORS error" in browser console

**Solution**: Check backend .env has correct CORS_ORIGINS.
```bash
# In backend/.env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Problem: "Module not found" in frontend

**Solution**: Install dependencies.
```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/frontend
npm install
```

### Problem: Port already in use

**Solution**: Kill the process or use different port.
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>

# Or use different port
uvicorn main:app --reload --port 8001
```

---

## Quick Start Commands (After Initial Setup)

### Start Backend (Terminal 1)
```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/backend
source venv/bin/activate
uvicorn main:app --reload
```

### Start Frontend (Terminal 2)
```bash
cd /mnt/d/Data/GIAIC/hackathon2_prayertodo/phase2_new/frontend
npm run dev
```

### Run Both with One Command (Optional)
Create a `start.sh` script in phase2_new/:

```bash
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both servers"

wait
```

Make it executable:
```bash
chmod +x start.sh
./start.sh
```

---

## Deactivate Virtual Environment

When you're done:
```bash
# In backend terminal
deactivate

# This returns you to system Python
```

---

## Summary

The key points:
1. ✅ Use `python3 -m venv venv` to create virtual environment
2. ✅ Always `source venv/bin/activate` before pip install
3. ✅ Configure `.env` (backend) and `.env.local` (frontend)
4. ✅ Get Neon PostgreSQL database URL
5. ✅ Run migrations and seed data
6. ✅ Start both backend and frontend servers
7. ✅ Test at http://localhost:3000

---

**Need Help?**
- Backend API docs: http://localhost:8000/docs
- Check backend logs in terminal 1
- Check frontend logs in terminal 2
- Check browser console (F12) for frontend errors

---

**Next Steps After Setup:**
- Explore the application
- Create tasks
- Test filtering and search
- Review code in /phase2/backend and /phase2/frontend

**Phase II Progress**: 85% complete
**Remaining**: Testing and documentation (Tasks 37-40)
