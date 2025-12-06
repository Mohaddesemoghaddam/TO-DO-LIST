# from sqlalchemy.orm import Session
# from datetime import datetime

# from repositories.project_repository import ProjectRepository
# from repositories.task_repository import TaskRepository
# from db.session import SessionLocal

# from exceptions.service_exceptions import (
#     ProjectNotFoundException,
#     TaskNotFoundException,
#     TaskValidationError
# )


# class TaskService:
#     VALID_STATUSES = ("todo", "doing", "done")

#     def __init__(self, db=None):
#         if db is None:
#             from db.session import SessionLocal
#             db = SessionLocal()
#         self.db = db
#         self.repo = TaskRepository(db)


#     # ------------------------------------
#     # Create Task
#     # ------------------------------------
#     def add_task_to_project(self, project_name, title, description, deadline):
#         with SessionLocal() as db:

#             project = self.project_repo.get_by_name(db, project_name)
#             if not project:
#                 raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#             existing = self.task_repo.get_task_by_title(db, project.id, title)
#             if existing:
#                 raise TaskValidationError(f"Task '{title}' already exists in this project.")

#             self._validate_deadline(deadline)

#             task = self.task_repo.create(
#                 db,
#                 title=title,
#                 description=description,
#                 deadline=deadline,
#                 status="todo",
#                 project_id=project.id
#             )

#             return {
#                 "message": "Task created successfully",
#                 "task": task
#             }

#     # ------------------------------------
#     # Edit Task
#     # ------------------------------------
#     def edit_task(self, project_name, task_title,
#                   new_title=None, new_desc=None, new_deadline=None, new_status=None):

#         with SessionLocal() as db:

#             project = self.project_repo.get_by_name(db, project_name)
#             if not project:
#                 raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#             task = self.task_repo.get_task_by_title(db, project.id, task_title)
#             if not task:
#                 raise TaskNotFoundException(f"Task '{task_title}' not found.")

#             if new_title:
#                 duplicate = self.task_repo.get_task_by_title(db, project.id, new_title)
#                 if duplicate and duplicate.id != task.id:
#                     raise TaskValidationError(
#                         f"Another task with title '{new_title}' already exists."
#                     )
#                 task.title = new_title

#             if new_desc:
#                 task.description = new_desc

#             if new_deadline:
#                 self._validate_deadline(new_deadline)
#                 task.deadline = new_deadline

#             if new_status:
#                 self._validate_status(new_status)
#                 task.status = new_status

#             updated = self.task_repo.update(db, task)

#             return {
#                 "message": "Task updated successfully",
#                 "task": updated
#             }

#     # ------------------------------------
#     # Update Only Status
#     # ------------------------------------
#     def update_status(self, project_name, task_title, new_status):
#         with SessionLocal() as db:

#             project = self.project_repo.get_by_name(db, project_name)
#             if not project:
#                 raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#             task = self.task_repo.get_task_by_title(db, project.id, task_title)
#             if not task:
#                 raise TaskNotFoundException(f"Task '{task_title}' not found.")

#             self._validate_status(new_status)
#             task.status = new_status

#             updated = self.task_repo.update(db, task)

#             return {
#                 "message": "Status updated",
#                 "task": updated
#             }

#     # ------------------------------------
#     # Delete Task
#     # ------------------------------------
#     def delete_task(self, project_name, task_title):
#         with SessionLocal() as db:

#             project = self.project_repo.get_by_name(db, project_name)
#             if not project:
#                 raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#             task = self.task_repo.get_task_by_title(db, project.id, task_title)
#             if not task:
#                 raise TaskNotFoundException(f"Task '{task_title}' not found.")

#             self.task_repo.delete(db, task)

#             return {"message": "Task deleted successfully"}

#     # ------------------------------------
#     # PRIVATE VALIDATIONS
#     # ------------------------------------
#     def _validate_deadline(self, date_str):
#         try:
#             datetime.strptime(date_str, "%Y-%m-%d")
#         except ValueError:
#             raise TaskValidationError("Deadline must be YYYY-MM-DD")

#     def _validate_status(self, status):
#         if status not in self.VALID_STATUSES:
#             raise TaskValidationError(
#                 f"Invalid status. Choose one of: {', '.join(self.VALID_STATUSES)}"
#             )

#     # ------------------------------------
#     # AUTO-CLOSE OVERDUE TASKS
#     # ------------------------------------
#     def autoclose_overdue_tasks(self):
#         with SessionLocal() as db:
#             today = datetime.now().date()

#             overdue_tasks = (
#                 db.query(self.task_repo.model)
#                 .filter(self.task_repo.model.deadline < today)
#                 .filter(self.task_repo.model.status != "done")
#                 .all()
#             )

