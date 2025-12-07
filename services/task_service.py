from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository
from exceptions.service_exceptions import (
    ProjectNotFoundException,
    TaskNotFoundException,
    TaskValidationError
)
from datetime import datetime
from models.task import Task

class TaskService:
    def __init__(self, db):
        self.db = db
        self.task_repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)

    # ----------------------------------------------------
    # UTIL – Get Task (with 404 rules)
    # ----------------------------------------------------
    def _get_task_or_404(self, project_name: str, task_title: str):
        task = self.task_repo.get_task_by_project_name_and_title(project_name, task_title)
        if task:
            return task

        project = self.project_repo.get_by_name(project_name)
        if not project:
            raise ProjectNotFoundException(f"Project '{project_name}' not found.")

        raise TaskNotFoundException(f"Task '{task_title}' not found.")

    # ----------------------------------------------------
    # CREATE (POST)
    # ----------------------------------------------------
    def create_task(self, project_name: str, data):
        project = self.project_repo.get_by_name(project_name)
        if not project:
            raise ProjectNotFoundException(f"Project '{project_name}' not found.")

        # check duplicate title
        existing = self.task_repo.get_task_by_title(project.id, data.title)
        if existing:
            raise TaskValidationError(f"Task '{data.title}' already exists in this project.")

        return self.task_repo.create(
            title=data.title,
            description=data.description,
            deadline=data.deadline,    # already datetime from schema
            status=data.status,        # schema validated
            project_id=project.id
        )

    # ----------------------------------------------------
    # READ
    # ----------------------------------------------------
    def list_tasks(self, project_name: str):
        project = self.project_repo.get_by_name(project_name)
        if not project:
            raise ProjectNotFoundException(f"Project '{project_name}' not found.")
        return self.task_repo.get_tasks_by_project_name(project_name)

    def get_task(self, project_name: str, task_title: str):
        return self._get_task_or_404(project_name, task_title)

    # # ----------------------------------------------------
    # # PUT – Full Replace
    # # ----------------------------------------------------
    # def replace_task(self, project_name: str, task_title: str, data):
    #     task = self._get_task_or_404(project_name, task_title)

    #     # If title changes → check duplicate
    #     if data.title is not None and data.title != task.title:
    #         duplicate = self.task_repo.get_task_by_title(task.project_id, data.title)
    #         if duplicate:
    #             raise TaskValidationError(
    #                 f"Task '{data.title}' already exists in this project."
    #             )

    #     task.title = data.title
    #     task.description = data.description
    #     task.status = data.status
    #     task.deadline = data.deadline

    #     return self.task_repo.update(task)

    # ----------------------------------------------------
    # PATCH – Partial Update
    # ----------------------------------------------------
    def update_task(self, project_name: str, task_title: str, data):
        task = self._get_task_or_404(project_name, task_title)

        # TITLE
        if data.title is not None:
            if data.title != task.title:
                duplicate = self.task_repo.get_task_by_title(task.project_id, data.title)
                if duplicate:
                    raise TaskValidationError(
                        f"Task '{data.title}' already exists in this project."
                    )
            task.title = data.title

        # DESCRIPTION
        if data.description is not None:
            task.description = data.description

        # STATUS
        if data.status is not None:
            task.status = data.status

        # DEADLINE
        if data.deadline is not None:
            task.deadline = data.deadline

        return self.task_repo.update(task)

    # ----------------------------------------------------
    # PATCH – STATUS ONLY
    # ----------------------------------------------------
    def update_status(self, project_name: str, task_title: str, new_status: str):
        task = self._get_task_or_404(project_name, task_title)
        task.status = new_status
        return self.task_repo.update(task)

    # ----------------------------------------------------
    # DELETE
    # ----------------------------------------------------
    def delete_task(self, project_name: str, task_title: str):
        task = self._get_task_or_404(project_name, task_title)
        self.task_repo.delete(task)
        return True
    # ----------------------------------------------------
    # CLOSE LATE TASKS
    # ----------------------------------------------------
    def close_late_tasks(self):
        now = datetime.utcnow()

        late_tasks = (
            self.db.query(Task)
            .filter(Task.deadline < now)
            .filter(Task.status != "done")
            .all()
        )

        for task in late_tasks:
            task.status = "done"

        self.db.commit()

        return len(late_tasks)

