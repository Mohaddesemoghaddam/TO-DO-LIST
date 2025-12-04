from manager import Manager

def show_menu() -> str:
    """Display command-line menu and return user choice as string."""
    print("\n=== ToDoList CLI ===")
    print("1. Create Project")
    print("2. Show All Projects")
    print("3. Add Task to Project")
    print("4. Edit Project")
    print("5. Edit Task")
    print("6. Update Task Status")
    print("7. Delete Task")
    print("8. Delete Project")
    print("9. Show Tasks of a Project")
    print("10. Exit")

    return input("\nChoose an option (1–9): ").strip()

def main() -> None:
    """Main loop for CLI program."""
    manager: Manager = Manager()
    while True:
        choice: str = show_menu()

        try:
            if choice == "1":
                name: str = input("Enter project name: ").strip()
                description: str = input("Enter project description: ").strip()
                manager.add_project(name, description)

            elif choice == "2":
                manager.show_all_projects()

            elif choice == "3":
                project_name: str = input("Project name: ").strip()
                title: str = input("Task title: ").strip()
                description: str = input("Task description: ").strip()
                deadline: str = input("Deadline (YYYY-MM-DD): ").strip()
                manager.add_task_to_project(project_name, title, description, deadline)

            elif choice == "4":
                project_name: str = input("Project name to edit: ").strip()
                new_name: str | None = input("New project name (blank to skip): ").strip() or None
                new_desc: str | None = input("New project description (blank to skip): ").strip() or None
                manager.edit_project(project_name, new_name, new_desc)

            elif choice == "5":
                project_name: str = input("Project name: ").strip()
                task_title: str = input("Task title to edit: ").strip()
                new_title: str | None = input("New task title (blank to skip): ").strip() or None
                new_desc: str | None = input("New task description (blank to skip): ").strip() or None
                new_deadline: str | None = input("New task deadline (YYYY-MM-DD, blank to skip): ").strip() or None
                new_status: str | None = input("New task status (todo/doing/done, blank to skip): ").strip() or None
                manager.edit_task(project_name, task_title, new_title, new_desc, new_deadline, new_status)

            elif choice == "6":
                project_name: str = input("Project name: ").strip()
                task_title: str = input("Task title: ").strip()
                new_status: str = input("New status (todo/doing/done): ").strip()
                manager.update_task_status(project_name, task_title, new_status)

            elif choice == "7":
                project_name: str = input("Project name: ").strip()
                task_title: str = input("Task title to delete: ").strip()
                manager.delete_task_from_project(project_name, task_title)

            elif choice == "8":
                project_name: str = input("Project name to delete: ").strip()
                manager.delete_project(project_name)

            elif choice == "9":
                project_name: str = input("Enter project name: ").strip()
                manager.show_tasks_of_project(project_name)

            elif choice == "10":
                print("👋 Exiting. Goodbye!")
                break

            else:
                print("[ERROR] Invalid choice! Enter a number 1–9.")

        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    print("WARNING: This CLI is deprecated and will be removed in the next phase. Please use the FastAPI-based web API instead.")
    main()
