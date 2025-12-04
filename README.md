
# 🗂️ ToDoList – Python OOP → RDB → FastAPI Web API

## ⚠️ Deprecation Notice
The **CLI version** (`main.py`, `manager.py`) is now **deprecated** and will be removed in the next phase.
Please use the **FastAPI Web API** instead.

---

## 📍 Overview
This repository contains the complete evolution of the ToDoList application across 3 phases:

- **Phase 1:** In‑Memory Python OOP + CLI  
- **Phase 2:** PostgreSQL + SQLAlchemy ORM + Alembic Migrations  
- **Phase 3:** FastAPI Web API with Controllers, Services, Repositories, Schemas

The current active version of the project runs through the **Web API**, not the CLI.

---

# ✅ Project Progress Summary

## Phase 1 – Python OOP (In‑Memory)
- Implemented classes: `Project`, `Task`, `Manager`
- CLI menu system (`main.py`)
- Full CRUD for Projects and Tasks
- In‑memory storage (no DB)
- Robust validation (name, description, deadlines, status)
- Unit tests: `test_task.py`, `test_manager.py`

---

## Phase 2 – Database Migration (RDB)
- Added PostgreSQL (Docker)
- SQLAlchemy ORM models for:
  - `projects`
  - `tasks`
  - `users`
- Added DB session + base models
- Added Repository layer
- Full Alembic migration chain (valid & verified)
- Auto-close overdue tasks command
- Database schema successfully tested

---

## Phase 3 – Web API (FastAPI)
- Designed full multi-layer architecture:
  - Routes
  - Controllers
  - Services
  - Repositories
  - Schemas (Request/Response)
- Implemented complete Project API (CRUD)
- Implemented complete Task API (CRUD)
- Implemented User API
- Fixed legacy import-path issues
- Fully functional Swagger UI
- Postman branch prepared for testing
- Web API replaces CLI as the main interface

---

# 🎛️ CLI (Deprecated)
The CLI version exists only for historical and grading purposes.

### CLI Features
- Create / edit / delete projects
- Add / edit / delete tasks
- Update status
- Show all tasks of a project
- Menu-driven system

### CLI Structure
```
main.py          (DEPRECATED)
manager.py       (DEPRECATED)
project.py
task.py
.env
tests/
```

---

# 🌐 Web API (Active System)

### Run FastAPI
```
uvicorn app.api.main:app --reload
```

### Swagger
```
http://127.0.0.1:8000/docs
```

### API Directory Structure
```
app/
 ├── api/
 │    ├── main.py
 │    └── routes/
 │         ├── project_router.py
 │         ├── task_router.py
 │         └── user_router.py
 ├── controllers/
 ├── services/
 ├── repositories/
 ├── schemas/
 │     ├── project/
 │     ├── task/
 │     └── user/
 └── models/
```

---

# 🧩 Future Improvements
- JWT authentication
- React/Vue frontend
- Redis caching
- Background tasks (Celery/RQ)
- CI/CD pipeline

---

# 📄 License
This project was developed as part of the **ToDoList – Software Engineering Course (AUT)**.