#             for task in overdue_tasks:
#                 task.status = "done"

#             db.commit()
#             return len(overdue_tasks)
    
#     def api_get_task(self, task_id: int):
#         return self.repo.get_by_id(task_id)
# from datetime import datetime
# from repositories.project_repository import ProjectRepository
# from repositories.task_repository import TaskRepository
# from db.session import SessionLocal

# from exceptions.service_exceptions import (
#     ProjectNotFoundException,
#     TaskNotFoundException,
#     TaskValidationError
# )


# class TaskService:
#     VALID_STATUSES = ("todo", "doing", "done")

#     def __init__(self, db=None):
#         if db is None:
#             db = SessionLocal()

#         self.db = db
#         self.task_repo = TaskRepository(db)
#         self.project_repo = ProjectRepository(db)

#     # ======================================================
#     #                   VALIDATIONS
#     # ======================================================
#     def _validate_deadline(self, value):
#         # Accept both: "2025-12-30" (string) and datetime objects
#         if value is None:
#             return None

#         # If already datetime → valid
#         if isinstance(value, datetime):
#             return value

#         # If it's string → validate format
#         if isinstance(value, str):
#             try:
#                 return datetime.strptime(value, "%Y-%m-%d")
#             except ValueError:
#                 raise TaskValidationError("Deadline must be in YYYY-MM-DD format.")

#         # Otherwise → invalid
#         raise TaskValidationError("Invalid deadline type.")

#     def _validate_status(self, status):
#         if status not in self.VALID_STATUSES:
#             raise TaskValidationError(
#                 f"Invalid status. Choose: {', '.join(self.VALID_STATUSES)}"
#             )

#     # ======================================================
#     #                   CLI METHODS
#     # ======================================================
#     def add_task_to_project(self, project_name, title, description, deadline):
#         project = self.project_repo.get_by_name(project_name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#         existing = self.task_repo.get_task_by_title(project.id, title)
#         if existing:
#             raise TaskValidationError(f"Task '{title}' already exists in this project.")

#         deadline = self._validate_deadline(deadline)

#         task = self.task_repo.create(
#             title=title,
#             description=description,
#             deadline=deadline,
#             status="todo",
#             project_id=project.id
#         )

#         return {"message": "Task created successfully", "task": task}

#     def edit_task(self, project_name, task_title,
#                   new_title=None, new_desc=None, new_deadline=None, new_status=None):

#         project = self.project_repo.get_by_name(project_name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#         task = self.task_repo.get_task_by_title(project.id, task_title)
#         if not task:
#             raise TaskNotFoundException(f"Task '{task_title}' not found.")

#         if new_title:
#             duplicate = self.task_repo.get_task_by_title(project.id, new_title)
#             if duplicate and duplicate.id != task.id:
#                 raise TaskValidationError(
#                     f"Another task with title '{new_title}' already exists."
#                 )
#             task.title = new_title

#         if new_desc:
#             task.description = new_desc

#         if new_deadline:
#             task.deadline = self._validate_deadline(new_deadline)

#         if new_status:
#             self._validate_status(new_status)
#             task.status = new_status

#         updated = self.task_repo.update(task)
#         return {"message": "Task updated successfully", "task": updated}

#     def update_status(self, project_name, task_title, new_status):
#         project = self.project_repo.get_by_name(project_name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#         task = self.task_repo.get_task_by_title(project.id, task_title)
#         if not task:
#             raise TaskNotFoundException(f"Task '{task_title}' not found.")

#         self._validate_status(new_status)
#         task.status = new_status

#         updated = self.task_repo.update(task)
#         return {"message": "Status updated", "task": updated}

#     def delete_task(self, project_name, task_title):
#         project = self.project_repo.get_by_name(project_name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{project_name}' not found.")

#         task = self.task_repo.get_task_by_title(project.id, task_title)
#         if not task:
#             raise TaskNotFoundException(f"Task '{task_title}' not found.")

#         self.task_repo.delete(task)
#         return {"message": "Task deleted successfully"}

#     # ======================================================
#     #                   API METHODS
#     # ======================================================
#     def api_create_task(self, data):

#         project = self.project_repo.get_by_id(data.project_id)
#         if not project:
#             raise ProjectNotFoundException(f"Project id={data.project_id} not found.")

#         existing = self.task_repo.get_task_by_title(project.id, data.title)
#         if existing:
#             raise TaskValidationError(
#                 f"Task '{data.title}' already exists in this project."
#             )

#         # Parse deadline safely
#         deadline = self._validate_deadline(data.deadline)

#         task = self.task_repo.create(
#             title=data.title,
#             description=data.description,
#             deadline=deadline,
#             status=data.status or "todo",
#             project_id=data.project_id
#         )

#         return task

#     def api_get_task(self, task_id: int):
#         task = self.task_repo.get_by_id(task_id)
#         if not task:
#             raise TaskNotFoundException(f"Task id={task_id} not found.")
#         return task

#     def api_list_tasks(self):
#         return self.task_repo.get_all()

#     def api_update_task(self, task_id, data):

#         task = self.task_repo.get_by_id(task_id)
#         if not task:
#             raise TaskNotFoundException(f"Task id={task_id} not found.")

#         if data.title:
#             duplicate = self.task_repo.get_task_by_title(task.project_id, data.title)
#             if duplicate and duplicate.id != task.id:
#                 raise TaskValidationError(
#                     f"Another task with title '{data.title}' already exists."
#                 )
#             task.title = data.title

#         if data.description is not None:
#             task.description = data.description

#         if data.deadline is not None:
#             task.deadline = self._validate_deadline(data.deadline)

#         if data.status is not None:
#             self._validate_status(data.status)
#             task.status = data.status

#         return self.task_repo.update(task)

#     def api_delete_task(self, task_id):
#         task = self.task_repo.get_by_id(task_id)
#         if not task:
#             raise TaskNotFoundException(f"Task id={task_id} not found.")

#         self.task_repo.delete(task)
#         return True
from datetime import datetime
from db.session import SessionLocal

from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository

from exceptions.service_exceptions import (
    ProjectNotFoundException,
    TaskNotFoundException,
    TaskValidationError
)


class TaskService:
    VALID_STATUSES = ("todo", "doing", "done")

    def __init__(self, db=None):
        if db is None:
            db = SessionLocal()

        self.db = db
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    # ----------------------------------------------------
    # Validators
    # ----------------------------------------------------
    def _validate_deadline(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise TaskValidationError("Deadline must be YYYY-MM-DD format.")
        raise TaskValidationError("Invalid deadline type.")

    def _validate_status(self, status):
        if status not in self.VALID_STATUSES:
            raise TaskValidationError(
                f"Status must be one of: {', '.join(self.VALID_STATUSES)}"
            )

    # ----------------------------------------------------
    # Create
    # ----------------------------------------------------
    def add_task_to_project(self, project_name, title, description, deadline):
        project = self.project_repo.get_by_name(project_name)
        if not project:
            raise ProjectNotFoundException(f"Project '{project_name}' not found.")

        existing = self.task_repo.get_task_by_title(project.id, title)
        if existing:
            raise TaskValidationError(f"Task '{title}' already exists in this project.")

        deadline = self._validate_deadline(deadline)

        return self.task_repo.create(
            title=title,
            description=description,
            deadline=deadline,
            status="todo",
            project_id=project.id
        )

    # ----------------------------------------------------
    # Read
    # ----------------------------------------------------
    def list_tasks_of_project(self, project_name):
        project = self.project_repo.get_by_name(project_name)
        if not project:
            raise ProjectNotFoundException(f"Project '{project_name}' not found.")

        return self.task_repo.get_tasks_by_project_name(project_name)

    def get_task(self, project_name, task_title):
        task = self.task_repo.get_task_by_project_name_and_title(
            project_name, task_title
        )
        if not task:
            # could be project or task not found
            project = self.project_repo.get_by_name(project_name)
            if not project:
                raise ProjectNotFoundException(f"Project '{project_name}' not found.")
            raise TaskNotFoundException(f"Task '{task_title}' not found.")
        return task

    # ----------------------------------------------------
    # Update
    # ----------------------------------------------------
    def edit_task(self, project_name, task_title,
                  new_title=None, new_desc=None,
                  new_deadline=None, new_status=None):

        task = self.get_task(project_name, task_title)

        if new_title:
            duplicate = self.task_repo.get_task_by_title(task.project_id, new_title)
            if duplicate and duplicate.id != task.id:
                raise TaskValidationError(
                    f"Another task with title '{new_title}' already exists."
                )
            task.title = new_title

        if new_desc is not None:
            task.description = new_desc

        if new_deadline is not None:
            task.deadline = self._validate_deadline(new_deadline)

        if new_status:
            self._validate_status(new_status)
            task.status = new_status

        updated = self.task_repo.update(task)
        return updated

    # ----------------------------------------------------
    # Update only status
    # ----------------------------------------------------
    def update_status(self, project_name, task_title, new_status):
        task = self.get_task(project_name, task_title)

        self._validate_status(new_status)
        task.status = new_status

        return self.task_repo.update(task)

    # ----------------------------------------------------
    # Delete
    # ----------------------------------------------------
    def delete_task(self, project_name, task_title):
        task = self.get_task(project_name, task_title)
        self.task_repo.delete(task)
        return True
