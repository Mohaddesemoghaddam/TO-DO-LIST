from services.project_service import ProjectService
from services.task_service import TaskService


class Manager:
    def __init__(self):
        self.project_service = ProjectService()
        self.task_service = TaskService()

    # ---------------------------
    # PROJECTS
    # ---------------------------
    def add_project(self, name, description):
        result = self.project_service.create_project(name, description)
        print("[SUCCESS] Project created:", result.name)

    def show_all_projects(self):
        projects = self.project_service.get_all_projects()
        if not projects:
            print("[INFO] No projects found.")
            return

        print("\n=== Projects ===")
        for p in projects:
            print(f"- {p.name}: {p.description}")

    def edit_project(self, old_name, new_name, new_desc):
        updated = self.project_service.update_project(old_name, new_name, new_desc)
        print("[SUCCESS] Project updated:", updated.name)

    def delete_project(self, name):
        self.project_service.delete_project(name)
        print("[SUCCESS] Project deleted.")

    def show_tasks_of_project(self, project_name):
        tasks = self.project_service.get_tasks_of_project(project_name)
        if not tasks:
            print("[INFO] No tasks in this project.")
            return

        print(f"\n=== Tasks of {project_name} ===")
        for t in tasks:
            print(f"- {t.title} | {t.status} | {t.deadline}")

    # ---------------------------
    # TASKS
    # ---------------------------
    def add_task_to_project(self, project_name, title, description, deadline):
        result = self.task_service.add_task_to_project(
            project_name, title, description, deadline
        )
        print("[SUCCESS] Task created:", result["task"].title)

    def edit_task(self, project_name, task_title,
                  new_title, new_desc, new_deadline, new_status):

        result = self.task_service.edit_task(
            project_name, task_title,
            new_title, new_desc, new_deadline, new_status
        )
        print("[SUCCESS] Task updated:", result["task"].title)

    def update_task_status(self, project_name, task_title, new_status):
        result = self.task_service.update_status(project_name, task_title, new_status)
        print("[SUCCESS] Status updated:", result["task"].title)

    def delete_task_from_project(self, project_name, task_title):
        self.task_service.delete_task(project_name, task_title)
        print("[SUCCESS] Task deleted.")

