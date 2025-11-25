# 🗂️ ToDoList – Python OOP (In-Memory)

## 📍 Overview
This project implements a **command-line ToDoList manager** built entirely with **Object-Oriented Programming (OOP)** principles in Python.  
It allows users to create multiple projects, add and manage tasks inside them, and edit or delete items — all in memory (no database).  
The design strictly follows the **User Stories** and **Acceptance Criteria** defined in the project’s official PDF (Phase 1 & 2).

---
## 🚀 Features 
| # | Feature | Description |
|---|----------|-------------|
| 1 | **Create Project** | Add new projects with name ≤ 30 char and description ≤ 150 char. |
| 2 | **Show All Projects** | Display all projects sorted by creation time. |
| 3 | **Add Task to Project** | Each project can hold limited tasks (max from `.env`); defaults to status = `todo`. |
| 4 | **Edit Project** | Change project name/description (unique name validation). |
| 5 | **Edit Task** | Change any task field (title, description, deadline, status). |
| 6 | **Update Task Status** | Mark tasks as `todo` → `doing` → `done`. |
| 7 | **Delete Task** | Remove a specific task from a project. |
| 8 | **Delete Project** | Cascade deletes all tasks within the project. |
| 9 | **Show Tasks of a Project** | Display all tasks linked to a selected project (title, status, deadline). |
| 10 | **Exit** | Safely break from the CLI loop. |


---

## 🧠 Architecture
```
📦 todo_list/
│
├── main.py          # CLI interface (menu-driven)
├── manager.py       # Handles CRUD for projects & tasks
├── project.py       # Project class (name, desc, tasks)
├── task.py          # Task class (title, desc, deadline, status)
├── .env             # MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK
└── tests/
    ├── test_manager.py
    └── test_task.py
```

- **Manager** acts as a controller connecting the CLI and model classes.  
- **In‑Memory:** All data live during runtime — no file or DB persistence.  
- **Validation:** Input size, status choice, and date format (`YYYY‑MM‑DD`) enforced at the class level.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/<Mohaddesemoghaddam>/todo-list-oop.git
cd todo-list-oop
```

### 2️⃣ Create `.env`
```
MAX_NUMBER_OF_PROJECT=5
MAX_NUMBER_OF_TASK=10
```

### 3️⃣ Run the CLI
```bash
python main.py
```

---

## 💾 Sample CLI Session
```
=== ToDoList CLI ===
1. Create Project
2. Show All Projects
3. Add Task to Project
...
Choose an option (1–9): 1
Enter project name: StudyPlan
Enter project description: Semester goal tracking system
[SUCCESS] Project created successfully.

Choose an option (1–9): 3
Project name: StudyPlan
Task title: Math revision
Task description: Review chapters 1–3
Deadline (YYYY-MM-DD): 2025-11-01
[SUCCESS] Task added to project 'StudyPlan'
```

---


## 🧩 Future Improvements
- Add JSON/SQLite persistence layer.  
- Implement search/sort for tasks.  
- Add colored CLI output (using `colorama`).  
- Integrate date validation via `datetime.date` type.

---


_This project was developed as part of the **ToDoList – Python OOP (In‑Memory)** assignment (Phase 1 & 2) to demonstrate CRUD, input validation, OOP design, and adherence to Git Policy._
