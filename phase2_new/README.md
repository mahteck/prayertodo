# SalaatFlow - Phase 2

Islamic Task Management System with Prayer Time Integration - Full Stack Application

## Overview

SalaatFlow is a comprehensive task management system designed for Muslims to organize their daily tasks, spiritual activities, and connect with local masjids while receiving daily hadith inspiration.

## Project Structure

```
phase2_new/
├── backend/              # FastAPI Backend
│   ├── alembic/         # Database migrations
│   ├── routers/         # API route handlers
│   ├── models.py        # SQLModel database models
│   ├── database.py      # Database configuration
│   ├── main.py          # FastAPI application entry
│   ├── config.py        # Environment configuration
│   ├── seed_data.py     # Database seeding script
│   └── requirements.txt # Python dependencies
│
└── frontend/            # Next.js Frontend
    ├── app/            # Next.js App Router
    │   ├── layout.tsx  # Root layout
    │   ├── page.tsx    # Home page
    │   └── globals.css # Global styles
    ├── components/      # React components
    ├── lib/            # Utility functions
    └── package.json    # Node dependencies
```

## Features

### Backend (FastAPI)

- **24 RESTful API Endpoints**
- **PostgreSQL Database** with Neon (serverless)
- **SQLModel ORM** for type-safe operations
- **Advanced Filtering & Search**
- **Bulk Operations**
- **Automatic API Documentation** (Swagger/OpenAPI)
- **Database Migrations** with Alembic

### Frontend (Next.js)

- **Server-Side Rendering** with App Router
- **Responsive Design** with Tailwind CSS
- **TypeScript** for type safety
- **Modern React Components**
- **Real-time Updates**
- **Prayer Time Integration** (planned)
- **Dark Mode Support**

## Tech Stack

### Backend
- Python 3.11+
- FastAPI 0.110+
- SQLModel 0.0.14
- PostgreSQL (Neon)
- Alembic
- Uvicorn

### Frontend
- Next.js 14.2
- React 18
- TypeScript
- Tailwind CSS
- Axios
- date-fns

## Prerequisites

- **Node.js** >= 20.0.0
- **npm** >= 10.0.0
- **Python** >= 3.11
- **PostgreSQL** database (Neon recommended)

## Quick Start

### 1. Clone Repository

```bash
cd /path/to/phase2_new
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL from https://neon.tech

# Run migrations
alembic upgrade head

# Seed database (optional)
python3 seed_data.py

# Start server
uvicorn main:app --reload
```

Backend will run at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with backend URL

# Start development server
npm run dev
```

Frontend will run at: http://localhost:3000

## API Documentation

Once the backend is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Features

### 1. Spiritual Task Management

Manage tasks with Islamic categories:
- **Farz** (Obligatory)
- **Sunnah** (Prophetic tradition)
- **Nafl** (Voluntary)
- **Deed** (Good deeds)
- **Other**

Priority levels:
- Urgent
- High
- Medium
- Low

Recurrence patterns:
- None
- Daily
- Weekly
- Monthly

### 2. Masjid Management

- Store masjid information
- Link tasks to specific masjids
- Track imam details
- Manage facilities and contact info

### 3. Daily Hadith

- Daily hadith rotation
- Arabic text with English translation
- Source and narrator information
- Thematic categorization

## Database Schema

### SpiritualTask
```sql
id: UUID (primary key)
title: String
description: Text (optional)
category: Enum (Farz, Sunnah, Nafl, Deed, Other)
priority: Enum (Urgent, High, Medium, Low)
tags: String[] (optional)
masjid_id: UUID (foreign key, optional)
due_datetime: DateTime (optional)
recurrence: Enum (None, Daily, Weekly, Monthly)
completed: Boolean
created_at: DateTime
updated_at: DateTime
```

### Masjid
```sql
id: UUID (primary key)
name: String
area: String
city: String
address: Text (optional)
imam_name: String (optional)
phone: String (optional)
facilities: String (optional)
created_at: DateTime
updated_at: DateTime
```

### DailyHadith
```sql
id: UUID (primary key)
hadith_date: Date (unique)
arabic_text: Text
english_translation: Text
narrator: String
source: String
theme: String (optional)
created_at: DateTime
```

## API Endpoints

### Tasks
- `GET /api/v1/tasks` - List tasks (with filters)
- `GET /api/v1/tasks/{id}` - Get single task
- `POST /api/v1/tasks` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `PATCH /api/v1/tasks/{id}/complete` - Mark complete
- `DELETE /api/v1/tasks/{id}` - Delete task
- `GET /api/v1/tasks/upcoming` - Get upcoming tasks
- `GET /api/v1/tasks/stats/summary` - Get statistics
- `POST /api/v1/tasks/bulk/complete` - Bulk complete
- `POST /api/v1/tasks/bulk/delete` - Bulk delete

### Masjids
- `GET /api/v1/masjids` - List masjids
- `GET /api/v1/masjids/{id}` - Get single masjid
- `POST /api/v1/masjids` - Create masjid
- `PUT /api/v1/masjids/{id}` - Update masjid
- `DELETE /api/v1/masjids/{id}` - Delete masjid
- `GET /api/v1/masjids/{id}/tasks` - Get masjid tasks

### Daily Hadith
- `GET /api/v1/hadith/today` - Get today's hadith
- `GET /api/v1/hadith` - List all hadith
- `GET /api/v1/hadith/date/{date}` - Get by date
- `GET /api/v1/hadith/{id}` - Get by ID
- `POST /api/v1/hadith` - Create hadith
- `PUT /api/v1/hadith/{id}` - Update hadith
- `DELETE /api/v1/hadith/{id}` - Delete hadith

## Development Workflow

### Backend Development

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Run tests
pytest
```

### Frontend Development

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:port/database
ENVIRONMENT=development
DEBUG=true
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_PRAYER_API_KEY=your_api_key
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Backend Deployment

**Option 1: Railway**
1. Create account at railway.app
2. Connect GitHub repository
3. Add PostgreSQL database
4. Configure environment variables
5. Deploy

**Option 2: Render**
1. Create account at render.com
2. Create Web Service
3. Connect repository
4. Add PostgreSQL database
5. Configure environment variables
6. Deploy

### Frontend Deployment

**Option 1: Vercel (Recommended)**
1. Push code to GitHub
2. Import project to Vercel
3. Configure environment variables
4. Deploy

**Option 2: Netlify**
1. Connect GitHub repository
2. Configure build settings
3. Add environment variables
4. Deploy

## Docker Support

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api/v1
```

## Troubleshooting

### Common Issues

**Backend won't start**
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify all dependencies installed
- Check Python version (3.11+)

**Frontend build errors**
- Clear .next cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node version (20+)

**Database connection issues**
- Verify DATABASE_URL format
- Check network connectivity
- Ensure database exists
- Verify credentials

**CORS errors**
- Check backend CORS configuration in main.py
- Verify frontend API URL in .env.local
- Ensure backend is running

## Performance Optimization

### Backend
- Use database indexes on frequently queried fields
- Implement pagination for large datasets
- Enable query result caching
- Use connection pooling

### Frontend
- Implement code splitting
- Optimize images with Next.js Image
- Use React.memo for expensive components
- Implement lazy loading

## Security Considerations

- Never commit .env files
- Use environment variables for secrets
- Implement rate limiting (planned)
- Add authentication (planned)
- Validate all user inputs
- Use HTTPS in production
- Implement CORS properly

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request
5. Follow code style guidelines

## Roadmap

### Phase 3 (Planned)
- [ ] User authentication and authorization
- [ ] Real-time prayer time calculations
- [ ] Push notifications
- [ ] Mobile app (React Native)
- [ ] Advanced task analytics
- [ ] Task sharing and collaboration
- [ ] Calendar integration
- [ ] Offline support (PWA)

## License

MIT

## Support

For help and support:
- Read the documentation in `/backend/README.md` and `/frontend/README.md`
- Check existing GitHub issues
- Create new issue with detailed description

## Acknowledgments

- Built with FastAPI and Next.js
- Database hosted on Neon
- Inspired by Islamic principles of time management

## Version History

- **v1.0.0** - Initial release with core features
  - Task management
  - Masjid directory
  - Daily hadith
  - Full CRUD operations
  - Responsive UI
