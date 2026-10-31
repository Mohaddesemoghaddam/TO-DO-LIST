# ToDoList: From Python OOP to a Layered FastAPI Web API

A task and project management application developed in three phases, evolving from an **in-memory Python CLI** to a **PostgreSQL-backed REST API** built with **FastAPI**, **SQLAlchemy**, and **Alembic**, using a clean, layered architecture.

## Development phases

| Phase | Focus | Highlights |
|---|---|---|
| **1 · Python OOP** | Core domain and CLI | `Project` and `Task` classes, menu-driven CLI, full CRUD, input validation |
| **2 · Relational database** | Persistence | PostgreSQL in Docker, SQLAlchemy ORM models, repository layer, Alembic migrations, scheduled auto-close of overdue tasks |
| **3 · Web API** | REST interface | FastAPI with routers, controllers, services, repositories, and Pydantic schemas; interactive Swagger documentation |

## Architecture

```text
HTTP request
    │
    ▼
Routers          app/api/routes/       endpoint definitions
    │
    ▼
Controllers      app/api/controllers/  request handling and HTTP errors
    │
    ▼
Services         services/             business rules and validation
    │
    ▼
Repositories     repositories/         database access
    │
    ▼
Models           models/               SQLAlchemy ORM (PostgreSQL)
```

Request and response bodies are validated with **Pydantic** schemas (`app/schemas/`), and domain errors are handled through custom exception classes (`exceptions/`).

## Features

- **Projects:** create, list, view, update, and delete projects, and list a project's tasks
- **Tasks:** create, list, view, update, and delete tasks within a project, and update task status
- **Validation:** Pydantic schemas for names, descriptions, deadlines, and status values
- **Configurable limits** on the number of projects and tasks through environment variables
- **Automatic deadline handling:** a scheduled job closes overdue tasks every two minutes
- **Database migrations** with Alembic, including timestamps, cascade deletes, and a users table
- **Interactive API docs** with Swagger UI

## API endpoints

### Projects

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/projects` | Create a project |
| `GET` | `/projects` | List all projects |
| `GET` | `/projects/{project_name}` | Get a project |
| `PATCH` | `/projects/{project_name}` | Update a project |
| `DELETE` | `/projects/{project_name}` | Delete a project and its tasks |
| `GET` | `/projects/{project_name}/tasks` | List the tasks of a project |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/projects/{project_name}/tasks` | Create a task |
| `GET` | `/projects/{project_name}/tasks` | List tasks |
| `GET` | `/projects/{project_name}/tasks/{task_title}` | Get a task |
| `PATCH` | `/projects/{project_name}/tasks/{task_title}` | Update a task |
| `PATCH` | `/projects/{project_name}/tasks/{task_title}/status` | Update task status |
| `DELETE` | `/projects/{project_name}/tasks/{task_title}` | Delete a task |

## Project structure

```text
├── app/
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   ├── routes/              # project and task routers
│   │   └── controllers/         # project and task controllers
│   └── schemas/                 # Pydantic request and response schemas
├── services/                    # business logic
├── repositories/                # data access layer
├── models/                      # SQLAlchemy models (Project, Task, User)
├── exceptions/                  # custom exception hierarchy
├── db/                          # database engine and session
├── commands/
│   └── autoclose_overdue.py     # scheduled overdue-task job
├── alembic/                     # database migrations
├── docker-compose.yml           # PostgreSQL service
├── main.py                      # Phase 1 CLI
└── project.py, task.py, manager.py
```

## Getting started

### 1. Configure the environment

Create a `.env` file in the project root:

```env
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=todo_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://todo_user:your_password@localhost:5432/todo_db
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50
```

### 2. Start PostgreSQL

```bash
docker compose up -d
```

### 3. Install dependencies and run migrations

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic python-dotenv schedule
alembic upgrade head
```

### 4. Run the API

```bash
uvicorn app.api.main:app --reload
```

Open the interactive documentation at **http://127.0.0.1:8000/docs**.

### 5. Run the overdue-task scheduler (optional)

```bash
python -m commands.autoclose_overdue
```

### Phase 1 CLI

The original command-line version is still available:

```bash
python main.py
```

## Future work

- JWT authentication and user-specific projects
- Automated tests and a CI/CD pipeline
- Web frontend with React or Vue
- Redis caching
- Background task queue with Celery or RQ

## Tech stack

Python · FastAPI · Pydantic · SQLAlchemy · Alembic · PostgreSQL · Docker

---

Developed as part of the Software Engineering course at Amirkabir University of Technology.
