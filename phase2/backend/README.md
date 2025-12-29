# SalaatFlow - Phase II Backend

**FastAPI REST API for Prayer & Spiritual Task Management**

---

## Overview

This is the backend service for SalaatFlow Phase II, providing a RESTful API for managing spiritual tasks, masjids, and daily hadith content.

## Tech Stack

- **FastAPI 0.110+** - Modern Python web framework
- **SQLModel 0.0.14** - SQL database ORM with Pydantic integration
- **PostgreSQL** - Database (via Neon serverless)
- **Alembic** - Database migrations
- **Uvicorn** - ASGI server

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL database account (free tier available at [neon.tech](https://neon.tech))
- pip or pip3

## Setup

### 1. Install Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and fill in your database credentials:

```bash
cp .env.example .env
```

Edit `.env` and set your Neon PostgreSQL connection string:
```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

### 3. Run Database Migrations

```bash
alembic upgrade head
```

### 4. Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

---

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Tasks
- `GET /tasks` - List all tasks (with filtering)
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `PATCH /tasks/{id}/complete` - Mark task as complete
- `PATCH /tasks/{id}/uncomplete` - Mark task as incomplete

#### Masjids
- `GET /masjids` - List all masjids
- `POST /masjids` - Create new masjid
- `GET /masjids/{id}` - Get masjid by ID
- `PUT /masjids/{id}` - Update masjid
- `DELETE /masjids/{id}` - Delete masjid
- `GET /masjids/{id}/tasks` - Get tasks for a masjid

#### Daily Hadith
- `GET /hadith/daily` - Get today's hadith
- `POST /hadith` - Create hadith entry
- `GET /hadith/{id}` - Get hadith by ID

Full API documentation available at `/docs` when server is running.

---

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel data models
├── database.py          # Database connection and session management
├── config.py            # Environment configuration
├── routers/             # API route handlers
│   ├── tasks.py         # Task endpoints
│   ├── masjids.py       # Masjid endpoints
│   └── hadith.py        # Hadith endpoints
├── tests/               # Test files
├── alembic/             # Database migrations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md            # This file
```

---

## Development

### Running Tests

```bash
pytest tests/
```

### Creating Database Migrations

After modifying models:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Code Style

This project follows PEP 8 style guidelines. Use type hints for all function parameters and return values.

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:3000` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `ENVIRONMENT` | Environment mode | `development` or `production` |

---

## Deployment

See `/docs/deployment.md` for Docker and production deployment instructions.

---

**Phase**: II - Full-Stack Web Application (Backend)
**Status**: In Development
