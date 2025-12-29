# SalaatFlow Backend API

FastAPI backend for Islamic task management system.

## Features

- **RESTful API** with 24 endpoints
- **PostgreSQL database** via Neon (serverless)
- **SQLModel ORM** for type-safe database operations
- **Automatic API documentation** via Swagger/OpenAPI
- **Advanced filtering, sorting, and search**
- **Bulk operations** for tasks
- **Daily hadith management**
- **Masjid (mosque) management**

## Tech Stack

- Python 3.11+
- FastAPI 0.110+
- SQLModel 0.0.14
- PostgreSQL (Neon)
- Alembic (migrations)
- Uvicorn (ASGI server)

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your DATABASE_URL from https://neon.tech
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Seed Database (Optional)

```bash
python3 seed_data.py
```

### 6. Start Server

```bash
uvicorn main:app --reload
```

API will be available at:
- http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Tasks (`/api/v1/tasks`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks (with filters, sort, search) |
| GET | `/tasks/{id}` | Get single task |
| GET | `/tasks/upcoming` | Get upcoming tasks |
| GET | `/tasks/stats/summary` | Get task statistics |
| POST | `/tasks` | Create new task |
| PUT | `/tasks/{id}` | Update task |
| PATCH | `/tasks/{id}/complete` | Mark task complete |
| PATCH | `/tasks/{id}/incomplete` | Mark task incomplete |
| DELETE | `/tasks/{id}` | Delete task |
| POST | `/tasks/bulk/complete` | Complete multiple tasks |
| POST | `/tasks/bulk/delete` | Delete multiple tasks |

### Masjids (`/api/v1/masjids`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/masjids` | List all masjids |
| GET | `/masjids/{id}` | Get single masjid |
| GET | `/masjids/{id}/tasks` | Get tasks for masjid |
| POST | `/masjids` | Create new masjid |
| PUT | `/masjids/{id}` | Update masjid |
| DELETE | `/masjids/{id}` | Delete masjid |

### Daily Hadith (`/api/v1/hadith`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/hadith/today` | Get today's hadith |
| GET | `/hadith` | List all hadith |
| GET | `/hadith/date/{date}` | Get hadith by date |
| GET | `/hadith/{id}` | Get hadith by ID |
| POST | `/hadith` | Create new hadith |
| PUT | `/hadith/{id}` | Update hadith |
| DELETE | `/hadith/{id}` | Delete hadith |

## Database Models

### SpiritualTask

- **Categories**: Farz, Sunnah, Nafl, Deed, Other
- **Priorities**: Urgent, High, Medium, Low
- **Recurrence**: None, Daily, Weekly, Monthly
- **Fields**: title, description, category, priority, tags, masjid_id, due_datetime, recurrence, completed

### Masjid

- **Fields**: name, area, city, address, imam_name, phone, facilities

### DailyHadith

- **Fields**: hadith_date (unique), arabic_text, english_translation, narrator, source, theme

## Development

### Run Tests

```bash
pytest
```

### Create Migration

```bash
alembic revision --autogenerate -m "Description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT
