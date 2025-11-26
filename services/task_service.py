from sqlalchemy.orm import Session
from datetime import datetime

from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository
from db.session import SessionLocal

from exceptions.service_exceptions import (
    ProjectNotFoundException,
    TaskAlreadyExistsException,
    TaskNotFoundException,
    InvalidStatusException,
    InvalidDeadlineException
)


class TaskService:
    VALID_STATUSES = ("todo", "doing", "done")

    def __init__(self):
        self.project_repo = ProjectRepository()
        self.task_repo = TaskRepository()

    # ------------------------------------
    # Create Task
    # ------------------------------------
    def add_task_to_project(self, project_name, title, description, deadline):
        with SessionLocal() as db:

            # Check project exists
            project = self.project_repo.get_by_name(db, project_name)
            if not project:
                raise ProjectNotFoundException(f"Project '{project_name}' not found.")

            # Check duplicate task title in this project
            existing = self.task_repo.get_task_by_title(db, project.id, title)
            if existing:
                raise TaskAlreadyExistsException(f"Task '{title}' already exists in this project.")

            # Validate deadline
            self._validate_deadline(deadline)

            # Create
            task = self.task_repo.create(
                db,
                title=title,
                description=description,
                deadline=deadline,
                status="todo",
                project_id=project.id
            )

            return {
                "message": "Task created successfully",
                "task": task
            }

    # ------------------------------------
    # Edit Task (any field)
    # ------------------------------------
    def edit_task(self, project_name, task_title,
                  new_title=None, new_desc=None, new_deadline=None, new_status=None):

        with SessionLocal() as db:
            # Validate project
            project = self.project_repo.get_by_name(db, project_name)
            if not project:
                raise ProjectNotFoundException(f"Project '{project_name}' not found.")

            task = self.task_repo.get_task_by_title(db, project.id, task_title)
            if not task:
                raise TaskNotFoundException(f"Task '{task_title}' not found.")

            # title
            if new_title:
                duplicate = self.task_repo.get_task_by_title(db, project.id, new_title)
                if duplicate and duplicate.id != task.id:
                    raise TaskAlreadyExistsException(
                        f"Another task with title '{new_title}' already exists."
                    )
                task.title = new_title

            # description
            if new_desc:
                task.description = new_desc

            # deadline
            if new_deadline:
                self._validate_deadline(new_deadline)
                task.deadline = new_deadline

            # status
            if new_status:
                self._validate_status(new_status)
                task.status = new_status

            updated = self.task_repo.update(db, task)

            return {
                "message": "Task updated successfully",
                "task": updated
            }

    # ------------------------------------
    # Update Only Status
    # ------------------------------------
    def update_status(self, project_name, task_title, new_status):
        with SessionLocal() as db:
            project = self.project_repo.get_by_name(db, project_name)
            if not project:
                raise ProjectNotFoundException(f"Project '{project_name}' not found.")

            task = self.task_repo.get_task_by_title(db, project.id, task_title)
            if not task:
                raise TaskNotFoundException(f"Task '{task_title}' not found.")

            self._validate_status(new_status)
            task.status = new_status

            updated = self.task_repo.update(db, task)

            return {
                "message": "Status updated",
                "task": updated
            }

    # ------------------------------------
    # Delete Task
    # ------------------------------------
    def delete_task(self, project_name, task_title):
        with SessionLocal() as db:
            project = self.project_repo.get_by_name(db, project_name)
            if not project:
                raise ProjectNotFoundException(f"Project '{project_name}' not found.")

            task = self.task_repo.get_task_by_title(db, project.id, task_title)
            if not task:
                raise TaskNotFoundException(f"Task '{task_title}' not found.")

            self.task_repo.delete(db, task)

            return {"message": "Task deleted successfully"}

    # ------------------------------------
    # PRIVATE VALIDATIONS
    # ------------------------------------
    def _validate_deadline(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise InvalidDeadlineException("Deadline must be in format YYYY-MM-DD")

    def _validate_status(self, status):
        if status not in self.VALID_STATUSES:
            raise InvalidStatusException(
                f"Invalid status. Choose one of: {', '.join(self.VALID_STATUSES)}"
            )
    
        # ------------------------------------
    # AUTO-CLOSE OVERDUE TASKS (Scheduled)
    # ------------------------------------
    def autoclose_overdue_tasks(self):
        """
        Close all tasks where:
        - deadline < today
        - status != 'done'
        Returns: number of closed tasks
        """
        with SessionLocal() as db:
            today = datetime.now().date()

            # پیدا کردن تسک‌های دیرکرددار
            overdue_tasks = (
                db.query(self.task_repo.model)
                .filter(self.task_repo.model.deadline < today)
                .filter(self.task_repo.model.status != "done")
                .all()
            )

            # بستن آنها
            for task in overdue_tasks:
                task.status = "done"

            db.commit()

            return len(overdue_tasks)
